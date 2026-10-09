# The map of ideas about Luthier, 2026-10-09

Written by `scripts/consolidate_lineages.py` (consolidate_lineages v1); prompt `consolidate_lineages_v1` (sha256 84d44a5d32ec), model opus at effort low. The grouping and the states are the model's reading; who said each idea
first and when come from the rows.

725 ideas in 33 themes: seedling 226, latent seed 486, open tension 13.

| theme | ideas | seedling | latent seed | open tension |
|---|---|---|---|---|
| Sonolocalización: the inference application | 54 | 17 | 37 | 0 |
| Working method and the pipeline | 54 | 9 | 45 | 0 |
| Laws as predicates and verification by test | 53 | 17 | 36 | 0 |
| Generators and the quality of the sample | 42 | 16 | 26 | 0 |
| Mathematical structures, presentations and translations | 36 | 14 | 22 | 0 |
| The minimal kernel and its primitives | 31 | 8 | 21 | 2 |
| Declaration versus definition and the states of a type | 31 | 11 | 20 | 0 |
| The declarative/executive split and realization | 31 | 6 | 24 | 1 |
| What Luthier is for: expressiveness, minimalism and its limits | 30 | 7 | 17 | 6 |
| Code as data and the self-interpreter | 29 | 8 | 21 | 0 |
| Numbers: Real, Float64 and intervals | 29 | 13 | 16 | 0 |
| Errors as data and the certificate | 28 | 11 | 17 | 0 |
| Probability, Bayes and statistical verification | 26 | 8 | 17 | 1 |
| The external world, extern and orchestration | 23 | 13 | 10 | 0 |
| The construction pattern: certified subtype and Library | 22 | 9 | 13 | 0 |
| Purpose, meaning and motivation | 22 | 5 | 16 | 1 |
| Concrete syntax and notation | 22 | 3 | 19 | 0 |
| Dependent types and the HoTT foundation | 15 | 2 | 12 | 1 |
| The forget functor and the typing-load problem | 14 | 6 | 8 | 0 |
| The derivation store and provenance | 14 | 1 | 13 | 0 |
| The code universe and reflection | 14 | 2 | 12 | 0 |
| Constructors, recursors and data mechanics | 13 | 4 | 9 | 0 |
| Equality: definitional, propositional and levels | 12 | 3 | 9 | 0 |
| Types as propositions that carry their laws | 11 | 5 | 6 | 0 |
| The run database and its synthesis | 11 | 7 | 4 | 0 |
| Program as DAG, commutativity and time | 11 | 4 | 6 | 1 |
| Luthier as a higher-order cross-language orchestrator | 11 | 2 | 9 | 0 |
| Path equivalence, implementations and optimization | 10 | 5 | 5 | 0 |
| Arrays and performance primitives | 7 | 3 | 4 | 0 |
| Environment, variables and memory | 6 | 0 | 6 | 0 |
| Objects as cyclic codependent definitions | 5 | 5 | 0 | 0 |
| Decorators, uncertainty functors and value annotations | 5 | 2 | 3 | 0 |
| Early identifier and naming explorations | 3 | 0 | 3 | 0 |

## Sonolocalización: the inference application

The concrete case that drives Luthier: situated objects, MAP, likelihood, score identities and the sampler.

- *seedling* `L-couple-to-sonolocalizacion`: Luthier is a meta-project whose next development couples to sonolocalización at the library (and MacroIR) stage, and how to relate the two remains to be worked out. (Luciano, 2026-09-21, 5 rows)
- *seedling* `L-concepts-belong-in-luthier`: Luthier is where the concepts are expressed, so organizing by Python module instead of by concept was the error that left the central concept (the likelihood) as a black box in Python; the concept must have its own type with its laws inside Luthier. (model, 2026-09-30, 7 rows)
- *seedling* `L-situated-physical-types`: The primary types are the situated physical objects of the inference (emitters and receivers in time, space and emission frequency), with recording and propagating as the forward model and inference as the inverse path to the object's coordinates decorated by uncertainty. (Luciano, 2026-09-30, 7 rows)
- *seedling* `L-absolute-vs-local-coords`: A situated object carries two coordinate systems with distinct roles, absolute (GPS/datetime) fixing identity and hash since two objects cannot share a place and time, and local for inference, joined by a Frame with a consistency law; both kinds of type are needed. (Luciano, 2026-09-30, 4 rows)
- *seedling* `L-score-identities-test`: The score identities (expected score zero, expected Hessian equal to score variance, Bartlett per row) tie a likelihood to its sampler and are what is_density_of asserts and tests. (Luciano, 2026-10-02, 12 rows)
- *seedling* `L-sampler-likelihood-kernel`: Sampler and likelihood are two readings of one Markov kernel, related as adjoint operators rather than adjoint functors. (Luciano, 2026-10-02, 12 rows)
- *seedling* `L-math-concept-stack`: The statistical objects are a bottom-up stack of mathematical concepts as types (measurable space, measure, density as Radon-Nikodym derivative, Markov kernel, expectation as positive linear functional, inner product), with Fisher information the inner product of L squared restricted to the tangent space and the gaussian model a map between inner-product spaces. (Luciano, 2026-10-02, 4 rows)
- *seedling* `L-shift-retraction`: shift moves a parameter in a tangent direction, the retraction of a manifold, distinguishing parameter space Theta from the tangent space Vec, and its laws read Theta through the likelihood since Theta has no equality of its own. (model, 2026-10-02, 4 rows)
- *seedling* `L-belief-prior-posterior`: Prior and posterior are one state of knowledge about theta (a Belief with a cursor over the data) updated by one operation; the gaussian belief in information form closes under the Laplace update so the MAP is how that update is implemented, and null-eigenvalue precision is an improper belief for rigid directions. (Luciano, 2026-10-02, 6 rows)
- *seedling* `L-convergence-law`: The Laplace update as a convergence law (departure shrinks with noise at the expected order) measures approximation quality not correctness, so it is not diagnostic and was removed; the optimizer's convergence differs from the approximation's convergence. (model, 2026-10-02, 5 rows)
- *seedling* `L-shapes-preconditions-in-types`: The leaves do not carry their shape or range preconditions in their types (matVec accepts any shape, missing range checks), which should become dependent invariants. (model, 2026-10-05, 4 rows)
- *seedling* `L-shift-is-action`: shift is an action of the tangent space on Theta (an affine space), with ShiftByZero as its left identity and ShiftComposes its associativity, carried as invariant by MeanModel/Likelihood. (model, 2026-10-05, 3 rows)
- *seedling* `L-runs-not-what-certified`: What runs (10 nodes, full vector) is not what was certified (7 nodes, gauge); the transfer rests on an informal argument no law states and the checker ignores. (model, 2026-10-05, 5 rows)
- *seedling* `L-interpreted-likelihood-slow`: A 30-parameter fit takes 3 minutes because the cost is the interpreted likelihood. (model, 2026-10-05, 4 rows)
- *seedling* `L-likelihood-tangent-dimension`: Likelihood does not carry the dimension of its tangent space, so a density pair declared over the whole vector asserted something false and is restated over the dimensioned domain. (model, 2026-10-05, 6 rows)
- *seedling* `L-dimension-in-types`: The model's dimension must enter the types of probability, belief and optimization (Theta is VecOf n throughout), since with an unconstrained Vec Float64 the model's obligations were false. (model, 2026-10-05, 4 rows)
- *seedling* `L-problem-vs-objective`: negate falsely promises an Objective with laws from arbitrary functions, so a lawless Problem (what the algorithm runs) is split from an Objective (a Problem with laws) and negate returns a Problem, making the obligation disappear. (model, 2026-10-05, 4 rows)
- *latent seed* `L-couplings-as-types`: Energetic couplings, binding schemes and conformational spaces are represented and certified as types. (model, 2025-06-17, 3 rows)
- *latent seed* `L-dsl-unifies-domains`: One DSL framework unifies models across channels, enzymes, networks, signaling and regulation. (model, 2025-06-17, 2 rows)
- *latent seed* `L-embedded-semantic-structure`: Biological models carry embedded semantic structure such as symmetry groups, compositional operators and equivalence classes. (model, 2025-06-17, 2 rows)
- *latent seed* `L-formalize-state-energy-algebra`: Planned work to formalize a type system for state and energy algebra and HoTT-based state composition primitives. (model, 2025-06-17, 1 rows)
- *latent seed* `L-likelihood-type-propagation`: Likelihood recursion is encoded via type-theoretic propagation, with noise structures and model boundaries as dependent types. (model, 2025-06-17, 3 rows)
- *latent seed* `L-markov-generated`: Markov models become generated objects rather than arbitrary inputs. (model, 2025-06-17, 2 rows)
- *latent seed* `L-sampler-type-indexed`: Sampler state spaces and parameter manifolds are treated as type-indexed temperature-ladder manifolds. (model, 2025-06-17, 2 rows)
- *latent seed* `L-symmetry-as-identity-paths`: Symmetry reductions are path-based identities that collapse state redundancies into reduced Markov spaces. (model, 2025-06-17, 3 rows)
- *latent seed* `L-type-safe-priors`: Type-safe prior spaces bridge the MacroIR likelihood engine with structural model spaces. (model, 2025-06-17, 1 rows)
- *latent seed* `L-encode-as-types`: Model components, entities and deterministic structure are encoded as types. (model, 2025-06-17, 3 rows)
- *latent seed* `L-compositional-kinetic`: Kinetic models are built compositionally from conformational state components as an external product of degrees of freedom with energetic coupling rules and state aggregation. (model, 2025-06-17, 3 rows)
- *latent seed* `L-fisher-validation`: A likelihood implementation is validated by agreement between the Fisher Information Matrix from score covariance and the one from the Hessian, without full inference. (model, 2025-06-17, 1 rows)
- *latent seed* `L-macroir-consumes-models`: MacroIR consumes structurally defined Markov models and computes interval-averaged likelihoods for macroscopic current data. (model, 2025-06-17, 2 rows)
- *latent seed* `L-replace-adhoc-model-spaces`: Replace ad hoc model design with compositional, type-safe, generative model spaces. (model, 2025-06-17, 1 rows)
- *latent seed* `L-adjoint-forward-diagnostic`: Each forward operation (simulate, infer) is paired by adjunction with a diagnostic approximation (recover, summarize). (model, 2025-06-18, 4 rows)
- *latent seed* `L-groupoid-structure`: Inference operations and their diagnostics form equivalence classes, a pre-formal groupoid structure. (model, 2025-06-18, 1 rows)
- *latent seed* `L-modelgraph-parammanager`: Clean separation of the ModelGraph and ParameterManager structures. (model, 2025-06-18, 1 rows)
- *latent seed* `L-newton-raphson-toy-application`: Writing Newton-Raphson with all its invariants typed is Luthier's first concrete application and toy model. (Luciano, 2026-06-05, 2 rows)
- *latent seed* `L-graph-ends-types-middle-trace`: The whole thing is a graph with the situated-object types at the ends and inference running over the Python trace in the middle. (Luciano, 2026-09-30, 2 rows)
- *latent seed* `L-map-invariants`: Proposed invariants that certify the MAP (covariance calibration, null score, exact Hessian, rigid motion, scale, permutations, prior limits, and more). (model, 2026-10-02, 1 rows)
- *latent seed* `L-mutual-test-chain`: The MAP is tested with the likelihood as the likelihood is tested with the sampler, a closed chain where the algorithm produces a record and the test is a predicate over it. (Luciano, 2026-10-02, 2 rows)
- *latent seed* `L-map-as-iterate`: The MAP is assembled from a step function and an is_finished predicate via a generic iterate_until driver that separates algorithm from model, with an optimization module whose laws take the implementation as argument. (Luciano, 2026-10-02, 3 rows)
- *latent seed* `L-reported-vs-observed-info`: For the updated precision keep the information the likelihood reports (expected curvature, the paper's H) rather than the observed Hessian (curvature of the data at hand), adding the observed Hessian as an optional member. (model, 2026-10-02, 3 rows)
- *latent seed* `L-rewrite-regression-numbers`: The rewritten experiment_zero must reproduce the same numbers on session A (σ 25.6 cm with everything, 4.9 cm without parlante_A2) as a concrete regression. (model, 2026-10-04, 2 rows)
- *latent seed* `L-experiment-zero-independent`: experiment_zero does not depend on distances; it uses its own model over the whole position vector, with distances a separate branch. (model, 2026-10-04, 2 rows)
- *latent seed* `L-symmetric-matrix-type`: Spectral operations must take a Symmetric type (with a tolerance, since numpy's inverses are not exactly symmetric), putting the mathematical precondition in the type that the code was lying about. (model, 2026-10-05, 3 rows)
- *latent seed* `L-position-encodings-iso`: The three encodings of the positions are tied by no law though flatten is an Iso, and the gauge should be one injection with the rest derived. (model, 2026-10-05, 1 rows)
- *latent seed* `L-normalvec-uniform-law`: normalVec gets a law for the first time: its integral transform is uniform. (model, 2026-10-05, 1 rows)
- *latent seed* `L-objective-laws`: Objective carries its laws: the gradient is that of its value and the step matrix is positive semidefinite, plus the laws of any maximizer. (model, 2026-10-05, 1 rows)
- *latent seed* `L-certs-internal-not-empirical`: Nothing is applied to the real data; the certificates speak of internal coherence, not of whether the model describes the measurements. (model, 2026-10-05, 1 rows)
- *latent seed* `L-dome-gcc-externs`: The dome and GCC-PHAT with thousands of samples cannot be native given the speed and will be externs end to end. (model, 2026-10-05, 1 rows)
- *latent seed* `L-guarantees-in-comments`: Guarantees live in comments instead of in types (meanModel says its inputs are nodes but MapInput carries Vec Int unrelated to Node). (model, 2026-10-05, 3 rows)
- *latent seed* `L-kernel-triangle-works`: The Kernel triangle with two controls, each breaking a different side, is among what works. (model, 2026-10-05, 1 rows)
- *latent seed* `L-lm-controls-excluded`: The Levenberg-Marquardt controls were excluded on purpose because they belong to this particular case. (Luciano, 2026-10-05, 3 rows)
- *latent seed* `L-certify-full-design-fisher`: The density-pair laws are certified over the full design (all pairs of the seven nodes) rather than over sampled graphs, because they need a non-singular Fisher information that the session-A graph does not provide. (model, 2026-10-05, 1 rows)
- *latent seed* `L-note-not-field-data`: A note a model wrote inside a data table is not a field datum and must not be read back as one. (model, 2026-10-06, 1 rows)
- *latent seed* `L-sonoloc-written-in-luthier`: Use sonolocalización as a real case: write it in Luthier, see it work, and execute it possibly in Python. (Luciano, 2026-10-07, 1 rows)

## Working method and the pipeline

How the work is organized: audios to ideas to spec, records, reviews, waterfall versus iteration, mechanical checks.

- *seedling* `L-hottification-roadmap`: HoTTification is a staged program, a semantic elevation not a rewrite, running from SAV diagnostics through DSL/CLI modularization and wrappers to a full homotopical, type-theoretic kernel. (model, 2025-06-18, 7 rows)
- *seedling* `L-start-from-zero-light`: Start Luthier and its sonolocalization layer from zero with only the indispensable, archiving what exists and adding only what gets used, deferring the highly conceptual parts. (Luciano, 2026-10-02, 4 rows)
- *seedling* `L-spec-interpreter-first`: Write the formal specification first, not of the whole interpreter but the static semantics, the judgments the checker decides, which today live only in the code. (Luciano, 2026-10-04, 5 rows)
- *seedling* `L-spec-rule-accept-reject`: Each spec rule is written with two small .lut files, one to accept and one to reject, turning the spec into the interpreter's test suite, the law with its negative control applied to Luthier itself. (model, 2026-10-04, 5 rows)
- *seedling* `L-rules-as-errors-no-migration`: Rather than migrate old code behind a --strict flag, do not migrate it so the rules apply as errors from day one and each rewritten library is a pilot of the spec. (model, 2026-10-04, 4 rows)
- *seedling* `L-hardcode-twice-across-bridge`: Fixed facts like the gauge nodes are written twice across the Python/Luthier bridge, breaking one-name-per-thing and the no-hardcoding rule. (model, 2026-10-05, 5 rows)
- *seedling* `L-fix-certification-as-gate`: Freeze v0 and commit, then fix certification as a gate (generators respecting refinements, pending distinct from failure, delete entries without a current name, record the uncertified cone). (model, 2026-10-05, 5 rows)
- *seedling* `L-luthier-describe-deal-inverted`: The handoff deal that Luthier only describes got inverted; now gauge, jacobian, model and native solvers live in Luthier and Python must match it bit for bit. (model, 2026-10-05, 5 rows)
- *seedling* `L-mechanize-rules-lint-hook`: The instructions living in memory are moved to mechanical checks in three layers (what Luthier can reject, what a repo lint catches, what stays judgment with a mechanical reminder), which requires relaxing the rule that only Luciano runs the scripts for lints and certification. (Luciano, 2026-10-05, 5 rows)
- *latent seed* `L-snapshot-first`: Before committing to tests, record snapshots and compare results outside the system to decide which tests to run. (Luciano, 2025-09-27, 1 rows)
- *latent seed* `L-reasonable-then-wild`: His method of thinking is to work out the reasonable version first, then look for the wild move. (Luciano, 2026-05-26, 1 rows)
- *latent seed* `L-decompose-components`: A first task is to understand all the things Luthier currently groups together, to see which are functionally separable and which depend on which. (Luciano, 2026-05-27, 2 rows)
- *latent seed* `L-concept-first`: The first step is expressing concepts in Luthier with conceptual depth; the translation/implementation comes after. (Luciano, 2026-05-29, 1 rows)
- *latent seed* `L-acritical-amplifier`: The Luthier AI acted as an acritical amplifier, celebrating every idea without flagging contradictions or the state of the art. (model, 2026-05-29, 1 rows)
- *latent seed* `L-syntax-semantics-before-implementation`: Fix Luthier's syntax and semantics on paper first, and only then implement it. (Luciano, 2026-06-03, 3 rows)
- *latent seed* `L-concrete-to-luthier-problem`: A concrete implementation need is used to surface the underlying Luthier design problem. (Luciano, 2026-06-05, 2 rows)
- *latent seed* `L-infectability-lens`: Consolidation uses infectability as its lens: the ideas that most change how you program are the ones that most structure the language; it is a project-specific choice. (model, 2026-08-31, 2 rows)
- *latent seed* `L-mentor-friction`: The mentor step produces friction on the design process without designing itself. (model, 2026-08-31, 1 rows)
- *latent seed* `L-pipeline-method`: The working method is the pipeline audios to ideas to consolidation to mentor, and only after that cycle comes writing the specification. (model, 2026-08-31, 2 rows)
- *latent seed* `L-date-both-consolidations`: The May consolidation is kept by renaming and dating both versions so the ecosystem's evolution can be compared. (Luciano, 2026-08-31, 1 rows)
- *latent seed* `L-no-principle-without-example`: No principle enters the specification without an example worked by hand in the candidate notation. (model, 2026-08-31, 1 rows)
- *latent seed* `L-spec-makes-decisions`: The specification is the first document that makes decisions; a decision is recognized because it excludes something that still coexists in the audios. (model, 2026-08-31, 1 rows)
- *latent seed* `L-pipeline-forgetting`: The consolidation cost growing with the corpus is the forget-functor problem applied to the pipeline, to be handled by consolidating in batches or from a previous consolidate. (model, 2026-08-31, 1 rows)
- *latent seed* `L-prototype-python-then-fast`: Write the core interpreter in Python now to validate the design, since the interpreter uses its own types which are data, and only later rewrite eval in a fast language. (model, 2026-09-30, 3 rows)
- *latent seed* `L-luthier-describes-python-works`: In this phase Luthier only describes (types, laws, extern, test) with no non-trivial function bodies, and Python does the work. (model, 2026-09-30, 3 rows)
- *latent seed* `L-v0-scope-decisions`: The v0 scope (definitions, data, binders, match, named-component subtypes, extern, test; no Term-as-data, no propositional =, no bootstrap, Failure := String) with three revertible choices: name-bound variables with capture-renaming, generators as a registered Python function per type, and test as an operation over Program. (model, 2026-09-30, 1 rows)
- *latent seed* `L-what-belongs-in-luthier`: Python holds only the machine (ops behind extern) and the bridge; any decision that changes what the certificate means, including generators, arithmetic types and test itself, must be written and visible in Luthier. (Luciano, 2026-09-30, 3 rows)
- *latent seed* `L-report-in-concepts`: Work is reported to Luciano in concepts, the most important first, naming what failed or what limit was hit; a count like "33 laws" tells him nothing. (Luciano, 2026-09-30, 1 rows)
- *latent seed* `L-written-english`: Chat with Luciano is in Spanish but everything that stays written is in English, except his transcripts. (Luciano, 2026-09-30, 2 rows)
- *latent seed* `L-lut-first-then-python`: Develop the whole .lut program first and do the Python implementation afterward. (Luciano, 2026-09-30, 3 rows)
- *latent seed* `L-design-approval-before-code`: Before implementing anything the model describes the design and waits for approval before writing code. (model, 2026-10-01, 1 rows)
- *latent seed* `L-do-what-said`: The model does what Luciano said and nothing more. (Luciano, 2026-10-01, 1 rows)
- *latent seed* `L-static-semantics-doc`: A new 04-static-semantics document concentrates what was decided, with dated corrections to the existing four and pending decisions for Luciano. (model, 2026-10-04, 2 rows)
- *latent seed* `L-bases-firm-first`: First make Luthier's bases firm and complete, and only once decided revise everything so those bases hold, a waterfall approach. (Luciano, 2026-10-04, 2 rows)
- *latent seed* `L-against-pure-waterfall`: Pure waterfall fails: the rule changed three times and the two-bodies inconsistency surfaced only from writing a concrete example; specs written without executing err where no one imagined. (model, 2026-10-04, 2 rows)
- *latent seed* `L-rewrite-useful-new-syntax`: Take what is useful or theoretically elegant from the existing .lut and rewrite it under the new syntax. (Luciano, 2026-10-04, 2 rows)
- *latent seed* `L-generic-vs-project-location`: Generic libraries live in luthier/lib and project-specific files in sonolocalización, ending the duplicated copies that caused confusion. (model, 2026-10-04, 2 rows)
- *latent seed* `L-acoustic-stage-drives-next`: The next Luthier work should be pushed by the acoustic stage and the GCC likelihood, not the cleanup of the algebra. (model, 2026-10-05, 3 rows)
- *latent seed* `L-project-constants-leak`: Project-specific constants calibrated to the tape (pitTol, ensembleSize, zMax, fdStep) leak into the generic library instead of being parameters. (model, 2026-10-05, 3 rows)
- *latent seed* `L-tag-version-for-reproducibility`: Sonolocalización depends on Luthier's working tree with uncommitted changes and so is not reproducible from a commit; the fix is to tag a version. (model, 2026-10-05, 2 rows)
- *latent seed* `L-classify-problems-int-spec-proy`: Problems are split into three kinds marked so they don't mix: interpreter, specification and project. (model, 2026-10-05, 1 rows)
- *latent seed* `L-report-statistic-not-block`: A result like a residual's uniformity should be reported as a question, a statistic and its null level, informing rather than blocking (figures with a head). (model, 2026-10-05, 1 rows)
- *latent seed* `L-soundness-regression-suite`: A tests/soundness suite turns today's reproducible failures into regression tests. (model, 2026-10-05, 2 rows)
- *latent seed* `L-no-project-python-scripts`: Luthier's intent is that Luciano write no project-dedicated Python except the functions called through extern, and he asks whether the work is making patches. (Luciano, 2026-10-05, 3 rows)
- *latent seed* `L-name-the-patches`: The patches made in the work should be named as patches and noted in the plan rather than passing as specification. (model, 2026-10-05, 3 rows)
- *latent seed* `L-concurrent-session-commit`: With another session committing in the same repo, the model leaves its changes uncommitted and first looks at what the other session touched so its work is not swept into a commit with a different message. (model, 2026-10-05, 1 rows)
- *latent seed* `L-pi-stays-with-luciano`: The principal-investigator role in Luthier stays with Luciano because the design decisions are his, and an agent runs only subproblems with a mechanical acceptance criterion, since Luthier's mechanical verifier is stronger than a code-reading agent. (model, 2026-10-05, 2 rows)
- *latent seed* `L-phase-states-closing-check`: Each phase of a plan should state what check closes it, and a phase with no mechanical check belongs to Luciano and not to the autonomous run. (model, 2026-10-05, 1 rows)
- *latent seed* `L-hook-only-changed-files`: A Stop hook that runs luthier check over all project files charges every turn; it should run only on changed .lut files. (model, 2026-10-05, 1 rows)
- *latent seed* `L-precommit-lints-not-certify`: The pre-commit hook cannot run luthier certify (too slow, writes certificates mid-commit); it should run the lints and luthier check. (model, 2026-10-05, 2 rows)
- *latent seed* `L-mechanical-rules-plan-consistency`: Luciano doubts whether the mechanical-rules plan is consistent. (Luciano, 2026-10-05, 1 rows)
- *latent seed* `L-mechanical-check-is-shadow`: Rules that are matters of judgment transfer to a mechanical check only as a substitute, a shadow of the real rule. (model, 2026-10-05, 2 rows)
- *latent seed* `L-need-written-objectives`: Without the project's objectives written down, a model deciding within its margin has nothing to measure its decisions against. (model, 2026-10-06, 1 rows)
- *latent seed* `L-reduce-to-minimum`: AI output carries filler hard to judge; a criterion is to ask whether it can be reduced further and still work, as one minimizes an algorithm. (Luciano, 2026-10-07, 2 rows)

## Laws as predicates and verification by test

Defining a function defines its test; laws are ordinary declarations, holes until checked.

- *seedling* `L-types-make-code-safe`: Declaring a function declares the tests it must pass, so types encode preconditions and gate membership on testing, yielding self-verified programs. (Luciano, 2022-08-03, 5 rows)
- *seedling* `L-pre-postconditions`: Functions and types are defined by preconditions and postconditions, the postconditions defining the subtype. (Luciano, 2023-02-22, 12 rows)
- *seedling* `L-pre-formal-safety`: Semantic contracts and diagnostics form a pre-formal, soft homotopy layer that structures and defends correctness before hard type checking exists. (model, 2025-06-18, 5 rows)
- *seedling* `L-sav-framework`: Semantic Adjoint Verification is a lightweight diagnostic framework whose tests are derived from adjoint functor pairs rather than arbitrary unit tests. (model, 2025-06-18, 6 rows)
- *seedling* `L-oracle-vs-postcondition`: An oracle gives an external reference to compare against, beyond an intrinsic postcondition, though abstractly both are predicates over arguments and output returning a verdict. (model, 2025-09-27, 5 rows)
- *seedling* `L-definition-is-its-test`: Defining a function defines its test (its inverse, its simulation), so running the code runs the test. (Luciano, 2026-06-05, 10 rows)
- *seedling* `L-levels-of-verification`: A value can be untested or tested, with different levels of verification. (Luciano, 2026-08-31, 4 rows)
- *seedling* `L-define-invariants`: Defining an invariant f : A -> B with for-all x : A, g x (f x) where g : A -> B -> Bool: the for-all is the Π, g's Bool is lifted to a proposition via a data Cierto : Bool -> U, and the invariant ties to f either as a separate hole-definition (the declaration is the test) or as a package where the guarantee travels with the function. (Luciano, 2026-09-29, 8 rows)
- *seedling* `L-invariant-is-bool-function-field`: In version 0 an invariant is a function returning Bool, stored as a field of the definition beside the body, with a generator hole filled by type and the run kept as data. (model, 2026-09-29, 5 rows)
- *seedling* `L-laws-like-cpp-requires`: Laws are written in few lines like a C++ requires block: quantified variables in a header and one Bool expression per line, each a type requirement checked without running or a value requirement run by the test. (Luciano, 2026-09-29, 4 rows)
- *seedling* `L-native-extern-agree`: Each concept is written twice, native in Luthier as the slow conceptual reference and extern in Python as the fast version, and the test is that they agree; extern always, law always, native only when the law does not determine the operation. (Luciano, 2026-10-02, 16 rows)
- *seedling* `L-law-independence-witnessed`: A law is independent if a model exists satisfying all the others and violating it, an existential needing the witnessed verdict. (model, 2026-10-04, 2 rows)
- *seedling* `L-refined-codomain-no-obligation`: A refined codomain on an extern's type produces no obligation; neg : Float64 -> NonNeg can return -2.0 unchecked. (model, 2026-10-05, 5 rows)
- *seedling* `L-exception-skips-obligation`: A type obligation speaks of the values a computation produces, so an exception yields no value and that case is skipped, whereas a law stated in a definition's type keeps failing on an exception. (model, 2026-10-05, 3 rows)
- *seedling* `L-generic-laws-dont-run`: Laws generic in a type parameter (Theta : U) never run because there is no generator of U, so they are certified only when a program fills the hole with a concrete type that has a generator, or by a well-chosen instance, and asking for a generator of U is a static error. (model, 2026-10-05, 11 rows)
- *seedling* `L-check-refines-value-type`: A check done on a value refines its type (inside if p x, x has the refined type) so nobody checks it again, with the result's granularity chosen by the cost of redoing it; this applies to run results, which are checked once into the run record. (model, 2026-10-05, 10 rows)
- *seedling* `L-check-bool-primary-derived`: A check is written once as a Bool (the law, composing by and/or/not) with refinement by branch as the rule, and the refined type and other presentations are derived. (Luciano, 2026-10-05, 4 rows)
- *latent seed* `L-proof-assistants-verify`: Proof assistants (Coq, Lean, Agda) can verify the semantic correctness of biological models via type-checking. (model, 2025-06-17, 2 rows)
- *latent seed* `L-epistemic-firewall`: The SAV verification layer acts as an epistemic firewall defending the system against silent semantic drift during refactoring. (model, 2025-06-18, 3 rows)
- *latent seed* `L-sav-bridge-to-proof`: SAV bridges empirical outputs and tests toward future type-theoretic proofs, a proof proxy whose tests become type-inhabiting witnesses once types are ready. (model, 2025-06-18, 3 rows)
- *latent seed* `L-sav-triangle-identity`: An SAV test asserts that composing the diagnostic after the forward map recovers identity up to statistical or structural tolerance. (model, 2025-06-18, 2 rows)
- *latent seed* `L-tests-as-morphisms`: Each CLI operation is a typed morphism and each test a witness path or triangle identity, not a patch. (model, 2025-06-18, 5 rows)
- *latent seed* `L-contract-bundle`: A function's contract bundles its domains, postconditions, comparators, oracles, policies and metadata as one attached object. (model, 2025-09-27, 2 rows)
- *latent seed* `L-verifiability`: Luthier must verify that a function is correct; verifiability, with equivalence, is a minimal element of the language. (Luciano, 2026-05-27, 2 rows)
- *latent seed* `L-compiling-detects-errors`: Compiling is checking whether the code holds incompatible things; unlike algebraic calculation, many programs should not compile, because that is how errors are caught. (Luciano, 2026-09-02, 2 rows)
- *latent seed* `L-precondition-is-type`: A precondition is guaranteed by the argument's type, checked when the reference is formed; preconditions that are predicates over values require refined types. (model, 2026-09-13, 1 rows)
- *latent seed* `L-laws-are-declarations`: Laws are ordinary declarations, holes until proven, and falsifiable by an instance that does not type. (model, 2026-09-29, 3 rows)
- *latent seed* `L-total-vs-partial-guarantee`: A law can hold either by conditioning it in the type (total function, partial guarantee) or by restricting the function (partial function, total guarantee), the choice depending on who uses it. (model, 2026-09-29, 1 rows)
- *latent seed* `L-numeric-tests-not-logic`: The aim of the first version is to generate numeric tests, not to do propositional logic. (Luciano, 2026-09-29, 3 rows)
- *latent seed* `L-redundancy-crosses-coloneq`: The redundancy worth keeping is the one that crosses the := , where type and body say different things the verifier checks; redundancy repeated on one side is removable with sugar. (model, 2026-09-29, 3 rows)
- *latent seed* `L-law-is-type-plus-predicate`: A law is a type of arguments together with a predicate over them, so the generator knows what to sample and different laws can quantify over different variables. (model, 2026-09-29, 1 rows)
- *latent seed* `L-laws-force-decisions`: Writing a group's laws forces design decisions, such as what a read of an absent key returns. (model, 2026-09-29, 2 rows)
- *latent seed* `L-law-takes-function-as-argument`: A law takes the function under test as its first argument and the quantified variables after, so the type it belongs to has any implementation as a term. (model, 2026-09-29, 2 rows)
- *latent seed* `L-functions-need-no-self-knowledge`: Functions need no self-knowledge; a law is an ordinary function to Bool and the label is put by the verifier level, which knows the whole program and runs test as an operation over Program. (Luciano, 2026-09-30, 2 rows)
- *latent seed* `L-laws-live-in-type`: Laws live in the type and thus in the DAG like any definition, so changing a law invalidates dependents' certificates through the graph, and laws can be shared, cross components, or be inherited by a subtype over a subtype. (model, 2026-09-30, 2 rows)
- *latent seed* `L-atomic-laws`: Compound laws like Identity and Distributive are split into left and right atomic laws so each can fail separately, with the structure's components a product the predicate runs over. (model, 2026-09-30, 1 rows)
- *latent seed* `L-conjunction-of-predicates`: The law wrapper is unneeded; & is conjunction of quantified predicates (X->Bool)->(Y->Bool)->(X*Y->Bool) applied to curried functions, so the law's name is already the quoted expression. (Luciano, 2026-09-30, 2 rows)
- *latent seed* `L-conceptual-vs-machine-impl`: A de novo conceptual implementation stands alongside the machine's, and a conceptual test states and checks their relation (N is isomorphic to the non-negative integers, respecting sum and product), the conceptual definition serving as oracle with the certificate recording the range tested. (Luciano, 2026-09-30, 2 rows)
- *latent seed* `L-check-vs-test-stages`: check only verifies types and registers which laws remain pending; test runs the laws, writes the certificate and marks definitions certified, reverting them to stale when a definition or a dependency changes. (model, 2026-09-30, 1 rows)
- *latent seed* `L-law-only-when-known-true`: A hole-filled program is valid and the complete .lut is the specification; a law is written only when already known true (by math or existing tests), since an unverified law that turns out false is worse than a hole. (model, 2026-09-30, 2 rows)
- *latent seed* `L-tests-live-in-luthier`: The tests are not written by hand but generated in and belong to Luthier, not to the interface module. (Luciano, 2026-10-01, 2 rows)
- *latent seed* `L-test-run-same-operation`: Evaluating a predicate on determined names is running and on undetermined names is testing: the same evaluator under a different determination. (model, 2026-10-04, 1 rows)
- *latent seed* `L-law-needs-concrete-case`: As Luthier preaches for code, a law is written first but holds only when a concrete case puts it to the test. (model, 2026-10-04, 1 rows)
- *latent seed* `L-pattern-bound-not-quantified`: Obligations under a tuple pattern of any length are not quantified over the named components, but obligations under a constructor pattern still quantify over all of its argument. (Luciano, 2026-10-04, 3 rows)
- *latent seed* `L-law-in-hole-declaration`: The law belongs in the hole's declaration so filling it with the extern inherits the obligation and every use of the name is a certified value, removing the duplicated certified copies. (model, 2026-10-04, 3 rows)
- *latent seed* `L-abs-returns-nonnegative`: abs returns a NonNegative, backed by its law. (model, 2026-10-05, 1 rows)
- *latent seed* `L-setoid-caught-real-bug`: Typing same as a Setoid caught a real bug (the gaussian belief was not symmetric), the best evidence that the method catches errors. (model, 2026-10-05, 3 rows)
- *latent seed* `L-preconditions-only-bool-match`: Preconditions are only generated in match over Bool; match by constructor or label generates none. (model, 2026-10-05, 1 rows)
- *latent seed* `L-report-not-decidable`: When the checker cannot read which labels a law touches or decide an equality, it should report not decidable rather than approximate or count all labels as touched. (model, 2026-10-05, 2 rows)
- *latent seed* `L-refinements-in-sums-checked-flag`: Refinements inside sums and the --checked flag are added and recorded in the specification. (model, 2026-10-05, 1 rows)
- *latent seed* `L-checker-loses-laws-in-branches`: When the expected type has laws the checker does not inspect each branch of an if or match; it infers the type of the whole, loses the laws and raises one obligation over the whole expression. (model, 2026-10-05, 3 rows)
- *latent seed* `L-refine-reading-not-path`: When the checked fact is external, refining the value gives a guarantee that can expire, so the principle refines what was read, not the reference, and check and use must be the same operation. (model, 2026-10-05, 1 rows)
- *latent seed* `L-statistical-and-deductive-tests`: A function's type has two verification paths: a statistical test for what cannot be proved and a deductive test for what can, keeping both. (Luciano, 2026-10-07, 2 rows)

## Generators and the quality of the sample

How values of a type are produced for testing and what each certificate's reach then means.

- *seedling* `L-check-value-vs-function`: Checking a value is an exact computation and checking a function is sampling, but both are the same construct operation differing only in whether the check is exact or statistical. (model, 2026-09-29, 5 rows)
- *seedling* `L-exhaustive-int-is-small-range`: "Exhaustive" over Int means only the range -16 to 16, so a law is certified exhaustive on 33 cases that are not exhaustive. (model, 2026-10-05, 5 rows)
- *seedling* `L-field-laws-pass-by-tuned-magnitude`: The field laws of float64Field pass only because lawMagnitude is tuned to the generator range; associativity fails at (1e8, -1e8, 3e-9) and the type does not state the box. (model, 2026-10-05, 9 rows)
- *seedling* `L-generator-ignores-refinement`: The generator does not respect dependent refinements, producing false failures because the obligation was quantified over the base type, not the refined one. (model, 2026-10-05, 2 rows)
- *seedling* `L-pending-recorded-as-fail`: A law that cannot be run (no generator, out of fuel, pending over a theory) is recorded as FAIL, mixed with real counterexamples. (model, 2026-10-05, 10 rows)
- *seedling* `L-laws-didnt-need-language`: The four laws that paid off are well chosen but none needed the language; they come out the same with pytest plus hypothesis. (model, 2026-10-05, 7 rows)
- *seedling* `L-test-distribution-in-directive`: The distribution of test cases belongs in the directive, not in the type; an alias carrying a distribution contradicts R7. (model, 2026-10-05, 9 rows)
- *seedling* `L-gen-over-refined-type`: A generator is defined only over a type with a predicate, so a type like BrokenGraph must be a refinement subtype whose predicate the generated values are checked against. (model, 2026-10-05, 6 rows)
- *seedling* `L-generated-value-checked-against-type`: Each value a registered generator produces is checked against its type and a value outside it is an error, with gen T trusted as the declared-trust escape. (model, 2026-10-05, 6 rows)
- *seedling* `L-certification-performance-fixes`: Verifying each generated value used the slow substitution evaluator; Bool predicates are now decided on the fast machine and a law's type inferred once per type. (model, 2026-10-05, 4 rows)
- *seedling* `L-statistical-law-level-retry`: A statistical law declares its level (the probability of failing on a correct model), is retried with an independent seed before a failure counts as a counterexample (level alpha squared), and reports a verdict with that level rather than a bare pass/fail. (model, 2026-10-05, 8 rows)
- *seedling* `L-generation-part-of-certificate`: Unless a gen is declared the tester builds values from the type's structure, and that construction is part of what each certificate means and silently decides what a law actually tests; generators are checked for being in the type, never for covering it. (Luciano, 2026-10-05, 6 rows)
- *seedling* `L-generator-explicit-per-type`: There is no single generator per type, so a test must name the explicit generator it bound to each type and the certificate records it (gen T := disappears); functions are generated by a census over registered values. (Luciano, 2026-10-05, 12 rows)
- *seedling* `L-number-generator-limits-scale`: A number generator needs explicit limit values and a linear or logarithmic scale (with special values and their weight), the limits carried in the type, so a Float64 without limits in its type is a static error if the binding does not supply them. (Luciano, 2026-10-05, 5 rows)
- *seedling* `L-generator-is-luthier-value`: A generator is a Luthier value with its own type and laws, certifiable like any other, and the random number generator is an extern with its stochasticity laws declared in Luthier. (model, 2026-10-05, 2 rows)
- *seedling* `L-inverse-cdf-sampling`: Sampling by the cumulative sum of costs is inverse-CDF sampling, one primitive for the continuous case (linear or log) and the finite census, with exhaustive over an infinite type a static error. (model, 2026-10-05, 2 rows)
- *latent seed* `L-epistemic-compression`: A few adjunction-derived tests cover most of the risk; verification is compressed into a minimal, epistemically meaningful suite. (model, 2025-06-18, 2 rows)
- *latent seed* `L-argument-domains`: A Domain is defined for each function argument so sets of arguments can be sampled from it. (Luciano, 2025-09-27, 2 rows)
- *latent seed* `L-verify-by-sampling`: Luthier verifies postconditions by sampling possible inputs, and postcondition verification and coverage calibration are the same computation. (model, 2026-09-13, 1 rows)
- *latent seed* `L-certificate-reproducible`: A certificate that does not record the seed, generation parameters and domain of each variable is not reproducible, so one seed per run is chosen and stored, each definition's derived from it, and --seed repeats the whole run. (model, 2026-09-30, 2 rows)
- *latent seed* `L-generator-magnitude`: A depth-bounded generator only reaches small numbers, so size is a test parameter growing from 1 to a cap along the cases, and a generator that returns a refined type carries its own law and travels certified. (model, 2026-09-30, 3 rows)
- *latent seed* `L-hidden-parameter-exposed`: A hidden parameter that affects the guarantee, like a max depth with no criterion, must be recorded in the certificate and exposed. (model, 2026-09-30, 1 rows)
- *latent seed* `L-test-finds-domain-border`: Because size grows during a run, the first failure appears at the border of the domain where the law stops holding; the function does not change, what changes is the asserted domain, and the certificate records which assertion is true and where. (model, 2026-09-30, 2 rows)
- *latent seed* `L-negative-controls`: A test is diagnostic only if a wrong version fails it, so negative controls (a case that must fail) are needed, since a law nothing exercises certifies nothing. (Luciano, 2026-10-02, 3 rows)
- *latent seed* `L-alias-invariant-in-generator`: An apparent alias like Perturbed hides its real invariant in the generator rather than the type; the new rules expose it. (model, 2026-10-04, 2 rows)
- *latent seed* `L-certify-reloads-per-name`: Certification is slow because the script reloads and rechecks everything once per name; running all obligations of a file in one invocation would fix it. (model, 2026-10-04, 1 rows)
- *latent seed* `L-leaf-not-certified-via-another-leaf`: A leaf's certification tolerance should use the native definition, not another leaf, so no leaf certifies itself by leaning on another. (model, 2026-10-04, 2 rows)
- *latent seed* `L-statistical-tests-low-power`: The statistical tests have low power: few cases and controls that break the model at double sigma, the easiest case to detect, so a 10-20% error in sigma may go undetected. (model, 2026-10-05, 2 rows)
- *latent seed* `L-test-n-only-name`: test n over the whole object is not done: it runs only the name's obligations. (model, 2026-10-05, 2 rows)
- *latent seed* `L-function-generators-degenerate`: Function generators are degenerate, so any law quantified over functions is tested on a degenerate sample. (model, 2026-10-05, 1 rows)
- *latent seed* `L-vacuous-cases-pass`: Vacuous cases count as passes: an unreached antecedent, a false law with n=0, and an empty exhaustive domain all pass. (model, 2026-10-05, 1 rows)
- *latent seed* `L-one-generator-per-type`: A generator written over an alias is the generator of the type the alias names, and two generators for the same type are an error. (model, 2026-10-05, 3 rows)
- *latent seed* `L-brokentext-needs-grammar`: Giving BrokenText an honest predicate requires the format's grammar written in Luthier, which today only the Python parser has. (model, 2026-10-05, 3 rows)
- *latent seed* `L-time-per-law`: The time each law takes is recorded in its result and in the certificate so the explosive laws can be found. (model, 2026-10-05, 1 rows)
- *latent seed* `L-square-no-generator`: Square has no registered generator, so a square matrix is drawn by rejection (one in seventeen), a cost paid per case by every law with a Square parameter; it needs a real gen Square. (model, 2026-10-05, 3 rows)
- *latent seed* `L-objective-from-list`: An Objective should not be drawn by rejection (random functions almost never match their declared gradient) but taken from an explicit list of registered values, such as the project's own objective and a quadratic. (model, 2026-10-05, 2 rows)
- *latent seed* `L-reuse-not-run-law-result`: Re-running a not-run law is wasted work when code, generators and seed are the same, since the result is deterministic, so the tester could reuse that result as it reuses a certificate. (model, 2026-10-05, 2 rows)
- *latent seed* `L-binding-by-parameter`: Each quantified variable is paired with its generator by parameter, the only thing that distinguishes tol from an input of the mean, with profiles serving as abbreviation. (model, 2026-10-05, 2 rows)
- *latent seed* `L-polymorphic-one-instance`: For a broad class of polymorphic properties it suffices to test one well-chosen instance (Bernardy, Jansson and Claessen 2010). (model, 2026-10-05, 1 rows)
- *latent seed* `L-check-exit-zero-unproven`: luthier check exits with code 0 even when laws are unproven, so a Stop hook would not catch the uncovered obligations. (model, 2026-10-05, 2 rows)
- *latent seed* `L-generators-plan-not-implemented`: The most serious issue is that the whole generators plan is not implemented and may not even be specified. (Luciano, 2026-10-05, 2 rows)
- *latent seed* `L-sample-quality-is-prover-power`: Because Luthier certifies refinement types by sampling rather than by a prover, what in other languages is the power of the prover is here the quality of the sample. (model, 2026-10-06, 1 rows)

## Mathematical structures, presentations and translations

Expressing algebraic objects as types with laws, their several presentations, and certified translations between them.

- *seedling* `L-states-as-type-algebra`: States and channels and their multiplicities are represented with type algebra (sum for states, product for channels), with a constructor from a number to a set. (Luciano, 2022-06-28, 5 rows)
- *seedling* `L-express-math-structures`: The language must express mathematical structures (category, functor, group) with their laws, possibly in several declaration styles. (Luciano, 2023-02-22, 7 rows)
- *seedling* `L-generic-concept-contextualized`: A concept like status or iteration can be a generic class, with the particular algorithm it belongs to known from its containing context and carried as an identifier. (Luciano, 2026-06-05, 5 rows)
- *seedling* `L-projections-reconstruct`: Joining all the projections of an object recovers the original object. (Luciano, 2026-06-05, 4 rows)
- *seedling* `L-iteration-as-successor`: An iteration is defined by construction, applying a step that increments a successor, and the successor applies to sets beyond the naturals. (model, 2026-06-05, 4 rows)
- *seedling* `L-type-classes`: A class like Ring is instantiated over a carrier (Ring Vec, Int, R) with its members (+, *, zero and an equality member making it a setoid) bound to implementations via a named-field record literal checked field by field, and using the operators for members needs real type classes resolving by operand type. (Luciano, 2026-10-02, 9 rows)
- *seedling* `L-table-is-dependent-function`: Table is a dependent function from column and row to cell, the cell type depending on the column, with fromColumns as constructor and application as observer. (Luciano, 2026-10-03, 4 rows)
- *seedling* `L-theory-is-record`: A Theory is a record (tuple) of types and predicates over them, defined when its laws are written and concrete/inhabited only when a model is given. (model, 2026-10-03, 5 rows)
- *seedling* `L-theory-vs-presentation`: A mathematical object is a theory and what one writes is a presentation; the theory is never written, Luthier has presentations (cycles with laws) and certified translations between them. (model, 2026-10-04, 2 rows)
- *seedling* `L-translation-second-order`: A translation between presentations of the same structure is a second-order Luthier concept, expressible in Luthier quantifying over presentations (type operators U->U), where Luthier starts to show its uses. (Luciano, 2026-10-04, 6 rows)
- *seedling* `L-luthier-self-presentations`: Luthier itself admits different equivalent primitive elements and laws (it already has several presentations of itself, with sugar-to-core a translation), and one must be chosen. (Luciano, 2026-10-04, 4 rows)
- *seedling* `L-determined-up-to-iso`: Laws never determine a unique implementation and need not; they make all implementations behave the same from outside, determining the object up to isomorphism. (model, 2026-10-04, 1 rows)
- *seedling* `L-ad-hoc-laws-reproduce-implementation`: The objects-as-types-with-laws theory is not used in the key cases (Vec, Table, Mat, Objective); ad hoc laws reproduce the function's implementation instead of stating the mathematical invariants that characterize it. (Luciano, 2026-10-05, 4 rows)
- *seedling* `L-law-characterizes-not-reimplements`: A law states the mathematical property that determines an operation up to the presentation's equality; a second implementation is consistency not characterization, and the native definition is one more model certified against it. (model, 2026-10-05, 8 rows)
- *latent seed* `L-functor-as-implementation`: A functor is read as an implementation and a natural transformation as translating one implementation into another. (Luciano, 2023-03-02, 2 rows)
- *latent seed* `L-category-style-basics`: The basic elements are defined in category-theory style, functors from arrows, out of a few basal elements. (Luciano, 2026-05-30, 1 rows)
- *latent seed* `L-class-carries-structure`: A class should generate and carry its structure and give access to its records, rather than being a bare simple structure. (Luciano, 2026-06-05, 1 rows)
- *latent seed* `L-concepts-independent-or-tied`: Some concepts can live independently of their container (like a mean) while others are intrinsically tied to one (like an iteration to its algorithm). (Luciano, 2026-06-05, 3 rows)
- *latent seed* `L-abstract-algebra`: Luthier has to do with abstract algebra. (Luciano, 2026-08-28, 2 rows)
- *latent seed* `L-cross-representation-is-function`: A subtype is a restriction within one representation; when two types have different representations their relation is always a certified function with laws, never a subtype, with no implicit coercion (integers injected into the reals do not become reals). (Luciano, 2026-09-29, 2 rows)
- *latent seed* `L-nested-certified-structure`: A structure can carry another certified structure as a named component, the laws reaching into it with a dot and quantifying over two types at once, with the precision parameter propagating through the composition. (model, 2026-09-30, 2 rows)
- *latent seed* `L-module-is-record`: A module is a record whose components are its definitions, so qualifying with the dot is the same as projecting. (model, 2026-10-01, 1 rows)
- *latent seed* `L-operations-by-ops-or-properties`: A mathematical object's operations can be defined through other operations or by their properties; when both, a theorem connects them, and the elemental set is not unique. (Luciano, 2026-10-03, 3 rows)
- *latent seed* `L-pure-vs-derived-math-objects`: Some mathematical objects are pure, arising from nothing like the integers, and others are derived, built upon other objects. (Luciano, 2026-10-03, 1 rows)
- *latent seed* `L-presentation-must-be-value`: A presentation by holes is a file not a value and cannot be passed to a translation, which tilts objects with several presentations toward the record-of-laws style. (model, 2026-10-04, 2 rows)
- *latent seed* `L-presentation-supplies-equality`: The round-trip law is an undecidable equality between records of functions, so each presentation must supply its own observational equality as a component. (model, 2026-10-04, 2 rows)
- *latent seed* `L-translation-inherits-laws`: Because a translation returns a value in the target presentation, the target's laws become the obligation of the translated model and are inherited automatically. (model, 2026-10-04, 2 rows)
- *latent seed* `L-translation-tested-per-model`: A translation quantified over all carriers and models cannot be tested without a model generator, so it is certified per concrete model, not in general. (model, 2026-10-04, 3 rows)
- *latent seed* `L-extensionality-law`: An extensionality law (two values equal when all observers agree) is what turns 'the same observations' into 'the same object'. (model, 2026-10-04, 2 rows)
- *latent seed* `L-theorem-is-agrees-law`: An operation defined both via other operations and by its properties yields a theorem, which in Luthier is a law over a branch, the Agrees pattern. (model, 2026-10-04, 2 rows)
- *latent seed* `L-several-canonical-presentations`: There should be several canonical presentations and Luthier should prove their equivalence, though it is good to start with one. (Luciano, 2026-10-04, 2 rows)
- *latent seed* `L-table-accessor-partial`: A table accessor returning a default (0, 0.0, "") where a column is missing is a partial function in disguise, guarded by the schema invariants rather than the type. (model, 2026-10-04, 2 rows)
- *latent seed* `L-algebra-always-imported`: The algebra library must always be imported because it is the base of all the properties. (Luciano, 2026-10-05, 2 rows)
- *latent seed* `L-best-math-object-as-invariant`: For every concept, find the mathematical object that best represents it and put it as the type's invariant rather than merely stating it. (Luciano, 2026-10-05, 2 rows)
- *latent seed* `L-symmetric-matrix-vs-operation`: A symmetric matrix and a symmetric operation are distinct things, though a symmetric matrix obeys symmetric laws. (Luciano, 2026-10-05, 2 rows)
- *latent seed* `L-table-by-schema-laws`: Table becomes a type defined by the laws of its schema, with accessors carrying the column as a precondition, though the schema laws are not verified over the tables Python returns. (model, 2026-10-05, 3 rows)

## The minimal kernel and its primitives

What the few founding elements of the language are, from which everything else is built.

- *seedling* `L-only-types-and-functions`: Luthier collapses the many constructs into a single kind: only types and functions exist, and functions are themselves a type. (Luciano, 2026-05-29, 5 rows)
- *seedling* `L-executable-by-hand`: If well written, Luthier should be executable by hand with pencil and paper, like Lisp. (Luciano, 2026-05-29, 5 rows)
- *seedling* `L-quantifiers-first-class`: The logical quantifiers for-all and exists should be first-class citizens of Luthier. (Luciano, 2026-05-31, 6 rows)
- *seedling* `L-fundamental-elements-question`: What are the most fundamental elements of a program? Candidates: elementary types, elementary functions, code versus data, true/false, true-by-definition, address/data. (Luciano, 2026-09-28, 6 rows)
- *seedling* `L-core-library-sugar-layers`: The language is three layers: a small core (a handful of term forms plus data, definition and reduction, a ten-line EBNF with reserved words data, match, extern), a base library written in Luthier, and sugar whose translation is mechanical; no Bool, numbers, =, Sigma or Subtype in the core. (model, 2026-09-28, 3 rows)
- *seedling* `L-hole-needs-no-symbol`: The hole needs no symbol in the core: a bodyless declaration f : A → B is already a hole, an opaque name that doesn't reduce, and ? is derivable surface sugar. (Luciano, 2026-09-29, 4 rows)
- *seedling* `L-cartesian-closed`: Product, sum and exponential of types are missing to make Luthier a cartesian closed category. (Luciano, 2026-10-04, 6 rows)
- *seedling* `L-structural-types-primitive`: Product, sum and exponential of types are made language primitives with their named record {..} and variant <..> forms, a named type being a Π or Σ over a finite set of labels read positionally. (model, 2026-10-04, 13 rows)
- *latent seed* `L-create-objects-uniformly`: The language expresses and creates values, variables, types and functions uniformly, with their semantics. (Luciano, 2022-06-28, 2 rows)
- *latent seed* `L-primitives`: A proposed set of primitive value types and primitive functions. (Luciano, 2022-06-28, 2 rows)
- *latent seed* `L-semantics-own-universe`: The semantics lives in its own universe, not that of C++, even while using C++ structures to express it. (Luciano, 2022-06-28, 1 rows)
- *latent seed* `L-function-kinds`: Functions are of two kinds: predefined and user defined. (Luciano, 2022-08-03, 1 rows)
- *latent seed* `L-grammar-parallel`: Natural-language grammatical categories parallel programming constructs, a frame for choosing Luthier's primitives. (Luciano, 2026-05-29, 1 rows)
- *latent seed* `L-inventory-cpp-constructs`: An inventory of C++ constructs (classes, functions, enums, structs, templates, pointers, references, derived classes, polymorphism) as what exists and must be selected from. (Luciano, 2026-05-29, 1 rows)
- *latent seed* `L-no-inheritance-polymorphism`: Luthier would not incorporate C++-style derived classes or polymorphism. (Luciano, 2026-05-29, 1 rows)
- *latent seed* `L-lisp-single-primitive`: Lisp reduces everything to one primitive, lists, as inspiration for reducing Luthier. (Luciano, 2026-05-29, 1 rows)
- *latent seed* `L-minimal-core-primitives`: There should be a clear core where all Luthier operations execute, with only a few primitives implemented in C or similar so it runs. (Luciano, 2026-05-30, 3 rows)
- *latent seed* `L-recursive-like-lisp`: Luthier is imagined as a recursive language like LISP but nicer, with a clear mathematical equivalence for its code. (Luciano, 2026-09-02, 3 rows)
- *latent seed* `L-knuth-expressive-languages`: Luthier draws the most expressive and natural from lambda calculus, Lisp, C++ and Python, aiming at a language Knuth would like, with code as a first-class citizen. (Luciano, 2026-09-28, 1 rows)
- *latent seed* `L-core-five-pieces`: The core is five pieces (the definition with the hole, lambda calculus with reduction, U, Π, data); from data come Σ, =, ⊥, ⊤, N, Program, while Bayes, the run database and numbers-with-error stay outside as libraries. (model, 2026-09-28, 2 rows)
- *latent seed* `L-definition-fundamental`: The most fundamental element of a program is not the type or the function but the definition, name : Type := term; a program is a finite unordered set of definitions and the DAG comes from which names each uses. (model, 2026-09-28, 3 rows)
- *latent seed* `L-formers-are-primitive`: Elementary types and functions are not primitive; the primitives are the formers (U, Π, data), with N defined by data, R a structure with axioms and seno a hole. (model, 2026-09-28, 2 rows)
- *latent seed* `L-hole-five-roles`: The hole, a definition with a type and no body, plays five roles at once (axiom, program input, external function, pending definition, dead code), and "you don't execute until it's defined" is its exact semantics, removing the need for an External type. (model, 2026-09-28, 2 rows)
- *latent seed* `L-reject-address-data`: Address/data is rejected as a fundamental element: the name is the reference and the memory address is a decoration of the lowest equivalence level, with nothing to distinguish without mutation and time. (model, 2026-09-28, 2 rows)
- *latent seed* `L-mutation-and-ownership`: The core could include controlled mutation cells and linear or affine ownership for in-place mutation without garbage collection. (model, 2026-09-28, 1 rows)
- *latent seed* `L-hole-goal-messages`: A hole inside a term lets the verifier accept what is written and state the exact type of what is missing (Agda's goal), which is the compiler with good messages about what is happening. (model, 2026-09-29, 1 rows)
- *latent seed* `L-hole-no-intention`: The core does not distinguish why a hole has no body (to be filled externally or just unwritten); huecos : Program → List Name lists them all and intention goes in the definition's text field. (model, 2026-09-29, 2 rows)
- *latent seed* `L-ten-elements`: The whole language reduces to ten elements, of which eight are standard type theory and two are Luthier's own, the first-class hole and the test-checked certified subtype. (model, 2026-09-29, 2 rows)
- *latent seed* `L-kernel-choice-criterion`: The canonical core is chosen not by minimality but so the static semantics can be stated directly on it without a translation, keeping the subtype primitive though derivable. (model, 2026-10-04, 2 rows)
- *open tension* `L-function-type-expression`: Open question of how to express the type of a function such as write : a -> string. (Luciano, 2022-08-03, 1 rows)
- *open tension* `L-minimal-primitives`: Open question whether Luthier needs primitive functions or only coordinates external ones, keeping native components minimal, perhaps only identity and equality. (Luciano, 2026-05-27, 7 rows)

## Declaration versus definition and the states of a type

Declared, defined, determined, certified; whether type and value are one scale.

- *seedling* `L-two-kinds-of-definition`: There are two ways to define types, the constructive and the declarative. (Luciano, 2022-08-03, 4 rows)
- *seedling* `L-forms-of-definition`: The language distinguishes declaration from definition and lets one define functions or variables by their type without giving the implementation or value (parameters). (Luciano, 2023-03-02, 4 rows)
- *seedling* `L-double-definition`: A type defined twice could be flagged as error or read as a cartesian product that runs two ways. (Luciano, 2026-05-29, 6 rows)
- *seedling* `L-forward-and-undefined-types`: A type may be referenced before it is defined and defined later, or left undefined, in which case it is a program input. (Luciano, 2026-05-29, 3 rows)
- *seedling* `L-type-closes-with-laws`: Defining a type must mean something: a mere juxtaposition or product is not a new type, which closes only when laws connect its subcomponents (the closed style, unusable until closed), as opposed to a derived type that is an expression of operators over defined types. (Luciano, 2026-10-02, 14 rows)
- *seedling* `L-declared-vs-defined`: A type has states, declared (a forward-declared hole), defined (its invariants given) and certified; a value or extern definition requires a defined type while declarations may reference merely-declared types, which is what builds cyclic definitions. (Luciano, 2026-10-03, 24 rows)
- *seedling* `L-types-and-values-unified`: Almost eliminate the type/value distinction: everything is a type, some types are values of others, differing only in whether they are determined, so no extra symbol is needed. (Luciano, 2026-10-04, 4 rows)
- *seedling* `L-defined-determined-axes`: Defined and determined are independent axes (a hole can have laws without implementation, an extern implementation without laws); a name passes declared, defined, determined, certified. (model, 2026-10-04, 4 rows)
- *seedling* `L-alias-equals-not-coloneq`: Naming a product (AB = A*B) is an abbreviation expanded before verification with no states; naming it with := is rejected, with = it is an alias. (model, 2026-10-04, 5 rows)
- *seedling* `L-real-vs-theoretical-objects`: There are real objects with constructors and theoretical objects without; both exist and which is meant is made explicit, the native type being the real and the parametrized record the theoretical. (Luciano, 2026-10-04, 4 rows)
- *seedling* `L-primitive-keyword-explicit-state`: A name like R:U without a body does not error only because the checker holds a hidden primitives set; a name's state should be readable in the program through a `primitive` body, not a hidden list. (Luciano, 2026-10-04, 4 rows)
- *latent seed* `L-element-belongs-one-type`: Each element belongs to exactly one type but can serve to build many types. (Luciano, 2022-08-03, 2 rows)
- *latent seed* `L-inject-multiple-identifiers`: A type or function can inject more than one identifier into the environment. (Luciano, 2022-08-03, 1 rows)
- *latent seed* `L-type-autodetection`: Types can be handled by autodetection. (Luciano, 2022-08-03, 1 rows)
- *latent seed* `L-type-inference`: The type is deduced by type calculation, and a derived type larger than the parameter's type is flagged. (Luciano, 2023-03-02, 1 rows)
- *latent seed* `L-implicit-types`: Types can be defined implicitly, as the solution to a problem or the optimum of a function, rather than declared directly. (Luciano, 2026-05-29, 1 rows)
- *latent seed* `L-data-vs-subtype-choice`: Use data when a thing has its own form and operations and a subtype when it is a restriction of something that already has operations; the two are types of equal status and the subtype's short name is the interface. (Luciano, 2026-09-30, 3 rows)
- *latent seed* `L-closed-vs-open-definition`: A type can be defined closed, its carrier with operations and invariants together, or open, a bare carrier plus separately declared operations and laws that a model satisfies. (model, 2026-10-03, 2 rows)
- *latent seed* `L-rules-cost`: Enforcing order-independence and cycle detection has costs: native code over a declared-only type must become generic (the ML functor), and the whole file must be read before typing. (model, 2026-10-04, 1 rows)
- *latent seed* `L-form-before-laws`: A type's form, its base and labels, must be fixed in the declaration before its laws, since laws are written over its components and typed before the type closes. (model, 2026-10-04, 2 rows)
- *latent seed* `L-labels-are-binders`: Record labels are binding names like parameter names, so they do not enter the type's identity; a labelled record and the bare product are the same type. (model, 2026-10-04, 2 rows)
- *latent seed* `L-subtype-declaration-mark`: A distinct mark like C <: {...} is needed so the same phrase does not ambiguously declare a type-by-laws and a value-by-intention. (model, 2026-10-04, 1 rows)
- *latent seed* `L-determined-means-reducing-body`: A body computes while a law only verifies, so 'determined' in practice means having a body or extern that reduces. (model, 2026-10-04, 1 rows)
- *latent seed* `L-value-single-inhabitant`: A value is a type with a single inhabitant (4 is {n:N|n==4}), which makes the determined/undetermined scale literal and collapses the two relations into refinement; x:T means x refines T. (model, 2026-10-04, 3 rows)
- *latent seed* `L-body-type-resolves-ambiguity`: Whether a definition gives a value or a subtype is resolved by the body's type (T vs T->Bool), not by a symbol. (model, 2026-10-04, 2 rows)
- *latent seed* `L-one-body-per-name`: Giving a name both a body of laws and := extern is two bodies for one name, forbidden; the two styles that seemed to coexist are one badly written. (model, 2026-10-04, 2 rows)
- *latent seed* `L-new-type-from-recursion-or-laws`: Only recursion (infinite freedom) or laws (refinement) generate a new named type; a product or sum without laws deserves no new name. (model, 2026-10-04, 3 rows)
- *latent seed* `L-one-name-per-thing`: Do not declare the same thing under two distinct names. (Luciano, 2026-10-05, 2 rows)
- *latent seed* `L-positional-identity-trap`: The positional identity of products and sums lets fields be swapped silently, which the spec says and which is a trap. (model, 2026-10-05, 1 rows)
- *latent seed* `L-membership-construction-or-hypothesis`: A value belongs to a type either by construction (the case is given) or by hypothesis, a construction by value that can fail. (Luciano, 2026-10-08, 2 rows)
- *latent seed* `L-many-function-types`: A function's type need not be unique; there can be many function types one invents, such as positive functions from reals to positive reals. (Luciano, 2026-10-08, 1 rows)

## The declarative/executive split and realization

Separating the timeless plan from execution, the host as a realization, and writing the interpreter in Luthier.

- *seedling* `L-program-as-function`: A Luthier program is modeled first as a pure function (input to output), extendable later to an interactive model, and can take another Luthier program as input. (Luciano, 2026-05-30, 4 rows)
- *seedling* `L-express-then-execute`: You first express the ideas with pencil and paper and then go to execution or the empirical database; these are two layers, not opposed philosophies. (Luciano, 2026-05-30, 6 rows)
- *seedling* `L-pyluthier-implementation`: A Python implementation carries the type as a floating class attribute, the easiest start, though Python is not a real type tool and the type ends up as fields and decorations. (Luciano, 2026-08-31, 4 rows)
- *seedling* `L-constants-must-be-parameters`: A criterion hardcoded as a constant in the code (lmMaxIter, the rejection-sampler's try budget) must be a parameter, by the rule that every criterion is a parameter. (model, 2026-10-05, 8 rows)
- *seedling* `L-hole-no-default`: In Luthier a hole has no default, so each run must supply every parameter by --set; a parameter with a default value that --set replaces and the run records would be a new language feature. (model, 2026-10-05, 3 rows)
- *seedling* `L-declarative-and-executive`: Luthier has a declarative part (types that follow laws) and an executive part that runs commands (read a file, execute a function); the executive part can be internal or external. (pasted, 2026-10-08, 7 rows)
- *latent seed* `L-language-parts-compiler`: The language has parts: a grammar with semantic rules and a front compiler to C++. (Luciano, 2023-02-22, 1 rows)
- *latent seed* `L-spec-without-implementation`: Inspired by Modelica, Luthier separates the specification of a program from its implementation. (Luciano, 2026-05-30, 2 rows)
- *latent seed* `L-description-language`: Luthier's first stage is a language for describing the problem, the functions and the conditions under which they work, not for execution. (Luciano, 2026-05-30, 3 rows)
- *latent seed* `L-execution-is-verification`: Execution in Luthier is the verification of equivalences, as mathematics does not execute but only verifies equivalences. (Luciano, 2026-05-30, 2 rows)
- *latent seed* `L-import-declares-dependencies`: A .lut file declares its dependencies with import, which is the combinar operation (union of definitions rejecting conflicts), with a prefix form to disambiguate clashing names. (Luciano, 2026-09-30, 2 rows)
- *latent seed* `L-dismantle-prelude`: Dismantle the prelude: fundamental is only what the interpreter names on its own while elaborating (Bool, List, Unit/Maybe, Nat), which fits in a twenty-line core, and everything else is a library imported on demand. (Luciano, 2026-09-30, 2 rows)
- *latent seed* `L-criterion-is-cli-hole`: A criterion is a hole filled from the command line with --set and recorded in the certificate with the hashes, while effects become externs and luthier run evaluates a main definition. (model, 2026-10-03, 1 rows)
- *latent seed* `L-literal-lint-type-vs-criterion`: A mechanical criterion to classify numeric literals: a constant in type position (a refinement bound) defines a type, one in term position is a criterion. (model, 2026-10-05, 2 rows)
- *latent seed* `L-luciano-writes-interpreter-c`: Once the syntax is fixed, Luciano would write the Luthier interpreter himself, eventually a small core in C for speed with the rest in Luthier. (Luciano, 2026-10-07, 2 rows)
- *latent seed* `L-host-minimal-duties`: If the interpreter is written in Luthier the host need only reduce, run the primitive types' operations, and call an extern reading and writing a File, plus read a canonical serialization of Term, with everything else Luthier definitions over Program. (pasted, 2026-10-08, 3 rows)
- *latent seed* `L-knowledge-ties-parts`: What ties the declarative and executive parts is knowledge: the program holds propositions and updates them by what it executes. (pasted, 2026-10-08, 2 rows)
- *latent seed* `L-realization-ideal-and-runner`: A realization is the ideal and what runs it, related by a law and a cost, with mutation and destruction as optimizations that keep the consequence and the host as a realization of the reduction rules. (pasted, 2026-10-08, 1 rows)
- *latent seed* `L-run-changes-states`: Running a function is modeled as changing the states of the program and the states of the universe (a written file, a printed line, a sent message), the universe's changes also following rules. (pasted, 2026-10-08, 3 rows)
- *latent seed* `L-trace-compare-consequence-cost`: run fills holes, reduces and leaves a trace, and two traces compare in two ways, by consequence as an equivalence and by cost as a partial order measured with its variance. (pasted, 2026-10-08, 1 rows)
- *latent seed* `L-laws-of-interpretation-steps`: Luthier should carry the laws of each interpretation step (reduce, apply), written in Luthier, so one can check that Luthier's precepts hold; with apply and reduce almost all of it is done. (model, 2026-10-08, 3 rows)
- *latent seed* `L-specs-in-luthier`: The aspiration is to write Luthier's own specifications in Luthier itself, the ideal to reach. (model, 2026-10-08, 2 rows)
- *latent seed* `L-abstract-machine-certify`: An abstract machine is an interpreter whose state is a datum, the most convenient way to certify one interpreter against another by comparing states step by step rather than only results. (model, 2026-10-08, 1 rows)
- *latent seed* `L-eval-modes`: You define a program and ask to execute/eval it under different modified evaluations (with test, with extensive test, copying everything that happens); having several execution modes is the attraction of such a language. (model, 2026-10-08, 3 rows)
- *latent seed* `L-agnostic-program-universe-state`: The language should not distinguish types that speak of the program's internal state from those that speak of the universe's state; the program should be agnostic. (Luciano, 2026-10-08, 2 rows)
- *latent seed* `L-when-to-evaluate`: An open question of evaluation strategy: for A=2+2 whether A is stored as 2+2 or as 4, since keeping the expression lets one recompute with different assumptions. (Luciano, 2026-10-08, 3 rows)
- *latent seed* `L-evaluation-steps-memory-states`: Evaluation is represented by the states of memory (2; 2+; 2+2; 4), possibly with pointers to a partially applied function, with syntax, range and type errors (arcsin of a string, a value out of range) caught along the way. (Luciano, 2026-10-08, 3 rows)
- *latent seed* `L-declarative-of-implementation`: Luthier needs a declarative description, written in Luthier, of its own implementation: how Luthier code transforms into execution code. (Luciano, 2026-10-08, 2 rows)
- *latent seed* `L-executive-code-in-luthier`: One must be able to write the executive code itself in Luthier. (Luciano, 2026-10-08, 1 rows)
- *latent seed* `L-reuse-prior-interpreter-experience`: He already built this kind of interpreter/compiler in C++ (MacroIR, Kimball) storing in virtual classes; the question is whether it makes sense to do it in Luthier instead of Python. (Luciano, 2026-10-08, 1 rows)
- *open tension* `L-start-easy-own-language`: One can implement Luthier inside a host language starting with the easiest 'kind of Luthier', or make it directly its own language. (Luciano, 2026-08-31, 2 rows)

## What Luthier is for: expressiveness, minimalism and its limits

Whether it adds real expressiveness, stays legible, is worth its cost, and where it begins to be useful.

- *seedling* `L-express-invariances`: Luthier's aim is to express the invariances of the disciplines (a species mates within itself; electrons are fermions, photons bosons). (Luciano, 2026-05-29, 7 rows)
- *seedling* `L-expressivity-vs-redundancy`: A choice between redundancy (robustness) and expressivity; he prefers expressivity with good compiler messages, since redundancy can needlessly limit. (Luciano, 2026-05-29, 6 rows)
- *seedling* `L-express-alternatives`: The point is not to do everything but to have the tools to express different alternatives; no option is best or worst, and even expressing something to discard it has value. (Luciano, 2026-05-29, 7 rows)
- *seedling* `L-is-it-a-dsl`: In implementation Luthier is a DSL in Python, and only a few things justify a separate language: the judgment that a value satisfies a type, the certificate as persistent composable evidence, the hole as a first-class citizen, environment independence, and a future fifth of proving rather than testing. (Luciano, 2026-09-30, 4 rows)
- *seedling* `L-own-contributions-vs-precedents`: Theory-with-equality, models as records and laws run as tests have precedents (Maude views, Lean structures, QuickCheck); three contributions are own (the cone-hash certificate, R10, the object as a strongly connected component). (model, 2026-10-05, 5 rows)
- *seedling* `L-spec-faster-than-use`: The specification moves faster than any use, so no program built on Luthier can stabilize. (pasted, 2026-10-05, 4 rows)
- *seedling* `L-novel-evidence-combination`: Luthier adds no new expressiveness over Lean or Agda; its novelty is the evidence regime that joins laws in types, sampling with named generators and statistical levels, hash-tied evidence, and results carrying which laws they rest on. (model, 2026-10-06, 7 rows)
- *latent seed* `L-expressiveness`: Code must express its intention to both the human reader and the compiler, referring truthfully to known structures. (Luciano, 2022-06-28, 2 rows)
- *latent seed* `L-abstraction-mechanism`: Luthier is an abstraction mechanism, a relator, for expressing ideas clearly (probability, sample, matrix, units, experiment). (Luciano, 2026-05-29, 3 rows)
- *latent seed* `L-minimalism-maximalism`: There is no contradiction between minimalism and maximalism: the minimalism is in the few founding components, from which a huge edifice of complex concepts is built. (Luciano, 2026-05-30, 3 rows)
- *latent seed* `L-language-of-ideas`: Luthier is a language for defining ideas, where ideas are first-class citizens, like natural languages define things. (Luciano, 2026-06-03, 3 rows)
- *latent seed* `L-living-vs-dead-language`: Luthier can be a living language that acts or a dead language that only describes; the descriptive role is where it starts. (Luciano, 2026-06-03, 2 rows)
- *latent seed* `L-accumulates-without-advancing`: Luthier keeps accumulating ideas without starting to advance, tending to grow to encompass the universe, attractive but like a bag of gas. (Luciano, 2026-09-02, 3 rows)
- *latent seed* `L-algebraic-and-semantic`: Luthier should have a very algebraic way of writing itself that can express almost anything like a universal Turing machine, yet where each element is semantically defined and understandable by humans. (Luciano, 2026-09-02, 3 rows)
- *latent seed* `L-must-be-useful`: Luthier must be useful and take root in something real, not stay purely theoretical, so it hits reality and reveals its limits. (Luciano, 2026-09-21, 2 rows)
- *latent seed* `L-gap-of-usefulness`: The method is to find the gap of usefulness, a concrete place from which Luthier can begin to develop while being useful. (Luciano, 2026-09-21, 3 rows)
- *latent seed* `L-luthier-v0-limits`: Luthier v0 cannot express expectations, certify a concrete run, or handle objects that are files, so stages that need those stay typed holes; that boundary is Luthier's limit, named as a gap in what was built. (model, 2026-09-30, 1 rows)
- *latent seed* `L-luthier-runs-and-tests`: Luthier both runs and tests, becoming the legible documentation of a Python project, with leaves in Python that iterate over data and composition in Luthier that iterates over concepts, so a program that runs is its documentation. (Luciano, 2026-10-03, 3 rows)
- *latent seed* `L-generated-code-not-real`: He is stuck because the model generates Luthier code that to him is not code, since he cannot tell whether it meets Luthier's real norms. (Luciano, 2026-10-03, 3 rows)
- *latent seed* `L-luthier-costs-more-than-returns`: As a design Luthier improved this week, but as a sonolocalización tool it today costs the project more than it returns. (pasted, 2026-10-05, 1 rows)
- *latent seed* `L-elegant-vs-mosaic`: A language is elegant when its constructions follow from one or two ideas and its self-interpreter fits a page, mosaic when each construction was added for a need; Luthier's spec is elegant but the interpreter has mosaic pieces the next round should remove. (model, 2026-10-06, 2 rows)
- *latent seed* `L-languages-from-theory`: Popular languages are not better founded; now that metatheory can be machine-verified an old language can end up better founded than a new one, and Luthier is on the side born from a theory. (model, 2026-10-06, 1 rows)
- *latent seed* `L-luthier-states-not-programs`: Luthier should be a language to state and certify the claims of a computation done in Python or R, not a language to program in. (model, 2026-10-06, 1 rows)
- *latent seed* `L-optimize-needs-strong-certificates`: Type, certification and measurement are one idea from three sides; optimizing over weak certificates is worse than not optimizing, so generators and certificate reach come before selection, which picks only among covering implementations and records the chosen one in each result's provenance. (model, 2026-10-06, 3 rows)
- *open tension* `L-delegate-execution`: Luthier might delegate execution entirely and do only verification, as extreme minimalism. (Luciano, 2026-05-27, 2 rows)
- *open tension* `L-what-is-it-for`: Open question of what Luthier is actually for; so far it is an intellectual adventure. (Luciano, 2026-08-31, 2 rows)
- *open tension* `L-arena-or-lambda-calculus`: Luthier can grow as a universal arena or, more simply, as a down-to-earth lambda calculus. (Luciano, 2026-09-02, 2 rows)
- *open tension* `L-luthier-fills-need`: Can Luthier fill an existing need and let one express things not expressible in other languages? (Luciano, 2026-10-06, 1 rows)
- *open tension* `L-functions-by-hand-cheaper`: Against his own argument: the same verified functions could be written by hand without the whole Luthier apparatus. (Luciano, 2026-10-07, 2 rows)
- *open tension* `L-monads-in-luthier-question`: Open doubt whether monads or functors must be writable in Luthier, as Haskell has them. (Luciano, 2026-10-07, 2 rows)

## Code as data and the self-interpreter

Homoiconicity, Term as a datum, eval, and Luthier operating on its own code.

- *seedling* `L-code-is-data`: Code is data, erasing the distinction between code and data, following the Lisp model. (Luciano, 2022-06-15, 13 rows)
- *seedling* `L-self-extensible`: Luthier must be completely self-extensible: you write all of Luthier in Luthier, so only a few primitives are actually implemented. (Luciano, 2026-05-29, 5 rows)
- *seedling* `L-meta-recursive`: The object of Luthier is to work on Luthier; being meta-recursive, operating on itself from the start, is fundamental. (Luciano, 2026-05-29, 9 rows)
- *seedling* `L-term-is-data-syntax`: Term is the type of Luthier's syntax defined in Luthier itself with data, one constructor per form of term (including one for data { ... }); code is a first element because syntax is a data like N, making the core self-verifying and metacircular. (model, 2026-09-28, 5 rows)
- *seedling* `L-eval-fuel`: eval repeating a step is not structural recursion and need not terminate, so it is given fuel, eval : N -> Program -> Term -> Maybe Term, making it total, and how much fuel was needed is the first cost measure for free. (model, 2026-09-29, 3 rows)
- *seedling* `L-environment-evaluator`: Luthier's evaluator should use environments and closures so each argument and constant is computed once (concepts are unique), replacing substitution which copies the body and recomputes multiply-used arguments. (model, 2026-10-02, 7 rows)
- *seedling* `L-bool-read-by-position`: Bool is read by position, so any sum of two Units counts as Bool with the first alternative true, and a predicate that always returns the wrong label passes. (model, 2026-10-05, 11 rows)
- *seedling* `L-two-evaluators-diverge`: There are two evaluators that differ in edge cases, and the machine silently falls back to the substitution one. (model, 2026-10-05, 4 rows)
- *latent seed* `L-code-operations`: The language builds in functions that operate on code: tests, errors, derivatives, finding equivalents, and timing. (Luciano, 2022-08-03, 2 rows)
- *latent seed* `L-function-holds-code`: A function holds its code written in the language plus a compiled simplified form. (Luciano, 2022-08-03, 1 rows)
- *latent seed* `L-language-self-writing`: Defining new types and functions should itself be programmable, the language writing itself, which requires a simple robust language with no syntactic sugar. (Luciano, 2022-08-03, 1 rows)
- *latent seed* `L-code-many-operations`: Luthier code is not merely compiled and run; many operations apply to it (verify, compile, run), giving more complexity but more expressivity. (Luciano, 2026-05-30, 2 rows)
- *latent seed* `L-code-enables-autodiff`: Code that represents the calculations can be autodifferentiated and yield a step-by-step written result. (Luciano, 2026-08-31, 1 rows)
- *latent seed* `L-bootstrap-pact`: The only thing outside Luthier is a bootstrap that accepts a Program value, parses it and runs eval; once eval written in Luthier runs on itself the bootstrapper can be discarded, which is the concrete self-extensibility. (model, 2026-09-28, 3 rows)
- *latent seed* `L-program-inductive-eval`: Code and data in the Lisp form: Program is an inductive type and eval a partial function Program → Name → Maybe Term, with no eval injecting arbitrary terms into the type system, which prevents self-hacking. (model, 2026-09-28, 2 rows)
- *latent seed* `L-unevaluated-is-syntactic`: "Unevaluated" is not a runtime state like a thunk because there is no time; it is a syntactic datum, which removes any lazy-evaluation semantics. (model, 2026-09-29, 1 rows)
- *latent seed* `L-term-untyped-check`: Term is untyped syntax (senseless terms are constructible) and whether a term has sense is decided by check; a Term admitting only well-typed terms exists but is much harder, so raw syntax plus check suffices to start. (model, 2026-09-29, 2 rows)
- *latent seed* `L-check-infer-bidirectional`: check traverses the definitions verifying each type is a type and each body has its declared type, infer computes the type by recursion over Term, and real verifiers are bidirectional, which is where refl types or not. (model, 2026-09-29, 1 rows)
- *latent seed* `L-reduction-three-rules`: A reduction step has three rules, beta (substitute a lambda), delta (unfold a definition) and iota (run the recursor); the order of the clauses is the evaluation strategy, and another choice gives another trace for the same result. (model, 2026-09-29, 1 rows)
- *latent seed* `L-substitution-capture`: Substitution has a variable-capture problem; the cheap by-hand fix is requiring all bound names distinct and the serious fix is de Bruijn indices (var : N -> Term for bound variables). (model, 2026-09-29, 2 rows)
- *latent seed* `L-definition-form-depends-on-type`: The form of a definition, how its clauses are written, may depend on reducing its type, the same definitional equality at work. (model, 2026-09-29, 2 rows)
- *latent seed* `L-stuck-not-fail`: A match on a pair with a free component must get stuck rather than fail so that normalizing a law with quantified variables terminates, with unfolding only saturated calls closing the other termination hole. (model, 2026-09-30, 1 rows)
- *latent seed* `L-checker-richer-presentation`: The checker may keep its richer presentation for speed, like Lean's kernel/elaborator split, provided its Term-to-core translation is written. (model, 2026-10-04, 1 rows)
- *latent seed* `L-certification-forced-interpreter-rules`: Certifying real code forced several interpreter rules written into the spec (laws not quantified over unmentioned parameters, infinite-domain generators, tuple patterns, empty-matrix shape, lazy tables). (model, 2026-10-04, 1 rows)
- *latent seed* `L-right-association-bit-equality`: Summation and the product of types associate to the right, like the tuple, which is what enabled bit-for-bit equality. (model, 2026-10-04, 2 rows)
- *latent seed* `L-slow-nested-op-inference`: Loading anything importing array.lut takes ~17-19s because each nested + or * re-infers the left operand's type. (model, 2026-10-05, 1 rows)
- *latent seed* `L-conversion-syntactic-no-dependent-elim`: Conversion is syntactic on neutral terms and there is no dependent elimination, so a type error becomes a pending obligation. (model, 2026-10-05, 1 rows)
- *latent seed* `L-hardwired-names-interpreter`: There are hardwired names in the interpreter, so Fin is recognized only by name and an alias of Fin loses its array representation and memoization. (model, 2026-10-05, 1 rows)
- *latent seed* `L-order-is-confluence`: Evaluation order is free for pure terms by confluence (Church-Rosser), not by purity, so the order is a strategy and a parameter, not a truth. (model, 2026-10-08, 2 rows)

## Numbers: Real, Float64 and intervals

Writing numeric code over the ideal reals and realizing it in approximations with a stated law.

- *seedling* `L-start-from-reals`: Start from the ABC: numbers, the reals, their operations, and a concept of error of the reals. (Luciano, 2026-05-29, 2 rows)
- *seedling* `L-properties-within-error`: The properties a function must satisfy (like an inverse recovering the value) hold only within a certain error. (Luciano, 2026-08-31, 4 rows)
- *seedling* `L-fin-int-vs-machine`: Fin n is semantically the finite set over ℤ; a machine integer is not another definition of Fin but a representation of a subset of ℤ, written as two presentations with an equivalence law. (Luciano, 2026-10-04, 4 rows)
- *seedling* `L-reals-theory-rationals-float-models`: Separate ℝ as a theory with no finite implementation, ℚ as an exact computable model, and Float64 as a model of the rounded field tied to ℚ by a correct-rounding law testable in ℚ. (model, 2026-10-04, 15 rows)
- *seedling* `L-write-over-real-approximate-with-float`: The numeric code is written once over Real, which has the better properties, and Float64 (or intervals, or Rational) is one of its approximations, so f(Real) is approximated by f(Float64). (Luciano, 2026-10-04, 3 rows)
- *seedling* `L-comparisons-undecidable`: Moving off a fixed Float64 makes comparisons undecidable in general (a branch on overlapping intervals has no answer), the most delicate point, met by making decision stability a law. (model, 2026-10-04, 5 rows)
- *seedling* `L-nan-inf-not-reals`: Since Float64 is a Real, NaN and overflow to infinity are always errors, and a meaningful infinity is requested in the type via ExtendedReal. (Luciano, 2026-10-04, 3 rows)
- *seedling* `L-real-realized-by-float64`: Real is not implemented but delegated to Float64, which realizes it at runtime as an interpreter choice recorded in the certificate. (Luciano, 2026-10-04, 4 rows)
- *seedling* `L-leaf-declared-over-float64`: An extern leaf is declared over what it really receives and returns (Vec Float64, not Real), since the type cannot affirm what the implementation does not deliver, forcing libraries generic in the number type. (Luciano, 2026-10-04, 4 rows)
- *seedling* `L-function-subtyping-float64`: The function subtyping rule (domain contravariant, codomain covariant) accepts the argument and promotes the Float64 a leaf returns to Real, with an explicit toFloat64 where a Real must be rounded. (Luciano, 2026-10-04, 4 rows)
- *seedling* `L-real-only-a-label`: Real exists only at type-checking with no representation or generator and arithmetic over it rejected; the libraries are Float64 end to end, so the distinction yields nothing today. (model, 2026-10-05, 6 rows)
- *seedling* `L-int-tables-as-float`: Fin n -> Int tables are generated as float64 against spec 06, so integer laws over indices run with floating-point division. (model, 2026-10-05, 2 rows)
- *seedling* `L-interval-arithmetic-bounded-real`: Interval arithmetic fits Luthier because its correctness is a single inclusion law Luthier can already certify: a bounded Real is a certificate carried across a computation that yields a bound for a function's values. (Luciano, 2026-10-05, 2 rows)
- *latent seed* `L-code-obeys-laws-not-floats`: Floating-point numbers do not obey the algebraic laws of numbers, but the code is assumed to, so it can be reorganized for efficiency. (Luciano, 2026-08-31, 2 rows)
- *latent seed* `L-approxring-eps`: Floats are not a ring but satisfy the laws of a distinct subtype with a tolerance parameter eps in the type, and the exact ring is that subtype at eps=0 rather than an independent definition. (model, 2026-09-30, 2 rows)
- *latent seed* `L-no-exact-equality-floats`: == does not decide over floats or arrays; comparison is an approximate relation with a tolerance (tolOf n = 8 n eps, the slack declared once). (model, 2026-10-02, 1 rows)
- *latent seed* `L-reals-with-without-zero`: Division by zero leads to two distinct types, the reals with zero and the reals without it. (Luciano, 2026-10-03, 3 rows)
- *latent seed* `L-int-real-string-primitive`: Int, R and String are an unavoidable exception as core primitives, since defining IEEE double with data makes no sense. (model, 2026-10-04, 1 rows)
- *latent seed* `L-int-overflow-numpy-bridge`: Int in the interpreter is unbounded ℤ (Python int) but becomes int64 on crossing to numpy with no check, a silent-overflow source the spec and bridge must name. (model, 2026-10-04, 3 rows)
- *latent seed* `L-algebra-chooses-number-object`: Rather than rewrite floating-point arithmetic, use algebra to choose the mathematical object that best represents the reals. (Luciano, 2026-10-04, 2 rows)
- *latent seed* `L-distinguish-reals-from-float-subtype`: Distinguish R, the set of reals, from the Python-implemented subtype (real/Float64), being precise about which is which. (Luciano, 2026-10-04, 2 rows)
- *latent seed* `L-float64-refines-real`: Float64 is written as a refinement of the real type (Float64 : Real := primitive), each finite double being a real. (Luciano, 2026-10-04, 3 rows)
- *latent seed* `L-constructive-reals`: Define the reals constructively as Cauchy sequences of rationals with a modulus of convergence, making ℝ's laws testable at finite precision and equality a precision parameter. (model, 2026-10-04, 2 rows)
- *latent seed* `L-name-real`: Name the real type Real rather than R. (Luciano, 2026-10-04, 2 rows)
- *latent seed* `L-interval-enclosure-law`: With an interval model the approximation law is stated once for any f as enclosure (f_Float64 x ∈ f_Interval x), so the tolerance is computed in test rather than chosen by hand. (model, 2026-10-04, 2 rows)
- *latent seed* `L-number-theory-record`: Numeric code is written once over a theory of numbers, a record with carrier, operations and equality; Real is its ideal model and Float64, intervals, Rational are others, filled through a per-file hole as in the ML functor. (model, 2026-10-04, 2 rows)
- *latent seed* `L-real-carrier-plus-axiom`: Real is written as carrier plus structure, Real := primitive and realField : CompleteOrderedField Real := axiom, where axiom is a value whose laws are assumed. (model, 2026-10-04, 3 rows)
- *latent seed* `L-indexat-nat`: An index typed Int admits negatives and makes an obligation genuinely false, so the honest type for an index is Nat. (model, 2026-10-05, 3 rows)
- *latent seed* `L-tolerance-checks-dont-compose`: Checks with a tolerance do not compose, since a near b and b near c do not give a near c at the same tolerance, so if used to refine, the tolerance must go in the type. (model, 2026-10-05, 1 rows)

## Errors as data and the certificate

Failure as a predicate that fails, structured error trees, and the certificate as composable graded evidence.

- *seedling* `L-test-result-one-or-explanation`: A check returns success (one) if met or an explanation of why it failed, not just a boolean. (Luciano, 2022-08-03, 7 rows)
- *seedling* `L-error-is-failing-predicate`: An error is a predicate that fails, represented by a single recursive type Failure, a tree of label, argument and sub-failures whose labels are quotes of program terms, the same structure as the success certificate, which only a language where code is data can build. (Luciano, 2026-09-30, 4 rows)
- *seedling* `L-content-hash-certificate`: Content-addressed build: a definition's certificate carries a hash of its elaborated type and body (and its dependency cone), so a matching hash on import satisfies the obligation, files are the source of truth and a relational DB is a reconstructible index. (model, 2026-09-30, 4 rows)
- *seedling* `L-cert-hash-misses-python`: The certificate hash covers only the extern's text, not the Python source, generator, case count or interpreter version, so editing lm.py leaves the certificate current. (model, 2026-10-05, 9 rows)
- *seedling* `L-certs-on-holes-never-match`: Certificates depending on holes never match because the hash is compared at import before the parent fills the holes but was computed after. (model, 2026-10-05, 3 rows)
- *seedling* `L-stale-certificates-not-pruned`: Certificate entries only accumulate and old ones are never pruned, so reading the file one cannot tell current from obsolete without recomputing the hashes. (model, 2026-10-05, 3 rows)
- *seedling* `L-certificate-is-only-a-record`: The certificate neither enables nor blocks anything, it is only a record, so the word certificate is excessive. (model, 2026-10-05, 4 rows)
- *seedling* `L-hash-compared-after-holes-filled`: Certificate hashes are compared at the end of loading with the holes filled, a library with holes being a structure with parameters whose laws are certified per filling. (model, 2026-10-05, 5 rows)
- *seedling* `L-interpreter-hash-recertify-cost`: Including the interpreter's fingerprint in the hash means any interpreter fix invalidates every certificate, forcing recertification in batches. (model, 2026-10-05, 4 rows)
- *seedling* `L-cert-guarantees-via-typed-externs`: A certificate now guarantees something because every value returned from Python is read by its declared type, and the certificate hash covers the Luthier code, the Python behind each extern and the interpreter. (model, 2026-10-05, 3 rows)
- *seedling* `L-knowledge-vs-certificate`: Certified is knowledge not a state of the name, so the record splits into knowledge (the posterior over a model's behavior given prior, model class and evidence, joined across runs) and certificate (a decision for a use, a query over that knowledge that must not write the posterior's mode as a fact). (model, 2026-10-08, 4 rows)
- *latent seed* `L-proof-capsules`: Local safety containers (ScientificSafe<T>, Maybe_error<T>) are validity capsules wrapping high-risk regions. (model, 2025-06-18, 3 rows)
- *latent seed* `L-error-messages-remembering`: Luthier must produce well-structured error messages, the remembering of why one erred, returning the failed sub-graph with each node's trace. (model, 2026-06-26, 3 rows)
- *latent seed* `L-certificate-first-class`: The certificate is a first-class value carrying its level of guarantee, composable and forgettable, accumulating by composition across values, functions and programs, with runs persisted as data. (model, 2026-09-29, 3 rows)
- *latent seed* `L-certificate-clause-with-hypotheses`: A certificate is a clause with hypotheses (H1 and ... and Hn imply L), and a program's certificate is the closure of those clauses, which gives composition its exact meaning. (model, 2026-09-29, 1 rows)
- *latent seed* `L-explicit-error-types`: Errors should be explicit types rather than Maybe_error over a string, and the error sum E1+E2 is an ordinary type the verifier computes, neither dynamic nor dependent, with Maybe_error being the maximally forgotten Failure. (Luciano, 2026-09-30, 4 rows)
- *latent seed* `L-possible-vs-occurred-error`: Distinguish the type of error that can occur (computed before running, linear in the chain, small) from the error that occurred (computed at run time, a datum with variable structure). (model, 2026-09-30, 1 rows)
- *latent seed* `L-iteration-propagation`: Data-length iteration (MCMC and the like) is the common case, and what must be designed is its three forms of propagation, cut at first fail, accumulate, and decorate, with the forget functor keeping the decoration from overwhelming the value. (Luciano, 2026-09-30, 2 rows)
- *latent seed* `L-certification-is-pointwise`: What is certified is not a name but a pointwise application of it on values (a chain of functions), so there are grades: point, sampled, exhaustive, proven, a chain at its weakest link. (Luciano, 2026-10-04, 3 rows)
- *latent seed* `L-run-record-omits-uncertified-cone`: Spec 05 asks the run record to note the uncertified names of the cone, but the CLI saves only entry, hash, when, parameters and result. (model, 2026-10-05, 1 rows)
- *latent seed* `L-cert-grades-not-implemented`: The certificate grades spec 05 promises (point, witnessed, assumed, weakest link of a chain) are not implemented. (model, 2026-10-05, 2 rows)
- *latent seed* `L-certification-impl-broken`: The certification machinery does not do what spec 05 promises (failing certs, stale ones, generators ignoring refinements, what runs not what was certified) and should be fixed before the next library rewrite. (model, 2026-10-05, 3 rows)
- *latent seed* `L-certifying-algorithm-witness`: A certifying algorithm returns its result plus a witness a simple checker verifies, the refined value being the special case where the witness is the value itself, giving in general a dependent pair with a law. (model, 2026-10-05, 1 rows)
- *latent seed* `L-monad-vs-applicative-validation`: A monad stops at the first failure (fit for a pipeline) while validating by hand wants the full list of violations (an applicative that accumulates errors), and the context decides between the two. (model, 2026-10-05, 2 rows)
- *latent seed* `L-run-inputs-vs-cert-reach`: A run's inputs are compared against the reach of the certificates: what arrives via --set at startup, and what is computed during the run only under --checked. (model, 2026-10-05, 1 rows)
- *latent seed* `L-full-to-unprovable`: What distinguishes Luthier is carrying types-as-propositions a full to propositions that cannot be proved, so the grade of verification must be part of what belonging to a type affirms. (model, 2026-10-06, 2 rows)
- *latent seed* `L-three-kinds-of-proposition`: A certificate is a proposition with its evidence, and propositions are of three kinds (a timeless law, a trace fact never revised, a statement about the world that ages), every chain of evidence ending in laws assumed. (pasted, 2026-10-08, 2 rows)
- *latent seed* `L-keep-witness-high-information`: Since these functions are expensive, keep the witness that a function worked or failed, giving priority to high-information values far from the prior (the unexpected ones). (model, 2026-10-08, 3 rows)

## Probability, Bayes and statistical verification

Marrying types with probability: laws with costs, posteriors over behavior, and verification as a Bayesian observer.

- *seedling* `L-probabilistic-hott`: Proving path equivalence needs a probabilistic extension of HoTT, a marriage of HoTT and Bayes, with an internal prover plus empirical statistical demonstration. (Luciano, 2026-05-29, 10 rows)
- *seedling* `L-nonunivocal-functions`: The language must natively model non-univocal functions, functions with error, samples. (Luciano, 2026-05-29, 4 rows)
- *seedling* `L-uncertainty-functor`: Uncertainty is a functor decorating a value such as position with a prior or credibility interval, with five forms differing in how exact the functor is and what they lose, a distribution over a grid proposed as canonical and the type parameterized by the functor to avoid duplication. (Luciano, 2026-09-30, 4 rows)
- *seedling* `L-failure-mass-sampling`: What n passing sampled cases update is the failure mass theta under the usage distribution, not the law's truth, with a Beta prior giving Beta(a,b+n), theta of order 1/n, composing by union bound and transferring between uses through the saved posterior. (model, 2026-10-08, 4 rows)
- *seedling* `L-search-vs-cost-split`: Searching where a law fails and weighting where it costs are distinct, the Use / TestPlan split, so search-generator cases inform theta only with importance weights and the generator must declare its density. (model, 2026-10-08, 4 rows)
- *seedling* `L-use-as-plan-element`: Use enters the plan as a timeless element, a distribution over inputs, a loss over the law's residual and a decision criterion, with the certificate indexed by model, theory, use and prior and test taking a use whose generator is the distribution component. (model, 2026-10-08, 4 rows)
- *seedling* `L-type-parametrized-by-use`: A type can be parametrized by its conditions of use and environment: a cost of failure varying by situation and a prior probability of each parameter combination occurring, which need only be expressible now. (model, 2026-10-08, 5 rows)
- *seedling* `L-law-as-object-classifier`: A law need not return Bool: its codomain can be an object classifier with an order and a 'holds' element (a quantale Omega, the positive reals as a cost, or the universe U of evidence types), the theory being the sublevel set under a threshold and Bool the case {0,infinity}. (Luciano, 2026-10-08, 11 rows)
- *latent seed* `L-express-extracomputational`: The language expresses extra-computational concepts like probability by abstracting their properties and verifying compliance (e.g. a probability lies in [0,1]). (Luciano, 2022-06-28, 1 rows)
- *latent seed* `L-sample-probability-duality`: Sample and probability form a duality, with tests demonstrating it holds. (Luciano, 2022-06-28, 1 rows)
- *latent seed* `L-separate-structure-inference`: Deterministic structural validity (via HoTT) is kept separate from probabilistic inference (via Bayesian layers), probability handled downstream. (model, 2025-06-17, 2 rows)
- *latent seed* `L-bayesian-mapping`: Scientific knowledge production is mapped into explicit Bayesian structures (introduction to prior, methods to likelihood, results to observations, discussion to posterior) to make reasoning auditable and probabilistic. (model, 2025-06-17, 3 rows)
- *latent seed* `L-hott-not-probabilistic`: HoTT does not work on probabilities, though probabilities could be built within it; the defect is that it is not native. (Luciano, 2026-05-30, 1 rows)
- *latent seed* `L-probabilities-and-types-together`: Probabilities and types should go almost together, the equivalences being probabilistic, with HoTT giving the universe over which the probabilities apply. (Luciano, 2026-05-30, 3 rows)
- *latent seed* `L-statistical-law-over-sample`: A distribution defect like a biased generator is invisible to any per-case quantified law and needs a law over the whole sample with a probabilistic verdict, the statistical Bayes layer. (model, 2026-09-30, 1 rows)
- *latent seed* `L-discrete-output-distribution`: When a probabilistic path makes the output discrete (a rank, stop reason, count), the result type must be able to say it is a distribution over outcomes. (model, 2026-10-04, 2 rows)
- *latent seed* `L-bayesian-verification-regime`: Verification is read as a Bayesian observer updating what it knows by what it observes, with proof, exhaustive and assumed at the logical limit of probabilities 0 and 1 and sampling where the rest enters. (pasted, 2026-10-08, 3 rows)
- *latent seed* `L-cost-laws`: Laws could be extended to go not to a boolean but to a cost: graded cost laws like a generalized unnormalized likelihood, asking how much a value costs rather than whether it complies. (model, 2026-10-08, 5 rows)
- *latent seed* `L-discrepancy-threshold-cost`: A law computes a discrepancy, the theory sets the threshold that makes it Bool, and the use sets the cost, so the theory stays independent of the use. (model, 2026-10-08, 2 rows)
- *latent seed* `L-posterior-per-computation`: With this bayesian logic any computation in Luthier carries a posterior of how sure you are of that computation. (model, 2026-10-08, 3 rows)
- *latent seed* `L-sup-not-sampleable`: A law's for-all in [0,infinity] is a sup that a sample bounds only from below, the mathematical reason sampled testing cannot certify a universal law and why the use is needed, replacing the sup by an expectation against the usage distribution. (model, 2026-10-08, 2 rows)
- *latent seed* `L-object-classifier-laws`: Luthier has a kind of object classifier: predicates about types that are the laws, the names. (Luciano, 2026-10-08, 1 rows)
- *latent seed* `L-function-as-expected-loss`: What is left of a function is an expected loss, a posterior characterization that must be processable, expressible as a type of generator, test and cost. (Luciano, 2026-10-08, 2 rows)
- *latent seed* `L-combine-evidence-refine-certainty`: Combine different evidences, different programs running the same function, to refine the certainty in that function. (Luciano, 2026-10-08, 1 rows)
- *latent seed* `L-analysis-only-at-moments`: The whole verification apparatus is expensive parafernalia layered on top, so one must be able to say it runs only at some moments, not always. (Luciano, 2026-10-08, 1 rows)
- *open tension* `L-hott-prob-tension`: There is a tension between HoTT's invertible identities and univalence and probability's non-invertible uncertainty, with no fully unified model yet. (model, 2025-06-17, 3 rows)

## The external world, extern and orchestration

The read/write boundary to C++, Python and resources, and how Luthier delegates execution.

- *seedling* `L-io-codec-prism`: Luthier separates the IO effect (a law-less extern) from the format, a pure codec of parse and render with round-trip laws, which is a prism, the partial version of Iso. (Luciano, 2025-09-28, 6 rows)
- *seedling* `L-hijack-code`: Luthier must be able to hijack code from any other language. (Luciano, 2026-05-29, 4 rows)
- *seedling* `L-core-plus-libraries`: Luthier is a closed core plus libraries, the libraries being Luthier functions that connect it to external programs. (Luciano, 2026-05-29, 2 rows)
- *seedling* `L-closed-observer`: Luthier is a closed, internally complete universe that observes the outside through a read/write boundary which is also a compilation. (Luciano, 2026-05-29, 5 rows)
- *seedling* `L-luthierize-foreign-code`: Luthier annotates and 'luthierizes' foreign code, verifying it against the definition of what it should do within some error. (Luciano, 2026-08-31, 4 rows)
- *seedling* `L-delegate-representation-python`: Luthier expresses the concepts and delegates the representation to Python, with a compiler generating the Python representation now written by hand (the chosen way being to load the .lut at import rather than compile to files), the generated code never edited and carrying the .lut's hash. (Luciano, 2026-09-30, 7 rows)
- *seedling* `L-luthier-types-python-values`: Luthier provides only the types with their postconditions and laws; the values are external, instantiated extern in Python, and no extern is declared U. (Luciano, 2026-10-02, 10 rows)
- *seedling* `L-pure-interface-files`: Pure .lut files declare carriers and operations without bodies (like C++ pure virtual classes but with verified laws and concrete definitions on the leaves), and a separate Python-linking file fills each hole, while real.lut keeps its externs as the environment layer. (Luciano, 2026-10-02, 5 rows)
- *seedling* `L-extern-provisional-qualifier`: A qualifier (extern provisional) lets an extern stand over a not-yet-defined type in a rush, recording the debt in the certificate. (Luciano, 2026-10-04, 4 rows)
- *seedling* `L-extern-gives-value-not-type`: An extern always gives a value, never a type (pyTable : Table .= extern, not Table := extern); when a Python value represents a native type the boundary is a certified representation translation. (Luciano, 2026-10-04, 5 rows)
- *seedling* `L-bridge-ignores-declared-type`: The Python bridge turns any int, float or str into a literal regardless of the declared type, and division follows the Python type, so an Int disguised as Float64 gives integer division. (model, 2026-10-05, 5 rows)
- *seedling* `L-provisional-externs-certified`: Provisional externs are certified although R5 forbids it, and the certificate carries no provisional field. (model, 2026-10-05, 5 rows)
- *seedling* `L-validate-bridge-first`: Validating everything crossing from Python and --set against the declared type, including codomain refinements, is the only fix that can prevent a wrong number with no warning and so comes first. (model, 2026-10-05, 4 rows)
- *latent seed* `L-external-element`: Everything that is not Luthier (C++, Python, the machine, any resource) is modeled as its own kind of external element. (Luciano, 2026-05-29, 3 rows)
- *latent seed* `L-run-external-programs`: Luthier needs a built-in facility to run external programs and compilers easily. (Luciano, 2026-05-30, 2 rows)
- *latent seed* `L-library-adapter`: A library is used by requiring it follow patterns and satisfy propositions defined from Luthier, with an adapter fitting it to each use, so Luthier acts as a universal adapter between libraries. (Luciano, 2026-09-02, 3 rows)
- *latent seed* `L-extern-is-labeled-hole`: extern is a hole with a label saying who fills it, the border between what runs and what does not, possibly an ordinary library function rather than a keyword. (model, 2026-09-30, 1 rows)
- *latent seed* `L-opaque-type`: A large machine value like a numpy array enters Luthier as an opaque extern type whose values pass through untouched; such values have no equality, and comparing them is a function to R with tolerance. (model, 2026-09-30, 2 rows)
- *latent seed* `L-invert-arrow-registration`: Invert the arrow so the .lut declares a hole with its signature and the environment (sonolik) fills it by registration, instead of signatures coming from what Python already has. (model, 2026-09-30, 2 rows)
- *latent seed* `L-types-native-values-either`: Types are defined natively, while the values (executable functions) may be native or not, admitting both, since only the dubious part is worth reimplementing. (Luciano, 2026-10-04, 2 rows)
- *latent seed* `L-synthesize-python-call`: Luthier should synthesize the call to a Python function using Luthier syntax, so one can work in layers more outward or more inward of Python. (Luciano, 2026-10-07, 2 rows)
- *latent seed* `L-effects-as-threaded-pointers`: The external world is a type that exists and nothing constructs, with no equality, whose values are pointers externs give, threaded linearly so their order lives in the graph of definitions and a reused pointer is a type error. (pasted, 2026-10-08, 3 rows)
- *latent seed* `L-exterior-is-files`: What is outside Luthier is largely files (executables, Python code, data, plots, even sensors), plus mutable memory, resources and processors. (model, 2026-10-08, 4 rows)

## The construction pattern: certified subtype and Library

Deriving a certified type, its validating constructor and its forgetful projection from a material type and a predicate.

- *seedling* `L-subtype-by-predicate`: A subtype (subObject) is the subset of a type whose values satisfy a predicate, a test. (Luciano, 2022-08-03, 10 rows)
- *seedling* `L-unit-is-group-of-functions`: The unit of definition is not a function with a postcondition but a group of functions with the laws relating them; a single function is the group of size one. (model, 2026-09-29, 10 rows)
- *seedling* `L-concept-is-a-function`: A concept needs no new type: it is an ordinary function returning a type (with proofs) or a list of laws (with tests). (Luciano, 2026-09-29, 6 rows)
- *seedling* `L-almacen-is-constructor-function`: A structure like Almacen is a function that takes the raw operations and returns the verified versions, so the only way to obtain one is to pass the check. (Luciano, 2026-09-29, 4 rows)
- *seedling* `L-construction-pattern-is-core`: The core of Luthier is one construction pattern: from a material type and a predicate over it derive a certified type, a validating constructor and the forgetful projection to the material, the same for values, functions and whole programs. (Luciano, 2026-09-29, 9 rows)
- *seedling* `L-name-the-pattern-library`: The verification structure the pattern builds is named Library, not Luthier the language; an instance is a program that passed its tests and can show it, so the adjective tested is superfluous. (Luciano, 2026-09-29, 5 rows)
- *seedling* `L-set-builder-notation`: The single subtype form is set-builder notation { pattern : material | predicate }, which denotes a Sigma; mainstream languages omit it because deciding the predicate needs a solver, a proof or a runtime check, and Luthier's fourth way tests it with n cases recorded in the certificate. (model, 2026-09-29, 9 rows)
- *seedling* `L-file-is-sigma-value`: A .lut file denotes a value of a Sigma type with named components like Ring, so a library's signature is its type, two interchangeable libraries are two values of one type, and a parametrized library is a module-to-module function. (model, 2026-09-30, 1 rows)
- *seedling* `L-object-is-record-type`: An object is always a record type including its carrier, defined by its laws; implementations are its values, so there is never more than one body per name and translations always work. (model, 2026-10-04, 4 rows)
- *latent seed* `L-reject-material-name`: The base of the construction pattern should not be called 'material', which hides what matters; it only makes sense if functors are applied over it, and English mathematical names like ring or field should be used. (Luciano, , 1 rows)
- *latent seed* `L-concept-is-predicate-over-functions`: A concept is a predicate over functions, a list of requirements, so two implementations satisfying it are interchangeable. (model, 2026-09-29, 2 rows)
- *latent seed* `L-no-value-without-passing-check`: There is no way to hold a value of a subtype without its predicate having been evaluated or proved; the check runs when the value is built. (model, 2026-09-29, 3 rows)
- *latent seed* `L-laws-are-the-normal-form`: The novelty is that a group of functions with its laws, as a type whose laws are run by default, is the normal way to define anything, not a separate verification tool. (model, 2026-09-29, 3 rows)
- *latent seed* `L-luthier-is-verified-library`: Luthier itself is a series of verified types and functions with their theorems and tests, almost an instance of the pattern. (Luciano, 2026-09-29, 2 rows)
- *latent seed* `L-units-with-parametrizable-requirements`: No language ships units that carry a set of requirements they must satisfy; in Luthier the predicate is a function with parameters (max error, scalability), so the certificate states which parameters are met and a dependent library inherits them. (Luciano, 2026-09-29, 2 rows)
- *latent seed* `L-luthier-is-extended-concepts`: Luthier is C++ concepts extended to the whole language: predicates with semantic requirements that are run and whose results are stored, keeping subsumption and composition. (Luciano, 2026-09-29, 2 rows)
- *latent seed* `L-predicate-concatenation`: Predicates concatenate two ways: conjunction where both pass, and refinement where the second is defined over the subtype the first carves and the order is forced. (model, 2026-09-29, 1 rows)
- *latent seed* `L-candidate-named-not-forall`: The candidate value is named and the laws applied to it explicitly, but it has the material's type (naming it by the subtype is circular) and needs no forall; the sample size is certificate data, not part of the type. (Luciano, 2026-09-29, 2 rows)
- *latent seed* `L-type-three-uses`: A type's one piece of information is used for three purposes, typing (a judgement), constructing, and asking as a predicate; only the third exists for subtypes, is what Luthier adds, and leaves a certificate, with construction being asking and packaging. (Luciano, 2026-09-29, 3 rows)
- *latent seed* `L-base-vs-predicate-line`: The distinction between a base type and a predicate is structural, but where the base ends and predicates begin is a design decision that decides what is computation and what is data. (model, 2026-09-29, 1 rows)
- *latent seed* `L-object-has-head`: Every object has a head: a type whose body names its laws, so there are no free-standing laws that define. (model, 2026-10-04, 2 rows)
- *latent seed* `L-opaque-body-is-law-conjunction`: The body of an opaque type is the conjunction of the laws over it and its operations (Table := NonNegative & Reflexive & IntColumn); an operation the laws do not name stays outside the cycle. (model, 2026-10-04, 3 rows)

## Purpose, meaning and motivation

What Luthier is for and why to build it: recovering meaning under AI, platforms, epistemics, biology.

- *seedling* `L-encode-epistemic-structure`: Scientific code should encode its epistemic structure as executable epistemology, with verification semantic rather than syntactic and type safety arising from epistemic clarity. (model, 2025-06-18, 5 rows)
- *seedling* `L-language-for-the-ai`: Luthier should be a language used by the AI itself, with the risk that it self-hacks. (model, 2026-06-28, 4 rows)
- *seedling* `L-sharing-platform`: Luthier is a platform where sharing your information makes you win, because you learn where you stand relative to the rest. (Luciano, 2026-08-28, 5 rows)
- *seedling* `L-things-guaranteed`: Luthier's purpose is better error management and things guaranteed, because having a type means satisfying certain propositions. (Luciano, 2026-08-31, 5 rows)
- *seedling* `L-certificates-enable-autonomy`: Luthier's mechanical certificates and file-held state let the AI work sustainedly through the night and across context compaction, since a pass/fail certificate makes it prudent to run the check and continue. (Luciano, 2026-10-05, 7 rows)
- *latent seed* `L-remaking-foundations`: He has re-made the language many times, each time rethinking the foundations of programming more deeply. (Luciano, 2022-06-15, 1 rows)
- *latent seed* `L-code-to-understand`: He codes to understand, which means being able to manipulate the code and see how changes affect its observables. (Luciano, 2022-06-28, 1 rows)
- *latent seed* `L-machine-verifiable-theories`: HoTTification offers a path toward machine-verifiable biological theories. (model, 2025-06-17, 1 rows)
- *latent seed* `L-meta-theory-discovery`: The final product is a meta-theory of scientific discovery architecture, a unifiable theory-building system, not just new models. (model, 2025-06-17, 2 rows)
- *latent seed* `L-reproducibility-formal`: The reproducibility crisis is a lack of structural verification, and reproducibility is a formal property. (model, 2025-06-18, 2 rows)
- *latent seed* `L-language-is-universe`: Inventing a programming language is like inventing a universe with its own laws. (Luciano, 2026-05-29, 3 rows)
- *latent seed* `L-optimize-own-rules`: Since he invents the language it follows his rules, so he can optimize the rules to make manipulating programs easy. (Luciano, 2026-05-29, 2 rows)
- *latent seed* `L-von-neumann-epigraph`: Luthier's founding epigraph is Von Neumann's: state exactly what a machine supposedly cannot do and he will build a machine that does it. (Luciano, 2026-06-03, 3 rows)
- *latent seed* `L-publish-arxiv`: Publish Luthier's first result the way physicists do, on arXiv, and let it spread. (Luciano, 2026-06-05, 1 rows)
- *latent seed* `L-build-before-it-falls`: Luthier must be built now, before access to highly qualified AI guidance becomes restricted. (Luciano, 2026-08-28, 1 rows)
- *latent seed* `L-correlated-data-worth-more`: Correlated data are worth more than isolated data, and larger patterns need ever more data. (Luciano, 2026-08-28, 2 rows)
- *latent seed* `L-recover-meaning-as-ai-codes`: Since the AI now writes all the code, Luthier is the way to recover contact with meaning and have things guaranteed without looking at the code. (model, 2026-08-31, 2 rows)
- *latent seed* `L-language-indicates-knowledge`: Luthier is thought of as a language that indicates knowledge, in Martin-Löf's reading where a judgment is an act of knowledge and the bodyless hole is an epistemic assumption. (Luciano, 2026-09-29, 3 rows)
- *latent seed* `L-chain-interpretable-steps`: The AI generates so much output that the only workable way to use it is to chain steps whose result you can interpret. (Luciano, 2026-10-07, 1 rows)
- *latent seed* `L-language-forces-method`: Luthier's relevance is forcing the author and the AI to be methodical, and a program that compiles gives some assurance it is not garbage, by analogy with Lean's proofs. (Luciano, 2026-10-07, 2 rows)
- *latent seed* `L-computation-for-biology`: His student intuition and life's aim is that computation could play for biology the role mathematics played for physics. (Luciano, 2026-10-08, 1 rows)
- *open tension* `L-intermediate-ai-scale`: Is there an intermediate scale where the AI multiplies the author's effort without the result ceasing to be legible and checkable by him? (Luciano, 2026-10-07, 2 rows)

## Concrete syntax and notation

The surface forms: binders, symbols versus keywords, the dot, quotes, and reading the language aloud.

- *seedling* `L-dot-separator`: The dot in Σ (x : X). A x is a notational separator marking where the bound variable ends and the body begins, the same dot as in λ and Π, like the brace in f(x) { ... }, and one convention should serve all three binders. (Luciano, 2026-09-29, 4 rows)
- *seedling* `L-symbol-economy`: A symbol is used only for what appears often with a fixed universal meaning and already exists outside with it; anything rare, content-bearing or without a natural reading is a word, since the language is read aloud and written by hand. (model, 2026-09-29, 4 rows)
- *seedling* `L-ergonomics-let-unary-minus`: Writing costs for lack of let, implicit arguments and unary minus (functions end in ten closing braces), which should come before any kernel refinement. (model, 2026-10-05, 7 rows)
- *latent seed* `L-composition-dot`: Composition is written with a dot, which explains class methods. (Luciano, 2022-08-03, 1 rows)
- *latent seed* `L-well-defined-dsl`: The DSL and the way code is written must be very well defined. (Luciano, 2026-05-29, 2 rows)
- *latent seed* `L-python-spirit`: Luthier imitates Python's spirit of expressing human ideas easily (with the Monty Python / Luthier wordplay). (Luciano, 2026-09-02, 2 rows)
- *latent seed* `L-syntax-declarations-instantiations`: Luthier's syntax is reduced to only declarations and instantiations. (Luciano, 2026-09-29, 2 rows)
- *latent seed* `L-block-is-program`: Braces delimit a block that can hold local definitions; a block is a Program with one definition marked as output, giving local definitions without new primitives. (model, 2026-09-29, 1 rows)
- *latent seed* `L-no-parameterless-lambda`: A parameterless lambda should not exist: without time or effects \ () { a + a } and a + a are the same value, a consequence of the commutativity of statements. (model, 2026-09-29, 2 rows)
- *latent seed* `L-one-binding-form`: One binding form name : Type appears identically in declaration, parameter, dependent type and pair, with A -> B sugar for (_ : A) -> B and the dot disappearing. (model, 2026-09-29, 2 rows)
- *latent seed* `L-separate-type-from-term`: The notation f : A -> A := \ (x) { x + x } separating type from term is preferred: instantiation is declaration plus := term, with one way to build functions (the lambda) and one to write their type (the arrow). (model, 2026-09-29, 2 rows)
- *latent seed* `L-juxtaposition-application`: Application is written by juxtaposition f a and binds tighter than any operator, so f(a) is the same, f a b is curried and f (a, b) applies to a pair, the two coexisting as distinct types, with multiplication explicit. (model, 2026-09-29, 3 rows)
- *latent seed* `L-lisp-quote-code-as-data`: Writing f a as data within a program uses the Lisp quote '(f a) as sugar, with the parser producing the Term constructors. (model, 2026-09-29, 4 rows)
- *latent seed* `L-sugar-adds-no-term-constructor`: Sugar may add nothing to Term: a construct that forces a new Term constructor is a primitive to discuss, not sugar. (model, 2026-09-29, 2 rows)
- *latent seed* `L-ascii-canonical`: The canonical form of the language is ASCII; an editor may display -> as an arrow or * as a cross, but what is run by hand and grepped is the ASCII. (Luciano, 2026-09-29, 2 rows)
- *latent seed* `L-predicate-delimiter-syntax`: How to mark where a subtype's predicate begins: the bar is overloaded, so use a dedicated form rather than overload it further. (Luciano, 2026-09-29, 2 rows)
- *latent seed* `L-dot-projection`: Since a subtype's component names are public, a field is read with dot notation e.position, pure sugar over a match on the pattern the type declares that needs no new Term constructor and resolves root-level projection name collisions. (Luciano, 2026-10-01, 3 rows)
- *latent seed* `L-parser-leniency`: What the parser rejects does not matter unless there are weighty theoretical reasons. (Luciano, 2026-10-02, 1 rows)
- *latent seed* `L-implicit-type-params`: Implicit type parameters are deduced by unification at application, so an unannotated lambda is checked after deducing its type from the other argument. (model, 2026-10-05, 2 rows)
- *latent seed* `L-el-reading`: El abbreviates elements: El c reads as the elements of what the code c names. (Luciano, 2026-10-06, 2 rows)
- *latent seed* `L-el-vs-typeof-naming`: typeOf would mislead since typeOf c means Code, not the type c names; for Luthier the decoder is named Decode, pairing with Code. (Luciano, 2026-10-06, 2 rows)
- *latent seed* `L-define-bnf-task`: The concrete task is to understand Luthier's syntax and keep a well-defined BNF. (Luciano, 2026-10-07, 2 rows)

## Dependent types and the HoTT foundation

Which type-theoretic foundation Luthier maps onto and what it provides.

- *seedling* `L-based-on-hott`: Build Luthier to map strictly onto homotopy type theory, with very few types following its small set of well-defined rules. (Luciano, 2026-05-29, 5 rows)
- *seedling* `L-dependent-types-as-type-returning`: A dependent type is a function that returns a type instead of a value, raising the level of abstraction. (Luciano, 2026-05-29, 6 rows)
- *latent seed* `L-dependent-types-def`: Dependent types are types that depend on a value, taking the cardinality of that value's type. (Luciano, 2022-06-28, 1 rows)
- *latent seed* `L-dep-types-composition`: Hierarchical, algebraic model composition across subunits, pathways and scales is enforced by dependent types. (model, 2025-06-17, 3 rows)
- *latent seed* `L-hott-dsl-for-biology`: Build a domain-specific modeling language on Homotopy Type Theory for expressing, composing and transforming biological models with access to type-level structure. (model, 2025-06-17, 2 rows)
- *latent seed* `L-hott-ingredients-sufficient`: Sigma-types, Pi-types, identity types and HITs suffice to encode conformational models, energetic couplings and symmetry structures. (model, 2025-06-17, 2 rows)
- *latent seed* `L-models-as-well-typed-objects`: Biological models are well-typed objects where types are molecular states, identity paths are symmetries, and composition emerges from dependent type operations. (model, 2025-06-17, 2 rows)
- *latent seed* `L-types-spaces-identities-paths`: HoTT gives types as spaces and identities as paths, its internal equality replacing ad hoc isomorphisms. (model, 2025-06-17, 2 rows)
- *latent seed* `L-higher-paths-symmetries`: Higher-order symmetries and transformations between equivalences are captured as higher paths. (model, 2025-06-17, 2 rows)
- *latent seed* `L-hottification-definition`: HoTTification is transforming a scientific model, algorithm or modeling language into a formal structure governed by HoTT, analogous to categorification or quantization. (model, 2025-06-17, 3 rows)
- *latent seed* `L-hottification-models-typed-objects`: Under HoTTification models themselves become typed mathematical objects whose equivalences, symmetries and compositions are validated by the type system. (model, 2025-06-17, 2 rows)
- *latent seed* `L-semantic-zones-kernel`: A type-theoretic HoTT kernel provides a formal model/inference algebra plus constructible semantic zones for safety. (model, 2025-06-18, 2 rows)
- *latent seed* `L-universal-type`: A universal type comprising the types of all dimensions, like an abstract class, taken as a feasible coding challenge. (Luciano, 2026-05-29, 3 rows)
- *latent seed* `L-dependent-types-basic`: Dependent types are probably one of the language's basic initial concepts. (Luciano, 2026-05-30, 1 rows)
- *open tension* `L-foundation-choice`: Open question of which foundation to build on (type theory vs category theory, HoTT vs ZMT). (Luciano, 2022-06-28, 2 rows)

## The forget functor and the typing-load problem

Controlling the typing information that grows as types compose; forgetting as a projection that defines the language.

- *seedling* `L-forgetting-problem`: The forgetting problem, controlling the typing information that grows as types compose, is one of Luthier's fundamental problems to solve. (Luciano, 2026-05-29, 4 rows)
- *seedling* `L-simplify-type-composition`: Simplifying the composition of dependent types needs a simplifying typing algebra, not a free monoid, that keeps the resulting type's complexity bounded; a key engineering problem. (Luciano, 2026-05-29, 7 rows)
- *seedling* `L-forgetful-functors`: Which forgetting function you apply to the types defines the language you speak; forgetful functors are among Luthier's most important components, and different ones optimize different things. (Luciano, 2026-05-29, 24 rows)
- *seedling* `L-type-is-history`: What a type holds is the history of how you arrived at it (e.g. a loop as a combination of types with an exponent). (Luciano, 2026-05-29, 4 rows)
- *seedling* `L-commuting-squares`: Coherence of forgetting and applying functions is analyzed with commuting squares: the two paths are compared for equivalence. (Luciano, 2026-05-29, 7 rows)
- *seedling* `L-forgetting-affects-precision`: How much of the operational history is kept determines the recoverable numerical precision, tying the forget functor to precision. (Luciano, 2026-08-31, 1 rows)
- *latent seed* `L-summary-bigger-than-data`: A model or summary can end up bigger than the data it summarizes. (Luciano, 2026-05-27, 1 rows)
- *latent seed* `L-typing-accumulates`: Composing dependent functions accumulates a growing typing load, so the decoration can end up far bigger than the value. (Luciano, 2026-05-29, 2 rows)
- *latent seed* `L-truncation-operators`: The programmer could use homotopy truncation operators to clean a complex type. (model, 2026-05-29, 2 rows)
- *latent seed* `L-patterns-in-composition`: When functions are associative you can find patterns in the composition, such as a loop as a series of functions raised to a power. (Luciano, 2026-05-29, 2 rows)
- *latent seed* `L-forgetting-in-hott`: The concept of forgetting (a type forgetting parts of the type) is already present in HoTT. (Luciano, 2026-05-30, 2 rows)
- *latent seed* `L-execution-as-forgetting`: Execution is a forgetful function: code generates code, with one level that keeps the generated code and one that forgets it. (Luciano, 2026-08-31, 3 rows)
- *latent seed* `L-forgetting-is-fst`: Forgetting is fst of a Σ, and what to forget is library policy. (model, 2026-09-28, 2 rows)
- *latent seed* `L-know-that-vs-which`: The distinction to keep is knowing that (a mere proposition's proof) versus knowing which (a set's value); the passage from the second to the first is truncation, the most basic forgetting, where the forget functor begins. (model, 2026-09-29, 2 rows)

## The derivation store and provenance

Storing derived objects as proof terms with their inputs, never edited, cumulative.

- *seedling* `L-records-as-relational-db`: What a record is can be stored as a relational database: fields, relations, a record being a subset of the cartesian product with duplicates removed. (Luciano, 2026-06-05, 4 rows)
- *latent seed* `L-apply-luthier-to-[private word]`: Luthier's concepts (function plus version, a table of functions) are carried into the design of the analysis/derivation store. (Luciano, 2026-09-13, 1 rows)
- *latent seed* `L-result-type-closed`: Each function declares a result type with fixed fields; the set of result types is open but every individual type is closed, a sum of types, not a JSON blob. (Luciano, 2026-09-13, 2 rows)
- *latent seed* `L-derived-is-proof-term`: A derived object, the tuple of inputs, function, parameters and result, is a proof term whose type is the proposition that the result was obtained that way, making the base a store of proofs. (model, 2026-09-13, 1 rows)
- *latent seed* `L-schema-from-type`: The storage schema is generated from the function's declared type rather than written by hand, and migration is derived. (model, 2026-09-13, 1 rows)
- *latent seed* `L-original-vs-derivative-types`: Some types are original (made from audios and questionnaires) and all the rest are derivative, results of functions, so they necessarily have structure. (Luciano, 2026-09-13, 3 rows)
- *latent seed* `L-derived-never-edited`: A derived object is never edited; corrections are human assertions that are themselves originals, putting labels, quality control and corrections in the same place. (model, 2026-09-13, 1 rows)
- *latent seed* `L-function-deterministic`: If the identity of a derived object is its inputs, function, version and parameters, the function must be deterministic: seed and environment enter as explicit arguments, or the certificate lies. (model, 2026-09-13, 1 rows)
- *latent seed* `L-evaluation-storage-object`: The object storing a function, its argument and its result is the graph of evaluation (Ev f), with a sugar that evaluates and stores it; evalstore is just that pair, not a third operation, and the run base is a list of them. (Luciano, 2026-09-29, 6 rows)
- *latent seed* `L-ev-sugar-syntax`: The sugar that stores an evaluation needs delimiters and always stores, since the context cannot decide its type and keeping only failures is the test's filter, not a property of the evaluation. (Luciano, 2026-09-29, 3 rows)
- *latent seed* `L-cumulative-no-recompute`: Luthier is cumulative, never computing the same thing twice except on an explicit override, with knowledge accumulating, perhaps in a relational database. (Luciano, 2026-09-30, 2 rows)
- *latent seed* `L-files-as-interface`: What remains after running are files and pdfs, and the human interface is reading comprehensible files, perhaps json. (Luciano, 2026-09-30, 1 rows)
- *latent seed* `L-validate-at-frontier`: What is reusable is the format every conversion must reach, not the per-experiment conversion; the throwaway script stays outside Luthier and its only contract is that its output passes the schema, validated at the frontier. (Luciano, 2026-10-03, 2 rows)
- *latent seed* `L-no-pdfs-doi-link`: No PDFs or books are committed to git; the DOI is the pointer to each source, so for sources the repository points instead of containing. (Luciano, 2026-10-08, 1 rows)

## The code universe and reflection

A closed Tarski universe of codes so generators and generic functors can be written in Luthier.

- *seedling* `L-russell-plus-tarski-library`: Keep Russell's U for everything and add a small closed Tarski universe of codes as a library for what must be treated generically. (model, 2026-10-06, 2 rows)
- *seedling* `L-russell-vs-tarski-universe`: A Russell universe is open (an element of U is a type, match can't be exhaustive) while a Tarski universe is a closed inductive data of codes over which match by induction is available. (model, 2026-10-06, 3 rows)
- *latent seed* `L-generic-functor-in-interpreter`: Generic functors live in the interpreter, derived from the type's structure as == already is, named and recorded in the certificate but not written in Luthier. (model, 2026-10-05, 2 rows)
- *latent seed* `L-generic-functor-needs-reflection`: Generators as values and generics as functors over the type contradict, since a functor over any type would need (T:U)->Gen T and reflection over types, which Luthier lacks. (model, 2026-10-05, 2 rows)
- *latent seed* `L-luthier-reflection-question`: Luciano challenges the claim that Luthier has no reflection over types. (Luciano, 2026-10-05, 2 rows)
- *latent seed* `L-code-universe`: A data Code describes the type shapes that can be generated, El decodes each to a type, and the functors become ordinary Luthier functions over codes. (model, 2026-10-05, 2 rows)
- *latent seed* `L-typecase-breaks-parametricity`: A match over types would break the parametricity on which proving a generic law in one instance rests. (model, 2026-10-05, 2 rows)
- *latent seed* `L-u-no-elimination`: The universe U has introduction (every type is a value of U) but an empty elimination column: a function can use a T:U but cannot match on its shape. (model, 2026-10-05, 2 rows)
- *latent seed* `L-code-el-induction-recursion`: Code and El are defined mutually (induction-recursion), which in Luthier's vocabulary is a cycle, i.e. an object. (model, 2026-10-06, 2 rows)
- *latent seed* `L-code-fixpoint-constructors`: Recursive types are described with var and mu constructors as a fixpoint, with strict positivity holding for free because Code has no arrow with var on the left. (model, 2026-10-06, 2 rows)
- *latent seed* `L-code-universe-staged`: Implement the code universe in stages: first codes without mu (numbers with bounds, products, sums, vectors, refinements), adding mu with Boltzmann sampling when a recursive data needs generating. (model, 2026-10-06, 2 rows)
- *latent seed* `L-fixpoint-generation-cost`: Generating a value of a fixpoint needs termination control: the cost is the size and the per-size counts come from the code without looking at a value, under the same accumulated-cost rule as numbers and censuses. (model, 2026-10-06, 1 rows)
- *latent seed* `L-code-universe-requirements`: The code universe asks of Luthier mutual definition of Code and El, large elimination, and dependent pattern matching, so R11 is its prerequisite. (model, 2026-10-06, 2 rows)
- *latent seed* `L-signature-shows-parametricity`: With both universes a signature carries what it can do: (A:U)-> is parametric and cannot inspect A, (c:Code)-> may inspect the code's shape, and a typecase over U breaks parametricity silently. (model, 2026-10-06, 2 rows)

## Constructors, recursors and data mechanics

How data declarations give types, constructors and recursors, and how match derives from them.

- *seedling* `L-data-sum-of-products`: A data is a sum of products plus recursion (sum between constructors, product inside each, recursion as least fixpoint), so data is primitive and + and × are its degenerate cases. (model, 2026-09-28, 4 rows)
- *seedling* `L-data-gives-recursor`: A data declaration gives three things: the type, the constructors (ordinary bodyless functions in normal form), and the recursor (one case per constructor with a reduction rule each); every function over the type is an instance of this recursor. (model, 2026-09-29, 8 rows)
- *seedling* `L-constructors-are-generator`: Presenting a type by constructors tied to observers by laws (algebraic ADT spec) makes the constructors the generator, so gen comes free from composing them; without constructors there are no completeness cells. (model, 2026-10-04, 6 rows)
- *seedling* `L-sufficient-completeness`: Aim at sufficient completeness (a law per observer-constructor cell plus extensionality), which the checker verifies mechanically, rather than minimality of laws. (Luciano, 2026-10-04, 3 rows)
- *latent seed* `L-constructor-vs-function`: A constructor differs from a function in that a constructor plus its parameters is the element, making elements transparent, while a function involves a computation. (Luciano, 2022-08-03, 1 rows)
- *latent seed* `L-constructors-in-type-space`: Constructors should live in each type's space rather than in the global space. (Luciano, 2022-08-03, 1 rows)
- *latent seed* `L-type-definition-recursive`: A type's definition is necessarily recursive, since the type must be universally accessible like identifiers. (Luciano, 2022-08-03, 1 rows)
- *latent seed* `L-sum-types-with-bar`: Types are expressed as alternatives with a bar, as in maybe, either and sum. (Luciano, 2022-08-03, 2 rows)
- *latent seed* `L-next-recursor-syntax`: What to attack next, in order: choose the recursor (without the dependent one there are no general paths proven by induction), then the concrete syntax. (model, 2026-09-28, 2 rows)
- *latent seed* `L-indexed-data-families`: Indexed constructors whose return type carries an index (Vec : N -> U) are a further layer of data, letting a type like Traza t u have constructors only for pairs that really reduce to one another. (model, 2026-09-29, 1 rows)
- *latent seed* `L-match-is-recursor-sugar`: match is not primitive but sugar for the recursor a data declaration gives, the only way to open a data value, and over Bool it is if. (Luciano, 2026-09-29, 3 rows)
- *latent seed* `L-constructors-freely-generated`: Constructors of an inductive type are freely generated with no equations, so the Peano disequalities (disjoint, succ injective, succ n distinct from n) are free theorems that survive without definition. (Luciano, 2026-10-04, 3 rows)
- *latent seed* `L-recursor-in-core`: Whether the recursor is a core primitive: keep it as it is already implemented, versus the core having data, match and general recursion with the recursor of each type being a library definition. (Luciano, 2026-10-04, 3 rows)

## Equality: definitional, propositional and levels

The distinct equalities and the levels of equivalence the language expresses.

- *seedling* `L-equality-symbols`: Equality gets distinct symbols: := defines (an asymmetric act), = is the identity type (the proposition), == is library decidable equality, and ≡, the definitional one, is not written in programs. (model, 2026-09-29, 5 rows)
- *seedling* `L-equality-parametrized-probability`: Objects are parametrized by observational equality and eventually by a probability of being equal or distinct, where equality returns a verdict with its level rather than a Bool. (Luciano, 2026-10-04, 6 rows)
- *seedling* `L-equality-check-holes`: R8 has holes: == is accepted over data containing functions, over Real as float equality, and not checked past depth 20. (model, 2026-10-05, 6 rows)
- *latent seed* `L-equals-assertion`: The equals sign is an assertion that both sides are equal, also used for pattern matching when a symbol is unknown. (Luciano, 2022-08-03, 2 rows)
- *latent seed* `L-identity-paths-equivalences`: Identity paths represent structural equivalences between model entities. (model, 2025-06-17, 2 rows)
- *latent seed* `L-levels-of-equivalence`: A fundamental idea of Luthier is to express different levels of equivalence (same information, isomorphic, exactly equal, same memory location), each a different equivalence functor. (Luciano, 2026-05-30, 2 rows)
- *latent seed* `L-definitional-equality`: "True by definition" is definitional equality ≡ (two terms reducing to the same normal form), a judgment the reducer decides, distinct from =, the identity type whose terms are paths, making "the test is the code" literal. (model, 2026-09-28, 2 rows)
- *latent seed* `L-proposition-is-type-truth`: True/false is not Bool: a proposition is a type, true if it has a term; ⊤ and ⊥ are the extremes and Bool is a datum with two constructors. (model, 2026-09-28, 2 rows)
- *latent seed* `L-refl-checks-definitional`: To assert a definitional equality as a check in a program, write _ : a = b := refl, which types only if a ≡ b, so no extra symbol is needed, and this is what makes the test be the code itself. (model, 2026-09-28, 3 rows)
- *latent seed* `L-judgment-depends-on-type`: a : A is a judgment, not a proposition, and what it means depends on the kind of type A is (a mere proposition: A holds and a is how I know; a set: a is one of A's elements). (model, 2026-09-29, 2 rows)
- *latent seed* `L-coloneq-act-vs-equiv`: := is the act of giving a name a body, while ≡ is the larger relation that follows from all the := plus the computation rules (lambda substitution, recursor rules); "true by definition" broadly means true by unfolding and computing. (model, 2026-09-29, 2 rows)
- *latent seed* `L-equalities-should-be-setoid`: Loose equalities like BeliefFamily.same and Codec.eq should be Setoid instances. (model, 2026-10-05, 2 rows)

## Types as propositions that carry their laws

A type states the law its values satisfy, making type safety a consequence of semantic clarity.

- *seedling* `L-type-carries-its-laws`: A type (or function) carries, as a proposition, the law its values must satisfy. (Luciano, 2022-06-15, 9 rows)
- *seedling* `L-compile-time-prevents-invalid`: The type system prevents invalid models from being constructed, eliminating consistency violations at compile time before execution or inference. (model, 2025-06-17, 8 rows)
- *seedling* `L-contagiously-safe-dsl`: A compile-time safe model DSL whose safety is contagious, propagating through the system via the compiler, with backend codegen, as the endgame of HoTTification. (model, 2025-06-18, 5 rows)
- *seedling* `L-types-are-concepts`: Types are concepts, types as propositions, and types include functions and higher-order functions. (Luciano, 2026-05-26, 9 rows)
- *seedling* `L-function-by-properties`: A function can be defined by its properties, the propositions its inputs and outputs satisfy, not only operationally, keeping both. (Luciano, 2026-05-29, 4 rows)
- *latent seed* `L-reasoning-to-code-isomorphism`: There should be a one-to-one relation between reasoning and the flow of the code, so running the code verifies the reasoning. (Luciano, 2022-06-28, 1 rows)
- *latent seed* `L-dep-types-semantic-safety`: Dependent typing enforces semantic safety, guaranteeing the internal consistency of model compositions. (model, 2025-06-17, 2 rows)
- *latent seed* `L-runtime-vs-semantic-safety`: Runtime safety prevents crashes while semantic safety, a layer above runtime, prevents invalid models from existing at all. (model, 2025-06-17, 2 rows)
- *latent seed* `L-compiler-is-prover`: Letting functions return types makes the Luthier compiler a mathematical prover, so code and its proof become the same thing. (model, 2026-05-26, 2 rows)
- *latent seed* `L-implementation-of-concept`: A Luthier definition should determine uniquely that a concrete computation is an implementation of a concept (e.g. of matrices). (Luciano, 2026-05-29, 2 rows)
- *latent seed* `L-evidence-in-sigma`: Being more specific with types means types are data and knowledge about a value is carried as an evidence component in a Σ, marked erasable, but with the evidence sometimes written and kept and the erasable mark set by whoever defines. (model, 2026-09-29, 2 rows)

## The run database and its synthesis

Recording measured time and precision per run, generalizing it, and keeping it from growing monstrous.

- *seedling* `L-bayesian-complexity-estimate`: The a priori complexity of implementations is estimated by a Bayesian strategy: give chances to different algorithms, measure their actual times, and estimate from accumulated experience. (model, 2026-05-26, 8 rows)
- *seedling* `L-performance-database`: Luthier keeps a database recording, for each function, initial data, scale and algorithm, the measured time, precision and run characterization. (Luciano, 2026-05-26, 5 rows)
- *seedling* `L-computation-categories`: There are categories of computations that take the same time for different inputs, and these classes must be found so not every computation need be measured. (Luciano, 2026-05-26, 4 rows)
- *seedling* `L-generalize-database`: The performance database must be generalizable from point measurements to trends, e.g. estimating an empty cell from its row and column averages or something more sophisticated. (Luciano, 2026-05-26, 7 rows)
- *seedling* `L-self-estimation-functions`: The time- and precision-modelling functions are themselves written in Luthier and used by Luthier itself. (model, 2026-05-26, 5 rows)
- *seedling* `L-time-from-input-features`: Compute time is predicted from a simplification of the inputs (the most predictive features, e.g. a matrix's rows and columns); some functions are independent of their inputs. (Luciano, 2026-05-26, 5 rows)
- *seedling* `L-model-of-computation`: Luthier contains a model of computation that you keep testing and simplifying and must keep active, through selective forgetting or aggregation, justified by its use on a particular case. (Luciano, 2026-05-27, 4 rows)
- *latent seed* `L-learn-from-each-run`: From each run of the code something is learned, whether an implementation is correct or how fast it is. (Luciano, 2023-02-22, 1 rows)
- *latent seed* `L-synthesize-runs`: The accumulated run information must be synthesized over time so it doesn't grow monstrous and paralyzing. (Luciano, 2026-05-27, 2 rows)
- *latent seed* `L-collaborative-filtering`: Use matrix factorization / collaborative filtering to predict an algorithm's runtime on an input. (model, 2026-05-29, 1 rows)
- *latent seed* `L-synthesis-is-key`: Synthesizing information well is the key to the whole design. (Luciano, 2026-05-30, 1 rows)

## Program as DAG, commutativity and time

A program as an unordered set of definitions where temporality emerges from dependency.

- *seedling* `L-program-not-a-type-in-hott`: HoTT models functions and types but not a complete program (a set/series of expressions), a theoretical gap between the part and the whole. (Luciano, 2026-05-29, 7 rows)
- *seedling* `L-context-as-dag`: The program/context is modeled as a Directed Acyclic Graph of definitions where types depend on others, and operating on Luthier is combining DAGs via substitution. (Luciano, 2026-05-29, 15 rows)
- *seedling* `L-statements-commute`: Make statements commutative so their order doesn't change the result, with temporality reconstructed from causal type dependence, trading some expressivity. (Luciano, 2026-05-29, 7 rows)
- *seedling* `L-execute-when-defined`: Code is not executed until it is fully defined, so undefined dead code can sit there without bothering anyone. (Luciano, 2026-05-30, 2 rows)
- *latent seed* `L-luthier-is-assignments`: Luthier is a chain of assignments, each an identifier, an equals sign and an operation that creates the object. (Luciano, 2023-03-13, 2 rows)
- *latent seed* `L-commutative-program`: An open question is whether a Luthier program is commutative in the order of its statements, and how to model time/order; declarations can be near-commutative. (Luciano, 2026-05-29, 4 rows)
- *latent seed* `L-first-class-contexts`: The context could be treated as a type in itself, what theory calls first-class contexts. (model, 2026-05-29, 2 rows)
- *latent seed* `L-time-as-dependency`: Time, the order of things, is modeled as dependency between definitions, the mathematical way: if one thing depends on another there is a time. (Luciano, 2026-05-29, 3 rows)
- *latent seed* `L-compose-programs-harmonically`: The fundamental problem is how Luthier programs connect and expand one another so they grow harmonically, with incompatibilities possible. (Luciano, 2026-09-02, 3 rows)
- *latent seed* `L-do-as-data-dependency`: Haskell's do sequencing can be simulated as a data dependency (an output needing an input that doesn't exist yet), so do may not be strictly necessary. (Luciano, 2026-10-08, 2 rows)
- *open tension* `L-what-is-a-program`: The basic question of Luthier: what is a Luthier program, a map or a graph? (Luciano, 2026-09-02, 2 rows)

## Luthier as a higher-order cross-language orchestrator

A minimal bridge-language butler that coordinates other languages and their programs.

- *seedling* `L-cross-language`: Luthier is not tied to one language but a pseudo-language implementable across languages (cross-language, not cross-compiler), with its engine in one and PyLuthier/RLuthier/CLuthier transformable into one another. (Luciano, 2026-05-26, 10 rows)
- *seedling* `L-butler-orchestrator`: Luthier is a higher-order language, a butler that orchestrates other languages, runs programs, compares their outputs, and chooses where to run each computation. (Luciano, 2026-05-26, 7 rows)
- *latent seed* `L-dsl-as-model-compiler`: The DSLs are model compilers that translate high-level mechanistic specifications into executable, inferable structures. (model, 2025-06-17, 3 rows)
- *latent seed* `L-meta-layer`: The language sits as a meta-layer above the ConformationalModel DSL, MacroIR and Bayesian pipelines. (model, 2025-06-17, 2 rows)
- *latent seed* `L-dsl-kernel-yaml`: A DSL kernel gives a declarative model interface in YAML, isolating the model interface from the C++ internals. (model, 2025-06-18, 2 rows)
- *latent seed* `L-compose-programs`: Luthier composes the input and output of one program with another, chaining external programs. (Luciano, 2026-05-27, 1 rows)
- *latent seed* `L-bridge-language`: Luthier should be minimal, essentially a bridge language connecting other languages. (Luciano, 2026-05-27, 2 rows)
- *latent seed* `L-easy-delegation`: Delegation should be easy in Luthier, an idea he traces to Modelica. (Luciano, 2026-05-30, 2 rows)
- *latent seed* `L-map-to-other-languages`: Describe functions and equivalences and map them to other languages (C, C++, Java), not directly but by giving the tools for others to extend the translation. (Luciano, 2026-05-30, 1 rows)
- *latent seed* `L-knowledge-butler`: The ideal is to use Luthier alongside the AI as a kind of butler of knowledge. (Luciano, 2026-09-21, 2 rows)
- *latent seed* `L-passthrough-or-orchestrator`: Luthier can be a language the code passes through or an orchestrator pointing outward, and both are fine with passage between them. (Luciano, 2026-10-07, 2 rows)

## Path equivalence, implementations and optimization

Many implementations of one function, their equivalence, and choosing the best for a case.

- *seedling* `L-semantic-then-efficient`: Once semantic validity and equivalence are established, a clear slow algorithm can be replaced by an efficient equivalent one, enabling optimization. (Luciano, 2022-06-28, 6 rows)
- *seedling* `L-declarative-and-optimizer`: Luthier is at once a declarative language and an optimization tool: you declare what you want and it openly shuffles implementations, a map between a declarative language and an executive one. (Luciano, 2026-05-26, 9 rows)
- *seedling* `L-path-cost-estimate`: Each execution path carries an estimate of its characteristics: compute time above all, also error, memory, and where it runs. (model, 2026-05-26, 7 rows)
- *seedling* `L-paths-implementations`: One function can be implemented in many ways (paths), each with its own precision and speed, and the equivalence between implementations is seen through the paths. (Luciano, 2026-05-26, 13 rows)
- *seedling* `L-two-layers`: Luthier has two layers: a first of equivalences and verifiability, and a second that measures time, complexity, resources and success/failure and picks the faster of two equivalent paths. (Luciano, 2026-05-27, 3 rows)
- *latent seed* `L-compare-equivalent-paths`: Luthier compares two paths that do the same thing and determines they are equivalent, possibly with format-conversion stages at the start and end. (Luciano, 2026-05-27, 2 rows)
- *latent seed* `L-path-equivalence-core`: Path equivalence, proving that different implementations are equivalent, is Luthier's fundamental and hardest concept. (Luciano, 2026-05-29, 2 rows)
- *latent seed* `L-essential-vs-decoration`: Function equivalences separate what is essential (the equivalent) from what is decoration (efficiency, cost), the non-equivalent. (Luciano, 2026-05-30, 1 rows)
- *latent seed* `L-hot-values-paths`: Hot values open a larger universe of possible paths than ordinary values. (Luciano, 2026-05-30, 1 rows)
- *latent seed* `L-particle-filtering-paths`: The exponential explosion of the path space is handled by particle filtering: running several stochastic programs in parallel exploring different paths. (Luciano, 2026-05-30, 2 rows)

## Arrays and performance primitives

Vec and Mat as definitions whose fast implementations are externs certified against them.

- *seedling* `L-array-primitive`: Arrays (Vec, Mat) enter as a primitive certified by algebraic laws with generators, with accessors and tabulate so Python traverses while Luthier still sees values, the conceptual endpoint being a dimension-indexed Vec : Nat -> U. (Luciano, 2026-10-02, 6 rows)
- *seedling* `L-vec-is-function`: A Vec is a function from indices below n to R (VecOf n := Pi with subtype), with tabulate as constructor and at as observer, the list being another presentation, yet it feels almost primitive. (Luciano, 2026-10-04, 7 rows)
- *seedling* `L-semantic-vs-performance-primitives`: What makes Vec seem primitive is performance not semantics, separating semantic primitives (the core) from performance primitives (the externs certified against the definition). (model, 2026-10-04, 4 rows)
- *latent seed* `L-array-laws-missing`: array.lut uses the opaque Vec/at/tabulate pattern but the laws defining Vec are written nowhere, so numpy fills holes untied by any law, which R3 would reject. (model, 2026-10-04, 2 rows)
- *latent seed* `L-array-generic-element-type`: Array is generic in the element type with numeric operations over Real (Vec = Array Real), so index arrays become Array Int and writing it over Float64 would reglue definition to realization. (Luciano, 2026-10-04, 3 rows)
- *latent seed* `L-folds-are-monoid-fold`: The folds over Fin n (sumTo, totalDef, maxOver, forallBelow, listLength) are all the same monoid fold and should be one right-associated fold. (model, 2026-10-05, 2 rows)
- *latent seed* `L-materialization-cache-bug`: The materialization cache keyed only by id(f) returns incorrect results, a correctness bug not a performance one. (model, 2026-10-05, 1 rows)

## Environment, variables and memory

The early model of an environment that stores and retrieves variables by name.

- *latent seed* `L-environment-first-object`: The environment is the first object the language must define, since data is loaded into it. (Luciano, 2022-07-05, 1 rows)
- *latent seed* `L-environment-kinds`: There are simple environments (one value type, one identifier) and compound ones that admit multiple. (Luciano, 2022-07-05, 1 rows)
- *latent seed* `L-environment-resources`: The environment needs and manages resources (memory and compute) and function execution, a problem that ties to it but exceeds it (OS, compiler). (Luciano, 2022-07-05, 3 rows)
- *latent seed* `L-environment-stores-retrieves`: The environment is a map of definitions whose two mechanisms are storing and retrieving variables by name. (Luciano, 2022-07-05, 3 rows)
- *latent seed* `L-variable-is-fields`: A variable is a name, a memory address, a size and a type; the type contains the size and the name can be the address. (Luciano, 2022-07-05, 1 rows)
- *latent seed* `L-variable-not-know-environment`: A variable knows its name but should not know its environment, so its resource acquisition stays predictable. (Luciano, 2022-07-05, 1 rows)

## Objects as cyclic codependent definitions

Interdependent laws making a group of types one object, a cycle in the definition graph.

- *seedling* `L-simultaneous-definition`: When postconditions are interdependent, objects are defined together, in tuples with crossconditions, the one form of definition. (Luciano, 2023-02-22, 4 rows)
- *seedling* `L-coupled-functions-product`: When a law couples several functions, the material is their product and the pattern unpacks it to name each component, so the laws are written over named components. (Luciano, 2026-09-29, 4 rows)
- *seedling* `L-objects-are-cycles`: When the invariants of several definitions need each other they are a co-dependent object defined together in one simultaneous definition against a type that ties them with laws; objects are the cycles of the definition graph. (Luciano, 2026-10-02, 12 rows)
- *seedling* `L-genuine-dependence`: The predicates connecting a type's components must be genuinely dependent and non-separable; a fake f(x,y)=g(x) should not count, and a separability failure needs a witnessed verdict. (Luciano, 2026-10-04, 9 rows)
- *seedling* `L-laws-hypergraph-connected`: Connection is a property of the whole set of laws: the hypergraph of laws must be connected and cover all components. (model, 2026-10-04, 13 rows)

## Decorators, uncertainty functors and value annotations

Decorating a value with error, provenance or what is known about it, and the views one can take.

- *seedling* `L-decorator-algebra`: Decorators should be easy to express, and one asks whether composing them is associative or commutative, representing the simplest form when it is. (Luciano, 2026-05-29, 4 rows)
- *seedling* `L-levels-of-view`: From a series of operations one can take different views or levels: the magma, the result, the execution, the code. (Luciano, 2026-08-31, 5 rows)
- *latent seed* `L-decorators-error`: Decorators express the error of a number and its propagation (derivatives), as he did in C++ with templates. (Luciano, 2026-05-29, 3 rows)
- *latent seed* `L-value-carries-annotations`: A value carries an annotation of everything already known about its class. (Luciano, 2026-08-31, 1 rows)
- *latent seed* `L-value-knows-operation`: A value knows the concrete operation that produced it: the sum is the sum, not the generic magma operation. (Luciano, 2026-08-31, 2 rows)

## Early identifier and naming explorations

The 2022 ideas on identifiers as the human-machine dictionary and on names for dynamic objects.

- *latent seed* `L-identifiers-central`: Identifiers are central: a simple label recovers a complex object, the dictionary joining human and machine. (Luciano, 2022-06-15, 3 rows)
- *latent seed* `L-dynamic-naming`: For dynamically created types or functions, a name is really an address, so a generated numeric identifier suffices. (Luciano, 2022-08-03, 1 rows)
- *latent seed* `L-identifier-type-independent`: The identifier and the type are completely independent; the identifier is a fantasy name unknown until resolved. (Luciano, 2022-08-03, 1 rows)
