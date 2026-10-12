# The principles of Luthier

Projected from `record/principles-language.md` (sha256 294bfac2341f, commit c6a9bc0 (modified in the working tree)) by `scripts/project_principles.py` (project_principles v2) on 2026-10-12; not edited by hand: edit the record and rerun the script (D-2026-10-12-d). Written for the agent that builds the specification. Each entry gives its statement, its current formulation (the model's unless a clause is marked his), what it derives from, its clauses each with its status, and its status; his quotes, the sources and the history by draft are in the record, and the way of working, W1 to W15, is `docs/way-of-working.md`.

## Purpose

One sentence, which is L1, heads the document: the language exists so that the invariances of a
discipline can be stated in it. Everything below says how.

**L1. Luthier expresses the invariances of the disciplines.**
From: G1 (what is known of a thing is its description; "la idea de luthier es ayudar a descubrir las
invariantes de los calculos", note), with P14 (a type is a concept).
- L1.1 What moves the language: a species mates within itself, electrons are fermions, a probability
  integrates to one. A definition states the invariances that determine a concept, and the language
  exists so that stating them is natural. [settled]
Status: settled; the purpose, not a design rule, so it heads the document.

## Terms

Each term has one category and is defined here and nowhere else; the principles cite Terms.

- A *structure* is a type in the kernel's language (`04`), built from four forms: a product, a
  value made of several named fields (a record, a tuple); a sum, a value that is one of several
  cases, each tagged (a variant, an enumeration, `Maybe`); a function type `A -> B`; and a
  recursive type, one defined in terms of itself (a list, a tree). Each form may hold the others.
- A *predicate* is a function into `Bool`. A *cost* is a function into `Cost`, the non-negative
  reals with infinity, 0 true and ∞ false.
- A *law* is a predicate or a cost, or a combination of laws that is again a predicate or a cost;
  how laws combine is L6.
- A *theory* is a structure with its law.
- A *model* is an inhabitant of a theory: a value of its structure whose law is certified.
- A *function* is a value of a function type `A -> B`, in the standard sense. A function type with
  its law is a theory, and a function that satisfies it is a model of that theory.
- The *dependences* of a theory are the theories whose models its structure and law use
  (`Monoid A` depends on `Setoid A`; `VectorSpace K V` on `Field K`). A carrier is assumed to come
  with the models it names, `A` with its setoid, `K` with its field, so a theory reads them from
  the type (O2 for the syntax). Every theory has dependences; a function type has at least the
  setoids of its carriers, since its law uses their equality.
- A *certificate* is the record that a law was checked, with its *grade*: *proved*, by a theorem
  cited or by delegation to a library's guarantee; *exhaustive*, over every case; *cases*, over
  chosen cases; *sampled at a level*, over a sample drawn from a stated distribution; *assumed*,
  not checked. A proof is a certificate of grade proved. To *certify* is to produce one.
- *Evaluation* computes a function, and has no effect (L9). *Execution* is an action on the world
  (print, save). Writing a certificate into the store Luthier owns is an action on Luthier's own
  state, verified by reading the store back (L9); `test` is that action (L10).
- The *demand* is a request for a value from outside the program, an action, carrying the type and
  the tolerance it wants, the type possibly decorated: the value with its error, its derivative,
  its certificate. The *planner* is what chooses, among the models certified equivalent, the one
  that runs, and plans the decorated type the demand asks for.
- The *declarative face* of a program is what it states: its types, laws and definitions. The
  *executive face* is what the demands ask of it.

*Object* (`05 §3`) is not a term (O7).

## The organizers

The guide and the two eurekas, in his order. An organizer is two sentences: what it says and what
it decides; it carries no mechanics and no status, and the principles under it are its section
below. The history of the eurekas and the P13 count are in the record.

**G0. Type theory is the guide.** A type is a proposition and a value its proof; a law is a
proposition over terms, so it defines a mathematical object and a quotient, and inside the class the
representative is free. Type theory guides what is declared, and what governs execution is the
demand, read in the same theory: a demanded type is a judgment to inhabit, execution is the search
for an inhabitant, and where type theory normalizes a given term, Luthier searches for one.
Tier: the guide.

**G1. A type is a theory and its values are its models.** If a type is a proposition, then a
proposition can say that a structure follows the rules of a theory, so "this structure satisfies the
laws of the theory" is said, in the language of types, as "it is of the type of the theory": it is a
model of the theory, and Luthier verifies that it is. Types thereby carry a strong semantic meaning,
and coding and testing are one act: to declare `m : T` is to declare the tests `m` will pass.
Tier: eureka, the first (the trigger, audio 09.19, 00:00 to 00:14).

**G2. Laws are valued in cost: one logic, extended to the non-negative reals.** Not every theory is
easily described by Booleans; many are represented better by costs. Since object classifiers exist
that extend logic to the non-negative reals, with the Booleans as a special case, the composition of
errors in numerical libraries can be attacked with this one unified logic.
Tier: the second eureka on his note of 2026-10-12.

## Precedence

When two statements conflict, the organizer they derive from decides; when two organizers
conflict, G0 decides; within an entry, the statement decides over its clauses. A clause marked
proposed, candidate or mark pending yields to one marked settled.

## The principles of the language

Fifteen principles, each under the organizer it derives from, in the order of his six topics.
Each is a statement, the fixed part, and numbered clauses, each with its own status: settled,
proposed (the model's, awaiting his mark), candidate, or mark pending (his words, the wording
awaiting his mark). Where a clause has a worked example, the example follows the clauses; what
each entry rests on among the open questions is named. The Numbering table at the end maps the
numbers of drafts 1 to 10.

### Under G0, the guide

**L4. Declare, then define, then inhabit.**
From: G0 (a hole is a hypothesis of the context) with G0, the demand (nothing is produced until
demanded).
- L4.1 A declaration without a body is a first-class hole: at once axiom, program input, external
  function, pending definition and dead code; nothing executes until it is defined, and no value
  inhabits an undefined type. [settled]
- L4.2 An axiom is not a value but a law with grade `assumed`, so it does not inhabit; `assumed` has
  one meaning, the grade. [settled]
- L4.3 To the type checker the five are one, and the elaborated form records which it is, since the
  demand treats them differently: an input asks for a value, an external calls the host, a pending
  definition is an error, an axiom is a law with grade `assumed`, reasoned with and never run (O9).
  [settled]
- L4.4 `extern` is the operation that inhabits a hole with a body in another language, naming the
  language; a theoretical module (types, functions, laws, no values) is a module of holes. [settled]
- L4.5 (His words) A declared name is assumed to have its declared type, and its use where that type
  is incompatible is an error (`05` R1, the checker). [settled]
References: `05` R1.
Rests on: O9 (the kind of a hole in the elaborated form, for the spec).
Status: settled.

**L5. Equality has levels and belongs to the object.**
From: G0 (the identity type and its levels) with G2 (under cost, the identity proposition acquires a
distance); clause 4 from G1 (the specimen can be recognized as the same specimen, or described).
- L5.1 Definition (`:=`), the identity proposition (`=`), decidable equality (`==`) and definitional
  equality by reduction (`≡`) are different things, and each object carries the observational equality
  that fits it. [settled]
- L5.2 In the kernel the binding is exact: the name denotes the term, and reduction does not depend
  on a tolerance; the distance enters when the planner realizes the term by another representative,
  which it does only along a certified equivalence carrying its distance (L13, D-2026-10-11-m).
  [settled]
- L5.3 Equality is a law of the object: Boolean where the carrier is decidable, a distance where it
  carries one, and the type of the identity law's result, `Bool` or `Cost`, says which (L7); how a
  certified identity composes along a path is L16.7. [proposed]
References: D-2026-10-11-m.
Rests on: O2 (the equality a type comes with).
Status: settled; clause 3 proposed.

**L9. A program is a DAG of definitions without effects, and statements commute; actions have
effects, and are verified by observing the world before and after.**
From: G0, the demand (the DAG is what the demand walks backward) with G2 (the second structure's
metric); a definition without effects is G0, the demand's precondition rather than its consequence:
the declarative face can be universal and minimally processed only if definitions have no effects;
the separation of the second structure is the model's proposal.
- L9.1 The unit is the definition; dependencies give the only order there is, and time is
  reconstructed from them rather than from the text. [settled]
- L9.2 Inside a block the text fixes which binding a name means, each `<-` a fresh name
  (D-2026-10-11-i), and then dependencies give the only order. [settled]
- L9.3 (His annotation) The binding acts are two, `:=` once and `<-` rebinding, and they share one
  law: after the act the name equals the term in the equality its type has, structural `==` where it
  exists (`05` R8), observational otherwise, a distance under G2; after `:=` for all time, after `<-`
  until the next `<-` (`05` R12). [settled]
- L9.4 Operations are declared before their laws, so a law that binds two operations is a node with
  two parents, not a cycle. [settled]
- L9.5 A mutable parameter is two variables, before and after, so it is not an effect, the
  dependence is an edge, and mutation in place is the planner's optimization when the earlier one has
  no other consumer; what is forbidden is what the graph does not show. [settled]
- L9.6 The DAG says what depends on what; the structure the laws generate over terms (an equivalence
  when laws are boolean, a metric space when they carry a distance) is a second structure, where L13
  and L11 live. [settled]
- L9.7 A definition's result depends only on its inputs; effects live only in the actions (print,
  save). It is the one assumption under which every evaluation strategy gives the same result; over a
  carrier with a distance, a result in the same class at a distance the plan records, and for the
  Boolean case this is `Confluent` in `lib/plan.lut`, a law a dataflow is certified against rather
  than a theorem assumed. [settled]
- L9.8 (His words) No effect on the world; its one effect is on the program: it takes its name,
  once, and enters the map of definitions, so the same name is not defined twice (`:=` once; `<-` only
  in a block, D-2026-10-11-i). [settled]
- L9.9 (His annotation) Executing is the executive face: an action changes the state of the world,
  and it is verified too, by observing the world before and after it; the laws over actions are stated
  over those two observations, as a mutable parameter is two variables (L9). [settled]
- L9.10 An observation is itself an action, so this stops where the world can be read back (a file
  written and reread), and says nothing beyond; an effect on state Luthier owns is verified this way,
  an irreversible or concurrent effect outside it is typed, logged and audited, never verified.
  [settled]
- L9.11 An action on Luthier's own state, writing a certificate or running a test, is idempotent and
  memoizable; an action on the world never is: the world is an opaque, unique value, so an action on
  it is never served from the memo (D-2026-10-12-m, O3). [proposed]
Example: after `x <- 1`, `y := x + 10`, `x <- 2`, y is 11, as the session answers (clause 2).
References: `05` R12, `05` R8; D-2026-10-11-i, D-2026-10-12-m.
Rests on: O3 (the world as a value).
Status: settled; clause 11 proposed.

**L10. The demand determines the computation and the types produced; the meaning of a program, its
realization under a plan and its evidence are three objects, never one.**
From: G0, the demand directly; the audio of 08.58 (15:35 to 17:12, 30:37 to 31:21) adds the
iteration step, read every demand, run, collapse to the outputs, write, and asks whether the code
object is consumed or stable: kept; with G1 for what is derived (the former L13).
- L10.1 The declarative face states what is known, universal and minimally processed; the executive
  face is a demand from outside, and the demanded type fixes the path, the types and the tolerances
  actually produced. [settled]
- L10.2 The evaluation strategy is a parameter separate from the program (clause 18); by default, a
  plan backward from the actions over names, evaluating nothing, then a strict forward run over the
  live subgraph, each node once and whole: forward on demand. [settled]
- L10.3 What the action asks for flows backward along the plan and is produced forward: the value,
  its error, its derivative, its test, the type of its result; at the leaves a value lifts on its own,
  takes a mark given with the demand, or is a hole. [settled]
- L10.4 A decoration of the output is another model of the theory the code was written over (G1):
  run over dual numbers the code gives its derivative, run over intervals or over pairs of value and
  cost it gives its error; the demand choosing the output type is the demand choosing the model, and
  the planner inserts the bridges (L13). The derivative needs nothing new; the error waits for the
  algebra of costs (O1, O5). [proposed]
- L10.5 The tests are actions, so verifying is demanding; what a demand requires of the certificates
  in its cone, and when a certificate serves it, is L16.5 and L16.6. [settled]
- L10.6 A result is identified by code, inputs, mode, the demanded type and tolerance, the model its
  type names, the seed, the plan that produced it, the plan being a value (`lib/plan.lut`), and the
  hashes of the certificates in its live cone, so a host library or platform that changed is a new
  result. [settled]
- L10.7 The runtime includes the thread count and scheduling of the host, and an extern whose bits
  depend on scheduling is not bit-identical to itself, so its identity law is `Cost`, never `Bool`
  (L5). [settled]
- L10.8 The run database is what the planner reads to choose the plan and is not an input of the
  result once the plan is fixed; evidence accumulates by a separate action with its own record, so
  "each node once" and G2's "kept across runs" never meet on one node. [settled]
- L10.9 A test is an action whose result is a certificate (L16.4), rerun when asked or when the
  certificate's identity changed; "each node once" is once per plan: a stricter demand on the same
  definition is another node of another plan, and the looser certificate still serves what it met.
  [settled]
- L10.10 The meaning of a program is the class its laws fix; a realization is the result under a
  plan; the evidence is its certificates (L16): three objects, never one. [settled]
- L10.11 Two sessions that differ only in the order of independent bindings are equivalent by
  `Confluent` (L9), the law the session block is certified against. [settled]
- L10.12 The program is the synthesis and is kept, the computation is the expansion and is redone.
  Script and interpreter are the same under this L, one batch of demands or demands one at a time with
  the memo between them (`04` §7, O8); a session is a block and a file is never one, so a session
  saved to a file becomes its `main` block (D-2026-10-11-i). [settled]
- L10.13 What is produced, and which types, is what the demanded value needs; what it does not need,
  the complement of its dependency cone, is not produced, so the choice is canonical, one per demand,
  and the types being spoken are what was asked for. [settled]
- L10.14 Not producing at run time (a node freed after its last consumer) and not carrying in the
  type (how much history a certificate keeps) are one; the program is always kept, only what leaves
  scope is lost; not producing is not materializing a derived value, never erasing what reconstructs
  or recertifies it (code, inputs, model, seed, plan, tolerance), which the memo's identity keeps.
  [settled]
- L10.15 A function on a type applied to a subtype does not produce one overload per subtype; the
  demanded return type selects which law to derive by composition (G1, O4), and the rest is not
  produced. [settled]
- L10.16 What is derivable is a property of the expression, independent of the demand; the demand
  chooses which of it is derived, certified and carried, so the elaboration (types, derivable laws)
  does not depend on the observer; the memo of results does, and they are two caches. [settled]
- L10.17 The demand carries the cutoff: the minimal cutoff for a specimen to be considered, applied
  to the composed bound and the composed evidence cost of a path (D-2026-10-12-h, L16.5); a cutoff
  does not compose (L6.3), so it lives in the demand and is passed down from it, and no law carries
  one. [proposed]
- L10.18 No unrecorded policy constants: thresholds, budgets, limits, statistical levels and the
  planner's default policies are never constants in code; they are declared, passed and recorded. The
  kernel's primitives (0, ∞, `lift`, `exact`) and mathematical constants are not policies
  (D-2026-10-12-n). [proposed]
- L10.19 The outermost demand, an action with no caller, carries its tolerance as a declared default
  argument (D-2026-10-11-c), recorded with the call, so there is a root and it is a parameter.
  [settled]
Example: doubling positives is positive only when positivity is demanded and derivable, sin of
positives is only Real because no law composes (clause 15).
References: `04`; D-2026-10-11-c, D-2026-10-11-i, D-2026-10-12-h, D-2026-10-12-n.
Rests on: O1 (the error decoration), O3 (the world as a value), O5, O8, O12.
Status: settled; clause 4 proposed on his note on Terms; clauses 17 and 18 proposed.

**L13. One function, many specimens, chosen by maximizing the performance the demander chooses,
along certified identities.**
From: G0 (the quotient), G2 (the choice by cost and the database of runs) and, before its retirement
in draft 9, the organizer "expressive over restrictive" (every path expressible; now L13's own
clause).
- L13.1 A function has many equivalent implementations, its specimens, each with its precision,
  speed, memory and place of execution; equivalence is established first, and the choice among paths
  follows expected loss and resources, estimated from a database of measured runs. [settled]
- L13.2 The cost of a law and the resources of a run, time and memory, are not one scalar, and the
  trade-off among them is a parameter of the demand (L10), never the planner's own. [settled]
- L13.3 (His formula) What the planner ranks is an efficiency, exp(−w·cost) over the resources used,
  so that a specimen of cost zero has efficiency 1/resources and not zero, with w, the weight between
  cost and resources, the demand's parameter. [proposed]
- L13.4 Two regimes: on a decidable carrier (`Int`, `Fin n`) two implementations compute the same
  function or not, the quotient is exact, there is no precision to trade and the Boolean kernel stands
  on its own; on a carrier with a distance (`Float64`) they are interchangeable only up to a distance
  within the demanded tolerance, and precision can be traded for resources, which is where cost (G2)
  and the demand enter G0's quotient. [settled]
- L13.5 Semantic equivalence forms classes; certified substitutability forms a graph. In the theory
  the specimens of a function are the quotient by "compute the same function up to the law's
  equality", one class per mathematical function, the class chosen by law; in a model that carries a
  distance closeness is not transitive, there is no class, only the ball of the demanded radius (`11`
  §3), and the planner substitutes one specimen for another only along a certified identity between
  the two, the identity law of L5 with its result `Bool` or `Cost` (D-2026-10-11-m). [proposed]
- L13.6 The law gives the candidates; the identity certificates say which the planner may exchange,
  and they form a weighted graph: a substitution is a path whose summed distance (`11` §2) and summed
  evidence cost (L16.7) are within the demand's cutoff, so two specimens joined through a third may
  each replace it and not each other; a lone specimen is never replaced. [proposed]
- L13.7 A sampled edge is admissible on the distribution it sampled; it composes with edges sampled
  over the same distribution, the failure fractions summed, and not with others; the demand's evidence
  cutoff says whether it accepts the path (L16.8, D-2026-10-12-q). [proposed]
- L13.8 The tolerance charged at a node is the demand's pulled back through the sensitivity of the
  cone from the node to the demand (`11` §5), and where no sensitivity is known there is no
  substitution. [settled]
- L13.9 A link certified on a subtype is a link only at inputs certified (L3) in that subtype, so a
  path exists at x only where every link does; a `proved` link by citation carries the theorem's
  hypotheses as parameters and is void where they fail. [settled]
- L13.10 The author's free choice among the inhabitants of an under-determined function
  (D-2026-10-11-d, P5) stays; the planner's choice is only among what has been compared. [settled]
- L13.11 The identity law between two specimens, with its distance, is what admits a second
  implementation into the planner's graph (L13, D-2026-10-11-m); the agreement test of W5 between
  native and extern is this law, and the reference formula of a law evaluated over `Rational` is one
  more specimen, with grade exact, checked by the same law. [candidate]
Example: γ_n needs n·u < 1, false for float32 over an hour at 48 kHz, so the cited bound is void
there (clause 9).
References: `11`; D-2026-10-11-d, D-2026-10-11-m, D-2026-10-12-q; W5; P5.
Rests on: O1 (the sensitivity), O2.
Status: settled; statement in his words, 2026-10-12, with "specimens" and "along certified
identities" added; clauses 3, 5, 6, 7 proposed; clause 11 candidate, from L5.

**L15. The core is minimal, executable by hand, and its programs are data.**
From: G0 (a type theory is a few rules whose judgments a person checks; a small trusted kernel) and
G1 (the paper semantics is the description, and every interpreter is a specimen certified against
it); programs as data from G0 through the universe, the type of types (the object classifier of
HoTT; the note's "object classifier" names this when it means types as values, and the subobject
classifier when it means G2's truth values).
- L15.1 A handful of well-specified primitives, so that a program can be run with pencil and paper;
  everything else is a library whose translation to the core is mechanical. [settled]
- L15.2 Hand execution is of the kernel given a plan, an order of execution that is a value
  (`lib/plan.lut`); the planner's choice among plans is outside the kernel. [settled]
- L15.3 Four layers, each trusted differently: the kernel, checked by hand; the libraries and the
  interpreter in Luthier, certified against the kernel's laws; the host runtime, a specimen; the
  planner, advice that the plan records. [settled]
- L15.4 A Luthier program is an element of Luthier; programs build, inspect and run other programs,
  and the interpreter is meant to be written in the language it interprets. [settled]
Rests on: O11 (the kernel's theory stated in Luthier).
Status: settled.

### Under G1, theory and model

**L2. A type is a proposition, and membership is a guarantee.**
From: G0 directly; the second clause is the step to G1.
- L2.1 Belonging to a type asserts the propositions, laws included, that the value satisfies;
  function types carry their laws the same way. [settled]
- L2.2 `a : A` is one judgment, structural and decidable for the kernel's types; it asserts the
  structural proposition outright and the laws through the certificate, at the grade the certificate
  has. [settled]
- L2.3 "Guarantee" means what the grade (Terms) says: proved or exhaustive, a guarantee; sampled,
  evidence at a level; assumed, a hole that says so. [settled]
- L2.4 What a law adds is evidence, and the certificate of the law carries its grade and, for a law
  into `Cost`, the worst cost seen (`11` §4). [settled]
- L2.5 The guarantee is what the certificate says and no more, and what leaves the program carries
  one (L10, D-2026-10-11-n). [settled]
References: `11`; D-2026-10-11-n.
Rests on: O1 (the worst cost seen, and how the uncertainty of a cost sits in a certificate).
Status: settled.

**L7. A law characterizes; it is verified by one operation, exact or statistical; and the
certificate of identity is not the certificate of the law.**
From: G0 (a law defines the object) and G1 (a law that transcribes the specimen is acquaintance, not
description; observation is how a description is verified) with G2 (the grade is the uncertainty of
the cost); extends P10 (the mathematical object that best represents a concept is the invariant of
its type).
- L7.1 A law states a mathematical property of an operation; a second implementation checked against
  the first is consistency, and the native definition is one more model certified against the law.
  [settled]
- L7.2 A law over several functions is tested on the values actually computed, as a puzzle whose
  pieces must fit; the cases to test are chosen by the law, its arity (three elements for
  associativity) and the distribution sampled, never every path. [settled]
- L7.3 Laws accumulate, and a law need not determine the operation; when the laws do determine it up
  to the presentation's equality, that is the limit (D-2026-10-11-d). [settled]
- L7.4 What is known by a theorem is cited, what can be enumerated is checked exhaustively, what has
  chosen cases is checked on them, what can only be sampled is checked statistically, and the grade of
  the evidence (Terms) travels with the value in a certificate hashed over its dependency cone; the
  line is the method, since associativity over `Int` is computable and cannot be checked by running.
  [settled]
- L7.5 The grade of a sampled certificate depends on the distribution sampled, not only on the
  number of samples, because errors concentrate at the edges. [settled]
- L7.6 Checking that an implementation gives the same bits as before, with the same seed, certifies
  that the implementation has not changed; checking it against its laws, by chosen or sampled cases,
  certifies the description. Both are kept, apart. [settled]
- L7.7 (His annotation) The certificate of the law travels by the certificate of identity: exactly
  where the identity is boolean (`==` structural, `05` R8: integers, decidable types, the same
  implementation rerun), and with the observed distance added where it is a cost (G2), since two
  implementations over floats are almost never bit-identical; the type of the identity law's result
  says which (`Bool` or `Cost`). [settled]
References: `05` R8; D-2026-10-11-d.
Rests on: O1 (what a sampled level asserts, and its conversion to a cost, D-2026-10-12-r).
Status: settled.

**L16. A certificate records what is known of a law, its domain, its bound and its evidence; it is
frozen, it serves every demand it meets, and it transports along identity.**
From: G1 (a model is known by the law it satisfies, with the evidence it has) with G2 (evidence is a
cost) and G0, the demand (what the demand requires of the evidence is its own).
- L16.1 A certificate (Terms) names the law it records as checked, the domain the check covered (a
  subtype, the cases listed, or the distribution sampled), the bound observed (for a law into `Cost`,
  the worst cost seen), and the evidence: its grade and, for a sampled check, the sample's statistics
  converted to an evidence cost (D-2026-10-12-r). [proposed]
- L16.2 The grade is derived from the domain and the evidence cost: proved and exhaustive have
  evidence cost 0 on their domain; cases, 0 on the cases listed and ∞ outside; sampled, the finite
  cost of its statistics on the distribution sampled; assumed, the evidence cost the demand assigns to
  assumptions, a parameter with no default, so that a demand that names none refuses assumed values
  (D-2026-10-11-n, D-2026-10-12-r). The five names stay in the certificate for the reader; the planner
  reads the costs. [proposed]
- L16.3 The conversion from statistics to an evidence cost is a function with a declared shape, the
  sample's statistics and the demand's level in, a cost out, filled per theory (D-2026-10-12-r); the
  first instance is −log(1 − ε̂(n, δ)) in nats, with ε̂ the bound on the fraction of the distribution
  where the law's bound fails, from n samples at confidence 1 − δ, and δ the demand's parameter.
  [proposed]
- L16.4 A certificate is identified by a hash over its dependency cone (code, cases, seed, the
  distribution and level sampled); it is a frozen snapshot, and a later check does not change it but
  issues a new one that supersedes it, both kept, the latest in front (P3), so progress is the chain
  of certificates. [settled]
- L16.5 A certificate serves every demand whose cutoff it meets, on the bound and on the evidence
  cost alike (D-2026-10-12-h); the demand states what it requires (P11), and a memo hit serves a
  demand only if the cached cone meets it, checked at the hit and not only when the certificate was
  issued. [settled]
- L16.6 Certification is the default: demanding a value demands every certificate in its dependency
  cone, paid once through the memo, unless the demand opts out by a mechanism to be named (O3), which
  leaves a certificate of grade `assumed` (D-2026-10-11-n); what never reaches an output needs no
  certificate, and what reaches one carries its cone's; `test` is the action that demands certificates
  without values (L10). [settled]
- L16.7 Certification transports along identity: if B is certified on inputs X with bound b and
  evidence cost e, and the identity A ≡ B is certified on inputs Y with distance d and evidence cost
  e′, then A is certified on X ∩ Y with bound b + d and evidence cost e + e′, and by nothing else; a
  path of identities composes the same way, link by link, the distances summed and the evidence summed
  (D-2026-10-12-q). (His correction, in grades) A is certified at the weaker of the two grades on X ∩
  Y. [proposed]
- L16.8 Links sampled over different distributions do not compose without a law relating the
  distributions; links sampled over the same distribution compose by the union bound, the failure
  fractions summed, which is the probabilistic bound the planner waited for (D-2026-10-12-q). The
  composition algebra belongs to the theory's cost type, the sum its first instance; whether a demand
  accepts a sampled path is its evidence cutoff, a parameter (P11). [proposed]
- L16.9 No operation on certificates raises a grade, lowers an evidence cost or widens a domain
  without new evidence. [proposed]
Example: with B's laws only `assumed`, A inherits the cost of an assumption and nothing more; a
lookup table equal to the native on a grid is certified on the grid and nowhere else (clause 7).
References: D-2026-10-11-n, D-2026-10-12-h, D-2026-10-12-q, D-2026-10-12-r; P3, P11.
Rests on: O1 (the conversion and the algebra), O3 (the opt-out's syntax).
Status: proposed in draft 11; clauses 4 to 6 settled, moved from L10 and L14; clause 7 carries his
correction of draft 7 in grades.

**L14. Luthier orchestrates other languages; what does not follow its way lives in a world; a
foreign function is certified by delegation, and certification transports along equality.**
From: G1: an absorbed library is a specimen known by its description, and its code is not needed
("que la IA pueda ... extraer de librerías ajenas, chuparlas y usar las funciones con sus propias
invarianzas", audio 08.58, 31:25 to 32:00); the world from G0, the demand (the demand names the
world it runs in) with L11; delegation from G1 and G2 (the former L11); transport (clause 9) from
G1.
- L14.1 Types and laws are native; values may come through `extern` from Python or any host,
  declared over what they really receive and return, with description and verification kept on
  Luthier's side. [settled]
- L14.2 (His words, "si el tipo no sigue la ley no se aplica el calculo") An extern is declared over
  a type, a type carries its laws (L2), and the extern is validated against them, like any other
  function, the first time an action asks for it, before it is applied, and refused if it fails; its
  certificate stays by hash; without a type with a law to validate against it is not applied; the
  agreement test with the native is in addition (W5), and the planner's substitution is
  D-2026-10-11-m. [settled]
- L14.3 A function with no laws at all is not a function to run but a hole of a theory being defined
  (L4). [settled]
- L14.4 The extern's certificate binds the host library's version and the platform (W10), and its
  declaration says whether it is a definition or an action (L9). [settled]
- L14.5 Certification is the default for every value: demanding a value demands every certificate in
  its dependency cone, paid once through the memo, unless the demand asks otherwise by a mechanism to
  be named (O3), which leaves a certificate of grade `assumed` (D-2026-10-11-n), since what could be
  done Luthier gives a way to do; `test` is the action that demands certificates without values (L10).
  [settled]
- L14.6 Luthier is in use a coupling language: the joint between two libraries is a theory of which
  each is a model, the bridges between representations live at the joint with their cost and error,
  and no coupling without a law. [settled]
- L14.7 A definition or an implementation that does not follow Luthier's way, an extern with no law
  yet, a foreign algorithm taken as is, is allowed inside a named world (L11): its certificates are
  `assumed` (D-2026-10-11-n), the plan shows the world it ran in, and nothing from it enters the
  planner's graph (L13) until a law is certified. [candidate]
- L14.8 Verification by a theorem is `proved` by citation (D-2026-10-11-f); verification by
  delegation is the same mechanism with the host library's guarantee as the theorem cited (LAPACK's
  backward-error bounds, the condition number their hypothesis) and the library's version and platform
  as hypotheses the certificate carries; no new grade. A function known correct by a theorem outside
  Luthier is certified this way, and the chain law, citation, native, identity, extern is carried by
  hash. [proposed]
- L14.9 (His correction) Certification transports along identity: if B is certified at grade g on
  inputs X and the identity A ≡ B is certified at grade h on inputs Y, then A is certified at the
  weaker of g and h on X ∩ Y, and by nothing else. [mark pending]
Example: with B's laws only `assumed` the transport gives A `assumed`, nothing; a lookup table equal
to the native on a grid is certified on the grid and nowhere else (clause 9).
References: D-2026-10-11-f, D-2026-10-11-m, D-2026-10-11-n; W5, W10.
Rests on: O3 (the opt-out's syntax; the world as a value).
Status: settled by his correction of draft 7; clause 7 candidate, clause 8 proposed on his mark,
clause 9 his correction, his mark on the wording pending.

### Under G2, cost

**L6. Laws combine, and a predicate lifts to a cost.**
From: G2 directly (lift, exact and within were named under it on his mark, draft 9) with G0, the
demand (the cutoff lives in the demand).
- L6.1 Predicates combine by and, or, then, and by a quantifier over a carrier, and the result is a
  predicate; costs combine by sum, max and weighted sum, and the result is a cost; a combination that
  mixes the two is a cost, each predicate lifted. [proposed]
- L6.2 The lift is explicit and named: `lift : Bool -> Cost` sends true to 0 and false to ∞, `exact
  : Cost -> Bool` is c == 0, both homomorphisms with `exact ∘ lift = id`, so `Bool` is a retract of
  `Cost`, not a subtype, and the planner inserts the lift as a bridge of cost zero. [settled]
- L6.3 The cutoff `within ε : Cost -> Bool` lives only in the demand, since it does not compose (two
  links within ε are within 2ε). [settled]
- L6.4 `&`, the only join the libraries use today, is the Boolean and. [settled]
- L6.5 The law of a theory is one law, so its certificate is one certificate, and its grade is
  composed from the grades of the parts: with `&`, the weakest; with a sum of costs, the costs summed,
  each at its grade. [proposed]
Rests on: O1 (the algebra of costs; the two candidate models, D-2026-10-12-p).
Status: proposed on his note of 2026-10-12; clauses 2 and 3 settled on his mark of draft 9, the
names lift, exact and within his to rename.

**L8. The ideal world is realized with a guarantee.**
From: G2 directly: the realization's distance to the ideal law is the law's value, and the tolerance
is the demand's (G0, the demand).
- L8.1 Code is written over ideal objects (Real) and realized by concrete ones (Float64); the
  realization's laws hold within a stated tolerance, and the error of each step is itself a law rather
  than a false claim of exactness. [settled]
- L8.2 (His reading) Rounding `Real -> Float64` is a functor in Lawvere's sense, and each law of
  `Real` is projected onto `Float64` with its cost; it is not a homomorphism, and the exact map is the
  inclusion the other way. [settled]
- L8.3 Rounding does not expand distances by at most a constant: two reals astride a rounding
  boundary land one ulp apart at any distance, so no multiplicative constant exists; rounding is
  non-expansive up to an additive defect of about ε|x|, and for subtraction and division the
  sensitivity is per input, the condition number (`11` §7). [mark pending]
- L8.4 The functor reading stands with "non-expansive plus an additive term", and the cost algebra
  needs both parts: a multiplicative one where a Lipschitz constant exists and an additive one where
  rounding enters (`11` §5). [mark pending]
References: `11`.
Rests on: O1 (the two parts of the algebra).
Status: settled in its statement; clauses 3 and 4 are the correction proposed, his mark pending.

## What is open

Only questions whose answer changes the language or the specification, each with the entries it
blocks; the done and implemented items are in the record's drafts table.

- **O1** (language) The algebra of costs. Its articulation is `docs/rationale/11-cost-valued-laws.md`
  draft 0: Ω replaced by [0,∞), quantitative equality, graded judgments, cost as −log p or as
  distance, how the uncertainty of a cost is represented in a certificate; the composition: a
  Lipschitz constant per function type where known (sensitivity types, Reed and Pierce 2010;
  condition numbers), a sampled cost where not, costs adding as −log p under independence; the
  interface of `Cost` in a certificate (a multiplicative constant where it exists, an additive
  defect where rounding enters, the grade as a lattice, the worst cost seen; `11` §5, §6); worked
  examples the sum of n floats, a matrix inverse with κ(A), a sampled probability integrating to
  one. Two candidate models (D-2026-10-12-p): min and max, or 1/n log-sum-exp with 1/n sum. The
  extension of Boolean logic to Lawvere and Bayes, which he names as another motivator or eureka;
  whether it is the third eureka or a principle of good use is his to mark after that analysis.
  Until it exists the application runs on a Boolean interim: laws of the form d(f x, g x) ≤ tol
  with tol a parameter (L10), every law returning `Bool` or `Cost` with the result type saying
  which (`11` §2, L5), no composition of tolerances along a chain, no run database. Blocks L2.7,
  L5.3, L6, L8.3, L8.4, L10.4, L13.6, L13.8, L16.3, L16.8.
- **O2** (language) The type with its equality as the base case of every theory (a setoid; a
  metric space where the equality is a cost), the kernel's structural `==` its model for the
  decidable types (`05` R8), the equality of functions extensional and derived from it (L5), the
  equality of models componentwise; and whether a type names its equality as it names its model
  (`05` R13). Proposed by the model on his observation of 2026-10-12 (D-2026-10-12-e); his note of
  the same day on Terms goes the same way ("podríamos suponer que A viene con su Setoid", `K` with
  its `Field`); the syntax, how a type names its setoid and its field, is the open part. Blocks
  Terms (dependences), L5, L7, L13.
- **O3** (language) The opt-out of certification in a demand (D-2026-10-11-n, syntax open); the
  world as an opaque, unique value so that an action is never served from the memo (L9, L10);
  actions and the world as a value, designed and not implemented. Blocks L9.11, L10.6, L14.6, L16.6.
- **O4** (language) The composition of invariances (G1's derived route): which laws compose and how
  the demand selects them (audio 08.58, 32:01 to 34:07; audio 09.21). Blocks L10.15.
- **O5** (language) The decorated output (L10.4): the derivative by dual numbers as a model of the
  theory, the error by intervals or value-and-cost pairs once O1 exists; what in the planner
  chooses the model and inserts the bridges. Blocks L10.4.
- **O6** (language) Units as a candidate L under G0: a dimension is a proposition, dimensions form
  a group under multiplication, the quantities of one dimension a one-dimensional vector space,
  the whole a graded algebra; addition inside a dimension, multiplication across (second round
  §18). Precedent quimulun (his repository); pressure from sonolocalización (metres, seconds, the
  speed of sound). Blocks nothing.
- **O7** (spec) *Object* in the spec (`05 §3`, a strongly connected component of the dependency
  graph): not among the terms; in them it is a theory written in one cycle of names with its
  models, never a function. Proposed: `05 §3` becomes "theories are cycles" and the word survives
  only in "object classifier"; one commit over `04` and `05`; his decision (D-2026-10-12-f). Blocks
  Terms.
- **O8** (spec) The session as a block over the dataflow of L10: `<-` to explore, `:=` to lock, a
  file may contain a block, `<-` banned at the top level of a file (decided, D-2026-10-11-i); the
  spec's `04 §7` and a section on the session; the memo between the items of a session. Blocks
  L10.12.
- **O9** (spec) The kind of a hole in the elaborated form (L4.3). Blocks L4.3.
- **O10** (spec) `proved` by citation: the citation a `.bib` key with a resolved DOI, ISBN or URL,
  and who checked (human, ai+human, none) recorded; syntax `cite name bibkey checked ai+human`
  proposed, allowed in user code (D-2026-10-11-f as amended; to `05 §7`). Blocks L7.7.
- **O11** (spec) The kernel's theory stated in Luthier: `src/luthier/lib/kernel_laws.lut`, tested
  on `Fin 3`, `Fin 2` (`examples/kernel_finite.lut`, 10 laws, sampled); eta not statable (`05`
  R8), functions over `Fin n` not enumerated by `exhaustive` (to fix). Blocks L15.
- **O12** (spec) The identity of a result in the memo (L10.6) and `plan.lut` as its carrier.
  Blocks L10.6.

## His marks pending

- L16.7 and L16.8, the composition of identities as paths (his note of 2026-10-12 put in
  words, with D-2026-10-12-q).
- L6, the names lift, exact and within (his to rename), and clauses 1 and 5.
- L8.3 and L8.4, the correction on rounding.
- L10.4, the decorated output as another model.
- L13.3, the wording of his formula for the efficiency.
- L14.6, the world as a candidate; L7.7, delegation as citation; L16.7, the wording of the graded
  transport (his correction).
- L16, the certificate entry; L2.3, what `a : A` asserts; L9.11, actions on Luthier's own state;
  L10.17 and L10.18, the cutoff and the policy constants; L13.3, 5, 6, 7; L6.2, 3, 5; L7.1.
- The two faces defined in Terms, and the shape of this draft (D-2026-10-12-g, -s).

## Keys

- G0, G1, G2: the organizers above; L1 to L15: the principles; L10.4: clause 4 of L10.
- O1 to O12: the open questions above.
- D-2026-10-11-n and the like: decisions, in `record/decisions.md`.
- P1 to P15: the principles of the method, `record/principles.md`.
- W1 to W15: the way of working, `docs/way-of-working.md`.
- `02` to `08`: the specification, `docs/spec/02-grammar.md` to `08-tests.md`; R1 to R13 the rules
  of `05`, the static semantics; `11`: `docs/rationale/11-cost-valued-laws.md`, and `01`, `07`,
  `09`, `10` the other rationale documents.
- His words, his annotation, his correction, his reading, his formula: Luciano's; a clause without
  such a mark is the model's.

## Numbering

The tags of draft 10 against those of drafts 1 to 9 (his marks on the reorder plan, 14ea9f0).

| Draft 11 | Before | What happened |
|---|---|---|
| G0 | G0 | kept |
| G1 | G2 | theory and model, printed first since draft 8; the former L3 and L20 absorbed |
| G2 | G3 | cost, the second eureka on his note; lift, exact and within moved to L6 |
| G3 | G1 | the demand, printed third in draft 10; dissolved in draft 11 into G0's second sentence and L10.1 |
| retired | G4 | retired in draft 9 (D-2026-10-12-c); its content became L22, now in L14 |
| L1 | L1 | kept; the Purpose section since draft 11 |
| L2 | L2 | kept |
| L3 | L4 | renumbered; "from a law" his correction |
| L4 | L8 | renumbered |
| L5 | L16, L21 | merged: equality has levels, with the identity clauses of L21 |
| L6 | new | how laws combine, the lift and the cutoff, from the former G3 |
| L7 | L5, L11, L21 | merged: a law characterizes, verified by one operation; identity is not the law |
| L8 | L15 | renumbered |
| L9 | L9, L18 | merged: a DAG of definitions without effects |
| L10 | L19, L13 | merged: the demand determines the computation and the types produced |
| L11 | L12 | renumbered and shortened; merged into L9 in draft 11 |
| L12 | L17 | renumbered; statement in his words; merged into L10 in draft 11 |
| L13 | L10 | renumbered; statement in his words |
| L14 | L14, L22, L11 (delegation), L21 (transport) | merged |
| L15 | L6, L7 | merged: the core is minimal and its programs are data |
| absorbed | L3 | into G1 (draft 10) |
| L16 | new | certificates, draft 11 (step 4) |
| absorbed | L20 | into G1 (draft 9) |
