# Two runs of the fit on session A, 2026-10-14 evening

Run by the coordinating session (luthier-3e) at commit 69c78ad of this repository, on the graphs
copied under `examples/sonolocalizacion/A/` (their `SOURCE.md` names the sonolocalización
commit; both predate D-2026-10-06-sa/sb there). The command, for each graph `G`:

    PYTHONPATH=src python3 -m luthier.cli run examples/sonolocalizacion/experiment_zero.lut \
      --set graphDir=examples/sonolocalizacion/A/G --set outDir=<scratch> \
      --set lmMaxIter=500 --set lmTol=1e-12 --set lmFloor=<3N eps> --fuel 100000000000

with `lmFloor` 6.661338147750939e-15 for `graph` (N = 10) and 5.995204332975845e-15 for
`graph_noA2` (N = 9): v0.1's n eps. The outputs are `fit-A-graph.txt` and `fit-A-graph_noA2.txt`,
verbatim (stdout: the three tables after a `== <path>` line each, then the summary line).
Uncertified (12.S17 not enforced). Luciano's decision on the A2 block is open; this is Luthier's
output on the two files, not the analysis's result.

## A certified run, 2026-10-15

`fit-A-graph_noA2-certified.txt`: the same command on `graph_noA2` at commit 871ea67 (the
stores of src/luthier/lib/ at revision v0.2 serving every law in the cone; `run` strict,
12.S17), with `--fuel 100000000000` (the default fuel of 10,000,000 is spent before the fit
converges; a first attempt at the default stopped with "fuel spent" after 2 min and is not
kept). Its record is the last entry of `examples/sonolocalizacion/experiment_zero.run.json`
(ignored by git), with the certification state of the cone: 83 laws, 6 certified, 175 names
vacuous, none uncertified, stale or failed.

## The figures, 2026-10-15

`figures/positions.png`, `residuals.png`, `transform.png`: the three plots of G4
(record/plan/plots/plan-plots-2026-10-14-decisions.md) that `experiment_zero.lut` at fd498a9
renders with `figures.lut` at 8e0ab62, by the command above on `graph_noA2` with `--set lmTol=1e-6`
and `--set outDir=<scratch>`, run in a worktree at 325a709 holding those two files (the library at
HEAD then refused the cone: numpy's `PinvRestricts` stale after 6157fbc changed arrays.lth), 3 min;
its summary line: sigma 0.02214331908164216 m, nu 4.471102722862414, Kolmogorov distance
0.17285053266082867 over 19, tail probability 0.5794153448510095. matplotlib 3.11.1.
