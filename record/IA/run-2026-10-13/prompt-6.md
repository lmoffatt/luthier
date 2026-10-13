# run.py bite 6: the loader scopes imports by name, externs' arity from the type, brief

Written 2026-10-14 by the coordinating session (luthier-1b). On the tester's report
(`record/IA/tester-2026-10-14/report.md`, choice 8 and "Findings for others").

## The prompt

Read `CLAUDE.md` first, then that report's two sections, `docs/spec/12-files-and-tools.md` (12.S22,
12.S23, 12.S4: what an `import "x" a b c` and `import "x" m : T` bring in, and by what name),
`src/luthier/lib/library.lth` (the loader's laws: what `admits` and the import form say about
names), `src/luthier/run.py` (`load`, `runtime_slice`) and `src/luthier/tester.py` (`Scope`, the
workaround to replace). Other agents edit `check.py` and `tests/test_check.py` meanwhile: change
only `src/luthier/run.py`, `src/luthier/tester.py` (to remove `Scope` once the loader does its
job), `tests/test_run.py`, `tests/test_tester.py`, programs under `tests/run/` and `tests/tester/`.

1. The loader brings in, from an imported file, only the names the import lists (and the model
   name typed by its theory), as 12.S22 says; a name defined by two imported files and listed by
   neither does not collide: each file's references resolve to the file's own definition, else
   to what it imports explicitly, else it is an error naming the file (not "the first in its
   imports"). Internally qualify by file (`name@file` or your choice, invisible to the user). The
   tester's `Scope` goes away; its tests still pass; `tests/tester/numbers_laws.lut` still runs
   (under `LUTHIER_SLOW=1`). The clashes named (`LeqPair`, `LeqChain`, `LeqBoth`, `PlusCommutes`,
   `NonNegative`, `Exhaustive`, `Assumed`) become tests.
2. An extern's arity comes from its declared type (the `TypedExtern` of bite 4), and only when no
   type is declared from `inspect.signature`, with a builtin lacking one taken as unary; the four
   `log` laws of numbers.lth then settle (run `luthier test tests/tester/numbers_laws.lut` under
   `LUTHIER_SLOW=1` and paste the four lines).

Check: `PYTHONPATH=src python3 -m pytest tests/test_run.py tests/test_tester.py -q`,
`PYTHONPATH=src python3 -m luthier.cli run examples/hello.lut`, then `PYTHONPATH=src python3 -m
pytest tests -q`. Do not commit. Report in your final message.
