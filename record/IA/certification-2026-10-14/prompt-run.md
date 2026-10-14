# run refuses a cone that is not certified (12.S17, 7.S15), brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-3e). After certify.py and the entry
store (prompt-certify.md; its report in `record/IA/certification-2026-10-14/`), the last piece
of his priority: "que Luthier empiece a generar certificados y ver que todo funcione como debe
ser". certification.lth §3 states what a run requires.

## The prompt

Read `CLAUDE.md` first, then `src/luthier/lib/certification.lth` §3 (`Demand`, `ConeName`,
`Refusal`, `coversAll`, `anyServes`, `Certified`, `refuse`; the laws `StaleCertifiesNothing`,
`OnlyAPassServes`, `CertifiesOnlyUnderItsBinding`, `ServesAtTheCutoff`, `ACoveringPassServes`,
`ServesIsMonotoneInTheCutoff`, `ProvisionalIsRefused`, `RefusalSaysWhy`, `RefusalIsPerLaw`),
`docs/spec/12-files-and-tools.md` 12.S17, 12.S18, `07-tests.md` 7.S15, `06-certification.md`
6.S14, `src/luthier/certify.py` (the store, the identity, the cone hash) and `src/luthier/run.py`
(`Loaded`, `runtime_slice`, `run`, `record`). Nobody else edits code now: change
`src/luthier/run.py`, `src/luthier/cli.py`, `src/luthier/certify.py` (a reader of the store only),
`tests/test_run.py`, programs under `tests/run/`, and `tests/test_run.py`'s slow tests.

1. Before evaluating, `run` reads the stores (`x.cert.json` of the file and of each file in the
   cone's imports, 12.S11) and, for each name in the cone of the entry and each law its type
   states (6.S1: the laws of a name's type; a name whose type states no law is certified
   vacuously, [proposed] 10 of the theory), looks for a current passed entry whose reach covers
   the values the run gives it (the holes filled by `--set`, 7.S15) at or above the cutoff the
   demand sets (`ServesAtTheCutoff`: the weakest accepted grade is a parameter of the run,
   `--accept GRADE`, with no default: a run that names none refuses every assumed entry, and
   with no `--accept` at all takes `sampled` [proposed], say so); a provisional name (an extern
   not yet validated at its first action, 10.S10) is refused whole.
2. The refusal lists each unserved law with its state (`RefusalSaysWhy`, `RefusalIsPerLaw`),
   exits 1, evaluates nothing, writes no record; a certified cone runs and its record carries
   the certification state (12.S18: the counts of states of the cone with the names not
   certified, now empty).
3. There is no opt-out (D-2026-10-12-y). The programs that ran uncertified until now
   (`examples/hello.lut`, `tests/run/*.lut`, `examples/sonolocalizacion/*.lut`) must still run:
   say what the stores need for each (which laws their cones state: hello.lut's `Host` laws of
   world.lth? the slice's arrays and fit laws?), run `luthier certify` on what the evidence
   agent wrote (`tests/tester/*_laws.lut`, whose entries certify the library's laws under their
   bindings) and on the port's files, and report which of the 32 run tests, the slow tests and
   the fit still run, which are refused and for which laws. If the slice's cone states laws no
   entry serves (records of functions, 7.R4), say exactly which, with the smallest change that
   would certify them (a listed case entry), and do not weaken the rule.

Check: `PYTHONPATH=src python3 -m pytest tests/test_run.py tests/test_certify.py -q`, then
`PYTHONPATH=src python3 -m pytest tests -q`; `LUTHIER_SLOW=1` for the slow tests. Do not commit.
Report in your final message.
