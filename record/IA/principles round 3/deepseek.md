## Break 1 — L10 (draft 5): composed sampled identity links

**Example.** Over `Float64`, let `f : Float64 -> Float64` have three implementations:

```
A = f_native
B = f_series
C = f_extern_fast
```

Certificates:

```
id_AB : d(A x, B x) <= 0.04   grade sampled, seed 0, U[0,1]
id_BC : d(B x, C x) <= 0.04   grade sampled, seed 0, U[0,1]
```

Demand:

```
y := f(1.5) : Float64 tolerance 0.1
```

At `x = 1.5`, outside the sampled distribution:

```
A(1.5) = 0.00
B(1.5) = 0.04
C(1.5) = 0.14
```

So the true distance is `d(A(1.5), C(1.5)) = 0.14 > 0.1`.

**Rule’s verdict, step by step.**

1. L10 says the law gives the candidates `A, B, C`.
2. The identity certificates say which the planner may exchange.
3. The path `A → B → C` sums distances: `0.04 + 0.04 = 0.08 <= 0.1`.
4. L10 says the sum is a bound only when every link is `proved` or `exhaustive`; here both are `sampled`, so the sum is only an estimate.
5. But L10 does not forbid using the estimate. It allows the substitution path whose summed distance is within the demanded tolerance.
6. The planner returns `C(1.5) = 0.14`, which is outside the demanded tolerance `0.1`.

**One-line fix.** Only compose identity links whose grade is `proved` or `exhaustive`; `sampled` links may be used only as direct edges, never summed into a substitution path.

---

## Break 2 — L19 (draft 6): result identity lacks the host runtime

**Example.** Same Luthier code, inputs, mode, type, tolerance, model, seed and plan, but different host numerical library:

```
code h:
  A := extern openblas_dgemm A B
  main: print A : Float64 tolerance 1e-9
```

Run 1:

```
host: OpenBLAS 0.3.26, x86_64, NumPy 1.26
```

Run 2:

```
host: MKL 2024, arm64, NumPy 2.0
```

L19 identifies a result by:

```
code, inputs, mode, demanded type and tolerance, model, seed, plan
```

The host runtime and library version are absent. So these two runs have the same result identity.

**Rule’s verdict, step by step.**

1. L19 says the result is identified by code, inputs, mode, demanded type and tolerance, model, seed and plan.
2. Run 1 and run 2 agree on all those fields.
3. L19 therefore treats the two results as the same result.
4. Certificates may supersede by hash, and L14/W10 can bind the extern certificate to the host library version.
5. But the result memo key does not include the host version. It can serve run 1’s result to run 2 without rerunning the extern.
6. A scientist cares: the same nominal run on a different BLAS/CPU can produce different floating-point output. If the difference exceeds the tolerance, the reused result is wrong; even if it does not, the run is not reproducible.

**One-line fix.** Add the host runtime and library version/platform, or the extern certificate hash, to the result identity.

---

## Break 3 — L14 (draft 5, proposed): an extern with no laws yet

**Example.** A function starts with no laws, as L14 says every function does:

```
theory Sin
  sin : Float64 -> Float64
  -- no laws yet

native sin_native x = series20 x
extern sin_fast x = if x <= 1.0 then series20 x else 0.0
```

Identity certificate:

```
id_native_fast : d(sin_native x, sin_fast x) = 0
  grade sampled, seed 0, U[0,1]
```

Demand:

```
y := sin(2.0) : Float64 tolerance 1e-6
```

**Rule’s verdict, step by step.**

1. The type `Sin` has no laws yet.
2. L14 says an extern with no laws may run, with its certificate graded by what it has.
3. It may replace the native only by the identity law of L21.
4. L21 samples `x ∈ [0,1]`; on that sample `sin_fast` is bit-identical to `sin_native`.
5. The planner substitutes `sin_fast` for `sin_native` on `sin(2.0)`.
6. `sin_fast(2.0) = 0.0`; the true `sin(2.0) ≈ 0.909`. The error is far above `1e-6`.
7. G2 should have refused this: no law `sin(x+2π)=sin(x)` or `sin(π/2)=1` certified the description. The identity law only says “same as native on sampled cases,” which is acquaintance, not description.

**One-line fix.** An extern with no laws may run only in a hole or beside the native; it may replace the native only after at least one non-identity law of its type is certified.

---

## Rank by how early it bites sonolocalización on floats

1. **L14** — first extern, before any laws exist. Sonolocalización will wrap Python/C FFT, filtering and linear-algebra routines immediately; identity on small samples admits a host function that fails outside the sampled domain.
2. **L19** — as soon as expensive float results are memoized across host/library versions or machines. Sonolocalización will cache runs; missing host identity reuses stale numerical results.
3. **L10** — after laws, multiple implementations, identity certificates and a planner exist. It still bites on floats, but it requires more machinery than L14 or L19.