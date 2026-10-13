# elaborate.py bite 4: a pattern on `<-`, report

Written 2026-10-13 by an Opus 5.5 subagent of the coordinating session, on the brief `prompt-4.md`
against translation.lth at 87d6091 (law `Blocks`) and the parser at a590378. Not committed.

Changed. `elaborate.py`: a block is elaborated item by item by a new `block` function, each item
wrapping the rest of the block. `x := t`, and a bare name on a value that is not an action, give a
`Let` on a fresh name as before. A pattern on an action (inferred type `W * A`) gives
`Match t [(pattern, rest)]`, the pattern translated as in a `match` arm with its variables renamed
fresh (so `w <- print w "a"; w <- print w "b"` chains `w`, `w'`, like the `y0`, `y1` of 4.R12), and
its variables get the components of `W * A` as types. A bare name on `W * Unit` gives
`PPair (PVar w1) PWild`. `pattern` takes a `fresh` flag for this; `Rebind.name` is no longer read
in elaborate.py (the property itself is left for check.py's bite). `test_elaborate.py`: the law's
two action `gives` (`test_Blocks_action_pattern`, `test_Blocks_action_unit`; the `Let` one was
already in `test_Blocks`), a chain that rebinds the token, and the refusal. `LIMITATIONS`
unchanged: no xfailed case passes now.

Where translation.lth did not decide, what I chose. (1) A pattern that is not a bare name on a
value that is not an action raises `ElaborationError` naming the item, as the brief says, e.g.
"block item (a, b) <- n: a pattern that is not a bare name on a value of type (_ : Int) * Int,
which is not an action W * A". Question for Luciano: 2.S17 reads "the left of `<-` is a pattern
against what the right gives", which would make `(a, b) <- n` a one-arm `match` too; should
translation.lth say so? (2) A value whose type the bootstrap inference cannot tell (a Hole) with a
pattern that is not a bare name is read as an action (a `match`); with a bare name it stays a
`Let`. (3) A bare name on an action whose `A` is not `Unit` (`p <- readFile w0 "f"`) follows the
law's general case: `Match t [(PVar p, rest)]`, `p` the whole pair. D-2026-10-13-ag allows a bare
name only when `A` is `Unit`; rejecting the other case I left to the checker
(`cite_proved.accept.lut` binds such a pair today).

Checks. The four named files: 154 passed, 7 xfailed. Full suite: 437 passed, 7 xfailed, nothing
failed (`test_read_first_line` passes in this working tree, with the host bite's uncommitted
changes). The 56 programs of `tests/eval/`, `tests/spec/`, `tests/run/` and `examples/hello.lut`
elaborate to the same repr as with HEAD's elaborate.py (50 identical, 6 failing with the same
message before and after). `luthier run` of two blocks over `host.print`, one with
`w1 <- host.print w "one"` and one with `(w1, u) <- ...`, prints both lines.
