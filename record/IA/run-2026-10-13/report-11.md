# run.py bite 11: the run record completed, the interpreter lock: report

2026-10-15, Claude Sonnet 5.5, an agent of luthier-3e, on prompt-11.md; saved by the coordinator.
Files: `src/luthier/run.py`, `src/luthier/host.py` (reads logged), `tests/test_run.py`,
`record/runs/README.md` (new, the entry's fields). Checks: test_run 86 passed; the suite green.

An entry of `x.run.json` now holds: `entry`, `time`, `parameters`, `output`, `calls`, `fuel`
`{given, spent}`, `files_read` as `[path, sha256]` pairs (each read once per run, first-read
order, `observe` and `read_file` both), `lock` `{path, pinned, status}`, and `certification`
with `cone`, `fingerprint` (the cone's code alone, no hosts, empty interpreter, [proposed]),
`interpreter` (the tag), `python`, `hosts` (each extern route to `certify.host_hash`'s
"numpy x.y"), `accept`, `states`, `laws`, `not certified`.

The lock (12.S13): `luthier.lock` searched in the program's directory then the one above;
JSON `{"interpreter": rev}` with the tag as `certify.interpreter_revision` reads it (12.S13
says "commit"); status `matches`, `differs` (a warning on stderr, the run goes on) or `absent`,
in which case `record()` writes it beside the program after a successful run (`written`); no
`--no-lock` (12.S13 names none). Only `run` checks it (12.S13 says "every command that loads a
program": check, test, eval do not warn yet). Not gitignored: meant to be committed; running
the CLI on a program in the repository writes one beside it.

Decisions of the agent: the lock's format and the tag; `run` only; the fingerprint's
definition; the fields carried in `run()`'s dict and moved out by `record()`.
