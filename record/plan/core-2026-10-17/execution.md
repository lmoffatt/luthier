# The new core: execution plan

Written 2026-10-17 by Claude Fable 5.1, an agent of the coordinating session, on the brief
`record/plan/core-2026-10-17/prompt-design.md`; revised 2026-10-18 by the same agent for
D-2026-10-18-a (the core alone, to its measurable end) and D-2026-10-18-b (the whole core a prelude,
names per concept resolved by the type's model, no collisions), on the coordinator's brief of that
day. Inputs: the library at d280a18 (bites 1 and 2 landed, their reports beside this file),
`record/decisions.md` D-2026-10-14-b, D-2026-10-16-l, D-2026-10-17-a to -i, D-2026-10-18-a, -b,
`record/principles-language.md` L1 to L3, L7 (L7.6, the style clause), L9.14, L10.12, spec 4.R13,
4.S14, 5.S6, 12.S4, 12.S22, 12.S23, 12.R2, `src/luthier/elaborate.py` (`infer`, the operator table),
`src/luthier/run.py` (`Loaded`), `src/luthier/check.py` (`coreNames`, `resolve`). The questions this
design leaves to Luciano are in `decisions.md` beside this file; every choice marked [proposed] is
the agent's, one commit undoes it. The first version of this plan (54f6228) had the core imported by
name; D-2026-10-18-b decided otherwise and this version replaces it (git keeps the first).

Status: bites 1 and 2 landed (report-bite-1.md, report-bite-2.md): lib/core/ exists with core.lut,
properties/{relations, operations, functions}.lth and structures/{equality, algebraic, universal}.lth
(kernel_laws.lth split without renames, kernel_models.lut absorbed), the hash erases binder
annotations, the library re-certified once (536 entries in 29 stores), suite 820 passed. Not
started: bites 4 to 13 below. Bite 3 landed (scripts/core_metrics.py): at the tree after ded76d4,
over lib, examples and tests/tester, homonyms among importable files 96, executive-file names
shadowing an importable name 112 (D-2026-10-16-e, D-2026-10-18-b), list helpers 427 (every file),
unclaimed 137, loose 1974 (real 1341, the rest 633; unclaimed and loose over importable files);
over lib alone 81, 0, 397, 70, 1737 (1116, 621). The library at d280a18: `check -v` reports 70 unclaimed Bool laws (32
of them bite 2's properties, claimed only by tests/tester/core_instances.lut until the structures
claim them), the `loose` notice on every top-level function, 48 names defined in more than one file
(the count of 2026-10-17's survey before bite 1; core_metrics.py counts 81 over lib at ded76d4).
Bite 4b landed 2026-10-18 (report-bite-4b.md): the tester splits a law whose body is a `&` of
partially applied laws into its conjuncts, each with its entry, the grade their combination (spec
7.S22), so bite 6 can write the structures and composites bare; the classifier's two bounds are
fields of `Budgets` (`regionNumbers`, `regionEntries`). core_metrics unchanged (96, 112, 427, 137,
1974).
Bite 4 landed 2026-10-18 (report-bite-4.md): `infer` total on the library (3285 definitions, no
`Hole('type')`), the core the elaborator's prelude, operators and the fields of a structure resolved
by type with claims as bindings, omitted structure parameters filled, the bare fallback gone; check
types each act in its file's context and refuses what the typing refuses (4.R9, 4.R13); no cone
moved; suite 847 passed; core_metrics unchanged (96, 112, 427, 137, 1974).

## 0. The core's end (D-2026-10-18-a)

His criteria, measured over the whole library by `scripts/core_metrics.py` (bite 3), printed by
every bite's commit message:

1. names defined at the top level of more than one file: 0 (accepted homonyms listed in the script
   with their reason, such as algebra.lth's `Field` and grammar.lth's `Field`, until a rename);
2. list helpers reinvented per type (the `all...`, `any...`, `append...`, `member...`, `lookup...`,
   `concat...`, `lengthOf`, `listLength`, `mapList` families and the hand-written recursions over
   `List` that a core function covers): 0;
3. Bool laws `check -v` reports unclaimed: 0;
4. `loose` notices: only where real (a top-level function at a bare exponential that no theory
   names; today the notice fires on every top-level function, 1675 times), the real ones listed;
5. the suite green, the stores re-certified, `experiment_zero.run.lut` and `validate_graph.run.lut`
   reproducing their records.

One thing at a time: the core alone, from bite 3 to bite 13; the queued bites of
record/plan/code-follows-principles-2026-10-16.md wait unless the core needs one (the budgets bite,
already landed, was one).

## 1. The core as a prelude

```
src/luthier/lib/core/
  core.lut                      what the interpreter provides (11.R2) and the claims of the kernel's
                                own types and forms (Unit, Empty, Bool, Maybe, List, Nat, Fin, Int,
                                String; application, pairing, records, sums)
  lists.lut                     List's models of the container structures and the functions of
                                lists no structure covers
  properties/
    relations.lth               Reflexive … Total; Equivalence, Preorder, PartialOrder, TotalOrder,
                                StrictOrder; Related, Chain, Both             (bite 2, as built)
    operations.lth              Associative … Distinct; the within-bound versions   (bite 2)
    functions.lth               id, compose, flip, const; Pointwise; Injective … Isomorphism  (bite 2)
  structures/
    equality.lth                Object (eq), Concrete, structural, Structural; Metric (d) and its
                                variants, Ball, Tolerance, MetricWithin
    order.lth                   Order (leq); Least, Greatest, Discrete, MonotoneIn; OrderedSemiring
    algebraic.lth               Semigroup, Monoid (neutral, combine), Group (inverse), Semiring and
                                Ring (zero, one, plus, times, negate), Lattice (meet, join),
                                BooleanAlgebra (top, bottom, complement)
    containers.lth              Functor (map), Indexed (size, at), Foldable (fold), Tabulated
                                (build); the generic functions over them: all, any, member, count,
                                lookup, sum, toList, filter, zipWith, sameEntries, supDistance
    universal.lth               Terminal (point), Initial (absurd), Exponential (apply), Product
                                (pair, first, second), Coproduct (left, right, cases), NamedProduct,
                                NamedCoproduct, Equalizer (include, restrict), Pullback,
                                Coequalizer (project, lift), FreeMonoid (inject)
```

The whole directory is the prelude (D-2026-10-18-b): every file under `lib/core/` is loaded before
any other file, and its names are visible in every file without an import, as core.lut's are today
(12.S22). What changes in the loader and the spec (bite 5):

- `run.py`'s `Loaded` visits every `.lth` and `.lut` under `lib/core/` (today `CORE`, one file),
  each after its imports, and resolves a name a file does not define or import in the core as a
  whole (`Loaded.__init__`'s `owner in (self.top, self.core)` becomes the set of core files);
  `core_data` roots a run's slice in core.lut's data as today. The imports among core files stay
  written (they say what each file reads; a cycle of files is allowed when no name reaches itself,
  as core.lut notes; bite 2's report asks for the test, which bite 5 adds).
- `check.py`'s `coreNames` (a frozenset of 30 names) becomes the names defined at the top level of
  the core's files, read from them; `resolve` is unchanged.
- 12.S22's sentence "`core.lut` encloses the top-level scope of every file" becomes "the core,
  `lib/core/`, encloses it"; 12.S4's "`core.lut` is imported implicitly" likewise; `--no-core` keeps
  its meaning for the whole prelude. The spec's agent writes the two sentences from this plan.
- A file outside the core that defines a name the core defines is refused by `check` and by the
  loader, naming the core file (D-2026-10-18-b: no general collision). A file that imports a core
  name by its path gets a `redundant` notice from `check -v` and the import is dropped in migration
  [proposed: a notice and not a refusal, so bites land one file at a time].
- A core file may not define a name another core file defines (the same rule, inside the core);
  the structures' field names may repeat across structures (`first` of Product and of Pullback)
  since a use is resolved by the type, and a type that models both says which by qualification.

Stores: `lib/core/core.cert.json` and `lib/core/lists.cert.json` beside the files that claim
(L10.12); the .lth files keep none. Test programs: `tests/tester/core_laws.test.lut`,
`core_controls.test.lut` (bite 2's, extended), `lists_laws.test.lut`, `lists_controls.test.lut`.
What is not core (arrays, tables, probability, the machinery) is imported by name as today, until
analysed (D-2026-10-18-b).

## 2. Concepts, names and how a name resolves

A concept is a structure: a record of its data with its laws, stated once (section 3). Its names are
per concept, not per type (D-2026-10-18-b): one `map` of `Functor`, one `size` and `at` of
`Indexed`, one `d` of `Metric`, one `plus` of `Semiring`, one `eq` of `Object`. A type claims the
structure in the file that defines the type (L2.8), as core.lut claims `UnitIsTerminal : Bool :=
Terminal Unit { point := unit }` today; that claim is the model the type names.

### 2.1 What a use looks like

```
-- in arrays.lth, after `VecIsIndexed : Bool := Indexed (Vec A) A { size := fn v { v.n }, at := fn v k { v.f k } }`
dotDef (x : Vec Float64) (y : VecOf (size x)) : Float64 := sum Float64 (zipWith times x y)
-- in numbers.lth
PlusCommutative (d : Doubles) (x y : Moderate) : Bool := Commutative Float64 Float64 d.plus x y
-- in any file: the list's and the vector's map are one name
names := map (fn n { n.name }) nodes
```

`size x` resolves to `Vec`'s `Indexed` model because `x : Vec Float64`; `times` to `Float64`'s
`Semiring` (the doubles claim `Semiring` within bounds, so `times` is the field of that claim's
record; see section 4); `Commutative`'s equality parameter `(o : Object Float64)` is filled by
`Float64`'s `Object` (`structural Float64`) without being written; `map` by `List`'s `Functor` at
`nodes : List Node`.

### 2.2 The rule

4.R13 says an operator is resolved by the type of its operands and a type names its model; the
elaborator keeps a table `(operator, domain type) -> function`, filled by `operator` acts, and looks
it up with the inferred type of the left operand (`elaborate.py`, `walk` of `Binop`, `infer`).
D-2026-10-18-b extends the rule from operators to every name of a structure. Stated for the
elaborator:

1. A structure's field name used as a function (`map`, `size`, `d`, `plus`, `eq`) is resolved by the
   type of its discriminating argument: the argument whose type is the structure's carrier (the
   first argument of that type in the field's signature; for `map : (A -> B) -> F A -> F B` the
   second, for `size : C -> Nat` the first, for `d : A -> A -> Float64` the first). The model is the
   claim of that type (`VecIsIndexed`), found by the structure's head and the type's head.
2. A parameter whose type is a structure applied to a type (`(o : Object A)`, `(m : Functor F)`,
   `(f : Foldable F)`) is implicit: the call may omit it and it is filled by the model the type
   names once `A` or `F` is known from the other arguments; it may be passed by name,
   `Commutative Int plus x y (o <- parity)`, the surface's named argument (`NamedArg`, as test
   lines pass `(profile <- models)`). This is what lets a generic function over a structure
   (`all p xs`, section 3.8) be called as the field names are; decisions.md, question 4.
3. Qualified access, `Functor.map`, `Indexed.size`, `Product.first`, names the structure when two
   structures a type models share a field name, or when the argument's type cannot be inferred;
   `Functor.map listFunctor f xs` names the model too. It parses today as a projection on a name
   (`Proj(Var "Functor", "map")`); the elaborator reads a projection whose head is a structure's
   name as the qualified field.
4. A type with two models of one structure is two types (4.R13: `Int` as a ring and as the
   max-plus semiring; `Float64` under two metrics); the conversion between them is explicit.
5. Failure is an error, never a fallback: a field name whose discriminating argument has no
   inferable type, or whose type names no model of the structure, is refused with the name, the
   type found and the candidates. Today an operator whose left operand's type is unknown falls
   back to the bare name (`c.operators.get((op, ty), t.Var(op))`), which is how `x + "a"` passes
   `check` (report-bite-2.md).

### 2.3 Does the elaborator's `infer` extend as it is? No: the typing bite comes first

`infer` (elaborate.py:74) is partial by design: it knows the types of names declared in the
context, literals, annotated lambdas, applications whose function has a `Pi` type, projections on
records whose type it knows, and returns `Hole('type')` for the rest. Three things stand between it
and rule 2.2:

- the fallback (2.2.5): with per-concept names, an unresolved `map` has no bare function to fall
  back to (`map` is a field, defined nowhere at the top level), so every unresolved use would be a
  stuck term found at run time or by a test, not by `check`; item 39's finding (`asBad (x : Int)
  : Bool := x` passes; `check.py` runs program.lth's predicates and is no type checker) is the same
  gap;
- the key: the operator table is keyed by the syntactic domain type (`List A` with `A` a variable
  does not match `List Int`); resolution by the type's head (`List`, `Vec`, `Float64`) and
  matching under instantiation is new;
- the binding: nothing says today which definition is the model of `Functor` at `List`; the claim
  `ListIsAFunctor : Bool := Functor List {...}` is read by the tester as a law to run, not by the
  elaborator as a binding.

So the core's next code bite is the typing bite (bite 4), scoped to what resolution needs and not to
a full type checker (4.R9's strict conversion and 4.R11's refinement checks stay item 39's later
part). Its criteria are in section 6. Until it lands, bite 2's rule holds: "check clean" in an
acceptance criterion means the checker's predicates, and the signatures are verified by the test
programs' instances and controls.

### 2.4 The two forms, kept

A property is a Bool law over a type, its equality and the datum it qualifies (bite 2's files):

```
Commutative (A B : U) (o : Object B) (op : A -> A -> B) (x y : A) : Bool := o.eq (op x y) (op y x)
```

A structure is a record of its data with one line per law applying a property to a field, and the
conjunction (decisions.md, question 3, still open; the record form is what run.py's enumeration and
the tester evaluate today, and report-bite-2.md shows the kernel does not reduce a `&` of partially
applied laws):

```
Monoid (M : U) (o : Object M) : { neutral : M, combine : M -> M -> M }
MonoidAssociative (M : U) (o : Object M) (m : Monoid M o) (x y z : M) : Bool := Associative M o m.combine x y z
MonoidNeutral (M : U) (o : Object M) (m : Monoid M o) (x : M) : Bool := Neutral M o m.combine m.neutral x
Monoid (M : U) (o : Object M) := MonoidAssociative M o & MonoidNeutral M o
```

With rule 2.2.2 the `(o : Object M)` of every structure and property is filled by `M`'s `Object`
and written only when it is not the type's own (a second equality on one carrier is a second type,
2.2.4). The signatures below keep it, as the elaborated form keeps it.

A theory claims a property on its own operation by a one-line wrapper that binds the drawn domain
(`PlusCommutative (d : Doubles) (x y : Moderate) : Bool := Commutative Float64 Float64 d.plus x y`),
the property at the carrier (`Float64`), the parameters at the subtype the test draws (`Moderate`;
3.S6). The wrapper's name is the field's name joined to the adjective and is what a test line names.
The checker counts a property as claimed when any body mentions it (4.S14, `claimed_laws`).

## 3. The files, with their declarations

Bite 2's three properties files stand as built (report-bite-2.md: the composites quantify their
parts' variables and conjoin with `and`; `Complemented`'s constant is `z`; functions.lth imports
`Related`). Below, the files bites 6 and 7 write or rewrite; the `(o : Object A)` parameters are
implicit by 2.2.2.

### 3.1 structures/equality.lth

```
Object (A : U) : { eq : A -> A -> Bool }
ObjectEquivalence (A : U) (o : Object A) (x : A) (p : Related A o.eq) (c : Chain A o.eq) : Bool := Equivalence A o.eq x p c
Object (A : U) := ObjectEquivalence A
EqualPair (A : U) (o : Object A) : U := Related A o.eq
hasStructuralEquality : U -> Bool
Concrete : U := { A : U | hasStructuralEquality A }
structural (A : Concrete) : Object A := { eq := fn x y { x == y } }
Structural (A : Concrete) : { eq : A -> A -> Bool }        -- its laws: Equivalence and Substitutive, as today

-- a metric space over the type's equality (D-2026-10-17-f); its one name is `d`
Metric (A : U) (o : Object A) : { d : A -> A -> Float64 }
MetricZeroOnEqual (A : U) (o : Object A) (m : Metric A o) (p : EqualPair A o) : Bool := m.d p.x p.y == 0.0
MetricIndiscernible (A : U) (o : Object A) (m : Metric A o) (x y : A) : Bool := o.eq x y or not (m.d x y == 0.0)
MetricSymmetric (A : U) (o : Object A) (m : Metric A o) (x y : A) : Bool := Commutative A Float64 (structural Float64) m.d x y
Triangular (A : U) (d : A -> A -> Float64) (x y z : A) : Bool := d x z <= d x y + d y z
Ultratriangular (A : U) (d : A -> A -> Float64) (x y z : A) : Bool := d x z <= larger (d x y) (d y z)
MetricTriangular (A : U) (o : Object A) (m : Metric A o) (x y z : A) : Bool := Triangular A m.d x y z
MetricNonNegative (A : U) (o : Object A) (m : Metric A o) (x y : A) : Bool := 0.0 <= m.d x y     -- a theorem, stated for the control
Metric (A : U) (o : Object A) := MetricZeroOnEqual A o & MetricIndiscernible A o & MetricSymmetric A o & MetricTriangular A o & MetricNonNegative A o
Pseudometric (A : U) (o : Object A) : { d : A -> A -> Float64 }      -- M1 one way
Quasimetric (A : U) (o : Object A) : { d : A -> A -> Float64 }       -- no M2
Ultrametric (A : U) (o : Object A) : { d : A -> A -> Float64 }       -- M3 with max
Extended = { finite : NonNegativeFloat || infinite : Unit }
ExtendedMetric (A : U) (o : Object A) : { d : A -> A -> Extended }   -- declared; no model until one asks

Ball (A : U) (d : A -> A -> Float64) (radius : A -> A -> Float64) (x y : A) : Bool := d x y <= radius x y
Tolerance : U := { tol : Float64 | 0.0 <= tol }
MetricWithin (A : U) (o : Object A) : { d : A -> A -> Float64, bound : A -> A -> Float64 }   -- the floating-point claim, laws WithinZeroOnEqual, WithinSymmetric, WithinTriangular as in 54f6228
abs (x : Float64) : Float64
larger (a b : Float64) : Float64
absDistance (a b : Float64) : Float64 := abs (a - b)
NonNegativeFloat : U := { x : Float64 | 0.0 <= x }
```

The four variants share the field name `d` with `Metric`; a type that models two of them says which
by qualification (`Ultrametric.d`), and a type with two metrics is two types (2.2.4). Models and
controls: as in 54f6228's section 3.5 (core.lut claims `|a - b|` on `Small` and the discrete metric
on `Bool`; lists.lut the Hamming distance; the controls Kullback-Leibler, relative error, squared
Euclidean, a negative "distance" in `core_controls.test.lut`; `absDistance` on `Moderate` a
`MetricWithin` in numbers.lth with `bound := fn a b { u * absDistance a b }`).

### 3.2 structures/order.lth

```
Order (A : U) (o : Object A) : { leq : A -> A -> Bool }                -- the one name of an order
OrderIsTotal (A : U) (o : Object A) (r : Order A o) (x y : A) (c : Chain A r.leq) : Bool := TotalOrder A o r.leq x y c
Order (A : U) (o : Object A) := OrderIsTotal A o
less (A : U) (o : Object A) (r : Order A o) (x y : A) : Bool := r.leq x y and not (o.eq x y)
Least (A : U) (leq : A -> A -> Bool) (bottom : A) (x : A) : Bool := leq bottom x
Greatest (A : U) (leq : A -> A -> Bool) (top : A) (x : A) : Bool := leq x top
Discrete (A : U) (o : Object A) (leq : A -> A -> Bool) (succ : A -> A) (p : Related A leq) : Bool := o.eq p.x p.y or leq (succ p.x) p.y
MonotoneIn (A : U) (leq : A -> A -> Bool) (op : A -> A -> A) (p : Related A leq) (z : A) : Bool := leq (op p.x z) (op p.y z)
NonNegativePair (A : U) (leq : A -> A -> Bool) (zero : A) : U := { x y : A | leq zero x and leq zero y }
PositiveClosed (A : U) (leq : A -> A -> Bool) (times : A -> A -> A) (zero : A) (p : NonNegativePair A leq zero) : Bool := leq zero (times p.x p.y)
OrderedSemiring (S : U) (o : Object S) : { semiring : Semiring S o, order : Order S o }   -- laws: Semiring's, Order's, MonotoneIn plus, Least zero, Discrete (x + 1)
```

[proposed] `Order` as a structure with the one field `leq`, total: every order the library claims
is total (`Int`, `Nat`, `Float64` on `Moderate`, the grades' rank); a partial order gets its own
structure when a type asks. `leq` resolved by type replaces the `<=` primitive's role in laws;
`<=` stays the kernel's comparison (3.S17) and `IntIsOrdered` binds `leq := fn a b { a <= b }`.

### 3.3 structures/algebraic.lth

Each structure: a record, one wrapper per law, the conjunction. The field names are the concept's
and are the names every use resolves (section 2):

```
Semigroup (A : U) (o : Object A) : { combine : A -> A -> A }                              -- Associative
Monoid (A : U) (o : Object A) : { neutral : A, combine : A -> A -> A }                    -- Associative, Neutral
CommutativeMonoid (A : U) (o : Object A) : { neutral : A, combine : A -> A -> A }         -- Monoid's, Commutative
Group (A : U) (o : Object A) : { neutral : A, combine : A -> A -> A, inverse : A -> A }   -- Monoid's, Invertible
AbelianGroup (A : U) (o : Object A) : { neutral : A, combine : A -> A -> A, inverse : A -> A }
Semiring (A : U) (o : Object A) : { zero one : A, plus times : A -> A -> A }
  -- CommutativeMonoid plus zero, Monoid times one, Distributive times plus, Absorbing times zero, Distinct one zero
Ring (A : U) (o : Object A) : { zero one : A, plus times : A -> A -> A, negate : A -> A }
CommutativeRing (A : U) (o : Object A) : { zero one : A, plus times : A -> A -> A, negate : A -> A }
Lattice (A : U) (o : Object A) : { meet join : A -> A -> A }                              -- Associative, Commutative, Idempotent each; Absorptive
BooleanAlgebra (B : U) (o : Object B) : { top bottom : B, complement : B -> B, meet join : B -> B -> B }   -- Huntington, as in 54f6228
```

`+`, `*`, `-` stay bound by `operator` acts per type in core.lut (they are the kernel's
primitives); `plus x y` and `x + y` denote the same function at every type that claims `Semiring`
with them (`IntIsASemiring := Semiring Int { plus := intPlus, ... }`), and a law written with
`plus` reads at every semiring. [proposed] `List A`'s monoid operation is written `combine xs ys`
when generic and `xs + ys` at lists, with `operator + := combine` at `List A` in lists.lut, as
`String`'s `+` is its monoid already (core.lut); decisions.md, question 5.

### 3.4 structures/containers.lth

```
Functor (F : U -> U) : { map : (A B : U) -> (A -> B) -> F A -> F B }
Indexed (C A : U) : { size : C -> Nat, at : (c : C) -> Fin (size c) -> A }
Foldable (F : U -> U) : { fold : (A M : U) -> (M -> M -> M) -> M -> (A -> M) -> F A -> M }   -- to the right; nil -> neutral
Tabulated (C A : U) : { build : (n : Nat) -> (Fin n -> A) -> C }     -- the constructor from entries: List, Vec, Mat (row-major)

-- the generic functions over the structures, written once (L7.6); their structure parameters are
-- implicit (2.2.2), so a use reads `all p xs`, `member x xs`, `lookup k kvs`, `sum xs`
all (F : U -> U) (A : U) (f : Foldable F) (p : A -> Bool) (c : F A) : Bool := f.fold A Bool conj true p c
any (F : U -> U) (A : U) (f : Foldable F) (p : A -> Bool) (c : F A) : Bool := f.fold A Bool disj false p c
count (F : U -> U) (A : U) (f : Foldable F) (p : A -> Bool) (c : F A) : Nat
member (F : U -> U) (A : U) (f : Foldable F) (o : Object A) (x : A) (c : F A) : Bool := any F A f (fn y { o.eq x y }) c
lookup (F : U -> U) (K V : U) (f : Foldable F) (o : Object K) (k : K) (c : F (K * V)) : Maybe V
sum (F : U -> U) (A : U) (f : Foldable F) (m : Monoid A o) (c : F A) : A := f.fold A A m.combine m.neutral (id A) c
toList (F : U -> U) (A : U) (f : Foldable F) (c : F A) : List A
filter (F : U -> U) (A : U) (f : Foldable F) (p : A -> Bool) (c : F A) : List A
zipWith (C D E A B R : U) (i : Indexed C A) (j : Indexed D B) (t : Tabulated E R) (g : A -> B -> R) (c : C) (d : { d : D | size d == size c }) : E
sameEntries (C A : U) (i : Indexed C A) (o : Object A) (c d : C) : Bool
pointwise (C A : U) (i : Indexed C A) (o : Object A) : Object C := { eq := sameEntries C A i o }
supDistance (C A : U) (i : Indexed C A) (d : A -> A -> Float64) (c e : C) : Float64
entrywiseBall (C A : U) (i : Indexed C A) (d : A -> A -> Float64) (radius : (c : C) -> C -> Fin (i.size c) -> Float64) (c e : C) : Bool

-- the laws (D-2026-10-17-c), as in 54f6228: SizeMap, AtMap, SizeAppend (Preserving of monoids),
-- Extensional, MapId, MapCompose, FoldOfBuild; the folds over Fin n: forallBelow, existsBelow,
-- forallPairs, countBelow, foldWith, foldFrom, moved here from arrays.lth
```

`conj` and `disj` are core.lut's `and` and `or` as functions. `length` is `size` (one name of
`Indexed`); `nth` is `at` made total on `Fin (size xs)`, with `nth : List A -> Nat -> Maybe A` kept
in lists.lut for the callers that index by an `Int`. Claimants: `List` (lists.lut), `Vec` and `Mat`
(arrays.lth; `Mat` indexed row-major by `Fin (m * n)`, its two-index `f` kept), `Table` (tables.lth,
over its rows). The `approxVec`/`approxMat` family becomes `Ball` or `entrywiseBall` of
`supDistance absDistance` with the radius the law names (bite 11).

### 3.5 structures/universal.lth

As bite 1 left it (kernel_laws.lth §2, §4's free monoid, §6, names unchanged), with `(o : Object
P)` where a law compared a type parameter with `==`, plus `Equalizer`, `Pullback` and `Coequalizer`
as in 54f6228's section 3.9 (with `agreeing` for the pullback's pairs). `FreeMonoid`'s extension is
`Foldable`'s `fold`: `FreeMonoid (A : U) (F : U -> U) (o : Object (F A)) : { monoid : Monoid (F A) o,
inject : A -> F A, foldable : Foldable F }`, its laws `FoldNeutral`, `FoldInject`, `FoldCombine`,
`FoldIsItself` over `foldable.fold`, so the core has one `fold`. `Pushout` waits for a case
[proposed, as before]; the pushforward of measures is probability.lth's (bite 12).

### 3.6 core/core.lut

Keeps its content and its claims, renamed per 54f6228's section 3.10 (`NatIsAnOrderedSemiring`,
`KernelApplies`, `PairsAreTheProduct`, `RecordsAreNamedProducts`, `SumsAreNamedCoproducts`,
`BoolIsABooleanAlgebra` with `TopIsTheFirstBranch`, `ListIsTheFreeMonoid` over lists.lut's model),
and gains the claims that bind the per-concept names at the kernel's types (L2.8): `IntIsASemiring`,
`IntIsACommutativeRing`, `IntIsOrdered`, `NatIsOrdered`, `FloatIsOrdered` (on `Moderate`, through
numbers.lth's reading of `<=`: [proposed] the `Order` of `Float64` is claimed in core.lut since
`Float64` is core's, the within-bound semiring in numbers.lth where the doubles' laws are),
`StringIsAMonoid`, `IntIsAMetric` (`|a - b|` on `Small`), `BoolIsAMetric`, `FinIsACoequalizer`,
`SubtypeIsAnEqualizer`, `UnitIsTerminal`, `EmptyIsInitial`, `BoolIsACoproduct`, `MaybeIsACoproduct`.
Each claim is the binding rule 2.2.1 reads for its structure at its type. `CoreData` names them all;
`core_laws.test.lut` runs them; the store is `core.cert.json`.

### 3.7 core/lists.lut

List's models and the functions no structure covers:

```
mapList (A B : U) (f : A -> B) (xs : List A) : List B           -- the body behind the claims; a use writes `map`
foldList (A M : U) (combine : M -> M -> M) (neutral : M) (f : A -> M) (xs : List A) : M
lengthList (A : U) (xs : List A) : Nat
atList (A : U) (xs : List A) (i : Fin (lengthList A xs)) : A
buildList (A : U) (n : Nat) (f : Fin n -> A) : List A
appendList (A : U) (xs ys : List A) : List A
ListIsAFunctor (A B : U) : Bool := Functor List { map := mapList }
ListIsFoldable : Bool := Foldable List { fold := foldList }
ListIsIndexed (A : U) : Bool := Indexed (List A) A { size := lengthList A, at := atList A }
ListIsTabulated (A : U) : Bool := Tabulated (List A) A { build := buildList A }
ListIsAMonoid (A : U) : Bool := Monoid (List A) { neutral := nil, combine := appendList A }
operator + := appendList          -- [proposed] at List A; decisions.md, question 5
-- functions of lists alone
concat (A : U) (xss : List (List A)) : List A := sum (List (List A)) ... (the monoid's sum)
reverse (A : U) (xs : List A) : List A
nth (A : U) (xs : List A) (i : Nat) : Maybe A
zip (A B : U) (xs : List A) (ys : List B) : List (A * B)
take (A : U) (n : Nat) (xs : List A) : List A
drop (A : U) (n : Nat) (xs : List A) : List A
remove (A : U) (o : Object A) (x : A) (xs : List A) : List A
removeAll (A : U) (o : Object A) (xs ys : List A) : List A
distinct (A : U) (o : Object A) (xs : List A) : Bool
insertSorted (A : U) (leq : A -> A -> Bool) (x : A) (xs : List A) : List A
sortBy (A : U) (leq : A -> A -> Bool) (xs : List A) : List A
isEmpty (A : U) (xs : List A) : Bool
singleton (A : U) (x : A) : List A
hammingList : the Hamming distance on `List Bool` of a length, a `Metric` (3.1)
```

Laws claimed here: `MapKeepsLength` (SizeMap), `AppendAddsLengths` (SizeAppend), `MapId`,
`MapCompose`, `FoldOfBuild`, `ReverseIsAnInvolution`, `FilterKeeps` (LandsIn), `SortIsSorted`,
`SortIsAPermutation`; tests in `lists_laws.test.lut`, controls in `lists_controls.test.lut` (a `map`
that drops the last entry, an `append` that reverses its second argument, a `reverse` that fixes the
head, a `sortBy` that drops duplicates). The `...List` bodies are the models' and are not names a
file uses: the core's end counts a `mapList` written elsewhere as a reinvention.

### 3.8 What leaves the library

laws.lth §2 (the twelve `is...` templates, all unclaimed) in bite 9; algebra.lth §0 to §2 (`Iso`,
`AbelianGroup`, `CommutativeRing`, now the core's) and its three `Leq...` subtypes in bite 8, §3 to
§5 kept over the core (`Field`, `OrderedRing`, `OrderedField`, `CompleteOrderedField`);
numbers_model.lut's `integers` and `strings` become core.lut's claims; every `import "core/..."` line
outside the core (bite 1 wrote eleven) in bite 5.

## 4. The within-bound claims of numbers.lth

As in 54f6228's section 4, with per-concept names: `Doubles` keeps its record (the machine's
operations are what numbers.lth is about, 11.S4) and claims, over `Moderate`, `Commutative` on
`plus` and `times`, `Neutral` on `plus`/`0.0` and `times`/`1.0`, `Absorbing` on `times`/`0.0` (one
side), `Involutive` on negation, `Order` on `leq` (through core.lut's `FloatIsOrdered`), `MonotoneIn`
on `plus` and on `times` by a non-negative, and within a bound `AssociativeWithin` on `plus` with
`bound := fn x y z { 3.0 * gamma2 * (abs x + abs y + abs z) }` (`gamma2 := 2 u / (1 - 2 u)`, `u :=
epsilon / 2`; Higham 2002, Lemma 3.1, each side within `gamma2` of the exact sum, twice for the
difference, `(1 + u)^3` for measuring it, rounded up to 3; D-2026-10-17-f writes `gamma2` alone and
bite 2's instance already certified the 3-gamma2 form, report-bite-2.md), `AssociativeWithin` on
`times` over `|x y z|`, `DistributiveWithin` over `|x| (|y| + |z|)`, `InvertibleWithin` on
`divide` (`x * (1 / x)` within `2 u` of one); `absDistance` a `MetricWithin`. The doubles do not
claim `Semiring` (they are not one, 11.S15): `plus` and `times` at `Float64` resolve to `Doubles`'
fields through numbers.lth's claim `DoublesHaveTheOperations : Bool := Doubles { plus := floatPlus,
... }` [proposed], so a law written with `plus` reads at `Float64` too, with the within-bound laws
as its evidence. `within tol a b` and `withinOf tol scale a b` keep their names, defined by `Ball`.

## 5. The migration map

Every law and helper of today's library that the new core replaces, by concept. Old file paths are
under `src/luthier/lib/` unless written otherwise. "wrapper" means the theory keeps a one-line law
of the new name applying the property. Checked by:

```
cd /home/lmoffatt/Projects/luthier && awk -F'|' '/^\| `/ { print $2 }' record/plan/core-2026-10-17/execution.md \
  | grep -oE '`[^`]+`' | tr -d '`' | grep -vE '…' | sort -u | while read n; do \
  grep -rqE "^$n[ (:]|^$n\$" src/luthier/lib examples tests/tester || echo "MISSING $n"; done
```

(at d280a18 the command prints nothing). Rows of names that bite 1 moved unchanged
(kernel_laws.lth's, now in lib/core/structures/) give their present file.

### 5.1 Laws and theories

| old name | old file | new name | new file | note |
|---|---|---|---|---|
| `Object`, `EqualPair`, `Reflexive`, `Symmetric`, `Transitive` (of Object) | core/structures/equality.lth | `Object`, `EqualPair`; `ObjectEquivalence` wrapper of `Equivalence` | core/structures/equality.lth | the relation properties are bite 2's |
| `EqualChain` | core/structures/equality.lth | `Chain A o.eq` | core/properties/relations.lth | |
| `hasStructuralEquality`, `Concrete`, `Structural`, `Substitutive` | core/structures/equality.lth | same | core/structures/equality.lth | |
| `asObject`, `StructuralReflexive`, `StructuralSymmetric`, `StructuralTransitive` | core/structures/equality.lth | removed; `StructuralEquivalence` | core/structures/equality.lth | |
| `structuralEquality` | core/core.lut | `structural` | core/structures/equality.lth | |
| `Terminal`, `OnlyThePoint`, `Initial`, `NoValue` | core/structures/universal.lth | same | core/structures/universal.lth | |
| `BooleanAlgebra` | core/structures/algebraic.lth | `BooleanAlgebra` with `(o : Object B)` | core/structures/algebraic.lth | |
| `MeetCommutes`, `JoinCommutes` | core/structures/algebraic.lth | `MeetCommutative`, `JoinCommutative` wrappers of `Commutative` | core/structures/algebraic.lth | |
| `MeetIdentity`, `JoinIdentity` | core/structures/algebraic.lth | `MeetNeutral`, `JoinNeutral` wrappers of `Neutral` | core/structures/algebraic.lth | |
| `MeetDistributes`, `JoinDistributes` | core/structures/algebraic.lth | `MeetDistributive`, `JoinDistributive` wrappers of `Distributive` | core/structures/algebraic.lth | |
| `MeetComplement`, `JoinComplement` | core/structures/algebraic.lth | `MeetComplemented`, `JoinComplemented` wrappers of `Complemented` | core/structures/algebraic.lth | |
| `TopIsNotBottom` | core/structures/algebraic.lth | `TopDistinct` wrapper of `Distinct` | core/structures/algebraic.lth | |
| `TheBooleans` | core/structures/algebraic.lth | removed | | `BoolIsABooleanAlgebra` (core.lut) claims the algebra |
| `TopIsTheFirstBranch` | core/structures/algebraic.lth | `TopIsTheFirstBranch` | core/core.lut | Bool's own law (L2.8) |
| `Monoid` | core/structures/algebraic.lth | `Monoid` with `(o : Object A)`; fields `neutral`, `combine` | core/structures/algebraic.lth | importers algebra.lth, numbers_model.lut, universal.lth |
| `LeftNeutral`, `RightNeutral`, `Associative` (of Monoid) | core/structures/algebraic.lth | `MonoidNeutral`, `MonoidAssociative` wrappers of bite 2's `Neutral`, `Associative` | core/structures/algebraic.lth | the three names of bite 1's file collide with properties/operations.lth's and go |
| `FreeMonoid`, `asMonoid`, `IsMonoid` | core/structures/universal.lth | `FreeMonoid (A) (F) (o)` over `Foldable F`; `FreeMonoidIsAMonoid` | core/structures/universal.lth | one `fold` in the core |
| `FoldNeutral`, `FoldInject`, `FoldCombine`, `FoldIsItself` | core/structures/universal.lth | same, over `foldable.fold` | core/structures/universal.lth | |
| `Lists`, `NilIsNeutral`, `ConsIsInjectionCombined` | core/structures/universal.lth | removed; `NilIsNeutral`, `ConsIsInjectionCombined` | core/core.lut | List's own laws |
| `OrderedSemiring` and its laws (`PlusAssociative`, `PlusCommutes`, `PlusZero`, `TimesAssociative`, `TimesCommutes`, `TimesOne`, `TimesDistributes`, `TimesZero`, `LeqTotal`, `LeqAntisymmetric`, `LeqTransitive`, `PlusMonotone`, `ZeroLeast`, `OneIsNotZero`, `SuccessorIsNext`) | core/structures/algebraic.lth | `Semiring`'s wrappers (`PlusCommutative`, `PlusNeutral`, `TimesNeutral`, `TimesDistributive`, `TimesAbsorbing`, `OneDistinct`) and `OrderedSemiring`'s (`OrderIsTotal`, `OrderedSemiringPlusMonotone`, `OrderedSemiringZeroLeast`, `OrderedSemiringDiscrete`) | core/structures/algebraic.lth, order.lth | |
| `LeqPair`, `LeqChain`, `LeqBoth` | core/structures/algebraic.lth | `Related`, `Chain`; removed | core/properties/relations.lth | |
| `naturals` | core/core.lut | `NatIsAnOrderedSemiring` | core/core.lut | |
| `Exponential`, `Beta`, `Product`, `PairFst`, `PairSnd`, `Pairing`, `Coproduct`, `CaseLeft`, `CaseRight`, `CasesAreAll`, `Selected`, `one`, `two`, `NamedProduct`, `asProduct`, `NamedPairs`, `ProjectionNamesDistinct`, `SelectByName`, `NamedCoproduct`, `asCoproduct`, `NamedCases`, `InjectionNamesDistinct`, `LabelByName` | core/structures/universal.lth | same | core/structures/universal.lth | |
| `application`, `pairs`, `recordXY`, `sumAB` | core/core.lut | `KernelApplies`, `PairsAreTheProduct`, `RecordsAreNamedProducts`, `SumsAreNamedCoproducts` | core/core.lut | |
| `Iso`, `FromUndoesTo`, `ToUndoesFrom` | algebra.lth | `Isomorphism`, `Inverse` | core/properties/functions.lth (bite 2) | positions.lut's `layout` becomes `flatten`, `unflatten` and a claim; tests sonolocalizacion_* |
| `AbelianGroup`, `GroupIsMonoid`, `GroupCommutes`, `GroupInverse` | algebra.lth | `AbelianGroup` and its wrappers (`GroupInvertible` of `Invertible`) | core/structures/algebraic.lth | |
| `CommutativeRing`, `RingAdds`, `RingMultiplies`, `TimesCommutes`, `Distributes`, `OneIsNotZero` | algebra.lth | `CommutativeRing` and its wrappers | core/structures/algebraic.lth | |
| `zeroOf`, `oneOf`, `plusOf`, `timesOf`, `negateOf` | algebra.lth | `zero`, `one`, `plus`, `times`, `negate` | core/structures/algebraic.lth | the fields, resolved by type |
| `Field`, `Reciprocal`, `OrderedRing`, `OrderedField`, `FieldIsOrdered`, `CompleteOrderedField`, `SupIsUpperBound`, `SupIsLeast` | algebra.lth | stay, over the core's records | algebra.lth | |
| `LeqPair`, `LeqChain`, `LeqBoth`, `NonNegativePair`, `LeqTotal`, `LeqAntisymmetric`, `LeqTransitive`, `PlusMonotone`, `TimesPositive` | algebra.lth | `Related`, `Chain`, removed, `NonNegativePair`; `OrderedRingIsOrdered` wrapper of `Order`, `OrderedRingPlusMonotone` of `MonotoneIn`, `OrderedRingPositiveClosed` of `PositiveClosed` | core/properties/relations.lth, core/structures/order.lth, algebra.lth | |
| `integers`, `strings` | numbers_model.lut | `IntIsACommutativeRing`, `IntIsOrdered`, `StringIsAMonoid` | core/core.lut | |
| `PlusCommutes`, `TimesCommutes` | numbers.lth | `PlusCommutative`, `TimesCommutative` wrappers of `Commutative` | numbers.lth | test lines numbers_laws, numbers_controls; tests/test_certify.py:388-433, test_run.py:654-688, test_tester.py:28-31 |
| `PlusZero`, `TimesOne`, `TimesZero`, `NegateTwice` | numbers.lth | `PlusNeutral`, `TimesNeutral`, `TimesAbsorbing`, `NegateInvolutive` wrappers | numbers.lth | |
| `LeqPair`, `LeqChain`, `LeqReflexive`, `LeqTotal`, `LeqAntisymmetric`, `LeqTransitive` | numbers.lth | `Related`, `Chain`; `FloatIsOrdered` (core.lut) claims `Order` | core/properties/relations.lth, core/core.lut | |
| `PlusMonotone`, `TimesMonotone`, `SqrtMonotone` | numbers.lth | wrappers of `MonotoneIn`, `Monotone` | numbers.lth | |
| `doublesOrder` | numbers.lth | `Float64`'s `Order` (core.lut) | core/core.lut | |
| `Tolerance`, `abs` | numbers.lth | `Tolerance`, `abs` | core/structures/equality.lth | prelude: the import lines of arrays, probability, belief, optimization, generators, distances.lut and the test programs go |
| `within`, `withinOf` | numbers.lth | stay, defined by `Ball` | numbers.lth | |
| `Metric`, `WithinBounds`, `Grows`, `StartsAtLo`, `Translates`, `WithinAnyBounds`, `LinearMetric`, `LinearTranslates`, `LinearWithinAny`, `Scales`, `LogMetric`, `LogScales` | generators.lth | `Placement`, `LinearPlacement`, `LogPlacement` and their laws | generators.lth | decisions.md, question 2 (open); `test.lth`'s `SampledMode`, generators_model.lut, program.lth:328 |
| `Sized`, `SizeBounded` | generators.lth | `SizedGenerator`, `SizeBounded` | generators.lth | frees nothing now (containers' `Sized` is gone: `Indexed` carries `size`), kept for the clash with the concept's name |
| `isReflexive` … `isHomomorphism` (12 templates) | laws.lth | removed | | properties/ states each |
| `CombineCommutes`, `CombineAssociates` | laws.lth | `CombineCommutative`, `CombineAssociative` wrappers | laws.lth | |
| `CombineCommutes` | certification.lth | `CombineCommutative` wrapper | certification.lth | test lines regions_laws:98, regions_controls:130, tests/test_certify.py:1084 |
| `OwnIsIdempotent` | world.lth | wrapper of `Idempotent` (functions) | world.lth | |
| `CanonIdempotent`, `UnqualifyIdempotent` | term.lth | wrappers of `Idempotent` (functions) | term.lth | |
| `AddPointwise`, `SubPointwise`, `ScalePointwise`, `TransposePointwise`, `MaddPointwise`, `MsubPointwise`, `MscalePointwise` | arrays.lth | wrappers of `Pointwise` with `pointwise` equality | arrays.lth | |
| `DotSymmetric` | arrays.lth | `DotCommutative` wrapper of `Commutative` | arrays.lth | |
| `DotAgrees`, `MatVecAgrees`, `MatMulAgrees`, `TraceAgrees` | arrays.lth | stay, over `PointwiseWithin`/`entrywiseBall` with the radius from `absSumTo` | arrays.lth | |
| `MatMulIdentity` | arrays.lth | `MatMulNeutral` wrapper of `Neutral` on square matrices; the rectangular case its own law | arrays.lth | |
| `PinvSymmetric`, `PrecisionSymmetric`, `PosteriorInfoSymmetric`, `InfoSymmetric`, `StepMatrixSymmetric` | arrays, belief, probability, optimization | wrappers of `Ball` against `transpose` | same files | |
| `approxVec`, `approxMat`, `approxMatSlack`, `approxMatOf`, `approxMatSlackOf` | arrays.lth | `Ball`/`entrywiseBall` of `supDistance absDistance`; `approxVec tol`, `approxMat tol` kept as abbreviations | core/structures/equality.lth, containers.lth, arrays.lth | |
| `Symmetric` | arrays.lth | `Symmetric` the equalizer of `id` and `transpose` (`SymmetricIsAnEqualizer`) | arrays.lth, arrays_model.lut | |
| `KolmogorovOfMultiset`, `KolmogorovAgrees` | probability.lth | wrappers of `Congruent`, `Pointwise` | probability.lth | |
| `forallBelow`, `existsBelow`, `forallPairs`, `forallPairs2`, `countBelow`, `foldWith`, `foldFrom` | arrays.lth | same names | core/structures/containers.lth | prelude: the import lines go |
| `larger` | probability.lth | `larger` | core/structures/equality.lth | |
| `NonNegativeFloat` | grammar.lth | `NonNegativeFloat` | core/structures/equality.lth | |

### 5.2 Helpers the concepts replace

Generated by `grep -nE "^(all|any|append|member|lookup|concat|lengthOf)[A-Za-z0-9_]* " src/luthier/lib/*.lth
src/luthier/lib/*.lut examples/sonolocalizacion/*.lut` (104 lines at ca90ee8) plus the names found by
hand. The new name is the concept's, resolved at `List` (section 2); a row says which concept.

| old name | old file | new name | concept | note |
|---|---|---|---|---|
| `appendList`, `foldInto` | core/core.lut | `appendList`, `foldList` | lists.lut's models | core.lut's claim uses them through lists.lut |
| `lengthOf` | generators.lth, certification.lth, probability.lth, world.lth | `size` | Indexed | world_controls.test.lut:18,159-163 names world.lth's |
| `listLength` | tables.lth | `size` | Indexed | |
| `mapList` | world.lth | `map` | Functor | world_controls.test.lut names it |
| `memberOf` | generators.lth | `member` | Foldable, Object | |
| `allOf` | generators.lth | `all` | Foldable | unclaimed today |
| `noDuplicates` | generators.lth, plan.lth | `distinct` | lists.lut | |
| `distinct` | tables.lth | `distinct` | lists.lut | |
| `upTo` | generators.lth | `filter` with `size x <= n` | Foldable | |
| `nth` | generators.lth | `nth` | lists.lut | |
| `isEmptyList`, `isOneElement` | generators.lth | `isEmpty`, `size xs == 1` | lists.lut, Indexed | |
| `isEmpty` | ebnf.lth, checks.lth | `isEmpty` | lists.lut | checks.lth's over `Failures E = List E` |
| `member`, `concat`, `remove`, `removeAll` | term.lth, program.lth | `member`, `+` (or `combine`), `remove`, `removeAll` | Foldable, Monoid, lists.lut | |
| `memberStr` | plan.lth, tables.lth, world.lth | `member` | Foldable | |
| `memberString` | ebnf.lth | `member` | Foldable | |
| `memberChars` | grammar.lth | `all (fn c { member c ws }) cs` | Foldable | |
| `memberRegion` | certification.lth | `member` | Foldable | |
| `append` | ebnf.lth | `+` (or `combine`) | Monoid | |
| `appendRegions`, `appendRefusals`, `appendEntries` | certification.lth | `+` | Monoid | |
| `appendOne` | plan.lth | `xs + singleton n` | Monoid | |
| `appendStrs` | plot.lth | `+` | Monoid | |
| `appendLayer`, `appendTable` | plot.lth | `ls + singleton l` | Monoid | |
| `appendText`, `appendEnv`, `appendBindings` | term_model.lut | `+` | Monoid | |
| `appendApps`, `appendTerms` | program.lth | `+` | Monoid | |
| `appendNames` | examples/sonolocalizacion/figures.lut | `+` | Monoid | |
| `appendStr` | world.lth | keeps its name | | two strings, `+` already; not a list |
| `append` | examples/sonolocalizacion/distances.lut | `pushEntry` | | appends an entry to a `Vec`; renamed |
| `concatFailures` | checks.lth | `+` | Monoid | |
| `concatNames` | library.lth | `+` | Monoid | |
| `concatTerms` | program.lth | `+` | Monoid | |
| `concatFields`, `concatStrs` | world.lth | `+` | Monoid | |
| `lookupValue` | demand.lth | `lookup` | Foldable, Object | over `List (String * Value)` |
| `lookupStr`, `lookupTable`, `lookupScale` | plot.lth | `lookup` | Foldable | `Mapping = List (String * String)` |
| `lookupFile` | world_model.lut | `lookup` | Foldable | |
| `lookup` | program.lth | `lookup` | Foldable | `Context = List (String * Term)` |
| `lookupBody` | term_model.lut | keeps its name | | reads a `Program`'s acts |
| `lookupField` | term_model.lut | `lookup` | Foldable | |
| `allNonNegative` | generators.lth | `all (fn (x, w) { 0.0 <= w })` | Foldable | |
| `allNullable`, `anyNullable`, `anyReaches`, `allDefined`, `anyRhs` | ebnf.lth | `all`/`any` with the local predicate | Foldable | `anySplit` keeps its name: a search over positions |
| `allIn` | certification.lth, library.lth | `all (fn x { member x ys }) xs` | Foldable | |
| `anyServes`, `anyIs` | certification.lth | `any` | Foldable | |
| `anyExtern`, `anyMentions` | library.lth | `any` | Foldable | |
| `allNames`, `allPatterns`, `allWf`, `allFields`, `allPairs`, `allItems`, `allParams`, `allArms`, `allBinders`, `allClauses`, `allImportNames`, `allLiteralsLex`, `allKindsKnown` | grammar.lth | `all` with the local predicate | Foldable | |
| `allNames` | plan.lth | `all` | Foldable | |
| `allNames` | term_model.lut | keeps its name | | collects the names of a term |
| `allKnown` | tables.lth | `all knownKind` | Foldable | |
| `allConfirmed`, `anyRefuted`, `anyConfirmed`, `allRefutedOf`, `allConfirmedOrSupported` | laws.lth | `all`/`any` | Foldable | |
| `anyValue`, `anyFailure` | certification_model.lut | `any` | Foldable | |
| `allUnqualified`, `allFree` | term.lth | `all` | Foldable | |
| `allLayers`, `anyLayer`, `allStr`, `allScales` | plot.lth | `all`/`any` | Foldable | |
| `allUnit` | probability.lth | `all unitVec` | Foldable | |
| `anyUnknown`, `anyAct`, `anyUnclaimed`, `anyNotIn`, `anyUndefined`, `anyTerms`, `anyClause`, `anyIn`, `anyFault`, `anyApp`, `anyArgumentArrow`, `anyTermArrow`, `anyArrow`, `anyDatum` | program.lth | `any` with the local predicate | Foldable | `anyTerm (f) (t : Surface)` keeps its name: over one term's children |
| `insertSorted`, `sortedValues` | probability.lth | `insertSorted`, `sortBy` with `<=` | lists.lut | |
| `reverseOnto` | probability.lth | `reverse` | lists.lut | |
| `pooled`, `entriesOnto` | probability.lth | `concat (map entries vs)` | lists.lut, Functor | `entries : Vec Float64 -> List Float64` is `toList` of `Vec` |
| `isNilStr`, `isJustStr`, `isJustTable` | plot.lth | `isEmpty`; keep | lists.lut | the `Maybe` tests are not list helpers |
| `sumTo`, `sumToInt` | arrays.lth | stay | arrays.lth | a sum in 3.S27's order; `sum` of `Foldable` is the monoid's and does not fix the order |

## 6. The bites

Common acceptance (every bite): `luthier check` clean on every file touched, `check -v` with no
unclaimed law in `lib/core/` (elsewhere no more than before) and, after bite 4, no resolution
failure; `python -m pytest tests -q` green with at least as many tests as before (run in the
background, about 22 minutes); `luthier certify` on the test programs touched grades every law
(none `not run`) and reports every law controlled (no `uncontrolled`); the four counts of
`scripts/core_metrics.py` in the commit message, none higher than before; the plan's Status line
updated. Commits of two lines (subject, blank line, body), staged by path. No push, no tag
(D-2026-10-17-e). Bites 1 and 2 are landed (their sections of 54f6228 stand as history; the reports
say what was built).

Frame for bites 6 and 7 (D-2026-10-18-c, read it before writing them): three planes, the objects,
the levels of equivalence as one structure enriched over a base (Bool and, [0, inf] and +, later
distributions with a t-norm), and the computable types as their certified models; the theories of
the first two planes only declare and state laws with their mathematical references; whatever
computes lives in the third. The Boolean and metric bases first. The designer revises sections 2
and 3 for it before bite 6.

His answers of 2026-10-18 (D-2026-10-18-e, -f, -g): question 2 as recommended, generators.lth's
`Metric` becomes `Placement` (`LinearPlacement`, `LogPlacement`), test lines keep `SampledMode
linear`, done in bite 5 with chapter 7's three sentences; question 3 otherwise: no one-line wrappers
per law and structure; the tester first learns to split a conjunction of laws into its conjuncts,
each partially applied law with its missing variables quantified on its own (a new bite, 4b, Opus,
after the budgets bite and beside bite 5, in tester.py), then structures and composite properties
are written bare (bite 6, which also rewrites bite 2's composites to the bare form); question 4 as
recommended with three owners: the structure from the type's model when omitted (the theory's),
another structure passed by name (the author's, part of the definition), and a graded structure's
bound (a metric ball's epsilon) a demand parameter (L5.17), never fixed by the model or the
resolution. Question 5 (list append as `+`) open.

D-2026-10-18-h (2026-10-18): the rest of the night explores what the principle of the three levels
of equivalence changes and whether it can be done (record/plan/three-levels-2026-10-18/), read
only, before more code: bites 4 and 4b wait for its report; the budgets bite, already running,
finishes.

For bite 6 (D-2026-10-18-i): "cost" splits into error (a value's propagated bound, the metric
level), uncertainty (a value as a distribution, the probabilistic level), evidence (what a
certificate knows with a finite budget, eps-hat at 1 - delta) and resources (the budget, D-2026-10-
18-d). Their common algebra is a commutative ordered monoid, a quantale in complete form (the
Lawvere base): bite 6 declares `Quantale` in structures as the base of the three levels, with its
models named (error [0, inf] with + and <=; uncertainty distribution functions with a t-norm or
convolution; evidence [0, 1] with + or max; resources + in sequence and max in parallel), and the
functions group gains NonExpansive and Lipschitz, the generalization of Monotone (L6.8; Fuzz).
Declarations only; the recording bites belong to the three-levels plan after the core.

### Bite 3. The metrics script (Sonnet; first, alone)

Files: new `scripts/core_metrics.py` and `tests/test_core_metrics.py`. The script prints the four
counts of section 0 over `src/luthier/lib`, `examples/` and `tests/tester`: (1) names defined at
the top level in more than one file, with the files, less an explicit list of accepted homonyms
(each with a one-line reason); (2) reinvented list helpers: a top-level definition whose body is a
`match` on a `List` with `nil` and `cons` arms, or whose name is in the seven families, outside
`lib/core/lists.lut`; (3) unclaimed Bool laws, from `luthier check -v`; (4) `loose` notices, split
into real (a top-level definition at a bare exponential that no theory's record names) and the
rest. Each count with its list under `-v`. Luciano runs scripts that process the record; this one
processes the library and a bite's agent may run it (CLAUDE.md).
Accepted when: the script runs in under a minute; its counts at d280a18 are in its header and in
this plan's Status; the test checks each count on a fixture of three small files.
May break: nothing.

### Bite 4. Typing for resolution (Opus; after 3)

Files: `src/luthier/elaborate.py` (`infer`, `walk`, the operator table, the structure table),
`src/luthier/check.py` (the refusals), `src/luthier/run.py` (`Loaded` reads the structure
bindings), `tests/test_elaborate.py`, `tests/test_check.py`, `tests/spec/` (new accept and reject
programs), spec 4.R13 and 4.R9 (the spec's agent, from this plan); `docs/spec/04-static-semantics.md`
is not this bite's to edit.
What it does: rule 2.2 as the elaborator's. (a) `infer` total on the fragment the library writes
(names with declared types, literals, lambdas, applications, projections, `match`, `if`, blocks,
records, tuples, subtypes), returning the type or raising an error that names the term; a
`Hole('type')` result is a defect. (b) The structure table: a claim `X : Bool := S T m` (a structure
head `S`, a type `T`, a model record `m`) binds `(S, head of T) -> m`, read from every loaded file
at elaboration (the binding is the claim, so there is no second act). (c) A field name of a
structure, unqualified, resolves by the inferred type of its discriminating argument (2.2.1); a
structure-typed parameter omitted at a call is filled from the table (2.2.2); `S.f` and `S.f m`
qualify (2.2.3); operators match under instantiation (`List A` against `List Int`). (d) Failures
are errors with the name, the type found and the candidates (2.2.5); the bare fallback goes.
Accepted when: bite 2's three probes (`r x` typed `Bool` with `r : A -> A -> Bool`, a projection of
a field that does not exist, `x + "a"`) and item 39's `asBad (x : Int) : Bool := x` are refused
(four `tests/spec/*.reject.lut`); `tests/spec/r13_*` still accept and reject; a new
`r13_structure_name.accept.lut` resolves `size`, `map` and `eq` at two types and
`r13_structure_ambiguous.reject.lut` is refused until qualified; every file of the library and every
test program elaborates with zero `Hole('type')` from `infer` on a definition's body (a pytest test
walks them); the stores do not change (an explicit model and a resolved one elaborate to the same
term, so no cone moves; checked by `luthier certify tests/tester/*.test.lut` printing `0 lines ran`
for every non-fixture program); the suite green.
May break: files whose terms `infer` could not type before and that now raise (the bite lists them
and fixes the library's annotations where the error is the library's, as item 39's audit expected);
`luthier eval`'s and `session`'s terms, which elaborate in a context with no file.

### Bite 5. The prelude, the refusal, qualified access (Opus; after 4)

Files: `src/luthier/run.py` (`Loaded` over the directory; `CORE` becomes the directory), `check.py`
(`coreNames` read from the core's files; the refusal of a redefinition; the `redundant` notice),
`cli.py` (`--no-core`), `tests/test_run.py`, `tests/test_check.py`, `tests/spec/` (a reject program
that redefines `map`; an accept program that uses `size` with no import); every `import "core/..."`
line outside lib/core/ removed (eleven after bite 1: term.lth, numbers_model.lut, world.lth,
plot.lth, algebra.lth, generators.lth, generators_model.lut, five test programs,
tests/test_run.py:1164); spec 12.S4 and 12.S22 (the spec's agent, from section 1).
Accepted when: a file that defines or declares a core name is refused by `check` and by the loader
with the core file named; `luthier check` on a file that writes `size xs` with no import passes;
the file cycle inside the core is tested (a name reaching itself through two core files is an
error with the path; the present cycle is not one); the suite green; no store changes (the loader's
scoping gives the same internal names).
May break: a user file that defines `map`, `size`, `at`, `d`, `plus`, `eq` or any field name of
section 3 (the examples define none; the refusal names what to rename); scripts that pass
`--no-core`.

### Bite 6. The structures and core's claims (Fable; after 5)

Files: `lib/core/structures/{equality, order, algebraic, containers, universal}.lth` (sections 3.1
to 3.5), `lib/core/core.lut` (3.6), `numbers_model.lut` (`integers`, `strings` gone), `algebra.lth`
(§0 to §2 removed; §3 to §5 over the core), the importers of the moved folds (import lines go),
`tests/tester/core_instances.lut`, `core_laws.test.lut`, `core_controls.test.lut` (the wrappers of
bite 2 become the structures' and core.lut's claims; the instances that are the kernel's types stay
in core.lut; the metric controls).
Accepted when: `check -v` lists no unclaimed law in `lib/core/`; every claim of core.lut graded and
controlled; `Metric`'s four controls refuted; `size`, `at`, `map`, `eq`, `d`, `plus`, `leq` resolve
at `Int`, `Bool`, `String`, `Nat` through core.lut's claims (the accept program of bite 5 extended);
core_metrics' count (1) down by the `Leq...` and `OneIsNotZero` duplicates, count (3) down by bite
2's 32.
May break: positions.lut's `Iso` import (an alias `Iso` stays in algebra.lth until bite 12, noted);
the stores of algebra.lth's and core's laws (re-certified).

### Bite 7. The list library (Sonnet; after 6)

Files: new `lib/core/lists.lut` (3.7); `lib/core/core.lut` (`ListIsTheFreeMonoid` over lists.lut's
model; `appendList`, `foldInto` gone); new `tests/tester/lists_laws.test.lut`,
`lists_controls.test.lut`.
Accepted when: every function of 3.7 defined; every claim graded and controlled; `map`, `size`,
`at`, `fold`, `all`, `member`, `lookup`, `+` resolve at `List Int` with no import (an accept
program); core_metrics' count (2) unchanged (the reinventions go in bites 9 to 12).
May break: nothing outside core.lut.

### Bite 8. numbers.lth and algebra.lth (Opus; after 6, parallel with 7)

Files: `numbers.lth` (section 4), `numbers_model.lut`, `algebra.lth`, `tests/tester/numbers_laws.
test.lut`, `numbers_controls.test.lut`, `tests/test_certify.py:388-433`, `tests/test_run.py:654-688`,
`tests/test_tester.py:28-31` (the message names `PlusCommutes`; laws.test.lut's local `PlusCommutes`
may keep its name).
Accepted when: `Doubles`' within-bound laws graded with section 4's bounds and each controlled (an
`op` that rounds to a coarser grid; a bound too small on the real doubles, which also tells
`gamma2` from `3 gamma2`); `absDistance`'s `MetricWithin` graded and controlled; `plus`, `times`,
`leq` resolve at `Float64`; no `PlusCommutes` remains in lib/ or tests/ but laws.test.lut's.
May break: the importers of `Tolerance`, `within`, `abs` (import lines; the names and types stay).

### Bite 9. The machinery (Sonnet; after 7, parallel with 8 and 10)

Files: `laws.lth` (§2 removed; `Settling`'s wrappers), `certification.lth`, `generators.lth`
(`Placement` if question 2 is decided so, else `Metric` kept and the core's named `MetricSpace`;
`SizedGenerator`; helpers), `generators_model.lut`, `test.lth`, `world.lth`, `world_model.lut`,
`plan.lth`, `plan_model.lut`, `demand.lth`, `checks.lth`, `certification_model.lut`; their test
programs (`regions_*`, `certification_*`, `generators_*`, `world_*`, `plan_*`, `demand_*`,
`pooling_*`, `cutoff_controls`, `cases`, `weakest`, `laws`); `tests/test_certify.py:1084`.
Accepted when: no name of section 5.2's rows for these files remains; every renamed law graded and
controlled; core_metrics' count (2) down by these files' rows.
May break: program.lth's comment on `Metric` (line 328); nothing named `linear` changes.

### Bite 10. Luthier's self-description (Sonnet; after 7, parallel with 8 and 9)

Files: `term.lth`, `term_model.lut`, `program.lth`, `grammar.lth`, `ebnf.lth`, `ebnf_model.lut`,
`library.lth`, `translation.lth` (section 5.2's rows; `CanonIdempotent`, `UnqualifyIdempotent` as
wrappers); no test program of these exists (the finding "11 theories without tests or stores");
this bite adds none and says so in the plan.
Accepted when: `check` clean, the suite green (test_check, test_elaborate, test_parse read these
files), no old name remains, count (2) down by these rows.
May break: check.py's docstrings that name program.lth's helpers.

### Bite 11. Arrays and tables (Opus; after 8, parallel with 9 and 10)

Files: `arrays.lth` (`VecIsIndexed`, `VecIsAFunctor`, `VecIsTabulated`, `MatIsIndexed` and the rest
of 3.4's claims; the `Pointwise` wrappers; `Ball` and `entrywiseBall` for the `approx...` family,
the two abbreviations kept; `Symmetric` as an equalizer; `lengthOf` gone), `arrays_model.lut`,
`tables.lth` (`TableIsIndexed` over its rows; helpers), `tables_model.lut`, `generators_model.lut`'s
arrays imports (two lines, sent to bite 9's agent); `tests/tester/arrays_*`, `tables_*`.
Accepted when: every law of `Arrays` graded and controlled at the new names; `size v`, `at v k`,
`map f v` resolve at `Vec Float64`; `distance_graph.lut` and `validate_graph.run.lut` run unchanged.
May break: probability, belief, optimization, the examples (import lines of `approxVec`, `approxMat`,
`exact`: the names stay).

### Bite 12. Probability, belief, optimization, plot, the examples (Opus; after 11)

Files: `probability.lth` (Kolmogorov's wrappers; `pooled`, `sortedValues` by the core; the
pushforward of a measure as a structure with its law, D-2026-10-17-g), `probability_model.lut`,
`belief.lth`, `belief_model.lut`, `optimization.lth`, `optimization_model.lut`, `plot.lth` (helpers
only; its [proposed] readings wait for G1 to G5, D-2026-10-17-h), `plot_model.lut`;
`examples/sonolocalizacion/positions.lut` (`flatten`, `unflatten`, `LayoutIsAnIsomorphism`),
`distances.lut` (`pushEntry`), `figures.lut`, `distance_graph.lut` (the join as a `Pullback`
claim); `algebra.lth` (the `Iso` alias removed); their test programs (`probability_*`, `belief_*`,
`optimization_*`, `plot_*`, `fit_*`, `sonolocalizacion_*`).
Accepted when: the examples' stores re-certified; `experiment_zero.run.lut` and
`validate_graph.run.lut` reproduce their records; the check command of section 5 run with the new
names prints every old name as MISSING; core_metrics' counts (1) to (3) are 0.
May break: the fit's records (`*.run.json`): a changed cone is a changed key, so the runs are
redone and compared with the recorded values.
Also (D-2026-10-18, the coordinator on report-bite-4.md's question): correct the elaborations bite 4
kept for the hash. (1) `T * Float64` with `T : Concrete` is written `*` applied, not the product
(generators.lth's `weightOf`, `before`, `occurs`, `firstWeightOf`, `allNonNegative`;
generators_model.lut's `supportOf`; world.lth's `stateAfter`, `resultOf`): elaborate.py's `walk` of
`Binop` takes a type whose type is a subtype of `U` as a type. (2) An alias parameter captures a
record field of the same name (experiment_zero.lut's `fit` and `transformOf`): the field names of a
record type are bound in its later fields' types. (3) Product types nest to the left (`(A * B) *
C`) where 3.S4 says right, as tuples do. Each moves the cones that reach those definitions; the
stores re-certified once with this bite's. The spec marks each as a known defect (2.S8, 4.R7, 3.S4).

### Bite 13. Closing (Sonnet; after 12)

Files: this plan (Status), `record/plan/code-follows-principles-2026-10-16.md` (the core done, the
queue reopened), `record/handoff-*.md`; the notes to the spec's agent gathered (12.S4, 12.S22,
4.R13, 7.S2/7.S4 if question 2 is yes); `check.py`'s `loose` notice narrowed to the real cases
(count 4) if no earlier bite did it; `scripts/core_metrics.py` run and its four counts recorded
with the commit; the tag is Luciano's (D-2026-10-17-e).
Accepted when: the plan says nothing false; the counts are (1) 0, (2) 0, (3) 0, (4) the real ones
listed; the suite green; the stores committed.

## 7. Schedule

```
wave 1:  bite 3 (Sonnet, metrics)
wave 2:  bite 4 (Opus, typing for resolution)
wave 3:  bite 5 (Opus, prelude and refusal)
wave 4:  bite 6 (Fable, structures and core.lut)
wave 5:  bite 7 (Sonnet, lists.lut)          | bite 8 (Opus, numbers and algebra)
wave 6:  bite 9 (Sonnet, machinery)          | bite 10 (Sonnet, self-description)  | bite 11 (Opus, arrays and tables)
wave 7:  bite 12 (Opus, probability to the examples)
wave 8:  bite 13 (Sonnet, closing)
```

Waves 1 to 4 are sequential because each changes what the next writes against (the counts, the
resolution, the prelude, the structures); bite 3 is small and could run beside bite 4 if the code
agent is free, since they share no file. Wave 5 shares `core.lut` only through bite 7's edit of
`ListIsTheFreeMonoid`, made last; wave 6's three bites touch disjoint libraries and test programs
(bite 11's two import lines in `generators_model.lut` go to bite 9's agent). Never more than three
agents at once.

## 8. Decisions taken by the agent in this design (one commit undoes each)

From 54f6228, still standing: structures keep a record with one-line wrappers (question 3 open);
`Commutative` takes a domain and a codomain; contrapositive forms; `Surjective` by a section;
`functions (A B) (o)` declared, not defined; Metric's M1 as two laws and `MetricNonNegative` for the
control; `MetricWithin` as the floating-point claim; `Pushout` waits for a case; matrices indexed
row-major; `SizedGenerator`; `within`, `withinOf`, `approxVec tol`, `approxMat tol` kept as
abbreviations; the folds over `Fin n` in containers.lth; `integers` and `strings` as core.lut's
claims; the constant 3 gamma2.

New on 2026-10-18:
- The field names are the concepts' names: `eq`, `d`, `leq`, `neutral`, `combine`, `inverse`,
  `zero`, `one`, `plus`, `times`, `negate`, `meet`, `join`, `top`, `bottom`, `complement`, `map`,
  `size`, `at`, `fold`, `build`, `point`, `absurd`, `apply`, `pair`, `first`, `second`, `left`,
  `right`, `cases`, `include`, `restrict`, `project`, `lift`, `inject`; `length` is `size`, `nth`
  is `at` where the index is a `Fin`.
- A structure-typed parameter is implicit and filled from the type's model, passed by name when
  explicit (2.2.2); pending question 4.
- The claim is the binding (`ListIsAFunctor : Bool := Functor List {...}`): no second act.
- An import of a core name by its path is a `redundant` notice, not a refusal.
- `Order` is a structure with the one field `leq`, total.
- One `fold` in the core: `FreeMonoid` carries a `Foldable`.
- `Tabulated` (`build`) joins the container structures, so `map`, `zipWith` and `reverse` can be
  derived where a type has it.
- `Float64`'s `Order` is claimed in core.lut; the doubles' operations resolve through numbers.lth's
  claim of `Doubles` (section 4).
- The typing bite is scoped to resolution (section 2.3), not to a full type checker.
- The order of bites: metrics, typing, prelude, structures, lists, then the libraries by group.
