# host.py and luthier run, the hello world: brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Fable 5.1 (the coordinating
session), launched by it with `codex exec`. The first half of step 6 of
`record/plan/luthier-from-zero/plan-from-zero-2026-10-13-execution.md` (D-2026-10-13-ad), at its
smallest: `examples/hello.lut` prints "hello, world".

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time (Codex on `elaborate.py` and on
`check.py`): change only `src/luthier/host.py` (new), `src/luthier/run.py` (new), the `run`
command in `src/luthier/cli.py`, `tests/test_run.py` (new), and write your report; a failure from
another file is someone else's, report it, do not fix it. Do not change `elaborate.py`,
`kernel.py` or `src/luthier/lib/`; if they lack something, say what.

Read `docs/spec/10-world.md` (10.S2 to 10.S10), `src/luthier/lib/world.lth`,
`src/luthier/lib/world_model.lut` and `examples/hello.lut` (1f8c61c). The world is a token `W`
threaded through actions: an action takes the token first and gives `W * A` (D8); `main (w : W) :
W * Unit := console.print w "hello, world"`. `world_model.lut` routes the operations of `World` and
`Console` to host functions `python:luthier.host.places`, `read_place`, `print_line`, `read_file`.

1. `src/luthier/host.py`: those four functions. `places()` gives `["stdout"]` plus the files read so
   far; `read_place(name)` gives the stdout buffer or a file's text; `print_line(w, s)` appends `s`
   and a newline to the stdout buffer and returns the token with `unit`; `read_file(w, path)`
   returns the token with the text. The token is a value the host hands back unchanged; the buffer
   lives in the module for one run.
2. `src/luthier/run.py` and `luthier run FILE [--main NAME]`: parse, elaborate (with the imports of
   the file resolved: `import "world.lth" Console` and `import "world_model.lut" console :
   Console` bring those files' acts in, relative to the file; say what `elaborate.py` does with
   imports today and what you had to add around it), supply the token to `main`, reduce; when
   reduction reaches an applied extern (`Extern "python:..."` with its arguments as values), call
   the host function (10.S8: an extern runs when a demand reaches it), substitute its result and go
   on; at the end print the stdout place to the real standard output and exit 0; exit 1 with a
   message on a parse error, a missing `main`, fuel spent, or an extern that fails.
3. `tests/test_run.py`: `luthier run examples/hello.lut` prints `hello, world`; a second program
   you write in `tests/run/` reads a file and prints its first line.

Check: `python3 -m pytest tests/test_run.py -q`, then `python3 -m pytest tests/ -q`;
`PYTHONPATH=src python3 -m luthier.cli run examples/hello.lut`. Do not commit. Report in a few lines
to `record/IA/run-2026-10-13/codex.md`: what you wrote, what the kernel or the elaborator lacked
and how you worked around it, and every choice where spec 10 or world.lth did not decide.
