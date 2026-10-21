# Bite 11: arrays and tables over the core

Claude Opus 5.5, 2026-10-21, on `prompt-bite-11.md`. Input: `a7c0b5c`. Bites 9 and 10 and the
refusal-holes agent committed in the same tree meanwhile; every count below is of the shared
tree. Commits: `6e8f276`, `ab2c210`, `37a63dd`, `d6b2387`, `6623993`, `f71b06b`, `756ec7f`,
`6de1017`, `cc6d37c`, `d75119b`, `30c176c`, `e56a4fa` (stores), `582621e`, `625783b`, the plot
stores' commit and this report's. The arrays programs were certified in a separate worktree
(`~/.cache/luthier-sdk/bite11/head`) holding the committed tree plus the rename of bite 9's files
below, since without it `generators_model.lut` does not load.

## What was built

arrays.lth §1. `Vec` and `Mat` claim the core's container structures where they are defined
(L2.8): `VecIsIndexed`, `VecIsAnObject` (entry by entry), `VecIsAFunctor`, `VecIsFoldable`,
`VecIsTabulated`, `MatIsAnObject` (shape and entries), `MatIsAFunctor`, and `MatIsIndexed`,
row-major by `Fin (m * n)` with the two-index `f` kept, at one shape (`MatShaped A r c`). They
are gathered in `ArrayContainers`. `Symmetric` is `SymmetricMatrix`, the equalizer of the
identity and `transposeDef` (`SymmetricIsAnEqualizer`); `SymmetricOf` keeps its name. `size v`,
`at v k` and `map g v` resolve at `Vec Float64` with no qualification
(`tests/run/vec_resolution.run.lut`, and its test in test_run.py).

arrays.lth §3. The `approx...` family is the core's `entrywiseBall` of `absDistance` through
§1's index (`vecBall`, `matBall`). `approxVec tol` and `approxMat tol` keep their names and
meaning; `approxMatOf`, `approxMatSlackOf` and `approxMatBoth` keep their radii. `approxMatSlack`
(unused) and `forallPairs2` are gone.

arrays.lth §4. The entrywise laws are the core's `Pointwise` and `Pointwise2` at §1's equality.
`DotSymmetric` is `DotCommutative` (the core's `Commutative`). `MatMulIdentity` splits into
`MatMulNeutral` (the core's `Neutral`, square) and `MatMulByIdentity` (rectangular). Six summing
laws dropped the demand's tolerance for the theory's bound (D-2026-10-18-j). Each states its
range as a premise in its body: at most 10^6 terms, entries zero or of magnitude in
[1e-150, 1e150] (numbers.lth's `Moderate`).

| law | radius; `gamma n = n u / (1 - n u)`, `u = epsilon / 2` from the `Doubles` model `fp` |
|---|---|
| `DotAgrees` | `3 gamma n` times the sum of the magnitudes of the products |
| `MatVecAgrees` | `3 gamma c` times the same, row by row |
| `MatMulAgrees`, `MatMulTransposes` | `3 gamma k` times the same, entry by entry |
| `TraceCyclic` | `3 gamma (r + c)` (nested sums, Higham's Lemma 3.3) |
| `TraceAgrees` | `3 gamma k` times the sum of the diagonal's magnitudes |

Source: Higham, Accuracy and Stability of Numerical Algorithms (2002), eq. (3.5) and Lemmas 3.1
and 3.3, which hold in any order of summation, with or without a fused multiply-add. The 3 is
derived in the file the way numbers.lth gets its 3 gamma2: two computations of one exact value
differ by `2 gamma n S`, and measuring the difference and `S` in floating point costs a factor
`(1 + u) / (1 - gamma n)` plus the radius's own roundings. No bound was tuned. All six passed
on numpy and were refuted on their wrong models.

tables.lth. Its list helpers are the core's `size`, `member`, `distinct`, `all` and `zip`.
`listLength`, `memberStr`, `distinctColumns`, `allKnown`, `columnsOfKind`, `pairIn` and
`sameCells` are gone. plot.lth imported three of them; its import line and 13 uses now call the
core's functions, and nothing else in it changed. A table is indexed by its rows
(`TableIsIndexed`, at one schema) and `sameTable` is its `Object` (`TableIsAnObject`), gathered
in `TableClaims`.

elaborate.py. Two hunks. An alias with parameters, named without its arguments where a kind
`U -> U` is asked (a claim's structure parameter: `Functor Vec`), is its type former, unfolded
where it is applied. Anywhere else it is still refused ("alias A needs arguments";
test_check's case). Applied aliases elaborate as before, so this moves no cone. Before, `Functor
Vec` was refused and `map` found no model at `Vec Float64`.

run.py. `CORE_COLLISIONS` is empty.

## Findings

1. The row-major index does not see a matrix's shape. A 2 x 3, a 3 x 2 and a 1 x 6 matrix can
   have the same entries in the same order, so `Extensional` fails at `Mat A` under the
   shape-aware equality. The claim is made at one shape (`MatShaped A r c`). Tables have the same
   problem: two tables with no rows and different columns have the same rows, so
   `TableIsIndexed` is claimed at one schema. Neither claim binds `size` at `Mat Float64` or at
   `Table` for resolution. `Mat` has no `Tabulated` claim, since `build n f` cannot know the shape.
2. A binding can't hand a test `Float64` as a value of `Concrete`, because core.lut declares
   `Float64 : Real`. The generic claims are tested at `Int`, which is finite evidence at one
   carrier.
3. Drawing a refinement of `VecOf n` (the first form of the ranges, `ModerateVecOf`) failed with
   "maximum recursion depth exceeded" in the host, and one line hung for over 20 minutes. The
   ranges are now premises in the law bodies.
4. The coordinator asked about the operator key. With arrays_model.lut loaded, `2.0 * 3.0` gives
   6.0. But `c * v` with `c : Float64` resolved to `floatTimes` and was refused, so arrays_model's
   `* := scale` and `* := mscale` could never be reached. I removed them (`cc6d37c`): write
   `scale c v`. A probe also found that none of arrays_model's operator bindings reach an
   importer: `a * v` and `a * a` in an importing file are refused ("names no model of *"). The
   file's comment had already left that question open; I did not change it.
5. `SymmetricIsAnEqualizer` did not run until its test line bound the model (`30c176c`). An
   unbound record of an equalizer has no finite enumeration (7.R3).

## Checks

- `luthier certify` (worktree, the lines' own seeds, no `--deep`), second pass:
  `arrays_laws.test.lut: 45 laws, 0 lines ran, 62 known`;
  `arrays_controls.test.lut: 0 laws, 47 controls, 0 lines ran, 47 known`. In the tree:
  `tables_laws.test.lut: 10 laws, 0 lines ran, 10 known`;
  `tables_controls.test.lut: 0 laws, 10 controls, 0 lines ran, 10 known`. Every law is graded
  and controlled, and every control refuted. One line still reports `not run`: the plain sampled
  `RankUnderRotation`, which by design shows that `Orthogonal` has no generator.
  `RankUnderRotation` is graded on its listed and generated lines.
- Lines re-certified: 63 law lines and 47 control lines of arrays; 10 and 10 of tables; the plot
  programs (below).
- `pytest` (worktree, full suite, 43 min): 59 failed, 838 passed, 6 skipped, 9 xfailed. Two
  failures were mine, test_certify's and test_tester's counts of tables' lines, fixed in
  `582621e` and `625783b`. One is unrelated: test_chat_tools' select verdict. One is
  `test_plots`' two-table run, stale on plot's stores, which my plot.lth change moved; the plot
  wave below re-certifies them. Every other failure is a run refused for the stale
  `console:` laws of world_model.lut (bite 9's store): PrintAppendsALine,
  PrintChangesOnlyStdout, ReadGivesThePlace, ReadChangesNothing.
- `validate_graph.run.lut`, through `test_validate_graph_slow` (which leaves no record), is now
  refused only for `doubles: Neutral, Absorbing, Involutive, TotalOrder: uncertified (no
  entry)`, numbers.lth's store. At `7180f7b`, before this bite, the same refusal also listed the
  console laws, `doubles: Commutative` and the stale numpy laws, so the doubles' entries are
  older than this bite.
- `python scripts/check_spec.py`: only its known finding (03-kernel.md:192, the run of 10 words).
- `luthier check -v` on arrays.lth and tables.lth: every act typed. The only unclaimed notices
  are `hasColumn` and `sameTable`, both there before.
- `scripts/core_metrics.py`, before (`a7c0b5c` plus the others' uncommitted work) and after:

| count | before | after |
|---|---:|---:|
| homonyms | 59 | 58 |
| executive shadows | 107 | 107 |
| list helpers | 226 | 219 |
| unclaimed | 32 | 31 |
| loose | 1973 (real 1325) | 1995 (real 1346) |

  Loose rose: the new models' functions (`vecIndexed`, `vecMap`, `matBall`, `gammaN`, ...) get
  the notice like every top-level function. Narrowing it is bite 13's count 4.

## For the coordinator: bite 9's files

`Symmetric` became `SymmetricMatrix`. Bite 9's files still import `Symmetric` from arrays.lth,
so generators_model.lut does not load, and everything importing it fails. That includes the
`Symmetric * Seed` that test_infer_is_total_on_the_library reports, which is `Gen Symmetric`
unfolded: after the rename it is `SymmetricMatrix * Seed`, a product, and the test passed in the
worktree. The rename, applied in the worktree by this script:

```
sed -i -E '42s/\bSymmetric\b/SymmetricMatrix/; 51,110s/\bGen Symmetric\b/Gen SymmetricMatrix/g; 51s/\(`Symmetric`\)/(`SymmetricMatrix`)/' src/luthier/lib/generators_model.lut
sed -i -E '31s/\bSymmetric\b/SymmetricMatrix/; s/\bGen Symmetric\b/Gen SymmetricMatrix/g' tests/tester/generators_laws.test.lut tests/tester/generators_controls.test.lut
sed -i -E '20s/\bSymmetric\b/SymmetricMatrix/; 36s/\[Symmetric\]/[SymmetricMatrix]/; 37s/Degeneracies Symmetric\b/Degeneracies SymmetricMatrix/; 3s/`Symmetric`/`SymmetricMatrix`/' tests/tester/regions_laws.test.lut
```

That is generators_model.lut's import line (42) and its `Gen Symmetric` lines (53, 55, 73, 76,
102, 106); generators_laws (31, 43, 45); generators_controls (31, 43, 47, 56, 58); and
regions_laws (20, 36, 37). Their stores, generators_model's and regions', need one wave after.
The second import line of generators_model.lut (`arrays_model.lut numpy : Arrays`) needs no
change.

## Decisions taken on my own (one commit undoes each)

- The name `SymmetricMatrix`, with `SymmetricOf` kept.
- `MatIsIndexed` and `TableIsIndexed` claimed at one shape or schema (finding 1), not at `Mat A`
  or `Table` with an equality that ignores the shape.
- The summing laws take the `Doubles` model as a parameter `fp`, bound to `doubles` by the tests,
  rather than importing it into the theory. Their ranges (10^6 terms, `Moderate` entries) are
  written as premises in the body (finding 3).
- `NormOfDot`, `NormScales`, `TraceAdditive`, `Orthogonal` and the pseudo-inverse's laws keep
  the demand's tolerance. The four that sum could take Higham's bounds the same way; the
  pseudo-inverse's depend on conditioning and have no theorem bound written yet. Left for the
  three-levels plan.
- plot.lth's three tables helpers replaced by the core's, its stores re-certified, rather than
  the helpers kept in tables.lth for plot.
- The alias rule in elaborate.py; the two scalar `*` bindings removed (finding 4).
- No control "a bound too small on the real doubles" for the six bounds: random draws sit far
  below `gamma n`, so a witness would have to be searched for. Each law is controlled by a wrong
  model.

## Question

None.
