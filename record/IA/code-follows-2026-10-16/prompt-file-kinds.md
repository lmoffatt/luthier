# Brief: three kinds of file (step 3g, D-2026-10-16-e)

Read `CLAUDE.md` first, then `record/decisions.md` at D-2026-10-16-e (and -d, the modes of running
in the demand), `record/principles-language.md` L2.6 and L5.1 (their 2026-10-16 sentences),
L10.12; `docs/spec/02-*.md`, `docs/spec/07-tests.md`, `docs/spec/12-files-and-tools.md`;
`src/luthier/check.py`, `src/luthier/cli.py` (`run`, `certify`, `test`, `check`), the loader
(where imports are resolved), `tests/conftest.py`.

The rule: a theory `.lth` (types, declarations, laws; never executed); a model or library `.lut`
(definitions that claim a theory; executed only when a demand reaches them); an executive file,
which carries a demand with its entry and is never imported: `*.run.lut` (an entry `main` that
`luthier run` applies to the world, with the run's modes) or `*.test.lut` (the `test` lines
`luthier certify` runs). The suffix declares the kind and the content verifies it.

Build:
1. Checker refusals, each with a message naming the file and the rule: an import of an executive
   file; a `test` line or a demand in a `.lut` or `.lth`; a `.run.lut` without `main`; a `.test.lut`
   without `test` lines. `run` takes only `.run.lut`, `certify` (and `test`) only `.test.lut`, each
   refusing another kind with a message saying which suffix it wants.
2. Executive files may define local names, seen nowhere else; their results (`x.run.json`,
   `x.results.json`) live beside them; certificates still live beside the claiming file (L10.12).
3. Migration, with `git mv` so history follows: tests/tester/*_laws.lut and *_controls.lut become
   `*.test.lut`; every file with a `main` that `run` is applied to becomes `*.run.lut`; files that
   mix a library and a `main` (examples/sonolocalizacion/validate_graph.lut, experiment_zero.lut,
   and any other you find) split into a model `.lut` and a `.run.lut` that imports it. Update every
   reference: tests, scripts, docs, the record's plans only where a command is quoted for future
   use (leave historical reports as they are).
4. Spec: the chapters on files and tools and on tests state the three kinds and the refusals;
   statuses `[implemented]` for what you did and tested.
Tests: each refusal (accept and reject programs, as `tests/spec/` does for rules); `run` on a
`.test.lut` and `certify` on a `.run.lut` refused; a `.run.lut` imported by another file refused (the
control).

Accepted when: `python -m pytest -q` passes in full (count before: 759 passed, 6 skipped, 9 xfailed,
plus yours); `python3 scripts/check_spec.py` prints its known finding (03-kernel.md:190) and the
counts; `python3 scripts/project_principles.py --check` ok; `luthier certify` over every
`tests/tester/*.test.lut` reports every line known with no store changed (md5 before and after);
the sonolocalización run that was `luthier run examples/sonolocalizacion/experiment_zero.lut`
(with the same `--set` its last record shows, if any) is accepted as a `.run.lut` up to the
certification check (do not run the fit to the end: stop it with `--time-limit 30` and say what the
record shows). You are the only agent working in the repository; commit in small two-line commits
ending with "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>", the renames apart from the
edits. Report: `record/IA/code-follows-2026-10-16/report-file-kinds.md`, by shell heredoc,
committed: what you built, the renames (old and new paths), the checks' output, decisions taken on
your own, at most one question.
