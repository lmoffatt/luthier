# Report: the evidence of a law kept per region (3j, the theory)

By Claude Fable 5.1, an agent of the coordinating session, on prompt-theory.md, 2026-10-17.
Implements D-2026-10-16-i and D-2026-10-16-j in the theories; the code follows (section 5).

## 1. What was written

Commits, in order (all on `numbers`):

- 1b4ea60 generators.lth §9: `DegenerateCase T = { name, holds : T -> Bool, witness : T }` and the
  theory `Degeneracies T : { cases : List (DegenerateCase T) }` with two laws, `EachWitnessIsItsCase`
  and `CaseNamesAreDistinct`; `casesOf` (what `classify` records of a value); `listDegeneracies A a`
  (empty, one element). The List example lives here and not in kernel_laws.lth, which this file
  imports (a cycle of files), nor in core (the brief touches no other theory).
- 4e3df1a arrays.lth §5: `matDegeneracies` (zero, 0 x 0, 1 x 1, rank deficient) and
  `symmetricDegeneracies (m : Arrays) (fl : RankFloor)` (the same, rank deficiency at the floor
  through `retainedRank`). For a general matrix the rank deficiency the entries decide exactly is a
  zero row or two equal rows; the comment says the predicate names that part of the case.
- 50d0743 certification.lth draft 5 and certification_model.lut draft 4. §2: `Source` (FromType,
  FromLaw, FromCode, Label), `Region = { source, name }`, `grades` (a label enters no grade),
  `RegionEvidence = { region, n }` with the bound `regionBound : RegionEvidence -> C` a hole beside
  `entryBound`, `BindingEvidence` (the evidence per binding and region), `lawRegions cutoffs
  premises` (two sides per cutoff, one boundary per premise), `regionGrade` (the binding's grade
  where the region has cases, at most sampled where it has none), `regionedGrade k comb c rs ev`
  (the fold over regions then bindings with the demand's combination). §5: `Regioning k :
  { combine, graded }` with ten laws (no regions leave the grade; refuted in every region; a label
  enters no grade; an empty region leaves the law below cases, and so for each of the three sources
  by name; the fold over regions and across bindings; the combination commutes, has `nothing` as
  unit, never raises), and `Deriving : { ofLaw }` with three (each cutoff two sides, each premise
  its boundary, nothing else). The models: `regioning` (combine := orWeakest, 5.S8's default) and
  `deriving` (lawRegions). `Certifying`'s fields and `Entry` are unchanged.
- fc8f08d plan.lth §4: `KeyReadsOnlyTheCone` restated with the hole tested against what the entry
  reaches in the dataflow (`reaches A eq d dm.entry`) instead of the plan's own live set, so a
  planner whose live set is wider than the cone fails it; claimed by `Planning`; controlled in
  plan_controls.test.lut by `wholeGraph` (hole `e`, which `d` does not reach in `example`).
  `KeyReadsTheType` removed: it is `demandKey`'s definition and no planner enters it; the claim a
  model can fail is `Keying`'s `KeySeesTheDemand` on two keys differing in the decoration, which
  waits for a model of `Keying`. plan_laws.test.lut loses its line and binding.
- 3e523d5 tests/tester/regions_laws.test.lut and regions_controls.test.lut (15 laws, each with a
  broken model), and tests/test_certify.py's
  `test_the_regions_hold_on_the_references_and_their_controls_refute_the_broken_ones`.
- c084d31 plan stores; 7753934 the stores of the regions (arrays, certification,
  certification_model, generators.cert.json new).

## 2. The checks

`luthier check` on generators.lth, arrays.lth, certification.lth, certification_model.lut,
plan.lth, plan_laws, plan_controls, regions_laws, regions_controls: exit 0, nothing printed.

`luthier certify tests/tester/regions_laws.test.lut tests/tester/regions_controls.test.lut`
(second run, after the census fix of section 3): "15 laws, 13 lines ran, 6 known", every law
"cases; controlled (refuted on its control at ...)", "0 laws, 15 controls", exit 0. The first run
had refuted `AnEmptyRegionLeavesBelowCases` and `CombinesOverRegions` on the reference at
`r = kappa`: the census bound to `r : GradingRegion` held the label; see section 3.

`luthier certify tests/tester/plan_laws.test.lut tests/tester/plan_controls.test.lut`: "12 laws",
`KeyReadsOnlyTheCone: cases; controlled (refuted on its control at ... p = wholeGraph, ...
n = "e", v = (Number 2.0))`, exit 0.

`python -m pytest -q`: 799 passed, 6 skipped, 9 xfailed in 1103 s (798 before, plus mine).

`python3 scripts/check_spec.py`: its known finding only (03-kernel.md:190), "185 implemented, 80
decided (of which 33 suspended), 8 proposed".

## 3. Decisions taken on my own

- A degenerate case is a named predicate with a witness (not a list of values): the predicate is
  what `classify` needs over drawn values, the witness is what "or they are listed" needs. Marked
  [proposed] in generators.lth §9.
- A region with no evidence under a binding caps that binding's grade at `Sampled` (below cases)
  rather than leaving no grade: the sample still bounds the failure fraction under its
  distribution (L10.3); a demand that wants more chooses another combination. The laws every
  combination keeps are commutativity, `nothing` as unit, never raising; the rest is the demand's.
- The per-region evidence is given beside the certificate (`BindingEvidence`), not as a field of
  `Entry`: adding the field would have changed every entry built in six test files and certify.py's
  JSON; marked as a gap of the draft, like the cutoffs' parameter in draft 3.
- The source of a region is a four-constructor data with `Label` as the fourth, so that the record
  of a label is typed and `grades` is one match.
- The names of the law's regions are built from the parameter's name ("tol above", "tol below",
  "s boundary"); the boundary of an exact premise (`Symmetric`) is the premise itself, recorded as
  the premise held (7.S14).
- `KeyReadsOnlyTheCone` enters `Planning`'s conjunction, since a planner can now fail it;
  `KeyReadsTheType` is removed rather than kept as a statement.
- The first certify run wrote two failures of the reference into certification_model.cert.json
  (uncommitted). The failures were the census's (a label listed as a `GradingRegion`; the tester
  takes a census as values of the type and filters nothing, 7.R4), so I restored the store from
  HEAD before the second run instead of archiving them: nothing had been committed, and this report
  keeps the evidence. 
- Numbers' cases (0, +1, -1) are not declared: numbers.lth is another theory.

## 4. Findings

- The tester does not validate a census against the predicate of a named subtype parameter
  (`r : GradingRegion` bound to a list holding a label ran the label). 7.S1 says every value a
  generator gives is checked against its type; a census is not. One check in `census` would catch it.
- `luthier certify` of the regions pair takes about twelve minutes: the fold over regions and
  bindings is evaluated by the kernel for 108 cases per law.

## 5. What tester.py and generators.py must do (the code that follows)

Each item names the law it implements.

1. generators.py: numeric generators draw the special values with `Budgets.specialMass` and the
   atom at zero with `atomAtZero` (7.S4; section 4 of record/generators-2026-10-06.md): the bounds
   and their neighbours, 0, 1, -1, the literals of the law. Gives mass to the type's cases of
   numbers; no law in Luthier yet (numbers.lth), it serves `AnEmptyRegionLeavesBelowCases`.
2. generators.py: `gen_mat_of`, `gen_symmetric` draw dimensions from a list (0, 1, 2, 3, 5, 10 by
   default, 7.S5) and the zero and rank-deficient families with a share, so that
   `matDegeneracies`' and `symmetricDegeneracies`' cases get mass (`AnEmptyRegionLeavesBelowCases`,
   `TheThreeSourcesGrade`).
3. tester.py, classify: for each parameter whose type (or whose base type) has a `Degeneracies`
   declaration in scope, evaluate `casesOf` on every case drawn or listed and count per
   (binding, region FromType name) (`EachWitnessIsItsCase`: a case's witness is one listed value
   the tester may add to a census under `ExhaustiveMode`; `CaseNamesAreDistinct`: the counts key on
   the name). A case no value of a subtype meets is dropped from the law's regions.
4. tester.py, the law's regions: read the law's signature; a parameter of a cutoff type
   (`Tolerance`, `RankFloor`, `Sequential`, the types the demand supplies) gives the regions
   `above`/`below` (the value drawn just above and just below the cutoff; the generator draws a
   share there), a parameter of a subtype gives `boundary` (`Deriving`: `EachCutoffGivesTwoSides`,
   `EachPremiseGivesItsBoundary`, `OnlyTheLawsRegions`; `lawRegions` is the reference).
5. tester.py, branch coverage: the Runner records which branch of each `if` and `match` of the
   law's cone each case takes; one region FromCode per branch, named by the cone's name and the
   branch (`TheThreeSourcesGrade`).
6. tester.py / certify.py, the entry: record per entry the list of (region, n), the labels' field
   of 7.S9, from which `BindingEvidence` is read per binding (`RegionEvidence`; the gap noted in
   certification.lth §2).
7. certify.py, the grade: `grade` of a certificate becomes `regionedGrade` with the demand's
   combination, `orWeakest` by default, over the regions of items 3 to 5 and the evidence of item 6
   (`NoRegionsLeaveTheGrade`, `RefutedInEveryRegion`, `CombinesOverRegions`,
   `CombinesAcrossBindings`, `AnEmptyRegionLeavesBelowCases`); the demand's choice is a field of
   `Demand` (D-2026-10-16-k item 20 made per-law cutoffs typed fields).
8. tester.py, `cover` (7.S14): a law may ask a share for a region; checked with the sequential
   Wilson bound; failing it is a not-run with its reason, not a refutation. No law here yet.
9. tester.py, labels: an author's `classify` label is recorded with its share and never enters
   items 3 to 7 (`ALabelEntersNoGrade`).
10. tester.py, census validation: check every census value against the parameter's predicate
    (finding 1 of section 4).

## 6. One question

The empty region caps a binding at `Sampled` (section 3, second item). The alternative reading of
D-2026-10-16-i, that a region with no evidence leaves the law with no grade until the region is
reached, is one line in `regionGrade` (`nothing` in place of `capped`) and one control. Which do
you want?
