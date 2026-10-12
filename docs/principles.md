# The principles of Luthier

Draft 10, 2026-10-12, unapproved; written by hand from the projection of 44df5a7 and Luciano's
corrections on it (`docs/principles_corr.md` d5e81e3, his notes e3fa339, `docs/principles_cont.md`
323bda0, `docs/principles_3.md` 59ea8e9, `docs/principles copy.md` 01ba854, `docs/principles copy 2.md` 660b019, `docs/principles copy 3.md` 792ac84), every one of them
applied; the
organizers renumbered on the last (G1 theory and model, G2 cost, G3 the demand; the record keeps
the old tags until it is updated); what the model added on his
notes is marked *proposed* in the entry's Status. Written for the agent that builds the
specification: each entry gives its statement, its formulation, what it derives from, and its
status. His quotes, the sources and the history by draft are in `record/principles-language.md`,
which is to be updated from this draft once he marks it, after which `docs/principles.md` is again
the projection of the record (D-2026-10-12-d; `scripts/project_principles.py --check` fails until
then). The way of working, W1 to W15, is `docs/way-of-working.md`.

## Terms

- A *structure* is a type in the kernel's language (`04`), built from four forms: a product, a
  value made of several named fields (a record, a tuple); a sum, a value that is one of several
  cases, each tagged (a variant, an enumeration, `Maybe`); a function type `A -> B`; and a
  recursive type, one defined in terms of itself (a list, a tree). Each form may hold the others.
- A *predicate* is a function into `Bool`. A *cost* is a function into `Cost`, the non-negative
  reals with infinity, 0 true and ∞ false.
- A *law* is a predicate or a cost, or a combination of laws that is again a predicate or a cost;
  how laws combine is stated under G2.
- A *theory* is a structure with its law.
- A *model* is an inhabitant of a theory: a value of its structure whose law is certified.
- A *function* is a value of a function type `A -> B`, in the standard sense. A function type with
  its law is a theory, and a function that satisfies it is a model of that theory.
- The *dependences* of a theory are the theories whose models its structure and law use
  (`Monoid A` depends on `Setoid A`; `VectorSpace K V` on `Field K`). A carrier is assumed to come
  with the models it names, `A` with its setoid, `K` with its field, so a theory reads them from
  the type (his note of 2026-10-12; today the libraries pass them as parameters). Every theory has
  dependences; a function type has at least the setoids of its carriers, since its law uses their
  equality.
- A *certificate* is the record that a law was checked, with its grade (proved, exhaustive, cases,
  sampled at a level, assumed); a proof is a certificate of grade proved. To *certify* is to
  produce one.
- *Evaluation* computes a function, and has no effect (L18). *Execution* is an action on the world
  (print, save). Writing a certificate into the store Luthier owns is an action on Luthier's own
  state, verified by reading the store back (L12); `test` is that action (L19).
- The *demand* is a request for a value from outside the program, an action, carrying the type and
  the tolerance it wants, the type possibly decorated: the value with its error, its derivative,
  its certificate. The *planner* is what chooses, among the models certified equivalent, the one
  that runs, and plans the decorated type the demand asks for.

Status of the terms: his list (D-2026-10-12-f); the names structure, cost and certificate are the
model's where he left a question mark, marked OK by him on 2026-10-12; *dependences* replaces the
model's "dependent theory" on his note (every theory is one, so the emphasis goes on what it
depends on); the reading of certification as an action on Luthier's own state is proposed, kept
by him on 2026-10-12 with the clause "never an action on the world" removed as obscuring; the
carrier coming with its setoid and its field is his note of the same day. *Object* (`05 §3`) is
not a term; see What is open.

## The organizers

The guide, then the two eurekas, then the demand. Renumbered on his note of 2026-10-12: G1 is
theory and model (G2 until draft 9), G2 is cost (G3 until draft 9), G3 is the demand (G1 until
draft 9); the record and `record/decisions.md` keep the old tags until the record is updated with
this mapping.

**G0. Type theory is the guide.** A type is a proposition and a value its proof; a law is a
proposition over terms, so it defines a mathematical object and a quotient, and inside the class
the representative is free. Type theory guides what is declared. What governs execution is the
demand (G3), read in the same theory: a demanded type is a judgment to inhabit, execution is the
search for an inhabitant, and cost ranks the candidates (G2); where type theory normalizes a
given term, Luthier searches for one.
Status: settled, marked OK by him on 2026-10-12.

**G1. A type is a theory and its values are its models.** If a type is a proposition, then a
proposition can say that a structure follows the rules of a theory; so "this structure satisfies
the laws of the theory" is said, in the language of types, as "it is of the type of the theory": it is a model of the theory, and Luthier verifies that it is. Types thereby carry a
strong semantic meaning, and coding and testing are one act: to declare `m : T` is to declare the
tests `m` will pass (L3). What type
theory lacks: it knows a value by its term; Luthier knows it by the law it satisfies.
Status: settled; this wording is his note of 2026-10-12 put in order; the long form in the record.

**G2. Laws are valued in cost: one logic, extended to the non-negative reals.** Not every theory
is easily described by Booleans; many are represented better by costs; and
since object classifiers exist that extend logic to the non-negative reals, the composition of
errors in numerical libraries can be attacked with this one unified logic. How a law is validated:
a law is a predicate or a cost, a function into `Bool` or into `Cost`, [0,∞) with 0 true and ∞
false. Laws combine by and, or, then, and a quantifier over a carrier; a combination of predicates
is a predicate, and a cost as soon as one cost enters; `&`, the only join the libraries use today,
is one operator among these, and under cost the join is a sum, a max or a weighted sum. A law is
validated by a certificate with a grade (proved, exhaustive, cases, sampled at a level, assumed);
the demand supplies the tolerance; what a run teaches is kept.
Status: the second eureka on his note of 2026-10-12 (candidate by the P13 count, one decision
guided so far); the combinations are proposed on his note on Terms; the algebra of costs open
(`11`), the analysis he announced pending.

**G3. The demand defines what is computed.** The declarative face states what is known, universal
and minimally processed; the executive face is a demand from outside, and the demanded type fixes
the path, the types and the tolerances actually produced. What type theory lacks: an executive
face; there, computation is the normalization of a given term, with no demand.
Status: settled; printed third on his renumbering; whether it is an eureka of its own or the
executive clause of the guide (G0) is his to say.

## How the organizers depend on each other

*Proposed* (D8 of the generative plan).

1. G0's quotient needs G3 and G2 where the carrier carries a distance: there two implementations
   are interchangeable only up to a distance and below the tolerance the demanded type carries.
   On decidable carriers the exact quotient is correct and the kernel proceeds without G2;
   "optimización por error" has no meaning there and needs none. The interface that lets G2
   arrive without a rewrite: every law returns a `Cost`, and `Bool` is the two-valued case, the
   type of the result saying which (`11` §2, L21). A law into `Cost` returns a measure; the
   proposition is cost ≤ ε with ε the demand's, so G0's "a law is a proposition" holds once the
   tolerance is supplied. Until G2's algebra exists the application runs on this Boolean interim:
   laws of the form d(f x, g x) ≤ tol with tol a parameter (L17), no composition of tolerances
   along a chain, no run database.
2. G1's inhabitance needs G2: "validada aunque sea una vez" gives the certificate of a : A a
   grade, which is sound only if truth is graded. The judgment itself stays one and structural;
   the grade is its evidence (L2, `11` §4).
3. G3's planner is G0's proof search with G2's cost: it searches for an inhabitant of the
   demanded type and ranks candidates by cost.

So G2, the least developed, is load-bearing for G0 and G1 over carriers with a distance, whatever
the P13 count says today; over decidable carriers the Boolean kernel stands on its own.

## The principles of the language

Each L keeps its number and source from draft 1. `From:` names the organizers it derives from and
the derivation, the model's unless marked his. Order: by first organizer, G0, G1, G3, G2.

### From the guide, G0

**L2. A type is a proposition, and membership is a guarantee.** Belonging to a type asserts the
propositions, laws included, that the value satisfies; function types carry their laws the same way.
`a : A` is one judgment, structural and decidable for the kernel's types; it asserts the structural
proposition outright and the laws through the certificate, at the grade the certificate has, so
"guarantee" means what the grade says: proved or exhaustive, a guarantee; sampled, evidence at a
level; assumed, a hole that says so. What a law adds is evidence, and the certificate of the law
carries its grade (proved, exhaustive, cases, sampled, assumed) and, for a law into `Cost`, the
worst cost seen (`11` §4). The guarantee is what the certificate says and no more, and what leaves
the program carries one (L19, D-2026-10-11-n).
From: G0 directly; the second clause is the step to G1.
Status: settled.

**L4. The certified subtype from a predicate is the fundamental construction pattern.** From a
material type and a predicate come the certified type, its only constructor and the forgetful
projection; the same pattern builds values, functions and programs. A law gives the three at once:
the type, the constructor with Maybe, the membership function. Where the law is into `Cost`, the
constructor takes the tolerance as a parameter (L17) and the certificate records the tolerance it
was checked at, so a stricter demand asks for a new check (`11` §4). Types are verified before they
are constructed: Luthier starts from types by verification, and types by construction may come in
later.
From: G0 (a predicate is a proposition; its subtype is the type of its proofs) with G1 (verified,
not constructed).
Status: settled.

**L5. A law characterizes; it does not re-run.** A law states a mathematical property of an
operation; a second implementation checked against the first is consistency, and the native
definition is one more model certified against the law. A law over several functions is tested on
the values actually computed, as a puzzle whose pieces must fit; the cases to test are chosen by the
law, its arity (three elements for associativity) and the distribution sampled (L11), never every
path. Laws accumulate, and a law need not determine the operation; when the laws do determine it up
to the presentation's equality, that is the limit (D-2026-10-11-d). The generators are the model's
addition.
From: G0 (a law defines the object) and G1 (a law that transcribes the specimen is acquaintance, not
description); extends P10 (the mathematical object that best represents a concept is the invariant
of its type).
Status: settled.

**L6. Code is data.** A Luthier program is an element of Luthier; programs build, inspect and run
other programs, and the interpreter is meant to be written in the language it interprets.
From: G0 through the universe, the type of types (the object classifier of HoTT; the note's "object
classifier" names this when it means types as values, and the subobject classifier when it means
G2's truth values).
Status: settled.

**L7. The core is minimal and executable by hand.** A handful of well-specified primitives, so that
a program can be run with pencil and paper; everything else is a library whose translation to the
core is mechanical. Hand execution is of the kernel given a plan, an order of execution that is a
value (`lib/plan.lut`); the planner's choice among plans is outside the kernel. Four layers, each
trusted differently: the kernel, checked by hand; the libraries and the interpreter in Luthier,
certified against the kernel's laws; the host runtime, a specimen; the planner, advice that the plan
records.
From: G0 (a type theory is a few rules whose judgments a person checks; a small trusted kernel) and
G1 (the paper semantics is the description, and every interpreter is a specimen certified against
it).
Status: settled.

**L8. Declare, then define, then inhabit.** A declaration without a body is a first-class hole: at
once axiom, program input, external function, pending definition and dead code; nothing executes
until it is defined, and no value inhabits an undefined type; an axiom is not a value but a law with
grade `assumed`, so it does not inhabit. To the type checker the five are one, and the elaborated
form records which it is, since the demand treats them differently: an input asks for a value, an
external calls the host, a pending definition is an error, an axiom is a law with grade `assumed`,
reasoned with and never run (an item for the spec; `assumed` has one meaning, the grade). `extern`
is the operation that inhabits a hole with a body in another language, naming the language; a
theoretical module (types, functions, laws, no values) is a module of holes. (His words) A declared
name is assumed to have its declared type, and its use where that type is incompatible is an error
(`05` R1, the checker).
From: G0 (a hole is a hypothesis of the context) with G3 (nothing is produced until demanded).
Status: settled.

**L10. One function, many paths.** A function has many equivalent implementations, each with its
precision, speed, memory and place of execution; equivalence is established first, and the choice
among paths follows expected loss and cost, estimated from a database of measured runs; error, time
and memory are not one scalar, and the trade-off among them is a parameter of the demand (L17),
never the planner's own. Stated as a quotient: the implementations of a function are the quotient by
"compute the same function up to the law's equality", one class per mathematical function, and
inside the class the fibre of what differs; the class is chosen by law, the representative by cost.
The class is exact in the theory (`Real`); in a model that carries a distance it is the ball of the
demanded radius (`11` §3), and closeness is not transitive, so the planner substitutes one
implementation for another only along a certified equivalence between the two, the identity law of
L21 with its result `Bool` or `Cost` (D-2026-10-11-m). The law gives the candidates; the identity
certificates say which the planner may exchange, and they form a weighted graph, not a class: a
substitution is a path whose summed distance (`11` §2) is within the demanded tolerance, so two
specimens joined through a third may each replace it and not each other; the sum is a bound only
when every link is one (proved, exhaustive), otherwise an estimate with the weakest grade and the
samples it was seen on; a lone implementation is never replaced. A sampled edge is admissible only
on inputs the distribution it sampled covers, and only as a direct edge, never summed into a path,
until a probabilistic bound exists as a law; the tolerance charged at a node is the demand's pulled
back through the sensitivity of the cone from the node to the demand (`11` §5), and where no
sensitivity is known there is no substitution. The same for every grade: a link certified on a
subtype is a link only at inputs certified (L4) in that subtype, so a path exists at x only where
every link does; a `proved` link by citation carries the theorem's hypotheses as parameters (γ_n
needs n·u < 1, false for float32 over an hour at 48 kHz) and is void where they fail. The author's
free choice among the inhabitants of an under-determined function (D-2026-10-11-d, P5) stays; the
planner's choice is only among what has been compared.
From: G0 (the quotient), G2 (the choice by cost and the database of runs) and, before its
retirement, G4 (every path expressible; now L10's own clause).
Status: settled; the weighted graph, the admissibility of sampled edges and the subtype clause are
the model's, from the rounds of critiques.

**L12. Evaluation is verification; execution is an action on the world.** Luthier first describes
the problem and its equivalences; evaluating is checking them, as mathematics verifies rather than
runs. (His annotation) Executing is the executive face: an action changes the state of the world,
and it is verified too, by observing the world before and after it; the laws over actions are stated
over those two observations, as a mutable parameter is two variables (L9). An observation is itself
an action, so this stops where the world can be read back (a file written and reread), and says
nothing beyond; an effect on state Luthier owns is verified this way, an irreversible or concurrent
effect outside it is typed, logged and audited, never verified. Every function induces an
equivalence on its domain, its kernel, so computing f(x) is placing x in its class and the value is
the class's name: an interpretation of computation, not the evaluator's mechanism, and a name exists
only where a normal form does, the decidable fragment (no canonical form elsewhere); a predicate is
the two-class case and `Maybe T` places x in one of them. This equivalence on the domain is distinct
from the equivalence between terms that a law induces, which is L10's quotient.
From: G0 (identity is the first proposition; his "path equivalence is the fundamental concept",
2026-05-29); the two faces are G3's statement; the verification of actions from G1 (observation) and
G3.
Status: settled.

**L16. Equality has levels and belongs to the object.** Definition (`:=`), the identity proposition
(`=`), decidable equality (`==`) and definitional equality by reduction (`≡`) are different things,
and each object carries the observational equality that fits it. (His annotation) The binding acts
are two, `:=` once and `<-` rebinding, and they share one law: after the act the name equals the
term in the equality its type has, structural `==` where it exists (`05` R8), observational
otherwise, a distance under G2; after `:=` for all time, after `<-` until the next `<-` (`05` R12).
In the kernel the binding is exact: the name denotes the term, and reduction does not depend on a
tolerance; the distance enters when the planner realizes the term by another representative, which
it does only along a certified equivalence carrying its distance (L10, D-2026-10-11-m).
From: G0 (the identity type and its levels) with G2 (under cost, the identity proposition acquires a
distance).
Status: settled.

### From theory and model, G1

**L1. Luthier expresses the invariances of the disciplines.** What moves the language: a species
mates within itself, electrons are fermions, a probability integrates to one. A definition states
the invariances that determine a concept, and the language exists so that stating them is natural.
From: G1 (what is known of a thing is its description; "la idea de luthier es ayudar a descubrir las
invariantes de los calculos", note), with P14 (a type is a concept).
Status: settled.

**L3. Defining a model defines its test.** Declaring a model of a theory, `m : T`, declares the
tests it will be run on, so definition and verification are one act; a function type with its law
is a theory, and its model a function.
From: G1 directly: the eureka of 09.19 in its 2022 form.
Status: settled (the widening is his mark).

**L11. Verification is one operation, exact or statistical.** What is known by a theorem is cited,
what can be enumerated is checked exhaustively, what has chosen cases is checked on them, what can
only be sampled is checked statistically, and the grade of the evidence (proved, exhaustive, cases,
sampled at a level, assumed) travels with the value in a certificate hashed over its dependency
cone; the line is the method, since associativity over `Int` is computable and cannot be checked by
running. The grade of a sampled certificate depends on the distribution sampled, not only on the
number of samples, because errors concentrate at the edges (the model's correction, from the
practice of property-based testing). Verification by a theorem is `proved` by citation
(D-2026-10-11-f); verification by delegation is the same mechanism with the host library's guarantee
as the theorem cited (LAPACK's backward-error bounds, the condition number their hypothesis) and the
library's version and platform as hypotheses the certificate carries (L14); no new grade
(*Proposed*, on his mark). The law of a theory is one law, so its certificate is one certificate,
and its grade is composed from the grades of the parts: with `&`, the weakest; with a sum of costs,
the costs summed, each at its grade (proposed, on his note on Terms).
From: G1 (observation is how a description is verified) and G2 (the grade is the uncertainty of the
cost).
Status: settled; the reading of delegation as citation is proposed, his mark pending; he restated
the delegation in his own words on the readers' document ("proved by citing a theorem or taken from
a software library", afdd7c7), the reading as citation not marked.

**L14. Luthier orchestrates other languages.** Types and laws are native; values may come through
`extern` from Python or any host, declared over what they really receive and return, with
description and verification kept on Luthier's side. An external function is validated like any
other, against its type with its laws, the first time an action asks for it, and its certificate
stays by hash; without a type with a law to validate against it is not applied. (His words) "si el
tipo no sigue la ley no se aplica el calculo": an extern is declared over a type, a type carries its
laws (L2), the extern is validated against them before it is applied and refused if it fails; the
agreement test with the native is in addition (W5), and the planner's substitution is
D-2026-10-11-m. A function with no laws at all is not a function to run but a hole of a theory being
defined (L8). The extern's certificate binds the host library's version and the platform (W10), and
its declaration says whether it is a definition or an action (L12, L18). Certification is the
default for every value: demanding a value demands every certificate in its dependency cone, paid
once through the memo, unless the demand asks otherwise by a mechanism to be named, which leaves a
certificate of grade `assumed` (D-2026-10-11-n), since what could be done Luthier gives a way to do
(L22); `test` is the action that demands certificates without values (L19). Luthier is in use a
coupling language: the joint between two libraries is a theory of which each is a model, the bridges
between representations live at the joint with their cost and error, and no coupling without a law.
From: G1: an absorbed library is a specimen known by its description, and its code is not needed
("que la IA pueda ... extraer de librerías ajenas, chuparlas y usar las funciones con sus propias
invarianzas", audio 08.58, 31:25 to 32:00).
Status: settled by his correction (draft 7); the opt-out's syntax open.

**L21. A certificate of identity is not a certificate of the law.** Checking that an implementation
gives the same bits as before, with the same seed, certifies that the implementation has not
changed; checking it against its laws, by chosen or sampled cases, certifies the description. Both
are kept, apart, and the certificate of the law travels by the certificate of identity (his
annotation): exactly where the identity is boolean (`==` structural, `05` R8: integers, decidable
types, the same implementation rerun), and with the observed distance added where it is a cost (G2),
since two implementations over floats are almost never bit-identical. The type of the identity law's
result says which (`Bool` or `Cost`). The identity law between two specimens, with its distance, is
what admits a second implementation into the class the planner moves in (L10, D-2026-10-11-m); the
agreement test of W5 between native and extern is this law, and the reference formula of a law
evaluated over `Rational` is one more specimen, with grade exact, checked by the same law. (His
correction) Certification transports along identity: if B is certified at grade g on inputs X and
the identity A ≡ B is certified at grade h on inputs Y, then A is certified at the weaker of g and h
on X ∩ Y, and by nothing else. The two counterexamples of the third round follow: with B's laws only
`assumed` the transport gives A `assumed`, nothing (Kimi); a lookup table equal to the native on a
grid is certified on the grid and nowhere else (Claude). A function known correct by a theorem
outside Luthier is certified `proved` by citation (D-2026-10-11-f), and the chain law, citation,
native, identity, extern is carried by hash.
From: G1 (the specimen can be recognized as the same specimen, or described).
Status: proposed, candidate; the graded transport is his correction, his mark on the wording
pending.

**L20. A function is declared in a theory and is universal over its models.** A function belongs to
a theory (Real, Field, LinearAlgebra) and takes its model as its first, often implicit, argument, so
it is written once for every model; the model is named by the type of the argument (D-2026-10-11-j)
and can be passed explicitly. A theory over a model of another theory is a theory. Every type
belongs to a theory; the concrete types (products, sums, exponentials, `data`) belong to the
kernel's, whose laws are the β and η rules and the recursion principle, stated in
`lib/kernel_laws.lut`. Operators are resolved by the type, the type naming its model; a carrier with
two models is two types (D-2026-10-11-j). Modules are values by design, files today: a parametrized
module is a function from models to definitions, applicative because definitions have no effects
(L18), instantiated on demand with the parameter threaded down from the action. A specialization is
one more representative of the law's class (L10), valid on a subtype, certified against the same
law; where representations differ, the orchestrator inserts bridges by cost, coherent up to the law,
carrying their error, visible in the plan; a specialization and a bridge each enter the planner's
graph by an identity certificate with its distance (L10, D-2026-10-11-m). The conditions on bridges
are the model's, accepted.
From: G1, of which it is the definition rather than a consequence: a function belongs to the theory
its laws are stated in, and a model is where it runs; before draft 8 from G0 (a theory is a type, a
model its inhabitant) and G3 ("lo declarativo pasa a ser todo lo universal posible"; instantiated on
demand).
Status: absorbed into G1 on his mark (draft 9): the clause on specializations and bridges belongs to
L10 and modules as values to the spec (`03`); the tag stays for the record's citations and the text
stays until the spec takes its parts.

### From cost, G2

**L15. The ideal world is realized with a guarantee.** Code is written over ideal objects (Real) and
realized by concrete ones (Float64); the realization's laws hold within a stated tolerance, and the
error of each step is itself a law rather than a false claim of exactness. (His reading) Rounding
`Real -> Float64` is a functor in Lawvere's sense, and each law of `Real` is projected onto
`Float64` with its cost; it is not a homomorphism, and the exact map is the inclusion the other way.
(Correction proposed, his mark pending) Rounding does not expand distances by at most a constant:
two reals astride a rounding boundary land one ulp apart at any distance, so no multiplicative
constant exists; rounding is non-expansive up to an additive defect of about ε|x|, and for
subtraction and division the sensitivity is per input, the condition number (`11` §7). The functor
reading stands with "non-expansive plus an additive term", and the cost algebra needs both parts: a
multiplicative one where a Lipschitz constant exists and an additive one where rounding enters (`11`
§5, open).
From: G2 directly: the realization's distance to the ideal law is the law's value, and the tolerance
is the demand's (G3).
Status: settled in its statement; the correction on rounding is proposed, his mark pending.

### From the demand, G3

**L9. A program is a DAG and statements commute.** The unit is the definition; dependencies give the
only order there is, and time is reconstructed from them rather than from the text. Inside a block
the text fixes which binding a name means, each `<-` a fresh name (D-2026-10-11-i), and then
dependencies give the only order: after `x <- 1`, `y := x + 10`, `x <- 2`, y is 11, as the session
answers. Operations are declared before their laws, so a law that binds two operations is a node
with two parents, not a cycle; a mutable parameter is two variables, before and after, and mutation
in place is the planner's optimization when the earlier one has no other consumer. The DAG says what
depends on what; the structure the laws generate over terms (an equivalence when laws are boolean, a
metric space when they carry a distance) is a second structure, where L10 and L12 live.
From: G3 (the DAG is what the demand walks backward) with G2 (the second structure's metric); the
separation of the second structure is the model's proposal.
Status: settled.

**L13. Forgetting is determined by the demand.** Dependent typing accumulates history, so the
language needs non-invertible forgetful projections, and the demand chooses them: what is forgotten
is everything the demanded value does not need, the complement of its dependency cone, so the
projection is canonical, one per demand, and the language being spoken is what was asked for.
Forgetting at run time (a node freed after its last consumer) and forgetting in the type (how much
history a certificate keeps) are one; the program is never forgotten, only what leaves scope is
lost; forgetting is not materializing a derived value, never erasing what reconstructs or
recertifies it (code, inputs, model, seed, plan, tolerance), which the memo's identity keeps. A
function on a type applied to a subtype does not produce one overload per subtype; the demanded
return type selects which law to derive by composition (G1), and the rest is forgotten: doubling
positives is positive only when positivity is demanded and derivable, sin of positives forgets to
Real because no law composes. What is derivable is a property of the expression, independent of the
demand; the demand chooses which of it is derived, certified and carried, so the elaboration (types,
derivable laws) does not depend on the observer; the memo of results does (L19), and they are two
caches.
From: G3 directly, with G1 for what is derived.
Status: settled.

**L17. Every criterion is a parameter.** Thresholds, budgets, limits and statistical levels are
never constants in code; they are declared, passed and recorded. The outermost demand, an action
with no caller, carries its tolerance as a declared default argument (D-2026-10-11-c), recorded with
the call, so there is a root and it is a parameter.
From: G3 (the tolerance belongs to the demand) and G2 (a law states a distance, not a threshold), so
a constant in the code has no place to live; restates P11 (every criterion is a parameter, never a
constant in the code).
Status: settled.

**L18. A definition has no effects.** Its result depends only on its inputs; effects live only in
the actions (print, save). A mutable parameter written as before and after is not an effect, the
dependence is an edge; what is forbidden is what the graph does not show. It is the one assumption
under which every evaluation strategy gives the same result; over a carrier with a distance, a
result in the same class at a distance the plan records, and for the Boolean case this is
`Confluent` in `lib/plan.lut`, a law a dataflow is certified against rather than a theorem assumed.
(His words) No effect on the world; its one effect is on the program: it takes its name, once, and
enters the map of definitions, so the same name is not defined twice (`:=` once; `<-` only in a
block, D-2026-10-11-i).
From: G3 as its precondition rather than its consequence: the declarative face can be universal and
minimally processed only if definitions have no effects.
Status: settled.

**L19. The demand determines the computation.** The evaluation strategy is a parameter separate from
the program (L17); by default, a plan backward from the actions over names, evaluating nothing, then
a strict forward run over the live subgraph, each node once and whole: forward on demand. What the
action asks for flows backward along the plan and is produced forward: the value, its error, its derivative, its test, the type of its result; at the leaves a value lifts on
its own, takes a mark given with the demand, or is a hole. A decoration of the output is another
model of the theory the code was written over (L20): run over dual numbers the code gives its
derivative, run over intervals or over pairs of value and cost it gives its error; the demand
choosing the output type is the demand choosing the model, and the planner inserts the bridges
(L10). The derivative needs nothing new; the error waits for the algebra of costs (proposed, on his
note on Terms). The tests are actions, so verifying is demanding. What never
reaches an output needs no certificate, and what reaches one carries its cone's certificates
(D-2026-10-11-n; `test` demands certificates without values). A result is identified by code,
inputs, mode, the demanded type and tolerance, the model its type names, the seed, the plan that
produced it, the plan being a value (`lib/plan.lut`), and the hashes of the certificates in its live
cone, so a host library or platform that changed is a new result; the grade the demand states is in
the identity too, and a memo hit serves a demand only if the cached cone meets that grade, checked
at the hit and not only when the certificate was issued; the runtime includes the thread count and
scheduling of the host, and an extern whose bits depend on scheduling is not bit-identical to
itself, so its identity law is `Cost`, never `Bool` (L21). The run database is what the planner
reads to choose the plan and is not an input of the result once the plan is fixed; evidence
accumulates by a separate action with its own record, so "each node once" and G2's "kept across
runs" never meet on one node. A test is an action whose result is a certificate, memoized by the
certificate's identity (code, cases, seed, the distribution and level sampled, L11) and rerun when
asked or when that identity changed; the demand states the grade it requires (P11), and a
certificate serves every demand whose tolerance and grade it meets (`11` §4). "Each node once" is
once per plan: a stricter demand on the same definition is another node of another plan, and the
looser certificate still serves what it met. Three objects, never one: the meaning of a program, the
class its laws fix; a realization, the result under a plan; the evidence, its certificates. A
certificate is a frozen snapshot by hash; a later test does not change it, it issues a new one that
supersedes it, both kept, the latest in front (P3), so progress is the chain of certificates. Two
sessions that differ only in the order of independent bindings are equivalent by `Confluent` (L18),
the law the session block is certified against. The program is the synthesis and is kept, the
computation is the expansion and is redone. Script and interpreter are the same under this L, one
batch of demands or demands one at a time with the memo between them (08.58, 17:12 to 23:35; an item
for the spec, 04 §7); a session is a block and a file is never one, so a session saved to a file
becomes its `main` block (D-2026-10-11-i). The three cases at the leaves and the memo key are the
model's, accepted.
From: G3 directly; the audio of 08.58 (15:35 to 17:12, 30:37 to 31:21) adds the iteration step, read
every demand, run, collapse to the outputs, write, and asks whether the code object is consumed or
stable: kept.
Status: settled; the identity of a result, the memo gate and the three objects are the model's, from
the rounds of critiques.

**L22. The escape hatch is a world.** A definition or an implementation that does not follow
Luthier's way, an extern with no law yet, a foreign algorithm taken as is, is allowed inside a named
world (L12): its certificates are `assumed` (D-2026-10-11-n), the plan shows the world it ran in,
and nothing from it enters the planner's graph (L10) until a law is certified.
From: G3 (the demand names the world it runs in) with L12 and L14.
Status: proposed, candidate; the wording is the model's.

## What is open

- The articulation of G2, `docs/rationale/11-cost-valued-laws.md` draft 0 (D6): Ω replaced by
  [0,∞), quantitative equality, graded judgments, cost as −log p or as distance, how the
  uncertainty of a cost is represented in a certificate; the algebra of composition (second
  round §16): a Lipschitz constant per function type where known (sensitivity types, Reed and
  Pierce 2010; condition numbers), a sampled cost where not, costs adding as −log p under
  independence; worked examples the sum of n floats, a matrix inverse with κ(A), a sampled
  probability integrating to one.
- The extension of Boolean logic to Lawvere and Bayes, G2, which he names as another motivator or
  eureka (chat, 2026-10-12); whether it is the third eureka or a principle of good use is his to
  mark after that analysis.
- The composition of invariances (G1's derived route): which laws compose and how the demand
  selects them (audio 08.58, 32:01 to 34:07; audio 09.21).
- The session as a block over the dataflow of L19: `<-` to explore, `:=` to lock, a file may
  contain a block, `<-` banned at the top level of a file (decided, D-2026-10-11-i); the spec's
  `04 §7` and a section on the session.
- Done 2026-10-11, in the spec: blocks (`02 §9`, `04 §5`, `05` R12, D-2026-10-11-i); operators by
  the type naming its model (`05` R13, D-2026-10-11-j; `examples/z7ring.lut` rewritten, Z7 its
  own type and `mod 7` a certified homomorphism); Python-like separators (`02 §1`,
  D-2026-10-11-k); `cite` and `proved` by citation (`05 §7`, D-2026-10-11-f); `lib/laws.lut`
  split from `algebra.lut` (D-2026-10-11-l). Implemented 2026-10-11 in the interpreter: blocks
  and the session (`luthier session`), defaults and named arguments, R13's refusal of two models
  on one type, `cite` with `.bib` modules, exhaustive tables of `Fin n -> T`; `lib/plan.lut`
  states an order of execution as a value and confluence as a law, checked exhaustively in
  `examples/plan_confluence.lut`. Pending: actions and the world as a value; the memo between
  the items of a session.
- From the round of critiques: the interface of `Cost` in a certificate (a multiplicative
  constant where it exists, an additive defect where rounding enters, the grade as a lattice,
  the worst cost seen; `11` §5, §6); the identity of a result in the memo (L19) and `plan.lut`
  as its carrier; the opt-out of certification in a demand (D-2026-10-11-n, syntax open); the
  kind of a hole in the elaborated form (L8); the world as an opaque, unique value so that an
  action is never served from the memo (L18, L19); L15's rounding, his mark pending.
- The kernel's theory stated in Luthier: `src/luthier/lib/kernel_laws.lut`, tested on `Fin 3`,
  `Fin 2` (`examples/kernel_finite.lut`, 10 laws, sampled); eta not statable (`05` R8),
  functions over `Fin n` not enumerated by `exhaustive` (to fix).
- `proved` by citation: the citation a `.bib` key with a resolved DOI, ISBN or URL, and who
  checked (human, ai+human, none) recorded; syntax `cite name bibkey checked ai+human` proposed,
  allowed in user code (D-2026-10-11-f as amended; to `05 §7`).
- *Object* in the spec (`05 §3`, a strongly connected component of the dependency graph): not among
  the terms; in them it is a theory written in one cycle of names with its models, never a
  function. Proposed: `05 §3` becomes "theories are cycles" and the word survives only in "object
  classifier"; one commit over `04` and `05`; his decision.
- The decorated output (L19): the derivative by dual numbers as a model of the theory, the error
  by intervals or value-and-cost pairs once the algebra of costs exists; what in the planner
  chooses the model and inserts the bridges.
- Units as a candidate L under G0: a dimension is a proposition, dimensions form a group under
  multiplication, the quantities of one dimension a one-dimensional vector space, the whole a
  graded algebra; addition inside a dimension, multiplication across (second round §18).
  Precedent quimulun (his repository); pressure from sonolocalización (metres, seconds, the
  speed of sound).
- The type with its equality as the base case of every theory (a setoid; a metric space where
  the equality is a cost), the kernel's structural `==` its model for the decidable types
  (`05` R8), the equality of functions extensional and derived from it (L21), the equality of
  models componentwise; and whether a type names its equality as it names its model (`05` R13).
  Proposed by the model on his observation of 2026-10-12 (D-2026-10-12-e); his note of the same
  day on Terms goes the same way ("podríamos suponer que A viene con su Setoid", `K` with its
  `Field`); the syntax, how a type names its setoid and its field, is the open part.
- The names he left with a question mark in his list of terms (structure, cost, certificate) and
  the three-level answer to his doubt on validation as execution; and whether `05 §3` renames
  *object* (D-2026-10-12-f).
- His marks pending on this record: L21's wording (graded transport), L15's correction on
  rounding, L11's delegation as citation, the names lift, exact and within (G2), L22 as a
  candidate.
