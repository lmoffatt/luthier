# Report: a law's samples pooled across seeds (step 3i)

Brief: `record/IA/code-follows-2026-10-16/prompt-pool-seeds.md`. By Claude Opus 5.5, an agent of the
coordinating session, 2026-10-16. Commits: edaeb6f (theory, model, test programs), 58db41a (certify.py,
tester.py, tests), afa8685 (spec 7.S11, 7.S13, 7.S17; 6.S14 with the coordinator's sentence on
provisionals, D-2026-10-16-c).

## What was built

The union (D-2026-10-16-g, L10.3). certification.lth draft 3, §2: a stretch is one run of a law under
one binding and one seed. `pooledCases` is the size of the union of a law's stretches at the current
hash under a binding: the passes and, for a statistical law, the stretches it left unresolved, each
seed once at its largest `n`. A run over every value or a census is one stretch whatever its seed
(`drawnStretch`: a statistical test, or points over `Drawn`). The grade is the fold of §2, unchanged:
a failure in any stretch refutes, a disagreement in any stretch refuses, as before. §5 adds the theory
`Pooling` (like `Recording`, apart from `Certifying`, so no existing cone hash moves), with two laws:
`TheUnionIsMonotone` (a pass of a new seed adds its cases and lowers no grade under its binding) and
`AReplayIsNotANewStretch`. Reference `pooling` in certification_model.lut, specimen `certify.pooled`.
Test programs tests/tester/pooling_laws.lut (both laws hold on the reference) and pooling_controls.lut
(a union counting every entry, so a replay twice, refuted; one counting the latest stretch only,
refuted).

The continued test. laws.lth §4 gains `ratioAfter` (the ratio a stretch stops at, the recursion of
`sequentialFrom`) and `spentOf`; `sequential` and `sequentialFrom` are untouched. The tester, with the
store read, starts the line of a new seed from the ratio the latest stretch of the same law, cone,
binding and kind stopped at (`certify.continuation`), drawing at most the budget again; the entry's
evidence records `"ratio"` and, when it continued, `"from"` (ratio, samples, seeds before it). A
`--deep` replay starts from its own recorded `"from"`, so it stays deterministic and agrees. The line
says "continuing the test of seed 5 (2 samples in all)".

Standing: `certify` and `check -v` append "pooled over seeds 1, 2: 200 cases in all" when a binding's
union holds two stretches or more; one stretch reads as before.

## Checks

- `python -m pytest -q`: 759 passed, 6 skipped, 9 xfailed. The known failure
  test_an_alias_or_a_constructor_is_no_model_home is gone (the other agent's fix landed).
  One existing assertion changed: test_tester's statistical evidence now holds `"ratio"`.
- `python3 scripts/check_spec.py`: the one known finding, 03-kernel.md:190; counts 182 implemented,
  80 decided (33 suspended), 8 proposed (unchanged: the new text is inside existing items).
- `luthier certify tests/tester/arrays_laws.lut`: "35 laws, 0 lines ran, 52 known"; md5 of the 22
  src/luthier/lib/*.cert.json identical before and after.

## Decisions taken on my own

1. `Pooling` is its own theory beside `Certifying`, as `Recording` was, so no cone of the existing
   certification laws changes and no store goes stale.
2. [proposed] The budget bounds each stretch, not the total: a stretch is a line under its cutoffs,
   and with a total budget a stretch that ran out could never be continued under the same binding.
3. [proposed] Of two entries of one seed, the larger `n` counts (the first n cases of a seed are those
   of any larger run of it).
4. [proposed] An exhaustive or census run is one stretch whatever its seed.
5. A new seed after a resolved test continues it too, and so draws nothing and repeats the verdict:
   one sequential test per law and binding.
6. The ratio and the start are in the evidence, not in the outcome, so an old `Unresolved` entry still
   agrees with its replay; old entries without a ratio are not continued (a new seed starts fresh).
7. Continuation only when the store is read (`--no-cert` runs each line alone).
8. The standing prints the union only from two stretches up, so every existing text stays.

A slip, undone: an early `luthier test tests/tester/pooling_laws.lut` (without `--no-cert`) wrote two
entries into src/luthier/lib/certification_model.cert.json; I removed them, and the file is identical
to HEAD. The pooling programs are not certified into the library's stores.

## Question

Decision 2: should the sequential test's `budget` bound each stretch (as built: a new seed buys one
more budget) or the whole test across stretches, which would need a second cutoff for a stretch?

## Change: the budget bounds the whole test (after the coordinator's answer, 2026-10-16)

The coordinator answered the question by D-2026-10-15-b, which already names two cutoffs: the size of
each sample (`initial`) and the budget, what the demand pays in all. So decision 2 is reversed: its
reading of the budget as bounding each stretch is dropped. Commits: ec3574c (laws.lth, certification.lth,
certify.py, tester.py, tests) and 8c40434 (spec 7.S17).

- A stretch now starts from the ratio and from the number of samples the earlier stretches left
  (`sequentialFrom ... ratio spentBefore`). The budget is checked against the total, so a new seed
  buys no budget: a line whose budget the test has spent draws nothing and stays unresolved. A line
  with a larger budget continues the test from the recorded ratio. An entry's `spent` is the samples
  it drew itself (the rates' `spent` less the samples before it).
- Under two budgets the cutoffs census differs, so the binding differs, but the stretches are still
  one test. A statistical entry now records its cutoffs' parameter (`"cutoffs"` in its evidence), and
  its union key is its binding without that drawing (`certify.union_key`). `continuation` matches on
  that key and on the same alpha, beta, delta and `initial`, with the budget left free. A line whose
  seed already has a stretch (a replay, or the same seed under another budget) starts where that
  stretch started, so it draws the same stream further and never re-uses those samples as new.
- An unresolved verdict at budget B serves no demand with a larger budget: that demand's budget sits
  in another census, so its identity differs, the line runs, and it continues the test.
- Test (tests/test_certify.py): delta 0.5 and a p-value of one, so the law holds at the seventh
  sample. Seeds 5 and 6 under budget 3 stop at 3 samples in all, both unresolved (the second draws 0).
  Seed 7 under budget 10 continues them to 7 in all and holds; the union is "pooled over seeds 5, 6,
  7: 7 samples in all"; a `--deep` replay writes nothing.
- A gap left in the theory: certification.lth's `Entry` does not name its cutoffs' parameter, so
  `pooledCases` compares bindings whole, while the specimen leaves the cutoffs out. This is noted at
  `pooledCases` and waits for the entry to carry that parameter.

Checks: `python -m pytest -q` 759 passed, 6 skipped, 9 xfailed; `check_spec.py` prints its known
finding (03-kernel.md:190) and the same counts.
