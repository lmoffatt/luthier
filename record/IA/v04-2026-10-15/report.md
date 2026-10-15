# Report: v0.4's criteria, then `luthier eval` with imports (12.S19)

2026-10-15, by Claude Opus 5.5, an agent of the coordinating session, on `prompt.md` of this
folder (24d3d43).

## 1. The criteria (step 6.3), committed alone at 32a09b9

Written in the plan's step 6 item 3, in the form of v0.3's, with a dated Status line; item 1's
"Next: the external review" and item 2's "`--checked` running" corrected (both done).

- (a) `eval` as 12.S19: not met at 32a09b9; met by the change below once committed.
- (b) `session` as 2.S18 and 12.S20: not met. cli.py has no `session`; 12.S20 says
  `[implemented]` and 2.S18 says it is not. The code agrees with 2.S18, so 12.S20's marker is
  wrong (the spec's, left to the coordinator).
- (c) the result store across runs at its smallest (8.S3, 8.S8, 8.S10): not met, and it waits
  for one word of his: whether a run whose cone acts on the world (`print`, `readFile`) may be
  served from the store, or only a pure entry.
- (d) the layer 3 external review applied: met (step 5.5's f, bc646d8).
- (e) step 6's theories each with its laws controlled (L9.14): not met. Measured with `luthier
  check -v tests/tester/*_laws.lut tests/tester/*_controls.lut` (1 min 40 s): 148 law lines,
  142 controlled, 6 uncontrolled, all six in sonolocalizacion_laws.lut (an example's laws).
  world.lth has lines for `Console`'s four laws only; demand.lth and plan.lth have none.
- (f) the suite and the lints: met at 24d3d43 (710 passed, 5 skipped, 9 xfailed;
  check_spec.py silent; project_principles.py --check --strict exit 0; check_quotes.py exit 1,
  the old debt, his question).

## 2. `luthier eval files term` (12.S19), uncommitted

What 12.S19 says on certification: "It records nothing and demands no certificate. [decided
D-2026-10-12-ah] `eval` is exempt from the strictness of `run` (D-2026-10-12-y) as a probe, and
prints the states of the cone of its term, so that what it shows is never taken for a certified
result." Followed: nothing is refused and nothing is written, and the states are printed after
the value.

Changes:
- `src/luthier/run.py`: `Probe(Loaded)` loads the files with their imports and core as `run`
  does, and gives the term a file of its own (`<eval>`, beside the first file) that sees what
  each file sees: its definitions, constructors, labels and the names its imports list.
  `evaluate(files, term, fuel)` takes the runtime slice, elaborates it, infers the type (the
  elaborator's `infer` on `it := term`), reads the states with `certification(...,
  refuse=False)`, and reduces the value in every concrete part (`Runner.value`).
  `show_states` prints them. `certification` gains `refuse` (default True: `run` is unchanged
  and its record has no new field). With `refuse=False` each refused name is counted by its
  state and the refusal lines go under `refused`.
- `src/luthier/cli.py`: `eval files... term [--fuel]`. It prints `value : type`, then
  `states of the cone, accepting sampled and above: ...` and one indented line per law not
  served. Errors go to stderr (as `run`'s do), exit 1. The fuel defaults to the demand's
  (10,000,000), not 10,000.
- `tests/eval/plan_agree.lut` (new) imports `agree`, `bothLinearize`, `readersFirstRefused` and
  `needPlan` from plan_model.lut, and defines `allHold`.
- `tests/eval/labeled_sum.lut` drops its own `Bool` and `Maybe`. With core loaded, the kernel's
  `==` returns core's `true`, which the file's own `Bool` does not match ("stuck match"). The
  same holds for `run` on any file that redefines `Bool`. That's a latent defect of the loader
  (a core type redefined by the file run), reported here and left alone.
- `tests/test_elaborate.py`: the eight eval tests now expect `value : type` and a states line;
  the error tests read stderr. New tests cover imports (`agree`, `needPlan.schedule`), the
  states listed and not refused (`allHold`), a term over two files, and that nothing gets
  written.

Example:

    $ PYTHONPATH=src python3 -m luthier.cli eval tests/eval/plan_agree.lut agree
    true : Bool
    states of the cone, accepting sampled and above: 47 vacuous, 1 uncertified
      example: NamesAreUnique: uncertified (no entry)
      example: Acyclic: uncertified (no entry)
      example: StepIsLocal: uncertified (no entry)

## Accepted when

- The plan has 6.3 with each criterion's state: yes (32a09b9).
- `PYTHONPATH=src python3 -m luthier.cli eval tests/eval/plan_agree.lut agree` prints
  `true : Bool`, exit 0, in 1.9 s; `git status --short --ignored` on tests/eval and
  src/luthier/lib shows nothing new after it.
- The suite passes: `python3 -m pytest -q`, 714 passed, 5 skipped, 9 xfailed (4 min 46 s);
  check_spec.py silent, project_principles.py --check --strict exit 0.

## Decisions I took on my own (each undone by reverting its file)

1. A name two of the files give resolves to the first file's; the term's definition is the first
   of `it`, `it1`, ... that no file sees.
2. The states are read at the demand's default cutoff (sampled). A name with several laws not
   served takes its first law's state. A passed entry that doesn't serve the cutoff counts as
   uncertified, with its line saying why.
3. `eval` gives its term no world, so it performs no action and validates no first action
   (10.S10). It doesn't warn about the lock either (12.S13 says it doesn't yet).
4. If the states can't be read, the value is still printed, followed by `states: not read (why)`.
5. The value comes first on stdout, then the states, also on stdout. Errors go to stderr.
6. The fixture `labeled_sum.lut` uses core's `Bool` and `Maybe`.

## For the coordinator

- 12.S19's "Today it prints no states" and 12.S20's `[implemented]` are now false. The first
  becomes true once this lands; the second was already false.
- 12.S19 writes `eval files term`, and the old `eval file name` form is gone: a name is a term.
