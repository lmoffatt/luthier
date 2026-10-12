# The specification, wave 1: the decisions

Draft 0, 2026-10-12. Written for Luciano, to answer before the first wave starts. The execution is
`plan-spec-2026-10-12-execution.md`. Settled in chat today and not asked again: Luthier has four
documents and the record (principles, specification, manual, way of working); the specification
is one document in twelve chapters, each rule with its status, describing the language designed
and not only what runs; the rationale folder dissolves into the record once the manual exists;
the chapters go in three waves, and wave 1 is the chapters whose content exists today: 1 terms
and notation, 2 grammar, 3 kernel, 4 static semantics, 7 tests and generators, 11 numbers, 12
files and tools. What comes from a source is cited; the rest is the model's proposal.

Answer with the number and ok, no, or a correction.

**D1. Layout.** A directory `docs/spec/` with one file per chapter, `01-terms.md` to
`12-files-and-tools.md`, and `00-index.md` with the table of contents, the status legend and the
citation form: a rule is cited `spec 4.R3`, a section `spec 8 §2`. The six files of today
(02, 03, 04, 05, 06, 08) are replaced by the new chapters in the same commit that writes each,
git keeping them; the record's drafts table of the principles gains a sibling for the spec,
`record/spec-drafts.md`, one row per chapter with its sources and commits (P2, P3). Alternative:
one file `docs/spec.md`; rejected by the model because twelve sessions would edit one file.

**D2. Status per rule, and the check that closes a chapter.** Every rule and every stated
behaviour carries one of three marks, `[implemented]`, `[decided]` (by a D id, not yet in the
interpreter), `[proposed]` (the model's, awaiting his mark), and a rule carries the names of its
accept and reject programs in `tests/spec/`. `scripts/check_spec_tests.py` (today: the R rules of
05 §5) is extended to every chapter: each rule has a status, each `[implemented]` rule has both
files and they pass, each `[decided]` rule names its D id and it exists, references to principles
(L, G, O ids) and to other chapters resolve, and no sentence of eight words appears in two
chapters. A chapter is done when the check passes on it. This repeats for the spec the mechanism
of D-2026-10-12-o; the real case is the drift between 05 §7 and 08 C2 on the grades.

**D3. Terms are the principles'.** Chapter 1 has the formal notation only (`x : T`, `≡`,
`t[a/x]`, D(n), B(n), the dependency graph, accept/reject) and cites `docs/principles.md` Terms for
every word of the language; it defines nothing twice. Today the §0 of 04, 05, 06, 08 and 09 each
restate the notation.

**D4. The grades in wave 1 are the five of Terms.** Chapter 7 and the mentions in 4 and 12 use
proved, exhaustive, cases, sampled, assumed, with the domain and the evidence cost carrying what
the extra grades of 05 §7 and 08 C2 said: *point* is cases with one case; *census of k* is cases;
*bounded* is exhaustive on the box the domain names; *witnessed* is cases with a witness, since an
existential law's certifier exhibits one. The conversion of a sample to an evidence cost (L10.3)
is stated in chapter 7 as `[decided]` by D-2026-10-12-r with 08 C2's 3/n rule as its first
instance, and its full form waits for chapter 6 (wave 2). This changes the vocabulary the
interpreter prints; the certificate files gain a field and lose none.

**D5. Object.** O7 is taken in chapter 4: `05 §3` reads "theories are cycles", a strongly
connected component of the dependency graph is the presentation of a theory with its models, and
the word *object* survives only in "object classifier" (D-2026-10-12-f left it open). One
commit over chapters 3 and 4.

**D6. Numbers: the rounding correction.** Chapter 11 states L13.3 and L13.4 (rounding is
non-expansive up to an additive defect of about ε|x|; the functor reading stands with
"non-expansive plus an additive term") as `[decided]` if you mark them ok here, `[proposed]`
otherwise; the rest of chapter 11 is 06 as it stands, with the rounding law of 06 §8 as its
worked instance.

**D7. What `run` requires.** Chapter 12 states certification by default (D-2026-10-11-n): `run`
refuses a cone with an uncertified or provisional name unless the demand opts out; the opt-out's
syntax is O3 and stays `[proposed]` in wave 1 with one candidate, a flag `--assume name` that
leaves a certificate of grade assumed for that name, recorded in `.run.json`. Today
`--require-certified` is the exception and the default runs anything; the default inverts.

**D8. Libraries: spec or manual.** The spec specifies what a library file is, how it is imported,
and what travels with it (chapter 12, from 03 §1 to §4). The content of the libraries (`algebra`,
`array`, `probability`, the table of 03 §5) is the manual's, so wave 1 does not describe them and
03 §5 goes to the record's spec-drafts note until the manual exists.

**D9. Who writes wave 1, and the cost.** Chapters 1, 2, 3, 11 and 12 by Sonnet, one agent each,
in parallel, each in its own worktree; chapters 4 and 7 by Opus, since they carry the most rules
and the grade change; the model of this session integrates, runs the check and commits. Each
agent gets a brief that names its sources by commit, what is decided (this document), what it
does not touch (the principles, the interpreter, the other chapters) and the check that closes
it. Alternative: everything by this session's model, serial; slower, no cheaper in attention.

**D10. Out of scope for wave 1, stated so that nobody drifts into it.** The manual (00, 01,
principles-for-readers); the rationale folder (02-que-robar, 07, 09, 10, 11 stay as they are,
cited by the chapters where they are sources); chapters 5, 6, 8, 9, 10; the interpreter, except
the accept/reject programs of rules already implemented, which the check runs and does not
change.
