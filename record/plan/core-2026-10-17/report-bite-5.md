# Bite 5, the prelude, the refusal, qualified access, and Placement: report

2026-10-18, by Claude Opus 5.5, an agent of the coordinating session, on `prompt-bite-5.md` of this
folder (execution.md §1 and §6, bite 5; D-2026-10-18-b, D-2026-10-18-e). Started at ff7fe35; a
session closed in the middle and the work resumed from the uncommitted tree.

## Commits

- fd7b9ee run.py: `Loaded` visits every file under lib/core/ (`core_files`, core.lut first, then by
  path), resolves a name a file neither defines nor imports in the core as a whole, allows a cycle
  of imports among core files and names the path of a name that reaches itself; a file that defines
  a core name is refused naming the core file (`redefinitions`); tests.
- 8e51033 elaborate.py: the prelude is every core file; a file sees every core name but the seven
  two core files define.
- 2f38b8c check.py: `core_names` read from the core's files; the refusal (rule 12.S22); the
  `redundant` notice of `check -v`; `check --no-core`; spec programs `core_unimported.accept.lut`
  and `core_redefined.reject.lut`; four spec programs renamed off the core names they defined.
- f706ef4 tests of check (the names read, the refusal, a known collision, `--no-core`, the notice).
- 4eaba8a the `import "core/..."` lines outside lib/core/ removed (term.lth, numbers_model.lut,
  world.lth, plot.lth, generators.lth, generators_model.lut, five test programs, test_run.py's
  FIRST_ACTION_LAWS), but algebra.lth's and core_instances.lut's names that two core files define;
  check reads a core type's definition (`Concrete`) from the prelude; world tests' `flip` and
  `functions` are `opposite` and `intFunctions`, laws.test.lut's `PlusCommutes` is
  `IntPlusCommutes`.
- f66d569 generators.lth's `Metric`, `LinearMetric`, `LogMetric` are `Placement`,
  `LinearPlacement`, `LogPlacement` (field `placement`, models `linearPlacement`, `logPlacement`);
  test.lth's `SampledMode : Placement -> Mode`; tester.py's `Spec.placement` and its line "placement
  ignored"; spec 7.S2, 7.S4, 7.R1 reworded; test lines keep `SampledMode linear`.
- 7a5a6e0, 79352ca spec 12.S4 and 12.S22 (from §1); the Files line I first gave 12.S22 removed,
  check_spec refuses one on a statement.
- 50c246b the stores after the wave.
- bd59354 three fixtures of test_certify.py and test_tester.py renamed off core names.
- this commit, the report and the plan's Status (core_metrics in its message; bd59354, the last code commit, lacks them, and a later commit of the coordinator, 0b0f35f, sits above it).

## The wave (one, without --deep)

`luthier certify` on the four programs whose lines a dry run (every line's identity against the
stores, nothing run) found unknown: certification_laws 1 line ran (ErasureKeepsTheStep),
certification_controls 1 (its control), world_laws 3 (CallbackGivesTheFunction, CallsAreCounted,
RecordCrossesByField), world_controls 3 (their controls). Every law graded cases, controlled; no
law refuted, no control failed. Stores written: certification_model, term_model, world.

What moved the lines: the world lines by the renames of `flip` and `functions` (a binding names the
census by its name); ErasureKeepsTheStep by bite 4's finding-3 fix (e6cabf2), which changed how
term_model.lut's `stepApplication` elaborates. The addendum to report-bite-4.md says no cone moved
with that fix; the dry run at e6cabf2^ knows both lines and at HEAD before this bite does not, so it
did move them. Neither the loader nor the Placement rename moved a cone: the dry run after each
gave the same unknown lines and no others (no certified law reaches `Placement`).

After the wave, `luthier certify` over the 35 non-fixture test programs (all of tests/tester but
cases, laws and weakest, whose stores are untracked fixtures) prints `0 lines ran` for every one,
no law `not run`, none `uncontrolled`.

## The acceptance criteria

- A file that defines or declares a core name is refused by check (rule 12.S22) and by the loader,
  the core file named: `core_redefined.reject.lut`, `test_a_file_that_redefines_a_core_name_is_refused`
  (three names, three core files), `test_a_file_that_defines_a_core_name_is_refused_with_the_core_file`.
- A core name with no import passes check: `core_unimported.accept.lut` uses `compose`, `Total`,
  a claim of `Object` and its field `eq`, none of which a file could reach before this bite (check
  refuses it at ff7fe35). `size` is not a core name yet: it arrives with bite 6's containers.lth, and
  so does `map` for the reject program; both programs say so in their header.
- The file cycle inside the core: `test_a_cycle_of_core_files_is_allowed_when_no_name_reaches_itself`
  and `test_a_name_that_reaches_itself_through_two_core_files_is_an_error_with_its_path` ("a.lth: x
  is imported in a cycle: a.lth x -> b.lth x -> a.lth x"), on a core directory of the test's
  (`Loaded(path, core=directory)`). The present core has no cycle of files.
- `grep -rn "\bMetric\b" src/luthier/lib/generators.lth src/luthier/lib/test.lth`: nothing.
- `python -m pytest -q`: 862 passed, 6 skipped, 9 xfailed (24 min; 848 passed before, 14 tests added). The first full run failed three fixtures of test_certify.py and test_tester.py that defined core names; bd59354 renamed them.
- `python3 scripts/check_spec.py`: its known finding only (03-kernel.md:192 shares ten words with
  principles.md).
- `scripts/core_metrics.py`: homonyms 96, executive names shadowing 107 (112 before: `flip`,
  `functions` twice, `PlusCommutes`), list helpers 427, unclaimed 137, loose 1974 (real 1341, the
  rest 633).
- `check` over lib/, examples/ and tests/tester/: the same six failures as before (distances.lut's
  `pairI`, `pairJ`; plot_cases.lut's `perms`; experiment_zero.run.lut's three 4.R2).

## Decisions taken in this bite (one commit undoes each)

- The present collisions are listed, not refused, until the bite that rewrites their file
  (run.py's `CORE_COLLISIONS`, a parameter with the reason and the bite of each): algebra.lth 9
  names and numbers.lth 11 (core/structures/algebraic.lth's OrderedSemiring laws; bite 8), laws.lth
  `Both`, `flip` (bite 9), arrays.lth `Symmetric` (bite 11), term.lth `Beta`, translation.lth
  `Lists` (bite 10), and inside the core equality.lth's `Reflexive`, `Symmetric`, `Transitive`,
  algebraic.lth's `Associative`, `LeftNeutral`, `RightNeutral` against properties/, and the two
  `Idempotent` of functions.lth and operations.lth (bite 6). Any other collision is refused.
- A name two core files define is not seen without an import: the loader says it is defined by
  both and is imported from one; check does not count it a core name. So algebra.lth keeps
  `import "core/structures/algebraic.lth" LeftNeutral RightNeutral Associative` and core_instances.lut
  keeps the imports of those seven names; every other `import "core/..."` outside lib/core/ is gone.
- An import of a core name by its path is a `redundant` notice of `check -v` (the plan's
  [proposed]), and no notice for a name two core files define or an import under another name.
- The refusal is rule 12.S22 in check's output.
- A core file sees the whole core too (before, core.lut's names reached every file but core.lut).
- `loaded.core` stays core.lut (the data that roots a run's slice, a model's home excluded);
  `loaded.core_files` is the directory.
- `--no-core` is implemented for `luthier check` only (12.S14 names it there); run, eval, test and
  certify keep the core.
- check reads a core type defined without parameters (`Concrete`) from the prelude, so a file that
  stopped importing it still sees its base (4.R9).
- Renames in tests to leave core names: scope fixture `not` to `keep`, eval fixture `Nat` to
  `Peano`, world tests `flip`/`functions` to `opposite`/`intFunctions`, laws.test.lut and the
  pooled-seeds fixture `PlusCommutes` to `IntPlusCommutes`, the pair fixture `Idempotent`,
  `Reflexive`, `flip` to `Stable`, `SelfEqual`, `toggle`, the generated fixture `Unit` to `AllUnit`;
  spec programs: k_bare_conjunction's six names prefixed `Is`/`Rel`, r13_structure_name's structure
  `Equality`, r3's `Associative` as `AssociativeOp`.
- Placement: the field is `placement` and the models `linearPlacement`, `logPlacement` (the
  decision names the three theories); the tester's line says "placement ignored".

## Findings

- ErasureKeepsTheStep's cone moved with bite 4's finding-3 fix, contrary to report-bite-4.md's
  addendum; re-certified here, cases, controlled.
- Chapter 7 still says metric for the placement outside the three clauses D-2026-10-18-e names:
  the opening list (its line 7), the table of modes (`sampled m`, "a metric: linear, log"), three rows
  of the table of generators ("the metric over the bounds") and 7.S20's "`sampled` with its metric".
  Left as they are, the decision naming three sentences.
- A worktree I did not create, `scratchpad/wt-argon` at fd7b9ee, appeared during the bite.

## Question

The present collisions (20 names in numbers.lth and algebra.lth, six more in laws, arrays, term and
translation, seven inside the core) are listed as known until the bite that rewrites each file,
where D-2026-10-18-b says a redefinition is refused: keep the list, emptied bite by bite, or rename
them now at the cost of re-certifying numbers' and algebra's laws twice (now and again in bite 8)?
Recommended: keep the list.
