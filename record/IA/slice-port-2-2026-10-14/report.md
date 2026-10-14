# The port of experiment_zero.lut, positions.lut and distances.lut: report

2026-10-14, Claude Opus 5.5, an agent of the coordinating session, on `prompt.md` of this
directory (bede3a4), with the coordinator's two messages during the work (one-arm matches for
host results; the regression of validate_graph.lut). Sources read only, in sonolocalización at
5ffc36ef70e16e11182bc09e4a927c381e35df1c: `prototipo-cero/luthier/{experiment_zero,positions,distances}.lut`
and `prototipo-cero/src/distance_graph.py:238-284`. Nothing was changed there, nor in `src/` or
`tests/` here. The run was tried on the tree at 9fc993f (the host side and call by need).

## What was written

| file | commits | parse | check |
|---|---|---|---|
| `examples/sonolocalizacion/positions.lut` | 5019221, d59cf12 | passes | passes |
| `examples/sonolocalizacion/positions_model.lut` (`positionsModel`, `nodesOf`) | e77536c | passes | passes |
| `distance_graph.lut` (imports `positions.lut`), `positions_slice.lut` deleted | 63ee303 | passes | passes, and so does `validate_graph.lut` (its two 4.R9 of the first port are gone) |
| `examples/sonolocalizacion/distances.lut` | 5d96c5d, b2cc73e | passes | 2 refusals, 4.R9 |
| `examples/sonolocalizacion/experiment_zero.lut` | fa081f3, 9163b3d, 7ff2fb4 | passes | 1 refusal, 4.R9 |

`validate_graph.lut` imports only `distance_graph.lut`, so it needed no change. Its run prints
again, in 32 s, `valid: 10 nodes, 22 measurements, 21 distinct pairs; directions the distances do
not see: 14 (of which 10 are the heights and 3 the rigid motions of the plane)`, and the slow test
(`LUTHIER_SLOW=1`) passes in 31 s. experiment_zero.lut's run stops with `stuck match` (below).

## Renames

Those of the first port (`fn`, `vec`/`mat` for the tuple literals, blocks for the one-arm
`match`es used as `let` where nothing heavy is bound, named imports), and those the theories'
report lists: `MeanModel (PositionsOf n)` to `MeanModel (3 * n)` with `k := i.n` and no `dim`,
`shift`; `Likelihood (PositionsOf n) (Vec Float64)` to `Likelihood (3 * n)`; `fastMaximizer` gone
for `lm : Maximizer` of `belief_model.lut`; `laplaceMode (3 * m.x0.n) lm runSettings lik prior m.d`;
`laplaceAt` without `(Vec Float64)`; `pinvSym` with its floor first; `trace (matMul f cov)`; the
prior's precision by `mat Float64 s.n s.n (fn ...)`; `valueSums` matched as a triple, unchanged;
`IsGradient`-style resolutions as `Resolution` (`pitResolution`). `log`, `sqrt`, `exp` are
`elementary.log`, `elementary.sqrt`, `elementary.exp`; `*` and `-` on arrays are the named leaves
(`matMul`, `sub`), since whether an importer sees `operator` acts is unstated. Every other name
is v0.1's: of positions.lut all of it (`Positions`, `PositionsOf`, `Node`, `point`, `foot`,
`pairDistance`, `Pairs`, `pairDistances`, `Separated`, `SeparatedPairs`, `distanceJacobian`,
`PairsAmong`, `Design`, `nodesOf`, `positionsModel`, `flatten`, `unflatten`, `layout`); of
distances.lut the design, the gauge, the domains, `posModel`, `fullModel`, `nativeFull`,
`nativeProfile`, `FullAgrees`, `ProfileAgrees`, `ProfileIsFullAtItsSigma`; of experiment_zero.lut
the parameters (`graphDir`, `outDir`, `horizontalWidening`, `fixedSigma`, `lmTol`, `lmMaxIter`),
`meanModel`, `priorBelief`, `widenedPrior`, `SigmaTreatment` with `eliminated` and `known`,
`likelihoodOf`, `runSettings`, `Fit`, `Widening`, `fitOf`, `fit`, `Transform`, `keptTransforms`,
`leverages`, `residualSds`, `overSds`, `normalTransforms`, `transformOf`, `transformTail`,
`posteriorSd`, `summary`, `Report`, `reportOf`, `runWith`, `main`, `priorWidened`, `sigmaKnown`,
`positionsTable`, `residualsTable`, `transformTable`, `writeTable`.

## What was more than a rename

1. `positions_slice.lut` is gone into `positions.lut`, except `positionsModel` and `nodesOf`, which
   are in `positions_model.lut`. They need `probability.lth`, and its import broke
   validate_graph.lut's run from 63ee303 (the coordinator's finding): importing probability.lth
   reaches program.lth (through generators.lth), whose `int : Term` takes the name of tables.lth's
   constructor `int` in a run, so every `intAt` is a `stuck match` (below). distance_graph.lut
   needs only positions.lut, so with the model apart validate_graph.lut runs again (e77536c,
   d59cf12). [proposed] Back into positions.lut once the run keeps the two apart.
2. `layout` compares at arrays.lth's `exact` where v0.1 wrote `0.0`.
3. distances.lut: the sampler is not ported (`nativeSampler`, `profileSamplerOf`, `sigmaProfile`,
   `SamplerAgrees`, `ensemble`): there is no generator of normals (the theories' report). The
   three laws that drew `y` from it take `(y : VecOf nPairs)` as a parameter, which a test binds,
   and a tolerance `(tol : Tolerance)` (11.S18, P11) in place of v0.1's `8 eps` inside
   `scaledTol`: `agreeTol tol magnitude = tol * nPairs * freeDim * (1 + magnitude)`. `last` and
   `append` are written there (arrays.lth has neither). `pitResolution`'s step is the value of
   the cube root of `doubles.epsilon`, 6.055454452393343e-06, written out: `Elementary` has no
   cube root.
4. experiment_zero.lut: `lmFloor : Float64` is a new parameter, `runSettings` is belief.lth's
   `Settings` (`tol`, `maxIter`, `floor`) and v0.1's `LMSettings` is gone. The parameters are plain
   `Float64` and `Int` since `--set` fills only those (run bite 7); v0.1 refined them in the
   declaration. `priorWidened` and `sigmaKnown` therefore test their parameter positive and print
   `horizontalWidening must be positive: x` or `fixedSigma must be positive: x` otherwise.
5. `main`, `priorWidened`, `sigmaKnown` are actions `(w : W) : W * Unit`, reached by `run --main`
   (v0.1 said `--entry`). `readGraph` is the first port's action; a graph that cannot be read
   prints the first port's `FAIL ReadGraph` line.
6. The three tables are native `Table` values (`positionsTable`, `residualsTable`,
   `transformTable`, with `positionCell`, `residualCell`, `transformCell`), the columns, kinds and
   cells of `distance_graph.py:248-284`. `nodeNames` (an extern) is gone: the name is read by
   `nameOf`. `joinPath` (os.path.join) is gone: paths are `outDir + "/positions.csv"`.
7. **world_model.lut has no write action** (`print`, `readFile` only). So `writeTable w path t`
   prints a header line `== <path>` and then `csv.render t` to the standard output. Nothing is
   written under `outDir`; the header names the path it would have.
8. `test fit with 30`, `test transformOf with 30`, `test reportOf with 30` are not ported: they
   need a generator of valid graphs (v0.1's distance_graph_python.lut), which is not here.
9. Following the coordinator's message (the host side's finding, 8.S4): every host result used
   more than once is bound by a one-arm `match`, which the run evaluates once (9163b3d):
   `laplaceMode`, the posterior's precision, the prediction, the residual, `nu`, the covariance in
   `leverages` and `posteriorSd`, the leverages, the kept transforms, `fit` and `transformOf` and
   `posteriorSd` in `reportOf`, and the report in `runOn`. The posterior's mean is read as
   `mode.x` (what `laplaceAt` sets it to), so `laplaceAt` is projected once, for its precision.
   Run bite 9 (9fc993f) then brought call by need, so the matches are no longer needed for that;
   they stay, harmless (the coordinator's second message).

## Readings (mine; each undone by one commit)

- `lmFloor` for the run is v0.1's `n eps` for the 30 coordinates of session A,
  6.661338147750939e-15 (v0.1 had no floor: its `solve` inverted the matrix whole).
- The covariance's floor `covFloor n = n * doubles.epsilon` is v0.1's `n eps`, which its
  `pinv_sym` held inside, so that `nu`, the leverages and the sds are v0.1's. It could equally
  be `lmFloor`.
- `fixedSigma` is kept as the run parameter's name (v0.1's command lines,
  `--set fixedSigma=0.03`), which clashes with probability.lth's `fixedSigma`; the same
  definition is written in experiment_zero.lut as `knownSigma`. The alternative is to rename the
  parameter and import the theory's.
- The tables are printed in the order v0.1 wrote them, then the summary line last.
- `transformTail` stays as written (with `kolmogorovTail` and Stephens's correction inline):
  `Transform` keeps the distance and the count, not the values, so `uniformPValue` has nothing
  to take.
- `entry v k` reads a vector entry with a guard (0.0 outside) so that a table's cell, indexed by
  the table's row, does not need the vector's length to match it in its type.

## What check says (reported, not fixed)

- `distances.lut:45, 46`, 4.R9 on `pairI`, `pairJ`: `vec (Fin nodes) nPairs (fn k { firstFrom k 0 })`
  gives an `Int` where `Fin nodes` is asked. True of the program as written: the bound is a fact
  about `firstFrom`, which check cannot see.
- `experiment_zero.lut`, 4.R9 on `sigmaKnown`: `known fixedSigma` (and `known 0.03`) is refused,
  inside the guard `0.0 < fixedSigma`. The cause is not the refinement: program.lth defines a
  function `known`, and importing any file that reaches program.lth (`generators.lth`, so
  `probability.lth`, `belief.lth`, `positions.lut`, `distance_graph.lut`) makes `known` resolve to
  it. Smallest:

      import "generators.lth" Level
      T = { a : Unit || known : { s : Float64 | 0.0 < s } }
      x : T := known 0.03

  is refused; without the import it passes. A name a file did not import reaches it (12.S22 says
  the importer sees only what it names).
- Two refusals were sidestepped, both reported so that check can be looked at:
  1. A record literal passed where a theory's type is asked is refused, and the same record
     returned by a definition declared at that type passes. Smallest:

         P (n : Nat) : { k : Nat, g : Fin n -> Float64 }
         use (n : Nat) (p : P n) : Nat := p.k
         ok (n : Nat) : P n := { k := n, g := fn i { 0.0 } }
         viaDef (n : Nat) : Nat := use n (ok n)                    -- passes
         inline (n : Nat) : Nat := use n { k := n, g := fn i { 0.0 } }   -- 4.R9

     So `likelihoodOf` calls `knownSigma` in place of an inline `ScaledModel`.
  2. In `fit`, a block binding `n := 3 * m.x0.n` used as the index of `laplaceMode n ...` was
     refused (4.R9) and `(3 * m.x0.n)` written out passes; I could not reproduce it in a small
     file, so it depends on something of the context (the imported theories). Written out.
- The Cell constructors `int`, `real`, `text` must be named in the import of tables.lth to build a
  cell (4.R2 otherwise); done.

## What stopped the run

`PYTHONPATH=src python3 -m luthier.cli run examples/sonolocalizacion/experiment_zero.lut --set
graphDir=examples/sonolocalizacion/A/graph --set outDir=<dir> --set lmTol=1e-12 --set lmMaxIter=500
--set lmFloor=6.661338147750939e-15` at 9fc993f prints `stuck match` after 2 s.

**The stop: a definition of one file takes the name of another file's constructor.** The run
reaches `ValidGraph g`, whose `IndicesInRange` reads `intAt g.measurements "i" k`, and `intAt`'s
`match v { int k -> k ; ... }` is stuck: program.lth defines `int : Term := Var "Int"` (line
600), which is in the run because experiment_zero.lut imports probability.lth, which imports
generators.lth, which imports program.lth. run.py's `Loaded` keeps two files' definitions of one
name apart (`name@file`), but a definition and a constructor of the same name are not kept apart.
`realAt` is not affected (no definition is called `real`). Smallest, no graph:

    import "world_model.lut" HostConsole host : HostConsole
    import "tables.lth" Table Codec intAt
    import "tables_model.lut" csv : Codec
    import "generators.lth" Level
    showInt (x : Int) : String := extern "python:builtins.repr" x
    main (w : W) : W * Unit := host.print w (match csv.parse "a:int\n7\n" { nothing -> "no table" ; just t -> showInt (intAt t "a" 0) })

prints `stuck match`; without the `generators.lth` line it prints `7`. The same leak is behind
check's refusal of `sigmaKnown` (program.lth's `known`, above). It is also what broke
validate_graph.lut at 63ee303, now avoided by `positions_model.lut`; experiment_zero.lut needs
probability.lth, so it cannot avoid it. The fix belongs to run.py (and check.py): a constructor's
name is not taken by another file's definition (12.S22).

**Behind it, in probes** that ran the same command on a scratch copy of `src/luthier` at 9fc993f
with program.lth's `int` renamed `intTerm` (nothing in `src/` changed, nothing committed):

1. With the default fuel (10,000,000 steps) the run stops with `fuel spent` after 1891 s wall,
   inside `lm.maximize`, at about the 13th iteration of Levenberg-Marquardt.
2. The fit is slow per iteration: about 95 s, every iteration the same. A copy of lm.py that
   timed its callbacks gave, per iteration, the score 16 s twice, the information 23 s twice and
   the log posterior 6 s once. The information is asked twice at the same point (`decrement` in
   `finished`, then `step`), and so is the score. Most of the time is the native Jacobian
   (22 x 30) and the native means, evaluated entry by entry when they cross to the host.
3. The fit's progress: the log posterior's negative went from 69.43 (iteration 1) to 51.42
   (iteration 12) and 39.61 (iteration 22), the damping falling by 3 each iteration to 3e-14:
   every step accepted, and not converged after 22 iterations (35 min). v0.1's Python run of
   the same problem converged within its 500; whether this one does, and in how many, the probe
   below says.
4. With `--set lmMaxIter=2 --fuel 1000000000` the whole program runs to the end in 302 s wall
   (two iterations, then the posterior, the covariance, the leverages, the transform and the
   three tables), and prints the three tables and the line

       nodes 10, measurements 22, sigma 5.878085247321709 m, nu 18.90455443922829, transform of the residuals: Kolmogorov distance 0.4238554341635174 over 22, tail probability 0.00045168891550244436, NOT CONVERGED: the maximizer ran out of its 2 iterations

   The tables' first lines:

       == <outDir>/positions.csv
       name:str,x:float,y:float,z:float,sx:float,sy:float,sz:float,shift:float
       mic1,1.8279749164415643e-07,-2.5722146841670215e-07,1.689999999999995,0.0009999999808464359,0.0009999999668780497,0.009999999999999976,3.1555951382558563e-07
       == <outDir>/residuals.csv
       i:int,j:int,d:float,predicted:float,residual:float,standardized:float
       1,2,5.38,4.981170118146589,0.39882988185341084,0.06785030585174547
       == <outDir>/transform.csv
       i:int,j:int,leverage:float,z:float,u:float
       1,2,0.0026673610987479656,0.06794097791665658,0.5270836907817745

   These are of an unconverged fit, two iterations from the prior; they say the program's tail
   runs, not what the fit gives.

5. With `--set lmMaxIter=500 --fuel 100000000000` (v0.1's values otherwise) the run converges
   and finishes in **4856 s wall** (81 min). Levenberg-Marquardt took 59 iterations: the negative
   log posterior fell from 69.43 to 10.59 by iteration 26, then converged linearly, its change
   halving each iteration, to 10.591140896946865 (the damping at its least, 1e-15, from
   iteration 26). The summary line:

       nodes 10, measurements 22, sigma 0.23547527629512058 m, nu 7.610802926053918, transform of the residuals: Kolmogorov distance 0.2821202626913203 over 22, tail probability 0.04849001594351214

   The tables' first lines:

       == <outDir>/positions.csv
       name:str,x:float,y:float,z:float,sx:float,sy:float,sz:float,shift:float
       mic1,-8.247250338963302e-07,3.960820163849524e-06,1.69,0.0009999961873634559,0.0009999817344074674,0.009999999999999978,4.045771589189418e-06
       == <outDir>/residuals.csv
       i:int,j:int,d:float,predicted:float,residual:float,standardized:float
       1,2,5.38,5.1870960237120975,0.19290397628790235,0.8192111686754591
       == <outDir>/transform.csv
       i:int,j:int,leverage:float,z:float,u:float
       1,2,0.3435279364112367,1.0110851688730105,0.8440121659174156

   v0.1's header says sigma was 25.7 cm in session A "with every standardized residual below
   0.8"; here sigma is 23.5 cm and the standardized residuals run from -1.46 to 0.95. I did not
   run v0.1 to compare (data scripts are Luciano's); a run of v0.1's experiment_zero.lut on
   `examples/sonolocalizacion/A/graph` is the reference. Candidates for the difference: the
   graph (A/graph/SOURCE.md says where it came from), the floors (`lmFloor`, `covFloor`), or
   where v0.1's run stopped.

What it would take to run at HEAD: run.py (and check.py) keeping a constructor's name from
another file's definition; then a fuel above the default (10,000,000 steps is about 13
iterations); and, for the time, the callbacks' cost (the information and the score asked twice
per iteration at one point; the native Jacobian crossing entry by entry), which is lm.py's and
run.py's.

## Decisions I took on my own

The readings above; the items of "more than a rename" the brief did not fix (2, 3, 4's guards, 6's
`nodeNames` and `joinPath`, 7's header line `== <path>`, 8); the two sidesteps of the checker; the
deletion of `positions_slice.lut` in the commit that switches `distance_graph.lut`'s import. The split of
`positionsModel` and `nodesOf` into `positions_model.lut` to restore validate_graph.lut's run
(e77536c, 7ff2fb4, b2cc73e, d59cf12), [proposed] until run.py keeps a constructor's name apart.
