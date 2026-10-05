"""Command line: luthier check | test | eval."""
from __future__ import annotations
import argparse
import importlib
import json
import os
import random
import sys

from .parser import parse, parse_term, ParseError
from .lexer import LexError
from .checker import Checker, TypeCheckError
from .evaluator import Env, EvalError, evaluate
from .generators import Generators
from .testing import run_test
from .certify import (cert_path, read_certificate, write_certificate, definition_hash, entries_of,
                      fingerprint, hash_of, why_different, generator_fingerprint)
from .pretty import pp

PACKAGE_DIR = os.path.dirname(__file__)
CORE = os.path.join(PACKAGE_DIR, "core.lut")          # loaded implicitly
LIB_DIR = os.path.join(PACKAGE_DIR, "lib")            # `import "algebra"`, `import "random"`, ...
PRELUDE = CORE  # old name


def search_dirs(importer: str) -> list:
    dirs = [os.path.dirname(os.path.abspath(importer))]
    for d in os.environ.get("LUTHIER_PATH", "").split(os.pathsep):
        if d:
            dirs.append(d)
    dirs.append(LIB_DIR)
    dirs.append(PACKAGE_DIR)   # `import "core"` when running with --no-core
    return dirs


def resolve_import(path: str, importer: str) -> str:
    """`import "x"`: next to the importing file, then LUTHIER_PATH, then the base library. `.lut` optional."""
    for base in search_dirs(importer):
        for name in (path, path + ".lut"):
            c = os.path.join(base, name)
            if os.path.isfile(c):
                return os.path.abspath(c)
    raise SystemExit(f"{importer}: cannot find import {path!r}")


def qualify(prefix: str, name: str) -> str:
    return f"{prefix}.{name}" if prefix else name


def derive_seed(run_seed: int, name: str) -> int:
    """Each definition gets its own seed, derived from the run's, so one number repeats the run."""
    import hashlib
    h = hashlib.sha256(f"{run_seed}:{name}".encode()).digest()
    return int.from_bytes(h[:4], "big") % (2 ** 31)


class Loader:
    """Loads files with their imports. A file imported `as m` is loaded under prefix `m`;
    the same file may be loaded under several prefixes (once each)."""

    def __init__(self, checker: Checker):
        self.checker = checker
        self.loaded: set = set()          # (path, prefix)
        self.stack: list = []             # paths being loaded, for cycles
        self.programs: list = []          # (prog, prefix, top, path)
        self.tests: list = []             # (qualified name, n, exhaustive, top)
        self.origin: dict = {}            # qualified name -> (path, prefix, name in file)
        self.stale: list = []             # qualified names whose certificate no longer matches
        self.stale_why: dict = {}         # qualified name -> why its certificate is not trusted
        self.known: dict = {}             # qualified name -> its matching entry, when that test did not pass
        self.cert_files: list = []        # (path, prefix) in load order, accepted once all is loaded

    def load_file(self, path: str, prefix: str = "", top: bool = False):
        path = os.path.abspath(path)
        key = (path, prefix)
        if key in self.loaded:
            return
        if path in self.stack:
            cycle = " -> ".join(os.path.basename(p) for p in self.stack + [path])
            raise SystemExit(f"import cycle: {cycle}")
        self.stack.append(path)
        with open(path, encoding="utf-8") as f:
            src = f.read()
        try:
            prog = parse(src)
        except (ParseError, LexError) as e:
            raise SystemExit(f"{path}: parse error: {e}")
        for imp in prog.imports:
            child = prefix if imp.alias is None else qualify(prefix, imp.alias)
            self.load_file(resolve_import(imp.path, path), child)
        saved = self.checker.prefix
        saved_kernel = self.checker.kernel
        self.checker.prefix = prefix
        self.checker.kernel = os.path.abspath(path) == os.path.abspath(CORE)
        saved_library = self.checker.library
        self.checker.library = os.path.abspath(path).startswith(os.path.abspath(PACKAGE_DIR) + os.sep)
        try:
            self.checker.load(prog)
        except TypeCheckError as e:
            raise SystemExit(f"{path}: type error: {e}")
        except EvalError as e:
            raise SystemExit(f"{path}: evaluation error while checking: {e}")
        finally:
            self.checker.prefix = saved
            self.checker.kernel = saved_kernel
            self.checker.library = saved_library
        for d in prog.defs:
            self.origin[qualify(prefix, d.name)] = (path, prefix, d.name)
        for t in prog.tests:
            self.tests.append((qualify(prefix, t.name), t.n, t.exhaustive, t.size, top))
        self.cert_files.append((path, prefix))
        self.stack.pop()
        self.loaded.add(key)
        self.programs.append((prog, prefix, top, path))

    def accept_certificates(self):
        """Trust the certificates of every loaded file, once the whole program is loaded and every
        hole it fills is filled (05 §7): an entry is trusted when its hash matches the definition's
        fingerprint now, its generators are unchanged, and it ran at least the cases its directive
        asks for. A certificate keeps an entry per filling of the holes; the one that matches is
        this program's."""
        directives = {}
        for q, n, ex, sz, top in self.tests:
            directives[q] = (n, ex)
        env = self.checker.env
        for path, prefix in self.cert_files:
            cert = read_certificate(cert_path(path))
            for name, value in cert.items():
                q = qualify(prefix, name)
                if q not in self.checker.obligations or q in self.checker.certified:
                    continue
                entries = entries_of(value)
                if not entries:
                    continue
                fp = fingerprint(env, q, prefix)
                h = hash_of(fp)
                match = next((e for e in entries if e.get("hash") == h), None)
                if match is None:
                    self._stale(q, why_different(entries[0].get("fingerprint", {}), fp))
                    continue
                why = self._unacceptable(match, directives.get(q))
                if why is not None:
                    self._stale(q, why)
                    continue
                outcome = match.get("outcome") or ("passed" if match.get("passed") else "failed")
                if outcome == "passed" and match.get("provisional"):
                    self.known[q] = dict(match, outcome="passed over provisional externs "
                                                       + ", ".join(match["provisional"]) + ", not certified")
                elif outcome == "passed":
                    self.checker.certified[q] = match
                else:
                    self.known[q] = match

    def _stale(self, q: str, why: str):
        if q not in self.stale:
            self.stale.append(q)
        self.stale_why[q] = why

    def _unacceptable(self, entry: dict, directive) -> str:
        for key, fpg in (entry.get("generators") or {}).items():
            if generator_fingerprint(self.checker, key) != fpg:
                return f"the generator {key} changed"
        if directive is not None:
            n, exhaustive = directive
            if exhaustive and entry.get("mode") != "exhaustive":
                return "its directive asks for an exhaustive test"
            if not exhaustive and entry.get("n", 0) < n:
                return f"it ran {entry.get('n', 0)} cases and its directive asks for {n}"
        return None

    def accept_certificate(self, path: str, prefix: str):
        """One file's certificates, as accept_certificates does for all."""
        saved = self.cert_files
        self.cert_files = [(path, prefix)]
        try:
            self.accept_certificates()
        finally:
            self.cert_files = saved

    def top_programs(self):
        return [(p, pre, path) for p, pre, top, path in self.programs if top]


def load(paths: list, with_core: bool = True) -> Loader:
    checker = Checker(Env())
    loader = Loader(checker)
    if with_core:
        loader.load_file(CORE)
    for path in paths:
        loader.load_file(path, top=True)
    loader.accept_certificates()
    return loader


def make_generators(loader: Loader, size: int = 16) -> Generators:
    return Generators.from_checker(loader.checker, size)


def cmd_check(args):
    loader = load(args.files, not args.no_core)
    ck = loader.checker
    n_defs = sum(len(p.defs) for p, _, _ in loader.top_programs())
    package = os.path.abspath(PACKAGE_DIR)

    def shown(q):   # the shipped libraries' own certified laws are not the user's business
        path = loader.origin.get(q, ("",))[0]
        return not (path.startswith(package) and q in ck.certified)
    obligations = {q: o for q, o in ck.obligations.items() if shown(q)}
    certified = [q for q in obligations if q in ck.certified]
    pending = [q for q in obligations if q not in ck.certified]
    print(f"ok: {n_defs} definitions, {len(obligations)} with laws, "
          f"{len(certified)} certified, {len(pending)} pending test"
          + (f", {len(ck.provisional)} provisional" if ck.provisional else ""))
    if args.verbose and ck.axioms:
        for q, desc in ck.axioms.items():
            print(f"  assumed {q}: {desc}; its laws are stated and never tested (06 §3)")
    if args.verbose and ck.provisional:
        for q, over in ck.provisional.items():
            what = f"builds on {', '.join(over)}" if over else "an extern type nobody has defined"
            print(f"  provisional {q}: {what}")
    if args.verbose:
        for q, obls in obligations.items():
            if q in ck.certified:
                status = f"certified ({ck.certified[q].get('when', '')})"
            elif q in loader.known:
                e = loader.known[q]
                status = f"{e.get('outcome') or 'failed'} in its last test ({e.get('when', '')})"
            elif q in loader.stale:
                status = f"stale certificate: {loader.stale_why.get(q, 'it no longer matches')}; needs test"
            else:
                status = "pending"
            path, prefix, _ = loader.origin.get(q, ("?", "", q))
            print(f"  {q}: {', '.join(o.label for o in obls)}  [{status}; {os.path.basename(path)}]")
    return 0


def cmd_test(args):
    loader = load(args.files, not args.no_core)
    ck = loader.checker
    if args.fuel is not None:
        ck.env.run_fuel = args.fuel
    gens = make_generators(loader, args.size)
    directives = []
    if args.name:
        # the file's own directive for that name gives its case count and mode, unless the
        # command line sets them
        own = [(q, n, ex, sz) for q, n, ex, sz, top in loader.tests
               if q == args.name or q.endswith("." + args.name)]
        if own:
            q, n, ex, sz = own[0]
            directives.append((q, args.n if args.n_given else n, ex or args.exhaustive, sz or args.size))
        else:
            directives.append((args.name, args.n, args.exhaustive, args.size))
    else:
        directives = [(q, args.n if args.n_given else n, ex or args.exhaustive, sz or args.size)
                      for q, n, ex, sz, top in loader.tests if top]
        if not directives:
            for prog, prefix, _ in loader.top_programs():
                for d in prog.defs:
                    q = qualify(prefix, d.name)
                    if q in ck.obligations:
                        directives.append((q, args.n, args.exhaustive, args.size))
    if args.imports:
        # 05 §7: a library with holes is certified per filling; this program is one, so the
        # imported obligations without a certificate for it are run here and written to their files
        own = {q: (n, ex, sz) for q, n, ex, sz, top in loader.tests}
        have = {q for q, _, _, _ in directives}
        for q in ck.obligations:
            if q in have or q in ck.certified:
                continue
            n, ex, sz = own.get(q, (args.n, args.exhaustive, args.size))
            directives.append((q, args.n if args.n_given else n, ex, sz))
            have.add(q)
    # 05 §7: `test n` runs the obligations of n and of every member of n's object
    seen = {q for q, _, _, _ in directives}
    for q, n, ex, sz in list(directives):
        for m in ck.object_of.get(q, []):
            if m not in seen and m in ck.obligations:
                directives.append((m, n, ex, sz))
                seen.add(m)
    reports = []
    ok = True
    run_seed = args.seed if args.seed is not None else random.randrange(2 ** 31)
    if any(not ex for _, _, ex, _ in directives):
        print(f"run seed {run_seed} (repeat with --seed {run_seed})")
    for name, n, exhaustive, size in directives:
        path, prefix, _ = loader.origin.get(name, (None, "", name))
        is_top = any(p == path for _, _, p in loader.top_programs())
        if args.show_cases:
            print(f"{name}:")
        r = run_test(ck, gens, name, n=n, exhaustive=exhaustive, seed=derive_seed(run_seed, name),
                     deep=args.deep or is_top, prefix=prefix, show_cases=args.show_cases, size=size)
        r.run_seed = run_seed
        print(r.summary())
        reports.append(r)
        ok = ok and r.passed
    tops = {p for _, _, p in loader.top_programs()}
    done = {r.definition for r in reports}
    by_file: dict = {}
    for q in ck.obligations:
        path = loader.origin.get(q, ("",))[0]
        if q in ck.certified or path in tops or q in done or not path:
            continue
        by_file.setdefault(path, []).append(q)
    for path, names in by_file.items():
        state = "stale certificate" if any(q in loader.stale for q in names) else "no certificate"
        rel = os.path.relpath(path)
        print(f"imported, {state}: {', '.join(names)}\n"
              f"  run `luthier test {rel}` to certify them, or add --imports to run them here")
    if reports and not args.no_cert:
        by_file: dict = {}
        for r in reports:
            if r.certified:
                continue
            path, prefix, local = loader.origin.get(r.definition, (None, "", r.definition))
            if path is None:
                continue
            by_file.setdefault(path, ([], {}))
            by_file[path][0].append(r)
            by_file[path][1][r.definition] = local
        for path, (rs, names) in by_file.items():
            keep = {local for q, (p, pre, local) in loader.origin.items() if p == path and q in ck.obligations}
            write_certificate(cert_path(path), rs, names, keep)
            print(f"certificate: {cert_path(path)}")
    return 0 if ok else 1


def _parse_setting(text: str):
    """`name=value`, split; the value stays text until the hole's declared type reads it."""
    name, sep, raw = text.partition("=")
    if not sep or not name:
        raise SystemExit(f"--set expects name=value, got {text!r}")
    return name.strip(), raw.strip()


def typed_setting(env, name: str, raw: str, ty):
    """The text of `--set name=raw` read by the declared type of the hole: an Int, a Float64, a
    String or a Bool, and nothing else. Reading by the type, not by how the text looks, keeps
    `--set dir=2026` a String and `--set sigma=3` a Float64 (06 §6)."""
    import math
    from .evaluator import scalar_kind, strip_subtypes, _sum_of
    kind = scalar_kind(env, ty)
    if kind == "String":
        return raw
    if kind == "Int":
        try:
            return int(raw)
        except ValueError:
            raise SystemExit(f"--set {name}={raw}: {name} is {pp(ty)}, and {raw!r} is not an integer")
    if kind in ("Float64", "Real"):
        try:
            x = float(raw)
        except ValueError:
            raise SystemExit(f"--set {name}={raw}: {name} is {pp(ty)}, and {raw!r} is not a number")
        if not math.isfinite(x):
            raise SystemExit(f"--set {name}={raw}: NaN and infinities are not values of {pp(ty)}")
        return x
    sm = _sum_of(env, ty)
    if sm is not None and sm.labels() == ["true", "false"]:
        if raw not in ("true", "false"):
            raise SystemExit(f"--set {name}={raw}: {name} is a Bool, give true or false")
        return raw == "true"
    raise SystemExit(f"--set {name}: {name} is {pp(ty)}; only holes of Int, Float64, String or Bool "
                     f"(or refinements of them) can be set from the command line")


def cmd_run(args):
    from .syntax import Pi
    """Evaluate a program's `main` (or --entry) after giving its parameter holes their values,
    and record the run: the hash of main's dependency cone, the parameters, the result."""
    import datetime
    from .api import Program
    from .certify import definition_hash, read_certificate
    loader = load(args.files, not args.no_core)
    ck = loader.checker
    if args.fuel is not None:
        ck.env.run_fuel = args.fuel
    prog = Program(loader)
    settings = {}
    for name, raw in (_parse_setting(x) for x in (args.set or [])):
        q = prog.resolve(name)
        d = ck.env.defs.get(q) if q is not None else None
        if d is None or d.body is not None or d.data is not None:
            raise SystemExit(f"--set {name}: not a hole of the program")
        if isinstance(ck.whnf(d.type), Pi):
            raise SystemExit(f"--set {name}: a function hole cannot be set from the command line")
        value = typed_setting(ck.env, name, raw, d.type)
        settings[name] = value
        try:
            prog.fill(name, (lambda v: (lambda: v))(value))
        except (TypeCheckError, EvalError) as e:
            raise SystemExit(f"--set {name}={raw}: {e}")
    entry = args.entry
    q = prog.resolve(entry)
    if q not in ck.env.defs:
        raise SystemExit(f"no definition {entry!r} to run")
    open_holes = [h for h in prog.holes() if h not in prog.filled]
    needed = [h for h in open_holes if h in set(cone_names(ck.env, q))]
    if needed:
        raise SystemExit(f"{entry} depends on holes without a value: {', '.join(needed)}; give them with --set name=value")
    path, prefix, local = loader.origin.get(q, (args.files[0], "", entry))
    cone_state = cone_states(loader, q)
    counts: dict = {}
    for state in cone_state.values():
        kind = state.split(":")[0].split(" (")[0]
        counts[kind] = counts.get(kind, 0) + 1
    shown = ", ".join(f"{k} {v}" for k, v in sorted(counts.items()))
    print(f"the cone of {entry}: {shown}")
    weak = {n: st for n, st in cone_state.items() if not st.startswith("certified")}
    if weak and args.require_certified:
        lines = "\n".join(f"  {n}: {st}" for n, st in sorted(weak.items()))
        raise SystemExit(f"--require-certified: {len(weak)} names of the cone of {entry} are not certified\n{lines}")
    started = datetime.datetime.now().isoformat(timespec="seconds")
    try:
        value = prog.eval(entry)
    except EvalError as e:
        raise SystemExit(f"error: {e}")
    record = {
        "entry": entry,
        "hash": definition_hash(ck.env, q, prefix),
        "when": started,
        "parameters": settings,
        "result": value if isinstance(value, (int, float, str, bool, type(None))) else pp(value) if hasattr(value, "__class__") and not isinstance(value, (list, dict)) else value,
        "fingerprint": fingerprint(ck.env, q, prefix),
        "luthier": luthier_revision(),
        "cone": {"counts": counts, "not certified": dict(sorted(weak.items()))},
    }
    if not args.no_record:
        rec_path = os.path.splitext(path)[0] + ".run.json"
        runs = read_certificate(rec_path)
        runs.setdefault("runs", []).append(record)
        with open(rec_path, "w", encoding="utf-8") as f:
            json.dump(runs, f, indent=2, ensure_ascii=False, default=str)
        print(f"run recorded: {rec_path}")
    if record["result"] is not None:
        print(record["result"])
    return 0


def cmd_certify(args):
    """Each file is tested by its own process (`luthier test file`), so the files of a project are
    certified at once and each writes only its own certificate; a file's line says how its
    definitions came out."""
    import subprocess
    import time
    from concurrent.futures import ThreadPoolExecutor

    def one(path):
        cmd = [sys.executable, "-m", "luthier.cli", "test", path] + (["--imports"] if args.imports else [])
        if args.seed is not None:
            cmd += ["--seed", str(args.seed)]
        t0 = time.time()
        r = subprocess.run(cmd, capture_output=True, text=True)
        verdicts = {}
        for line in r.stdout.splitlines():
            if line and not line.startswith(" ") and ": " in line and not line.startswith(("run seed", "certificate", "imported")):
                v = line.split(": ", 1)[1].split(" ")[0].split(",")[0]
                verdicts[v] = verdicts.get(v, 0) + 1
        err = r.stderr.strip().splitlines()[-1] if r.returncode not in (0, 1) and r.stderr.strip() else ""
        return path, r.returncode, verdicts, time.time() - t0, err, r.stdout
    ok = True
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        for path, code, verdicts, secs, err, out in pool.map(one, args.files):
            shown = ", ".join(f"{k} {v}" for k, v in sorted(verdicts.items())) or "nothing tested"
            print(f"{os.path.relpath(path)}: {shown}  ({secs:.0f} s)" + (f"\n  error: {err}" if err else ""))
            ok = ok and code == 0
    return 0 if ok else 1


def cone_states(loader: Loader, q: str) -> dict:
    """The state of every name with laws in the cone of q (05 §7): certified, failed or not run in
    its last test, stale (and why), pending, or provisional; and the axioms it rests on, assumed."""
    from .certify import cone
    ck = loader.checker
    out = {}
    for n in cone(ck.env, q):
        if n in ck.axioms:
            out[n] = "assumed (an axiom)"
        elif n in ck.provisional:
            out[n] = "provisional (an extern over a type nobody has defined)"
        elif n not in ck.obligations:
            continue
        elif n in ck.certified:
            out[n] = f"certified ({ck.certified[n].get('when', '')})"
        elif n in loader.known:
            out[n] = f"{loader.known[n].get('outcome') or 'failed'} ({loader.known[n].get('when', '')})"
        elif n in loader.stale:
            out[n] = f"stale: {loader.stale_why.get(n, 'it no longer matches')}"
        else:
            out[n] = "pending"
    return out


def luthier_revision() -> dict:
    """The commit of the interpreter's repository and whether its tree had changes, when it is a
    git checkout; with the fingerprint of its sources, which the certificates also use."""
    import subprocess
    from .certify import interpreter_fingerprint
    out = {"interpreter": interpreter_fingerprint()}
    try:
        head = subprocess.run(["git", "-C", PACKAGE_DIR, "rev-parse", "HEAD"], capture_output=True, text=True, timeout=10)
        dirty = subprocess.run(["git", "-C", PACKAGE_DIR, "status", "--porcelain", "--", "."], capture_output=True, text=True, timeout=10)
        if head.returncode == 0:
            out["commit"] = head.stdout.strip()
            out["changes"] = bool(dirty.stdout.strip())
    except (OSError, subprocess.SubprocessError):
        pass
    return out


def cone_names(env, q):
    from .certify import cone
    return cone(env, q)


def cmd_eval(args):
    loader = load(args.files, not args.no_core)
    ck = loader.checker
    if args.fuel is not None:
        ck.env.run_fuel = args.fuel
    try:
        t = parse_term(args.term)
        with ck.silent():
            t2, ty = ck.infer([], t)
        v = evaluate(ck.env, t2)
        print(f"{pp(v)} : {pp(ty)}")
    except (ParseError, LexError, TypeCheckError, EvalError) as e:
        raise SystemExit(f"error: {e}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="luthier", description="Luthier version 0")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("check", help="parse and type-check .lut files")
    p.add_argument("files", nargs="+")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("--no-core", action="store_true", help="do not load core.lut implicitly")
    p.set_defaults(fn=cmd_check)

    p = sub.add_parser("test", help="run the laws of a definition")
    p.add_argument("files", nargs="+")
    p.add_argument("--name", help="definition to test (default: the file's test directives)")
    p.add_argument("--n", type=int, default=100, help="sampled cases per law")
    p.add_argument("--exhaustive", action="store_true")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--size", type=int, default=16,
                   help="largest size of generated values (Int range, N magnitude, nesting); "
                        "grows from 1 to this over a sampled run; the Int range for exhaustive")
    p.add_argument("--deep", action="store_true", help="rerun even where a matching certificate exists")
    p.add_argument("--imports", action="store_true",
                   help="also run the imported obligations with no certificate for this program, and "
                        "write them to their own files' certificates")
    p.add_argument("--show-cases", action="store_true", help="print every case as it is evaluated")
    p.add_argument("--no-cert", action="store_true")
    p.add_argument("--fuel", type=int, default=None,
                   help="steps allowed per evaluation of a law case or term (default 2000000000)")
    p.add_argument("--no-core", action="store_true", help="do not load core.lut implicitly")
    p.set_defaults(fn=cmd_test)

    p = sub.add_parser("run", help="run a program: evaluate its main after setting its parameters")
    p.add_argument("files", nargs="+")
    p.add_argument("--entry", default="main", help="the definition to evaluate (default: main)")
    p.add_argument("--set", action="append", metavar="NAME=VALUE",
                   help="give a parameter hole its value; repeatable")
    p.add_argument("--fuel", type=int, default=None, help="steps allowed for the evaluation")
    p.add_argument("--no-record", action="store_true", help="do not append to the .run.json record")
    p.add_argument("--require-certified", action="store_true",
                   help="refuse to run unless every name with laws in the cone of the entry is certified")
    p.add_argument("--no-core", action="store_true", help="do not load core.lut implicitly")
    p.set_defaults(fn=cmd_run)

    p = sub.add_parser("certify", help="run the test directives of several files, each as its own "
                                       "`luthier test`, in parallel, and summarize")
    p.add_argument("files", nargs="+")
    p.add_argument("--jobs", type=int, default=os.cpu_count() or 1, help="files tested at once")
    p.add_argument("--seed", type=int, default=None, help="the run seed of every file")
    p.add_argument("--imports", action="store_true", help="pass --imports to every `luthier test`")
    p.set_defaults(fn=cmd_certify)

    p = sub.add_parser("eval", help="evaluate a term in the context of .lut files")
    p.add_argument("files", nargs="+")
    p.add_argument("term")
    p.add_argument("--fuel", type=int, default=None,
                   help="steps allowed per evaluation of a law case or term (default 2000000000)")
    p.add_argument("--no-core", action="store_true", help="do not load core.lut implicitly")
    p.set_defaults(fn=cmd_eval)

    args = ap.parse_args(argv)
    raw = argv if argv is not None else sys.argv[1:]
    args.n_given = any(a == "--n" or a.startswith("--n=") for a in raw)
    return run_deep(lambda: args.fn(args))


def run_deep(fn):
    """The evaluator is recursive and unary naturals are deep: give it a big stack."""
    import threading
    result = {}

    def target():
        try:
            sys.setrecursionlimit(200_000)
            result["value"] = fn()
        except BaseException as e:  # re-raised in the caller
            result["error"] = e
    threading.stack_size(512 * 1024 * 1024)
    th = threading.Thread(target=target)
    th.start()
    th.join()
    if "error" in result:
        raise result["error"]
    return result.get("value", 0)


if __name__ == "__main__":
    sys.exit(main())
