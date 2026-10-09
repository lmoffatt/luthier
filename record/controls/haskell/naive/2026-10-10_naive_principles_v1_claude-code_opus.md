# Principles of Haskell, asked naively, 2026-10-10

Written by `scripts/naive_principles.py` (naive_principles v1). Prompt `naive_principles_v1` (sha256 f28d1cbd5fe5),
model opus at effort low via claude-code (2.1.197 (Claude Code)); the model saw every row
of the timeline (date, who, the idea) and was asked for the rules and principles, nothing more.
Inputs by sha256: `record/controls/haskell/ideas/timeline.jsonl` a487c657e131.
Rows shown: 387. The quote is the first row each candidate cites, filled in by the script.

```
C1  Haskell is purely functional with no side effects, a firm commitment that made it radical and
    elegant and shaped the whole design.
Quote:      "the nature of the language to be designed (non-strict, purely functional)"
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00 (row written:2007-06-09_01-introduction:nature-non-strict-purely-functional)
Rows:       5

C2  Haskell is non-strict, using lazy (call-by-need) evaluation, prized for its tie to the lambda
    calculus, infinite data structures, and elegant implementation.
Quote:      "the nature of the language to be designed (non-strict, purely functional)"
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00 (row written:2007-06-09_01-introduction:nature-non-strict-purely-functional)
Rows:       5

C3  Type classes, Haskell's most distinctive feature after laziness, provide principled overloading
    and became the framework into which a stream of type-system extensions fitted.
Quote:      "A class declaration specifies the methods of the class ... and their types. A type is
            made into an instance of the class using an instance declaration, which provides an
            implementation for each of the class's methods, at the appropriate instance type."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00 (row written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-class-basic-idea)
Rows:       5

C4  Effects are made explicit and tamed through monads, especially the IO monad, which gives pure
    code a way to do input/output while keeping deterministic semantics.
Quote:      "A monad consists of a type constructor M and a pair of functions, return and >>=
            (sometimes pronounced “bind”)."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00 (row written:2007-06-09_07-monads-and-input-output:monad-definition)
Rows:       5

C5  The language was designed by a committee aiming for a conservative, consensus language that
    united existing groups rather than breaking new ground.
Quote:      "It was decided that a committee should be formed to design such a language"
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00 (row written:2007-06-09_01-introduction:design-by-committee)
Rows:       5

C6  Syntax was treated as the language's user interface and worked on very hard, with the aim that
    expressions look like mathematics and programs look nice.
Quote:      "Despite this, the Haskell Committee worked very hard...on designing (and arguing about)
            the syntax of Haskell."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00 (row written:2007-06-09_04-syntax:syntax-taken-seriously-despite-dismissal)
Rows:       5

C7  Haskell 98 marked a deliberate commitment to long-term stability after years of a frequently
    changing research vehicle, tentatively credited with the community's growth.
Quote:      "this was a very significant moment because it represented a commitment to stability."
Said by:    Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler, 2007-06-09 00:00 (row written:2007-06-09_02-the-genesis-of-haskell:haskell98-commitment-to-stability)
Rows:       5

```
