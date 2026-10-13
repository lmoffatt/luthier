# host.py and luthier run, bite 2: world.lth draft 1, brief for a Claude agent

Written 2026-10-13 at the commit that holds this file, by Claude Fable 5.1 (the coordinating
session, luthier-1b), for an Opus agent launched by it. After `prompt.md` (host.py, run.py,
test_run.py at 45f60dc and 108fb96) and world.lth draft 1 (0c920f0, by luthier-03 on the internal
review of layers 2-3: no law uses a token twice, nothing generates `W`, no action inside a Bool).

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time (one on `parse.py` and
`surface.py`, one on `check.py`): change only `src/luthier/host.py`, `src/luthier/run.py`,
`tests/test_run.py`, the programs of `tests/run/`, and write your report; a failure from another
file is someone else's, report it, do not fix it. Do not change `examples/hello.lut`,
`src/luthier/lib/` or the elaborator; if they lack something, say what.

Read `docs/spec/10-world.md`, `src/luthier/lib/world.lth` and `world_model.lut` at 0c920f0 or
later (`git log -1 -- src/luthier/lib/world.lth`), and `examples/hello.lut`. The laws are now over
the library's representation `State = { stdout : String, files : List (String * String) }` and an
action's description `S -> S * A`; the host's actions are certified against their descriptions by
the protocol `agreement` of world.lth §5 (observe, act once, observe, compare). The host must
provide:
1. `observe(w)` returning `(w, state)` with `state` the record `{ stdout := <text so far>, files
   := [(path, text), ...] }`, in whatever form the bridge of `run.py` turns a Python dict with
   those two keys into a kernel record value (say which, and whether the bridge needed a case);
2. `print_line(w, s)` and `read_file(w, path)` with their signatures; `read_file` on a missing
   file gives `(w, nothing)` instead of raising (its type is `W * Maybe String`), and on a present
   file `(w, just text)`;
3. `places` is gone (a place is any string); remove it and what used it.
`examples/hello.lut` imports `HostConsole host : HostConsole` from world_model.lut (`HostConsole =
Host State` is an alias of the `.lut`, then a model typed by it) and calls `host.print w "hello,
world"`: make `run.py` resolve that import form if it does not yet (an alias imported from a `.lut`,
then a model typed by it), keeping the test's expected output. Rewrite `tests/run/read_first_line.lut`
for the new `world_model.lut` and keep every test of `tests/test_run.py` meaningful (the places
test becomes an observe test).

Check: `PYTHONPATH=src python3 -m pytest tests/test_run.py -q`, `PYTHONPATH=src python3 -m
luthier.cli run examples/hello.lut`, then `PYTHONPATH=src python3 -m pytest tests -q`. Do not
commit. Report in a few lines to `record/IA/run-2026-10-13/opus-2.md`: what you changed, what the
kernel, the elaborator or world_model.lut lacked and how you worked around it, every choice where
spec 10 or world.lth did not decide.
