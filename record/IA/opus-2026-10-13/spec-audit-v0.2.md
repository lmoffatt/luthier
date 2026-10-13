# Audit of chapters 2 to 4 for v0.2's status flips: brief for an Opus subagent

Written 2026-10-13 by Claude Fable 5.1 (the coordinating session) for a Claude Opus 5.5 subagent.
Read only: you write exactly one file, `record/IA/opus-2026-10-13/spec-audit-v0.2-report.md`, and
commit it alone (`git add` that path; never `-A` or `.`; message ending with
"Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"). Other agents edit the tree meanwhile.

Read `CLAUDE.md`, `record/plan/luthier-from-zero/plan-from-zero-2026-10-13-execution.md` (step 4.4,
the criteria of `v0.2`, criterion e in particular), `scripts/check_spec.py` (what a status means and
what it checks), and `docs/spec/02-grammar.md`, `03-kernel.md`, `04-static-semantics.md`. Today
`[implemented]` on an item means "in `v0.1-final`", the retired interpreter; at `v0.2` it must mean
"the new specimens run it": `src/luthier/parse.py`, `elaborate.py`, `kernel.py`, `check.py`, their
theories in `src/luthier/lib/` and the programs of `tests/spec/` (`tests/test_spec.py` says which
get their verdict and which are xfails with reasons) and `tests/eval/`. For every item of the three
chapters, one row: item; status now; what the new specimens do with it (a program of `tests/spec/`
or `tests/eval/`, a test in `tests/`, a law in a theory, or nothing); the status it should carry at
`v0.2` (`[implemented]`, `[decided D-...]`, `[proposed]`) with the evidence; and whether its text
says something now false (name the sentence). Then a list of the sentences to change, grouped by
chapter, and the items whose programs are missing (a rule `[implemented]` needs an accept and a
reject program). Do not edit the chapters: the coordinator applies the flips at `v0.2`.
