# Characterizations of the key objects

Draft 1, 2026-10-05; the rewrite of §8 is done. For each object the
libraries use, the laws that determine its operations (`05` R10, `01 §6`), what today's laws say
instead, and what the rewrite changes. The mathematics is standard; the point is to write it as
the laws of the object, so that every implementation is a model of them.

Principle (Luciano, 2026-10-05): find the mathematical object that best represents each concept and
put it as the invariant of the type. Laws have one name each, written in `algebra` in their most
general form; structures are built by inclusion; nothing is declared twice under two names.

## 0. Notation

Every symbol used in this document.

- `Real`, `Float64`, `Int`, `Fin n`: as in `06`. `n` is a dimension, `i`, `j`, `k` are indices.
- `V`, `W`: vector spaces over `Real`; `x`, `y`, `z` their vectors; `a`, `b` scalars.
- `<x, y>`: an inner product; `|x|`: its norm, `sqrt <x, x>`.
- `e i`: the i-th vector of the standard basis; `delta i j`: 1 when `i == j`, else 0.
- `A`, `B`: matrices, read as linear maps; `A x` the map applied; `A^T` the transpose; `I` the
  identity; `tr`, `det`: trace and determinant.
- `eq`: the equality of the presentation (`05` R8); on `Float64` and arrays it is `approx` with the
  tolerance of `06 §8`.
- "Characterizes": a set of laws determines the operation uniquely, up to `eq`. Where that is a
  theorem it is named.

## 1. Vectors: the Euclidean space of dimension n

**The object.** `Euclidean n`: a vector space over `Real` with an inner product and a basis of
`n` vectors that is orthonormal. In Luthier its carrier is `Vec Real n = Fin n -> Real`, so the
coordinates are application and the basis is `e i = \ k { delta i k }`; both are definitional.

**The laws.**
- `VectorSpace` (in `algebra`): `add` associative and commutative with `zero` and `neg`; `scale`
  associative, unital, distributive over `add` and over `+`.
- `InnerProductSpace` (in `algebra`): `inner` symmetric, bilinear, positive on nonzero vectors.
- The basis: `inner (e i) (e j) == delta i j` (orthonormal), and every vector is the combination of
  its coordinates: `x == sum_i (x i) (e i)`.

**What this determines.** Bilinearity and orthonormality give `inner x y == sum_i x i * y i`
(theorem); `norm x == sqrt (inner x x)` is a definition; `zeros n`, `ones n`, `add`, `scale`
are determined pointwise by the vector space laws with the coordinates. So `dot` is characterized,
and the leaf `dot` of numpy is a model of the characterization, not of `dotDef`.

**Today.** `Vec` is the function type with no laws; `dot` is a hole whose only law is
`DotAgrees` (equals `dotDef`); the `InnerProductSpace` laws are applied to an instance in
`algebra_python`, apart from the leaf. The rewrite states the laws on `Euclidean n` and certifies
`dotDef` and numpy's `dot` as two models; `DotAgrees` remains as the corollary that tightens the
tolerance.

## 2. Matrices: linear maps with a basis

**The object.** `Mat Real m n` is a linear map from `Euclidean n` to `Euclidean m`, together with
its table on the bases: `entry A i j = coord (A (e j)) i`. In Luthier the carrier is
`Fin m -> Fin n -> Real`, so `entry` is application.

**The laws.**
- `matVec`: linear (`LeftDistrib` and `CommutingActions` with the scaling, in `algebra`), and its table is the
  matrix: `coord (matVec A (e j)) i == A i j`. A linear map is determined by its values on a
  basis: this characterizes `matVec`.
- `matMul`: `matVec (matMul A B) x == matVec A (matVec B x)` (`Associative` of the action: composition acting is acting twice). Since `matVec` is
  injective on matrices (a map determines its table), this characterizes `matMul`.
- `transpose`: `inner (matVec A x) y == inner x (matVec (transpose A) y)` (`AdjointOfInner`). The
  adjoint is unique: characterizes `transpose`.
- `identity n`: `matVec (identity n) x == x` (`LeftIdentity` of the action).
- `trace`: linear in `A`, `tr (matMul A B) == tr (matMul B A)`, `tr (identity n) == n`. A linear
  functional on square matrices that is cyclic is a multiple of the trace; the normalization fixes
  it: characterizes `trace`.
- `det`: multilinear in the rows, alternating (two equal rows give 0; swapping two rows changes the
  sign), `det (identity n) == 1`. This is the definition of the determinant as the unique such
  function; Laplace's expansion (`detDef`) is a model.
- `frob`: `frob A == sqrt (tr (matMul (transpose A) A))`, a definition.

**Today.** `matVec`, `matMul`, `transpose`, `trace`, `det` are holes with `...Agrees` laws against
`...Def`; the characterizing laws (the action laws, `AdjointOfInner`, `TransposeIsAdjoint`,
`MatMulAssociates`) exist in `algebra` and in the "laws the definitions do not need" section of
`array`, treated as secondary. The rewrite makes them the laws of the object.

## 3. Solving, the spectrum, the pseudo-inverse

- `solve A b` on a nonsingular `A`: `matVec A (solve A b) == b` (`SolveInverts`). Unique by
  nonsingularity: characterizes `solve`. The domain is a law: `det A /= 0`, or `A` symmetric
  positive definite where that is what the program has.
- `eigen A` on a symmetric `A`, returning the values `e` and the vectors `V`: `A V == V diag(e)`,
  `transpose V V == I` (orthonormal), `e` ascending. This characterizes the pair up to the order and
  sign of the vectors of a repeated value, which `eq` on the spectrum does not see. `eigvalsSym` is
  its first component. Returning the vectors is what makes the law universal; "the values of `A`
  are `e`" alone is an existential (there exist vectors) that version 0 cannot run.
- `invSqrtSym A` on symmetric positive definite `A`: `M` symmetric, positive definite, with
  `M A M == I`. The positive definite square root is unique: characterizes `M`.
- `pinvSym A` on symmetric `A`: Moore-Penrose, `A P A == A`, `P A P == P`, `A P` and `P A`
  symmetric. Unique: characterizes `P`.
- `retainedRank A`: the rank of the projector `A P`: `retainedRank A == round (tr (matMul A (pinvSym A)))`.
  It is defined through the pseudo-inverse, with the threshold of the retained subspace as the
  pseudo-inverse's.
- `pinvSqrtSym A`: `M` symmetric positive semidefinite with `M A M == A P` (the projector).

**Today.** All leaves certified against Jacobi written natively (`eigenDef`); `SolveInverts`,
`InvSqrtInverts`, `EigenvaluesSumToTrace`, `EigenvaluesMultiplyToDet` exist as secondary laws.

## 4. Reductions over a vector

- `total x == inner x (ones n)`: a definition through the inner product.
- `product x`: `product (append x a) == a * product x`, `product (zeros 0) == 1`: the fold,
  characterized by its recursion.
- `maximum x`, `minimum x`, `maxAbs x`: an upper bound that is attained. The bound is universal
  (`x i <= maximum x` for all `i`); that it is attained is an existential (some `i` has
  `x i == maximum x`), which version 0 writes as `maximum x == x (argmax x)` with `argmax` one more
  leaf, or leaves noted (`05 §10`).

## 5. Tables

**The object.** A table is a finite set of named, typed columns and `nRows` rows: a function
from a column name and a row to a cell, defined exactly on the names of the schema.

**The laws** (`Table` as a declared type over its labeled base, defined by them):
- names are distinct;
- `cell c r` is `just` exactly when `c` is a name of the schema (`hasColumn`), and `nothing`
  otherwise;
- well-kinded: the cell of a column of kind `"int"` is `int k`, of `"float"` is `real x`, of
  `"str"` is `text s`;
- extensionality: two tables with the same schema and the same cells are the same (`sameTable`).

**What this changes.** `intAt`, `realAt`, `textAt` stop returning `0`, `0.0`, `""` where the
column is missing or of another kind: their column argument carries the precondition
`hasColumn t c "int"`, and the impossible branches are unreachable by the laws. `Codec` is already
right.

## 6. Objectives of an optimization

**Today.** `Objective = { value, grad, stepMatrix }` with no law: nothing ties `grad` to `value`.

**The laws.** `GradIsGradient value grad`: the directional derivative of `value` along `grad`,
by central difference, equals `|grad|^2` (the law `ScoreIsGradient` of `probability`, which does
this for the likelihood). `stepMatrix` symmetric and positive semidefinite: `inner v (stepMatrix
x v) >= 0`. Whether it approximates the Hessian is a quality of the method, not a law of the
objective. With these, `Objective` is a declared type defined by its laws, and the laws of
Levenberg-Marquardt (`StepRule`, `DescentDirection`, `Certified`) stand on an objective that
cannot lie.

## 6b. The algebra the rest stands on (rewritten 2026-10-05)

Laws of a relation: `Reflexive`, `Symmetric`, `Antisymmetric`, `Transitive`, `Total`. `Symmetric`
takes any function of two arguments of one type with an equality on its result, so it is the
symmetry of a relation, the commutativity of an operation, the symmetry of a bilinear form and of a
matrix's entries. Laws of an action `act : M -> X -> V`: `Associative`, `LeftIdentity`,
`LeftDistrib`, `RightDistrib`, `CommutingActions`, `Homogeneous`; the laws of a binary operation are
their case M = X = V. Structures by inclusion: `Setoid`, `TotalOrder`, `Monoid`, `Group`,
`AbelianGroup` (a group whose operation is symmetric), `Ring` (an abelian group and a monoid over one
setoid, joined by distributivity), `CommutativeRing`, `Field`, `OrderedField`,
`CompleteOrderedField`; `VectorSpace K F V` over a field, `InnerProductSpace K F V` over an ordered
field, `LinearMaps`. Instances: `intRing : CommutativeRing Int`, `realField : CompleteOrderedField
Real` (axiom). `float64Field` was removed on 2026-10-05: the doubles are not a field; what they have
is the rounding law of `rational.lut` (06 §8).

A symmetric matrix and a commutative operation are different objects under one law. The matrix is a
symmetric bilinear form (equivalently a self-adjoint map, `⟨x, A y⟩ == ⟨A x, y⟩`); on the basis its
form is the entry function, so `Symmetric` over the indices is the law over all vectors by
bilinearity, and over the indices it is finite and checked exhaustively.

## 7. Already characterized

`Kernel` (three presentations, one law per side), `BeliefFamily` (exchangeability, the chain of
evidence, calibration), `Codec` (round trip, canonical, tolerant, rejects), and the structures of
`algebra` (rings, fields, spaces). These are the pattern the rest follows.

## 8. The rewrite, done 2026-10-05

1. `algebra`: one law per name in its most general form (§6b), `Homomorphism` with the two
   distributive laws defined through it, `Orthonormal` and `Euclidean K F V n`, the exact setoids,
   `float64Field` (moved here from `algebra_python`), and the folds over the indices: `fold` of a
   monoid, associated to the right, with `sumTo`, `sumToInt`, `factorial`, `power`, `forallBelow`,
   `existsBelow` and `forallPairs` defined through it.
2. `array`: each leaf declared with its laws in its type, so `array_python` fills it
   (`dot := extern ...`) and certifies the leaf itself; the 24 copies are gone. Pointwise
   operations carry their coordinate law (the characterization of the vector space of functions);
   `trace` is additive, cyclic and `n` on the identity (`TraceAdditive` is `Homomorphism`); `det`
   multilinear, alternating and one on the identity; `norm` and `total` are the inner product's;
   `product` by its recursion; `maximum`, `minimum`, `maxAbs` an upper bound that is attained
   (`GreatestOf`, the existential as a fold over the finite indices); `matVec` has its table on
   the basis; `invSqrtSym`, `pinvSym`, `pinvSqrtSym`, `retainedRank`, `cond` as in §3; `approxVec`
   and `approxMat` are `approx` entry by entry. The structural laws of `add`, `scale`, `dot`,
   `matVec`, `matMul`, `transpose` are the instances `vecSpace`, `euclidean` (with the basis
   orthonormal) and `matrices` of `algebra_python`, whose components are the leaves. `...Agrees`
   kept as corollaries where a native definition exists. The second names of the projections
   (`length`, `at`, `entry`, `rows`, `cols`, `tabulate`) are gone: `v.n`, `v.f k`, `(n, g)`.
   `symmetric tol a` is `Symmetric` over the indices judged by `approx tol`: exact for
   `SymmetricSquare`, within rounding for a computed matrix, whose positivity is read on its
   symmetric part.
3. `table`: `Table` is declared over its labeled base and defined by the laws of its schema; the
   accessors take the column as a precondition. In `distance_graph` the schema is checked first
   (`ValidGraph` reads rows only on a `GraphWithColumns`), and `experiment_zero` validates the graph
   before fitting it, which it did not do before.
4. `optimization`: `Objective` carries its dimension and is defined by `GradIsGradient` and
   `StepMatrixPositive`; `MaximizerAscends` and `MaximizerStationary` are what any maximizer
   satisfies. `IsGradient` (in `array`) is the one gradient law, used by the score and the objective.
5. `probability`: the shift is an action of the vectors on Theta (`ShiftByZero` is `LeftIdentity`,
   `ShiftComposes` is `Associative`), the information is symmetric positive semidefinite
   (`InfoIsPositive`), `Kernel` contains a `DensityPair` instead of restating its laws, and the
   uniformity of a transform or a rank is one law, `UniformDraws`, used by the kernel, both
   calibrations of `belief`, and `normalVec`, now declared in `probability` with its law (its
   probability integral transform is uniform) and bound in `probability_python`. `BeliefFamily`'s
   `same` and `Codec`'s `eq` are `Setoid`s; typing `same` so showed the Gaussian one was not
   symmetric (the gap between means was measured in the first belief's precision only).
6. Project: `positions.lut` writes once the distance between two nodes, the distances of the pairs,
   their Jacobian and the layout `Iso` between the 3 x N matrix and the vector; `distances`,
   `distance_graph` and `experiment_zero` use them. The gauge of `distances` says its fixed
   coordinates once and derives the rest. `experiment_zero` reproduces session A bit for bit.

## 9. Open

- The existential laws (attained maximum, existence of eigenvectors when only the values are
  returned): the witness grade of `05 §10`. Over the finite indices the existential is a fold and
  is tested (`GreatestOf`); over a continuous domain it is not.
- The values of `eigvalsSym` alone are not characterized by trace and determinant. The power sums
  `sum_i lambda_i^k == tr (A^k)` for k up to n would characterize them (Newton's identities), at
  the price of a monoid of matrices with an equality within rounding; not done.
- The leaves do not carry their shapes in their types (`matVec : (a : Mat Float64) -> VecOf a.n ->
  VecOf a.m`): every call site would carry an obligation, and those inside definitions over a
  type without a generator would stay pending. The laws quantify over shaped values instead.
- The laws of a type are not checked on values the environment returns: a table that
  `luthier/tables.py` parses is a `Table` by its type, and nothing tests its schema laws on it.
  Either the bridge checks a refinement on what crosses, or each extern returning a lawful type is
  certified by a law-lambda; neither is in place.
- The parameter spaces of the positions (`ThetaPos`, `ThetaFull`) are `Vec Float64`, not vectors of
  their dimension: `Likelihood` is invariant in Theta (its `shift` takes and gives one), and the
  Gaussian beliefs, `Objective` and `Maximizer` work on `Vec Float64`, so a refined Theta does not
  pass. The dimension is a precondition of `embed`, `meanDist` and `jacDist` (`HasFree`) and is
  what the generators produce. An `Objective` over `VecOf dim` would carry it; not done.
- `Maximizer` and `Objective`: laws quantified over functions of an infinite domain have no
  generator, so an objective built by `negate` and the `Maximizer` type itself stay pending; they
  are certified on the problems of `optimization_check` by law-lambdas.
- Rank is defined numerically, through the pseudo-inverse's threshold; the rank of the ideal object
  is not continuous and has no tolerance version.
- The tolerances are written by hand (`roundingSlack`); `06 §8` makes them consequences of the
  rounding law.
