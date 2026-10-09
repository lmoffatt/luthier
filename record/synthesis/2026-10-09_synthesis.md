# Synthesis of Luthier's ideas, rules and principles, 2026-10-09

Written by `scripts/assemble_synthesis.py` (assemble_synthesis v1) for Luciano, from the night's outputs (plan:
`record/plan-synthesis-2026-10-09.md`). Every grouping, state, candidate and trace is a model's reading; who said each
idea and when comes from the rows. Nothing here is decided: the candidates have a `Mark:` line for you.

## Summary

- **Ideas.** 725 ideas in 33 themes; 226 seedling, 486 latent seed, 13 open tension. Largest themes: Sonolocalización: the inference application (54); Working method and the pipeline (54); Laws as predicates and verification by test (53); Generators and the quality of the sample (42); Mathematical structures, presentations and translations (36); The minimal kernel and its primitives (31).
- **Principles.** 10 candidates found blind from the ideas: new 9, extends 1, covered 0 against P1 to P14.
- **Rules.** 100 rules (58 of the specification, 42 decisions); 87 come from at least one idea, 13 from none.

## 1. The ideas, by theme

The full map, every idea with its state: `record/synthesis/2026-10-09_consolidate_lineages_v1_claude-code_opus.md`. Here each theme with its size;
under it every open tension, and at most 5 latent seeds, those you said first, earliest first.

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

### Sonolocalización: the inference application

The concrete case that drives Luthier: situated objects, MAP, likelihood, score identities and the sampler.

- *latent seed*: Writing Newton-Raphson with all its invariants typed is Luthier's first concrete application and toy model. (2026-06-05, `L-newton-raphson-toy-application`)
- *latent seed*: The whole thing is a graph with the situated-object types at the ends and inference running over the Python trace in the middle. (2026-09-30, `L-graph-ends-types-middle-trace`)
- *latent seed*: The MAP is tested with the likelihood as the likelihood is tested with the sampler, a closed chain where the algorithm produces a record and the test is a predicate over it. (2026-10-02, `L-mutual-test-chain`)
- *latent seed*: The MAP is assembled from a step function and an is_finished predicate via a generic iterate_until driver that separates algorithm from model, with an optimization module whose laws take the implementation as argument. (2026-10-02, `L-map-as-iterate`)
- *latent seed*: The Levenberg-Marquardt controls were excluded on purpose because they belong to this particular case. (2026-10-05, `L-lm-controls-excluded`)
- and 32 more latent seeds in the full map (31 first said by a model)

### Working method and the pipeline

How the work is organized: audios to ideas to spec, records, reviews, waterfall versus iteration, mechanical checks.

- *latent seed*: Before committing to tests, record snapshots and compare results outside the system to decide which tests to run. (2025-09-27, `L-snapshot-first`)
- *latent seed*: His method of thinking is to work out the reasonable version first, then look for the wild move. (2026-05-26, `L-reasonable-then-wild`)
- *latent seed*: A first task is to understand all the things Luthier currently groups together, to see which are functionally separable and which depend on which. (2026-05-27, `L-decompose-components`)
- *latent seed*: The first step is expressing concepts in Luthier with conceptual depth; the translation/implementation comes after. (2026-05-29, `L-concept-first`)
- *latent seed*: Fix Luthier's syntax and semantics on paper first, and only then implement it. (2026-06-03, `L-syntax-semantics-before-implementation`)
- and 40 more latent seeds in the full map (28 first said by a model)

### Laws as predicates and verification by test

Defining a function defines its test; laws are ordinary declarations, holes until checked.

- *latent seed*: Luthier must verify that a function is correct; verifiability, with equivalence, is a minimal element of the language. (2026-05-27, `L-verifiability`)
- *latent seed*: Compiling is checking whether the code holds incompatible things; unlike algebraic calculation, many programs should not compile, because that is how errors are caught. (2026-09-02, `L-compiling-detects-errors`)
- *latent seed*: The aim of the first version is to generate numeric tests, not to do propositional logic. (2026-09-29, `L-numeric-tests-not-logic`)
- *latent seed*: Functions need no self-knowledge; a law is an ordinary function to Bool and the label is put by the verifier level, which knows the whole program and runs test as an operation over Program. (2026-09-30, `L-functions-need-no-self-knowledge`)
- *latent seed*: The law wrapper is unneeded; & is conjunction of quantified predicates (X->Bool)->(Y->Bool)->(X*Y->Bool) applied to curried functions, so the law's name is already the quoted expression. (2026-09-30, `L-conjunction-of-predicates`)
- and 31 more latent seeds in the full map (27 first said by a model)

### Generators and the quality of the sample

How values of a type are produced for testing and what each certificate's reach then means.

- *latent seed*: A Domain is defined for each function argument so sets of arguments can be sampled from it. (2025-09-27, `L-argument-domains`)
- *latent seed*: A test is diagnostic only if a wrong version fails it, so negative controls (a case that must fail) are needed, since a law nothing exercises certifies nothing. (2026-10-02, `L-negative-controls`)
- *latent seed*: The most serious issue is that the whole generators plan is not implemented and may not even be specified. (2026-10-05, `L-generators-plan-not-implemented`)
- and 23 more latent seeds in the full map (23 first said by a model)

### Mathematical structures, presentations and translations

Expressing algebraic objects as types with laws, their several presentations, and certified translations between them.

- *latent seed*: A functor is read as an implementation and a natural transformation as translating one implementation into another. (2023-03-02, `L-functor-as-implementation`)
- *latent seed*: The basic elements are defined in category-theory style, functors from arrows, out of a few basal elements. (2026-05-30, `L-category-style-basics`)
- *latent seed*: A class should generate and carry its structure and give access to its records, rather than being a bare simple structure. (2026-06-05, `L-class-carries-structure`)
- *latent seed*: Some concepts can live independently of their container (like a mean) while others are intrinsically tied to one (like an iteration to its algorithm). (2026-06-05, `L-concepts-independent-or-tied`)
- *latent seed*: Luthier has to do with abstract algebra. (2026-08-28, `L-abstract-algebra`)
- and 17 more latent seeds in the full map (10 first said by a model)

### The minimal kernel and its primitives

What the few founding elements of the language are, from which everything else is built.

- *open tension*: Open question of how to express the type of a function such as write : a -> string. (Luciano, 2022-08-03, `L-function-type-expression`)
- *open tension*: Open question whether Luthier needs primitive functions or only coordinates external ones, keeping native components minimal, perhaps only identity and equality. (Luciano, 2026-05-27, `L-minimal-primitives`)
- *latent seed*: The language expresses and creates values, variables, types and functions uniformly, with their semantics. (2022-06-28, `L-create-objects-uniformly`)
- *latent seed*: A proposed set of primitive value types and primitive functions. (2022-06-28, `L-primitives`)
- *latent seed*: The semantics lives in its own universe, not that of C++, even while using C++ structures to express it. (2022-06-28, `L-semantics-own-universe`)
- *latent seed*: Functions are of two kinds: predefined and user defined. (2022-08-03, `L-function-kinds`)
- *latent seed*: Natural-language grammatical categories parallel programming constructs, a frame for choosing Luthier's primitives. (2026-05-29, `L-grammar-parallel`)
- and 16 more latent seeds in the full map (10 first said by a model)

### Declaration versus definition and the states of a type

Declared, defined, determined, certified; whether type and value are one scale.

- *latent seed*: Each element belongs to exactly one type but can serve to build many types. (2022-08-03, `L-element-belongs-one-type`)
- *latent seed*: A type or function can inject more than one identifier into the environment. (2022-08-03, `L-inject-multiple-identifiers`)
- *latent seed*: Types can be handled by autodetection. (2022-08-03, `L-type-autodetection`)
- *latent seed*: The type is deduced by type calculation, and a derived type larger than the parameter's type is flagged. (2023-03-02, `L-type-inference`)
- *latent seed*: Types can be defined implicitly, as the solution to a problem or the optimum of a function, rather than declared directly. (2026-05-29, `L-implicit-types`)
- and 15 more latent seeds in the full map (11 first said by a model)

### The declarative/executive split and realization

Separating the timeless plan from execution, the host as a realization, and writing the interpreter in Luthier.

- *open tension*: One can implement Luthier inside a host language starting with the easiest 'kind of Luthier', or make it directly its own language. (Luciano, 2026-08-31, `L-start-easy-own-language`)
- *latent seed*: The language has parts: a grammar with semantic rules and a front compiler to C++. (2023-02-22, `L-language-parts-compiler`)
- *latent seed*: Inspired by Modelica, Luthier separates the specification of a program from its implementation. (2026-05-30, `L-spec-without-implementation`)
- *latent seed*: Luthier's first stage is a language for describing the problem, the functions and the conditions under which they work, not for execution. (2026-05-30, `L-description-language`)
- *latent seed*: Execution in Luthier is the verification of equivalences, as mathematics does not execute but only verifies equivalences. (2026-05-30, `L-execution-is-verification`)
- *latent seed*: A .lut file declares its dependencies with import, which is the combinar operation (union of definitions rejecting conflicts), with a prefix form to disambiguate clashing names. (2026-09-30, `L-import-declares-dependencies`)
- and 19 more latent seeds in the full map (11 first said by a model)

### What Luthier is for: expressiveness, minimalism and its limits

Whether it adds real expressiveness, stays legible, is worth its cost, and where it begins to be useful.

- *open tension*: Luthier might delegate execution entirely and do only verification, as extreme minimalism. (Luciano, 2026-05-27, `L-delegate-execution`)
- *open tension*: Open question of what Luthier is actually for; so far it is an intellectual adventure. (Luciano, 2026-08-31, `L-what-is-it-for`)
- *open tension*: Luthier can grow as a universal arena or, more simply, as a down-to-earth lambda calculus. (Luciano, 2026-09-02, `L-arena-or-lambda-calculus`)
- *open tension*: Can Luthier fill an existing need and let one express things not expressible in other languages? (Luciano, 2026-10-06, `L-luthier-fills-need`)
- *open tension*: Against his own argument: the same verified functions could be written by hand without the whole Luthier apparatus. (Luciano, 2026-10-07, `L-functions-by-hand-cheaper`)
- *open tension*: Open doubt whether monads or functors must be writable in Luthier, as Haskell has them. (Luciano, 2026-10-07, `L-monads-in-luthier-question`)
- *latent seed*: Code must express its intention to both the human reader and the compiler, referring truthfully to known structures. (2022-06-28, `L-expressiveness`)
- *latent seed*: Luthier is an abstraction mechanism, a relator, for expressing ideas clearly (probability, sample, matrix, units, experiment). (2026-05-29, `L-abstraction-mechanism`)
- *latent seed*: There is no contradiction between minimalism and maximalism: the minimalism is in the few founding components, from which a huge edifice of complex concepts is built. (2026-05-30, `L-minimalism-maximalism`)
- *latent seed*: Luthier is a language for defining ideas, where ideas are first-class citizens, like natural languages define things. (2026-06-03, `L-language-of-ideas`)
- *latent seed*: Luthier can be a living language that acts or a dead language that only describes; the descriptive role is where it starts. (2026-06-03, `L-living-vs-dead-language`)
- and 12 more latent seeds in the full map (6 first said by a model)

### Code as data and the self-interpreter

Homoiconicity, Term as a datum, eval, and Luthier operating on its own code.

- *latent seed*: The language builds in functions that operate on code: tests, errors, derivatives, finding equivalents, and timing. (2022-08-03, `L-code-operations`)
- *latent seed*: A function holds its code written in the language plus a compiled simplified form. (2022-08-03, `L-function-holds-code`)
- *latent seed*: Defining new types and functions should itself be programmable, the language writing itself, which requires a simple robust language with no syntactic sugar. (2022-08-03, `L-language-self-writing`)
- *latent seed*: Luthier code is not merely compiled and run; many operations apply to it (verify, compile, run), giving more complexity but more expressivity. (2026-05-30, `L-code-many-operations`)
- *latent seed*: Code that represents the calculations can be autodifferentiated and yield a step-by-step written result. (2026-08-31, `L-code-enables-autodiff`)
- and 16 more latent seeds in the full map (16 first said by a model)

### Numbers: Real, Float64 and intervals

Writing numeric code over the ideal reals and realizing it in approximations with a stated law.

- *latent seed*: Floating-point numbers do not obey the algebraic laws of numbers, but the code is assumed to, so it can be reorganized for efficiency. (2026-08-31, `L-code-obeys-laws-not-floats`)
- *latent seed*: Division by zero leads to two distinct types, the reals with zero and the reals without it. (2026-10-03, `L-reals-with-without-zero`)
- *latent seed*: Rather than rewrite floating-point arithmetic, use algebra to choose the mathematical object that best represents the reals. (2026-10-04, `L-algebra-chooses-number-object`)
- *latent seed*: Distinguish R, the set of reals, from the Python-implemented subtype (real/Float64), being precise about which is which. (2026-10-04, `L-distinguish-reals-from-float-subtype`)
- *latent seed*: Float64 is written as a refinement of the real type (Float64 : Real := primitive), each finite double being a real. (2026-10-04, `L-float64-refines-real`)
- and 11 more latent seeds in the full map (10 first said by a model)

### Errors as data and the certificate

Failure as a predicate that fails, structured error trees, and the certificate as composable graded evidence.

- *latent seed*: Errors should be explicit types rather than Maybe_error over a string, and the error sum E1+E2 is an ordinary type the verifier computes, neither dynamic nor dependent, with Maybe_error being the maximally forgotten Failure. (2026-09-30, `L-explicit-error-types`)
- *latent seed*: Data-length iteration (MCMC and the like) is the common case, and what must be designed is its three forms of propagation, cut at first fail, accumulate, and decorate, with the forget functor keeping the decoration from overwhelming the value. (2026-09-30, `L-iteration-propagation`)
- *latent seed*: What is certified is not a name but a pointwise application of it on values (a chain of functions), so there are grades: point, sampled, exhaustive, proven, a chain at its weakest link. (2026-10-04, `L-certification-is-pointwise`)
- and 14 more latent seeds in the full map (14 first said by a model)

### Probability, Bayes and statistical verification

Marrying types with probability: laws with costs, posteriors over behavior, and verification as a Bayesian observer.

- *open tension*: There is a tension between HoTT's invertible identities and univalence and probability's non-invertible uncertainty, with no fully unified model yet. (model, 2025-06-17, `L-hott-prob-tension`)
- *latent seed*: The language expresses extra-computational concepts like probability by abstracting their properties and verifying compliance (e.g. a probability lies in [0,1]). (2022-06-28, `L-express-extracomputational`)
- *latent seed*: Sample and probability form a duality, with tests demonstrating it holds. (2022-06-28, `L-sample-probability-duality`)
- *latent seed*: HoTT does not work on probabilities, though probabilities could be built within it; the defect is that it is not native. (2026-05-30, `L-hott-not-probabilistic`)
- *latent seed*: Probabilities and types should go almost together, the equivalences being probabilistic, with HoTT giving the universe over which the probabilities apply. (2026-05-30, `L-probabilities-and-types-together`)
- *latent seed*: Luthier has a kind of object classifier: predicates about types that are the laws, the names. (2026-10-08, `L-object-classifier-laws`)
- and 12 more latent seeds in the full map (9 first said by a model)

### The external world, extern and orchestration

The read/write boundary to C++, Python and resources, and how Luthier delegates execution.

- *latent seed*: Everything that is not Luthier (C++, Python, the machine, any resource) is modeled as its own kind of external element. (2026-05-29, `L-external-element`)
- *latent seed*: Luthier needs a built-in facility to run external programs and compilers easily. (2026-05-30, `L-run-external-programs`)
- *latent seed*: A library is used by requiring it follow patterns and satisfy propositions defined from Luthier, with an adapter fitting it to each use, so Luthier acts as a universal adapter between libraries. (2026-09-02, `L-library-adapter`)
- *latent seed*: Types are defined natively, while the values (executable functions) may be native or not, admitting both, since only the dubious part is worth reimplementing. (2026-10-04, `L-types-native-values-either`)
- *latent seed*: Luthier should synthesize the call to a Python function using Luthier syntax, so one can work in layers more outward or more inward of Python. (2026-10-07, `L-synthesize-python-call`)
- and 5 more latent seeds in the full map (5 first said by a model)

### The construction pattern: certified subtype and Library

Deriving a certified type, its validating constructor and its forgetful projection from a material type and a predicate.

- *latent seed*: The base of the construction pattern should not be called 'material', which hides what matters; it only makes sense if functors are applied over it, and English mathematical names like ring or field should be used. (, `L-reject-material-name`)
- *latent seed*: Luthier itself is a series of verified types and functions with their theorems and tests, almost an instance of the pattern. (2026-09-29, `L-luthier-is-verified-library`)
- *latent seed*: No language ships units that carry a set of requirements they must satisfy; in Luthier the predicate is a function with parameters (max error, scalability), so the certificate states which parameters are met and a dependent library inherits them. (2026-09-29, `L-units-with-parametrizable-requirements`)
- *latent seed*: Luthier is C++ concepts extended to the whole language: predicates with semantic requirements that are run and whose results are stored, keeping subsumption and composition. (2026-09-29, `L-luthier-is-extended-concepts`)
- *latent seed*: The candidate value is named and the laws applied to it explicitly, but it has the material's type (naming it by the subtype is circular) and needs no forall; the sample size is certificate data, not part of the type. (2026-09-29, `L-candidate-named-not-forall`)
- and 8 more latent seeds in the full map (7 first said by a model)

### Purpose, meaning and motivation

What Luthier is for and why to build it: recovering meaning under AI, platforms, epistemics, biology.

- *open tension*: Is there an intermediate scale where the AI multiplies the author's effort without the result ceasing to be legible and checkable by him? (Luciano, 2026-10-07, `L-intermediate-ai-scale`)
- *latent seed*: He has re-made the language many times, each time rethinking the foundations of programming more deeply. (2022-06-15, `L-remaking-foundations`)
- *latent seed*: He codes to understand, which means being able to manipulate the code and see how changes affect its observables. (2022-06-28, `L-code-to-understand`)
- *latent seed*: Inventing a programming language is like inventing a universe with its own laws. (2026-05-29, `L-language-is-universe`)
- *latent seed*: Since he invents the language it follows his rules, so he can optimize the rules to make manipulating programs easy. (2026-05-29, `L-optimize-own-rules`)
- *latent seed*: Luthier's founding epigraph is Von Neumann's: state exactly what a machine supposedly cannot do and he will build a machine that does it. (2026-06-03, `L-von-neumann-epigraph`)
- and 11 more latent seeds in the full map (4 first said by a model)

### Concrete syntax and notation

The surface forms: binders, symbols versus keywords, the dot, quotes, and reading the language aloud.

- *latent seed*: Composition is written with a dot, which explains class methods. (2022-08-03, `L-composition-dot`)
- *latent seed*: The DSL and the way code is written must be very well defined. (2026-05-29, `L-well-defined-dsl`)
- *latent seed*: Luthier imitates Python's spirit of expressing human ideas easily (with the Monty Python / Luthier wordplay). (2026-09-02, `L-python-spirit`)
- *latent seed*: Luthier's syntax is reduced to only declarations and instantiations. (2026-09-29, `L-syntax-declarations-instantiations`)
- *latent seed*: The canonical form of the language is ASCII; an editor may display -> as an arrow or * as a cross, but what is run by hand and grepped is the ASCII. (2026-09-29, `L-ascii-canonical`)
- and 14 more latent seeds in the full map (8 first said by a model)

### Dependent types and the HoTT foundation

Which type-theoretic foundation Luthier maps onto and what it provides.

- *open tension*: Open question of which foundation to build on (type theory vs category theory, HoTT vs ZMT). (Luciano, 2022-06-28, `L-foundation-choice`)
- *latent seed*: Dependent types are types that depend on a value, taking the cardinality of that value's type. (2022-06-28, `L-dependent-types-def`)
- *latent seed*: A universal type comprising the types of all dimensions, like an abstract class, taken as a feasible coding challenge. (2026-05-29, `L-universal-type`)
- *latent seed*: Dependent types are probably one of the language's basic initial concepts. (2026-05-30, `L-dependent-types-basic`)
- and 9 more latent seeds in the full map (9 first said by a model)

### The forget functor and the typing-load problem

Controlling the typing information that grows as types compose; forgetting as a projection that defines the language.

- *latent seed*: A model or summary can end up bigger than the data it summarizes. (2026-05-27, `L-summary-bigger-than-data`)
- *latent seed*: Composing dependent functions accumulates a growing typing load, so the decoration can end up far bigger than the value. (2026-05-29, `L-typing-accumulates`)
- *latent seed*: When functions are associative you can find patterns in the composition, such as a loop as a series of functions raised to a power. (2026-05-29, `L-patterns-in-composition`)
- *latent seed*: The concept of forgetting (a type forgetting parts of the type) is already present in HoTT. (2026-05-30, `L-forgetting-in-hott`)
- *latent seed*: Execution is a forgetful function: code generates code, with one level that keeps the generated code and one that forgets it. (2026-08-31, `L-execution-as-forgetting`)
- and 3 more latent seeds in the full map (3 first said by a model)

### The derivation store and provenance

Storing derived objects as proof terms with their inputs, never edited, cumulative.

- *latent seed*: Luthier's concepts (function plus version, a table of functions) are carried into the design of the analysis/derivation store. (2026-09-13, `L-apply-luthier-to-[private word]`)
- *latent seed*: Each function declares a result type with fixed fields; the set of result types is open but every individual type is closed, a sum of types, not a JSON blob. (2026-09-13, `L-result-type-closed`)
- *latent seed*: Some types are original (made from audios and questionnaires) and all the rest are derivative, results of functions, so they necessarily have structure. (2026-09-13, `L-original-vs-derivative-types`)
- *latent seed*: The object storing a function, its argument and its result is the graph of evaluation (Ev f), with a sugar that evaluates and stores it; evalstore is just that pair, not a third operation, and the run base is a list of them. (2026-09-29, `L-evaluation-storage-object`)
- *latent seed*: The sugar that stores an evaluation needs delimiters and always stores, since the context cannot decide its type and keeping only failures is the test's filter, not a property of the evaluation. (2026-09-29, `L-ev-sugar-syntax`)
- and 8 more latent seeds in the full map (4 first said by a model)

### The code universe and reflection

A closed Tarski universe of codes so generators and generic functors can be written in Luthier.

- *latent seed*: Luciano challenges the claim that Luthier has no reflection over types. (2026-10-05, `L-luthier-reflection-question`)
- and 11 more latent seeds in the full map (11 first said by a model)

### Constructors, recursors and data mechanics

How data declarations give types, constructors and recursors, and how match derives from them.

- *latent seed*: A constructor differs from a function in that a constructor plus its parameters is the element, making elements transparent, while a function involves a computation. (2022-08-03, `L-constructor-vs-function`)
- *latent seed*: Constructors should live in each type's space rather than in the global space. (2022-08-03, `L-constructors-in-type-space`)
- *latent seed*: A type's definition is necessarily recursive, since the type must be universally accessible like identifiers. (2022-08-03, `L-type-definition-recursive`)
- *latent seed*: Types are expressed as alternatives with a bar, as in maybe, either and sum. (2022-08-03, `L-sum-types-with-bar`)
- *latent seed*: match is not primitive but sugar for the recursor a data declaration gives, the only way to open a data value, and over Bool it is if. (2026-09-29, `L-match-is-recursor-sugar`)
- and 4 more latent seeds in the full map (2 first said by a model)

### Equality: definitional, propositional and levels

The distinct equalities and the levels of equivalence the language expresses.

- *latent seed*: The equals sign is an assertion that both sides are equal, also used for pattern matching when a symbol is unknown. (2022-08-03, `L-equals-assertion`)
- *latent seed*: A fundamental idea of Luthier is to express different levels of equivalence (same information, isomorphic, exactly equal, same memory location), each a different equivalence functor. (2026-05-30, `L-levels-of-equivalence`)
- and 7 more latent seeds in the full map (7 first said by a model)

### Types as propositions that carry their laws

A type states the law its values satisfy, making type safety a consequence of semantic clarity.

- *latent seed*: There should be a one-to-one relation between reasoning and the flow of the code, so running the code verifies the reasoning. (2022-06-28, `L-reasoning-to-code-isomorphism`)
- *latent seed*: A Luthier definition should determine uniquely that a concrete computation is an implementation of a concept (e.g. of matrices). (2026-05-29, `L-implementation-of-concept`)
- and 4 more latent seeds in the full map (4 first said by a model)

### The run database and its synthesis

Recording measured time and precision per run, generalizing it, and keeping it from growing monstrous.

- *latent seed*: From each run of the code something is learned, whether an implementation is correct or how fast it is. (2023-02-22, `L-learn-from-each-run`)
- *latent seed*: The accumulated run information must be synthesized over time so it doesn't grow monstrous and paralyzing. (2026-05-27, `L-synthesize-runs`)
- *latent seed*: Synthesizing information well is the key to the whole design. (2026-05-30, `L-synthesis-is-key`)
- and 1 more latent seeds in the full map (1 first said by a model)

### Program as DAG, commutativity and time

A program as an unordered set of definitions where temporality emerges from dependency.

- *open tension*: The basic question of Luthier: what is a Luthier program, a map or a graph? (Luciano, 2026-09-02, `L-what-is-a-program`)
- *latent seed*: Luthier is a chain of assignments, each an identifier, an equals sign and an operation that creates the object. (2023-03-13, `L-luthier-is-assignments`)
- *latent seed*: An open question is whether a Luthier program is commutative in the order of its statements, and how to model time/order; declarations can be near-commutative. (2026-05-29, `L-commutative-program`)
- *latent seed*: Time, the order of things, is modeled as dependency between definitions, the mathematical way: if one thing depends on another there is a time. (2026-05-29, `L-time-as-dependency`)
- *latent seed*: The fundamental problem is how Luthier programs connect and expand one another so they grow harmonically, with incompatibilities possible. (2026-09-02, `L-compose-programs-harmonically`)
- *latent seed*: Haskell's do sequencing can be simulated as a data dependency (an output needing an input that doesn't exist yet), so do may not be strictly necessary. (2026-10-08, `L-do-as-data-dependency`)
- and 1 more latent seeds in the full map (1 first said by a model)

### Luthier as a higher-order cross-language orchestrator

A minimal bridge-language butler that coordinates other languages and their programs.

- *latent seed*: Luthier composes the input and output of one program with another, chaining external programs. (2026-05-27, `L-compose-programs`)
- *latent seed*: Luthier should be minimal, essentially a bridge language connecting other languages. (2026-05-27, `L-bridge-language`)
- *latent seed*: Delegation should be easy in Luthier, an idea he traces to Modelica. (2026-05-30, `L-easy-delegation`)
- *latent seed*: Describe functions and equivalences and map them to other languages (C, C++, Java), not directly but by giving the tools for others to extend the translation. (2026-05-30, `L-map-to-other-languages`)
- *latent seed*: The ideal is to use Luthier alongside the AI as a kind of butler of knowledge. (2026-09-21, `L-knowledge-butler`)
- and 4 more latent seeds in the full map (3 first said by a model)

### Path equivalence, implementations and optimization

Many implementations of one function, their equivalence, and choosing the best for a case.

- *latent seed*: Luthier compares two paths that do the same thing and determines they are equivalent, possibly with format-conversion stages at the start and end. (2026-05-27, `L-compare-equivalent-paths`)
- *latent seed*: Path equivalence, proving that different implementations are equivalent, is Luthier's fundamental and hardest concept. (2026-05-29, `L-path-equivalence-core`)
- *latent seed*: Function equivalences separate what is essential (the equivalent) from what is decoration (efficiency, cost), the non-equivalent. (2026-05-30, `L-essential-vs-decoration`)
- *latent seed*: Hot values open a larger universe of possible paths than ordinary values. (2026-05-30, `L-hot-values-paths`)
- *latent seed*: The exponential explosion of the path space is handled by particle filtering: running several stochastic programs in parallel exploring different paths. (2026-05-30, `L-particle-filtering-paths`)

### Arrays and performance primitives

Vec and Mat as definitions whose fast implementations are externs certified against them.

- *latent seed*: Array is generic in the element type with numeric operations over Real (Vec = Array Real), so index arrays become Array Int and writing it over Float64 would reglue definition to realization. (2026-10-04, `L-array-generic-element-type`)
- and 3 more latent seeds in the full map (3 first said by a model)

### Environment, variables and memory

The early model of an environment that stores and retrieves variables by name.

- *latent seed*: The environment is the first object the language must define, since data is loaded into it. (2022-07-05, `L-environment-first-object`)
- *latent seed*: There are simple environments (one value type, one identifier) and compound ones that admit multiple. (2022-07-05, `L-environment-kinds`)
- *latent seed*: The environment needs and manages resources (memory and compute) and function execution, a problem that ties to it but exceeds it (OS, compiler). (2022-07-05, `L-environment-resources`)
- *latent seed*: The environment is a map of definitions whose two mechanisms are storing and retrieving variables by name. (2022-07-05, `L-environment-stores-retrieves`)
- *latent seed*: A variable is a name, a memory address, a size and a type; the type contains the size and the name can be the address. (2022-07-05, `L-variable-is-fields`)
- and 1 more latent seeds in the full map

### Objects as cyclic codependent definitions

Interdependent laws making a group of types one object, a cycle in the definition graph.


### Decorators, uncertainty functors and value annotations

Decorating a value with error, provenance or what is known about it, and the views one can take.

- *latent seed*: Decorators express the error of a number and its propagation (derivatives), as he did in C++ with templates. (2026-05-29, `L-decorators-error`)
- *latent seed*: A value carries an annotation of everything already known about its class. (2026-08-31, `L-value-carries-annotations`)
- *latent seed*: A value knows the concrete operation that produced it: the sum is the sum, not the generic magma operation. (2026-08-31, `L-value-knows-operation`)

### Early identifier and naming explorations

The 2022 ideas on identifiers as the human-machine dictionary and on names for dynamic objects.

- *latent seed*: Identifiers are central: a simple label recovers a complex object, the dictionary joining human and machine. (2022-06-15, `L-identifiers-central`)
- *latent seed*: For dynamically created types or functions, a name is really an address, so a generated numeric identifier suffices. (2022-08-03, `L-dynamic-naming`)
- *latent seed*: The identifier and the type are completely independent; the identifier is a fantasy name unknown until resolved. (2022-08-03, `L-identifier-type-independent`)

## 2. The candidate principles

Found blind by `find_principles_v2` (it saw only the ideas and your criterion of infectability), set against P1 to P14 by `match_principles_v1`. Full detail: `record/distillation/2026-10-09_match_principles_v1_claude-code_opus.md`.

```
C1  A type is the proposition its values must satisfy, extended to functions whose type is their
    laws, so membership is a guarantee.
Instead of: types as mere storage shapes or tags with no semantic content
Quote:      "los tipos tienen que ser conceptos, tipos como proposiciones y los tipos incluyen
            también funciones, funciones y funciones de orden superior"
Said by:    Luciano, 2026-05-26 12:33
Strongest:  conceptual. collapsing type, test and proposition into one thing reorganizes what it
            means to define anything, so a function's type is the law it obeys.
In force:   new
Mark:       

C2  Code is a datum of the language itself, so a program can be built, inspected and run by other
    programs, and Luthier operates on Luthier.
Instead of: a fixed boundary where source is compiled once and never seen as a value
Quote:      "La idea de que el codigo sea dato es muy, pero muy fuerte en cuanto a la flexibilidad
            que ofrece pero es notable que los lenguajes modernos no sigan ese camino Lispeano."
Said by:    Luciano, 2022-06-15 08:55
Strongest:  conceptual. erasing the code/data line lets the language operate on itself, so the
            interpreter, the trace and the verifier all become ordinary data.
In force:   new
Mark:       

C3  From a type and a predicate over it, derive a certified subtype, a validating constructor and
    the projection back, the one pattern for values, functions and programs.
Instead of: ad hoc validation scattered at call sites, separate from the type
Quote:      "este tipo Almacen que en realidad confunde dos cosas el constructor de almacen y el
            almacen es el concepto fundamental de Luthier (no almacen sino el patron de
            construccion)."
Said by:    Luciano, 2026-09-29 06:00
Strongest:  conceptual. one pattern (material type plus predicate yields certified type, validating
            constructor and forgetful projection) is read as the single core act the whole language
            is built from.
In force:   new
Mark:       

C4  For each concept find the mathematical object that best represents it and put it as the type's
    invariant, characterizing an operation rather than reproducing its implementation.
Instead of: laws that just restate what the fast code does (consistency, not characterization)
Quote:      "La idea en realidad es buscar el objeto matematico que mejor lo represente y decirlo."
Said by:    Luciano, 2026-10-05 00:35
Strongest:  ethical. it says a law must state the property that determines an operation up to
            equality, not re-run its implementation, which is a discipline about what counts as a
            real invariant.
In force:   extends P10: Adds that the invariant characterizes the operation up to the presentation's equality, so a second implementation is consistency not characterization and the native definition is one more model certified against it.
Mark:       

C5  Luthier first describes the problem and its equivalences and only then executes; execution is
    the verification of those equivalences, as mathematics verifies rather than runs.
Instead of: a language whose primary act is to compile and run code
Quote:      "Hay una idea, que la matemática no ejecuta, porque lo único que hace es verificar
            equivalencias. Entonces, bueno, sí, la ejecución en Luthier sería esa verificación de
            equivalencias"
Said by:    Luciano, 2026-05-30 18:03
Strongest:  conceptual. reading execution as mathematics does, verifying equivalences, inverts the
            usual picture: the program describes and the run certifies, with a declarative and an
            executive side.
In force:   new
Mark:       

C6  Keep the native core to a handful of primitives, self-extensible and executable by hand, and
    build every complex concept on top of it.
Instead of: a large built-in language with syntactic sugar and many primitives
Quote:      "Luthier tendría que ser ejecutable a mano es decir que uno pudiese con l y papel
            escribir las cosas"
Said by:    Luciano, 2026-05-29 14:14
Strongest:  aesthetic. the demand that a well-written Luthier be executable by hand with pencil and
            paper is an austere standard of economy that shapes every primitive.
In force:   new
Mark:       

C7  Luthier is an abstraction mechanism whose aim is to express the invariances of the disciplines
    clearly.
Instead of: a language organized around computation rather than meaning
Quote:      "la idea de luthier es expresar invarianzas de los de las disciplinas"
Said by:    Luciano, 2026-05-29 14:29
Strongest:  emotive. it names what moves the author to invent the language: a relator of
            invariances, against the statistical predictor, a species mates within itself, electrons
            are fermions.
In force:   new
Mark:       

C8  A declaration without a body is a first-class hole, an opaque name that does not reduce, and
    nothing executes until it is defined.
Instead of: treating a missing definition as a compile error
Quote:      "porque necesitamos el simbolo para el hueco, ?. No basta con decri f: A-> B y no
            definirlo?"
Said by:    Luciano, 2026-09-29 04:20
Strongest:  conceptual. a bodyless declaration plays axiom, program input, external function,
            pending definition and dead code at once, so one construct absorbs five roles usually
            kept apart.
In force:   new
Mark:       

C9  A function has many equivalent implementations (paths), each with its precision and cost, and
    Luthier chooses among them by expected loss and speed.
Instead of: one fixed implementation bound to a function name
Quote:      "una funci esta funci puede ser implementada de muchas maneras, son los distintos paths y
            cada forma tiene una precisión y una velocidad"
Said by:    Luciano, 2026-05-26 12:33
Strongest:  conceptual. one function with many implementations (paths), each with its precision and
            speed, chosen by expected loss, turns a program into a declarative object that
            self-optimizes.
In force:   new
Mark:       

C10  Verification is one operation, exact when it can compute and statistical when it samples, and
    every value carries the grade of guarantee it was checked to.
Instead of: a single pass/fail notion of correctness
Quote:      "La comprobación de un valor es un cómputo; la de una función es un experimento. Luthier
            tiene que tratar a los dos como la misma operación de construir, sabiendo que uno es
            exacto y el otro estadístico."
Said by:    model, 2026-09-29 05:56
Strongest:  conceptual. treating checking a value and checking a function as one construct
            operation, exact or statistical, and reading verification as a Bayesian observer
            updating a posterior, makes the grade of guarantee part of what membership means.
In force:   new
Mark:       

```

## 3. The rules and the ideas behind them

Full detail: `record/synthesis/2026-10-09_trace_rules_v1_claude-code_opus.md`.

| source | rules | from at least one idea | from none |
|---|---|---|---|
| `docs/spec/02-grammar.md` | 6 | 6 | 0 |
| `docs/spec/03-libraries.md` | 5 | 5 | 0 |
| `docs/spec/04-kernel.md` | 7 | 7 | 0 |
| `docs/spec/05-static-semantics.md` | 11 | 11 | 0 |
| `docs/spec/06-numbers.md` | 7 | 7 | 0 |
| `docs/spec/08-tests.md` | 22 | 21 | 1 |
| `record/decisions.md` | 42 | 30 | 12 |

Rules with no idea behind them (written in the specification or decided in the log without a trace in your ideas):

- **G11** Dependent components are drawn in order.
- **D-2026-10-06-b** One decision log per repository; a decision that affects both goes in both.
- **D-2026-10-06-f** Every change is applied on top of a commit.
- **D-2026-10-06-h** Reversibility, the parts of working method §8 that "Si." confirmed as a bundle.
- **D-2026-10-06-i** The git for large data keeps its repository outside the folder it tracks.
- **D-2026-10-06-j** A document for Luciano is committed before he annotates it; his annotations are then committed verbatim, so they are the diff.
- **D-2026-10-06-k** The chat exports go to GitHub.
- **D-2026-10-06-l** In a document for Luciano, a numbered reference carries its statement; records may be terse.
- **D-2026-10-06-n** CLAUDE.md is a living document of operative rules, with no meta-information.
- **D-2026-10-06-o** The principles audit asks three questions (followed and useful; failing by conflict; new principles and their cost) and is run by a script.
- **D-2026-10-06-t** Sources are written in one grammar: repo@commit:path:line (or :a-b), and chat:session8:line.
- **D-2026-10-06-u** A quote that the check of quotes finds at its line confirms a decision of Luciano's; the statements go through the fidelity audit.
- **D-2026-10-07-a** Luthier proper is separated from the record of its development: README, docs/, src/, examples/ and tests/ present Luthier; record/ holds how it came to be. scri

## Inputs

- `record/synthesis/2026-10-09_consolidate_lineages_v1_claude-code_opus.json` sha256 0bbf7c6f4782
- `record/distillation/2026-10-09_find_principles_v2_claude-code_opus.json` sha256 36069e9a04e8
- `record/synthesis/2026-10-09_trace_rules_v1_claude-code_opus.json` sha256 6f212a933675
- `record/ideas/lineages_link_ideas_v1_claude-code_opus.json` sha256 9a2d5795a122
- `record/ideas/timeline.jsonl` sha256 b18b5806955d
- `record/distillation/2026-10-09_match_principles_v1_claude-code_opus.json` sha256 f3e8e0198bc8
