# The left of `<-` is a pattern: the parser, brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Fable 5.1 (the coordinating
session), launched by it with `codex exec`.

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time (Codex on `elaborate.py`, on
`check.py`, on `host.py`/`run.py`): change only `src/luthier/surface.py`, `src/luthier/parse.py`,
`tests/test_parse.py`, `tests/test_roundtrip_trees.py`, and write your report; a failure from
another file is someone else's, report it, do not fix it.

Luciano decided (D-2026-10-13-ag in `record/decisions.md`) that in a block the left of `<-` is a
pattern: `(w1, s) <- readFile w0 "f"`, and a bare name `w1 <- print w0 "x"` when the result is
`Unit`. `src/luthier/lib/grammar.lth` already says so (`git log -1 -- src/luthier/lib/grammar.lth`):
`item ::= name ":=" term | pattern "<-" term`; `Item`'s `rebind` now takes a `SurfacePattern`
(`a <- 1` is `rebind (pApp "a" []) ...`, `(w1, s) <- f w0` is `rebind (pTuple [pvar "w1", pvar "s"])
...`); `wf` checks the pattern with `wfPattern`; `BlockOrRecordValue` gained the tuple case.

Make `surface.py` (`Rebind` takes a `SurfacePattern`), the parser, the printer, the random-tree
generator and the tests follow: transcribe `BlockOrRecordValue` anew, add the tuple case to the
generator's `Rebind`, keep every other law test passing.

Check: `python3 -m pytest tests/test_parse.py tests/test_roundtrip_trees.py tests/test_ebnf.py
tests/test_spec.py tests/test_render_grammar.py -q`; `luthier parse src/luthier/lib/*.lth
src/luthier/lib/*.lut examples/hello.lut tests/spec/*.lut` (the one syntax reject excepted). Do not
commit. Report in a few lines to `record/IA/sums-2026-10-13/codex-rebind.md`.
