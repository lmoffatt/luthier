# run.py bite 9: a bound value is demanded once (call by need, 8.S4), brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-3e). On the fit host agent's finding
(`record/IA/fit-host-2026-10-14/report.md`, "Finding worth attention"): the Runner passes
arguments unevaluated, so a `:=`-bound host call (`r := lm.maximize ...`) is re-run at every
projection of `r` (three fits instead of one); only a one-arm `match` forces it once. In the fit
every projection of a `laplaceMode` result would rerun the maximizer.

## The prompt

Read `CLAUDE.md` first, then that finding, `docs/spec/08-*.md` 8.S4 (call by need: a value is
computed when first demanded and kept; what is kept and keyed by what) and 3.S25 (each entry of
a materialized lambda evaluated once), `src/luthier/lib/term.lth` §5 where `Let` steps (and
whether it states sharing: say what it says), and `src/luthier/run.py` (`Runner.whnf`, `Let`,
`App`, how arguments are substituted). Another agent ports `.lut` files under
`examples/sonolocalizacion/` meanwhile: change only `src/luthier/run.py`, `tests/test_run.py`,
programs under `tests/run/`.

Make the Runner demand a `Let`-bound value once: when a `Let x := v in b` is reduced, `v` is not
substituted as a term but bound to a thunk that is reduced to weak head normal form at the first
demand and then shared by every later use (a `Var x` reaching the thunk), and the same for an
argument of an application when the function's body uses its parameter more than once (if that
is what 8.S4 asks; if 8.S4 speaks of the entry store across runs rather than within a run, say
so and do only the within-run sharing, marked [proposed]). The kernel's `step` (the specimen of
term.lth's definitional equality) is unchanged: the sharing lives in the Runner, which already
drives reduction with the host. Tests: `r := lm.maximize ...` projected three times counts one
maximize (the counts of `x.run.json`); a `Let`-bound `host.readFile` observed twice reads once
(host.observe or a counter); the 32 earlier run tests, `maximize_quadratic.lut` and
`validate_graph.lut` (under `LUTHIER_SLOW=1`, in the background: paste the wall time before and
after, since sharing should make it faster) unchanged in their output.

Check: `PYTHONPATH=src python3 -m pytest tests/test_run.py tests/test_lm.py tests/test_tester.py
-q`, then `PYTHONPATH=src python3 -m pytest tests -q`. Do not commit. Report in your final
message: what is shared and keyed by what, what 8.S4 and term.lth say, the timings.
