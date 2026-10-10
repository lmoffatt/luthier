# The principles of Luthier and the way it is built

Draft 1, 2026-10-10, unapproved: every statement here waits for Luciano's mark. Draft 0 (commit
6d9dbd3) was drafted by the session's model from the synthesis of 2026-10-09
(`record/synthesis/2026-10-09_synthesis.md`), the cutoff candidates (`record/validation/cutoff/`),
the naive runs (`record/distillation/naive/`, D-2026-10-10-a) and the answers of five AIs reading
all 2,322 ideas (`record/distillation/web/alignment_2026-10-10.md`). Draft 1 adds the work of
2026-10-10 on execution: nine voice notes of that day (`record/audios/`, commits 60a10aa, 8a4c70f,
76ba165, 7b0481d, c6b302c, 0b5bd1c), the decisions D-2026-10-10-c to D-2026-10-10-i
(`record/decisions.md`) and the candidates file `record/principles-candidates-2026-10-10.md`,
which says item by item what is his and what the model proposed. L18 to L20 and W14 are new; L4,
L5, L8, L9, L10, L11, L13 and L14 are retouched, the retouch marked in each. Each principle
carries who first said it and the row of `record/ideas/timeline.jsonl` that holds the quote; the
notes of 2026-10-10 are cited by file and minute until the timeline carries them. The statements
are the model's wording of those sources; the division into two lists follows the two questions
the evidence answered separately.

The way of working below presents practice; the record of the principles in force, with their
quotes, assumptions and status, stays `record/principles.md` (P1 to P14).

## The language

**L1. Luthier expresses the invariances of the disciplines.** What moves the language: a species
mates within itself, electrons are fermions, a probability integrates to one. A definition states
the invariances that determine a concept, and the language exists so that stating them is natural.
Source: Luciano, 2026-05-29 (`dialogue:20260529T1400:expresar-invarianzas-de-disciplinas`).

**L2. A type is a proposition, and membership is a guarantee.** Belonging to a type asserts the
propositions, laws included, that the value satisfies; function types carry their laws the same
way. Source: Luciano, 2022-08-03 (`written:2022-08-03_haskell:proposicion-que-cada-tipo-cumple`);
restated 2026-05-26 (`day:2026-05-26:tipos-como-conceptos-y-proposiciones`).

**L3. Defining a function defines its test.** Declaring what a function must satisfy is declaring
the test that will be run on it, so definition and verification are one act. Source: Luciano,
2022-08-03 (`written:2022-08-03_haskell:declarar-funcion-es-declarar-su-test`).

**L4. The certified subtype from a predicate is the fundamental construction pattern.** From a
material type and a predicate come the certified type, its only constructor and the forgetful
projection; the same pattern builds values, functions and programs. A law gives the three at
once: the type, the constructor with Maybe, the membership function. Types are verified before
they are constructed: Luthier starts from types by verification, and types by construction may
come in later. Source: Luciano, 2022-08-03 (`written:2022-08-03_haskell:subtipos-con-predicado`);
named fundamental 2026-09-29 (`record/distillation/2026-10-09_find_principles_v2_claude-code_opus.md`,
C3); the three things and the scope 2026-10-10 (`WhatsApp Ptt 2026-10-10 at 10.12.21.md`, 05:24
to 08:10).

**L5. A law characterizes; it does not re-run.** A law states the mathematical property that
determines an operation up to the presentation's equality; a second implementation checked against
the first is consistency, and the native definition is one more model certified against the law.
A law over several functions is tested on the values actually computed, as a puzzle whose pieces
must fit; the cases to test are the generators the law's theory dictates (three elements for
associativity), never every path. Source: Luciano, 2026-10-05 ("La idea en realidad es buscar el
objeto matematico que mejor lo represente y decirlo"); extends P10 (the mathematical object that
best represents a concept is the invariant of its type); the puzzle 2026-10-10 (`WhatsApp Ptt
2026-10-10 at 10.12.21.md`, 11:38 to 18:20); the generators are the model's addition.

**L6. Code is data.** A Luthier program is an element of Luthier; programs build, inspect and run
other programs, and the interpreter is meant to be written in the language it interprets. Source:
Luciano, 2022-06-15 (`written:2022-06-15_sin-titulo-2:codigo-es-dato`).

**L7. The core is minimal and executable by hand.** A handful of well-specified primitives, so
that a program can be run with pencil and paper; everything else is a library whose translation to
the core is mechanical. Source: Luciano, 2026-05-29 ("Luthier tendría que ser ejecutable a mano").

**L8. Declare, then define, then inhabit.** A declaration without a body is a first-class hole: at
once axiom, program input, external function, pending definition and dead code; nothing executes
until it is defined, and no value inhabits an undefined type. `external` is the operation that
inhabits a hole with a body in another language, naming the language; a theoretical module (types,
functions, laws, no values) is a module of holes. Source: Luciano, 2026-05-29
(`dialogue:20260529T1400:tipos-no-definidos-y-forward-reference`); the hole named 2026-09-29;
`external` and the theoretical module 2026-10-10 (`WhatsApp Ptt 2026-10-10 at 17.41.53.md`;
`WhatsApp Ptt 2026-10-10 at 17.25.23.md`, 00:00 to 00:40).

**L9. A program is a DAG and statements commute.** The unit is the definition; dependencies give
the only order there is, and time is reconstructed from them rather than from the text.
Operations are declared before their laws, so a law that binds two operations is a node with two
parents, not a cycle; a mutable parameter is two variables, before and after, and mutation in
place is the planner's optimization when the earlier one has no other consumer. The DAG says what
depends on what; the structure the laws generate over terms (an equivalence when laws are boolean,
a metric space when they carry a distance) is a second structure, where L10 and L12 live. Source:
Luciano, 2026-05-29 (`note:2026-05-29T14.46.22:contexto-como-dag`); the unordered set of
definitions already in 2023-03-13 (`written:2023-03-13_hacia-luthier`); the two structures and the
mutable parameters 2026-10-10 (chat; D-2026-10-10-e); the separation of the second structure is
the model's proposal.

**L10. One function, many paths.** A function has many equivalent implementations, each with its
precision, speed, memory and place of execution; equivalence is established first, and the choice
among paths follows expected loss and cost, estimated from a database of measured runs. Stated as
a quotient: the implementations of a function are the quotient by "compute the same function up to
the law's equality", one class per mathematical function, and inside the class the fibre of what
differs; the class is chosen by law, the representative by cost. Source: Luciano, 2022-06-28
(`written:2022-06-28_luciano-code-style:choose-efficient-path-after-validity`); the quotient
2026-10-10 (`WhatsApp Ptt 2026-10-10 at 16.49.14.md`, 00:04 to 01:39), the same idea without the
word 2026-05-30 (`note:2026-05-30T18.01.53:equivalencias-para-clasificar-y-separar-decoraciones`).

**L11. Verification is one operation, exact or statistical.** What can be computed is checked
exactly; what can only be sampled is checked statistically, and the grade of the evidence (proved,
exhaustive, sampled at a level, assumed) travels with the value in a certificate hashed over its
dependency cone. The grade of a sampled certificate depends on the distribution sampled, not only
on the number of samples, because errors concentrate at the edges. Source: Luciano, 2022-08-03 and
2023-02-22 (`written:2023-02-22_tapp-wish-list:untested-a-tested`); the grades by samples
2026-10-10 (`WhatsApp Ptt 2026-10-10 at 11.11.22.md`, 03:02 to 04:12); the dependence on the
distribution is the model's correction, from the practice of property-based testing.

**L12. Execution is the verification of equivalences.** Luthier first describes the problem and
its equivalences; running is checking them, as mathematics verifies rather than runs, with a
declarative face (types, laws, theories, holes) and an executive face (values, actions). Source:
Luciano, 2026-05-30 ("la matemática no ejecuta ... la ejecución en Luthier sería esa verificación
de equivalencias").

**L13. Forgetting is determined by the demand.** Dependent typing accumulates history, so the
language needs non-invertible forgetful projections, and the demand chooses them: what is
forgotten is everything the demanded value does not need, the complement of its dependency cone,
so the projection is canonical, one per demand, and the language being spoken is what was asked
for. Forgetting at run time (a node freed after its last consumer) and forgetting in the type (how
much history a certificate keeps) are one; the program is never forgotten, only what leaves scope
is lost. Source: Luciano, 2026-05-29 (`note:2026-05-29T14.52.08:problema-del-olvido`); resolved
2026-10-10 ("olvidar esta determinado por todo lo que no hay que recordar, es decir lo que pide el
valor demandado. Eso soluciona el tema de los functores de olvido", chat; `WhatsApp Ptt
2026-10-10 at 11.42.15.md`, 01:07 and 03:20 to 03:55; `WhatsApp Ptt 2026-10-10 at 17.28.45.md`).

**L14. Luthier orchestrates other languages.** Types and laws are native; values may come through
`extern` from Python or any host, declared over what they really receive and return, with
description and verification kept on Luthier's side. An external function is validated like any
other, against its type with its laws, the first time an action asks for it, and its certificate
stays by hash; without a type with a law to validate against it is not applied. Luthier is in use
a coupling language: the joint between two libraries is a theory of which each is a model, the
bridges between representations live at the joint with their cost and error, and no coupling
without a law. Source: Luciano, 2026-05-26 (`note:2026-05-26T12.32.24:lenguaje-no-atado-a-cpp`);
the validation on first demand and the coupling language 2026-10-10 (chat: "si el tipo no sigue
la ley no se aplica el calculo"; `WhatsApp Ptt 2026-10-10 at 17.41.53.md`; `WhatsApp Ptt
2026-10-10 at 16.49.14.md`, 01:39 to 03:18).

**L15. The ideal world is realized with a guarantee.** Code is written over ideal objects (Real)
and realized by concrete ones (Float64); the realization's laws hold within a stated tolerance,
and the error of each step is itself a law rather than a false claim of exactness. Source:
Luciano, 2026-05-29.

**L16. Equality has levels and belongs to the object.** Definition (`:=`), the identity
proposition (`=`), decidable equality (`==`) and definitional equality by reduction (`≡`) are
different things, and each object carries the observational equality that fits it. Source:
Luciano, 2026-05-30 (`day:2026-05-30:niveles-de-equivalencia`).

**L17. Every criterion is a parameter.** Thresholds, budgets, limits and statistical levels are
never constants in code; they are declared, passed and recorded. Source: P11, in force; first
applied as a rule of the language 2026-10-05
(`dialogue:c7437496:lmmaxiter-should-be-a-parameter`).

**L18. A definition has no effects.** Its result depends only on its inputs; effects live only in
the actions (print, save). A mutable parameter written as before and after is not an effect, the
dependence is an edge; what is forbidden is what the graph does not show. It is the one assumption
under which every evaluation strategy gives the same result. Source: Luciano, 2026-10-10 ("lo que
si es no-side effects", chat; D-2026-10-10-c).

**L19. The demand determines the computation.** The evaluation strategy is a parameter separate
from the program (L17); by default, a plan backward from the actions over names, evaluating
nothing, then a strict forward run over the live subgraph, each node once and whole: forward on
demand. What the action asks for flows backward along the plan and is produced forward: the
value, its error, its derivative, its test, the type of its result; at the leaves a value lifts on
its own, takes a mark given with the demand, or is a hole. The tests are actions, so verifying is
demanding. What never reaches an output needs no certificate. Results are memoized by the hash of
code, inputs and mode; the program is the synthesis and is kept, the computation is the expansion
and is redone. Source: Luciano, 2026-10-10 (`WhatsApp Ptt 2026-10-10 at 11.11.22.md`, 00:00;
`WhatsApp Ptt 2026-10-10 at 11.42.15.md`, 01:02 to 04:07; `WhatsApp Ptt 2026-10-10 at 16.49.14.md`,
03:20 to 07:06; `WhatsApp Ptt 2026-10-10 at 17.25.23.md`, 05:49 to 07:53; `WhatsApp Ptt 2026-10-10
at 17.28.45.md`; D-2026-10-10-d, f, h). The three cases at the leaves and the memo key are the
model's, accepted.

**L20. Code is universal over the models of its theories.** A function is parametrized by theories
(Real, Field, LinearAlgebra), not by single functions; the model is resolved from the scope and can
be passed explicitly. Modules are values: a parametrized module is a function from models to
definitions, applicative because definitions have no effects (L18), instantiated on demand with
the parameter threaded down from the action. A specialization is one more representative of the
law's class (L10), valid on a subtype, certified against the same law; where representations
differ, the orchestrator inserts bridges by cost, coherent up to the law, carrying their error,
visible in the plan. Source: Luciano, 2026-10-10 ("el codigo seria, en principio universal a los
valores de funciones que cumplan las leyes requeridas", chat; `WhatsApp Ptt 2026-10-10 at
17.00.40.md`; `WhatsApp Ptt 2026-10-10 at 17.25.23.md`, 00:00 to 04:25; D-2026-10-10-g). The
conditions on bridges are the model's, accepted.

## The way of working

**W1. The specification comes before the implementation.** Syntax and semantics are fixed on paper
first, and the implementation passes the specification instead of silently defining the language.
Source: Luciano, 2026-06-03 (`day:2026-06-03:primero-sintaxis-y-semantica-despues-implementar`).

**W2. No rule enters without a worked example.** Each principle is tried by hand in the candidate
notation before it enters, and each rule of the specification is written as accept/reject pairs,
so the specification is an executable suite. Source: the model from Luciano's audios, 2026-08-31
(`dialogue:e6fc53cf:disciplina-ejemplo-en-papel`); the pairs 2026-10-04
(`dialogue:52d3e68e:short-cascade-with-pilot-spec-as-tests`).

**W3. Start minimal and add only what is used.** Begin from zero with the indispensable, do each
step in detail before scaling, and reduce until removing more would break something needed.
Source: Luciano, 2026-10-02 (`dialogue:51cca364:empezar-de-cero-con-luthier-liviano`).

**W4. The real application drives the growth.** Luthier must take root in something useful
(sonolocalización) and grow only where the application finds something it cannot express; kernel
work without real pressure moves the specification for nothing. Source: Luciano, 2026-09-21
(`day:2026-09-21:luthier-tiene-que-ser-util`).

**W5. Concepts live in Luthier, execution in the host.** The `.lut` is designed before the Python;
each concept is written native (slow, conceptual) and extern (fast, pragmatic) with the test that
they agree, and work has gone astray whenever something that belongs in Luthier sits in Python.
Source: Luciano, 2026-09-30.

**W6. A test must fail when the thing is wrong.** Laws are written before the algorithm; a law not
known to be true is worse than a hole; negative controls and reproduced numbers, never passing
examples alone, are what make a test diagnostic. Source: Luciano, 2025-09-27 (snapshots before
tests); the control stated 2026-10-02 (`dialogue:51cca364:a-test-needs-a-negative-control`).

**W7. The design stays with Luciano.** The model describes and waits; AI work comes in scoped
steps whose results he can interpret and check, because wholesale delegation cannot be judged.
For P1 (Luciano's part stays discernible). Source: Luciano, 2026-10-07
(`day:2026-10-07:chaining-ai-output-you-can-interpret`); the PI role 2026-10-05
(`dialogue:fea341bd:el-pi-de-diseño-queda-en-luciano`).

**W8. Every phase closes on a mechanical check.** A phase of a plan names the check that closes
it; a phase without one belongs to Luciano, and every rule that can become a check becomes one
(certifier, lint, test). State lives in files, never in a conversation. Source: the model,
2026-10-05 (`dialogue:fea341bd:cada-fase-con-su-chequeo-o-es-de-luciano`), adopted by Luciano.

**W9. A patch is named as a patch.** What compensates for a missing piece is logged as such and
kept out of the specification until the piece exists. Source: the model, 2026-10-05
(`dialogue:aa680014:tres-parches-reconocidos`), adopted by Luciano.

**W10. What is derived carries how it was derived.** Inputs by hash, the script or prompt with its
version, every parameter and the seed; certificates and the record are the same discipline. P2 in
force. Source: `record/principles.md`.

**W11. Every change can be undone.** Small commits, one decision per commit, tags for what is
reproduced, ownership declared between concurrent sessions. P6 in force. Source:
`record/principles.md`.

**W12. Reports are concepts, the most important first.** What failed and what limit was hit come
first; a count says nothing. For P12 (Luciano's attention is the scarce resource). Source:
Luciano, 2026-09-30 (`dialogue:ac750929:answers-at-concept-level`).

**W13. The foundations are rethought, the reasonable version first.** The language has been remade
many times (quimulun, tapp, macror, Luthier), each time deeper; the method is to work out the
reasonable version and then look for the wild one. Source: Luciano, 2022-06-15
(`written:2022-06-15_sin-titulo-2:rehacer-desde-las-bases`) and 2026-05-26
(`day:2026-05-26:razonar-primero-despues-la-locura`).

**W14. What reaches Luciano has few, rich concepts.** A synthesis can be judged because it has few
concepts; a long text with ideas he does not fully handle makes him doubt everything, and that is
what to avoid. For P12 (Luciano's attention is the scarce resource), as a criterion for what the
model brings him. Source: Luciano, 2026-10-09 (`WhatsApp Ptt 2026-10-09 at 10.43.06.md`, 04:24 to
05:06).
