All three break. Surface syntax beyond the document's own fragments (`:=`, `\ x { … }`, `extern`, `cite`, `Fin n -> T`, grades) is mine; `u` = 2⁻⁵³, the float64 unit roundoff. The float arithmetic below ties-to-even exactly as written.

### 1. L10 (draft 5): a path through a subtype sums to a "proved" bound that is false

```
Prob      := { x : Float64 | 0 <= x, x <= 1 }                     -- certified subtype (L4)
sum       := \ v { neumaier v }   : (Fin 3 -> Float64) -> Float64 -- native, taken as holotype
sum_naive := \ v { v 0 + v 1 + v 2 }                              -- total, cheapest
sum_prob  := \ v { ascending recursive sum }  : (Fin 3 -> Prob) -> Float64   -- specialization (L20)

sum      ~ sum_prob   : Cost, proved, d <= 12u   on Fin 3 -> Prob   -- cite higham2002 checked ai+human
sum_prob ~ sum_naive  : Cost, proved, d <= 12u   on Fin 3 -> Prob   -- same
```

On `Prob` the exact sum S ≤ 3, so recursive and compensated summation are each within 6u of S (Higham, *Accuracy and Stability*, 2nd ed., §4.2–4.3 — from memory, check the sections) and every pair is within 12u; each certificate records that number. No direct edge `sum ~ sum_naive`: the author only ever compared the fast one against the one proved thing around.

```
x := [2^53, 1, -2^53]        -- : Fin 3 -> Float64, not : Fin 3 -> Prob
print (sum x) tol 1e-9
```

Verdict:
1. The law gives the candidates {`sum`, `sum_naive`, `sum_prob`}; L20 puts the specialization in the planner's graph by its identity certificate.
2. Path `sum → sum_prob → sum_naive`, summed distance 24u ≈ 2.7e-15 ≤ 1e-9.
3. Every link proved, so "the sum is a bound".
4. Representative by cost: `sum_naive` (no sort, no compensation). Substitute.
5. `sum_naive x` = (2⁵³ + 1) − 2⁵³ = 0, since 2⁵³+1 ties to 2⁵³. `sum x` = 1 (Neumaier keeps the 1 in the compensation). Returned: 0, carrying "proved, within 2.7e-15 of `sum x`". Off by 1, under a proved certificate.

Both links hold on `Fin 3 -> Prob` and nowhere else; `sum_prob` is never run, so the type checker never sees `x` against `Prob`, and the rule reads distance and grade, never domain. The 2-node degenerate form is `cite` dropping a theorem's hypotheses: γₙ needs n·u < 1, and float32 (u = 2⁻²⁴) for one hour at 48 kHz gives n·u ≈ 10, so a float32 extern certified `proved` against the Rational holotype is a single link void on every field recording.

Fix: *a link certified on a subtype is a link only at inputs certified (L4) in that subtype; a path exists at x only where every link does.*

### 2. L19 (draft 6): the identity omits the runtime that produced the bits

```
xcorr_lag := extern "python" numpy.dot : (Fin 4 -> Float64) -> (Fin 4 -> Float64) -> Float64
             -- one lag of a direct cross-correlation; declared a definition
x := [2^53, 1, 1, -2^53] ; w := [1, 1, 1, 1]
r1 := xcorr_lag x w                 -- lag τ1
r2 := 0.5                           -- lag τ2, exact in both runs
tdoa := if r1 > r2 then τ1 else τ2
print tdoa tol 1e-6
```

Run A, one BLAS thread, sequential: ((2⁵³+1)+1) − 2⁵³ = 0. Run B, two threads, each half then combined: (2⁵³+1) + (1 − 2⁵³) = 2⁵³ − (2⁵³ − 1) = 1. Exact: 2. So `tdoa` is τ2 in A and τ1 in B.

Verdict:
1. Code (same declaration, same hash), inputs, mode (Luthier's evaluation strategy), demanded type and tolerance, model (`Float64`), seed (nothing sampled), plan (the extern is one node; the reduction order inside `ddot` is below the plan): all equal. One identity.
2. L18 draft 4 allows "a result in the same class at a distance the plan records"; the plan records nothing inside an extern, and |0 − 1| ≫ 1e-6: not the same class.
3. The memo keeps whichever ran first. Under one identity the laptop says τ2 and the field machine says τ1; at 2 ms that is 0.7 m of bird.
4. L14 binds library version and platform into the extern's *certificate*, L19's key does not, so after `pip install -U numpy` the certificate is reissued from the new library while the memoized value stays from the old one: value and certificate in front of it come from different specimens.
5. With dynamic scheduling the two values occur on one machine at one setting, so L21's `Bool` identity (same implementation rerun, same bits) fails and reports an implementation change that did not happen.

n = 4 stands in for n = 1.7e8, where a threaded BLAS splits the reduction; the gap scales as n·u and the flip happens at near-ties, routine with multipath.

Fix: *add to the identity the host runtime the plan's extern nodes ran under — library version, platform, thread count, the triple L14 already binds into the extern's certificate — and memoize no result an identical rerun fails to reproduce within its tolerance.*

### 3. L14 (draft 5, proposed): the lawless extern the identity law admits is a table

```
Point := Fin 3 -> Float64 ; Station := Point
c : Float64 := 343                                      -- declared parameter (L17)
delay : Point -> Station -> Real                        -- no laws yet, as every function starts
delay := \ p s { norm (p - s) / c }                     -- native, holotype
G : Fin 2000 -> Point                                   -- the volumetric grid
delay_grid := extern "python" table.lookup : Point -> Station -> Float64
             -- delays[g, s] filled by running delay over G × S, nearest-point lookup off G; a definition
print (srp frames) tol 1e-4                             -- srp evaluates delay on G × S
```

Later: `refine := argmin p near p* { Σ_ij (tdoa_ij − (delay p i − delay p j))² }` with p off G, and the first law anyone writes, `delay p p = 0`.

Verdict:
1. No laws on the type, so no validation and no refusal; structurally a `Point -> Station -> Float64`: applied under its declared type.
2. "Runs with its certificate graded by what it has": the structural judgment alone.
3. "May replace the native only by the identity law": the W5 agreement test, sampled on the values actually computed (L5) = G × S. The table *is* the native's output there: distance 0, `Bool` true, seen on G × S — the strongest identity the system issues short of proved.
4. L10: path `delay → delay_grid`, 0 ≤ 1e-4; a lookup costs less than a `sqrt`, so `delay_grid` replaces `delay` wherever it is demanded. In the Boolean interim, with no run database, the author does the same by hand under W5, licensed by the same certificate.
5. "G2 is not bypassed": the identity certificate certifies no description, as the rule says. But nothing required one. The native was replaced by a specimen whose entire description is the native's memo on G × S: acquaintance in L5's sense, in its limiting form.
6. At `refine`, `delay_grid p i = delay (nearest p) i`: with 1 m cells, up to 0.87 m / c ≈ 2.5 ms, 25 tolerances; the objective is piecewise constant, the argmin returns the coarse cell, and the reported sub-grid precision is fictitious. `delay s s = 0` fails unless the station sits on a grid point. One law over the signature, sampled on L11's distribution, refuses the table before it runs; the identity law on the computed values cannot, by construction.

Fix: *with no law over its signature an extern runs where the author names it and replaces nothing; the identity law admits it to the planner's graph only beside a certificate of at least one law of the description.*

### Ranking, earliest bite first

1. **L14.** Bites now: the W5 bootstrap is exactly a lawless extern replacing a native by agreement on the computed values, and a precomputed delay table over the grid is how the SRP step is already done. Silent.
2. **L19.** Bites at the first reproduction elsewhere — second machine, GPU, upgrade, thread count — the W11 tag. Visible as a false "implementation changed" from L21, or silent through the memo. Scientifically small except at argmax near-ties, and at the UMAP/HDBSCAN step, where the result that changes is the song count.
3. **L10.** Its proved-through-subtype form needs proved links, the last certificates to exist on floats. Its 2-node form bites at the first `cite` on a float32 extern over an hour-long recording, which is the first proved certificate anyone will want.

Severity runs the other way: L10's break is the one that says "proved" about a wrong number.