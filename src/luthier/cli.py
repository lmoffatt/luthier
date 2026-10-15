"""Command line interface for the bootstrap Luthier parser."""

from __future__ import annotations

import argparse
from pathlib import Path

from .parse import parse
from .surface import ParseFailed, Parsed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="luthier")
    sub = parser.add_subparsers(dest="command", required=True)
    p_parse = sub.add_parser("parse", help="parse Luthier source files")
    p_parse.add_argument("--tree", action="store_true", help="print each parsed act")
    p_parse.add_argument("files", nargs="+")
    p_check = sub.add_parser("check", help="check static semantics")
    p_check.add_argument("-v", "--verbose", action="store_true")
    p_check.add_argument("files", nargs="+")
    p_eval = sub.add_parser("eval", help="evaluate a term in the context of the files, their imports and "
                                          "core, printing its value, its type and the states of its cone; "
                                          "records nothing, demands no certificate (12.S19)")
    p_eval.add_argument("files", nargs="+")
    p_eval.add_argument("term", help="a term, as it would be written in the files (a name, an application, ...)")
    p_eval.add_argument("--fuel", type=int, default=None, help="reduction fuel [default the demand's, as run's]")
    p_session = sub.add_parser("session", help="read one item of a block per line from standard input over the "
                                                "files, their imports and core: `x := t`, `x <- t`, a term "
                                                "printed with its type and its cone's states; `:items`, "
                                                "`:quit`; records nothing (12.S20, 2.S18)")
    p_session.add_argument("files", nargs="*")
    p_session.add_argument("--fuel", type=int, default=None, help="reduction fuel per line [default the demand's, as run's]")
    p_session.add_argument("--world", action="store_true",
                           help="[proposed] the session block takes the world as `w`, and its actions run with "
                                "the run's token, validated at their first action as run validates them (10.S10); "
                                "without it the session has no world and acts on nothing")
    p_run = sub.add_parser("run", help="run a program with the host world")
    p_run.add_argument("file")
    # the defaults of `run`'s arguments are the demand's, declared in lib/demand_model.lut's
    # `theDemand` and mirrored in run.DEMAND_DEFAULTS (L5.19, P11): None here means "not given"
    p_run.add_argument("--main", default=None, help="the entry [default main]")
    p_run.add_argument("--fuel", type=int, default=None,
                       help="reduction fuel [proposed: default 10,000,000, 10,000 was a hundred times too small for validate_graph.lut]")
    p_run.add_argument("--set", action="append", default=[], metavar="NAME=VALUE",
                       help="give a hole of the file (a declared String, Int, Float64 or Bool) its value (12.S18)")
    p_run.add_argument("--accept", choices=["proved", "exhaustive", "cases", "sampled", "assumed"], default=None,
                       help="the weakest grade an entry of the store may have to serve the run (6.S15, 7.S15) "
                            "[proposed: sampled when none is named, so an assumed entry serves only a run "
                            "that accepts assumed]; the run is refused when its cone is not certified (12.S17)")
    p_run.add_argument("--checked", action="store_true", default=None,
                       help="test each value an extern gives at a declared subtype against its predicate as "
                            "it crosses, refusing the run at the first refuted one (12.S18, 4.R5); off by "
                            "default, a parameter of the demand (P11): without it the refinement is an "
                            "obligation the certificate of the extern's laws covers")
    p_run.add_argument("--fresh", action="store_true",
                       help="execute even when x.results.json holds this run's key (L5.20); nothing is written "
                            "if the value agrees, and both are kept if it does not")
    p_test = sub.add_parser("test", help="run the file's test lines (test.lth's Tester)")
    p_test.add_argument("file")
    p_test.add_argument("--seed", type=int, default=None, help="the seed of every test, in place of each line's")
    p_test.add_argument("--fuel", type=int, default=1_000_000,
                        help="reduction fuel per case [proposed: default 1,000,000]")
    p_test.add_argument("--deep", action="store_true", help="run again a line whose outcome the store knows (7.S13)")
    p_test.add_argument("--no-cert", action="store_true", help="neither read nor write the store x.cert.json (12.S15)")
    p_cert = sub.add_parser("certify", help="run the test lines of several files, each in its own process (12.S16)")
    p_cert.add_argument("files", nargs="+")
    p_cert.add_argument("--prune", action="store_true",
                        help="rewrite the stores of FILES (x.cert.json) bounded (6.S8), running nothing")
    p_cert.add_argument("--jobs", type=int, default=1, help="files run at a time")
    p_cert.add_argument("--seed", type=int, default=None, help="the seed of every test, in place of each line's")
    p_cert.add_argument("--deep", action="store_true", help="run again the lines whose outcome a store knows")
    p_cert.add_argument("--fuel", type=int, default=1_000_000, help="reduction fuel per case")
    p_cert.add_argument("--no-cert", action="store_true",
                        help="neither read nor write the stores x.cert.json: run every line and report")
    ns = parser.parse_args(argv)

    if ns.command == "certify" and ns.prune:
        from .certify import prune_stores
        return prune_stores(ns.files)

    if ns.command == "certify":
        from .certify import certify
        return 0 if certify(ns.files, ns.jobs, ns.seed, ns.deep, ns.fuel, store=not ns.no_cert) else 1

    if ns.command == "test":
        from .tester import line, passes, run_tests
        try:
            outcomes = run_tests(ns.file, ns.seed, ns.fuel, deep=ns.deep, store=not ns.no_cert)
        except (OSError, ValueError, RecursionError) as exc:
            import sys
            print(f"{ns.file}: {exc}", file=sys.stderr)
            return 1
        for outcome in outcomes:
            print(line(outcome))
        # a law line passes with a grade, a control line when its law is refuted (7.S19)
        return 0 if all(passes(o) for o in outcomes) else 1

    if ns.command == "run":
        from .certify import GRADES
        from .run import record, run
        try:
            output, values, state = run(ns.file, ns.main, ns.fuel, ns.set, GRADES.get(ns.accept), ns.checked,
                                        ns.fresh)
            print(output, end="")
            record(ns.file, state["demand"]["entry"], values, output, state)
            return 0
        except (OSError, ValueError, RecursionError) as exc:
            import sys
            print(f"{ns.file}: {exc}", file=sys.stderr)
            return 1

    if ns.command == "session":
        return _session(ns.files, ns.world, ns.fuel)

    if ns.command == "eval":
        from .run import RunError, _type_shown, evaluate, show_states
        import sys
        try:
            value, ty, states = evaluate(ns.files, ns.term, ns.fuel)
        except (OSError, RunError, ValueError, RecursionError) as exc:
            print(f"{ns.files[0]}: {exc}", file=sys.stderr)
            return 1
        print(f"{_type_shown(value, sys.maxsize)} : {_type_shown(ty, sys.maxsize)}")
        for line in show_states(states):
            print(line)
        return 0

    failed = False
    for raw_path in ns.files:
        path = Path(raw_path)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"{path}:1:0: {exc}")
            failed = True
            continue
        result = parse(text)
        if isinstance(result, ParseFailed):
            failed = True
            for error in result.errors:
                print(f"{path}:{error.line}: syntax <parse>: {error.message}" if ns.command == "check"
                      else f"{path}:{error.line}:{error.column}: {error.message}")
        elif ns.command == "check":
            from .check import check, report
            import re
            def line_of(name):
                return next((i for i, line in enumerate(text.splitlines(), 1)
                             if re.match(r"^" + re.escape(name) + r"(?:\s|:|=|$)", line)), 1)
            failures = check(result.program, path)
            failed |= bool(failures)
            for failure in failures:
                print(f"{path}:{line_of(failure.name)}: {failure.rule} {failure.name}: {failure.message}")
            if ns.verbose:
                for item in report(result.program):
                    print(f"{path}:{line_of(item.name)}: {item.kind} {item.name}: {item.message}")
                failed |= _standings(path, line_of, ns.files)
        elif ns.tree and isinstance(result, Parsed):
            for act in result.program:
                print(act)
    return 1 if failed else 0


def _session(files, world=False, fuel=None):
    """`luthier session [files]` (12.S20): the lines of standard input, one item or term each, until
    `:quit` or the end; a refused line is reported on standard error and leaves the block as it
    was. [proposed] Exit 1 when the files cannot be loaded or a line was refused, else 0. With no
    file, the session sees core alone."""
    import sys
    from .run import RunError, Session
    try:
        session = Session(files, world, fuel)
    except (OSError, RunError, ValueError, RecursionError) as exc:
        print(f"session: {exc}", file=sys.stderr)
        return 1
    failed = False
    prompt = sys.stdin.isatty()
    while True:
        if prompt:
            print("> ", end="", flush=True)
        text = sys.stdin.readline()
        if not text or text.strip() == ":quit":
            break
        try:
            for line in session.line(text):
                print(line, flush=True)
        except (RunError, ValueError, RecursionError) as exc:
            failed = True
            for line in getattr(exc, "out", ()):
                print(line, flush=True)
            print(f"session: {exc}", file=sys.stderr, flush=True)
    return 1 if failed else 0


def _standings(path, line_of, files=()):
    """`check -v`: per law a test line of the file names, its standing from the store against the
    current hash of its cone (12.S11, 12.S14): the grade, refuted, not run, stale or uncertified;
    and its control status from the control entries of the stores of every file checked (7.S19,
    L9.14): controlled, control failed, or uncontrolled. Per control line, its control's standing.
    Only for a file with test lines; True when the program cannot be loaded."""
    from .tester import collect_tests, line_cones
    try:
        if not collect_tests(path):
            return False
        from .certify import control_standing, control_status, controls_in, read_store, standing
        controls = controls_in(dict.fromkeys([path, *files]))
        entries = read_store(path)
        lines = line_cones(path)
        for law, current, control in lines:
            if not control:
                print(f"{path}:{line_of(law)}: certificate {law}: {standing(entries, law, current)}; "
                      f"{control_status(controls, law, current)}")
        for law, current, control in lines:
            if control:
                print(f"{path}:{line_of(law)}: certificate control of {law}: "
                      f"{control_standing(entries, law, current)}")
        return False
    except (OSError, ValueError, RecursionError) as exc:
        print(f"{path}:1: certificate: {exc}")
        return True


if __name__ == "__main__":
    raise SystemExit(main())
