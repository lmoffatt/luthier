# The slice's first theories: report

By Claude Fable 5.1, an agent of the coordinating session, 2026-10-14, on `prompt.md` of this
directory (committed at 5fa3d84) and the answers of the sonolocalización session
(`record/IA/sonolocalizacion-inventory-2026-10-13/answers-2026-10-14.md`, c49b34b), which fixed
the names the first stage uses. Nothing outside `src/luthier/lib/` was touched, and in term.lth
only §5 next to `Prim`. Each file was committed alone.

## What was written

| file | commit | states |
|---|---|---|
| `src/luthier/lib/core.lut` | 3c43822 | the primitives (11.R1), `Unit`, `Empty`, `Bool`, `Maybe`, `List` as data (3.S7, 3.R3), `Nat`, `Fin`, `ExtendedReal`, the arithmetic as `primitive` bodies per type bound by `operator` (4.R13), `toFloat64` |
| `src/luthier/lib/algebra.lth` | 65b7e36 | `Iso`, `AbelianGroup`, `CommutativeRing`, `Field`, `OrderedRing`, `OrderedField`, `CompleteOrderedField` (11.R3, 4.R10), on kernel_laws.lth's `Monoid` |
| `src/luthier/lib/numbers.lth` | 47675c6 | `abs`, `Tolerance`, `within`, `withinOf`, `Moderate`; `Doubles` (exact laws of the four operations and the order, 11.S4), `IntegerDivision`, `Conversion` (11.S5), `Elementary` (`sqrt exp log erf`, 11.S2; exact cases, identities within a `Tolerance`, 11.S18) |
| `src/luthier/lib/numbers_model.lut` | dc0cef2 | `integers : OrderedRing Int`, `integerDivision`, `realField : CompleteOrderedField Real := axiom` (11.R3), `doubles`, `conversion`, `elementary` (routes to Python's `math`), `strings : Monoid String` |
| `src/luthier/lib/term.lth` §5 | 681742e | `PrimInt`, `PrimFloat`, `PrimString`, `PrimConvert`, added to `Reduction` (3.S17) |
| `src/luthier/lib/arrays.lth` | c6890a6 | `Array`, `Vec`, `Mat`, `vec`, `mat`, `Dim`, `VecOf`, `MatOf`, `MatRows`, `Square`, `Symmetric`; `sumTo` (3.S27), `sumToInt`, `forallBelow`, `existsBelow`, `forallPairs`, `countBelow`; the native definitions, `distance`, `approxVec`, `approxMat`; `RankFloor` and the theory `Arrays` of the leaves |
| `src/luthier/lib/arrays_model.lut` | 04757b9 | `numpy : Arrays` (routes to `src/luthier/arrays.py`), the leaves by name, the `operator` acts of `+ - *` on vectors and matrices |
| `src/luthier/lib/tables.lth` | 81e72ea | `Cell`, `listLength`, `firstFailing`, `Table` with its schema laws, `nCols`, `hasColumn`, `intAt`, `realAt`, `textAt`, `sameTable`, `Codec` with `RoundTrip`, `Canonical`, `Tolerant`, `Rejects` |
| `src/luthier/lib/tables_model.lut` | 79f6f7e | `csv : Codec` over `src/luthier/tables.py` |

Every file passes `PYTHONPATH=src python3 -m luthier.cli parse`. `luthier check`: numbers.lth,
numbers_model.lut, term.lth and tables_model.lut pass clean; the refusals of the others are
listed under "What the checker refuses", each attributed.

## The choices where the specification was silent or divided (all marked `[proposed]` in the files)

1. core is `src/luthier/lib/core.lut`, a model file by extension and by content (the interpreter's
   values), under `lib/` because the brief allowed files there only; its laws live in
   kernel_laws.lth and numbers.lth with their models in kernel_models.lut and numbers_model.lut.
   The spec says `core.lut` (11.R2, 12.S22) and the loader anchors on that name.
2. `Bool`, `Maybe`, `List` are `data` (3.R3, D-2026-10-13-o; the kernel represents `true` as the
   constructor `Var "true"`), not the labeled sums of 2.S12. `Unit` and `Empty` as 3.S7 says.
3. The arithmetic `+ - * / mod` is in core as typed `primitive` bodies named by their symbol
   (`intPlus : Int -> Int -> Int := primitive "+"`, `floatPlus`, `stringAppend`, ...) and bound by
   `operator` at each type (4.R13), since no definition can be named `+`. The comparisons
   `== /= < <= > >=` have no act that binds them (`operator` takes `+ - * / and or mod`), so they
   are left to the kernel's `Primitive` reached directly by the elaboration (term.lth `Prim` and
   its neighbours), and named only in a comment of core.lut. `and`, `or` are keywords: their
   functions are `conj`, `disj`, bound by `operator and`, `operator or` at `Bool`.
4. Integer `/` and `mod` are floor division, the host's (`(a / b) * b + a mod b == a`, the
   remainder of the divisor's sign). Truncation is the other reading; one law changes.
5. A zero divisor (Int and Float64) does not step: the Luthier model answers `nothing`, the host
   raises (11.S7 makes it an error; a step has no error to give).
6. Float64 laws are quantified over `Moderate` (zero or magnitude in [1e-150, 1e150], the range
   of 11.S13), where every operation of two is finite, so the laws do not raise on their own cases.
7. Tolerances are a parameter of the law, `Tolerance : U := { tol : Float64 | 0.0 <= tol }`, bound
   by the demand (11.S18, D-2026-10-12-h, P11), in the pattern of `Level` in generators.lth; no
   number of the kind `roundingSlack := 8.0` is in any file. A sum is compared relative to the sum
   of the magnitudes of its terms (`withinOf`, 11.S14), never to its result.
8. `Doubles.epsilon` is characterized as the ulp of one (`(1 + eps) - 1 == eps`, `1 + eps/2 == 1`);
   the model holds the constant `2.220446049250313e-16` (a fact of the machine, 1.S9, not a
   criterion).
9. `SqrtOfSquare`, `sqrt (x * x) == abs x` on `Moderate`, is stated as a theorem of binary
   floating point (Muller et al., Handbook of Floating-Point Arithmetic) to be cited if kept;
   `SqrtMonotone` rests on IEEE 754's correctly rounded square root; `ErfOdd` and `ErfBounded` on
   the host library's construction. Drop any one that fails on the host.
10. The leastness of `sup` in `CompleteOrderedField` is a `Law` of laws.lth (`Forall`, `Then`,
    `Exists`) conjoined with Bool laws: stated and not tested, as 11.R3 says. `Rational`'s model
    waits for rational.lut (no literal exists to write its zero).
11. Arrays: `Vec A = { n : Nat, f : Fin n -> A }` as 11.S9, built by `vec A n f` (a record, not
    the pair `(n, fn k {...})` of v0.1 and of `tests/spec/n5_arrays.accept.lut`, which under
    D-2026-10-13-x is an isomorphic structure and not the record). The port of the slice's files
    replaces `(n, \ k { e })` by `vec Float64 n (fn k { e })` and `(r, c, \ a b { e })` by
    `mat Float64 r c (fn a b { e })`.
12. `normDef` (hence `distance`) takes its square root from the imported model `elementary` of
    numbers_model.lut: a theory file importing a model by name (12.S22 allows it; checking reads
    numbers.lth only). The alternative is a parameter `(e : Elementary)` on every norm.
13. `retainedRank : RankFloor -> Mat Float64 -> Int`: the floor is its first argument (P11;
    v0.1 held `n eps` inside the leaf, inventory row 13). The port of distance_graph.lut passes
    the floor, which `experiment_zero`'s parameters or the demand give; this is the one name of
    the first stage whose port is more than a rename. Its characterization: diagonals clear of
    the floor (counting the positive entries, as the host counts eigenvalues above the floor times
    the largest in magnitude, so negatives are never retained), the zero matrix and the identity,
    a bound by the size, invariance under a positive scale and under rotation by an orthogonal
    matrix (whose generator, a family of 7.S5, is the model's and does not exist). Agreement with
    Jacobi's spectrum (v0.1) is a corollary (4.R10) and was not restated.
14. Exact laws for the entrywise leaves (`add`, `sub`, `scale`, `transpose`, `madd`, `msub`,
    `mscale`: the host does the same machine operation per entry), for `DotSymmetric`,
    `DotOnBasis`, `NormOfBasis`, `MatVecOnBasis` and `MatMulIdentity` (one nonzero term, exact
    zeros elsewhere); the sums within the demand's tolerance. If numpy's BLAS breaks an exact one
    (an FMA or a blocked order could, in principle), that law moves to a tolerance.
15. The `operator` acts for `Vec`/`Mat` arithmetic sit in arrays_model.lut beside the model, with
    the leaves given names there (`matMul : ... := numpy.matMul`) so that `operator` binds a
    name with a type; whether an importer sees an imported file's `operator` acts is not stated.
16. Tables: `BrokenText = { s : String }` has no law of its own until the format is an `Ebnf`
    (v0.1's recognizer over characters, 150 lines, needs `chars`, which nothing provides); so
    `Rejects` is tested on what the host's `gen_broken` breaks, one defect at a time. The format
    is stated in prose in §5 and marked todo as an `Ebnf` over characters.
17. `sameTable` and `approxVec`/`approxMat` are native (4.R8: no `==` on a type holding a
    function) and guard the shape with `if`, relying on 4.R11 (refinement in the branch, decided,
    not implemented) for the index types.
18. Not written: rational.lut (11.S13; the slice does not need it), the operations the slice does
    not use (`trace`, `det`, `solve`, `eigvalsSym`, `pinvSym`, `cbrt`, `ulp`, `round`), string
    operations beyond `+`, `number_model.lut` of 11.S3 (`Doubles` is the record a generic
    definition would take), the `test` data of the models (the tester is step 5).

## What the checker refuses, and whose it is

All parse. `luthier check` refuses:

- core.lut: 4.R3 on `Unit`, `Bool`, `Maybe`, `List` (their constructors' roles are in
  kernel_laws.lth and kernel_models.lut, D-2026-10-13-t; the checker reads one file). 4.R4 on
  `Int`, `Real`, `String` (a `primitive` body; `check.py`'s R4 lists `extern` and not
  `primitive`, 3.S39). 4.R13 on every `operator` target (`check.py` compares `declared(p, g)`,
  which is `None` for a definition with its type written inline, so every pair looks alike).
  All three the checker's.
- algebra.lth: 4.R3 on `OrderedField` and `CompleteOrderedField`: fields reached through a
  chained projection (`c.ordered.leq`) or a helper (`asOrderedRing`) are not counted, the same
  refusal the checker gives world.lth's `Console` and kernel_laws.lth's `Lists` (verified on a
  variant with a Bool law in place of the `Law`). The checker's.
- arrays.lth: 4.R3 on `VecOf`, `MatOf`, `MatRows`, `Square`, `Symmetric`, `SymmetricOf`,
  `ClearDiagonal` (a predicate reading a field of its binder, `v.n == k`, is not counted; a
  three-line variant reproduces it) and 4.R9 on 45 definitions (passing `n : Nat` where `Int` is
  expected, or a `VecOf n` where `Vec Float64` is: the subtype-to-base half of 4.R9 that check.py
  bite 3b's part 2 leaves; a three-line variant reproduces it). The checker's.
- arrays_model.lut: 4.R13 on the operator targets, as core.lut. The checker's.
- tables.lth: 4.R3 on `Table` and `Codec` (fields reached through helpers `columnsOfKind`,
  `sameParse`), 4.R9 on `sameParse`. The checker's.

Nothing refused is the file's. The refusals are on the checker's list already (3b part 2, the
reading of fields through helpers) except `primitive` in R4, which is new.

## What the kernel and the bridge must do, per operation

The kernel (kernel.py, a specimen of term.lth §5):

| operation | the kernel |
|---|---|
| Int `/`, `mod` | `Primitive "/"`, `Primitive "mod"` on two `IntConst`: Python's `//` and `%` (`PrimInt`); on a zero divisor, no step (the model) or the error (the host), never a value |
| Int `<=`, `>`, `>=`, `/=` | `Primitive` of each symbol on two `IntConst` → `Var "true"`/`Var "false"` (`PrimInt`); `==`, `<` exist |
| Float64 `-`, `*`, `/` | `Primitive` on two `FloatConst`: the IEEE operation; a NaN or an infinite result is an error, not a constant (11.S7, `PrimFloat`); `+` exists |
| Float64 `<`, `<=`, `>`, `>=`, `/=`, `==` | `Primitive` on two `FloatConst` (`PrimFloat`; `==` on floats is in `PrimStructural` already) |
| String `+` | `Primitive "+"` on two `StringConst`: concatenation (`PrimString`); `==` exists |
| `toFloat64` | `Primitive "toFloat64"` applied to one `IntConst`: `float(i)`, an error above the doubles' range (`PrimConvert`) |
| the infix forms | the elaborator gives `Var "+"`, `Var "<"`, ... (`quote { 1 + 2 }` law). Either the kernel's program carries `Define(sym, Primitive(sym))` for every symbol (cli.py does it for `+ - * == <`; extend to `/ mod <= > >= /=`), or the elaborator resolves the arithmetic through core.lut's `operator` acts (`(op, type) -> intPlus` etc., which `elaborate.py` already keys by `(op, domain)`) and the comparisons to `Primitive` directly. Both readings agree with core.lut; the coordinator chooses |
| `and`, `or` | `Var "and"`/`Var "or"` from the elaborator; core.lut binds them by `operator and := conj`, `operator or := disj`, so resolution by `(op, Bool)` reaches `conj`/`disj`; with no resolution, a `Define("and", ...)` cannot be written in the surface (reserved word), so the kernel would have to provide them |
| `primitive "..."` bodies | `App (Var "primitive") (Lit s)` from the elaborator; the kernel treats a definition with that body as `Primitive s` (3.S39) |
| `axiom "..."` | `realField` is a hole for reduction (`HolesStay`) |
| `Fin n` indexing | unchanged; `vec`/`mat` are plain records, `x.f k` a projection applied |

The bridge (run.py, 3.S22 to 3.S26, 11.S6):

| value | to the host | from the host |
|---|---|---|
| `Vec Float64` `{ n, f }` | the ndarray of `f` materialized over `Fin n` (3.S23, `n` evaluations); the record's `n` is the shape | an ndarray `a` at type `Vec Float64` is `{ n := a.shape[0], f := a }` with `f` a host object applied by indexing (3.S22, bounds checked by the interpreter), float dtype, exactly one dimension (11.S6) |
| `Mat Float64` `{ m, n, f }` | the 2-d ndarray of `f` over `Fin m × Fin n` | `{ m := a.shape[0], n := a.shape[1], f := a }`, two dimensions |
| `Fin n -> Float64` alone | 1-d float64 ndarray; `Fin n -> Int` int64 with the range check of 11.S8 (3.S24) | the same |
| `Float64` | a Python float; an int with an exact double promoted (11.S6); NaN or inf an error (11.S7) | the same |
| `Int` | a Python int, never a bool | the same |
| `RankFloor` | a float (a subtype of `Float64`) | |
| `Table` | the record `{ nRows, names, kinds, cell }`: tables.py's `as_table` reads those attributes, with `cell` a Luthier function the host calls (`name, row -> None or (label, value)`); or the host's own `Table` object passed through unchanged when it came from the host | a `Table` object at type `Table`: `nRows`, `names`, `kinds` read as the fields (int, list of str, list of str) and `cell` as a host function giving `nothing` for `None` and `just (int k)`, `just (real x)`, `just (text s)` for `("int", k)`, `("real", x)`, `("text", s)`, the labels of `Cell` |
| `Maybe Table` | | `parse` returns `None` or a `Table`: `None` is `nothing` (host.NOTHING today), a `Table` is `just` of the above |
| `List String` | a Python list of str (exists) | a list (exists) |
| a lambda over `Fin n` | each entry once (3.S25) | |
| `extern` inside a record value | `elementary.sqrt`, `numpy.matMul`, `csv.parse` are projections of a record whose field is an `Extern`: the demand reaches the extern through `Proj`, so the route is read when the projection is applied (3.S40) | |

The host code: `arrays.py` needs `retained_rank_at(floor, a)` (one line: `w > floor * max|w|`
counted, with `floor` given) beside `retained_rank`; `tables.py` is used as it is; `math` is
used as it is. `host.py` is untouched by these theories (reading the graph as an action is item 5
of the inventory's §6).

## For the port of validate_graph.lut and distance_graph.lut (item 5, not done here)

The names of the answers are kept: `Table`, `nRows`, `hasColumn`, `intAt`, `realAt`, `textAt`,
`firstFailing`; `Vec`, `Mat`, `VecOf`, `MatOf`, `MatRows`, `distance`, `transpose`, `retainedRank`,
`approxVec`, `approxMat`, `operator *` as `matMul`; `sumTo`, `sumToInt`, `forallBelow`,
`existsBelow`, `forallPairs`, `Iso`; `toFloat64`; `Bool`, `not`, `Unit`, `String`, `Maybe`, `Fin`.
Beyond renames: vectors and matrices by `vec`/`mat` (choice 11); `retainedRank` takes the floor
(choice 13); `approxVec 0.0` becomes `approxVec exact`; the imports become
`import "tables.lth" Table hasColumn intAt realAt textAt firstFailing`,
`import "tables_model.lut" csv : Codec`, `import "arrays.lth" ...`,
`import "arrays_model.lut" numpy : Arrays matMul transpose retainedRank`, `import "algebra.lth" Iso`.
