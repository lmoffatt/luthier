# Items 1, 2 and 4 of summary-BCD.md, and B19: report

2026-10-15, by Claude Opus 5.5, an agent of the coordinating session, on `prompt-fix-BCD.md` of
this folder and the coordinator's addition to it (after 69aa416: `Dataflow` a theory first;
`Demanding` in demand.lth an empty theory, demand.lth and demand_model.lut added to the files).
Every change is marked `[proposed]` in its file. Commits, one per file:

- 7801a3f probability.lth: `IsGradient` along a drawn direction `v`.
- 31e9b65 belief.lth: `PosteriorScoreIsGradient` along `v`; `PosteriorInfoNonNegative` added to
  `Posterior`; `QuadraticConverges` takes `budget`.
- ffc7d31 optimization.lth: `GradIsGradient` along `v`; `StepRule` determined.
- 1f3464a plan.lth: `placedBefore`; `Dataflow` a theory; the strategies' role laws.
- 3fc9870 plan_model.lut: the model follows; `["d","b","c","a"]` refused.
- 984558b demand.lth, 6b119fe demand_model.lut: `Demanding` gone, `Store` in its place.
- 2439bd0 belief_model.cert.json: derived, lm's `QuadraticConverges` re-certified (below).

## What changed

Item 1. `IsGradient n r f g t v` compares the central difference of `f` along the unit vector of a
drawn `v` with `dot (g t) (v/|v|)`, at the scale `1 + |f t| + |g t|` (as before with `|g t|`).
A zero `v` passes, as in `IsJacobian`. The four consumers take the extra `v`: `DLogSigmaIsGradient`,
`ScoreIsGradient`, `PosteriorScoreIsGradient`, `GradIsGradient`. The test files did not need to
change; the tester draws `v`.

Item 4. `StepRule` now computes the trial point `xt` from the model's own direction and its value
`pt := o.value xt`, and asks `accepted == (pt < st.phi)`; accepted, `x = xt`, `phi == pt`, the
damping lowered; rejected, as before; the iteration counted in both. That determines the step from
the direction. The state is still drawn whole, its `phi` unrelated to `x`; the law compares with
`st.phi` as given, which is what `lmStep` and lm.py read, so no subtype was needed.
`QuadraticConverges` takes `budget : Nat`, the iterations the demand grants a maximizer on the
family (P11), and asks nothing when `s.maxIter < budget`. `MaximizerStationary` is unchanged; its
comment now says it is vacuous for a maximizer that gives up and that `QuadraticConverges` is the
law that refutes that one. `Posterior` gains `PosteriorInfoNonNegative` (the quadratic form of the
information on a drawn direction, as `InfoNonNegative`), so `negate` is total.

Item 2 and B7 to B9. `placedBefore ns live placed s` asks each name's reads among `live` to be
in `placed` already; the fix Fable proposed, with `live` passed in. `Dataflow (A : U) (eq : A -> A
-> Bool)` is a theory with three laws: `NamesAreUnique`, `Acyclic` (no name in the closure of its
own reads), `StepIsLocal` (the step of a name gives one value on a drawn environment and on that
environment reset to `init` outside the node's reads). The equality is a parameter because 4.R8
gives no `==` on a type variable; checking it forced `init` into a law (4.R3: a theory touches every
field), which is why locality resets to `init` and does not draw a second environment. Every
function and law over a dataflow takes `eq` now; `dataflowOf` takes it too. Role laws of
`Strategy`, in `Planning`: `ForwardIsByLevels` (the levels along the forward schedule never fall, a
name's level one more than the highest of what it reads among the live names) and
`ByNeedIsFirstDemand` (the call-by-need schedule is `firstDemand`, the depth-first first-demand
order, now a definition in plan.lth). In the model, `byNeed` is `firstDemand`, `forward` places in
strict rounds (a round reads only what earlier rounds placed; the greedy version could place a
name and its reader in one round, against levels), and `readsIn`, `keepIn` are gone in favour of
plan.lth's `readsOf`, `keep`.

B19. `lawDemand` and `recorded` are definitions in demand.lth; `Demanding` and the model's
`demanding` are gone. The one law a model can break is now `OneIdentityOneResult` of a theory
`Store (K : U) (eq : K -> K -> Bool) : { runs : List (Stored K) }`. The identity is a parameter on
purpose: whether it is `Record` or plan.lth's `MemoKey` is item 5, Luciano's question, and the
comment says the law is false at `Record` (B2). `Run` and `Runs` are gone with it. No model file
gives a store (8.S10). `NoPriceRefusesAssumed` and `LoweringLosesNothing` stay as predicates over
`k : Certifying` alone, unclaimed here; their place is certification.lth, which another session is
editing.

## Results

`luthier parse` and `luthier check` on the five theory files and their models: clean (exit 0).

`luthier test ... --no-cert`, no refuted line in any of the four:

    probability_laws.lut: exit 1, no line refuted; 13 lines unsettled by fuel, all on distances.lut's
      posModel, nativeProfile, nativeFull (JacIsJacobian, TangentShapes, ScoreIsGradient,
      InfoSymmetric, InfoNonNegative, ProfiledIsGaussianAtItsSigma); session A's ScoreIsGradient
      and fullModel's DLogSigmaIsGradient, with the drawn v, sampled (ran), 20 cases each
    belief_laws.lut: exit 1, no line refuted; the 3 session-A maximizer lines unsettled by fuel,
      as at baseline (the baseline run before my change gave the same 15 lines); the two
      GaussianBelief lines not run, no generator, as at baseline
    optimization_laws.lut: exit 0, 12 lines sampled, StepRule on native and on host (lm.py)
      included
    fit_laws.lut: exit 0, 11 lines sampled

The unsettled lines in probability_laws.lut include laws I did not touch (`TangentShapes`,
`JacIsJacobian`), so the fuel limit is not mine; the cost is that the new `ScoreIsGradient` is
exercised on session A only. No refutation of lm.py.

The counterexamples, by a probe in the scratchpad that imports the library (not committed),
through the tester, seed 20261014, cases 20 (100 for the second):

    QuadraticConverges at a maximizer that returns { x0, converged = false }: refuted
    StepRule at `phi := pt - 1` (lmStep with phi lowered by one): refuted
    StepRule at "accept only on even iterations": refuted
    StepRule at native: sampled
    PosteriorScoreIsGradient at score := 0 on the quadratic: refuted
    PosteriorInfoNonNegative at info := -I: refuted

plan_model.lut, evaluated: `exampleIsADag`, `bothLinearize`, `agree`, `readersFirstRefused` are
true; both plans are a, b, c, d. A probe: `ForwardIsByLevels` and `ByNeedIsFirstDemand` hold of
`planning` on `example`; a two-node cycle is not `Acyclic`; a step that reads a name its node does
not list fails `StepIsLocal`; `byLevels` refuses a, b, d, c. tests/test_run.py's demand and plan
tests and tests/test_lm.py pass.

The fit. The first run was refused, with and without `--accept assumed`: `lm: QuadraticConverges:
stale` (the law's cone changed with `budget`). I re-certified it with `luthier certify --deep
tests/tester/fit_laws.lut` (without `--deep` the line was known in the untracked test store and
the model's store was not written); belief_model.cert.json changed and is committed alone
(2439bd0). Then, with no `--accept`:

    PYTHONPATH=src python3 -m luthier.cli run examples/sonolocalizacion/experiment_zero.lut
      --set graphDir=examples/sonolocalizacion/A/graph_noA2 --set outDir=<scratch>
      --set lmMaxIter=500 --set lmTol=1e-6 --set lmFloor=5.995204332975845e-15 --fuel 100000000000
    nodes 9, measurements 19, sigma 0.02214331908164216 m, nu 4.471102722862414, transform of the
    residuals: Kolmogorov distance 0.17285053266082867 over 19, tail probability 0.5794153448510095

The same line, to the last digit, as the previous run at lmTol 1e-6 in experiment_zero.run.json.

## Left for others

- The test lines do not bind `budget`, so the tester draws it: with `s = settingsA` (maxIter 500)
  a drawn budget above 500 makes a case vacuous, and drawn settings with a small `maxIter` and a
  small budget would refute a correct maximizer again. tests/tester/belief_laws.lut and
  fit_laws.lut should bind it in `cutoffs` (a census of one, the demand's), as my probe did with 50.
- run.py's docstrings name demand.lth's `PassedDownNotRecomputed`, `RecordsEveryCutoff` and `Runs`,
  which are gone (`lawDemand`, `recorded` are definitions now; `determined` is over `Stored K`).
- certification.lth could claim `NoPriceRefusesAssumed` and `LoweringLosesNothing` in `Certifying`.
- Not done, out of the brief: B11 (`Confluent` over arbitrary schedules), `PlanIsConfluent` not
  reading `p`, leaves in `reaches` (Fable's minor point), B1's decoration in `Record` (with item 5).

## Decisions I took on my own

1. `IsGradient`'s comparison scale stays `1 + |f t| + |g t|`.
2. `negate` made total by a law of `Posterior`, not by a subtype of `negate`'s argument.
3. The budget of `QuadraticConverges` is a `Nat` parameter with the premise `s.maxIter >= budget`.
4. `StepRule` compares with `st.phi` as drawn, states not restricted.
5. `Dataflow`'s equality is a theory parameter, not a field; locality resets to `init`.
6. `NamesAreUnique` added (Fable's list); acyclicity by the closure of reads in `count` rounds.
7. The forward strategy's role is "by levels" and the model's `forward` changed to strict rounds;
   call by need's role is equality with `firstDemand`, now defined in plan.lth.
8. `Store` over a parameter identity, leaving item 5 open; `Run`, `Runs` removed.
9. Re-certifying lm's `QuadraticConverges` and committing the model's store.
