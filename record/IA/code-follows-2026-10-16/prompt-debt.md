# Brief: what the spec decides and the code does not do yet

Read `CLAUDE.md` first, then `record/plan/code-follows-principles-2026-10-16.md` (why this exists).

Task, read only except for your report: for every clause of `docs/spec/*.md` whose status is
`[decided ...]` or `[proposed]` (about 123), classify it in one of three:
- implemented in fact: name the file and line in `src/luthier/` (Python or `lib/*.lth`/`*.lut`) or
  the test in `tests/` that shows it;
- postponed: name the decision that postpones it (`record/decisions.md`, e.g. D-2026-10-14-c, Boolean
  first) or the comment in a theory that leaves it as a hole (search `src/luthier/lib/*.lth` for
  "hole" and for the clause's id);
- pending: decided, nothing implements it, nothing postpones it.
Also list every comment in `src/luthier/lib/*.lth` and `src/luthier/*.py` that names a spec clause
as left out, a hole or later, with its line.

Be cheap: grep for each clause's id and its key words before reading; read a code region only to
confirm. Do not edit the spec or the code.

Output `record/IA/code-follows-2026-10-16/report-debt.md`: one table per chapter (clause, class,
evidence, one line each), then the list of holes, then counts per class. Write it with a shell
heredoc and commit it alone (two-line message ending with "Co-Authored-By: Claude Sonnet 5.5
<noreply@anthropic.com>").
Accepted when: every `[decided]` and `[proposed]` clause appears once with a class and evidence; the
counts add up to the number of such clauses (`grep -c` it and say the number).
