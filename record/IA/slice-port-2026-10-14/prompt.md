# The port of validate_graph.lut and distance_graph.lut: brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-1b). Step 3 of
`record/plan/sonolocalizacion/plan-sonolocalizacion-2026-10-13-execution.md`, first stage of the
slice (the inventory, `record/IA/sonolocalizacion-inventory-2026-10-13/inventory.md` §1 and §6;
the answers of the sonolocalización session, `answers-2026-10-14.md`, item 3: every construct and
library name the two files use; the slice's theories, `record/IA/slice-theories-2026-10-14/report.md`,
"Port notes").

## The prompt

Read `CLAUDE.md` first, then the three documents above (the inventory's §1, §2 rows marked (v)
and §6 only), then `docs/spec/02-grammar.md` for the current syntax and `examples/hello.lut`,
`tests/run/*.lut` for how a program with actions and imports is written today. The sources are
read only, in `/home/lmoffatt/Projects/sonolocalizacion/prototipo-cero/luthier/`:
`validate_graph.lut`, `distance_graph.lut`, `distance_graph_python.lut`, `positions.lut` (only
what the first stage needs: `pairDistance`, `distanceJacobian`, `flatten`, `Design`, `PairsAmong`),
and `src/distance_graph.py` (the fast check and `row_text`, for what the externs did). Change
nothing there.

Write here, under `examples/sonolocalizacion/` (new): `distance_graph.lut` (the graph record, the
invariants, `Violation`, `ValidDistanceGraph`, `firstViolation`, `describe`), `positions_slice.lut`
(the four or five definitions of positions.lut the stage needs), `validate_graph.lut` (`main`),
in the current syntax: `fn` lambdas, braced sums `{ a : A || b : B }`, blocks for `let`, named
imports (`import "tables.lth" Table hasColumn intAt realAt textAt firstFailing`, `import
"tables_model.lut" csv : Codec`, `import "arrays_model.lut" numpy : Arrays`, the theories of
`src/luthier/lib/`), `vec`/`mat` constructors for the tuple literals, `retainedRank` with its floor
first, every name of v0.1 kept where the new theories keep it (the answers' list). Reading the
graph is an action (10.S3): `readGraph (w : W) (dir : String) : W * Maybe DistanceGraph` reads the
two files as text through the host (`host.readFile`, `world_model.lut`) and parses them with
`csv.parse`; `main (w : W) : W * Unit` prints the same lines v0.1 printed (`FAIL <Name>...`,
`valid: N nodes, ...`, from the answers' item 2) with `host.print`. `graphDir` has no `--set` yet
(12.S18): define it in `validate_graph.lut` as `"examples/sonolocalizacion/A/graph"` with a comment
that `--set` replaces it, and copy session A's `nodes.csv` and `measurements.csv` from
`sonolocalizacion/prototipo-cero/2026-09-07/derived/A/graph/` to `examples/sonolocalizacion/A/graph/`
with a `SOURCE.md` naming the file, the commit of sonolocalización you read them at (`git -C
/home/lmoffatt/Projects/sonolocalizacion log -1 --format=%H`), and that they predate
D-2026-10-06-sa/sb (the answers, item 1).

Then: every file must pass `PYTHONPATH=src python3 -m luthier.cli parse`; run `PYTHONPATH=src
python3 -m luthier.cli check` on each (report, do not fix check.py); run `PYTHONPATH=src python3
-m luthier.cli run examples/sonolocalizacion/validate_graph.lut`. It will most likely stop in the
elaborator, the kernel or the bridge (other agents are on run.py's bridge for arrays and tables
right now, and kernel bite 9 just landed): report exactly where and on what, with the smallest
program that reproduces it, and do not change `src/luthier/*.py`. Commit your files as they are
done, one commit each (`git add` the path; never `-A` or `.`; messages naming the spec items,
ending with "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"). Report to
`record/IA/slice-port-2026-10-14/report.md` (commit it): what was a rename, what was more, every
reading where the spec or the theories did not decide, and what stopped the run.
