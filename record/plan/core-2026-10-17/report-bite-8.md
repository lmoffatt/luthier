# Bite 8: numbers.lth and algebra.lth over the core

Claude Opus 5.5, 2026-10-21, on `prompt-bite-8.md`. Input: `1429de8` (bite 6 landed). Commits:
`da91279`, `22c14fb`, `4c923bf`, `9387de7`, `f656d45`, `d2da32d`, `719661a`, `4a5db0e` (stores),
and this report's. `da91279` staged two lines of bite 7's uncommitted work with mine (run.py's `<>`
slice, a `<>` in test_check.py); `d2da32d` took them back through the index, leaving bite 7's
working tree as it was.
Bite 7 ran at the same time in the same working tree, uncommitted; every check below ran in a
separate worktree (`~/.cache/luthier-sdk/bite8/head`) holding the committed tree and nothing of
bite 7's, so its evidence is about bite 8 alone. Scripts of the numerical probes, with seed
20261021: `~/.cache/luthier-sdk/bite8/{probe,uniform,tri,witness,edges}.py`.

## What was built

numbers.lth §1: `absDistance a b = abs (a - b)`; `within` and `withinOf` keep their names and
meaning, now balls of `absDistance` (`Ball`, section 4); two ranges join `Moderate`: `NonZero`, and
`Tame` (zero or magnitude in [1e-100, 1e100], where products of three stay normal).

numbers.lth §2: `Doubles` keeps its record unchanged (so the examples' cones that read it as a type
do not move). Its claim is a bare conjunction (D-2026-10-18-f) of 25 conjuncts: the core's
`Commutative` on `plus` and `times` over `Moderate`; `Neutral` on `plus`/0 and `times`/1,
`Absorbing` on `times`/0 and `Involutive` on negation, over every double; `Order` on `leq`; then
the laws with no core property or with a range the core's property cannot state (`PlusMonotone`,
`TimesMonotone` as `Monotone` of the operation with `z`, `DivideOne`, `MinusSelf`, `DivideSelf`,
`MinusIsPlusNegated`, `LessIsStrict`, the reversed comparisons, `EpsilonIsTheUlpOfOne`); and the
four within-bound laws of section 4:

| law | bound (u = epsilon / 2, gamma2 = 2u / (1 - 2u)) | range (premise) |
|---|---|---|
| `PlusAssociativeWithin` | 3 gamma2 (abs x + abs y + abs z) | `Moderate` |
| `TimesAssociativeWithin` | 3 gamma2 abs x abs y abs z | `Tame` |
| `TimesDistributiveWithin` | 3 gamma2 abs x (abs y + abs z) | `Moderate` |
| `DivideInvertibleWithin` | 2u, of `x (1 / x)` against one | `NonZero` |

Each bound is computed in the law from the model's `epsilon`, never a demand's tolerance (P11 and
D-2026-10-18-j); sources (Higham 2002, Lemma 3.1 and section 2.2) are in the file. Removed:
`PlusCommutes`, `TimesCommutes`, `PlusZero`, `TimesOne`, `TimesZero`, `NegateTwice`, `LeqPair`,
`LeqChain`, `LeqReflexive`, `LeqTotal`, `LeqAntisymmetric`, `LeqTransitive`, `doublesOrder`.
`SqrtMonotone` is `Monotone` over `Related NonNegative`.

numbers_model.lut: `AbsDistanceIsAMetricWithin`, the computed distance a `MetricWithin` with bound
`u (abs a + abs b)` (one rounding in the subtraction, the standard model), gathered in
`NumberModels` as core.lut gathers `CoreData`.

algebra.lth §4: `OrderedRing` is `Order`, `MonotoneIn` on `plus` and `PositiveClosed` on `times`,
bare; `OrderedField` is the ordered ring at its field's ring. Its `Leq…`, `PlusMonotone`,
`TimesPositive` and `FieldIsOrdered` are gone.

run.py: the `CORE_COLLISIONS` entries of numbers.lth and algebra.lth removed. They were already
empty: bite 6 had removed every name they listed from the core.

Tests: numbers_laws.test.lut runs `Doubles` conjunct by conjunct at sizes 10 and 10^6, each law of
§2 on its own line, the within-bound laws also exhaustively at the edges of their ranges (216, 216,
216 and 5 listed cases: 1e±150, 1e±100, zero, one), and `AbsDistanceIsAMetricWithin`.
numbers_controls.test.lut: ten controls of `Doubles`, each refuting a different conjunct (two
commutativities, the two neutrals, absorption, involution, the four parts of the order); one
control per named law; two per within-bound law and two for the distance. The Python tests and
tests/tester/cases.test.lut name `DivideOne` and `TimesMonotone` where they named `PlusCommutes`
and `LeqTransitive`. No `PlusCommutes` remains in lib/ or tests/ (laws.test.lut's is
`IntPlusCommutes`).

## The bounds: confirmed, none refuted

Section 4's bounds held everywhere: 2,500 sampled cases per size, the edge cases, and in Python
2·10^6 structured triples and 10^6 uniform ones. The largest ratios of error to gamma2 seen were
1.73 (sum), 1.78 (product) and 1.77 (distributive), all below 3. So **gamma2 alone, the bound
D-2026-10-17-f first wrote, is refuted for all three**, and 3 gamma2 is needed. `x (1 / x)` came
within exactly u of one, inside 2u (the 2u is loose by a factor of two; the spacing below one is
u).

The controls, each refuted (the line, the case):

- an operation rounded to 26 bits (Veltkamp's split, `coarse`): sum, product, distributive,
  reciprocal and distance, each at the first drawn cases;
- a bound too small on the real doubles: the model with `epsilon / 3` turns 3 gamma2 into just
  below gamma2. Refuted at (1.822, 8.248, 4.954) for the sum, (2.64, -5.153, 8.311) for the
  product, (-3.892, -8.146, -8.159) for distributivity; `epsilon / 4` (bound u/2) at x = 1.637;
  the distance with bound zero at (46335101106.32112, -0.001832427150917524, -2161794998296.6406).

With uniform draws in [-10, 10], gamma2 is broken in only 1.5e-4 (sum), 2.9e-3 (product) and
7.5e-4 (distributive) of the cases. So these controls list their witness, as the `LeqTransitive`
control already did, instead of hoping a draw finds one.

## Checks

All in the worktree, with the conda Python (`luthier.cli.main` from the worktree's `src`, the
same entry point as /home/lmoffatt/miniconda3/bin/luthier). The first wave (17:51) was lost when
the coordinator's session ended; these ran again after it, at `0f128d2`, then at `4a5db0e`.

- `luthier certify tests/tester/numbers_laws.test.lut tests/tester/numbers_controls.test.lut`
  (jobs 4, the lines' own seeds, no --deep), first pass: `38 laws, 53 lines ran, 2 known` and
  `52 controls, 50 lines ran, 2 known`. Second pass, and again at `4a5db0e`: `38 laws, 0 lines ran,
  55 known`, `0 laws, 52 controls, 0 lines ran, 52 known`. Every law graded (sampled, or cases for
  the exhaustive ones), every law controlled, every control refuted.
- Lines re-certified: 53 law lines and 50 control lines (the 2 + 2 known were `EpsilonIsTheUlpOfOne`
  and `ConvertZeroAndOne`, whose cones did not move). Stores written: numbers.cert.json and
  numbers_model.cert.json only, committed in `4a5db0e`.
- Not re-certified by this bite: the laws whose cone reaches `within`/`withinOf` (arrays,
  probability, belief, optimization, generators, the sonolocalización programs). Their stores were
  already stale at `1429de8` (bite 6's dependent wave was not committed: `vector_norm.run.lut` is
  refused there too), and today they are uncommitted files of the agents of bites 9 and 10, which I
  was told not to touch. The full-wave criterion ("0 lines ran for every non-fixture program") is
  met for my two programs only; it needs one wave after bites 9 and 10 land.
- `luthier check` on numbers.lth, numbers_model.lut, algebra.lth and the two test programs: clean.
  `check -v`: no new unclaimed law (`withinOf`'s notice was there at `1429de8`).
- pytest at `0f128d2` (worktree): test_tester + test_check 112 passed, 1 skipped; test_certify 52
  passed, 1 skipped, 3 failed, and one not finished (`test_the_regions_hold_…`, killed at its
  10-minute limit; it reads regions_* programs, generators.lth and certification.lth, which bites 9
  and 10 are changing); test_run 93 passed, 45 failed. Every failure I opened is a run refused for
  stale stores: world.lth's console laws (`PrintAppendsALine` and three more, changed by bite 9) and
  the arrays stores (stale since `1429de8`). None names numbers.lth. The full suite cannot pass
  until those stores are re-certified, so the "pytest passes in full" criterion is not met here.
- `python3 scripts/check_spec.py`: only its known finding (03-kernel.md:192, the run of 10 words).
- `scripts/core_metrics.py` on clean trees: at `1429de8` 81, 103, 426, 45, 2060 (real 1400, rest
  660); at `719661a` (bite 8 alone) 77, 103, 426, 45, 2047 (1397, 650). Bite 8 lowers homonyms by 4
  and loose by 13, raises nothing. At `4a5db0e` (with bites 7 and 9) 66, 107, 260, 32, 2002 (1353,
  649).

## Decisions taken on my own (one commit undoes each)

- Within-bound laws named per law with their range as the type of their variables, not bare
  conjuncts of the core's `…Within`: the core's properties quantify over one carrier, which must
  be closed under the operation, and a range like `Moderate` is not. Same reason for `PlusMonotone`
  and `TimesMonotone` as `Monotone` instead of `MonotoneIn` (check refused `MonotoneIn Moderate`).
- The bound inside the law, computed from the model's `epsilon`, instead of a parameter with a
  default (the tester does not use defaults, it asks for a census). As a result, the "bound too
  small" control is a model with a smaller epsilon.
- `Tame` as the range of the product's associativity; listed edge cases for each range
  (D-2026-10-18-j asks for the boundary to be sampled; values outside the range overflow, which
  is an error, so only the inside is sampled).
- The distance's bound `u (|a| + |b|)`, argument-only, rather than `u |a - b|`.
- `Tolerance` and `abs` stay in numbers.lth (the plan moves them to the core): core.lut was bite 7's
  file today, and `floatAbs` already lives there. The importers' lines are unchanged.
- The `Elementary` identities keep their demand tolerance. D-2026-10-18-j would turn them into
  stability and sensitivity laws with theorems' bounds, but the host's `exp`, `log` and `erf`
  document none (sqrt's could be done). That's a later bite, not section 4.

## Question

`plus` and `times` don't resolve at `Float64` (`leq` does, through core.lut's `FloatIsOrdered`).
Section 4's `DoublesHaveTheOperations` can't do it as written: the elaborator registers only a
declaration with parameters as a structure, and `Doubles` has none, so a claim of it binds nothing
at `Float64`. I see two ways. (a) Give `Doubles` its carrier, `Doubles (F : U)`, claimed at
`Float64`: the laws stay as they are, but the examples' `doubles : Doubles` becomes
`Doubles Float64`, their cones and run records move, so it belongs with bite 12. (b) A
within-bound semiring in the core (`SemiringWithin`), claimed at `Float64` with the bounds in the
model: generic, but its laws would range over all of `Float64` and lose the ranges (`Moderate`,
`Tame`) that D-2026-10-18-j asks every such law to state. I recommend (a), done in bite 12. Do you
agree?
