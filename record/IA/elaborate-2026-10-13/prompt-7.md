# A chained projection on a parenthesised expression does not reduce, brief for a Sonnet agent

Written 2026-10-14 by the coordinating session (luthier-3e). On the evidence report
(`record/IA/evidence-2026-10-14/report.md`, "Findings"): `MaximizerKeepsDimension` is
unevaluable because `(e).x.n == n` stays as `((== (record).x.n) 30)` even on a literal record,
while `r := e; v := r.x; v.n` reduces: a chained projection on a parenthesised expression is
read as one label `x.n`, or not elaborated as two projections.

## The prompt

Read `CLAUDE.md` first, then that finding, `docs/spec/02-grammar.md` 2.S14 (projection, the
dotted name), `src/luthier/lib/grammar.lth` at `ProjectionTree` and the `proj` production,
`translation.lth` at `Records` (what `m.f` and `e.f` translate to), `src/luthier/parse.py` at the
postfix projection and `_print`, `src/luthier/elaborate.py` at `Proj` and dotted names. Other
agents edit `tester.py`, `certify.py`, `cli.py`, `arrays.lth`: touch none; change only
`src/luthier/parse.py`, `src/luthier/elaborate.py`, `tests/test_parse.py`,
`tests/test_elaborate.py`, and one program under `tests/eval/` or `tests/run/`.

Find where `(e).x.n` loses its second projection (the parser reading `.x.n` as a dotted name
after a parenthesis, or the elaborator turning a dotted suffix into one label) and make it two
projections as grammar.lth and translation.lth state; `e.x.n` on a bare name must keep working
as it does; `luthier eval` of `({ x := { n := 3 } }).x.n` gives `3`, and of `(f y).x.n` with `f`
a function returning such a record too. Tests for both in test_parse (the tree) and
test_elaborate (the term), and an eval or run program.

Check: `PYTHONPATH=src python3 -m pytest tests/test_parse.py tests/test_elaborate.py
tests/test_roundtrip_trees.py -q`, then `PYTHONPATH=src python3 -m pytest tests -q`. Do not
commit. Report in your final message.
