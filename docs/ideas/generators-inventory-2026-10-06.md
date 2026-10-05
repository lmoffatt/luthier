# What `luthier test` draws: an inventory of the generators

Survey of 2026-10-06, 05:00 to 06:15. Read-only: nothing was written to either repository and no
`luthier test` or `luthier certify` was run.

## 0. Scope, method and conventions

**State surveyed.** Interpreter `~/Projects/luthier`, branch `numbers`. The survey started at
20a786b; commit d6d59c6 (05:56) added `gen Square` and `gen SquareOf` while it ran, and this report
includes them. Uncommitted: seven comment lines at the end of `src/luthier/lib/random.lut` and
rewritten certificates. Project `~/Projects/sonolocalizacion/prototipo-cero`, branch `numbers`,
e6fdc02 at the start and e5ada7d at the end (commits b8c5fdf, 9b6aa97, e5ada7d changed
`experiment_zero.lut`, `distances_python.lut` and `src/positions_luthier.py`). Another session kept
editing `src/positions_luthier.py`: its line numbers below are those of 06:10, so search by function
name if they have moved again.

**Method.**

1. Read `generators.py`, `testing.py`, the `gen` declarations and their implementations.
2. Dumped every certificate (`*.cert.json`, the latest entry of each definition): parameters,
   `domains`, outcome, `cases`, `skipped`, `registered_values`. Five project certificates
   (distances, distances_python, laplace_check, optimization_check, optimization_python) date from
   2026-10-05 15:40 and describe an older version of those files (types ThetaPos, ThetaFull), so I
   used them only as history.
3. Loaded every `.lut` file of both repositories as the top program, the way `luthier check` does,
   flattened each obligation with `testing.flatten`, peeled it with `testing.peel`, and classified
   how `Generators.sample` would draw each parameter. Each file is analysed in its own context:
   with the `gen` directives of the files it imports, and no others.
4. For 19 files, drew 20 cases per law with sizes 1 to 16, through `Generators.sample` and the retry
   logic of `draw` in `testing.run_law`, without evaluating any law, and counted for each refinement
   predicate how many candidates were tried and how many accepted. Laws over `GraphDir` were skipped,
   because its generator writes temporary directories.

Scripts and raw outputs are next to this report: `inventory.py`, `inventory2.py`,
`sample_rates.py`, `dump_certs.py`, `agg_certs.py`, `family.py`; `inv_*.json` (classification),
`smp_*.json` and `smp_*.log` (draws), `certs_dump.txt` and `certs_agg.txt` (certificates).

**Counting unit.** A *law* is one flattened conjunct, which is what `run_law` runs. In the files'
own contexts there are 573 of them in 26 files: 103 stated in a definition's type and 470 type
obligations (coercions inside bodies and what externs owe). Six more obligations, of `reportOf`
(experiment_zero.lut:187), could not be flattened within 120 s each (section 1).

**Symbols used throughout.** *s* is the size a case is drawn at; *S* is the largest size of a run (16,
or the `size k` of a directive); *n* in a directive is the number of cases asked for. "Acceptance" is
the fraction of candidates a rejection sampler keeps. *U* is Luthier's type of types.

Per file, in its own context (a law can fall in several of the last four columns):

| File | stated laws | type obligations | some parameter registered | some by rejection | some constant function | some with no generator |
|---|---:|---:|---:|---:|---:|---:|
| luthier lib/algebra.lut | 16 | 14 | 0 | 8 | 0 | 0 |
| lib/algebra_python.lut | 6 | 3 | 9 | 9 | 3 | 0 |
| lib/array.lut | 0 | 104 | 0 | 102 | 7 | 2 |
| lib/array_python.lut | 0 | 50 | 49 | 2 | 0 | 0 |
| lib/belief.lut | 0 | 15 | 15 | 3 | 9 | 9 |
| lib/optimization.lut | 0 | 10 | 10 | 8 | 9 | 0 |
| lib/probability.lut | 0 | 24 | 24 | 0 | 22 | 22 |
| lib/probability_python.lut | 0 | 3 | 2 | 0 | 0 | 0 |
| lib/random.lut | 0 | 2 | 2 | 0 | 0 | 0 |
| lib/rational.lut | 12 | 18 | 8 | 3 | 0 | 0 |
| lib/real_python.lut | 0 | 2 | 0 | 0 | 0 | 0 |
| lib/table.lut | 0 | 9 | 0 | 8 | 2 | 0 |
| lib/table_python.lut | 7 | 4 | 6 | 1 | 0 | 0 |
| lib/text.lut | 0 | 2 | 0 | 0 | 0 | 0 |
| examples/z7ring.lut | 3 | 23 | 0 | 15 | 0 | 0 |
| project belief_check.lut | 3 | 3 | 6 | 0 | 0 | 0 |
| distance_graph.lut | 0 | 29 | 27 | 27 | 27 | 0 |
| distance_graph_python.lut | 9 | 24 | 33 | 0 | 0 | 0 |
| distances.lut | 1 | 24 | 21 | 20 | 3 | 0 |
| distances_python.lut | 22 | 2 | 24 | 0 | 0 | 0 |
| experiment_zero.lut | 0 | 46 (+6 not flattened) | 46 | 9 | 1 | 0 |
| laplace_check.lut | 1 | 9 | 10 | 0 | 0 | 0 |
| optimization_check.lut | 5 | 4 | 9 | 0 | 0 | 0 |
| optimization_python.lut | 18 | 16 | 34 | 3 | 4 | 0 |
| positions.lut | 0 | 29 | 28 | 28 | 0 | 0 |
| validate_graph.lut | 0 | 1 | 1 | 0 | 0 | 0 |

## 1. From an obligation to draws (testing.py)

- `flatten` (testing.py:121-139) gives one law per conjunct, quantified only over the parameters the
  conjunct mentions and those their types mention. `_split_and` (149-158) first looks for a
  conjunction without unfolding, then unfolds with full fuel. For 6 of the 9 obligations of
  `reportOf` this second step ran over 120 s each in my scripts, so a test of `reportOf` spends
  minutes per obligation before it draws anything.
- `peel` (104-118) lists the parameters in order. Each type is instantiated with the values drawn
  before it (line 275), so a bound such as `Fin (fastMapInput x).i.n` is computed at draw time, by
  running the code under test.
- Size schedule (287-289): case i of n is drawn at size 1 + (i·S) div n, where i counts from 0, n is
  the number of cases and S the run's largest size. S is reached only when n ≥ S: with n = 5 the
  sizes are 1, 4, 7, 10, 13; with n = 3 they are 1, 6, 11. The five cases a certificate keeps
  (`SAMPLE_CASES`, line 24) are the first five, all drawn at the smallest sizes.
- `draw` (267-283): a GenError on the first parameter propagates. A GenError on any later parameter,
  whatever its cause (an empty `Fin 0`, "no generator for U", a rejection that ran out of tries),
  redraws the whole case up to 50 times and then gives up; the case is dropped as vacuous (304-305)
  and not counted anywhere. OutsideType propagates.
- `run_law` (161-328): a GenError at a size below S skips the case as unreachable (294-297); at size
  S it leaves the law "not run" (`broken`, 207-216). In a type obligation, an EvalError while
  drawing or evaluating skips the case and counts it in `skipped` (299-312). A law with no counted
  case is "not run" (321-327); one with some counted cases passes.
- Acceptance of a certificate (`Loader._unacceptable`, cli.py:159-169) compares the fingerprints of
  the registered generators the entry used, and the entry's requested `n` with the directive's
  (line 167). It does not look at `cases` or `skipped`.

## 2. The structural default rules (generators.py)

`Generators.__init__` (generators.py:40-51) sets size 16, `max_tries` 2000, `recursive_bias` 0.8 and
`law_probes` 5. `sample` (129-231) tries these rules in order; R1 to R15 are used as names below.

| Rule | Type form | Lines | What is drawn | Failure |
|---|---|---|---|---|
| R1 | `Fin n`, or an alias of it such as `Node p = Fin (p.n / 3)`, whose bound evaluates to an integer | 132-142 | uniform on {0, ..., n-1} (`rng.randrange`), whatever the size | n ≤ 0: EmptyDomain |
| R2 | a type with a registered generator: first the exact key with aliases unfolded (`VecOf 16`), then the family (`gen VecOf` receives the arguments), then the head of the type's weak head normal form | 80-95, 143-152 | Luthier: `gen s seed` on the machine with the fuel of a run, the seed from `rng.randrange(2^31)` (233-246). Python: `fn(rng, s, *args)`, the arguments normalized and converted with `to_python`, the result converted with `from_python` | evaluation error: GenError. Every value is checked against every predicate the type unfolds through (`laws_of` 97-110, `from_registered` 112-127); a value outside raises OutsideType, which fails the law. A Python exception other than GenError or EvalError is not caught by `run_law` (testing.py:319) and ends the run |
| R3 | `Int` | 156-157 | uniform integer on [-s, s] | none |
| R4 | `Float64` | 158-159 | `rng.uniform(-s, s)`, continuous | none |
| R5 | `Rational` | 160-162 | N/D with N a uniform integer on [-s·10^6, s·10^6] and D a uniform integer on [1, 10^6] | none |
| R6 | `String` | 163-164 | 0 to min(s, 6) characters, each uniform from `abcxyz` | none |
| R7 | a `data` type (`List`, `Unit`) | 165-166, 377-393 | a constructor uniform among those allowed: while depth < s and both kinds exist, the recursive ones with probability 0.8, at depth ≥ s only the others; arguments at depth + 1. A `List` gets a length roughly geometric with mean 4, at most s minus the depth it starts at | no constructors: GenError |
| R8 | dependent pair or record (`Sigma`) | 167-179 | the components in order, each later one with the earlier values substituted | EmptyDomain in the second component redraws the first, up to 10 times; other GenErrors propagate |
| R9 | sum (`Bool`, `Maybe`, `Cell`, `SigmaTreatment`) | 180-185 | an alternative uniform over the labels, its payload at depth + 1 | empty sum: EmptyDomain |
| R10 | labelled product without laws | 186-187 | its base, by R8 | as R8 |
| R11 | refinement `{ x : A \| p }` | 188-197, 248-356 | rejection: draw A until the predicate holds, at most 2000 tries. A predicate that evaluates to a Bool decides (`decide`, 259-272); a conjunction checks both sides; a predicate that is a quantified law (the record laws of `Table`, `Objective`) is probed 5 times with arguments drawn from its parameter types (292-314, 340-356): one counterexample rejects, none accepts | 2000 rejections: GenError "could not find a value ... give it a `gen`". A predicate that raises: GenError (256-257), and the draw is abandoned, not counted as a rejection. A predicate that calls a hole and does not reduce to a Bool: GenError |
| R12 | function on `Fin n` | 198-217 | its table: n independent values of the codomain, a dependent codomain instantiated at each index; numbers become an int64 or float numpy array, arrays are stacked, other values become a `match` on the index | as the codomain |
| R13 | non-dependent function on an infinite domain | 218-228 | `Float64 -> Float64`: with probability 1/2 the affine map x ↦ a·x + b (a and b drawn as `Float64`), otherwise a constant; any other `A -> B`: the constant function returning one drawn B | as the codomain |
| R14 | dependent function on an infinite domain (`Step`, `Runner`, `Maximizer`) | 229-230 | nothing | GenError "no generator for the function type ...; give it a `gen`" |
| R15 | anything else: `U`, a type variable (`Theta`, `Y`), `Real`, an opaque type | 231 | nothing | GenError "no generator for ..." |

Exhaustive mode (`test X exhaustive`, used only by examples/z7ring.lut) goes through `enumerate`
(452-518): `Fin` and refinements of `Int` with closed bounds exactly (`int_interval`, 520-569), `Int`
on [-S, S] marked "bounded", non-recursive data, pairs and sums by product.

The `domains` text of a certificate comes from `describe` (396-432). It has no case for R1, so a
`Fin n` parameter is described as "Int in [-16, 16] ... where 0 <= k and k < n" although it is drawn
uniformly on its range; it has no case for `Rational` (printed as "Rational"); and it says "size up
to S" for every registered generator, including those that ignore the size.

## 3. The `gen` declarations

Twenty-nine live declarations: 19 in the interpreter's libraries and 10 in the project. None is
generic over a type parameter; a family generator (`gen VecOf`) receives the family's arguments.

### 3.1 Luthier generators (src/luthier/lib/random.lut)

All draw from one linear congruential step (`nextSeed`, random.lut:10: seed·1103515245 + 12345
modulo 2^31) through `randBelow m` (14-15), which joins the high 15 bits of two steps into 30 bits and
reduces them modulo m. Each call starts from a fresh seed taken from Python's Mersenne Twister
(generators.py:235), so one value uses two or four steps of the congruential generator.

| Declaration | Keyed on | Implementation | Distribution |
|---|---|---|---|
| random.lut:30 `gen Int` | `Int` | `genInt`, random.lut:19 (through `genIntBetween`, 17) | uniform integer on [-s, s] |
| random.lut:31 `gen Nat` | `Nat` | `genNat`, 20 | uniform integer on [0, s] |
| random.lut:32 `gen Bool` | the unfolded sum `< true : Unit \| false : Unit >` | `genBool`, 21 | true or false, 1/2 each |
| random.lut:33 `gen Float64` | `Float64` | `genFloat64`, 22 | (k - 10^6)/10^6 · s, with k uniform on {0, ..., 2·10^6}: a grid of 2,000,001 points on [-s, s] with spacing s·10^-6. Zero has probability 5·10^-7; no value has 0 < \|x\| < s·10^-6 or \|x\| > s |
| random.lut:40 `gen Seed` | `Seed` (random.lut:38) | `genSeed`, 39 | a·65536 + b with a uniform on [0, 2^15) and b on [0, 2^16): uniform on [0, 2^31); ignores the size |

`genList` and `genListN` (24-28) exist but no `gen` uses them; lists come from R7. These generators
are active only in programs that import random.lut, directly or through probability.lut, belief.lut
or distances.lut. Elsewhere `Int`, `Float64` and `Bool` come from R3, R4 and R9, and `Nat` is a
rejection over R3 with acceptance (s+1)/(2s+1), s being the size (measured 0.525 in array.lut).
random.lut states no law about the distributions it draws; the uncommitted note at random.lut:43-49
says the same.

### 3.2 Python generators of the libraries

| Declaration | Keyed on (definition) | Implementation | Distribution and structure |
|---|---|---|---|
| rational.lut:62 `gen NormalDouble` | `NormalDouble` (rational.lut:60) | rational.py:28-34 (`EXP = 498`, line 25) | 0.0 with probability 0.02; otherwise a sign ±1, a mantissa uniform on [1, 2) and an exponent uniform on the integers [-498, 497]: magnitudes log-uniform from 1.2·10^-150 to 8.2·10^149. Ignores the size. Never subnormal, never above 10^150, almost never an integer or a short decimal |
| array_python.lut:43 `gen Dim` | `Dim` (array.lut:26) | arrays.py:305-306 | uniform integer on [1, min(s, 8)] |
| array_python.lut:44 `gen Dim2` | `Dim2` (array.lut:27) | arrays.py:309-310 | uniform integer on [2, max(2, min(s, 8))] |
| array_python.lut:45 `gen VecOf` | family `VecOf k` (array.lut:28) and its aliases `PositionsOf`, `FreeCoords`, `FullCoords` | arrays.py:313-314, `_vec` 141-142 | k entries uniform on [-s, s] |
| array_python.lut:46 `gen MatOf` | family `MatOf r c` (array.lut:29) | arrays.py:317-318, `_mat` 145-147 | r × c entries uniform on [-s, s] |
| array_python.lut:47 `gen MatRows` | family `MatRows r` (array.lut:30) | arrays.py:321-323 | r rows and a number of columns uniform on [0, s] (up to 16, where `Dim` stops at 8), entries uniform on [-s, s] |
| array_python.lut:48 `gen SpdOf` | family `SpdOf n` (array.lut:163) | arrays.py:344-347 | BᵀB + I, with B an n × n matrix of entries uniform on [-s, s] and I the identity: symmetric positive definite (SPD below), every eigenvalue at least 1, condition number below roughly 1 + 4n·s²/3 (a few hundred at the `size 5` of the spectral tests, a few thousand at s = 16 and n = 8) |
| array_python.lut:49 `gen Square` (new in d6d59c6) | `Square` (array.lut:31) | arrays.py:326-329 | n uniform on [0, s], n × n entries uniform on [-s, s] |
| array_python.lut:50 `gen SquareOf` (new in d6d59c6) | family `SquareOf k` (array.lut:32) | arrays.py:332-334 | k × k entries uniform on [-s, s] |
| array_python.lut:51 `gen SymmetricSquare` | `SymmetricSquare` (array.lut:42) | arrays.py:337-341 | B + Bᵀ with B an n × n matrix of entries uniform on [-s, s] and n uniform on [1, s] (up to 16): a generic spectrum, so almost surely nonsingular with distinct eigenvalues; never diagonal, never 0 × 0 |
| array_python.lut:52 `gen DeficientOf` | family `DeficientOf n` (array.lut:164) | arrays.py:350-355 | BᵀB with B an r × n matrix of entries uniform on [-s, s] and r uniform on [1, n-1]: exactly n-r zero eigenvalues (at rounding level) and r eigenvalues of order s², so the spectrum never comes near the retention threshold n·eps·max\|λ\| of arrays.py:279-280 (eps the machine epsilon of a double, 2^-52; λ an eigenvalue); never rank 0. For n = 1 it would raise ValueError; it is drawn only with n of type `Dim2` |
| table_python.lut:11 `gen Table` | `Table` (table.lut:37, laws at 51) | tables.py:255-260, with `_gen_value` 247-252, `_gen_float` 236-244, `_gen_str` 227-233 | 1 to 5 columns named c0 to c4, kinds uniform among int, float, str; rows uniform on [0, min(s, 8)]. Int cells uniform on [-10^a, 10^b] with a and b uniform on [1, 18], so most have 15 to 18 digits and small integers are rare. Float cells: 0.0 (10%), an integer on [-s, s] (10%), uniform(-1, 1)·10^e with e uniform on [-300, 300] (10%), uniform on [-s, s] (70%). Str cells: "" (10%), an integer on [-99, 99] as text (10%), 1 to 8 characters from `ab xyz09.,"\n\r-+e:` (80%). Never another column name (so no space, quote, comma or colon in a name), never zero or more than 5 columns, never more than 8 rows, never a subnormal float |
| table_python.lut:12 `gen Perturbed` | the unfolded record `{ table : Table, text : String }` (table.lut:215) | tables.py:298-300, `_perturb` 263-295 | a `gen_table` table and a rendering of it with the same content: spaces around header parts (50%), each float cell as `%.17g` (30%) or with a trailing zero (30%), spaces around non-string cells (30%), CRLF line ends (30%, skipped when a string holds a line break), the final newline dropped (30%) or doubled (30% of the rest) |
| table_python.lut:13 `gen BrokenText` | `BrokenText` (table.lut:216) | tables.py:303-307, `_broken_with_defect` 310-340 | a rendering of a table with at least one row (the size raised to 2) and exactly one defect: a ragged row, the unknown kind `real`, a repeated name (needs two columns, otherwise ragged), a bad number `abc` or a non-finite `nan`, `inf`, `-inf` (needs a numeric column, otherwise ragged) |

### 3.3 Python generators of the project

| Declaration | Keyed on (definition) | Implementation (prototipo-cero/src) | Distribution and structure |
|---|---|---|---|
| positions_python.lut:12 `gen Pairs` | family `Pairs p i` (positions.lut:26) | `gen_pairs`, positions_luthier.py:121-128 | for each of the pairs listed by i, a node uniform among the m nodes of p; it equals the pair's first node with probability 1/m (a pair at distance 0). EmptyDomain when p has no nodes and i is not empty |
| positions_python.lut:13 `gen PairsAmong` | family `PairsAmong n i` (positions.lut:50) | `gen_pairs_among`, 131-137 | the same among n nodes |
| positions_python.lut:14 `gen SeparatedPairs` | family `SeparatedPairs p i` (positions.lut:33) | `gen_separated_pairs`, 140-152 | for each pair, a node uniform among those whose position differs from the first node's, the distance computed as positions.lut computes it. EmptyDomain when there is none |
| distances_python.lut:18 `gen PositionsWithin` | family `PositionsWithin d box` (distances.lut:84); `TestedFree` is an alias (87) | `gen_positions_within`, 100-102 | d coordinates uniform on [-box, box]; ignores the size. TestedFree has d = 15 and box = 5 m: 7 nodes, node 0 at the origin, node 1 on the x axis, node 2 in the xy plane (the gauge, distances.lut:43) |
| distances_python.lut:19 `gen ScaledPositionsWithin` | family `ScaledPositionsWithin d box lo hi` (distances.lut:85); alias `TestedFull` (88) | `gen_scaled_positions_within`, 105-107 | the same, then u = log σ uniform on [lo, hi], with σ the tape's error; for TestedFull σ is log-uniform between 1 and 10 cm |
| distance_graph_python.lut:43 `gen ValidDistanceGraph` | `ValidDistanceGraph` (distance_graph.lut:77) | `gen_good_graph`, distance_graph.py:103-109 | N nodes uniform on [3, max(3, min(s, 8))]; prior means uniform in the cube [-10, 10]³ m (`BOX`, line 85); prior sds uniform on [0.01, 2] m (`SD_RANGE`, 86); K measurements uniform on [1, 3N], each an ordered pair of distinct nodes drawn uniformly with replacement, so repeats and both orders occur and some nodes may stay unmeasured; each distance is the true one plus \|e\| with e normal of sd 0.03 m (`NOISE`, 87; `_measure` 96-100), so it always exceeds the true distance; names n0 to n(N-1) |
| distance_graph_python.lut:44 `gen CompleteGraph` | `CompleteGraph` (distance_graph_python.lut:42) | `gen_complete_graph`, 112-117 | N uniform on [4, max(4, min(s, 8))], every pair a < b measured once, the same layout and noise |
| distance_graph_python.lut:45 `gen BrokenGraph` | `BrokenGraph` (distance_graph_python.lut:41) | `gen_broken_graph`, 124-151 | a valid graph with exactly one of 8 defects (`DEFECTS`, 120-121), chosen uniformly: an index out of range (N to N+3), a negative index (-1 to -3), a self pair, a distance not positive (negative 80%, zero 20%), a prior sd not positive, a repeated name (rows 0 and 1), a missing measurement column (never a node column), a coincident prior (the two nodes of one measured pair get the same prior mean) |
| distance_graph_python.lut:46 `gen GraphWithColumns` | `GraphWithColumns` (distance_graph.lut:33) | `gen_good_graph`, as above | valid graphs only |
| distance_graph_python.lut:56 `gen GraphDir` | `GraphDir` (distance_graph_python.lut:55) | `gen_graph_dir`, 214-226 | writes a broken graph (30%) or a valid one (70%) as `nodes.csv` and `measurements.csv` into a new subdirectory of one temporary directory per process (removed at exit) and returns its path |

### 3.4 Archived declarations (not loaded by any live file)

luthier/archive/lib-2026-10-04/: random.lut (Int, Nat, Bool, R), peano.lut (N), array_python.lut
(Dim, Dim2, VecOf, MatOf, SpdOf, DeficientOf), table_python.lut (Table, Perturbed, TableText,
BrokenText). luthier/archive/examples-2026-10-04/signal.lut (Signal).
sonolocalizacion/archive/luthier-kernel-2026-10-04/: copies of the library ones plus GoodGraph,
CompleteGraph, BrokenGraph, ThetaPos, ThetaFull. sonolocalizacion/archive/luthier-2026-10-02/:
Scene, Silence, Nperseg, Oversample, Density, PositiveDensity, Position, PositionMass,
PositionDistribution, PositionEvent, Waveform, NoiseSpectrum, Response, Clock, and a copy of
random.lut.

## 4. The types the tester draws

Counts are laws and parameter occurrences in the files' own contexts (step 3 of the method). The
route is a rule of section 2 or a generator of section 3. Where a certificate shows another route,
it was written by a program that loaded more `gen` directives (problem 6 in section 5). In every
acceptance formula s is the size of the case.

### 4.1 Numbers and scalars

**Int** (core.lut:27). R3, or `genInt` where random.lut is loaded; both uniform on [-s, s]. 45 laws,
66 parameters: algebra.lut intRing and exactInt (27 parameters), seeds in probability.lut,
table.lut, experiment_zero.lut. No magnitude above 16, so nothing near 2^53, where `toFloat64`
(real.lut:12) stops being exact, and nothing like the 18-digit integers `gen_table` puts in tables.
When an Int is a seed (belief.lut rankOf, probability.lut ShiftComposes, the `seed` of
belief_check.lut scalarSampler) only 33 seeds exist and cases repeat.

**Nat** (core.lut:43). `genNat` (uniform on [0, s]) or rejection over R3 with acceptance
(s+1)/(2s+1) (measured 0.525). 63 laws, 81 parameters, mostly lengths and dimensions:
algebra_python.lut VecRounds, array.lut, belief.lut, table.lut firstFailing. Zero comes with
probability 1/(s+1), so empty vectors and matrices with no rows are frequent (half the cases at
s = 1).

**Fin n, and Fin of a computed bound** (core.lut:47). R1. The largest family: 105 laws, 144
parameters, nearly all index bounds of type obligations (array.lut 67, distance_graph.lut 11,
positions.lut 11, experiment_zero.lut 10). When the bound is 0 the case is dropped: 7 of 100 cases
of array.lut minor and 13 of 100 of positions.lut point in their certificates. Certificates describe
these parameters as a rejection over Int (section 2).

**Float64** (core.lut:29). R4 (continuous uniform on [-s, s]) or `genFloat64` (a grid of spacing
s·10^-6). 27 laws, 32 parameters: real_python.lut abs, rational.lut toQ, array_python.lut scale,
mscale and product, the `tol` of belief.lut gaussianFamily, the `sigma` of laplace_check.lut
fixedLik, the `c` of experiment_zero.lut widenedPrior. Never below s·10^-6 in magnitude, never above
16, never -0.0, and under R4 never exactly 0. A parameter that stands for a tolerance or a scale is
negative half the time: belief.cert.json records gaussianFamily's Reflexive law failing at
tol = -0.81.

**NonNegative** (real.lut:29). Rejection over Float64, acceptance about 1/2 (measured 0.53 to 0.59).
8 laws, 12 parameters: algebra.lut exactNonNegative and largest, the `tol` of array_python.lut
approxVec and approxMat. Under R4 it is never 0, so the exact case of `approx` (tolerance 0,
real.lut:27) is not drawn there.

**Rational** (core.lut:30). R5 only. 20 laws, 38 parameters, all in rational.lut (exactRational,
rationalField). At s = 16 a value is below 1 in magnitude about 3% of the time and mostly between 1
and 10^3; zero comes with probability about 3·10^-8 per draw, so the zero branches of the field's
inverse (rational.lut:35) and of Invertible (algebra.lut:97-98) are never reached; no denominator
exceeds 10^6.

**NormalDouble** (rational.lut:60) and **NonZeroDouble** (rational.lut:61). The registered generator,
and a rejection over it with acceptance 0.98. 8 and 1 laws, 12 and 1 parameters, plus 11 laws over
tables `Fin n -> NormalDouble` (section 4.5): rational.lut float64Add, Sub, Mul, Div, Sqrt and
offByThree; algebra_python.lut addRounds to matVecRounds. algebra_python.cert.json shows 422 to
3,203 values drawn per law and none outside the type. It is the only generator in the libraries
that spans magnitudes. RootRounds (rational.lut:85-87) holds by its first branch for negative x,
which is about half of float64Sqrt's 300 cases.

**Bool** (core.lut:10). `genBool` or R9, uniform. 19 laws, 33 parameters: algebra.lut exactBool,
allOf, anyOf; examples/z7ring.lut badRing (exhaustive).

**String** (core.lut:31). R6 only. 13 laws, 14 parameters: text.lut chars, table.lut FloatCell,
table_python.lut parseTable and the csv law ReadsTheFormat, the column name `c` in
distance_graph_python.lut and experiment_zero.lut. Only the letters a, b, c, x, y, z: no digit,
separator, quote, line break, colon or non-ASCII character. None of 32,000 such strings parses as a
table (checked with `luthier.tables.parse`), so the four type obligations of `parseTable`
(table_python.lut:7; `match parseTable x { just j -> SchemaWellFormed j ; _ -> true }`) and
ReadsTheFormat on a String (table.lut:230) only ever take their rejecting branch, and FloatCell's
obligation only sees non-numeric text.

**Seed** (random.lut:38). `genSeed`, uniform on [0, 2^31). 65 laws, 72 parameters: every density
pair, kernel, agreement and Levenberg-Marquardt (LM below) law of the project (distances_python.lut,
optimization_check.lut, optimization_python.lut, belief_check.lut) and probability_python.lut
normalVec.

**Dim** (array.lut:26) and **Dim2** (array.lut:27). `gen_dim` and `gen_dim2` where array_python.lut
is loaded; otherwise rejection over Int with acceptance s/(2s+1) for Dim (measured 0.45) and
(s-1)/(2s+1) for Dim2 (none at s = 1). Dim: 85 laws, 119 parameters (every leaf law of array.lut,
positions.lut layout). Dim2: 7 laws (pinvSym, pinvSqrtSym, retainedRank). The spectral leaves are
tested with `size 5` (array_python.lut:75-79), so their dimensions run from 1 to 5. No dimension
above 8 is drawn. DetAgrees (array.lut:264-265) holds by its first disjunct `n > laplaceLimit`
(laplaceLimit = 4, line 263) for every dimension from 5 to 8, about half the draws once s ≥ 8.

**Z7** (examples/z7ring.lut:6). Enumerated exhaustively. 15 laws.

**Widening** (experiment_zero.lut:108) and the anonymous `{ t : Float64 | 0.0 < t }` inside
LMSettings (98) and SigmaTreatment (84). Rejection over `genFloat64` with acceptance 1/2, which gives
a uniform value on (0, s]. Widening: 7 laws (fit, transformOf). The run values c = 1 and 5 are
inside; an LM tolerance of 10^-9 to 10^-16 and the tape's σ of 1 to 10 cm sit at or below the grid's
spacing and are not drawn in practice.

**Node p** (positions.lut:19). R1 through the alias. 1 law (point), and the entries of
`Vec (Node p)`.

### 4.2 Vectors and matrices

**Vec A** (array.lut:22). R8 and R12: a length from Nat and the entries as a table. `Vec Float64` 34
parameters, `Vec (Node p)` 5, `Vec Int` 2, `Vec (Fin d.nodes)` 1; 37 laws (array.lut addDef,
subDef, append, head; belief_check.lut scalarLik; experiment_zero.lut keptTransforms;
laplace_check.lut). Lengths 0 to s, entries on [-s, s]. The empty vector is what made
belief_check.lut scalarLik and scalarSampler fail (`t.f 0` with `t.n = 0`, belief_check.cert.json).

**NonEmptyVec** (array.lut:33). Rejection, acceptance s/(s+1). 1 law (last).

**VecOf k** (array.lut:28), with its aliases PositionsOf (positions.lut:16), FreeCoords and
FullCoords (distances.lut:70-71). `gen_vec_of` where array_python.lut is loaded; otherwise rejection
over `Vec Float64` with acceptance 1/(s+1) when k ≤ s and none when k > s. About 60 laws and 86
parameters (array.lut 20 parameters, array_python.lut 23, experiment_zero.lut 21 with
k = g.measurements.nRows), plus PositionsOf 13 laws, FreeCoords 10 and FullCoords 4. In
positions.lut's own context, which does not import array_python.lut, `PositionsOf d.nodes` is a
rejection that succeeds only for d.nodes ≤ s/3: nodesOf and positionsModel drew 0 to 13 cases in
40 s, all of designs with 0 or 1 node.

**Mat A** (array.lut:23). R8 and R12. 11 laws, 12 parameters (array.lut symmetric, maddDef,
msubDef). Shapes up to 16 × 16.

**MatOf r c** (array.lut:29). `gen_mat_of`; otherwise rejection with acceptance 1/(s+1)² when r and c
are at most s (0.35% at s = 16; measured 0.1% to 1.5% depending on the shape), none otherwise. 49
laws, 70 parameters. **MatRows r** (array.lut:30): `gen_mat_rows` or rejection with acceptance
1/(s+1); 4 laws (matMulDef, positions.lut flatten).

**Square** (array.lut:31), **SquareOf k** (32) and `{ s : Square | 1 <= s.m }` (82). Since d6d59c6,
`gen_square` and `gen_square_of` where array_python.lut is loaded, and the refinement a rejection over
`gen_square` with acceptance s/(s+1). Elsewhere, as in every certificate written before 05:56,
rejection over Mat with acceptance 1/(s+1) (measured 0.10 over sizes 1 to 16) and nested rejections
for the others. Square: 12 laws (traceDef, detDef, diagonal, optimization.lut diagOf); the
refinement: 4 laws (minor); the pair `SquareOf n * SquareOf n`: 10 laws, 15 parameters (rotate,
sweepFrom, jacobi). With the old route, rotate took 17 to 22 s per law (array.cert.json).

**SymmetricSquare** (array.lut:42). `gen_symmetric` where array_python.lut is loaded. Otherwise a
rejection over Square: random entries are never exactly symmetric, so only 0 × 0 and 1 × 1 matrices
pass, and in array.lut's own context even 1 × 1 fails, because `symmetric` calls `approx`, which calls
`abs`, a leaf bound only in real_python.lut, and the predicate does not reduce. 5 laws, 6 parameters
(eigenDef, spectralMap).

**SpdOf n** (array.lut:163) and **DeficientOf n** (164). `gen_spd_of` and `gen_deficient_of`; by
rejection they cannot be drawn for n ≥ 2 (in array.lut's own context all 20 cases of Ascending,
InvSqrtPositive and PinvSqrtProjects were dropped, after 23 to 27 s each). SpdOf: 12 laws
(Ascending, EigenvaluesSumToTrace, EigenvaluesMultiplyToDet, EigvalsAgree, CondOfSpectrum,
InvSqrtInverts, InvSqrtPositive, InvSqrtAgrees, SolveInverts, cond). DeficientOf: 7 laws
(MoorePenrose, PinvAgrees, PinvSqrtProjects, PinvSqrtAgrees, RankOfProjector, RankAgrees). The
spectra drawn (section 3.2) never test the tolerances these laws carry: `cond s * tolOf (n * n)` is
never large and the retention threshold is never approached.

**Tables of NormalDouble**, `Fin n -> NormalDouble` and `Fin m -> Fin n -> NormalDouble`
(algebra_python.lut:17-35, rational.lut:94-104). R12 over the registered generator. 11 laws, 18
parameters. Their length n is a Nat on [0, s] (at most 8 for matVecRounds, tested with `size 8`).

Common to all generated vectors and matrices: independent entries uniform on [-s, s]. Never exact
zeros, repeated rows, special structure (diagonal, triangular, permutation, rank one), extreme scale
or ill conditioning, except what the three spectral generators build.

### 4.3 Records

With laws of their own:

**Table** (table.lut:37, laws at 51). `gen_table` where table_python.lut is loaded (section 3.2).
Without it (table.lut or distance_graph.lut tested alone) a rejection over the record `{ nRows,
names : List String, kinds : List String, cell : String -> Fin nRows -> Maybe Cell }`, whose `cell`
is a constant function: acceptance 0.34% (116 of 33,702) and 0.75% (6,524 of 867,649) in the two
contexts, and every accepted table had no columns. Because NoCellsOffSchema is probed only 5 times,
an accepted table can break it: one accepted 4-row table had a cell in row 1 and no column. 3 laws
over Table (sameCells, sameTable, the csv law RoundTrip), besides the tables inside Perturbed and
DistanceGraph. By rejection, sameCells drew 9 cases in 40 s.

**Objective** (optimization.lut:16, laws at 24). No generator. In optimization.lut's own context the
predicate calls `add` and `norm`, holes until array_python.lut binds them, so it does not reduce:
GenError, laws not run. With the leaves bound (optimization_check.lut's context) I measured: at sizes
1 and 2 the only objectives accepted have dimension 0, a constant value, an empty gradient and a
1 × 1 step matrix; other draws raise inside the predicate; at sizes 8 and 16 every draw ends in
"could not find a value in 2000 tries" after 10 to 26 s. 8 laws (optimization.lut GradIsGradient,
StepMatrixPositive, dampedStep and lmStep type obligations; optimization_python.lut pyStep,
pyMinimize, pyStepFactor). The project tests LM on objectives built by `objectiveAt`
(optimization_check.lut:25); these generic obligations stay untested.

**Ensemble** (probability.lut:34). Rejection over `{ draws : Nat, zMax : Float64 }` with
`100 <= draws`: unreachable, because a Nat is at most s ≤ 16. 2 laws (the IsDensityOf and PitUniform
of gaussianKernel), which stop earlier at `Theta : U`.

**PitResolution** (probability.lut:252). Rejection, acceptance 1/4; step and tolerance uniform on
(0, s], never near the values in use (step about 6·10^-6 and tolerance 10^-6, distances.lut:95). 3
laws, all stopped by `Theta : U`.

Labelled products without laws, drawn by R8 one component at a time:

**GaussianBelief n** (belief.lut:110). The mean from `gen_vec_of`, the precision from `gen_mat_of`:
for n ≥ 2 a non-symmetric, indefinite matrix, so almost never a belief. 6 laws, 7 parameters
(belief.lut laplaceAt, drawGaussian, gaussianFamily; experiment_zero.lut posteriorSd, and inside
Fit). belief.cert.json: drawGaussian passed on 24 cases with 76 skipped (the computation raised),
gaussianFamily's Symmetric law on 33 with 67 skipped.

**LMState n** (optimization.lut:27). x from `VecOf n`; phi and the damping mu from Float64, so mu is
negative half the time and never below s·10^-6 or above 16 in magnitude, while the damping schedule
runs from 10^-15 to 10^15 (lines 30-33); iter from Int, negative half the time; accepted from Bool.
4 laws (lmStep, pyStep, pyStepFactor), all of which also quantify over Objective.

**MapInput** (distance_graph.lut:120). x0 from `gen_mat_rows` (3 rows, 0 to s columns), sdx from
`gen_mat_of` (half of the sds negative), i from `Vec (Fin x0.n)`, j from `gen_pairs_among` (self
pairs with probability 1 over the number of nodes), d from `gen_vec_of` (half negative). 9 laws
(experiment_zero.lut priorBelief, widenedPrior, likelihoodOf). Not the image of any graph:
priorBelief divides by squared sds that can be near zero.

**Design** (positions.lut:51). nodes from Nat, i from `Vec (Fin nodes)`, j from `gen_pairs_among`,
or in positions.lut's own context a rejection with acceptance 1/(s+1). 9 laws, 11 parameters
(nodesOf, positionsModel). In my draws 6 of 20 designs had no pair at all.

**LMSettings** (experiment_zero.lut:98). tol on (0, s], maxIter on [0, s] (0 with probability
1/(s+1)). 5 laws, 6 parameters (fit). Session A runs with tol = 10^-12 and 500 iterations
(experiment_zero.lut:25-26).

**Fit n** (experiment_zero.lut:105). The posterior as a GaussianBelief, sigma and nu of either sign, a
`predicted` vector of unrelated length, two Bools. 1 law (transformOf).

**Perturbed** (table.lut:215). Registered (section 3.2). 4 laws (the csv laws Canonical, Tolerant,
ReadsRenderings, ReadsMutations).

**DistanceGraph** (distance_graph.lut:18). Two tables from `gen_table`, or two column-less tables by
rejection. 1 law, the type obligation of firstViolation, whose premises `HasNodeColumns g` and
`HasMeasurementColumns g` never hold for tables with columns c0 to c4, so it passes vacuously
(distance_graph.cert.json: 100 cases, 200 tables drawn).

**Likelihood Theta Y** (probability.lut:114), **ScaledModel Theta** (283), **Discrete Theta**
(belief.lut:61), and the aliases Sampler (probability.lut:105) and LogLik (belief.lut:29): R8 with
constant functions inside, and a `Theta` or `Y` somewhere, so not run (section 4.7). 9, 9 and 8 laws;
Sampler 11, LogLik 2.

Records that appear only as results and are never drawn: Run, MaxResult, Report, Transform,
Diagnosis, Moments, Violation, RowViolation.

### 4.4 Sums and data types

**Maybe A** (core.lut:33) and **Cell** (table.lut:23): R9, uniform over the alternatives; drawn only
inside column-less tables. **List A** (core.lut:36): R7. `List (Vec Float64)` in
probability_python.lut kolmogorovDistance (1 law; about 4 vectors of length 0 to 16 with entries on
[-16, 16], outside [0, 1]); `List String` in experiment_zero.lut positionsTable (5 laws; names from
a, b, c, x, y, z, repeats possible). **SigmaTreatment** (experiment_zero.lut:84): R9, `eliminated`
or `known` with σ uniform on (0, s]; 5 laws (fit). **Violation** (distance_graph.lut:84), **Reason**
(optimization.lut:54) and **ExtendedReal** (core.lut:40) are not drawn.

### 4.5 Function types

Finite domains (R12): `Fin n -> NormalDouble` (16 parameters), `Fin m -> Fin n -> NormalDouble` (2),
`Fin n -> Bool` (table.lut firstFailing, 1), and the entry function of every Vec and Mat. Complete
tables of independent entries.

Infinite domains (R13): 18 laws and 30 parameters, all drawn as constants except `Float64 ->
Float64`. Examples: optimization.lut negate and lmMaximizer, and fastMaximizer in
optimization_python.lut and experiment_zero.lut, with `f : VecOf n -> Float64`,
`g : VecOf n -> Vec Float64` and `m : VecOf n -> Mat Float64`, so LM runs on a constant objective
whose constant gradient has a random length; the type obligations of algebra_python.lut VecRounds,
ScaleRounds and MatVecWithinGamma (`op`, `s`, `mv`); array.lut Ascending, InvSqrtPositive and
PinvSqrtProjects (`ev`, `m`), and spectralMap's `f : Float64 -> Float64`, constant or affine, never
like the 1/√x and pseudo-inverse maps it is used with (array.lut:156-158); distances.lut
ProfileIsFullAtItsSigma's type obligations, over `s : Sampler FreeCoords (Vec Float64)`, a sampler
that ignores its parameter and its seed. The samplers and likelihood components of probability.lut
would be constants too, but they are never drawn (section 4.7).

Dependent functions (R14): Step, Direction and Runner (optimization.lut:78-80), Maximizer
(belief.lut:122), Finisher and Tracer (optimization_python.lut:33-34) have no generator. No current
law quantifies over them; they are the subjects of refinements (`{ f : Step | ... }`).

### 4.6 Domain types of the project

**Positions** (positions.lut:15). Rejection over `Vec Float64` (`p.n mod 3 == 0`): acceptance 6/17 at
s = 16 (measured 0.39 over all sizes); at s = 1 only the empty vector passes. 8 laws (point,
pairDistances, Separated, distanceJacobian, unflatten). Entries uniform on [-s, s]: coincident nodes
have probability 0 and nearly coincident ones are rare; empty positions are frequent (9 of 20 draws
for unflatten), and then `Node p` is empty and the case is dropped.

**Pairs p i** (positions.lut:26), **SeparatedPairs p i** (33), **PairsAmong n i** (50). Registered in
programs that load positions_python.lut, which positions.lut does not import. In positions.lut's own
context Pairs is a rejection with acceptance 1/(s+1) (17 of 20 cases drawn) and SeparatedPairs a
nested rejection that drew nothing (all 20 cases of each distanceJacobian law dropped, 11 s each).
Pairs: 2 laws; SeparatedPairs: 3 laws (distanceJacobian). positions.cert.json used the generators:
distanceJacobian drew 3,799 SeparatedPairs values for 68 counted cases.

**HasFree** (distances.lut:52). Rejection (`freeDim <= v.n`, freeDim = 15): acceptance 2/17 at
s = 16 and none below s = 15. 2 laws (embed, jacDist).

**PositionsWithin and TestedFree** (distances.lut:84, 87), **ScaledPositionsWithin and TestedFull**
(85, 88). Registered in distances_python.lut and the files that import it. In distances.lut's own
context a rejection over `VecOf 15` and then WithinBox: acceptance about 1.5·10^-9 at s = 16 (1/17 for
the length times (10/32)^15 for the box), so unreachable. TestedFree: 45 laws, 53 parameters (30 in
optimization_python.lut, 9 in optimization_check.lut, 8 in distances_python.lut); TestedFull: 17
laws, 18 parameters (one more law, PitAgrees, since e5ada7d). The 7 nodes are in general position
with probability 1: never coincident or nearly so, never collinear or coplanar, never outside the
box, and σ never outside 1 to 10 cm.

**ValidDistanceGraph** (distance_graph.lut:77). Registered in programs that load
distance_graph_python.lut. In distance_graph.lut's own context a rejection that accepted 0 of 2,006
candidates (every law over it timed out). 42 laws, 49 parameters (22 in experiment_zero.lut, 15 in
distance_graph.lut, 11 in distance_graph_python.lut). Never more than 8 nodes or 24 measurements.
The graph of session A (2026-09-07/derived/A/graph) has 10 nodes, 22 measurements and prior sds from
0.001 to 3 m, outside the generator's 3 to 8 nodes and 0.01 to 2 m. The measurement error is
one-sided, always positive.

**GraphWithColumns** (distance_graph.lut:33). Drawn with `gen_good_graph`, so valid graphs only. 15
laws, 17 parameters (iOf, jOf, dOf, priorAt, sdAt, nameOf, rowPriorSeparated, rowNameUnique,
distinctPairs, priorMatrix, priorScatter, nodeNames). A graph with the columns and a bad row (an index
out of range, a repeated name) is never drawn: the `indexOk` premises of rowPriorSeparated are always
true, and the accessors never see an invalid row. In distance_graph.lut's own context the rejection
accepted 0 of 1,229 candidates.

**CompleteGraph** (distance_graph_python.lut:42): 1 law (rigidity). **BrokenGraph** (41): 3 laws
(validity, checks, fastCheck). One defect per graph, so the order in which firstViolation checks the
invariants is exercised only where one defect breaks two of them (an index out of range also breaks
PriorSeparated).

**GraphDir** (distance_graph_python.lut:55): 10 laws (the type obligations of readGraph).

**Seed** and **NormalDouble**: section 4.1.

### 4.7 Type parameters

`Theta : U` and `Y : U`, and values of the type variables Theta and Y. U has no generator (R15). 30
laws and 46 parameters over U, all "not run" (33 laws counting those that stop at a value of a type
variable): array.lut IsGradient (2 laws); probability.lut ShiftComposes (3), InfoIsPositive (1),
diagnose (7), pitSlope (2), gaussianPit (1), gaussianKernel (8); belief.lut weights (2), bayes (2),
discreteFamily (2), rankOf (2), laplaceAt (1). The U of laplaceAt is its second parameter, so `draw`
treats the GenError as an empty domain and belief.cert.json says "no case could be drawn: every draw
met an empty domain". What these laws state is tested only through instances: the density pairs and
kernel of distances_python.lut, belief_check.lut, laplace_check.lut.

## 5. Problems, ordered by how much they weaken what a certificate means

1. **A passed law can rest on few, skipped or vacuous cases, and neither its outcome nor the
   acceptance of its certificate shows it.**
   - Dropped cases: any GenError of a later parameter becomes a dropped case after 50 redraws
     (testing.py:280-283, 304-305), whatever its cause. Certificates record `cases` below `n`
     (positions.cert.json distanceJacobian 68 of 100; array.cert.json minor and Ascending 93 of 100),
     and `_unacceptable` accepts them because it compares the requested n (cli.py:167). A law loses
     all its cases this way only if every draw fails; then it is "not run", with the reason lost.
   - Skipped cases: a type obligation drops the cases whose computation raised (testing.py:299-312).
     drawGaussian passed on 24 of 100 and gaussianFamily's Symmetric law on 33 of 100
     (belief.cert.json), because the generated precision is not a precision.
   - Premises the generator never meets: firstViolation in distance_graph.lut (the columns are never
     there), the four type obligations of `parseTable` and ReadsTheFormat on a String (no drawn
     string parses), the `indexOk` premises over GraphWithColumns (always true, so the other branch
     never runs), DetAgrees for dimensions 5 to 8, RootRounds for negative x (about half of
     float64Sqrt's cases). Nothing in a certificate says how often a premise or a disjunct decided a
     case.
2. **The drawn domains stop short of where numerical code fails and of the experiment's own inputs.**
   Scalars stay on [-16, 16]: floats never below s·10^-6 in magnitude nor above 16, integers never
   above 16; dimensions stop at 8 (16 for SymmetricSquare and the columns of MatRows). SPD matrices
   have every eigenvalue at least 1, deficient ones a clean gap, symmetric ones a generic spectrum, so
   the conditioning and retention tolerances of the spectral laws are never tested near their limits.
   Positions are uniform in a box, with no nearly coincident or degenerate layouts. Tolerances, steps
   and LM settings (PitResolution, LMSettings, every unconstrained `tol : Float64`) are drawn on
   (0, 16] or [-16, 16], far from 10^-6 to 10^-16. The graph generator never reaches session A's 10
   nodes or its 0.001 m prior sds, and its noise is one-sided. NormalDouble is the only generator
   that spans magnitudes.
3. **A registered generator draws a well-behaved part of its type, and nothing measures how much.**
   The OutsideType check (generators.py:112-127) catches values outside the type and never parts of
   the type left out. GraphWithColumns is drawn from valid graphs only; Dim stops at 8 while its type
   has no bound; Table never has other column names, more than 5 columns or more than 8 rows;
   BrokenGraph always has exactly one defect; SpdOf never comes near singular. A certificate over the
   type covers the generator's image. The Luthier generators of random.lut carry no law about their
   own distribution.
4. **Records without a generator are drawn one component at a time, so most values are not members of
   the concept the laws are about.** GaussianBelief's precision is a random non-symmetric matrix;
   MapInput has negative sds and distances; LMState has negative damping and iterations; the parts of
   Fit are unrelated; Objective can be drawn only at dimension 0; a Table without its generator has
   no columns; Ensemble cannot be drawn at all. The results are the skipped and failed cases of
   problem 1 and the laws over Objective that never run.
5. **Functions over infinite domains are constants, or affine maps on Float64.** 18 laws quantify over
   such parameters; each is checked against constant samplers, objectives and spectral maps only.
6. **The route, and with it the domain behind a certificate, depends on the program that ran the
   test.** Dim, VecOf, MatOf, Square, SquareOf, SpdOf, SymmetricSquare and DeficientOf have
   generators only where array_python.lut is loaded; Pairs and SeparatedPairs where
   positions_python.lut is; PositionsWithin where distances_python.lut is; Table where
   table_python.lut is; Int, Nat, Float64 and Bool use random.lut where it is imported and Python
   fallbacks elsewhere. `--imports` writes each imported law's result to its own file's
   certificate, so a certificate carries whichever context ran it, and `_unacceptable`
   (cli.py:159-169) compares only the registered generators recorded in the entry. In their own
   files: positions.lut's distanceJacobian has every case dropped, and layout, nodesOf and
   positionsModel time out; array.lut's SymmetricSquare, SpdOf and DeficientOf laws cannot be drawn;
   distances.lut's TestedFree and TestedFull are unreachable; every law of distance_graph.lut over
   ValidDistanceGraph or GraphWithColumns times out; optimization.lut's Objective predicate does not
   reduce.
7. **Quantified laws inside a type are accepted after five probes** (generators.py:292-314, 340-356).
   A column-less Table that breaks NoCellsOffSchema was accepted in my draws. Five probes are also all
   the checking a registered generator's value gets against such a law.
8. **Generic laws over U are never run** (30 laws), and laplaceAt's reason is misreported as an empty
   domain.
9. **What a certificate shows about its draws is partly wrong or unrepresentative.** `describe`
   reports `Fin` parameters as a rejection over Int and says "size up to S" for generators that ignore
   the size; the five `sample_cases` are always the smallest draws; with fewer than S cases a run never
   reaches size S (n = 5 stops at 13, n = 3 at 11), which matters for the generators that use the size
   (graphs, tables, dimensions, every structural rule).
10. **Cost.** Nested rejection (the SquareOf pairs of rotate, 17 to 22 s per law before d6d59c6),
    rejection inside the 50-redraw loop (202,378 candidates of Dim2 for one law of array.lut, up to
    100,000 per case), predicates that run code (Objective, 10 to 26 s per failed draw) and the
    flattening of `reportOf` (over 120 s for each of 6 obligations) push directives toward small n and
    `size 5`, which feeds problems 1, 2 and 9.
