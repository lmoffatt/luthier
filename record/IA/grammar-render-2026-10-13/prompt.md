# Chapter 2's grammar generated from `luthierSyntax`: brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Opus 5.5 for Luciano, who gives it
to Codex working in this repository (step 1.1.e of `record/plan-from-zero-2026-10-13-execution.md`;
Z9, D-2026-10-13-r; R6 of round 2: the chapter's EBNF is to be generated from the value).

## The prompt

Read `CLAUDE.md` first: its working rules bind you too. In this repository, `luthierSyntax` in
`src/luthier/lib/grammar.lth` is the grammar of Luthier, a value of the type `Ebnf` of
`src/luthier/lib/ebnf.lth`; `src/luthier/ebnf.py` reads it into Python (`luthier_syntax()`, right-hand
sides as tuples, documented there). Chapter 2 of the specification, `docs/spec/02-grammar.md`,
explains the grammar, and today its EBNF blocks drift from the value. Make the chapter carry the
grammar generated from the value, and a check that it is current.

Write exactly these files, and touch nothing else except as said in 3:

1. `scripts/render_grammar.py`, standard library only, importing `luthier.ebnf`:
   - renders `luthierSyntax` as EBNF in the chapter's notation (2.S1's paragraph at the top of the
     chapter): one production per nonterminal, `name ::= ...`, in the order of the value; `|`
     between alternatives; `[ ]` for `opt`; `{ }` for `rep`; `( )` where grouping is needed;
     literals in double quotes; the literal `"\n"` written as `newline`; categories as their bare
     names (`name`, `number`, `string`); continuation lines indented, no line over 100 characters;
   - `--write` replaces the text between the lines `<!-- luthierSyntax: begin -->` and
     `<!-- luthierSyntax: end -->` in `docs/spec/02-grammar.md` with: one line saying the block is
     generated from `src/luthier/lib/grammar.lth` by `scripts/render_grammar.py`, with the sha256
     of `grammar.lth`'s bytes; then the productions in an indented code block (four spaces, as the
     chapter's other blocks);
   - `--check` exits 1 and says why if the block is missing or differs from what `--write` would
     write, 0 otherwise.
2. `tests/test_render_grammar.py`: (a) a reader of the rendered notation back into the tuples of
   `luthier.ebnf`, and the test that reading the rendering gives `luthierSyntax` exactly, rule by
   rule; (b) the test that `--check` passes on the repository; (c) `--write` on a copy of the
   chapter is idempotent.
3. In `docs/spec/02-grammar.md`, insert the two marker lines, with the generated block between
   them, right after the first paragraph of item 2.S9 (the one that says `luthierSyntax` is the
   grammar), and nothing else: the old EBNF blocks and the prose stay; the session rewrites them.

Rules: Python 3.11; run `python3 -m pytest tests/test_render_grammar.py tests/test_ebnf.py -q` and
`python3 scripts/check_spec.py` until they pass. Do not edit `ebnf.py`, the `.lth` files, other
chapters, `record/` (except your report below) or anything ChatGPT is writing (`src/luthier/surface.py`,
`parse.py`, `cli.py`, `tests/test_parse.py`, `pyproject.toml`). Do not commit: leave the changes in
the working tree. Write your report, in English and in a few lines, to
`record/IA/grammar-render-2026-10-13/codex.md`: what you did, what passed, and any place where the
notation could not render the value faithfully.
