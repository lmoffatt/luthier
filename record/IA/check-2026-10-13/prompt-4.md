# check.py, bite 4: a rebind binds the pattern's names, brief for a Claude agent

Written 2026-10-13 at the commit that holds this file, by Claude Fable 5.1 (the coordinating
session, luthier-1b), for an Opus agent launched by it. After bite 3b (opus-3b.md) and after the
parser follows D-2026-10-13-ag (`surface.Rebind` takes a `SurfacePattern`, report
`record/IA/sums-2026-10-13/opus-rebind.md`).

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time: change only
`src/luthier/check.py`, `tests/test_check.py`, the `LIMITATIONS` table of `tests/test_spec.py`, and
write your report; a failure from another file is someone else's, report it, do not fix it.

`src/luthier/lib/program.lth` (87d6091 or later) reads a block item `rebind q v` with `q` a
pattern: `itemsNames` removes `patternBinds k q` from the names of the rest (free names); 4.R12
(`itemsFault`: `<-` may rebind a parameter or a name bound by an earlier `<-`, never a name bound
with `:=` in scope, `anyIn (patternBinds nil q) defined`); 2.R6 (`unusedRebinding`: a `<-` whose
previous binding of the same name was never used is an unused binding, now over every name the
pattern binds). Mirror the three in `check.py` (today they assume a bare name), with a test each in
`tests/test_check.py` on a tuple pattern: `(w, x) <- readFile w "f"` rebinding the parameter `w`
and binding `x`; the same refused when `x` was bound with `:=`; `(w, x) <- ...` twice with `x`
unused between them refused by 2.R6. Add to `tests/spec/` an accept and a reject program for the
pattern case only if the chapter's rule already has programs for the bare-name case (then name
them the same way, `r12_pattern_rebind.accept.lut` and `.reject.lut`), and register them in
`tests/test_spec.py` as the others are.

Check: `PYTHONPATH=src python3 -m pytest tests/test_check.py tests/test_spec.py -q`, then
`PYTHONPATH=src python3 -m pytest tests -q`. Do not commit. Report in a few lines to
`record/IA/check-2026-10-13/opus-4.md`.
