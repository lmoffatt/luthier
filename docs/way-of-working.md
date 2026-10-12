# The way of working on Luthier

Split from `docs/principles.md` (draft 8, bcdac41) on 2026-10-12 at Luciano's instruction: the principles of the language and the way of working are two documents (D-2026-10-12-b). The W numbers and statements are those of draft 8, unchanged; each W keeps its source and its draft marks. On 2026-10-12 the citations of organizers and principles were moved to draft 11 of `docs/principles.md` (G0, G1 theory and model, G2 cost; L1 to L13; the Numbering table there maps the old tags), the statements untouched, and W15's order of precedence replaced by the one D-2026-10-12-s settled. The record of the working method, its plan and his bites are `record/working-method.md` and `record/plan-working-method-*.md`; decisions cite a W by number and its statement is here.

Unchanged from draft 1 except W5, restated.

**W1. The specification comes before the implementation.** Syntax and semantics are fixed on paper
first, and the implementation passes the specification instead of silently defining the language.
(Draft 3) The implementation may return a counterexample to the specification, a program it
accepts and nothing can run, or two rules that cannot both hold; the specification then changes by
a recorded decision, never silently (W9 is what the implementation does meanwhile). Source:
Luciano, 2026-06-03 (`day:2026-06-03:primero-sintaxis-y-semantica-despues-implementar`).

**W2. No rule enters without a worked example.** Each principle is tried by hand in the candidate
notation before it enters, and each rule of the specification is written as accept/reject pairs,
so the specification is an executable suite; (draft 6) a pair over a law into `Cost` carries its
parameters (tolerance, level, seed, distribution) as the test does (`08`), so the suite stays
Boolean at a declared tolerance. (Draft 3) "El ejercicio clears the mind": a worked
example shows contradictions that are not obvious. Source: the model from Luciano's audios,
2026-08-31
(`dialogue:e6fc53cf:disciplina-ejemplo-en-papel`); the pairs 2026-10-04
(`dialogue:52d3e68e:short-cascade-with-pilot-spec-as-tests`).

**W4. The real application drives the growth.** Luthier must take root in something useful
(sonolocalización) and grow only where the application finds something it cannot express; kernel
work without real pressure moves the specification for nothing. (Draft 3) The motor of growth; W3
is its brake. Source: Luciano, 2026-09-21
(`day:2026-09-21:luthier-tiene-que-ser-util`).

**W3. Start minimal and add only what is used.** Begin from zero with the indispensable, do each
step in detail before scaling, and reduce until removing more would break something needed. (Draft
3) Its job is to stop the proliferation of abstractions; a brake, not a motor, and in his words
not often invoked. The order of work, not a limit on the language (every path expressible is L6's own clause). Source: Luciano, 2026-10-02
(`dialogue:51cca364:empezar-de-cero-con-luthier-liviano`).

**W5. Concepts live in Luthier, execution in the host; native against extern is bootstrapping.**
The `.lut` is designed before the Python; each concept is written native (slow, conceptual) and
extern (fast, pragmatic) with the test that they agree, and work has gone astray whenever something
that belongs in Luthier sits in Python. Restated (D-2026-10-11-d, G1): the native definition is
not an oracle, since "agrees with the native" would be a law that copies an implementation; it is
one more specimen (L9), the agreement test is a consistency check between specimens, (draft 4) which
is the identity
law of L6.11 that admits the second specimen into the planner's graph (D-2026-10-11-m), and the
practice holds while a function has too few laws to be known by description. Source: Luciano,
2026-09-30.

**W6. A test must fail when the thing is wrong.** Laws are written before the algorithm; a law not
known to be true is worse than a hole, (draft 5, proposed) that is, one asserted without a grade,
since a law with grade `assumed` visible is a hole that says so; negative controls and reproduced
numbers, never passing
examples alone, are what make a test diagnostic. (Draft 3, his words) A meta-test that must always
exist: the test must fail where it must fail, not only pass where it must pass; realized today by
negative controls on the input and, to implement (D-2026-10-11-h), by mutation of the
implementation: a law that no mutation fails is not diagnostic; (draft 5) mutation cannot tell a
law transcribed from the implementation from a description, since every mutation fails the
transcription; what tells them apart is that a law is stated over the theory's signature and
cannot transcribe a model's code (G1). For G1. Source: Luciano, 2025-09-27
(snapshots
before tests); the control stated 2026-10-02 (`dialogue:51cca364:a-test-needs-a-negative-control`).

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
first; a count says nothing. For P12 (Luciano's attention is the scarce resource); (draft 3) in his
words, "muy importante para la interacción con la IA". Source: Luciano, 2026-09-30
(`dialogue:ac750929:answers-at-concept-level`).

**W13. The foundations are rethought, the reasonable version first.** The language has been remade
many times (quimulun, tapp, macror, Luthier), each time deeper; the method is to work out the
reasonable version and then look for the wild one. G0 is the reasonable version; G1 and G2 the
wild one. (Draft 3, his words) This is the meta-method: it destabilizes the system and makes it
grow, and the art is not to destabilize it before its time. Source: Luciano, 2022-06-15
(`written:2022-06-15_sin-titulo-2:rehacer-desde-las-bases`)
and 2026-05-26 (`day:2026-05-26:razonar-primero-despues-la-locura`).

**W14. What reaches Luciano has few, rich concepts.** A synthesis can be judged because it has few
concepts; a long text with ideas he does not fully handle makes him doubt everything, and that is
what to avoid. For P12 (Luciano's attention is the scarce resource), as a criterion for what the
model brings him. (Draft 3, his annotation) His engagement is served when his cognition goes to the
strategic direction of the project, optimal by these principles; so adherence to them must be
cheap to compute (P15, proposed in his words, `record/principles.md`). Source: Luciano, 2026-10-09
(`WhatsApp Ptt 2026-10-09 at 10.43.06.md`, 04:24 to 05:06); the annotation of 2026-10-11.

**W15. A long analysis is reported as such.** (Draft 3, new, D-2026-10-11-g.) When an analysis
revisits the same decision twice without new evidence, or exceeds what one screen can carry, the
session stops and reports which it is: a delicate question, or a conflict between principles,
naming them; either goes to Luciano as one question (P12), and the second is the signal that a
principle is missing or two must be ordered (P4, P13). (Draft 6, proposed; settled by D-2026-10-12-s on 2026-10-12) The
order is the precedence of `docs/principles.md`: a statement decides over its clauses, the organizer
decides between the principles under it, G0 decides between organizers; inside an organizer the
conflict goes to him.
Source: Luciano, 2026-10-11 (annotation on
W14: "deadlocks ... legitimos ... o ilegitimos: hay una contradiccion entre los principios"; reply:
"agree"); the trigger is the model's.
