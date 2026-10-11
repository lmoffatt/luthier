I can break all three, but in different senses. L10’s exact core is sound; its failure enters through non-exact certificates. L19 has a genuine identity collision. L14 has a bootstrapping hole that is semantically more serious than its wording admits.

### 1. L10 — two implementations are enough once a sampled certificate is allowed

L10 says substitutions form a weighted graph; the planner may traverse a path when the summed certified distance is within the demanded tolerance. Only `proved`/`exhaustive` links are bounds; sampled links are estimates carrying their grade and samples. principles_2

Paper example:

```text
tof : Trace -> Time

tof_native := ...
tof_fft    := extern Python ...

C : d(tof_native x, tof_fft x) ≤ tol
C.grade        := sampled
C.level        := 0.99
C.distribution := D_even_length
C.worst_seen   := 0.2 us
```

Suppose `D_even_length` sampled ordinary even-length acquisition blocks. Now demand:

```text
tof x_prime
tol   := 1 us
grade := sampled 0.99
```

where `x_prime` is a prime-length trace exposing an FFT-padding/wraparound case:

```text
tof_native x_prime = 41 us
tof_fft    x_prime = 57 us
```

So the actual distance is `16 us`.

**Rule's verdict, step by step**

1. `tof_native` and `tof_fft` are two specimens of the same declared function.
2. There is a pairwise identity certificate between them.
3. Its observed distance, `0.2 us`, is below the demanded `1 us`.
4. Its grade is `sampled 0.99`, which satisfies a demand that accepts `sampled 0.99`.
5. Therefore the planner may replace `tof_native` by the cheaper `tof_fft`.
6. It returns `57 us`.
7. On this actual input the error is `16 us > 1 us`.

The important defect is not that sampling can miss a rare failure—that is unavoidable and L2 explicitly acknowledges it. The defect is that nothing in L10 requires the **scope of the certificate to cover the substitution being made**. L11 remembers the sampled distribution, but L10's admissibility rule does not say that the current input/domain/demanded distribution must be covered by it.

This is already minimal: **2 implementations + 1 certificate**.

There is an important sound subcase. If every edge is `proved` or `exhaustive`, is about the same model/domain, and `d` really is a metric, then I cannot construct the requested counterexample. For a chain

```text
A --e1--> B --e2--> C
```

triangle inequality gives

```text
d(A,C) ≤ d(A,B) + d(B,C) ≤ e1 + e2 ≤ tol.
```

So the graph-and-sum rule itself is fine under those hypotheses. The hole is letting empirical edges participate as though their observed cost were a bound.

**One-line repair**

> A substitution edge is admissible only where its certificate's validity domain/distribution covers the current demand; a sampled cost may satisfy a tolerance only through a certified probabilistic bound, never merely through the worst value observed.

That preserves sampled optimization instead of banning it.

---

### 2. L19 — same result identity, different extern realization

L19 defines a realization by `code, inputs, mode, demanded type and tolerance, model, seed, plan`; certificates are separate immutable objects superseded by hash. principles_2

But L14 separately requires an extern certificate to bind the host library version and platform. principles_2

That creates a direct collision.

Consider:

```text
xcorr : Trace -> Correlation
xcorr_fast := extern Python ...

tau := peak(xcorr_fast signal)
```

Two runs:

```text
Run A
code          = H
inputs        = I
mode          = forward
demanded type = Time
tol           = 1 us
model         = Float64
seed          = 17
plan          = P

extern certificate = C1
host library       = FFT implementation/version V1
platform           = machine P1

result = tau_A
```

and later:

```text
Run B
code          = H
inputs        = I
mode          = forward
demanded type = Time
tol           = 1 us
model         = Float64
seed          = 17
plan          = P

extern certificate = C2
host library       = FFT implementation/version V2
platform           = machine P2

result = tau_B
```

Take a trace where two correlation peaks are almost tied. V1's floating-point reduction makes peak `k` infinitesimally larger; V2's reduction makes `k+1` larger.

Thus:

```text
tau_A = k     / fs
tau_B = (k+1) / fs
```

For sonolocalización that is a physically different inferred range. A scientist absolutely cares which echo won.

**Rule's verdict**

1. Same Luthier code: yes.
2. Same input bytes: yes.
3. Same mode: yes.
4. Same demanded type and tolerance: yes.
5. Same model `Float64`: yes.
6. Same seed: yes.
7. Same plan `P`: yes; it still says use `xcorr_fast`.
8. Therefore L19 assigns the **same result identity**.
9. L14 correctly generates a different certificate because the host version/platform changed: `C1 != C2`.
10. But the certificate hash is not in the result identity.
11. Therefore two scientifically different realizations collide in the memo key.

Worse, Run B may never expose the difference: the memo can return Run A's value because its result key is identical.

`plan` does not rescue the rule as written. The document says the plan records the selected realization/path, but L14 deliberately keeps host version/platform in the certificate. If those data were already part of `plan`, the explicit certificate requirement would be redundant.

**One-line repair**

> A result is identified additionally by the hashes of all implementation/environment certificates in its live dependency cone.

Equivalently:

```text
ResultId :=
  hash(code, inputs, mode, demanded type, tolerance,
       model, seed, plan, certificate_cone)
```

Then superseding `C1` with `C2` necessarily creates a new realization.

This is the cleanest actual bug of the three.

---

### 3. L14 — perfect native/extern agreement can certify the wrong concept

G2 says the laws are what is known of a function and implementations are specimens; agreement between specimens is not itself description. principles_2 L21 makes the separation explicit: identity of implementations and certification of the law are different certificates. principles_2

L14 nevertheless permits a lawless extern to run and says it may replace the native by the identity law alone. principles_2

Take the first sonolocalización concept:

```text
delay : Trace -> Time
```

No descriptive laws exist yet.

Someone writes the obvious prototype:

```text
delay_native :=
    time_of(argmax(cross_correlation(trace, pulse)))

delay_fast :=
    extern Python ...
```

The Python implementation performs exactly the same algorithm.

Hence the identity certificate is excellent:

```text
d(delay_native x, delay_fast x) = 0
```

possibly even `proved`, not sampled.

Now use a multipath trace:

```text
direct echo:       10 ms, amplitude 0.2
wall reflection:   12 ms, amplitude 1.0
```

Both specimens return:

```text
delay_native x = 12 ms
delay_fast   x = 12 ms
```

But suppose the scientific concept intended by `delay` is **first-arrival propagation time**. The scientifically meaningful answer is `10 ms`.

**Rule's verdict**

1. `delay` currently has no laws.
2. L14 therefore does not validate `delay_fast` against descriptive laws.
3. It is allowed to run.
4. It agrees perfectly with `delay_native`.
5. The L21 identity certificate therefore admits it as a replacement.
6. The planner may use the faster extern.
7. The result is `12 ms`.

Nothing has failed according to the identity test.

But G2 has learned literally nothing that distinguishes:

```text
first arrival
strongest arrival
centroid of arrivals
matched-filter maximum
last arrival
```

All are inhabitants of the bare structural signature

```text
Trace -> Time
```

until a descriptive law says otherwise.

So the sentence in L14 that identity “admits a specimen and never certifies the description, so G2 is not bypassed” is too optimistic. G2 is not bypassed **epistemically**—the system does not falsely claim a descriptive certificate—but it is bypassed **executively**: the undescribed specimen is nevertheless allowed to provide the scientific value.

This failure survives even with a perfect, exact identity certificate. Native and extern can be identically wrong about what the named concept was supposed to mean.

**One-line repair**

> A lawless extern may be executed explicitly as a specimen, but neither it nor the native enters L10's substitution graph for a named function until at least one non-identity descriptive law of that function has been certified.

That still permits the early exploratory workflow. It merely distinguishes:

```text
"run this specimen"
```

from

```text
"this specimen realizes the concept delay".
```

That distinction seems exactly G2.

## Order in which these would bite sonolocalización

**1. L14 — earliest.** W5 explicitly says sonolocalización grows by writing a conceptual native and a pragmatic extern together. The first scientifically ambiguous operation—arrival time, peak, envelope, threshold crossing—can therefore acquire operational meaning from two agreeing specimens before it has any descriptive meaning. This can bite on day one.

**2. L10.** As soon as the first faster Float64 path is selected from empirical native/extern agreement, certificate scope becomes important. Float algorithms are precisely where “worked on these sampled traces” must not silently become “interchangeable on this trace.”

**3. L19.** This becomes damaging once the cross-run memo exists and the same analysis is rerun after a Python/FFT/BLAS/platform change. The document itself still lists the session memo as pending, so this is likely to appear later in implementation, although once memoization exists it is a serious reproducibility failure. principles_2

Of the three, I would change **L14 first** because it changes what Luthier is allowed to call a realization of a scientific concept. I would change **L19 before implementing the memo**, because its current key is not provenance-complete. L10 needs a smaller but important qualification: **certificate applicability must be part of edge admissibility**.