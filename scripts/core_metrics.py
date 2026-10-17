#!/usr/bin/env python3
"""core_metrics.py: the four counts of the core's end (record/plan/core-2026-10-17/execution.md
section 0, D-2026-10-18-a), measured over src/luthier/lib, examples/ and tests/tester.

  1. homonyms: names defined at the top level of more than one file (a name is defined by a
     declaration, a definition, an alias or a data constructor), less ACCEPTED_HOMONYMS.
  2. reinvented list helpers: a top-level definition outside lib/core/lists.lut whose body is a
     `match` (or clauses) with a `nil` arm and a `cons` arm, or whose name is in the seven
     families (all..., any..., append..., member..., lookup..., concat..., lengthOf, listLength,
     mapList).
  3. unclaimed: the Bool laws `luthier check -v` reports `unclaimed`.
  5. shadows: names an executive file defines that an importable file also defines.
  4. loose: the `loose` notices of `luthier check -v`, split into real and the rest. [proposed]
     A notice is real when the name is a function defined at the top level that no theory names,
     the rest being the names a theory names (they stand to be absorbed by their theory):
     a theory is a name declared or defined with a record type, and it names the fields of that
     record and every name in the bodies of its definitions (its `T := laws` list).

Usage: scripts/core_metrics.py [-v] [ROOT ...]   (ROOT defaults to the three above, from the repo
root; the lists under -v). Parameters (P11): ACCEPTED_HOMONYMS, FAMILIES, LISTS_FILE below, the
roots, the seed (none: the script is deterministic).
Version: 1, 2026-10-18, Claude Sonnet 5.5, on record/plan/core-2026-10-17/prompt-bite-3.md.
Inputs: the library at ded76d4, luthier 0.2.0.dev0.

Roots rule (D-2026-10-16-e): an executive file (`*.run.lut`, `*.test.lut`) may define local names
seen nowhere else, so counts 1 and 3 and 4 read the importable files only (`.lth` and the `.lut`
that are not executive); count 2 reads every file, since a reinvented recursion is one wherever it
is; a fifth count, the names an executive file defines that an importable file also defines (the
collisions D-2026-10-18-b refuses), stands apart from the homonyms.

Counts at the tree after ded76d4 (9a3d665 plus bite 3's files), 24 s:
  all three roots:  homonyms 96, executive shadows 112, list helpers 427, unclaimed 137,
                    loose 1974 (real 1341, the rest 633)
  lib alone:        homonyms 81, executive shadows 0, list helpers 397, unclaimed 70,
                    loose 1737 (real 1116, the rest 621)
The 70 unclaimed of the library are `check -v`'s own; the loose total differs from the 1675 of the
plan's survey because this one counts the .lut files and the data constructors the survey did not.
ACCEPTED_HOMONYMS is empty: no homonym is required by the language.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import fields, is_dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
from luthier import surface as s  # noqa: E402
from luthier.parse import parse  # noqa: E402

ROOTS = ["src/luthier/lib", "examples", "tests/tester"]
SUFFIXES = (".lth", ".lut")
# the file whose list functions are the core's (a name -> reason table for homonyms follows)
LISTS_FILE = "core/lists.lut"
# names defined in more than one file that the language requires, each with its reason; empty:
# no homonym is required by the language (a rename removes each one, 12.S4)
ACCEPTED_HOMONYMS: dict[str, str] = {}
FAMILIES = re.compile(r"^(all|any|append|member|lookup|concat)([A-Z0-9_].*)?$|^(lengthOf|listLength|mapList)$")


def executive(p):
    """D-2026-10-16-e: a `*.run.lut` or `*.test.lut` is executive; its names are local, seen nowhere else."""
    return p.name.endswith((".run.lut", ".test.lut"))


def rel(p, base):
    try: return p.relative_to(base)
    except ValueError: return p


def files(roots, base=REPO):
    out = []
    for r in roots:
        p = (base / r)
        found = [p] if p.is_file() else sorted(p.rglob("*"))
        out += [f for f in found if f.suffix in SUFFIXES and f.is_file()]
    return out


def program_of(path):
    result = parse(path.read_text(encoding="utf-8"))
    return None if isinstance(result, s.ParseFailed) else result.program


def defined(program):
    """The names a file defines at its top level."""
    names = []
    for a in program:
        if isinstance(a, (s.Declare, s.Define, s.Alias)):
            names.append(a.name)
            if isinstance(a, s.Define) and isinstance(a.body, s.DataBody):
                names += [c for c, _ in a.body.constructors]
    return list(dict.fromkeys(names))


def walk(u):
    yield u
    if isinstance(u, tuple):
        for x in u:
            yield from walk(x)
    elif is_dataclass(u):
        for f in fields(u):
            yield from walk(getattr(u, f.name))


def heads(pattern):
    return {pattern.name} if isinstance(pattern, s.PApp) else set()


def matches_list(term):
    """Whether a body is, under lambdas and blocks, a match with a nil arm and a cons arm."""
    while True:
        if isinstance(term, s.Lambda): term = term.body
        elif isinstance(term, s.Block): term = term.value
        else: break
    if isinstance(term, s.MatchOf):
        return {"nil", "cons"} <= set().union(*(heads(p) for p, _ in term.arms))
    return False


def reinvents(a):
    if not isinstance(a, s.Define): return False
    if FAMILIES.match(a.name): return True
    if isinstance(a.body, s.TermBody): return matches_list(a.body.term)
    if isinstance(a.body, s.ClausesBody):
        return {"nil", "cons"} <= set().union(*(heads(p) for c in a.body.clauses for p in c.patterns))
    return False


def homonyms(paths, programs, base):
    """Names defined in more than one importable file (executive files are left out)."""
    where = defaultdict(list)
    for p in paths:
        if executive(p): continue
        for n in defined(programs[p]): where[n].append(str(rel(p, base)))
    found = {n: fs for n, fs in where.items() if len(fs) > 1 and n not in ACCEPTED_HOMONYMS}
    return dict(sorted(found.items(), key=lambda kv: (-len(kv[1]), kv[0])))  # most files first


def shadows(paths, programs, base):
    """Names an executive file defines that an importable file also defines (D-2026-10-18-b refuses them)."""
    library = defaultdict(list)
    for p in paths:
        if not executive(p):
            for n in defined(programs[p]): library[n].append(str(rel(p, base)))
    out = [f"{rel(p, base)}: {n} (also in {', '.join(library[n][:3])})"
           for p in paths if executive(p) for n in defined(programs[p]) if n in library]
    return sorted(out)


def helpers(paths, programs, base):
    out = []
    for p in paths:
        path_rel = rel(p, base).as_posix()
        if path_rel.endswith(LISTS_FILE): continue
        out += [f"{path_rel}: {a.name}" for a in programs[p] if reinvents(a)]
    return out


def theory_names(program):
    """The names the theories of a file name: fields of their records and the names in their definitions."""
    is_record = lambda t: isinstance(t, s.Record)
    theories = {a.name for a in program if isinstance(a, (s.Declare, s.Define)) and is_record(a.type)}
    named = set()
    for a in program:
        if isinstance(a, (s.Declare, s.Define)) and a.name in theories and is_record(a.type):
            named |= {n for f in a.type.fields for n in f.names}
        if isinstance(a, s.Define) and a.name in theories:
            named |= {x.name for x in walk(a.body) if isinstance(x, s.Name)}
    return named


def check_notices(paths, programs, base=REPO):
    """kind -> [(file, line, name)]: the `unclaimed` and `loose` reports of `luthier check -v`,
    from the same predicates (check.py's violatesS14 and looseFunction) called on the parsed
    file. The command itself also types each file and reads its stores, about four seconds a file,
    which these two reports do not use."""
    from luthier.check import looseFunction, violatesS14
    out = defaultdict(list)
    for path in paths:
        program = programs[path]
        text = path.read_text(encoding="utf-8").splitlines()
        line_of = lambda n: next((i for i, l in enumerate(text, 1) if re.match(r"^" + re.escape(n) + r"(?:\s|:|=|$)", l)), 1)
        for n in dict.fromkeys(a.name for a in program if isinstance(a, (s.Declare, s.Define, s.Alias))):
            for kind, pred in (("unclaimed", violatesS14), ("loose", looseFunction)):
                if pred(program, n): out[kind].append((rel(path, base).as_posix(), line_of(n), n))
    return out


def measure(roots=ROOTS, base=REPO):
    paths = files(roots, base)
    programs = {p: program_of(p) for p in paths}
    paths = [p for p in paths if programs[p] is not None]
    notices = check_notices([p for p in paths if not executive(p)], programs, base)
    named = set().union(*(theory_names(programs[p]) for p in paths))
    loose = notices["loose"]
    real = [x for x in loose if x[2] not in named]
    return {
        "homonyms": homonyms(paths, programs, base),
        "shadows": shadows(paths, programs, base),
        "helpers": helpers(paths, programs, base),
        "unclaimed": [f"{f}:{l}: {n}" for f, l, n in notices["unclaimed"]],
        "loose_real": [f"{f}:{l}: {n}" for f, l, n in real],
        "loose_rest": [f"{f}:{l}: {n}" for f, l, n in loose if (f, l, n) not in real],
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("roots", nargs="*", default=ROOTS)
    ns = ap.parse_args(argv)
    m = measure(ns.roots)
    print(f"homonyms {len(m['homonyms'])}")
    print(f"executive names shadowing {len(m['shadows'])}")
    print(f"list helpers {len(m['helpers'])}")
    print(f"unclaimed {len(m['unclaimed'])}")
    print(f"loose {len(m['loose_real']) + len(m['loose_rest'])} (real {len(m['loose_real'])}, the rest {len(m['loose_rest'])})")
    if ns.verbose:
        for n, fs in m["homonyms"].items(): print(f"homonym {n}: {', '.join(fs)}")
        for x in m["shadows"]: print(f"shadow {x}")
        for h in m["helpers"]: print(f"helper {h}")
        for u in m["unclaimed"]: print(f"unclaimed {u}")
        for r in m["loose_real"]: print(f"loose real {r}")
        for r in m["loose_rest"]: print(f"loose rest {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
