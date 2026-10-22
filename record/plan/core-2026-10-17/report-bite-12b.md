# Report: the core's bite 12b, the library and the examples

Agent: Claude Opus 5.5, brief `prompt-bite-12b.md`, 2026-10-22. Started at 76818b6, alongside bite 12a's agent, so the commits are interleaved. Committed by the coordinator from the agent's hand-back (the agent's Write was refused for report files). Scratch files are under `~/.cache/luthier-12b/` and not versioned: `run_pass.sh` with one log per program in `pass1/` and `pass2/`; `run_pytest.sh` and `pytest/`; `runs/`, the logs of the three runs; `metrics-*.txt`. The witness searches are versioned in `record/plan/core-2026-10-17/witness-12b/` (seed 20261022).

Commits: source a8035e9, 61c14fa, f04efb4, 310e7bf, 7544f6d, 232b997, c5bf74a, 032a2ec, f3f78d6, 3be5f96, a77d3cd; stores cedaf9f, 7e303d8; run records and the runs' store entries 44532ce, f9a6e27; witness search ca0f235.

## What was built

- probability.lth. The list helpers are the core's: `valueSums` is a `fold`; the pooled values are `concat` of each vector's entries, sorted with `sortBy`; the distance is a `foldWith` of `larger` (a maximum, so the fold's order doesn't change it); `reverse` replaces `reverseOnto`, and `allUnit` uses `all`. Gone: `entriesOnto`, `pooled`, `insertSortedValue`, `sortedValues`, `lengthOf`, `kolmogorovFrom`, `reverseOnto`. `KolmogorovOfMultiset` and `KolmogorovAgrees` are the core's `Pointwise`. New §6, the pushforward of a distribution along a function (D-2026-10-17-g): `Pushforward (A : U) (B : Concrete) (f)`, a sampler pushed draw by draw; its law `PushedDraw` says the pushed draw is `f` of the draw, with the same seed after it (Billingsley 1995, eq. 13.7, cited in the file). The model `pushGen` and the claim `PushingDraws` are in probability_model.lut, with one law line and one control (a push that forgets `f`). Old and new definitions compared on two vectors: the distance and `valueSums` agree with the old definitions and with numpy's.
- belief.lth and optimization.lth. Renamed to remove clashes: `negate` to `asObjective` (the core's `Ring` has a `negate` field), `Reason` to `StopReason` (checks.lth has its own `Reason`), optimization_model.lut's `host` to `hostStep` (world_model.lut has a `host`). Laws no conjunction named are gathered in `LMStepOnQuadratic` and `MaximizerComparisons`, as arrays.lth gathers `ArrayContainers`.
- plot.lth (helpers only; G1 to G5 untouched). 14 helpers gone: `appendLayer`, `dropTable`, `appendTable`, `dropScale`, `allLayers`, `anyLayer`, `allStr`, `isNilStr`, `lookupStr`, `lookupTable`, `lookupScale`, `nthLayer`, `appendStrs`, `allScales`. `keysOf`, `namesOf`, `rangeOver`, `replaceTable` and the three `same...` comparisons are rewritten over `map`, `fold`, `zip` and `all`. `swapAt` stays: a positional swap, which no core function does. plot_model.lut's `dropFile` is a `filter`.
- examples/sonolocalizacion. positions.lut: `LayoutIsAnIsomorphism` is the core's `Isomorphism` of `flatten` and `unflatten`, at `MatOf 3 n` and `VecOf (3 n)`, under arrays.lth's equalities; the two functions are parameters with the layout's as defaults; algebra.lth's `Iso` alias and its two laws are gone. distance_graph.lut: the measurements joined with the nodes are the core's `Pullback`, one claim per end (`JoinOnFirstEnd`, `JoinOnSecondEnd`; models `firstEndJoin`, `secondEndJoin`), each with a law line on session A's graph (66 cases) and a control that reads the other end, refuted; `rowCells` is a fold. distances.lut: `append` became `pushEntry`. figures.lut: `appendNames` became `<>`. Renamed to remove clashes: `Node` to `NodeOf`, `point` to `nodePoint`, `dOf` to `measuredOf`, distance_graph's `cellText` to `showCell`, figures' `rankOf` to `rankAmongKept`, `Report` to `FitReport`, the two `summary` to `fitSummary` and `graphSummary`, distances' `positions` to `meanOfDesign`, plot_cases' `bind` and `names` to `bindTo` and `tableNames`.
- arrays_controls.test.lut, the "bound too small" control: a `Doubles` model with a third of the machine's epsilon turns `3 gamma n` into `gamma n`. Random draws never get that close, so a witness was searched (search.py, 20,000 draws): at draw 5438, three products whose right fold and numpy's left-to-right sum round apart by more than `gamma 3` times their magnitudes. That witness refutes `DotAgrees`, `MatVecAgrees`, `MatMulAgrees` and `TraceAgrees` at epsilon/3; all four pass at the machine's epsilon. No bound was changed.

## Findings

1. `Doubles (F : U)` can't be written as decided (bite 12's "Also" of 2026-10-21). Rule 4.R6 of check requires the conjunction to be a predicate over `Doubles F` with `F` a parameter; rule 4.R9 then refuses every conjunct, since they are stated at `Float64` (`Moderate`, the literals 0.0 and 1.0, `PlusMonotone d` at `Doubles Float64`). With the conjunction written at `Doubles Float64`, 4.R6 refuses it instead. The edit was reverted: `Doubles` is unchanged, and `plus` and `times` still don't resolve at `Float64`. See the question.
2. Two summing laws have no "bound too small" control. `MatMulTransposes`: numpy computes both sides in the same order (bitwise equal on 3000 drawn pairs), so no bound of any size can be refuted. `TraceCyclic`: over 150,000 draws of seven shapes, the largest error seen was 0.64 of `gamma (r + c)` (cyclic.log). Both remain controlled by their wrong models only; their law report still says "uncontrolled ... its controls are at another hash of its cone", as report-verify-6-11 saw for all six. The other four now read controlled.
3. The core's generic functions don't reach `Vec`'s claims: `toList Vec Float64 v` takes `v` as the `Foldable` model instead of filling it, while the field `fold` does resolve at `Vec`. probability.lth uses `fold` directly.
4. `size` at `Mat Float64` and at `Table` (claims made at one shape or schema, bite 11's finding 1). The examples' uses left on the old fields: `m.m * m.n` once, in positions.lut's `flatten`; `t.nRows` 71 times (distance_graph 50, experiment_zero 11, figures 7, validate_graph 3).
5. Already refused by check at the base (76818b6), not caused by this bite: distances.lut `pairI` and `pairJ` (4.R9, an `Int` where `Fin nodes` is asked); plot_cases.lut `perms` (4.R9); lists_controls.test.lut (4.R3); experiment_zero.run.lut (4.R2, bite 13's).
6. belief_laws exits 1: `PrecisionSymmetric` on session A's prior is "not run: maximum recursion depth exceeded", the same entry as on 2026-10-21. The plain sampled line still has no generator of `GaussianBelief` (7.R4).
7. `allUnit` had to come back (a77d3cd) because generators_model.lut and tests/test_tester.py import it. Its body is the core's `all`, but its name makes it count as one list helper.

## Checks

- Certification: `luthier certify --jobs 1`, program by program, 40 programs, 3 areas at a time. Pass 1, after 12a's report: 191 lines ran in all; the longest were probability_laws (35 lines, 56 min), sonolocalizacion_laws (7 lines, 22 min) and arrays_laws (10 lines, 22 min). Pass 2: 0 lines ran for every one of the 40. Exit code 1 only for cases.test and laws.test (fixtures refuted on purpose) and belief_laws (finding 6).
- New lines: every new law line is graded and every new control refuted (the four bound-too-small controls, `PushingDraws`, `LayoutIsAnIsomorphism` with 2 conjuncts and 200 sampled cases, the two joins).
- Runs, after 12a's follow-up (012b3ce): validate_graph prints "valid: 10 nodes, 22 measurements, 21 distinct pairs; ... 14 (of which 10 are the heights and 3 the rigid motions of the plane)", the same as its records. experiment_zero on A (record 17's parameters) and on A without A2 (record 19's): the output matches the record line for line, but the three `== <outDir>/...` header lines; sigma is 0.23547527629512058 and 0.02214295792547442. The cone changed, so the keys are new. The follow-up refused no demand in any of the three runs.
- Suite, file by file under `timeout 1800`, LUTHIER_SLOW tests skipped by their marker: 42 files, none failed. test_run 146 passed, test_certify 58, test_elaborate 67, test_tester 23. test_check_private collects nothing (rc 5).
- `python scripts/check_spec.py`: only its known finding (03-kernel.md:192).
- `luthier check` on every file of lib, examples and tests/tester: only finding 5's refusals.

## core_metrics (scripts/core_metrics.py)

| count | before (76818b6) | after (ca0f235) |
|---|---:|---:|
| (1) homonyms | 58 | 44 |
| executive shadows | 107 | 107 |
| (2) list helpers | 219 | 185 |
| (3) unclaimed | 31 | 21 |
| loose | 1995 (real 1346) | 1979 (real 1334) |

What's left, with reasons:

- (1) Homonyms, 44. None is between two of this bite's files. Three cross into machinery files: `Resolution` (probability's central difference against generators.lth's binding resolution), `uniformPValue` (generators.lth declares one, probability.lth defines another), `pi` (grammar.lth's). `larger` is also in certification_model.lut and core_instances.lut: one join of `Float64`'s order belongs in the core (plan 5.1). plot's `Drawing`, `contains`, `scale` and `withData` are plot's public names, which wait for G1 to G5 (D-2026-10-17-h). Of the rest, 7 are the core_instances.lut fixture's and 30 are between machinery files (certification, demand, grammar, term, translation, program, laws, world), for bite 13.
- (2) List helpers, 185. Of this bite's files only `swapAt` and `allUnit` remain (finding 7). The rest are bite 13's search-style recursions: program.lth 64, term_model.lut 25, certification.lth 20, plan.lth 14, and so on.
- (3) Unclaimed, 21. The only one in this bite's files is optimization.lth's `isConverged`, a predicate, not a law; the count reads every Bool-typed definition. The rest are in generators_model, plan, demand, tables, test.lth and core_instances.

## Decisions taken on my own (one commit undoes each)

- `Pointwise` rather than `Congruent` for `KolmogorovOfMultiset`: the same statement, and it needs no generator of related pairs.
- The pushforward stated over samplers, per draw, with `B : Concrete`; its claim gathered in `ProbabilityModels`.
- The join as one `Pullback` claim per end, with the model a function of the graph so that a control can pass a wrong one; `nodeIndex` reads a node row as its index.
- Unclaimed laws gathered in unannotated conjunctions: `LMStepOnQuadratic`, `MaximizerComparisons`, `DistanceLaws`, `GraphLaws`, `LayoutClaims`, `ProbabilityModels`.
- The renames listed above, each to remove a clash with another file or a core field name.
- The bound-too-small witness listed rather than drawn, as numbers_controls does.
- `Doubles` left unchanged after finding 1.

## Question

`Doubles (F : U)` is refused by check (finding 1): its laws hold only at `Float64`, and a structure with a carrier must state its laws over that carrier. How should `plus` and `times` resolve at `Float64`? (a) check accepts a structure whose laws fix its carrier, with the conjunction written at `Doubles Float64`: this changes 4.R6 in check.py and the spec. (b) the core's within-bound semiring, claimed at `Float64`: bite 8's option (b), which loses the `Moderate` and `Tame` ranges. The agent would take (a): the laws stay as written, at the cost of one rule in check and one sentence of 4.R6.
