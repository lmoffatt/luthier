# Principles of Haskell, asked naively, 2026-10-10

Written by `scripts/naive_principles.py` (naive_principles v1). Prompt `naive_principles_v1` (sha256 f28d1cbd5fe5),
model opus at effort low via claude-code (2.1.197 (Claude Code)); the model saw every row
of the timeline (date, who, the idea) and was asked for the rules and principles, nothing more; names redacted (Haskell=L).
Inputs by sha256: `record/controls/haskell/ideas/timeline.jsonl` a487c657e131.
Rows shown: 387. The quote is the first row each candidate cites, filled in by the script.

```
C1  L is non-strict, purely functional with lazy (call-by-need) evaluation as its defining core,
    embracing both the power (infinite structures, elegant combinators) and the cost (unpredictable
    space and evaluation order) that laziness brings.
Quote:      "the nature of the language to be designed (non-strict, purely functional)"
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00 (row written:2007-06-09_01-introduction:nature-non-strict-purely-functional)
Rows:       8

C2  Purity, meaning no side effects, is held to firmly, which makes controlled handling of effects
    (I/O, state, exceptions) through monads the central design achievement and L's conscious
    long-term bet.
Quote:      "The Haskell Committee was resolute in its decision to keep the language pure—meaning no
            side effects— so the design of the I/O system was an important issue."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00 (row written:2007-06-09_07-monads-and-input-output:purity-drove-io-design)
Rows:       8

C3  Type classes, with their generalisations to higher kinds (constructor classes), multi-parameter
    classes, and functional dependencies, are L's most distinctive feature after laziness and the
    principled solution to overloading.
Quote:      "Aside from laziness, type classes are undoubtedly Haskell's most distinctive feature."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00 (row written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-classes-as-distinctive-feature)
Rows:       8

C4  L has strong static polymorphic typing with Hindley-Milner inference, inherited from ML via
    Miranda and extended anarchically into a laboratory for type-system research.
Quote:      "Miranda added strong polymorphic typing and type inference, ideas that had proven very
            successful in ML."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00 (row written:2007-06-09_02-the-genesis-of-haskell:miranda-polymorphic-typing)
Rows:       8

C5  Algebraic data types defined as a sum of products, together with top-to-bottom left-to-right
    pattern matching, are fundamental to the language and its readability.
Quote:      "Hope, the language that introduced algebraic data types"
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00 (row written:2007-06-09_02-the-genesis-of-haskell:hope-algebraic-data-types)
Rows:       8

C6  Syntax was treated as the user interface and worked very hard: layout/offside rule, infix
    operators and sections, currying by juxtaposition, few keywords, aiming for programs that look
    like mathematics and read nicely.
Quote:      "Despite this, the Haskell Committee worked very hard...on designing (and arguing about)
            the syntax of Haskell."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00 (row written:2007-06-09_04-syntax:syntax-taken-seriously-despite-dismissal)
Rows:       8

C7  L was built by committee as a conservative common standard embodying consensus (ideally
    tried-and-true ideas) to unite the scattered lazy-functional community, with stability (L 98)
    and a growing community taken as both goal and measure of success.
Quote:      "It was decided that a committee should be formed to design such a language"
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00 (row written:2007-06-09_01-introduction:design-by-committee)
Rows:       8

```
