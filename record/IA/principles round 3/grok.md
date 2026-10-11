**1. L10 (draft 5) – planner substitution along certified pairwise equivalences**

**Example (smallest set that returns a wrong result).**  
Three implementations of the same function `f : Real → Real` under the theory `Real`, realized in `Float64` (the carrier that matters for sonolocalización):

- `N` – the native holotype formula evaluated over `Float64`.  
- `A` – an extern that is bit-identical to `N` on the sampled set used for the identity certificate.  
- `B` – an extern that is bit-identical to `A` on a *different* sampled set.

Identity certificates (both graded `sampled`, weakest grade therefore `sampled`):

- `id(N,A)` with observed distance \(d_{NA}=0.0\) (exact on its samples).  
- `id(A,B)` with observed distance \(d_{AB}=0.0\) (exact on its samples).

No direct certificate \(id(N,B)\).  
Demand: tolerance \(\varepsilon=0.0\) (exact bits), seed \(s\), plan \(P\) that asks for any representative of the class.

Planner builds the weighted graph and finds the path \(N \xrightarrow{0} A \xrightarrow{0} B\). Summed distance \(0+0=0\le\varepsilon\). It therefore substitutes \(B\) for \(N\).

On a fresh input that lies outside both sample sets (the classic float case that appears in acoustic range calculations), \(B(x)\neq N(x)\) by several ulps. The planner returns the wrong value while believing the substitution is certified.

**Verdict step by step.**  
1. Law of \(f\) supplies the candidates \(\{N,A,B\}\).  
2. Identity certificates exist only for the two edges.  
3. L10 explicitly permits a path whose *summed* distances stay inside the demanded tolerance.  
4. Both edges are \(0\), sum is \(0\), substitution is legal.  
5. Transitivity fails for sampled (or even exhaustive) distances on floats; the missing direct edge is exactly the one that would have revealed the error.

**One-line fix.**  
“A substitution is admitted only by a *direct* identity certificate whose distance (or bound) is within the demanded tolerance; paths of length >1 are forbidden until every link is proved/exhaustive and the algebra of composition is closed.”

**2. L19 (draft 6) – result identity by (code, inputs, mode, demanded type+tol, model, seed, plan)**

**Example (two runs treated as identical that a scientist must distinguish).**  
Same definition of a matrix inverse used in the covariance step of a sonolocalización pipeline:

- Code hash identical.  
- Inputs identical (same measured array).  
- Mode, demanded type (`Float64`), tolerance, model, seed identical.  
- Plan \(P\) identical (same topological order, same choice of bridges).

Run 1: the host BLAS library is version 1.2; the result \(R_1\) is written to the memo under the identity key above.  
Run 2: the host library is silently upgraded to 1.3 (or the machine changes NUMA layout, or a different number of OpenMP threads is used). The numerical result \(R_2\) differs in the last few ulps—enough to move a localization peak across a decision boundary.  

Because the identity key does not contain the host-runtime version, platform fingerprint, or any other environmental hash, L19 treats the two results as the same memo entry. The second run is never recomputed; the scientist sees the stale value.

**Verdict step by step.**  
1. L19 enumerates the exact fields that form the identity.  
2. Host-runtime version / platform / thread schedule are absent.  
3. Certificates supersede only by re-hashing those fields; an environmental change leaves the key unchanged.  
4. The memo therefore serves the old result.  
5. For any floating-point numerical library the difference is scientifically material.

**One-line fix.**  
“Add the host-runtime identity (library versions, platform fingerprint, thread/NUMA configuration) to the memo key; a change in any of them forces a new plan node.”

**3. L14 (draft 5, proposed) – extern with no laws yet may replace native only by identity**

**Example (extern that G2 should have refused).**  
Native holotype of `speed_of_sound : Real → Real` (temperature dependence) written over the theory `Real`.  
No laws have yet been stated for the function (the normal starting point under D-2026-10-11-d).  

An extern `E` is declared with the same signature. On the first demand it is applied under the declared type (L14 allows this when laws are absent). An identity certificate \(id(N,E)\) is obtained on a small sample set and is graded `sampled`. The planner therefore admits \(E\) into the substitution graph of L10.

`E` implements a completely different physical model (wrong functional form). Because no diagnostic law exists, the identity check only confirms “same bits on these points”; G2’s requirement that a specimen be recognized *by description* is never enforced. The wrong model is used for the rest of the localization pipeline.

**Verdict step by step.**  
1. L14: “where it has none yet \ldots it runs \ldots and may replace the native only by the identity law of L21 \ldots which admits a specimen and never certifies the description”.  
2. The identity law is satisfied on the samples.  
3. No law of the theory is ever checked, so G2 is bypassed exactly as the draft claims it is not.  
4. The planner (L10) thereafter treats \(E\) as interchangeable.

**One-line fix.**  
“An extern may be applied under a type that still has no laws, but it may never enter the planner’s substitution graph until at least one non-identity law of the theory has been certified against it.”

**Ranking by how early each bites an implementation of sonolocalización on floats**

1. **L14** – bites first. The very first external numerical routine (speed of sound, hydrophone response, FFT \ldots) arrives with zero laws; the identity-only admission is the default path.  
2. **L10** – bites as soon as two or more float implementations exist and the planner is allowed to walk multi-hop paths (the common case once a few externs have been admitted).  
3. **L19** – bites later, only after a library or platform upgrade occurs under an otherwise identical memo key; still inevitable on any real floating-point stack, but not on day one.