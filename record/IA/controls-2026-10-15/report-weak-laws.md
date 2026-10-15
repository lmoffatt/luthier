# Report: the laws the controls showed too weak (L9.14)

Brief: record/IA/controls-2026-10-15/prompt-weak-laws.md. By Claude Opus 5.5, a subagent of the
coordinating session, 2026-10-15. Each change is [proposed] and undone by its own commit.

Principles touched: L9.14 (a law is evidence of nothing until a wrong model refutes it), applied
to the four groups report-mutants.md left uncontrolled or too weak; P11 (every criterion a
parameter): no new constant enters a law; P2 (everything derived carries how it was derived) for
the three model stores committed. Assumes, as before, that a control matches its law by the law's
cone hash.

## What changed, one commit per file

1. numbers.lth `LessIsStrict` (1f9924b): the law takes a third parameter `tie : Bool` and is
   stated on the pair `(x, if tie then x else y)`. The instances are the same as over every pair;
   the sampler now draws a tie half the time. numbers_controls.lut (b856c34): the control is
   `less := a <= b`, the model the law could not see. Refuted at `tie = true`.
2. arrays.lth `RankScales` (15caf52): besides `rank (c s) == rank s`, the law scales s relative to
   its magnitude, to a Frobenius norm of `c * fl` (the norm bounds every eigenvalue), and asks the
   same rank there; a zero floor or a zero matrix skips that clause. A floor relative to the
   largest eigenvalue keeps the rank; an absolute floor above `c * fl` drops everything.
   arrays_controls.lut (aa514b8): `rankAbs` is now an absolute floor of 1e-3 (none retained when
   the norm is at most 1e-3, else the leaf at 1e-3 over the norm), the floor that passed before.
   Why the old law missed it: `Positive` is drawn within the size, so c sat in (0, 10] and never
   pushed an eigenvalue of order one below 1e-3.
3. generators_model.lut (8c6aef6): the six family laws take their family as a first parameter `g`
   (`Gen Symmetric`, `(k : Dim) -> Gen (SymmetricOf k)`, ...). generators_laws.lut (91264a7): each
   line binds `g` to a census of one listing the family (`symmetricFamily := [symmetric]`), since
   a binding that names a `Gen T` directly is drawn from, not passed (tester.py `generator_of`).
   generators_controls.lut (7aeab97): the wrapper laws `XOnBroken` are gone; each control is the
   law's own line with `g` bound to a broken family typed as the family it impersonates
   (`brokenSymmetric : Gen Symmetric` gives an upper-triangular matrix; the checker accepts the
   claim, and the law is what tests it). Two broken families draw at `size + 2` and `size + 1` so
   that a 0 x 0 or 1 x 1 draw is not accidentally valid. Only the non-statistical lines were
   touched in both test files.
4. probability.lth §4 (10a433c): a theory
   `GaussianConstruction : { full : (n : Nat) -> ScaledModel n -> Likelihood n, profile : (n :
   Nat) -> MeanModel n -> Likelihood n }`, the two laws over `g : GaussianConstruction` first, and
   `GaussianConstruction := GaussianPeaksAtMean & ProfiledIsGaussianAtItsSigma`.
   probability_model.lut (cde1618): `gaussianConstruction := { full := gaussian, profile := profiled }`.
   probability_laws.lut (6e0c86b): the three construction lines take `onConstruction`, the
   cutoffs plus `g`, as profile (a separate list, so the other lines keep their identities).
   probability_controls.lut (6288940): `residualFlipped` (the full log-likelihood with
   `+1/2 e^{-2u} |r|^2`, least at the mean) controls GaussianPeaksAtMean on `fullModel`;
   `unbiased` (the profile at sigma^2 = RSS / (K - 1), in value, score and information) controls
   ProfiledIsGaussianAtItsSigma on `posModel`, 5 cases. The "no control" comments are replaced by
   a note of the model breaks tried before.

## The run

`luthier check` on every changed file: clean (and `luthier parse` on each). `luthier certify
--jobs 2 --fuel 100000000`, with stores, on numbers, arrays, generators and probability `_laws.lut`
and `_controls.lut` at 1cdf276: exit 0, 12 min; `CONTROL FAILED` appears 0 times. The four groups:

    numbers_laws.lut     LessIsStrict: sampled; controlled (d = lessLoose, x = -9.79, y = 6.47, tie = true)
    arrays_laws.lut      RankScales: sampled; controlled (m = rankAbs, fl = floor, c = 9.14, s 4 x 4)
    generators_laws.lut  SymmetricGivesSymmetric: sampled; controlled (g = brokenSymmetric)
                         SymmetricOfGivesItsSize: sampled; controlled (g = brokenSymmetricOf, k = 4)
                         GramGivesPsd: sampled; controlled (g = brokenGram)
                         OrthogonalGivesOrthogonal: sampled; controlled (g = brokenOrthogonal, k = 4)
                         UnitListGivesUnitValues: sampled; controlled (g = brokenUnitList)
                         ClearDiagonalGivesClear: sampled; controlled (g = brokenClear)
    probability_laws.lut GaussianPeaksAtMean: sampled; controlled (g = residualFlipped, m = fullModel)
                         ProfiledIsGaussianAtItsSigma: sampled; controlled (g = unbiased, m = posModel)

Every other law of the four files kept its status: all controlled, except generators'
`UniformSampleIsUniform`, which reads uncontrolled because its control is the separate law
`SkewedSampleIsUniform` (the other agent's, as report-mutants.md already said).

`python -m pytest -q`, run alone after the stores were rewritten: 709 passed, 5 skipped,
9 xfailed.

## Findings

- The suite and a certify run must not overlap. tests/conftest.py puts every library store back
  after each test; my first suite run, concurrent with certify, put numbers_model.cert.json and
  arrays_model.cert.json back to HEAD and dropped two of generators_model's entries, and the next
  suite then failed seven tests on `numpy: RankScales: stale`. I wrote them again with
  `luthier certify --deep` on numbers_laws.lut and arrays_laws.lut (--jobs 2) and on
  generators_laws.lut (one job), then ran the suite alone. Committed as derived: a830e53
  numbers_model, 5cb7d7a arrays_model, ae94ce4 generators_model (a new store).
- probability_model.cert.json now holds the two construction entries, mixed with the other
  agent's uncommitted entries; left uncommitted, as report-mutants.md left it.
- RankScales's lesson is general: a sampled scale lives within the size, so a law about
  invariance under scale sees only scales near one unless it constructs the far ones itself.
  PinvScales has the same shape and was not in this brief.
- A law over a family typed `Gen Symmetric` is honest only because the checker does not prove a
  function's subtype obligation; if it ever does, the broken families would have to be typed
  `Gen (Mat Float64)` and the laws' parameters widened.

## Decisions taken on my own (each undone by one commit)

- LessIsStrict's tie as a `Bool` parameter of the law, not a new subtype or a generator.
- RankScales's second scale is `c * fl / frobDef s`, the floor itself as the target magnitude.
- The family as a law parameter bound through a census list, not a record theory per family.
- GaussianConstruction as a record of both constructions (the profile law needs both).
- The two probability controls run on fullModel and posModel (5 cases), not on session A's model.
- Committed the three model stores as derived evidence.
