"""Put every entry of every store in the one store L10.12 names: the claim's.

Brief: record/IA/code-follows-2026-10-16/prompt-claim-store.md, follow-up items 1 and 2 (L10.12,
D-2026-10-16-b). Written 2026-10-16 by Claude Opus 5.5, an agent of the coordinating session.

Every store with a list of entries under src/luthier/lib, examples and tests/tester is read. Each
entry is assigned the file that makes its claim, by the current test lines of every test program
in tests/tester (scripts/fold_claim_stores.py's `lines_of` and `claim_of`): by group (law, binding
without fingerprints, kind), else by (law, kind) when all lines of that law and kind share a
claim, else by the generators' names, else by `tester.claim_file` on the entry's own binding,
loaded by a test program whose files define the law. An entry a run wrote at a first action
(`FirstAction`, 10.S10) stays where the run put it, as does an entry no tier resolves (each
printed), unless its identity is in the archive of removed laws (record/archive/stores-2026-10-16,
scripts/fold_claim_stores.py), which keeps it. Each identity is then kept once, in its claim's store, the latest in front, nothing
pruned; a store left with no entry is removed. Without `--write` nothing is written: the plan and
the counts are printed, with the sha256 of every store read.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from luthier import certify, tester  # noqa: E402

_spec = importlib.util.spec_from_file_location("fold_claim_stores", ROOT / "scripts" / "fold_claim_stores.py")
fold = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fold)


def stores():
    found = []
    for d in ("src/luthier/lib", "examples", "tests/tester"):
        for p in sorted((ROOT / d).rglob("*.cert.json")):
            try:
                entries = json.loads(p.read_bytes())
            except ValueError:
                continue
            if isinstance(entries, list):
                found.append(p)
    return found


def source_of(store):
    """The file a store is beside: x.lut or x.lth, whichever exists (x.lut when neither does)."""
    stem = store.name[:-len(".cert.json")]
    for ext in (".lut", ".lth"):
        if (store.parent / (stem + ext)).exists():
            return (store.parent / (stem + ext)).resolve()
    return (store.parent / (stem + ".lut")).resolve()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--write", action="store_true", help="rewrite the stores")
    ns = ap.parse_args(argv)
    if os.environ.get(certify.LIBRARY_STORES):
        sys.exit(f"{certify.LIBRARY_STORES} is set: the library's stores would be read elsewhere")
    programs = [p for p in sorted((ROOT / "tests" / "tester").glob("*.lut")) if tester.collect_tests(p)]
    lines, loaded = [], []
    for p in programs:
        ls, program = fold.lines_of(p)
        lines += ls
        loaded.append(program)
    read = {}
    before = 0
    for store in stores():
        raw = store.read_bytes()
        read[store] = json.loads(raw)
        before += len(read[store])
        print(f"read: {store.relative_to(ROOT)} {len(read[store])} entries sha256:{hashlib.sha256(raw).hexdigest()}")
    identities_before = {certify.identity(e) for es in read.values() for e in es}
    placed = {}  # claim file -> {identity: entry}
    tiers, stayed = {}, []
    archived = {certify.identity(e) for p in fold.ARCHIVE.glob("*.cert.json")
                for e in json.loads(p.read_text(encoding="utf-8"))}
    for store, entries in read.items():
        here = source_of(store)
        for e in entries:
            if certify.entry_kind(e) == certify.FIRST_ACTION:
                claim, tier = here, "first action"
            else:
                claim, tier = _claim(e, lines, loaded)
                if tier == 4:
                    print(f"  tier 4: {store.relative_to(ROOT)} {e['law']} {fold.generators(e)} -> "
                          f"{Path(claim).relative_to(ROOT)}")
                if claim is None and certify.identity(e) in archived:
                    tiers["archived"] = tiers.get("archived", 0) + 1
                    print(f"  archived already, dropped: {store.relative_to(ROOT)} {e['law']}")
                    continue
                if claim is None:
                    claim, tier = here, "unresolved"
                    stayed.append((store, e["law"]))
            tiers[tier] = tiers.get(tier, 0) + 1
            placed.setdefault(claim, {}).setdefault(certify.identity(e), e)
    after = {}
    for claim, by_identity in placed.items():
        merged = sorted(by_identity.values(), key=lambda e: e.get("date", ""), reverse=True)
        errors = certify.store_errors(merged)
        if errors:
            sys.exit(f"{claim}: {'; '.join(errors)}")
        after[certify.store_path(claim)] = (claim, merged)
    for store, entries in read.items():
        now = len(after.get(store, (None, []))[1])
        if now != len(entries):
            print(f"store: {store.relative_to(ROOT)} {len(entries)} -> {now}")
    for where, (claim, merged) in after.items():
        if where not in read:
            print(f"store: {where.relative_to(ROOT)} new, {len(merged)}")
    for store, law in stayed:
        print(f"unresolved, left in place: {store.relative_to(ROOT)} {law}")
    total_after = sum(len(m) for _, m in after.values())
    identities_after = {certify.identity(e) for _, m in after.values() for e in m}
    print(f"tiers: {tiers}")
    print(f"before: {before} entries in {len(read)} stores, {len(identities_before)} identities")
    lost = identities_before - identities_after - archived
    print(f"after: {total_after} entries in {len(after)} stores, {len(identities_after)} identities "
          f"(and {len((identities_before - identities_after) & archived)} kept in the archive); lost: {len(lost)}")
    if ns.write:
        for where, (claim, merged) in after.items():
            certify.write_store(claim, merged)
        for store in read:
            if store not in after:
                store.unlink()
                print(f"removed: {store.relative_to(ROOT)}")
    return 0


def _sees(loaded, name):
    try:
        return loaded.see(loaded.top, name) is not None
    except Exception:
        return False


def _claim(entry, lines, loaded):
    """fold_claim_stores' tiers 1 to 3 over every program's lines, then tier 4 with the first
    program whose files define the law."""
    group = certify._group(entry)
    by_group = {c for g, _, _, c in lines if g == group}
    if len(by_group) == 1:
        return by_group.pop(), 1
    same = [(gens, c) for _, k, gens, c in lines if k == (entry["law"], fold.kind(entry))]
    if same and len({c for _, c in same}) == 1:
        return same[0][1], 2
    by_names = {c for gens, c in same if gens == fold.generators(entry)}
    if len(by_names) == 1:
        return by_names.pop(), 3
    defining = [p for p in loaded if any(entry["law"] in f.defined for f in p[1].files.values())]
    # [proposed] the first program that sees every census the entry names, else the first that defines the law
    defining = [p for p in defining if all(_sees(p[1], g) for g in fold.generators(entry) if g.isidentifier())] or defining
    for program in defining[:1]:
        if True:
            try:
                return fold.from_entry(entry, program), 4
            except Exception as exc:
                print(f"tier 4 failed: {entry['law']}: {type(exc).__name__}: {exc}")
                return None, None
    return None, None


if __name__ == "__main__":
    raise SystemExit(main())
