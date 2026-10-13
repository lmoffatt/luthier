# Applying the audit's flips to chapters 2 to 4: brief for a Sonnet agent

Written 2026-10-14 by the coordinating session (luthier-1b), on the audit
`record/IA/opus-2026-10-13/spec-audit-v0.2-report.md` (342b757), for v0.2's criterion e.

## The prompt

Read `CLAUDE.md` first, then the audit report whole, then `scripts/check_spec.py` (what a status
means, what it lints: run `python3 scripts/check_spec.py` before every commit, it must print
nothing). You may change only `docs/spec/02-grammar.md`, `03-kernel.md`, `04-static-semantics.md`
and `00-index.md` (its legend, if it says `[implemented]` means `v0.1-final`); other agents edit
code and theories meanwhile.

Apply, item by item, what the audit supports with evidence: (1) the status each item should carry
at `v0.2` (`[implemented]` now means "the new specimens run it": `parse.py`, `elaborate.py`,
`kernel.py`, `check.py`, `run.py`, their theories and the programs of `tests/spec/`, `tests/eval/`,
`tests/run/`); (2) the sentences the audit names as false about the tooling today (a parser that
"still reads gen", a `session` command that does not exist, `syntax.py`, `checker.py`,
`program.lut`, `z7ring.lut`, "none yet", "not written"): rewrite each to what is true at the
commit you work on, in the item's own voice, citing the file or test that makes it true, or
delete the clause if nothing replaces it. Do NOT change the content of a rule or a decision: the
audit's finding 4 (3.R1 and 3.R2 against D-2026-10-13-x) is a question for Luciano, leave the text
and add nothing; 2.S18 (sessions) and `run --set`, `run --checked` keep their statements with the
status the evidence gives (`[decided D-...]` or `[proposed]`), not a deletion. Where the audit says
a program is missing for an `[implemented]` rule, the rule goes to `[decided ...]` with the
decision it cites, or stays `[implemented]` only if `tests/test_spec.py` gives it a verdict; say
which in the commit. Keep every `Files:` line true (a program named must exist in `tests/spec/`).
One commit per chapter (`git add` the file; never `-A` or `.`; messages naming the items,
ending with "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"). Report in your final
message: per chapter, the items flipped with their new status, the sentences rewritten, and the
audit's findings you did not apply and why.
