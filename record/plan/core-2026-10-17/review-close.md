# Review of the core's close, before the tag

Agent: Claude Sonnet 5.5, naive reviewer, 2026-10-22, brief `prompt-review-close.md`. Read-only but for
this file. Tree: HEAD c44d0e5 plus the working changes of the agent editing certification.lth,
certification_model.lut and their tests (read, not judged). `scripts/core_metrics.py -v` printed:
homonyms 0, executive shadows 113, list helpers 48, unclaimed 7, loose 1411 (real 1343, rest 68).
Scratch (not versioned): the session scratchpad, `m.txt` (the -v output), `hid.py`, `cls.py`.

## 1. The two accepted homonyms

`Unresolved`: holds, with one correction. laws.lth:252 (a `StatisticalVerdict` constructor) and
certification.lth:128 (an `Outcome` constructor) are different types. The host reads the first in
`tester.py:224` (`SETTLED_BY_TEST`), 1840 and 2434, and the second in `certify.py:982` and 1082; both
are written to the stores (`tests/test_certify.py:946`), so a rename is a store migration. The reason
in `ACCEPTED_HOMONYMS` says "two places"; it is about six. Minor. Both files can be imported together
(test_run.py:735 lists them as the clash), and nothing broke in the suite per bite 13b.

`scale`: holds. arrays_model.lut:39 is the top-level leaf `scale : Float64 -> Vec Float64 -> Vec
Float64`, there so that `operator` can bind it by name (its comment at line 59 says to write `scale c
v`), and plot.lth:167 is `scale (a : String) (s : Scale) (p : Plot)`. Both are imported by name in
different files (plot_laws.test.lut:22 against probability_controls.test.lut:39). The script's text
says arrays_model's `scale` is "the name the `Arrays` record gives its python extern": that is the
field at line 18; the homonym is the line 39 binding. Also, the cheaper side to rename is arrays_model's
(its sibling is `mscale`; two uses, probability_controls.test.lut:39 and 208), not plot's, which waits
for G1 to G5. One commit undoes it. Can wait.

## 2. The 48 list helpers

Core list functions available: `foldList` (right fold only), `fold`/`all`/`any`/`count`/`member`/
`lookup`/`sum`/`toList`/`filter`/`concat`/`zip`/`take`/`drop`/`nth`/`remove`/`removeAll`/`distinct`/
`insertSorted`/`sortBy`/`reverse`/`buildList`. No `foldLeft`, `takeWhile`, `find`, `findIndex`,
`nub`.

Could go with a core function (3):
- `probability.lth:269 allUnit`: the body is `all List (Vec Float64) unitVec vs`. Its comment says
  "kept as a recursion" but it is not one; it is kept because generators_model.lut and
  tests/test_tester.py import it. Replace the two imports and delete it. Before the tag, small.
- `certification.lth:463 overRegions`: the comment's reason ("a region that does not grade is skipped
  without a neutral element") is false. The `nil` case returns `k.grade (only b c)`, so this is
  `fold Region (Maybe Grade) comb (k.grade (only b c)) (fn r { regionGrade k c b r ev }) (filter Region
  grades rs)`; `overBindings` at line 477 already uses `fold` the same way. The other agent edits this
  file now, so it goes to them or after.
- `certification.lth:323 prepend`: a right fold into `Certificate -> Certificate` (`compose`, `id`,
  `fn x { withEntry x e }`). The comment concedes "the recursion is the clearer form", which is taste,
  not a reason the core cannot. Weakest of the three.

Reason holds (the core has no function for it) but the core is what is missing: about 20 of the
48 are left folds or early-stop searches that `foldLeft`, `takeWhile` and `find` would cover, and
their own comments say so ("the core has only the right fold": plan.lth:75, term_model.lut:29, 218,
386; "the core has no takeWhile": ebnf.lth:101). Left folds: `addNew`, `runFrom`, `placedBefore`,
`byLevels`, `demandAll`, `lastComponent`, `finishBindings`, `applyArguments`, `stageBindings`,
`unusedRebinding`, `itemsFault`, `remaindersSeq`, `disputes`, `bindingsFrom`, `sumOfLargest`. Searches:
`leftCallsSeq`, `longestPrefix`, `chooseArm`, `demandFields`, `demandTerms`, `pick`, `before`, `along`,
`behind`, `determined`. Strictly a right fold into a function does the left folds, so the "only the
right fold" reason is true of the core's surface, not of the language. D-2026-10-18-a's criterion
("hand-written recursions that a core function covers: 0") is met only because no core function
covers them. Worth saying to Luciano as it is; adding `foldLeft` and `takeWhile`/`find` to
core/lists.lut is the way to take the count down, and it is the queue's, not the tag's.

Reason holds, no change: the telescopes `fieldsNames`, `itemsNames`, `paramsNames`, `binderNames`
(program.lth:189-214), `telescopeFree` (term.lth:157), `renameAll` (term.lth:267, two lists at once),
term_model.lut `allNames` (a tree collector), 109, 117, 167-185, 207 (counter threaded through
entries), `badCitation` (program.lth:758, destructures the application spine, no iteration),
`swapAt` (plot.lth:509, a positional swap), the two broken controls in lists_controls (4.R3).
`anyTerm` (program.lth:442) is a false positive of the name family: it recurses over a term's
children, not a list, and its body uses `any`. Renaming it (`someSubterm`) takes it off the count.

## 3. The 7 unclaimed

Each is not a law. `withinOf` (numbers.lth:62) and `within` are balls used inside laws' bodies
(probability.lth:83); `isConverged` (optimization.lth:115) a predicate on a stop reason;
`hasColumn` (tables.lth:81) a refinement guard used in the types of `intAt`, `realAt`, `textAt`;
`sameTable` (tables.lth:109) the `eq` of the table's `Object`, claimed through `TableIsAnObject`;
`controlPasses` (test.lth:95) the definition "a control passes when refuted"; `top`, `bottom`
(core_instances.lut:78-79) fixture constants. The check flags a Bool-typed name no other body of its
own file mentions, so the cause is the file split, not a missing law. One could ask for a law of
`withinOf` (a ball with a symmetric radius is symmetric); not a tag matter.

## 4. The loose notice's narrowing

Seed 20261022 (python `random.seed`, `random.sample` over the 1343 `loose real` lines in file order of
`core_metrics.py -v`). The 20: runFrom, rowNameUnique, GramGivesPsd, combineList, known, RunStore,
MetricWithin, NamedProduct, VecOf, stepPatternList, KernelApplies, hasKey, Surjective,
AppendAddsLengths, maybeName, remainder2, rankAmongKept, conj, IntNeutral, programWithData.
Ten are functions (runFrom, combineList, known, stepPatternList, hasKey, maybeName, remainder2,
rankAmongKept, conj, programWithData). Ten are not: six are parametrised laws (rowNameUnique,
GramGivesPsd, KernelApplies, Surjective, AppendAddsLengths, IntNeutral) and four are type or theory
constructors with parameters (RunStore, MetricWithin, NamedProduct, VecOf). `looseFunction`
(check.py:1055) fires on any definition with binders. Over the whole 1343 (the 107 in
certification.lth did not parse when I classified, the other agent's edit in progress) 424 are
Bool-typed and 73 record-typed, so at least 37% of "real" are laws or theories, not functions at a
bare exponential. 4.S17 and the plan say "a function"; the count is inflated, not a finding of
a missing law. Worth correcting the predicate (exclude Bool-typed definitions and record or `U`-typed
ones) or the wording of "the loose notice only where real", since "1343 real" will be read as 1343
loose functions. Can wait, but do not quote 1343 as functions in the tag note.

The other direction (what the narrowing hides): 1986 definitions fire the old predicate, 575 are
absorbed. A sample of 20 of the hidden (same seed): all laws or functions named by a theory's
composite (LogOfOne, LambdaTree, NotRunAddsNothing, ...), correctly absorbed, but one is not:
`certification.lth:301 record` (a `Store k` function) is hidden only because `Recording` (line 866)
has a field named `record` with another type. The same coincidence hides seven in all: `record`,
`pick` (generators.lth, a field of `WeightedSupport`, plausibly intended), `symmetricOf` and
`orthogonal` (generators_model.lut), `coord`, `facet`, `labels` (plot.lth, fields of `Plot`). The rule
"the name of a record's field" absorbs a same-named top-level function without checking it is that
field's model. Nothing important hidden; the notice is still reported by name coincidence, so tighten to
fields of a theory the function is typed as a model of, or note it. Spec 4.S17 (04-static-semantics.md:318)
still says a bare-exponential definition is loose, with no word of the narrowing; the narrowing is in
check.py and the plan only. Can wait.

## 5. Three renames of bite 13b, old name grepped across src, examples, tests, docs

No code or string use of an old name remains (the Python hosts read neither `Demand`, `Record` nor
`Resolution` as strings; `Drawn`, `Interval`, `Support` are certification.lth's own constructors,
unchanged). Stale mentions, all comments or docstrings:
- `Resolution` to `StepResolution` (probability.lth:66): examples/sonolocalizacion/distances.lut:11
  still says "a `Resolution` (probability.lth §1)". generators.lth:254 keeps its own `Resolution`, which
  is a different thing; the comment is easy to misread either way.
- `Record` to `RunRecord` (demand.lth): src/luthier/run.py:2012, 3188, 3319, tester.py:2097,
  tests/test_tester.py:407 (alias `Record`).
- `Demand` to `ConeDemand` (certification.lth): demand.lth:37 and 116 ("certification.lth's its
  `Demand`"), run.py:2367, certify.py:809 (`Demand.combine`). demand.lth has its own `Demand` (line 106);
  run.py:1960, 3037 mean that one and are right.
- `Store` to `RunStore` (demand.lth): run.py:3399 ("its `Store`'s `OneIdentityOneResult`"), and
  `State` to `WorldState`: tests/tester/world_laws.test.lut:6, 109, tests/test_tester.py:407.
  certify.py:20, 598, 632 (`Store`) and 1468 (`State`) mean certification.lth's, which still exist.
About a dozen comment lines. None breaks anything; they send a reader to a name that now means
something else or nothing.

## What must change before the tag

Nothing that fails a check or a test. If Luciano wants the end criteria true as written, three small
edits: delete `allUnit` (item 2), replace `overRegions` by `fold` over `filter grades` (item 2, in
certification.lth, after the other agent), and fix the stale comments (item 5), say one commit.

## What can wait

The tag note should say the 1343 loose count includes about 37% parametrised laws and theories
(item 4); `looseFunction` narrowed to functions, and its field-name coincidence (7 hidden), and 4.S17's
wording. `foldLeft`, `takeWhile`, `find` in core/lists.lut would remove about 20 of the 48 kept
recursions (item 2), a decision for the queue. Rename arrays_model's `scale` to retire the accepted
homonym (item 1). `prepend` as a fold. A law for `withinOf`.

## Decisions I took on my own

Seed and sample method (item 4); looking at the hidden side as well as the reported one (item 4);
nothing else. No decision for `record/decisions.md`.

## Before the tag: cleanup

Commits (brief prompt-pre-tag-cleanup.md): bb5e40e deletes `allUnit` (generators_model.lut,
tests/test_tester.py and `UnitList` use `all List (Vec Float64) unitVec`); 2846405 `overRegions` as
a `fold` over `filter List Region grades rs` and `prepend` as a fold into `Certificate -> Certificate`
(`compose`, `id`); d347991 the stale names in the 13 listed comments and docstrings; 7f7ad86 the eight
stores that moved (arrays, arrays_model, certification, certification_model, generators_model, laws,
probability, probability_model).

Certification: `luthier certify` over the 44 files of tests/tester, one at a time, twice. First pass
76 lines ran; second pass 0 lines ran, 44 files. Exit 1 on belief_laws, cases and laws: their
output is the same on both passes (known refutations and uncontrolled notices, no store changed
for them); I did not look further. Outputs in ~/.cache/luthier-cleanup/pass{1,2}-*.out.

Suite: every tests/test_*.py file by itself under `timeout 1800`; all pass (test_certify 70 passed,
test_run 146, test_elaborate 69, test_tester 24, and so on). test_check_private collects no tests
(rc 5), as before. Outputs in ~/.cache/luthier-cleanup/suite-*.out.

`scripts/core_metrics.py`: homonyms 0, executive shadows 113, list helpers 45 (was 48), unclaimed 7,
loose 1407 (real 1330, rest 77; was 1411, 1343, 68). The total and the real count are down; "rest"
is up by 9, which I did not trace.
