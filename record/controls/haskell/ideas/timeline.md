# Timeline of ideas about Luthier

Written by `scripts/ideas_timeline.py` (ideas_timeline v1) on 2026-10-09, for Luciano and for the tools that read it.
One row per idea as the extractors found it, in time order; the local times are in America/Argentina/Buenos_Aires, a chat turn's
time is its UTC converted. A note extracted both per note and by day gives two rows, each marked, so a
restatement across notes is told from the same note read twice. Nothing here was judged or merged.

Rows: 387 (written 387). Inputs: 12 files, listed at the end with their sha256.

| month | Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler | total |
|---|---|---|
| 2007-06 | 387 | 387 |

## Ideas, by day

### 2007-06-09

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 01_introduction.md] `written:2007-06-09_01-introduction:community-as-cause-and-indicator-of-success`
  The size, quality, breadth, and depth of the Haskell community are presented as both the indicator of Haskell's success and its cause.
  > The size and quality of the Haskell community, its breadth and its depth, are both the indicator of Haskell’s success and its cause

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 01_introduction.md line 10] `written:2007-06-09_01-introduction:design-by-committee`
  Haskell was to be designed by a committee formed for that purpose, rather than by an individual.
  > It was decided that a committee should be formed to design such a language

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 01_introduction.md] `written:2007-06-09_01-introduction:history-not-technical-description`
  The authors frame the paper's goal as telling the story (who was involved and what inspired them), a history rather than a technical description or tutorial.
  > the paper is supposed to be a history rather than a technical description or a tutorial

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 01_introduction.md line 8] `written:2007-06-09_01-introduction:lack-of-common-language-hampers-use`
  The spread of this class of functional languages was being held back by not having one common language.
  > more widespread use of this class of functional languages was being hampered by the lack of a common language

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 01_introduction.md line 36] `written:2007-06-09_01-introduction:monads-and-io`
  Monads and input/output are named as one of the distinctive areas of the language's evolution.
  > monads and input/output (Section 7)

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 01_introduction.md line 11] `written:2007-06-09_01-introduction:motivation-common-language`
  The motivation for designing Haskell was the need for a common language, meant to speed communication of new ideas, give a stable foundation for real applications, and draw others to use functional languages.
  > providing faster communication of new ideas, a stable foundation for real applications development, and a vehicle through which others would be encouraged to use functional languages

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 01_introduction.md line 16] `written:2007-06-09_01-introduction:nature-non-strict-purely-functional`
  The language to be designed was fixed as non-strict and purely functional.
  > the nature of the language to be designed (non-strict, purely functional)

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 01_introduction.md] `written:2007-06-09_01-introduction:programming-in-the-large`
  Support for programming in the large, such as modules, packages, and the foreign-function interface, is identified as a technical area of Haskell.
  > support for programming in the large, such as modules and packages, and the foreign-function interface (Section 8)

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 01_introduction.md line 5] `written:2007-06-09_01-introduction:proliferation-of-similar-languages-as-problem`
  By 1987 more than a dozen non-strict, purely functional languages existed, all alike in expressive power and semantic underpinnings; this was framed as an unfortunate situation for the community.
  > there had come into being more than a dozen non-strict, purely functional programming languages, all similar in expressive power and semantic underpinnings

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 01_introduction.md] `written:2007-06-09_01-introduction:skew-toward-authors-participation`
  The authors acknowledge their account will be skewed toward the meetings and conversations they personally took part in, an admitted bias in the record.
  > our account will be skewed towards the meetings and conversations in which we personally participated

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 01_introduction.md] `written:2007-06-09_01-introduction:type-classes-as-distinctive`
  Among Haskell's technical contributions, the type system and type classes in particular are singled out as distinctive aspects worth reflection.
  > the type system, and type classes in particular (Section 6)

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 363] `written:2007-06-09_02-the-genesis-of-haskell:adt-extensions`
  Algebraic data types were extended with newtypes, strictness annotations, and named fields.
  > Algebraic data types were extended in several ways: new-

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 204] `written:2007-06-09_02-the-genesis-of-haskell:begin-from-existing-language`
  A key outcome of the first meeting was that the easiest way forward was to start from an existing language and evolve it.
  > the easiest way to move forward was to begin with an existing language, and evolve it in whatever direction suited us.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 39] `written:2007-06-09_02-the-genesis-of-haskell:cons-should-not-evaluate-arguments`
  Friedman and Wise framed lazy evaluation from a Lisp perspective with the slogan that cons should not evaluate its arguments.
  > “Cons should not evaluate its arguments”

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 240] `written:2007-06-09_02-the-genesis-of-haskell:conservative-consensus-intent`
  The committee intended a conservative language that embodied the current consensus of ideas and united the disparate groups, rather than breaking new ground.
  > we intended the language to be quite conservative, rather than to break new ground

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 360] `written:2007-06-09_02-the-genesis-of-haskell:constructor-classes`
  Type classes were generalised to higher kinds, giving constructor classes.
  > Type classes were generalised to higher kinds—so-called “constructor classes”

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 227] `written:2007-06-09_02-the-genesis-of-haskell:debt-to-miranda`
  Despite the fork, Haskell owes Miranda a considerable debt, in general inspiration and in specific elements freely adopted where they fit.
  > Haskell owes a considerable debt to Miranda, both for general inspiration and specific language elements that we freely adopted

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 225] `written:2007-06-09_02-the-genesis-of-haskell:fork-freedom-enabled-type-classes`
  Not starting from Miranda forced a full new design but allowed more radical approaches; type classes would likely not have been developed from a Miranda base.
  > it allowed us the freedom to contemplate more radical approaches to many aspects of the language design. For example, if we had started from Miranda it seems unlikely that we would have developed type classes

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 388] `written:2007-06-09_02-the-genesis-of-haskell:free-online-text-defuses-ip-debate`
  Publishing the Report as a book while keeping the full text freely available online defused a tricky debate about freedom and intellectual property.
  > the entire text could still be available online and be freely usable in that form by anyone

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 4] `written:2007-06-09_02-the-genesis-of-haskell:functional-programming-as-practical-tool`
  Backus's Turing Award lecture recast functional programming as a radical attack on the whole programming enterprise, moving it from mathematical curiosity to practical tool.
  > which positioned functional programming as a radical attack on the whole programming enterprise, from hardware architecture upwards

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 143] `written:2007-06-09_02-the-genesis-of-haskell:g-machine-laziness-not-interpretation`
  The G-machine showed lazy functional programs could be compiled to efficient code, overturning the assumption that laziness meant graph reduction and graph reduction meant interpretation.
  > the influential development of the Gmachine, which showed that one could compile lazy functional programs to rather efficient code

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 245] `written:2007-06-09_02-the-genesis-of-haskell:goals-not-realised`
  Several initial goals were not met: the OL basis was abandoned early, the well-tried-ideas goal was violated (notably by type classes), and no formal semantics was ever developed.
  > We abandoned the idea of basing Haskell explicitly on OL very early; we violated the goal of embodying only well-tried ideas, notably by the inclusion of type classes; and we never developed a formal semantics.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 62] `written:2007-06-09_02-the-genesis-of-haskell:graph-reduction-and-sk-combinators`
  Lazy languages were implemented through graph reduction techniques, notably Turner's elegant use of SK combinators derived from combinatory calculus.
  > a variety of techniques based on graph reduction were being explored, and in particular Turner’s inspirationally elegant use of SK combinators

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 471] `written:2007-06-09_02-the-genesis-of-haskell:haskell-features-in-csharp-and-linq`
  Features of C# were pioneered by Haskell and other functional languages, with LINQ directly inspired by Haskell's monad comprehensions (reported via Erik Meijer).
  > many of the features in C# were pioneered by Haskell and other functional languages, notably polymorphic types and LINQ

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 372] `written:2007-06-09_02-the-genesis-of-haskell:haskell98-commitment-to-stability`
  The Haskell 98 Report represented a deliberate commitment to stability.
  > this was a very significant moment because it represented a commitment to stability.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 84] `written:2007-06-09_02-the-genesis-of-haskell:hope-algebraic-data-types`
  Hope introduced algebraic data types.
  > Hope, the language that introduced algebraic data types

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 12] `written:2007-06-09_02-the-genesis-of-haskell:lambda-calculus-for-modelling-languages`
  Landin and Strachey established the lambda calculus as fundamental for modelling programming languages, grounding both operational and denotational semantics.
  > identified the fundamental importance of the lambda calculus for modelling programming languages

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 394] `written:2007-06-09_02-the-genesis-of-haskell:language-design-is-slow`
  The four years taken to shake down Haskell 98 illustrate that language design is a slow process.
  > Language design is a slow process!

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 117] `written:2007-06-09_02-the-genesis-of-haskell:laziness-as-a-drug`
  The appeal of lazy evaluation lay in its direct connection to the call-by-name lambda calculus, the possibility of infinite data structures, and simple, beautiful implementation techniques.
  > Lazy evaluation—with its direct connection to the pure, call-by-name lambda calculus, the remarkable possibility of representing and manipulating infinite data structures, and addictively simple and beautiful implementation techniques—was like a drug.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 35] `written:2007-06-09_02-the-genesis-of-haskell:lazy-evaluation-invented-three-times`
  Lazy (non-strict, call-by-need) evaluation emerged independently three times, igniting interest in lazy functional languages for serious programs.
  > Lazy evaluation appears to have been invented independently three times.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 54] `written:2007-06-09_02-the-genesis-of-haskell:lazy-lists-emulate-behaviours`
  Turner demonstrated the elegance of programming with lazy evaluation, using lazy lists to emulate many kinds of behaviours.
  > Turner showed the elegance of programming with lazy evaluation, and in particular the use of lazy lists to emulate many kinds of behaviours

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 353] `written:2007-06-09_02-the-genesis-of-haskell:library-report-for-portability`
  Haskell 1.3 added a Library Report, recognising that programs can hardly be portable without standard libraries to rely on.
  > A Library Report was added, reflecting the fact that pro-

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 369] `written:2007-06-09_02-the-genesis-of-haskell:list-comprehensions-over-monads-reversed`
  Haskell 1.4 generalised list comprehensions to arbitrary monads, a decision reversed two years later (reverted to just lists in Haskell 98).
  > list comprehensions were generalised to arbitrary monads, a decision that was reversed two years later.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 209] `written:2007-06-09_02-the-genesis-of-haskell:miranda-most-mature-candidate`
  Of the lazy languages, Miranda was the most mature (pure, well designed, robustly implemented, widely deployed), making it the natural starting-point candidate.
  > David Turner’s Miranda was by far the most mature. It was pure, well designed, fulfilled many of our goals

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 139] `written:2007-06-09_02-the-genesis-of-haskell:miranda-polymorphic-typing`
  Where SASL and KRC were untyped, Miranda added strong polymorphic typing and type inference, ideas proven successful in ML.
  > Miranda added strong polymorphic typing and type inference, ideas that had proven very successful in ML.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 268] `written:2007-06-09_02-the-genesis-of-haskell:moment-of-naming`
  The authors treat the moment a language is named as a small but important moment in its evolution.
  > a small but important moment in any language’s evolution is the moment it is named

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 356] `written:2007-06-09_02-the-genesis-of-haskell:monadic-io-and-do`
  Haskell 1.3 introduced monadic I/O with "do" syntax, dropping the earlier I/O semantics in the Appendix.
  > Monadic I/O made its first appearance, including “do” syn-

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 68] `written:2007-06-09_02-the-genesis-of-haskell:non-von-neumann-hardware-dead-end`
  A hope was that lazy evaluation would lead to radically different non-von Neumann hardware; much of this work later proved a dead end when stock-architecture compilers outperformed specialised machines.
  > the possibility that all this would lead to a radically different non-von Neumann hardware architectures

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 256] `written:2007-06-09_02-the-genesis-of-haskell:ol-as-default-solution`
  The committee process used OL's design as the described default, to be kept for any topic lacking a clearly better solution.
  > OL will be the default if no clearly better solution exists.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 377] `written:2007-06-09_02-the-genesis-of-haskell:open-participation-benign-dictator`
  After the committee ceased, decisions were no longer limited to a small group; anyone on the mailing list could participate, with Peyton Jones as editor of linguistic minutiae.
  > Decisions were no longer limited to a small committee; now anyone reading the Haskell mailing list could participate.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 330] `written:2007-06-09_02-the-genesis-of-haskell:public-vs-private-governance`
  Discomfort with the "us-and-them" of having both public and private mailing lists led debate to move fully public, though decisions were still made by the committee.
  > Members of the committee became increasingly uncomfortable with the “us-and-them” overtones of having both public and private mailing lists

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 57] `written:2007-06-09_02-the-genesis-of-haskell:pure-lazy-fp-in-the-large`
  SASL was used at Burroughs to build an entire operating system, likely the first exercise of pure, lazy, functional programming at large scale.
  > SASL was even used at Burroughs to develop an entire operating system—almost certainly the first exercise of pure, lazy, functional programming “in the large”.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 20] `written:2007-06-09_02-the-genesis-of-haskell:sasl-sugared-lambda-with-pattern-matching`
  Turner's SASL was a pure higher-order functional language, a sugared lambda calculus with lexical scoping, that brought Burstall and Darlington's pattern matching into an executable language.
  > a pure higher-order functional language with lexically scoped variables

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 124] `written:2007-06-09_02-the-genesis-of-haskell:simulate-call-by-name-easier`
  Reported from an anonymous reviewer: Sussman and Steele kept Scheme call-by-value, reasoning that simulating call-by-name in a call-by-value language (via thunks) is easier than the reverse.
  > reasoning that it seemed to be much easier to simulate call-by-name in a call-by-value language (using lambda-expressions as thunks) than to simulate call-by-value in a call-by-name language

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 180] `written:2007-06-09_02-the-genesis-of-haskell:tower-of-babel-common-language`
  The many single-site lazy languages were felt to be roughly the same bar syntax, prompting the wish for a single, common language all could benefit from.
  > we felt that they were all roughly the same, bar the syntax, and we started to wonder why we didn’t have a single, common language that we could all benefit from.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 02_the-genesis-of-haskell.md line 217] `written:2007-06-09_02-the-genesis-of-haskell:turner-declined-goals-differed`
  Turner declined to let Miranda be the basis: the committee wanted freedom for anyone to extend, modify and distribute the language, while Turner was committed to a single portable standard with no dialects.
  > we sought the freedom for anyone to extend or modify the language, and to build and distribute an implementation. Turner, by contrast, was strongly committed to maintaining a single language standard

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 242] `written:2007-06-09_04-syntax:abandon-just-one-way`
  An underlying assumption that there should be "just one way to do something" (making let and where redundant) was abandoned; full support for both styles was provided and is now regarded as a strength, its extra complexity superficial and explained by syntactic transformations.
  > In the end, we abandoned the underlying assumption, and provided full syntactic support for both styles.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 43] `written:2007-06-09_04-syntax:anonymous-function-backslash`
  The `\x -> exp` syntax for anonymous functions was chosen to resemble lambda, with backslash as the closest ASCII to λ, and `->` used instead of a period so the period could be reserved for function composition.
  > the backslash was the closest single ASCII character to the Greek letter λ. However, "->" was used instead of a period in order to reserve the period for function composition.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 103] `written:2007-06-09_04-syntax:application-by-juxtaposition`
  Function application is denoted by juxtaposition and associates to the left, so `f x y` parses as `(f x) y`, leading to concise and powerful code.
  > Function application is denoted by juxtaposition and associates to the left. Thus, f x y is parsed (f x) y.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 85] `written:2007-06-09_04-syntax:at-patterns-bind-tightly-mistake`
  The simple binding rule is not followed by @-patterns, which bind more tightly than anything; this was probably a mistake, though not a major problem given their limited use.
  > Sadly, this simple rule is not adhered to by @-patterns, which bind more tightly than anything; this was probably a mistake

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 30] `written:2007-06-09_04-syntax:avoid-semicolon-no-sequencing`
  Because a language without side effects has no notion of sequencing, the committee chose to avoid the semicolon and its imperative baggage, while still separating declarations.
  > the feeling of the Haskell Committee was that we should avoid the semicolon and its sequential, imperative baggage.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 150] `written:2007-06-09_04-syntax:backquotes-function-to-infix`
  Having converted infix operators into values via sections, the committee added the reverse: enclosing a function identifier in backquotes makes it infix, as in `x \`elem\` xs`, valued for generality and readability; Miranda used a similar `$elem` notation from PAL.
  > Our simple solution was to enclose a function identifier in backquotes. For example, x 'f' y is the same as f x y.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 173] `written:2007-06-09_04-syntax:capitalisation-and-colon-conventions`
  From Miranda, data constructors are capitalised and variables are not; infix constructors must start with a colon, chosen for consistency with using single colon `:` for list cons, with `::` for type signatures, a choice opposite to ML and still controversial.
  > We adopted from Miranda the convention that data constructors are capitalised while variables are not, and added a similar convention for infix constructors, which in Haskell must start with a colon.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 90] `written:2007-06-09_04-syntax:complex-layout-rule-programmer-expects`
  Driven by the constraints and a desire to do what the programmer expects, Haskell evolved a fairly complex layout rule, complex enough to be formally specified first in the Haskell 98 Report, yet most users adopt a conforming style.
  > Influenced by these constraints and a desire to "do what the programmer expects", Haskell evolved a fairly complex layout rule

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 313] `written:2007-06-09_04-syntax:comprehensions-popular-in-lazy-languages`
  For some reason list comprehensions seem more popular in lazy languages, found in Miranda and Haskell but not SML or Scheme, though present in Erlang and later added to Python and planned for Javascript.
  > list comprehensions seem to be more popular in lazy languages; for example they are found in Miranda and Haskell, but not in SML or Scheme.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 108] `written:2007-06-09_04-syntax:curried-and-uncurried-both-supported`
  Like other lambda-calculus-based languages, Haskell supports both curried and uncurried definitions.
  > Haskell, like many other languages based on lambda calculus, supports both curried and uncurried definitions:

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 99] `written:2007-06-09_04-syntax:currying`
  Following a tradition from Frege, honed by Schönfinkel and Curry, a function of two arguments is represented as a one-argument function returning a one-argument function; one advantage is that curried form is often more compact.
  > a function of two arguments may be represented as a function of one argument that itself returns a function of one argument.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 196] `written:2007-06-09_04-syntax:declaration-vs-expression-style`
  Two styles of writing functional programs emerged: declaration style (multiple equations with pattern matching and guards, where clauses, arguments on the left) and expression style (composing expressions, with let, lambda, case, if).
  > there were two different styles in which functional programs could be written: "declaration style" and "expression style".

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 188] `written:2007-06-09_04-syntax:few-reserved-keywords`
  Keeping the number of reserved keywords low (21, against higher counts in other languages) was a priority, and the committee tried to avoid keywords like "as" that might be useful variable names.
  > Haskell has 21 reserved keywords that cannot be used as names for values or types... keeping it low was a priority of the Haskell Committee.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 113] `written:2007-06-09_04-syntax:first-class-values-and-infix-ambiguity`
  The feeling that all values, especially functions, should be first class clashed with infix operators not being first class, a problem made apparent by the ambiguity of `f + x`.
  > there was also the feeling that all values in Haskell should be "first class"—especially functions.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 272] `written:2007-06-09_04-syntax:guards-moved-to-left`
  Where Miranda placed guards on the far right of equations resembling mathematics, Haskell moved them to the left-hand side, better for long definitions, placing the guard next to the patterns and in a place suggestive of evaluation order, viewed as an improvement over mathematical notation.
  > we moved them to the left-hand side of the definition... which had the added benefit of placing the guard right next to the patterns on formal parameters... and in a place more suggestive of the evaluation order

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 18] `written:2007-06-09_04-syntax:haskell-is-a-pretty-language`
  A pleasing, though not explicit, consequence of the effort on syntax is the repeated comment that Haskell programs look nice.
  > one of the most pleasing consequences of our effort has been comments heard... that "Haskell is a pretty language."

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 81] `written:2007-06-09_04-syntax:infix-binds-less-tightly`
  Infix application always binds less tightly than conventional function application, so expressions like `f x + g y` never need parentheses; this decision proved good for readability.
  > the former always binds less tightly than the latter. Thus f x + g y never needs parentheses, regardless of what infix operator is used.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 74] `written:2007-06-09_04-syntax:infix-operators-like-mathematics`
  Wanting expressions to look like mathematics, the committee adopted infix operators from day one, in contrast to Scheme's consistent prefix application.
  > The Haskell Committee wanted expressions to look as much like mathematics as possible, and thus from day one we bought into the idea that Haskell would have infix operators.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 47] `written:2007-06-09_04-syntax:layout-avoids-clutter`
  Exploiting the physical layout of the program, via the offside rule, is a simple and elegant way to avoid syntactic clutter; the idea was familiar from SASL and Miranda and goes back to CPL and ISWIM.
  > Exploiting the physical layout of the program text is a simple and elegant way to avoid syntactic clutter.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 61] `written:2007-06-09_04-syntax:layout-rules-simple-and-lenient`
  The layout rules had to be very simple, and after exploring variations the committee adopted a design more lenient than Miranda's, supporting larger function definitions with less enforced indentation, because programmers would want large definitions and layout shouldn't get in the way.
  > We ended up with a design that differed from our most immediate inspiration, Miranda, in supporting larger function definitions with less enforced indentation.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 294] `written:2007-06-09_04-syntax:list-comprehensions`
  List comprehensions give a convenient notation for maps, filters, and Cartesian products; first suggested by Darlington, popularised and generalised to lazy lists by Turner in KRC as "ZF expression", and named "list comprehension" by Wadler.
  > List comprehensions provide a very convenient notation for maps, filters, and Cartesian products.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 339] `written:2007-06-09_04-syntax:literate-comments`
  Haskell added literate comments (from OL, suggested by Bird, inspired by Knuth's literate programming): reversing the usual convention so code lines carry a special mark, a `>` ("Bird tracks"), with a later Latex-style form marking code by `\begin{code}` and `\end{code}` so one file serves as both typeset paper and program.
  > proposed reversing the usual comment convention: lines of code, rather than lines of comment, should be the ones requiring a special mark.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 95] `written:2007-06-09_04-syntax:many-ways-to-define-functions`
  Haskell offers many ways to define functions, but they are simple and all fit together sensibly.
  > There are lots of ways to define functions in Haskell...but the ways are simple and all fit together in a sensible manner.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 140] `written:2007-06-09_04-syntax:minus-42-section-problem`
  Sections introduced an ambiguity around negation: `(-42)` means negative 42, so one must write `\x-> x-42` or `(subtract 42)`; this was viewed as a problem with prefix operators rather than sections, and the committee chose not to buck convention on negation.
  > what is the meaning of (-42)? The answer is negative 42!

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 161] `written:2007-06-09_04-syntax:namespaces-orthogonal-and-overlapping`
  Namespaces were defined to give users freedom while avoiding ambiguity: lexemes orthogonal when they needed to be and overlapping when context was sufficient, so a capitalised name like `Foo` can refer to type constructor, data constructor, and module at once.
  > we carefully defined a set of lexemes for each namespace that were orthogonal when they needed to be, and overlapped when context was sufficient to distinguish their meaning.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 54] `written:2007-06-09_04-syntax:one-prefix-operator-negation`
  Haskell has only one prefix operator, arithmetic negation; the committee wanted none but couldn't force users to write `minus 42` or `~42` instead of `-42`, and the scarcity of prefix operators makes parsing easier.
  > The Haskell Committee in fact did not want any prefix operators, but we couldn't bring ourselves to force users to write something like minus 42 or ~42 for the more conventional -42.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 70] `written:2007-06-09_04-syntax:override-layout-for-generated-programs`
  Like Miranda, Haskell lets the user override implicit layout with explicit curly braces and semicolons, thought important because people were expected to write programs that generate Haskell programs, for which explicit separators are easier to generate than layout.
  > we expected people to write programs that generated Haskell programs, and we thought it would be easier to generate explicit separators than layout.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 121] `written:2007-06-09_04-syntax:sections`
  The solution was a generalised notion of sections (from Wile's dissertation, via IFIP WG2.1 to Bird and Turner/Miranda): a partial application of an infix operator that, parenthesised, yields a first-class functional value, consistent with partial application of curried functions.
  > A section is a partial application of an infix operator to no arguments, the left argument, or the right argument—and by surrounding the result in parentheses, one then has a first-class functional value.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 184] `written:2007-06-09_04-syntax:shadowing-allowed`
  A minority argued against allowing variable shadowing to avoid accidental capture, but outlawing it is inconsistent with alpha renaming, so in the end Haskell allowed shadowing.
  > outlawing shadowing is inconsistent with alpha renaming... So, in the end, Haskell allowed shadowing.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 14] `written:2007-06-09_04-syntax:syntax-as-personal-user-interface`
  Syntax is the user interface of a language and can become very personal, which is why some of the committee's most heated debates were over syntax.
  > We also found that syntax, being the user interface of a language, could become very personal.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 8] `written:2007-06-09_04-syntax:syntax-taken-seriously-despite-dismissal`
  Against the common view that syntax is trivial and semantics is where the real work lies, the Haskell Committee worked very hard on designing the syntax.
  > Despite this, the Haskell Committee worked very hard...on designing (and arguing about) the syntax of Haskell.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 333] `written:2007-06-09_04-syntax:two-comment-styles`
  Haskell originally supported two comment styles, short comments with `--` to newline and longer nestable comments with `{-` and `-}`, the longer form designed to make it easy to comment out code, including code containing comments.
  > The longer form was designed to make it easy to comment out segments of code, including code containing comments.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 77] `written:2007-06-09_04-syntax:user-definable-infix-operators`
  It was important that infix operators be definable by the user, including declarations of precedence and associativity.
  > It was also important to us that infix operators be definable by the user, including declarations of precedence and associativity.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 322] `written:2007-06-09_04-syntax:wadlers-law-of-effort`
  Wadler's law describes how committee effort was allotted: semantics discussed half as much as syntax, syntax half as much as lexical syntax, lexical syntax half as much as the syntax of comments, an exaggeration that still reflected strong views on low-level details.
  > semantics is discussed half as much as syntax, syntax is discussed half as much as lexical syntax, and lexical syntax is discussed half as much as the syntax of comments.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 04_syntax.md line 279] `written:2007-06-09_04-syntax:where-attached-to-declaration`
  Adopted from Miranda, a where clause is attached to a declaration (not an expression) and scopes over the guards as well as the right-hand sides; its bindings are lazy, so a binding used in only one clause is fine.
  > a where clause is attached to a declaration, not an expression, and scopes over the guards as well as the right-hand sides of the declarations.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 123] `written:2007-06-09_05-data-types-and-pattern-matching:abstract-type-distinct-class-instance`
  The most important point is that Haskell's approach allows a different type-class instance for the abstract type than for its representation, which it was unclear how to do with abstype.
  > The most important point is that Haskell's solution allows one to give a different instance to a type-class for the abstract type than for its representation ... It was unclear to us how to achieve this effect with abstype.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 121] `written:2007-06-09_05-data-types-and-pattern-matching:abstract-types-tradeoff`
  Haskell's solution is cluttered by the extra constructor but avoids an extra construct and lets operation types be inferred.
  > Haskell's solution is somewhat cluttered by the Stk constructors, but in exchange an extra construct is avoided, and the types of the operations can be inferred if desired.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 105] `written:2007-06-09_05-data-types-and-pattern-matching:abstract-types-via-module-system`
  Instead of Miranda's special abstype construct, Haskell uses the module system for data abstraction: declare an algebraic type, export the type but hide its constructors.
  > In Haskell, instead of a special construct, the module system is used to support data abstraction. One constructs an abstract data type by introducing an algebraic type, and then exporting the type but hiding its constructors.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 11] `written:2007-06-09_05-data-types-and-pattern-matching:algebraic-types-history`
  Algebraic types first appeared in Burstall's NPL and Hope, were absent from original ML and KRC, and appeared in their successors Standard ML and Miranda; conditional guards came from Turner's KRC.
  > Algebraic types as a programming language feature first appeared in Burstall's NPL ... They were absent from the original ML ... and KRC ..., but appeared in their successors Standard ML ... and Miranda ... Equations with conditional guards were introduced by Turner in KRC

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 5] `written:2007-06-09_05-data-types-and-pattern-matching:basic-algebraic-types-straightforward-rest-interesting`
  Including basic algebraic types was easy, but pattern matching, abstract types, tuples, newtypes, records, n+k patterns and views raised interesting issues.
  > The inclusion of basic algebraic types was straightforward, but interesting issues arose for pattern matching, abstract types, tuples, new types, records, n+k patterns, and views.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 132] `written:2007-06-09_05-data-types-and-pattern-matching:bottom-value-every-type`
  An expression that diverges or calls error has the value "bottom" (⊥), a value belonging to every type.
  > An expression that diverges (or calls Haskell's error function) is considered to have the value 'bottom', usually written ⊥, a value that belongs to every type.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 60] `written:2007-06-09_05-data-types-and-pattern-matching:capitalization-rule-extended-to-types`
  Haskell extended the capitalization rule to type constructors and type variables, an unusual uniform rule that differed from Standard ML's tick and Miranda's asterisks.
  > Haskell further extended this rule to apply to type constructors ... and type variables ... This uniform rule was unusual.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 55] `written:2007-06-09_05-data-types-and-pattern-matching:capitalized-constructors-from-miranda`
  Haskell took from Miranda the rule that constructor names begin with a capital, making constructors easy to distinguish from variables, unlike Standard ML's lower case for both.
  > Haskell also took from Miranda the rule that constructor names always begin with a capital, making it easy to distinguish constructors ... from variables ... In Standard ML, it is common to use lower case for both

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 30] `written:2007-06-09_05-data-types-and-pattern-matching:data-constructors-two-roles`
  Data constructors serve both in pattern matching to decompose a value and in expressions to build a value.
  > Data constructors can be used both in pattern-matching, to decompose a value of Maybe type, and in an expression, to build a value of Maybe type.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 3] `written:2007-06-09_05-data-types-and-pattern-matching:data-types-and-pattern-matching-fundamental`
  Data types and pattern matching are fundamental to most modern functional languages, Scheme being a notable exception.
  > Data types and pattern matching are fundamental to most modern functional languages (with the notable exception of Scheme).

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 52] `written:2007-06-09_05-data-types-and-pattern-matching:empty-type-not-appreciated`
  A sum of zero alternatives, a completely empty type, might have been useful but its value was not appreciated at the time.
  > It might have been useful to permit a sum of zero alternatives, which would be a completely empty type, but at the time the value of such a type was not appreciated.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 7] `written:2007-06-09_05-data-types-and-pattern-matching:equations-with-pattern-matching-lineage`
  The style of writing functional programs as equations with pattern matching over algebraic types traces back to Burstall's structural induction and his program-transformation work with Darlington.
  > The style of writing functional programs as a sequence of equations with pattern matching over algebraic types goes back at least to Burstall's work on structural induction ... and his work with his student Darlington on program transformation

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 66] `written:2007-06-09_05-data-types-and-pattern-matching:lazy-pattern-matching-semantics-complex`
  Pattern matching semantics is more complex in lazy languages because the choice to match first against a variable or a constructor can change whether a program terminates.
  > The semantics of pattern matching in lazy languages is more complex than in strict languages, because laziness means that whether one chooses to first match against a variable ... or a constructor ... can change the semantics of a program, in particular, whether or not the program terminates.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 193] `written:2007-06-09_05-data-types-and-pattern-matching:let-where-always-lazy-wart`
  Pattern matching in let and where clauses is always lazy, unlike case/λ; this difference can be considered a wart that complicates the language description.
  > pattern matching in let and where clauses is always lazy ... (This difference in the semantics of pattern matching between let/where and case/λ can perhaps be considered a wart on the language design—certainly it complicates the language description.)

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 184] `written:2007-06-09_05-data-types-and-pattern-matching:lifted-decision-and-tilde-patterns`
  In the end tuples and algebraic data types were made lifted so pattern matching always induces evaluation, with an uneasy compromise of reintroducing lazy matching via tilde-patterns.
  > we decided to make both tuples and algebraic data types have a lifted semantics, so that pattern matching always induces evaluation. However, in a somewhat uneasy compromise, we also reintroduced lazy pattern-matching, in the form of tilde-patterns

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 135] `written:2007-06-09_05-data-types-and-pattern-matching:lifted-vs-unlifted-tuple-semantics`
  There is a choice whether ⊥ and (⊥, ⊥) are distinct: a lifted tuple semantics distinguishes them, an unlifted semantics treats them as the same.
  > are ⊥ and (⊥, ⊥) distinct values? In the jargon of denotational semantics, a lifted tuple semantics distinguishes the two values, while an unlifted semantics treats them as the same value.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 86] `written:2007-06-09_05-data-types-and-pattern-matching:matching-tradeoff-equational-reasoning`
  Top-to-bottom matching was simple, fit guards, and was more expressive, but the rejected alternatives had an order-independent semantics that aids equational reasoning; the widely used design was chosen over one programmers might find limiting.
  > But the other alternatives had a semantics in which the order of equations did not matter, which aids equational reasoning ... In the end, it was thought better to adopt the more widely used top-to-bottom design than to choose something that programmers might find limiting.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 222] `written:2007-06-09_05-data-types-and-pattern-matching:minimal-records-leave-field-open`
  The minimal design left the field open for more sophisticated proposals such as TRex, with new proposals and type-class encodings continuing to appear.
  > This minimal design has left the field open for more sophisticated proposals, of which the best documented is TRex ... New record proposals continue to appear regularly on the Haskell mailing list

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 216] `written:2007-06-09_05-data-types-and-pattern-matching:minimalist-record-syntax`
  Under user pressure, Haskell 1.3 adopted Mark Jones's minimalist design: record syntax is syntactic sugar for operations on regular algebraic data types, with no record polymorphism or subtyping.
  > the committee eventually adopted a minimalist design originally suggested by Mark Jones: record syntax in Haskell 1.3 ... is simply syntactic sugar for equivalent operation on regular algebraic data types. Neither record-polymorphic operations nor subtyping are supported.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 166] `written:2007-06-09_05-data-types-and-pattern-matching:miranda-currying-isomorphism`
  The semantic point became a controversy in the committee; Miranda identified ⊥ with (⊥, ⊥), which influenced them and made currying an exact isomorphism.
  > Miranda's design identified ⊥ with (⊥, ⊥), which influenced us considerably. Furthermore, this identification made currying an exact isomorphism

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 251] `written:2007-06-09_05-data-types-and-pattern-matching:n-plus-k-controversy`
  n+k patterns provoked controversy: some found them essential for defining functions by cases over the naturals, others worried that Int did not denote the natural numbers.
  > Some users considered n+k patterns essential, because they allowed function definition by cases over the natural numbers ... But others worried that the Int type did not, in fact, denote the natural numbers.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 270] `written:2007-06-09_05-data-types-and-pattern-matching:n-plus-k-horse-trading`
  The majority of the committee suggested removing n+k patterns; in rare horse-trading, Hudak tried to convince Wadler, who agreed only if another feature went, and in the end n+k patterns stayed.
  > One of the very few bits of horse-trading in the design of Haskell occurred when Hudak ... tried to convince Wadler to agree to remove n+k patterns. Wadler said he would agree to their removal only if some other feature went ... In the end, n+k patterns stayed.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 243] `written:2007-06-09_05-data-types-and-pattern-matching:n-plus-k-origin`
  n+k patterns were suggested by Wadler, who first saw them in Gödel's incompleteness proof, and were earlier in Darlington's NPL and (at Wadler's instigation) in Miranda.
  > Patterns of the form n+k were suggested for Haskell by Wadler, who first saw them in Gödel's incompleteness proof ... They were earlier incorporated into Darlington's NPL ... and (partially at Wadler's instigation) into Miranda.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 255] `written:2007-06-09_05-data-types-and-pattern-matching:n-plus-k-overloading-complexity`
  Because numeric literals were overloaded, fib's type consistently became Num a => a -> a (one could apply fib to matrices), substantially increasing the complexity of pattern matching, which now had to invoke overloaded comparison and arithmetic.
  > it seemed only consistent that fib's type should be fib :: Num a => a -> a ... This gave rise to a substantial increase in the complexity of pattern matching, which now had to invoke overloaded comparison and arithmetic operations.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 232] `written:2007-06-09_05-data-types-and-pattern-matching:n-plus-k-patterns`
  Haskell provides n+k patterns to get the benefits of pattern matching without the loss of efficiency; n+k matches m only if m ≥ k and binds n to m − k, and can be seen as a special case of a view with convenient syntax.
  > Haskell provides so-called n+k patterns that provide the benefits of pattern matching without the loss of efficiency. (The n+k pattern feature can be considered a special case of a view ... combined with convenient syntax.)

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 264] `written:2007-06-09_05-data-types-and-pattern-matching:n-plus-k-syntactic-ambiguity`
  n+k produced syntactic niceties where apparently redundant brackets change meaning: n + 1 = 7 defines +, while (n + 1) = 7 defines n.
  > n + 1 = 7 is a (function) definition of +, while (n + 1) = 7 is a (pattern) definition of n—so apparently redundant brackets change the meaning completely!

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 230] `written:2007-06-09_05-data-types-and-pattern-matching:nat-type-inefficient-unary`
  A type isomorphic to the natural numbers allows pattern matching in definitions but its unary representation is far less efficient than built-in integers.
  > This definition has the advantage that one can use pattern matching in definitions, but the disadvantage that the unary representation implied in the definition is far less efficient than the built-in representation of integers.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 152] `written:2007-06-09_05-data-types-and-pattern-matching:newtype-motivation-isomorphic-abstract-types`
  newtype's main motivation was abstract data types: lifting made Stack not quite isomorphic to lists by adding a bottom distinct from Stk ⊥, and newtype defines a type isomorphic to an existing one.
  > The main motivation for introducing this had to do with abstract data types. It was unfortunate that the Haskell definition of Stack given above forced the representation of stacks to be not quite isomorphic to lists ... We can view this as a way to define a new type isomorphic to an existing one.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 206] `written:2007-06-09_05-data-types-and-pattern-matching:newtype-single-constructor-choice`
  The lifted/unlifted choice arose for any single-constructor algebraic type; from Haskell 1.0 single-constructor types were lifted, and from 1.3 newtype gave a second way to introduce an unlifted single-constructor single-component type.
  > From Haskell 1.0, it was decided that algebraic types with a single constructor should have a lifted semantics. From Haskell 1.3 onwards ... a second way to introduce a new algebraic type with a single constructor and a single component, with an unlifted semantics.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 34] `written:2007-06-09_05-data-types-and-pattern-matching:pattern-matching-increases-readability`
  Pattern matching against algebraic data types greatly increases readability.
  > The use of pattern matching against algebraic data types greatly increases readability.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 211] `written:2007-06-09_05-data-types-and-pattern-matching:records-no-right-design`
  The strongest reason records were omitted was that there was no obvious "right" design: many record systems exist, all complicating an already complicated type system, and type classes could encode some of their power.
  > The strongest reason seems to have been that there was no obvious 'right' design. There are a huge number of record systems ... All of them have a complicating effect on the type system ... type classes could be used to encode at least some of the power of records.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 172] `written:2007-06-09_05-data-types-and-pattern-matching:records-omitted-despite-usefulness`
  One of the most obvious omissions from early Haskell was records with named fields, despite their usefulness in practice.
  > One of the most obvious omissions from early versions of Haskell was the absence of records, offering named fields. Given that records are extremely useful in practice, why were they omitted?

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 74] `written:2007-06-09_05-data-types-and-pattern-matching:rejected-matching-alternatives`
  Tightest match, sequential equations, and uniform patterns were considered at length and rejected.
  > after considering at length and rejecting some other possibilities: • Tightest match ... • Sequential equations ... • Uniform patterns

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 176] `written:2007-06-09_05-data-types-and-pattern-matching:single-constructor-sharing-tuple-properties-difficulty`
  A difficulty was whether single-constructor data types should share tuple properties, with a semantic discontinuity appearing when a second constructor is added.
  > should single constructor data types ... share the same properties as tuples, with a semantic discontinuity induced by adding a second constructor?

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 43] `written:2007-06-09_05-data-types-and-pattern-matching:sum-of-products-from-miranda`
  Haskell took from Miranda the notion of defining algebraic types as a "sum of products", in contrast to Hope and Standard ML which separated sums and products.
  > Haskell took from Miranda the notion of defining algebraic types as a 'sum of products'. ... In contrast, Hope and Standard ML separated sums (algebraic types) and products (tuple types)

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 70] `written:2007-06-09_05-data-types-and-pattern-matching:top-to-bottom-left-to-right-matching`
  Haskell adopted top-to-bottom, left-to-right equation matching as in SASL, KRC and Miranda; left-to-right matters in a lazy language since a non-match passes to the next equation, avoiding nontermination.
  > matching is from left to right within each left-hand-side—which is important in a lazy language, since as soon as a non-matching pattern is found, matching proceeds to the next equation, potentially avoiding nontermination or an error in a match further to the right.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 141] `written:2007-06-09_05-data-types-and-pattern-matching:unlifted-distinguished-only-by-pattern-matching`
  Under unlifted semantics the two values are indistinguishable except possibly by pattern matching, which can be instead read as binding via fst and snd so the two remain indistinguishable.
  > The only way in which they might be distinguished is by pattern matching ... One can instead consider this definition to be equivalent to ... in which case f ⊥ = True and the two values are indistinguishable.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 181] `written:2007-06-09_05-data-types-and-pattern-matching:unlifted-tuples-incompatible-with-seq`
  The unlifted form of tuples is essentially incompatible with seq, since parallel evaluation would be required to implement seq on them; efficiency and space leaks of lazy matching were also concerns.
  > the unlifted form of tuples is essentially incompatible with seq ... because parallel evaluation would be required to implement seq on unlifted tuples.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 277] `written:2007-06-09_05-data-types-and-pattern-matching:views-ease-abstraction-tension`
  Wadler noticed a tension between the convenience of pattern matching and the advantages of data abstraction, and suggested views to lessen it; a view specifies an isomorphism letting constructors of an algebraic type appear in patterns matching the other type.
  > Wadler had noticed there was a tension between the convenience of pattern matching and the advantages of data abstraction, and suggested views as a programming language feature that lessens this tension. A view specifies an isomorphism between two data types ... and then permits constructors of the second type to appear in patterns that match against the first

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 288] `written:2007-06-09_05-data-types-and-pattern-matching:views-never-returned`
  Despite Peyton Jones wanting views in an experimental extension and a detailed 1.3 proposal by Burton and others, views never made it back into the language or into implementations.
  > a detailed proposal to include views in Haskell 1.3 was put forward by Burton and others ... But views never made it back into the language nor appeared among the many extensions available in some implementations.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 284] `written:2007-06-09_05-data-types-and-pattern-matching:views-removed`
  The original Haskell included views, based on constructors and views being indistinguishable, which complicated export lists and derived type classes; by April 1989 Wadler argued the language could be simplified by removing them.
  > The original design of Haskell included views, and was based on the notion that the constructors and views exported by a module should be indistinguishable. This led to complications in export lists and derived type classes, and by April 1989 Wadler was arguing that the language could be simplified by removing views.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 05_data-types-and-pattern-matching.md line 296] `written:2007-06-09_05-data-types-and-pattern-matching:views-tried-and-true-criterion`
  Views or similar features are discussed for Haskell′ but are unlikely to be included because they do not satisfy the criterion of being "tried and true".
  > they are unlikely to be included as they do not satisfy the criterion of being 'tried and true'.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 129] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:ambiguity-in-type-classes`
  A second difficulty with type classes is ambiguity: when nothing fixes the type of an intermediate subexpression and the choice affects the program's semantics, the program is rejected and the programmer adds a type signature.
  > we rapidly discovered a second source of difficulty with type classes, namely ambiguity.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 477] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:anarchic-development`
  Haskell's type system developed anarchically, with features sketched, implemented, and applied before formalisation; the strength is faster exploration of the design space, the weakness is extreme complexity and programs reduced to experiments on the compiler.
  > Haskell's type system has developed extremely anarchically. Many of the new features described above were sketched, implemented, and applied well before they were formalised.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 486] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:attempts-to-bring-order`
  Notable attempts brought some order: a static semantics for all of Haskell 98, Jones's theory of qualified types subsuming type classes, implicit parameters and extensible records, a complete type-inference engine in code, and a constraint-handling-rules framework; still the result is dauntingly complicated.
  > Some notable attempts have been made to bring order to this chaos.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 500] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:awaiting-unifying-insight`
  The authors sense they are still awaiting a unifying insight that would explain and simplify the chaotic world of type classes without throwing out the baby with the bath water.
  > we are still awaiting a unifying insight that will not only explain but also simplify the chaotic world of type classes, without throwing the baby out with the bath water.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 39] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:bounded-quantification`
  A type class constraint expresses a form of bounded quantification: a function is typed for any type that is an instance of a given class.
  > The type signature for member uses a form of bounded quantification: it declares that member has type a -> [a] -> Bool, for any type a that is an instance of the class Eq.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 240] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:committee-resistant-to-multi-parameter`
  The committee resisted multi-parameter type classes, feeling single-parameter classes already went far beyond their conservative goals and that going further was an unforced step into the dark, with worries about overlap, confluence, and decidability; Haskell 98 kept the single-parameter restriction.
  > Going beyond that would be an unforced step into the dark, and we were anxious about questions of overlap, confluence, and decidability of type inference.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 178] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:constructor-classes-higher-kinded`
  Mark Jones's constructor classes parameterise a class over a type constructor instead of a type, giving higher-kinded polymorphism; the type variable has kind *->*.
  > Mark Jones ... suggested parameterising a class over a type constructor instead of over a type, an idea he called constructor classes ...

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 166] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:defaulting-clumsy-but-conservative`
  The defaulting rule is clumsy but conservative, avoiding arbitrary choices except in tightly constrained cases; it seems too conservative for interpreters, so GHCi relaxes it further.
  > This rule is clumsy but conservative: it tries to avoid making an arbitrary choice in all but a few tightly constrained situations.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 45] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:dictionary-passing-translation`
  Type classes can be translated into dictionary-passing style by a type-directed transformation: a class becomes a data type (a record of methods), a constraint becomes a dictionary parameter, and an instance becomes a function from dictionaries to a dictionary.
  > A particularly attractive feature of type classes is that they can be translated into so-called \"dictionary-passing style\" by a typedirected transformation.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 85] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:dynamic-semantics-depends-on-type-checker`
  Unlike most statically typed languages, Haskell's dynamic semantics depends on how type-class overloading is resolved by the type checker, which makes it harder for the programmer to reason about execution.
  > Not so in Haskell: the dynamic semantics of the program necessarily depends on the way that its type-class overloading is resolved by the type checker.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 318] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:existential-data-constructors`
  Perry showed existential quantification of a value packaged with functions over it could be expressed with almost no new complexity, by letting a data constructor mention type variables in its arguments that do not appear in its result; later formalised and integrated with type classes, now universally supported.
  > this pattern could be expressed with almost no new language complexity, simply by allowing a data constructor to mention type variables in its arguments that do not appear in its result.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 338] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:extensible-records-trex`
  Jones showed type classes are an instance of a more general framework, qualified types; a second instance is the TRex system of polymorphic extensible records, where the qualification is a collection of lacks predicates.
  > Mark Jones showed that type classes were an example of a more general framework he called qualified types ... he developed a second instance of the qualified-type idea, a system of polymorphic, extensible records called TRex ...

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 209] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:first-order-unification-suffices`
  Higher kinds seem to require higher-order unification, but by treating higher-kinded constructors as uninterpreted functions and disallowing type-level lambda, ordinary first-order unification suffices; the solution is a bit ad hoc but has an excellent power-to-weight ratio.
  > by treating higher-kinded type constructors as uninterpreted functions and not allowing lambda at the type level, Jones's paper ... shows that ordinary first-order unification suffices.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 274] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:functional-dependencies`
  Jones's functional dependencies, borrowed from the database community, declare an explicit dependency between class parameters (a b -> r), so that fixing some parameters fixes others and resolves the ambiguity.
  > declare an explicit functional dependency between the parameters of a class ... The \"a b -> r\" says that fixing a and b should fix r, resolving the ambiguity.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 418] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:generalised-algebraic-data-types`
  GADTs generalise algebraic data types by letting a constructor's return type be specified directly, so pattern matching gives type as well as value information; well known in type theory, recent in programming languages, with many applications.
  > GADTs are a simple but farreaching generalisation of ordinary algebraic data types ... The idea is to allow a data constructor's return type to be specified directly:

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 461] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:generic-programming`
  A generic function behaves uniformly on any data type with a few type-specific cases; Haskell hosted a variety of generic-programming experiments, from pure Haskell 98 to higher-rank-type approaches, specific extensions, and whole new language designs.
  > A generic function behaves in a uniform way on arguments of any data types, while having a few typespecific cases.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 9] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:haskell-as-type-system-laboratory`
  An unforeseen development, perhaps encouraged by type classes, is that Haskell became a laboratory where many type-system extensions were designed, implemented, and applied.
  > An entirely unforeseen development—perhaps encouraged by type classes—is that Haskell has become a kind of laboratory in which numerous type-system extensions have been designed, implemented, and applied.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 213] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:higher-kinded-as-elegant-generalisation`
  In retrospect, higher-kinded quantification is a simple, elegant, useful generalisation of the Hindley-Milner typing discipline, solidified into the Haskell 1.3 Report.
  > In retrospect, higherkinded quantification is a simple, elegant, and useful generalisation of the conventional Hindley-Milner typing discipline ...

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 201] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:higher-kinds-independent-utility`
  Higher-kinded polymorphism has utility beyond monads: one can declare data types parameterised over higher kinds, and need functions quantified over higher-kinded variables to process nested data types.
  > higher-kinded polymorphism has independent utility: it is entirely possible, and occasionally very useful, to declare data types parameterised over higher kinds ...

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 409] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:higher-rank-types`
  Higher-rank types allow abstracting over a polymorphic function; they make inference undecidable without annotations, but a few explicit annotations make inference easy; first implemented in GHC in 2000, motivated by polymorphic data constructor fields and runST.
  > In the absence of any type annotations, higher-rank types make type inference undecidable; but a few explicit type annotations from the programmer ... transform the type inference problem into an easy one ...

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 373] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:implicit-parameters`
  Implicit parameters, a third instantiation of qualified types, make tiresome parameter passing happen implicitly like dictionary passing; one way to understand them is selective use of dynamic rather than lexical scoping.
  > Implicit parameters arrange that this parameter passing happens implicitly, rather like dictionary passing ...

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 301] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:informal-spec-did-not-stop-use`
  As usual with Haskell, functional dependencies being only informally described did not stop them from being implemented and widely used; they proved extremely tricky in detail, especially combined with other extensions, and formalisation is still in progress.
  > Jones's original paper gave only an informal description of functional dependencies, but (as usual with Haskell) that did not stop them from being implemented and widely used.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 219] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:kinds-classify-types`
  Kinds classify types as types classify values; the kind * is "type", and kind *->* denotes a type-level function from one type to another.
  > Kinds classify types just as types classify values. The kind * is pronounced ... \"type\", so if m has kind *->*, then m is a type-level function mapping one type to another.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 356] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:lacks-predicate-witnessed-at-runtime`
  Just as each type-class constraint corresponds to a runtime dictionary, each lacks predicate is witnessed by a runtime argument giving the field offset; the integration of record polymorphism with the general qualified-type framework is particularly elegant.
  > so each lacks predicate is also witnessed by a runtime argument. The witness for the predicate (r\\l) is the offset in r at which a field labelled l would be inserted.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 452] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:lexically-scoped-type-variables`
  Closed type signatures in Haskell 98 sometimes make it impossible to write a signature for an inner function; lexically scoped type variables are required so an outer binding's variable can be used in the inner signature.
  > some kind of lexically scoped type variables are required, so that \"a\" is bound by prefix and used in the signature for xcons.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 113] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:monomorphism-restriction`
  The monomorphism restriction, adopted after much debate, says a definition that does not look like a function should be monomorphic in overloaded type variables, forcing a shared binding to one type.
  > it says that a definition that does not look like a function ... should be monomorphic in any overloaded type variables.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 121] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:monomorphism-restriction-a-wart`
  The authors judge the monomorphism restriction a wart that bites every new programmer with obscure errors; a GHC flag suppresses it, but no satisfactory alternative has evolved.
  > The monomorphism restriction is manifestly a wart on the language. It seems to bite every new Haskell programmer ...

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 249] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:multi-parameter-ambiguity`
  The trouble with multi-parameter type classes is that it is very easy to write ambiguous types; even trivial programs can have ambiguous types because intended relations between parameters are only implied by the absence of instances.
  > The trouble with multi-parameter type classes is that it is very easy to write ambiguous types.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 230] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:multi-parameter-type-classes`
  Wadler and Blott observed type classes could be generalised to multiple parameters; a single-parameter class is a predicate over types, while a multi-parameter class is a relation between types.
  > a single-parameter type class can be viewed as a predicate over types ..., a multi-parameter class can be viewed a relation between types ...

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 80] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:numeric-classes-compromise`
  The collection of numeric type classes reflected an uneasy compromise between algebraic purity (which suggested more classes like Ring and Monoid) and pragmatism (which suggested fewer).
  > The rather daunting collection of type classes used to categorise the numeric operations reflected a slightly uneasy compromise between algebraic purity ... and pragmatism (which suggested fewer).

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 453] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:omission-of-scoped-type-variables-a-mistake`
  In retrospect the omission of lexically scoped type variables was a mistake, because polymorphic recursion and higher-rank types require type signatures; the omission came not from fierce debate but because the importance of signatures was never realised.
  > In retrospect, the omission of lexically scoped type variables was a mistake, because polymorphic recursion and (more recently) higher-rank types absolutely require type signatures.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 390] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:polymorphic-recursion`
  Polymorphic recursion lets a function be used polymorphically in its own definition; hard to infer but easy to check given the signature, so Haskell 98 allows it only when the programmer supplies the type signature.
  > So Haskell 98 allows polymorphic recursion when (and only when) the programmer explicitly specifies the type signature of the function.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 110] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:reluctance-on-compiler-dependent-performance`
  The committee was reluctant to let performance differences this large depend on compiler optimisations.
  > we were reluctant to make performance differences as big as this dependent on compiler optimisations.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 109] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:silent-duplication-of-computation`
  Hughes argued it was unacceptable to silently duplicate computation, since a binding inferred as overloaded becomes a function called once per occurrence, possibly at different types; his argument came from a program that ran exponentially slower than expected.
  > Hughes argued strongly that it was unacceptable to silently duplicate computation in this way. His argument was motivated by a program he had written that ran exponentially slower than he expected.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 474] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:template-meta-programming`
  Inspired by C++ template meta-programming and MetaML's staged type system, GHC supports a form of type-safe meta-programming.
  > Inspired by the template metaprogramming of C++ and the staged type system of MetaML ..., GHC supports a form of type-safe metaprogramming ...

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 41] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-class-basic-idea`
  The basic idea of a type class: a class declaration specifies the methods and their types, and a type is made an instance through an instance declaration providing an implementation at the instance type.
  > A class declaration specifies the methods of the class ... and their types. A type is made into an instance of the class using an instance declaration, which provides an implementation for each of the class's methods, at the appropriate instance type.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 3] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-classes-as-distinctive-feature`
  The authors hold that, aside from laziness, type classes are Haskell's most distinctive feature.
  > Aside from laziness, type classes are undoubtedly Haskell's most distinctive feature.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 77] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-classes-first-applications`
  Once adopted, type classes were immediately applied to main groups of operations: equality and ordering, string conversion, enumerations, numeric operations, and array indexing.
  > they were immediately applied to support the following main groups of operations: equality (Eq) and ordering (Ord); converting values to and from strings (Read and Show); enumerations (Enum); numeric operations ...; and array indexing (Ix).

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 7] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-classes-generalised-over-time`
  Over time type classes were generalised in varied and surprising ways, some summarised in a 1997 paper on the design space.
  > type classes began to be generalised in a variety of interesting and surprising ways, some of them summarised in a 1997 paper ...

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 4] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-classes-origin-small-problem`
  Type classes were proposed by Wadler and Blott early in the design as a principled solution to a small problem, operator overloading for numeric operations and equality.
  > They were originally proposed early in the design process, by Wadler and Blott ... as a ... principled solution to a relatively small problem (operator overloading for numeric operations and equality).

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 89] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-classes-serendipity`
  Type classes were serendipitous, invented at the right moment and rapidly pervasive (thirteen in the first release's standard library), and they opened far richer opportunities than their initial purpose.
  > Type classes were extremely serendipitous: they were invented at exactly the right moment to catch the imagination of the Haskell Committee ...

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 199] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-classes-supported-monads`
  Type classes directly supported monads, which made monads more accessible and popular; dually, the usefulness of monadic I/O ensured the adoption of higher-kinded polymorphism.
  > The fact that type classes so directly supported monads made monads far more accessible and popular; and dually, the usefulness of monadic I/O ensured the adoption of higher-kinded polymorphism.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 159] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-defaulting`
  Rejecting all ambiguous programs seemed too pedantic for numeric constants, so the committee added an ad hoc defaulting rule: when an ambiguous constraint is numeric and all constraints are Standard Prelude classes, a programmer-specified default type list is tried in order.
  > After much debate, we compromised by adding an ad hoc rule for choosing a particular default type.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 294] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-level-programming`
  The combination of multi-parameter classes and functional dependencies allowed arbitrary computation at the type level in logic-programming style, giving rise to a cottage industry of type-level programming, at the risk of non-termination in the type checker.
  > it turned out that one could write arbitrary computations at the type level, in logic-programming style.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 521] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:why-haskell-friendly-to-innovation-nontechnical`
  Nontechnical reasons: the committee encouraged innovation and disbanded itself in 1999; the two main implementations had teams that encouraged experimentation; and a smallish, geeky user base welcomed new features and even breaking changes.
  > The Haskell Committee encouraged innovation right from the beginning and, far from exercising control over the language, disbanded itself in 1999 ...

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 06_haskell-as-a-type-system-laboratory.md line 506] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:why-haskell-friendly-to-innovation-technical`
  Technical reasons Haskell hosted type-system innovation: the language's purity removed the obstacle of mutable state; qualified types gave a rich framework into which innovations fitted neatly; and polymorphic recursion had already abandoned the tenet that every legal program typecheck without annotations.
  > The purity of the language removed a significant technical obstacle to many type-system innovations, namely dealing with mutable state.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 525] `written:2007-06-09_07-monads-and-input-output:arrows-generalise-monads`
  The text reports that arrows, proposed by Hughes, are an abstract view of computation with the same flavour as monads but more general, with applications in GUIs, reactive and polytypic programming; like monads, arrow programming is much easier with syntactic support, handled directly by the type checker.
  > Arrows are an abstract view of computation with the same flavour as monads, but in a more general setting.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 534] `written:2007-06-09_07-monads-and-input-output:being-explicit-about-effects`
  Underlying all these developments is the realisation that being explicit about effects is extremely useful, which the authors believe may be one of Haskell's main impacts on mainstream programming; transactional memory is an example, since the crude IO effect system means most memory operations need not be logged, and transposing STM into Haskell revealed two new composition operators (retry and orElse).
  > Underlying all these developments is the realisation that being explicit about effects is extremely useful, and this is something that we believe may ultimately be seen as one of Haskell’s main impacts on mainstream programming

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 481] `written:2007-06-09_07-monads-and-input-output:concurrent-haskell-mvars`
  Concurrent Haskell extends the IO monad with lightweight threads, each able to do I/O, making the semantics nondeterministic by design; threads communicate through synchronised mutable locations called MVars, inspired by the M-structures of Id.
  > Concurrent Haskell ... extends the IO monad with the ability to fork lightweight threads, each of which can perform I/O by itself

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 76] `written:2007-06-09_07-monads-and-input-output:continuation-io-transactions`
  In the continuation model the program is still of type Behaviour, but each request/response pair is captured by a transaction, a function taking failure and success continuations.
  > a collection of transactions were defined that cap- tured the effect of each request/response pair in a continuationpassing style. Transactions were just functions.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 118] `written:2007-06-09_07-monads-and-input-output:continuations-preferred-localised-control`
  Though the two styles looked similar, most programmers preferred continuations because control flow was more localised, whereas stream pattern matching forced the reader's focus to jump between responses and requests.
  > the continuation style was preferred by most programmers, since the flow of control was more localised.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 371] `written:2007-06-09_07-monads-and-input-output:do-notation-looks-imperative`
  Rewriting the example in do-notation makes the monadic parts of Haskell programs appear much more imperative.
  > This notation makes (the monadic parts of) Haskell programs appear much more imperative!

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 446] `written:2007-06-09_07-monads-and-input-output:do-notation-not-monads-blurred-the-line`
  It was do-notation, rather than monads themselves, that made Haskell programs look like conventional imperative programs and seriously blurred the line between pure and imperative code, yet the committee heartily adopted it.
  > it was really the advent of do-notation—not monads themselves—that made Haskell programs look more like conventional imperative programs

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 498] `written:2007-06-09_07-monads-and-input-output:exceptions-recovered-via-io`
  Exceptions were in the IO monad from the start, but pure code originally had only error, which halts the whole program; the IO monad lets programs catch and recover from error and pattern-match failures without giving up the deterministic semantics of pure code.
  > The IO monad provides a way to achieve this goal without giving up the simple, deterministic semantics of purely functional code

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 399] `written:2007-06-09_07-monads-and-input-output:imperative-functional-programming`
  The text reports that Peyton Jones and Wadler named the world-passing-with-token implementation of IO "imperative functional programming".
  > Peyton Jones and Wadler dubbed the result “imperative functional programming”

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 362] `written:2007-06-09_07-monads-and-input-output:io-monad-exceptions`
  The IO monad supports exceptions through ioError, which fails throwing an exception, and catch, which runs a computation and passes any exception to a handler.
  > The Haskell IO monad also supports exceptions, offering two new primitives:

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 382] `written:2007-06-09_07-monads-and-input-output:io-two-implementations`
  Haskell's I/O is specified monadically and can be implemented with continuations (FailCont -> SuccCont a -> Behaviour) or, in GHC, with a world-passing type World -> (a, World), where a dummy token ensures sequencing under lazy evaluation and real side effects are performed.
  > it is also possible to implement the IO monad in a completely different style, without any recourse to a stream of requests and responses.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 425] `written:2007-06-09_07-monads-and-input-output:lambda-precedence-change`
  To avoid the piling up of parentheses when lambdas nest in the continuation style, the committee changed, late in the design, the precedence rules for lambda in the context of infix operators, letting continuation code look strikingly like the monadic code.
  > the Haskell Committee decided quite late in the design process to change the precedence rules for lambda in the context of infix operators

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 42] `written:2007-06-09_07-monads-and-input-output:lazy-evaluation-enables-streams`
  Lazy evaluation lets a program generate a request before processing any responses, which makes the stream model work.
  > Lazy evaluation allows a program to generate a request prior to processing any responses.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 136] `written:2007-06-09_07-monads-and-input-output:moggi-monads-for-semantics`
  The text reports that Moggi published the use of monads from category theory to modularise denotational semantics, systematising features such as state and exceptions.
  > Moggi used monads to modularise the structure of a denotational semantics, systematising the treatment of diverse features such as state and exceptions.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 413] `written:2007-06-09_07-monads-and-input-output:monad-abstraction-conceptual-advantage`
  The big advantage of monadic I/O is conceptual: thinking abstractly in terms of computations is easier than thinking in terms of failure and success continuations, and the abstraction makes the underlying details easy to change later.
  > the big advantage is conceptual. It is much easier to think abstractly in terms of computations than concretely in terms of the details of failure and success continuations.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 295] `written:2007-06-09_07-monads-and-input-output:monad-as-type-class`
  A monad is a programming pattern, and that pattern can be expressed directly in Haskell as a type class, giving concrete expression to the mathematical idea that any suitably typed type constructor is a monad, with direct practical use for writing combinators that work for any monad.
  > A monad is a kind of “programming pattern”. It turned out that this pattern can be directly expressed in Haskell, using a type class

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 159] `written:2007-06-09_07-monads-and-input-output:monad-definition`
  A monad is a type constructor M together with return and >>= (bind); M a is read as a computation returning a value of type a and perhaps performing side effects, and bind sequences such computations.
  > A monad consists of a type constructor M and a pair of functions, return and >>= (sometimes pronounced “bind”).

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 279] `written:2007-06-09_07-monads-and-input-output:monad-laws-unenforced`
  A true monad's return and >>= must satisfy three laws guaranteeing associative composition with an identity, but Haskell provides no mechanism to ensure them, and some programmers use monadic patterns where the laws do not hold.
  > There are three laws that these definitions should satisfy in order to be a true monad ... These laws guarantee that composition of functions with side effects is associative and has an identity

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 331] `written:2007-06-09_07-monads-and-input-output:monad-transformers-dont-compose`
  Monads are often combined, and abstracting further yields monad transformers; the first modular interpreter in Haskell used them but needed type class extensions only in Gofer, which motivated extensions to type classes. Despite their utility, monads do not compose modularly, an open research problem.
  > Despite the utility of monad transformers, monads do not compose in a nice, modular way, a research problem that is still open

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 346] `written:2007-06-09_07-monads-and-input-output:monadic-io-key-idea`
  The key idea of monadic I/O is to treat a value of type IO a as a computation that, when performed, may do input and output before delivering a value of type a.
  > The key idea is to treat a value of type IO a as a “computation” that, when performed, might perform input and output before delivering a value of type a.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 402] `written:2007-06-09_07-monads-and-input-output:monadic-types-compact-and-polymorphic`
  The monadic approach dominated earlier models because the types are more compact and informative, uncluttered by passed continuations, showing the result type, and allowing polymorphic IO types that a fixed Request/Response type could not express.
  > The monadic approach rapidly dominated earlier models. The types are more compact, and more informative.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 3] `written:2007-06-09_07-monads-and-input-output:monads-distinctive-but-not-original`
  Monads are among the most distinctive design features of Haskell, yet were absent from the original design because the concept's relevance to programming was unrecognised at the time.
  > monads are one of the most distinctive language design features in Haskell. Monads were not in the original Haskell design, because when Haskell was born a “monad” was an obscure feature of category theory whose implications for programming were largely unrecognised.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 315] `written:2007-06-09_07-monads-and-input-output:monads-typeclasses-symbiosis`
  Intellectual reuse of the monad idea becomes actual code reuse through libraries of monadic functions; the conjunction of monads and type classes made each more attractive.
  > This happy conjunction of monads and type classes gave the two a symbiotic relationship: each made the other much more attractive.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 176] `written:2007-06-09_07-monads-and-input-output:monads-vs-ml-sequencing`
  Bind is analogous to let in a side-effecting language like ML, but the types record the effect (M a rather than a), and monads give freedom in defining return and >>=, whereas ML fixes one built-in notion of computation and sequencing.
  > monads give quite a bit of freedom in how one defines the operators return and >>=, while ML fixes a single built-in notion of computation and sequencing.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 457] `written:2007-06-09_07-monads-and-input-output:mutable-state-in-io`
  From the beginning it was clear the IO monad could support mutable locations and arrays via newIORef, readIORef and writeIORef.
  > From the very beginning it was clear that the IO monad could also support mutable locations and arrays

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 67] `written:2007-06-09_07-monads-and-input-output:no-special-io-syntax`
  With stream I/O no special-purpose syntax or constructs were needed; the system was defined entirely by how the OS interpreted a program of the given type, specified abstractly as an OS function with a nondeterministic merge over parallel programs.
  > With this treatment of I/O there was no need for any specialpurpose I/O syntax or I/O constructs.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 11] `written:2007-06-09_07-monads-and-input-output:purity-drove-io-design`
  The committee's firm commitment to a pure language, meaning no side effects, made the design of the I/O system a central problem; they feared a weak solution would make Haskell look like a toy.
  > The Haskell Committee was resolute in its decision to keep the language pure—meaning no side effects— so the design of the I/O system was an important issue.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 479] `written:2007-06-09_07-monads-and-input-output:random-numbers-use-io`
  The Haskell 98 Random library uses the IO monad as a source of seeds, since random numbers need a seed.
  > Random numbers need a seed, and the Haskell 98 Random library uses the IO monad as a source of such seeds.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 450] `written:2007-06-09_07-monads-and-input-output:retrospective-syntax-for-streams`
  In retrospect the authors ask whether the same or a similar syntactic device could have been used to make stream or continuation I/O look more natural.
  > In retrospect it is worth asking whether this same (or similar) syntactic device could have been used to make stream or continuation-based I/O look more natural.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 463] `written:2007-06-09_07-monads-and-input-output:runST-encapsulates-imperative`
  An unexpected development was that imperative computations could be securely encapsulated inside a pure function: a state monad parameterised by a type s that infects its references, encapsulated by runST with a rank-2 type, with parametricity ensuring no references leak between encapsulated computations.
  > An exciting and entirely unexpected development was Launchbury and Peyton Jones’s discovery that imperative computations could be securely encapsulated inside a pure function.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 155] `written:2007-06-09_07-monads-and-input-output:state-monad-hides-plumbing`
  Lacking reference cells, Haskell must thread a counter by hand to generate fresh names, which is tedious and error-prone; a state transformer monad hides the plumbing so the names cannot be misspelled.
  > Using a state transformer monad would let you hide all the “plumbing.” The monad itself would be responsible for passing counter values, so there is no chance to misspell the associated names.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 487] `written:2007-06-09_07-monads-and-input-output:stm-fits-haskell`
  MVars make programs non-composable; software transactional memory is a promising approach to this composition problem that fits particularly well into Haskell.
  > Software transactional memory is a recent and apparently very promising new approach to this problem, and one that fits particularly beautifully into Haskell

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 39] `written:2007-06-09_07-monads-and-input-output:stream-io-as-behaviour`
  In the stream model a program is a value of type Behaviour mapping responses to requests; the program issues a Request to the OS and the OS reacts with a Response.
  > type Behaviour = [Response] -> [Request]

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 21] `written:2007-06-09_07-monads-and-input-output:streams-and-continuations-equivalent`
  The two leading pure solutions, streams and continuations, turned out to be functionally equivalent, so Haskell 1.0 defined I/O by streams and included an equivalent continuation design.
  > we realised that in fact they were functionally equivalent—that is, it was possible to completely model stream I/O with continuations, and vice versa.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 126] `written:2007-06-09_07-monads-and-input-output:streams-primitive-for-efficiency`
  Streams can be defined from continuations too, but that definition was inefficient (linear space, quadratic time), so Haskell 1.0 took streams as primitive and defined continuations from them, even though continuations were easier to use.
  > the definition of streams in terms of continuations was inefficient, requiring linear space and quadratic time ... For this reason, Haskell 1.0 defined streams as primitive, and continuations in terms of them, even though continuations were considered easier to use for most purposes.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 337] `written:2007-06-09_07-monads-and-input-output:syntactic-sugar-for-monads`
  Two syntactic sugars appeared at different times: Haskell 1.3's do-notation (from Launchbury's work) and Haskell 1.4's monad comprehensions; comprehensions were proposed first, yet users preferred do-notation and generalising comprehensions confused novices, so comprehensions were removed in Haskell 98.
  > Most users preferred the do-notation, and generalising comprehensions to monads meant that errors in ordinary list comprehensions could be difficult for novices to understand, so monad comprehensions were removed in Haskell 98.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 503] `written:2007-06-09_07-monads-and-input-output:unsafePerformIO-no-safe-escape`
  Unlike runST there is no safe way to escape the IO monad, yet all implementations provide unsafePerformIO; its use is a programmer's promise that the I/O's repetition and ordering do not matter, and it can even subvert the type system, so it arguably deserves a longer name.
  > unlike runST, which safely encapsulates an imperative computation, there is no safe way to escape from the IO monad.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 179] `written:2007-06-09_07-monads-and-input-output:varieties-of-monads`
  Many notions of side effect are definable as monads: state transformer, state reader, exception, continuation, list (for nondeterminism), and parser (a combination of state transformer and list).
  > Here are a few examples of the notions of side effects that one can define with monads:

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 140] `written:2007-06-09_07-monads-and-input-output:wadler-monads-for-programs`
  The text reports that Wadler recognised Moggi's semantic technique could structure ordinary functional programs, using monads to express the very features Moggi used them to describe.
  > Wadler recognised that the technique Moggi had used to structure semantics could be fruitfully applied to structure other functional programs

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 07_monads-and-input-output.md line 29] `written:2007-06-09_07-monads-and-input-output:world-passing-rejected`
  A third model passing and updating world state like any data structure was considered but rejected, because they saw no easy way to ensure single-threaded access to the world state; the Clean designers later solved this with uniqueness types.
  > This “world-passing” model was never a serious contender for Haskell, however, because we saw no easy way to ensure “single-threaded” access to the world state.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 08_haskell-in-middle-age.md line 4] `written:2007-06-09_08-haskell-in-middle-age:areas-neglected-by-original-designers`
  As Haskell found real use, attention turned to practically important areas the original designers had neglected; these are recent, still in flux, and seen with less historical perspective.
  > more and more attention has been paid to areas that received short shrift from the original designers of the language. These areas are of enormous practical importance, but they have evolved more recently and are still in flux, so we have less historical perspective on them.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 08_haskell-in-middle-age.md line 24] `written:2007-06-09_08-haskell-in-middle-age:blessed-addenda`
  The FFI effort was valuable enough to spawn "Blessed Addenda," well-specified appendices to the Haskell 98 Report giving precise advice on implementing language extensions.
  > the idea of “Blessed Addenda” emerged, a well-specified Appendix to the Haskell 98 Report that contained precise advice regarding the implementation of a variety of language extensions.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 08_haskell-in-middle-age.md line 13] `written:2007-06-09_08-haskell-in-middle-age:early-ad-hoc-ffi-mechanisms`
  Once the IO monad existed, implementation-specific mechanisms for foreign calls appeared quickly, such as GHC allowing literal C in monadic procedures and Hugs exposing C functions as Haskell primitives; their trouble was being tied to one implementation.
  > Once the IO monad was established, a variety of ad hoc mechanisms rapidly appeared... The difficulty was that these mechanisms tended to be implementation-specific.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 08_haskell-in-middle-age.md line 22] `written:2007-06-09_08-haskell-in-middle-age:ffi-c-as-lowest-common-denominator`
  An implementation-independent Foreign Function Interface was specified treating C as a lowest common denominator, since being able to call C lets you call almost anything else.
  > This so-called Foreign Function Interface (FFI) treats C as a lowest common denominator: once you can call C you can call practically anything else.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 08_haskell-in-middle-age.md line 34] `written:2007-06-09_08-haskell-in-middle-age:ffi-process-different-in-kind`
  The authors note the FFI process differed in kind from the original language development: open to all, but critically dependent on one person's willingness to drive it and act as Editor, which is why they describe it in passive verbs.
  > it was different in kind to the original development of the Haskell language. The exercise was open to all, but depended critically on the willingness of one person... to drive the process and act as Editor for the specification.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 08_haskell-in-middle-age.md line 61] `written:2007-06-09_08-haskell-in-middle-age:flat-namespace-irksome`
  As use grew, the completely flat module name space became increasingly irksome, e.g. two collection libraries could not both use the module name Map.
  > the fact that the module name space was completely flat became increasingly irksome; for example, if there are two collection libraries, they cannot both use the module name Map.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 08_haskell-in-middle-age.md line 65] `written:2007-06-09_08-haskell-in-middle-age:hierarchical-module-names`
  An effort led by Malcolm Wallace specified hierarchical multi-component module names (e.g. Data.Map), borrowing largely from Java; this second Blessed Addendum stayed at version 0.0 "Candidate" status yet was swiftly implemented and has survived unchanged.
  > an extension to Haskell that would allow multi-component hierarchical module names (e.g., Data.Map), using a design largely borrowed from Java.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 08_haskell-in-middle-age.md line 56] `written:2007-06-09_08-haskell-in-middle-age:interfaces-abandoned`
  Early versions required each module to have an interface as well as an implementation, with much discussion of their syntax, semantics, and tensions; Haskell 1.4 abandoned interfaces as a formal part of the language, treating interface files as an artifact of separate compilation.
  > In the end, Haskell 1.4 completely abandoned interfaces as a formal part of the language; instead interface files were regarded as a possible artifact of separate compilation.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 08_haskell-in-middle-age.md line 45] `written:2007-06-09_08-haskell-in-middle-age:module-system-as-namespace-control`
  They converged on a very simple design: the module system is only a namespace control mechanism, with the merit of simplicity and clarity, e.g. being specified separately from the type system.
  > the module system is a namespace control mechanism, nothing more and nothing less. This had the great merit of simplicity and clarity—for example, the module system is specified completely separately from the type system

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 08_haskell-in-middle-age.md line 38] `written:2007-06-09_08-haskell-in-middle-age:module-system-emerged-without-debate`
  Haskell's module system emerged with surprisingly little debate; an anticipated argument over adopting ML's sophisticated module system never really happened.
  > Haskell’s module system emerged with surprisingly little debate.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 08_haskell-in-middle-age.md line 11] `written:2007-06-09_08-haskell-in-middle-age:need-to-call-other-languages`
  A very common application need is to call procedures written in another language from Haskell, and preferably the reverse.
  > One feature that very many applications need is the ability to call procedures written in some other language from Haskell, and preferably vice versa.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 08_haskell-in-middle-age.md line 29] `written:2007-06-09_08-haskell-in-middle-age:preprocessing-tools-for-bindings`
  Alongside the standardisation, pre-processing tools emerged to ease writing the many foreign import declarations a large binding requires (Green Card, H/Direct, C2Hs).
  > a number of pre-processing tools designed to ease the labour of writing all the foreign import declarations required for a large binding

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 08_haskell-in-middle-age.md line 57] `written:2007-06-09_08-haskell-in-middle-age:regret-no-checked-interface-language`
  As a consequence, Haskell sadly lacks a formally checked language in which a programmer can advertise the interface a module supports; the authors mark this as a regret.
  > As a result, Haskell sadly lacks a formally checked language in which a programmer can advertise the interface that the module supports.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 08_haskell-in-middle-age.md line 52] `written:2007-06-09_08-haskell-in-middle-age:tensions-in-interfaces`
  The interface discussion surfaced issues such as duplication between interfaces and implementations, whether one can deduce from an interface which module ultimately defines an entity, and a tension between what a compiler wants in an interface and what a programmer wants to write.
  > issues such as the duplication of information between interfaces and implementations... whether one can deduce from an interface which module ultimately defines an entity; a tension between what a compiler might want in an interface and what a programmer might want to write

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 08_haskell-in-middle-age.md line 42] `written:2007-06-09_08-haskell-in-middle-age:why-no-ml-module-debate`
  Possible reasons the ML-module debate never occurred: perhaps no committee member knew ML's module system well enough to advocate it, or there was tacit agreement that combining type classes with ML modules was a bridge too far.
  > Perhaps no member of the committee was sufficiently familiar with ML’s module system to advocate it, or perhaps there was a tacit agreement that the combination of type classes and ML modules was a bridge too far.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 11] `written:2007-06-09_09-implementations:cabal-and-hackage-for-packaging`
  Cabal, led by Isaac Jones from 2004, specifies and implements a system for constructing and distributing Haskell packages; Hackage, implemented by David Himmelstrup, is a Cabal package server for finding and downloading packages.
  > Isaac Jones took up the challenge of leading an effort to specify and implement a system called Cabal that supports the construction and distribution of Haskell packages

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 336] `written:2007-06-09_09-implementations:common-lisp-backend-limits`
  The Common Lisp back end ultimately limited Yale Haskell: performance in strict code was comparable but lazy code ran 3 to 5 times slower, because Lisp's imperative nature prevented Haskell-specific optimisations (reusing thunk storage, avoiding the extra indirection of a Lisp cons cell per thunk); with no hope of speedup without replacing the back end and no funding, it was abandoned circa 1995.
  > there was a factor of 3 to 5 in lazy code that could not be overcome due to the limitations of the Lisp back end.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 104] `written:2007-06-09_09-implementations:core-based-on-system-f`
  Core was initially based on the lambda calculus; in 1992 they realised Girard's System F ω was a ready-made basis for decorating it with types, needing only to add data types, let- and case-expressions. GHC appears to be the first compiler to use System F as a typed intermediate language.
  > we realised in 1992 that a ready-made basis lay to hand, namely Girard’s System F ω ...; all we needed to do was to add data types, let-expressions, and case expressions. GHC appears to be the first compiler to use System F as a typed intermediate language

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 90] `written:2007-06-09_09-implementations:core-intermediate-language`
  After type checking the program is desugared into a small explicitly typed intermediate language called Core, then processed by a long sequence of Core-to-Core analyses and optimising transformations before STG and C/machine code.
  > the program is desugared into an explicitly typed intermediate language called simply “Core” and then processed by a long sequence of Core-to-Core analyses and optimising transformations.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 130] `written:2007-06-09_09-implementations:core-lint-consistency-check`
  A "Core Lint" typechecker checks each pass's output stays well-typed; this provides a surprisingly strong consistency check since most optimiser bugs produce type-incorrect code, catching bugs far more cheaply than running incorrect code. It turned out to be one of the biggest benefits of a typed intermediate language, though recognising this took a long time.
  > This consistency checking turned out to be one of the biggest benefits of a typed intermediate language, although it took us a remarkably long time to recognise this fact.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 39] `written:2007-06-09_09-implementations:cross-implementation-common-libraries`
  Driven by user desire for cross-implementation compatibility, the Hugs, GHC and nhc teams began in 2001 to work on a common open-source set of libraries shipped with each compiler.
  > driven by user desire for cross-implementation compatibility, the Hugs, GHC and nhc teams began in 2001 to work together on a common, open-source set of libraries that could be shipped with each of their compilers

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 17] `written:2007-06-09_09-implementations:distribution-took-fifteen-years`
  It took more than fifteen years for Haskell to gain enough momentum for distribution and discovery mechanisms to become important.
  > it has taken more than fifteen years for Haskell to gain enough momentum that these distribution and discovery mechanisms have become important.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 350] `written:2007-06-09_09-implementations:environments-long-neglected`
  Until recently, with the exception of Yale Haskell, Haskell implementers paid little attention to the programming environment, though that is beginning to change (Haskell Refactorer, Visual Haskell, EclipseFP).
  > Until recently, with the notable exception of Yale Haskell, little attention has been paid by Haskell implementers to the programming environment.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 70] `written:2007-06-09_09-implementations:ghc-complete-implementation-in-haskell`
  GHC proper, begun autumn 1989, was designed from the ground up as a complete implementation of Haskell in Haskell, bootstrapped via the prototype; only the parser (Yacc and C) was shared.
  > It was designed from the ground up as a complete implementation of Haskell in Haskell, bootstrapped via the prototype compiler.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 76] `written:2007-06-09_09-implementations:ghc-early-extensions`
  GHC's first full release already supported extensions beyond Haskell: monadic I/O (official only in 1996), mutable arrays, unboxed data types, and a novel space/time profiling system.
  > This version of GHC already supported several extensions to Haskell: monadic I/O ..., mutable arrays, unboxed data types ..., and a novel system for space and time profiling

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 136] `written:2007-06-09_09-implementations:ghc-grew-complex`
  Over fifteen years GHC grew a huge number of features (dozens of extensions, GHCi, concurrency, transactional memory, Template Haskell, packages), making it a dauntingly complex beast to understand and modify.
  > This makes GHC a dauntingly complex beast to understand and modify

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 56] `written:2007-06-09_09-implementations:ghc-origins-as-lml-front-end`
  GHC began in January 1989 at Glasgow as soon as the language design was fixed; the first version, written in LML by Kevin Hammond, was essentially a new front end to the Chalmers LML compiler.
  > The first version of GHC was written in LML by Kevin Hammond, and was essentially a new front end to the Chalmers LML compiler.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 184] `written:2007-06-09_09-implementations:gofer-dictionary-passing-variant`
  Gofer adopted a variant of Wadler and Blott's dictionary-passing translation designed to minimise dictionary construction at run time, work with multi-parameter type classes, and give more accurate principal types; this caused small but significant differences between the Haskell and Gofer type systems, so some programs would not port either way.
  > an interesting variant of Wadler and Blott’s dictionary-passing translation ... designed to minimise the construction of dictionaries at run time, to work with multiple parameter type classes, and to provide more accurate principal types.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 191] `written:2007-06-09_09-implementations:gofer-do-notation-and-constructor-classes`
  Jones added constructor classes and produced the first implementation of the do-notation in Gofer; both features were subsequently adopted in Haskell 98. He also built a Gofer-to-C compiler and the first "dictionary-free" implementation of type classes using partial evaluation.
  > adding support for constructor classes ... in 1992–93 and producing the first implementation of the do-notation in 1994. Both of these features were subsequently adopted in Haskell 98.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 181] `written:2007-06-09_09-implementations:gofer-first-multi-parameter-type-classes`
  Gofer included the first implementation of multi-parameter type classes, as originally suggested by Wadler and Blott and a regular topic on the Haskell mailing list.
  > Gofer included the first implementation of multi-parameter type classes, as originally suggested by Wadler and Blott

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 174] `written:2007-06-09_09-implementations:gofer-interpreter-small-footprint`
  In contrast to the memory-hungry compilers, Mark Jones released Gofer in 1991, an interpreter in C developed on an 8086 PC with 640KB, small enough to fit on a single 360KB floppy, written to learn about implementing functional languages.
  > Gofer was an interpreter, implemented in C, developed on an 8MHz 8086 PC with 640KB of memory, and small enough to fit on a single (360KB) floppy disk.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 213] `written:2007-06-09_09-implementations:gofer-to-hugs`
  Jones rewrote the Gofer code base to track the Haskell standard, briefly called "Hg" then "Hugs"; the first release (February 1995) supported almost all Haskell 1.2 features, its most prominent missing feature being the module system, which Hugs 1.0 parsed but ignored.
  > The most prominent missing feature was the Haskell module system; Hugs 1.0 would parse but otherwise ignore module headers and import declarations.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 33] `written:2007-06-09_09-implementations:haskell-98-libraries-still-modest`
  The Haskell 98 libraries were still fairly modest, 100 of 240 report pages, but real applications need much richer libraries, which drove an informal library evolution mechanism.
  > The libraries defined as part of Haskell 98 were still fairly modest in scope. ... But real applications need much richer libraries, and an informal library evolution mechanism began

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 48] `written:2007-06-09_09-implementations:haskell-is-a-big-language-to-implement`
  Haskell is a big language and quite a lot of work to implement, yet several implementations exist.
  > Haskell is a big language, and it is quite a lot of work to implement. Nevertheless, several implementations are available

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 168] `written:2007-06-09_09-implementations:hbc-doomed-by-lml`
  Augustsson reports hbc became a test bed for extensions and lived actively for over five years, but being written in LML it was more or less doomed to dwindle.
  > since the compiler was written in LML it was more or less doomed to dwindle.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 163] `written:2007-06-09_09-implementations:hbc-type-checking-hard`
  Augustsson reports that in hbc the two problematic areas were modules (renaming import/export with many validity conditions) and especially type checking, which was hard because it predated good papers on how it should be done.
  > the big stumbling block was the type checking. It was hard to do. This was way before there were any good papers about how it was supposed to be done.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 149] `written:2007-06-09_09-implementations:hbc-written-out-of-impatience`
  Augustsson reports he and Truvé decided to write their own Haskell compiler based on LML rather than wait longer for the Glasgow compiler; he had a mostly complete implementation of Haskell by late August 1990.
  > we would write our own Haskell compiler based on the LML compiler.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 341] `written:2007-06-09_09-implementations:helium-for-teaching-and-error-messages`
  The Helium compiler at Utrecht focuses especially on teaching and on giving high-quality type error messages.
  > The Helium compiler, based at Utrecht, is focused especially on teaching, and on giving high-quality type error messages

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 232] `written:2007-06-09_09-implementations:hugs-experimental-type-features`
  Jones overhauled the Hugs type checker with experimental support for advanced type system features (rank-2 polymorphism, polymorphic recursion, scoped type variables, existentials, extensible records) and restored multi-parameter type classes; these were too experimental for Hugs 1.4 and released separately as Hugs 1.3c.
  > experimental support for advanced type system features including rank-2 polymorphism, polymorphic recursion, scoped type variables, existentials, and extensible records

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 344] `written:2007-06-09_09-implementations:jhc-whole-program-no-dictionaries`
  jhc, by John Meacham, focuses on aggressive optimisation via whole-program analysis; this whole-program approach allows a completely different way of implementing type classes without dictionary-passing, using flow analysis to support a defunctionalised representation of thunks.
  > This whole-program approach allows a completely different approach to implementing type classes, without using dictionary-passing.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 80] `written:2007-06-09_09-implementations:large-front-end-data-type-for-good-errors`
  GHC uses a very large front-end data type reflecting Haskell's full syntax, performing error-generating processing on it, in contrast to the popular method of removing syntactic sugar first; this cost much broad code but let error messages report exactly what the programmer wrote.
  > GHC uses a very large data type in its front end that accurately reflects the full glory of Haskell’s syntax. ... but has the huge advantage that the error messages could report exactly what the programmer wrote.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 30] `written:2007-06-09_09-implementations:libraries-grew-into-a-separate-report`
  The importance of well-specified and well-implemented libraries became apparent early; the Standard Prelude began as an appendix, but by Haskell 1.3 the volume of library code warranted a separate companion Library Report.
  > the volume of standard library code had grown to the extent that it was given a separate companion Library Report, alongside the language definition.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 22] `written:2007-06-09_09-implementations:module-system-of-modesty`
  Haskell's module system is distinguished by its modesty, doing about as little as a language can and still be a practical tool; perhaps a good choice, since it avoids the technically complicated area that ML modules occupy.
  > a module system distinguished by its modesty. It does about as little as it is possible for a language to do and still call itself a practical programming tool. Perhaps this was a good choice; it certainly avoids a technically complicated area

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 5] `written:2007-06-09_09-implementations:modules-are-not-a-unit-of-distribution`
  Modules work as a unit of program construction but not of distribution; developers want to ship a related group of modules as a package with its documentation, licensing, dependencies and build information, and none of this was in the language design.
  > Modules form a reasonable unit of program construction, but not of distribution. Developers want to distribute a related group of modules as a “package,” ... None of this was part of the Haskell language design.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 267] `written:2007-06-09_09-implementations:nhc-heap-profiling-link`
  nhc's development used first-generation heap-profiling tools from York (developed to reveal space-leaks in hbc); this link brought Röjemo to York, where more advanced heap-profiling methods found residual space-inefficiencies and led to a still more space-efficient nhc.
  > he made use during development of the first-generation heap-profiling tools—which had previously been developed at York and used to reveal space-leaks in hbc

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 261] `written:2007-06-09_09-implementations:nhc-space-efficiency-goal`
  Röjemo's motivation for nhc from the start was a space-efficient compiler that could be bootstrapped in much smaller memory than hbc and GHC, specifically on his ~2Mbyte machine.
  > His motivation from the start was to have a space-efficient compiler ... that could be bootstrapped in a much smaller memory space than required by systems such as hbc and GHC.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 241] `written:2007-06-09_09-implementations:parallel-hugs-development-and-merge`
  Reid at Yale added module-system support while Jones independently developed Hugs 1.3 with Haskell 1.3 features; the parallel versions were confusing for users and developers, finally merged in Hugs 98 (March 1999), the first version to support Haskell 98.
  > This problem was finally addressed with the release of Hugs 98 in March 1999, which merged the features of the previous Yale and Nottingham releases into a single system.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 59] `written:2007-06-09_09-implementations:prototype-implemented-all-of-haskell-1-0`
  The prototype implemented essentially all of Haskell 1.0 including views (later removed), type classes, the deriving mechanism, the full module system, binary I/O, and both streams and continuations.
  > The prototype compiler implemented essentially all of Haskell 1.0 including views (later removed), type classes, the deriving mechanism, the full module system, and binary I/O as well as both streams and continuations.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 249] `written:2007-06-09_09-implementations:standardisation-stabilised-hugs`
  Hugs development slowed after Hugs 98, benefiting from the stability provided by the standardisation of Haskell 98, while still adding features such as implicit parameters, functional dependencies, .NET support, and hierarchical module names.
  > benefiting in part from the stability provided by the standardisation of Haskell 98.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 62] `written:2007-06-09_09-implementations:type-classes-cost-size-and-speed`
  Type classes added complexity that made the compiler bigger and slower than the base LML compiler, and the larger Haskell prelude stressed the LML prelude mechanism; experience with this compiler partly led the Committee to introduce the monomorphism restriction, remove views, and make other changes.
  > the added complexity of type classes meant the compiler was quite a lot bigger and slower than the base LML compiler.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 108] `written:2007-06-09_09-implementations:underestimating-typed-intermediate-language`
  They thought the System F idea too simple to publish and only noted it in a small section; the same idea was used independently in the TIL compiler, whose authors understood its significance better, and type-directed compilation became very influential.
  > at the time we thought it was such a simple idea that we did not think it worth publishing ... They understood its significance much better than the GHC team, and the whole approach of type-directed compilation subsequently became extremely influential.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 322] `written:2007-06-09_09-implementations:yale-haskell-as-extension-testbed`
  Yale Haskell supported many language extensions (monads, dynamic types, polymorphic recursion, strictness annotations, inlining pragmas, specialising overloaded functions, mutually recursive modules, a flexible foreign function interface), serving as a test bed for new ideas.
  > thus served as an excellent test bed for new ideas. These extensions included monads, dynamic types, polymorphic recursion, strictness annotations, inlining pragmas

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 312] `written:2007-06-09_09-implementations:yale-haskell-programming-environment`
  The underlying Lisp system let the Yale effort focus on the programming environment; Yale Haskell was the first implementation to support both compiled and interpreted code in the same program, with an emacs-based environment of two-keystroke commands and queued commands.
  > Yale Haskell was the first implementation to support both compiled and interpreted code in the same program

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 319] `written:2007-06-09_09-implementations:yale-haskell-scratch-pad`
  Yale Haskell offered a "scratch pad", a logical extension of a module where additional function and value definitions could be added without recompiling the module.
  > A scratch pad was a logical extension of a module in which additional function and value definitions could be added, but whose evaluation did not result in recompilation of the module.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 300] `written:2007-06-09_09-implementations:yale-haskell-strictness-for-performance`
  Yale Haskell used strictness analysis and type information to compile the strict part of Haskell into very efficient Lisp code, with a dual-entry-point approach for efficient first-order calls and aggressive in-lining, plus optimisations to reduce lazy-evaluation overhead.
  > Yale Haskell used strictness analysis and type information to compile the strict part of Haskell into very efficient Lisp code.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 09_implementations.md line 291] `written:2007-06-09_09-implementations:yale-haskell-via-scheme-techniques`
  Building on prior Yale work on Scheme and the T dialect (and the Orbit compiler), Hudak applied Scheme compilation techniques to Haskell by compiling Haskell into Scheme or T and using a Scheme compiler as a back end, rather than a stand-alone compiler; T was abandoned for Common Lisp over performance and portability, yielding Yale Haskell.
  > rather than port the ideas to a stand-alone Haskell compiler, it seemed easier to compile Haskell into Scheme or T, and then use a Scheme compiler as a back end.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 272] `written:2007-06-09_10-profiling-and-debugging:algorithmic-debugging`
  In algorithmic debugging the debugger takes the initiative, presenting calls with arguments and results and asking if correct, descending to children until it finds a call with an incorrect result whose children all behaved correctly, reported as the bug's location.
  > an approach in which the debugger, rather than the user, takes the initiative to explore the program's behaviour.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 284] `written:2007-06-09_10-profiling-and-debugging:algorithmic-debugging-laziness-problem`
  Algorithmic debugging suits lazy programs since it depends on input-output behaviour, but computing argument and result values early to display them might itself trigger faults or loops that would otherwise not occur.
  > If they were computed early by an algorithmic debugger, in order to display them in questions to the user, then this itself might trigger faults or loops that would otherwise not have been a problem at all!

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 34] `written:2007-06-09_10-profiling-and-debugging:cost-assignment-for-higher-order-functions`
  The conventional approach of assigning costs to functions works poorly for higher-order functions like map, which Haskell provides many of; knowing map's total share is less useful than knowing which occurrence of it dominates.
  > The conventional approach, of assigning costs to functions and procedures, works poorly for higher-order functions such as map.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 56] `written:2007-06-09_10-profiling-and-debugging:cost-centre-assignment-subtle`
  Assigning costs to cost centres raises subtle questions (closest lexical vs dynamic enclosing, first-class functions, order-independence under call-by-need), which drove the development of a formal cost semantics; a prototype ran with GHC before the semantics was published.
  > Assigning costs to explicitly labelled cost centres is much more subtle than it sounds.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 47] `written:2007-06-09_10-profiling-and-debugging:cost-centres`
  Sansom and Peyton Jones's new idea was to label source code with cost centres, manually or automatically, and aggregate the costs of one logical task into one count.
  > The new idea Sansom and Peyton Jones introduced was to label the source code with cost centres

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 22] `written:2007-06-09_10-profiling-and-debugging:eager-haskell-non-strict-semantics`
  Evaluating Haskell eagerly rather than lazily while retaining non-strict semantics, on a uniprocessor, was explored by Eager Haskell and optimistic evaluation.
  > The idea of evaluating Haskell eagerly rather than lazily (while retaining non-strict semantics), but on a uniprocessor, was also explored by Maessen's Eager Haskell

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 193] `written:2007-06-09_10-profiling-and-debugging:eval-class-solution`
  Haskell 1.3's solution made seq overloaded via a class Eval with automatically derived instances, recording uses of seq as Eval a => contexts so parametricity restrictions were visible, keeping short-cut deforestation sound while allowing leaks to be fixed at any type.
  > The solution adopted for Haskell 1.3 was to make seq an overloaded function, rather than a polymorphic one

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 218] `written:2007-06-09_10-profiling-and-debugging:eval-class-too-heavyweight`
  A TCP/IP stack in Haskell showed the Eval solution's limits: each seq on a type variable changed many explicit type signatures (forced by the monomorphism restriction), making trial-and-error space debugging too heavyweight, which provided ammunition for removing class Eval in Haskell 98.
  > each insertion of a seq became a nightmare, requiring repeated compilations to find affected type signatures and manual correction of each one.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 295] `written:2007-06-09_10-profiling-and-debugging:evaluation-dependence-trees`
  Sparud developed a debugger for Haskell by transforming source to collect debugging information while computing the result, and with Nilsson built evaluation dependence trees providing the information for post-mortem algorithmic debugging.
  > developing efficient methods to build 'evaluation dependence trees' (Nilsson and Sparud, 1997), data structures that provided all the necessary information for post-mortem algorithmic debugging.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 28] `written:2007-06-09_10-profiling-and-debugging:haskell-dauntingly-large`
  Haskell had come to seem such a dauntingly large language that no further implementations were expected, yet several new projects started in the last five years.
  > it had begun to seem that Haskell was such a dauntingly large language that no further implementations would emerge.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 306] `written:2007-06-09_10-profiling-and-debugging:hat-not-mainstream`
  Despite their power the Hat tools have not become a regular part of programming, probably because Haskell as used remains a moving target with frequent extensions, Hat was long restricted to Haskell 98, and its whole-program source-to-source transformation imposes a substantial performance penalty.
  > This is probably because Haskell, as it is used in practice, has remained a moving target: new extensions appear frequently, and so it is hard for a language-aware tool such as Hat to keep up.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 317] `written:2007-06-09_10-profiling-and-debugging:hood-observational-debugging`
  HOOD is a lighter post-mortem debugger where users insert observe calls; unlike trace it prints nothing when called, collecting its second argument tagged by the first, printing all values grouped by tag at the end, which also reveals how much of a lazy input was needed.
  > A more lightweight idea was pursued by Andy Gill, who developed HOOD, the Haskell Object Observation Debugger

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 346] `written:2007-06-09_10-profiling-and-debugging:hood-observes-functions`
  HOOD can observe function values as a table of observed arguments and results, the same information an algorithmic debugger would use, but it leaves locating the bug to the programmer.
  > HOOD can even observe function values, displaying them as a table of observed arguments and results

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 162] `written:2007-06-09_10-profiling-and-debugging:hughes-seq-for-space-debugging`
  Through working with Runciman on stubborn space leaks in an LML program where a carefully placed seq repeatedly proved critical, Hughes became concerned that Haskell's seq should support space debugging well.
  > Hughes was very concerned that Haskell's version of seq should support space debugging well.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 390] `written:2007-06-09_10-profiling-and-debugging:hunit-traditional-testing`
  HUnit, inspired by JUnit, supports more traditional unit testing: it does not generate test cases but provides ways to define them, structure them hierarchically, and run them automatically with a summary.
  > HUnit supports more traditional unit testing: it does not generate test cases, but rather provides ways to define test cases, structure them into a hierarchy, and run tests automatically with a summary of the results.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 456] `written:2007-06-09_10-profiling-and-debugging:impact-as-a-goal`
  A language need not have direct real-world impact to matter historically (Algol), but real-world impact was an important goal of the Haskell Committee; Haskell is not mainstream but has fared well in certain niches, with successes attributable to specific language characteristics.
  > impact on the real world was an important goal of the Haskell Committee, so it is worthwhile to consider how well we have achieved this goal.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 101] `written:2007-06-09_10-profiling-and-debugging:lag-drag-void-profiling`
  Extending the heap profiler to object lifetimes let it show data not yet needed (lag), never used again (drag), or never used at all (void).
  > The new profiler could show how much of the heap contained data that was not yet needed (lag), would never be used again (drag), or, indeed, was never used at all (void)

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 190] `written:2007-06-09_10-profiling-and-debugging:launchbury-vs-hughes`
  seq cast doubt on this use of parametricity; Launchbury argued parametricity was too important to give up, while Hughes wanted seq applicable to any type including type variables, two virtually incompatible goals.
  > Launchbury argued forcefully that parametricity was too important to give up, for this very reason.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 93] `written:2007-06-09_10-profiling-and-debugging:laziness-abstracts-object-lifetimes`
  By abstracting from evaluation order, lazy evaluation also abstracts from object lifetimes, which is why it contributes to space leaks: programmers cannot predict which structures live long, and fast allocation makes peak space high.
  > By abstracting away from evaluation order, lazy evaluation also abstracts away from object lifetimes, and that is why lazy evaluation contributes to space leaks.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 236] `written:2007-06-09_10-profiling-and-debugging:laziness-also-fixes-leaks`
  Making programs stricter is not the only way to fix space leaks; lifetimes can be shortened by moving last use earlier or creating objects later, and Runciman and Wakeling's first optimisation made the program more lazy, beating a fully strict ML translation.
  > making programs stricter is not the only way to fix space leaks in Haskell. Object lifetimes can be shortened by moving their last use earlier—or by creating them later.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 3] `written:2007-06-09_10-profiling-and-debugging:lazy-evaluation-hides-operational-aspects`
  A disadvantage of lazy evaluation is that operational aspects like evaluation order or memory contents are not predictable from the source and vary between runs, so conventional profiling and debugging are hard to apply.
  > One of the disadvantages of lazy evaluation is that operational aspects such as evaluation order, or the contents of a snapshot of memory at any particular time, are not easily predictable from the source code

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 351] `written:2007-06-09_10-profiling-and-debugging:one-trace-many-debuggers`
  Runciman realised that with a little generalisation the same trace could support several different kinds of debugging, the origin of the Hat project, which became a separate source-to-source tool usable with any Haskell 98 compiler and supporting many trace browsers.
  > Runciman realised that, with a little generalisation, the same trace could be used to support several different kinds of debugging

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 174] `written:2007-06-09_10-profiling-and-debugging:parametricity-justifies-deforestation`
  Parametricity was not just a bonus but the justification for short-cut deforestation (the foldr/build rule), which eliminates intermediate lists cheaply and holds only for sufficiently polymorphic g, guaranteed by a rank-2 type for build.
  > parametricity was by this time not just a nice bonus, but the justification for an important compiler optimisation, namely deforestation

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 20] `written:2007-06-09_10-profiling-and-debugging:ph-eager-haskell-syntax`
  pH adopted Haskell's syntax and type system while keeping Id's eager, parallel evaluation order, I-structures and M-structures, inspired by the MIT dataflow project.
  > In 1993 Arvind and his colleagues decided to adopt Haskell's syntax and type system, while retaining Id's eager, parallel evaluation order, I-structures, and M-structures.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 291] `written:2007-06-09_10-profiling-and-debugging:post-mortem-debugging`
  Nilsson solved the problem by waiting until execution completes before debugging: it is then known whether each value was required, so needed values can be used in questions and unneeded ones were irrelevant; this post-mortem approach abstracts from evaluation order and is used by all Haskell debuggers since.
  > This 'post mortem' approach abstracts nicely from evaluation order, and has been used by all Haskell debuggers since.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 73] `written:2007-06-09_10-profiling-and-debugging:profiler-faster-programs`
  The availability of a profiler led rapidly to faster Haskell programs, speeding up GHC itself by a factor of two.
  > the availability of a profiler led rapidly to faster Haskell programs, in particular speeding up GHC itself by a factor of two.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 12] `written:2007-06-09_10-profiling-and-debugging:profiling-debugging-took-research`
  Developing successful profiling and debugging tools for Haskell took considerable research, beginning in the early 1990s.
  > Developing successful profiling and debugging tools for Haskell has taken considerable research, beginning in the early 1990s.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 441] `written:2007-06-09_10-profiling-and-debugging:quickcheck-emulated-elsewhere`
  QuickCheck's design has been emulated in other languages, including Lindig's random C programs finding compiler calling-convention bugs and an Erlang port finding errors in an Ericsson Media Gateway.
  > This design has been emulated in many other languages.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 396] `written:2007-06-09_10-profiling-and-debugging:quickcheck-generators`
  To scale beyond toy examples, QuickCheck lets programmers control random generation via an abstract data type of generators that conceptually represent sets of values with a probability distribution, with a library of combinators to define them.
  > QuickCheck supports this via an abstract data type of 'generators,' which conceptually represent sets of values (together with a probability distribution).

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 367] `written:2007-06-09_10-profiling-and-debugging:quickcheck-specifications-as-tests`
  QuickCheck's idea is to test programs against specifications written as boolean functions that should always return True, invoked on random data, with counter-examples displayed on failure, letting programmers test many cases for the effort of one property.
  > programs can be tested against specifications by formulating specifications as boolean functions that should always return True, and then invoking these functions on random data.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 428] `written:2007-06-09_10-profiling-and-debugging:quickcheck-succeeds-by-audience`
  QuickCheck may have succeeded partly because of who Haskell programmers are: many would rather write formal specifications than test code, and QuickCheck lets them test by writing specifications.
  > Perhaps QuickCheck has succeeded in part because of who Haskell programmers are

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 433] `written:2007-06-09_10-profiling-and-debugging:quickcheck-uses-haskell-features`
  QuickCheck exemplifies Haskell's features: a domain-specific language of testable properties, the class system associating a generator with each type and overloading quickCheck, generators as a monad with syntactic sugar; the language profoundly influenced its design.
  > QuickCheck is not only a useful tool, but also a good example of applying some of Haskell's unique features.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 340] `written:2007-06-09_10-profiling-and-debugging:redex-trails`
  Redex trails are a form of program trace supporting stepping backwards through execution, so programmers can ask why a function was called with given arguments as well as inspect the call.
  > redex trails, another form of program trace which supports stepping backwards through the execution

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 104] `written:2007-06-09_10-profiling-and-debugging:retainer-profiling`
  Retainer profiling could explain why data was not garbage collected by showing which objects pointed at the data of interest.
  > A further extension introduced retainer profiling, which could explain why data was not garbage collected by showing which objects pointed at the data of interest

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 117] `written:2007-06-09_10-profiling-and-debugging:seq-and-strictness-annotations`
  Haskell 1.3 introduced seq (evaluates its first argument then returns its second) and strictness annotations in data definitions, giving the programmer control over evaluation order and letting computations move earlier to shorten lifetimes.
  > In 1996, Haskell 1.3 introduced two features that give the programmer better control over evaluation order

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 164] `written:2007-06-09_10-profiling-and-debugging:seq-breaks-semantics`
  seq was controversial for its effect on semantics: not definable in the lambda calculus and the only way to distinguish \x -> ⊥ from ⊥, a distinction Fairbairn was set against.
  > adding seq to Haskell was controversial because of its negative effect on semantic properties.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 142] `written:2007-06-09_10-profiling-and-debugging:seq-introduced-for-speed`
  Although seq is now a common way to fix space leaks, it was primarily introduced to improve speed, by helping the strictness analyser deliver better results on nearly-strict functions; strictness annotations addressed poor analysis of data types and let the compiler optimise representations.
  > interestingly, this was not the main reason for introducing it into Haskell. On the contrary, seq was primarily introduced to improve the speed of Haskell programs!

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 227] `written:2007-06-09_10-profiling-and-debugging:seq-now-polymorphic-unsound-deforestation`
  Today seq is a simple polymorphic function insertable freely, sacrificing parametricity for agility and optimisation; GHC's short-cut deforestation is consequently unsound.
  > We have sacrificed parametricity in the interests of programming agility and (sometimes dramatic) optimisations. GHC still uses short-cut deforestation, but it is unsound

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 138] `written:2007-06-09_10-profiling-and-debugging:seq-predates-haskell`
  seq and strict data components were already in Miranda for the same reasons, and seq had been used to fix space leaks since the early 1980s.
  > Both seq and strict components of data structures were already present in Miranda for the same reasons

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 166] `written:2007-06-09_10-profiling-and-debugging:seq-weakens-parametricity`
  seq does not satisfy the parametricity property for its type and so weakens the parametricity of functions that use it, weakening Wadler's free theorems.
  > seq weakens the parametricity property that polymorphic functions enjoy, because seq does not satisfy the parametricity property for its type ∀a,b.a -> b -> b

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 79] `written:2007-06-09_10-profiling-and-debugging:space-leaks-heap-profiling`
  Lazy programs could exhibit astonishingly poor space behaviour (space leaks); Runciman and Wakeling built a heap profiler classifying heap contents by allocating function or constructor, enabling dramatic space improvements.
  > It had been known for some time that lazy programs could sometimes exhibit astonishingly poor space behaviour—so-called space leaks.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 247] `written:2007-06-09_10-profiling-and-debugging:space-sensitivity-two-edged`
  Haskell's extreme sensitivity of space use to evaluation order is a two-edged sword: hard to anticipate when writing, but fixable dramatically by tiny changes with good profiling; the designers are a little ashamed reasoning about space is so intractable, yet the language lets programmers defer space optimisation and then supplies powerful tools.
  > The extreme sensitivity of Haskell's space use to evaluation order is a two-edged sword.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 10_profiling-and-debugging.md line 262] `written:2007-06-09_10-profiling-and-debugging:trace-garbled-output`
  Unpredictable evaluation order makes conventional tracing hard: the trace function's printing of its first argument can trigger another call before the first completes, giving garbled output, so better debuggers abstract from evaluation order.
  > it is not at all uncommon for the printing of the first argument to trigger another call of trace before the printing is complete, leading to very garbled output.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 3] `written:2007-06-09_11-applications:applications-grew-from-libraries`
  Some of Haskell's most important applications began life as libraries; the standard set is modest but many more exist.
  > Some of the most important applications of Haskell were originally developed as libraries. The Haskell standard includes a modest selection of libraries, but many more are available.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 192] `written:2007-06-09_11-applications:arrows-improve-frp`
  An arrow-based version of FRP called Yampa improved both the modularity and performance of previous implementations.
  > the development of an arrowbased version of FRP called Yampa in 2002, that improves both the modularity and performance of previous implementations

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 153] `written:2007-06-09_11-applications:behaviour-as-time-varying-value`
  The key idea in Fran is a behaviour, a first-class data type representing a time-varying value, really a function from time to values.
  > The key idea in Fran is the notion of a behaviour, a first-class data type that represents a time-varying value.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 54] `written:2007-06-09_11-applications:bnf-to-executable-code`
  Parser combinators allow an extraordinarily direct transcription of BNF into executable code.
  > doing so allows an extraordinarily direct transcription of BNF into executable code.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 114] `written:2007-06-09_11-applications:call-by-value-cost-of-eta-expansion`
  In call-by-value languages recursive combinator definitions are generally disallowed, forcing eta-expansion that clutters code and wrecks the abstraction.
  > In call-by-value languages, recursive definitions like this are generally not allowed. Instead, one would have to eta-expand the definition, thereby cluttering the code and (much more importantly) wrecking the abstraction

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 284] `written:2007-06-09_11-applications:class-system-signals-lists`
  Clever use of Haskell's class system let Lava use signals-of-lists and lists-of-signals almost interchangeably, without a profusion of zips and unzips.
  > Clever use of the class system enables signals-of-lists and lists-of-signals, for example, to be used almost interchangeably, without a profusion of zips and unzips.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 450] `written:2007-06-09_11-applications:clean-integrated-io-vs-fragmented-haskell`
  Clean's graphical I/O library was integral from an early stage, letting the user specify the interface by a data structure of call-back functions, contrasted with the fragmented approach Haskell took to GUIs.
  > A notable example is the Clean graphical I/O library, which formed an integral part of the Clean system from a very early stage ... (unlike the fragmented approach to GUIs taken by Haskell).

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 98] `written:2007-06-09_11-applications:combinator-libraries-not-new-but-influential`
  Combinator libraries embody nothing fundamentally new, yet the idea has been extremely influential across widely different areas.
  > combinator libraries do not embody anything fundamentally new. Nevertheless, the idea has been extremely influential

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 383] `written:2007-06-09_11-applications:combinator-library-and-dsel-same`
  There is little conceptual difference between combinator libraries and DSELs; which term a project uses is probably only historical.
  > It is probably only for historical reasons that one project might use the term “combinator library” and another the term “DSL” (or “DSEL”).

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 38] `written:2007-06-09_11-applications:combinator-library-as-dsl`
  A combinator library can be viewed as a domain-specific language for describing values of a particular type.
  > Another productive way to think of a combinator library is as a domain-specific language (DSL) for describing values of a particular type

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 17] `written:2007-06-09_11-applications:combinator-library-definition`
  The term "combinator library" has no settled definition in the literature; its key idea is a library of functions that combine functions into bigger functions.
  > a combinator library offers functions (the combinators) that combine functions together to make bigger functions.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 37] `written:2007-06-09_11-applications:conceptual-vs-implementation-representation`
  Though a Doc can be thought of as a function, it need not be implemented as one; this trade-off is a theme of Hughes's paper.
  > While a Doc can be thought of as a function, it may not be implemented as a function; indeed, this trade-off is a theme of Hughes’s paper.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 221] `written:2007-06-09_11-applications:continuations-or-monads-for-web`
  The inverted web approach needs no new language; it can be supported with continuations or monads (the two quite similar), and arrows arose independently as a generalisation.
  > this idea can be supported using concepts available in functional languages, either continuations or monads (the two approaches are quite similar).

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 389] `written:2007-06-09_11-applications:declarative-gui-radical-question`
  The idealists rejected the imperative event-loop model and asked what the right way is to interact with a GUI in a purely declarative setting, yielding unusual systems (Fudgets, Haggis, FranTk, Fruit).
  > they sought to answer the question, “What is the right way to interact with a GUI in a purely declarative setting?”

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 121] `written:2007-06-09_11-applications:dsel-definition`
  A DSEL turns Haskell into a domain-specific embedded language, a term first coined by Hudak; the embedded language is simply an extension of Haskell sharing its syntax, function definition, type system and modules.
  > the idea of writing a library that turns Haskell into a domainspecific embedded language (DSEL), a term first coined by Hudak

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 131] `written:2007-06-09_11-applications:dsel-execution-model`
  A DSEL typically defines a data type whose nature is conceptually a function, with operators combining these into larger ones, the final program "executed" by decomposing and applying the embedded functions.
  > The final program is then “executed” by decomposing these larger pieces and applying the embedded functions in a suitable manner.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 134] `written:2007-06-09_11-applications:embedded-vs-nonembedded-dsl`
  A non-embedded DSL can instead be implemented with a conventional parser, type checker and interpreter or compiler, an approach Haskell also suits well, but Haskell has been particularly successful at embedded DSLs.
  > a non-embedded DSL can be implemented by writing a conventional parser, type checker, and interpreter (or compiler) for the language. Haskell is very well suited to such approaches as well. However, Haskell has been particularly successful for domain-specific embedded languages.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 182] `written:2007-06-09_11-applications:events-and-hybrid-systems`
  Fran's second key idea is an infinite stream of events; switching combinators connect behaviours and events (continuous and discrete), making Fran-like languages suitable for hybrid systems.
  > Various “switching” combinators provide the connection between behaviours and events—i.e. between the continuous and the discrete—thus making Fran-like languages suitable for socalled “hybrid systems.”

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 440] `written:2007-06-09_11-applications:ffi-absence-hampered-bindings`
  Pragmatist bindings were hampered by the absence of a well-defined foreign-function interface, making early bindings compiler-specific and partial; later ones generate the binding automatically into the Haskell 98 FFI.
  > These efforts were hampered by the absence of a well defined foreignfunction interface for Haskell, especially as the libraries involved have huge interfaces.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 409] `written:2007-06-09_11-applications:haggis-drove-concurrent-haskell`
  Haggis replaced the event loop with lightweight concurrency, and its requirements directly drove the development of Concurrent Haskell.
  > The requirements of Haggis directly drove the development of Concurrent Haskell

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 512] `written:2007-06-09_11-applications:haskell-chosen-for-compilation-partial-evaluation`
  Haskell was chosen for GF as suitable particularly for the compilation and partial evaluation aspects of grammars, with monads and type classes extensively used.
  > Haskell was chosen as a suitable language for this kind of system, particularly for the compilation and partial evaluation aspects (of grammars).

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 328] `written:2007-06-09_11-applications:haskore-declarative-music-model`
  Haskore expresses high-level musical concepts purely declaratively, combining primitive notes and rests with combinators for sequential and parallel composition into larger musical values.
  > Haskore is a computer music library written in Haskell that allows expressing high-level musical concepts in a purely declarative way

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 209] `written:2007-06-09_11-applications:haxml-two-approaches-tradeoff`
  HaXml gave two XML approaches with complementary strengths: a flexible combinator library where all XML has one type, and a data-binding approach capturing more precise types but less flexible.
  > the combinator library is flexible but all XML data has the same type; the data-binding approach captures more precise types but is less flexible.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 468] `written:2007-06-09_11-applications:house-os-monad-for-hardware-access`
  House implemented a system (kernel, window system, device drivers) entirely in Haskell, using a monad to provide access to the Intel IA32 architecture including virtual memory and low-level IO.
  > It uses a monad to provide access to the Intel IA32 architecture, including virtual memory management, protected execution of user binaries, and low-level IO operations.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 388] `written:2007-06-09_11-applications:idealists-vs-pragmatists-gui`
  For GUIs, Haskell people split into idealists seeking the right purely declarative way to interact, and pragmatists wanting to get the job done by binding to an existing toolkit.
  > People interested in this area rapidly split into two groups: the idealists and the pragmatists.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 108] `written:2007-06-09_11-applications:laziness-enables-combinator-libraries`
  Beyond higher-order functions and data abstraction, two main factors make Haskell a natural fit for combinator libraries, both about laziness: writing recursive combinators without fuss, and unusual control flow.
  > there seem to be two main factors, both concerning laziness. First, one can write recursive combinators without fuss

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 494] `written:2007-06-09_11-applications:laziness-essential-for-nlp-ambiguity`
  In LOLITA, handling unrestricted text made ambiguity unavoidable and significant; laziness was essential to handle the explosion of syntactic ambiguity from a large grammar, and much used for semantic ambiguity too.
  > Laziness was essential in handling the explosion of syntactic ambiguity resulting from a large grammar, and it was much used with semantic ambiguity too.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 130] `written:2007-06-09_11-applications:laziness-gives-macro-power`
  In Haskell, thanks to lazy evaluation, much (though not all) of the power of Lisp macros is available through ordinary function definitions.
  > in Haskell, thanks to lazy evaluation, much (although emphatically not all) of the power of macros is available through ordinary function definitions.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 247] `written:2007-06-09_11-applications:laziness-higher-order-for-hardware`
  Lazy functional languages suit synchronous hardware for two fundamental reasons: lazy streams model discrete time-varying signals for easy simulation, and higher-order functions express regular circuit structure.
  > first, because lazy streams provide a natural model for discrete time-varying signals, making simulation of functional models very easy; and second, because higher-order functions are ideal for expressing the regular structure of many circuits.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 459] `written:2007-06-09_11-applications:no-standard-gui-inhibits-haskell`
  The community periodically agonises over the absence of a single standard Haskell GUI; lacking it is undoubtedly an inhibiting factor on Haskell's development, yet no approach has garnered enough support.
  > Lacking such a standard is undoubtedly an inhibiting factor on Haskell’s development. Yet no one approach has garnered enough support to become the design

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 170] `written:2007-06-09_11-applications:num-classes-overload-behaviours`
  Since many Fran behaviours are numeric, Haskell's Num and Floating classes let one specify how to add behaviours or take their sine.
  > Haskell’s Num and Floating classes (for example) allow one to specify how to add two behaviours or take the sine of a behaviour

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 315] `written:2007-06-09_11-applications:observable-sharing-unsafe-but-tractable`
  Claessen used unsafePerformIO for "observable sharing", keeping the natural syntax while distinguishing sharing from duplication; despite its unsafe implementation it has a tractable theory and extended Haskell's power.
  > Claessen used unsafePerformIO to implement “observable sharing” ... Despite its unsafe implementation, observable sharing turns out to have a rather tractable theory

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 50] `written:2007-06-09_11-applications:parser-as-function-type`
  A parser can be modelled as a function from a string to a list of depleted input strings, with failure as the empty list.
  > type Parser = String -> [String]

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 47] `written:2007-06-09_11-applications:parser-combinators-history`
  Parser combinators, a fertile use of combinator libraries, go back to Burge (1975) and were brought to wider attention by Wadler's "list of successes" paper, though he called it folklore and did not use the word "combinator".
  > it was probably Wadler’s paper “How to replace failure by a list of successes” ... that brought it wider attention, although he did not use the word “combinator” and described the work as “folklore”.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 74] `written:2007-06-09_11-applications:parsers-and-monads`
  Wanting a parser to return a value, not just recognise, dovetails precisely with Haskell's notion of a monad, giving parameterised Parser t and do-notation.
  > a requirement that dovetails precisely with Haskell’s notion of a monad (Section 7).

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 71] `written:2007-06-09_11-applications:programmer-makes-new-combinators`
  Programmers can easily build new parser combinators by combining existing ones.
  > It is easy for the programmer to make new parser combinators by combining existing ones.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 429] `written:2007-06-09_11-applications:purity-cost-for-gui`
  None of the declarative GUIs became the toolkit of choice; developing a full GUI is huge, and the quest for purity always led to programming inconvenience in some form.
  > Second, the quest for purity always led to programming inconvenience in one form or another.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 351] `written:2007-06-09_11-applications:purity-laziness-ho-enable-elegant-music`
  Haskore rests on a simple declarative model of music with nice algebraic properties, generalizable to other time-varying media; purity, lazy evaluation and higher-order functions are the key features making the design possible.
  > Haskell’s purity, lazy evaluation, and higher-order functions are the key features that make possible this elegant design.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 300] `written:2007-06-09_11-applications:sharing-vs-duplication-problem`
  Capturing sharing was tricky because two code fragments the designer intends differently (two gates vs one shared gate) are indistinguishable under Haskell's intended semantics, though their net-lists should differ.
  > yet according to Haskell’s intended semantics, these two fragments should be indistinguishable. For a while, Lava used a “circuit monad” to make the difference observable

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 361] `written:2007-06-09_11-applications:six-features-for-dsels`
  No single feature dominates, but six ways make Haskell a friendly host for a DSEL: type classes (overloading), higher-order functions (glue), infix syntax, over-loaded numeric literals, monads and arrows, and lazy evaluation.
  > No single feature seems dominant, but we may identify the following ways in which Haskell is a particularly friendly host language for a DSEL

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 22] `written:2007-06-09_11-applications:smart-document-as-abstract-type`
  In Hughes's pretty-printing library a "smart document" is an abstract type conceptually a function from available width to a layout string.
  > a “smart document” was an abstract type that can be thought of like this: ... type Doc = Int -> String

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 235] `written:2007-06-09_11-applications:static-typing-for-web-forms`
  Thiemann's work showed the web approach works with a static type system guaranteeing the form's returned type matches what the application expects, and used type classes to ensure HTML/XML satisfies DTD-imposed regular expression types.
  > the same approach works with a static type system that can guarantee that the type of information returned by the form matches the type of information that the application expects.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 6] `written:2007-06-09_11-applications:type-classes-organise-data-structures`
  The Edison library offers multiple implementations of sequences and collections, organised using type classes.
  > provides multiple implementations of sequences and collections, organised using type classes.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 11_applications.md line 216] `written:2007-06-09_11-applications:web-app-invert-the-view`
  Rather than split a web application into one program per client-server interaction, it is better to invert the view and write a single program calling a primitive that takes an HTML form and returns the responses.
  > Arguably, it is better to invert this view, and instead to write a single program containing calls to a primitive that takes an HTML form as argument and returns the responses as the result

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md line 261] `written:2007-06-09_12-the-impact-of-haskell:abstraction-and-non-interference`
  The abstraction and non-interference properties of functional languages make compilers and code translation natural applications, giving high productivity even with minimal project management.
  > the abstraction and non-interference properties of functional languages meant that productivity was very high, even with minimal project management overhead

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md line 136] `written:2007-06-09_12-the-impact-of-haskell:class-system-error-messages`
  The class system causes minor irritations, sometimes producing puzzling error messages.
  > The class system causes minor irritations, sometimes leading to ... puzzling error messages for students.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md line 570] `written:2007-06-09_12-the-impact-of-haskell:comprehensions-and-monad-comprehensions-as-influence`
  The authors trace list comprehensions (adopted by Python, then Javascript) and monad comprehensions (basis of LINQ in C#/Visual Basic, and Scala's for-comprehensions) as features of Haskell carried into other languages.
  > The LINQ (Language INtegrated Query) features of C# 3.0 and Visual Basic 9.0 are based on monad comprehensions from Haskell.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:extensions-vs-standard`
  So many extensions have appeared since Haskell 98 that few real programs adhere to the standard, which the authors frame as a problem for users (naming their language), tool builders (which extensions to support), and teachers (which to teach), motivating a new "Industrial Haskell" standard.
  > So many extensions have appeared since the latter was defined that few real programs adhere to the standard nowadays.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:haskell-as-two-level-compile-time-language`
  Reporting Bluespec, the full power of Haskell is available at compile time and eliminated by a partial evaluator, making it "a two-level language."
  > Bluespec is really a two-level language. The full power of Haskell is available at compile time, but almost all Haskell language constructs are eliminated by a partial evaluator

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:haskell98-stability-step`
  The authors read Haskell 98 as the step from a frequently changing research vehicle to a language with a guarantee of long-term stability, tentatively linking it to the community's stronger growth.
  > the year that Haskell took the step from a frequently changing vehicle for research to a language with a guarantee of long-term stability

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:helium-drops-classes-tradeoff`
  Helium, a simplified Haskell for teaching, omits classes to give clearer error messages, at the cost of textbooks and the ability to "tackle the awkward squad" (a deliberate trade-off).
  > Helium lacks classes, which enables it to give clearer error messages, but then it also lacks textbooks and the ability to “tackle the awkward squad.”

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:high-level-concentrate-on-problem`
  As a very high-level language Haskell lets programmers write succinct but readable code and concentrate on the problem without boilerplate and housekeeping.
  > they can concentrate on the problem at hand without being distracted by all the attendant programming boilerplate and housekeeping

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md line 139] `written:2007-06-09_12-the-impact-of-haskell:in-place-update-messier`
  Array processing and algorithms relying on in-place update are messier in Haskell than in imperative languages.
  > Array processing and algorithms using in-place update are ... messier in Haskell.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md line 142] `written:2007-06-09_12-the-impact-of-haskell:io-and-the-awkward-squad`
  Haskell's input/output, and the issues of the "awkward squad," are poorly covered by textbooks that present only the purely functional aspects.
  > Haskell input/output is not well covered by current textbooks

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:legacy-is-influence-on-successors`
  The authors' wish/belief that Haskell's most important legacy will be its influence on the languages that succeed it.
  > We believe the most important legacy of Haskell will be how it influences the languages that succeed it.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md line 39] `written:2007-06-09_12-the-impact-of-haskell:mathematical-look-and-feel`
  Haskell has a mathematical look and feel that makes it a medium for teaching discrete mathematics and logic.
  > exploiting Haskell’s mathematical look and feel

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:minimal-surfaces`
  An analogy for Haskell solutions: the language, libraries and culture lead to solutions that feel like minimal surfaces, simple expressions comprising significant complexity with natural, recurring forms.
  > solutions that feel like minimal surfaces: simple expressions that comprise significant complexity, with forms that seem natural, recurring in problem after problem

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md line 133] `written:2007-06-09_12-the-impact-of-haskell:recursion-vs-simple-loops`
  Expressing simple loop programs through recursion can be harder for students to grasp (a cost of the functional style).
  > Simple loop programs can be harder for students to grasp when ... expressed using recursion.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:referential-transparency-executable-mathematics`
  Because of referential transparency, Haskell programs can be read as executable mathematics, equations over the category of complete partial orders, so that in principle the specification becomes the program.
  > Because of referential transparency, Haskell programs can be viewed as executable mathematics, as equations over the category of complete partial orders. In principle, at least, the specification becomes the program.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:rewrite-rules-for-performance`
  Data.ByteString represents strings as byte vectors and uses GHC's rewrite rules to program the optimiser so loop fusion happens when bytestring functions compose; the correctness of the rules (and agreement with String operations) is tested by QuickCheck, held up as using advanced features for performance and reliability without compromising elegance.
  > by using GHC’s rewrite rules to program the compiler’s optimiser, so that loop fusion is performed when bytestring functions are composed

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:rich-static-type-system-as-reason-to-choose`
  Aetion chose Haskell for its rich static type system, open-source compilers, and active research community; static typing is reported to catch many errors that would otherwise surface in the field.
  > They chose Haskell, because of its rich static type system, open-source compilers, and its active research community.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:separate-data-types-for-legacy-formats`
  Explicitly segregating legacy data formats into separate data types prevented the mysterious errors that propagate through shell programs when a format changes.
  > Explicitly segregating these formats into separate data types prevented the mysterious errors that always seem to propagate through shell programs when the format changes.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:strict-and-lazy-evaluation-difficulty`
  A main difficulty is constructing software that uses both strict and lazy evaluation well (an efficiency/evaluation-model tension).
  > how to construct software that uses both strict and lazy evaluation well

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md line 9] `written:2007-06-09_12-the-impact-of-haskell:teaching-as-explicit-design-goal`
  Suitability for teaching was one of the stated goals the designers set for Haskell.
  > One of the explicit goals of Haskell’s designers was to create a language suitable for teaching.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:type-classes-as-influence`
  The authors treat type classes as a Haskell contribution picked up elsewhere: Java 5's bounded generic types (on Hindley-Milner) are closely related to them, as are Scala's view bounds and implicit parameters.
  > The use of bounded types in that system is closely related to type classes in Haskell.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:type-classes-with-laws`
  Reporting Isabelle, declaring a type class can carry the laws its operations obey (e.g. a ring), and declaring an instance requires proving the instance satisfies them.
  > When a type class is declared one associates with it the laws obeyed by the operations in a class ... and when an instance is declared one must prove that the instance satisfies those properties

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md line 127] `written:2007-06-09_12-the-impact-of-haskell:types-and-recursion-early`
  Teaching reports that Haskell drives fundamental concepts like types and recursion home early, and lets students tackle more ambitious problems sooner than in a language like Java.
  > Fundamental concepts such as types and recursion are ham- mered home early.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:types-of-numeric-kind`
  Reporting Bluespec, the authors note Haskell's type system was extended with types of numeric kind, so the class system can do (limited, statically checked) arithmetic on them, giving accurate types to things like bit vectors rather than using lists whose sizes the type checker cannot check.
  > The type system has been extended with types of numeric kind. ... Their purpose is to give accurate types to things like bit vectors (instead of using lists where the sizes cannot be checked by the type checker).

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md line 335] `written:2007-06-09_12-the-impact-of-haskell:uniformity-vs-perl-compactness`
  Reporting Linspire, Haskell has comparable versatility to shell/script languages but promotes much greater uniformity; its idioms for systems programming are not quite as compact as Perl's, an acknowledged lack offset by other benefits and an active research area.
  > Haskell has comparable versatility but promotes much greater uniformity.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:uniqueness-types-as-io-alternative`
  Reporting Clean, the authors note it adopted type classes from Haskell but used uniqueness (linear) types for input-output instead of monads, presenting an alternative to Haskell's monadic I/O.
  > instead of using monads for input-output it uses an approach based on uniqueness (or linear) types

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 13_conclusion.md line 18] `written:2007-06-09_13-conclusion:convergence-from-both-ends`
  The authors observe a convergence: the functional community has learned the value of effects and a way to tame them, while mainstream languages adopt declarative constructs.
  > At one end, the purely functional community has learnt both the merit of effects, and at least one way to tame them. At the other end, mainstream languages are adopting more and more declarative constructs: comprehensions, iterators, database query expressions, first-class functions, and more besides.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 13_conclusion.md line 6] `written:2007-06-09_13-conclusion:early-impracticality`
  In the early 1980s purely functional languages, though radical and elegant, were impractical: slow, memory-hungry, and lacking input/output.
  > purely functional languages might have been radical and elegant, but they were also laughably impractical: they were slow, took lots of memory, and had no input/output.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 13_conclusion.md line 26] `written:2007-06-09_13-conclusion:enduring-value-through-influence`
  The authors anticipate that even after Haskell itself is forgotten, the ideas and techniques it nurtured will have lasting value through their influence on future languages.
  > when that day comes, the ideas and techniques that it nurtured will prove to have been of enduring value through their influence on languages of the future.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 13_conclusion.md line 9] `written:2007-06-09_13-conclusion:haskell-contributed-through-purity-and-critical-mass`
  The authors credit Haskell with helping overcome that impracticality by holding strictly to purity and by gathering a critical mass of interest and research around one language.
  > Haskell has contributed to that progress, by sticking remorselessly to the discipline of purity, and by building a critical mass of interest and research effort behind a single language.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 13_conclusion.md line 13] `written:2007-06-09_13-conclusion:longterm-bet-on-principled-control-of-effects`
  Beyond instinct, the authors describe a conscious long-term bet that principled control of effects would prove important, against the mainstream default of unrestricted effects.
  > many of us were consciously making a longterm bet that principled control of effects would ultimately turn out to be important, despite the dominance of effects-by-default in mainstream languages.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 13_conclusion.md line 23] `written:2007-06-09_13-conclusion:parallelism-punishes-unrestricted-effects`
  The authors expect the convergence to continue, driven especially by parallelism, which they say penalizes unrestricted effects severely.
  > driven especially by the goad of parallelism, which punishes unrestricted effects cruelly.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 13_conclusion.md line 3] `written:2007-06-09_13-conclusion:purely-functional-as-principled-attack`
  Functional programming in its purely functional form is characterized as a deliberate, principled attempt to meet the difficulty of writing programs that work.
  > Functional programming, particularly in its purely functional form, is a radical and principled attack on the challenge of writing programs that work.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 13_conclusion.md line 12] `written:2007-06-09_13-conclusion:purity-not-the-one-right-way`
  The authors disclaim that purely functional programming is necessarily the correct way to write programs.
  > Purely functional programming is not necessarily the Right Way to write programs.

- **00:00** Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler [written: 13_conclusion.md line 4] `written:2007-06-09_13-conclusion:quirky-elegance-drew-designers`
  The authors say what first drew many of them to the field was the odd elegance of the purely functional approach.
  > It was precisely this quirky elegance that attracted many of us to the field.

## Inputs

| file | prompt | model | effort | rows | quotes found | sha256 |
|---|---|---|---|---|---|---|
| 2007-06-09_01-introduction_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 11 | 6/11 | 19f0a6af4665 |
| 2007-06-09_02-the-genesis-of-haskell_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 35 | 34/35 | fe776ee4dcb5 |
| 2007-06-09_04-syntax_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 35 | 35/35 | e7c389998bc8 |
| 2007-06-09_05-data-types-and-pattern-matching_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 42 | 40/42 | a2c1d5f20aa3 |
| 2007-06-09_06-haskell-as-a-type-system-laboratory_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 46 | 44/46 | 063472531956 |
| 2007-06-09_07-monads-and-input-output_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 40 | 39/40 | 65c0b1004608 |
| 2007-06-09_08-haskell-in-middle-age_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 15 | 15/15 | 35e745d2a0d8 |
| 2007-06-09_09-implementations_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 41 | 41/41 | f9d105effc42 |
| 2007-06-09_10-profiling-and-debugging_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 43 | 41/43 | 0a1eb342ca64 |
| 2007-06-09_11-applications_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 44 | 43/44 | f219f7359a8d |
| 2007-06-09_12-the-impact-of-haskell_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 26 | 10/26 | a6c96eb49ede |
| 2007-06-09_13-conclusion_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 9 | 9/9 | 349d8c5fc097 |
