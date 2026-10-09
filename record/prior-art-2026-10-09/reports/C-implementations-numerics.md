# Prior art, cluster C: one concept with many implementations, autotuning, equivalence, numerical realization

Searched 2026-10-09. Every claim below was checked against the linked source in this session unless it is marked UNVERIFIED.

## 1. Candidates

| Candidate | What it is | Luthier features (partial where marked) | Primary source |
|---|---|---|---|
| PetaBricks (Ansel et al., PLDI 2009; variable-accuracy version CGO 2011) | Language where `either…or` alternatives are first-class and an autotuner picks among them | F5 (strong: alternatives are checked against each other with a threshold, and the choice is written to a config file), F13 partial (threshold and accuracy requirement are arguments), F15 partial (accuracy metric) | https://commit.csail.mit.edu/papers/2009/ansel-pldi09.pdf ; https://dspace.mit.edu/handle/1721.1/67465 |
| Halide | The algorithm is stated once; the schedule is separate and searched | F5 partial (equivalent by construction, never tested) | https://people.csail.mit.edu/jrk/halide12/ ; PLDI'13 https://gpbib.cs.ucl.ac.uk/gp-html/Ragan-Kelley_2013_PLDI.html |
| Exo (PLDI 2022) | User-scheduled language; schedules are rewrites with effect analyses that guarantee equivalence; hardware instructions defined in user libraries | F5 partial, F6 partial (a foreign instruction's meaning is given as an Exo body) | https://github.com/exo-lang/exo/blob/main/docs/instructions.md ; https://dspace.mit.edu/handle/1721.1/144822 |
| SPIRAL | Transforms written as SPL matrix factorizations, rewritten by rules, then searched | F5 partial, F3 partial (Coq proof that each rule preserves the matrix) | https://www.spiral.net/doc/papers/SPIRAL_IEEE_2018.pdf ; https://popl21.sigplan.org/details/CoqPL-2021-papers/6/Verification-of-Algorithm-and-Code-Generation-for-Signal-Transforms |
| FFTW wisdom | The planner measures candidate plans; "wisdom" saves enough to rebuild the chosen plan, and it can be exported and imported | F5 partial (records the choice) | https://www.fftw.org/fftw3_doc/Words-of-Wisdom_002dSaving-Plans.html |
| ATLAS | Empirical BLAS tuning at install time | F5 partial | https://math-atlas.sourceforge.net/ |
| TVM AutoTVM / MetaSchedule | Tuning records in JSON: workload keyed by structural hash, schedule trace, measured run times; best one reapplied | F5 partial, F10 partial (hash-keyed record with costs) | https://tvm.apache.org/docs/deep_dive/tensor_ir/tutorials/meta_schedule.html ; https://tvm.apache.org/docs/reference/api/python/autotvm.html |
| Kernel Tuner (Python) | Benchmarks kernel variants and checks each against a reference `answer` with `atol`, or a user `verify(cpu, gpu, atol)` | F5, F13 partial, F16 partial | https://kerneltuner.github.io/kernel_tuner/stable/correctness.html |
| TASO (SOSP 2019) | Generates graph substitutions from operator specifications and verifies them with Z3 | F1 partial (operators as axioms), F5 partial | https://par.nsf.gov/servlets/purl/10129637 |
| array-api-tests | One spec, Hypothesis-generated inputs, run against any array library (numpy, cupy, torch, …) chosen by `ARRAY_API_TESTS_MODULE` | F2 partial, F5 partial (shared laws, no cost measurement), F16 | https://data-apis.org/array-api-tests/ |
| Julia Interfaces.jl (+ BenchmarkTools) | An interface is a named tuple of Bool test functions (mandatory and optional); `@implements` gives test objects; `Interfaces.test()` runs them. BenchmarkTools caches benchmark parameters | F1 partial, F2 partial, F5 partial | https://github.com/rafaqz/Interfaces.jl ; https://github.com/JuliaCI/BenchmarkTools.jl |
| Rosa (POPL 2014) / Daisy (TACAS 2018) | Programs over a non-executable `Real`; `require`/`ensuring` carry error bounds `x +/- 1e-11`; the compiler picks a float or fixed-point type that meets them | F7 (strong), F13 partial | https://arxiv.org/abs/1410.0198 ; https://people.mpi-sws.org/~eva/papers/tacas18_daisy_toolpaper.pdf |
| Herbie | Samples about 8000 inputs, compares against a high-precision ground truth (Rival/MPFR), measures error in bits, rewrites to cut it | F7 partial, F2 partial (sampled), F15 partial (error as a metric) | https://herbie.uwplse.org/doc/2.3/error.html |
| FPBench / FPCore | Common format for real-valued benchmarks with precondition and precision properties | F7 partial. UNVERIFIED in detail: the spec page would not load | https://fpbench.org/spec/fpcore-2.0.html |
| FPTaylor | Sound roundoff bounds by symbolic Taylor expansion; HOL Light formalization in the repo | F7 partial | https://github.com/soarlab/FPTaylor |
| Precimonious (SC13) | Delta-debugging search over variable precisions under a user error threshold on test inputs | F5 partial, F7 partial, F13 partial | https://www.davidhbailey.com/dhbpapers/precimonious.pdf |
| EnerJ (PLDI 2011) | `@Approx` vs precise type qualifiers; `endorse` is the explicit cast from approximate to precise | F7 partial, F6 partial (explicit crossing) | https://ece.uwaterloo.ca/~wdietl/publications/pubs/EnerJ11.pdf |
| Rely (OOPSLA 2013) | Each output has a reliability spec (probability of being correct), checked statically against a hardware spec | F15 partial | https://dspace.mit.edu/handle/1721.1/79355 |
| Chisel (OOPSLA 2014) | Picks approximate operations to minimize energy under a reliability and accuracy spec | F5 partial, F15 partial | https://people.csail.mit.edu/rinard/paper/oopsla14.pdf |
| Decaf (OOPSLA 2015) | Probability types with solver-aided inference; optional dynamic tracking | F8 partial, F15 partial | https://ready.cs.washington.edu/~luisceze/publications/decaf-oopsla2015.pdf |
| Uncertain<T> (ASPLOS 2014) | Conditionals on uncertain values are decided by Wald's sequential probability ratio test (SPRT), with significance level and power; Bayesian-network semantics | F8 partial (level and power) | https://jamesbornholt.com/papers/uncertaint-asplos14.pdf |
| Probabilistic assertions / MAYHAP (PLDI 2014) | `passert e, p, c`: e holds with probability ≥ p at confidence c; checked exactly or by acceptance sampling on a Bayesian network | F8 (closest), F2 partial | https://ready.cs.washington.edu/~luisceze/publications/passert-pldi2014.pdf |
| IntervalArithmetic.jl / IEEE 1788 decorations | Every interval carries a decoration (com, dac, def, trv, ill); an output's decoration is the minimum over its inputs; since v0.23 (July 2025) an NG flag marks results where non-interval numbers were mixed in | F7, F3 partial (graded, weakest link), F6 partial (debt mark) | https://juliaintervals.github.io/IntervalArithmetic.jl/stable/manual/construction/ ; https://discourse.julialang.org/t/ann-intervalarithmetic-0-23/131136 ; https://grouper.ieee.org/groups/1788/email/pdfqyG69NzyMS.pdf (draft text) |
| Arb / FLINT | Ball arithmetic: every result ball contains the exact result | F7 ("balls later") | https://flintlib.org/doc/arb.html |
| Gappa (+ Flocq) | Proves bounds on rounded expressions by interval arithmetic and emits a proof checkable in Coq or HOL Light | F7, F3 partial (exported proof object) | https://arxiv.org/abs/0801.0523 |
| Exact reals: ERC, iRRAM, AERN2, Marshall | Reals computed exactly; ERC adds a specification logic and Hoare logic over the reals (LMCS 2024) | F7 partial, but the reverse of Luthier: these compute `Real` | https://lmcs.episciences.org/13822 ; https://hackage.haskell.org/package/aern2-real ; https://github.com/andrejbauer/marshall |
| Alive2 (PLDI 2021) | Bounded translation validation of LLVM optimizations by SMT, loops unrolled to a bound | F5 partial (equivalence), its verdict is a "bounded" grade | https://www-old.cs.utah.edu/~regehr/alive2-pldi21.pdf |
| Lean 4 `Float` | `Float` deliberately has no lemmas; to reason about it you prove equivalence to a separate library and transfer | F7 partial (ideal vs realization kept separate) | https://lean-lang.org/doc/reference/4.33.0/Basic-Types/Floating-Point-Numbers/ |

Not counted: TACO and Tiramisu. Their algorithm/schedule split only matches F5 in the trivial sense.

## 2. Closest candidates

**PetaBricks.** This is the nearest thing to F5 (one concept, several implementations, tested and measured). Alternatives are written with `either…or`. The autotuner measures them and writes an application configuration file that a person can edit and feed back to the compiler. Section 3.5, "Automated Consistency Checking", runs every candidate on the same input and checks that the outputs agree. A threshold argument handles iterative methods that don't give exact answers. Where it differs from Luthier: the check uses a fixed input instead of laws on generated cases, it is behind a flag, it produces no certificate, and implementations are all native. Mechanism worth taking: the paper says it "makes it advisable to include a slow reference implementation as a choice so that faster choices can be checked against it." Because the checks ride on the tuner's own search, testing concentrates on the alternatives that actually get chosen.

**Rosa / Daisy.** This is F7 almost word for word. The paper calls `Real` a "non-executable specification language" and an "ideal baseline". Error bounds are part of the contract (`require(x +/- 1e-11)`, `ensuring(res => res +/- 1.001e-11)`), and the compiler synthesizes the finite-precision type. Where it differs from Luthier: bounds are proved statically, not tested on doubles; there is no notion of a law as a reusable predicate; it handles one function at a time. Mechanism worth taking: put the tolerance in the function's signature on the real-valued side, so the choice of realization is solved against the declared tolerance instead of being hard-coded. That fits F13 (every criterion is a parameter) directly.

**Probabilistic assertions (MAYHAP) and Uncertain<T>.** Together these are the nearest thing to F8 "statistical laws declare level and power". `passert e, p, c` puts the probability and the confidence in the assertion itself. MAYHAP answers true, false or unverifiable, with a confidence interval. Uncertain<T> decides each conditional with SPRT: it draws batches of k samples until the result is significant or a maximum is reached, and the paper says the cap only slightly changes the actual significance and power. Where they differ from Luthier: the uncertainty is in program values (sensors, approximate hardware), not in evidence that a law holds, and the reading is frequentist, not Bayesian with the prior as a parameter. Mechanism worth taking: three-valued verdicts plus sequential testing with a declared cap, so a law's test stops as soon as the evidence suffices and records n, level and power.

**Exo `@instr`.** This is close to F6 in a stronger form. A foreign instruction (a C intrinsic) is declared with an Exo procedure body that "acts as a specification", next to the C template to emit. `replace()` swaps code for the instruction only when that body unifies with the code being replaced. Where it differs from Luthier: the match is syntactic unification, not testing, and the scope is kernels. Mechanism worth taking: an extern has two parts, a native reference body (its meaning) and the foreign call (its cost). The reference body is what laws and equivalence tests run against.

**IEEE 1788 decorations as implemented in IntervalArithmetic.jl.** This is a working, standardized version of F3's "graded by the weakest link", even though it is numeric. Decorations are ordered, and an output's decoration is the minimum of its inputs' decorations. The new NG flag marks results contaminated by non-interval numbers, which is F6's "provisional/debt" mark propagated by value. The same release also removed `==` and `<` on intervals because the meaning of equality was ambiguous, an argument for F13 (the equality a law uses is a parameter). Mechanism worth taking: carry the grade on the value and combine it with a lattice meet, so the weakest-link rule costs nothing per operation.

**Kernel Tuner and array-api-tests** are the closest on the Python side (F16). Kernel Tuner checks every tuned variant against a reference with `atol` or a custom `verify`. array-api-tests runs one Hypothesis-driven spec against any array library. Neither keeps certificates.

## 3. Features with nothing found in this cluster

- F3 itself: persistent certificates keyed by content hash, recording generators, seed and number of cases. Only fragments exist: the IEEE 1788 grade, Gappa's exported proofs, TVM's hash-keyed tuning records.
- F4: holes.
- F9: plan vs execution with a trace of actions. TVM records come closest, and only for tuning.
- F11: a minimal kernel and an interpreter stated in the language.
- F12: dependent types and universes.
- F14: AI writes the code, a scientist reads the specs.
- F8: generators as functors derived from types, and the Bayesian reading with the prior as a parameter.
- F10: provenance of every derived value. Only tuning logs come near it.
- F1: subtype by laws. TASO's operator axioms and Interfaces.jl are partial.

## 4. Surprises

- The IEEE 1788 decoration system and the NG flag (above) are the cleanest existing instance of "graded evidence, weakest link, debt marked when crossing a boundary". They come from interval arithmetic, not from PL verification.
- Alive2's verdict is literally "bounded" (correct up to an unrolling bound), which matches one of Luthier's grades and is a precedent for naming it.
- Lean 4's reference says `Float` is not meant to have lemmas. Its stated method (prove equivalence to a separate model, then transfer lemmas) is the F7 refinement relation written as policy.
- Interfaces.jl (Julia, actively developed, JuliaCon 2024) is the nearest thing in a scientific language to "a theory is a labeled product of operations plus Bool laws, tested on supplied objects". It is outside this cluster and probably worth a look by whoever covers F1/F2.
