# Report: the rest of the external review that does not wait for Luciano

2026-10-15, by Claude Opus 5.5, an agent of the coordinating session, on `prompt-second-line.md`
of this folder (fd2baa8). Inputs: `summary.md` and `summary-BCD.md`; the four fix reports of this
folder; `record/IA/controls-2026-10-15/report-*.md` and `record/IA/statistical-2026-10-15/report-*.md`
for what was closed before; the theory files at fd2baa8. Every change to a theory is marked
`[proposed]` in its file, one commit per file.

## Accepted when

- Changed files parse and check clean: laws.lth, certification.lth, certification_model.lut,
  demand.lth, plan.lth, test.lth, generators.lth (`luthier parse`, `luthier check`, exit 0). A
  sweep of `luthier check` over every `src/luthier/lib/*.lth`, `*.lut`, `tests/tester/*.lut`,
  `examples/*.lut` and `examples/sonolocalizacion/*.lut` at 3716a9b: all clean but
  `examples/sonolocalizacion/distances.lut:46-47` (4.R9 `pairI`, `pairJ`), which fails the same
  way at fd2baa8, before any change of mine.
- `python3 scripts/check_spec.py` prints nothing (it printed one finding at fd2baa8, a run of
  eleven words of 7.S17 repeated in docs/principles.md; reworded in b986747).
- `python -m pytest -q`, alone: 710 passed, 5 skipped, 9 xfailed (4 min 28 s).
- `luthier certify tests/tester/generators_laws.lut tests/tester/generators_controls.lut --jobs 2
  --fuel 100000000`, with stores, before the suite: exit 0, every line known (the cones of the
  certified laws did not change), 7 laws controlled, CONTROL FAILED 0 times; no store changed.
  generators.lth is the only changed theory with a `_laws.lut`; laws.lth, certification.lth,
  test.lth, plan.lth and demand.lth have none.
- Scratch probes (session scratchpad, not committed), each through `luthier test --no-cert`:
  the model's `transport` holds the four transport laws and a transport that ignores the link is
  refuted on `TransportNeedsTheIdentity` and `TransportTakesTheWeaker`; `PlanIsConfluent` holds of
  `planning` on `example` and is refuted on a dataflow whose `b` reads `c` unlisted, at choices
  [0, 1, 0, 0]; `ProportionalToWeight` holds of `supportOf [(x,1),(y,1),(x,1)]`; a filter that
  never moves the seed is refuted by `DrawIsTheFirstKept`.

## Commits

0eaa1f3 laws.lth; 5fc1e4d certification.lth; 6a45a6f certification_model.lut; ec21438 demand.lth;
520c1ad plan.lth; 3b540bd test.lth; 1636b17 generators.lth; c2d0ba2 spec 6; b986747 spec 7;
1894070 spec 8; 3716a9b spec 10.

## Every finding and its state

"Before" names the commit that closed it; "Luciano" names his open question; "left" says why.

### summary.md

| finding | state |
|---|---|
| W1 Host held to what it supplies | before: 2ac8f12, 44578c4, 2be25d3; the observer's fidelity is an axiom, its default price Luciano's (the observer assumed) |
| W2 laws act and drop the token | before: 2ac8f12, 2be25d3 |
| W3 extern's declared type | before: 2ac8f12 (`Route.declared`, `NoLawNoGrade`) |
| W4 RecordCrossesByField | before: 2ac8f12 |
| W5 provisional applied vs refused | Luciano: the provisional extern |
| W6 implications over a type | misreading (Fable's reading, adopted by the summary) |
| W7 OwnIsIdempotent and the result | before: 2ac8f12 |
| W8 `settled` constant | before: 2ac8f12 (the demand's `accepts`) |
| W9 Persistence and the disk | Luciano: the observer assumed; the representation's laws have a model and controls (cfd4188) |
| W10 one case at the first application | Luciano: the one-case first action |
| W11 smaller points | before in part (observe an action, 2ac8f12; the place named, 2be25d3); left: a description reading an undeclared place fails safe, and `World` as alias and `hash` unused are cosmetic |
| M1 the three routes, "stdout" file | before: 2ac8f12 (premise in `HostAgreesReadFile`) |
| M2 "stdout" special-cased | left: one map of places changes world_model's `State` and host.py's `observe`, a specimen bite |
| M3 pure part satisfies its laws | no finding |
| M4 token comment | before: 44578c4 |
| C1 grade underdetermined | before: 262d3d3 |
| C2 implications over a type | before: 262d3d3; here ec21438 (demand.lth's `LoweringLosesNothing` on the new domain) |
| C3 `record` on a known identity | Luciano: the replay in the identity |
| C4 budgets in the identity | Luciano: the budget in the identity |
| C5 a current failure bypassed | before: 262d3d3, 82c4cb4, 2be25d3 |
| C6 grade tied to nothing | before: 262d3d3, 9a348b9 |
| C7 transport takes any standing | here: 5fc1e4d, 6a45a6f (a `Link` names the two names; nothing from another law); the shared distribution of two sampled links waits for the cost types (D-2026-10-13-m) |
| C8 the store's writer held to nothing | left: certify.py's reader and writer as a model of `Store` need a specimen bridge (with CM3) |
| C9 roles of `Value` | before: 262d3d3; the payload strings minor |
| C10 HashSees* injective | no finding |
| C11 latest in front | before: 262d3d3 (the date order a hole) |
| C12 Certificate holds no domain | misreading in part; the rest is S6-1 |
| C13 a name with no laws never refused | before: 2ac8f12 (`NoLawNoGrade`: an extern with no law gets no grade, so is not applied) |
| C14 one identity, two grades | here: 5fc1e4d; Grok's two claims misreadings |
| CM1 no law of Certifying broken | no finding |
| CM2 NaN in meet | no finding (11.S7) |
| CM3 the specimen described, not held | left with C8 |
| CM4 `hashing` an extern | no finding |
| S10-1 10.S5 two applications to one token | here: 3716a9b |
| S10-2 tested before applied vs agreement | Luciano: with the one-case first action |
| S10-3 one case serves the run | Luciano: the one-case first action |
| S10-4 10.S12 against 6.S14 | Luciano: the provisional extern (O3) |
| S10-5 own actions memoized and the token | left: which token follows a memo hit is a decision of 10.S6, no wording fix |
| S10-6 no obligation on observation | before, with W1 |
| S10-7 10.S13's heading | here: 3716a9b |
| S6-1 chapter 6 before D-2026-10-14-c | here: c2d0ba2 (6.S16 states the Boolean slice and names the file) |
| S6-2 ⊤ refused by every cutoff | left: whether ⊤ may be a cutoff is a decision of 6.S15; the Boolean slice refuses failures by `OnlyAPassServes` |
| S6-3 two cost types left to the library | here: c2d0ba2 |
| S6-4 "up to four" | misreading |
| S6-5 6.S8 against 6.S15 | Luciano: as C3 |

### summary-BCD.md

| finding | state |
|---|---|
| B1 the record drops the decoration | Luciano: the record as memo key |
| B2 `determined` too strong | Luciano: the record as memo key; the identity a parameter before (984558b) |
| B3 NoPriceRefusesAssumed has no price | left: the price waits for the cost types (D-2026-10-14-c) |
| B4 delta and decoration fixed | left: the file states why; a demand for `P T` waits for O5 |
| B5 delta not passed down | left: `delta` is `nothing` in this draft; the sequential cutoffs reach a law through the test's binding (D-2026-10-15-b) |
| B6 defaults as cutoffs | no finding |
| B7 placedBefore | before: 1f3464a |
| B8 Planning over any Dataflow | before: 1f3464a |
| B9 Strategy roles | before: 1f3464a |
| B10 default CallByNeed | left: marked [proposed] with its reason; changing it changes run.py, a decision on 8.S3 against 8.S4 |
| B11 Confluent over drawn schedules | here: 520c1ad |
| B12 KeySees* one coordinate | left: as C10; a joint-change law is another law |
| B13 KeyReadsTheType tautology | here: 520c1ad (both key statements unclaimed) |
| B14 no law ties the key to the run | Luciano: the record as memo key |
| B15 no Keying model | no finding |
| B16 planning not a model | before: 3fc9870 |
| B17 chapter 8 stale | here: 1894070 (8.S4, 8.S11); 8.S1's cost-valued cutoff left, read through 6.S16 |
| B18 by need computes the same subgraph | left: at the level of the reads the two agree (`TheDefaultsAgree`); what a branch skips is below the graph |
| B19 Demanding empty | before: 984558b, 6b119fe |
| B20 planOf uses only the entry | here: 520c1ad |
| B21 key values not canonical | left: a canonical order needs an order on `String` the kernel lacks (as the store's dates) |
| B22 the strategy in the demand | left: 8.S1's list, a decision of the spec |
| B23 per-law cutoffs in `Demand` | Luciano (the summary's question) |
| B24 8.S11's list omits laws | left: whether the model enters by plan hash or cone is a decision of 8.S8 |
| G1 Random universal over seeds | before: f442e00 |
| G2 Translates, Scales exact == | here: 1636b17 |
| G3 Metric laws do not separate | left: the log conjugacy needs `log` in the theory, and `power` is still declared |
| G4 ProportionalToWeight, duplicates | here: 1636b17 |
| G5 Filter's seed | here: 1636b17 |
| G6 where type binding vs profile parameter | left: 7.R1's rule, a decision of the spec |
| G7 dependent without redraw | left: needs an emptiness test of `B x` the theory lacks |
| G8 rare premises (CensusFirst) | left: needs a dependent domain of seeds the tester builds |
| G9 masses above 1 | here: 1636b17 |
| G10 LogScales's `m` | misreading (`l.metric`) |
| G11 missing generators | left: tester work |
| GM1 masses in the value | left: moving them to the demand changes every family's line and certificate; whether a family's domain constant is a cutoff is A3's criterion |
| GM2 families claim more | left: a distribution claim (Haar) is a statistical law of 7.S1; the family laws take the family and have controls (8c6aef6, 7aeab97) |
| GM3 UniformSampleIsUniform Boolean | before: 1283a12, d55ef9c |
| T1 specCoverage | left: needs the law's parameters, which `TestSpec` does not hold |
| T2 the always-NotRun tester | left: what a tester must run depends on generators the theory does not see |
| T3 RunIsPointsOrNotRun | here: 3b540bd |
| T4 Confirmed with Bounded | Luciano: 7.S10's Bounded |
| T5 gradeRank not by evidence cost | left: L10.2's order without a domain, the spec's |
| T6 Grading restates grade | Luciano: 4.R3 over a library (the night plan's Questions) |
| T7 mode has no default | left: the default needs `linear`, generators_model.lut's; a theory importing a model is a layering choice |
| T8 defaultBudgets constants | Luciano (criterion) |
| T9 Mode and Grade roles | Luciano: with T6 |
| L1 NotFlips and CitedWhole | here: 0eaa1f3 |
| L2 ForallOnPoints | here: 0eaa1f3 (and `EitherBySide` on a supported side) |
| L3 Exhaustive forgeable | left: confirming needs the enumeration of `A`, which `Settling` does not take |
| L4 combine underdetermined | here: 0eaa1f3 (`CombineNeverConfirmsMore`) |
| L5 `(A : U)` inside a law | left: a rule for 7.R2, the spec's |
| L6 isSymmetric implications | left: the file tells clients to quantify over related pairs; templates over subtypes change numbers.lth's certified cones |
| L7 Coverage payloads | left: `Bounded`'s box is T4's question |
| L8 older than D-2026-10-14-c | before in part (laws.lth §4, 2d4519e); 05-laws.md not re-read |
| S7-1 7.S12 vacuous vs not run | left: two decided sentences; which wins is a decision |
| S7-2 3/n above 1 | here: b986747 |
| P1 IsGradient | before: 7801a3f |
| P2 info bound weakly | left: the Bartlett identity waits on the sampler; zero information controlled (a14bc0c) |
| P3 InfoNonNegative sampled | left: arrays.lth §4's own caveat |
| P4 profiled at zero residual | left: unreachable on drawn data (Fable); a subtype changes the fit's cones |
| P5 KolmogorovAgrees vs 4.R10 | left: not sure, 4.R10 not re-read |
| P6 tailSeries cutoffs | Luciano: the tailSeries cutoffs |
| P7 UniformAtLevel | before: 2da386c |
| P8 laws outside a conjunction | before in part: 10a433c; whether a Bool definition outside one is tested is the spec's |
| BE1 QuadraticConverges | before: 31e9b65, f717a7e |
| BE2 MaximizerStationary vacuous | before in part (`giveUp` refuted, b777faf); `MaxResult`'s reason left |
| BE3 negative information | before: 31e9b65 |
| BE4 `y : Vec` vs `VecOf` | left: retyping changes the fit's certified cones and experiment_zero, a bite with its re-certification |
| BE5 laplaceUpdate drops converged; Fisher | Luciano: a design question (the summary's) |
| BE6 damping schedule the host's | left: with BE4 |
| BE7 a maximizer law beyond the quadratic | left: a new family of laws, a bite of its own |
| O1 StepRule | before: ffc7d31 |
| O2 StepRule over any state | left: report-fix-BCD.md decision 4 |
| O3 Reason and isConverged | misreading in part (Fable: alias); `Run`'s reason is a theorem of `minimize` |
| O4 QuadraticStepAccepts in floating point | left: moot if `Damping` is the demand's, the not-sure |
| O5 DirectionAgrees native | no finding |
| OM1 lmMaximizer vs QuadraticConverges | before: 31e9b65 |
| OM2 native at large damping | left: as O4 |
| A1 RankUnderRotation | left: quoted, not re-run |
| A2 RankScales underflow | left: quoted, not re-run |
| A3 eligibility constants | Luciano (criterion) |
| A4 pinvSym on an indefinite matrix | misreading: a zero pinv fails `PinvOfIdentity` (controls, 331f4e3) |
| A5 diagonals only | before in part: symmetric and gram families in the controls (aa514b8, 8f4a02c) |
| E1 covFloor, bandLevel | left: experiment_zero.lut is the slice's program, run by Luciano |

## Counts

130 findings: 19 fixed here, 34 fixed before (some in part), 20 waiting for Luciano, 6 a
reviewer's misreading, 8 no finding, 43 left with the reason above.

## Decisions I took on my own

- A transport `Link` record (`from`, `to`, `standing`) and `transport : Standing -> Link -> Maybe
  Standing`, the law `TransportNeedsTheIdentity` over any link and the others over `LinkFrom`.
- `ForallOnPoints`: every point confirmed or supported gives `Supported`, also under `Exhaustive`
  when some inner point is only supported; `EitherBySide` keeps a supported side.
- `NotFlips` exempts citations and assumptions; `CombineNeverConfirmsMore` added.
- `PlanIsConfluent` takes the strategy and a list of choices, comparing the plan's schedule with
  `linearization`; `KeyReadsOnlyTheCone` and `KeyReadsTheType` kept as definitions, not claimed.
- `dataflowOf` takes the demand.
- `RunIsPointsOrNotRun` refuses only `Cited` and `Assumed` (name kept, for its clients).
- generators.lth imports numbers.lth's `Tolerance` and `within` for `Translates` and `Scales`.
- Spec wording: 10.S5's row, 10.S13's and 6.S16's headings, 6.S16's Boolean slice under
  D-2026-10-14-c, 6.S5's last sentence, 7.S11's cap at 1, 7.S17's reword, 8.S4 and 8.S11.
