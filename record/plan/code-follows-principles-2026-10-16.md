# The code follows the principles: execution, 2026-10-16

Why (chat of 2026-10-16): L10.5 (a certificate serves every demand it meets) is settled and 6.S15 is
`[decided]`, yet the code matches the tolerance exactly. Not a lack of emphasis: D-2026-10-14-c
(Boolean first) postponed the cost part, the coordinator's brief told the theory's agent to leave it
as a hole, and the postponement was written only in a comment (certification.lth 267). The spec kept
saying `[decided]`; nothing lists what is decided and not implemented (114 clauses of the spec).

Rules adopted (coordinator's, each undone by one commit):
- A postponement is written in the clause it postpones (spec status, principles clause), not only in
  a comment of the code.
- Before reasoning a design question, search the principles record, the spec and the decisions.

Status: 2026-10-16, step 0 done (e6eb343, b27dae8, 805daff); step 1 done (b9705b0: 131 clauses, 60 implemented, 44 postponed, 27 pending); step 3a done (5f2b87d..812bc15; v0.4 criterion c met, verified by the coordinator); step 2 done (6c08c32..97ff0dd: check_spec counts 181 implemented, 81 decided of which 33 suspended, 8 proposed; 42 raised to implemented with evidence, 33 suspended, 11 postponements in text); step 3b running. For the next spec-touching bite: 12.S17's last sentence ("refuses only under --require-certified") and 10.S7's "until a world library exists nothing checks it" are stale.

## Step 0. His decisions of 2026-10-15/16 into the principles (agent, Sonnet)
D-2026-10-16-b: L2.8, L2.7's sentence, L13.5, L11.8, O1's note, L10.5 marked suspended in the Boolean
slice, L5.6's citation; P11's reading (item 22) as a sentence in L5.18. Brief:
`record/IA/code-follows-2026-10-16/prompt-principles.md`.
Accepted when: `scripts/project_principles.py --check` prints ok after `--write`; each clause cites
its decision; the record and the projection are committed apart.

## Step 1. The debt made visible (agent, Sonnet, read only but for its report)
Every `[decided]` and `[proposed]` clause of `docs/spec/` classified: implemented in fact (where),
postponed (by which decision, to when), or pending; the holes the theories mark (comments naming a
spec clause left as a hole). Brief: `record/IA/code-follows-2026-10-16/prompt-debt.md`.
Accepted when: every such clause has one class with its evidence (a file and line, or a decision id);
the report is committed.

## Step 2. The spec says what the code does
From step 1: the clauses implemented in fact get `[implemented]`; the postponed ones get their
postponement in the status (a format for `check_spec.py`, e.g. `[decided D-x; suspended by D-y]`);
`check_spec.py` prints the count of decided-not-implemented as information.
Accepted when: `check_spec.py` exits 0 and its information line gives the debt.

## Step 3. Code bites from the decisions of 2026-10-15/16 (agent, Opus, one at a time)
a. D-2026-10-15-d (item 1): each run records the hash of every store it read; the hole marked in
   certification.lth; only pure results served (v0.4's criterion c at its smallest).
b. D-2026-10-16-b (item 7): `certify` writes an entry only in the store of the claiming file; the
   copies beside test programs dropped.
c. D-2026-10-15-f, -g (items 3, 4): an agreeing replay absorbed, a disagreeing one kept and the law
   refused; a not-run for lack of fuel never memoized.
d. D-2026-10-15-h (item 5): `x.run.json` carries the hash of the whole key (seed included); the law
   relating record and key in demand.lth / plan.lth.
e. D-2026-10-15-e (item 2): the cone's hash erases binder annotations, with the law that erasure
   leaves the term's behavior unchanged; one re-certification wave; then the elaborator's fix at the
   source (a projection typed everywhere).
Each accepted when: the suite is green, the named law or test exists and a control refutes a wrong
version (L9.14), and the stores touched are committed with the code.

f. D-2026-10-16-c and -d (one agent, run.py and cli.py): a provisional extern refused by default in
   world.lth as in run, run as assumed only when the demand names it (`--accept assumed:NAME`), a
   warning on stderr per application, `provisional` with its reason, `check -v` lists them; the
   modes of running as fields of `Demand` with declared defaults: strategy (forward on demand the
   default, call by need the specimen under `TheDefaultsAgree`), fuel unbounded by default for run
   with an optional bound in steps or time, `fresh`. Brief: prompt-modes.md.
f'. 3f landed (cc883f1..749e0e4; 755 passed). The coordinator's choices: the 90 s past-the-bound
   test behind LUTHIER_SLOW with a cheap one in its place (asked of the same agent); 6.S14's sentence
   given to the 3i agent, which holds chapter 6.
g. D-2026-10-16-e (after f; renames many files): executive files `.run.lut` and `.test.lut`; the
   checker's refusals; run and certify take only their kind; the migration of tests/tester and the
   two mixed sonolocalización files. Principles text (L2.6, L5.1) by a separate agent, launched.
Order: 3b's follow-up (done, 741 passed, verified), then f and 3c together (launched), then g, then 3e.

h. D-2026-10-16-h: tables.py returns the host's `Just` or nothing at a `Maybe` (item 14), the
   table cones re-certified; no cutoff accepts a failure, running past one names it
   (`--accept assumed:LAW`, item 16); records of `.run.lut` under examples/ tracked, under tests/
   ignored (item 8, after g).
c'. 3c landed (af07d24..3a364a2). Its question answered by the coordinator (one commit undoes it):
   a failure in a disagreement keeps refusing until resolved by hand with its reason recorded (P2),
   two later passes do not erase a counterexample (D-2026-10-15-f); a resolving command later.
   `luthier certify` of certification_laws.lut and certification_controls.lut waits for 3f.
i. D-2026-10-16-g: (launched after 3c) a law's samples pooled across seeds, each stretch keeping its seed; a statistical
   law continues one sequential test (certify.py, tester.py; after 3c).
j. D-2026-10-16-i: evidence kept per binding and per labelled region with its n and bound; the
   demand combines grades, weakest by default (5.S8); special values and atoms in the generators,
   `classify`/`cover` (7.S14); certification.lth's grade rules rewritten (a theory: Fable); a
   principles clause on null sets [proposed], its sentence written by the coordinator in the brief.
   Refined by D-2026-10-16-j: the regions that enter a grade come only from three finite sources,
   the type (its theory declares its degenerate cases once), the law (each cutoff's two sides, each
   premise's boundary) and the code (each branch of the cone: branch coverage); an author's label is
   informative and enters no grade.
v0.4: D-2026-10-16-f, tag when (c) is met with (e) as debt. (c) verified by the coordinator at
1922758 (741 passed); 3470c54 adds only record files. The tag is his.

## Step 4. The first cost (v0.5)
`PinvProjects` returns its distance; the certificate records it; a demand is served by
`distance <= tolerance` (L10.5, 6.S15 for that law); the pattern written for the other laws.
Accepted when: one certificate serves demands at 1e-6 and 1e-8 without re-testing, and refuses one
below the recorded distance.

Waiting on him: item 41 (a law's evidence pooled across seeds) and the rest of the pending list.
