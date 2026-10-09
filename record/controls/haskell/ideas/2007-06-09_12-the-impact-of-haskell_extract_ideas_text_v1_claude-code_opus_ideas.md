---
note: 12_the-impact-of-haskell.md
note_dir: texts
note_sha256: 1332110abe6fd37d66ecb7888bcd133da0eed0f3909c320d1b3f46de92273920
title: "12. The impact of Haskell"
author: Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler
created: 2007-06-09T00:00:00
ideas: 26
quotes_found: 10/26
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Haskell; designers=Paul Hudak, John Hughes, Simon Peyton Jones and Philip Wadler
agent: claude-code
model: opus
effort: low
---

## Ideas

### teaching-as-explicit-design-goal
- **What**: Suitability for teaching was one of the stated goals the designers set for Haskell.
- **Quote**: "One of the explicit goals of Haskell’s designers was to create a language suitable for teaching." (line 9)
- **Also at**: lines 492-493 ("our goals of designing a language suitable for teaching and research have certainly been fulfilled")

### mathematical-look-and-feel
- **What**: Haskell has a mathematical look and feel that makes it a medium for teaching discrete mathematics and logic.
- **Quote**: "exploiting Haskell’s mathematical look and feel" (line 39)
- **Also at**: lines 90-91 ("symbolic computation and its mathematical flavour")

### types-and-recursion-early
- **What**: Teaching reports that Haskell drives fundamental concepts like types and recursion home early, and lets students tackle more ambitious problems sooner than in a language like Java.
- **Quote**: "Fundamental concepts such as types and recursion are ham- mered home early." (line 127)
- **Also at**: lines 130-132

### recursion-vs-simple-loops
- **What**: Expressing simple loop programs through recursion can be harder for students to grasp (a cost of the functional style).
- **Quote**: "Simple loop programs can be harder for students to grasp when ... expressed using recursion." (line 133)

### class-system-error-messages
- **What**: The class system causes minor irritations, sometimes producing puzzling error messages.
- **Quote**: "The class system causes minor irritations, sometimes leading to ... puzzling error messages for students." (line 136)
- **Also at**: lines 152-153 (Helium drops classes to give clearer errors), line 320

### in-place-update-messier
- **What**: Array processing and algorithms relying on in-place update are messier in Haskell than in imperative languages.
- **Quote**: "Array processing and algorithms using in-place update are ... messier in Haskell." (line 139)

### io-and-the-awkward-squad
- **What**: Haskell's input/output, and the issues of the "awkward squad," are poorly covered by textbooks that present only the purely functional aspects.
- **Quote**: "Haskell input/output is not well covered by current textbooks" (line 142)
- **Also at**: lines 144-149

### helium-drops-classes-tradeoff
- **What**: Helium, a simplified Haskell for teaching, omits classes to give clearer error messages, at the cost of textbooks and the ability to "tackle the awkward squad" (a deliberate trade-off).
- **Quote**: "Helium lacks classes, which enables it to give clearer error messages, but then it also lacks textbooks and the ability to “tackle the awkward squad.”" (lines 152-154)
- **Open**: whether the trade-off succeeds is left undecided ("It remains to be seen how successful it will be")

### abstraction-and-non-interference
- **What**: The abstraction and non-interference properties of functional languages make compilers and code translation natural applications, giving high productivity even with minimal project management.
- **Quote**: "the abstraction and non-interference properties of functional languages meant that productivity was very high, even with minimal project management overhead" (line 261)

### referential-transparency-executable-mathematics
- **What**: Because of referential transparency, Haskell programs can be read as executable mathematics, equations over the category of complete partial orders, so that in principle the specification becomes the program.
- **Quote**: "Because of referential transparency, Haskell programs can be viewed as executable mathematics, as equations over the category of complete partial orders. In principle, at least, the specification becomes the program." (lines 268-269)

### types-of-numeric-kind
- **What**: Reporting Bluespec, the authors note Haskell's type system was extended with types of numeric kind, so the class system can do (limited, statically checked) arithmetic on them, giving accurate types to things like bit vectors rather than using lists whose sizes the type checker cannot check.
- **Quote**: "The type system has been extended with types of numeric kind. ... Their purpose is to give accurate types to things like bit vectors (instead of using lists where the sizes cannot be checked by the type checker)." (lines 288-292)

### haskell-as-two-level-compile-time-language
- **What**: Reporting Bluespec, the full power of Haskell is available at compile time and eliminated by a partial evaluator, making it "a two-level language."
- **Quote**: "Bluespec is really a two-level language. The full power of Haskell is available at compile time, but almost all Haskell language constructs are eliminated by a partial evaluator" (lines 295-296)

### rich-static-type-system-as-reason-to-choose
- **What**: Aetion chose Haskell for its rich static type system, open-source compilers, and active research community; static typing is reported to catch many errors that would otherwise surface in the field.
- **Quote**: "They chose Haskell, because of its rich static type system, open-source compilers, and its active research community." (lines 302-303)
- **Also at**: lines 343-345

### high-level-concentrate-on-problem
- **What**: As a very high-level language Haskell lets programmers write succinct but readable code and concentrate on the problem without boilerplate and housekeeping.
- **Quote**: "they can concentrate on the problem at hand without being distracted by all the attendant programming boilerplate and housekeeping" (lines 310-312)

### strict-and-lazy-evaluation-difficulty
- **What**: A main difficulty is constructing software that uses both strict and lazy evaluation well (an efficiency/evaluation-model tension).
- **Quote**: "how to construct software that uses both strict and lazy evaluation well" (lines 318-319)

### uniformity-vs-perl-compactness
- **What**: Reporting Linspire, Haskell has comparable versatility to shell/script languages but promotes much greater uniformity; its idioms for systems programming are not quite as compact as Perl's, an acknowledged lack offset by other benefits and an active research area.
- **Quote**: "Haskell has comparable versatility but promotes much greater uniformity." (line 335)
- **Also at**: lines 339-342

### separate-data-types-for-legacy-formats
- **What**: Explicitly segregating legacy data formats into separate data types prevented the mysterious errors that propagate through shell programs when a format changes.
- **Quote**: "Explicitly segregating these formats into separate data types prevented the mysterious errors that always seem to propagate through shell programs when the format changes." (lines 398-400)

### minimal-surfaces
- **What**: An analogy for Haskell solutions: the language, libraries and culture lead to solutions that feel like minimal surfaces, simple expressions comprising significant complexity with natural, recurring forms.
- **Quote**: "solutions that feel like minimal surfaces: simple expressions that comprise significant complexity, with forms that seem natural, recurring in problem after problem" (lines 408-411)

### haskell98-stability-step
- **What**: The authors read Haskell 98 as the step from a frequently changing research vehicle to a language with a guarantee of long-term stability, tentatively linking it to the community's stronger growth.
- **Quote**: "the year that Haskell took the step from a frequently changing vehicle for research to a language with a guarantee of long-term stability" (lines 468-469)
- **Open**: whether stability caused the growth is left tentative ("It is tempting to conclude that this is cause and effect")

### uniqueness-types-as-io-alternative
- **What**: Reporting Clean, the authors note it adopted type classes from Haskell but used uniqueness (linear) types for input-output instead of monads, presenting an alternative to Haskell's monadic I/O.
- **Quote**: "instead of using monads for input-output it uses an approach based on uniqueness (or linear) types" (lines 536-537)

### type-classes-with-laws
- **What**: Reporting Isabelle, declaring a type class can carry the laws its operations obey (e.g. a ring), and declaring an instance requires proving the instance satisfies them.
- **Quote**: "When a type class is declared one associates with it the laws obeyed by the operations in a class ... and when an instance is declared one must prove that the instance satisfies those properties" (lines 555-559)

### type-classes-as-influence
- **What**: The authors treat type classes as a Haskell contribution picked up elsewhere: Java 5's bounded generic types (on Hindley-Milner) are closely related to them, as are Scala's view bounds and implicit parameters.
- **Quote**: "The use of bounded types in that system is closely related to type classes in Haskell." (lines 567-568)
- **Also at**: lines 540 (Mercury), 574-576 (Scala)

### comprehensions-and-monad-comprehensions-as-influence
- **What**: The authors trace list comprehensions (adopted by Python, then Javascript) and monad comprehensions (basis of LINQ in C#/Visual Basic, and Scala's for-comprehensions) as features of Haskell carried into other languages.
- **Quote**: "The LINQ (Language INtegrated Query) features of C# 3.0 and Visual Basic 9.0 are based on monad comprehensions from Haskell." (line 570)
- **Also at**: lines 561-564, 573-575

### legacy-is-influence-on-successors
- **What**: The authors' wish/belief that Haskell's most important legacy will be its influence on the languages that succeed it.
- **Quote**: "We believe the most important legacy of Haskell will be how it influences the languages that succeed it." (lines 577-578)

### extensions-vs-standard
- **What**: So many extensions have appeared since Haskell 98 that few real programs adhere to the standard, which the authors frame as a problem for users (naming their language), tool builders (which extensions to support), and teachers (which to teach), motivating a new "Industrial Haskell" standard.
- **Quote**: "So many extensions have appeared since the latter was defined that few real programs adhere to the standard nowadays." (lines 582-583)
- **Also at**: lines 584-590

### rewrite-rules-for-performance
- **What**: Data.ByteString represents strings as byte vectors and uses GHC's rewrite rules to program the optimiser so loop fusion happens when bytestring functions compose; the correctness of the rules (and agreement with String operations) is tested by QuickCheck, held up as using advanced features for performance and reliability without compromising elegance.
- **Quote**: "by using GHC’s rewrite rules to program the compiler’s optimiser, so that loop fusion is performed when bytestring functions are composed" (lines 606-608)
- **Also at**: lines 609-612
