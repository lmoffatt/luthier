# Fix what the random trees found: brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Opus 5.5 for Luciano, who gives it
to Codex in this repository, after its report `codex.md` in this folder.

## The prompt

Read `CLAUDE.md` first. Another session writes `src/luthier/lib/term.lth` and `term_model.lut`:
do not touch `src/luthier/lib/`, `docs/`, `tests/spec/*.lut`, or `record/` (except your report).

Your three failure families, read against `src/luthier/lib/grammar.lth` (amended at 03f98ba):

1. Signed term and pattern literals: not trees a text gives. `intLit` takes a `Nat` and `floatLit`
   a `NonNegativeFloat`, so `IntLit(-1)`, `FloatLit(-0.5)` and a negative `PLit` are outside the
   types `wf` is stated over. Fix the generator in `tests/test_roundtrip_trees.py` to draw only
   values of those types. Then `-0.0`: it is a `NonNegativeFloat` and equals `0.0`, so the printer
   writes it as `0.0` (the comment above `NonNegativeFloat`); fix the printer in
   `src/luthier/parse.py`.
2. A datum beginning with `-` or `<` on the line after an act joined that act: a parser defect. A
   token at column 0 outside brackets starts an act whatever it is; continuation by an operator is
   inside braces only (the layout comment above `luthierSyntax`, the new law
   `ColumnZeroStartsAct`). Fix the layout in `src/luthier/parse.py` and transcribe the law into
   `tests/test_parse.py` as `test_column_zero_starts_act`.

Then remove the strict xfails of `tests/test_roundtrip_trees.py` that these fixes clear. If any
failure remains, keep it as a strict xfail and report it as before.

Check: `python3 -m pytest tests/ -q` passes whole; `python3 scripts/check_spec.py` and
`python3 scripts/render_grammar.py --check` pass; `luthier parse src/luthier/lib/*.lth
src/luthier/lib/*.lut` parses. Do not commit. Report in a few lines to `codex-2.md` in this folder:
what changed, the counts, any failing tree left with its text.
