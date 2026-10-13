# The inventory of sonolocalización

Step 1 of `record/plan/sonolocalizacion/plan-sonolocalizacion-2026-10-13-execution.md`, on
D-2026-10-13-ac. Written 2026-10-13 by Claude Opus 5.5, a subagent of the coordinating session, on
the brief `record/IA/sonolocalizacion-inventory-2026-10-13/prompt.md` (committed at a93c6ad).

Inputs. Sonolocalización at 5ffc36e (read only; its working tree had one modified file of
Luciano's, untouched and unread). Luthier at ac29b54 with uncommitted edits of other agents in
`src/luthier/parse.py`, `surface.py` and `run.py`; the v0.1 libraries were read at the tag
`v0.1-final` (fd3cba9). The certificates of sonolocalización were made at 487406d
(`prototipo-cero/luthier.lock`); between that commit and `v0.1-final` the libraries this analysis
imports are byte-identical except `algebra.lut` (38 lines), so the line numbers given for `real`,
`array`, `table`, `probability`, `belief`, `optimization` and `random` hold at both. Nothing was run
in sonolocalización. Two things were run here, in the scratchpad: the new parser
(`python3 -m luthier.cli parse`) on copies of the twelve `.lut` files, and small read-only Python
one-liners (`python3 -I`) that counted rows of `distancias.csv` and outcomes in the `.cert.json`
files. Paths are relative to `~/Projects/sonolocalizacion` unless they start with `src/luthier`,
`docs/spec` or `record/`, which are this repository's; `v0.1:x.lut:n` is line n of
`src/luthier/lib/x.lut` at `v0.1-final`.

What comes from the sources is cited by file and line. What I propose is marked "Proposed".

## 1. The analyses

What the repository runs, one line each, with its entry point:

| analysis | entry point | Luthier? |
|---|---|---|
| Acoustic self-calibration of the array, stages 00 to 04 (manifest, code detection, fine arrival times, blind calibration of positions and clocks, comparison with the tape) | `analisis/run_pipeline.py --session A` (`analisis/run_pipeline.py:16-17`, `README.md:65`) | no |
| The same with the phone's two loudspeakers in the model (stage 3b, then stage 4 on it) | `analisis/03b_calibrate_two_drivers.py`, `analisis/04_validate.py --calibration 03b` (`analisis/04_validate.py:27-29`) | no |
| What a recorded pulse is made of (copies of the code, their lags and amplitudes) | `analisis/05_two_drivers_figures.py` | no |
| Diagnostic figures of stages 1 and 2 | `analisis/01_plots.py`, `analisis/02_plots.py` (run by `run_pipeline.py` unless `--no-plots`) | no |
| Likelihood-based library for the correlation trace, with its tests | `sonolik/` (`sonolik/__init__.py:1-31`), tests `pytest sonolik/tests` | its Luthier layer (`sonolik/luthier_env.py:27-30`) loads files that were archived; `sonolik/tests/test_laws.py` fails today (`README.md:116`) |
| Check of the two-loudspeaker hypothesis on session A | `python3 -m sonolik.check_two_drivers --session A` (`sonolik/check_two_drivers.py:27-30`) | no |
| Positions of phones and speaker placements from the tape distances, a maximum a posteriori fit with a Laplace posterior, session A | `prototipo-cero/src/prepare_experiment_zero.py`, then `luthier run luthier/validate_graph.lut`, then `luthier run luthier/experiment_zero.lut` (`README.md:77-81`), with two control entries `priorWidened` and `sigmaKnown` (`experiment_zero.lut:16-28`) | yes, v0.1 |
| Certification of the positions model and its pieces (likelihoods, Levenberg-Marquardt, Laplace, graph invariants) | `luthier test luthier/<file>.lut --imports --seed 20261005` (`README.md:99`) over the ten files of `prototipo-cero/luthier/` | yes, v0.1 |
| The older three-dimensional positions fit in Python | `prototipo-cero/src/positions_from_distances.py` (a module, no entry point; nothing of the Luthier layer uses it, `docs/decisions.md:42-44`) | no |
| Design of experiment zero: the audio battery, the draw of speaker positions, the figure, the dome geometry | `generar_audio.py`, `sorteo_posiciones.py`, `figura_geometria.py`, `analisis/geometria_domo.py` | no |
| Integrity of the raw data (sha256 manifests) | `bash lint/manifests.sh` (`README.md:58`) | no |
| Voice notes to ideas (extract, consolidate, mentor; calls the `claude` or `codex` command line) | `scripts/extract_ideas.py`, `consolidate_ideas.py`, `mentor.py` (`PIPELINE.md`) | no |

**The smallest end-to-end case: the positions from the tape, session A.** Data in:
`prototipo-cero/2026-09-07/distancias.csv` (24 KB, 37 valid readings for session A). Result out:
`positions.csv`, `residuals.csv`, `transform.csv` and one summary line with the tape error
(`experiment_zero.lut:10-14`, `:174-180`). Why this one:

- It is the only analysis written in Luthier, so it is the only one that tests what the plan wants
  to test: running and certifying Luthier code on real work. The acoustic stages are Python with
  scipy over 3.8 GB of audio and state no laws; porting them would be a rewrite, not a run.
- Its laws already exist and cover every kind of evidence the plan has to design (§3): exact
  Boolean checks, sampled type obligations, agreement within a rounding tolerance, exact bitwise
  agreement, statistical laws with a declared ensemble, and negative controls.
- Its Python side needs numpy only (§2, row 34). The Jacobians are analytic
  (`positions.lut:47-53`), so S3's question (JAX for gradients) does not arise for this slice.
- `analisis/04_validate.py` is smaller (two small inputs, one comparison) but has no Luthier code and
  no law, so running it in Luthier would exercise nothing the plan needs. I rejected it for that
  reason.

Proposed: run it in two stages. First `validate_graph.lut` alone (`validate_graph.lut:39-43`):
it reads the graph, checks its invariants and reports the directions the distances do not see.
It needs the table reader, the invariants, the native Jacobian and one numpy leaf (`retainedRank`),
and none of probability, belief or optimization. Then `experiment_zero.lut`, the full fit. The rows
of §2 marked (v) are what the first stage needs.

The first step, `prepare_experiment_zero.py`, decides which tape readings are measurements and
which are prior (`prepare_experiment_zero.py:7-28`). It is per-experiment Python by design
(`distance_graph.lut:9-11`). Proposed: it stays Python in the slice, run by Luciano, and Luthier
starts at the graph directory.

## 2. What the analysis needs

Kind: **lib** a v0.1 Luthier library, **construct** a Luthier construct, **py** a Python package
or module, **format** a data format, **program** an external program. "Provides" names the spec
item or theory of the new Luthier that covers it, and says "missing" when nothing does yet. "Host
code survives" means the Python file is still in `src/luthier/` as code externs call
(`src/luthier/__init__.py:3-6`) but no theory states it. (v) marks what `validate_graph.lut` needs.

| # | item | where | kind | provides |
|---|---|---|---|---|
| 1 | Tape readings, 16 untyped columns | `prepare_experiment_zero.py:56-58` | format (CSV) + py | outside Luthier (proposed above) |
| 2 (v) | Graph directory: `nodes.csv` (name:str, x, y, z, sx, sy, sz:float) and `measurements.csv` (i, j:int, d:float), the typed CSV of `luthier.tables` | `prototipo-cero/src/distance_graph.py:3-13, 33-43` | format | host code survives (`src/luthier/tables.py`); no theory; missing |
| 3 (v) | `GraphDir`, a subtype whose predicate is an extern that looks at the disk (`isGraphDir`) | `distance_graph_python.lut:54-56`; `distance_graph.py:209-211` | construct | an observation of the world is an action (10.S1, 10.S3); `world.lth` §2 has places, no directory; missing |
| 4 (v) | `readGraph : GraphDir -> DistanceGraph`, an extern that reads two files, typed as a pure function | `distance_graph_python.lut:57`; `distance_graph.py:232-235` | construct + py | must become an action `W -> ... -> W * A` (10.S3); `world.lth:151-167` `readFile` gives text only; the hash of what is read in the identity of the result (7.S16, 8 §4); missing |
| 5 (v) | `Table` and its accessors `hasColumn`, `intAt`, `realAt`, `textAt`, `firstFailing`, `listLength`; the codec laws | `v0.1:table.lut:26-70`; `v0.1:table_python.lut:7-17` | lib | missing (no table theory in `src/luthier/lib/`) |
| 6 (v) | `DistanceGraph` record, the invariants, `Violation` as a sum of records, `Maybe` | `distance_graph.lut:19-106` | construct | type formers (spec 3 §2); braced sums (2.S9, D-2026-10-13-w); `Maybe`, `List`, `Bool`, `Nat`, `Fin` are core's, and core is not written (`program.lth:240` declares `coreNames` only) |
| 7 (v) | Positions as one vector, `pairDistance`, `distanceJacobian`, `positionsModel`, `flatten`; vectors built as tuples `(n, \ k { ... })` | `positions.lut:18-79` | construct (native) | 11.S9 defines `Vec` and `Mat` as records; whether a pair is accepted where the record `{ n, f }` is expected is not stated (unsure) |
| 8 (v) | `Vec`, `Mat`, `VecOf`, `MatOf`, `MatRows`, `Dim` | `v0.1:array.lut:26-30` | lib | 11.R1 and 11.S9 state them; no core or array theory in the new tree; missing |
| 9 (v) | Float64 arithmetic `- * /`, comparisons `< <= > >=`, Int `/` and `mod`, `toFloat64` | e.g. `positions.lut:50-52`, `distances.lut:31-33`, `distance_graph.lut:55` | construct (core) | spec 11 §2; `src/luthier/kernel.py:485-501` computes Int `+ * - == <`, Float64 `+`, String `==`, nothing else; missing |
| 10 | `sqrt`, `log`, `exp`, `erf`, `cbrt`, `abs`, `ulp` | `v0.1:real.lut:8-23`, `v0.1:real_python.lut:5-12` | lib (externs to Python's `math`) | 11.S2 (a leaf declared over what it receives); `python:` routes run (`run.py:65-71`); the theory is missing |
| 11 (v) | `+ - *` on vectors and matrices, resolved by `operator` | `v0.1:array.lut:355-364`; used `experiment_zero.lut:119, 145`, `distance_graph.lut:144` | construct + lib | 2.R2 (a type names its model), 4.R13; the leaves are missing |
| 12 (v) | `transpose`, matrix product, `retainedRank` (v); `trace`, `dot`, `norm`, `pinvSym`, `mscale`, `zeros`, `identity` | `v0.1:array.lut:318-352`, `v0.1:array_python.lut:11-58` | lib (numpy externs) | 3.S28, the pattern 12.S9; host code survives (`src/luthier/arrays.py`); theory missing |
| 13 (v) | The rank floor `n eps` times the largest eigenvalue, a criterion written in the library | `v0.1:array.lut:150-154` | lib | P11 (every criterion is a parameter) is not met there; 11.S18 says such tolerances become measured costs; missing |
| 14 (v) | Run parameters `graphDir`, `outDir`, `lmTol`, `lmMaxIter`, `horizontalWidening`, `fixedSigma`: declared holes filled by `run --set` | `experiment_zero.lut:46-54`; `validate_graph.lut:21` | construct + tool | 3.S9 (a declared name is a hole), 8.S1 (the demand sets holes), 12.S18 (implemented at v0.1 only); the new `run` has no `--set` (`src/luthier/cli.py:25-28`); missing |
| 15 | Entries `main`, `priorWidened`, `sigmaKnown` | `experiment_zero.lut:207-209` | tool (`--entry`) | new `run --main` (`src/luthier/cli.py:27`) |
| 16 (v) | `main : String`, printed, recorded in `x.run.json` with the cone's hash and the parameters | `validate_graph.lut:39`; 12.S18 | tool | printing: `world.lth:151-167`, `world_model.lut:35-39`, `examples/hello.lut`; the run record is missing |
| 17 | Writing the three output tables, `writeTable : String -> Table -> Unit`, an extern with an effect typed as pure | `experiment_zero.lut:57, 201-204`; `distance_graph.py:238-240` | construct + py | an action by its type (10.S3); `world.lth:98-106` has `write` on the representation only; no host write action; missing |
| 18 | Tables built in numpy: `positionsTable`, `residualsTable`, `transformTable`, `nodeNames` | `experiment_zero.lut:59-64`; `distance_graph.py:243-284` | py | needs the bridge for lists, records and arrays (row 23); missing |
| 19 (v) | `intToString`, `realToString`, `joinPath`, `rowText` | `experiment_zero.lut:65, 171-172`; `validate_graph.lut:23-24` | py (builtins, `os.path`) | `python:` routes (`run.py:65-71`); strings cross today |
| 20 (v) | String concatenation `+` | `validate_graph.lut:27-36`; `experiment_zero.lut:175-180` | construct (core) | `world.lth:150` declares `appendStr`; the kernel has none; missing |
| 21 | `MeanModel`, `ScaledModel`, `Likelihood`, `gaussian`, `profiled` | `v0.1:probability.lut:114-120, 275-313`; used `experiment_zero.lut:70, 86-89` | lib | missing; 7.R2 asks that their `(Theta : U)` be rewritten over `VecOf n` |
| 22 | `GaussianBelief`, `laplaceMode`, `laplaceAt`, `Maximizer`, `MaxResult` | `v0.1:belief.lut:110-136`; used `experiment_zero.lut:73-75, 116-117` | lib | missing |
| 23 | `lm.maximize`, the fast Levenberg-Marquardt: Python receives three Luthier functions (log posterior, gradient, step matrix) and calls them back; `lm.py` reads an objective record by attribute | `experiment_zero.lut:95`; `prototipo-cero/src/lm.py:27-44, 94-101` | py + construct (the bridge) | externs as routes (10.S8 to 10.S10); the bridge is 3.S22 to 3.S25 (arrays, lambdas over `Fin n`), implemented at v0.1; functions over an infinite domain crossing in either direction are not stated in the spec; today `run.py:73-115` carries literals, unit, pairs, `Maybe` and records, lists only from the host, no arrays and no functions; missing |
| 24 | `normalCdf` (by `erf`), `kolmogorovDistance` (numpy sort), `kolmogorovTail`, `valueSums` | `v0.1:probability.lut:36, 57-86`; used `experiment_zero.lut:149, 161, 164-165` | lib + py | missing |
| 25 | Obligations of the declared types of externs at the crossing (`nodeNames` returns a list of the right length) | `experiment_zero.lut:59` | construct | 4.R5, 10.S10, 12.S18 (`--checked`); missing |
| 26 | Interpreter pinned by `luthier.lock`, a warning when another runs | `prototipo-cero/luthier.lock`; `README.md:72-74` | tool | 12.S13 (implemented at v0.1); missing |
| 27 | A run refuses an uncertified cone (`--require-certified` at v0.1) | `README.md:92-96` | tool | 12.S17 (decided: strict, no opt-out); there is no `test` command yet; missing |
| 28 | Generators registered by type, `gen T := extern "python:..."`, Python functions `(rng, size, ...)` | `distance_graph_python.lut:43-46, 56`; `distances_python.lut:18-19`; `positions_python.lut:12-14` | construct + py | the act `gen` is removed (2.S19, 7.R1); bindings, census and profiles are `generators.lth` §5 and `test.lth` §1; the calling convention of a Python generator is not stated; missing |
| 29 | Test directives `test X with n` | e.g. `distances_python.lut:97-107`, `experiment_zero.lut:212-214` | construct | `test` as a function (7.S20, `test.lth:53`); the old form still parses; no tester; missing |
| 30 | Statistical laws over an ensemble (`Ensemble`, `DensityPairOn`, `KernelOn`, `CalibratedGaussian`) | `v0.1:probability.lut:34, 216-271`; `v0.1:belief.lut:205-216` | lib | 7.S17 to 7.S19 (decided); `generators.lth:56` has one uniformity law with a level; missing |
| 31 | A generator with effects: `gen_graph_dir` writes graphs to a temporary directory and registers its removal at exit | `distance_graph.py:217-229` | py | no place in the spec: a generator is a value (7.S1), an effect is an action (10.S1); missing (unsure what it should become) |
| 32 | The fast likelihoods and sampler of the certification (not of the run) | `distances_python.lut:23-30`; `positions_luthier.py:59-119` | py | as row 23 |
| 33 | `positions_luthier.py` imports `luthier.generators.EmptyDomain` when a domain is empty | `positions_luthier.py:151, 160, 173` | py (the v0.1 interpreter) | gone from `src/luthier/`; fails only when raised |
| 34 | numpy (and the standard library: `csv`, `math`, `os`, `random`, `tempfile`, `shutil`, `atexit`) | `positions_luthier.py:14-16`, `lm.py:16`, `distance_graph.py:21-26`, `prepare_experiment_zero.py:30-36` | py | an extern's host; the certificate's hash covers the installed package (6.S8); a declared dependency is proposed (spec 12, Open) |

### The constructs of v0.1 it uses, and what the spec keeps

I parsed copies of the twelve `.lut` files with the new parser. All twelve fail. After six
mechanical rewrites in the copies (below, marked "rejected") all twelve parse. Nothing beyond
parsing was tried: the libraries they import do not exist in the new tree.

| construct | where | the spec | today's parser |
|---|---|---|---|
| `\ x { ... }` lambdas | every file, e.g. `positions.lut:23` | changed to `fn x { ... }` (2.S9, D-2026-10-13-y) | rejected |
| `import "real"`, flat | every file | changed: named imports with their theory (12.S22), theory files `.lth` apart from model files `.lut` (12.S23) | rejected |
| `< a : A \| b : B >` sums | `distance_graph.lut:85`, `experiment_zero.lut:84` | changed to `{ a : A \|\| b : B }` (D-2026-10-13-w) | rejected |
| `gen T := extern "..."` | three files (row 28) | removed (2.S19, 7.R1) | rejected |
| `let x = e in body` | `experiment_zero.lut:112-122, 152-159` | retired, replaced by blocks (2.S17, 2.S21) | rejected |
| a refinement whose law starts on the line after `\|` | `distance_graph_python.lut:84-87`, `optimization_python.lut:111-114` | line breaks inside braces are separators (2.S4); I could not tell whether this case is meant to be rejected (unsure) | rejected |
| `x : T := extern "python:m.f"` | rows 4, 17 to 19, 23 | kept, as an application of the core name `extern` (3.S39, 2.S21) | parses |
| `test x with n` | every certified file | kept as the older surface of `test` (7.S20) | parses |
| a declared name with no body as a run parameter | row 14 | kept (3.S9, 8.S1) | parses |
| a declaration in one file defined in another (`kolmogorovDistance`, the array leaves) | `v0.1:probability.lut:76` with `v0.1:probability_python.lut:10`; `v0.1:array.lut:318-352` with `v0.1:array_python.lut:28-58` | retired (12.S8, D-2026-10-13-o): a model is a named value of its theory | not used by the sonolocalización files directly, by every library they import |
| `operator + := add` and its kin | `v0.1:array.lut:357-364` | kept (2.R2) | not tried |
| refinement by a conjunction of laws, laws as lambdas over a domain and a seed | e.g. `distances_python.lut:57`, `v0.1:probability.lut:216-224` | kept (5.S1, 5.S6) | parses |
| laws attached to a declared type, `T := A & B` | `v0.1:optimization.lut:24`, `v0.1:table.lut:51` | kept (`world.lth:92` uses it) | parses |
| types as parameters, `(Theta : U)` | all of `probability`, `belief`, `optimization` | allowed by the kernel; their laws cannot be tested (7.R2), which asks for a rewrite over `VecOf n` | parses |
| `main : String` with no world token | `validate_graph.lut:39`, `experiment_zero.lut:207` | `W` is optional in `main` (D8, cited at `world.lth:9-10`) | parses |
| `Seed` as `Int`, `Gen` over `Int` | `v0.1:random.lut:8, 38` | `Seed` a bounded subtype, `Gen T = Nat -> Seed -> T * Seed` (7.S1, `generators.lth:43-44`) | parses |

## 3. The laws and the evidence each needs

Evidence kinds as the brief names them: **exact** (a Boolean on finite cases), **sampled**
(random cases), **tolerance** (floating point within a tolerance), **statistical** (a p-value, a
z-score or a likelihood), **citation**. Most laws are exact or within a tolerance at each case and
sampled over their domain, so the column gives both when both apply. "v0.1" gives the last outcome
in the file's `.cert.json`.

### In the run itself (results checked once, 7.S16)

| check | where | evidence |
|---|---|---|
| The graph satisfies `ValidGraph` before it is fit; an invalid one is reported, not fit | `experiment_zero.lut:199`; `validate_graph.lut:41-43` | exact, on the data |
| The fit says whether Levenberg-Marquardt converged and whether the measured pairs are apart where it ended | `experiment_zero.lut:105, 124-125, 179-180` | exact, on the result |
| The residuals' transforms against the uniform, Kolmogorov distance and tail probability; reported, never enforced | `experiment_zero.lut:13-14, 151-165` | statistical (with 22 data and 30 parameters it has little power, `:22`; spec 7.S19 shows on the data of 2026-10-06 that it cannot see a problem of scale) |

### The graph and its reading

| law | where | says | evidence | v0.1 |
|---|---|---|---|---|
| `validity` | `distance_graph_python.lut:62-63, 79, 95` | `ValidGraph` accepts every generated valid graph and rejects every graph with one defect (eight kinds of defect, `distance_graph.py:122-153`) | exact per case, sampled 200; the bodies restate the predicates, so what is tested is the generators (`:59-61`) | passed |
| `checks` | `:84-85, 96` | `firstViolation` reports nothing exactly on valid graphs | exact, sampled 100 | passed |
| `fastCheck` | `:86-88, 97` | the Python check agrees with the native one on which invariant fails first and at which row | exact, sampled 200 | passed |
| `translation` | `:69-72, 92, 98` | the Python translation to the fit's arguments equals the native one | exact (tolerance 0.0), sampled 100 | passed |
| `rigidity` | `:76-77, 93, 99` | the distances never see the heights or the three rigid motions; a complete graph in general position sees everything else | exact on integers, sampled 100; rests on the rank floor of row 13, a tolerance inside the leaf | passed |
| `layout` | `positions.lut:78-79`; `distance_graph_python.lut:91, 100` | the 3 x N table and the vector are the same positions (an isomorphism) | exact, sampled 50 | passed |
| `readGraph`'s type | `distance_graph_python.lut:57` | what is read from a directory is a well-formed table (schema, kinds, cells) | exact, sampled 100 over directories a generator writes | passed |
| The type obligations of every definition (indices in `Fin n`, lengths) | `distance_graph.cert.json`, `positions.cert.json` | | exact per case, sampled 100 | passed |

### The likelihood of the distances (`distances.lut`, `distances_python.lut`)

| law | where | says | evidence | v0.1 |
|---|---|---|---|---|
| `samplerFast` | `distances_python.lut:49, 102`; `distances.lut:117-118` | the numpy sampler draws what the native one draws, seed for seed | tolerance (`scaledTol`, `v0.1:real.lut:35-37`), sampled 20 | passed |
| `pitFast` | `distances_python.lut:52-55, 103` | the numpy transform agrees with the native one | tolerance, sampled 20 | passed |
| `fullFast` | `:56, 104`; `distances.lut:120-127` | log-likelihood, score and information agree with the native ones, tolerance scaled by the size of the terms | tolerance, sampled 20 | passed |
| `profileFast` | `:57, 105`; `distances.lut:129-145` | the same for the profile likelihood, and the profile is the full one at its own sigma | tolerance, sampled 20 | passed |
| `fullPair`, `profilePair` | `:62-63, 106-107`; `v0.1:probability.lut:216-224` | a density pair: shapes, shift by zero (exact), shifts compose (tolerance), the score is the gradient (finite difference, tolerance `sqrt eps`, `v0.1:array.lut:182-191`), the information is positive semidefinite (eigenvalues against a tolerance), mean score zero and delivered information equal to reported (z-scores over 400 draws below 5) | statistical and tolerance, sampled 5 | passed |
| `fullKernel` | `:72-73, 97`; `v0.1:probability.lut:258-271` | the slope of the transform is the density (central difference, tolerance 1e-6); the transforms of sampled data are uniform (two moments and Kolmogorov over 400 draws, `zMax` 5) | tolerance and statistical, sampled 5 | passed |
| `sampleControl`, `sampleControlNear`, `pitControl`, `pitControlNear` | `:81-95, 98-101` | negative controls: sigma scaled by 2 and by 1.3 on one side of the triangle is caught on every case | statistical (power on a control, 7.S19), sampled 10 each | passed |
| Domain of all of these | `distances.lut:30-37, 73-95` | a complete design of 7 nodes, free coordinates within 5 m, sigma between 1 and 10 cm | | |

The run's values lie outside this domain: session A has 10 nodes and 26 measurements, not every
pair, and speaker placements more than 5 m from the origin (row `parlante_A5` at about 17 m in
`derived/A/positions/positions.csv`). By 7.S15 these certificates do not reach the run.

### Levenberg-Marquardt (`optimization_check.lut`, `optimization_python.lut`)

| law | where | says | evidence | v0.1 |
|---|---|---|---|---|
| `stepRule` | `optimization_check.lut:41, 56`; `v0.1:optimization.lut:82-85` | a step accepts only when the value falls, and then the damping does not grow; otherwise nothing moves and the damping grows | exact, sampled 50 | stale |
| `descent` | `:42, 57`; `v0.1:optimization.lut:88-89` | the damped step is a descent direction | exact (sign), sampled 50 | stale |
| `certified` | `:43, 58`; `v0.1:optimization.lut:93-99` | a run that says converged ends below the tolerance with a positive definite step matrix | tolerance (`lmTol` is a parameter), sampled 20 | stale |
| `nativeMaximizer` | `:46-50, 59`; `v0.1:optimization.lut:119-122` | the maximizer ascends, and is stationary where it says it converged | exact and tolerance (`fdTol`), sampled 20 | stale |
| `objectives` | `:53-54, 60` | the gradient is the gradient of the value; the step matrix is positive | tolerance (finite difference), sampled 20 | stale |
| `fastStep` | `optimization_python.lut:57-60, 95, 116` | `lm.py`'s step agrees within rounding and bit for bit, and obeys the step rule | tolerance and exact, sampled 50 | stale |
| `fastDirection`, `fastFinished`, `fastTrace`, `fastRunner`, `fastMaximizer` | `:62-92, 96-100, 117-121` | the same for the direction, the stopping reason, the whole trace of a run (also with budgets of 1 to 5), the certified run and the maximizer | exact (and tolerance for `MaximizerAgrees`), sampled 20 to 50 | stale |
| `stepControl`, `traceControl`, `budgetControl` | `:106-114, 122-124`; `prototipo-cero/src/lm_controls.py` | three mutants of `lm.py` (damping factor 2.9, budget checked before convergence) are each caught on some seed among the first 20 | exact, an existential over a census of 20 seeds, sampled 5 to 10 | stale |

"Stale": the two certificates are dated 2026-10-05, have no outcome field, and name laws the files
no longer state (`converges`, `StepAgrees` alone); the README says the four files that import
`optimization.lut` were not certified at v0.1 because their draws take hours (`README.md:103-104`).
The bitwise laws hold only under one BLAS (the linear algebra library numpy calls), as the file
says (`optimization_python.lut:8-9`).

### Laplace and the belief library

| law | where | says | evidence | v0.1 |
|---|---|---|---|---|
| `laplaceCalibrated` | `laplace_check.lut:61-65`; `v0.1:belief.lut:205-216` | at the tape's error of 3 cm, the Laplace posterior's error bars are calibrated: a projected rank is uniform | statistical (moments and Kolmogorov over 400 draws), sampled 3 | not run (certificate with no outcome, 2026-10-05) |
| `exchange`, `evidence`, `calibration` | `belief_check.lut:39-45` | the exact discrete update is exchangeable, its evidence chains, its likelihood is calibrated, on a toy scalar model | tolerance and statistical, sampled 50, 50, 5 | passed (with failed entries of two type obligations kept beside) |

### Of the experiment's own definitions, and of the libraries

`test fit with 30`, `test transformOf with 30`, `test reportOf with 30`
(`experiment_zero.lut:212-214`): the type obligations of the fit on generated valid graphs, exact
and sampled. Never run: there is no `experiment_zero.cert.json`, and an inventory of its
obligations timed out at two minutes on six of `reportOf`
(`prototipo-cero/luthier/certification-logs-2026-10-05-06/README.txt`, last paragraph).

The libraries in the cone carry their own laws: each numpy leaf of `array_python.lut` against its
native definition (tolerance, sampled 30 to 100, `v0.1:array_python.lut:74-104`); `normalVec`
(length exact, distribution statistical, `v0.1:probability.lut:99-101`); `kolmogorovDistance`
equal to its native definition (exact); the codec of tables, round trip, canonical, tolerant,
rejects (exact, sampled 200, `v0.1:table.lut:1-16`, `v0.1:table_python.lut:15-17`).

No law of this analysis is certified by citation. Every law with `Real` in its statement is out of
reach: none is tested (11.S5).

**What this means for the cone of the run.** `experiment_zero.lut` declares its maximizer with no
law (`experiment_zero.lut:95`) and uses the native `profiled` and `gaussian`
(`experiment_zero.lut:86-89`). The evidence that `lm.maximize` is right lives in
`optimization_python.lut` under another name, `fastMaximizer` (`optimization_python.lut:100`), and
the evidence on the likelihood in `distances_python.lut`, on the 7-node design. Neither file is
imported by `experiment_zero.lut`. So under 6.S14 (every name in the cone certified) the run's cone
contains an uncertified extern, and the certificates that would justify it are not reachable from
it. The comment at `experiment_zero.lut:92-94` makes the link in prose only.

## 4. The data

| file | format | size | read or written by |
|---|---|---|---|
| `prototipo-cero/2026-09-07/distancias.csv` | CSV, 16 columns, text cells (id, time, file, type, start, end, distance_m, valid, height_source, array, ..., transcript, notes, correction), UTF-8 | 24,290 bytes, 94 rows; session A (`array` = 3.5m): 26 valid distances (11 microphone to microphone, 15 speaker to microphone) and 11 valid heights over 10 nodes; session B (14m): 37 valid distances, 8 heights | read by `prepare_experiment_zero.py:56-58` with `csv.DictReader`, rows filtered by `array` and `valid` |
| `derived/A/graph/nodes.csv`, `measurements.csv` | typed CSV, header cells `name:type`, types int, float, str (`src/luthier/tables.py:1-12`) | 629 and 218 bytes; 10 nodes, 22 measurements | written by `prepare_experiment_zero.py:115-116` through `distance_graph.write_graph` (`distance_graph.py:46-49`); read by `readGraph` (`distance_graph.py:33-43`) with `luthier.tables.read_file` |
| `derived/A/positions/positions.csv`, `residuals.csv` | typed CSV | 1,546 and 1,566 bytes | written by `writeTable` (`experiment_zero.lut:201-203`, `distance_graph.py:238-240`) |
| `derived/A/positions/transform.csv` | typed CSV | not on disk | written by `experiment_zero.lut:203` |
| `prototipo-cero/luthier/*.cert.json` | JSON | 1 KB to 358 KB each, ten files | written by `luthier test` (12.S10) |
| `prototipo-cero/luthier.lock` | text, one commit hash | | read by the interpreter (12.S13) |

The graph and the positions on disk predate the two corrections of 2026-10-06. They were made on
2026-10-04, when the model predicted the three-dimensional distance and the four distances from
`mic1` were taken as nominal, so `measurements.csv` has 22 rows where the corrected script gives 26
(`docs/decisions.md:27-63`). The fit on the corrected model is not recorded (`README.md:36-44`).
There is no current result to compare a new run with.

For context, the acoustic pipeline reads ten mono 16-bit WAV files at 44.1 kHz, about 45 minutes
each, 3.8 GB in all (`derived/A/00_manifest.json`; Python's `wave` module, chunked,
`analisis/sonolib.py:78-103`), and writes CSV through pandas, JSON with a `.meta.json` sidecar
recording script, version, arguments and input hashes (`sonolib.py:121-129`), NPZ (numpy's
compressed archive of arrays; `02_traces.npz` is 31.7 MB) and PNG figures.

## 5. The world

What the analysis does to the outside world, and where:

| action | where | today |
|---|---|---|
| Reads `distancias.csv` | `prepare_experiment_zero.py:56` | Python, run by Luciano |
| Creates the graph directory and writes two CSV files; prints a summary line | `prepare_experiment_zero.py:115-118`; `distance_graph.py:46-49` | Python |
| Tests whether a directory holds the two files (`os.path.isfile`), as the predicate of a type | `distance_graph.py:209-211` via `distance_graph_python.lut:54-55` | an extern typed as pure |
| Reads the two CSV files of the graph | `distance_graph.py:33-43` via `distance_graph_python.lut:57` | an extern typed as pure |
| Creates the output directory and writes three CSV files | `distance_graph.py:238-240` via `experiment_zero.lut:57, 201-203` | an extern typed `-> Unit` |
| Prints the result and appends to `x.run.json` | 12.S18 | the v0.1 `run` command |
| Reads `luthier.lock` and compares it with the interpreter's commit | 12.S13 | the v0.1 interpreter |
| Imports Python modules from `prototipo-cero/src` (`PYTHONPATH=src`) | `README.md:77-81` | the environment |
| numpy's linear algebra: `linalg.solve` (`lm.py:40-44, 59-61`), `eigh` and `eigvalsh` (`pinvSym`, `retainedRank`, `src/luthier/arrays.py:283-291` at `v0.1-final`), sort (`kolmogorovDistance`) | | pure functions, but the bitwise laws depend on the BLAS and LAPACK (linear algebra libraries) numpy is built with |
| Python's `math` (`sqrt`, `log`, `exp`, `erf`, `cbrt`, `ulp`), `builtins.str`, `os.path.join` | `v0.1:real_python.lut:5-12`; `experiment_zero.lut:65, 171-172` | pure |

Randomness: none in the run; the fit is deterministic from the graph and the parameters. In
certification: the interpreter's `random.Random`, seeded by `--seed` (20261005), passed to every
Python generator (`distance_graph.py:92-153`, `positions_luthier.py:125-176`); numpy's
`default_rng(seed)` inside the fast sampler (`positions_luthier.py:86-88`) and in `normal_vec`,
returning the next seed so that native and fast draws agree (`positions_luthier.py:10-11`); a fixed
`random.Random(20261002)` for the prior of the Laplace laws (`positions_luthier.py:180-183`).

Temporary files: `gen_graph_dir` writes graphs under `tempfile.mkdtemp` and registers their
removal at exit (`distance_graph.py:217-229`), so drawing a value of `GraphDir` writes to the disk.

Clocks: none in the analysis; the certificates and the run record write the time of each entry
(12.S10, 12.S18).

External programs: none in this analysis. Elsewhere, `run_pipeline.py` calls each stage with
`subprocess.call` (`analisis/run_pipeline.py:30-32`), and the ideas pipeline calls the `claude` or
`codex` command line (`PIPELINE.md`, "Convenciones heredadas").

## 6. What is missing, ordered by what blocks first

Each item blocks the ones after it; (v) as in §2.

1. **Numbers and strings in the core** (v). Float64 `- * /` and comparisons, Int `/` and `mod`,
   `toFloat64`, String `+`, and `sqrt`, `log`, `exp`, `erf` as externs with a theory. The kernel
   computes Int `+ * - == <` and Float64 `+` only (`src/luthier/kernel.py:485-501`). Every file
   of the analysis needs these before anything else evaluates.
2. **Core and the array types** (v). `Bool`, `Maybe`, `List`, `Nat`, `Fin`, `Vec`, `Mat`, `VecOf`,
   `MatOf` (11.R1, 11.S9) with no `core.lut` and no array theory in the new tree; and whether a
   vector may still be written as the pair `(n, fn k { ... })` (§2 row 7, unsure).
3. **The bridge with numpy** (v). Arrays both ways (3.S22 to 3.S25, implemented only at v0.1),
   lists to the host, sums crossing (the Python check returns `("inRow", {...})`,
   `distance_graph.py:181-182`), opaque host values (a `Table` object). `run.py` carries none of
   these today (`src/luthier/run.py:73-115`).
4. **Tables** (v). A table theory and its model over the surviving `src/luthier/tables.py`:
   `Table`, its accessors, the codec laws.
5. **Reading the graph as an action, and run parameters** (v). `readGraph` and `isGraphDir` become
   actions (10.S3), with a host action that reads a typed CSV and the hash of the bytes read in the
   identity of the result; `run --set` for the holes (12.S18, 8.S1). `world.lth` §4 has `print` and
   `readFile` to text only, and §7 waits for this inventory. The port of the files to the new
   syntax also lands here: six mechanical rewrites (§2, constructs), then the named imports, which
   need the theories of items 1 to 4 to exist.
   After items 1 to 5, plus `transpose`, the matrix product and `retainedRank`, `validate_graph.lut`
   can run, uncertified.
6. **Functions across the bridge.** `lm.maximize` calls three Luthier functions and reads a
   record by attribute (`lm.py:94-101`); the fast likelihoods return Python functions partially
   applied (`distances_python.lut:23-44`). The spec states the bridge for lambdas over `Fin n` only
   (3.S23); functions over an infinite domain in either direction are not stated. This blocks the
   fit.
7. **The libraries of the fit**: the Gaussian likelihoods and the mean model (probability), the
   Gaussian belief with Laplace's update (belief), the types of optimization, `pinvSym`, `trace`,
   the Kolmogorov distance and tail. 7.R2 asks that they be rewritten over `VecOf n` in place of
   `(Theta : U)`, which is also what makes their laws testable.
8. **Writing the outputs as an action.** `writeTable` is typed `String -> Table -> Unit`
   (`experiment_zero.lut:57`); under 10.S3 it must take and give `W`. No host write action exists
   (`world_model.lut:35-39`). After items 6 to 8 `experiment_zero.lut` can run, uncertified.
9. **Speed and fuel (unsure).** Each Levenberg-Marquardt iteration materializes the native Jacobian,
   26 x 30 entries evaluated by the kernel, for up to `lmMaxIter` = 500 iterations; v0.1 did this by
   call by need with a table per lambda (3.S25, 8.S4). The new kernel reduces by substitution with
   a default fuel of 10,000 steps (`src/luthier/cli.py:28`). I did not measure; whether the fit
   finishes in usable time is open.
10. **Certification.** No `test` command, no tester, no certificate file, no cone hash in the new
    code. Generators: the `gen` act is gone, so each of the 10 Python generators the
    sonolocalización files register (13 more in the libraries they import) needs a binding by
    parameter or type, a census or a profile (7.R1, 7.R4), and a stated calling convention for a
    Python generator. Statistical laws need their level and their controls' power
    (7.S17 to 7.S19); tolerance laws need the measured cost of 11.S18 (`lib/evidence.lut` is not
    written). A generator that writes to the disk (`gen_graph_dir`) has no place in the spec.
11. **Evidence that reaches the run.** The run's maximizer is an extern with no law
    (`experiment_zero.lut:95`); its certificate is on another name in a file the run does not
    import, and the likelihood's certificates cover a 7-node design within 5 m, not session A
    (§3). Proposed: declare `lm.maximize` once, with its laws, in a file the run imports, and state
    the domain of the likelihood's laws so that it contains the run's design, or carry the
    certificate by 6.S11 (transport along an identity).
12. **A reference result.** Nothing recorded is on the corrected model (§4), so step 4 of the plan
    (compare with the current results) needs Luciano to regenerate the graph and run
    `experiment_zero.lut` under v0.1 first (`README.md:77-81`).

A conflict between rules, for the coordinator to weigh: 12.S17 makes `run` refuse any uncertified
cone with no opt-out (D-2026-10-12-y), and D-2026-10-13-ac puts the run of this slice before
certification exists. The slice cannot run under the spec as written until item 10 is done, unless
the run of the slice is allowed uncertified (which O3 leaves open).

## Where I was unsure

- Whether a pair `(n, f)` is accepted where the record `Vec` is expected (§2 row 7).
- Whether a refinement law starting on the line after `|` is meant to be rejected (§2,
  constructs).
- How a Python generator's arguments (`rng`, `size`, the type's arguments) cross, and how a sum
  crosses from Python, under the new bridge; the spec does not say.
- How long the v0.1 fit took: no run record is in the repository, and the certification logs only
  time obligations.
- Whether `prepare_experiment_zero.py` handles session B (`--array 14m`): no graph for B exists.
- What `gen_graph_dir` should become: a generator that writes files mixes a value and an action.
