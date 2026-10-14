# certify.py and the entry store: `luthier certify`, the tester reusing entries, brief

Written 2026-10-14 by the coordinating session (luthier-3e). On certification.lth and its model
(043f4b9, 9918c38; the agent's report in `record/plan/night-2026-10-13.md` at 22:30 and below),
step 5.3 of the execution plan. Luciano: "lo importante es que Luthier empiece a generar
certificados".

## The prompt

Read `CLAUDE.md` first, then `src/luthier/lib/certification.lth` whole (its §1 entry, §2
certificate, §4 the cone's hash, §5 the laws) and `certification_model.lut`, then
`docs/spec/06-certification.md` 6.S8, `07-tests.md` 7.S9, 7.S13, `12-files-and-tools.md` 12.S11,
12.S16, `record/IA/tester-2026-10-14/report.md` (how the tester runs a `test` line and what it
knows of the law, the binding, the seed, `n`), `src/luthier/tester.py`, `src/luthier/run.py`
(`Loaded`, `runtime_slice`: the cone of a name; `record` of `x.run.json`), `src/luthier/kernel.py`
`canonical` (term.lth §4). Nobody else edits code now: change `src/luthier/certify.py` (new),
`src/luthier/tester.py`, `src/luthier/cli.py` (the `certify` command and `test`'s store options),
`tests/test_certify.py` (new), `tests/test_tester.py`, programs under `tests/tester/`.

1. `certify.cone_hash(loaded, name)`: the hash (sha256) of the cone of `name`: the canonical
   form of each definition the name reaches (term.lth §4, `kernel.canonical`, module prefixes
   and alpha-renaming not seen), the host code behind each extern the cone calls (the source
   file of the module, or the installed package and its version, 6.S8), and the interpreter's
   revision (this repository's commit of `src/luthier/`, or the package version); the four laws
   of `ConeHashing` as tests (`HashOfTheCanonicalForm`, `HashSeesTheCode`, `HashSeesTheHost`,
   `HashSeesTheInterpreter`). The route `python:luthier.certify.cone_hash` the model names.
2. The store: `x.cert.json` beside `x.lut`, a JSON list of entries as certification.lth's `Entry`
   reads them (identity: the law, the cone hash, the binding expanded per parameter, the seed,
   `n`; the reach per parameter; the evidence; the grade when passed; the outcome; the date; the
   interpreter revision; the host hashes by route). `Store`'s predicate holds on every store
   written or read (determinism per identity, a grade exactly when passed); `record` never edits
   an entry and leaves the store unchanged on a known identity ([proposed] 5); a stale entry
   (hash differs) is kept and marked stale on reading (12.S11).
3. The tester writes an entry per `test` line it runs and, before running, looks the identity
   up (7.S13): a known outcome is reused whatever it is and reported as known with its date,
   not run again; `--deep` reruns; a new seed is a new entry. `luthier test FILE` prints per
   line the grade and whether it ran or was known.
4. `luthier certify FILES [--jobs N] [--seed N] [--deep]` (12.S16): runs the `test` lines of
   several files, each in its own process, writing their stores; prints per file the laws and
   their grades, the weakest across bindings ([proposed] 6).
5. `luthier check -v FILE` says per law its standing from the store (the grade, or uncertified,
   or stale) if cheap; else leave it for the next bite and say so.
Tests: the four hash laws; a store round trip; an entry reused on a second `test` (the counts
show no rerun); `--deep` reruns; a changed definition makes the entry stale; `luthier certify`
on `tests/tester/laws.lut` and on `src/luthier/lib/numbers_model.lut`'s test lines if the
evidence agent added them (read `git log -5 -- src/luthier/lib/*_model.lut`).

Check: `PYTHONPATH=src python3 -m pytest tests/test_certify.py tests/test_tester.py -q`, then
`PYTHONPATH=src python3 -m pytest tests -q`; no `.cert.json` left in the repository (they are
gitignored but clean up anyway). Do not commit. Report in your final message: what is written,
each law of §1, §4 and `Store` met and how, every choice the theory left open.
