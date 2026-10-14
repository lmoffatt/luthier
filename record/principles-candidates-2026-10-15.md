# Candidates for the principles from the sessions of 2026-10-13 to 15

Written 2026-10-15 by a fork of the coordinating session (luthier-5d, Claude Fable 5.1), on
Luciano's request: "revisar si de las nuevas directivas o insights hay cosas que no estén en
los principles y que deberían estar". Read against `docs/principles.md` (G0 to G2, L1 to L14,
What is open) and `record/principles.md` (P1 to P16). What each item proposes is marked; his
words are quoted from the chat of the coordinating session (transcript a5ea3059; the lines
unknown until the export, as in D-2026-10-14-c). The night's decisions are D-2026-10-14-a, -b,
-c in `record/decisions.md`.

## One screen

Four clauses worth adding, one note for O1, three tensions to name; nothing that needs a new
principle. In order of what they would have guided tonight:

1. **A definition and the law of its role live in one file, and nothing is said twice.** Not in
   the principles; it guided D-2026-10-14-b. A clause of L2, his words.
2. **The conceptual is the practical at another level; a missing law is a finding.** L2.7 has
   "everything has laws; it is a matter of finding them"; what is new is why, and its consequence
   for a review. A sentence in L2.7 (his words) and a clause under P13.
3. **A cutoff below what the realization resolves buys nothing.** His intuition on the fit's
   tolerance, confirmed (1e-12 and 1e-6 agree to 4e-7 m); the evidence's finding on `PinvScales`
   (a flat tolerance against a condition number) is the same thing. A clause of L13.
4. **What crosses the bridge is recorded; a host value Luthier cannot reduce is opaque.** It
   guided D-2026-10-14-a ("necesario de última como control"). A clause of L11.
5. **Note for O1.** D-2026-10-14-c is O1's Boolean interim stated by him, with one addition: the
   cutoff parameters are where the cost will enter.

Tensions, not candidates: P2 against P8 in the certificate's identity (the interpreter by its
tag, not by every commit) and in the run records (ignored by git); L14.6's "the theory is
refined" against who refines it (its author, never the specimen's writer: a working rule).

## The candidates

### C1. Locality without repetition (a clause of L2, after L2.7)

His words (2026-10-14, on Q2 of `record/plan/questions-2026-10-14.md`): "la verdad prefiero que
las construcciones tengan su ley en su archivo. pero es peor repetir cosas. No se puede definir
el rol en core, que sería lo correcto?"

What exists: L2.6 (a theory file holds types, declarations and laws; a model lives in its own
file; a theory file never holds a model of a theory declared elsewhere), L2.7 (a `data` with no
law of its constructors' roles is a collection), spec 4.R3 ("a law stating its role in some
theory"). None says where the role law lives, and 4.R3's "some theory" let the roles of core's
data sit in kernel_laws.lth and `Coverage`'s in test.lth, which the checker, reading one file,
refused.

Proposed clause, L2.8 (his words, the wording the model's): A definition and the law of its role
live in one file, the one that defines it, so that the file is the concept whole; and nothing
is said twice: where the role is a theory stated elsewhere, the defining file claims that
theory's model (core.lut claims `Unit`, `Bool`, `Maybe`, `List` as models of kernel_laws.lth's
theories) rather than restating the law. Locality yields to non-repetition. (D-2026-10-14-b.)

What it would have guided: the four refusals of 4.R3 on core.lut and laws.lth, the question Q2,
and the choice between a library-level 4.R3 and restating the roles. Cost: one clause.

### C2. The conceptual is the practical at another level (L2.7, and a clause under P13)

His words (2026-10-15, on the proposed review experiment): "otro peligro es que el estudio
degrade los principles porque van a tender a no buscar leyes en todos lados sino en ser
prácticos y la idea es ser conceptuales (que es ser prácticos a otro nivel)".

What exists: L2.7 ("Everything has laws; it is a matter of finding them ... It costs thought,
and that is its purpose"); P13 (a principle is worth the decisions it guides); P15 (adherence
must be cheap to compute).

What is new: the justification, and a consequence for how work is judged. The law found by
thought pays when it bites, not when it is read; so a judgment that weighs a finding by its
immediate use will always prefer the practical and will erode the search for laws. The night's
instance: the fit's "bad smell" was answered by stating the relation between the information
and the Hessian of the score, a law the theory could have stated and had not (belief.lth has
`PosteriorScoreIsGradient`, `PosteriorInfoSymmetric`, and no `InfoIsTheHessian`); the practical
question found the missing law.

Proposed: a sentence added to L2.7, his words: "To be conceptual is to be practical at another
level: the law pays when it bites, not when it is read." And a clause under P13 (the record,
terse): a review under the principles counts the laws that could have been stated and were not
as a class of finding of its own, apart from defects; a judge of findings classifies and
attributes, and does not rank a missing law below a bug, since the ranking is Luciano's (P1,
P12).

Cost: a sentence and a clause; the review experiment, if run, gets its judge's consigna from it.

### C3. A cutoff below the realization's resolution buys nothing (a clause of L13)

His words (2026-10-15, on the fit's iterations): "capaz que estamos usando un target demasiado
fino? reducir la última sección puede ser difícil". Confirmed: at tol 1e-6 the fit stops at 35
iterations and sigma agrees with tol 1e-12 to 4e-7 m (`record/IA/fit-convergence-2026-10-15/`).
The same thing from the evidence (`record/IA/evidence-2026-10-14/report.md`): `PinvProjects`,
`PinvSymmetric`, `PinvScales` refuted on Hilbert 5 by rounding of order cond × eps against a
flat 1e-12; fixed by scaling the comparison by the magnitudes compared (11.S14).

What exists: L13.1 (the realization's laws hold within a stated tolerance), L13.3 (rounding's
additive defect of about ε|x|, the condition number per input; mark pending), L12.3 (the cutoff
is the demand's), L5.18 (no unrecorded policy constants), 11.S18.

Proposed clause, L13.5: A cutoff is read against the realization's defect at the point where it
is met: a demand's tolerance below what rounding resolves there (ε times the magnitudes
compared, times the condition number where one enters) asks for evidence the computation cannot
give, and the law's comparison carries the scale (11.S14) so that the tolerance the demand
supplies is in the units of what is compared. Below that resolution a stricter cutoff buys
nothing, as the last iterations of a fit at 1e-12 bought nothing at 1e-6. [proposed]

Cost: one clause; it names what the evidence agent did ad hoc on arrays.lth.

### C4. What crosses the bridge is recorded; an opaque host value (a clause of L11)

His words (2026-10-14, Q1): "admitir (suena caro pero necesario de última como control)".

What exists: L11.1 (values through `extern`, description and verification on Luthier's side),
L11.2 (an extern validated at its first action), L4 (the token used once), P2 (everything
derived carries how it was derived), spec 3.S23 as stated at 1e38cb4 and implemented at dda4192.

What is new: three forms of crossing the principles do not name, and the control he asked for.

Proposed clause, L11.8: A function crosses the bridge as a callback: the host calls it through
the bridge, each call crossing by the declared types, and the calls are counted and recorded
with the run (the control: what the host did with Luthier's function is known); a record of
functions crosses by field; a host function given to Luthier is an opaque value, applied only
through the bridge and never reduced by the kernel, so what Luthier knows of it is its declared
type and its laws (L11.2); a partial application of an extern is a value, its arity from its
declared type. (D-2026-10-14-a, world.lth `Crossing`, term.lth `ExternPartialIsValue`,
`HostGivesBackAValue`.) [proposed]

Cost: one clause.

### C5. Note for O1 (no clause)

D-2026-10-14-c, his words: "hagamos primero todo booleano, pero expongamos los parámetros de
tolerancia de corte como variables que luego pide la demanda. La idea es que quizás luego esos
parámetros de corte estén relacionados con el costo." O1 already says the application runs on a
Boolean interim with tol a parameter; D-c is that interim decided by him, with one addition
worth a sentence in O1: the cutoff parameters the Boolean laws take are the hook where the cost
enters when the algebra exists (a cutoff is a cost's threshold, L12.3). Also the exception kept:
a quantifier with no finite Boolean form stays a `Law`, stated and not tested (`SupIsLeast`).

## Tensions to name (for him, not candidates)

- **P2 against P8 in the certificate's identity.** 6.S8 puts the interpreter in the hash; by
  every commit, every store goes stale daily (25 minutes to re-certify); the night read it as the
  last tag (`v0.2`), proposed. P2 wants the exact revision; P8 wants the stores to last. The
  same tension in the run records (`*.run.json`), ignored by git by default: derived, with how
  they were derived, and not kept.
- **Who refines a theory a specimen refutes.** L14.6: a specimen that shows the theory wrong is
  evidence and the theory is refined. The night's rule: by its author, never by the specimen's
  writer, who reports. A working rule (CLAUDE.md), not a clause; but the night applied it some
  ten times and it kept P1 discernible under agents.
- **The reversible default in his absence** (P5, P6, P9, P16 together): a decision that is his
  and blocks a step takes the reading one commit undoes, marked `[proposed]`, listed for him.
  Applied about forty times in two nights; worth a count under P13, not a clause.
