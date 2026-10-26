#!/usr/bin/env python3
"""law_instances.py: each law of the library, the examples and the tester recognized as a core
property by its normal form (src/luthier/normal.py), with the instantiation.

Usage: scripts/law_instances.py [ROOT ...]   (ROOT defaults to the three below, from the repo root).
Prints one line per recognized law (`file: L is P at ...`), marked `wrapper` when the law's body
names the property (a one-line claim of it) and `ad hoc` when it does not; then the laws whose
normal form is `X == X` (true by the claims the order used); then the files that did not read.
The laws of DICTIONARY_FILES themselves are left out (each is its own entry). Nothing is claimed of
a law not listed. Parameters (P11): ROOTS, SUFFIXES and normal.py's (UNFOLD, EXACT, WITHIN,
ALIASES, DICTIONARY_FILES, MAX_PERMUTATIONS, FUEL, LABEL_ROUNDS). Deterministic, no seed.
Version: 1, 2026-10-27, Claude Opus 5.5, on record/plan/law-normal-form-2026-10-27/prompt.md.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
from luthier import normal, kernel  # noqa: E402

ROOTS = ["src/luthier/lib", "examples", "tests/tester"]
SUFFIXES = (".lth", ".lut")


def files(roots):
    out = []
    for r in roots:
        p = REPO / r
        found = [p] if p.is_file() else sorted(p.rglob("*"))
        out += [f for f in found if f.suffix in SUFFIXES and f.is_file()]
    return out


def main(argv):
    roots = argv or ROOTS
    start = time.time()
    entries = {e.name for e in normal.dictionary()}
    skip = {(normal.CORE / rel).resolve() for rel in normal.DICTIONARY_FILES}
    recognized, trivial, failed = [], [], []
    for path in files(roots):
        if path.resolve() in skip:
            continue
        rel = path.relative_to(REPO)
        try:
            env, own = normal.env_of(path)
        except Exception as e:  # a file the parser or the typing does not read is listed, not fatal
            failed.append((rel, f"{type(e).__name__}: {e}"[:160]))
            continue
        for law in normal.laws_of(env, own):
            try:
                found = normal.recognize(law)
                if not found and normal.trivial(law):
                    trivial.append((rel, law.name))
            except Exception as e:
                failed.append((rel, f"{law.name}: {type(e).__name__}: {e}"[:160]))
                continue
            act = env.defs.get(law.name)
            named = kernel.free_names(act.body) if act is not None else set()
            for inst in found:
                kind = "wrapper" if inst.property in named else "ad hoc"
                recognized.append((rel, kind, inst.notice()))
    for rel, kind, line in recognized:
        print(f"{rel}: [{kind}] {line}")
    print(f"-- {len(recognized)} recognized ({sum(k == 'ad hoc' for _, k, _ in recognized)} ad hoc)")
    for rel, name in trivial:
        print(f"{rel}: [trivial] {name} is X == X under the core's exact claims")
    for rel, why in failed:
        print(f"{rel}: [not read] {why}")
    print(f"-- {len(entries)} properties in the dictionary; {time.time() - start:.0f} s")


if __name__ == "__main__":
    main(sys.argv[1:])
