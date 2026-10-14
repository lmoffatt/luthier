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
