# The new core: execution plan

Written 2026-10-17 by Claude Fable 5.1, an agent of the coordinating session, on the brief
`record/plan/core-2026-10-17/prompt-design.md`. Inputs: the library at ca90ee8 (`luthier check -v`
run on it, the greps below), `record/decisions.md` D-2026-10-14-b, D-2026-10-16-l, D-2026-10-17-a
to -i, `record/principles-language.md` L1 to L3, L7, L9.14, L10.12, spec 4.S14, 5.S6, 12.S22,
12.S23, 12.R2. The questions this design leaves to Luciano are in `decisions.md` beside this file;
every choice marked [proposed] here is the agent's, one commit undoes it.

Status: design; no bite started. The library at ca90ee8: 494 test lines in tests/tester, 31 stores
with 927 entries over 208 distinct laws; `check -v` reports 38 unclaimed Bool laws in lib/; the
suite was 799 passed at a1c994b (record/plan/code-follows-principles-2026-10-16.md) and a full
`pytest tests` run takes well over fifteen minutes, so a bite runs it in the background.

## 1. The layout

```
src/luthier/lib/core/
  core.lut                      what the interpreter provides (11.R2) and the claims of its own
                                types and of the kernel's forms (absorbs kernel_models.lut)
  lists.lut                     the generic library of lists (map, filter, fold, all, any, member,
                                lookup, append, concat, length, ...) with its claims of containers
  properties/
    relations.lth               Reflexive, Irreflexive, Symmetric, Antisymmetric, Transitive, Total,
                                Asymmetric; Equivalence, Preorder, PartialOrder, TotalOrder,
                                StrictOrder; the subtypes Related, Chain, Both
    operations.lth              Associative, Commutative, Idempotent, Cancellative, Neutral,
                                Absorbing, Invertible, Distributive, Absorptive, Complemented,
                                Distinct; the within-bound versions
    functions.lth               id, compose, flip, const; Pointwise (the equality of functions);
                                Injective, Surjective, Bijective, Idempotent, Involutive, Monotone,
                                Preserving, Congruent, LandsIn, Inverse, Isomorphism
  structures/
    equality.lth                Object, Concrete, structural, Structural; Metric and its variants,
                                Ball, Tolerance, MetricWithin
    order.lth                   Least, Greatest, Discrete, MonotoneIn; OrderedSemiring
    algebraic.lth               Semigroup, Monoid, CommutativeMonoid, Group, AbelianGroup, Semiring,
                                Ring, CommutativeRing, Lattice, BooleanAlgebra
    containers.lth              Sized, Indexed, Functor, Foldable; SizeMap, AtMap, SizeAppend,
                                Extensional; pointwise equality and sup distance of a container
    universal.lth               Terminal, Initial, Exponential, Product, Coproduct, NamedProduct,
                                NamedCoproduct, Equalizer, Pullback, Coequalizer, FreeMonoid
```

This is the layout D-2026-10-17-g proposes, kept. Reasons it holds up against the alternatives
considered: one file per subsection keeps each under 200 lines (kernel_laws.lth is 296 and
would reach 600 with the additions); properties and structures are two directories because a
property is a predicate on data and a structure is a record of data with its properties applied
(section 2), so the import of a file says which kind enters. Imports from any file name the path
under lib/: `import "core/properties/relations.lth" Reflexive Transitive`; check.py's `resolve`
already looks up `d / name` under lib/, so a subpath needs no code. core.lut keeps enclosing the
top-level scope of every file (12.S22); lists.lut is imported by name (decisions.md, question 1).

Stores follow their files (L10.12: an entry lives beside the file that makes the claim):
`lib/core/core.cert.json`, `lib/core/lists.cert.json`; the structures' and properties' laws are
claimed by core.lut, lists.lut and the libraries, so the .lth files keep no store. Test programs:
`tests/tester/core_laws.test.lut`, `core_controls.test.lut`, `lists_laws.test.lut`,
`lists_controls.test.lut`.

Host code the layout touches: `run.py:143` (`CORE = ... / "lib" / "core.lut"` becomes
`lib/core/core.lut`), `run.py:9`'s docstring, and the tests that name kernel_laws.lth
(`tests/test_run.py:654-657, 687, 1164`, `tests/test_check.py:427, 552`, `tests/test_tester.py:69`,
`tests/test_elaborate.py:364`, `tests/test_check_quotes.py` if it reads the file).

## 2. The two forms: property and structure

A property is a Bool law over a type, its equality and the datum it qualifies, with the quantified
variables last (D-2026-10-17-b, -c):

```
Commutative (A B : U) (o : Object B) (op : A -> A -> B) (x y : A) : Bool := o.eq (op x y) (op y x)
```

A structure is a record of its data, with each law a one-line application of a property to a field,
and its definition the conjunction of those lines (today's pattern, which run.py's theory-law
enumeration and the tester handle; 5.S6):

```
Monoid (M : U) (o : Object M) : { neutral : M, combine : M -> M -> M }
MonoidAssociative (M : U) (o : Object M) (m : Monoid M o) (x y z : M) : Bool := Associative M o m.combine x y z
MonoidNeutral (M : U) (o : Object M) (m : Monoid M o) (x : M) : Bool := Neutral M o m.combine m.neutral x
Monoid (M : U) (o : Object M) := MonoidAssociative M o & MonoidNeutral M o
```

[proposed] The structure keeps a record rather than being a bare predicate on its data
(`Monoid A o op e := Associative A o op & Neutral A o op e`): a bare predicate's conjuncts have
different quantified variables each, and the tester quantifies a conjunction's variables as one
law's today (tester.py `_conjuncts`, run.py's enumeration); a claim `ListIsAMonoid : Bool := Monoid
(List A) o { neutral := nil, combine := append A }` is the form the runner already evaluates
(core.lut's `UnitIsTerminal`). The law's text is still written once, in the property; the one-line
wrapper names the field it applies to. When the tester learns to quantify each conjunct on its
own, the record can go; nothing else depends on it.

A theory claims a property on its own operation by the same one-line form, binding the drawn
domain in the wrapper and applying the property at the carrier:

```
PlusCommutative (d : Doubles) (x y : Moderate) : Bool := Commutative Float64 Float64 (structural Float64) d.plus x y
```

The wrapper's parameters are the subtype the test draws from (`Moderate`), the property is stated
at the type the operation is closed on (`Float64`); a subtype passes where its type is expected
(3.S6). This is why `Commutative` takes a domain `A` and a codomain `B`: an operation drawn on a
subtype of its carrier is not closed on the subtype. `Associative` needs closure and is stated at
the carrier only. The wrapper's name is the field's name joined to the adjective
(`PlusCommutative`, `MeetCommutative`, `CombineAssociative`), and it is what a test line names.

The checker counts a property as claimed when any body mentions it (check.py `claimed_laws`,
4.S14), so the wrappers claim the properties; the properties are also tested on their own at listed
instances in `core_laws.test.lut` and refuted at wrong instances in `core_controls.test.lut`
(L9.14: a law without a refuted model is evidence of nothing).

The equality parameter `o : Object A` is explicit everywhere (D-2026-10-17-b's signature). For a
concrete type it is `structural A`; for a type holding functions (`Vec`, `Mat`, `Table`) it is the
pointwise equality containers.lth builds (section 3.8), which is how `approxVec exact` disappears.

## 3. The files, with their declarations

Signatures in Luthier syntax; `luthier check` passed on a scratch file holding the forms used below
(dependent record fields, `F : U -> U`, conjunctions of partially applied laws, `fn` bodies). Bodies
are given where they fix the meaning; the rest is the session's.

### 3.1 properties/relations.lth

```
-- the pairs and chains a relation relates: drawn by their generators, said once (7.S12; replaces
-- EqualPair, EqualChain, LeqPair x3, LeqChain x3, LeqBoth x2)
Related (A : U) (r : A -> A -> Bool) : U := { x y : A | r x y }
Chain (A : U) (r : A -> A -> Bool) : U := { x y z : A | r x y and r y z }
Both (A : U) (r : A -> A -> Bool) : U := { x y : A | r x y and r y x }

Reflexive (A : U) (r : A -> A -> Bool) (x : A) : Bool := r x x
Irreflexive (A : U) (r : A -> A -> Bool) (x : A) : Bool := not (r x x)
Symmetric (A : U) (r : A -> A -> Bool) (p : Related A r) : Bool := r p.y p.x
-- by its contrapositive over every pair (numbers.lth's LeqAntisymmetric, 7.S12: no rare premise)
Antisymmetric (A : U) (o : Object A) (r : A -> A -> Bool) (x y : A) : Bool := o.eq x y or not (r x y and r y x)
Asymmetric (A : U) (r : A -> A -> Bool) (p : Related A r) : Bool := not (r p.y p.x)
Transitive (A : U) (r : A -> A -> Bool) (c : Chain A r) : Bool := r c.x c.z
Total (A : U) (r : A -> A -> Bool) (x y : A) : Bool := r x y or r y x

Equivalence (A : U) (r : A -> A -> Bool) : Bool := Reflexive A r & Symmetric A r & Transitive A r
Preorder (A : U) (r : A -> A -> Bool) : Bool := Reflexive A r & Transitive A r
PartialOrder (A : U) (o : Object A) (r : A -> A -> Bool) : Bool := Preorder A r & Antisymmetric A o r
TotalOrder (A : U) (o : Object A) (r : A -> A -> Bool) : Bool := PartialOrder A o r & Total A r
StrictOrder (A : U) (r : A -> A -> Bool) : Bool := Irreflexive A r & Asymmetric A r & Transitive A r
```

`Object` is imported from structures/equality.lth; relations.lth needs only its field `eq`.
[proposed] The composite predicates (`Equivalence`, orders) are conjunctions of applied properties
and are claimed through structures' wrappers (`Object`'s laws claim `Equivalence A o.eq`).

### 3.2 properties/operations.lth

```
Associative (A : U) (o : Object A) (op : A -> A -> A) (x y z : A) : Bool := o.eq (op (op x y) z) (op x (op y z))
Commutative (A B : U) (o : Object B) (op : A -> A -> B) (x y : A) : Bool := o.eq (op x y) (op y x)
Idempotent (A : U) (o : Object A) (op : A -> A -> A) (x : A) : Bool := o.eq (op x x) x
LeftNeutral (A : U) (o : Object A) (op : A -> A -> A) (e : A) (x : A) : Bool := o.eq (op e x) x
RightNeutral (A : U) (o : Object A) (op : A -> A -> A) (e : A) (x : A) : Bool := o.eq (op x e) x
Neutral (A : U) (o : Object A) (op : A -> A -> A) (e : A) (x : A) : Bool := LeftNeutral A o op e x and RightNeutral A o op e x
Absorbing (A : U) (o : Object A) (op : A -> A -> A) (z : A) (x : A) : Bool := o.eq (op x z) z and o.eq (op z x) z
-- by its contrapositive: unequal results on unequal arguments
Cancellative (A : U) (o : Object A) (op : A -> A -> A) (x y z : A) : Bool := o.eq y z or not (o.eq (op x y) (op x z))
Invertible (A : U) (o : Object A) (op : A -> A -> A) (e : A) (inv : A -> A) (x : A) : Bool :=
  o.eq (op x (inv x)) e and o.eq (op (inv x) x) e
Distributive (A : U) (o : Object A) (times plus : A -> A -> A) (x y z : A) : Bool :=
  o.eq (times x (plus y z)) (plus (times x y) (times x z)) and o.eq (times (plus y z) x) (plus (times y x) (times z x))
Absorptive (A : U) (o : Object A) (meet join : A -> A -> A) (x y : A) : Bool :=
  o.eq (meet x (join x y)) x and o.eq (join x (meet x y)) x
Complemented (A : U) (o : Object A) (op : A -> A -> A) (complement : A -> A) (unit : A) (x : A) : Bool :=
  o.eq (op x (complement x)) unit
Distinct (A : U) (o : Object A) (a b : A) : Bool := not (o.eq a b)

-- the same within a bound over a distance: the bound a function of the arguments, from the
-- claimant's theory, never a constant (D-2026-10-17-f, P11)
AssociativeWithin (A : U) (d : A -> A -> Float64) (op : A -> A -> A) (bound : A -> A -> A -> Float64) (x y z : A) : Bool :=
  d (op (op x y) z) (op x (op y z)) <= bound x y z
CommutativeWithin (A B : U) (d : B -> B -> Float64) (op : A -> A -> B) (bound : A -> A -> Float64) (x y : A) : Bool :=
  d (op x y) (op y x) <= bound x y
NeutralWithin (A : U) (d : A -> A -> Float64) (op : A -> A -> A) (e : A) (bound : A -> Float64) (x : A) : Bool :=
  d (op e x) x <= bound x and d (op x e) x <= bound x
DistributiveWithin (A : U) (d : A -> A -> Float64) (times plus : A -> A -> A) (bound : A -> A -> A -> Float64) (x y z : A) : Bool :=
  d (times x (plus y z)) (plus (times x y) (times x z)) <= bound x y z
InvertibleWithin (A : U) (d : A -> A -> Float64) (op : A -> A -> A) (e : A) (inv : A -> A) (bound : A -> Float64) (x : A) : Bool :=
  d (op x (inv x)) e <= bound x
```

The within-bound versions take the distance as a function, not a `Metric` record, so a claimant
can pass a `MetricWithin`'s `dist` (a floating-point realization, 3.5) as well as a `Metric`'s.
[proposed] `Distributive` states both sides; a one-sided version is not needed by any present
claimant (all rings here are commutative).

### 3.3 properties/functions.lth

```
id (A : U) : A -> A := fn x { x }
compose (A B C : U) (g : B -> C) (f : A -> B) : A -> C := fn x { g (f x) }
flip (A B C : U) (f : A -> B -> C) : B -> A -> C := fn b a { f a b }
const (A B : U) (b : B) : A -> B := fn a { b }

-- the equality of functions: pointwise from the codomain's, sampled on the domain (D-2026-10-17-d)
Pointwise (A B : U) (o : Object B) (f g : A -> B) (x : A) : Bool := o.eq (f x) (g x)
Pointwise2 (A B C : U) (o : Object C) (f g : A -> B -> C) (x : A) (y : B) : Bool := o.eq (f x y) (g x y)
-- the function type's Object, for a claimant that needs one as a value (an `Indexed` container's
-- entries are a function); its laws are the codomain's, applied pointwise, so it claims nothing new
functions (A B : U) (o : Object B) : Object (A -> B)

-- by its contrapositive over every pair
Injective (A B : U) (oA : Object A) (oB : Object B) (f : A -> B) (x y : A) : Bool := oA.eq x y or not (oB.eq (f x) (f y))
-- surjective by a witness: a section `s` with `f (s y) == y`
Surjective (A B : U) (o : Object B) (f : A -> B) (s : B -> A) (y : B) : Bool := o.eq (f (s y)) y
-- `g` undoes `f`
Inverse (A B : U) (o : Object A) (f : A -> B) (g : B -> A) (x : A) : Bool := o.eq (g (f x)) x
Isomorphism (A B : U) (oA : Object A) (oB : Object B) (to : A -> B) (from : B -> A) : Bool :=
  Inverse A B oA to from & Inverse B A oB from to
Bijective (A B : U) (oA : Object A) (oB : Object B) (f : A -> B) (s : B -> A) : Bool :=
  Injective A B oA oB f & Surjective A B oB f s
Idempotent (A : U) (o : Object A) (f : A -> A) (x : A) : Bool := o.eq (f (f x)) (f x)
Involutive (A : U) (o : Object A) (f : A -> A) (x : A) : Bool := o.eq (f (f x)) x
-- order-preserving between two relations, over the pairs the first relates
Monotone (A B : U) (r : A -> A -> Bool) (s : B -> B -> Bool) (f : A -> B) (p : Related A r) : Bool := s (f p.x) (f p.y)
-- a homomorphism of binary operations (SizeAppend is one from append to +)
Preserving (A B : U) (o : Object B) (opA : A -> A -> A) (opB : B -> B -> B) (f : A -> B) (x y : A) : Bool :=
  o.eq (f (opA x y)) (opB (f x) (f y))
-- respects an equivalence: equal arguments, equal results (Substitutive for one function)
Congruent (A B : U) (rA : A -> A -> Bool) (oB : Object B) (f : A -> B) (p : Related A rA) : Bool := oB.eq (f p.x) (f p.y)
-- the result lies in a subtype, given by its predicate
LandsIn (A B : U) (f : A -> B) (p : B -> Bool) (x : A) : Bool := p (f x)

IdempotentWithin (A : U) (d : A -> A -> Float64) (f : A -> A) (bound : A -> Float64) (x : A) : Bool := d (f (f x)) (f x) <= bound x
InvolutiveWithin (A : U) (d : A -> A -> Float64) (f : A -> A) (bound : A -> Float64) (x : A) : Bool := d (f (f x)) x <= bound x
PointwiseWithin (A B : U) (d : B -> B -> Float64) (f g : A -> B) (bound : A -> Float64) (x : A) : Bool := d (f x) (g x) <= bound x
```

The file has two `Idempotent`s with operations.lth (one on an operation, one on a function); they
live in different files and an importer names the one it needs. [proposed] `functions (A B) (o)`
is declared, not defined: a value of `Object (A -> B)` whose `eq` is a function over an infinite
domain has no body a test could run; what is tested is `Pointwise`. A claimant that wants a
container's equality as a value uses containers.lth's `pointwise`, which is finite.

### 3.4 structures/equality.lth, part one: Object

```
Object (A : U) : { eq : A -> A -> Bool }
ObjectEquivalence (A : U) (o : Object A) : Bool := Equivalence A o.eq
Object (A : U) := ObjectEquivalence A
EqualPair (A : U) (o : Object A) : U := Related A o.eq

hasStructuralEquality : U -> Bool
Concrete : U := { A : U | hasStructuralEquality A }
structural (A : Concrete) : Object A := { eq := fn x y { x == y } }
-- the structural equality's own laws, each on its own cases (review of layers 0-1, A), and
-- substitutive over every function (D-2026-10-13-z)
Structural (A : Concrete) : { eq : A -> A -> Bool }
StructuralEquivalence (A : Concrete) (s : Structural A) : Bool := Equivalence A s.eq
Substitutive (A : Concrete) (s : Structural A) (B : Concrete) (f : A -> B) (p : Related A s.eq) : Bool := f p.x == f p.y
Structural (A : Concrete) := StructuralEquivalence A & Substitutive A
```

`structural` replaces kernel_models.lut's `structuralEquality`; it is a value the theory of equality
is about (12.S23 allows one), not a model of a theory declared elsewhere.

### 3.5 structures/equality.lth, part two: Metric

```
-- a metric space over the type's equality (D-2026-10-17-f): d : A x A -> R, realized in Float64
Metric (A : U) (o : Object A) : { dist : A -> A -> Float64 }
-- M1 in two laws: zero on equal pairs; equal where zero, by its contrapositive over every pair
MetricZeroOnEqual (A : U) (o : Object A) (d : Metric A o) (p : EqualPair A o) : Bool := d.dist p.x p.y == 0.0
MetricIndiscernible (A : U) (o : Object A) (d : Metric A o) (x y : A) : Bool := o.eq x y or not (d.dist x y == 0.0)
-- M2: `dist == flip dist`
MetricSymmetric (A : U) (o : Object A) (d : Metric A o) (x y : A) : Bool := Commutative A Float64 (structural Float64) d.dist x y
-- M3
Triangular (A : U) (d : A -> A -> Float64) (x y z : A) : Bool := d x z <= d x y + d y z
Ultratriangular (A : U) (d : A -> A -> Float64) (x y z : A) : Bool := d x z <= larger (d x y) (d y z)
MetricTriangular (A : U) (o : Object A) (d : Metric A o) (x y z : A) : Bool := Triangular A d.dist x y z
Metric (A : U) (o : Object A) := MetricZeroOnEqual A o & MetricIndiscernible A o & MetricSymmetric A o & MetricTriangular A o
-- non-negativity is a theorem (0 = d(x,x) <= d(x,y) + d(y,x) = 2 d(x,y)) and is not an axiom; it
-- is stated as a derived law so that a control that returns a negative value is refuted by name
MetricNonNegative (A : U) (o : Object A) (d : Metric A o) (x y : A) : Bool := 0.0 <= d.dist x y

-- the variants, by their exact names
Pseudometric (A : U) (o : Object A) : { dist : A -> A -> Float64 }      -- M1 one way: zero on equal, not conversely
Pseudometric (A : U) (o : Object A) := PseudometricZeroOnEqual A o & PseudometricSymmetric A o & PseudometricTriangular A o
Quasimetric (A : U) (o : Object A) : { dist : A -> A -> Float64 }       -- no M2
Quasimetric (A : U) (o : Object A) := QuasimetricZeroOnEqual A o & QuasimetricIndiscernible A o & QuasimetricTriangular A o
Ultrametric (A : U) (o : Object A) : { dist : A -> A -> Float64 }       -- M3 with max
Ultrametric (A : U) (o : Object A) := UltrametricZeroOnEqual A o & UltrametricIndiscernible A o & UltrametricSymmetric A o & UltrametricUltratriangular A o
-- values in [0, inf]: declared with its laws over `Extended`, with no model until one asks
Extended = { finite : NonNegativeFloat || infinite : Unit }
ExtendedMetric (A : U) (o : Object A) : { dist : A -> A -> Extended }

-- a ball: within a radius of a distance, the radius a function of the two points (11.S14: a sum is
-- compared relative to the magnitudes of its terms); replaces the `approx...` and `within` family
Ball (A : U) (d : A -> A -> Float64) (radius : A -> A -> Float64) (x y : A) : Bool := d x y <= radius x y
Tolerance : U := { tol : Float64 | 0.0 <= tol }

-- a floating-point realization of a metric: not a model of `Metric` (D-2026-10-17-f) but a claim
-- that the computed distance is within `bound` of an exact metric; its testable consequences
MetricWithin (A : U) (o : Object A) : { dist : A -> A -> Float64, bound : A -> A -> Float64 }
WithinZeroOnEqual (A : U) (o : Object A) (m : MetricWithin A o) (p : EqualPair A o) : Bool := m.dist p.x p.y <= m.bound p.x p.y
WithinSymmetric (A : U) (o : Object A) (m : MetricWithin A o) (x y : A) : Bool :=
  CommutativeWithin A Float64 absDistance m.dist (fn x y { m.bound x y + m.bound y x }) x y
WithinTriangular (A : U) (o : Object A) (m : MetricWithin A o) (x y z : A) : Bool :=
  m.dist x z <= m.dist x y + m.dist y z + m.bound x y + m.bound y z + m.bound x z
MetricWithin (A : U) (o : Object A) := WithinZeroOnEqual A o & WithinSymmetric A o & WithinTriangular A o
absDistance (a b : Float64) : Float64 := abs (a - b)
```

`abs` and `larger` move here from numbers.lth and probability.lth (`abs` is exact; core defines
`Float64`). `NonNegativeFloat` is grammar.lth's `{ x : Float64 | 0.0 <= x }`, moved here. The
exact models of `Metric` are claimed where their types are defined: core.lut claims `|a - b|` on
`Small` integers (converted, exact below 2^53), the discrete metric on `Bool`; lists.lut claims the
Hamming distance on `List Bool` of equal length and the edit distance when written. The controls
D-2026-10-17-f names go in `core_controls.test.lut`: Kullback-Leibler between two Bernoulli
parameters (fails M2 and M3), relative error `|a - b| / larger |a| |b|` (fails M3), squared
Euclidean `(a - b)^2` (fails M3, 0, 1, 2), and a negative-valued "distance" refuted by
`MetricNonNegative`. The `MetricWithin` model of `absDistance` on `Moderate` doubles is
numbers.lth's, with `bound := fn a b { u * absDistance a b }` where `u = epsilon / 2`, since
`fl(a - b) = (a - b)(1 + delta)`, `|delta| <= u`, and `abs` is exact; the triangle law then holds
with the three bounds, a derivation of one line to cite in the file (Higham 2002, §2.2).
[proposed] Ultrametric's model, when one is asked for: the p-adic or the longest-common-prefix
distance on strings; none is needed now.

### 3.6 structures/order.lth

```
Least (A : U) (leq : A -> A -> Bool) (bottom : A) (x : A) : Bool := leq bottom x
Greatest (A : U) (leq : A -> A -> Bool) (top : A) (x : A) : Bool := leq x top
-- nothing lies strictly between x and its successor (SuccessorIsNext, generic)
Discrete (A : U) (o : Object A) (leq : A -> A -> Bool) (succ : A -> A) (p : Related A leq) : Bool :=
  o.eq p.x p.y or leq (succ p.x) p.y
-- an operation respects the order in its first argument (PlusMonotone x3, TimesMonotone, TimesPositive)
MonotoneIn (A : U) (leq : A -> A -> Bool) (op : A -> A -> A) (p : Related A leq) (z : A) : Bool := leq (op p.x z) (op p.y z)
-- the product of two non-negatives is non-negative, over the pairs above zero
NonNegativePair (A : U) (leq : A -> A -> Bool) (zero : A) : U := { x y : A | leq zero x and leq zero y }
PositiveClosed (A : U) (leq : A -> A -> Bool) (times : A -> A -> A) (zero : A) (p : NonNegativePair A leq zero) : Bool :=
  leq zero (times p.x p.y)

-- Nat's structure (11.R1, D-2026-10-13-t): a commutative semiring totally ordered, the order
-- respected by `+`, zero least, `x + 1` the successor
OrderedSemiring (S : U) (o : Object S) : { semiring : Semiring S o, leq : S -> S -> Bool }
OrderedSemiringIsASemiring (S : U) (o : Object S) (s : OrderedSemiring S o) : Bool := Semiring S o s.semiring
OrderedSemiringTotalOrder (S : U) (o : Object S) (s : OrderedSemiring S o) : Bool := TotalOrder S o s.leq
OrderedSemiringPlusMonotone (S : U) (o : Object S) (s : OrderedSemiring S o) (p : Related S s.leq) (z : S) : Bool := MonotoneIn S s.leq s.semiring.plus p z
OrderedSemiringZeroLeast (S : U) (o : Object S) (s : OrderedSemiring S o) (x : S) : Bool := Least S s.leq s.semiring.zero x
OrderedSemiringDiscrete (S : U) (o : Object S) (s : OrderedSemiring S o) (p : Related S s.leq) : Bool :=
  Discrete S o s.leq (fn x { s.semiring.plus x s.semiring.one }) p
OrderedSemiring (S : U) (o : Object S) := OrderedSemiringIsASemiring S o & OrderedSemiringTotalOrder S o
  & OrderedSemiringPlusMonotone S o & OrderedSemiringZeroLeast S o & OrderedSemiringDiscrete S o
```

A structure that includes another passes the included record to the included theory's head
(`Semiring S o s.semiring`), the form core.lut's claims already use; run.py reads a theory head in a
conjunct through to its laws.

### 3.7 structures/algebraic.lth

Each structure: a record, one wrapper per law applying a property of operations.lth, and the
conjunction. Listed by record and laws; the wrappers follow the naming of section 2.

```
Semigroup (A : U) (o : Object A) : { combine : A -> A -> A }                         -- Associative
Monoid (A : U) (o : Object A) : { neutral : A, combine : A -> A -> A }               -- Associative, Neutral
CommutativeMonoid (A : U) (o : Object A) : { neutral : A, combine : A -> A -> A }    -- Monoid's, Commutative
Group (A : U) (o : Object A) : { neutral : A, combine : A -> A -> A, inverse : A -> A }   -- Monoid's, Invertible
AbelianGroup (A : U) (o : Object A) : { neutral : A, combine : A -> A -> A, inverse : A -> A }   -- Group's, Commutative
Semiring (A : U) (o : Object A) : { zero one : A, plus times : A -> A -> A }
  -- CommutativeMonoid on plus/zero, Monoid on times/one, Distributive times plus, Absorbing times zero, Distinct one zero
Ring (A : U) (o : Object A) : { zero one : A, plus times : A -> A -> A, negate : A -> A }
  -- AbelianGroup on plus/zero/negate, Monoid on times/one, Distributive, Distinct one zero
CommutativeRing (A : U) (o : Object A) : { zero one : A, plus times : A -> A -> A, negate : A -> A }   -- Ring's, Commutative times
Lattice (A : U) (o : Object A) : { meet join : A -> A -> A }
  -- Associative, Commutative, Idempotent on each; Absorptive meet join
BooleanAlgebra (B : U) (o : Object B) : { top bottom : B, complement : B -> B, meet join : B -> B -> B }
  -- Huntington: Commutative meet, Commutative join, Neutral meet top, Neutral join bottom,
  -- Distributive meet join, Distributive join meet, Complemented meet complement bottom,
  -- Complemented join complement top, Distinct top bottom
```

`Semiring`'s `Distinct one zero` and `Ring`'s replace `OneIsNotZero` (kernel_laws.lth, algebra.lth)
and `TopIsNotBottom`. The dual of `Bool`'s algebra is told apart by `if` in core.lut
(`TopIsTheFirstBranch`), where `Bool` is defined (L2.8).

### 3.8 structures/containers.lth

```
Sized (C : U) : { size : C -> Nat }
-- entries at a finite index; a matrix is indexed row-major by Fin (m * n) [proposed]
Indexed (C A : U) : { size : C -> Nat, at : (c : C) -> Fin (size c) -> A }
Functor (F : U -> U) : { map : (A B : U) -> (A -> B) -> F A -> F B }
Foldable (F : U -> U) : { fold : (A M : U) -> (M -> M -> M) -> M -> (A -> M) -> F A -> M }

-- the equality of two containers: same size, equal entries; the Object of a container
sameEntries (C A : U) (i : Indexed C A) (o : Object A) (c d : C) : Bool :=
  if i.size c == i.size d then forallBelow (i.size c) (fn k { o.eq (i.at c k) (i.at d k) }) else false
pointwise (C A : U) (i : Indexed C A) (o : Object A) : Object C := { eq := sameEntries C A i o }
-- the sup distance of two containers over a distance on the entries; of different sizes, infinite
-- is not a value (11.S7), so the distance is 1 + the largest entry and the sizes
supDistance (C A : U) (i : Indexed C A) (d : A -> A -> Float64) (c e : C) : Float64
-- a ball entry by entry, the radius per entry (what approxMatOf states: 11.S14)
entrywiseBall (C A : U) (i : Indexed C A) (d : A -> A -> Float64) (radius : (c : C) -> C -> Fin (i.size c) -> Float64) (c e : C) : Bool

-- the laws a container with map, fold or append must meet (D-2026-10-17-c)
SizeMap (F : U -> U) (A B : U) (i : Indexed (F A) A) (j : Indexed (F B) B) (m : Functor F) (f : A -> B) (c : F A) : Bool :=
  j.size (m.map A B f c) == i.size c
AtMap (F : U -> U) (A B : U) (i : Indexed (F A) A) (j : Indexed (F B) B) (m : Functor F) (f : A -> B) (c : F A) (k : Fin (i.size c)) : Bool
SizeAppend (C : U) (s : Sized C) (append : C -> C -> C) (c d : C) : Bool :=
  Preserving C Nat (structural Nat) append (fn a b { a + b }) s.size c d
Extensional (C A : U) (i : Indexed C A) (o : Object A) (oc : Object C) (c d : C) : Bool :=
  oc.eq c d == sameEntries C A i o c d
MapId (F : U -> U) (A : U) (m : Functor F) (o : Object (F A)) (c : F A) : Bool := o.eq (m.map A A (id A) c) c
MapCompose (F : U -> U) (A B C : U) (m : Functor F) (o : Object (F C)) (f : A -> B) (g : B -> C) (c : F A) : Bool :=
  o.eq (m.map A C (compose A B C g f) c) (m.map B C g (m.map A B f c))
FoldIsTheFreeExtension ...   -- stated in universal.lth's FreeMonoid, claimed by lists.lut
```

`forallBelow`, `existsBelow`, `countBelow`, `foldWith`, `foldFrom` move here from arrays.lth (they
are folds over `Fin n`, which every container's laws need); `sumTo` and `sumToInt` stay in
arrays.lth (a sum in 3.S27's order is the arrays' business). Claimants: `List A` (lists.lut:
`size := length`, `at := nth` made total on `Fin`), `Vec A` and `Mat A` (arrays.lth, D-2026-10-17-c:
`Mat` by `Fin r × Fin c` through the row-major index), `Table` (tables.lth: its rows). The
`approxVec`/`approxMat` family becomes `Ball` or `entrywiseBall` of `supDistance` over
`absDistance` with the radius the law names (section 5, bite 8).

### 3.9 structures/universal.lth

Terminal, Initial, Exponential, Product, Coproduct, NamedProduct, NamedCoproduct, Selected with
their laws keep kernel_laws.lth §2 and §6's text and names (`OnlyThePoint`, `NoValue`, `Beta`,
`PairFst`, `PairSnd`, `Pairing`, `CaseLeft`, `CaseRight`, `CasesAreAll`, `NamedPairs`,
`ProjectionNamesDistinct`, `SelectByName`, `NamedCases`, `InjectionNamesDistinct`, `LabelByName`),
with `(o : Object P)` added where the law compared with `==` on a type parameter. `FreeMonoid` moves
here from kernel_laws.lth §4 with its laws (`FoldNeutral`, `FoldInject`, `FoldCombine`,
`FoldIsItself`), `fold` taking the monoid's data `(N : U) -> (N -> N -> N) -> N -> (A -> N) -> M -> N`
and `IsMonoid` replaced by `Monoid M o { neutral, combine }`. Added, in D-2026-10-17-g's order:

```
-- the equalizer of f and g: E with `include` into A, and every x with f x = g x reached once
Equalizer (A B E : U) (oA : Object A) (oB : Object B) (oE : Object E) : {
  f g : A -> B, include : E -> A, restrict : { x : A | oB.eq (f x) (g x) } -> E }
EqualizerEqualizes (…) (e : E) : Bool := oB.eq (f (include e)) (g (include e))
EqualizerIncludesBack (…) (x : { x : A | oB.eq (f x) (g x) }) : Bool := oA.eq (include (restrict x)) x
EqualizerRestrictsBack (…) (e : E) : Bool := oE.eq (restrict (include e)) e
-- the pullback of f : A -> C and g : B -> C: the pairs that agree in C (D-2026-10-16-a's join)
agreeing (A B C : U) (oC : Object C) (f : A -> C) (g : B -> C) (q : A * B) : Bool := match q { (a, b) -> oC.eq (f a) (g b) }
Pullback (A B C P : U) (oA : Object A) (oB : Object B) (oC : Object C) (oP : Object P) : {
  f : A -> C, g : B -> C, first : P -> A, second : P -> B,
  pair : { q : A * B | agreeing A B C oC f g q } -> P }
PullbackCommutes (…) (p : P) : Bool := oC.eq (f (first p)) (g (second p))
PullbackFst, PullbackSnd, PullbackPairing   -- the product's three laws on the agreeing pairs
-- the coequalizer of f g : A -> B: the quotient Q with `project : B -> Q` identifying f x and g x,
-- and nothing else that a listed map does not already identify
Coequalizer (A B Q : U) (oQ : Object Q) : { f g : A -> B, project : B -> Q, lift : (D : U) -> (B -> D) -> Q -> D }
CoequalizerCoequalizes (…) (x : A) : Bool := oQ.eq (project (f x)) (project (g x))
CoequalizerLifts (…) (D : U) (oD : Object D) (h : { h : B -> D | ... h (f x) = h (g x) ... }) (b : B) : Bool := oD.eq (lift D h (project b)) (h b)
```

[proposed] `Pushout` is declared when a case asks for one: today's gluing of theories over a shared
sub-theory (algebra.lth's `OrderedField` from `Field` and `OrderedRing` over `CommutativeRing`) is
realized by the pullback of their model types, which `Pullback` states; the pushout of theories is
the same fact read from the side of the presentations and has no second model to test. The
pushforward of measures is probability.lth's (D-2026-10-17-g), bite 8b. Models: `Product` and
`Coproduct` the kernel's forms and `Bool`, `Maybe` (core.lut, as today); `Equalizer` `Symmetric` as
the equalizer of `id` and `transpose` (arrays_model.lut), and every subtype `{ x : A | p x }` as
the equalizer of `p` and `const true` (core.lut, one instance); `Pullback` the join of nodes and
measurements by id (distance_graph.lut, bite 8b) and `Mat r k` with `Mat k c` over `k`
(arrays_model.lut); `Coequalizer` `Fin n` as the quotient of `Int` by `x ~ x + n`,
`project := fn x { x mod n }` (core.lut), where `lift` takes the maps a census lists (7.R4).

### 3.10 core/core.lut

Keeps its content (the data, the primitives, the operators) and gains every claim of the kernel's
own types and forms, which kernel_models.lut held (D-2026-10-14-b read to the end: core claims its
models, and the kernel's forms are the interpreter's): `structural` replaces `structuralEquality`
(now in equality.lth); `naturals` becomes `NatIsAnOrderedSemiring : Bool := OrderedSemiring Nat
(structural Nat) { semiring := {...}, leq := fn a b { a <= b } }`; `application`, `pairs`,
`recordXY`, `sumAB` become `KernelApplies`, `PairsAreTheProduct`, `RecordsAreNamedProducts`,
`SumsAreNamedCoproducts`, each `: Bool := Theory ... { model }`. The data claims are rewritten over
the new heads: `BoolIsABooleanAlgebra` (with `TopIsTheFirstBranch` kept here as `Bool`'s own law),
`BoolIsACoproduct`, `MaybeIsACoproduct`, `ListIsTheFreeMonoid` (with `append` and `fold` imported
from lists.lut), `UnitIsTerminal`, `EmptyIsInitial`. Added, since core defines these types (L2.8):
`IntIsACommutativeRing`, `IntIsTotallyOrdered` (numbers_model.lut's `integers`), `StringIsAMonoid`
(numbers_model.lut's `strings`), `SmallIntegersAreAMetric` (`|a - b|` converted), `BoolIsAMetric`
(the discrete metric), `FinIsACoequalizer`, `SubtypeIsAnEqualizer`. `CoreData` names them all.
[proposed] The claims are Bool definitions in a .lut, as `UnitIsTerminal` is today; the test
program `core_laws.test.lut` runs them and the store is `core.cert.json`.

### 3.11 core/lists.lut

```
length (A : U) (xs : List A) : Nat
append (A : U) (xs ys : List A) : List A
concat (A : U) (xss : List (List A)) : List A
reverse (A : U) (xs : List A) : List A
map (A B : U) (f : A -> B) (xs : List A) : List B
filter (A : U) (p : A -> Bool) (xs : List A) : List A
fold (A M : U) (combine : M -> M -> M) (neutral : M) (f : A -> M) (xs : List A) : M     -- to the right, nil -> neutral
foldl (A M : U) (step : M -> A -> M) (start : M) (xs : List A) : M
all (A : U) (p : A -> Bool) (xs : List A) : Bool
any (A : U) (p : A -> Bool) (xs : List A) : Bool
member (A : U) (o : Object A) (x : A) (xs : List A) : Bool
lookup (K V : U) (o : Object K) (k : K) (kvs : List (K * V)) : Maybe V
nth (A : U) (xs : List A) (i : Nat) : Maybe A
at (A : U) (xs : List A) (i : Fin (length A xs)) : A
zip (A B : U) (xs : List A) (ys : List B) : List (A * B)
zipWith (A B C : U) (f : A -> B -> C) (xs : List A) (ys : List B) : List C
take (A : U) (n : Nat) (xs : List A) : List A
drop (A : U) (n : Nat) (xs : List A) : List A
remove (A : U) (o : Object A) (x : A) (xs : List A) : List A
removeAll (A : U) (o : Object A) (xs ys : List A) : List A
distinct (A : U) (o : Object A) (xs : List A) : Bool
insertSorted (A : U) (leq : A -> A -> Bool) (x : A) (xs : List A) : List A
sortBy (A : U) (leq : A -> A -> Bool) (xs : List A) : List A
isEmpty (A : U) (xs : List A) : Bool
singleton (A : U) (x : A) : List A
```

Its claims, in the file (L2.8): `ListIsAMonoid`, `ListIsAFunctor` (MapId, MapCompose),
`ListIsFoldable`, `ListIsIndexed` (length, at), `MapKeepsLength` (SizeMap), `AppendAddsLengths`
(SizeAppend as `Preserving`), `ReverseIsAnInvolution` (Involutive), `FilterKeeps` (LandsIn of every
entry), `MemberOfAppend`, `LookupOfZip`, `SortIsSorted` and `SortIsAPermutation` (sortBy), and the
Hamming distance on `List Bool` of a length as a `Metric`. Tests in `lists_laws.test.lut` at
`List Int` and `List Bool`; controls (`lists_controls.test.lut`): a `map` that drops the last
entry (refutes SizeMap), an `append` that reverses its second argument (refutes the monoid's
associativity), a `reverse` that fixes the head (refutes Involutive), a `sortBy` that drops
duplicates (refutes the permutation law).

### 3.12 What leaves the library

kernel_laws.lth and kernel_models.lut are removed in bite 1 (content moved). laws.lth §2 (the
`is...` templates) is removed in bite 6: nothing claims them today (check -v lists all twelve
unclaimed) and properties/ states each. algebra.lth keeps §3 to §5 (`Field`, `OrderedRing`,
`OrderedField`, `CompleteOrderedField`) rewritten over the core's records and properties, and loses
§0 to §2 (`Iso`, `AbelianGroup`, `CommutativeRing`, now the core's) and its three `Leq...` subtypes.

## 4. Metric, bounds and the within-bound claims of numbers.lth

`Doubles` claims (bite 5), each a one-line wrapper over `Moderate`:

- exactly: `PlusCommutative`, `TimesCommutative` (Commutative at Float64), `PlusNeutral` (0.0),
  `TimesNeutral` (1.0), `DivideNeutral` (`x / 1.0 == x`, kept as its own law), `TimesAbsorbing`
  (0.0), `MinusSelf`, `DivideSelf`, `MinusIsPlusNegated`, `NegateInvolutive` (Involutive of
  `fn x { 0.0 - x }`), `LeqTotalOrder` (TotalOrder of `leq` at Float64 over Moderate: Reflexive,
  Antisymmetric by contrapositive, Transitive over `Chain`, Total), `LessIsStrict`,
  `GreaterIsLessReversed`, `GeqIsLeqReversed`, `UnequalIsNotEqual`, `PlusMonotone` and
  `TimesMonotone` (MonotoneIn), `EpsilonIsTheUlpOfOne`;
- within a bound: `PlusAssociativeWithin` with `bound := fn x y z { 3.0 * gamma2 * (abs x + abs y + abs z) }`,
  where `gamma2 := 2.0 * u / (1.0 - 2.0 * u)`, `u := epsilon / 2.0` (Higham 2002, Lemma 3.1: each
  side is within `gamma2 (|x| + |y| + |z|)` of the exact sum, so their difference is within twice
  that; measuring the difference in floating point and summing the magnitudes in floating point
  each add a factor `(1 + u)`, and `2 (1 + u)^3 < 3`). [proposed] The constant 3 rounds the
  derivation up; D-2026-10-17-f writes `gamma2` alone, which the control run of the first
  certification will confirm or refute (decisions.md, note 3). `TimesAssociativeWithin` with the
  same form over `|x y z|`: `bound := fn x y z { 3.0 * gamma2 * abs (x * y * z) }`;
  `TimesDistributiveWithin` over `|x| (|y| + |z|)`; `DivideInvertsWithin` (`x * (1 / x)` within
  `2 u` of 1, `x : Positive`). Each bound names its source in the file (L9.7, provable by citation);
  the law stays Boolean and tested.
- the realization of the absolute distance: `absDistance` on `Moderate` as a `MetricWithin` with
  `bound := fn a b { u * absDistance a b }` (section 3.5).

`within tol a b` and `withinOf tol scale a b` (numbers.lth) become `Ball Float64 absDistance (fn a b
{ tol * (1.0 + abs a + abs b) }) a b` and `Ball Float64 absDistance (fn a b { tol * scale }) a b`; the
two names stay in numbers.lth as abbreviations with those bodies (every importer keeps working;
the bodies say what they are). `exact : Tolerance := 0.0` stays (arrays.lth) with `Ball` at radius
zero equal to `pointwise` equality, a law (`ExactBallIsEquality`) that claims it.

## 5. The migration map

Every law and helper of today's library that the new core replaces. Old file paths are under
`src/luthier/lib/` unless written otherwise; new ones under `src/luthier/lib/core/`. "wrapper" means
the theory keeps a one-line law of the new name applying the property named. Checked by:

```
cd /home/lmoffatt/Projects/luthier && awk -F'|' '/^\| `/ { print $2 }' record/plan/core-2026-10-17/execution.md \
  | grep -oE '`[^`]+`' | tr -d '`' | grep -vE '…' | sort -u | while read n; do \
  grep -rqE "^$n[ (:]|^$n\$" src/luthier/lib examples tests/tester || echo "MISSING $n"; done
```

(at ca90ee8 the command prints nothing: every old name is defined at the top level of some file).
Names defined in several files are one row per file, or one row naming the files.

### 5.1 Laws and theories

| old name | old file | new name | new file | note |
|---|---|---|---|---|
| `Object` | kernel_laws.lth | `Object` | structures/equality.lth | laws by `Equivalence` |
| `EqualPair` | kernel_laws.lth | `EqualPair` := `Related A o.eq` | structures/equality.lth | |
| `EqualChain` | kernel_laws.lth | `Chain A o.eq` | properties/relations.lth | |
| `Reflexive` | kernel_laws.lth | `Reflexive` | properties/relations.lth | over a relation |
| `Symmetric` | kernel_laws.lth | `Symmetric` | properties/relations.lth | |
| `Transitive` | kernel_laws.lth | `Transitive` | properties/relations.lth | |
| `hasStructuralEquality` | kernel_laws.lth | same | structures/equality.lth | |
| `Concrete` | kernel_laws.lth | `Concrete` | structures/equality.lth | importers: generators.lth, world.lth, generators_model.lut, 3 test programs, tests/test_run.py |
| `Structural` | kernel_laws.lth | `Structural` | structures/equality.lth | |
| `asObject` | kernel_laws.lth | removed | | `Structural` and `Object` share the field; `structural` gives the value |
| `StructuralReflexive` | kernel_laws.lth | `StructuralEquivalence` | structures/equality.lth | |
| `StructuralSymmetric` | kernel_laws.lth | `StructuralEquivalence` | structures/equality.lth | |
| `StructuralTransitive` | kernel_laws.lth | `StructuralEquivalence` | structures/equality.lth | |
| `Substitutive` | kernel_laws.lth | `Substitutive` | structures/equality.lth | |
| `structuralEquality` | kernel_models.lut | `structural` | structures/equality.lth | |
| `Terminal` | kernel_laws.lth | `Terminal` | structures/universal.lth | |
| `OnlyThePoint` | kernel_laws.lth | `OnlyThePoint` | structures/universal.lth | |
| `Initial` | kernel_laws.lth | `Initial` | structures/universal.lth | |
| `NoValue` | kernel_laws.lth | `NoValue` | structures/universal.lth | |
| `BooleanAlgebra` | kernel_laws.lth | `BooleanAlgebra` | structures/algebraic.lth | with `(o : Object B)` |
| `MeetCommutes` | kernel_laws.lth | `MeetCommutative` wrapper of `Commutative` | structures/algebraic.lth, properties/operations.lth | |
| `JoinCommutes` | kernel_laws.lth | `JoinCommutative` wrapper of `Commutative` | structures/algebraic.lth | |
| `MeetIdentity` | kernel_laws.lth | `MeetNeutral` wrapper of `Neutral` | structures/algebraic.lth | |
| `JoinIdentity` | kernel_laws.lth | `JoinNeutral` wrapper of `Neutral` | structures/algebraic.lth | |
| `MeetDistributes` | kernel_laws.lth | `MeetDistributive` wrapper of `Distributive` | structures/algebraic.lth | |
| `JoinDistributes` | kernel_laws.lth | `JoinDistributive` wrapper of `Distributive` | structures/algebraic.lth | |
| `MeetComplement` | kernel_laws.lth | `MeetComplemented` wrapper of `Complemented` | structures/algebraic.lth | |
| `JoinComplement` | kernel_laws.lth | `JoinComplemented` wrapper of `Complemented` | structures/algebraic.lth | |
| `TopIsNotBottom` | kernel_laws.lth | `TopDistinct` wrapper of `Distinct` | structures/algebraic.lth | |
| `TheBooleans` | kernel_laws.lth | removed | | `BoolIsABooleanAlgebra` in core.lut claims the algebra |
| `TopIsTheFirstBranch` | kernel_laws.lth | `TopIsTheFirstBranch` | core.lut | Bool's own law (L2.8) |
| `Monoid` | kernel_laws.lth | `Monoid` | structures/algebraic.lth | with `(o : Object A)`; importer numbers_model.lut |
| `LeftNeutral` | kernel_laws.lth | `LeftNeutral` | properties/operations.lth | |
| `RightNeutral` | kernel_laws.lth | `RightNeutral` | properties/operations.lth | |
| `Associative` | kernel_laws.lth | `Associative` | properties/operations.lth | over an operation, not a monoid |
| `FreeMonoid` | kernel_laws.lth | `FreeMonoid` | structures/universal.lth | `fold` takes the monoid's data |
| `asMonoid` | kernel_laws.lth | removed | | the claim passes `{ neutral, combine }` |
| `IsMonoid` | kernel_laws.lth | `FreeMonoidIsAMonoid` wrapper of `Monoid` | structures/universal.lth | |
| `FoldNeutral` | kernel_laws.lth | `FoldNeutral` | structures/universal.lth | |
| `FoldInject` | kernel_laws.lth | `FoldInject` | structures/universal.lth | |
| `FoldCombine` | kernel_laws.lth | `FoldCombine` | structures/universal.lth | |
| `FoldIsItself` | kernel_laws.lth | `FoldIsItself` | structures/universal.lth | |
| `Lists` | kernel_laws.lth | removed | | `ListIsTheFreeMonoid` (core.lut) claims `FreeMonoid` with `nil`, `cons` |
| `NilIsNeutral` | kernel_laws.lth | `NilIsNeutral` | core.lut | |
| `ConsIsInjectionCombined` | kernel_laws.lth | `ConsIsInjectionCombined` | core.lut | |
| `OrderedSemiring` | kernel_laws.lth | `OrderedSemiring` | structures/order.lth | |
| `PlusAssociative` | kernel_laws.lth | `Semiring`'s `PlusAssociative` wrapper | structures/algebraic.lth | |
| `PlusCommutes` | kernel_laws.lth | `PlusCommutative` wrapper | structures/algebraic.lth | |
| `PlusZero` | kernel_laws.lth | `PlusNeutral` wrapper | structures/algebraic.lth | |
| `TimesAssociative` | kernel_laws.lth | `TimesAssociative` wrapper | structures/algebraic.lth | |
| `TimesCommutes` | kernel_laws.lth | `TimesCommutative` wrapper | structures/algebraic.lth | |
| `TimesOne` | kernel_laws.lth | `TimesNeutral` wrapper | structures/algebraic.lth | |
| `TimesDistributes` | kernel_laws.lth | `TimesDistributive` wrapper | structures/algebraic.lth | |
| `TimesZero` | kernel_laws.lth | `TimesAbsorbing` wrapper | structures/algebraic.lth | |
| `LeqPair` | kernel_laws.lth | `Related S s.leq` | properties/relations.lth | |
| `LeqChain` | kernel_laws.lth | `Chain S s.leq` | properties/relations.lth | |
| `LeqBoth` | kernel_laws.lth | removed | | antisymmetry by contrapositive |
| `LeqTotal` | kernel_laws.lth | `OrderedSemiringTotalOrder` wrapper of `TotalOrder` | structures/order.lth | |
| `LeqAntisymmetric` | kernel_laws.lth | same wrapper (`Antisymmetric`) | structures/order.lth | |
| `LeqTransitive` | kernel_laws.lth | same wrapper (`Transitive`) | structures/order.lth | |
| `PlusMonotone` | kernel_laws.lth | `OrderedSemiringPlusMonotone` wrapper of `MonotoneIn` | structures/order.lth | |
| `ZeroLeast` | kernel_laws.lth | `OrderedSemiringZeroLeast` wrapper of `Least` | structures/order.lth | |
| `OneIsNotZero` | kernel_laws.lth | `OneDistinct` wrapper of `Distinct` | structures/algebraic.lth | |
| `SuccessorIsNext` | kernel_laws.lth | `OrderedSemiringDiscrete` wrapper of `Discrete` | structures/order.lth | |
| `naturals` | kernel_models.lut | `NatIsAnOrderedSemiring` | core.lut | |
| `Exponential`, `Beta` | kernel_laws.lth | same | structures/universal.lth | |
| `Product`, `PairFst`, `PairSnd`, `Pairing` | kernel_laws.lth | same | structures/universal.lth | |
| `Coproduct`, `CaseLeft`, `CaseRight`, `CasesAreAll` | kernel_laws.lth | same | structures/universal.lth | |
| `Selected`, `one`, `two` | kernel_laws.lth | same | structures/universal.lth | |
| `NamedProduct`, `asProduct`, `NamedPairs`, `ProjectionNamesDistinct`, `SelectByName` | kernel_laws.lth | same | structures/universal.lth | |
| `NamedCoproduct`, `asCoproduct`, `NamedCases`, `InjectionNamesDistinct`, `LabelByName` | kernel_laws.lth | same | structures/universal.lth | |
| `application` | kernel_models.lut | `KernelApplies` | core.lut | |
| `pairs` | kernel_models.lut | `PairsAreTheProduct` | core.lut | |
| `recordXY` | kernel_models.lut | `RecordsAreNamedProducts` | core.lut | |
| `sumAB` | kernel_models.lut | `SumsAreNamedCoproducts` | core.lut | |
| `Iso` | algebra.lth | `Isomorphism` | properties/functions.lth | a predicate on (to, from); positions.lut's `layout` becomes two functions and a claim; tests sonolocalizacion_* |
| `FromUndoesTo` | algebra.lth | `Inverse A B oA to from` | properties/functions.lth | |
| `ToUndoesFrom` | algebra.lth | `Inverse B A oB from to` | properties/functions.lth | |
| `AbelianGroup` | algebra.lth | `AbelianGroup` | structures/algebraic.lth | |
| `GroupIsMonoid` | algebra.lth | `GroupAssociative`, `GroupNeutral` wrappers | structures/algebraic.lth | |
| `GroupCommutes` | algebra.lth | `GroupCommutative` wrapper | structures/algebraic.lth | |
| `GroupInverse` | algebra.lth | `GroupInvertible` wrapper of `Invertible` | structures/algebraic.lth | |
| `CommutativeRing` | algebra.lth | `CommutativeRing` | structures/algebraic.lth | a flat record |
| `zeroOf`, `oneOf`, `plusOf`, `timesOf`, `negateOf` | algebra.lth | removed | | the record is flat: `r.zero`, `r.plus` |
| `RingAdds` | algebra.lth | `Ring`'s plus wrappers (`AbelianGroup`) | structures/algebraic.lth | |
| `RingMultiplies` | algebra.lth | `Ring`'s times wrappers (`Monoid`) | structures/algebraic.lth | |
| `TimesCommutes` | algebra.lth | `TimesCommutative` wrapper | structures/algebraic.lth | |
| `Distributes` | algebra.lth | `TimesDistributive` wrapper of `Distributive` | structures/algebraic.lth | |
| `OneIsNotZero` | algebra.lth | `OneDistinct` wrapper of `Distinct` | structures/algebraic.lth | |
| `Field`, `Reciprocal` | algebra.lth | stay | algebra.lth | over `CommutativeRing` of the core |
| `OrderedRing` | algebra.lth | stays | algebra.lth | laws by `TotalOrder`, `MonotoneIn`, `PositiveClosed` |
| `LeqPair`, `LeqChain`, `LeqBoth`, `NonNegativePair` | algebra.lth | `Related`, `Chain`, removed, `NonNegativePair` | properties/relations.lth, structures/order.lth | |
| `LeqTotal`, `LeqAntisymmetric`, `LeqTransitive` | algebra.lth | `OrderedRingTotalOrder` wrapper of `TotalOrder` | algebra.lth | |
| `PlusMonotone` | algebra.lth | `OrderedRingPlusMonotone` wrapper of `MonotoneIn` | algebra.lth | |
| `TimesPositive` | algebra.lth | `OrderedRingPositiveClosed` wrapper of `PositiveClosed` | algebra.lth | |
| `OrderedField`, `FieldIsOrdered` | algebra.lth | stay | algebra.lth | `FieldIsOrdered` passes the ordered ring built in the law, as today |
| `CompleteOrderedField`, `SupIsUpperBound`, `SupIsLeast` | algebra.lth | stay | algebra.lth | |
| `integers` | numbers_model.lut | `IntIsACommutativeRing`, `IntIsTotallyOrdered` | core.lut | numbers_model.lut keeps `integers : OrderedRing Int` as a value for the field's laws only if a law needs it; else removed |
| `strings` | numbers_model.lut | `StringIsAMonoid` | core.lut | |
| `PlusCommutes` | numbers.lth | `PlusCommutative` wrapper of `Commutative` | numbers.lth | test lines in numbers_laws, numbers_controls, test_certify.py:388-396, test_run.py:657 |
| `TimesCommutes` | numbers.lth | `TimesCommutative` wrapper | numbers.lth | |
| `PlusZero` | numbers.lth | `PlusNeutral` wrapper of `Neutral` | numbers.lth | |
| `TimesOne` | numbers.lth | `TimesNeutral` wrapper | numbers.lth | |
| `TimesZero` | numbers.lth | `TimesAbsorbing` wrapper of `Absorbing` | numbers.lth | one side: doubles have `x * 0.0 == 0.0`; the wrapper states the side it claims |
| `NegateTwice` | numbers.lth | `NegateInvolutive` wrapper of `Involutive` | numbers.lth | |
| `LeqPair`, `LeqChain` | numbers.lth | `Related`, `Chain` | properties/relations.lth | |
| `LeqReflexive`, `LeqTotal`, `LeqAntisymmetric`, `LeqTransitive` | numbers.lth | `LeqTotalOrder` wrapper of `TotalOrder` | numbers.lth | |
| `PlusMonotone`, `TimesMonotone` | numbers.lth | wrappers of `MonotoneIn` | numbers.lth | |
| `SqrtMonotone` | numbers.lth | `SqrtMonotone` wrapper of `Monotone` | numbers.lth | `doublesOrder` stays as the relation passed |
| `SqrtSquares`, `ExpOfLog`, `LogOfExp`, `ExpAdds`, `LogMultiplies` | numbers.lth | stay, over `Ball` | numbers.lth | `within` keeps its name as the ball's abbreviation |
| `Tolerance` | numbers.lth | `Tolerance` | structures/equality.lth | importers: arrays, probability, belief, optimization, generators, distances.lut, test programs |
| `abs` | numbers.lth | `abs` | structures/equality.lth | |
| `within`, `withinOf` | numbers.lth | stay, defined by `Ball` | numbers.lth | |
| `Metric`, `WithinBounds`, `Grows`, `StartsAtLo`, `LinearMetric`, `LogMetric` and their laws | generators.lth | `Placement`, `LinearPlacement`, `LogPlacement` | generators.lth | frees the name (decisions.md, question 2); importers test.lth (`SampledMode`), generators_model.lut, program.lth's comment |
| `Sized`, `SizeBounded` | generators.lth | `SizedGenerator`, `SizeBounded` | generators.lth | frees `Sized` for containers.lth |
| `Enumeration` | generators.lth | stays | generators.lth | |
| `isReflexive` … `isHomomorphism` (12 templates) | laws.lth | removed | | properties/ states each; all 12 unclaimed today |
| `CombineCommutes`, `CombineAssociates` | laws.lth | `CombineCommutative`, `CombineAssociative` wrappers | laws.lth | `Settling`'s |
| `CombineCommutes` | certification.lth | `CombineCommutative` wrapper | certification.lth | `Regioning`'s; test lines regions_laws:98, regions_controls:130, test_certify.py:1084 |
| `OwnIsIdempotent` | world.lth | wrapper of `Idempotent` (functions) | world.lth | |
| `CanonIdempotent`, `UnqualifyIdempotent` | term.lth | wrappers of `Idempotent` (functions) | term.lth | |
| `AddPointwise` … `MscalePointwise` (7) | arrays.lth | wrappers of `Pointwise`/`Pointwise2` with `pointwise` equality | arrays.lth | `approxVec exact` becomes the container's `Object` |
| `DotSymmetric` | arrays.lth | `DotCommutative` wrapper of `Commutative` | arrays.lth | |
| `DotAgrees`, `MatVecAgrees`, `MatMulAgrees`, `TraceAgrees` | arrays.lth | stay, over `Ball`/`entrywiseBall` with the radius from `absSumTo` | arrays.lth | an equality of two functions within a bound (`PointwiseWithin`) |
| `MatMulIdentity` | arrays.lth | `MatMulNeutral` wrapper of `Neutral` on square matrices | arrays.lth | the rectangular case stays a law of its own |
| `PinvSymmetric`, `PrecisionSymmetric`, `PosteriorInfoSymmetric`, `InfoSymmetric`, `StepMatrixSymmetric` | arrays, belief, probability, optimization | wrappers of `Ball` against the transpose | same files | a matrix in the ball of its transpose |
| `approxVec`, `approxMat`, `approxMatSlack`, `approxMatOf`, `approxMatSlackOf` | arrays.lth | `Ball`/`entrywiseBall` of `supDistance absDistance` with the radius named | structures/equality.lth, containers.lth | arrays.lth keeps `approxVec tol`, `approxMat tol` as abbreviations with those bodies; the `Of`/`Slack` forms become radius functions at the call |
| `Symmetric` | arrays.lth | `Symmetric` the equalizer of `id` and `transpose` | arrays.lth, arrays_model.lut | the subtype stays; `SymmetricIsAnEqualizer` claims `Equalizer` |
| `KolmogorovOfMultiset` | probability.lth | wrapper of `Congruent` (reverse) | probability.lth | |
| `KolmogorovAgrees` | probability.lth | wrapper of `Pointwise` | probability.lth | exact |
| `forallBelow`, `existsBelow`, `forallPairs`, `forallPairs2`, `countBelow`, `foldWith`, `foldFrom` | arrays.lth | same names | structures/containers.lth | importers: tables, probability, generators_model, distances, positions, distance_graph |
| `larger` | probability.lth | `larger` | structures/equality.lth | |
| `NonNegativeFloat` | grammar.lth | `NonNegativeFloat` | structures/equality.lth | grammar.lth imports it (bite 7) |

### 5.2 Helpers the list library replaces

Generated by `grep -nE "^(all|any|append|member|lookup|concat|lengthOf)[A-Za-z0-9_]* " src/luthier/lib/*.lth
src/luthier/lib/*.lut examples/sonolocalizacion/*.lut` (104 lines) plus the names found by hand
(`listLength`, `distinct`, `noDuplicates`, `memberOf`, `allOf`, `upTo`, `nth`, `remove`,
`removeAll`, `isEmpty`, `isEmptyList`, `isOneElement`, `insertSorted`, `sortedValues`,
`reverseOnto`, `mapList`, `appendList`, `foldInto`). Each old name becomes a call of the new name
with the local predicate or key, unless the note says it keeps its name.

| old name | old file | new name | new file | note |
|---|---|---|---|---|
| `appendList`, `foldInto` | core.lut | `append`, `fold` | lists.lut | core.lut imports them for `ListIsTheFreeMonoid` |
| `lengthOf` | generators.lth, certification.lth, probability.lth, world.lth | `length` | lists.lut | world_controls.test.lut:18,159-163 names world.lth's |
| `listLength` | tables.lth | `length` | lists.lut | |
| `mapList` | world.lth | `map` | lists.lut | world_controls.test.lut names it |
| `memberOf` | generators.lth | `member` | lists.lut | |
| `allOf` | generators.lth | `all` | lists.lut | unclaimed today |
| `noDuplicates` | generators.lth, plan.lth | `distinct` | lists.lut | |
| `distinct` | tables.lth | `distinct` | lists.lut | |
| `upTo` | generators.lth | `filter` with `size x <= n` | lists.lut | |
| `nth` | generators.lth | `nth` | lists.lut | |
| `isEmptyList`, `isOneElement` | generators.lth | `isEmpty`, `length xs == 1` | lists.lut | |
| `isEmpty` | ebnf.lth, checks.lth | `isEmpty` | lists.lut | checks.lth's is over `Failures E = List E` |
| `member`, `concat`, `remove`, `removeAll` | term.lth, program.lth | `member`, `append`, `remove`, `removeAll` | lists.lut | `concat (xs ys)` is `append`; the `String` equality `structural String` |
| `memberStr` | plan.lth, tables.lth, world.lth | `member String (structural String)` | lists.lut | |
| `memberString` | ebnf.lth | `member` | lists.lut | |
| `memberChars` | grammar.lth | `all (fn c { member ... c ws }) cs` | lists.lut | |
| `memberRegion` | certification.lth | `member` | lists.lut | |
| `append` | ebnf.lth | `append` | lists.lut | |
| `appendRegions`, `appendRefusals`, `appendEntries` | certification.lth | `append` | lists.lut | |
| `appendOne` | plan.lth | `append xs (singleton n)` | lists.lut | |
| `appendStrs` | plot.lth | `append` | lists.lut | |
| `appendLayer`, `appendTable` | plot.lth | `append ls (singleton l)` | lists.lut | |
| `appendText`, `appendEnv`, `appendBindings` | term_model.lut | `append` | lists.lut | |
| `appendApps`, `appendTerms` | program.lth | `append` | lists.lut | |
| `appendNames` | examples/sonolocalizacion/figures.lut | `append` | lists.lut | |
| `appendStr` | world.lth | keeps its name | world.lth | concatenation of two strings, `+`; not a list |
| `append` | examples/sonolocalizacion/distances.lut | `pushEntry` | distances.lut | appends an entry to a `Vec`; renamed so `append` names the list's |
| `concatFailures` | checks.lth | `append` | lists.lut | |
| `concatNames` | library.lth | `append` | lists.lut | |
| `concatTerms` | program.lth | `append` | lists.lut | |
| `concatFields`, `concatStrs` | world.lth | `append` | lists.lut | |
| `lookupValue` | demand.lth | `lookup` | lists.lut | over `List (String * Value)` |
| `lookupStr`, `lookupTable`, `lookupScale` | plot.lth | `lookup` | lists.lut | `Mapping = List (String * String)` |
| `lookupFile` | world_model.lut | `lookup` | lists.lut | |
| `lookup` | program.lth | `lookup` | lists.lut | `Context = List (String * Term)` |
| `lookupBody` | term_model.lut | keeps its name | term_model.lut | reads a `Program`'s acts, not an association list; its body may call `lookup` over the pairs it builds |
| `lookupField` | term_model.lut | `lookup` | lists.lut | over `List (String * Term)` |
| `allNonNegative` | generators.lth | `all (fn (x, w) { 0.0 <= w })` | lists.lut | |
| `allNullable`, `anyNullable`, `anyReaches`, `allDefined`, `anyRhs` | ebnf.lth | `all`/`any` with the local predicate | lists.lut | `anySplit` keeps its name: a search over positions, not a fold over a list |
| `allIn` | certification.lth, library.lth | `all (fn x { member ... x ys }) xs` | lists.lut | |
| `anyServes`, `anyIs` | certification.lth | `any` | lists.lut | |
| `anyExtern`, `anyMentions` | library.lth | `any` | lists.lut | |
| `allNames`, `allPatterns`, `allWf`, `allFields`, `allPairs`, `allItems`, `allParams`, `allArms`, `allBinders`, `allClauses`, `allImportNames`, `allLiteralsLex`, `allKindsKnown` | grammar.lth | `all` with the local predicate | lists.lut | |
| `allNames` | plan.lth | `all` | lists.lut | |
| `allNames` | term_model.lut | keeps its name | term_model.lut | collects the names of a term; not a predicate |
| `allKnown` | tables.lth | `all knownKind` | lists.lut | |
| `allConfirmed`, `anyRefuted`, `anyConfirmed`, `allRefutedOf`, `allConfirmedOrSupported` | laws.lth | `all`/`any` | lists.lut | |
| `anyValue`, `anyFailure` | certification_model.lut | `any` | lists.lut | |
| `allUnqualified`, `allFree` | term.lth | `all` | lists.lut | |
| `allLayers`, `anyLayer`, `allStr`, `allScales` | plot.lth | `all`/`any` | lists.lut | |
| `allUnit` | probability.lth | `all unitVec` | lists.lut | |
| `anyUnknown`, `anyAct`, `anyUnclaimed`, `anyNotIn`, `anyUndefined`, `anyTerm`, `anyTerms`, `anyClause`, `anyIn`, `anyFault`, `anyApp`, `anyArgumentArrow`, `anyTermArrow`, `anyArrow`, `anyDatum` | program.lth | `any` with the local predicate | lists.lut | `anyTerm (f) (t : Surface)` is over one term's children: keeps its name |
| `insertSorted`, `sortedValues` | probability.lth | `insertSorted`, `sortBy` with `<=` | lists.lut | |
| `reverseOnto` | probability.lth | `reverse` | lists.lut | |
| `pooled`, `entriesOnto` | probability.lth | `concat (map entries vs)` | lists.lut | `entries : Vec Float64 -> List Float64` stays in arrays.lth |
| `isNilStr`, `isJustStr`, `isJustTable` | plot.lth | `isEmpty`, keep | lists.lut, plot.lth | the `Maybe` tests are not list helpers |

## 6. The bites

Each bite is accepted when: `luthier check` is clean on every file it touched and `check -v`
reports no unclaimed law in `lib/core/` (elsewhere, no more than before); `python -m pytest tests -q`
is green with at least as many tests as before the bite; `luthier certify` on the test programs it
touched grades every law (none `not run`) and reports every law controlled (certify.py
`control_status`: no `uncontrolled`); the commit message counts the store entries rewritten
(`git diff --stat` on the `.cert.json` files and the number of entries at the new cone hashes);
the plan's Status line is updated. Commits of two lines, staged by path. Nothing is pushed and no
tag is cut (D-2026-10-17-e).

### Bite 1. The code fixes and the directory (Opus)

Files: `src/luthier/certify.py` (3e: the cone's hash erases the binder annotations the elaborator
writes, D-2026-10-15-e, with the law that erasure leaves the term's behavior unchanged and its
control), `src/luthier/tester.py` (`_list_members` fingerprints a census's members built by an
expression, 3h's finding), `src/luthier/run.py:143` (`CORE`), `tests/test_certify.py`,
`tests/test_tester.py`, `tests/test_run.py`; the move `lib/core.lut` to `lib/core/core.lut`,
`lib/kernel_laws.lth` split without renaming any law into `lib/core/structures/equality.lth` (§1),
`algebraic.lth` (§3, §4's Monoid, §5), `universal.lth` (§2, §4's FreeMonoid, §6), `kernel_models.lut`
absorbed into core.lut (section 3.10's names), every `import "kernel_laws.lth"` and
`import "kernel_models.lut"` repointed (generators.lth, world.lth, numbers_model.lut,
generators_model.lut, algebra.lth, core.lut, 3 test programs, tests/test_run.py:1164); the stores
moved with their files; one full re-certification, `luthier certify tests/tester/*.test.lut`
(the examples' test programs are there too, `sonolocalizacion_*`).
Waits for: the agent now in tester.py and certify.py to land.
Accepted when, besides the common criteria: the erasure law exists with a refuted control; a
census built by an expression changes its fingerprint when its members change (a test); every
store entry is at a new cone hash (the count equals the number of entries, 927 at ca90ee8, less
the entries whose cones hold no binder); `luthier run examples/sonolocalizacion/experiment_zero.run.lut`
reproduces its recorded result.
May break: every store (expected, once); `run`'s core path in any script that names it; the
`examples/hello.run.json` the suite writes.

### Bite 2. The properties (Fable; in parallel with bite 1)

Files: new `lib/core/properties/relations.lth`, `operations.lth`, `functions.lth` (section 3.1 to
3.3); new `tests/tester/core_laws.test.lut` and `core_controls.test.lut` with each property tested
at a listed instance (`Int` with `+`, `*`, `<=`; `Bool` with `and`, `or`; `String` with `+`) and
refuted at a wrong one (`-` for Commutative and Associative; `<` for Reflexive; `fn x { x + 1 }`
for Idempotent and Involutive; `fn x y { x }` for Cancellative; a `bound` of zero for
`AssociativeWithin` on doubles).
Accepted when: every property has a confirmed instance and a refuted control. The instances are
the test program's own definitions, so their entries land beside it (as `cases.test.cert.json` does
today), untracked under tests/ (D-2026-10-16-h); bite 3 moves the claims into core.lut, where they
get their tracked store. The test program's header says so.
May break: nothing in the library (new files only).

### Bite 3. The structures and core's claims (Fable; after 1 and 2)

Files: `lib/core/structures/{equality, order, algebraic, containers, universal}.lth` rewritten over
properties/ (sections 3.4 to 3.9: Object by Equivalence, Metric and its variants with `Ball`,
`Tolerance`, `MetricWithin`; the structures as records with one-line wrappers; containers.lth with
the folds over `Fin n` moved from arrays.lth; the equalizer, pullback, coequalizer); `lib/core/core.lut`
(section 3.10's claims, `Int`, `String`, `Fin`, the metrics); `numbers_model.lut` (`integers`,
`strings` gone or reduced); `algebra.lth` (§0 to §2 removed, §3 to §5 over the core); every importer
of the moved folds (`arrays.lth`, `tables.lth`, `probability.lth`, `generators_model.lut`,
`distances.lut`, `positions.lut`, `distance_graph.lut`: import lines only); `core_laws.test.lut`,
`core_controls.test.lut` (the metric controls of section 3.5; the claims of core.lut tested).
Accepted when: `check -v` lists no unclaimed law in `lib/core/`; every structure has a claimant
in core.lut or lists.lut or a library; every claim of core.lut graded and controlled;
`Metric`'s four controls refuted; `numbers_laws` and `numbers_controls` still certify (they import
numbers.lth, untouched here).
May break: the test programs that import `kernel_laws.lth Concrete` (repointed in bite 1);
`algebra.lth`'s store entries (re-certified); `positions.lut`'s `Iso` import (kept until bite 8b:
`Iso` stays in algebra.lth as a deprecated alias until then, with a note).

### Bite 4. The list library (Sonnet; after 3)

Files: new `lib/core/lists.lut` (section 3.11) with its claims; `lib/core/core.lut` imports
`append` and `fold` and drops `appendList`, `foldInto`; new `tests/tester/lists_laws.test.lut`,
`lists_controls.test.lut`.
Accepted when: every function of 3.11 is defined; every claim graded and controlled;
`ListIsTheFreeMonoid` still holds through the imported `append` and `fold`.
May break: nothing outside core.lut.

### Bite 5. numbers.lth and algebra.lth (Opus; after 3, parallel with 4)

Files: `numbers.lth` (section 4), `numbers_model.lut`, `algebra.lth` (its remaining structures
over the core), `tests/tester/numbers_laws.test.lut`, `numbers_controls.test.lut`,
`tests/test_certify.py:388-433` (names `PlusCommutes`), `tests/test_run.py:654-688`,
`tests/test_tester.py:28-31` (the message text names `PlusCommutes`; tests/tester/laws.test.lut's
own `PlusCommutes` is a local definition and may keep its name).
Accepted when: `Doubles`' four within-bound laws are graded with the bounds of section 4 and each
has a control (an `op` that rounds to a coarser grid, refuted; a bound too small, refuted on the
real doubles, which is also what tells `gamma2` from `3 gamma2`); the `MetricWithin` of
`absDistance` graded and controlled; no `PlusCommutes` remains in lib/ or tests/ except
laws.test.lut's local one.
May break: every importer of `Tolerance`, `within`, `abs` (import lines; `within` and `withinOf`
keep their names and types).

### Bite 6. The machinery's renames and helpers (Sonnet; after 4, parallel with 5 and 7)

Files: `laws.lth` (§2 removed; `Settling`'s wrappers), `certification.lth` (`CombineCommutative`,
helpers), `generators.lth` (`Placement`, `SizedGenerator`, helpers), `generators_model.lut`,
`test.lth` (`SampledMode : Placement -> Mode`), `world.lth`, `world_model.lut`, `plan.lth`,
`plan_model.lut`, `demand.lth`, `checks.lth`, `certification_model.lut`; their test programs
(`regions_*`, `certification_*`, `generators_*`, `world_*`, `plan_*`, `demand_*`, `pooling_*`,
`cutoff_controls`, `cases`, `weakest`, `laws`); `tests/test_certify.py:1084` (`CombineCommutes`);
the spec's 7.S2, 7.S4 and 7.R1 wording of "metric" belongs to the spec's agent (a note to the
coordinator, not this bite's edit).
Accepted when: no name of section 5.2's rows for these files remains (`grep` of each old name is
empty); every renamed law graded and controlled.
May break: every test program that names `SampledMode linear` (no: `linear`'s name is kept; only
its type's name changes); program.lth's comment on `Metric` (line 328).

### Bite 7. Luthier's self-description (Sonnet; after 4, parallel with 5 and 6)

Files: `term.lth`, `term_model.lut`, `program.lth`, `grammar.lth`, `ebnf.lth`, `ebnf_model.lut`,
`library.lth`, `translation.lth` (section 5.2's rows for these files; `CanonIdempotent`,
`UnqualifyIdempotent` as wrappers); no test program of these exists today (the finding "11
theories without tests or stores"): this bite adds none, and notes it in the plan.
Accepted when: `check` clean, the suite green (test_check, test_elaborate, test_parse read these
files), no old name remains.
May break: `check`'s own reading of program.lth (check.py is a specimen of program.lth; a renamed
helper there is a renamed docstring reference at most).

### Bite 8a. Arrays and tables (Opus; after 5, parallel with 6 and 7)

Files: `arrays.lth` (the containers' claims for `Vec` and `Mat`; `Pointwise` wrappers; `Ball` and
`entrywiseBall` in place of the `approx...` family, the two abbreviations kept; `Symmetric` as an
equalizer; `lengthOf` gone), `arrays_model.lut` (`SymmetricIsAnEqualizer`, the shared-`k`
pullback), `tables.lth` (Table claims `Indexed` over its rows; helpers), `tables_model.lut`,
`generators_model.lut`'s arrays imports; `tests/tester/arrays_*`, `tables_*`.
Accepted when: every law of `Arrays` graded and controlled at the new names; `distance_graph.lut`
and `validate_graph.run.lut` run unchanged (they import `forallBelow` from its new file after bite
3).
May break: `probability.lth`, `belief.lth`, `optimization.lth`, the examples (they import
`approxVec`, `approxMat`, `exact`: kept as abbreviations, so only import lines move).

### Bite 8b. Probability, belief, optimization, plot, the examples (Opus; after 8a)

Files: `probability.lth` (Kolmogorov's wrappers; `pooled`, `sortedValues` by lists.lut; the
pushforward of a measure as a structure with its law, D-2026-10-17-g, for the generators and the
probability integral transform), `probability_model.lut`, `belief.lth`, `belief_model.lut`,
`optimization.lth`, `optimization_model.lut`, `plot.lth` (helpers only: its [proposed] readings
wait for G1 to G5, D-2026-10-17-h), `plot_model.lut`; `examples/sonolocalizacion/positions.lut`
(`layout` as `flatten`, `unflatten` and `LayoutIsAnIsomorphism`), `distances.lut` (`pushEntry`),
`figures.lut`, `distance_graph.lut` (the join as a `Pullback` claim); `algebra.lth` (the `Iso` alias
removed); their test programs (`probability_*`, `belief_*`, `optimization_*`, `plot_*`, `fit_*`,
`sonolocalizacion_*`).
Accepted when: the stores of the examples re-certified; `experiment_zero.run.lut` and
`validate_graph.run.lut` reproduce their recorded results; no old name of section 5 remains anywhere
(the check command of section 5 run with the new names: it prints every old name as MISSING).
May break: the fit's records (`examples/sonolocalizacion/*.run.json`): a changed cone is a changed
key, so the runs are redone and compared with the recorded values.

### Bite 9. Closing (Sonnet; after 8b)

Files: this plan (Status), `record/plan/code-follows-principles-2026-10-16.md` (the core line
marked done), `record/handoff-*.md`; `docs/spec/12-files-and-tools.md`'s 12.S22 note that
`core.lut` lives in `lib/core/` belongs to the spec's agent (a note). The survey rerun: names
defined in more than one file (expected: the pairs that are not duplicates of meaning, such as
`Field` of algebra and of grammar, listed as accepted homonyms), `check -v`'s unclaimed count
(expected 0 in core, the rest listed for the next plan), the loose notice count.
Accepted when: the plan says nothing false; the two surveys are in the record with the commands.

## 7. Schedule

```
wave 1:  bite 1 (Opus, code and the move)      | bite 2 (Fable, properties)
wave 2:  bite 3 (Fable, structures and core.lut)
wave 3:  bite 4 (Sonnet, lists.lut)            | bite 5 (Opus, numbers and algebra)
wave 4:  bite 6 (Sonnet, machinery)            | bite 7 (Sonnet, self-description)  | bite 8a (Opus, arrays and tables)
wave 5:  bite 8b (Opus, probability to the examples)
wave 6:  bite 9 (Sonnet, closing)
```

Disjoint files per wave: wave 1 shares nothing (bite 2 creates files; bite 1 moves others); wave 3
shares `core.lut` only through bite 4's two import lines, which bite 4 adds last; wave 4's three
bites touch disjoint libraries and disjoint test programs (bite 8a's `generators_model.lut` edit is
import lines; bite 6 owns the file's content, so 8a sends its two lines to bite 6's agent instead).
Never more than three agents at once (the rule of 2026-10-14).

## 8. Decisions taken by the agent in this design (one commit undoes each)

- Structures keep a record of their data with one-line wrappers; properties are bare predicates
  (section 2).
- `Commutative` takes a domain and a codomain; `Associative` and the rest are at the carrier.
- `Antisymmetric`, `Cancellative`, `Injective`, `MetricIndiscernible` by their contrapositive over
  every pair (7.S12's rule, numbers.lth's precedent).
- `Surjective` by a witnessed section; `functions (A B) (o) : Object (A -> B)` declared, not defined.
- Metric's M1 as two laws; `MetricNonNegative` stated as a derived law for the control's sake;
  `MetricWithin` as the floating-point claim with its three within-bound consequences.
- `Pushout` waits for a case; the pushforward of measures goes to probability.lth (bite 8b).
- The matrix is indexed row-major by `Fin (m * n)` for `Indexed`; its two-index `f` stays.
- generators.lth's `Metric` becomes `Placement` and its `Sized` `SizedGenerator`, pending question
  2 of decisions.md for the first (the second is a plain clash).
- `within`, `withinOf`, `approxVec tol`, `approxMat tol` keep their names as abbreviations defined by
  `Ball`.
- The folds over `Fin n` move to containers.lth; `sumTo` stays in arrays.lth.
- kernel_models.lut is absorbed into core.lut; `integers` and `strings` of numbers_model.lut become
  claims of core.lut.
- The constant of `PlusAssociativeWithin`'s bound is 3 gamma2, rounded up from the derivation,
  with the test to tell (decisions.md, note 3).
- Bite 1 moves without renaming; the renames come by group so that each bite re-certifies only
  its files.
