# Prior-art search of 2026-10-09: the prompts

Luciano asked (chat, 2026-10-09): "quiero hacer una busqueda extensiva para ver si existe un
lenguaje de programacion o DSL que tenga algunas o todas las Caracteristicas de Luthier".

The model (Claude Opus 5.5, claude-opus-5-5) wrote the feature list below from
`docs/guide/00-fundamental-elements.md`, `docs/spec/04-kernel.md`, `06-numbers.md`, `08-tests.md`,
`docs/rationale/09-extern-and-the-world.md` and `record/objectives.md` at commit 7eb7ecd, and ran
six research subagents (general-purpose, same model, with web search) in parallel, one per family
of languages. Each got the common preamble and its own cluster paragraph, verbatim below. Their
reports are in `reports/`, unedited. The synthesis is `docs/rationale/10-prior-art-languages.md`.

## Common preamble

You are doing prior-art research for Luthier, a small programming language being designed by a
biologist (Luciano) for scientific analysis, where AI models write most of the code and he reads
the specifications. The question: does any existing programming language or DSL have some or all
of Luthier's features? Search the web thoroughly (official docs, papers, repositories, recent
2023-2026 work included). Verify each claim against a primary source (documentation, paper,
source code) and give its URL; mark anything you could not verify as UNVERIFIED. Do not pad: a
candidate that only has a feature in a trivial sense (e.g. "has functions") does not count.

Luthier's features, numbered:

- F1 Type = theory. A named type is a subtype of a base cut out by executable laws
  (`{ f : R -> R | Homomorphic f & AtZero f }`); a value of it is a model of the theory. A
  function's type is its postconditions and invariants. A theory of several operations is a
  subtype of a labeled product (signature + laws). Only laws or recursion make a new type.
- F2 Laws are executable Bool predicates and the language itself runs them as tests on generated
  cases (property-based testing built into the language, not a library); defining a function
  defines its test.
- F3 Certificates: persistent, first-class records attached to definitions, keyed by content
  hash, with a grade of evidence (point, sampled, bounded, exhaustive, witnessed, proved,
  assumed), recording generators, seed and number of cases. Membership in a type is a
  certificate, so nothing is checked twice. A program's certificate is the chain of its parts'
  certificates, graded by the weakest link. Every chain ends in assumptions.
- F4 Holes: a declaration without body (`x : T`), a theory without a model, filled by another
  file; what depends on it does not reduce until filled.
- F5 One concept, several implementations (native and foreign, e.g. Python/numpy), their
  equivalence tested against the same laws, their costs measured, the fastest chosen per case
  and the choice recorded.
- F6 Extern/FFI at a defined type: what the type claims becomes obligations checked when a value
  crosses the boundary; an extern whose type nobody described is marked provisional (debt).
- F7 Ideal numbers vs realization: `Real` is the ideal type (axiomatized, never computed),
  `Float64` refines its values but has the machine's operations; laws are written over the
  reals and checked on doubles within a tolerance; intervals or balls later.
- F8 Generators are values of the language and functors over types (derived from the type
  definition; bounds are part of the type); statistical laws declare level and power; evidence
  is read in a Bayesian way, with the prior as a parameter.
- F9 Plan vs execution: a timeless declarative plan (definitions, laws, equivalence) and an
  execution of actions with laws (a reading is an action that leaves the world unchanged),
  leaving a trace (partial order of actions with results and costs); the world is reached
  through pointers (a File pinned by hash).
- F10 Provenance: everything derived records its inputs by hash, the script version, every
  parameter and the seed.
- F11 Minimal recursive kernel, executable by hand on paper; the interpreter is to be stated in
  the language itself (program as a value of type Program), and the host is certified against
  that statement.
- F12 Dependent types (Π, Σ), a universe U, structural vs nominal types, `data` as initial
  algebras, aliases expanded before checking.
- F13 Every criterion is a parameter (tolerances, the equality a law compares with, priors),
  never a constant in the code.
- F14 Designed so that AI models write the code and a human scientist reads it: legibility of
  specs over implementation.
- F15 Laws valued in something other than Bool: a discrepancy or cost (quantitative/metric laws,
  Lawvere-style), turned into a loss; a "use" of a function carries a prior and a cost.
- F16 Aimed at scientific data analysis (biology), interoperating with Python.

Already covered by an earlier search (2026-09-29), do not re-report unless you find something new
about them: Idris VerifiedSemigroup, Lean plausible, Coq QuickChick, Isabelle Quickcheck/eval,
Scala discipline, Haskell quickcheck-classes, Hypothesis/proptest failure databases, SPARK
explicit assumptions and Hi-Lite, Frama-C property status, SLSA/in-toto, Larch, C++0x axioms,
Catsfoot, Gaudel's selection hypotheses, Idris 2 / Agda erasure, Stainless laws, Dafny
test-assumptions, gradual verification (Bader/Aldrich/Tanter, Gradual C0), EVE AutoTest/AutoProof.

Report format (plain markdown, at most ~1800 words):
1. A table: candidate | one-line description | features it has (F-numbers, with "partial" where
   partial) | primary source URL.
2. For the 3-6 closest candidates, a short paragraph each: what it does that matches, how it
   differs from Luthier, and one concrete mechanism worth taking (with source).
3. Features from F1-F16 for which you found nothing in your cluster.
4. Anything surprising: a candidate outside your cluster you stumbled upon that seems close.

## Cluster prompts

A. Specification and algebraic-specification languages, and theorem provers with executable
specs. Types as theories, models as inhabitants, predicate subtypes, holes/parameters filled
elsewhere. Look at least at: PVS (predicate subtypes, TCCs), ACL2 (executable logic, defthm),
CASL/HETS, Maude and CafeOBJ, Specware, OBJ, Isabelle locales, Lean 4 structures/mathlib
classes, MMT/OMDoc theories and views, Event-B/Rodin, Z, VDM (VDMTools/Overture, executable
specs and combinatorial testing), Alloy, TLA+/Apalache/Quint, Why3 (theories, cloning,
realization), F*, Liquid Haskell, Agda, Twelf.

B. Contracts, specs-as-predicates and assertion systems with statuses or evidence. Look at least
at: Clojure spec and Malli (specs as predicates, generators derived from specs,
instrumentation), Racket contracts and Typed Racket boundaries, Ciao Prolog assertion language
(check/trust/true/checked statuses, combined static and dynamic checking), Eiffel/AutoProof,
Sage and hybrid type checking (Flanagan), Pact, Unison (content-addressed code, test results
cached by hash), JML/OpenJML, Ada/SPARK contracts beyond what's covered, Pharo/GT, Hedgehog and
its state-machine testing, Elixir StreamData/typespecs, Python libraries that turn type hints
into runtime checks and generators (beartype, pydantic, icontract/crosshair, hypothesis
`from_type`, deal), Kotlin/Arrow laws, and any language with property tests as syntax.

C. One concept with many implementations, autotuning, equivalence and numerical realization.
Look at least at: PetaBricks (algorithmic choice + autotuner), Halide and Exo (algorithm vs
schedule), SPIRAL, FFTW wisdom, Tiramisu, TACO, ATLAS, Julia multiple dispatch with
BenchmarkTools, approximate computing languages (EnerJ, Rely, Chisel, Decaf), floating-point
tools that compile reals to finite precision (Rosa, Daisy, FPTaylor, Herbie, FPBench/FPCore,
Precimonious), exact real arithmetic languages (iRRAM, RealPCF, Marshall, ERC, AERN), interval
and ball arithmetic (Arb/FLINT, IntervalArithmetic.jl), and verified numerics (Coq Flocq,
Gappa). Also translation validation and differential testing of implementations.

D. Plan vs execution, effects with laws, traces, provenance and content addressing. Look at
least at: Nix and Guix (derivations, hashes), Unison, Bazel/Buck2, Dhall, Snakemake, Nextflow,
CWL, WDL, DVC, Pachyderm, noWorkflow/YesWorkflow, W3C PROV, Vistrails, Koka/Eff/Frank (algebraic
effects and their laws), Haskell IO and free monads, Granule and graded/coeffect languages
(beyond Orchard 2019 already in the bibliography), self-adjusting/incremental computation
(Adapton, Salsa), Datalog with provenance semirings, Pachyderm, Lean 4 `IO`, and
reproducible-research languages or notebooks that record inputs by hash (e.g. Sumatra,
CDE, ReproZip, Popper, Sciunit, renv/targets in R).

E. Mathematical and scientific languages where types are theories over carriers and domains are
models: Axiom/FriCAS/Aldor (categories with axioms, domains), Magma, GAP, SageMath categories,
Catlab.jl / AlgebraicJulia (generalized algebraic theories, models, applied category theory for
science), ModelingToolkit/Modelica (equation-based models), Fortress (traits with properties and
tests), F# units of measure, Stan / Turing / Birch / Gen (probabilistic languages, with priors),
SBML/Kappa/BioNetGen and other biology DSLs, Kernel/Statistical model checking languages, and
quantitative/metric logics turned into languages (Fuzz/DFuzz, Duet, signal temporal logic
robustness tools like Breach/S-TaLiRo beyond what is cited, quantitative algebraic theories).

F. Minimal self-describing kernels, programs as data, and languages designed for AI or for
human-legible specs. Look at least at: Lisp/Scheme metacircular evaluators, Kernel (Shutt,
fexprs), Shen and KLambda (small portable kernel, sequent-calculus types), Lean 4 written in
Lean, Idris 2 self-hosted, Maude reflection, Racket #lang, Unison, Dhall, Nock/Urbit (minimal
kernel), Mu/Pie (The Little Typer), Cedille, and especially languages and DSLs from 2023-2026
designed for LLM-written code with human-readable specifications or verification (e.g. Dafny
or Verus for LLMs, Lean-for-AI efforts, intent/spec languages, "vericoding", AI-native
languages, LMQL, any language whose stated goal is that a model writes and a human reviews the
spec). Also literate and "executable paper" approaches where the spec is the program.

## Addendum: cluster G, launched after the other six

While A-F ran, Luciano wrote (chat, 2026-10-09): "fijate que hay nuevas ideas, (la ultima usar
el object identifier de reales positivos, funcion de costo)". The model read it as the
subobject classifier of a topos (Bool in Luthier today) replaced by the positive reals [0,∞],
Lawvere's 1973 construction, as in the voice note of 2026-10-08 18.10.00 [14:35]-[17:34] (laws
that go to a cost and not to a Boolean, "una especie de likelihood ... no normalizada") and
[03:37]-[08:30] (a prior over parameters and a cost of failure, the function judged by an
expectation). Cluster G got the same preamble with this paragraph:

G. Truth values in [0,∞] or another quantale instead of Bool: languages and DSLs where a law,
predicate or specification is valued in a cost, distance or unnormalized likelihood, and where
satisfying it becomes minimizing a loss. This is F15 in depth, with F8 (priors) and F3
(certificates). Look at least at: Lawvere-style quantitative/metric logics turned into
languages (quantitative algebraic theories of Mardare-Panangaden-Plotkin and their tools,
quantale-enriched or real-valued logics, continuous logic for metric structures), differentiable
logics and specification languages that compile properties to loss functions (Vehicle, DL2,
Logic Tensor Networks / Real Logic, fuzzy differentiable logics, "constraints as loss"),
Probabilistic Soft Logic and hinge-loss Markov random fields, Markov logic networks,
weighted/semiring logic programming (Dyna, semiring Datalog, weighted Prolog, ProbLog), soft
constraint languages, signal temporal logic robustness as a language construct, Stan/PyMC
(`target +=` as a cost), tropical/min-plus programming, and testing driven by a prior over
inputs times a cost of failure (risk-based or importance-weighted property testing, Bayesian
software reliability, "expected cost of failure" in test selection). For each, say whether the
cost value is a first-class result of a law, whether Bool laws are a special case of it (the
logical limit), and whether the language certifies or records the measured cost.

## Reports, by SHA-256 (commit 997059b)

    7c4a224d54880fce573f571972b6effc6c116a12a056fa6eab6f965a87562ebb  reports/A-specification-languages.md
    e50b605d5d577cb8aac5b6b43dba203f8205200322e435c3e94d1eb4862cfe2a  reports/B-contracts-assertions.md
    71bfb68c20aef60fe9ca461165918fca0df12b7daa4e30e2f1167a0b3692586f  reports/C-implementations-numerics.md
    40e6229f2098aeb2015b3aafd2c90595eee519cce924e033b8b0f9168e2bb6d8  reports/D-plan-effects-provenance.md
    ccbb413b4aeac49779d690fd57883e043c84794f9109099b2fe14956aac8b818  reports/E-math-science-languages.md
    903deb61dfc0ceaea2d79dd6e13f8ecde47d695206e80a3eaef6a5ee7989a3c4  reports/F-kernels-ai-languages.md
    3bc00bb4bab2ea7f60ac434edd9e29a72e45268db578768d9f6af596ed53cc73  reports/G-cost-valued-laws.md
