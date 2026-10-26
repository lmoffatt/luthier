# Basis for Comparing Luthier with Its Antecedents

This document specifies the experimental and analytical protocols for Part 1 of `plan.md`: comparing each part of Luthier that has a published antecedent in `related-work.md` against that antecedent on shared inputs, so that a paper can state with evidence where Luthier is equivalent, where it is weaker, and where it is stronger.

## Ordering Criterion

The thirteen comparisons below are ordered by **how much their outcome could force a change in a paper's core claims**:

1. **Rank 1 to 4 (Foundational quantitative and statistical claims):** Comparisons that test whether Luthier's static bound transformers (`BoundTransformer` and `Within`), sampled evidence pairs $(\hat\varepsilon, \delta)$ under sequential pooling, per-conjunct negative controls (`L9.14`), and proposed midpoint-radius balls (`RadiusWithinTransformer`) are sound and tight against established numerical and statistical tools (Herbie, Daisy, Rosa, Clopper-Pearson, Wald's SPRT, Howard et al.'s confidence sequences, FitSpec, and Arb/`python-flint`). A failure here would require changing a core mathematical formula or certification rule in Luthier.
2. **Rank 5 to 7 (Structural certification and caching mechanisms):** Comparisons that test whether Luthier's law normal form (`canon` plus certified AC-normalization), premise vacuity detector (`Vacuous n`), and dependency cone hashing (`canon(cone(n))`) match the recall and invariance of term rewriting/`egg`, Beer et al.'s vacuity detection, and Unison/Nix content addressing. A gap here would require qualifying the scope of `luthier check` and `luthier certify` or refining the normalizer/hasher.
3. **Rank 8 to 13 (Type-theoretic, provenance, planning, and world-action counterparts):** Comparisons that evaluate Luthier's sensitivity combinators, planner pull-back, refinement subtypes and generators, run records and derivations, LLM specification synthesis/routing, and single-use world token `W` against Fuzz/Granule, PetaBricks/Chisel, Dafny/Lean 4/QuickChick, W3C PROV/RO-Crate, RouteLLM/EvalPlus, and Clean. These sharpen the positioning of Luthier's architecture without invalidating its existing kernel certificates.

All tool versions, package compatibility facts, and benchmark URLs below were verified on 2026-10-26 on Linux (`x86_64`, Debian testing, kernel `7.2.9+deb14-amd64`), where both Python `3.12` (`/home/lmoffatt/miniconda3/bin/python3.12`) and Python `3.13.2` are present.

---

## 1. Floating-Point Bounds and Bound Transformers vs. Herbie, Daisy, Rosa, and Higham's Bounds on FPBench

*Antecedents:* `related-work.md` sections 2 and 4 (Panchekha et al. 2015; Darulova and Kuncak 2014; Darulova et al. 2018; Higham 2002).
*Luthier counterparts:* `Within` numerical laws (`laws.lth` section 5), Higham's $\gamma_n = nu/(1 - nu)$ bounds in `numbers.lth` and `arrays.lth` (`AssociativeWithin`, `DotStable`, `DotSensitive`), and the affine bound transformer $t = (L, \eta, D, r)$ with composition $t_2 \circ t_1 = (L_2 L_1, L_2 \eta_1 + \eta_2, D_1 \cap f_1^{-1}(D_2), \min(r_1, (r_2 - \eta_1)/L_1))$ and backward pull-back $\delta = (\varepsilon - \eta)/L$ in `core/properties/functions.lth` (`concepts.md` sections 9.1 to 9.4, `D-2026-10-25-a`).

### Exact question the comparison answers
On standard floating-point benchmarks with bounded input domains $D$, does Luthier's composition of first-order affine bound transformers $(L, \eta, D, r)$ and $\gamma_n$ laws (a) soundly upper-bound the worst-case empirical rounding error measured against an arbitrary-precision reference, (b) match or loosen the static worst-case bounds proved by Rosa and Daisy, and (c) yield non-empty backward pull-back radii $r_{\text{pullback}} = (\varepsilon - \eta)/L > 0$ on expressions where Herbie detects cancellation?

### Inputs
1. **Public benchmark (FPBench):** The FPBench benchmark suite at [https://github.com/FPBench/FPBench/tree/main/benchmarks](https://github.com/FPBench/FPBench/tree/main/benchmarks) (verified commit `d7ade34`, 2026-09-14, containing 136 `FPCore` benchmarks across 12 `.fpcore` files). Specifically:
   - `daisy.fpcore` (7 benchmarks) and `rosa.fpcore` (37 benchmarks), which carry explicit `:pre` interval preconditions defining the bounded domain $D$ for every input variable (for example, `rigidBody1`, `rigidBody2`, `doppler1`, `turbine1`, `verhulst`, `predatorPrey`, `bspline3`).
   - `hamming-ch3.fpcore` (28 benchmarks from Hamming's numerical analysis text) and `herbie.fpcore` (3 benchmarks) for cancellation-heavy expressions where Herbie synthesizes regime splits.
2. **Luthier library inputs:** Luthier's own numerical laws in `numbers.lth` (`AssociativeWithin`), `arrays.lth` (`DotStable`, `DotSensitive` at lengths $n \in \{1, 4, 16, 64, 256\}$), and `docs/concepts/tape.lth` (`MetresWithin` on `Mark` in $[0, 50000]$).

### Metric
For each benchmark expression $f$ on domain $D$:
1. **Soundness indicator (binary):** Whether the empirical maximum absolute error $\max_{x \in S} |\hat{f}(x) - f_{\text{exact}}(x)|$ over $N = 10^5$ points sampled from $D$ (plus boundary points and Herbie's adversarial points) is $\le$ the bound predicted by Luthier's composed `BoundTransformer` $\eta_{\text{Luthier}}(D)$ (meaning Luthier's `measured.worst` ratio $\le 1.0$).
2. **Tightness ratio against reference ($R_{\text{emp}}$):** $\max_{x \in S} |\hat{f}(x) - f_{\text{exact}}(x)| / \eta_{\text{Luthier}}(D)$ (closer to $1.0$ without exceeding $1.0$ is tighter; Luthier's `measured.worst` in `x.cert.json`).
3. **Static bound ratio against Daisy ($R_{\text{Daisy}}$):** $\eta_{\text{Luthier}}(D) / \eta_{\text{Daisy}}(D)$, where $\eta_{\text{Daisy}}(D)$ is Daisy's statically verified worst-case absolute error bound on $D$.
4. **Pull-back feasibility rate:** Given a target output tolerance $\varepsilon = 10^3 \cdot \eta_{\text{Daisy}}(D)$, the fraction of benchmarks for which Luthier's backward pull-back $(\varepsilon - \eta_{\text{Luthier}})/L_{\text{Luthier}}$ yields a positive allowable input radius $\delta > 0$.

### What result counts as "the same", "Luthier weaker", or "Luthier stronger"
- **The same:** Luthier's composed `BoundTransformer` is sound (`measured.worst <= 1.0`) on 100% of the translated `daisy.fpcore` and `rosa.fpcore` benchmarks, and its static bound $\eta_{\text{Luthier}}(D)$ is within a factor of $1.0$ to $5.0$ of Daisy's interval/affine bound $\eta_{\text{Daisy}}(D)$ (`0.2 <= R_Daisy <= 5.0`).
- **Luthier weaker:**
  1. *Unsoundness:* On any nonlinear benchmark with input error $\delta > 0$ (up to declared radius $r$), the actual error exceeds $L\delta + \eta$ because Luthier's `Affine` transformer drops second-order Taylor remainder terms $O(\delta^2)$ that Daisy and Rosa bound rigorously; or
  2. *Over-pessimism:* On DAG expressions where a variable is used along two paths (the dependency problem, such as $x - x$ or `bspline3`), `transformSum` ($\sum_i L_i \delta_i + \eta$) overestimates error by more than $10\times$ relative to Daisy's affine arithmetic (`R_Daisy > 10`), causing pull-back to report infeasibility where Daisy succeeds.
- **Luthier stronger:**
  1. On modular or external routines (such as `DotStable`/`DotSensitive` over arbitrary vector lengths $n$ or foreign Python/C `extern` kernels that Daisy and Herbie cannot parse), Luthier certifies parameterized $\gamma_n$ bounds and checks their tightness with negative controls (`noRoom`, `doublesThird`); and
  2. Combining Herbie's regime-split formulas on subdomains $D_1 \cup D_2$ as two domain-indexed Luthier specimens (`L10.2`) yields a tighter certified bound than Daisy's single-formula analysis while preserving a static `BoundTransformer` that Herbie alone lacks.

### Tools to install and Linux / Python 3.12 compatibility
- **Python reference packages:** `mpmath` `1.3.0` (already installed in `/home/lmoffatt/miniconda3/bin/python3.12`; `1.4.1` available on PyPI) and `python-flint` `0.9.0` (verified `manylinux2014_x86_64` `cp310-abi3` wheel on PyPI, runs natively on Linux with Python 3.12) for exact/ball ground-truth evaluation.
- **Herbie:** `herbie` version `2.3` (verified GitHub release `v2.3` at [https://github.com/herbie-fp/herbie/releases/tag/v2.3](https://github.com/herbie-fp/herbie/releases/tag/v2.3)). Installed on Linux via Racket (`apt install racket`, Debian candidate `8.18+dfsg1-1+b1`, followed by `raco pkg install --auto herbie`). Runs as a standalone CLI (`herbie report` / `herbie improve`) invoked from Python 3.12 via `subprocess`.
- **Daisy (which supersedes Rosa):** `daisy` commit `6a6f47a` (2026-09-03, tag `v0.1`, at [https://github.com/malyzajko/daisy](https://github.com/malyzajko/daisy); original Rosa is archived at [https://github.com/malyzajko/rosa](https://github.com/malyzajko/rosa), commit `68e58b8`). Runs on Linux using the already-installed OpenJDK (`default-jdk` `2:1.25-77`, `/usr/bin/java`), `sbt`, and `z3` (`apt install z3`, Debian candidate `4.13.3-1.1`, or `z3-solver` `5.3.2.0` on PyPI). Invoked from Python 3.12 via `subprocess`.

### Effort for one agent
**6 hours** (2 hours to translate 15 representative `daisy.fpcore`, `rosa.fpcore`, and `hamming-ch3.fpcore` benchmarks into `.lth`/`.lut` `BoundTransformer` chains and Python evaluation scripts; 2 hours to install and run Daisy and Herbie on the same `.fpcore` files; 2 hours to compute $R_{\text{emp}}$, $R_{\text{Daisy}}$, and pull-back feasibility tables).

---

## 2. Sampled Evidence $(\hat\varepsilon, \delta)$ and Pooling vs. the Rule of Three, Clopper-Pearson, Wald's SPRT, and Confidence Sequences

*Antecedents:* `related-work.md` section 12 (Hanley and Lippman-Hand 1983; Wald 1945, 1947; Younes and Simmons 2006; Howard, Ramdas, McAuliffe, and Sekhon 2021; Waudby-Smith and Ramdas 2024).
*Luthier counterparts:* The rule-of-three upper bound $\hat\varepsilon(n, \delta) \approx \min(1, 3/n)$ at $\delta = 0.05$ (`spec 7.S11`), the evidence base $(\hat\varepsilon, \delta)$ under the capped sum $\min(1, a + b)$ (`D-2026-10-25-a` question 1, `L10.3`, `AtLeastTheUnionBound`), pooling of sample stretches across seeds (`spec 7.S13`, `D-2026-10-16-g`), and Wald's SPRT for statistical laws (`L9.15`, `D-2026-10-15-b`, `concepts.md` sections 6.4 and 10).

### Exact question the comparison answers
1. For a single fixed sample of size $n$ with zero failures ($k = 0$), where does Luthier's rule-of-three approximation $\hat\varepsilon(n, \delta) = \min(1, -\ln(\delta)/n)$ (or $3/n$ at $\delta = 0.05$) underestimate or overestimate the exact one-sided Clopper-Pearson binomial upper bound $1 - \delta^{1/n}$?
2. When a user pools sample runs sequentially across seeds (`spec 7.S13`, say adding batches of $200$ cases until $\hat\varepsilon \le \varepsilon_{\text{demand}}$), how much does optional continuation inflate the actual type-I error rate above $\delta$ under fixed-$n$ bounds, and how much wider is a time-uniform confidence sequence (Howard et al. 2021; Ville's supermartingale bound) that remains valid under arbitrary pooling?
3. For statistical laws with ternary verdicts (`L9.15`), does Luthier's SPRT match Wald's theoretical stopping sample size and error rates $(\alpha, \beta)$?

### Inputs
No external dataset is needed; the inputs are parametric grids and Monte Carlo simulation runs generated by a deterministic Python script (fixed seed `20261021`):
1. **Deterministic zero-failure grid:** Sample sizes $n \in \{5, 10, 20, 50, 100, 200, 500, 1000, 10000\}$ and risk levels $\delta \in \{0.10, 0.05, 0.01, 0.001\}$.
2. **Sequential pooling simulation (`spec 7.S13`):** $10^5$ simulated Bernoulli streams with true defect rates $p \in \{0.001, 0.005, 0.01, 0.015, 0.05\}$, evaluated sequentially after every batch of $b \in \{1, 50, 200\}$ samples up to $N_{\max} = 10000$, where the user stops and certifies as soon as $\hat\varepsilon(n, \delta) \le p_{\text{target}}$ with zero failures.
3. **Composition grid (`AtLeastTheUnionBound`):** Chains of $m \in \{2, 4, 5, 10, 20\}$ conjuncts (including the 4 conjuncts of `Tape` and 5 conjuncts of `MarkIsAMetric` at $n = 200, \delta = 0.05$ from `concepts.md` section 6.3) under independent vs. maximally correlated failure events.
4. **SPRT simulation (`L9.15`):** $10^4$ Bernoulli streams at null $p_0 = 0.01$, alternative $p_1 = 0.05$, and target rates $\alpha = 0.05, \beta = 0.05$ with budgets $N_{\max} \in \{100, 500, 2000\}$.

### Metric
1. **Bound discrepancy ($\Delta \hat\varepsilon$):** $\hat\varepsilon_{\text{Luthier}}(n, \delta) - \hat\varepsilon_{\text{Clopper-Pearson}}(n, \delta)$, where $\hat\varepsilon_{\text{Clopper-Pearson}}(n, \delta) = 1 - \delta^{1/n}$ (`scipy.stats.beta.ppf(1 - delta, 1, n)`).
2. **Empirical false-certification rate under sequential pooling ($\hat\alpha_{\text{pool}}$):** The fraction of the $10^5$ sequential streams in which the upper bound $\hat\varepsilon(n, \delta)$ drops below the true failure probability $p$ at any pooled checkpoint $n \le N_{\max}$, compared against nominal $\delta$.
3. **Sample-size overhead of anytime-valid pooling ($n_{\text{CS}} / n_{\text{fixed}}$):** The ratio of samples required by a stitched/betting confidence sequence (or mixture martingale for $k=0$) to reach $\hat\varepsilon \le 0.015$ at $\delta = 0.05$ vs. fixed-sample Clopper-Pearson ($n = 200$).
4. **SPRT empirical $(\hat\alpha, \hat\beta)$ and unresolved fraction:** Compared against Wald's thresholds $A = (1 - \beta)/\alpha$ and $B = \beta/(1 - \alpha)$.

### What result counts as "the same", "Luthier weaker", or "Luthier stronger"
- **The same:**
  - For fixed $n \ge 50$ at $\delta = 0.05$, $\min(1, 3/n)$ agrees with exact Clopper-Pearson $1 - 0.05^{1/n}$ to within $1\%$ relative error ($3/200 = 0.01500$ vs. $1 - 0.05^{1/200} = 0.01487$, where $3/n$ is slightly conservative because $-\ln(0.05) = 2.9957 < 3$).
  - For conjunctions of $m$ laws without independence assumptions, Luthier's capped sum $\min(1, \sum \hat\varepsilon_i)$ matches the exact Frechet-Boole worst-case union bound.
- **Luthier weaker:**
  - *Hard-coded $3/n$ vs. general $\delta$:* If a rule uses $3/n$ at $\delta \ne 0.05$, it is wrong; even $-\ln(\delta)/n$ exceeds $1 - \delta^{1/n}$ by $\approx (\ln \delta)^2 / (2n)$, which is noticeable at $n < 30$ and small $\delta$. Worse, $1 - \delta^{1/n}$ is closed-form and just as cheap to compute at serve time (bite B1) as $3/n$.
  - *Sequential pooling inflation (`spec 7.S13`):* Under sequential peeking/pooling across seeds until a demand cutoff is met, fixed-sample Clopper-Pearson / rule-of-three violates nominal risk $\delta$: empirical false-certification $\hat\alpha_{\text{pool}}$ rises from $0.05$ to $0.15$-$0.35$ across $10$ to $50$ pooled checkpoints, whereas Howard et al.'s confidence sequences keep $\hat\alpha_{\text{pool}} \le \delta$ everywhere.
- **Luthier stronger:**
  - Unlike Statistical Model Checking tools that discard sample counts after returning a binary pass/fail for a fixed threshold, Luthier stores raw regional counts $n$ in `x.cert.json` and computes $\hat\varepsilon(n, \delta)$ at serve time for the demand's $\delta$ (`concepts.md` section 6.4, bite B1), and explicitly separates the assumption-free union bound (`cappedSumComposition`) from the independence-premised product (`IndependentComposition` under `FailuresIndependent`, `concepts.md` section 10).

### Tools to install and Linux / Python 3.12 compatibility
- **`scipy` and `numpy`:** `scipy` `1.17.1` and `numpy` `1.26.4` are already installed in `/home/lmoffatt/miniconda3/bin/python3.12` (`scipy` `1.18.1` wheel `cp312-manylinux_2_27_x86_64` verified on PyPI). Provides exact Clopper-Pearson via `scipy.stats.binomtest(0, n, p).proportion_ci(confidence_level=1-delta, method='exact')` and `scipy.stats.beta.ppf(1 - delta, 1, n)`.
- **`confseq`:** Version `0.0.11` on PyPI ([https://pypi.org/project/confseq/](https://pypi.org/project/confseq/), source at [https://github.com/gostevehoward/confseq](https://github.com/gostevehoward/confseq)). Verified: PyPI binary wheels stop at `cp310`, so on Python 3.12 on Linux `pip install --no-binary :all: confseq` compiles the C++ headers (`uniform_boundaries.h`) via `pybind11` and `g++`, while its betting confidence sequences (`src/confseq/betting.py` and `conjmix_bounded.py`) are pure Python using `numpy` and `scipy`.

### Effort for one agent
**3 hours** (1 hour to write the exact Clopper-Pearson, rule-of-three, stitched/betting confidence sequence, and SPRT Python comparison script; 1 hour to run the $10^5$-stream sequential pooling simulation; 1 hour to tabulate results and write the exact closed-form recommendation for bite B1 and `spec 7.S13`).

---

## 3. Per-Conjunct Negative Controls vs. FitSpec and Syntactic Mutation Testing

*Antecedents:* `related-work.md` section 6 (Braquehais and Runciman 2016, FitSpec; DeMillo, Lipton, and Sayward 1978; Jia and Harman 2011).
*Luthier counterparts:* Negative controls per conjunct (`L9.14`, `D-2026-10-15-a`, `D-2026-10-25-a` question 4, `spec 7.S19`, `7.S22`), where each conjunct of a theory must refute at least one wrong model (`hooked`, `lopsided`, `noRoom`, `flatMetric`, `oneWayMetric`, `squaredMetric`, `negativeMetric` in `docs/concepts/tape.test.lut`, `concepts.md` section 7).

### Exact question the comparison answers
When a Luthier theory is reported as fully "controlled" by `luthier check -v` (meaning every conjunct has at least one hand-written wrong model that it refutes), what fraction of systematically generated non-equivalent mutants (produced by FitSpec's type-directed mutant enumerator or by AST mutation testing) still survive all conjuncts of the theory, and conversely, do Luthier's domain-specific controls catch semantic and boundary bugs (such as `noRoom` and `doublesThird`) that syntactic mutation operators never generate?

### Inputs
1. **Public benchmark (FitSpec benchmark suite):** The 19 Haskell benchmark programs and property sets in the FitSpec repository at [https://github.com/rudymatela/fitspec/tree/master/bench](https://github.com/rudymatela/fitspec/tree/master/bench) and [https://github.com/rudymatela/fitspec/tree/master/eg](https://github.com/rudymatela/fitspec/tree/master/eg) (verified commit `250d610`, version `0.4.10`, including `bools.hs`, `list.hs`, `sets.hs`, `sorting.hs`, `heaps.hs`, `avltrees.hs`, `digraphs.hs`, `negation.hs`).
2. **Luthier theories and models:**
   - `docs/concepts/tape.lth`, `tape.lut`, and `tape.test.lut` (the 4 conjuncts of `Tape` and 5 conjuncts of `MarkIsAMetric`, with their 8 controls from `concepts.md` sections 6.3 and 7).
   - Core algebraic structures in `lib/core/` (`Equivalence`, `Monoid`, `Metric` in `equality.lth` and `operations.lth`) and numerical theories in `numbers.lth` (`AssociativeWithin`, `Doubles`) and `arrays.lth` (`DotStable`, `DotSensitive`).

### Metric
1. **Surviving non-equivalent mutant rate (Completeness gap):** Among all non-equivalent mutants $M_{\text{syn}}$ generated by FitSpec / AST mutation for the operations of a theory $T$, the percentage that pass every conjunct of $T$ under Luthier's test profile despite $T$ having one refuted hand-written control per conjunct.
2. **Conjunct minimality / independence matrix:** A $|C| \times |M|$ boolean matrix recording which conjunct $c \in C$ kills which mutant or control $m \in M$. A conjunct $c$ is *uniquely necessary* against $M$ if at least one mutant in $M$ is killed *only* by $c$.
3. **Semantic control coverage:** The fraction of Luthier's hand-written controls (`hooked`, `lopsided`, `noRoom`, `doublesThird`, `squaredMetric`, `negativeMetric`) that appear in the syntactic mutant space of FitSpec / `mutmut`.

### What result counts as "the same", "Luthier weaker", or "Luthier stronger"
- **The same:** On characterizing theories such as `Tape` (`concepts.md` section 2.3) and `Metric`, 0% of non-equivalent FitSpec mutants survive all conjuncts under Luthier's 200-case sampled profile with boundary regions (`sameOrNat`), and each conjunct uniquely kills at least one mutant just as FitSpec's minimal property set check requires.
- **Luthier weaker:**
  1. *Incomplete theories still pass `check -v`:* On partial theories (consistent with `L9.4`: "a law need not determine the operation", or if a conjunct such as `ReadingSteps` is omitted from `Tape` while the remaining three conjuncts each keep their own control), `luthier check -v` reports 0 uncontrolled conjuncts, whereas FitSpec immediately flags the property set as incomplete by exhibiting surviving mutants (for example, $r(a, b) = 2|a - b|$ survives `ReadingSymmetric` and `ReadingAdds`).
  2. *Order-dependent control stopping (`spec 7.S22`):* Before bite D1 (`concepts.md` section 7.1), stopping a control at the first refuted conjunct allowed a single broken model to leave later conjuncts untested. Even with bite D1 (requiring one control per conjunct), a control $m_i$ refuted by conjunct $c_i$ might also be refuted by $c_j$, so having one refuted control per conjunct does not prove that the conjuncts are logically irredundant unless each conjunct has a control that *passes* all other conjuncts (as `lopsided` does for `ReadingSymmetric`).
- **Luthier stronger:**
  1. FitSpec and `mutmut` only mutate code syntax and cannot mutate *theoretical error bounds* or floating-point machine constants; Luthier's controls (`noRoom` setting `epsilon := 0.0`, and `doublesThird` tightening $3\gamma_n$ to $\gamma_n$) test the tightness of quantitative bounds (`concepts.md` section 7).
  2. Luthier persists control refutations in `x.cert.json` keyed by the law's cone hash (`concepts.md` section 8.4), whereas FitSpec and `mutmut` are ephemeral CLI checks.

### Tools to install and Linux / Python 3.12 compatibility
- **FitSpec:** `fitspec` `0.4.10` on Hackage ([https://hackage.haskell.org/package/fitspec](https://hackage.haskell.org/package/fitspec), GitHub [https://github.com/rudymatela/fitspec](https://github.com/rudymatela/fitspec)). Installed on Linux via `apt install ghc cabal-install` (Debian candidates `ghc` `9.10.3-4` and `cabal-install` `3.12.1.0-1+b1`) and `cabal install fitspec`. Standalone binary/library invoked from Python 3.12 via `subprocess`.
- **Python mutation testers:** `mutmut` `3.8.0` (`py3-none-any.whl`, `requires_python >= 3.10`) and `cosmic-ray` `8.7.0` (`requires_python >= 3.9`), both verified on PyPI and fully compatible with Linux and Python 3.12 (`pip install mutmut==3.8.0`).

### Effort for one agent
**5 hours** (2 hours to translate `Tape`, `Metric`, and `Monoid` into FitSpec Haskell files and a Python mutant generator matching FitSpec's enumerative mutation rules; 2 hours to run Luthier's controls and FitSpec's mutants across full and deliberately weakened conjunct sets; 1 hour to build the $|C| \times |M|$ kill matrix).

---

## 4. Proposed Dynamic `Ball` Arithmetic vs. Arb (`python-flint`), Interval Arithmetic, and Affine Arithmetic

*Antecedents:* `related-work.md` section 3 (Johansson 2017, Arb; Moore 1966; IEEE Std 1788-2015; Stolfi and de Figueiredo 2003, 2004).
*Luthier counterparts:* Dynamic midpoint-radius `Ball` decorations as another model of `NumberModel` (`L5.4`, `concepts.md` sections 9.3, 10, and 15 `O5`) and the proposed bridge law `RadiusWithinTransformer` (`related-work.md` section 3), which propagates a ball $(m, \rho)$ through an operation with bound transformer $(L, \eta, D, r)$ by evaluating $L$ and $\eta$ at the midpoint $m$: $\rho_{\text{out}} = L(m)\rho + \eta(m)$.

### Exact question the comparison answers
When propagating midpoint-radius balls $[m \pm \rho]$ through numerical expressions and linear algebra routines (`dot`), is Luthier's proposed `RadiusWithinTransformer` rule $\rho_{\text{out}} = L(m)\rho + \eta(m)$ rigorously sound for finite non-zero radii $\rho > 0$ compared to Arb (`python-flint` `arb`), how much wider or narrower are its enclosures than Arb's and affine arithmetic's, and what happens when a ball straddles a domain boundary ($m \pm \rho \not\subseteq D$) or an `if <=` branch test?

### Inputs
1. **Public benchmark (FPBench):** The 37 benchmarks in `rosa.fpcore` and 3 benchmarks in `rump.fpcore` from [https://github.com/FPBench/FPBench/tree/main/benchmarks](https://github.com/FPBench/FPBench/tree/main/benchmarks), evaluated on balls $[m \pm \rho]$ where $m$ is drawn from the benchmark's domain $D$ and input radii span $\rho \in \{0, 10^{-15}, 10^{-10}, 10^{-6}, 10^{-3}, 10^{-1}\}$.
2. **Constructed stress cases:**
   - **Curvature stress test:** Nonlinear functions where $|f'(x)|$ increases sharply across $[m - \rho, m + \rho]$, specifically $f(x) = x^2$, $f(x) = \exp(x)$, and $f(x) = 1/x$ near $m = 0.1$ with $\rho = 0.05$.
   - **Correlated DAG test:** $g(x) = (x + 1) - x$ and $h(x) = x / (x + 1)$ to test first-order error cancellation (affine arithmetic vs. ball arithmetic).
   - **Branch-straddling test:** `tape.lut`'s `if a <= b then b - a else a - b` when $a = [1000 \pm 2]$ and $b = [1001 \pm 2]$ (straddling $a = b$).
   - **Dot product (`DotStable` / `DotSensitive`):** Random and ill-conditioned vectors of length $n \in \{4, 16, 64, 256\}$.

### Metric
1. **Enclosure soundness rate:** Fraction of test balls $[m \pm \rho]$ for which the true image $f([m - \rho, m + \rho])$ (computed at 256-bit precision in Arb) is strictly contained in the output ball $[m_{\text{out}} \pm \rho_{\text{out}}]$.
2. **Radius inflation ratio ($\rho_{\text{Luthier}} / \rho_{\text{Arb}}$):** Ratio of Luthier's propagated radius to `python-flint`'s 53-bit `arb` radius at $\rho = 0$ (pure rounding defect) and $\rho > 0$ (input uncertainty propagation).
3. **Runtime overhead:** Wall-clock time per evaluation of `Ball` in Python vs. `python-flint`'s C-level `arb` and plain `Float64`.

### What result counts as "the same", "Luthier weaker", or "Luthier stronger"
- **The same:** On affine operations (`+`, `-`, scalar multiplication, `tape.reading` away from the $a = b$ branch, and `dot` when $L$ bounds $\lVert y \rVert + \rho_y$), Luthier's `Ball` encloses 100% of true outputs and produces radii within a factor of $1$ to $3$ of 53-bit `arb`.
- **Luthier weaker:**
  1. *Midpoint sensitivity unsoundness on convex/nonlinear functions:* If `RadiusWithinTransformer` evaluates $L(m) = |f'(m)|$ at the *midpoint* $m$ instead of taking $\sup_{x \in [m-\rho, m+\rho]} |f'(x)|$, it is **unsound** for any strictly convex function: for $f(x) = x^2$ at $m = 1, \rho = 0.1$, $|f'(m)|\rho = 2(1)(0.1) = 0.2$, whereas $(1 + 0.1)^2 - 1^2 = 0.21 > 0.2$. Arb avoids this by bounding derivatives over the entire ball $[m \pm \rho]$ or adding higher-order Taylor bounds.
  2. *Dependency problem:* Like Arb and standard intervals, Luthier's `Ball` has no noise symbols, so on $(x + 1) - x$ with $x = [1 \pm \rho]$ it gives radius $2\rho + \eta$, whereas affine arithmetic gives $\eta$.
- **Luthier stronger:**
  - Arb is a dynamic library that only knows the radius *after* running on a concrete input $m$; Luthier's `BoundTransformer` uses the exact same $(L, \eta, D, r)$ data statically ahead of execution to pull a demand's tolerance $\varepsilon$ back to an input requirement $\delta = (\varepsilon - \eta)/L$, and checks domain/radius validity ($m \in D$ and $\rho \le r$) as an explicit certificate obligation rather than silently returning `[+/- inf]`.

### Tools to install and Linux / Python 3.12 compatibility
- **`python-flint` (Arb bindings):** Version `0.9.0` on PyPI ([https://pypi.org/project/python-flint/](https://pypi.org/project/python-flint/), source at [https://github.com/flintlib/python-flint](https://github.com/flintlib/python-flint), wrapping FLINT 3 / Arb). Verified: provides `manylinux2014_x86_64` wheel (`cp310-abi3`) that installs cleanly via `pip install python-flint==0.9.0` and runs on Linux with Python 3.12 (`flint.arb` with configurable bit precision `flint.ctx.prec = 53` and `256`).
- **`mpmath`:** Version `1.3.0` (already installed in Python 3.12; provides `mpmath.iv` interval arithmetic).

### Effort for one agent
**4 hours** (1.5 hours to implement a prototype Luthier `Ball` model in Python/Luthier using both midpoint $L(m)$ and interval-supremum $L([m \pm \rho])$ transformers; 1.5 hours to run `python-flint` `arb` and `mpmath.iv` across the FPBench and curvature stress inputs; 1 hour to document the soundness fix for `RadiusWithinTransformer`).

---

## 5. Law Normal Form vs. AC-Normalization in Term Rewriting and `egg`'s E-Graphs

*Antecedents:* `related-work.md` section 10 (Baader and Nipkow 1998; Dershowitz and Jouannaud 1990; Miller 1991; Willsey et al. 2021, `egg`).
*Luthier counterparts:* Canonical cone form `canon` (`concepts.md` section 8.2, `L3.4`, `spec 3.S34`), single-definition algebraic properties (`L7.6`, `D-2026-10-17-b`, `concepts.md` section 3.4), and the proposed law normal form (`related-work.md` section 10, citing `idea-law-normal-form-2026-10-27.md`) that applies $\beta\delta\alpha$-reduction, binder permutation, and AC-normalization restricted to operators *certified* to be `Commutative` or `Associative`.

### Exact question the comparison answers
Across all laws written in Luthier's library and examples (such as `ReadingSymmetric` in `tape.lth` vs. `Commutative` in `operations.lth`), does decidable $\beta\delta\alpha$-normalization plus Miller higher-order pattern matching and *certified-only* AC-normalization identify the exact same equivalences as (a) unrestricted AC term rewriting (`sympy`) and (b) equality saturation in an e-graph (`egg` / `egglog`), without unsoundly equating floating-point expressions whose operators only satisfy `AssociativeWithin`?

### Inputs
There is no external dataset of Luthier laws; build a corpus of **60 law pairs** from three sources:
1. **All laws in `lib/core/` and `docs/concepts/`:** Every Boolean and `Within` law in `equality.lth`, `operations.lth`, `functions.lth`, `numbers.lth`, `arrays.lth`, and `tape.lth` (for example, `ReadingSymmetric (t : Tape) (a b : Mark) := t.reading a b == t.reading b a` paired with `Commutative Mark Float64 (structural Float64) t.reading`).
2. **Syntactic variations that must normalize to the same form (Positive pairs, 30 pairs):**
   - Alpha-renamed quantifiers (`forall x y` vs. `forall a b`) and swapped quantifier order (`(a b : Mark)` vs. `(b a : Mark)`).
   - Flipped symmetric relations (`x == y` vs. `y == x`; `a <= b and b <= c` vs. `b <= c and a <= b`).
   - Unfolded aliases and helper definitions ($\beta\delta$-equivalence).
   - Rearranged integer additions (`(a + b) + c == a + (b + c)` over `Int`, where `+` is certified `Associative` and `Commutative`).
3. **Metric / floating-point variations that must NOT be equated as exact laws (Negative pairs, 15 pairs):**
   - Reassociated `Float64` sums (`(x + y) + z` vs. `x + (y + z)` where `+` is `Doubles.plus`, certified `Commutative` but NOT `Associative`, only `AssociativeWithin` $3\gamma_2$).
   - Distributed `Float64` products (`x * (y + z)` vs. `x * y + x * z`).
   - `(a + b) * 1.0` vs. `a + b` when NaN/signed-zero or non-exact operations are in scope (`concepts.md` section 12.4).

### Metric
1. **Recall on true semantic equivalences:** Percentage of the 30 positive law pairs recognized as equivalent by (a) Luthier's current `canon` (alpha + binder type erasure only), (b) Luthier's proposed law normal form ($\beta\delta\alpha$ + quantifier permutation + certified AC-normalization), (c) `sympy` canonicalization, and (d) `egglog` equality saturation.
2. **False-equivalence (unsoundness) rate on negative floating-point pairs:** Percentage of the 15 negative `Float64` pairs falsely merged into the same equivalence class.
3. **Normalization time per law:** Milliseconds per law pair.

### What result counts as "the same", "Luthier weaker", or "Luthier stronger"
- **The same:** On first-order Boolean and integer equational laws, Luthier's $\beta\delta\alpha$ + quantifier-permutation + certified AC-normalizer achieves the same 100% recall on the 30 positive pairs as `egglog` with AC rules, in $< 5$ ms per law.
- **Luthier weaker:**
  - Luthier's current `canon` (`spec 3.S34`, before law normal form) only renames bound variables in place and erases binder annotations: it fails on quantifier permutation (`fn a b { f a b == f b a }` vs. `fn b a { f a b == f b a }`), flipped `==` (`f a b == f b a` vs. `f b a == f a b`), and definition unfolding ($\delta$).
  - Even with AC-normalization, laws whose equivalence requires distributivity or congruence closure over conditional premises (`p -> f(x) == f(y)` where `p` implies `x == y`) are caught by `egglog` equality saturation and missed by tree-based AC-normalization.
- **Luthier stronger:**
  - Standard `sympy` simplification and unindexed `egglog` ring rules unsoundly merge `(x + y) + z` and `x + (y + z)` on `Float64` (false-equivalence rate $> 0\%$), whereas Luthier gates AC-flattening on whether the operator has a certificate for exact `Associative` vs. `AssociativeWithin` (`related-work.md` section 10).

### Tools to install and Linux / Python 3.12 compatibility
- **`egglog` (Python bindings to `egg` / `egglog`):** Version `14.0.0` on PyPI ([https://pypi.org/project/egglog/](https://pypi.org/project/egglog/), GitHub [https://github.com/egraphs-good/egglog-python](https://github.com/egraphs-good/egglog-python); underlying Rust `egg` crate is `v0.11.0` at [https://github.com/egraphs-good/egg](https://github.com/egraphs-good/egg)). Verified: provides prebuilt wheel `egglog-14.0.0-cp312-cp312-manylinux_2_17_x86_64.whl` that installs with `pip install egglog==14.0.0` and runs natively on Linux with Python 3.12.
- **`sympy`:** Version `1.14.0` (already installed in `/home/lmoffatt/miniconda3/bin/python3.12`).

### Effort for one agent
**4 hours** (1.5 hours to build the 60-pair law corpus from `lib/core/` and `tape.lth`; 1.5 hours to implement the certified AC-normalizer prototype and `egglog` rule set in Python 3.12; 1 hour to measure recall, false positives on `Float64`, and runtime).

---

## 6. Premise Vacuity Detection (`Vacuous n`) vs. Vacuity Detection After Beer et al.

*Antecedents:* `related-work.md` section 6 (Beer, Ben-David, Eisner, and Rodeh 2001, "Efficient Detection of Vacuity in Temporal Model Checking"; QuickCheck/Hypothesis precondition rejection).
*Luthier counterparts:* Premise counting (`held`) and vacuity rejection `Vacuous n` (`spec 7.S12`, `D-2026-10-16-m`, `laws.lth`, built in wave A bites A3 and A3b, `concepts.md` section 6.6), which recognizes top-level premises of the form `p -> q`, `if p then q else true`, and disjunctions with exactly one negated disjunct (`o.eq x y or not (m.d x y == 0.0)` in `MetricIndiscernible`).

### Exact question the comparison answers
Does Luthier's syntactic premise recognizer (`p -> q`, `if p then q else true`, and single-negated disjunctions `not p or q`) detect every law that passes vacuously on a test sample according to Beer et al.'s semantic subformula-witness definition of vacuity (where replacing a subformula $\psi$ of $\varphi$ with its strengthening $\bot$ or $\top$ leaves the law satisfied on all $n$ drawn cases)?

### Inputs
Build a test suite of **25 laws with preconditions or compound Boolean structure** drawn from and extending `lib/core/` and `docs/concepts/`:
1. **Laws from `lib/core/` and `docs/concepts/`:**
   - `MetricIndiscernible`: `o.eq x y or not (m.d x y == 0.0)` tested on `Mark` ($[0, 50000]$) under uniform sampling (where $x = y$ has probability $1/50001$) vs. `sameOrNat` (`concepts.md` section 6.6), and tested against the control `hookedMetric` (where `m.d x y >= 1.0` everywhere, so $d(x, y) = 0$ never holds, `concepts.md` section 7.1).
   - `MetricZeroOnEqual`, `ReadingAdds` (over subtype `InOrder`), `ReadingSteps` (over subtype `Step`), and `BoundTransformer`'s domain/radius laws (`ComposeSound`, `EmptyDomain`, `PullbackMeets`).
2. **Adversarial Boolean equivalents of implication (Beer et al. test cases):**
   - Double-negated disjunctions: `not (a < b) or not (b < c) or (f a c <= f a b + f b c)` (two negated disjuncts: equivalent to `(a < b and b < c) -> ...`, where bite A3b's rule "a disjunction with *exactly one* negated disjunct" does not fire).
   - Nested implications: `p1 x -> (p2 x -> q x)` where `p1 x` holds 50% of the time but `p1 x and p2 x` holds 0% of the time.
   - Conjunctions inside conclusions with dead branches: `(p x -> q1 x) and q2 x` where `q2 x` always holds and `p x` never holds (the whole law is not vacuously true, but subformula `q1 x` is never exercised: Beer et al.'s subformula vacuity).
   - De Morgan encodings: `not (p x and not (q x))` (literally the definition of `then` in `L12.7`, `concepts.md` section 6.6).

### Metric
For each of the 25 laws evaluated over $n = 200$ sampled cases:
1. **Beer et al. witness detection (Ground truth):** A law $\varphi$ is *Beer-vacuous in subformula $\psi$* on sample $S$ if $\varphi$ holds for all $x \in S$ and the witness formula $\varphi[\psi \leftarrow \mathrm{false}]$ (for positive-polarity $\psi$) or $\varphi[\psi \leftarrow \mathrm{true}]$ (for negative-polarity $\psi$) *also* holds for all $x \in S$.
2. **True positive rate (Recall) of Luthier's `Vacuous n`:** Fraction of Beer-vacuous laws on $S$ that Luthier marks as `Vacuous n` (`held == 0`).
3. **False positive rate of Luthier's `Vacuous n`:** Fraction of non-vacuous laws that Luthier falsely marks as `Vacuous n`.

### What result counts as "the same", "Luthier weaker", or "Luthier stronger"
- **The same:** On single-premise laws written as `p -> q`, `if p then q else true`, or `q or not p` (`MetricIndiscernible`), Luthier's `held == 0` check agrees 100% with Beer et al.'s witness formula $\varphi[q \leftarrow \mathrm{false}]$: `p -> false` is `not p`, which holds on all $n$ samples if and only if `p` held on $0$ samples.
- **Luthier weaker:**
  1. *Multi-negated disjunctions and De Morgan forms:* Because bite A3b only recognizes a disjunction with *exactly one* negated disjunct (`concepts.md` section 6.6), `not p1 or not p2 or q` (two negated premises) and `not (p and not q)` are not recognized as premises by Luthier's syntactic check, whereas Beer et al.'s witness replacement $\varphi[q \leftarrow \mathrm{false}]$ catches both immediately without any syntactic case-splitting.
  2. *Partial/subformula vacuity:* In `(p -> q1) and q2`, if `p` never holds and `q2` holds, the whole conjunction has `"held": 0` for `p` only if split first; if `p -> q1` is nested inside an expression, Beer et al.'s subformula replacement detects that `q1` was never tested.
- **Luthier stronger:**
  - In model checking (`Beer et al. 2001`), vacuity is binary: if a premise holds on *even 1 state* (say 1 out of 200 samples), the formula is non-vacuous. Luthier records the exact count `"held": k` in the certificate (`"held": 49` of 200 for `MetricIndiscernible`), so the statistical evidence bound $\hat\varepsilon(k, \delta)$ can be computed from $k$ (the number of non-vacuous trials where the premise held) rather than $n = 200$, preventing a law where `held = 1` out of `200` from claiming $\hat\varepsilon = 3/200 = 0.015$ when its effective sample size on the premise is $k = 1$ ($\hat\varepsilon = 1.0$).

### Tools to install and Linux / Python 3.12 compatibility
- **`z3-solver`:** Version `5.3.2.0` on PyPI ([https://pypi.org/project/z3-solver/](https://pypi.org/project/z3-solver/), verified `manylinux_2_27_x86_64` wheel, runs natively on Linux with Python 3.12) or `sympy.logic` (`sympy` `1.14.0`, already installed in Python 3.12) to compute subformula polarities and evaluate Beer et al.'s witness formulas $\varphi[\psi \leftarrow \bot / \top]$ over every subformula $\psi$ of each law.
- **`hypothesis`:** Version `6.170.11` on PyPI (`requires_python >= 3.11`, verified `cp311-abi3-manylinux` wheel compatible with Python 3.12) to compare Hypothesis's `assume(p)` filter-rejection health check (`FailedHealthCheck.filter_too_much`) against Luthier's `Vacuous n` and subtype generator `sameOrNat`.

### Effort for one agent
**3 hours** (1 hour to implement Beer et al.'s polarity-based witness generator $\varphi[\psi \leftarrow \bot/\top]$ over Luthier law ASTs in Python; 1 hour to run both Beer's witness check and Luthier's `Vacuous n` check on the 25-law suite; 1 hour to analyze the `held = k` effective-sample-size interaction with $\hat\varepsilon(k, \delta)$).

---

## 7. Dependency Cone Hashing vs. Unison's Canonical AST Hashing and Nix's Store Hashing

*Antecedents:* `related-work.md` section 9 (Chiusano and Bjarnason 2019, Unison; Dolstra et al. 2004, 2008, Nix; Mokhov, Mitchell, and Peyton Jones 2018, 2020, Build Systems a la Carte).
*Luthier counterparts:* Certificate identity $\mathrm{id}(\ell, n, g) = (\ell, H(\mathrm{canon}(\mathrm{cone}(n)) \,\|\, \mathrm{hosts} \,\|\, \mathrm{interpreter}), g)$ (`concepts.md` section 8.2, `L10.4`, `L3.4`, `spec 6.S8`, `3.S34`, `12.S11`), and result keys (`L5.6`, `concepts.md` section 12.4).

### Exact question the comparison answers
Across a battery of meaning-preserving refactorings and meaning-changing dependency edits (including changes in foreign `extern` host functions), when does Luthier's cone hash $H(\mathrm{canon}(\mathrm{cone}(n)) \,\|\, \mathrm{hosts} \,\|\, \mathrm{interpreter})$ preserve or invalidate certificates compared to Unison's hash-addressed ASTs and Nix's input-addressed store derivations?

### Inputs
Construct a benchmark of **20 repository edit scenarios** applied to an equivalent 4-module program (`tape` + helper module + foreign `extern` math/console module + test suite) implemented in Luthier, Unison, and Nix-packaged Python:
1. **Meaning-preserving edits (10 scenarios; ideal result = 0 certificates invalidated):**
   - E1: Formatting, whitespace, and comment edits in `tape.lth` and `tape.lut`.
   - E2: Alpha-renaming a bound parameter (`fn a b` to `fn x y`) in `tape.lut`.
   - E3: Adding or removing a redundant binder type annotation that the elaborator infers (`spec 3.S34`).
   - E4: Adding an unused helper function `unusedHelper` to `tape.lut` outside `cone(tape)`.
   - E5: Reordering top-level definitions inside `tape.lut`.
   - E6: Moving a helper function `metres` from `tape.lth` to another module and importing it (`module prefixes removed`, `concepts.md` section 8.2).
   - E7: **Top-level definition renaming:** Renaming an internal helper function `absDiff` called by `tape.reading` to `markDistance` (keeping its body identical).
   - E8: Renaming a record field of a theory (`reading` to `measure`, `L3.4`).
   - E9: Changing `seed` or `fuel` budget vs. changing special-value mass in `g` (`concepts.md` section 8.2, bite 13c).
   - E10: Editing a comment inside a Python `extern` file.
2. **Meaning-changing edits (10 scenarios; ideal result = affected certificates invalidated, unaffected preserved):**
   - E11-E15: Changing a constant (`1000.0` to `100.0`), operator (`<=` to `<`), subtype bound (`50000` to `40000`), law conjunct, or generator distribution in `cone(tape)`.
   - E16-E20: **External host edits:** Changing the body of a called Python `extern` function (E16); changing a Python helper function imported *by* the `extern` function in another `.py` file (E17); changing the NumPy/SciPy package version in the Python environment (E18); changing a shared C library called by the Python `extern` (E19); and a non-deterministic host `extern` returning a different value on exact replay (`D-2026-10-15-f`, E20).

### Metric
1. **False invalidation rate (over-invalidation):** Fraction of the 10 meaning-preserving edits (E1-E10) that change the cone hash and force re-certification.
2. **False cache-hit rate (under-invalidation / unsoundness):** Fraction of the 10 meaning-changing edits (E11-E20) that leave the cone hash unchanged and serve a stale certificate.

### What result counts as "the same", "Luthier weaker", or "Luthier stronger"
- **The same:** On E1-E6 (comments, bound-variable renaming, binder annotation erasure, dead definitions outside the cone, top-level reordering, module-prefix stripping) and E11-E16 (direct cone AST and direct `extern` changes), Luthier's cone hash behaves identically to Unison's term hash.
- **Luthier weaker:**
  1. *Against Unison on E7 (top-level helper renaming):* If Luthier's `canon(cone(n))` serializes top-level definitions in the cone with their symbolic names rather than replacing references to upstream definitions by their canonical hashes (Unison's #hash indexing), renaming a helper `absDiff` to `markDistance` changes `canon(cone(tape))` in Luthier (false invalidation on E7) while changing 0 hashes in Unison.
  2. *Against Nix on E17-E19 (transitive host dependencies):* Unless Luthier's `hosts` hash includes the transitive Python import closure and environment lockfile/shared-library digests, editing a transitive Python helper (E17) or upgrading NumPy/BLAS (E18-E19) is caught by Nix's `/nix/store` derivation hash but missed by hashing only the immediate `extern` function or file in Luthier (false cache hit).
- **Luthier stronger:**
  - Unison has no concept of hashing foreign host code (`hosts`), statistical generator profiles ($g$), sample pooling across seeds (`spec 7.S13`), or certificate transport along a certified renaming (`L3.4` on E8); Nix hashes raw source files (so comments E1, bound variable renames E2, and dead functions E4 in the same file invalidate the Nix derivation, giving Nix a high false-invalidation rate on E1-E6 where Luthier's AST-level `canon(cone(n))` invalidates nothing).

### Tools to install and Linux / Python 3.12 compatibility
- **Unison (`ucm`):** Release `release/1.5.0` (verified GitHub release at [https://github.com/unisonweb/unison/releases/tag/release/1.5.0](https://github.com/unisonweb/unison/releases/tag/release/1.5.0), provides standalone prebuilt Linux `x86_64` tarball `ucm-linux-x64.tar.gz` requiring no root privileges). Invoked from Python 3.12 via `ucm transcript`.
- **Nix:** `nix-bin` `2.34.8+dfsg-1+b1` in Debian testing (`apt install nix-bin`) or upstream Nix `2.35.4` ([https://github.com/NixOS/nix](https://github.com/NixOS/nix)). `nix-instantiate` computes store derivation hashes without executing builds and is invoked from Python 3.12 via `subprocess`.

### Effort for one agent
**4 hours** (1.5 hours to script the 20 edit scenarios in Python against Luthier's cone hasher; 1.5 hours to run the same 20 edits through `ucm transcript` and `nix-instantiate`; 1 hour to build the 20-row comparison matrix and check whether top-level names in `canon(cone(n))` are hash-substituted).

---

## 8. Sensitivity Typing and Quantitative Equational Logic (Fuzz, Granule, Mardare-Panangaden-Plotkin) vs. Luthier's `BoundTransformer` and Cost Bases

*Antecedents:* `related-work.md` sections 11 and 14.2 (Reed and Pierce 2010, Fuzz; Orchard, Liepelt, and Eades 2019, Granule; Lawvere 1973; Mardare, Panangaden, and Plotkin 2016).
*Luthier counterparts:* Multi-input sensitivity combinators `transformSum` ($\sum_i L_i \delta_i + \eta$, corresponding to Fuzz's tensor product $A \otimes B$) and `transformMax` ($\max_i L_i \delta_i + \eta$, corresponding to Fuzz's cartesian product $A \mathbin{\&} B$) in `core/properties/functions.lth`, plus `ErrorBase` and `EvidenceComposition` (`concepts.md` sections 3.2, 9.3, and 10).

### Exact question the comparison answers
On multi-argument numerical programs, what classes of functions can be typed in Granule/Fuzz vs. certified by Luthier's `BoundTransformer`, and how much tighter is backward pull-back tolerance allocation (`L6.2`, `L6.8`) when the planner distinguishes Fuzz's cartesian (`transformMax`) vs. tensor (`transformSum`) products?

### Inputs
Build a 12-function benchmark in Granule and Luthier:
1. **Purely Lipschitz exact functions (4 functions):** `plus`, `scale(c, x)`, `pair_add`, `max(x, y)` over exact rationals/reals ($\eta = 0$).
2. **Floating-point realizations with rounding defect $\eta > 0$ (4 functions):** `Float64` addition, `MetresWithin` (`tape.lth`), `DotSensitive` (`arrays.lth`), and polynomial evaluation on a bounded interval $D = [-10, 10]$ (locally Lipschitz on $D$, globally non-Lipschitz on $\mathbb{R}$).
3. **Multi-input pull-back trees (4 DAGs):** Binary trees of depth $d \in \{1, 2, 3, 4\}$ combining `transformSum` and `transformMax` under a root output demand $\varepsilon$.

### Metric
1. **Expressibility (binary per benchmark):** Whether the system can express and check the error/sensitivity bound of the function.
2. **Pull-back input budget ($\delta_{\text{in}}$):** The allowable input error $\delta_i$ assigned to each leaf of a depth-$d$ tree of `transformSum` vs. `transformMax` for a fixed output demand $\varepsilon$.

### What result counts as "the same", "Luthier weaker", or "Luthier stronger"
- **The same:** When $\eta = 0$ and $D = \mathbb{R}, r = \infty$, Luthier's `composeAffine`, `transformSum`, and `transformMax` reduce identically to Fuzz/Granule's semiring scaling $L_2 L_1$, additive tensor $A \otimes B$, and cartesian product $A \mathbin{\&} B$, and obey Mardare et al.'s quantitative triangle rule ($s =_{\varepsilon_1} t, t =_{\varepsilon_2} u \implies s =_{\varepsilon_1 + \varepsilon_2} u$).
- **Luthier weaker:** Granule checks sensitivity grades statically inside its linear type checker on every variable use, automatically catching when a program variable $x$ is duplicated across two arguments ($f(x, x)$ requires scaling sensitivity by $L_1 + L_2$), whereas in Luthier `transformSum` and `transformMax` are library combinators in `functions.lth` that are not yet automatically synthesized from term variable usage by `luthier check`.
- **Luthier stronger:** Fuzz, Granule, and Mardare et al.'s quantitative algebras require $\eta = 0$ ($x = y \implies f(x) = f(y)$) and global Lipschitz constants over the entire carrier type, so they cannot type any rounded floating-point operation ($\eta > 0$) or any nonlinear function like $x \cdot y$ (`DotSensitive`, which is Lipschitz only on a bounded domain $D$ and radius $r$).

### Tools to install and Linux / Python 3.12 compatibility
- **Granule:** Release `v0.9.6.0` (verified GitHub release at [https://github.com/granule-project/granule/releases/tag/v0.9.6.0](https://github.com/granule-project/granule/releases/tag/v0.9.6.0), provides prebuilt Linux binary or builds with `cabal`). Invoked from Python 3.12 via `subprocess`.

### Effort for one agent
**3 hours** (1 hour to run the 12 functions through Granule `v0.9.6.0` and Luthier's `functions.lth`; 1 hour to compute backward pull-back budgets on the depth-$d$ trees; 1 hour to write up the variable-sharing check that Luthier's planner needs).

---

## 9. Algorithmic Choice and Accuracy-Reliability Allocation (PetaBricks and Chisel) vs. Luthier's Planner and Budget Laws

*Antecedents:* `related-work.md` sections 1 and 14.4 (Ansel et al. 2009, 2011, PetaBricks; Misailovic et al. 2014, Chisel).
*Luthier counterparts:* Demand-driven specimen selection along a graph of certified identities (`L6`, `L6.3`, `L6.5`, `L6.8`, `L10.7`, `concepts.md` section 13) and budget-scaling laws (`L9.17`, `concepts.md` section 9.5, bite C2).

### Exact question the comparison answers
On a multi-step numerical pipeline where each node has multiple specimens of different accuracy $(L, \eta, D, r)$, reliability $(\hat\varepsilon, \delta)$, and resource cost, how does Luthier's certified substitution graph and objective $\text{cost} + w \log(\text{resources})$ (`L6.3`) compare to (a) PetaBricks's uncertified empirical autotuning and (b) Chisel's Integer Linear Programming (ILP) accuracy-and-reliability allocation?

### Inputs
Build a 3-stage numerical pipeline benchmark (inspired by Chisel's and PetaBricks's benchmarks and Luthier's `sonolocalizacion` distance-to-position pipeline):
1. **Stage 1 (Distance reading / preprocessing):** Exact `Float64` specimen vs. `Float32` specimen vs. coarse lookup-table specimen certified on a grid $D_{\text{grid}}$ (`concepts.md` section 13).
2. **Stage 2 (Dot product / matrix kernel):** Naive `Float32` dot product, standard `Float64` `dot`, and Kahan compensated summation.
3. **Stage 3 (Nonlinear solver / norm):** Iterative solver with step budget $k \in \{5, 10, 20, 50\}$ scaling with target bound (`L9.17`).
Evaluate across 20 demands $(\varepsilon_{\text{max}}, \delta_{\text{max}}, w)$ with both in-distribution training inputs and out-of-distribution test inputs inside $D$.

### Metric
1. **Out-of-distribution contract violation rate:** Fraction of demands where the chosen configuration violates $\varepsilon_{\text{max}}$ on test inputs in $D$ not seen during PetaBricks training.
2. **Resource cost of selected configuration:** Total FLOPs/time of the valid configuration chosen by Chisel's ILP vs. Luthier's backward pull-back with uniform vs. sensitivity-weighted budget splitting (`L6.2`).
3. **Transitivity violation detection:** Whether the selector prevents chaining two specimens $A \leftrightarrow B \leftrightarrow C$ whose pairwise distance is $\le \varepsilon_{\text{max}}$ but whose composed distance $d(A, C)$ exceeds $\varepsilon_{\text{max}}$ (`concepts.md` section 13).

### What result counts as "the same", "Luthier weaker", or "Luthier stronger"
- **The same:** On single-node selection where all candidates are certified on $D$, Luthier's Pareto pruning and ranking `cost + w * log(resources)` selects the same Pareto-optimal frontier as PetaBricks and Chisel.
- **Luthier weaker:** On multi-input DAGs, naive uniform splitting of an output tolerance $\varepsilon$ across $k$ inputs ($\varepsilon_i = (\varepsilon - \eta)/(k L_i)$) is suboptimal when one branch has much cheaper high-precision specimens than another; Chisel's ILP (`pulp` / `scipy.optimize.milp`) jointly optimizes the split $(\varepsilon_1, \dots, \varepsilon_k)$ and $(\delta_1, \dots, \delta_k)$ to achieve lower total resource cost (`L6.2` leaves the split weight to the demand).
- **Luthier stronger:** PetaBricks autotunes empirically on training inputs without static bounds or domain certificates, so it has a non-zero contract violation rate on adversarial/boundary inputs in $D$ and can unsoundly chain non-transitive approximations; Luthier's planner only substitutes along certified 2-cells whose accumulated `BoundTransformer` and `EvidenceComposition` costs stay within the demand's cutoffs on $D_{\text{path}} = D_1 \cap f_1^{-1}(D_2)$.

### Tools to install and Linux / Python 3.12 compatibility
- **ILP solver (Chisel formulation):** `scipy.optimize.milp` in `scipy` `1.17.1` (already installed in `/home/lmoffatt/miniconda3/bin/python3.12`) or `pulp` `4.2.0` (`requires_python >= 3.12`, verified on PyPI). Note: the historical C++ PetaBricks repository ([https://github.com/petabricks/petabricks](https://github.com/petabricks/petabricks), last updated for GCC 4.x / Python 2) does not build on modern Linux with GCC 14 and Python 3.12, so PetaBricks's empirical Pareto autotuner is implemented directly in Python 3.12 alongside Chisel's ILP model from Misailovic et al. (2014).

### Effort for one agent
**4 hours** (1.5 hours to encode the 3-stage specimen graph with certified `BoundTransformer` edges; 1.5 hours to run Chisel's MILP budget allocator, PetaBricks's empirical tuner, and Luthier's pull-back search in `scipy.optimize.milp`; 1 hour to compare resource cost and contract violations).

---

## 10. Deductive Verification, Refinement Types, and Foundational Generator Laws (Dafny, Lean 4 / Flocq, QuickChick) vs. Luthier's Subtypes, `Proved` Grade, and Generators

*Antecedents:* `related-work.md` sections 5, 14.1, and 14.3 (Leino 2010, Dafny; de Moura and Ullrich 2021, Lean 4; Boldo and Melquiond 2011, Flocq; Paraskevopoulou et al. 2015, QuickChick).
*Luthier counterparts:* Refinement subtypes `{ x : T | p }` (`L8.5`, `L8.10`, `concepts.md` section 2.1), the `Proved` certifier grade (`spec 6.R1`, `6.S9`, `concepts.md` section 6.1), and explicit generators `Gen T` with region coverage (`spec 7.S1`, `L9.16`, `concepts.md` sections 6.2 and 6.4).

### Exact question the comparison answers
1. Can the core laws that Luthier currently marks as `Proved` by prose citation (or certifies by `Cases` / `Sampled`) be mechanically proved in Dafny / Z3 or Lean 4, and do any of Luthier's stated laws require hidden preconditions to be deductively valid?
2. Do Luthier's subtype generators (`Mark`, `InOrder`, `Step`, `sameOrNat` in `tape.test.lut`) satisfy QuickChick's formal generator *soundness* (every generated value satisfies the subtype predicate) and *completeness* (every region/boundary of the subtype has non-zero probability of generation)?

### Inputs
1. **Deductive verification corpus:**
   - The 4 exact laws of `Tape` (`ReadingSymmetric`, `ReadingAdds`, `ReadingSteps`, and the uniqueness theorem $r(a, b) = |a - b|$ from `concepts.md` section 2.3).
   - The 5 laws of `Metric` (`MetricZeroOnEqual`, `MetricIndiscernible`, `Commutative`, `Triangular`, `MetricNonNegative`) on `MarkIsAMetric` (`concepts.md` section 3.2).
   - The 9 algebraic laws of `BoundTransformer` (`ComposeSound`, `ComposeAssociative`, `EmptyDomain`, `PullbackMeets`, etc., `concepts.md` section 9.3).
   - The dioid laws of `ErrorBase` and `EvidenceComposition` (`AtLeastTheUnionBound`, `IndependentComposition`, `concepts.md` section 10).
2. **Generator corpus:** Luthier's generators for `Mark`, `InOrder` (rejection-filtered from `Mark^3` vs. constructive ordered generation), `Step`, and `sameOrNat`.

### Metric
1. **Deductive discharge rate and missing-premise count:** Fraction of the 20 core laws discharged automatically by Z3 / Dafny, and the number of laws where Z3 finds a counterexample due to an unstated precondition (for example, $L_1 > 0$ or $L_1 \ge 0$ in `BoundTransformer`, or NaN/Infinity on `Float64`).
2. **Generator acceptance rate and region hit probability:** For each subtype generator over $N = 10^4$ draws, the fraction of draws accepted by the subtype filter (soundness = 100% after filter; efficiency = acceptance rate) and the minimum empirical probability mass across all declared regions (`FromLaw` boundaries).

### What result counts as "the same", "Luthier weaker", or "Luthier stronger"
- **The same:** Z3 / Dafny proves all 4 `Tape` laws (and the uniqueness theorem $r(a, b) = |a - b|$), all 5 `Metric` laws for `MarkIsAMetric`, all 9 `BoundTransformer` laws over real/rational parameters, and the dioid laws of `ErrorBase` and `EvidenceComposition` with 0 missing preconditions.
- **Luthier weaker:**
  1. *Unchecked `Proved` citations:* In Luthier today, `Proved` cites a theorem name in text (`spec 6.S9`) without checking a proof artifact; if a law over `Float64` or `BoundTransformer` omits a non-negativity premise ($L \ge 0, \eta \ge 0, r \ge 0$) or NaN exclusion, Z3 immediately produces a counterexample that a prose `Proved` citation or small `Cases` list misses.
  2. *Rejection sampling on narrow subtypes:* Drawing `InOrder = { a b c : Mark | a <= b and b <= c }` by filtering independent triples wastes $5/6$ of draws and hits the equality boundary $a = b = c$ with probability $1/50001^2 \approx 4 \times 10^{-10}$ unless constructive boundary generators (`sameOrNat`) are bound (`concepts.md` section 6.6).
- **Luthier stronger:**
  - Dafny and Lean 4 cannot certify foreign Python/C scientific libraries (`extern`) or empirical accuracy laws (`DotStable` on hardware floats without a full Flocq formalization of the binary), whereas Luthier's graded `(domain, cost)` model combines deductive `Proved` laws on `BoundTransformer` with `Sampled` $(\hat\varepsilon, \delta)$ certificates on foreign realizations.

### Tools to install and Linux / Python 3.12 compatibility
- **`z3-solver`:** Version `5.3.2.0` on PyPI (verified `manylinux_2_27_x86_64` wheel, runs natively in Python 3.12 via `import z3`).
- **Dafny:** Release `v4.11.0` (verified GitHub release at [https://github.com/dafny-lang/dafny/releases/tag/v4.11.0](https://github.com/dafny-lang/dafny/releases/tag/v4.11.0), provides prebuilt Linux `x86_64` zip).
- **Lean 4:** Release `v4.35.0` (verified GitHub release at [https://github.com/leanprover/lean4/releases/tag/v4.35.0](https://github.com/leanprover/lean4/releases/tag/v4.35.0)).

### Effort for one agent
**4 hours** (2 hours to encode the `Tape`, `Metric`, `BoundTransformer`, and `EvidenceComposition` laws in `z3-solver` in Python 3.12 and verify or find counterexamples; 1 hour to measure subtype generator acceptance and boundary region probabilities; 1 hour to document any missing preconditions found by Z3).

---

## 11. Workflow Provenance and Proof-Carrying Data (W3C PROV, RO-Crate, PCD) vs. Luthier's Run Records and Value Derivations

*Antecedents:* `related-work.md` sections 7 and 8 (Moreau et al. 2013, 2015, W3C PROV; Ó Carragáin et al. 2022 and Leo et al. 2024, Workflow Run RO-Crate; Chiesa and Tromer 2010, Proof-Carrying Data).
*Luthier counterparts:* The three separated records (`x.lth`/`x.lut` claim, `x.cert.json` certificate store, `x.run.json` and `x.results.json` execution records, `concepts.md` section 14, `L10.13`), pre-execution cone admission (`spec 12.S17`, `concepts.md` section 12.3), and the derivation of a value (`L5.22`, `L5.23`, `L11.10`, `concepts.md` section 12.4).

### Exact question the comparison answers
Can Luthier's three records (`tape.lut`, `tape.cert.json`, `tape.run.json`) be mapped losslessly into and out of W3C PROV and Workflow Run RO-Crate JSON-LD, and which integrity failures (stale cone hash, uncertified dependency, refuted control, violated numerical bound ratio, or uncalibrated input lineage) does Luthier's pre-execution gate (`luthier run`) block that W3C PROV and RO-Crate validators accept?

### Inputs
1. **Luthier artifacts:** `docs/concepts/tape.lth`, `tape.lut`, `tape.cert.json`, `tape.run.lut`, and a synthesized `tape.run.json` / `tape.results.json` following `concepts.md` sections 8.1, 12.3, and 14.
2. **Public RO-Crate profile:** The Workflow Run RO-Crate specification and example crates at [https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/](https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/).
3. **10 Tampered / Invalid Run Scenarios:**
   - T1: Source code of `tape.lut` modified after `tape.cert.json` was generated (stale cone hash).
   - T2: A law conjunct in `tape.cert.json` has outcome `Failed` or veto (`spec 6.S15`).
   - T3: A law conjunct has `"held": 0` (`Vacuous n`).
   - T4: The demand sets `--bound 0.3` while `MetresWithin` recorded `measured.worst = 0.4149` (`concepts.md` section 9.2).
   - T5: An `axiom` or `provisional` extern is in the live cone without `--accept assumed:LAW` (`spec 12.S17`).
   - T6-T10: Equivalence of consequence (`(a + b) * 1.0` vs. `a + b`), cross-language bridge precision loss (`Float64` to `Float32` in Python), and derivation subtype filtering ("must descend from calibrated input").

### Metric
1. **Round-trip field preservation (%):** Fraction of fields in `(x.cert.json, x.run.json, x.results.json)` preserved under export to W3C PROV (`prov`) / RO-Crate (`rocrate`) and re-import, vs. fields that require custom Luthier extension predicates.
2. **Pre-execution tamper/violation rejection rate:** Fraction of T1-T10 blocked *before* `main` executes by Luthier (`luthier run`) vs. standard `prov` / `rocrate` schema validation.

### What result counts as "the same", "Luthier weaker", or "Luthier stronger"
- **The same:** Prospective workflow structure (definitions in the cone) and retrospective execution metadata (inputs, timestamps, agent/interpreter version, output hashes) map 1-to-1 between Luthier's `x.run.json` and Workflow Run RO-Crate (`Entity`, `Activity`, `Agent`, `CreateAction`).
- **Luthier weaker:** Standard repositories (Zenodo, WorkflowHub) natively index RO-Crate `ro-crate-metadata.json` and W3C PROV JSON-LD, whereas Luthier's `x.cert.json` and `x.run.json` use a custom JSON schema and have not yet implemented O13's recursive constant-size derivation summaries (PCD's local compliance predicate $\Pi$).
- **Luthier stronger:** W3C PROV and RO-Crate are passive post-hoc logs that reject 0 of T1-T10 before execution and treat `(a + b) * 1.0` and `a + b` as unrelated operational traces; Luthier refuses T1-T5 before executing `main` (`spec 12.S17`), keeps certificates independent of run observations (`L10.13`), and defines derivation equality up to certified identities (`D-2026-10-25-a` question 5).

### Tools to install and Linux / Python 3.12 compatibility
- **`prov` (W3C PROV Python library):** Version `3.2.3` on PyPI ([https://pypi.org/project/prov/](https://pypi.org/project/prov/), `py3-none-any.whl`, `requires_python >= 3.10`, verified compatible with Linux and Python 3.12).
- **`rocrate` (RO-Crate Python library):** Version `0.16.0` on PyPI ([https://pypi.org/project/rocrate/](https://pypi.org/project/rocrate/), `py3-none-any.whl`, `requires_python >= 3.9`, verified compatible with Linux and Python 3.12).

### Effort for one agent
**3 hours** (1.5 hours to write a bidirectional converter between `tape.cert.json` + `tape.run.json` and `prov`/`rocrate` in Python 3.12; 1.5 hours to test T1-T10 and document the exact JSON-LD extension vocabulary needed for `cone`, `measured.worst`, and $(\hat\varepsilon, \delta)$).

---

## 12. LLM Specification Synthesis and Routing (Endres et al., FrugalGPT, RouteLLM) vs. Luthier's "Luthierizing a Library" and Specimen Routing

*Antecedents:* `related-work.md` section 13 (Endres, Fakhoury, Chakraborty, and Lahiri 2024; Chen, Zaharia, and Zou 2024, FrugalGPT; Ong et al. 2025, RouteLLM; Madaan et al. 2024, AutoMix).
*Luthier counterparts:* The two applications in `related-work.md` section 13: (1) "Luthierizing a library" (an AI agent synthesizes theories, laws, and controls, and Luthier's verifier filters them via `check`, `certify`, `Vacuous` rejection, and per-conjunct controls) and (2) routing among LLM specimens by certified results per dollar.

### Exact question the comparison answers
When an LLM proposes formal specifications (laws) for functions in a library, how many false, vacuous, or trivial postconditions accepted by naive property testing are rejected by Luthier's combination of `Vacuous n` (`spec 7.S12`), characterization checks (`spec 4.R10`), and per-conjunct negative controls (`L9.14`); and when routing across cheaper vs. more expensive LLM specimens, does cascading via `luthier check && luthier certify` reduce API cost per certified theory compared to static single-model selection or preference-based routing (`RouteLLM`)?

### Inputs
1. **Public benchmark (EvalPlus / HumanEval+):** A 25-function numerical and data-structure subset of HumanEval+ from [https://github.com/evalplus/evalplus](https://github.com/evalplus/evalplus) (verified release `v0.3.1`, matching the benchmark family used by Endres et al. 2024 for postcondition synthesis, which includes reference implementations and buggy mutant implementations for each problem).
2. **Luthier library functions:** 10 functions from `numbers.lth`, `arrays.lth`, and `tape.lth`.

### Metric
1. **Specification soundness (Reference pass rate):** Fraction of accepted specifications that hold on the ground-truth implementation.
2. **Specification completeness (Buggy mutant kill rate, Endres et al. 2024):** Fraction of EvalPlus buggy implementations killed by the accepted specifications under (a) `luthier certify` alone (pass on reference only), (b) `luthier certify` + `Vacuous n` check, and (c) `luthier certify` + `Vacuous n` + per-conjunct negative controls + characterization rule (`spec 4.R10`).
3. **Cost per fully certified specification ($/spec):** Total token cost divided by the number of sound, non-vacuous, mutant-killing specifications under single-model selection vs. a FrugalGPT-style cascade (`cheap_specimen -> luthier check/certify -> escalate to strong_specimen on failure`).

### What result counts as "the same", "Luthier weaker", or "Luthier stronger"
- **The same:** Luthier's control kill rate on synthesized `.lth` laws directly measures the same mutant-killing completeness metric defined by Endres et al. (2024).
- **Luthier weaker:** Requiring the LLM to synthesize both the `.lth` laws *and* a valid wrong-model control per conjunct increases prompt/token cost and lowers single-shot pass rates on smaller models compared to synthesizing bare postconditions without controls.
- **Luthier stronger:**
  1. Without `Vacuous n` and negative controls, LLMs frequently synthesize tautological laws (`x == x`), weak type-check laws (`result >= -1e9`), or second-implementation copies (`spec 4.R10`) that pass 100% of reference tests but kill $< 30\%$ of buggy mutants; requiring each synthesized conjunct to refute a control raises the mutant-killing completeness of accepted laws toward 100%.
  2. Unlike `RouteLLM` (which routes by a learned Chatbot Arena preference score without verifying the output), Luthier's mechanized verifier (`check` + `certify`) acts as an exact soundness/completeness oracle, so a cascade `try_then(cheap_model, strong_model)` has zero false-acceptance risk attributable to the router.

### Tools to install and Linux / Python 3.12 compatibility
- **`evalplus`:** Version `0.3.1` on PyPI ([https://pypi.org/project/evalplus/](https://pypi.org/project/evalplus/), `requires_python >= 3.9`, verified compatible with Linux and Python 3.12 via `pip install evalplus==0.3.1`).
- **`routellm`:** Version `0.2.0` on PyPI ([https://pypi.org/project/routellm/](https://pypi.org/project/routellm/), pure Python wheel `py3-none-any.whl`, runs on Linux with Python 3.12).

### Effort for one agent
**5 hours** (2 hours to extract 25 functions and their buggy mutants from `evalplus` `0.3.1`; 2 hours to evaluate candidate laws across the three filtering tiers (`certify` only, `+ Vacuous`, `+ controls & 4.R10`); 1 hour to compute the cascade cost-efficiency curve).

---

## 13. Uniqueness Typing for World Actions (Clean's `*World`) vs. Luthier's Single-Use World Token `W` and Action Validation

*Antecedents:* `related-work.md` section 14.5 (Barendsen and Smetsers 1996, Clean uniqueness typing).
*Luthier counterparts:* The world primitive `W` (`concepts.md` section 11, `D-2026-10-13-b`, `L4.11`, `spec 10.S3`, `10.S4`), sub-world independence theories (`D-2026-10-13-a`, `L4.12`), and runtime validation of host actions at first application (`L4.9`, `L4.10`, `spec 10.S10`).

### Exact question the comparison answers
Does Luthier's static check on `W` (`spec 10.S3`, `10.S4`) reject the exact same world-token duplication, aliasing, and closure-capture violations as Clean's uniqueness type checker (`*World`), and what host-side I/O bugs does Luthier's runtime action validation (`spec 10.S10`, observing `world.lth` state before and after) catch that Clean's trusted `*World` externs miss?

### Inputs
Build a test suite of **16 world-manipulating programs** in Luthier (`x.run.lut`):
1. **Linear / Uniqueness Violation Cases (10 programs):**
   - W1: Sequential threading `let (w1, _) = act1 w0 in act2 w1` (Valid).
   - W2: Direct duplication `(act1 w, act2 w)` reusing `w` twice (Invalid).
   - W3: Passing `w` twice to a binary function `f w w` (Invalid).
   - W4: Branching `if cond then act1 w else act2 w` where each branch uses `w` once (Valid).
   - W5: Using `w` both inside an `if` branch and after the `if` (Invalid).
   - W6: Capturing `w` inside a lambda `fn x { act w x }` that is called twice or mapped over a list (Invalid: closure duplication, a classic uniqueness typing subtle case in Barendsen and Smetsers 1996).
   - W7: Storing `w` in a record or tuple and projecting it twice (Invalid).
   - W8: Discarding `w` without returning it in `main : W -> W * Unit` (Invalid).
   - W9: Attempting `w1 == w2` (`W` has no `==`, `concepts.md` section 11) or using `W` inside a `.lth` theory file (`spec 12.S23`) (Invalid).
   - W10: Splitting `W` into independent sub-worlds `(w_file, w_console)` (`L4.12`, Clean's `openfiles`).
2. **Host Action Disagreement Cases (6 programs, `spec 10.S10`):**
   - W11-W16: Host `extern` implementations for `Console` or `File` actions whose post-state disagrees with the model in `world.lth` (for example, a host print/write that drops output, mutates the wrong channel, or fails silently).

### Metric
1. **Static uniqueness classification accuracy:** Agreement (`TP`, `TN`, `FP`, `FN`) between `luthier check` and Clean's uniqueness typing rules on W1-W10.
2. **Host disagreement detection rate:** Fraction of W11-W16 refused at first application by `luthier run` (`spec 10.S10`) vs. Clean (which trusts foreign C I/O primitives unconditionally).

### What result counts as "the same", "Luthier weaker", or "Luthier stronger"
- **The same:** `luthier check` accepts W1 and W4 and rejects direct duplication (W2, W3), branch-plus-continuation reuse (W5), discarded tokens (W8), and `==` on `W` (W9), matching Clean's `*World` rules.
- **Luthier weaker:**
  1. *Closure and container aliasing (W6, W7):* In Clean, any function closure or record that captures a unique `*World` becomes unique itself (`*`) so it cannot be applied or projected twice; if `luthier check` only counts syntactic occurrences of the variable `w` without propagating uniqueness attributes to closures and containers that capture `w`, W6 or W7 can slip past `check`.
  2. *Sub-world splitting (W10):* Clean's standard library provides `openfiles` to split `*World` into parallel sub-tokens, whereas in Luthier sub-world independence (`L4.12`) is declared in principle but `W` is currently threaded as a single token.
- **Luthier stronger:** Clean treats all `*World` primitives as unverified axioms; Luthier models the world in `world.lth` and checks host actions against that model on their first application in a run (`spec 10.S10`, catching W11-W16).

### Tools to install and Linux / Python 3.12 compatibility
- **Luthier (`luthier check` and `luthier run`):** Runs directly in the repository environment on Linux with Python 3.12/3.13. Clean's uniqueness typing rules for W1-W10 are self-contained and decidable (Barendsen and Smetsers 1996, section 4), so they can be checked directly by a 100-line Python 3.12 reference uniqueness-attribute checker alongside `luthier check` without needing a separate Clean compiler installation.

### Effort for one agent
**2.5 hours** (1 hour to write the 16 `.run.lut` test programs W1-W16; 1 hour to run `luthier check` and the reference Barendsen-Smetsers uniqueness checker on W1-W10 and test W11-W16; 0.5 hours to report any closure/container aliasing gaps).

---

## Summary Table

| Rank | Antecedent vs. Luthier Counterpart | Primary Benchmark / Input | Key Tools (Verified on Linux + Python 3.12) | Effort (1 Agent) |
|---|---|---|---|---|
| 1 | Herbie, Daisy, Rosa, Higham vs. `Within` and `BoundTransformer` | FPBench (`136` benchmarks in `FPBench/FPBench`, commit `d7ade34`) + `arrays.lth` | `python-flint 0.9.0`, `mpmath 1.3.0`, `herbie v2.3` (`racket 8.18`), `daisy 6a6f47a` (`OpenJDK 25`, `z3 4.13.3`) | 6.0 h |
| 2 | Rule of three, Clopper-Pearson, SPRT, Confidence Sequences vs. $(\hat\varepsilon, \delta)$ and `spec 7.S13` | Parametric grid + $10^5$ sequential Bernoulli streams (seed `20261021`) | `scipy 1.17.1` / `1.18.1`, `numpy 1.26.4`, `confseq 0.0.11` (from source + pure-Python `betting.py`) | 3.0 h |
| 3 | FitSpec and Mutation Testing vs. Per-Conjunct Controls (`L9.14`) | FitSpec `bench/` (`19` suites at `rudymatela/fitspec` `v0.4.10`) + `tape.lth`, `equality.lth`, `numbers.lth` | `fitspec 0.4.10` (`ghc 9.10.3`, `cabal 3.12.1`), `mutmut 3.8.0`, `cosmic-ray 8.7.0` | 5.0 h |
| 4 | Arb (`python-flint`), Interval, Affine Arithmetic vs. Proposed `Ball` (`RadiusWithinTransformer`) | FPBench (`rosa.fpcore`, `rump.fpcore`) + nonlinear curvature and branch-straddling stress cases | `python-flint 0.9.0` (`flint.arb`), `mpmath 1.3.0` (`mpmath.iv`) | 4.0 h |
| 5 | AC-Normalization and `egg` E-Graphs vs. Law Normal Form | 60 law pairs built from `lib/core/` and `tape.lth` (30 positive, 15 negative `Float64`, 15 library) | `egglog 14.0.0` (Python 3.12 wheel wrapping `egg`/`egglog`), `sympy 1.14.0` | 4.0 h |
| 6 | Vacuity Detection after Beer et al. vs. `Vacuous n` (`spec 7.S12`) | 25 laws from `lib/core/`, `tape.lth`, and adversarial De Morgan / multi-premise encodings | `z3-solver 5.3.2.0`, `sympy 1.14.0`, `hypothesis 6.170.11` | 3.0 h |
| 7 | Unison and Nix Content Hashing vs. Dependency Cones (`canon(cone(n))`) | 20 repository edit scenarios (10 meaning-preserving E1-E10, 10 meaning-changing E11-E20) | `ucm release/1.5.0` (Linux x64 binary), `nix 2.34.8` / `2.35.4` | 4.0 h |
| 8 | Fuzz, Granule, Mardare et al. vs. `transformSum`, `transformMax`, `ErrorBase` | 12 single- and multi-argument exact and floating-point functions + depth-$d$ pull-back trees | `granule v0.9.6.0` (Linux binary), `scipy 1.17.1` | 3.0 h |
| 9 | PetaBricks and Chisel vs. Planner (`L6`), Pull-Back (`L6.8`), Budget Laws (`L9.17`) | 3-stage multi-specimen numerical pipeline across 20 $(\varepsilon, \delta, w)$ demands | `scipy 1.17.1` (`scipy.optimize.milp`), `pulp 4.2.0` | 4.0 h |
| 10 | Dafny, Lean 4, QuickChick vs. `{ x : T \| p }`, `Proved` Grade, `Gen T` | 20 core laws (`Tape`, `Metric`, `BoundTransformer`, `EvidenceComposition`) + 4 subtype generators | `z3-solver 5.3.2.0`, `dafny v4.11.0`, `lean4 v4.35.0` | 4.0 h |
| 11 | W3C PROV, RO-Crate, PCD vs. `x.cert.json`, `x.run.json`, Value Derivations (`L5.22`) | `tape` artifacts + Workflow Run RO-Crate profile + 10 tampered/invalid run scenarios T1-T10 | `prov 3.2.3`, `rocrate 0.16.0` | 3.0 h |
| 12 | Endres et al., FrugalGPT, RouteLLM vs. "Luthierizing a Library" and Specimen Routing | 25 functions + buggy mutants from `evalplus/evalplus` (`v0.3.1`) + 10 Luthier library functions | `evalplus 0.3.1`, `routellm 0.2.0` | 5.0 h |
| 13 | Clean's `*World` Uniqueness Typing vs. World Token `W` (`spec 10.S3`, `10.S10`) | 16 world-action programs (10 uniqueness/closure cases W1-W10, 6 host disagreement cases W11-W16) | `luthier check` / `run` + Python 3.12 Barendsen-Smetsers uniqueness checker | 2.5 h |
| **Total** | **13 Comparisons** | | | **50.5 h** |
