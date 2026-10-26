# Brief: recognize a law as an instance of a core property by its normal form

Luciano's idea and its working-out are in `record/notes/idea-law-normal-form-2026-10-27.md` (read it
whole): a law written ad hoc (`ReadingSymmetric (t : Tape) (a b : Mark) : Bool := t.reading a b ==
t.reading b a`) is recognized as the core's `Commutative Mark Float64 (structural Float64)
t.reading`, by computing a normal form: the free term algebra, quotiented by the properties the
operations are certified to have, a representative chosen by an order with no meaning, and a
dictionary from normal forms to names. He approved this first, computable part (2026-10-27: "Sí,
lanzalo"), as a notice only.

Build, in a new module `src/luthier/normal.py` with `tests/test_normal.py`:
1. The normal form of a law's body: unfold definitions (δ) and reduce (β) as far as the elaborator
   and kernel already allow (reuse what `canon` and the cone hash do; read certify.py and
   elaborate.py first); compare up to α.
2. Ordering where it is allowed: the two sides of `==` at a structural equality, the arguments of
   `and` and `or`; the arguments of an operation the core claims commutative exactly (never one
   whose commutativity or associativity holds only within a bound: floating-point `+` may have its
   two arguments sorted, never be flattened); flatten only what is claimed associative exactly. The
   order on terms is total and has no meaning (structural, then by name).
3. Variables named canonically by first occurrence in the ordered body, iterated to a fixed point
   (the canonical-labelling problem the note names).
4. Abstraction of the operation: a head applied to the law's variables that is not a variable
   itself (`t.reading`) becomes a pattern variable, so the body reads as the core property's with
   its operation as a parameter (Miller's pattern fragment).
5. The dictionary: the normal forms of the core's properties (src/luthier/lib/core/properties/
   relations.lth, operations.lth, functions.lth, and the structures' laws where they are single
   properties), each with its name and the instantiation of its parameters.
6. A function that, given a law, returns the core properties it is an instance of, with the
   instantiation (`ReadingSymmetric` is `Commutative` at A = Mark, B = Float64, o = structural
   Float64, op = t.reading), or nothing.

Tests: the tape's `ReadingSymmetric` recognized as `Commutative`; a law written with its sides
swapped or its variables renamed recognized the same; a float associativity written ad hoc NOT
recognized as `Associative` (it holds within a bound only); a law that is no core property
recognized as nothing; every core property recognized as itself. Then scan every law of
src/luthier/lib, examples and tests/tester and list in the report each law recognized as a core
property with its instantiation (the homonyms core_metrics missed); claim nothing on the rest.

Last, and only after the agent working on D-2026-10-16-k/-l has committed its report
(record/plan/after-core-2026-10-23/report-queue-kl.md: check `git log` first; it edits check.py),
wire a notice into `luthier check -v`: "L is P at ...", one line per recognized law. No cone, store
or result changes: a notice only. Spec: a [proposed] clause in chapter 4 (static semantics) saying
what the notice does and its limit (it recognizes what the order decides; it claims nothing on the
rest; Richardson's theorem for the elementary functions).

Read CLAUDE.md first. Run with /home/lmoffatt/miniconda3/bin/python (never pyenv's python). Other
agents work in kernel.py and in run.py/check.py: stage by path, never git stash, checkout or reset
others' files. Small commits: subject, blank line, one body line, ending with "Co-Authored-By:
Claude Opus 5.5 <noreply@anthropic.com>". Report: `record/plan/law-normal-form-2026-10-27/report.md`,
committed (if your Write is refused, give its full text in your final message): what you built, the
tests, the scan's list, the limits met, decisions taken on your own, at most one question.
