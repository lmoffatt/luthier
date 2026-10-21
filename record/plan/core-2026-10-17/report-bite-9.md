# Bite 9: the machinery (partial report, written while the wave runs)

Claude Sonnet 5.5, 2026-10-21, on `prompt-bite-9.md`. Inputs: execution.md sections 0, 5, 6, reports 6 and 7,
D-2026-10-18-a, -b, -f, D-2026-10-21-a. The run was cut twice (API error, user interrupt); this report states what
landed and what did not.

## Landed (commits d4b8f85, 0f128d2, 8ef6389, eb49580, 386a5f0, 54c0f69)

- checks.lth: failuresEmpty, takeFailures, concatFailures gone (core `isEmpty`, `take`, `<>`); `reason` through `nth`.
- laws.lth: section 2 (twelve relation templates) removed; `allConfirmed`, `anyRefuted`, `anyConfirmed`, `allRefutedOf`,
  `allConfirmedOrSupported` replaced by `all`/`any`; `pointVerdicts` by `map`; `Both` renamed `Conjunction` (and
  `BothByPair` `ConjunctionByPair`), `flip` renamed `reversedVerdict`, which empties laws.lth's entry of
  run.py's CORE_COLLISIONS; `Settling` written bare with `Commutative` and `Associative` at Verdict.
- generators.lth: memberOf, allOf, noDuplicates, upTo, lengthOf, nthGenerated, isEmptyList, isOneElement, allNonNegative gone
  (core `any`, `all`, `distinct`, `filter`, `size`, `nth`, `isEmpty`); `total`, `weightOf`, `occurs`, `caseNames`,
  `witnessesHold`, `casesOf` on folds; `Sized` is `SizedGenerator`; `listDegeneracies` takes `A : Concrete`.
  generators_model.lut: `squares` is `map`.
- test.lth: countPoints gone (`size`), `bindingsCoverage` a `fold`.
- certification.lth: lengthOf, memberRegion, appendRegions, appendRefusals, appendEntries, allIn, anyServes, anyIs,
  countRegions, countStrings, nameIn and about 20 further maps, filters and searches on the core's functions;
  `CombineCommutes` removed, `Regioning` written bare (full form) with `Commutative (Maybe Grade) ...` as a conjunct.
  certification_model.lut: anyValue, anyFailure, keepWithin, refuse on core functions.
- world.lth, world_model.lut: memberStr, mapList, lengthOf, concatFields, concatStrs, lookupFile gone.
- plan.lth, plan_model.lut: memberStr, appendOne, noDuplicates, allNames, countNodes, lengthStrs gone. demand.lth: lookupValue gone.
- Test programs migrated: regions_laws/controls (the `CombineCommutes` line is now a line of the core law
  `Commutative` at `Maybe Grade`, with its control on the first-argument combination), certification_controls,
  world_laws/controls, tests/run/observe.run.lut, tests/test_certify.py (law list).

## Not done, or not verified

- The re-certification wave (one wave, no --deep, `luthier certify --jobs 3` over regions, certification, generators,
  world, plan, demand, pooling, cutoff programs) was started and had not finished when this was written.
  Its result is not in this report; the stores it writes are uncommitted. The full pytest was not run (about 50 minutes).
  An earlier `luthier test` of regions_laws failed only because bite 10's term.lth was mid-edit.
- Left as they were: search-with-result recursions (latestWith, behind, disputes, failureAt, reachOf, latestOf, latestAt,
  largestAt, sumOfLargest, `pick`, `before`, `firstBinding`, `determined`, `latestInFront`), `prepend`, `passes`,
  `bestUnder`, `meetReaches`, and the local helpers inside the test programs (regions_controls, world, demand, pooling,
  plan, plot controls). Laws.lth's `Settling` has no model and no test line, so its renamed combination laws are not graded
  (as before the bite); this is a finding.
- `OwnIsIdempotent` (world.lth) kept: `describe` is pair-valued, so core `Idempotent` does not state it.
- Not touched: homonyms `identity`, `larger`, `agree`, `contains`, `grade`, `known`, `State`, `Store`, etc. between my files and others.

## Decisions I took on my own

1. `Both` to `Conjunction`, `flip` to `reversedVerdict` (the plan named no new names).
2. `any` with `==` instead of `member` for element types with no `Object` claim (Region, Value, Entry, Identity).
3. `Indexed.size (listIndexed A)` where `A : Concrete` is a bound variable (`size` is refused as ambiguous there).
4. `Regioning` and `Settling` rewritten in the full bare form; the commutativity conjunct is graded by a line of the
   core law `Commutative`, not by a line of `Regioning` (whose ten conjuncts have ten different broken models).
5. `OwnIsIdempotent` kept (see above).

## Metrics (core_metrics.py, whole shared tree, includes bites 8 and 10 at their moment)

Before (tree at 24b63e9 plus bite 8 in progress): homonyms 74, shadows 107, list helpers 426, unclaimed 45, loose 2087.
After (end of my edits, bites 8 and 10 also moving): homonyms 64, shadows 107, list helpers 260, unclaimed 32, loose 2002.
`check_spec.py`: only its known finding.

## Question

May the commutativity of `Regioning`'s combination be graded by a line of the core law `Commutative` (as done), or must
`Regioning` itself get a line with ten controls?
