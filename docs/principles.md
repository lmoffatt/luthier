# The principles of Luthier and the way it is built

Draft 0, 2026-10-10, unapproved: every statement here waits for Luciano's mark. Drafted by the
session's model from the synthesis of 2026-10-09 (`record/synthesis/2026-10-09_synthesis.md`), the
cutoff candidates (`record/validation/cutoff/`), the naive runs (`record/distillation/naive/`,
D-2026-10-10-a) and the answers of five AIs reading all 2,322 ideas
(`record/distillation/web/alignment_2026-10-10.md`). Each principle carries who first said it and
the row of `record/ideas/timeline.jsonl` that holds the quote. The statements are the model's
wording of those sources; the division into two lists follows the two questions the evidence
answered separately.

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
projection; the same pattern builds values, functions and programs. Source: Luciano, 2022-08-03
(`written:2022-08-03_haskell:subtipos-con-predicado`); named fundamental 2026-09-29
(`record/distillation/2026-10-09_find_principles_v2_claude-code_opus.md`, C3).

**L5. A law characterizes; it does not re-run.** A law states the mathematical property that
determines an operation up to the presentation's equality; a second implementation checked against
the first is consistency, and the native definition is one more model certified against the law.
Source: Luciano, 2026-10-05 ("La idea en realidad es buscar el objeto matematico que mejor lo
represente y decirlo"); extends P10 (the mathematical object that best represents a concept is the
invariant of its type).

**L6. Code is data.** A Luthier program is an element of Luthier; programs build, inspect and run
other programs, and the interpreter is meant to be written in the language it interprets. Source:
Luciano, 2022-06-15 (`written:2022-06-15_sin-titulo-2:codigo-es-dato`).

**L7. The core is minimal and executable by hand.** A handful of well-specified primitives, so
that a program can be run with pencil and paper; everything else is a library whose translation to
the core is mechanical. Source: Luciano, 2026-05-29 ("Luthier tendría que ser ejecutable a mano").

**L8. Declare, then define, then inhabit.** A declaration without a body is a first-class hole: at
once axiom, program input, external function, pending definition and dead code; nothing executes
until it is defined, and no value inhabits an undefined type. Source: Luciano, 2026-05-29
(`dialogue:20260529T1400:tipos-no-definidos-y-forward-reference`); the hole named 2026-09-29.

**L9. A program is a DAG and statements commute.** The unit is the definition; dependencies give
the only order there is, and time is reconstructed from them rather than from the text. Source:
Luciano, 2026-05-29 (`note:2026-05-29T14.46.22:contexto-como-dag`); the unordered set of
definitions already in 2023-03-13 (`written:2023-03-13_hacia-luthier`).

**L10. One function, many paths.** A function has many equivalent implementations, each with its
precision, speed, memory and place of execution; equivalence is established first, and the choice
among paths follows expected loss and cost, estimated from a database of measured runs. Source:
Luciano, 2022-06-28 (`written:2022-06-28_luciano-code-style:choose-efficient-path-after-validity`).

**L11. Verification is one operation, exact or statistical.** What can be computed is checked
exactly; what can only be sampled is checked statistically, and the grade of the evidence (proved,
exhaustive, sampled at a level, assumed) travels with the value in a certificate hashed over its
dependency cone. Source: Luciano, 2022-08-03 and 2023-02-22
(`written:2023-02-22_tapp-wish-list:untested-a-tested`).

**L12. Execution is the verification of equivalences.** Luthier first describes the problem and
its equivalences; running is checking them, as mathematics verifies rather than runs, with a
declarative face (types, laws, theories, holes) and an executive face (values, actions). Source:
Luciano, 2026-05-30 ("la matemática no ejecuta ... la ejecución en Luthier sería esa verificación
de equivalencias").

**L13. Forgetting is first-class.** Dependent typing accumulates history, so the language needs
non-invertible forgetful projections; which forgetting is applied defines the language being
spoken. Source: Luciano, 2026-05-29 (`note:2026-05-29T14.52.08:problema-del-olvido`).

**L14. Luthier orchestrates other languages.** Types and laws are native; values may come through
`extern` from Python or any host, declared over what they really receive and return, with
description and verification kept on Luthier's side. Source: Luciano, 2026-05-26
(`note:2026-05-26T12.32.24:lenguaje-no-atado-a-cpp`).

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
