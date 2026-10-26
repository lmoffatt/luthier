# Kernel, 2026-10-27: the recursion depth and the substitution's cost

Claude Opus 5.5, on the coordinator's brief of 2026-10-26 (report-night-V.md findings 1 and 2; report-bite-12a.md item 5). Base commit 5d374dd. Commits: abc85ac (kernel), fc31823 (depth tests), 2817bdb (the regions test's marker); the run.py fix delivered as commit 0946bf8 of a scratch clone and as `~/.cache/luthier-kernel/0001-Runner-whnf-force-a-pattern-s-demand-operands-and-va.patch` (applied here afterwards, see the addendum). Committed by the coordinator from the agent's hand-back (its Write was refused).

## 1. Recursion depth: it is in run.py, not in the kernel

A traceback of `PrecisionSymmetric` on `priorA` at 5d374dd is 995 frames, 972 of them `Runner.whnf` (run.py:1580) and `Runner.force` (run.py:1570) alternating. The kernel's own functions already ran on explicit stacks (`kernel._run`); a kernel-only right fold over 3000 cons cells reduces at 5d374dd. The depth comes from the Runner's call by need: a right fold demands its right operand inside `operands` before `+` steps (`foldFrom` over a 30 by 30 matrix's 900 entries); and a recursion whose accumulator is shared and never demanded (`count (k - 1) (acc + 1)`, the native driver's state over 500 iterations) builds a chain of `Shared` cells forced one inside the other. Fix (the clone): `Runner.whnf`, `force`, `demanded_pattern`, `operands` and `value` became generators yielding their demands, run by one loop over a list (`_evaluated`), as `kernel._run` does; public methods keep their signatures; evaluation order, fuel (`spend` once per loop iteration) and the call-by-need schedule unchanged. `EVALUATION_DEPTH` (10^6 generators) bounds the list, so a self-demanding value still stops with a RecursionError (P11). Cost about 7% on `TheThreeSourcesGrade` (17.6 s of CPU against 16.4 s for its first 30 cases). Tests in tests/test_kernel_depth.py (fc31823): a right fold of 3000 (`foldList`), a 3000-step recursion with a lazy accumulator, the core's `sumTo 3000`, `EVALUATION_DEPTH` as a parameter; all four raise RecursionError at 5d374dd and pass with the clone's run.py (committed here as strict xfail until applied); a fifth, a kernel-only fold of 500, passes on both.

## 2. The substitution's cost (abc85ac)

Profile before (cProfile of `TheThreeSourcesGrade`, 270 exhaustive cases, no store, 5d374dd, load 9 to 14): 2000 s under the profiler; `kernel.step` 12.1 million calls, 1829 s; `substitute` 4.0 million, 1393 s; the free names through the identity memo 778 s; `_all_names` 136 s; `_run` 16.1 million calls (the memo cleared every 4096 terms, terms fresh at each step). Changes, same algorithm and result: the free names and all names kept on the term itself (in its `__dict__`, which equality and hashing never read; a term is immutable, so no cap; the identity memo gone; pattern names likewise); the substitution skips subterms where the name is not free and recurses on the Python stack up to `RECURSION_DEPTH` (200), then redoes the work on its explicit stack (on `_Deep` or a RecursionError); `step` skips `_step`'s generators where nothing is demanded (beta at the head of a spine, delta at the head except `and`/`or`, zeta, a record value's projection, a value's no-step, a match whose scrutinee needs no step); a match whose bound values are closed substitutes each binding once. A test compares `step` with `_run(_step(...))` on 2400 random terms. Differential check against 5d374dd's kernel on two seeds: 80,000 random substitutions, 640,000 steps and 80,000 fuelled reductions, no difference, fresh names included.

| | before | after |
|---|---:|---:|
| profiled total | 2000 s | 696 s |
| `kernel.step` (cumulative) | 1829 s | 534 s |
| `substitute` | 1393 s | 386 s |
| free names | 778 s | 220 s |
| all names | 136 s | 35 s |
| `_run` calls | 16.1 million | 1.2 million |

Without the profiler, the first 30 cases take 15.9 s of CPU against 49.3 s: about three times faster per case. The regions test (test_certify) still takes 41 minutes of wall time and 25 of CPU on the loaded machine (its two files 91 minutes summed before, 31 after), so its `LUTHIER_SLOW` marker stays with new figures (2817bdb).

## 3. Outcome comparison: the first kernel edge (D-2026-10-27-a)

Two clones at 5d374dd, one with the new kernel.py; each ran `luthier test --no-cert` on every tracked `*.test.lut` (59 programs) with `PYTHONPATH=<clone>/src` and miniconda's Python. Record: `~/.cache/luthier-kernel/edge-5d374dd-kernel-abc85ac.json` (written by `compare_outcomes.py`, runner `runall.sh`, beside it), with both kernels' sha256, the programs, and per program each line's law, mode, case count and outcome, the other lines and the exit code. kernel.py at 5d374dd: sha256 81c0e039b25a2d055a8a35f7376803775072c97c1b2205436d8f31f12fc0ae53; as tested 88019c7f18b98a572d263e28f6253739d8980325c1813ce6e4e36cbf00f515bd; as committed in abc85ac (plus a 4-line header comment) 8c41390d67b5d34ff83c4b6cdbe2912c8cbd1bd186b459916e162868e9368522. Result: 59 programs, 508 law lines and 3090 other lines (2687 control, 401 conjunct): every law line has the same law, mode, case count and verdict; every other line and exit code identical; four lines differ only in the reason text of a failure that is the same on both sides (`PosteriorInfoSymmetric`, `StepMatrixSymmetric`, `InfoSymmetric`, `ProfiledIsGaussianAtItsSigma`, each "unsettled: 20 cases raised" by Python's recursion limit in run.py; the kernel now finishes its own recursion on its explicit stack, so the Runner fails a little further on). Summed wall time 42,943 s before, 22,296 s after (shared machine). With the clone's run.py too (`runner-depth-after-kernel-abc85ac.json`): exactly five lines change, from unsettled by the recursion limit to settled: `PrecisionSymmetric` on `priorA` (exhaustive, 1 case), `PosteriorInfoSymmetric` on `posteriorA`, `StepMatrixSymmetric` on session A (optimization_laws now exits 0), `InfoSymmetric`, `ProfiledIsGaussianAtItsSigma` (20 cases sampled each); every other line identical; 16,157 s summed.

## 4. Where a case's steps come from

Method: `kernel.step` and `Runner.apply` wrapped, one case of `TheThreeSourcesGrade` (the 101st of 270; the first makes 16,000 step calls, the 201st 382); each lambda tagged with its definition, a beta step attributed to the definition whose lambda it consumes; a binder of type `U` (or `U -> U`) counted as a type argument. That case makes 58,375 calls of `kernel.step`; 32,436 (56%) give no step (the Runner asking about a term already in weak head normal form: a lambda 15,363 times, a constructor or declared name 8,406). The 25,939 steps:

| kind | steps | share |
|---|---:|---:|
| beta, value argument | 11,351 | 44% |
| beta, type argument | 4,176 | 16% |
| delta | 3,458 | 13% |
| projection | 2,987 | 12% |
| match | 2,851 | 11% |
| primitive (`==` 685, `<` 100, `<=` 48) | 833 | 3% |
| `and`, `or` | 283 | 1% |

By origin: the law's own logic about 3,000 steps (12%: certification.lth, certification_model.lut, test.lth and the test file, 2,619 betas, plus about 200 matches on the certification's data); the elaboration's generic, dictionary-passing route about 19,000 steps, three quarters of the case (core/lists.lut's generic functions take 12,750 of the 15,527 betas; `foldList` alone 8,052, six parameters, two of them types, unfolded 1,342 times; then combineList 1,498, filter 1,366, any 370, singleton 340, mapKernelList 300, nth 300, lengthList 200; all 4,176 type arguments theirs; the projections mostly fields of structure records passed as dictionaries); data representation about 3,300 (13%, overlapping: 1,816 matches on cons/nil, `if` as a match 609, `Maybe` 226; the 685 `==` mostly compare names); recomputation: of 3,506 applications of a top-level function, 624 (18%) repeat an earlier call with the same argument objects (a lower bound). Natively: about 1,300 list elements visited, 830 comparisons, a few hundred calls of the law's functions and 200 matches, 2,000 to 3,000 elementary operations, ten times fewer than the kernel's 26,000 steps; in time, a kernel step costs about 24 µs (76 µs before), so a case takes about 0.5 s against about a millisecond natively.

## Findings

1. The recursion depth is the Runner's (run.py); its fix is 0946bf8 of the clone and the patch in ~/.cache/luthier-kernel/.
2. fit_controls.test.lut runs `neverAccepts` under `settingsTwenty` because of this depth (report-night-V.md finding 2); with the run.py change a 500-iteration budget should run.
3. run.py:1287 calls `kernel.free_names`, uncached, walking the whole term, on every candidate of one of its rewrites (57,000 calls and 3 s of 111 in certification_laws); `kernel._cached_free_names` gives the same set.

## Decisions taken on my own

The free names on the term (`__dict__`), term.py untouched; recursion to `RECURSION_DEPTH` = 200 with explicit-stack fallback; `step`'s fast paths guarded by an equivalence test; a match with closed bound values substituting once per binding; run.py left alone here, its tests strict xfail, its fix delivered as a patch; `EVALUATION_DEPTH` = 10^6; the regions test keeps `LUTHIER_SLOW`; the edge record's format (`compare_outcomes.py`) until the edge store is built.

## Question

Apply the run.py commit now, or hand the patch to the agent working in run.py? Coordinator's answer (2026-10-27): apply it now, no agent works in run.py.

## Addendum: the run.py fix applied (2026-10-27)

Commits: 9fa103d (the Runner's `whnf`, `force`, `demanded_pattern`, `operands` and `value` as generators on an explicit stack bounded by `EVALUATION_DEPTH` = 10^6, applied with `git am` from the patch; strict xfail marks removed); 26fedc4 (finding 3: run.py's eta reading asks `kernel._cached_free_names`); e7588dc and 996a0e4 (finding 2: fit_controls' `LMStepsOnQuadratic` control on `neverAccepts` runs under session A's 500 iterations and is refuted at its first case, exhausted far beyond the allowed steps; `settingsTwenty` removed); 00d78d6 (stores re-certified: session_a, belief, laws, optimization, probability). Certification needed four passes: a plain pass ran nothing (the old unsettled outcomes were stored at unmoved cones); a `--deep` pass ran every line and three files returned 1, the replay rule (D-2026-10-15-f) refusing the five newly settled lines against their old unsettled entries at the same seed and n; a second `--deep` pass on those three resolved it (a later run agreeing with the latest); a final plain pass ran 0 lines in all seven files, all rc 0, belief_laws included. Checks: test_kernel.py and test_kernel_depth.py 84 passed; in a clone after 996a0e4, test_kernel, test_kernel_depth, test_run, test_tester and test_certify 366 passed, 6 skipped, 2 xfailed (in test_run). Decisions: the control at 500 iterations with `settingsTwenty` deleted; the replay disagreement resolved by a second `--deep` run rather than by removing entries by hand.
