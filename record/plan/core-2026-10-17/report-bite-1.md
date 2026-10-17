# Bite 1, the code fixes and the directory: report

2026-10-18, by Claude Opus 5.5, an agent of the coordinating session, on `prompt-bite-1.md` of this
folder (execution.md sections 1, 6 with its additions, and 8; report-bite-2.md; D-2026-10-15-e, the
hash erases binder annotations; D-2026-10-15-i, the interpreter's revision by stage). Started at
4051cb0.

## Commits

Code, theory and spec, each apart:

- f5acdff certify.py: `erase` (each `Lam`'s and `Let`'s type annotation becomes `Hole "erased"`),
  applied by `canon` and by `Cones`; tests/test_certify.py: the law checked step by step on the code
  of four test programs, its control refuted, two elaborations differing only in annotations with
  one hash.
- 40a7bdf certification.lth §4: `eraseBinders`, the theory `Erasure` and its law
  `ErasureKeepsTheStep`; `canonCode` reads the erased code; certification_model.lut's `erasure`;
  a test line and a control line.
- bc420b2 spec 6.S8.
- bc7adbc tester.py: a census whose list literal builds a member by an expression is fingerprinted by
  its own cone besides its named members (3h's finding); a test.
- cfa7138 tester.py: `drawing_revision`, the code that draws a sampled entry's cases, in its binding's
  fingerprints; a test. 2d31dcf spec 7.S9.
- 5dbce93 the moves only: `lib/core.lut` to `lib/core/core.lut`, `lib/kernel_laws.lth` to
  `lib/core/structures/equality.lth`.
- d8ed47f the split and the repointing: equality.lth keeps §1, `algebraic.lth` takes §3, the monoid
  of §4 and §5, `universal.lth` takes §2, the free monoid and lists of §4 and §6; kernel_models.lut's
  six models at the end of core.lut, names unchanged; run.py's `CORE`; every `import
  "kernel_laws.lth"` repointed (term.lth, numbers_model.lut, world.lth, plot.lth, algebra.lth,
  generators.lth, generators_model.lut, core.lut, bite 2's three properties files,
  core_instances.lut, five test programs, tests/test_run.py:1164) and the tests that name the files.
  b536f9a spec 3.S36.
- 82bf667 `certify.FUEL`, the default fuel per case, 3,000,000; e85dd1f spec 12.S15.
- edf556d certify.py and tests/conftest.py: a store under a directory of lib/ keeps its path in the
  suite's copy of the stores (before, `store_path` only redirected lib/'s top level, so bite 3's
  `lib/core/core.cert.json` would have been written by the suite into the library's own).
- cfed65f the stores after the re-certification.
- 735f7f3 experiment_zero's run record and the first actions it validated.
- 1ec2071 core.lut: `sumAB` on `Selected`'s labels `one` and `two` (finding 4).
- 6596967 test_certify.py lists the new law and control lines; fc27228 plot_cases.lut's duplicate
  `bind` removed.
- 82b77c1 execution.md's Status line; this commit, the report.

## The checks

- `luthier check` on the 24 .lth and .lut files bite 1 touched: nothing, exit 0 (after fc27228; the
  duplicate `bind` of plot_cases.lut, there since 472bc98, was the one refusal).
- `luthier check -v` over the library: 70 unclaimed Bool laws before and after, the same ones. In
  lib/core/ they are bite 2's 32 in properties/ and core.lut's `implies`, which moved with core.lut;
  structures/ has none (each section's laws are claimed by its theory, as in kernel_laws.lth). The
  three structure files type 36 of 39, 14 of 16 and 44 of 44 acts, kernel_laws.lth's 94 of 99.
- The wave: `luthier certify tests/tester/*.test.lut --jobs 5 --fuel 60000000`, 83 min, without
  `--deep`. 35 test programs, every line ran (no identity was known: every cone holds a binder), no
  law refuted, every law of every file controlled. The three fixture programs printed what they are
  built to print (laws.test.lut: AndIsOr and Small refuted; cases.test.lut: Partial and
  RootIsNotNegative not run).
- `luthier certify` again over the 38 files: `0 lines ran` in each of the 35, the fixtures' lines
  only ran; exit 1 for the fixtures alone. The stores they write beside themselves
  (`laws.test.cert.json`, `cases.test.cert.json`, `weakest.test.cert.json`) were removed after each
  run, as j2a did.
- `python -m pytest -q tests`: `820 passed, 6 skipped, 9 xfailed in 1286.15s` at fc27228 (814 passed
  at 6df1ba9; six tests added). The first full run, at cfed65f, failed two: the store law's test
  listed certification_laws' lines without the new one, and test_run's record of a plan found `a@...`
  where it expected `a` (finding 4).
- `python3 scripts/check_spec.py`: its known finding only, `docs/spec/03-kernel.md:190`; "185
  implemented, 80 decided (of which 33 suspended), 8 proposed".
- `luthier run examples/sonolocalizacion/experiment_zero.run.lut --set graphDir=examples/
  sonolocalizacion/A/graph_noA2 --set outDir=<scratchpad> --set lmMaxIter=500 --set lmTol=1e-06
  --set lmFloor=5.995204332975845e-15 --time-limit 120`: the certification check passed and the run
  went on until the time limit, 8,773,632 steps. Its record (the 24th of experiment_zero.run.json)
  says `finished: false`, `cut: time limit`, and the same certification states as the last full run
  of 2026-10-15: 9 certified, 1 at first action, 223 vacuous, 95 laws, none uncertified, stale or
  failed. It validated two first actions (`host.readFile` on nodes.csv), written to
  world_model.cert.json. The lock file the run wrote beside the program was removed. outDir was my
  scratchpad, since the last record's was another session's.

## The stores, before and after

Before (4051cb0): 953 entries in 28 stores. With bite 1's code, 0 of them were at the cone hash of
any test line, so the count of entries whose cones hold no binder is zero.

After the wave: 534 entries in 29 stores, 486 written by the wave at their lines' new hashes (207 of
them controls), and 48 older ones whose group (law and binding without fingerprints) no line runs any
more, kept stale by `prune`'s rule (the latest entry of a group with no current entry stays): 10
first-action entries runs wrote, entries under bindings the test programs have since rewritten, and
three of laws no line names (SourceIsUniform and its control, KeyReadsTheType). The example's run
then added 2 first-action entries: 536. `git diff --stat` on the stores at cfed65f: 28 files changed,
11286 insertions, 65883 deletions, and `term_model.cert.json` new.

## Findings

1. No law was refuted. Grades are those of j2a's last state (203 laws outside core_laws: 120
   sampled, 82 cases with ErasureKeepsTheStep, 1 supported; core_laws: 46 sampled, 11 cases).
2. MaximizerAscends, MaximizerStationary and MaximizerKeepsDimension on `fitA` (belief_laws, an
   ExhaustiveMode line) spend about 2.6e7 fuel per case (MaximizerAscends measured at 26,061,725,
   414 s for the line, with fuel 1e8). They are stored now only because the wave was given
   `--fuel 60000000`; with the default they are cut and never stored (D-2026-10-15-g). PinvProjects
   measured 1,240,249 per case at seed 20261014, close to j2a's 1.28e6. The measurement wrapped
   `tester.evaluate` and recorded, per line, the largest `fuel given - fuel left` after a case, with
   `tester.run_tests(path, fuel=100_000_000, store=False)` on belief_laws and arrays_laws, started at
   2d31dcf; the script is not in the repository.
3. ErasureKeepsTheStep's control entry went to a new store, `src/luthier/lib/term_model.cert.json`:
   the control binds term_model.lut's `alpha`, `substitute` and `stepper` and a broken erasure the
   controls program defines, so `claim_file` finds term_model.lut as the only home of a model. The
   law's own entry is in certification_model.cert.json beside `erasure`. Both are read by `certify`.
4. A label of a sum in core.lut reserves its name in every program (run.py's `Loaded` takes the
   labels of every file loaded). kernel_models.lut was imported by no file, so `sumAB`'s labels `a`
   and `b` never mattered; in core.lut they renamed a user's `a` and `b` to `a@file`, which the record
   of a run's plan showed. I moved `sumAB` to `Selected`'s labels `one` and `two`, which core loaded
   already through kernel_laws.lth (and now universal.lth). Bite 3 writes the claims of named
   products and coproducts in core.lut too and meets the same rule.
5. The structures' import paths resolve from any file as `"core/structures/x.lth"` (the loader looks
   beside the file first, then under lib/), so no code changed for subpaths.

## Decisions taken on my own (one commit undoes each)

- The erasure covers the annotations of `Lam` and `Let` only; a `Pi`'s domain, a `Sigma`, a
  `Subtype` and record fields stay (they are types the tester draws from). The erased annotation is
  `Hole "erased"`.
- The law is stated in certification.lth §4 on one step and up to alpha (`ErasureKeepsTheStep`,
  certified on term_model's `stepper` at listed terms) and checked on the host's `erase` against
  kernel.py over four test programs' code in pytest; its control erases a lambda's binder with its
  annotation. `canonCode` reads the erased code, so the theory's hash laws agree with the host's.
- A census with a member built by an expression keeps its named members' hashes and adds its own
  cone's; a census of names only is fingerprinted as before.
- The drawing code is the source of the tester's drawing functions (`Values`, `_draw_case`,
  `_in_its_type`, `census`, `generator_of`, `resolve_binding`, `is_cutoff`, `run_spec`,
  `parameters`), the alphabet and seed range, and generators.py's bytes; it is the fingerprint of a
  parameter drawn under SampledMode and is appended to a generator's. ExhaustiveMode bindings and
  statistical lines (whose draws are Luthier code in the cone) are unchanged.
- `certify.FUEL` is raised to 3,000,000 with its reason in the code, not derived; the three fitA
  lines take `--fuel`.
- kernel_models.lut's models keep their names in core.lut; section 3.10's renames are left to bite 3
  with the other renames. `Lists` goes with the free monoid to universal.lth, which imports the
  monoid's laws from algebraic.lth.
- `sumAB` on the labels `one` and `two` (finding 4).
- `store_path` and the suite's copy cover lib/'s subdirectories.
- The spec clauses 3.S36, 6.S8, 7.S9 and 12.S15 updated; the guide and docs/principles.md (a
  projection) still name kernel_laws.lth.
- tests/tester/core_instances.cert.json, untracked, was rewritten by the wave as any store is; its
  state before the wave is kept in my scratchpad. The fixtures' stores were removed.

## Question

The three fitA Maximizer lines need about 2.6e7 fuel per case, so a plain `luthier certify` cuts them
and stores nothing (D-2026-10-15-g). Should a test line carry its own fuel, as a budget beside
`coveringAbove` (generators.lth's `Budgets`, so P11, every criterion a parameter, holds per line), or
should those lines keep needing `--fuel` given by hand?
