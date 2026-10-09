---
note: 02_the-genesis-of-haskell.md
note_dir: texts
note_sha256: 8381c929d1fe62e35a8c8026bb0f871af3c5f8a46b460f058c1179389cf1ebd1
title: "2. The genesis of Haskell"
author: Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler
created: 2007-06-09T00:00:00
ideas: 35
quotes_found: 34/35
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Haskell; designers=Paul Hudak, John Hughes, Simon Peyton Jones and Philip Wadler
agent: claude-code
model: opus
effort: low
---

## Ideas

### functional-programming-as-practical-tool
- **What**: Backus's Turing Award lecture recast functional programming as a radical attack on the whole programming enterprise, moving it from mathematical curiosity to practical tool.
- **Quote**: "which positioned functional programming as a radical attack on the whole programming enterprise, from hardware architecture upwards" (line 4)
- **Also at**: lines 6-8

### lambda-calculus-for-modelling-languages
- **What**: Landin and Strachey established the lambda calculus as fundamental for modelling programming languages, grounding both operational and denotational semantics.
- **Quote**: "identified the fundamental importance of the lambda calculus for modelling programming languages" (line 12)

### sasl-sugared-lambda-with-pattern-matching
- **What**: Turner's SASL was a pure higher-order functional language, a sugared lambda calculus with lexical scoping, that brought Burstall and Darlington's pattern matching into an executable language.
- **Quote**: "a pure higher-order functional language with lexically scoped variables" (line 20)
- **Also at**: lines 23-24

### lazy-evaluation-invented-three-times
- **What**: Lazy (non-strict, call-by-need) evaluation emerged independently three times, igniting interest in lazy functional languages for serious programs.
- **Quote**: "Lazy evaluation appears to have been invented independently three times." (line 35)

### cons-should-not-evaluate-arguments
- **What**: Friedman and Wise framed lazy evaluation from a Lisp perspective with the slogan that cons should not evaluate its arguments.
- **Quote**: "“Cons should not evaluate its arguments”" (line 39)

### lazy-lists-emulate-behaviours
- **What**: Turner demonstrated the elegance of programming with lazy evaluation, using lazy lists to emulate many kinds of behaviours.
- **Quote**: "Turner showed the elegance of programming with lazy evaluation, and in particular the use of lazy lists to emulate many kinds of behaviours" (line 54)

### pure-lazy-fp-in-the-large
- **What**: SASL was used at Burroughs to build an entire operating system, likely the first exercise of pure, lazy, functional programming at large scale.
- **Quote**: "SASL was even used at Burroughs to develop an entire operating system—almost certainly the first exercise of pure, lazy, functional programming “in the large”." (line 57)

### graph-reduction-and-sk-combinators
- **What**: Lazy languages were implemented through graph reduction techniques, notably Turner's elegant use of SK combinators derived from combinatory calculus.
- **Quote**: "a variety of techniques based on graph reduction were being explored, and in particular Turner’s inspirationally elegant use of SK combinators" (line 62)

### non-von-neumann-hardware-dead-end
- **What**: A hope was that lazy evaluation would lead to radically different non-von Neumann hardware; much of this work later proved a dead end when stock-architecture compilers outperformed specialised machines.
- **Quote**: "the possibility that all this would lead to a radically different non-von Neumann hardware architectures" (line 68)
- **Also at**: lines 77-79

### hope-algebraic-data-types
- **What**: Hope introduced algebraic data types.
- **Quote**: "Hope, the language that introduced algebraic data types" (line 84)

### laziness-as-a-drug
- **What**: The appeal of lazy evaluation lay in its direct connection to the call-by-name lambda calculus, the possibility of infinite data structures, and simple, beautiful implementation techniques.
- **Quote**: "Lazy evaluation—with its direct connection to the pure, call-by-name lambda calculus, the remarkable possibility of representing and manipulating infinite data structures, and addictively simple and beautiful implementation techniques—was like a drug." (line 117)

### simulate-call-by-name-easier
- **What**: Reported from an anonymous reviewer: Sussman and Steele kept Scheme call-by-value, reasoning that simulating call-by-name in a call-by-value language (via thunks) is easier than the reverse.
- **Quote**: "reasoning that it seemed to be much easier to simulate call-by-name in a call-by-value language (using lambda-expressions as thunks) than to simulate call-by-value in a call-by-name language" (line 124)

### tower-of-babel-common-language
- **What**: The many single-site lazy languages were felt to be roughly the same bar syntax, prompting the wish for a single, common language all could benefit from.
- **Quote**: "we felt that they were all roughly the same, bar the syntax, and we started to wonder why we didn’t have a single, common language that we could all benefit from." (line 180)

### miranda-polymorphic-typing
- **What**: Where SASL and KRC were untyped, Miranda added strong polymorphic typing and type inference, ideas proven successful in ML.
- **Quote**: "Miranda added strong polymorphic typing and type inference, ideas that had proven very successful in ML." (line 139)

### g-machine-laziness-not-interpretation
- **What**: The G-machine showed lazy functional programs could be compiled to efficient code, overturning the assumption that laziness meant graph reduction and graph reduction meant interpretation.
- **Quote**: "the influential development of the Gmachine, which showed that one could compile lazy functional programs to rather efficient code" (line 143)
- **Also at**: lines 145-148

### begin-from-existing-language
- **What**: A key outcome of the first meeting was that the easiest way forward was to start from an existing language and evolve it.
- **Quote**: "the easiest way to move forward was to begin with an existing language, and evolve it in whatever direction suited us." (line 204)

### miranda-most-mature-candidate
- **What**: Of the lazy languages, Miranda was the most mature (pure, well designed, robustly implemented, widely deployed), making it the natural starting-point candidate.
- **Quote**: "David Turner’s Miranda was by far the most mature. It was pure, well designed, fulfilled many of our goals" (line 209)

### turner-declined-goals-differed
- **What**: Turner declined to let Miranda be the basis: the committee wanted freedom for anyone to extend, modify and distribute the language, while Turner was committed to a single portable standard with no dialects.
- **Quote**: "we sought the freedom for anyone to extend or modify the language, and to build and distribute an implementation. Turner, by contrast, was strongly committed to maintaining a single language standard" (line 217)
- **Open**: whether a shared standard or open extensibility was the better path was left as a genuine difference in goals, not resolved.

### fork-freedom-enabled-type-classes
- **What**: Not starting from Miranda forced a full new design but allowed more radical approaches; type classes would likely not have been developed from a Miranda base.
- **Quote**: "it allowed us the freedom to contemplate more radical approaches to many aspects of the language design. For example, if we had started from Miranda it seems unlikely that we would have developed type classes" (line 225)

### debt-to-miranda
- **What**: Despite the fork, Haskell owes Miranda a considerable debt, in general inspiration and in specific elements freely adopted where they fit.
- **Quote**: "Haskell owes a considerable debt to Miranda, both for general inspiration and specific language elements that we freely adopted" (line 227)

### conservative-consensus-intent
- **What**: The committee intended a conservative language that embodied the current consensus of ideas and united the disparate groups, rather than breaking new ground.
- **Quote**: "we intended the language to be quite conservative, rather than to break new ground" (line 240)
- **Also at**: lines 243-244

### goals-not-realised
- **What**: Several initial goals were not met: the OL basis was abandoned early, the well-tried-ideas goal was violated (notably by type classes), and no formal semantics was ever developed.
- **Quote**: "We abandoned the idea of basing Haskell explicitly on OL very early; we violated the goal of embodying only well-tried ideas, notably by the inclusion of type classes; and we never developed a formal semantics." (line 245)

### ol-as-default-solution
- **What**: The committee process used OL's design as the described default, to be kept for any topic lacking a clearly better solution.
- **Quote**: "OL will be the default if no clearly better solution exists." (line 256)
- **Also at**: line 255

### moment-of-naming
- **What**: The authors treat the moment a language is named as a small but important moment in its evolution.
- **Quote**: "a small but important moment in any language’s evolution is the moment it is named" (line 268)

### public-vs-private-governance
- **What**: Discomfort with the "us-and-them" of having both public and private mailing lists led debate to move fully public, though decisions were still made by the committee.
- **Quote**: "Members of the committee became increasingly uncomfortable with the “us-and-them” overtones of having both public and private mailing lists" (line 330)
- **Also at**: lines 333-334

### library-report-for-portability
- **What**: Haskell 1.3 added a Library Report, recognising that programs can hardly be portable without standard libraries to rely on.
- **Quote**: "A Library Report was added, reflecting the fact that pro-" (line 353)
- **Also at**: lines 354-355

### monadic-io-and-do
- **What**: Haskell 1.3 introduced monadic I/O with "do" syntax, dropping the earlier I/O semantics in the Appendix.
- **Quote**: "Monadic I/O made its first appearance, including “do” syn-" (line 356)
- **Also at**: lines 358-359

### constructor-classes
- **What**: Type classes were generalised to higher kinds, giving constructor classes.
- **Quote**: "Type classes were generalised to higher kinds—so-called “constructor classes”" (line 360)

### adt-extensions
- **What**: Algebraic data types were extended with newtypes, strictness annotations, and named fields.
- **Quote**: "Algebraic data types were extended in several ways: new-" (line 363)
- **Also at**: lines 364-365

### list-comprehensions-over-monads-reversed
- **What**: Haskell 1.4 generalised list comprehensions to arbitrary monads, a decision reversed two years later (reverted to just lists in Haskell 98).
- **Quote**: "list comprehensions were generalised to arbitrary monads, a decision that was reversed two years later." (line 369)
- **Also at**: line 374

### haskell98-commitment-to-stability
- **What**: The Haskell 98 Report represented a deliberate commitment to stability.
- **Quote**: "this was a very significant moment because it represented a commitment to stability." (line 372)

### open-participation-benign-dictator
- **What**: After the committee ceased, decisions were no longer limited to a small group; anyone on the mailing list could participate, with Peyton Jones as editor of linguistic minutiae.
- **Quote**: "Decisions were no longer limited to a small committee; now anyone reading the Haskell mailing list could participate." (line 377)
- **Also at**: lines 383-384

### free-online-text-defuses-ip-debate
- **What**: Publishing the Report as a book while keeping the full text freely available online defused a tricky debate about freedom and intellectual property.
- **Quote**: "the entire text could still be available online and be freely usable in that form by anyone" (line 388)
- **Also at**: line 390

### language-design-is-slow
- **What**: The four years taken to shake down Haskell 98 illustrate that language design is a slow process.
- **Quote**: "Language design is a slow process!" (line 394)

### haskell-features-in-csharp-and-linq
- **What**: Features of C# were pioneered by Haskell and other functional languages, with LINQ directly inspired by Haskell's monad comprehensions (reported via Erik Meijer).
- **Quote**: "many of the features in C# were pioneered by Haskell and other functional languages, notably polymorphic types and LINQ" (line 471)
- **Also at**: lines 473-474
