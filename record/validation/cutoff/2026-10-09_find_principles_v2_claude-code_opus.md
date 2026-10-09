# Candidate principles of Luthier, found blind, 2026-10-09

Written by `scripts/find_principles.py` (find_principles v1). Prompt `find_principles_v2` (sha256 5eb0cb1b3e6b),
model opus at effort low via claude-code (2.1.197 (Claude Code)); the model saw only the
lineages and the criterion of infectability.
Inputs by sha256: `record/validation/cutoff/lineages_link_ideas_v2_claude-code_opus.json` c81023f451dc; `record/ideas/timeline.jsonl` b18b5806955d.
Each candidate shows apart what the script took from the rows and what is the model's reading.

Lineages: 404; candidate 30, considered 169, not_principle 205.

## Candidates

```
C1  Defining a function means stating, as runnable tests, what it must satisfy, so definition and
    verification are one act.
Instead of: a definition that is only a body, with tests written separately and optionally later
Scope:      language
-- from the rows, by the script
Quote:      "La idea central del tapp es que al declarar una funcion vos declaras que es lo que la
            funcion debe cumplir como un test y entonces es posible generar tests automaticos."
Said by:    Luciano, 2022-08-03 11:56
Source:     2022-08-03 haskell.md line 19 (row written:2022-08-03_haskell:declarar-funcion-es-declarar-su-test)
Lineages:   L-declare-is-test, L-self-verified-programs, L-group-of-functions-with-laws
Witnesses:  first 2022-08-03 by Luciano; 20 witnesses over 7 days
-- the model's reading (opus, effort low)
Strongest:  ethical. it recasts what it means to have a function: you do not have it until you have
            said, as runnable tests, what it must satisfy.
Also:       conceptual. collapses definition and test into one object, so running the code is
            running the test.
Harms:      a function with no cheap test becomes hard to admit
Harms:      blurs the line between specification and verification, hiding which is trusted
Harms:      statistical tests give false confidence of proof
Beats:      L-types-defined-by-propositions (A type or function is defined by the propositions
            (postconditions) it satisfies, for variables and for functions alike.). l40 says a type
            is defined by the propositions it satisfies, the same idea stated as a property rather
            than as the sharper, more infectious 'defining is testing'.
Above next: It is the stance Luciano names again and again as the novelty, broader than the
            construction mechanism that realizes it.

C2  Make the predicate the primitive, and derive the certified type, its sole constructor and its
    forgetful projection from it.
Instead of: types and their validating constructors declared as separate, hand-matched things
Scope:      language
-- from the rows, by the script
Quote:      "lo primitivo es el predicado, y el tipo y el constructor se derivan de él mecánicamente.
            No son dos cosas que se confunden bajo un nombre; son dos usos de una sola cosa."
Said by:    model, 2026-09-29 06:01
Source:     2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 59 (row dialogue:890a551c:lo-primitivo-es-el-predicado-tipo-y-constructor-se-derivan)
Lineages:   L-subtype-by-predicate, L-concept-as-predicate, L-subtype-is-sigma-pair,
            L-construction-pattern, L-predicate-returns-result
Witnesses:  first 2022-08-03 by Luciano; 28 witnesses over 2 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. one primitive, a predicate over a material, generates type, constructor and
            forget mechanically, unifying values, functions and whole programs.
Also:       aesthetic. economy: the type and the constructor stop being two confused things and
            become two uses of one.
Harms:      every value carries a certificate, costing memory and compute
Harms:      the predicate may be undecidable or only testable, so 'checked' means different
            strengths
Harms:      forces thinking in predicates even where a plain value would do
Beats:      L-law-structure (A law is a type of arguments plus a predicate over them that takes the
            function under test as argument and returns the two sides rather than a bare Bool, so
            the counterexample explains itself; its failure is a reified application.). l382
            structures a single law well, but it is a piece of the pattern, not the generative
            pattern itself.
Above next: It is the single mechanism Luciano calls the core of Luthier, where C3's code-as-data is
            the older, broader frame it rides on.

C3  Hold a program's code as a value of an ordinary data type, so code and data are the same kind of
    thing.
Instead of: code as an opaque artifact the language runs but cannot hold or operate on
Scope:      language
-- from the rows, by the script
Quote:      "La idea de que el codigo sea dato es muy, pero muy fuerte en cuanto a la flexibilidad
            que ofrece pero es notable que los lenguajes modernos no sigan ese camino Lispeano."
Said by:    Luciano, 2022-06-15 08:55
Source:     2022-06-15 Sin título 2 .md line 13 (row written:2022-06-15_sin-titulo-2:codigo-es-dato)
Lineages:   L-code-as-data, L-meta-recursive, L-term-syntax-as-data
Witnesses:  first 2022-06-15 by Luciano; 25 witnesses over 12 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. erasing the code/data line lets a program hold, inspect and transform its
            own code as an ordinary value, reorganizing what a program is.
Also:       aesthetic. the syntax is a data like any inductive type, so the core explains itself,
            metacircular.
Harms:      homoiconicity invites self-modification and self-hacking
Harms:      a core that is its own data is harder to keep consistent
Harms:      power tempts cleverness over clarity
Beats:      L-code-many-operations (Luthier code is not merely compiled and run; many operations can
            be applied to it: verify, compile, run and others.). l228 says many operations apply to
            code, which is a consequence of code-as-data rather than the frame-opening idea itself.
Above next: It is a larger ontological commitment than the specific forgetting machinery that
            follows, which lives inside it.

C4  Treat the choice of what to forget from a type as the thing that defines the language you are
    speaking.
Instead of: forgetting as an ad hoc cleanup, with the language fixed independently of it
Scope:      language
-- from the rows, by the script
Quote:      "de qué función de olvido le aplicás a los tipos, es un, digamos, eso te define
            básicamente el lenguaje que estás hablando ... los functores de olvido serían, digamos,
            uno de los componentes más importantes de Luthier"
Said by:    Luciano, 2026-05-29 14:59
Source:     2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 21 (row dialogue:20260529T1400:funtores-de-olvido-definen-el-lenguaje)
Lineages:   L-forgetting-problem, L-forgetting-defines-language
Witnesses:  first 2026-05-29 by Luciano; 9 witnesses over 2 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. it reframes a language as defined by what it chooses to forget, turning the
            forgetful functor from a side tool into the identity of the language.
Also:       aesthetic. it unifies mean, projection, execution and compilation as instances of one
            operation, forgetting.
Harms:      choosing the wrong forgetful functor silently changes the language's meaning
Harms:      forgetting is non-invertible, so information is lost for good
Harms:      an ill-defined forgetting degenerates into crude truncation Luciano rejects
Beats:      L-forgetting-functions-vary (There are several forgetting functions, each optimizing
            different things, so understanding their properties and which to use for what is an
            engineering challenge.). l196 observes that different forgetting functions optimize
            different things, a corollary of the stronger claim that the choice of forgetting is the
            language.
Above next: It structures the whole type machinery, where C5's equivalence is the thing forgetting
            must commute with, downstream of it.

C5  Make execution the verification of equivalences, following mathematics, which does not run but
    only verifies.
Instead of: execution as a separate operational act distinct from reasoning about equivalence
Scope:      language
-- from the rows, by the script
Quote:      "Hay una idea, que la matemática no ejecuta, porque lo único que hace es verificar
            equivalencias. Entonces, bueno, sí, la ejecución en Luthier sería esa verificación de
            equivalencias"
Said by:    Luciano, 2026-05-30 18:03
Source:     WhatsApp Ptt 2026-05-30 at 18.01.53.md [01:47] (row day:2026-05-30:matematica-no-ejecuta-verifica-equivalencias)
Lineages:   L-verifiability, L-execution-is-equivalence-verification
Witnesses:  first 2026-05-27 by Luciano; 3 witnesses over 2 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. it redefines running a program as verifying equivalences, importing
            mathematics' stance that nothing executes, equivalences are only checked.
Also:       aesthetic. it dissolves the execution/proof divide into one act, elegant and spare.
Harms:      demoting execution may make the language impractical for real computation
Harms:      verifying equivalence is undecidable in general
Harms:      users wanting to just run things face a conceptual detour
Beats:      L-levels-of-equivalence (A fundamental idea of Luthier is to express the different
            levels of equivalence (same information, isomorphic, exactly equal, same memory
            location), each depending on a different equivalence functor.). l218 enumerates levels
            of equivalence, useful but a taxonomy inside the deeper claim that execution itself is
            equivalence-checking.
Above next: It is a sharp reframe of execution, where C6 reframes the purpose of the whole language
            and reaches wider.

C6  Aim the language at expressing the invariances of each discipline, as a relator of invariances.
Instead of: a language that expresses computations or statistical patterns, not the invariants
            behind them
Scope:      language
-- from the rows, by the script
Quote:      "la idea de luthier es expresar invarianzas de los de las disciplinas"
Said by:    Luciano, 2026-05-29 14:29
Source:     2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 11 (row dialogue:20260529T1400:expresar-invarianzas-de-disciplinas)
Lineages:   L-relator-abstraction, L-express-invariances
Witnesses:  first 2026-05-29 by Luciano; 8 witnesses over 3 days
-- the model's reading (opus, effort low)
Strongest:  emotive. it names what moves the author: a language that relates the invariances of each
            field, set against statistical predictors that only guess.
Also:       conceptual. it makes the unit of expression a discipline's invariant rather than an
            algorithm or value.
Harms:      'invariance of a discipline' is vague and hard to pin down operationally
Harms:      risks the project growing to cover the whole universe and becoming useless
Harms:      privileges domains with clean invariances over messy ones
Beats:      L-language-for-defining-ideas (Luthier is a language for defining things, where ideas
            are first-class citizens, like natural languages such as Spanish or English.). l238, a
            language where ideas are first-class, is close but more diffuse than the specific aim of
            expressing invariances.
Above next: It states the language's purpose, broader than the declarative-plus-optimizer mechanism
            that serves it.

C7  Let the programmer declare what they want and have the engine openly weigh many equivalent
    implementation paths by estimated cost.
Instead of: writing one implementation and committing to its performance by hand
Scope:      language
-- from the rows, by the script
Quote:      "que Luthier sea, en el fondo, una forma de ser a la vez un lenguaje declarativo y una
            herramienta de optimización. O sea, que vos declares lo que querés hacer, que sigan más
            decir las fórmulas, y después internamente baraja distintas formas de implementar eso,
            pero eso lo hace abiertamente"
Said by:    Luciano, 2026-05-26 12:33
Source:     2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 1 (row dialogue:20260526T1233:luthier-declarativo-y-optimizador)
Lineages:   L-declarative-and-optimizer, L-declarative-executive-map, L-paths,
            L-cost-estimation-per-path, L-path-equivalence-fundamental
Witnesses:  first 2026-05-26 by Luciano; 19 witnesses over 4 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. it splits a program into what it means (declared) and how it runs (openly
            chosen among estimated paths), reorganizing the frame of writing code.
Also:       ethical. it makes the trade-off between clarity and speed explicit and the machine's,
            not hidden in the programmer's head.
Harms:      maintaining many paths and their cost estimates is heavy machinery
Harms:      a priori cost estimation is the hardest open problem, maybe unsolvable well
Harms:      the run database can grow monstrous and paralyzing
Beats:      L-performance-database (Luthier keeps a database recording, for each function with given
            initial data, scale and algorithm, the time taken and precision achieved (and memory,
            CPUs, machine, range of results), known because actually measured.). l134, the
            performance database, is the implementation substrate for this idea rather than the
            reframe itself.
Above next: It opens a whole operational frame, where C8 is one elegant primitive within such a
            design.

C8  Let a bodyless typed declaration be the one construct that serves as axiom, input, external
    function, pending definition and dead code at once.
Instead of: separate language features for axioms, inputs, foreign calls, stubs and unused code
Scope:      language
-- from the rows, by the script
Quote:      "el **hueco**: una definición con tipo y sin cuerpo, `f : A → B := ?`. Una sola cosa
            cumple cinco papeles: axioma, input del programa, función externa que el entorno llena,
            definición pendiente, código muerto. Tu principio "no ejecutás hasta que está definido"
            es su semántica exacta"
Said by:    model, 2026-09-28 20:56
Source:     2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 2 (row dialogue:175c0408:hueco-cinco-papeles)
Lineages:   L-hole-unifies-roles, L-hole-symbol-needed
Witnesses:  first 2026-09-28 by model; 6 witnesses over 2 days
-- the model's reading (opus, effort low)
Strongest:  aesthetic. one construct, a bodyless declaration, collapses five roles that other
            languages keep as separate features.
Also:       conceptual. its semantics is exactly 'do not execute until defined', so dead and pending
            code sit harmlessly.
Harms:      overloading one construct with five meanings can confuse readers
Harms:      no way to mark intention means external vs unwritten is indistinguishable
Harms:      a program full of holes may typecheck yet do nothing
Beats:      L-no-execution-until-defined (Code is not executed until it is fully defined, so
            undefined dead code can sit there without bothering anyone.). l226 states the 'no
            execution until defined' rule, which the hole subsumes and sharpens into a single
            primitive.
Above next: It is a crisp unification, where C9 is the more foundational logical stance the whole
            type system rests on.

C9  Make types propositions and terms their proofs, so the code is its own mathematical
    demonstration.
Instead of: types as mere data shapes, with correctness argued outside the code
Scope:      language
-- from the rows, by the script
Quote:      "los tipos tienen que ser conceptos, tipos como proposiciones y los tipos incluyen
            también funciones, funciones y funciones de orden superior"
Said by:    Luciano, 2026-05-26 12:33
Source:     WhatsApp Ptt 2026-05-26 at 12.32.24.md [00:38] (row day:2026-05-26:tipos-como-conceptos-y-proposiciones)
Lineages:   L-types-as-concepts, L-proposition-is-type-truth
Witnesses:  first 2026-05-26 by Luciano; 12 witnesses over 4 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. types as propositions and code as its own proof fuses programming and
            proving, validating logic before a line runs.
Also:       ethical. it takes a stance that a program should carry the guarantee of what it claims,
            not just do it.
Harms:      Curry-Howard raises the entry cost for ordinary programmers
Harms:      making code its own proof demands discipline most code cannot pay
Harms:      proof obligations can balloon with each dependent composition
Beats:      L-laws-as-universal-propositions (A type carries laws its operations must satisfy
            universally (identity, io round-trip), stated with for_all.). l45, laws stated
            universally on a type, is an application of the propositions-as-types view rather than
            the view itself.
Above next: It is the logical foundation, where C10 is the stylistic and architectural discipline
            laid on top.

C10  Keep the founding components few and hand-executable, and build the whole edifice of complex
    concepts from them.
Instead of: a rich primitive set with special-cased features and sugar in the core
Scope:      language
-- from the rows, by the script
Quote:      "El minimalismo está en los componentes fundantes y después a partir de esos componentes
            fundantes vos construís un edificio enorme."
Said by:    Luciano, 2026-05-30 18:07
Source:     WhatsApp Ptt 2026-05-30 at 18.07.21.md [00:12] (row day:2026-05-30:minimalismo-fundante-maximalismo-construido)
Lineages:   L-language-self-writing, L-minimal-bridge-language, L-executable-by-hand,
            L-minimalism-in-foundations
Witnesses:  first 2022-08-03 by Luciano; 14 witnesses over 6 days
-- the model's reading (opus, effort low)
Strongest:  aesthetic. minimalism in the founding components, from which a huge edifice is built, is
            the classic beauty of economy.
Also:       ethical. a language executable with pencil and paper insists the programmer can always
            understand what runs.
Harms:      extreme minimalism can push complexity onto unreadable library layers
Harms:      'executable by hand' may forbid features users want
Harms:      few primitives risks cryptic error messages
Beats:      L-types-and-functions-only (Luthier keeps only two primitives, types and functions, and
            functions are themselves a type.). l154, keeping only types and functions, is one
            concrete reduction inside the broader principle of few founding components.

```

## Considered and left out

- `L-identifiers-central` (Luciano, 4 rows): Identifiers are central to programming: a simple label stands for a complex object, joining human and machine. *identifiers unite human and machine*
- `L-code-to-understand` (Luciano, 1 rows): I code to understand: understanding requires manipulating the code and seeing how changes affect its observables. *I code to understand, a method stance*
- `L-equivalence-optimization` (Luciano, 5 rows): Once semantic equivalence is established, a clear but slow implementation can be replaced by a faster equivalent one, enabling automatic optimization. *equivalence enables optimization*
- `L-expressiveness` (Luciano, 3 rows): Code must express its intention to both the human reader and the compiler, referring truthfully to known structures and to extra-computational concepts. *code expresses intention truthfully*
- `L-reasoning-code-isomorphism` (Luciano, 1 rows): Formalize semantic determination so there is a one-to-one relation between reasoning and the flow of the code, verifying the reasoning. *reasoning-code isomorphism*
- `L-semantics-own-universe` (Luciano, 1 rows): The language's semantics lives in its own universe, not C++'s, even though expressed with C++ structures. *semantics lives in its own universe*
- `L-code-metafunctions` (Luciano, 3 rows): One can apply functions that operate on code: run tests, compute errors or derivatives, find equivalents, estimate run time, incorporating these into the syntax. *functions operating on code*
- `L-element-one-type` (Luciano, 2 rows): An element satisfies many types, but the chosen relation is that each element belongs to exactly one type and can serve to build many. *each element belongs to one type*
- `L-identifier-type-independent` (Luciano, 1 rows): The identifier and the type are completely independent; the identifier is a fantasy name unknown until resolved. *identifier independent of type*
- `L-types-defined-by-propositions` (Luciano, 5 rows): A type or function is defined by the propositions (postconditions) it satisfies, for variables and for functions alike. *types defined by propositions*
- `L-laws-as-universal-propositions` (Luciano, 2 rows): A type carries laws its operations must satisfy universally (identity, io round-trip), stated with for_all. *laws as universal propositions*
- `L-test-result-explains` (Luciano, 2 rows): A condition or test yields either success (one) or an explanation of why it failed, not just a boolean. *test yields explanation not boolean*
- `L-define-together-tuples` (Luciano, 4 rows): There is only one way to define, in tuples that may hold several identifiers, assigned together when their postconditions are interdependent (crossconditions). *define functions in groups*
- `L-learn-from-runs` (Luciano, 1 rows): Each run of the code teaches something: whether an implementation is correct or how fast it is. *learn from runs*
- `L-post-becomes-precondition` (Luciano, 1 rows): A subtype defined by a function's postconditions can serve as a precondition of another function. *postcondition becomes precondition*
- `L-implementation-as-functor` (Luciano, 4 rows): A function's declaration (its type/postconditions) is separate from its implementation: implementations are functors, may depend on unknown functions, and natural transformations translate one into another. *implementation as functor*
- `L-internal-equality` (model, 2 rows): HoTT gives types as spaces and identities as paths, its internal equality replacing ad hoc isomorphisms. *internal equality replaces isomorphisms*
- `L-models-as-typed-objects` (model, 3 rows): Biological models are well-typed mathematical objects where types are molecular states, identity paths are symmetries, and composition emerges from dependent type operations. *models as typed objects*
- `L-separate-deterministic-probabilistic` (model, 3 rows): Deterministic structural validity (lifted into types via HoTT) is kept separate from probabilistic inference, handled downstream by Bayesian layers. *separate deterministic from probabilistic*
- `L-type-level-validity` (model, 5 rows): Invalid or inconsistent models are prevented at the type level, validated structurally at compile time instead of at runtime. *prevent invalid at type level*
- `L-hottification` (model, 6 rows): HoTTification is turning a scientific model, algorithm or language into a formal structure governed by HoTT, analogous to categorification, giving machine-verifiable theories. *hottification concept*
- `L-semantic-safety` (model, 6 rows): Semantic safety is model correctness enforced by the modeling language's structural rules (dependent typing), distinct from runtime safety, so only valid models can exist. *semantic safety, only valid models exist*
- `L-generative-model-spaces` (model, 1 rows): The strategic aim is to replace ad hoc model design with compositional, type-safe, generative model spaces. *replace ad hoc with generative spaces*
- `L-adjoint-diagnostic-pairs` (model, 8 rows): Each forward operation (simulate, infer, likelihood) is paired with a diagnostic co-operation (recover, invert, summarize) in an adjoint-like relation, and the system's tests are derived from these pairs. *adjoint diagnostic pairs*
- `L-contagiously-safe-dsl` (model, 6 rows): The endgame is a compile-time Contagiously Safe DSL whose safety propagates through the system, enforcing structure at the compiler level with a type-safe backend and a HoTT-verified inference algebra. *contagiously safe DSL*
- `L-structure-before-proof` (model, 8 rows): Epistemic and semantic structure and soft safety are established before hard type checking or proofs; diagnostics defend correctness until proofs exist and later become type-inhabiting witnesses. *structure before proof*
- `L-tests-are-morphisms` (model, 4 rows): Tests are not arbitrary unit tests or patches but morphisms and triangle identities encoding epistemic contracts derived from the engine's own structure, so semantic structure matters more than coverage. *tests are morphisms not patches*
- `L-program-goal-elevate-engines` (model, 3 rows): The program transforms scientific inference engines from empirically working black boxes into epistemically structured, formally safe systems, starting from the empirical systems themselves, a semantic elevation rather than a rewrite. *semantic elevation not rewrite*
- `L-reproducibility-formal` (model, 2 rows): The reproducibility crisis is a lack of structural verification rather than a sociological issue, and reproducibility is a formal property. *reproducibility is formal*
- `L-code-encodes-epistemology` (model, 2 rows): Scientific software should encode its epistemic structure, not just its algorithms; it is executable epistemology rather than engineering. *code is executable epistemology*
- `L-safety-semantic-zone` (model, 1 rows): Safety is a constructible semantic zone rather than an afterthought. *safety is a constructible zone*
- `L-semantic-verification` (model, 1 rows): Verification of scientific code should be semantic, not merely syntactic. *verification must be semantic*
- `L-snapshot-first` (Luciano, 1 rows): Before committing to tests and decisions, do the simpler thing: record snapshots, compare results outside the system, and study them to decide which tests to run. *snapshot first*
- `L-oracle` (model, 3 rows): An oracle supplies an external reference behavior to compare the implementation against, catching semantic drift that an intrinsic postcondition cannot when the exact expected value is unknown. *oracle as external reference*
- `L-serialization-invertible` (Luciano, 1 rows): A serialization is legitimate only if invertible: to_json followed by from_json is the identity, a law the representation of a value must satisfy. *serialization invertible as a law*
- `L-reasonable-then-wild` (Luciano, 1 rows): Luciano's method: first work out the reasonable version, then look for the wild one; here the wild move is to invent Luthier directly rather than through the other projects. *reasonable then wild*
- `L-cross-language` (Luciano, 10 rows): Luthier is not tied to C++ but a language-agnostic pseudo-language, cross-language rather than cross-compiler, implementable in different languages (PyLuthier, RLuthier, CLuthier) transformable between each other. *cross-language not cross-compiler*
- `L-butler-orchestrator` (Luciano, 8 rows): Luthier is a higher-order butler that can run and compile other languages, orchestrate them and compare their outputs, choosing where each computation runs by its complexity. *butler orchestrator*
- `L-explore-solutions` (Luciano, 1 rows): The purpose is to let the user find different solutions to their problem and compare the estimated complexity of each way of executing it. *explore different solutions*
- `L-bayesian-complexity-estimation` (Luciano, 4 rows): A priori complexity is estimated by a Bayesian strategy: give different algorithms chances at the same task, measure their actual times, and estimate from accumulated experience. *bayesian complexity estimation*
- `L-performance-database` (Luciano, 6 rows): Luthier keeps a database recording, for each function with given initial data, scale and algorithm, the time taken and precision achieved (and memory, CPUs, machine, range of results), known because actually measured. *performance database*
- `L-computation-categories` (Luciano, 5 rows): Just as different functions do the same thing, different computations take the same time; the categories or classes of computation must be found so one needn't measure each. *categories of computation*
- `L-self-modeling-estimation` (model, 5 rows): The time and precision estimation functions are themselves modeled by Luthier (lutearized) and used by Luthier itself, making the system metacircular. *self-modeling estimation*
- `L-compose-compare-paths` (Luciano, 3 rows): Luthier composes the output of one program into another and compares two alternative paths that do the same thing to see they are equivalent, with format conversion stages at the start and end. *compose and compare paths*
- `L-two-layers` (Luciano, 3 rows): Luthier has two layers: a first with equivalences and verifiability, and a second that measures time, complexity, resources and success/failure and lets you pick the faster of two equivalent paths. *two layers*
- `L-delegate-execution` (Luciano, 2 rows): Luthier could delegate execution entirely and keep only verification, as an extreme of minimalism. *delegate execution*
- `L-synthesize-run-info` (Luciano, 4 rows): A central challenge is synthesizing the accumulated run information so it doesn't grow monstrous and paralyzing. *synthesize run info*
- `L-model-of-computation` (Luciano, 4 rows): Luthier contains a model of the world, a model of computation continually tested and simplified and kept active through selective forgetting or aggregation, justified by use for predicting or interpreting a particular case. *model of computation*
- `L-lisp-single-primitive` (Luciano, 2 rows): Luthier should reduce to a single kind of element, the way Lisp reduces everything to lists. *single primitive like Lisp*
- `L-types-and-functions-only` (Luciano, 4 rows): Luthier keeps only two primitives, types and functions, and functions are themselves a type. *types and functions only*
- `L-few-types-good-rules` (Luciano, 2 rows): Luthier must have very few types, but those types follow a small set of well-thought, well-defined rules, likely from HoTT. *few types with good rules*
- `L-hijack-code` (Luciano, 4 rows): Luthier must be able to hijack code from any other language. *hijack foreign code*
- `L-hott-bayes-marriage` (Luciano, 9 rows): Proving path equivalence needs, beyond logical proof, an empirical statistical proof: a probabilistic extension of HoTT, a marriage of homotopy type theory and Bayes. *HoTT-Bayes marriage*
- `L-core-plus-libraries` (Luciano, 3 rows): Luthier is structured as a closed core plus libraries that are the Luthier functions handling interaction with the exterior. *core plus libraries*
- `L-observer-of-universe` (Luciano, 3 rows): Luthier is a closed, internally complete universe (its types perfect) that observes the external world, like an observer. *observer of the universe*
- `L-external-element` (Luciano, 2 rows): Everything that is not Luthier (C++, Python, the computer, any resource) is conceptually external and must be modeled as its own kind of external element. *external element type*
- `L-decorator-algebra` (Luciano, 4 rows): Decorator composition has algebraic properties (associativity, commutativity) that Luthier can express, representing them in the simplest form when the operation is commutative. *decorator algebra*
- `L-function-properties-and-operation` (Luciano, 4 rows): A function can be defined from its properties (propositions about its inputs and outputs), not only operationally, keeping both, and whether it is univocal or not. *function by properties and operation*
- `L-implementation-of-concept` (Luciano, 2 rows): A Luthier definition should determine univocally that a concrete calculation is an implementation of a concept (e.g. of matrices). *implementation of a concept*
- `L-non-univocal-functions` (Luciano, 2 rows): The language itself should let one model non-univocal functions, i.e. functions with error, samples, from the start. *non-univocal functions, samples*
- `L-concept-first` (Luciano, 3 rows): The first step is to express concepts in Luthier with conceptual depth; the translation and implementation come later, even if hard. *concept first*
- `L-context-as-dag` (Luciano, 9 rows): The context/program is modeled as a Directed Acyclic Graph of definitions where types depend on other types, and Luthier operates over that DAG. *context as DAG*
- `L-double-definition-cartesian` (Luciano, 5 rows): The compiler could verify that no type is defined twice, or allow a double definition read as a cartesian product (running two ways), flagged as a warning. *double definition as implementations*
- `L-expressivity-vs-redundancy` (Luciano, 6 rows): A philosophical choice between redundancy (robustness) and expressivity; expressivity is preferred, with good compiler messages making up for lost robustness. *expressivity over redundancy*
- `L-forward-undefined-types` (Luciano, 3 rows): Allow referring to a type not yet defined and defining it later; a type never defined is a program input. *forward undefined types*
- `L-implicit-types-solutions` (Luciano, 2 rows): Types can be defined implicitly, as the solution to a problem or the optimum of a function, instead of declared directly. *implicit types as solutions*
- `L-simplify-dependent-composition` (Luciano, 3 rows): A key engineering problem is a mechanism to simplify the composition of dependent types to something informative, without dragging the whole history. *simplify dependent composition*
- `L-simplifying-algebra-monoid` (Luciano, 3 rows): The typing must simplify through an algebra that is not a free monoid but some monoid keeping the resulting type's complexity bounded. *simplifying algebra, not free monoid*
- `L-reject-crude-truncation` (Luciano, 2 rows): If Luthier has dependent types it must have a well-defined algebra of dependent types; crude truncation or arbitrary forgetting is not acceptable. *reject crude truncation*
- `L-type-as-history` (Luciano, 3 rows): What a value's type holds is the history of how you arrived at it, the functions applied to reach it. *type as history*
- `L-forgetting-functions-vary` (Luciano, 4 rows): There are several forgetting functions, each optimizing different things, so understanding their properties and which to use for what is an engineering challenge. *forgetting functions vary*
- `L-selective-forgetting` (Luciano, 1 rows): Selective forgetting can be applied to the history accumulated in a type via a non-invertible function that discards part of the information. *selective forgetting*
- `L-commuting-squares` (Luciano, 7 rows): Forgetting is analyzed with commuting squares (equivalence quadrilaterals): forgetting then applying functions must equal applying functions then forgetting, the two paths compared for equivalence. *commuting squares law of forgetting*
- `L-express-alternatives` (Luciano, 6 rows): The point is not to do everything but to have the tools to express different alternatives; no option is best or worst, each has its use, even to convince yourself something is useless. *express alternatives, even to discard*
- `L-invent-rules-optimize` (Luciano, 2 rows): Since Luciano invents the language, its rules follow what he wants, so he can optimize the rules to make working on Luthier easy. *invent rules to optimize work*
- `L-commutative-statements-design` (Luciano, 4 rows): Make statements commutative so their order doesn't change the result, simplifying composition and manipulation of programs, at the cost of some expressivity. *commutative statements design*
- `L-model-time-as-dependency` (Luciano, 4 rows): Time (the order of things) in Luthier is modeled as dependency between definitions, the mathematical way: if one thing depends on another, there is a time. *time as dependency*
- `L-three-primitives-types-terms-paths` (pasted, 1 rows): The paper-and-pencil core of Luthier reduces to three logical primitives: Types, Terms and Paths. *three primitives types terms paths*
- `L-delegation-easy` (Luciano, 2 rows): Luthier should make delegation easy. *delegation easy*
- `L-modelica-spec-without-implementation` (Luciano, 1 rows): Luthier draws on Modelica, a specification of a program without its implementation, separating what is wanted from how it is implemented. *Modelica spec without implementation*
- `L-description-first` (Luciano, 5 rows): Luthier does execute, but its emphasis and first stage is describing the problem, the functions and their conditions, not execution; it could even be a dead language that only describes. *description first, execution second*
- `L-levels-of-equivalence` (Luciano, 2 rows): A fundamental idea of Luthier is to express the different levels of equivalence (same information, isomorphic, exactly equal, same memory location), each depending on a different equivalence functor. *levels of equivalence*
- `L-equivalence-separates-essence-decoration` (Luciano, 1 rows): Function equivalences separate what is essential (the equivalent) from decoration (efficiency, cost), which is what is not equivalent. *equivalence separates essence from decoration*
- `L-core-few-native-primitives` (Luciano, 1 rows): Luthier should have a core in which all its operations execute, with only a few primitives implemented in C or similar so it runs. *core with few native primitives*
- `L-facilities-not-direct-translation` (Luciano, 2 rows): Luthier does not translate to other languages directly but provides the facilities so functions and equivalences can be mapped and compiled to C, C++ or Java and extended by others. *facilities not direct translation*
- `L-no-execution-until-defined` (Luciano, 2 rows): Code is not executed until it is fully defined, so undefined dead code can sit there without bothering anyone. *no execution until defined*
- `L-code-many-operations` (Luciano, 2 rows): Luthier code is not merely compiled and run; many operations can be applied to it: verify, compile, run and others. *code admits many operations*
- `L-mean-is-forgetful-functor` (Luciano, 2 rows): A mean is a kind of forgetful functor, a mechanism that summarizes information by discarding detail. *mean as forgetful functor*
- `L-express-then-choose-method` (Luciano, 1 rows): A design method: first express something well in the language, which lets you express both hits and errors, and then choose the hits. *express then choose*
- `L-pencil-and-database-two-layers` (Luciano, 4 rows): A pencil-and-paper language and one needing a database of empirical runs are not opposite philosophies but two layers or moments: you express the ideas with pencil and paper and then go to execution and the database. *pencil and database as two layers*
- `L-quantifiers-first-class` (Luciano, 3 rows): The logical quantifiers 'for all' and 'exists' must be first-class citizens of Luthier. *quantifiers first class*
- `L-language-for-defining-ideas` (Luciano, 3 rows): Luthier is a language for defining things, where ideas are first-class citizens, like natural languages such as Spanish or English. *language for defining ideas*
- `L-generic-iteration-status-class` (Luciano, 3 rows): Iteration and status are concepts more general than their version in a particular algorithm, so there can be a generic status or iteration class, the instance knowing its algorithm from the context it sits inside. *generic iteration/status class*
- `L-independent-vs-bound-concepts` (Luciano, 3 rows): Some concepts can live independently of their container (a mean, separable from the variance) while others are intrinsically bound (an iteration is always the iteration of an algorithm). *independent vs bound concepts*
- `L-record-as-relational-database` (Luciano, 3 rows): What a record is can be stored as a relational database: fields with elements and relations, a record being a subset of the cartesian product with duplicates removed. *record as relational database*
- `L-forget-as-projection` (Luciano, 4 rows): A first form of the forget function: get_iteration drops the whole context and leaves a bare iteration; forgetting is a projection onto an axis, a reduction of dimensionality. *forget as projection*
- `L-rejoin-projections-recover` (Luciano, 4 rows): The projections can be rejoined to recover the original object; the interesting case is disjoint or complementary (orthogonal) projections, reconstructible by pullback. *rejoin projections to recover*
- `L-error-as-remembering` (model, 2 rows): Error messages are the opposite of forgetting, a well-structured remembering of why one erred, a comonad dual to the forgetful functor. *error as remembering, comonad*
- `L-platform-sharing-wins` (Luciano, 3 rows): Luthier is a platform where sharing your information makes you win, because the act of sharing raises the value of your own information. *platform where sharing wins*
- `L-data-upload-reciprocity` (Luciano, 2 rows): The minimal reciprocity of uploading your datum: the database gains your datum and you learn where you stand relative to the rest. *data upload reciprocity*
- `L-error-management-guarantees` (Luciano, 1 rows): The point of Luthier is that error management be better and results be guaranteed. *error management and guarantees*
- `L-value-knows-operation` (Luciano, 2 rows): A value knows the concrete operation that produced it: if it is the sum, it is the sum and not the generic magma operation. *value knows its operation*
- `L-views-of-operations` (Luciano, 1 rows): From a series of operations one can take different views or levels: the magma, the result, the execution, the code. *views of operations*
- `L-luthierize-foreign-code` (Luciano, 2 rows): Luthier annotates foreign code (luthierizes it), e.g. matrix-inversion libraries, starting from the definition of what the function should do and the property it must satisfy. *luthierize foreign code*
- `L-properties-hold-within-error` (Luciano, 1 rows): Declared properties (like an inverse recovering the value) hold only within a certain error, since inverse functions are not perfect. *properties hold within error*
- `L-value-as-interval-sample` (Luciano, 2 rows): A value is really an interval of values or a sample of values (as a Markov chain represented by a sample). *value as interval or sample*
- `L-precision-depends-on-history` (Luciano, 1 rows): The recoverable precision of a value depends on how much of its operational history is kept; forgetting the operation turns an exact value into an interval. *precision depends on kept history*
- `L-code-follows-laws-not-floats` (Luciano, 2 rows): Floating-point numbers do not obey the algebraic laws of numbers, but the code is assumed to, so it can be reorganized for a more efficient or more perfect execution. *code follows laws, not floats*
- `L-language-ai-uses` (Luciano, 2 rows): Luthier should be a language used by the AI itself, not only by a human. *language the AI itself uses*
- `L-execution-as-forgetting` (Luciano, 2 rows): Execution is a forgetful function: code generates code, with two levels, one that keeps the generated code and one that forgets it. *execution as forgetting*
- `L-example-before-principle` (model, 1 rows): No principle enters the specification without an example worked by hand in the candidate notation; the canonical cases test whether there is a language. *example before principle*
- `L-grows-to-universe-risk` (Luciano, 3 rows): Luthier risks accumulating without advancing and diffusing until it encompasses the whole universe, becoming useless; it must stay operative and practical. *stay operative, not grow to universe*
- `L-universal-yet-semantic` (Luciano, 3 rows): Luthier should be algebraically universal (able to write almost anything, like a universal Turing machine) while every element is semantically defined and human-understandable. *universal yet semantic*
- `L-code-mathematical-equivalence` (Luciano, 1 rows): A Luthier code has a clear mathematical equivalence. *code has clear mathematical equivalence*
- `L-program-composition-harmonic` (Luciano, 2 rows): The fundamental problem is how Luthier programs connect and expand one another so they compose and grow harmonically. *programs compose harmonically*
- `L-compile-detects-incompatibility` (Luciano, 3 rows): Compiling checks whether code contains incompatibilities (errors); many programs must be non-compilable, unlike an algebraic calculation where any expression computes something. *compile detects incompatibility*
- `L-universal-adapter` (Luciano, 3 rows): Using a library requires it to follow patterns and satisfy propositions defined from Luthier, and an adapter fits each library to the use, so Luthier works as a universal adapter between libraries. *universal adapter between libraries*
- `L-closed-vs-open-world` (model, 1 rows): Luthier verifies a closed world at compile time; for open-world field data, invariants are required at creation of derived objects but observed data gets a validation with a verdict, never a rejection. *closed vs open world verification*
- `L-derived-is-proof-term` (model, 1 rows): A derived object (inputs, function, parameters, result) is a proof term whose type is the proposition that the result was obtained that way, so the database is a store of proofs. *derived object is a proof term*
- `L-precondition-is-type` (model, 2 rows): A precondition is guaranteed by the argument's type, verified when the reference is formed; predicates on values require refined types, and a function failing its postcondition yields a stored failed-attempt object. *precondition is a type*
- `L-verify-by-sampling` (model, 1 rows): Luthier verifies postconditions by sampling possible inputs, and postcondition verification and coverage calibration are the same computation. *verify by sampling*
- `L-original-vs-derivative-types` (Luciano, 2 rows): There are original types generated from audios and questionnaires; all other types are derivative (results of functions) and therefore necessarily structured. *original vs derivative types*
- `L-function-must-be-deterministic` (model, 1 rows): If identity is (inputs, function, version, parameters), the function must be deterministic: the seed and everything from the environment enter as explicit arguments, or the certificate lies. *function must be deterministic*
- `L-never-edit-derived` (model, 1 rows): A derived object is never edited; corrections are new human assertions (originals), so labels, quality control and corrections all land in the same place. *never edit a derived object*
- `L-butler-of-knowledge` (Luciano, 2 rows): Luthier is used together with the AI as a kind of butler of knowledge. *butler of knowledge*
- `L-must-be-useful` (Luciano, 2 rows): Luthier must be useful and take root in something real, not stay purely theoretical, used at a rough level to hit reality and reveal its limits. *must be useful*
- `L-usefulness-gap` (Luciano, 2 rows): Find the gap of usefulness, a concrete place from which Luthier can begin to develop while being useful. *find the usefulness gap*
- `L-bootstrap-pact` (model, 3 rows): The only non-Luthier thing is the bootstrap pact: an implementation (in C or anything) accepts a Program value and mechanically applies the rules until eval runs on itself, after which the bootstrapper can be thrown away (self-extensibility). *bootstrap pact, self-extensibility*
- `L-core-five-pieces` (model, 2 rows): The core is five pieces: the definition (with the hole), lambda calculus with reduction, U, Π and data; from data come Σ, =, ⊥, ⊤, N, Program, and Bayes, the run database and numbers-with-error stay outside as libraries. *core in five pieces*
- `L-defeq-vs-identity` (model, 2 rows): "True by definition" is the definitional equality ≡ (two terms reducing to the same normal form, a judgment the reducer decides), distinct from =, the identity type ("true with evidence") whose terms are paths. *defeq vs identity type*
- `L-definition-is-fundamental` (model, 2 rows): The most fundamental element of a Luthier program is the definition (name : Type := term); a program is a finite unordered set of definitions and the DAG comes from which names each uses. *the definition is the atom*
- `L-forget-is-fst-sigma` (model, 1 rows): Forgetting is fst of a Σ; what to forget is library policy. *forget is fst of a sigma*
- `L-name-reference-not-address` (model, 1 rows): The name is the reference; the memory address is a decoration of the lowest level of equivalence, and without mutation or time a pointer has nothing to distinguish. *name is reference, address a decoration*
- `L-primitives-are-formers` (model, 2 rows): The primitives are the type formers (U, Pi, data), not elementary types or functions; N is defined with data, R is a structure with axioms, seno is a hole. *primitives are the type formers*
- `L-program-data-no-selfhack` (model, 1 rows): Program is an inductive type (a list of definitions) and eval is a partial function Program→Name→Maybe Term; there is no eval that injects arbitrary terms into the type system, which prevents self-hacking. *program as data prevents self-hack*
- `L-refl-test-is-code` (model, 1 rows): The rule tying ≡ and = (if a≡b then refl types as a=b) makes it literal that the test is the code itself: testing an instance is reducing and seeing refl types, proving the ∀ is building the path. *refl makes the test the code*
- `L-core-vs-surface-syntax` (model, 1 rows): A minimal ontological core (what the evaluator understands) must be strictly separated from the surface syntax and sugar. *core vs surface syntax*
- `L-hole-in-term-goal` (model, 1 rows): A hole inside a term lets the verifier accept what is written and report the exact type of what is missing (Agda's goal), which is the compiler with good messages about what is happening. *hole in a term as goal*
- `L-hole-no-intention` (model, 2 rows): The bare hole does not mark intention (whether a bodyless function will be filled by numpy or is just unwritten); the core need not distinguish, and huecos:Program→List Name lists all, intention going in the definition's text field. *hole does not mark intention*
- `L-language-indicates-knowledge` (Luciano, 5 rows): Luthier is a language that indicates knowledge: a:A is a judgment, not a proposition, read in Martin-Löf's sense where its meaning depends on which kind of type A is and a bodyless hole is an epistemic assumption. *language that indicates knowledge, judgments*
- `L-evidence-in-sigma-erasable` (model, 2 rows): "More specific with types" means types are data and knowledge about a value is carried as an evidence component in a Σ marked erasable (like a refinement type), but in Luthier the evidence is sometimes written and kept, and who defines marks it erasable, not the language. *evidence in sigma, erasable*
- `L-know-that-vs-which` (model, 2 rows): The distinction to keep from HoTT is knowing that (a mere proposition's proof) versus knowing which (a set's value); the passage from the second to the first is truncation, the most basic forgetting, where the forget functor begins. *know-that vs know-which, truncation*
- `L-syntax-decl-instant` (Luciano, 2 rows): Reduce Luthier's syntax to only declarations and instantiations. *syntax only declarations and instantiations*
- `L-no-parameterless-lambda` (model, 2 rows): A parameterless lambda should not exist in Luthier: without time or effects \(){a+a} and a+a are the same value, a consequence of the commutativity of statements. *no parameterless lambda*
- `L-coloneq-act-vs-defeq` (model, 2 rows): := is the act that gives a name a body, while ≡ is the relation following from all the := plus the computation rules (lambda substitution, recursor rules); each := gives a ≡ but ≡ is larger, so "true by definition" broadly is true by unfolding and computing. *:= act vs defeq relation*
- `L-fa-three-data` (Luciano, 4 rows): An application f a is three data all used, visible only when the program looks at its own code: the unevaluated term (code), the normal form (result), and the run f a→a+a as a term of an inductive Traza type; inside a program f a and a+a are ≡ by referential transparency. *f a is three data, code/result/trace*
- `L-confluence-traces-paths` (model, 2 rows): Since ≡ is confluent, the order of reduction steps affects only cost and termination, not the result; two traces from f a to a+a are two paths between the same points, the finest grain of "different paths with different speed". *confluence, traces are paths*
- `L-eval-two-versions-forget` (model, 1 rows): eval has two versions, the two levels of execution: eval_r returns result and run, eval_o forgets the run with fst; the order of forgetting is run, then result-with-proposition, then result alone. *eval two versions, one forgets*
- `L-unevaluated-syntactic` (model, 1 rows): "Unevaluated" is not a runtime state like a thunk because there is no time; it is a syntactic datum, which eliminates lazy-evaluation semantics. *unevaluated is syntactic, no time*
- `L-eval-fuel-total` (model, 2 rows): eval repeating a step is not structural recursion and does not always terminate, so the honest exit is fuel, eval:N→Program→Term→Maybe Term, making it total, and "how much fuel was needed" is the first cost measure, for free. *fuel makes eval total and measures cost*
- `L-invariant-tied-to-function` (model, 2 rows): An invariant can be tied to f two ways: as a separate definition f_inv (a hole until proven, the declaration being the test and filling it the proof) or as a package F:=(h:A→B)×(...) where the guarantee travels with the function. *invariant tied to function two ways*
- `L-verification-levels` (model, 3 rows): The verification levels are the same declaration with different degrees of body: running the test on a sample is empirical, filling the cases for all x is formal, and in between goes the statistical extension (a sample with its size as evidence of a ≈ type). *verification levels*
- `L-laws-as-holes-falsifiable` (model, 3 rows): Laws are declarations like any other, holes until proven and falsifiable by an instance that does not type, and a conditioned law can go either as a hypothesis in the type (total function, partial guarantee) or as a restriction in the function (partial function, total guarantee). *laws as holes, falsifiable*
- `L-redundancy-crosses-coloneq` (model, 3 rows): There are two kinds of redundancy: the one crossing the := (type says one thing, body another, verifier checks they match) is what gives something to verify; the one repeated on the same side is removable with sugar. *redundancy across := is what verifies*
- `L-invariant-is-bool-function-v0` (model, 3 rows): For numeric tests the proof layer (=, refl, induction) need not exist in version 0: an invariant is just a function returning Bool, with an input generator (a hole the environment fills by type) and a run storing the result, and the function's laws are a list of Bool functions, a field of Def. *invariant is a function to Bool*
- `L-laws-few-lines-requires` (Luciano, 3 rows): Express a function's laws in few lines borrowing the C++ requires form: a block with quantified variables in the header and one Bool expression per line, where unlike C++ a line can be a type requirement (checked by the verifier without running) or a value requirement (run by the test). *laws in few lines like requires*
- `L-subtype-cast-asymmetry` (model, 1 rows): Going to the supertype is free (fst, forgetting the guarantee); going from a type to its subset requires checking the predicate, a cast with content that verifies or fails. *subtype cast asymmetry*
- `L-no-value-without-check` (model, 2 rows): There is no way to have a value of a refined type without the predicate having been evaluated or proved; the type is written as a refinement and checked at construction, placing Luthier between Ada-style range types and dependent types. *no value without check*
- `L-law-structure` (model, 3 rows): A law is a type of arguments plus a predicate over them that takes the function under test as argument and returns the two sides rather than a bare Bool, so the counterexample explains itself; its failure is a reified application. *law returns both sides*
- `L-laws-force-decisions` (model, 2 rows): Writing out the laws forces deciding under-specified behaviour (such as what read returns for an absent key), which is exactly what the laws are for. *laws force under-specified decisions*
- `L-check-value-vs-function` (model, 3 rows): Checking a value is a computation decided by evaluating it; checking a function is an experiment that must be sampled; Luthier treats both as the same construct operation, one exact and one statistical. *check value vs check function*
- `L-certificate-composable` (model, 2 rows): The certificate is a first-class value carrying its guarantee level, composable and forgettable: it is a clause with hypotheses, a program's certificate is the closure of such clauses, and composed material is the chained forgetting. *certificate composable and forgettable*
- `L-pattern-prior-art` (Luciano, 4 rows): The pieces exist separately (Eiffel contracts, QuickCheck, dependent types, proof-carrying code); the novelty is one pattern for values, functions and whole programs, with the certificate as a first-class composable forgettable value and runs persisted as program data. *novelty is one pattern for all*
- `L-parametrizable-requirements` (Luciano, 2 rows): No language has distribution units that come with a set of requirements they must satisfy; in the pattern this is direct because the predicate is a function taking parameters (max error, scalability), so the certificate states which parameters are met and dependent libraries inherit them. *parametrizable requirements*
- `L-ev-graph-object` (Luciano, 8 rows): The object storing (function, argument, result) is the graph of the evaluation, Ev f := (x:A) x (y:B) x (f x = y), with sugar to evaluate and store the triple (which the context cannot infer, so it must be marked), and the runs database is a list of these. *ev graph object, runs as data*
- `L-lambda-is-forall` (model, 1 rows): A quantified law needs no for-all symbol: the lambda's typed parameters are the 'for all', and a law is a function to Bool whose parameters are the quantified variables. *lambda parameters are the for-all*
- `L-subtype-assignment-runs-tests` (model, 1 rows): Assigning to a subtype (resta:Resta:=sub) forces the verifier to run the cases at compile time; the alternative is leaving it as a declared hole until an explicit test. *subtype assignment runs tests*
- `L-setbuilder-prior-art` (Luciano, 4 rows): Set-builder subtype notation exists in Coq, Lean, F*, Z and even Python's comprehensions, but mainstream languages omit it because deciding the predicate needs a solver, a proof or a runtime check; Luthier's fourth way tests with n cases recorded in the certificate, letting the predicate be any function to Bool. *set-builder prior art and the fourth way*
- `L-setnotation-vindicated` (Luciano, 3 rows): Though Luthier aimed to be a modern HoTT language it ends up using primary-school set-builder notation, which is fine: that notation denotes a Sigma and category theory itself generalizes rather than contradicts sets, with the subtype defined by the mono forget arrow. *set notation denotes a sigma*
