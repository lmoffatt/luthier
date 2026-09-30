"""Command line: luthier check | test | eval."""
from __future__ import annotations
import argparse
import importlib
import os
import sys

from .parser import parse, parse_term, ParseError
from .lexer import LexError
from .checker import Checker, TypeCheckError
from .evaluator import Env, EvalError, evaluate
from .generators import Generators
from .testing import run_test
from .certify import cert_path, read_certificate, write_certificate, definition_hash
from .pretty import pp

PRELUDE_DIR = os.path.dirname(__file__)
PRELUDE = os.path.join(PRELUDE_DIR, "prelude.lut")


def search_dirs(importer: str) -> list:
    dirs = [os.path.dirname(os.path.abspath(importer))]
    for d in os.environ.get("LUTHIER_PATH", "").split(os.pathsep):
        if d:
            dirs.append(d)
    dirs.append(PRELUDE_DIR)
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
            self.tests.append((qualify(prefix, t.name), t.n, t.exhaustive, top))
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


def load(paths: list, with_prelude: bool = True) -> Loader:
    checker = Checker(Env())
    loader = Loader(checker)
    if with_prelude:
        loader.load_file(PRELUDE)
    for path in paths:
        loader.load_file(path, top=True)
    return loader


def make_generators(loader: Loader, int_range) -> Generators:
    gens = Generators(loader.checker.env, int_range=int_range)
    for prog, prefix, _, _ in loader.programs:
        for g in prog.gens:
            spec = g.target.split(":", 1)[1] if g.target.startswith("python:") else g.target
            if ":" in spec:
                mod, attr = spec.split(":", 1)
            else:
                mod, _, attr = spec.rpartition(".")
            fn = importlib.import_module(mod)
            for part in attr.split("."):
                fn = getattr(fn, part)
            gens.register(qualify(prefix, g.type_name), fn)
    return gens


def cmd_check(args):
    loader = load(args.files, not args.no_prelude)
    ck = loader.checker
    n_defs = sum(len(p.defs) for p, _, _ in loader.top_programs())
    pending = [q for q in ck.obligations if q not in ck.certified]
    print(f"ok: {n_defs} definitions, {len(ck.obligations)} with laws, "
          f"{len(ck.certified)} certified, {len(pending)} pending test")
    if args.verbose:
        for q, obls in ck.obligations.items():
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
    loader = load(args.files, not args.no_prelude)
    ck = loader.checker
    gens = make_generators(loader, (args.int_min, args.int_max))
    directives = []
    if args.name:
        directives.append((args.name, args.n, args.exhaustive))
    else:
        directives = [(q, args.n if args.n_given else n, ex or args.exhaustive)
                      for q, n, ex, top in loader.tests if top]
        if not directives:
            for prog, prefix, _ in loader.top_programs():
                for d in prog.defs:
                    q = qualify(prefix, d.name)
                    if q in ck.obligations:
                        directives.append((q, args.n, args.exhaustive))
    reports = []
    ok = True
    for name, n, exhaustive in directives:
        path, prefix, _ = loader.origin.get(name, (None, "", name))
        is_top = any(p == path for _, _, p in loader.top_programs())
        r = run_test(ck, gens, name, n=n, exhaustive=exhaustive, seed=args.seed,
                     deep=args.deep or is_top, prefix=prefix)
        print(r.summary())
        reports.append(r)
        ok = ok and r.passed
    imported_pending = [q for q in ck.obligations
                        if q not in ck.certified and loader.origin.get(q, ("",))[0] not in
                        {p for _, _, p in loader.top_programs()} and q not in {r.definition for r in reports}]
    if imported_pending:
        print("pending in imported files (run `luthier test` on them, or --deep): " + ", ".join(imported_pending))
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


def cmd_eval(args):
    loader = load(args.files, not args.no_prelude)
    ck = loader.checker
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
    p.add_argument("--no-prelude", action="store_true", help="do not load the base library implicitly")
    p.set_defaults(fn=cmd_check)

    p = sub.add_parser("test", help="run the laws of a definition")
    p.add_argument("files", nargs="+")
    p.add_argument("--name", help="definition to test (default: the file's test directives)")
    p.add_argument("--n", type=int, default=100, help="sampled cases per law")
    p.add_argument("--exhaustive", action="store_true")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--int-min", type=int, default=-16)
    p.add_argument("--int-max", type=int, default=16)
    p.add_argument("--deep", action="store_true", help="rerun even where a matching certificate exists")
    p.add_argument("--no-cert", action="store_true")
    p.add_argument("--no-prelude", action="store_true", help="do not load the base library implicitly")
    p.set_defaults(fn=cmd_test)

    p = sub.add_parser("eval", help="evaluate a term in the context of .lut files")
    p.add_argument("files", nargs="+")
    p.add_argument("term")
    p.add_argument("--no-prelude", action="store_true", help="do not load the base library implicitly")
    p.set_defaults(fn=cmd_eval)

    args = ap.parse_args(argv)
    raw = argv if argv is not None else sys.argv[1:]
    args.n_given = any(a == "--n" or a.startswith("--n=") for a in raw)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
