"""Fold the stores beside test programs into the stores of the files that make the claims.

Brief: record/IA/code-follows-2026-10-16/prompt-claim-store.md, item 2 (L10.12, D-2026-10-16-b).
Written 2026-10-16 by Claude Opus 5.5, an agent of the coordinating session.

A store beside a file with `test` lines (tests/tester/*.cert.json, examples/**/*.cert.json) is
read; each of its entries is assigned the file that makes its claim (tester.py's `claim_file`) by
matching it to a current test line of that file:
  1. by (law, binding without fingerprints, kind), the group `certify.prune` uses;
  2. else by (law, kind) when every current line of that law and kind has one claim file;
  3. else by the names of the binding's generators (each before " (").
An entry no tier resolves stops the fold (nothing is written). An entry whose identity is already
in the claim's store is not added again; the others are added without pruning (no entry lost), the
store kept latest in front, its predicate (`certify.store_errors`) checked. A store whose every
entry has its own file as claim is left in place; the others are removed once folded.

The library's stores are written in place (LUTHIER_LIBRARY_STORES must be unset). Without
`--write` nothing is written: the plan and the counts are printed. Every input store is printed
with the sha256 of its bytes.
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from luthier import certify, tester  # noqa: E402


def generators(entry):
    return tuple(str(d.get("generator", "")).split(" (")[0] for d in entry["binding"])


def kind(entry):
    return certify.entry_kind(entry)


def lines_of(program):
    """Per current test line: (group key, (law, kind), generator names, claim file)."""
    runner, specs, loaded = tester.prepare(program)
    cones = certify.Cones(runner)
    out = []
    for spec in specs:
        entry = tester.new_entry(runner, loaded, spec, cones, 1_000_000)
        if spec.control:
            entry["kind"] = certify.CONTROL
        claim = tester.claim_file(loaded, spec, runner).resolve()
        out.append((certify._group(entry), (entry["law"], kind(entry)), generators(entry), claim))
    return out


def claim_of(entry, lines):
    group = certify._group(entry)
    by_group = {c for g, _, _, c in lines if g == group}
    if len(by_group) == 1:
        return by_group.pop(), 1
    same = [(gens, c) for _, k, gens, c in lines if k == (entry["law"], kind(entry))]
    if same and len({c for _, c in same}) == 1:
        return same[0][1], 2
    by_names = {c for gens, c in same if gens == generators(entry)}
    if len(by_names) == 1:
        return by_names.pop(), 3
    return None, None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--write", action="store_true", help="write the claims' stores and remove the folded ones")
    ns = ap.parse_args(argv)
    if os.environ.get(certify.LIBRARY_STORES):
        sys.exit(f"{certify.LIBRARY_STORES} is set: the library's stores would be read elsewhere")
    stores = sorted(p for d in ("tests/tester", "examples") for p in (ROOT / d).rglob("*.cert.json"))
    folded, plan, tiers, unresolved = [], {}, {1: 0, 2: 0, 3: 0}, []
    total_before = 0
    for store in stores:
        program = store.with_name(store.name[:-len(".cert.json")] + ".lut")
        if not program.exists() or not tester.collect_tests(program):
            print(f"left: {store.relative_to(ROOT)} (beside no test program)")
            continue
        raw = store.read_bytes()
        entries = json.loads(raw)
        print(f"read: {store.relative_to(ROOT)} {len(entries)} entries sha256:{hashlib.sha256(raw).hexdigest()}")
        lines = lines_of(program)
        own = []
        for e in entries:
            claim, tier = claim_of(e, lines)
            if claim is None:
                unresolved.append((store, e["law"], generators(e)))
                continue
            tiers[tier] += 1
            if claim == program.resolve():
                own.append(e)
            else:
                plan.setdefault(claim, []).append(e)
        total_before += len(entries)
        folded.append((store, len(entries), own))
    if unresolved:
        for store, law, gens in unresolved:
            print(f"unresolved: {store.relative_to(ROOT)} {law} {gens}")
        sys.exit(1)
    moved = already = 0
    targets = {}
    for claim, entries in plan.items():
        current = certify.read_store(claim)
        seen = {certify.identity(e) for e in current}
        new = []
        for e in entries:
            i = certify.identity(e)
            if i in seen:
                already += 1
            else:
                seen.add(i)
                new.append(e)
                moved += 1
        merged = sorted(current + new, key=lambda e: e.get("date", ""), reverse=True)
        errors = certify.store_errors(merged)
        if errors:
            sys.exit(f"{claim}: {'; '.join(errors)}")
        targets[claim] = (len(current), merged)
        print(f"claim: {Path(claim).relative_to(ROOT)} {len(current)} + {len(new)} = {len(merged)} "
              f"({len(entries) - len(new)} already there)")
    kept = sum(len(own) for _, _, own in folded)
    print(f"tiers: {tiers}")
    print(f"before: {total_before} entries in {len(folded)} stores beside files with test lines")
    print(f"after: {moved} moved, {already} already in the claim's store, {kept} kept beside their own "
          f"claim; {moved + already + kept} accounted for")
    if ns.write:
        for claim, (_, merged) in targets.items():
            certify.write_store(claim, merged)
        for store, _, own in folded:
            if own:
                certify.write_store(store.with_name(store.name[:-len(".cert.json")]), sorted(
                    own, key=lambda e: e.get("date", ""), reverse=True))
                print(f"kept: {store.relative_to(ROOT)} {len(own)} entries of its own claims")
            else:
                store.unlink()
                print(f"removed: {store.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
