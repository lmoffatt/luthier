# certification.lth, Boolean first: the entry and the certificate as values, brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-3e). Luciano, 2026-10-14 evening: "Lo
importante es que Luthier empiece a generar certificados. Y ver que todo funcione como debe
ser." Step 5.1 of `record/plan/luthier-from-zero/plan-from-zero-2026-10-13-execution.md` named
`certification.lth` over a cost `C` and had it wait for a case with costs; D-2026-10-14-c
(`record/decisions.md`, end) says first everything Boolean with the cutoffs as parameters, the
costs later. So: the certificate without costs, extensible to them.

## The prompt

Read `CLAUDE.md` first, then D-2026-10-14-c, `docs/spec/06-certification.md` whole (6.S1 to
6.S16; what is `[decided]` there you state, the cost parts of 6.S5, 6.S11, 6.S15 you leave as a
hole or a parameter `C` with a comment), `docs/spec/07-tests.md` 7.S9, 7.S10, 7.S12, 7.S13, 7.S15,
`docs/spec/12-files-and-tools.md` 12.S11, 12.S16, 12.S17, and the theories this one builds on:
`src/luthier/lib/laws.lth` (§1 verdicts, §3 evidence and coverages), `test.lth` (§1 `TestSpec`,
§2 the run's evidence, §3 grades), `generators.lth` at `Binding`, `Seed`, `Budgets` (what 7.S9
expands), `term.lth` at the canonical form (what the cone's hash covers, 6.S8). Pattern: the
theories named, each law citing its item above it. Nobody else edits `src/luthier/lib/` now
except `test` lines added to model files by another agent: write `src/luthier/lib/certification.lth`
and `certification_model.lut` only, one commit each (`git add` the path; never `-A` or `.`; no
`git stash` or `git checkout`), messages naming the items, ending with "Co-Authored-By: Claude
Opus 5.5 <noreply@anthropic.com>".

State, Boolean, with the cutoffs as parameters (D-2026-10-14-c):
1. `Entry`: the identity of a test's outcome (7.S9: the law, the hash of its cone, the binding
   expanded per parameter, the seed, `n`), what it holds (the evidence of laws.lth, the grade of
   test.lth, the date, the interpreter's revision, the hash of the host code behind each extern
   the cone calls, 6.S8), and its state (passed, failed with its case, not run with its reason,
   stale when the hash differs from the current cone's, 12.S11). Laws: two entries with the same
   identity, seed and `n` have the same outcome (7.S13, determinism); an entry certifies only
   under its binding (7.S9); a stale entry certifies nothing.
2. `Certificate`: the entries of one law, with what the law is certified on (the reach of each
   parameter, 7.S10) and the grade read as the weakest (6.S7: computed, not stored apart); the
   operations of 6.S11 along an identity and of 6.S13 (no evidence for free: an operation never
   raises a grade, L10.9) stated for the Boolean case (the bound a hole or `C`'s zero).
3. `Certified`: what a run requires (7.S15, 12.S17, 6.S14): for each law in the cone of the
   entry, a passed entry whose reach covers what the run gives that law; a cone with an
   uncertified or provisional name is refused, each listed with its state; what the run's
   values are compared against (the holes filled by `--set`, 7.S15).
4. The model (`certification_model.lut`): the store as a value (a list of entries), `identity`,
   `grade`, `stale`, `serves`, written in Luthier over the kernel's types; the hash as an
   extern of the host (`python:luthier.certify.cone_hash`, a route the specimen will give),
   stated with the law 6.S8 reads (a change to the cone, to the host code or to the interpreter
   changes the hash).
Mark `[proposed]` every reading the spec leaves open, with the item above it; where a cost
would enter, leave a hole `C` with the comment "D-2026-10-13-m, after the slice's failures".
Both files must parse (`PYTHONPATH=src python3 -m luthier.cli parse FILE`) and `luthier check`
clean (report what it refuses if not yours). Report in your final message: what is stated,
every `[proposed]`, and what the specimen (`luthier certify`, the tester's store, `run`'s
refusal) must do per law, one line each.
