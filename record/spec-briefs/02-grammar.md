# Brief: chapter 2, Grammar

Read `record/spec-briefs/common.md` and `record/spec-brief-template.md` first.

## Goal

Rewrite `docs/spec/02-grammar.md` in place (the file exists; it is both your source and your
target) as chapter 2 of the specification: the concrete syntax, the acts, the terms, the
translation of every surface form into the kernel, blocks and the session, with a status per
production or group of productions.

## Sources

- `docs/spec/02-grammar.md` at d12b554, whole: lexical, acts, terms, translations, what the
  parser leaves to the checker, dotted names, the additions of 2026-10-05, the open points, blocks.
- `docs/spec/08-tests.md` §12 at d12b554: the test directive becomes
  `"test" name [ "with" number | "exhaustive" ] [ "sampled" metric ] [ "size" number ] [ "under" name ] [ "where" "{" binding { "," binding } "}" ]`,
  `profile name := "{" binding { "," binding } "}"` is a new act, the act `gen` is removed. These
  were decided by Luciano on 2026-10-06 but have no decision id in `record/decisions.md`: write
  them `[proposed]` and list them in your report under "decided without an id".
- `docs/spec/04-kernel.md` §5 for the table of translations (take it; chapter 3 will cite
  `spec 2` for it, so the table lives here and not in 3).
- `src/luthier/parser.py` and `src/luthier/lexer.py` (read only) to decide which productions are
  `[implemented]`.

## What changes against the source

- Every production group is a statement `**2.Sk. Title.** [status]` followed by its EBNF block.
  Group by the sections of the source (lexical, acts, terms, translations, dotted names, blocks).
- `gen` removed from the reserved words and the directives; `profile` and the extended `test`
  added, `[proposed]` as said above.
- `Term` and `Program` as data (D-2026-10-12-x): add a statement for the quote and unquote forms
  with one candidate syntax, `quote { t }` and `eval A t`, marked `[proposed]`; say that the data
  type `Term` itself is `spec 3`. The saved evaluation of §8 stays open, cited as `spec 8`.
- The session (§8, §9): keep the grammar of blocks here; the semantics of the session (memo,
  what a line re-evaluates) is `spec 8`, cite it.
- Decisions the source cites by id (D-2026-10-11-b, -c, -i, -j, -k, -f): keep them as
  `[decided D-...]` where the parser does not implement them yet, `[implemented]` where it does.
- The open points of §8 become citations of O ids where one exists (the session: O8) and a
  "decided without an id" or `[proposed]` item otherwise; `## Open` last.

## Length

The source is about 2100 words; the chapter should be about the same. Do not shorten the EBNF.
