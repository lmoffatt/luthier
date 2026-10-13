# kernel.py, bite 10: /= on every concrete type, constructors of parameterized data, brief

Written 2026-10-14 by the coordinating session (luthier-1b). On run bite 5's report
(`record/IA/run-2026-10-13/report-5.md`, "Where validate_graph.lut stops next" and "Found on the
way"): validate_graph.lut stops on `"mic2" /= "mic1"`, and `[1, 2] == [1, 2]`, `just 1 == just 1`
are stuck because core's `Maybe` and `List` are parameterized data and the kernel reads
constructors only from a `data` body at the top level of a definition.

## The prompt

Read `CLAUDE.md` first, then that report's two sections, then term.lth §5 at its latest commit
(`git log -1 -- src/luthier/lib/term.lth`: `PrimString`, `PrimConstructors`, `EqualityStuck`) and
`src/luthier/lib/core.lut` (`Maybe`, `List` as parameterized `data`), and `docs/spec/04-static-semantics.md`
4.R8. Other agents edit `check.py` and `tests/test_check.py` meanwhile: change only
`src/luthier/kernel.py`, `src/luthier/cli.py`, `tests/test_kernel.py`, `tests/test_run.py` (one
test), and term.lth §5 only to append a `gives` to `PrimString` (luthier-03 is paused; say so).

1. `/=` on two `StringConst` steps to the truth of their difference (4.R8: `==` is one operation
   on every concrete type; `/=` is its negation there). Append the `gives` to term.lth's
   `PrimString` beside `==`'s, cite 4.R8 above it, mark it `[proposed]` in the comment. Then
   `/=` on every pair of values `==` compares (pairs, records, injections, constructors) steps to
   the negation of `==`'s answer, under the same demand of parts (EqualityDemandsParts); a `gives`
   for that beside `PrimStructural`, `[proposed]`.
2. Constructors of a parameterized `data` (`Maybe (A : U) = data { nothing ; just : A -> Maybe A }`
   or however core.lut writes it: read it) are constructors of the program for `PrimConstructors`
   and for `match`: the kernel reads them through the definition's binders. Tests: `just 1 ==
   just 1`, `[1, 2] == [1, 2]`, `nothing /= just 1` in `eval` and in a `run` program.
3. `luthier run`'s default fuel: 10,000 is a hundred times too small for validate_graph.lut.
   Raise the default of `run` (cli.py) to 10,000,000, as a parameter still (`--fuel`), noted
   `[proposed]` in the help text; `eval`'s default unchanged.
4. Then `PYTHONPATH=src python3 -m luthier.cli run examples/sonolocalizacion/validate_graph.lut`
   from the repository root, in the background (about 5 minutes): paste its output line in the
   report, and the wall time. Add a test in `tests/test_run.py` that runs it, marked slow
   (`@pytest.mark.slow` if the suite has the marker, else skipped unless `LUTHIER_SLOW=1`), with
   the expected line.

Check: `PYTHONPATH=src python3 -m pytest tests/test_kernel.py tests/test_run.py -q`, then
`PYTHONPATH=src python3 -m pytest tests -q`. Do not commit. Report in your final message (the
harness may refuse a report file; the coordinator saves it).
