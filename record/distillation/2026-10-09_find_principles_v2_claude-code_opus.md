# Candidate principles of Luthier, found blind, 2026-10-09

Written by `scripts/find_principles.py` (find_principles v1). Prompt `find_principles_v2` (sha256 5eb0cb1b3e6b),
model opus at effort low via claude-code (2.1.197 (Claude Code)); the model saw only the
lineages and the criterion of infectability.
Inputs by sha256: `record/ideas/lineages_link_ideas_v1_claude-code_opus.json` 3b2b5d5a4745; `record/ideas/timeline.jsonl` b18b5806955d.
Each candidate shows apart what the script took from the rows and what is the model's reading.

Lineages: 725; candidate 33, considered 321, not_principle 371.

## Candidates

```
C1  A type is the proposition its values must satisfy, extended to functions whose type is their
    laws, so membership is a guarantee.
Instead of: types as mere storage shapes or tags with no semantic content
Scope:      language
-- from the rows, by the script
Quote:      "los tipos tienen que ser conceptos, tipos como proposiciones y los tipos incluyen
            también funciones, funciones y funciones de orden superior"
Said by:    Luciano, 2026-05-26 12:33
Source:     WhatsApp Ptt 2026-05-26 at 12.32.24.md [00:38] (row day:2026-05-26:tipos-como-conceptos-y-proposiciones)
Lineages:   L-type-carries-its-laws, L-types-are-concepts, L-no-principle-without-example,
            L-unit-is-group-of-functions, L-theory-is-record, L-own-contributions-vs-precedents,
            L-things-guaranteed
Witnesses:  first 2022-06-15 by Luciano; 40 witnesses over 14 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. collapsing type, test and proposition into one thing reorganizes what it
            means to define anything, so a function's type is the law it obeys.
Also:       ethical. it takes a stance: belonging to a type must mean a guarantee, not a mere tag.
Harms:      punishes code whose guarantees cannot be stated as laws
Harms:      can make every definition carry proof obligations it does not need
Harms:      excludes quick prototyping where a bare value suffices
Beats:      L-compile-time-prevents-invalid (The type system prevents invalid models from being
            constructed, eliminating consistency violations at compile time before execution or
            inference.). compile-time rejection of invalid models is one consequence of the same
            idea, stated narrowly for one domain rather than as the organizing rule.
Above next: It is the frame every other principle presupposes; code-as-data is powerful but serves
            this, not the reverse.

C2  Code is a datum of the language itself, so a program can be built, inspected and run by other
    programs, and Luthier operates on Luthier.
Instead of: a fixed boundary where source is compiled once and never seen as a value
Scope:      language
-- from the rows, by the script
Quote:      "La idea de que el codigo sea dato es muy, pero muy fuerte en cuanto a la flexibilidad
            que ofrece pero es notable que los lenguajes modernos no sigan ese camino Lispeano."
Said by:    Luciano, 2022-06-15 08:55
Source:     2022-06-15 Sin título 2 .md line 13 (row written:2022-06-15_sin-titulo-2:codigo-es-dato)
Lineages:   L-code-is-data, L-meta-recursive, L-term-is-data-syntax
Witnesses:  first 2022-06-15 by Luciano; 24 witnesses over 12 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. erasing the code/data line lets the language operate on itself, so the
            interpreter, the trace and the verifier all become ordinary data.
Also:       emotive. he returns to it for fifteen years as the move that gives flexibility no modern
            language takes.
Harms:      homoiconicity invites self-hacking if eval injects arbitrary terms
Harms:      a program manipulating its own code is harder to reason about
Harms:      blurs a distinction many programmers rely on for safety
Beats:      L-first-class-contexts (The context could be treated as a type in itself, what theory
            calls first-class contexts.). first-class contexts are one technical realization of
            code-as-data, a narrower consequence than the general erasure of the distinction.
Above next: It is the mechanism that makes the construction pattern reusable across values,
            functions and whole programs alike.

C3  From a type and a predicate over it, derive a certified subtype, a validating constructor and
    the projection back, the one pattern for values, functions and programs.
Instead of: ad hoc validation scattered at call sites, separate from the type
Scope:      language
-- from the rows, by the script
Quote:      "este tipo Almacen que en realidad confunde dos cosas el constructor de almacen y el
            almacen es el concepto fundamental de Luthier (no almacen sino el patron de
            construccion)."
Said by:    Luciano, 2026-09-29 06:00
Source:     2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 58 (row dialogue:175c0408:patron-de-construccion-concepto-fundamental)
Lineages:   L-construction-pattern-is-core, L-ten-elements, L-certificate-first-class
Witnesses:  first 2026-09-29 by Luciano; 13 witnesses over 2 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. one pattern (material type plus predicate yields certified type, validating
            constructor and forgetful projection) is read as the single core act the whole language
            is built from.
Also:       aesthetic. economy: the same construction serves values, functions and programs, with
            the subtype and its constructor two uses of one predicate.
Harms:      every construction forced through a predicate check has a cost per build
Harms:      a value you just want cheaply must pay the pattern
Harms:      overgeneralizing one shape risks hiding domain differences
Beats:      L-pre-postconditions (Functions and types are defined by preconditions and
            postconditions, the postconditions defining the subtype.). pre/postconditions are the
            same idea seen through one feature; the construction pattern names the general act they
            are instances of.
Above next: It is the operative core where C1 becomes a mechanism; characterizing by the best object
            (next) is how its predicates should be written.

C4  For each concept find the mathematical object that best represents it and put it as the type's
    invariant, characterizing an operation rather than reproducing its implementation.
Instead of: laws that just restate what the fast code does (consistency, not characterization)
Scope:      language
-- from the rows, by the script
Quote:      "La idea en realidad es buscar el objeto matematico que mejor lo represente y decirlo."
Said by:    Luciano, 2026-10-05 00:35
Source:     2026-10-04_52d3e68e_lee-la-ultima-trascripcion-de-audio.md turn 128 (row dialogue:52d3e68e:buscar-el-objeto-matematico-y-ponerlo-como-invariante)
Lineages:   L-best-math-object-as-invariant, L-law-characterizes-not-reimplements
Witnesses:  first 2026-10-05 by model; 8 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  ethical. it says a law must state the property that determines an operation up to
            equality, not re-run its implementation, which is a discipline about what counts as a
            real invariant.
Also:       conceptual. choosing the invariant of the concept's type reframes every definition as a
            search for the object that represents it.
Harms:      finding the best mathematical object is slow and may never settle
Harms:      a wrong characterization is worse than an honest reimplementation
Harms:      demands math literacy the everyday coder may lack
Beats:      L-levels-of-equivalence (A fundamental idea of Luthier is to express different levels of
            equivalence (same information, isomorphic, exactly equal, same memory location), each a
            different equivalence functor.). levels of equivalence name distinctions this principle
            uses, but do not carry the imperative to characterize rather than reimplement.
Above next: It tells you what to write in the laws; execution-as-verification (next) tells you what
            running them means.

C5  Luthier first describes the problem and its equivalences and only then executes; execution is
    the verification of those equivalences, as mathematics verifies rather than runs.
Instead of: a language whose primary act is to compile and run code
Scope:      language
-- from the rows, by the script
Quote:      "Hay una idea, que la matemática no ejecuta, porque lo único que hace es verificar
            equivalencias. Entonces, bueno, sí, la ejecución en Luthier sería esa verificación de
            equivalencias"
Said by:    Luciano, 2026-05-30 18:03
Source:     WhatsApp Ptt 2026-05-30 at 18.01.53.md [01:47] (row day:2026-05-30:matematica-no-ejecuta-verifica-equivalencias)
Lineages:   L-execution-is-verification, L-declarative-and-optimizer, L-path-equivalence-core
Witnesses:  first 2026-05-26 by Luciano; 10 witnesses over 4 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. reading execution as mathematics does, verifying equivalences, inverts the
            usual picture: the program describes and the run certifies, with a declarative and an
            executive side.
Also:       aesthetic. the whole language reduces to stating equivalences and then checking them,
            one idea doing double duty.
Harms:      treating execution as verification downplays the real cost of running
Harms:      delegating execution risks a gap between what is checked and what runs
Harms:      a declarative-first stance can stall before anything executes
Beats:      L-two-layers (Luthier has two layers: a first of equivalences and verifiability, and a
            second that measures time, complexity, resources and success/failure and picks the
            faster of two equivalent paths.). the two-layer split (equivalence, then cost) is the
            architecture this principle implies, stated as a feature rather than as the governing
            idea.
Above next: It frames why minimalism matters: a describing language needs only a tiny core to run by
            hand.

C6  Keep the native core to a handful of primitives, self-extensible and executable by hand, and
    build every complex concept on top of it.
Instead of: a large built-in language with syntactic sugar and many primitives
Scope:      language
-- from the rows, by the script
Quote:      "Luthier tendría que ser ejecutable a mano es decir que uno pudiese con l y papel
            escribir las cosas"
Said by:    Luciano, 2026-05-29 14:14
Source:     2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 7 (row dialogue:20260529T1400:ejecutable-a-mano)
Lineages:   L-self-extensible, L-executable-by-hand, L-minimalism-maximalism, L-minimal-primitives
Witnesses:  first 2026-05-27 by Luciano; 17 witnesses over 7 days
-- the model's reading (opus, effort low)
Strongest:  aesthetic. the demand that a well-written Luthier be executable by hand with pencil and
            paper is an austere standard of economy that shapes every primitive.
Also:       ethical. a stance on what a language should be: small, self-extensible, with the
            minimalism in the founding components and the maximalism built from them.
Harms:      few primitives push complexity into libraries that grow unwieldy
Harms:      executable-by-hand can conflict with the speed real work needs
Harms:      self-extensibility is a bootstrap burden before anything else
Beats:      L-bridge-language (Luthier should be minimal, essentially a bridge language connecting
            other languages.). bridge language is one motive for minimalism; the executable-by-hand
            standard is the sharper, more infectious formulation of the same drive.
Above next: It bounds the machinery so that expressing the invariances of the disciplines (next)
            stays within a readable core.

C7  Luthier is an abstraction mechanism whose aim is to express the invariances of the disciplines
    clearly.
Instead of: a language organized around computation rather than meaning
Scope:      language
-- from the rows, by the script
Quote:      "la idea de luthier es expresar invarianzas de los de las disciplinas"
Said by:    Luciano, 2026-05-29 14:29
Source:     2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 11 (row dialogue:20260529T1400:expresar-invarianzas-de-disciplinas)
Lineages:   L-express-invariances, L-abstraction-mechanism
Witnesses:  first 2026-05-29 by Luciano; 8 witnesses over 3 days
-- the model's reading (opus, effort low)
Strongest:  emotive. it names what moves the author to invent the language: a relator of
            invariances, against the statistical predictor, a species mates within itself, electrons
            are fermions.
Also:       conceptual. reframing a language as a mechanism to express the invariants of a field,
            not to compute, opens a different purpose for programming.
Harms:      aiming to express every discipline's invariances risks growing to encompass the universe
Harms:      invariance-hunting can detach from any usable program
Harms:      what counts as an invariance is itself a hard judgment
Beats:      L-language-of-ideas (Luthier is a language for defining ideas, where ideas are
            first-class citizens, like natural languages define things.). language of ideas is the
            same aspiration one level more abstract; expressing invariances is the concrete, more
            infectious version of it.
Above next: It gives the purpose; the hole (next) is the concrete device that lets an unexpressed
            invariance sit contained until filled.

C8  A declaration without a body is a first-class hole, an opaque name that does not reduce, and
    nothing executes until it is defined.
Instead of: treating a missing definition as a compile error
Scope:      language
-- from the rows, by the script
Quote:      "porque necesitamos el simbolo para el hueco, ?. No basta con decri f: A-> B y no
            definirlo?"
Said by:    Luciano, 2026-09-29 04:20
Source:     2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 3 (row dialogue:175c0408:por-que-simbolo-hueco)
Lineages:   L-hole-five-roles, L-hole-needs-no-symbol, L-luthier-v0-limits
Witnesses:  first 2026-09-28 by model; 7 witnesses over 3 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. a bodyless declaration plays axiom, program input, external function,
            pending definition and dead code at once, so one construct absorbs five roles usually
            kept apart.
Also:       aesthetic. no symbol is even needed: f : A -> B left undefined is already the hole,
            economy at its sharpest.
Harms:      holes everywhere can hide how much is actually undefined
Harms:      deferring bodies invites programs that never become executable
Harms:      a first-class gap complicates reasoning about totality
Beats:      L-forward-and-undefined-types (A type may be referenced before it is defined and defined
            later, or left undefined, in which case it is a program input.). forward and undefined
            types are the behavior the hole generalizes; the hole states it as one first-class
            citizen rather than a pair of cases.
Above next: The hole marks what is not yet known; paths (next) organize the many ways a known
            function can be done.

C9  A function has many equivalent implementations (paths), each with its precision and cost, and
    Luthier chooses among them by expected loss and speed.
Instead of: one fixed implementation bound to a function name
Scope:      language
-- from the rows, by the script
Quote:      "una funci esta funci puede ser implementada de muchas maneras, son los distintos paths y
            cada forma tiene una precisión y una velocidad"
Said by:    Luciano, 2026-05-26 12:33
Source:     2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 1 (row dialogue:20260526T1233:luthier-paths-con-precision-y-velocidad)
Lineages:   L-paths-implementations, L-path-cost-estimate
Witnesses:  first 2026-05-26 by Luciano; 17 witnesses over 7 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. one function with many implementations (paths), each with its precision and
            speed, chosen by expected loss, turns a program into a declarative object that
            self-optimizes.
Also:       emotive. the self-optimizing language, declarative and executive at once, is the vision
            he keeps returning to with evident pull.
Harms:      many implementations per function multiplies maintenance and testing
Harms:      choosing by measured cost needs a reliable performance database
Harms:      equivalence of paths is the hardest thing to prove
Beats:      L-bayesian-complexity-estimate (The a priori complexity of implementations is estimated
            by a Bayesian strategy: give chances to different algorithms, measure their actual
            times, and estimate from accumulated experience.). the Bayesian cost estimate is the
            technique that serves path selection; the paths idea is the structural reframing it
            supports.
Above next: Choosing by expected loss only makes sense if the certificates it chooses over are
            strong, which is what sampled verification (next) must deliver.

C10  Verification is one operation, exact when it can compute and statistical when it samples, and
    every value carries the grade of guarantee it was checked to.
Instead of: a single pass/fail notion of correctness
Scope:      language
-- from the rows, by the script
Quote:      "La comprobación de un valor es un cómputo; la de una función es un experimento. Luthier
            tiene que tratar a los dos como la misma operación de construir, sabiendo que uno es
            exacto y el otro estadístico."
Said by:    model, 2026-09-29 05:56
Source:     2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 55 (row dialogue:175c0408:comprobar-valor-computo-comprobar-funcion-experimento)
Lineages:   L-check-value-vs-function, L-novel-evidence-combination, L-bayesian-verification-regime,
            L-certification-is-pointwise
Witnesses:  first 2026-09-29 by model; 16 witnesses over 4 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. treating checking a value and checking a function as one construct
            operation, exact or statistical, and reading verification as a Bayesian observer
            updating a posterior, makes the grade of guarantee part of what membership means.
Also:       ethical. it refuses to call a sampled result a proof: the certificate carries its level,
            proof and sampled at the limits of probability.
Harms:      sampled verification certifies a risk, never a universal truth
Harms:      a tuned generator can make a false law pass
Harms:      certificate and record proliferate if not pruned
Beats:      L-levels-of-verification (A value can be untested or tested, with different levels of
            verification.). levels of verification name the untested/tested distinction; the
            construct that unifies exact and statistical checking under one operation with a graded
            certificate is the more infectious formulation.

```

## Considered and left out

- `L-identifiers-central` (Luciano, 3 rows): Identifiers are central: a simple label recovers a complex object, the dictionary joining human and machine. *identifiers central as principle*
- `L-create-objects-uniformly` (Luciano, 2 rows): The language expresses and creates values, variables, types and functions uniformly, with their semantics. *uniform creation of entities*
- `L-express-extracomputational` (Luciano, 1 rows): The language expresses extra-computational concepts like probability by abstracting their properties and verifying compliance (e.g. a probability lies in [0,1]). *express extra-computational concepts*
- `L-expressiveness` (Luciano, 2 rows): Code must express its intention to both the human reader and the compiler, referring truthfully to known structures. *reasoning-code isomorphism*
- `L-semantic-then-efficient` (Luciano, 6 rows): Once semantic validity and equivalence are established, a clear slow algorithm can be replaced by an efficient equivalent one, enabling optimization. *semantic then efficient*
- `L-code-operations` (Luciano, 2 rows): The language builds in functions that operate on code: tests, errors, derivatives, finding equivalents, and timing. *code operations built in*
- `L-language-self-writing` (Luciano, 1 rows): Defining new types and functions should itself be programmable, the language writing itself, which requires a simple robust language with no syntactic sugar. *language self-writing*
- `L-subtype-by-predicate` (Luciano, 10 rows): A subtype (subObject) is the subset of a type whose values satisfy a predicate, a test. *subtype by predicate*
- `L-types-make-code-safe` (Luciano, 5 rows): Declaring a function declares the tests it must pass, so types encode preconditions and gate membership on testing, yielding self-verified programs. *types make code safe*
- `L-test-result-one-or-explanation` (Luciano, 7 rows): A check returns success (one) if met or an explanation of why it failed, not just a boolean. *test returns explanation*
- `L-express-math-structures` (Luciano, 7 rows): The language must express mathematical structures (category, functor, group) with their laws, possibly in several declaration styles. *express math structures*
- `L-learn-from-each-run` (Luciano, 1 rows): From each run of the code something is learned, whether an implementation is correct or how fast it is. *learn from each run*
- `L-pre-postconditions` (Luciano, 12 rows): Functions and types are defined by preconditions and postconditions, the postconditions defining the subtype. *pre/postconditions*
- `L-simultaneous-definition` (Luciano, 4 rows): When postconditions are interdependent, objects are defined together, in tuples with crossconditions, the one form of definition. *simultaneous definition*
- `L-forms-of-definition` (Luciano, 4 rows): The language distinguishes declaration from definition and lets one define functions or variables by their type without giving the implementation or value (parameters). *forms of definition*
- `L-compile-time-prevents-invalid` (model, 8 rows): The type system prevents invalid models from being constructed, eliminating consistency violations at compile time before execution or inference. *compile-time prevents invalid*
- `L-dsl-as-model-compiler` (model, 3 rows): The DSLs are model compilers that translate high-level mechanistic specifications into executable, inferable structures. *dsl as model compiler*
- `L-hott-dsl-for-biology` (model, 2 rows): Build a domain-specific modeling language on Homotopy Type Theory for expressing, composing and transforming biological models with access to type-level structure. *hott dsl for biology*
- `L-separate-structure-inference` (model, 2 rows): Deterministic structural validity (via HoTT) is kept separate from probabilistic inference (via Bayesian layers), probability handled downstream. *separate structure from inference*
- `L-encode-as-types` (model, 3 rows): Model components, entities and deterministic structure are encoded as types. *encode as types*
- `L-runtime-vs-semantic-safety` (model, 2 rows): Runtime safety prevents crashes while semantic safety, a layer above runtime, prevents invalid models from existing at all. *semantic vs runtime safety*
- `L-replace-adhoc-model-spaces` (model, 1 rows): Replace ad hoc model design with compositional, type-safe, generative model spaces. *replace adhoc model spaces*
- `L-contagiously-safe-dsl` (model, 5 rows): A compile-time safe model DSL whose safety is contagious, propagating through the system via the compiler, with backend codegen, as the endgame of HoTTification. *contagiously safe dsl*
- `L-tests-as-morphisms` (model, 5 rows): Each CLI operation is a typed morphism and each test a witness path or triangle identity, not a patch. *tests as morphisms*
- `L-epistemic-compression` (model, 2 rows): A few adjunction-derived tests cover most of the risk; verification is compressed into a minimal, epistemically meaningful suite. *epistemic compression*
- `L-reproducibility-formal` (model, 2 rows): The reproducibility crisis is a lack of structural verification, and reproducibility is a formal property. *reproducibility is formal*
- `L-encode-epistemic-structure` (model, 5 rows): Scientific code should encode its epistemic structure as executable epistemology, with verification semantic rather than syntactic and type safety arising from epistemic clarity. *encode epistemic structure*
- `L-snapshot-first` (Luciano, 1 rows): Before committing to tests, record snapshots and compare results outside the system to decide which tests to run. *snapshot first*
- `L-io-codec-prism` (Luciano, 6 rows): Luthier separates the IO effect (a law-less extern) from the format, a pure codec of parse and render with round-trip laws, which is a prism, the partial version of Iso. *io codec prism reversibility*
- `L-reasonable-then-wild` (Luciano, 1 rows): His method of thinking is to work out the reasonable version first, then look for the wild move. *reasonable then wild*
- `L-cross-language` (Luciano, 10 rows): Luthier is not tied to one language but a pseudo-language implementable across languages (cross-language, not cross-compiler), with its engine in one and PyLuthier/RLuthier/CLuthier transformable into one another. *cross-language*
- `L-bayesian-complexity-estimate` (model, 8 rows): The a priori complexity of implementations is estimated by a Bayesian strategy: give chances to different algorithms, measure their actual times, and estimate from accumulated experience. *bayesian complexity estimate*
- `L-butler-orchestrator` (Luciano, 7 rows): Luthier is a higher-order language, a butler that orchestrates other languages, runs programs, compares their outputs, and chooses where to run each computation. *butler orchestrator*
- `L-compiler-is-prover` (model, 2 rows): Letting functions return types makes the Luthier compiler a mathematical prover, so code and its proof become the same thing. *compiler is prover*
- `L-compose-programs` (Luciano, 1 rows): Luthier composes the input and output of one program with another, chaining external programs. *compose programs*
- `L-compare-equivalent-paths` (Luciano, 2 rows): Luthier compares two paths that do the same thing and determines they are equivalent, possibly with format-conversion stages at the start and end. *compare equivalent paths*
- `L-verifiability` (Luciano, 2 rows): Luthier must verify that a function is correct; verifiability, with equivalence, is a minimal element of the language. *verifiability*
- `L-two-layers` (Luciano, 3 rows): Luthier has two layers: a first of equivalences and verifiability, and a second that measures time, complexity, resources and success/failure and picks the faster of two equivalent paths. *two layers*
- `L-bridge-language` (Luciano, 2 rows): Luthier should be minimal, essentially a bridge language connecting other languages. *bridge language*
- `L-synthesize-runs` (Luciano, 2 rows): The accumulated run information must be synthesized over time so it doesn't grow monstrous and paralyzing. *synthesize runs*
- `L-only-types-and-functions` (Luciano, 5 rows): Luthier collapses the many constructs into a single kind: only types and functions exist, and functions are themselves a type. *only types and functions*
- `L-based-on-hott` (Luciano, 5 rows): Build Luthier to map strictly onto homotopy type theory, with very few types following its small set of well-defined rules. *based on hott*
- `L-hijack-code` (Luciano, 4 rows): Luthier must be able to hijack code from any other language. *hijack code*
- `L-probabilistic-hott` (Luciano, 10 rows): Proving path equivalence needs a probabilistic extension of HoTT, a marriage of HoTT and Bayes, with an internal prover plus empirical statistical demonstration. *probabilistic hott*
- `L-core-plus-libraries` (Luciano, 2 rows): Luthier is a closed core plus libraries, the libraries being Luthier functions that connect it to external programs. *core plus libraries*
- `L-closed-observer` (Luciano, 5 rows): Luthier is a closed, internally complete universe that observes the outside through a read/write boundary which is also a compilation. *closed observer*
- `L-external-element` (Luciano, 3 rows): Everything that is not Luthier (C++, Python, the machine, any resource) is modeled as its own kind of external element. *external element*
- `L-function-by-properties` (Luciano, 4 rows): A function can be defined by its properties, the propositions its inputs and outputs satisfy, not only operationally, keeping both. *function by properties*
- `L-nonunivocal-functions` (Luciano, 4 rows): The language must natively model non-univocal functions, functions with error, samples. *nonunivocal functions native*
- `L-concept-first` (Luciano, 1 rows): The first step is expressing concepts in Luthier with conceptual depth; the translation/implementation comes after. *concept first*
- `L-first-class-contexts` (model, 2 rows): The context could be treated as a type in itself, what theory calls first-class contexts. *first-class contexts*
- `L-expressivity-vs-redundancy` (Luciano, 6 rows): A choice between redundancy (robustness) and expressivity; he prefers expressivity with good compiler messages, since redundancy can needlessly limit. *expressivity vs redundancy*
- `L-forward-and-undefined-types` (Luciano, 3 rows): A type may be referenced before it is defined and defined later, or left undefined, in which case it is a program input. *forward and undefined types*
- `L-implicit-types` (Luciano, 1 rows): Types can be defined implicitly, as the solution to a problem or the optimum of a function, rather than declared directly. *implicit types*
- `L-forgetting-problem` (Luciano, 4 rows): The forgetting problem, controlling the typing information that grows as types compose, is one of Luthier's fundamental problems to solve. *forgetting problem*
- `L-simplify-type-composition` (Luciano, 7 rows): Simplifying the composition of dependent types needs a simplifying typing algebra, not a free monoid, that keeps the resulting type's complexity bounded; a key engineering problem. *simplify type composition*
- `L-forgetful-functors` (Luciano, 24 rows): Which forgetting function you apply to the types defines the language you speak; forgetful functors are among Luthier's most important components, and different ones optimize different things. *forgetful functors define language*
- `L-type-is-history` (Luciano, 4 rows): What a type holds is the history of how you arrived at it (e.g. a loop as a combination of types with an exponent). *type is history*
- `L-express-alternatives` (Luciano, 7 rows): The point is not to do everything but to have the tools to express different alternatives; no option is best or worst, and even expressing something to discard it has value. *express alternatives*
- `L-optimize-own-rules` (Luciano, 2 rows): Since he invents the language it follows his rules, so he can optimize the rules to make manipulating programs easy. *optimize own rules*
- `L-statements-commute` (Luciano, 7 rows): Make statements commutative so their order doesn't change the result, with temporality reconstructed from causal type dependence, trading some expressivity. *statements commute*
- `L-time-as-dependency` (Luciano, 3 rows): Time, the order of things, is modeled as dependency between definitions, the mathematical way: if one thing depends on another there is a time. *time as dependency*
- `L-easy-delegation` (Luciano, 2 rows): Delegation should be easy in Luthier, an idea he traces to Modelica. *easy delegation*
- `L-spec-without-implementation` (Luciano, 2 rows): Inspired by Modelica, Luthier separates the specification of a program from its implementation. *spec without implementation*
- `L-description-language` (Luciano, 3 rows): Luthier's first stage is a language for describing the problem, the functions and the conditions under which they work, not for execution. *description language*
- `L-levels-of-equivalence` (Luciano, 2 rows): A fundamental idea of Luthier is to express different levels of equivalence (same information, isomorphic, exactly equal, same memory location), each a different equivalence functor. *levels of equivalence*
- `L-essential-vs-decoration` (Luciano, 1 rows): Function equivalences separate what is essential (the equivalent) from what is decoration (efficiency, cost), the non-equivalent. *essential vs decoration*
- `L-minimal-core-primitives` (Luciano, 3 rows): There should be a clear core where all Luthier operations execute, with only a few primitives implemented in C or similar so it runs. *minimal core primitives*
- `L-probabilities-and-types-together` (Luciano, 3 rows): Probabilities and types should go almost together, the equivalences being probabilistic, with HoTT giving the universe over which the probabilities apply. *probabilities and types together*
- `L-map-to-other-languages` (Luciano, 1 rows): Describe functions and equivalences and map them to other languages (C, C++, Java), not directly but by giving the tools for others to extend the translation. *map to other languages*
- `L-execute-when-defined` (Luciano, 2 rows): Code is not executed until it is fully defined, so undefined dead code can sit there without bothering anyone. *execute when defined*
- `L-code-many-operations` (Luciano, 2 rows): Luthier code is not merely compiled and run; many operations apply to it (verify, compile, run), giving more complexity but more expressivity. *code many operations*
- `L-synthesis-is-key` (Luciano, 1 rows): Synthesizing information well is the key to the whole design. *synthesis is key*
- `L-express-then-execute` (Luciano, 6 rows): You first express the ideas with pencil and paper and then go to execution or the empirical database; these are two layers, not opposed philosophies. *express then execute*
- `L-quantifiers-first-class` (Luciano, 6 rows): The logical quantifiers for-all and exists should be first-class citizens of Luthier. *quantifiers first-class*
- `L-language-of-ideas` (Luciano, 3 rows): Luthier is a language for defining ideas, where ideas are first-class citizens, like natural languages define things. *language of ideas*
- `L-living-vs-dead-language` (Luciano, 2 rows): Luthier can be a living language that acts or a dead language that only describes; the descriptive role is where it starts. *living vs dead language*
- `L-syntax-semantics-before-implementation` (Luciano, 3 rows): Fix Luthier's syntax and semantics on paper first, and only then implement it. *syntax semantics before implementation*
- `L-definition-is-its-test` (Luciano, 10 rows): Defining a function defines its test (its inverse, its simulation), so running the code runs the test. *definition is its test*
- `L-error-messages-remembering` (model, 3 rows): Luthier must produce well-structured error messages, the remembering of why one erred, returning the failed sub-graph with each node's trace. *error messages as remembering*
- `L-sharing-platform` (Luciano, 5 rows): Luthier is a platform where sharing your information makes you win, because you learn where you stand relative to the rest. *sharing platform*
- `L-value-knows-operation` (Luciano, 2 rows): A value knows the concrete operation that produced it: the sum is the sum, not the generic magma operation. *value knows operation*
- `L-levels-of-verification` (Luciano, 4 rows): A value can be untested or tested, with different levels of verification. *levels of verification*
- `L-luthierize-foreign-code` (Luciano, 4 rows): Luthier annotates and 'luthierizes' foreign code, verifying it against the definition of what it should do within some error. *luthierize foreign code*
- `L-properties-within-error` (Luciano, 4 rows): The properties a function must satisfy (like an inverse recovering the value) hold only within a certain error. *properties within error*
- `L-code-obeys-laws-not-floats` (Luciano, 2 rows): Floating-point numbers do not obey the algebraic laws of numbers, but the code is assumed to, so it can be reorganized for efficiency. *code obeys laws not floats*
- `L-execution-as-forgetting` (Luciano, 3 rows): Execution is a forgetful function: code generates code, with one level that keeps the generated code and one that forgets it. *execution as forgetting*
- `L-arena-or-lambda-calculus` (Luciano, 2 rows): Luthier can grow as a universal arena or, more simply, as a down-to-earth lambda calculus. *arena or lambda calculus*
- `L-algebraic-and-semantic` (Luciano, 3 rows): Luthier should have a very algebraic way of writing itself that can express almost anything like a universal Turing machine, yet where each element is semantically defined and understandable by humans. *algebraic and semantic*
- `L-recursive-like-lisp` (Luciano, 3 rows): Luthier is imagined as a recursive language like LISP but nicer, with a clear mathematical equivalence for its code. *recursive like lisp*
- `L-compose-programs-harmonically` (Luciano, 3 rows): The fundamental problem is how Luthier programs connect and expand one another so they grow harmonically, with incompatibilities possible. *compose programs harmonically*
- `L-compiling-detects-errors` (Luciano, 2 rows): Compiling is checking whether the code holds incompatible things; unlike algebraic calculation, many programs should not compile, because that is how errors are caught. *compiling detects errors*
- `L-library-adapter` (Luciano, 3 rows): A library is used by requiring it follow patterns and satisfy propositions defined from Luthier, with an adapter fitting it to each use, so Luthier acts as a universal adapter between libraries. *library adapter*
- `L-result-type-closed` (Luciano, 2 rows): Each function declares a result type with fixed fields; the set of result types is open but every individual type is closed, a sum of types, not a JSON blob. *result type closed*
- `L-derived-is-proof-term` (model, 1 rows): A derived object, the tuple of inputs, function, parameters and result, is a proof term whose type is the proposition that the result was obtained that way, making the base a store of proofs. *derived is proof term*
- `L-precondition-is-type` (model, 1 rows): A precondition is guaranteed by the argument's type, checked when the reference is formed; preconditions that are predicates over values require refined types. *precondition is type*
- `L-verify-by-sampling` (model, 1 rows): Luthier verifies postconditions by sampling possible inputs, and postcondition verification and coverage calibration are the same computation. *verify by sampling*
- `L-original-vs-derivative-types` (Luciano, 3 rows): Some types are original (made from audios and questionnaires) and all the rest are derivative, results of functions, so they necessarily have structure. *original vs derivative types*
- `L-derived-never-edited` (model, 1 rows): A derived object is never edited; corrections are human assertions that are themselves originals, putting labels, quality control and corrections in the same place. *derived never edited*
- `L-function-deterministic` (model, 1 rows): If the identity of a derived object is its inputs, function, version and parameters, the function must be deterministic: seed and environment enter as explicit arguments, or the certificate lies. *function deterministic*
- `L-must-be-useful` (Luciano, 2 rows): Luthier must be useful and take root in something real, not stay purely theoretical, so it hits reality and reveals its limits. *must be useful*
- `L-gap-of-usefulness` (Luciano, 3 rows): The method is to find the gap of usefulness, a concrete place from which Luthier can begin to develop while being useful. *gap of usefulness*
- `L-knuth-expressive-languages` (Luciano, 1 rows): Luthier draws the most expressive and natural from lambda calculus, Lisp, C++ and Python, aiming at a language Knuth would like, with code as a first-class citizen. *knuth expressive languages*
- `L-bootstrap-pact` (model, 3 rows): The only thing outside Luthier is a bootstrap that accepts a Program value, parses it and runs eval; once eval written in Luthier runs on itself the bootstrapper can be discarded, which is the concrete self-extensibility. *bootstrap pact*
- `L-definition-fundamental` (model, 3 rows): The most fundamental element of a program is not the type or the function but the definition, name : Type := term; a program is a finite unordered set of definitions and the DAG comes from which names each uses. *definition fundamental*
- `L-definitional-equality` (model, 2 rows): "True by definition" is definitional equality ≡ (two terms reducing to the same normal form), a judgment the reducer decides, distinct from =, the identity type whose terms are paths, making "the test is the code" literal. *definitional equality*
- `L-forgetting-is-fst` (model, 2 rows): Forgetting is fst of a Σ, and what to forget is library policy. *forgetting is fst*
- `L-formers-are-primitive` (model, 2 rows): Elementary types and functions are not primitive; the primitives are the formers (U, Π, data), with N defined by data, R a structure with axioms and seno a hole. *formers are primitive*
- `L-program-inductive-eval` (model, 2 rows): Code and data in the Lisp form: Program is an inductive type and eval a partial function Program → Name → Maybe Term, with no eval injecting arbitrary terms into the type system, which prevents self-hacking. *program inductive eval*
- `L-proposition-is-type-truth` (model, 2 rows): True/false is not Bool: a proposition is a type, true if it has a term; ⊤ and ⊥ are the extremes and Bool is a datum with two constructors. *proposition is type truth*
- `L-core-library-sugar-layers` (model, 3 rows): The language is three layers: a small core (a handful of term forms plus data, definition and reduction, a ten-line EBNF with reserved words data, match, extern), a base library written in Luthier, and sugar whose translation is mechanical; no Bool, numbers, =, Sigma or Subtype in the core. *core library sugar layers*
- `L-data-sum-of-products` (model, 4 rows): A data is a sum of products plus recursion (sum between constructors, product inside each, recursion as least fixpoint), so data is primitive and + and × are its degenerate cases. *data sum of products*
- `L-language-indicates-knowledge` (Luciano, 3 rows): Luthier is thought of as a language that indicates knowledge, in Martin-Löf's reading where a judgment is an act of knowledge and the bodyless hole is an epistemic assumption. *language indicates knowledge*
- `L-judgment-depends-on-type` (model, 2 rows): a : A is a judgment, not a proposition, and what it means depends on the kind of type A is (a mere proposition: A holds and a is how I know; a set: a is one of A's elements). *judgment depends on type*
- `L-know-that-vs-which` (model, 2 rows): The distinction to keep is knowing that (a mere proposition's proof) versus knowing which (a set's value); the passage from the second to the first is truncation, the most basic forgetting, where the forget functor begins. *know that vs which*
- `L-syntax-declarations-instantiations` (Luciano, 2 rows): Luthier's syntax is reduced to only declarations and instantiations. *syntax declarations instantiations*
- `L-eval-fuel` (model, 3 rows): eval repeating a step is not structural recursion and need not terminate, so it is given fuel, eval : N -> Program -> Term -> Maybe Term, making it total, and how much fuel was needed is the first cost measure for free. *eval fuel as cost measure*
- `L-define-invariants` (Luciano, 8 rows): Defining an invariant f : A -> B with for-all x : A, g x (f x) where g : A -> B -> Bool: the for-all is the Π, g's Bool is lifted to a proposition via a data Cierto : Bool -> U, and the invariant ties to f either as a separate hole-definition (the declaration is the test) or as a package where the guarantee travels with the function. *define invariants*
- `L-laws-are-declarations` (model, 3 rows): Laws are ordinary declarations, holes until proven, and falsifiable by an instance that does not type. *laws are declarations*
- `L-total-vs-partial-guarantee` (model, 1 rows): A law can hold either by conditioning it in the type (total function, partial guarantee) or by restricting the function (partial function, total guarantee), the choice depending on who uses it. *total vs partial guarantee*
- `L-redundancy-crosses-coloneq` (model, 3 rows): The redundancy worth keeping is the one that crosses the := , where type and body say different things the verifier checks; redundancy repeated on one side is removable with sugar. *redundancy crosses coloneq*
- `L-sugar-adds-no-term-constructor` (model, 2 rows): Sugar may add nothing to Term: a construct that forces a new Term constructor is a primitive to discuss, not sugar. *sugar adds no term constructor*
- `L-invariant-is-bool-function-field` (model, 5 rows): In version 0 an invariant is a function returning Bool, stored as a field of the definition beside the body, with a generator hole filled by type and the run kept as data. *invariant is bool function field*
- `L-laws-like-cpp-requires` (Luciano, 4 rows): Laws are written in few lines like a C++ requires block: quantified variables in a header and one Bool expression per line, each a type requirement checked without running or a value requirement run by the test. *laws like cpp requires*
- `L-concept-is-predicate-over-functions` (model, 2 rows): A concept is a predicate over functions, a list of requirements, so two implementations satisfying it are interchangeable. *concept is predicate over functions*
- `L-no-value-without-passing-check` (model, 3 rows): There is no way to hold a value of a subtype without its predicate having been evaluated or proved; the check runs when the value is built. *no value without passing check*
- `L-laws-are-the-normal-form` (model, 3 rows): The novelty is that a group of functions with its laws, as a type whose laws are run by default, is the normal way to define anything, not a separate verification tool. *laws are the normal form*
- `L-concept-is-a-function` (Luciano, 6 rows): A concept needs no new type: it is an ordinary function returning a type (with proofs) or a list of laws (with tests). *concept is a function*
- `L-almacen-is-constructor-function` (Luciano, 4 rows): A structure like Almacen is a function that takes the raw operations and returns the verified versions, so the only way to obtain one is to pass the check. *almacen is constructor function*
- `L-luthier-is-verified-library` (Luciano, 2 rows): Luthier itself is a series of verified types and functions with their theorems and tests, almost an instance of the pattern. *luthier is verified library*
- `L-name-the-pattern-library` (Luciano, 5 rows): The verification structure the pattern builds is named Library, not Luthier the language; an instance is a program that passed its tests and can show it, so the adjective tested is superfluous. *name the pattern library*
- `L-units-with-parametrizable-requirements` (Luciano, 2 rows): No language ships units that carry a set of requirements they must satisfy; in Luthier the predicate is a function with parameters (max error, scalability), so the certificate states which parameters are met and a dependent library inherits them. *units with parametrizable requirements*
- `L-luthier-is-extended-concepts` (Luciano, 2 rows): Luthier is C++ concepts extended to the whole language: predicates with semantic requirements that are run and whose results are stored, keeping subsumption and composition. *luthier is extended concepts*
- `L-symbol-economy` (model, 4 rows): A symbol is used only for what appears often with a fixed universal meaning and already exists outside with it; anything rare, content-bearing or without a natural reading is a word, since the language is read aloud and written by hand. *symbol economy*
- `L-ascii-canonical` (Luciano, 2 rows): The canonical form of the language is ASCII; an editor may display -> as an arrow or * as a cross, but what is run by hand and grepped is the ASCII. *ascii canonical*
- `L-set-builder-notation` (model, 9 rows): The single subtype form is set-builder notation { pattern : material | predicate }, which denotes a Sigma; mainstream languages omit it because deciding the predicate needs a solver, a proof or a runtime check, and Luthier's fourth way tests it with n cases recorded in the certificate. *set-builder notation*
- `L-type-three-uses` (Luciano, 3 rows): A type's one piece of information is used for three purposes, typing (a judgement), constructing, and asking as a predicate; only the third exists for subtypes, is what Luthier adds, and leaves a certificate, with construction being asking and packaging. *type three uses*
- `L-cross-representation-is-function` (Luciano, 2 rows): A subtype is a restriction within one representation; when two types have different representations their relation is always a certified function with laws, never a subtype, with no implicit coercion (integers injected into the reals do not become reals). *cross-representation is function*
- `L-data-vs-subtype-choice` (Luciano, 3 rows): Use data when a thing has its own form and operations and a subtype when it is a restriction of something that already has operations; the two are types of equal status and the subtype's short name is the interface. *data vs subtype choice*
- `L-explicit-error-types` (Luciano, 4 rows): Errors should be explicit types rather than Maybe_error over a string, and the error sum E1+E2 is an ordinary type the verifier computes, neither dynamic nor dependent, with Maybe_error being the maximally forgotten Failure. *explicit error types*
- `L-iteration-propagation` (Luciano, 2 rows): Data-length iteration (MCMC and the like) is the common case, and what must be designed is its three forms of propagation, cut at first fail, accumulate, and decorate, with the forget functor keeping the decoration from overwhelming the value. *iteration propagation*
- `L-error-is-failing-predicate` (Luciano, 4 rows): An error is a predicate that fails, represented by a single recursive type Failure, a tree of label, argument and sub-failures whose labels are quotes of program terms, the same structure as the success certificate, which only a language where code is data can build. *error is failing predicate*
- `L-functions-need-no-self-knowledge` (Luciano, 2 rows): Functions need no self-knowledge; a law is an ordinary function to Bool and the label is put by the verifier level, which knows the whole program and runs test as an operation over Program. *functions need no self-knowledge*
- `L-laws-live-in-type` (model, 2 rows): Laws live in the type and thus in the DAG like any definition, so changing a law invalidates dependents' certificates through the graph, and laws can be shared, cross components, or be inherited by a subtype over a subtype. *laws live in type*
- `L-prototype-python-then-fast` (model, 3 rows): Write the core interpreter in Python now to validate the design, since the interpreter uses its own types which are data, and only later rewrite eval in a fast language. *prototype python then fast*
- `L-luthier-describes-python-works` (model, 3 rows): In this phase Luthier only describes (types, laws, extern, test) with no non-trivial function bodies, and Python does the work. *luthier describes python works*
- `L-content-hash-certificate` (model, 4 rows): Content-addressed build: a definition's certificate carries a hash of its elaborated type and body (and its dependency cone), so a matching hash on import satisfies the obligation, files are the source of truth and a relational DB is a reconstructible index. *content hash certificate*
- `L-file-is-sigma-value` (model, 1 rows): A .lut file denotes a value of a Sigma type with named components like Ring, so a library's signature is its type, two interchangeable libraries are two values of one type, and a parametrized library is a module-to-module function. *file is sigma value*
- `L-conceptual-vs-machine-impl` (Luciano, 2 rows): A de novo conceptual implementation stands alongside the machine's, and a conceptual test states and checks their relation (N is isomorphic to the non-negative integers, respecting sum and product), the conceptual definition serving as oracle with the certificate recording the range tested. *conceptual vs machine impl*
- `L-certificate-reproducible` (model, 2 rows): A certificate that does not record the seed, generation parameters and domain of each variable is not reproducible, so one seed per run is chosen and stored, each definition's derived from it, and --seed repeats the whole run. *certificate reproducible*
- `L-hidden-parameter-exposed` (model, 1 rows): A hidden parameter that affects the guarantee, like a max depth with no criterion, must be recorded in the certificate and exposed. *hidden parameter exposed*
- `L-what-belongs-in-luthier` (Luciano, 3 rows): Python holds only the machine (ops behind extern) and the bridge; any decision that changes what the certificate means, including generators, arithmetic types and test itself, must be written and visible in Luthier. *what belongs in luthier*
- `L-statistical-law-over-sample` (model, 1 rows): A distribution defect like a biased generator is invisible to any per-case quantified law and needs a law over the whole sample with a probabilistic verdict, the statistical Bayes layer. *statistical law over sample*
- `L-test-finds-domain-border` (model, 2 rows): Because size grows during a run, the first failure appears at the border of the domain where the law stops holding; the function does not change, what changes is the asserted domain, and the certificate records which assertion is true and where. *test finds domain border*
- `L-report-in-concepts` (Luciano, 1 rows): Work is reported to Luciano in concepts, the most important first, naming what failed or what limit was hit; a count like "33 laws" tells him nothing. *report in concepts*
- `L-concepts-belong-in-luthier` (model, 7 rows): Luthier is where the concepts are expressed, so organizing by Python module instead of by concept was the error that left the central concept (the likelihood) as a black box in Python; the concept must have its own type with its laws inside Luthier. *concepts belong in luthier*
- `L-cumulative-no-recompute` (Luciano, 2 rows): Luthier is cumulative, never computing the same thing twice except on an explicit override, with knowledge accumulating, perhaps in a relational database. *cumulative no recompute*
- `L-uncertainty-functor` (Luciano, 4 rows): Uncertainty is a functor decorating a value such as position with a prior or credibility interval, with five forms differing in how exact the functor is and what they lose, a distribution over a grid proposed as canonical and the type parameterized by the functor to avoid duplication. *uncertainty functor*
- `L-delegate-representation-python` (Luciano, 7 rows): Luthier expresses the concepts and delegates the representation to Python, with a compiler generating the Python representation now written by hand (the chosen way being to load the .lut at import rather than compile to files), the generated code never edited and carrying the .lut's hash. *delegate representation python*
- `L-is-it-a-dsl` (Luciano, 4 rows): In implementation Luthier is a DSL in Python, and only a few things justify a separate language: the judgment that a value satisfies a type, the certificate as persistent composable evidence, the hole as a first-class citizen, environment independence, and a future fifth of proving rather than testing. *is it a dsl*
- `L-law-only-when-known-true` (model, 2 rows): A hole-filled program is valid and the complete .lut is the specification; a law is written only when already known true (by math or existing tests), since an unverified law that turns out false is worse than a hole. *law only when known true*
- `L-native-extern-agree` (Luciano, 16 rows): Each concept is written twice, native in Luthier as the slow conceptual reference and extern in Python as the fast version, and the test is that they agree; extern always, law always, native only when the law does not determine the operation. *native extern agree*
- `L-array-primitive` (Luciano, 6 rows): Arrays (Vec, Mat) enter as a primitive certified by algebraic laws with generators, with accessors and tabulate so Python traverses while Luthier still sees values, the conceptual endpoint being a dimension-indexed Vec : Nat -> U. *array primitive*
- `L-no-exact-equality-floats` (model, 1 rows): == does not decide over floats or arrays; comparison is an approximate relation with a tolerance (tolOf n = 8 n eps, the slack declared once). *no exact equality floats*
- `L-environment-evaluator` (model, 7 rows): Luthier's evaluator should use environments and closures so each argument and constant is computed once (concepts are unique), replacing substitution which copies the body and recomputes multiply-used arguments. *environment evaluator*
- `L-luthier-types-python-values` (Luciano, 10 rows): Luthier provides only the types with their postconditions and laws; the values are external, instantiated extern in Python, and no extern is declared U. *luthier types python values*
- `L-objects-are-cycles` (Luciano, 12 rows): When the invariants of several definitions need each other they are a co-dependent object defined together in one simultaneous definition against a type that ties them with laws; objects are the cycles of the definition graph. *objects are cycles*
- `L-type-closes-with-laws` (Luciano, 14 rows): Defining a type must mean something: a mere juxtaposition or product is not a new type, which closes only when laws connect its subcomponents (the closed style, unusable until closed), as opposed to a derived type that is an expression of operators over defined types. *type closes with laws*
- `L-pure-interface-files` (Luciano, 5 rows): Pure .lut files declare carriers and operations without bodies (like C++ pure virtual classes but with verified laws and concrete definitions on the leaves), and a separate Python-linking file fills each hole, while real.lut keeps its externs as the environment layer. *pure interface files*
- `L-negative-controls` (Luciano, 3 rows): A test is diagnostic only if a wrong version fails it, so negative controls (a case that must fail) are needed, since a law nothing exercises certifies nothing. *negative controls*
- `L-validate-at-frontier` (Luciano, 2 rows): What is reusable is the format every conversion must reach, not the per-experiment conversion; the throwaway script stays outside Luthier and its only contract is that its output passes the schema, validated at the frontier. *validate at frontier*
- `L-luthier-runs-and-tests` (Luciano, 3 rows): Luthier both runs and tests, becoming the legible documentation of a Python project, with leaves in Python that iterate over data and composition in Luthier that iterates over concepts, so a program that runs is its documentation. *luthier runs and tests*
- `L-closed-vs-open-definition` (model, 2 rows): A type can be defined closed, its carrier with operations and invariants together, or open, a bare carrier plus separately declared operations and laws that a model satisfies. *closed vs open definition*
- `L-declared-vs-defined` (Luciano, 24 rows): A type has states, declared (a forward-declared hole), defined (its invariants given) and certified; a value or extern definition requires a defined type while declarations may reference merely-declared types, which is what builds cyclic definitions. *declared vs defined*
- `L-operations-by-ops-or-properties` (Luciano, 3 rows): A mathematical object's operations can be defined through other operations or by their properties; when both, a theorem connects them, and the elemental set is not unique. *operations by ops or properties*
- `L-pure-vs-derived-math-objects` (Luciano, 1 rows): Some mathematical objects are pure, arising from nothing like the integers, and others are derived, built upon other objects. *pure vs derived math objects*
- `L-spec-interpreter-first` (Luciano, 5 rows): Write the formal specification first, not of the whole interpreter but the static semantics, the judgments the checker decides, which today live only in the code. *spec interpreter first*
- `L-spec-rule-accept-reject` (model, 5 rows): Each spec rule is written with two small .lut files, one to accept and one to reject, turning the spec into the interpreter's test suite, the law with its negative control applied to Luthier itself. *spec rule accept reject*
- `L-genuine-dependence` (Luciano, 9 rows): The predicates connecting a type's components must be genuinely dependent and non-separable; a fake f(x,y)=g(x) should not count, and a separability failure needs a witnessed verdict. *genuine dependence*
- `L-laws-hypergraph-connected` (model, 13 rows): Connection is a property of the whole set of laws: the hypergraph of laws must be connected and cover all components. *laws hypergraph connected*
- `L-form-before-laws` (model, 2 rows): A type's form, its base and labels, must be fixed in the declaration before its laws, since laws are written over its components and typed before the type closes. *form before laws*
- `L-types-and-values-unified` (Luciano, 4 rows): Almost eliminate the type/value distinction: everything is a type, some types are values of others, differing only in whether they are determined, so no extra symbol is needed. *types and values unified*
- `L-test-run-same-operation` (model, 1 rows): Evaluating a predicate on determined names is running and on undetermined names is testing: the same evaluator under a different determination. *test run same operation*
- `L-value-single-inhabitant` (model, 3 rows): A value is a type with a single inhabitant (4 is {n:N|n==4}), which makes the determined/undetermined scale literal and collapses the two relations into refinement; x:T means x refines T. *value single inhabitant*
- `L-defined-determined-axes` (model, 4 rows): Defined and determined are independent axes (a hole can have laws without implementation, an extern implementation without laws); a name passes declared, defined, determined, certified. *defined determined axes*
- `L-object-has-head` (model, 2 rows): Every object has a head: a type whose body names its laws, so there are no free-standing laws that define. *object has head*
- `L-constructors-are-generator` (model, 6 rows): Presenting a type by constructors tied to observers by laws (algebraic ADT spec) makes the constructors the generator, so gen comes free from composing them; without constructors there are no completeness cells. *constructors are generator*
- `L-theory-vs-presentation` (model, 2 rows): A mathematical object is a theory and what one writes is a presentation; the theory is never written, Luthier has presentations (cycles with laws) and certified translations between them. *theory vs presentation*
- `L-translation-second-order` (Luciano, 6 rows): A translation between presentations of the same structure is a second-order Luthier concept, expressible in Luthier quantifying over presentations (type operators U->U), where Luthier starts to show its uses. *translation second order*
- `L-luthier-self-presentations` (Luciano, 4 rows): Luthier itself admits different equivalent primitive elements and laws (it already has several presentations of itself, with sugar-to-core a translation), and one must be chosen. *luthier self presentations*
- `L-kernel-choice-criterion` (model, 2 rows): The canonical core is chosen not by minimality but so the static semantics can be stated directly on it without a translation, keeping the subtype primitive though derivable. *kernel choice criterion*
- `L-translation-tested-per-model` (model, 3 rows): A translation quantified over all carriers and models cannot be tested without a model generator, so it is certified per concrete model, not in general. *translation tested per model*
- `L-real-vs-theoretical-objects` (Luciano, 4 rows): There are real objects with constructors and theoretical objects without; both exist and which is meant is made explicit, the native type being the real and the parametrized record the theoretical. *real vs theoretical objects*
- `L-sufficient-completeness` (Luciano, 3 rows): Aim at sufficient completeness (a law per observer-constructor cell plus extensionality), which the checker verifies mechanically, rather than minimality of laws. *sufficient completeness*
- `L-vec-is-function` (Luciano, 7 rows): A Vec is a function from indices below n to R (VecOf n := Pi with subtype), with tabulate as constructor and at as observer, the list being another presentation, yet it feels almost primitive. *vec is function*
- `L-determined-up-to-iso` (model, 1 rows): Laws never determine a unique implementation and need not; they make all implementations behave the same from outside, determining the object up to isomorphism. *determined up to iso*
- `L-extensionality-law` (model, 2 rows): An extensionality law (two values equal when all observers agree) is what turns 'the same observations' into 'the same object'. *extensionality law*
- `L-law-independence-witnessed` (model, 2 rows): A law is independent if a model exists satisfying all the others and violating it, an existential needing the witnessed verdict. *law independence witnessed*
- `L-semantic-vs-performance-primitives` (model, 4 rows): What makes Vec seem primitive is performance not semantics, separating semantic primitives (the core) from performance primitives (the externs certified against the definition). *semantic vs performance primitives*
- `L-bases-firm-first` (Luciano, 2 rows): First make Luthier's bases firm and complete, and only once decided revise everything so those bases hold, a waterfall approach. *bases firm first*
- `L-object-is-record-type` (model, 4 rows): An object is always a record type including its carrier, defined by its laws; implementations are its values, so there is never more than one body per name and translations always work. *object is record type*
- `L-one-body-per-name` (model, 2 rows): Giving a name both a body of laws and := extern is two bodies for one name, forbidden; the two styles that seemed to coexist are one badly written. *one body per name*
- `L-theorem-is-agrees-law` (model, 2 rows): An operation defined both via other operations and by its properties yields a theorem, which in Luthier is a law over a branch, the Agrees pattern. *theorem is agrees law*
- `L-against-pure-waterfall` (model, 2 rows): Pure waterfall fails: the rule changed three times and the two-bodies inconsistency surfaced only from writing a concrete example; specs written without executing err where no one imagined. *against pure waterfall*
- `L-law-needs-concrete-case` (model, 1 rows): As Luthier preaches for code, a law is written first but holds only when a concrete case puts it to the test. *law needs concrete case*
- `L-equality-parametrized-probability` (Luciano, 6 rows): Objects are parametrized by observational equality and eventually by a probability of being equal or distinct, where equality returns a verdict with its level rather than a Bool. *equality parametrized probability*
- `L-extern-gives-value-not-type` (Luciano, 5 rows): An extern always gives a value, never a type (pyTable : Table .= extern, not Table := extern); when a Python value represents a native type the boundary is a certified representation translation. *extern gives value not type*
- `L-several-canonical-presentations` (Luciano, 2 rows): There should be several canonical presentations and Luthier should prove their equivalence, though it is good to start with one. *several canonical presentations*
- `L-types-native-values-either` (Luciano, 2 rows): Types are defined natively, while the values (executable functions) may be native or not, admitting both, since only the dubious part is worth reimplementing. *types native values either*
- `L-new-type-from-recursion-or-laws` (model, 3 rows): Only recursion (infinite freedom) or laws (refinement) generate a new named type; a product or sum without laws deserves no new name. *new type from recursion or laws*
- `L-fin-int-vs-machine` (Luciano, 4 rows): Fin n is semantically the finite set over ℤ; a machine integer is not another definition of Fin but a representation of a subset of ℤ, written as two presentations with an equivalence law. *fin int vs machine*
- `L-primitive-keyword-explicit-state` (Luciano, 4 rows): A name like R:U without a body does not error only because the checker holds a hidden primitives set; a name's state should be readable in the program through a `primitive` body, not a hidden list. *primitive keyword explicit state*
- `L-algebra-chooses-number-object` (Luciano, 2 rows): Rather than rewrite floating-point arithmetic, use algebra to choose the mathematical object that best represents the reals. *algebra chooses number object*
- `L-distinguish-reals-from-float-subtype` (Luciano, 2 rows): Distinguish R, the set of reals, from the Python-implemented subtype (real/Float64), being precise about which is which. *distinguish reals from float subtype*
- `L-reals-theory-rationals-float-models` (model, 15 rows): Separate ℝ as a theory with no finite implementation, ℚ as an exact computable model, and Float64 as a model of the rounded field tied to ℚ by a correct-rounding law testable in ℚ. *reals theory float models*
- `L-write-over-real-approximate-with-float` (Luciano, 3 rows): The numeric code is written once over Real, which has the better properties, and Float64 (or intervals, or Rational) is one of its approximations, so f(Real) is approximated by f(Float64). *write over real approximate with float*
- `L-interval-enclosure-law` (model, 2 rows): With an interval model the approximation law is stated once for any f as enclosure (f_Float64 x ∈ f_Interval x), so the tolerance is computed in test rather than chosen by hand. *interval enclosure law*
- `L-number-theory-record` (model, 2 rows): Numeric code is written once over a theory of numbers, a record with carrier, operations and equality; Real is its ideal model and Float64, intervals, Rational are others, filled through a per-file hole as in the ML functor. *number theory record*
- `L-real-realized-by-float64` (Luciano, 4 rows): Real is not implemented but delegated to Float64, which realizes it at runtime as an interpreter choice recorded in the certificate. *real realized by float64*
- `L-leaf-declared-over-float64` (Luciano, 4 rows): An extern leaf is declared over what it really receives and returns (Vec Float64, not Real), since the type cannot affirm what the implementation does not deliver, forcing libraries generic in the number type. *leaf declared over float64*
- `L-real-carrier-plus-axiom` (model, 3 rows): Real is written as carrier plus structure, Real := primitive and realField : CompleteOrderedField Real := axiom, where axiom is a value whose laws are assumed. *real carrier plus axiom*
- `L-law-in-hole-declaration` (model, 3 rows): The law belongs in the hole's declaration so filling it with the extern inherits the obligation and every use of the name is a certified value, removing the duplicated certified copies. *law in hole declaration*
- `L-ad-hoc-laws-reproduce-implementation` (Luciano, 4 rows): The objects-as-types-with-laws theory is not used in the key cases (Vec, Table, Mat, Objective); ad hoc laws reproduce the function's implementation instead of stating the mathematical invariants that characterize it. *ad hoc laws reproduce implementation*
- `L-one-name-per-thing` (Luciano, 2 rows): Do not declare the same thing under two distinct names. *one name per thing*
- `L-symmetric-matrix-type` (model, 3 rows): Spectral operations must take a Symmetric type (with a tolerance, since numpy's inverses are not exactly symmetric), putting the mathematical precondition in the type that the code was lying about. *symmetric matrix type*
- `L-shapes-preconditions-in-types` (model, 4 rows): The leaves do not carry their shape or range preconditions in their types (matVec accepts any shape, missing range checks), which should become dependent invariants. *shapes preconditions in types*
- `L-acoustic-stage-drives-next` (model, 3 rows): The next Luthier work should be pushed by the acoustic stage and the GCC likelihood, not the cleanup of the algebra. *acoustic stage drives next*
- `L-pending-recorded-as-fail` (model, 10 rows): A law that cannot be run (no generator, out of fuel, pending over a theory) is recorded as FAIL, mixed with real counterexamples. *pending recorded as fail*
- `L-run-record-omits-uncertified-cone` (model, 1 rows): Spec 05 asks the run record to note the uncertified names of the cone, but the CLI saves only entry, hash, when, parameters and result. *run record omits cone*
- `L-runs-not-what-certified` (model, 5 rows): What runs (10 nodes, full vector) is not what was certified (7 nodes, gauge); the transfer rests on an informal argument no law states and the checker ignores. *runs not what certified*
- `L-setoid-caught-real-bug` (model, 3 rows): Typing same as a Setoid caught a real bug (the gaussian belief was not symmetric), the best evidence that the method catches errors. *setoid caught real bug*
- `L-certs-internal-not-empirical` (model, 1 rows): Nothing is applied to the real data; the certificates speak of internal coherence, not of whether the model describes the measurements. *certs internal not empirical*
- `L-ergonomics-let-unary-minus` (model, 7 rows): Writing costs for lack of let, implicit arguments and unary minus (functions end in ten closing braces), which should come before any kernel refinement. *ergonomics let unary minus*
- `L-project-constants-leak` (model, 3 rows): Project-specific constants calibrated to the tape (pitTol, ensembleSize, zMax, fdStep) leak into the generic library instead of being parameters. *project constants leak*
- `L-statistical-tests-low-power` (model, 2 rows): The statistical tests have low power: few cases and controls that break the model at double sigma, the easiest case to detect, so a 10-20% error in sigma may go undetected. *statistical tests low power*
- `L-validate-bridge-first` (model, 4 rows): Validating everything crossing from Python and --set against the declared type, including codomain refinements, is the only fix that can prevent a wrong number with no warning and so comes first. *validate bridge first*
- `L-certificate-is-only-a-record` (model, 4 rows): The certificate neither enables nor blocks anything, it is only a record, so the word certificate is excessive. *certificate is only a record*
- `L-laws-didnt-need-language` (model, 7 rows): The four laws that paid off are well chosen but none needed the language; they come out the same with pytest plus hypothesis. *laws didnt need language*
- `L-luthier-describe-deal-inverted` (model, 5 rows): The handoff deal that Luthier only describes got inverted; now gauge, jacobian, model and native solvers live in Luthier and Python must match it bit for bit. *luthier describe deal inverted*
- `L-test-distribution-in-directive` (model, 9 rows): The distribution of test cases belongs in the directive, not in the type; an alias carrying a distribution contradicts R7. *test distribution in directive*
- `L-luthier-costs-more-than-returns` (pasted, 1 rows): As a design Luthier improved this week, but as a sonolocalización tool it today costs the project more than it returns. *luthier costs more than returns*
- `L-spec-faster-than-use` (pasted, 4 rows): The specification moves faster than any use, so no program built on Luthier can stabilize. *spec faster than use*
- `L-gen-over-refined-type` (model, 6 rows): A generator is defined only over a type with a predicate, so a type like BrokenGraph must be a refinement subtype whose predicate the generated values are checked against. *gen over refined type*
- `L-generated-value-checked-against-type` (model, 6 rows): Each value a registered generator produces is checked against its type and a value outside it is an error, with gen T trusted as the declared-trust escape. *generated value checked against type*
- `L-report-statistic-not-block` (model, 1 rows): A result like a residual's uniformity should be reported as a question, a statistic and its null level, informing rather than blocking (figures with a head). *report statistic not block*
- `L-positional-identity-trap` (model, 1 rows): The positional identity of products and sums lets fields be swapped silently, which the spec says and which is a trap. *positional identity trap*
- `L-one-generator-per-type` (model, 3 rows): A generator written over an alias is the generator of the type the alias names, and two generators for the same type are an error. *one generator per type*
- `L-name-the-patches` (model, 3 rows): The patches made in the work should be named as patches and noted in the plan rather than passing as specification. *name the patches*
- `L-report-not-decidable` (model, 2 rows): When the checker cannot read which labels a law touches or decide an equality, it should report not decidable rather than approximate or count all labels as touched. *report not decidable*
- `L-constants-must-be-parameters` (model, 8 rows): A criterion hardcoded as a constant in the code (lmMaxIter, the rejection-sampler's try budget) must be a parameter, by the rule that every criterion is a parameter. *constants must be parameters*
- `L-dimension-in-types` (model, 4 rows): The model's dimension must enter the types of probability, belief and optimization (Theta is VecOf n throughout), since with an unconstrained Vec Float64 the model's obligations were false. *dimension in types*
- `L-generic-laws-dont-run` (model, 11 rows): Laws generic in a type parameter (Theta : U) never run because there is no generator of U, so they are certified only when a program fills the hole with a concrete type that has a generator, or by a well-chosen instance, and asking for a generator of U is a static error. *generic laws dont run*
- `L-problem-vs-objective` (model, 4 rows): negate falsely promises an Objective with laws from arbitrary functions, so a lawless Problem (what the algorithm runs) is split from an Objective (a Problem with laws) and negate returns a Problem, making the obligation disappear. *problem vs objective*
- `L-statistical-law-level-retry` (model, 8 rows): A statistical law declares its level (the probability of failing on a correct model), is retried with an independent seed before a failure counts as a counterexample (level alpha squared), and reports a verdict with that level rather than a bare pass/fail. *statistical law level retry*
- `L-generation-part-of-certificate` (Luciano, 6 rows): Unless a gen is declared the tester builds values from the type's structure, and that construction is part of what each certificate means and silently decides what a law actually tests; generators are checked for being in the type, never for covering it. *generation part of certificate*
- `L-generator-explicit-per-type` (Luciano, 12 rows): There is no single generator per type, so a test must name the explicit generator it bound to each type and the certificate records it (gen T := disappears); functions are generated by a census over registered values. *generator explicit per type*
- `L-number-generator-limits-scale` (Luciano, 5 rows): A number generator needs explicit limit values and a linear or logarithmic scale (with special values and their weight), the limits carried in the type, so a Float64 without limits in its type is a static error if the binding does not supply them. *number generator limits scale*
- `L-check-refines-value-type` (model, 10 rows): A check done on a value refines its type (inside if p x, x has the refined type) so nobody checks it again, with the result's granularity chosen by the cost of redoing it; this applies to run results, which are checked once into the run record. *check refines value type*
- `L-interval-arithmetic-bounded-real` (Luciano, 2 rows): Interval arithmetic fits Luthier because its correctness is a single inclusion law Luthier can already certify: a bounded Real is a certificate carried across a computation that yields a bound for a function's values. *interval arithmetic bounded real*
- `L-check-bool-primary-derived` (Luciano, 4 rows): A check is written once as a Bool (the law, composing by and/or/not) with refinement by branch as the rule, and the refined type and other presentations are derived. *check bool primary derived*
- `L-certifying-algorithm-witness` (model, 1 rows): A certifying algorithm returns its result plus a witness a simple checker verifies, the refined value being the special case where the witness is the value itself, giving in general a dependent pair with a law. *certifying algorithm witness*
- `L-monad-vs-applicative-validation` (model, 2 rows): A monad stops at the first failure (fit for a pipeline) while validating by hand wants the full list of violations (an applicative that accumulates errors), and the context decides between the two. *monad vs applicative validation*
- `L-refine-reading-not-path` (model, 1 rows): When the checked fact is external, refining the value gives a guarantee that can expire, so the principle refines what was read, not the reference, and check and use must be the same operation. *refine reading not path*
- `L-tolerance-checks-dont-compose` (model, 1 rows): Checks with a tolerance do not compose, since a near b and b near c do not give a near c at the same tolerance, so if used to refine, the tolerance must go in the type. *tolerance checks dont compose*
- `L-certificates-enable-autonomy` (Luciano, 7 rows): Luthier's mechanical certificates and file-held state let the AI work sustainedly through the night and across context compaction, since a pass/fail certificate makes it prudent to run the check and continue. *certificates enable autonomy*
- `L-objective-from-list` (model, 2 rows): An Objective should not be drawn by rejection (random functions almost never match their declared gradient) but taken from an explicit list of registered values, such as the project's own objective and a quadratic. *objective from list*
- `L-reuse-not-run-law-result` (model, 2 rows): Re-running a not-run law is wasted work when code, generators and seed are the same, since the result is deterministic, so the tester could reuse that result as it reuses a certificate. *reuse not run law result*
- `L-cert-guarantees-via-typed-externs` (model, 3 rows): A certificate now guarantees something because every value returned from Python is read by its declared type, and the certificate hash covers the Luthier code, the Python behind each extern and the interpreter. *cert guarantees via typed externs*
- `L-phase-states-closing-check` (model, 1 rows): Each phase of a plan should state what check closes it, and a phase with no mechanical check belongs to Luciano and not to the autonomous run. *phase states closing check*
- `L-mechanize-rules-lint-hook` (Luciano, 5 rows): The instructions living in memory are moved to mechanical checks in three layers (what Luthier can reject, what a repo lint catches, what stays judgment with a mechanical reminder), which requires relaxing the rule that only Luciano runs the scripts for lints and certification. *mechanize rules lint hook*
- `L-binding-by-parameter` (model, 2 rows): Each quantified variable is paired with its generator by parameter, the only thing that distinguishes tol from an input of the mean, with profiles serving as abbreviation. *binding by parameter*
- `L-generator-is-luthier-value` (model, 2 rows): A generator is a Luthier value with its own type and laws, certifiable like any other, and the random number generator is an extern with its stochasticity laws declared in Luthier. *generator is luthier value*
- `L-run-inputs-vs-cert-reach` (model, 1 rows): A run's inputs are compared against the reach of the certificates: what arrives via --set at startup, and what is computed during the run only under --checked. *run inputs vs cert reach*
- `L-literal-lint-type-vs-criterion` (model, 2 rows): A mechanical criterion to classify numeric literals: a constant in type position (a refinement bound) defines a type, one in term position is a criterion. *literal lint type vs criterion*
- `L-mechanical-check-is-shadow` (model, 2 rows): Rules that are matters of judgment transfer to a mechanical check only as a substitute, a shadow of the real rule. *mechanical check is shadow*
- `L-generic-functor-in-interpreter` (model, 2 rows): Generic functors live in the interpreter, derived from the type's structure as == already is, named and recorded in the certificate but not written in Luthier. *generic functor in interpreter*
- `L-code-universe` (model, 2 rows): A data Code describes the type shapes that can be generated, El decodes each to a type, and the functors become ordinary Luthier functions over codes. *code universe*
- `L-code-universe-staged` (model, 2 rows): Implement the code universe in stages: first codes without mu (numbers with bounds, products, sums, vectors, refinements), adding mu with Boltzmann sampling when a recursive data needs generating. *code universe staged*
- `L-russell-plus-tarski-library` (model, 2 rows): Keep Russell's U for everything and add a small closed Tarski universe of codes as a library for what must be treated generically. *russell plus tarski library*
- `L-signature-shows-parametricity` (model, 2 rows): With both universes a signature carries what it can do: (A:U)-> is parametric and cannot inspect A, (c:Code)-> may inspect the code's shape, and a typecase over U breaks parametricity silently. *signature shows parametricity*
- `L-elegant-vs-mosaic` (model, 2 rows): A language is elegant when its constructions follow from one or two ideas and its self-interpreter fits a page, mosaic when each construction was added for a need; Luthier's spec is elegant but the interpreter has mosaic pieces the next round should remove. *elegant vs mosaic*
- `L-sample-quality-is-prover-power` (model, 1 rows): Because Luthier certifies refinement types by sampling rather than by a prover, what in other languages is the power of the prover is here the quality of the sample. *sample quality is prover power*
- `L-luthier-states-not-programs` (model, 1 rows): Luthier should be a language to state and certify the claims of a computation done in Python or R, not a language to program in. *luthier states not programs*
- `L-full-to-unprovable` (model, 2 rows): What distinguishes Luthier is carrying types-as-propositions a full to propositions that cannot be proved, so the grade of verification must be part of what belonging to a type affirms. *full to unprovable*
- `L-optimize-needs-strong-certificates` (model, 3 rows): Type, certification and measurement are one idea from three sides; optimizing over weak certificates is worse than not optimizing, so generators and certificate reach come before selection, which picks only among covering implementations and records the chosen one in each result's provenance. *optimize needs strong certificates*
- `L-chain-interpretable-steps` (Luciano, 1 rows): The AI generates so much output that the only workable way to use it is to chain steps whose result you can interpret. *chain interpretable steps*
- `L-statistical-and-deductive-tests` (Luciano, 2 rows): A function's type has two verification paths: a statistical test for what cannot be proved and a deductive test for what can, keeping both. *statistical and deductive tests*
- `L-language-forces-method` (Luciano, 2 rows): Luthier's relevance is forcing the author and the AI to be methodical, and a program that compiles gives some assurance it is not garbage, by analogy with Lean's proofs. *language forces method*
- `L-passthrough-or-orchestrator` (Luciano, 2 rows): Luthier can be a language the code passes through or an orchestrator pointing outward, and both are fine with passage between them. *passthrough or orchestrator*
- `L-synthesize-python-call` (Luciano, 2 rows): Luthier should synthesize the call to a Python function using Luthier syntax, so one can work in layers more outward or more inward of Python. *synthesize python call*
- `L-reduce-to-minimum` (Luciano, 2 rows): AI output carries filler hard to judge; a criterion is to ask whether it can be reduced further and still work, as one minimizes an algorithm. *reduce to minimum*
- `L-declarative-and-executive` (pasted, 7 rows): Luthier has a declarative part (types that follow laws) and an executive part that runs commands (read a file, execute a function); the executive part can be internal or external. *declarative and executive*
- `L-effects-as-threaded-pointers` (pasted, 3 rows): The external world is a type that exists and nothing constructs, with no equality, whose values are pointers externs give, threaded linearly so their order lives in the graph of definitions and a reused pointer is a type error. *effects as threaded pointers*
- `L-host-minimal-duties` (pasted, 3 rows): If the interpreter is written in Luthier the host need only reduce, run the primitive types' operations, and call an extern reading and writing a File, plus read a canonical serialization of Term, with everything else Luthier definitions over Program. *host minimal duties*
- `L-realization-ideal-and-runner` (pasted, 1 rows): A realization is the ideal and what runs it, related by a law and a cost, with mutation and destruction as optimizations that keep the consequence and the host as a realization of the reduction rules. *realization ideal and runner*
- `L-run-changes-states` (pasted, 3 rows): Running a function is modeled as changing the states of the program and the states of the universe (a written file, a printed line, a sent message), the universe's changes also following rules. *run changes states*
- `L-three-kinds-of-proposition` (pasted, 2 rows): A certificate is a proposition with its evidence, and propositions are of three kinds (a timeless law, a trace fact never revised, a statement about the world that ages), every chain of evidence ending in laws assumed. *three kinds of proposition*
- `L-trace-compare-consequence-cost` (pasted, 1 rows): run fills holes, reduces and leaves a trace, and two traces compare in two ways, by consequence as an equivalence and by cost as a partial order measured with its variance. *trace compare consequence cost*
- `L-failure-mass-sampling` (model, 4 rows): What n passing sampled cases update is the failure mass theta under the usage distribution, not the law's truth, with a Beta prior giving Beta(a,b+n), theta of order 1/n, composing by union bound and transferring between uses through the saved posterior. *failure mass sampling*
- `L-order-is-confluence` (model, 2 rows): Evaluation order is free for pure terms by confluence (Church-Rosser), not by purity, so the order is a strategy and a parameter, not a truth. *order is confluence*
- `L-knowledge-vs-certificate` (model, 4 rows): Certified is knowledge not a state of the name, so the record splits into knowledge (the posterior over a model's behavior given prior, model class and evidence, joined across runs) and certificate (a decision for a use, a query over that knowledge that must not write the posterior's mode as a fact). *knowledge vs certificate*
- `L-search-vs-cost-split` (model, 4 rows): Searching where a law fails and weighting where it costs are distinct, the Use / TestPlan split, so search-generator cases inform theta only with importance weights and the generator must declare its density. *search vs cost split*
- `L-use-as-plan-element` (model, 4 rows): Use enters the plan as a timeless element, a distribution over inputs, a loss over the law's residual and a decision criterion, with the certificate indexed by model, theory, use and prior and test taking a use whose generator is the distribution component. *use as plan element*
- `L-cost-laws` (model, 5 rows): Laws could be extended to go not to a boolean but to a cost: graded cost laws like a generalized unnormalized likelihood, asking how much a value costs rather than whether it complies. *cost laws*
- `L-discrepancy-threshold-cost` (model, 2 rows): A law computes a discrepancy, the theory sets the threshold that makes it Bool, and the use sets the cost, so the theory stays independent of the use. *discrepancy threshold cost*
- `L-exterior-is-files` (model, 4 rows): What is outside Luthier is largely files (executables, Python code, data, plots, even sensors), plus mutable memory, resources and processors. *exterior is files*
- `L-laws-of-interpretation-steps` (model, 3 rows): Luthier should carry the laws of each interpretation step (reduce, apply), written in Luthier, so one can check that Luthier's precepts hold; with apply and reduce almost all of it is done. *laws of interpretation steps*
- `L-posterior-per-computation` (model, 3 rows): With this bayesian logic any computation in Luthier carries a posterior of how sure you are of that computation. *posterior per computation*
- `L-type-parametrized-by-use` (model, 5 rows): A type can be parametrized by its conditions of use and environment: a cost of failure varying by situation and a prior probability of each parameter combination occurring, which need only be expressible now. *type parametrized by use*
- `L-keep-witness-high-information` (model, 3 rows): Since these functions are expensive, keep the witness that a function worked or failed, giving priority to high-information values far from the prior (the unexpected ones). *keep witness high information*
- `L-eval-modes` (model, 3 rows): You define a program and ask to execute/eval it under different modified evaluations (with test, with extensive test, copying everything that happens); having several execution modes is the attraction of such a language. *eval modes*
- `L-law-as-object-classifier` (Luciano, 11 rows): A law need not return Bool: its codomain can be an object classifier with an order and a 'holds' element (a quantale Omega, the positive reals as a cost, or the universe U of evidence types), the theory being the sublevel set under a threshold and Bool the case {0,infinity}. *law as object classifier*
- `L-sup-not-sampleable` (model, 2 rows): A law's for-all in [0,infinity] is a sup that a sample bounds only from below, the mathematical reason sampled testing cannot certify a universal law and why the use is needed, replacing the sup by an expectation against the usage distribution. *sup not sampleable*
- `L-object-classifier-laws` (Luciano, 1 rows): Luthier has a kind of object classifier: predicates about types that are the laws, the names. *object classifier laws*
- `L-membership-construction-or-hypothesis` (Luciano, 2 rows): A value belongs to a type either by construction (the case is given) or by hypothesis, a construction by value that can fail. *membership construction or hypothesis*
- `L-function-as-expected-loss` (Luciano, 2 rows): What is left of a function is an expected loss, a posterior characterization that must be processable, expressible as a type of generator, test and cost. *function as expected loss*
- `L-many-function-types` (Luciano, 1 rows): A function's type need not be unique; there can be many function types one invents, such as positive functions from reals to positive reals. *many function types*
- `L-agnostic-program-universe-state` (Luciano, 2 rows): The language should not distinguish types that speak of the program's internal state from those that speak of the universe's state; the program should be agnostic. *agnostic program universe state*
- `L-declarative-of-implementation` (Luciano, 2 rows): Luthier needs a declarative description, written in Luthier, of its own implementation: how Luthier code transforms into execution code. *declarative of implementation*
- `L-combine-evidence-refine-certainty` (Luciano, 1 rows): Combine different evidences, different programs running the same function, to refine the certainty in that function. *combine evidence refine certainty*
- `L-analysis-only-at-moments` (Luciano, 1 rows): The whole verification apparatus is expensive parafernalia layered on top, so one must be able to say it runs only at some moments, not always. *analysis only at moments*
