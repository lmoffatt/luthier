# The left of `<-` is a pattern: the parser, report

Written 2026-10-13 by an Opus 5.5 subagent of the coordinating session, on the brief
`prompt-rebind.md` against grammar.lth at 87d6091 (D-2026-10-13-ag). Not committed.

Changed. `surface.py`: `Rebind(pattern: SurfacePattern, value)`. `parse.py`: `item` transcribes
`item ::= name ":=" term | pattern "<-" term` (a name followed by `:=` is a bind, otherwise it
backtracks and reads a pattern, then `<-`); `_print_item` prints the pattern with
`_print_pattern`. `block`, `pattern`, `patom` unchanged: a failed item already backtracks to the
block's value, so `{ a := 1 ; (a, b) }` keeps its tuple value. `test_parse.py`:
`BlockOrRecordValue` transcribed anew (the `(w1, s) <- f w0` case), plus tests for the bare name
(`w1 <- print w0 "x"`), a nested pattern (`(w, just x) <- f w0`), the layout block of an action and
a tuple at an item's start without `<-`. `test_roundtrip_trees.py`: `wf` checks a `Rebind` with
`wfPattern`; the generator gives `Rebind` a pattern, half of them a tuple when the budget allows;
a new census `test_random_items_round_trip` (items alone in a block, sizes 1 to 6, seeds 0 to 999,
about a thousand tuple patterns), because whole programs gave only 2 or 3 tuple rebinds in 6000
trees.

Where grammar.lth did not decide, what I chose. (1) `Rebind.name` survives as a read-only property
that returns the name of a bare-name pattern and raises `ValueError` on any other pattern. It is
not in grammar.lth's `Item`; it keeps `elaborate.py:296` and `check.py:482-484` working on today's
programs until their bite 4 reads `.pattern`, and one deletion undoes it. (2) The generator's bias
toward tuples and the item census are mine.

The brief's example does not parse, and should not: its block ends with the item
`w <- console.print w x` and has no final term, while `block ::= { item sep } term [ sep ]`
(2.S17: a block's last item is a bare expression). With a final `(w, x)` it parses to two
`Rebind`s and prints back. Whether a block may end on a rebind is Luciano's question, not the
parser's.

Checks. The five named test files: 153 passed, 7 xfailed (the xfails are the pending ones already
marked in test_spec.py). Full suite: 429 passed, 7 xfailed, 1 failed:
`tests/test_run.py::test_read_first_line` (prints nothing). It fails the same on a clean copy of
HEAD without my change, so it belongs to the host.py/run.py bite after world.lth draft 1 (0c920f0),
not to the parser. `luthier parse` of the libraries, hello.lut and tests/spec: every file parses
except `tests/spec/r12_toplevel_arrow.reject.lut` (`x <- 1` at top level, 2.R5), the expected
syntax reject. `luthier check` of a block with `(a, b) <- m` stops in `check.py` on the
`Rebind.name` error: that is the check.py bite 4 (brief dcd1d5e).
