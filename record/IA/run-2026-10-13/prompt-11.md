# run.py bite 11: the run record completed (12.S18) and the interpreter lock (12.S13), brief for a Sonnet agent

Written 2026-10-15 by the coordinating session (luthier-3e). After run 7 (the record begun:
entry, time, parameters, output), run 8 (the callback counts), run's refusal (the
certification state). What 12.S18 still names and the record lacks.

## The prompt

Read `CLAUDE.md` first, then `docs/spec/12-files-and-tools.md` 12.S18 and 12.S13 (the lock),
`06-certification.md` 6.S8 (what the cone's hash covers), `src/luthier/run.py` (`record`,
`certification`, `run`), `src/luthier/certify.py` (`cone_hash`, `interpreter_revision`,
`host_hash`), the readme of a run (`record/runs/sonolocalizacion-2026-10-14/README.md`: what a
record should let one reproduce, P2). Nobody else edits now: change `src/luthier/run.py`,
`src/luthier/cli.py`, `src/luthier/certify.py` (readers only), `tests/test_run.py`, programs
under `tests/run/`.

1. The record (`x.run.json`, each entry) carries, beside what it has: the hash of the entry's
   cone (it does), the fingerprint of the cone (the canonical code's hash alone, apart from the
   hosts and the interpreter, so that two records say whether the code was the same), the
   interpreter's revision (the tag, as certify reads it) and the Python and the host libraries'
   versions the cone's externs route to (numpy, matplotlib, as `certify.host_hash` names them),
   the fuel given and spent, the files read with the hash of their bytes (host.observe and
   read_file: a list of (path, sha256)), the lock status (2), the counts of states of the cone
   as they are. Drop nothing that exists. A test that reads an entry back and finds each field.
2. `luthier.lock` (12.S13): a file beside the program (or in the repository's root: read the
   item) pinning the interpreter's revision; `run` writes it when absent, warns when it names
   another revision than the current one, and records in the entry whether the run matched the
   lock; `--no-lock` is not added (read the item: say whether it allows one). A test for the
   three cases.
3. The README of record/runs/ says which fields an entry has now (one paragraph).

Check: `PYTHONPATH=src python3 -m pytest tests/test_run.py -q`, then the suite; no
`.run.json` or `.lock` left in the repository (list what the tests create and clean). Do not
commit. Report in your final message.
