# The review of layers 0 and 1: seven questions for Luciano

2026-10-13, by Claude Opus 5.5 (the coordinating session), from the summary of the ten replies
written by the session that writes the theories (luthier-03),
`record/IA/layers-0-1-review-2026-10-13/summary.md`. The reviewers found no contradictory laws;
their common verdict is laws true but too weak, and those fixes are the sessions' (under way). These
seven are yours. Each is undone by one commit and carries the recommendation of both sessions.
Mark under each: "ok", "no", or a comment.

## Q1. A block in the kernel is a local definition, not a lambda applied

You accepted (D-2026-10-13-x, Q2) that a block is a lambda applied in the kernel. Claude Opus
showed the cost under dependent types: in `(fn n { body }) 3` the body does not know that `n` is
`3`, so `{ n := 3 ; v : Vec n := ... }` does not type, while a local definition would make `n ≡ 3`
inside the body. Recommended: the kernel gains `Let : String -> Term -> Term -> Term -> Term`
(name, type, value, body), with `n ≡ 3` inside the body, and a block becomes nested `Let`s. Cost:
one constructor and its laws. The surface (`fn`, blocks) does not change.



## Q2. The acts of the kernel, and chapter 3 brought up to the files

3.S29 (D-2026-10-12-ah) lists the kernel's `Act` as declaration, definition, alias and the
directives; `term.lth` has `Declare`, `Define` and `Datum`, since aliases are expanded before
checking and the directives became functions (3.S39, 2.S21). Fable lists more places where chapter
3 lags the files (3.R1, 3.S36's `KernelLaws` and `IfTrue` to `CaseJust`, the string of `Axiom`).
Recommended: `Act` as in `term.lth`, and chapter 3 updated to the files on these points.



## Q3. A `data` with a constructor that has no law of its role is rejected

Chapter 4 says both "each constructor needs a law of its role" and "a `data` with no constructor so
bound is reported". Recommended, by L2.7 (a definition is a concept): reject when any constructor
has no law of its role, as `Color` stays a reject in `tests/spec/` (70b1c26), and report the table
of observers against constructors besides.



## Q4. The universe: `U : U` in version 0

`Law` and `Evidence` live in `U` with constructors over `(A : U)`, and `Typing` states `U : U`.
That holds only without a hierarchy of universes; it is a known inconsistency (Girard's paradox),
harmless for testing, which proves nothing. Recommended: version 0 keeps `U : U`, said in chapter 3
as a known limit; a hierarchy waits for the layer of proofs (3.S11).



## Q5. A theory with a single model becomes a definition

`LawValue`, `Projections` and `Composition` are theories whose laws restate their one model, a
second implementation written as laws, which 4.R10 forbids (laws characterize, they do not
implement). Recommended: make them definitions, and keep as laws only what characterizes them,
such as `holds (both c d) x == (holds c x and holds d x)`.



## Q6. Laws valued in a cost wait for the cost library

`Law` admits only Boolean cases, while 5.S2 decides laws valued in the cost `C`. Recommended: keep
`Law` Boolean until the cost library (step 5 of the plan), and say so in 5.S1; `Law C` then gains a
cost case.



## Q7. Stuck terms: reduction unfolds names, the printer folds them back

3.S15 says a recursive function applied to an argument that does not reduce "stays folded": a name
is unfolded only when that makes progress. Fable: that is a way of presenting stuck terms, not a
definitional equality, and it makes the normal form depend on the specimen, so `Delta` is false of
one host and true of `term_model.lut`. Recommended: retire "stays folded" from 3.S15; reduction
unfolds a defined name in head position; a stuck term is whatever reduction leaves, the same for
every specimen; folding back for display is the printer's.


