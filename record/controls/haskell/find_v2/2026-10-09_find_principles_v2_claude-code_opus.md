# Candidate principles of Haskell, found blind, 2026-10-09

Written by `scripts/find_principles.py` (find_principles v1). Prompt `find_principles_v2` (sha256 5eb0cb1b3e6b),
model opus at effort low via claude-code (2.1.197 (Claude Code)); the model saw only the
lineages and the criterion of infectability.
Inputs by sha256: `record/controls/haskell/ideas/lineages_link_ideas_v2_claude-code_opus.json` ae8f9a7e5571; `record/controls/haskell/ideas/timeline.jsonl` a487c657e131.
Each candidate shows apart what the script took from the rows and what is the model's reading.

Lineages: 319; candidate 13, considered 19, not_principle 287.

## Candidates

```
C1  Control effects on principle and make them explicit, even at the cost of convenience.
Instead of: effects by default, unrestricted side effects
Scope:      language
-- from the rows, by the script
Quote:      "many of us were consciously making a longterm bet that principled control of effects
            would ultimately turn out to be important, despite the dominance of effects-by-default
            in mainstream languages."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     13_conclusion.md line 13 (row written:2007-06-09_13-conclusion:longterm-bet-on-principled-control-of-effects)
Lineages:   L-effects-bet, L-explicit-effects, L-haskell-overcame-impractical, L-pure-not-right-way,
            L-pure-principled-attack, L-purity-io-problem
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 6 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  ethical. it is a moral stance on how one should program: effects are not free, they must
            be controlled and declared, against the mainstream default of effects everywhere.
Also:       conceptual. typing effects reorganises computation itself, so a program's shape now
            shows where the world is touched.
Harms:      forces I/O and state into monadic plumbing
Harms:      steep entry for imperative programmers
Harms:      array and in-place algorithms become messier
Beats:      L-effects-convergence (A convergence is underway: the functional community has learnt
            the value of effects and a way to tame them while mainstream languages adopt declarative
            constructs, driven especially by parallelism, which punishes unrestricted effects
            cruelly.). the convergence of the two camps is an observation about where the field
            drifted, not a rule telling a designer which way to go.
Above next: it restructures the entire language and has infected mainstream ones, a wider reach than
            any single abstraction built on top of it.

C2  Capture any notion of computation as an abstract value you sequence, rather than wiring each
    effect into the language.
Instead of: a single built-in notion of computation and sequencing
Scope:      language
-- from the rows, by the script
Quote:      "the big advantage is conceptual. It is much easier to think abstractly in terms of
            computations than concretely in terms of the details of failure and success
            continuations."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     07_monads-and-input-output.md line 413 (row written:2007-06-09_07-monads-and-input-output:monad-abstraction-conceptual-advantage)
Lineages:   L-monad-as-typeclass, L-monadic-advantage
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. collapsing state, exceptions, IO, parsing and more under one return/bind
            frame is a genuine reorganisation of how sequencing is understood.
Also:       aesthetic. one small pattern covering so many notions of computation has an economy that
            is itself persuasive.
Harms:      monads do not compose modularly
Harms:      do-notation can hide that code is effectful
Harms:      a real conceptual wall for newcomers
Beats:      L-dsel-definition (A DSEL turns Haskell into a domain-specific embedded language sharing
            its syntax, types and modules, a term coined by Hudak.). the DSEL idea is a way of using
            the language, powerful but downstream of the abstraction that makes effects first-class
            values.
Above next: it is the frame that reuses across every effect, where type classes are the mechanism it
            happens to ride on.

C3  Solve overloading with one principled general mechanism, constraints on types, rather than ad
    hoc special cases.
Instead of: ad hoc operator overloading
Scope:      language
-- from the rows, by the script
Quote:      "They were originally proposed early in the design process, by Wadler and Blott ... as a
            ... principled solution to a relatively small problem (operator overloading for numeric
            operations and equality)."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     06_haskell-as-a-type-system-laboratory.md line 4 (row written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-classes-origin-small-problem)
Lineages:   L-type-class-origin
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. principled overloading as a constraint over types opened a design space
            whose reach no one foresaw at the start.
Also:       aesthetic. a small principled solution to a small problem that generalised cleanly has a
            quiet elegance.
Harms:      puzzling error messages
Harms:      ambiguity forcing annotations
Harms:      dynamic semantics now depends on type resolution
Beats:      L-class-bounded-quantification (A type-class constraint expresses a form of bounded
            quantification: a function is typed for any type that is an instance of a given class.).
            bounded quantification restates what a class constraint is; it describes the mechanism
            rather than urging its principled use.
Above next: distinctive and generative, but narrower in daily reach than the semantic ground that
            referential transparency names.

C4  Keep the language referentially transparent so programs read as executable mathematics.
Instead of: programs as sequences of state changes
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
Strongest:  conceptual. seeing a program as equations, where in principle the specification is the
            program, is a frame that stays in the head.
Also:       ethical. it takes a position that programs should be mathematical objects one can reason
            about, not recipes of state change.
Harms:      referential transparency rules out cheap mutation
Harms:      reasoning about performance becomes indirect
Beats:      L-high-level-succinct (As a very high-level language Haskell lets programmers write
            succinct but readable code and concentrate on the problem without boilerplate and
            housekeeping.). succinctness without boilerplate is a benefit the language delivers, not
            a rule choosing one road over another.
Above next: it is the semantic footing the abstractions stand on, but more a consequence than the
            surface a programmer touches each day.

C5  Make notation follow mathematical usage and the reader's eye.
Instead of: the syntactic tradition of other programming languages
Scope:      language
-- from the rows, by the script
Quote:      "The Haskell Committee wanted expressions to look as much like mathematics as possible,
            and thus from day one we bought into the idea that Haskell would have infix operators."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     04_syntax.md line 74 (row written:2007-06-09_04-syntax:infix-operators-like-mathematics)
Lineages:   L-infix-from-day-one
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  aesthetic. that expressions should look as much like mathematics as possible is a plain
            aesthetic commitment, taken from day one.
Also:       emotive. the pride that 'Haskell is a pretty language' shows the authors were moved by
            the look of the thing.
Harms:      infix and prefix ambiguities such as negation
Harms:      the layout rule grew complex enough to need formal specification
Beats:      L-layout-rule-design (Haskell exploits the physical layout of the text via the offside
            rule, in a design more lenient than Miranda's.). exploiting physical layout is one
            elegant device serving this larger aim of a mathematical surface.
Above next: it shapes the visible surface, where minimal surfaces is about the shape of solutions
            written on it.

C6  Prefer the simplest expression that carries the complexity, the form that recurs naturally
    across problems.
Instead of: bespoke machinery built per problem
Scope:      language
-- from the rows, by the script
Quote:      "solutions that feel like minimal surfaces: simple expressions that comprise significant
            complexity, with forms that seem natural, recurring in problem after problem"
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     12_the-impact-of-haskell.md (row written:2007-06-09_12-the-impact-of-haskell:minimal-surfaces)
Lineages:   L-minimal-surfaces
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  aesthetic. solutions as minimal surfaces, simple expressions holding real complexity, is
            a clear criterion of beauty guiding how code should be shaped.
Also:       emotive. the pleasure of a natural form recurring problem after problem is the
            enthusiasm that keeps the idea alive.
Harms:      elegance can hide cost and space behaviour
Harms:      what counts as a 'natural' form is subjective
Beats:      L-many-ways-fit (Haskell offers many ways to define functions, simple and fitting
            together sensibly.). that the many ways to define functions fit together is a fact about
            the design, not a rule to prefer the minimal form.
Above next: it is an aspiration for how solutions should look, above a stance about the design
            process itself.

C7  Embody tried-and-true consensus rather than break new ground.
Instead of: including novel, unproven features
Scope:      method
-- from the rows, by the script
Quote:      "we intended the language to be quite conservative, rather than to break new ground"
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00
Source:     02_the-genesis-of-haskell.md line 240 (row written:2007-06-09_02-the-genesis-of-haskell:conservative-consensus-intent)
Lineages:   L-conservative-language
Witnesses:  first 2007-06-09 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  ethical. it is a stance about what a language should be, embodying consensus rather than
            chasing novelty.
Harms:      excludes well-motivated but untried ideas
Harms:      the language broke it anyway, notably with type classes
Harms:      can ossify a design
Beats:      L-haskell98-stability (The Haskell 98 Report was a deliberate commitment to stability.).
            the Haskell 98 commitment to stability is one later application of this conservatism,
            narrower than the stance itself.

```

## Considered and left out

- `L-avoid-semicolon` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Without side effects there is no sequencing, so the committee avoided the semicolon and its imperative baggage. *avoid imperative syntactic baggage*
- `L-cbv-recursive-combinators` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Call-by-value languages disallow recursive combinator definitions, forcing eta-expansion that clutters code and wrecks the abstraction. *don't let call-by-value wreck abstraction*
- `L-class-bounded-quantification` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): A type-class constraint expresses a form of bounded quantification: a function is typed for any type that is an instance of a given class. *class constraint as bounded quantification*
- `L-dsel-definition` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): A DSEL turns Haskell into a domain-specific embedded language sharing its syntax, types and modules, a term coined by Hudak. *turning the language into a DSEL*
- `L-effects-convergence` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): A convergence is underway: the functional community has learnt the value of effects and a way to tame them while mainstream languages adopt declarative constructs, driven especially by parallelism, which punishes unrestricted effects cruelly. *convergence of the two camps on effects*
- `L-first-class-infix` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): The wish that all values be first class clashed with infix operators not being first class. *all values should be first class*
- `L-haskell98-stability` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): The Haskell 98 Report was a deliberate commitment to stability. *commitment to long-term stability*
- `L-high-level-succinct` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): As a very high-level language Haskell lets programmers write succinct but readable code and concentrate on the problem without boilerplate and housekeeping. *high-level succinctness, no boilerplate*
- `L-keywords-low` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Keeping the number of reserved keywords low was a priority, avoiding ones useful as variable names. *keep reserved keywords few*
- `L-layout-rule-design` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): Haskell exploits the physical layout of the text via the offside rule, in a design more lenient than Miranda's. *exploit physical layout to cut clutter*
- `L-laziness-combinators` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Laziness makes Haskell natural for combinator libraries, allowing recursive combinators without fuss and unusual control flow. *laziness makes combinator libraries natural*
- `L-legacy-influence` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): Haskell's most important legacy will be its influence on the languages that succeed it, the ideas and techniques it nurtured proving of enduring value even after Haskell itself is forgotten. *value lies in influence on successors*
- `L-many-ways-fit` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Haskell offers many ways to define functions, simple and fitting together sensibly. *many simple ways that fit together*
- `L-module-namespace-only` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2 rows): They converged on a simple design where the module system is only a namespace-control mechanism, specified separately from the type system. *module system does as little as possible*
- `L-multiparam-resisted` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 3 rows): Type classes can be generalised from a predicate over one type to a relation over several, but the committee resisted multi-parameter classes as an unforced step into ambiguity and kept the single-parameter restriction. *no unforced step into uncertainty*
- `L-non-strict-pure` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): The language to be designed was fixed as non-strict and purely functional. *non-strict, purely functional by choice*
- `L-ol-default` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): OL's design was the default to be kept for any topic lacking a clearly better solution. *keep the default unless clearly beaten*
- `L-start-from-existing` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): The easiest way forward was to begin with an existing language and evolve it. *start from an existing language and evolve it*
- `L-two-styles` (Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 1 rows): Two styles emerged: declaration style (equations, pattern matching, guards) and expression style (let, lambda, case, if). *support both declaration and expression styles*
