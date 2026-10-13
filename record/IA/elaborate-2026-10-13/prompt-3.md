# elaborate.py, bite 3: the type of a theory's conjunction and of a redefinition, brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Fable 5.1 (the coordinating
session), launched by it with `codex exec`. After check.py bite 2 (record/IA/check-2026-10-13/codex-2.md).

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time: change only
`src/luthier/elaborate.py`, `tests/test_elaborate.py` and the `LIMITATIONS` table of
`tests/test_spec.py` (removing an entry whose case now passes); a failure from another file is
someone else's, report it, do not fix it.

`luthier check` (`src/luthier/check.py`) fails 4.R6 on every theory file of `src/luthier/lib/`
and on three programs of `tests/spec/` (`k_recursor.accept.lut`, `r2_definition.accept.lut`,
`r4_recursive_data.accept.lut`) for reasons in `elaborate.py`:
1. The type of a conjunction `T := Law1 & Law2 & ...` is inferred as `Hole`. By 4.R6 and 4.S9 it
   is the theory: a definition `T := L1 & L2` under a declaration `T : { ... }` or `T (x : A) : {
   ... }` has the declared type, and the conjunction `&` of laws over a model of `T` is typed as
   the subtype of `T` by them (spec 5.S6); give `&` its type from its operands' types, the
   parameterized form with the binders repeated (4.R6).
2. A definition whose declaration gives a record type (`Codec : { parse : ..., render : ... }`)
   and whose body is a conjunction had its declared type overwritten by the type of the first law
   (`RoundTrip`): the declaration wins.
3. In `k_recursor`, `add (m n : N) : N := recN N m (fn k r { succ r }) n` types the application of
   `succ` as an implication instead of a function: a constructor applied is an application with
   the constructor's declared arrow type.
Each with its test in `tests/test_elaborate.py`; then run `luthier check src/luthier/lib/*.lth
src/luthier/lib/*.lut` and report the 4.R6 failures left, by file.

Check: `python3 -m pytest tests/test_elaborate.py tests/test_check.py tests/test_spec.py -q`, then
`python3 -m pytest tests/ -q`. Do not commit. Report in a few lines to
`record/IA/elaborate-2026-10-13/codex-3.md`.
