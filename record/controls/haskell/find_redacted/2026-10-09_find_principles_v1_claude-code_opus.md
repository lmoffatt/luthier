# Candidate principles of Haskell, found blind, 2026-10-09

Written by `scripts/find_principles.py` (find_principles v1). Prompt `find_principles_v1` (sha256 892e58875a4e),
model opus at effort low via claude-code (2.1.197 (Claude Code)); the model saw only the
lineages and the criterion of infectability, with names redacted (Haskell=L).
Inputs by sha256: `record/controls/haskell/ideas/lineages_link_ideas_v2_claude-code_opus.json` ae8f9a7e5571; `record/controls/haskell/ideas/timeline.jsonl` a487c657e131.
Each candidate shows apart what the script took from the rows and what is the model's reading.

Lineages: 319; candidate 16, considered 54, not_principle 249.

## Candidates

```
C1  Control effects on principle and make them explicit, against the mainstream default of effects
    everywhere.
Scope:      language
-- from the rows, by the script
Quote:      "many of us were consciously making a longterm bet that principled control of effects
            would ultimately turn out to be important, despite the dominance of effects-by-default
            in mainstream languages."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     13_conclusion.md line 13 (row written:2007-06-09_13-conclusion:longterm-bet-on-principled-control-of-effects)
Lineages:   L-effects-bet, L-explicit-effects
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  ethical. it is an explicit stance that effects should be controlled and made visible
            rather than scattered by default, a wager about how programming ought to be done.
Also:       conceptual. making effects part of the type reorganises how one reasons about what a
            program can do.
Harms:      punishes the programmer who just wants a quick side effect
Harms:      the I/O and effect machinery can look like ceremony to newcomers
Harms:      bets long-term usefulness against immediate convenience
Beats:      L-pure-principled-attack (Functional programming, particularly in its purely functional
            form, is a radical and principled attack on the challenge of writing programs that
            work.). l235 names functional programming a 'radical and principled attack' but stays a
            slogan about the field; the effect bet says concretely which way to go when a choice
            about effects arises.
Above next: It is a stance that reshapes the whole language's attitude to state, where C2 is a
            consequence one enjoys once purity is in place.

C2  Because of referential transparency, a program can be read and manipulated as mathematics.
Scope:      language
-- from the rows, by the script
Quote:      "Because of referential transparency, Haskell programs can be viewed as executable
            mathematics, as equations over the category of complete partial orders. In principle, at
            least, the specification becomes the program."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     12_the-impact-of-haskell.md (row written:2007-06-09_12-the-impact-of-haskell:referential-transparency-executable-mathematics)
Lineages:   L-executable-mathematics
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. seeing a running program as equations one can reason about collapses the
            usual gap between spec and code, a genuinely reorganising frame.
Also:       aesthetic. the idea that the specification is the program has a spare elegance.
Harms:      raises expectations the real language, with bottom and seq, cannot fully meet
Harms:      'specification becomes the program' can mislead about actual engineering cost
Harms:      array and in-place algorithms sit awkwardly with this view
Beats:      L-math-look-teaching (Haskell's mathematical look and feel makes it a medium for
            teaching discrete mathematics and logic.). l171 notes L's mathematical look suits
            teaching discrete maths, but that is about appearance; executable mathematics is a claim
            about what the program is.
Above next: It frames what the whole language is for; C3 is one powerful mechanism that lives inside
            such a language.

C3  Evaluate lazily, embracing infinite structures and abstraction from evaluation order as the
    language's organising choice.
Scope:      language
-- from the rows, by the script
Quote:      "Lazy evaluation—with its direct connection to the pure, call-by-name lambda calculus,
            the remarkable possibility of representing and manipulating infinite data structures,
            and addictively simple and beautiful implementation techniques—was like a drug."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     02_the-genesis-of-haskell.md line 117 (row written:2007-06-09_02-the-genesis-of-haskell:laziness-as-a-drug)
Lineages:   L-lazy-appeal, L-turner-lazy-lists
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  emotive. the authors describe laziness as 'like a drug', an unusually frank contact with
            what drew them in.
Also:       conceptual. infinite data structures and abstraction from evaluation order open a new
            way of structuring programs.
Also:       aesthetic. the 'addictively simple and beautiful' implementation is prized for its
            elegance.
Harms:      makes space and time behaviour hard to predict from the source
Harms:      complicates debugging and profiling
Harms:      mixing strict and lazy code well is a standing difficulty
Beats:      L-laziness-combinators (Laziness makes Haskell natural for combinator libraries,
            allowing recursive combinators without fuss and unusual control flow.). l148 explains
            that laziness makes L natural for combinator libraries, a useful consequence, but the
            appeal lineage names the pull of the idea itself.
Above next: Laziness is a pervasive stance on evaluation; monads are one structure that thrives
            under it but could be adopted without it.

C4  Model a computation as a first-class value with return and bind, so effects can be captured and
    sequenced abstractly.
Scope:      language
-- from the rows, by the script
Quote:      "the big advantage is conceptual. It is much easier to think abstractly in terms of
            computations than concretely in terms of the details of failure and success
            continuations."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     07_monads-and-input-output.md line 413 (row written:2007-06-09_07-monads-and-input-output:monad-abstraction-conceptual-advantage)
Lineages:   L-io-a-computation, L-monad-as-typeclass, L-monad-definition, L-monadic-advantage
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 4 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. treating a value as a computation to be performed, and sequencing such
            computations, is a reorganising frame that turns effects into first-class objects.
Also:       aesthetic. one small interface, return and bind, captures state, exceptions, parsing and
            I/O alike.
Harms:      the abstraction has a steep conceptual threshold
Harms:      monads do not compose modularly, an open problem
Harms:      no mechanism enforces the laws a true monad must obey
Beats:      L-classes-monads-symbiosis (Type classes and monads had a symbiotic relationship:
            classes made monads accessible and popular while monadic I/O ensured the adoption of
            higher-kinded polymorphism.). l26 observes the symbiosis of classes and monads, but that
            is a historical relationship between two ideas, not the infectious core of thinking in
            computations.
Above next: Monads reorganise how effects are handled; type classes are the more general device
            that, among much else, makes monads expressible.

C5  Resolve overloading on principle through type classes, typing a value for any type that is an
    instance of a class.
Scope:      language
-- from the rows, by the script
Quote:      "Type classes were extremely serendipitous: they were invented at exactly the right
            moment to catch the imagination of the Haskell Committee ..."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     06_haskell-as-a-type-system-laboratory.md line 89 (row written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-classes-serendipity)
Lineages:   L-type-class-origin, L-type-class-serendipity, L-type-classes-distinctive
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 4 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. principled overloading, typing a function for any type that is an instance
            of a class, opened a design space far beyond its small original purpose.
Also:       ethical. it answered a messy problem with a principled solution rather than an ad hoc
            one.
Harms:      the class world grew chaotically complex
Harms:      ambiguity and puzzling error messages for students
Harms:      the dynamic semantics comes to depend on type resolution
Beats:      L-qualified-types (Type classes are one instance of Jones's more general framework of
            qualified types, which also yields polymorphic extensible records with lacks predicates
            witnessed at run time.). l237 (qualified types) is the more general framework that
            explains classes, but it infects as an after-the-fact generalisation; the class idea
            itself is what caught imaginations.
Above next: Type classes restructure how abstraction and overloading work; minimal surfaces is a
            softer aesthetic value than a mechanism this generative.

C6  Seek solutions that feel like minimal surfaces: the simplest expression that spans the needed
    complexity.
Scope:      language
-- from the rows, by the script
Quote:      "solutions that feel like minimal surfaces: simple expressions that comprise significant
            complexity, with forms that seem natural, recurring in problem after problem"
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     12_the-impact-of-haskell.md (row written:2007-06-09_12-the-impact-of-haskell:minimal-surfaces)
Lineages:   L-high-level-succinct, L-minimal-surfaces
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  aesthetic. the image of a minimal surface, the simplest form that spans the required
            complexity, is a vivid criterion of beauty in design.
Also:       conceptual. it names a recurring natural form, a way of recognising the right shape of a
            solution across problems.
Harms:      the pursuit of minimality can leave real needs (records, GUIs) underserved
Harms:      'simple expressions comprising significant complexity' can hide cost from readers
Harms:      elegance can be valued over the pragmatic path
Beats:      L-many-ways-fit (Haskell offers many ways to define functions, simple and fitting
            together sensibly.). l169 says L's many ways to define functions fit together sensibly,
            a pleasant fact, but it lacks the generative pull of seeking the minimal natural form.
Above next: Minimal surfaces is a value guiding how to shape a solution; looking like mathematics is
            a narrower aesthetic about surface syntax.

C7  Make expressions look as much like mathematics as possible.
Scope:      language
-- from the rows, by the script
Quote:      "The Haskell Committee wanted expressions to look as much like mathematics as possible,
            and thus from day one we bought into the idea that Haskell would have infix operators."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     04_syntax.md line 74 (row written:2007-06-09_04-syntax:infix-operators-like-mathematics)
Lineages:   L-haskell-pretty, L-infix-from-day-one
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  aesthetic. wanting expressions to look as much like mathematics as possible is an
            explicit pursuit of beauty in the surface the programmer meets.
Harms:      chasing a mathematical look drove heated, time-consuming syntax debates
Harms:      the layout and operator rules grew complex enough to need formal specification
Harms:      prettiness can be weighed against regularity
Beats:      L-layout-rule-design (Haskell exploits the physical layout of the text via the offside
            rule, in a design more lenient than Miranda's.). l147 praises exploiting layout to avoid
            clutter, a real elegance, but it is one device serving the broader wish for
            mathematical-looking code.

```

## Considered and left out

- `L-arrows` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Arrows, proposed by Hughes, are an abstract view of computation like monads but more general, easier to use with syntactic support. *arrows as a more general view of computation; infects less than monads*
- `L-avoid-semicolon` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Without side effects there is no sequencing, so the committee avoided the semicolon and its imperative baggage. *no sequencing without effects, so avoid the semicolon*
- `L-class-bounded-quantification` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): A type-class constraint expresses a form of bounded quantification: a function is typed for any type that is an instance of a given class. *classes as bounded quantification*
- `L-classes-monads-symbiosis` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): Type classes and monads had a symbiotic relationship: classes made monads accessible and popular while monadic I/O ensured the adoption of higher-kinded polymorphism. *symbiosis of classes and monads*
- `L-committee-design` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Haskell was to be designed by a committee, not an individual. *method: design by committee*
- `L-cons-not-evaluate` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Friedman and Wise framed lazy evaluation from Lisp with the slogan that cons should not evaluate its arguments. *lazy-evaluation slogan (not designers')*
- `L-conservative-language` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): The committee intended a conservative language embodying current consensus rather than breaking new ground. *method: a conservative, consensus language*
- `L-effects-convergence` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): A convergence is underway: the functional community has learnt the value of effects and a way to tame them while mainstream languages adopt declarative constructs, driven especially by parallelism, which punishes unrestricted effects cruelly. *convergence of functional and mainstream around effects*
- `L-first-class-infix` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): The wish that all values be first class clashed with infix operators not being first class. *all values should be first class*
- `L-fp-compilers-productivity` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): The abstraction and non-interference of functional languages make compilers and translation natural applications with high productivity and little project management. *abstraction and non-interference raise productivity*
- `L-ghc-frontend-fullsyntax` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): GHC keeps a large front-end data type reflecting Haskell's full syntax so error messages match what the programmer wrote. *keep error messages matching what the programmer wrote*
- `L-haskell-overcame-impractical` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Haskell helped overcome that impracticality by sticking remorselessly to purity and by building a critical mass of interest and research around a single language. *sticking remorselessly to purity*
- `L-haskell98-stability` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): The Haskell 98 Report was a deliberate commitment to stability. *method: commitment to stability*
- `L-higher-kind-unification` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Treating higher-kinded constructors as uninterpreted functions and disallowing type-level lambda lets ordinary first-order unification suffice, an ad hoc solution with excellent power-to-weight ratio. *ad hoc choice with excellent power-to-weight ratio*
- `L-isabelle-class-laws` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): In Isabelle, declaring a type class can carry the laws its operations obey and declaring an instance requires proving the instance satisfies them. *carry the laws a class obeys with its declaration*
- `L-keywords-low` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Keeping the number of reserved keywords low was a priority, avoiding ones useful as variable names. *economy: keep reserved keywords few*
- `L-layout-rule-design` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): Haskell exploits the physical layout of the text via the offside rule, in a design more lenient than Miranda's. *exploit physical layout to avoid clutter*
- `L-laziness-combinators` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Laziness makes Haskell natural for combinator libraries, allowing recursive combinators without fuss and unusual control flow. *laziness makes combinator libraries natural*
- `L-laziness-macros` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Lazy evaluation gives much of the power of Lisp macros through ordinary function definitions. *laziness gives macro power through functions*
- `L-legacy-influence` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): Haskell's most important legacy will be its influence on the languages that succeed it, the ideas and techniques it nurtured proving of enduring value even after Haskell itself is forgotten. *method: legacy is influence on successors*
- `L-let-and-where` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): The assumption of one way to do something was abandoned; both let and where are fully supported. *abandon the one-way assumption, support both styles*
- `L-linspire-uniformity` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Haskell has versatility comparable to shell and scripting languages but promotes much greater uniformity, though its idioms for systems programming are not quite as compact as Perl's. *promote uniformity over compactness*
- `L-many-ways-fit` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Haskell offers many ways to define functions, simple and fitting together sensibly. *many ways to define functions that fit together*
- `L-math-look-teaching` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Haskell's mathematical look and feel makes it a medium for teaching discrete mathematics and logic. *mathematical look and feel suits teaching*
- `L-minimalist-records` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): Haskell 1.3 adopted Mark Jones's minimalist record syntax as sugar over algebraic data types, leaving the field open for richer proposals. *minimalist design leaving the field open*
- `L-module-namespace-only` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): They converged on a simple design where the module system is only a namespace-control mechanism, specified separately from the type system. *module system as namespace control, nothing more*
- `L-monad-laws` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): A true monad's return and bind must satisfy three laws of associative composition with identity, which Haskell provides no mechanism to enforce. *the three monad laws*
- `L-multiparam-resisted` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 3 rows): Type classes can be generalised from a predicate over one type to a relation over several, but the committee resisted multi-parameter classes as an unforced step into ambiguity and kept the single-parameter restriction. *resist an unforced step into ambiguity*
- `L-need-common-language` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 3 rows): The lack of a common language held back functional programming, motivating a single language all the groups could share. *method: a single common language*
- `L-non-strict-pure` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): The language to be designed was fixed as non-strict and purely functional. *the language is non-strict and purely functional*
- `L-not-from-miranda` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Not starting from Miranda forced a new design but allowed more radical approaches such as type classes. *freedom to be radical by not starting from Miranda*
- `L-ol-default` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): OL's design was the default to be kept for any topic lacking a clearly better solution. *method: default to OL absent a better solution*
- `L-open-participation` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): After the committee ceased, anyone on the mailing list could participate, with Peyton Jones as editor. *method: open participation*
- `L-parametricity-deforestation` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Parametricity justifies short-cut deforestation (the foldr/build rule), which needs a rank-2 type for build. *parametricity justifies an optimisation*
- `L-pattern-readability` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Pattern matching against algebraic data types greatly increases readability. *pattern matching increases readability*
- `L-public-lists` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Discomfort with public and private mailing lists moved debate fully public, though the committee still decided. *method: move debate fully public*
- `L-pure-not-right-way` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Purely functional programming is not necessarily the right way to write programs. *humility: purity not necessarily the right way*
- `L-pure-principled-attack` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Functional programming, particularly in its purely functional form, is a radical and principled attack on the challenge of writing programs that work. *FP as a radical and principled attack*
- `L-purity-io-problem` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): The committee's firm commitment to a pure language made the design of the I/O system a central problem, fearing a weak solution would make Haskell look like a toy. *resolute commitment to a pure language*
- `L-qualified-types` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): Type classes are one instance of Jones's more general framework of qualified types, which also yields polymorphic extensible records with lacks predicates witnessed at run time. *qualified types as the general framework*
- `L-quirky-elegance` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): What first drew many of the authors to the field was the quirky elegance of the purely functional approach. *quirky elegance of the pure approach*
- `L-realworld-impact` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Real-world impact was an important goal of the Committee; Haskell is not mainstream but fares well in niches owing to specific language characteristics. *method: real-world impact a goal*
- `L-report-book-online` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Publishing the Report as a book while keeping it free online defused a debate about freedom and intellectual property. *method: free online yet published*
- `L-runst` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Imperative computations can be securely encapsulated in a pure function via a state monad parameterised by a type s, encapsulated by runST with a rank-2 type and parametricity preventing reference leaks. *encapsulate imperative computation inside a pure function*
- `L-segregate-formats` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Explicitly segregating legacy data formats into separate data types prevented the mysterious errors that propagate through shell programs when a format changes. *segregate formats into types to prevent errors*
- `L-shadowing-allowed` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Haskell allowed variable shadowing, since outlawing it is inconsistent with alpha renaming. *shadowing allowed for consistency with alpha renaming*
- `L-start-from-existing` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): The easiest way forward was to begin with an existing language and evolve it. *method: evolve an existing language*
- `L-state-monad-plumbing` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Lacking reference cells, threading a counter by hand to generate fresh names is tedious and error-prone; a state transformer monad hides the plumbing. *hide the plumbing with a monad*
- `L-syntax-effort` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): The committee worked hard on syntax, which as the user interface is personal and provoked heated debate. *method: syntax as user interface worth the effort*
- `L-teaching-goal` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Suitability for teaching was one of the explicit goals the designers set for Haskell. *method: suitability for teaching a goal*
- `L-type-lab` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 3 rows): Haskell became an unforeseen laboratory for designing, implementing and applying type-system extensions, for technical reasons (purity, qualified types, abandoned full inference) and nontechnical ones (an innovation-friendly committee, experimenting implementations, a geeky user base). *method: language as a laboratory for extensions*
- `L-type-system-anarchic` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Haskell's type system developed anarchically, features used before formalisation, speeding exploration at the cost of complexity. *method: anarchic development, use before formalise*
- `L-user-infix-operators` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Infix operators are user-definable, including precedence and associativity. *user-definable infix operators*
- `L-wadler-monads-programs` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Wadler recognised that Moggi's semantic technique could structure ordinary functional programs, using monads to express the features Moggi used them to describe. *a semantic technique can structure ordinary programs*
