# Candidate principles of Haskell, found blind, 2026-10-09

Written by `scripts/find_principles.py` (find_principles v1). Prompt `find_principles_v2` (sha256 5eb0cb1b3e6b),
model opus at effort low via claude-code (2.1.197 (Claude Code)); the model saw only the
lineages and the criterion of infectability, with names redacted (Haskell=L).
Inputs by sha256: `record/controls/haskell/ideas/lineages_link_ideas_v2_claude-code_opus.json` ae8f9a7e5571; `record/controls/haskell/ideas/timeline.jsonl` a487c657e131.
Each candidate shows apart what the script took from the rows and what is the model's reading.

Lineages: 319; candidate 28, considered 21, not_principle 270.

## Candidates

```
C1  Keep the language pure and make every effect explicit in the types, rather than allowing effects
    by default.
Instead of: effects-by-default
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
Strongest:  ethical. it is a stance on how one should program: effects are not a default convenience
            but something to be controlled and declared.
Also:       conceptual. typing effects reorganizes a program around what may happen, not only what
            is computed.
Harms:      makes I/O and arrays awkward (l10)
Harms:      a steep barrier before a program can do anything useful
Harms:      forbids convenient in-place update
Beats:      L-effects-convergence (A convergence is underway: the functional community has learnt
            the value of effects and a way to tame them while mainstream languages adopt declarative
            constructs, driven especially by parallelism, which punishes unrestricted effects
            cruelly.). the convergence is an observation about where languages are heading, not the
            rule that chose purity in the first place.
Above next: purity is the ethical commitment the whole language is organized around; laziness is one
            of its consequences.

C2  Evaluate lazily by default, so values are computed only when needed and infinite structures and
    new abstractions become ordinary.
Instead of: strict, call-by-value evaluation
Scope:      language
-- from the rows, by the script
Quote:      "Lazy evaluation—with its direct connection to the pure, call-by-name lambda calculus,
            the remarkable possibility of representing and manipulating infinite data structures,
            and addictively simple and beautiful implementation techniques—was like a drug."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     02_the-genesis-of-haskell.md line 117 (row written:2007-06-09_02-the-genesis-of-haskell:laziness-as-a-drug)
Lineages:   L-laziness-combinators, L-laziness-macros, L-lazy-appeal, L-lazy-enables-stream,
            L-non-strict-pure, L-turner-lazy-lists
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 6 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. abstracting from evaluation order admits infinite structures and new control
            abstractions, changing what a value even is.
Also:       emotive. the authors describe lazy evaluation as "like a drug", contact with what moved
            them.
Also:       aesthetic. infinite data structures and simple implementation techniques are beautiful,
            economical constructions.
Harms:      unpredictable space use and space leaks (l149,l267)
Harms:      hard to profile and debug (l154)
Harms:      operational cost hidden from the source
Beats:      L-listcomp-lazy-popular (List comprehensions are more popular in lazy languages, found
            in Miranda and Haskell but not SML or Scheme.). list comprehensions suiting lazy
            languages is one pleasant consequence, not the evaluation discipline itself.
Above next: laziness rewrites the mental model of computation; executable mathematics is a reading
            that laziness and purity make possible.

C3  Preserve referential transparency so programs read as equations, as executable mathematics where
    the specification can become the program.
Instead of: programs as sequences of state-changing commands
Scope:      language
-- from the rows, by the script
Quote:      "Because of referential transparency, Haskell programs can be viewed as executable
            mathematics, as equations over the category of complete partial orders. In principle, at
            least, the specification becomes the program."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     12_the-impact-of-haskell.md (row written:2007-06-09_12-the-impact-of-haskell:referential-transparency-executable-mathematics)
Lineages:   L-executable-mathematics, L-infix-from-day-one
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. reading a program as equations, as mathematics one can reason about,
            reframes what programming is.
Also:       aesthetic. expressions that look like mathematics have an economy and beauty the authors
            sought from day one.
Harms:      the "specification becomes the program" gap holds only in principle
Harms:      the CPO/denotational framing intimidates newcomers
Harms:      seq and effects break the equational reading
Beats:      L-math-look-teaching (Haskell's mathematical look and feel makes it a medium for
            teaching discrete mathematics and logic.). the mathematical look aiding teaching is a
            use of the frame, not the commitment to referential transparency that creates it.
Above next: the equational frame is broader than any one mechanism; type classes are the distinctive
            device that serves it.

C4  Solve overloading with a principled, type-directed abstraction of classes and instances, not ad
    hoc special-casing.
Instead of: ad hoc operator overloading
Scope:      language
-- from the rows, by the script
Quote:      "Aside from laziness, type classes are undoubtedly Haskell's most distinctive feature."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     06_haskell-as-a-type-system-laboratory.md line 3 (row written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-classes-as-distinctive-feature)
Lineages:   L-class-bounded-quantification, L-type-class-origin, L-type-class-serendipity,
            L-type-classes-distinctive
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 5 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. overloading becomes a type-directed abstraction (classes, instances,
            dictionaries) that reorganizes how generic code is written.
Also:       aesthetic. a single principled construct replaced a tangle of special cases, with an
            elegant bounded-quantification reading.
Harms:      ambiguity and puzzling error messages (l25,l288)
Harms:      dynamic semantics depends on type resolution (l58)
Harms:      the design space grew chaotic (l291)
Beats:      L-qualified-types (Type classes are one instance of Jones's more general framework of
            qualified types, which also yields polymorphic extensible records with lacks predicates
            witnessed at run time.). qualified types generalise the idea further but it is type
            classes that caught the imagination and spread.
Above next: type classes are the distinctive feature that even made monads usable, so they rank
            above the monadic abstraction they carry.

C5  Model effects and other notions of computation as first-class values, reasoning about
    computations abstractly rather than wiring their details by hand.
Instead of: built-in, hard-wired notions of sequencing and effects
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
Strongest:  conceptual. treating a computation as a first-class value, reasoned about abstractly, is
            a new frame for effects and sequencing.
Also:       aesthetic. one small interface (return and bind) captures state, exceptions, parsing,
            continuations and more.
Harms:      monads do not compose modularly (l185)
Harms:      do-notation blurs pure and imperative code (l52)
Harms:      a steep conceptual barrier for learners
Beats:      L-arrows (Arrows, proposed by Hughes, are an abstract view of computation like monads
            but more general, easier to use with syntactic support.). arrows are the same flavour in
            a more general setting but reached far fewer minds than monads.
Above next: monads reorganize how effects are thought; combinator libraries are a building technique
            that benefits from them.

C6  Build abstractions as combinator libraries that turn the language itself into a domain-specific
    language, instead of inventing a new language and tooling each time.
Instead of: writing a standalone parser, type checker and interpreter per domain
Scope:      language
-- from the rows, by the script
Quote:      "Another productive way to think of a combinator library is as a domain-specific language
            (DSL) for describing values of a particular type"
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     11_applications.md line 38 (row written:2007-06-09_11-applications:combinator-library-as-dsl)
Lineages:   L-combinator-definition, L-combinator-dsel-same, L-combinator-influential,
            L-dsel-definition, L-dsel-host
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 6 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. a library becomes a language: you design notation and meaning for a domain
            without building a compiler for it.
Also:       aesthetic. new domain abstractions are composed from existing functions, an economical
            reuse of the whole host language.
Harms:      embodies nothing fundamentally new (l30)
Harms:      host-language error messages leak into the DSL
Harms:      blurs the library/language boundary
Beats:      L-parser-bnf (Parser combinators allow an extraordinarily direct transcription of BNF
            into executable code.). parser combinators are one striking instance of the idea, less
            than the general stance of embedding any DSL.
Above next: embedding DSLs opens a new frame of use; minimal surfaces is the aesthetic sense that
            pervades it but guides less concretely.

C7  Prefer solutions that are minimal surfaces: simple expressions carrying significant complexity,
    in forms that feel natural and recur across problems.
Instead of: accidental complexity and one-off special forms
Scope:      language
-- from the rows, by the script
Quote:      "solutions that feel like minimal surfaces: simple expressions that comprise significant
            complexity, with forms that seem natural, recurring in problem after problem"
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     12_the-impact-of-haskell.md (row written:2007-06-09_12-the-impact-of-haskell:minimal-surfaces)
Lineages:   L-high-level-succinct, L-many-ways-fit, L-minimal-surfaces
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 3 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  aesthetic. the ideal of a simple surface holding significant complexity, recurring form
            after form, is a standard of beauty for solutions.
Also:       conceptual. many ways to do a thing that still fit together coherently reshapes what a
            well-formed design looks like.
Harms:      "natural form" is subjective
Harms:      elegance can hide real cost
Beats:      L-linspire-uniformity (Haskell has versatility comparable to shell and scripting
            languages but promotes much greater uniformity, though its idioms for systems
            programming are not quite as compact as Perl's.). greater uniformity than scripting
            languages is one comparative virtue, not the aesthetic ideal of minimal surfaces itself.

```

## Considered and left out

- `L-arrows` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Arrows, proposed by Hughes, are an abstract view of computation like monads but more general, easier to use with syntactic support. *arrows as an abstract view of computation*
- `L-conservative-language` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): The committee intended a conservative language embodying current consensus rather than breaking new ground. *conservatism: embody consensus, not break ground*
- `L-effects-convergence` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): A convergence is underway: the functional community has learnt the value of effects and a way to tame them while mainstream languages adopt declarative constructs, driven especially by parallelism, which punishes unrestricted effects cruelly. *convergence toward taming effects*
- `L-first-class-infix` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): The wish that all values be first class clashed with infix operators not being first class. *all values first class, especially functions*
- `L-haskell98-stability` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): The Haskell 98 Report was a deliberate commitment to stability. *commit to long-term stability*
- `L-layout-rule-design` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): Haskell exploits the physical layout of the text via the offside rule, in a design more lenient than Miranda's. *exploit layout to avoid syntactic clutter*
- `L-linspire-uniformity` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Haskell has versatility comparable to shell and scripting languages but promotes much greater uniformity, though its idioms for systems programming are not quite as compact as Perl's. *greater uniformity than scripting languages*
- `L-listcomp-lazy-popular` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): List comprehensions are more popular in lazy languages, found in Miranda and Haskell but not SML or Scheme. *list comprehensions suit lazy languages*
- `L-math-look-teaching` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Haskell's mathematical look and feel makes it a medium for teaching discrete mathematics and logic. *mathematical look aids teaching*
- `L-module-namespace-only` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): They converged on a simple design where the module system is only a namespace-control mechanism, specified separately from the type system. *module system as minimal namespace control*
- `L-multiparam-resisted` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 3 rows): Type classes can be generalised from a predicate over one type to a relation over several, but the committee resisted multi-parameter classes as an unforced step into ambiguity and kept the single-parameter restriction. *resist unforced steps into complexity*
- `L-not-from-miranda` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Not starting from Miranda forced a new design but allowed more radical approaches such as type classes. *freedom for radical approaches*
- `L-ol-default` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): OL's design was the default to be kept for any topic lacking a clearly better solution. *keep the default unless clearly better*
- `L-parser-bnf` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Parser combinators allow an extraordinarily direct transcription of BNF into executable code. *parser combinators transcribe BNF directly*
- `L-pure-not-right-way` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Purely functional programming is not necessarily the right way to write programs. *purity is not necessarily the one right way*
- `L-pure-principled-attack` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Functional programming, particularly in its purely functional form, is a radical and principled attack on the challenge of writing programs that work. *functional programming as a principled attack*
- `L-qualified-types` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): Type classes are one instance of Jones's more general framework of qualified types, which also yields polymorphic extensible records with lacks predicates witnessed at run time. *qualified types as a general framework*
- `L-records-omitted` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): Records with named fields were omitted from early Haskell because there was no obvious right design. *omit features lacking an obvious right design*
- `L-start-from-existing` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): The easiest way forward was to begin with an existing language and evolve it. *start from an existing language and evolve*
- `L-syntax-effort` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): The committee worked hard on syntax, which as the user interface is personal and provoked heated debate. *syntax matters as the user interface*
- `L-type-system-anarchic` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Haskell's type system developed anarchically, features used before formalisation, speeding exploration at the cost of complexity. *implement and use before formalising*
