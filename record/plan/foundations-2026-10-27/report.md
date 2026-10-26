**Read-only audit: sampling evidence and certificate identity**

**Both foundations have confirmed defects.** The rule-of-three formula is mathematically sound under its sampling premise, but some current generators violate that premise. Certificate identities also omit inputs that demonstrably change results.

The strongest findings are:

| Severity | Finding |
|---|---|
| Critical | The golden-ratio sampler produces a deterministic rotation, with strong dependence between cases. Its advertised confidence bound can fail badly. |
| Critical | Census-only sampled and exhaustive lines can have identical entry identities despite opposite verdicts. |
| High | Pooling distinguishes starting seeds but does not detect overlapping streams or cycles. |
| High | An extern can read RNG state, environment variables or time without changing its cone identity. |
| High | BLAS threading and floating-point controls change numerical results under unchanged identities. |
| High | Host hashes omit transitive dependencies, package builds and Python’s version in important paths. |
| High | Verdict-producing tester and bridge code remains outside the content identity. |

No file was changed. I did not invoke `luthier certify`, `luthier test`, or `luthier run`.

**Scope, authority and provenance**

The governing identity contract is [1: **6.S8, a certificate is identified by its cone and frozen**]( /home/lmoffatt/Projects/luthier/docs/spec/06-certification.md:39). The sampling contract is [2: **chapter 7, generators declare their distribution, entries identify their bindings, and sampled passes state confidence bounds**](/home/lmoffatt/Projects/luthier/docs/spec/07-tests.md).

I read both requested decisions:

- [3: **D-2026-10-16-g, stretches of one law, cone, binding and distribution pool as one sample, with replays counted once**](/home/lmoffatt/Projects/luthier/record/decisions.md:2709).
- [4: **D-2026-10-25-a, evidence uses the pair `(ε̂, δ)`, capped-sum composition is the default, and independence-dependent composition requires a declared premise**](/home/lmoffatt/Projects/luthier/record/decisions.md:3444).

[5: **D-2026-10-27-a, kernel identity becomes a content hash, with evidence-bearing transport between kernel versions**](/home/lmoffatt/Projects/luthier/record/decisions.md:3476) is treated as settled. This report does not reopen it or audit evaluator scaling.

The inspected checkout was `649d3822aed5f3a3f732529d4c0dea127f676470`. The prompt’s SHA-256 was:

```text
1d3b1e3bd2d50d91a10e9e53b8b257e45e19e4ceedf045bc87c686dd3052617c
```

All Python probes used:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/lmoffatt/miniconda3/bin/python
```

They operated in memory. The environment was CPython 3.12.9, NumPy 1.26.4, SciPy 1.17.1 and SymPy 1.14.0 on Linux x86-64. The loaded NumPy BLAS was OpenBLAS `0.3.23.dev`, using pthreads and the Haswell kernel.

The working-tree status was unchanged at the end. The pre-existing modified specification file and two untracked paths were left untouched.

**1. Critical: the golden-ratio sampler does not support the claimed confidence bound**

**Locations:** [generators.lth:244](/home/lmoffatt/Projects/luthier/src/luthier/lib/generators.lth:244), [generators_model.lut:98](/home/lmoffatt/Projects/luthier/src/luthier/lib/generators_model.lut:98), [tester.py:622](/home/lmoffatt/Projects/luthier/src/luthier/tester.py:622), [certify.py:1294](/home/lmoffatt/Projects/luthier/src/luthier/certify.py:1294).

There are several distinct random mechanisms:

| Path | Actual mechanism |
|---|---|
| Built-in tester draws | One persistent `random.Random(spec.seed)` instance per line or conjunct. |
| Host families in `generators.py` | A fresh `random.Random(current_seed)` per generator call, returning another 31-bit seed drawn from that instance. |
| `scrambled`, `unitOf`, `equalOr`, and their fallback families | Modular multiplication applied to a counter that usually advances by one. |
| `skewedSource` | An explicit LCG used as an intentionally broken control, not the tester’s normal source. |

Python’s `random.Random` uses Mersenne Twister, not an LCG. Its core period is `2**19937 - 1`. [6: **Python documents the generator and its deterministic state model**](https://docs.python.org/3.12/library/random.html).

The Luthier definitions are:

```text
m = 2147483647 = 2^31 - 1
a = 1327217884

scrambled(s) = a*s mod m
unitOf(s)    = scrambled(s)/m
nextSeed(s)  = (s + 1) mod 2^31
```

`a/m = 0.6180339886890882`.

This is **not** the multiplicative recurrence `s[k+1] = a*s[k] mod m`. Away from the counter’s wrap, its transformed states satisfy:

```text
z[k+1] = (z[k] + a) mod m
```

It is an additive congruential sequence, or rational rotation. Choosing a well-spread rotation does not make its consecutive values independent.

The explicit control LCG at [generators_model.lut:156](/home/lmoffatt/Projects/luthier/src/luthier/lib/generators_model.lut:156) has multiplier `1103515245`, increment `12345`, and modulus `2^31`. It should not be confused with the live sampling path.

**How a line obtains its seeds.** `run_spec` initializes two separate pieces of state: the persistent Python RNG and `Values.seed`, both from the line’s seed. Built-in draws advance the Python RNG. Bound generators receive `Values.seed`, then replace it with the seed they return. A line with one `sameOrFloat` binding therefore hands that family consecutive seeds. Multiple generator-bound parameters share that threaded seed.

I instrumented the actual `Total` conjunct of [the `FloatIsOrdered` line](/home/lmoffatt/Projects/luthier/tests/tester/core_laws.test.lut:293), using its declared seed `20261020`, size `10`, and `100` cases. It returned `Supported`. The generator received exactly:

```text
20261020, 20261021, ..., 20261119
```

All 100 observed generated values matched the current nested `sameOrFloat` arithmetic exactly.

**Statistical checks**

The table tests the uniform selector used by that real family. A raw `sameOrFloat` output is intentionally a mixture, so testing its values directly against a uniform distribution would be incorrect.

| Check | Real 100-case selector | Same selector extended to 10,000 cases |
|---|---:|---:|
| Ten-bin χ² statistic | `0.2` | `0.012` |
| Upper-tail χ² p-value | `0.99999944` | approximately `1` |
| Lag-one correlation | `−0.420175` | `−0.416493` |
| Correlation p-value under the IID reference null | `1.49 × 10⁻⁵` | numerically underflowed |
| Runs above/below `0.5` | `77` | `7640` |
| Runs z-score | `5.22646` | `52.78265` |
| Two-sided runs p-value | `1.73 × 10⁻⁷` | numerically underflowed |
| Selector values below `0.25` | `26` | `2501` |
| Adjacent pairs both below `0.25` | `0` | `0` |

The runs calculation uses the usual normal approximation, without continuity correction. Correlation p-values are diagnostic IID-reference values, not proofs of a particular dependence model.

For 5,000 **non-overlapping** consecutive pairs from the extended sequence, a `10 × 10` uniformity check found:

```text
occupied cells: 20 of 100
χ²:             30227.52
degrees freedom: 99
```

The exact geometry explains the failure. Consecutive pairs lie on two parallel lines:

```text
u[k+1] - u[k] = a/m
            or a/m - 1
```

Their normal is `(1, −1)`, with length `√2` and line spacing `1/√2 ≈ 0.707107`. This is a severe spectral defect in the sequence the tester actually uses.

For comparison, I also checked the multiplier as though it belonged to a multiplicative LCG. In two dimensions its exact shortest dual vector is:

```text
(-29771, 28657)
length:  41322.343714
spacing: 0.000024199983
```

That hypothetical recurrence is much better distributed in two dimensions. The decisive defect is the actual counter-plus-multiplication construction. Replacing the multiplier again would not repair it.

The earlier [7: **wave A3b report chose the golden-ratio multiplier because `48271` clustered consecutive seeds**](/home/lmoffatt/Projects/luthier/record/plan/audit-algebras-2026-10-22/report-wave-a-3b.md) correctly identified that earlier clustering. I reproduced it: at seed `20261020`, 100 values with multiplier `48271` occupy `[0.4259110593, 0.4281363750]`, a span of `0.0022253`. The replacement improved marginal spread while preserving deterministic dependence.

**A concrete failure of the advertised bound**

Consider the fixed failure set:

```text
A = {u : fractional_part(1597*u) < 0.1}
```

Its mass under the seed-induced marginal distribution is approximately `0.10000000056`. This predicate can be expressed as a finite union of intervals; it is not selected after observing a particular starting seed.

For this rotation:

```text
(1597*a mod m)/m = 0.000279936473947
```

Thus the transformed failure indicator moves very slowly between consecutive cases. With 100 cases, most starting seeds miss the failure set entirely.

Using 100,000 independently selected starting seeds from `Philox(20261027)`:

```text
fraction with zero observed failures: 0.87145
IID probability of zero failures:     0.9^100 ≈ 0.0000265614
epsilon_hat(100, 0.05):               0.0299573227
```

The rotation calculation predicts a no-failure probability near `0.8722863`, consistent with the probe.

Consequently, a law that fails on about 10% of the declared marginal distribution can receive a bound below 3% for roughly 87% of starting seeds. The allowed error probability was 5%.

**Smallest fix.** Stop assigning the IID confidence interpretation to this protocol. Preserve the observations and their provenance, but return unknown quantitative evidence, or the trivial bound `1`, until the sampling premise is supplied.

For replacement, I recommend a versioned Philox protocol with explicit key and counter coordinates for stream, case, parameter, rejection attempt and word. Mixture selection and fallback generation need distinct coordinates. The key must not depend on requested `n`, so extending a run preserves its prefix. [8: **NumPy’s Philox exposes key/counter state and guarantees a fixed integer stream for a fixed seed**](https://numpy.org/doc/1.26/reference/random/bit_generators/philox.html).

This remains a declared pseudorandomness premise supported by testing. Finite statistical checks cannot establish independence for every possible law.

**2. Critical: sampled and exhaustive census traversals can share an identity**

**Locations:** [certify.py:427](/home/lmoffatt/Projects/luthier/src/luthier/certify.py:427), [certify.py:477](/home/lmoffatt/Projects/luthier/src/luthier/certify.py:477), [tester.py:1353](/home/lmoffatt/Projects/luthier/src/luthier/tester.py:1353), [tester.py:2172](/home/lmoffatt/Projects/luthier/src/luthier/tester.py:2172), [tester.py:3050](/home/lmoffatt/Projects/luthier/src/luthier/tester.py:3050).

Mode is not an explicit identity field. It appears in the binding description for an unbound parameter, but disappears when every parameter has an explicit census.

I constructed this example entirely in memory:

```text
L(x, y) = (x == y)
x census = [0, 1]
y census = [0, 1]
seed = 7
requested cases = 100
```

Results:

| Mode | Traversal | Verdict |
|---|---|---|
| Sampled | Both censuses use the same case index, repeatedly visiting `(0,0)` and `(1,1)` | `Supported`, 100 cases |
| Exhaustive | Cartesian product of both censuses | `Refuted`, 4 cases, including `(0,1)` |

`certify.identity` returned **the same identity** for both entries.

**Concrete scenario.** After recording the sampled result, changing the directive to exhaustive can reuse the sampled entry as “known.” It need not discover the counterexample. A deep replay instead produces a disagreement between experiments that should have different identities.

The sampled traversal is also not 100 independent draws from the Cartesian product of the censuses. Merely repairing the identity would not justify its rule-of-three interpretation.

**Smallest fix.** Put the effective mode and traversal protocol explicitly in both `identity` and `union_key`, independently of parameter bindings. For census-only sampling, either draw from the declared joint distribution or identify the visited cases as listed evidence with their actual reach.

**3. High: pooling counts distinct starting seeds without establishing distinct sampling coordinates**

**Locations:** [certify.py:1196](/home/lmoffatt/Projects/luthier/src/luthier/certify.py:1196), [certify.py:1226](/home/lmoffatt/Projects/luthier/src/luthier/certify.py:1226), [certify.py:1254](/home/lmoffatt/Projects/luthier/src/luthier/certify.py:1254), [generators.py:34](/home/lmoffatt/Projects/luthier/src/luthier/generators.py:34).

`stretches` correctly keeps the largest `n` for each starting seed. It assumes different starting seeds identify independent stretches. The docstring explicitly acknowledges that this premise is owed by the generator protocol and is not checked.

For a generator such as `floatsWithin`, two 100-case stretches beginning at `s` and `s+1` share 99 generator coordinates. An in-memory call to `pooled` counted:

```text
reported cases:             200
distinct source coordinates: 101
```

This is repeated evaluation of the same generator positions, not ordinary duplicate values arising from independent sampling with replacement.

The host families have another issue: their persistent state is only the returned 31-bit seed. Reinitializing Mersenne Twister at every call does not preserve its large internal state or period.

Starting `generators.uniform_sample(1, seed)` at `20261020`, I found:

```text
first occurrence of repeated state: index 12145
repeat detected:                   index 18646
cycle length:                      6501
repeated seed:                     1746532400
```

Thereafter, the entire sequence repeats.

The first 10,000 outputs nevertheless passed the requested basic diagnostics:

| Check | Result |
|---|---:|
| Ten-bin χ² | `12.358`, p `0.193871` |
| Lag-one correlation | `−0.001026`, reference p `0.918327` |
| Runs | `4994`, z `−0.111813`, p `0.910972` |

This is a useful warning: short-run diagnostics can look sound while stream continuation is structurally defective.

**Concrete scenario.** Increasing `n` beyond the cycle keeps tightening `ε̂` while revisiting the same cases indefinitely. Starting another stretch at a previously reached state reproduces an existing tail, yet pooling treats it as new evidence.

**Smallest fix.** Identify draws by protocol, stream key and counter range, then pool the union of those coordinates. Deduplicate overlapping ranges. Preserve full generator state, or use a counter-based source that avoids the 31-bit state bottleneck. Adding a good mixer before continuing to trust the same returned 31-bit state is insufficient.

**4. High: ambient extern state changes results under an unchanged cone**

**Locations:** [run.py:1076](/home/lmoffatt/Projects/luthier/src/luthier/run.py:1076), [run.py:1659](/home/lmoffatt/Projects/luthier/src/luthier/run.py:1659), [host.py:80](/home/lmoffatt/Projects/luthier/src/luthier/host.py:80), [certify.py:373](/home/lmoffatt/Projects/luthier/src/luthier/certify.py:373).

The bridge imports the routed object and calls it. Neither its mutable state nor its ambient reads enter the cone. `host.reset` clears Luthier’s output, call and file-read records; it does not reset third-party RNGs or arbitrary module state.

I evaluated small in-memory programs through `Runner`:

| Extern dependency | Probe | Result | Cone changed? |
|---|---|---|---|
| NumPy global RNG | Seed once with `123`, evaluate, call `host.reset`, evaluate again | `0.6964691856`, then `0.2861393350` | No |
| RNG replay | Restore seed `123` and evaluate | First value reproduced | No |
| Environment | Read one process-local variable with values `"first"` and `"second"` | Different strings | No |
| Clock | Evaluate `python:time.time` twice | Different floats | No |

The first probe used `python:numpy.random.random`; the others used `python:os.getenv` and `python:time.time`.

I did not find the bundled numerical generators using NumPy’s global RNG. They use local seeded instances. The defect is in what the extern contract permits and identifies, including user and third-party externs.

**Concrete scenario.** An extern’s result depends on how many unrelated RNG calls occurred earlier in the process. A certificate can be reused without evaluating it again, or a deep replay can disagree under the same identity.

**Smallest fix.** Give cacheable externs an explicit dependency contract:

- RNG algorithm and state are explicit inputs, with returned state explicit too.
- Environment values that affect computation are explicit inputs or declared context dependencies.
- Clock and other world observations are explicit effects or captured observations.

Hashing an arbitrary current RNG state without restoring and isolating it is insufficient. Call ordering would remain an undeclared input. A blanket timestamp in every identity would also be the wrong repair: creation time is metadata unless computation reads it.

**5. High: numerical runtime state is absent from identity and changes results**

**Locations:** [arrays.py:72](/home/lmoffatt/Projects/luthier/src/luthier/arrays.py:72), [arrays.py:80](/home/lmoffatt/Projects/luthier/src/luthier/arrays.py:80), [certify.py:229](/home/lmoffatt/Projects/luthier/src/luthier/certify.py:229), [certify.py:381](/home/lmoffatt/Projects/luthier/src/luthier/certify.py:381).

**BLAS threading, with identical inputs.** I generated two vectors of length `1,000,003` from `default_rng(20261027)`, then called the repository’s `arrays.dot` under `threadpool_limits`:

| BLAS threads | Result |
|---:|---:|
| 1 | `1557.0554152537165` |
| 2 | `1557.0554152537015` |

The host hash was unchanged:

```text
sha256:c7402a82220449d91a36e663f3353b6b02799c9894a45655584167b122b6f2ef
```

A comparison against `1557.0554152537090` changes Boolean result.

**Other floating-point probes**

| Dependency | Probe | Observed difference |
|---|---|---|
| Rounding mode | Runtime operands `1 + 2^-53` | Nearest gives `1`; upward gives `1 + 2^-52` |
| Flush-to-zero controls | `2^-1022 × 0.5`, with FTZ/DAZ disabled versus enabled | Subnormal `2^-1023` versus `0` |
| Fused versus separate arithmetic | `(1+2^-27)(1−2^-27)−1` | Separate operations give `0`; libc `fma` gives `−2^-54` |
| NumPy error policy | Scale the smallest positive subnormal by `0.1` | `[0.0]` under `under="ignore"`; `FloatingPointError` under `under="raise"` |
| Sum order | NumPy sum of `[1e16,1,-1e16]` versus `[1e16,-1e16,1]` | `0` versus `1` |

Rounding and FTZ/DAZ controls were restored after each probe.

The sum-order example demonstrates arithmetic sensitivity; changing input order is not itself an identity collision. The BLAS experiment establishes the collision with unchanged input arrays. The FMA experiment demonstrates the consequence of an arithmetic implementation choice; it was not a comparison between two CPUs.

For each requested platform dependency:

| Dependency | Can change a result? | In identity now? | Smallest fix |
|---|---|---|---|
| CPU and selected numerical kernel | Yes; FMA and reduction choices matter. A second CPU was not tested. | No explicit CPU or dispatch identity. | Record the relevant architecture and selected numerical implementation, or enforce a specified execution profile. |
| Linked BLAS/LAPACK build | Yes. | No for the local wrappers; direct package routes record only package/version. | Identify loaded numerical binaries and their build. |
| Threading | Yes, directly reproduced. | No. | Enforce and identify the effective thread configuration. |
| Rounding mode | Yes, directly reproduced. | No. | Set or validate it at execution boundaries and include the profile in identity. |
| FTZ/DAZ | Yes, directly reproduced. | No. | Set or validate the controls and identify them. |
| FMA policy | Yes, demonstrated numerically. | No. | Identify the selected implementation/build, or prescribe arithmetic semantics. |
| NumPy error policy | Yes, directly reproduced. | No. | Set or validate `np.geterr()` policy and identify it. |

A numerical context must be enforced, not merely observed once. An extern or worker thread can otherwise change it after identity construction.

NumPy itself limits stream reproducibility to the same build, environment and machine, and explicitly discusses CPU and LAPACK differences. [9: **NumPy’s compatibility contract includes these runtime dependencies**](https://numpy.org/doc/1.26/reference/random/compatibility.html).

**6. High: host hashes omit Python and transitive host dependencies**

**Locations:** [certify.py:199](/home/lmoffatt/Projects/luthier/src/luthier/certify.py:199), [certify.py:229](/home/lmoffatt/Projects/luthier/src/luthier/certify.py:229), [tester.py:3005](/home/lmoffatt/Projects/luthier/src/luthier/tester.py:3005), [run.py:2665](/home/lmoffatt/Projects/luthier/src/luthier/run.py:2665).

The code currently identifies:

- A local host module by the bytes of that one source file.
- An installed package route by distribution name and version.
- A direct standard-library or built-in route by Python’s version.
- The Luthier interpreter by its latest reachable tag, currently `v0.3`.

This leaves two gaps.

**Transitive dependencies.** Both `python:luthier.arrays.dot` and `python:luthier.arrays.solve` hash only `arrays.py`. The imported NumPy implementation, BLAS/LAPACK binaries and build configuration are absent. A direct `python:numpy.dot` route gives only `numpy 1.26.4`; different builds can retain that string.

**Python version.** Python’s version is not a global cone component. A direct standard-library route gets it, but a local wrapper that calls Python or NumPy does not. The drawing revision hashes selected tester source and `generators.py`, not the Python RNG implementation.

The run record’s `"python"` field is useful provenance, but recording it after admission does not make it part of certificate identity or freshness.

**Concrete scenario.** Upgrade NumPy behind an unchanged `arrays.py`, or upgrade Python while retaining the Luthier tag and local source. Relevant identities remain unchanged despite a possible behavior change. Python 3.12’s changed float-summation algorithm is a documented example of runtime semantics changing across versions. [10: **Python documents the summation change in 3.12**](https://docs.python.org/3.12/library/functions.html#sum).

I did not run a second Python version. The omission is established by the identity construction, and the numerical consequences of missing runtime dependencies were reproduced above.

**Smallest fix.** Add a runtime identity containing Python implementation/version/build, and add declared transitive dependency manifests for host modules. Numerical manifests need the loaded native builds, not just package version strings.

Put their digest into cones and generator fingerprints, and compare it when serving evidence. An extra descriptive field in the stored entry would not repair freshness.

**7. High: verdict-producing tester and bridge code is outside the content identity**

**Locations:** [tester.py:878](/home/lmoffatt/Projects/luthier/src/luthier/tester.py:878), [tester.py:3000](/home/lmoffatt/Projects/luthier/src/luthier/tester.py:3000), [run.py:1659](/home/lmoffatt/Projects/luthier/src/luthier/run.py:1659), [certify.py:199](/home/lmoffatt/Projects/luthier/src/luthier/certify.py:199).

The drawing revision hashes a selected list of functions. That list includes `run_spec`, but not `evaluate`, which decides a case’s verdict. Hashing the source that calls a function does not hash the callee’s implementation.

In an isolated in-memory probe, I replaced `tester.evaluate` with a function returning false, cleared the drawing-revision cache and reconstructed the entry:

```text
original verdict: Supported
replacement verdict: Refuted
entry identities equal: True
```

The probe isolates the identity boundary; it is not evidence of a current incorrect implementation of `evaluate`.

The bridge’s execution and conversion behavior also lives in `run.py`, outside the routed host module’s source hash. Hashing `kernel.py` under the settled kernel decision does not automatically identify those components.

**Concrete scenario.** Correct a tester verdict rule or host conversion rule without changing a tag, kernel source, generator source or law. An old entry can still be reused as known, although re-evaluation would differ.

**Smallest fix.** Add content identities for the verdict-producing certifier and host bridge. Keep reporting-only changes outside them. Apply the kernel decision’s granular transport approach where appropriate, while keeping these components explicit.

**What looked sound**

Several mechanisms are already doing useful work:

- The formula `min(1, −log δ/n)` is a conservative zero-failure bound under IID sampling. The defect is its application, not its algebra.
- [11: **the B1 report deliberately computes `(ε̂, δ)` at serve time from stored counts**](/home/lmoffatt/Projects/luthier/record/plan/audit-algebras-2026-10-22/report-b1-b3-d1.md). This avoids baking one demand’s `δ` into an entry.
- The default capped-sum composition does not require independence between obligations. It cannot repair invalid evidence supplied by an individual obligation.
- [12: **bite 13c added distribution-changing budgets to both entry identity and pooling identity**](/home/lmoffatt/Projects/luthier/record/plan/core-2026-10-17/report-bite-13c.md). Those fields remain present.
- Generator cones, binding fingerprints, sizes and drawing revisions are recorded on the appropriate generation paths.
- Pooling correctly avoids counting the same starting seed again merely because a longer prefix was recorded.
- Host families use private seeded RNGs. Their short-stream diagnostics looked reasonable.
- The actual built-in `Values.draw(Float64)` path also looked reasonable in this probe. With seed `20261020` and 10,000 cases, its 9,403 continuous draws gave χ² p `0.237551`, lag-one correlation `−0.001843`, and runs p `0.711387`. The atom and special-value branches were preserved.
- Replay disagreement preservation is a useful diagnostic. It exposes hidden dependencies when a replay happens, although ordinary known-entry reuse does not trigger that diagnostic.
- Certificate creation dates should remain metadata. They need identity treatment only when time is an input to the computation.

The declared `Random` uniformity and independence laws do not currently certify `scrambled`. The model explicitly says the corresponding p-value leaves and host model are unfinished at [generators_model.lut:148](/home/lmoffatt/Projects/luthier/src/luthier/lib/generators_model.lut:148).

**Recommended repair and migration**

The smallest coherent repair has three parts.

1. **Contain the unsupported statistical claim.** Retain old evidence and observed counterexamples, but do not serve an informative IID bound for protocols whose sampling premise is absent or refuted.

2. **Version the sampling protocol explicitly at entry level.** Replace the rotation and 31-bit continuation mechanism with a specified stream protocol, identify counter ranges, and put mode and traversal semantics into identity and pooling. A first implementation can use Philox; it should include fixed known-answer vectors and explicit integer-to-float and bounded-integer conversions.

3. **Identify and enforce execution dependencies.** Add certifier, bridge and runtime context identities, plus declared extern dependencies. Use explicit inputs or effects for ambient RNG, environment and time dependencies.

**Every sampled identity must move for the sampling-protocol migration.** Changing `generators.py` changes `drawing_revision`, but today not every sampled entry carries that revision. Census-only sampled entries demonstrate the gap. An explicit entry-level protocol revision must cover them too.

Old and new stretches must not pool together. Existing entries should remain historical evidence under their original protocol. They must not be relabelled with today’s runtime context, which was not recorded when they ran.

Runtime repairs may also move exhaustive and listed-case identities when they depend on the affected hosts or execution machinery. Pure finite evidence should retain its actual domain and provenance; it should not be treated as independent sampling merely to preserve an old grade.

For validation after repair, the concrete regressions this audit establishes are:

- The census-only sampled/exhaustive identity collision.
- Stream overlap and the reproduced 31-bit continuation cycle.
- The rotation’s serial, runs and spectral failures.
- Same-input dot results under different thread counts.
- Rounding, FTZ and NumPy-error-policy changes.
- Extern RNG, environment and clock dependencies.
- A changed verdict implementation retaining the old entry identity.

No repository tests were executed because the requested procedure was read-only and the ordinary certification/test commands can write records. All reported probes completed through direct in-memory functions.

**Decisions taken during this audit**

I selected the probes and severity ordering, used Philox as the proposed replacement, and treated the kernel decision as settled. These are audit recommendations, not implemented project decisions. No source, specification, store, record or memory file was changed.


