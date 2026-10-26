# An idea of Luciano's: a law written either way, recognized by its normal form

2026-10-27, in the coordinating session (chat:luthier-3e:0). Recorded as an idea to think about,
not a decision.

His words: "Yo creo que justamente lo Luthier sería expresarlo de ambas formas. Y Luthier debería
deducir que es un caso de Commutative Mark Float etc... Una forma de lograr esto es encontrar una
especie de Normal form (como metáfora) de la ley. Es decir vos reconocés que la estructura interna
'normalizada' de TapeSymmetric y Commutative Mark Float... es la misma, como deducís que Newton y
kg m s^-2 son lo mismo. Para pensar."

The case: a user writes `ReadingSymmetric (t : Tape) (a b : Mark) : Bool := t.reading a b ==
t.reading b a`; the core has `Commutative (A B : U) (o : Object B) (op : A -> A -> B) (x y : A) :
Bool := o.eq (op x y) (op y x)`. Both should be allowed, and Luthier should say that the first is
the second at `Mark`, `Float64`, the structural equality and `t.reading`.

The coordinator's first reading (to think about, nothing built):
- Unfold both bodies (δ), reduce (β), compare up to the names of bound variables (α), the canonical
  form the cone hash already computes (`canon`): `ReadingSymmetric` normalizes to
  `t.reading a b == t.reading b a`, and `Commutative Mark Float64 (structural Float64) t.reading`
  to the same once `o.eq` at the structural equality unfolds to `==`.
- Recognizing an instance is matching the user's normal form against each core property's, with
  the property's parameters as pattern variables: higher-order matching, decidable on Miller's
  pattern fragment, which covers the core's properties (a parameter applied to distinct bound
  variables). Up to argument order, the permutations of the law's parameters.
- What it would give: a notice ("ReadingSymmetric is Commutative at Mark Float64"), the core's
  controls reused, and certificates shared when the canonical forms are equal (the same law, the
  same cone). It agrees with D-2026-10-25-a question 5: a canonical form only at the Boolean level,
  and laws are Booleans.
- The units analogy holds in shape: a unit's normal form is its vector of exponents over the base
  units; a law's is its βδ-normal body up to α and argument order. Equality of programs is
  undecidable in general, so the normal form recognizes many cases and claims nothing on the rest.

## His addition: an order on the operations

His words: "Y la forma de tener una forma canónica es tener una relación de orden en las operaciones
que haga que haya una sola representación 'ordenada'."

The coordinator's reading: this is how term rewriting gets canonical forms modulo commutativity and
associativity (AC-normalization: flatten an associative operator, sort the arguments of a
commutative one by a total order on terms), how a polynomial gets one by a monomial order (Gröbner
bases), and how a unit gets one by sorting its base units. Two Luthier-specific turns: (1) only an
operation certified commutative or associative may be reordered or flattened, so the claims of the
core justify the normalization; (2) a property that holds only within a bound gives no rewriting:
floating-point `+` is commutative exactly but associative only within 3γ₂, so a sum of floats may
have its two arguments sorted and may not be flattened. Parameters are ordered by first occurrence
in the normalized body. Equations that are not commutativity or associativity need completion
(Knuth–Bendix), which may not terminate: the normal form recognizes what an order decides and claims
nothing on the rest.
