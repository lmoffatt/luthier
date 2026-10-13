# check.py bite 4: a rebind binds its pattern's names, report

Written 2026-10-14 by an Opus agent (Claude Opus 5.5) launched by the coordinating session, on
`prompt-4.md`, at 5fa3d84 plus the working tree. Not committed.

- `src/luthier/check.py`: a new `item_binds(it, k)` (`{x}` for `x := v`, `pattern_binds(q, k)` for
  `q <- v`) mirrors program.lth's `itemsNames`, used by `names`. 4.R12 (`block_fault`) refuses a
  `<-` when any name its pattern binds (constructors `nil`, as `itemsFault` reads it) is a `:=`
  name in scope. 2.R6 (`violatesR2R6`) refuses when any name the pattern binds is still pending
  after the value's names are removed, then adds them all to pending (`unusedRebinding`).
  Nothing in check.py reads `Rebind.name` any more.
- `src/luthier/surface.py`: the `Rebind.name` property removed (no other reader: elaborate.py
  reads `.pattern`, parse.py prints the pattern). Its removal also stops a latent trap: `hasattr`
  catches only `AttributeError`, so the property raised `ValueError` through any `hasattr(x, 'name')`.
- `tests/test_check.py`, `test_rebind_binds_its_pattern_names`: `(w, x) <- readFile w "f"`
  rebinding the parameter `w` and binding `x` passes 4.R12 and 2.R6, and its names are the
  body's free names less `w`, `x`; the same refused by 4.R12 when `x := 1` precedes it; two
  `(w, x) <- ...` with `x` unused between them refused by 2.R6, and accepted when the second reads `x`.
- `tests/spec/r12_pattern_rebind.accept.lut` and `.reject.lut` (4.R12 has bare-name programs,
  `r12_block.accept.lut` and `r12_rebind_defined.reject.lut`), the reject registered in
  `EXPECTED_RULE` as `4.R12`. 2.R6's reject (`r12_unused_rebinding.reject.lut`) has no pattern
  twin; the unit test covers it. No `Files:` line in docs/spec cites the two new programs.

Check: `tests/test_check.py tests/test_spec.py` 102 passed, 7 xfailed; `tests` 448 passed,
7 xfailed (with the other agents' uncommitted kernel.py and test_kernel.py in the tree). With
bite 3b part 2's two fixes on top (opus-3b.md, Part 2): 104 and 450 passed, 7 xfailed.
