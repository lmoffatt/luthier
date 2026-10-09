# Candidate principles of Haskell, found blind, 2026-10-09

Written by `scripts/find_principles.py` (find_principles v1). Prompt `find_principles_v1` (sha256 892e58875a4e),
model opus at effort low via claude-code (2.1.197 (Claude Code)); the model saw only the
lineages and the criterion of infectability.
Inputs by sha256: `record/controls/haskell/ideas/lineages_link_ideas_v2_claude-code_opus.json` ae8f9a7e5571; `record/controls/haskell/ideas/timeline.jsonl` a487c657e131.
Each candidate shows apart what the script took from the rows and what is the model's reading.

Lineages: 319; candidate 27, considered 25, not_principle 267.

## Candidates

```
C1  Keep the language pure and make every effect explicit in the type of a computation.
Scope:      language
-- from the rows, by the script
Quote:      "Underlying all these developments is the realisation that being explicit about effects
            is extremely useful, and this is something that we believe may ultimately be seen as one
            of Haskell’s main impacts on mainstream programming"
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     07_monads-and-input-output.md line 534 (row written:2007-06-09_07-monads-and-input-output:being-explicit-about-effects)
Lineages:   L-effects-bet, L-explicit-effects, L-haskell-overcame-impractical, L-purity-io-problem
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 4 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  ethical. it is a stance on how one should program: effects are a discipline to be
            controlled and made visible, not a default
Also:       conceptual. it reframes effects as something a type can carry, reorganising what a
            program's meaning is
Also:       emotive. the authors frame it as a long-term bet they consciously wagered against the
            mainstream
Harms:      forces awkward encoding of I/O and state
Harms:      array and in-place algorithms get messier
Harms:      a barrier for newcomers used to effects-by-default
Beats:      L-pure-principled-attack (Functional programming, particularly in its purely functional
            form, is a radical and principled attack on the challenge of writing programs that
            work.). l235 names functional programming a radical principled attack but stays a
            slogan; purity-with-explicit-effects is the operative rule that decides designs
Above next: purity is the ethical spine from which laziness, monads and the rest hang

C2  Evaluate lazily, so that evaluation order follows need and infinite structures are ordinary
    values.
Scope:      language
-- from the rows, by the script
Quote:      "Lazy evaluation—with its direct connection to the pure, call-by-name lambda calculus,
            the remarkable possibility of representing and manipulating infinite data structures,
            and addictively simple and beautiful implementation techniques—was like a drug."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     02_the-genesis-of-haskell.md line 117 (row written:2007-06-09_02-the-genesis-of-haskell:laziness-as-a-drug)
Lineages:   L-cons-not-evaluate, L-laziness-combinators, L-laziness-macros, L-lazy-appeal,
            L-lazy-enables-stream, L-lazy-three-times
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 6 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  emotive. the designers describe lazy evaluation as addictive, "like a drug", the thing
            that drew them in
Also:       conceptual. it opens infinite data structures and unusual control flow as ordinary
            values
Also:       aesthetic. its implementation techniques are called simple and beautiful
Harms:      space leaks that are hard to anticipate
Harms:      operational behaviour opaque, so profiling and debugging are hard
Harms:      mixing strict and lazy code well is a real difficulty
Beats:      L-non-strict-pure (The language to be designed was fixed as non-strict and purely
            functional.). l204 just records that the language was fixed non-strict; laziness as
            lived experience infects far more than the bare design choice
Above next: laziness grips the programmer's imagination more viscerally than the mathematical
            reading, though it costs more

C3  Because of referential transparency a program can be read as executable mathematics, equations
    whose specification is the program.
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
Strongest:  conceptual. it recasts a program as a system of equations, so the specification can be
            the program
Also:       aesthetic. the economy of reading code as mathematics over a known domain
Harms:      sets an ideal the language rarely fully meets
Harms:      can mislead about actual performance
Beats:      L-minimal-surfaces (Haskell's language, libraries and culture lead to solutions that
            feel like minimal surfaces: simple expressions comprising significant complexity, with
            natural forms recurring problem after problem.). l172's minimal surfaces is an evocative
            image but vaguer; executable mathematics names a precise, usable reframing
Above next: it reframes what a program is, but rests on the purity already stated above

C4  Model a computation that may have effects as a first-class value of type IO a (or any monad),
    sequenced by bind.
Scope:      language
-- from the rows, by the script
Quote:      "The key idea is to treat a value of type IO a as a “computation” that, when performed,
            might perform input and output before delivering a value of type a."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     07_monads-and-input-output.md line 346 (row written:2007-06-09_07-monads-and-input-output:monadic-io-key-idea)
Lineages:   L-io-a-computation, L-monad-as-typeclass, L-monadic-advantage
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 3 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. it turns an effectful computation into a first-class value you can build and
            sequence
Also:       aesthetic. a single pattern unifies state, exceptions, parsing, I/O and more
Also:       ethical. it shows effects can be had without abandoning deterministic pure semantics
Harms:      monads do not compose in a modular way
Harms:      do-notation makes code look imperative, blurring the pure line
Harms:      a steep learning curve for newcomers
Beats:      L-state-monad-plumbing (Lacking reference cells, threading a counter by hand to generate
            fresh names is tedious and error-prone; a state transformer monad hides the plumbing.).
            l269 shows a state monad hiding plumbing, a nice instance; the general idea of a
            computation-as-value infects more broadly
Above next: monads give effects a reusable structure, but they are one realisation of the purity
            principle rather than its root

C5  Resolve ad-hoc overloading in a principled way through type classes, constraints that qualify a
    polymorphic type.
Scope:      language
-- from the rows, by the script
Quote:      "They were originally proposed early in the design process, by Wadler and Blott ... as a
            ... principled solution to a relatively small problem (operator overloading for numeric
            operations and equality)."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     06_haskell-as-a-type-system-laboratory.md line 4 (row written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-classes-origin-small-problem)
Lineages:   L-class-bounded-quantification, L-dictionary-passing, L-type-class-origin,
            L-type-class-serendipity, L-type-classes-distinctive
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 7 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. a principled account of overloading as bounded quantification, a predicate
            over types
Also:       aesthetic. one mechanism cleanly captures equality, ordering, numbers, show/read and
            more
Harms:      ambiguity and puzzling error messages
Harms:      dynamic semantics depends on how overloading is resolved
Harms:      the design grew into chaotic complexity
Beats:      L-qualified-types (Type classes are one instance of Jones's more general framework of
            qualified types, which also yields polymorphic extensible records with lacks predicates
            witnessed at run time.). l237's qualified types is the deeper framework but came later
            and more technical; type classes are the infectious entry point
Above next: type classes reorganise polymorphism, but infect a narrower slice of thought than
            computations do

C6  Write a library that turns the language into a domain-specific embedded language sharing its
    syntax, types and tools.
Scope:      language
-- from the rows, by the script
Quote:      "the idea of writing a library that turns Haskell into a domainspecific embedded language
            (DSEL), a term first coined by Hudak"
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     11_applications.md line 121 (row written:2007-06-09_11-applications:dsel-definition)
Lineages:   L-combinator-definition, L-combinator-dsel-same, L-combinator-influential,
            L-dsel-definition, L-dsel-host
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 6 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. a library becomes a language, so writing a program is designing its
            vocabulary
Also:       ethical. it argues the way to attack a domain is to build its language rather than a
            program in a fixed one
Harms:      the embedded language inherits the host's error messages
Harms:      a leaky abstraction when host semantics intrudes (e.g. sharing)
Beats:      L-dsel-structure (A DSEL typically defines a data type conceptually a function, with
            operators combining pieces, executed by decomposing and applying them.). l56 describes
            the usual DSEL structure; the coined idea of turning the host itself into a domain
            language is the sharper infection
Above next: DSELs turn the language outward into domains, a reach slightly less central than the
            class system

C7  Make expressions look as much like mathematics as possible, with infix operators from day one.
Scope:      language
-- from the rows, by the script
Quote:      "The Haskell Committee wanted expressions to look as much like mathematics as possible,
            and thus from day one we bought into the idea that Haskell would have infix operators."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     04_syntax.md line 74 (row written:2007-06-09_04-syntax:infix-operators-like-mathematics)
Lineages:   L-haskell-pretty, L-infix-from-day-one, L-layout-rule-design
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 4 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  aesthetic. making code read like mathematics is pursued for the beauty and economy of
            the surface itself
Also:       ethical. a stance that the user interface of a language, its syntax, deserves
            first-class care
Harms:      notation debates consume disproportionate effort (Wadler's law)
Harms:      prefix negation introduces parsing ambiguity
Beats:      L-high-level-succinct (As a very high-level language Haskell lets programmers write
            succinct but readable code and concentrate on the problem without boilerplate and
            housekeeping.). l116's succinctness is a benefit; wanting the surface to look like
            mathematics is the design commitment that produces it

```

## Considered and left out

- `L-avoid-semicolon` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Without side effects there is no sequencing, so the committee avoided the semicolon and its imperative baggage. *avoid imperative sequencing baggage*
- `L-cbv-recursive-combinators` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Call-by-value languages disallow recursive combinator definitions, forcing eta-expansion that clutters code and wrecks the abstraction. *laziness keeps recursive combinators clean*
- `L-committee-design` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Haskell was to be designed by a committee, not an individual. *design by committee, method*
- `L-conservative-language` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): The committee intended a conservative language embodying current consensus rather than breaking new ground. *a conservative, consensus language, method*
- `L-dsel-structure` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): A DSEL typically defines a data type conceptually a function, with operators combining pieces, executed by decomposing and applying them. *typical DSEL structure*
- `L-first-class-infix` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): The wish that all values be first class clashed with infix operators not being first class. *all values should be first class*
- `L-haskell98-stability` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): The Haskell 98 Report was a deliberate commitment to stability. *commitment to stability, method*
- `L-high-level-succinct` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): As a very high-level language Haskell lets programmers write succinct but readable code and concentrate on the problem without boilerplate and housekeeping. *concentrate on the problem, no boilerplate*
- `L-keywords-low` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Keeping the number of reserved keywords low was a priority, avoiding ones useful as variable names. *keep reserved keywords few*
- `L-legacy-influence` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): Haskell's most important legacy will be its influence on the languages that succeed it, the ideas and techniques it nurtured proving of enduring value even after Haskell itself is forgotten. *legacy is influence on successors*
- `L-many-ways-fit` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Haskell offers many ways to define functions, simple and fitting together sensibly. *many ways to define, fitting sensibly*
- `L-minimal-surfaces` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Haskell's language, libraries and culture lead to solutions that feel like minimal surfaces: simple expressions comprising significant complexity, with natural forms recurring problem after problem. *solutions feel like minimal surfaces*
- `L-module-namespace-only` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): They converged on a simple design where the module system is only a namespace-control mechanism, specified separately from the type system. *module system does as little as possible*
- `L-non-strict-pure` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): The language to be designed was fixed as non-strict and purely functional. *non-strict, purely functional design choice*
- `L-ol-default` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): OL's design was the default to be kept for any topic lacking a clearly better solution. *keep the default unless clearly better*
- `L-open-participation` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): After the committee ceased, anyone on the mailing list could participate, with Peyton Jones as editor. *open participation, method*
- `L-pattern-readability` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Pattern matching against algebraic data types greatly increases readability. *pattern matching increases readability*
- `L-pure-principled-attack` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Functional programming, particularly in its purely functional form, is a radical and principled attack on the challenge of writing programs that work. *functional programming a principled attack*
- `L-qualified-types` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): Type classes are one instance of Jones's more general framework of qualified types, which also yields polymorphic extensible records with lacks predicates witnessed at run time. *qualified types general framework*
- `L-segregate-formats` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Explicitly segregating legacy data formats into separate data types prevented the mysterious errors that propagate through shell programs when a format changes. *segregate formats into distinct types*
- `L-shadowing-allowed` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Haskell allowed variable shadowing, since outlawing it is inconsistent with alpha renaming. *allow shadowing, consistent with alpha renaming*
- `L-start-from-existing` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): The easiest way forward was to begin with an existing language and evolve it. *start from an existing language, method*
- `L-state-monad-plumbing` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Lacking reference cells, threading a counter by hand to generate fresh names is tedious and error-prone; a state transformer monad hides the plumbing. *state monad hides the plumbing*
- `L-teaching-goal` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Suitability for teaching was one of the explicit goals the designers set for Haskell. *suitability for teaching, goal/method*
- `L-type-system-anarchic` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Haskell's type system developed anarchically, features used before formalisation, speeding exploration at the cost of complexity. *implement features before formalising, method*
