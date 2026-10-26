# Report: five fixes after the night of 2026-10-26

2026-10-27, Claude Opus 5.5, an agent of the coordinating session, on its brief (five items, then re-certification and the suite). Base commit d0d5f38; commits 6142e9d..f0e259b. Committed by the coordinator from the agent's hand-back (its Write was refused), with the agent's two corrections. Logs under ~/.cache/luthier-fixes/.

## 1. `prune` evicted entries across programs (e66395c)

`_group` keys a group by the law and the binding's generator names; within it, `prune` kept only the entries at the current stamp (cone hash plus fingerprints). belief_controls.test.lut and fit_controls.test.lut each define a `giveUp : Maximizer` with its own body and both write `QuadraticConverges`'s control into belief.cert.json, so each write dropped the other's entry and each program re-ran the line every pass. Change (proposed): within a group, an entry is stale only when its cone hash differs. Entries at a stale hash go once there is one at the current hash; at the current hash, entries are split by fingerprints, each set keeping its `keep` most recent plus every failure, confirmed control and disputed pair; a group with no entry at the current hash keeps only its latest. `_group` and `_stamp` unchanged. This is spec 6.S8 ("an entry is kept per filling of the holes its cone depends on, up to four"). certification.lth's `Pruning` says nothing about the grouping, so its three laws read the same; the comment beside `keepCurrent` in certification_model.lut is updated. Test: `test_two_programs_binding_one_name_to_two_bodies_keep_both_entries` (failed on the old prune, passes now). Consequence: a failure whose fingerprints no program binds any more stays at the current hash until the cone changes or it is removed by hand (6.S3; bite 13c); passing entries under old fingerprints also stay, at most four per set; no bound on the number of sets.

## 2. `ExtendedIsAnObject` on `nothingEqual` (368e8dd)

`leqPairs` and `leqChains` pass the type check but their values are outside `Related Extended nothingEqual.eq` (NotRun "a value outside ..."). An equality that relates nothing has no pairs and no chains, so the line binds `nothingPairs : List (Related Extended nothingEqual.eq) := []` and `nothingChains : List (Chain Extended nothingEqual.eq) := []`: `Reflexive` refuted at x = finiteDistance 0.0; `Symmetric` and `Transitive` NotRun ("the census ... is empty"), holding vacuously. The control means `nothingEqual` breaks reflexivity and nothing else. Second pass 0 lines in bases_controls.

## 3. An integer literal in arithmetic (6142e9d, eb82fbd, fd24ff2)

D-2026-10-26-a: elaborate.py's `numeric_literals` runs before `operator_use` for `+`, `-`, `*`, `/`, `mod`: with a `Float64` operand, an integer literal (or a negated one) on the other side becomes the `Float64` it denotes; two `Int`s stay `Int`s; a named `Int` beside a `Float64` is still refused. Test `test_an_integer_literal_in_arithmetic_takes_the_other_operand_s_float64` (failed before). Spec 4.R9 sentence (fd24ff2); D-2026-10-26-a's status names the commits (eb82fbd). No cone moved; the lines re-run in pass 1 are explained by host hashes of certify.py and run.py (items 1 and 4).

## 4. The bare `luthier eval` on `Extended`'s labels (8b384a0)

In run.py, `_sums_named` finds the aliases of a sum whose labels the slice names; `_probed` makes them roots of the slice and gives each to the kernel as a datum. Only the probe (`eval`, `session`) does this; `run`'s and the tester's slices are untouched, so no cone moves. `luthier eval src/luthier/lib/core/structures/equality.lth "finiteDistance 0.0 == infiniteDistance unit"` prints `false`. Test `test_eval_of_a_bare_term_reads_the_labels_of_an_aliased_sum`.

## 5. The tape example's controls (3835f7e)

`test_the_tape_example_lists_its_controls_per_conjunct` now checks the conjunct counts (4 and 5) and that none is uncontrolled (report-controls-E.md).

## Checks

- Certification: `/home/lmoffatt/miniconda3/bin/luthier certify --jobs 1` over the 54 test programs, six at a time. Pass 1 ran lines in fit_controls (1), plan_controls (10), plan_laws (10), certification_route_controls (10), certification_route (8). Pass 2 ran 0 lines in all 54. rc 1 on cases, belief_laws, laws and vacuity in both passes (known refutations). Stores in f0e259b.
- Suite: each tests/test_*.py by itself under `timeout 1800`. Every file passes under miniconda's Python, the one the stores were certified with; test_lm, test_run and test_certify re-run that way at f0e259b: 10, 159 and 90 passed. test_check_private collects no tests (rc 5). A first full run under pyenv's Python 3.13.2 (numpy 2.4.6) failed 7 tests: test_lm's host maximizer and six numpy runs in test_run. 6.S8 hashes an extern into an installed package by the package's version, so the numpy laws of arrays.lth get other cones under numpy 2.4.6 than the stores hold under 1.26.4 (DotSensitive at be69320c356f against d05fc8f8a8ef), and the runs are refused as stale. The same failures occur at d0d5f38, 6142e9d and 8b384a0, each checked in a worktree with PYTHONPATH set to it.

## The 7 failures under pyenv's Python

The coordinator asked for a bisect, suspecting item 3 or item 4. The host-maximizer test fails the same way at d0d5f38 and at every commit tried, with the code imported from the worktree, and passes at HEAD under miniconda's Python. `host_hash` (certify.py) identifies a route into an installed package as "<dist> <version>", and that hash enters the cone (6.S8). A suite has to run under the interpreter the stores were certified with, or the laws that call into numpy read as stale. Nothing was changed for this.

## Decisions taken on my own

- Item 1: an entry is stale only by its cone hash; fingerprint sets kept apart, no bound on their number (e66395c undoes it).
- Item 2: empty censuses typed against `nothingEqual.eq` (368e8dd undoes it).
- Item 4: the probe gives the sum to the kernel as a datum; `runtime_slice` unchanged.
- The arithmetic sentence in 4.R9 (fd24ff2) and D-2026-10-26-a's status line (eb82fbd).
