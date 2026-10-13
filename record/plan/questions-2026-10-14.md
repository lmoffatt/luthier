# Two questions for Luciano, 2026-10-14 morning

Written by Claude Fable 5.1 (luthier-1b, the coordinator) at his request, before he travels.
Each takes "ok" (the recommendation) or the alternative; his answer goes to `record/decisions.md`
as D-2026-10-14-a and -b. The rest of the night's questions are in
`record/plan/night-2026-10-13.md`, "Questions".

## Q1. Functions across the bridge (unblocks the fit, `experiment_zero.lut`)

What the fit needs and spec 3.S23 does not state (3.S23 covers only a lambda over `Fin n`
materialized as an array; sonolocalizacion-09's list, with lines, in
`record/IA/sonolocalizacion-inventory-2026-10-13/answers-2-2026-10-14.md`, item 2):
- (a) Luthier lambdas over `VecOf n` passed to `lm.maximize` and called back from Python, up to
  500 times each (`Maximizer`, belief.lut:122);
- (b) a record whose fields are functions, read by attribute in Python (`Objective`,
  optimization.lut:16, read in lm.py:33-61);
- (c) a Python function returned as a Luthier value (a partial, `sampleFull`,
  distances_python.lut:29) and an extern of six parameters applied to four (currying).

Recommended: admit the three as an extension of 3.S23: a callback crossing whose calls are
counted and recorded in the run's record (P2, 12.S18); a record of functions crossing as the
record with each function a callback; a host function crossing in as an opaque value, applicable
only through the bridge, never reduced by the kernel; a partial application of an extern allowed
with the arity from its declared type (run.py already reads the arity so, dacda49). Cost: a
spec paragraph in 3.S23 (or 3.S41), a law in world.lth or term.lth for the callback, one run.py
bite. Touches L11 (the bridge) in the direction of more crossing; assumes the host keeps no
reference to a Luthier value beyond the call.

Alternative: forbid (c) and rewrite `sampleFull` on the Luthier side; keep (a) and (b).

Answer (Luciano, 2026-10-14 ~10:20, verbatim): "1--> admitir (suena caro pero necesario de ultima
como control)"

## Q2. 4.R3 read over a library or per file (unblocks a clean checker and the tag v0.2)

4.R3 asks each constructor of a `data` "a law stating its role in some theory". Four cases have
that law in another file, one that imports the defining file: core.lut's `Unit`, `Bool`, `Maybe`,
`List` (roles in kernel_laws.lth through kernel_models.lut, as D-2026-10-13-t put them) and
laws.lth's `Coverage` (roles in test.lth). The checker reads one file at a time, so they are
refused; everything else of the 30 theory, model and example files is clean.

Recommended: 4.R3 is read over the library: a file together with the files that import it, so a
role stated by an importer counts; check.py loads the importers it can find (the files of
`src/luthier/lib/` and the file's siblings) when checking a file. Cost: a sentence in 4.R3, the
same in program.lth (a library-level predicate), one check.py bite. Touches P7 (each repository
self-contained: the importers are in the repository) and L2.7 (a definition is a concept: the
concept may be completed by its users). Alternative: repeat the role laws in the defining file
(four short laws in core.lut and laws.lth; no code change), at the cost of saying things twice.

Answer (Luciano, verbatim): "2--> la verdad prefiero que las construcciones tengan su ley en su
archivo. pero es peor repetir cosas. No se puede definir el rol en core, que seria lo correcto?"
The coordinator's reading, taken as the decision: the role stays in the defining file and
nothing is repeated: core.lut claims the theories of kernel_laws.lth for its own data (the
bindings of `Unit`, `Bool`, `Maybe`, `List` move from kernel_models.lut into core.lut), and the
law that gives `Coverage`'s constructors their roles moves from test.lth into laws.lth. 4.R3 and
the checker unchanged.

## Not asked here, already decided by the night as reversible defaults

The tag `v0.2` is yours: with Q2 answered either way, criterion a is met; criterion d still has
the quote lint's old debt (87 lines of `record/decisions.md`), listed in the night plan.
