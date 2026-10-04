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
from .certify import cert_path, read_certificate, write_certificate, definition_hash
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
        self.checker.prefix = prefix
        try:
            self.checker.load(prog)
        except TypeCheckError as e:
            raise SystemExit(f"{path}: type error: {e}")
        except EvalError as e:
            raise SystemExit(f"{path}: evaluation error while checking: {e}")
        finally:
            self.checker.prefix = saved
        for d in prog.defs:
            self.origin[qualify(prefix, d.name)] = (path, prefix, d.name)
        for t in prog.tests:
            self.tests.append((qualify(prefix, t.name), t.n, t.exhaustive, t.size, top))
        self.accept_certificate(path, prefix)
        self.stack.pop()
        self.loaded.add(key)
        self.programs.append((prog, prefix, top, path))

    def accept_certificate(self, path: str, prefix: str):
        cert = read_certificate(cert_path(path))
        for name, entry in cert.items():
            q = qualify(prefix, name)
            if q not in self.checker.obligations:
                continue
            if entry.get("passed") and entry.get("hash") == definition_hash(self.checker.env, q, prefix):
                self.checker.certified[q] = entry
            else:
                self.stale.append(q)

    def top_programs(self):
        return [(p, pre, path) for p, pre, top, path in self.programs if top]


def load(paths: list, with_core: bool = True) -> Loader:
    checker = Checker(Env())
    loader = Loader(checker)
    if with_core:
        loader.load_file(CORE)
    for path in paths:
        loader.load_file(path, top=True)
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
          f"{len(certified)} certified, {len(pending)} pending test")
    if args.verbose:
        for q, obls in obligations.items():
            if q in ck.certified:
                status = f"certified ({ck.certified[q].get('when', '')})"
            elif q in loader.stale:
                status = "stale certificate, needs test"
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
              f"  run `luthier test {rel}` to certify them, or add --deep to run them here")
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
            write_certificate(cert_path(path), rs, names)
            print(f"certificate: {cert_path(path)}")
    return 0 if ok else 1


def _parse_setting(text: str):
    """`name=value`: an int, a float, a bool or a string, by what the text looks like."""
    name, sep, raw = text.partition("=")
    if not sep or not name:
        raise SystemExit(f"--set expects name=value, got {text!r}")
    raw = raw.strip()
    if raw in ("true", "false"):
        return name.strip(), raw == "true"
    try:
        return name.strip(), int(raw)
    except ValueError:
        pass
    try:
        return name.strip(), float(raw)
    except ValueError:
        return name.strip(), raw


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
    settings = dict(_parse_setting(x) for x in (args.set or []))
    for name, value in settings.items():
        q = prog.resolve(name)
        d = ck.env.defs.get(q)
        if d is None or d.body is not None or d.data is not None:
            raise SystemExit(f"--set {name}: not a hole of the program")
        if isinstance(ck.whnf(d.type), Pi):
            raise SystemExit(f"--set {name}: a function hole cannot be set from the command line")
        prog.fill(name, (lambda v: (lambda: v))(value))
    entry = args.entry
    q = prog.resolve(entry)
    if q not in ck.env.defs:
        raise SystemExit(f"no definition {entry!r} to run")
    open_holes = [h for h in prog.holes() if h not in prog.filled]
    needed = [h for h in open_holes if h in set(cone_names(ck.env, q))]
    if needed:
        raise SystemExit(f"{entry} depends on holes without a value: {', '.join(needed)}; give them with --set name=value")
    started = datetime.datetime.now().isoformat(timespec="seconds")
    try:
        value = prog.eval(entry)
    except EvalError as e:
        raise SystemExit(f"error: {e}")
    path, prefix, local = loader.origin.get(q, (args.files[0], "", entry))
    record = {
        "entry": entry,
        "hash": definition_hash(ck.env, q, prefix),
        "when": started,
        "parameters": settings,
        "result": value if isinstance(value, (int, float, str, bool, type(None))) else pp(value) if hasattr(value, "__class__") and not isinstance(value, (list, dict)) else value,
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
    p.add_argument("--show-cases", action="store_true", help="print every case as it is evaluated")
    p.add_argument("--no-cert", action="store_true")
    p.add_argument("--fuel", type=int, default=None,
                   help="steps allowed per evaluation of a law case or term (default 50000000)")
    p.add_argument("--no-core", action="store_true", help="do not load core.lut implicitly")
    p.set_defaults(fn=cmd_test)

    p = sub.add_parser("run", help="run a program: evaluate its main after setting its parameters")
    p.add_argument("files", nargs="+")
    p.add_argument("--entry", default="main", help="the definition to evaluate (default: main)")
    p.add_argument("--set", action="append", metavar="NAME=VALUE",
                   help="give a parameter hole its value; repeatable")
    p.add_argument("--fuel", type=int, default=None, help="steps allowed for the evaluation")
    p.add_argument("--no-record", action="store_true", help="do not append to the .run.json record")
    p.add_argument("--no-core", action="store_true", help="do not load core.lut implicitly")
    p.set_defaults(fn=cmd_run)

    p = sub.add_parser("eval", help="evaluate a term in the context of .lut files")
    p.add_argument("files", nargs="+")
    p.add_argument("term")
    p.add_argument("--fuel", type=int, default=None,
                   help="steps allowed per evaluation of a law case or term (default 50000000)")
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
