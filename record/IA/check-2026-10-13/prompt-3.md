# check.py, bite 3: follow program.lth dc8a8e5 and name the leftovers, brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Fable 5.1 (the coordinating
session), launched by it with `codex exec`. After `codex-2.md`.

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time (Codex on `elaborate.py` and on
`host.py`/`run`): change only `src/luthier/check.py`, `tests/test_check.py`, the `LIMITATIONS`
table of `tests/test_spec.py`, and write your report; a failure from another file is someone
else's, report it, do not fix it.

`src/luthier/lib/program.lth` changed on your bite 2 findings (`git show dc8a8e5`): `untouchedFields`
reads fields through the bound model name (`fieldsRead`: the suffix of every dotted name and every
`proj`, unscoped, over the claimed laws' bodies); labels of a labeled sum anywhere in a type
(field types, binder types, declared types) are constructors; `base` looks through a name defined
as a subtype (`WellFormedEbnf` to `Ebnf`, `LexedText`). Mirror each, with a test.

Then run `luthier check src/luthier/lib/*.lth src/luthier/lib/*.lut examples/hello.lut` and, for
every failure left, print what the theory's author needs to judge whose it is: for 4.R9 the
application and the two bases compared; for 4.R2 the name reported and where it is read; for 4.R6
the body's inferred type and the declared one. Put that in the report, by file.

Check: `python3 -m pytest tests/test_check.py tests/test_spec.py -q`, then `python3 -m pytest
tests/ -q`. Do not commit. Report in a few lines to `record/IA/check-2026-10-13/codex-3.md`.
