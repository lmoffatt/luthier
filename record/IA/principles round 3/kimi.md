# Three breaks, worked on paper

All examples use sonolocalización's daily material: float signals, host libraries, sampled evidence.

---

## 1. L10 (draft 5) — the planner's substitution has no coverage premise

**Smallest failing set: 2 implementations, 1 sampled certificate. A single link suffices.**

**The example.** Function `delay : Signal -> Time` (cross-correlation peak). Two implementations:

```
d_native  -- slow, direct cross-correlation
d_fast    -- downsampled cross-correlation, 40x faster
```

One certificate, the identity law of L21 with its result `Cost`:

```
id₁ : d(d_native x, d_fast x) ≤ ε/2   grade sampled at 0.99
      on D = white noise, band-limited 0–8 kHz, 10⁴ samples
```

Demand: `print (delay click)` with tolerance ε, where `click` is a 40 kHz pulse. Calibration only ever ran the speaker's noise test signal — D is what the lab recorded; the click is outside D's support. On white noise the correlation peak is broad-band and the downsampling shift stays under ε/2. On the narrowband click, downsampling shifts the peak by **3ε**. (This is exactly where L11 says errors concentrate: the edges of the sampled distribution.)

**The rule's verdict, step by step:**

1. "The law gives the candidates" — {d_native, d_fast}. ✔
2. "The identity certificates say which the planner may exchange" — edge d_native —d_fast exists, weight ε/2. ✔
3. "A substitution is a path whose summed distance is within the demanded tolerance" — one link, sum ε/2 ≤ ε. **Substitution legal.** ✔
4. Result returned; grade sampled-0.99 attached; the cone says nothing false.

The failure sits in step 3: the summed-distance test compares the certificate's *number* against the tolerance, and the rule never asks whether the demanded input lies inside "the samples it was seen on" (draft 5 records the samples but attaches no premise to them). The planner extrapolates an estimate past its support, and L10 as written licenses it.

**Where it cannot fail.** If the link is `proved` or `exhaustive` over the demanded domain, |A−C| ≤ δ₁+δ₂ is a theorem — the triangle inequality for the metric — and no example exists. So the break is confined to sampled links used outside their samples. On floats that is not a corner case: L21 notes two float implementations are almost never bit-identical, so `Bool` links don't exist; every link is `Cost` plus a sample. The vulnerable configuration is the only configuration.

**One-line fix.** Add to L10: *a substitution at an input outside the certificate's sampled domain is legal only after a fresh identity check at that input's distribution; the summed-distance bound applies to the points the certificate was seen on.*

---

## 2. L19 (draft 6) — the result's identity omits the demand's stated grade

**The example.** Same program, same inputs, same mode, same demanded type, same tolerance, same model, same seed, same plan — two runs:

- **Run 1.** Interactive session, demand states no grade requirement (lenient default). Result cached. Cone: `shift_invariant: assumed` (law stated, never run — every function starts here, D-2026-10-11-d), `id(native, extern): sampled 0.99`. Memo key K.
- **Run 2.** Calibration run for a paper. Demand states grade requirement `sampled` (L19 draft 5: "the demand states the grade it requires"; a certificate "serves every demand whose tolerance and grade it meets"). Everything else identical to run 1. Memo key K.

**The rule's verdict, step by step:**

1. Identity tuple: (code, inputs, mode, demanded type and tolerance, model, seed, plan) — identical. **Memo hit.** ✔
2. Draft 6: "a certificate is a frozen snapshot by hash; a later test does not change it." The cached cone is served as-is. ✔
3. The gate — "serves every demand whose tolerance *and grade* it meets" — is checked when a certificate is *issued*, not when a memo entry is *served*. The memo key contains tolerance but not the stated grade, so run 2's demand is answered by run 1's evidence without the grade requirement ever being applied. ✔

The two runs are "the same result" by the identity; a scientist cares because one of them is allowed to carry an `assumed` hole where the other demanded `sampled`, and the memo cannot tell them apart. Publishable-grade and exploratory-grade results share one hash class.

**Second witness, same hole.** W10 binds the extern's certificate to "the host library's version and the platform" — and the L19 identity tuple has no field for it. scipy 1.11 → 1.12 between runs, same K, memo hit; L21's rerun-identity check ("same bits, same seed ⇒ implementation unchanged") never fires because memo hits don't run. Two runs, same identity, different numbers.

**One-line fix.** *The result's identity includes the demand's stated grade and the hash of every certificate in the cone, extern version and platform bindings included; a memo hit is legal only if the cached certificates meet the current demand's grade.*

---

## 3. L14 (draft 5) — the identity certificate can answer the grade gate

**The example.** `correlate : (Signal, Signal) -> Signal`. Laws stated (shift-invariance, symmetry) but never run — grade `assumed`. Native `c_native` slow; `extern scipy.signal.fftconvolve`, which internally zero-pads to the next power of two and therefore quietly breaks circular shift-invariance on long signals. No laws on the extern — where it "starts," as everything starts (D-2026-10-11-d).

**The rule's verdict, step by step:**

1. "Where it has none yet … it runs with its certificate graded by what it has" — the extern runs, grade `assumed`. ✔ per the rule as written.
2. Identity law c_native ↔ extern, sampled on white noise, distance ≤ ε, level 0.99 — passes on short windows (padding invisible at that length). "May replace the native only by the identity law" — **admitted into the class.** ✔ (L10, D-2026-10-11-m.)
3. A demand arrives stating grade requirement `sampled`. The gate is "a certificate serves every demand whose tolerance and grade it meets." The cone at the node now contains a certificate graded sampled-0.99 — **the identity certificate.**
4. Nothing in L14, L19, or L2 forbids an identity certificate from meeting a grade requirement; L21's title ("a certificate of identity is not a certificate of the law") states the principle but the gate doesn't read it. Gate passes; the planner picks the extern (faster); the result leaves with a cone that *presents* `sampled` while no law was ever validated against the extern — not once.

G2 should have refused exactly here: "validada aunque sea una vez" is validation against a description, progressive from the laws; the extern was validated against nothing but its resemblance to another specimen — which W5's restatement itself demotes to "a consistency check between specimens," and which cannot see the padding bug because that bug lives where the identity test never looked. The mechanism meant to protect G2 — the demand's grade requirement — is fed by the one certificate kind that certifies nothing about the description. The break needs the natural implementation detail the document never specifies: which certificate at a node answers the demand's grade requirement. Take the strongest in the cone, and L14 leaks.

**One-line fix.** *An identity certificate admits a specimen into the planner's class but never raises a node's grade: a demand's grade requirement is met only by certificates of the laws.*

---

## Ranking: how early each bites sonolocalización on floats

1. **L14 — first day.** The project runs on the native/extern loop (W5); sonolocalización lives on scipy-style host libraries, so the first fast path is an extern with no laws, admitted by an identity test. From that moment every optimized result carries a cone that presents sampled evidence where nothing was checked against a description, and the corruption is silent — it compounds into every downstream certificate.
2. **L10 — first week.** Bites when the planner actually substitutes outside the calibration distribution. Sonolocalización inputs (clicks, tones, echoes, reverberant tails) are narrowband and heavy-tailed; white noise — the distribution a lab actually samples — misses precisely the edges where L11 says errors concentrate. Requires sampled links, which on floats is all there is.
3. **L19 — first paper / first host upgrade.** Needs a second demand with a different stated grade, or a library bump across sessions. Latest to bite, but it is the one that reaches the publication: the memo cannot distinguish the exploratory run from the calibration run.

The pattern across the three: each rule *records* the protective information (samples seen on, tolerance checked at, certificate kind, grade required, version bound) and none of them *promises* it at the decision point — substitution, grade gate, memo hit. Three one-line additions, all of the same shape: make the recorded premise a condition of the act.