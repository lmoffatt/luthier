---
note: 09_implementations.md
note_dir: texts
note_sha256: 5fd0fe486c114e5dc145cd0c48ecfa0015bcc45da12228e7fa8f4de99db6fe3c
title: "9. Implementations"
author: Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler
created: 2007-06-09T00:00:00
ideas: 41
quotes_found: 41/41
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Haskell; designers=Paul Hudak, John Hughes, Simon Peyton Jones and Philip Wadler
agent: claude-code
model: opus
effort: low
---

## Ideas

### modules-are-not-a-unit-of-distribution
- **What**: Modules work as a unit of program construction but not of distribution; developers want to ship a related group of modules as a package with its documentation, licensing, dependencies and build information, and none of this was in the language design.
- **Quote**: "Modules form a reasonable unit of program construction, but not of distribution. Developers want to distribute a related group of modules as a “package,” ... None of this was part of the Haskell language design." (line 5)

### cabal-and-hackage-for-packaging
- **What**: Cabal, led by Isaac Jones from 2004, specifies and implements a system for constructing and distributing Haskell packages; Hackage, implemented by David Himmelstrup, is a Cabal package server for finding and downloading packages.
- **Quote**: "Isaac Jones took up the challenge of leading an effort to specify and implement a system called Cabal that supports the construction and distribution of Haskell packages" (line 11)
- **Also at**: lines 14-15

### distribution-took-fifteen-years
- **What**: It took more than fifteen years for Haskell to gain enough momentum for distribution and discovery mechanisms to become important.
- **Quote**: "it has taken more than fifteen years for Haskell to gain enough momentum that these distribution and discovery mechanisms have become important." (line 17)

### module-system-of-modesty
- **What**: Haskell's module system is distinguished by its modesty, doing about as little as a language can and still be a practical tool; perhaps a good choice, since it avoids the technically complicated area that ML modules occupy.
- **Quote**: "a module system distinguished by its modesty. It does about as little as it is possible for a language to do and still call itself a practical programming tool. Perhaps this was a good choice; it certainly avoids a technically complicated area" (line 22)
- **Open**: whether the modesty was a good choice is left as "Perhaps".

### libraries-grew-into-a-separate-report
- **What**: The importance of well-specified and well-implemented libraries became apparent early; the Standard Prelude began as an appendix, but by Haskell 1.3 the volume of library code warranted a separate companion Library Report.
- **Quote**: "the volume of standard library code had grown to the extent that it was given a separate companion Library Report, alongside the language definition." (line 30)

### haskell-98-libraries-still-modest
- **What**: The Haskell 98 libraries were still fairly modest, 100 of 240 report pages, but real applications need much richer libraries, which drove an informal library evolution mechanism.
- **Quote**: "The libraries defined as part of Haskell 98 were still fairly modest in scope. ... But real applications need much richer libraries, and an informal library evolution mechanism began" (line 33)

### cross-implementation-common-libraries
- **What**: Driven by user desire for cross-implementation compatibility, the Hugs, GHC and nhc teams began in 2001 to work on a common open-source set of libraries shipped with each compiler.
- **Quote**: "driven by user desire for cross-implementation compatibility, the Hugs, GHC and nhc teams began in 2001 to work together on a common, open-source set of libraries that could be shipped with each of their compilers" (line 39)

### haskell-is-a-big-language-to-implement
- **What**: Haskell is a big language and quite a lot of work to implement, yet several implementations exist.
- **Quote**: "Haskell is a big language, and it is quite a lot of work to implement. Nevertheless, several implementations are available" (line 48)

### ghc-origins-as-lml-front-end
- **What**: GHC began in January 1989 at Glasgow as soon as the language design was fixed; the first version, written in LML by Kevin Hammond, was essentially a new front end to the Chalmers LML compiler.
- **Quote**: "The first version of GHC was written in LML by Kevin Hammond, and was essentially a new front end to the Chalmers LML compiler." (line 56)

### prototype-implemented-all-of-haskell-1-0
- **What**: The prototype implemented essentially all of Haskell 1.0 including views (later removed), type classes, the deriving mechanism, the full module system, binary I/O, and both streams and continuations.
- **Quote**: "The prototype compiler implemented essentially all of Haskell 1.0 including views (later removed), type classes, the deriving mechanism, the full module system, and binary I/O as well as both streams and continuations." (line 59)

### type-classes-cost-size-and-speed
- **What**: Type classes added complexity that made the compiler bigger and slower than the base LML compiler, and the larger Haskell prelude stressed the LML prelude mechanism; experience with this compiler partly led the Committee to introduce the monomorphism restriction, remove views, and make other changes.
- **Quote**: "the added complexity of type classes meant the compiler was quite a lot bigger and slower than the base LML compiler." (line 62)
- **Also at**: lines 67-68

### ghc-complete-implementation-in-haskell
- **What**: GHC proper, begun autumn 1989, was designed from the ground up as a complete implementation of Haskell in Haskell, bootstrapped via the prototype; only the parser (Yacc and C) was shared.
- **Quote**: "It was designed from the ground up as a complete implementation of Haskell in Haskell, bootstrapped via the prototype compiler." (line 70)

### ghc-early-extensions
- **What**: GHC's first full release already supported extensions beyond Haskell: monadic I/O (official only in 1996), mutable arrays, unboxed data types, and a novel space/time profiling system.
- **Quote**: "This version of GHC already supported several extensions to Haskell: monadic I/O ..., mutable arrays, unboxed data types ..., and a novel system for space and time profiling" (line 76)

### large-front-end-data-type-for-good-errors
- **What**: GHC uses a very large front-end data type reflecting Haskell's full syntax, performing error-generating processing on it, in contrast to the popular method of removing syntactic sugar first; this cost much broad code but let error messages report exactly what the programmer wrote.
- **Quote**: "GHC uses a very large data type in its front end that accurately reflects the full glory of Haskell’s syntax. ... but has the huge advantage that the error messages could report exactly what the programmer wrote." (line 80)

### core-intermediate-language
- **What**: After type checking the program is desugared into a small explicitly typed intermediate language called Core, then processed by a long sequence of Core-to-Core analyses and optimising transformations before STG and C/machine code.
- **Quote**: "the program is desugared into an explicitly typed intermediate language called simply “Core” and then processed by a long sequence of Core-to-Core analyses and optimising transformations." (line 90)
- **Also at**: lines 100-101

### core-based-on-system-f
- **What**: Core was initially based on the lambda calculus; in 1992 they realised Girard's System F ω was a ready-made basis for decorating it with types, needing only to add data types, let- and case-expressions. GHC appears to be the first compiler to use System F as a typed intermediate language.
- **Quote**: "we realised in 1992 that a ready-made basis lay to hand, namely Girard’s System F ω ...; all we needed to do was to add data types, let-expressions, and case expressions. GHC appears to be the first compiler to use System F as a typed intermediate language" (line 104)

### underestimating-typed-intermediate-language
- **What**: They thought the System F idea too simple to publish and only noted it in a small section; the same idea was used independently in the TIL compiler, whose authors understood its significance better, and type-directed compilation became very influential.
- **Quote**: "at the time we thought it was such a simple idea that we did not think it worth publishing ... They understood its significance much better than the GHC team, and the whole approach of type-directed compilation subsequently became extremely influential." (line 108)

### core-lint-consistency-check
- **What**: A "Core Lint" typechecker checks each pass's output stays well-typed; this provides a surprisingly strong consistency check since most optimiser bugs produce type-incorrect code, catching bugs far more cheaply than running incorrect code. It turned out to be one of the biggest benefits of a typed intermediate language, though recognising this took a long time.
- **Quote**: "This consistency checking turned out to be one of the biggest benefits of a typed intermediate language, although it took us a remarkably long time to recognise this fact." (line 130)

### ghc-grew-complex
- **What**: Over fifteen years GHC grew a huge number of features (dozens of extensions, GHCi, concurrency, transactional memory, Template Haskell, packages), making it a dauntingly complex beast to understand and modify.
- **Quote**: "This makes GHC a dauntingly complex beast to understand and modify" (line 136)

### hbc-written-out-of-impatience
- **What**: Augustsson reports he and Truvé decided to write their own Haskell compiler based on LML rather than wait longer for the Glasgow compiler; he had a mostly complete implementation of Haskell by late August 1990.
- **Quote**: "we would write our own Haskell compiler based on the LML compiler." (line 149)
- **Also at**: lines 152-153

### hbc-type-checking-hard
- **What**: Augustsson reports that in hbc the two problematic areas were modules (renaming import/export with many validity conditions) and especially type checking, which was hard because it predated good papers on how it should be done.
- **Quote**: "the big stumbling block was the type checking. It was hard to do. This was way before there were any good papers about how it was supposed to be done." (line 163)

### hbc-doomed-by-lml
- **What**: Augustsson reports hbc became a test bed for extensions and lived actively for over five years, but being written in LML it was more or less doomed to dwindle.
- **Quote**: "since the compiler was written in LML it was more or less doomed to dwindle." (line 168)

### gofer-interpreter-small-footprint
- **What**: In contrast to the memory-hungry compilers, Mark Jones released Gofer in 1991, an interpreter in C developed on an 8086 PC with 640KB, small enough to fit on a single 360KB floppy, written to learn about implementing functional languages.
- **Quote**: "Gofer was an interpreter, implemented in C, developed on an 8MHz 8086 PC with 640KB of memory, and small enough to fit on a single (360KB) floppy disk." (line 174)

### gofer-first-multi-parameter-type-classes
- **What**: Gofer included the first implementation of multi-parameter type classes, as originally suggested by Wadler and Blott and a regular topic on the Haskell mailing list.
- **Quote**: "Gofer included the first implementation of multi-parameter type classes, as originally suggested by Wadler and Blott" (line 181)

### gofer-dictionary-passing-variant
- **What**: Gofer adopted a variant of Wadler and Blott's dictionary-passing translation designed to minimise dictionary construction at run time, work with multi-parameter type classes, and give more accurate principal types; this caused small but significant differences between the Haskell and Gofer type systems, so some programs would not port either way.
- **Quote**: "an interesting variant of Wadler and Blott’s dictionary-passing translation ... designed to minimise the construction of dictionaries at run time, to work with multiple parameter type classes, and to provide more accurate principal types." (line 184)
- **Also at**: lines 187-190

### gofer-do-notation-and-constructor-classes
- **What**: Jones added constructor classes and produced the first implementation of the do-notation in Gofer; both features were subsequently adopted in Haskell 98. He also built a Gofer-to-C compiler and the first "dictionary-free" implementation of type classes using partial evaluation.
- **Quote**: "adding support for constructor classes ... in 1992–93 and producing the first implementation of the do-notation in 1994. Both of these features were subsequently adopted in Haskell 98." (line 191)
- **Also at**: lines 193-196

### gofer-to-hugs
- **What**: Jones rewrote the Gofer code base to track the Haskell standard, briefly called "Hg" then "Hugs"; the first release (February 1995) supported almost all Haskell 1.2 features, its most prominent missing feature being the module system, which Hugs 1.0 parsed but ignored.
- **Quote**: "The most prominent missing feature was the Haskell module system; Hugs 1.0 would parse but otherwise ignore module headers and import declarations." (line 213)

### parallel-hugs-development-and-merge
- **What**: Reid at Yale added module-system support while Jones independently developed Hugs 1.3 with Haskell 1.3 features; the parallel versions were confusing for users and developers, finally merged in Hugs 98 (March 1999), the first version to support Haskell 98.
- **Quote**: "This problem was finally addressed with the release of Hugs 98 in March 1999, which merged the features of the previous Yale and Nottingham releases into a single system." (line 241)

### hugs-experimental-type-features
- **What**: Jones overhauled the Hugs type checker with experimental support for advanced type system features (rank-2 polymorphism, polymorphic recursion, scoped type variables, existentials, extensible records) and restored multi-parameter type classes; these were too experimental for Hugs 1.4 and released separately as Hugs 1.3c.
- **Quote**: "experimental support for advanced type system features including rank-2 polymorphism, polymorphic recursion, scoped type variables, existentials, and extensible records" (line 232)

### standardisation-stabilised-hugs
- **What**: Hugs development slowed after Hugs 98, benefiting from the stability provided by the standardisation of Haskell 98, while still adding features such as implicit parameters, functional dependencies, .NET support, and hierarchical module names.
- **Quote**: "benefiting in part from the stability provided by the standardisation of Haskell 98." (line 249)

### nhc-space-efficiency-goal
- **What**: Röjemo's motivation for nhc from the start was a space-efficient compiler that could be bootstrapped in much smaller memory than hbc and GHC, specifically on his ~2Mbyte machine.
- **Quote**: "His motivation from the start was to have a space-efficient compiler ... that could be bootstrapped in a much smaller memory space than required by systems such as hbc and GHC." (line 261)

### nhc-heap-profiling-link
- **What**: nhc's development used first-generation heap-profiling tools from York (developed to reveal space-leaks in hbc); this link brought Röjemo to York, where more advanced heap-profiling methods found residual space-inefficiencies and led to a still more space-efficient nhc.
- **Quote**: "he made use during development of the first-generation heap-profiling tools—which had previously been developed at York and used to reveal space-leaks in hbc" (line 267)

### yale-haskell-via-scheme-techniques
- **What**: Building on prior Yale work on Scheme and the T dialect (and the Orbit compiler), Hudak applied Scheme compilation techniques to Haskell by compiling Haskell into Scheme or T and using a Scheme compiler as a back end, rather than a stand-alone compiler; T was abandoned for Common Lisp over performance and portability, yielding Yale Haskell.
- **Quote**: "rather than port the ideas to a stand-alone Haskell compiler, it seemed easier to compile Haskell into Scheme or T, and then use a Scheme compiler as a back end." (line 291)

### yale-haskell-strictness-for-performance
- **What**: Yale Haskell used strictness analysis and type information to compile the strict part of Haskell into very efficient Lisp code, with a dual-entry-point approach for efficient first-order calls and aggressive in-lining, plus optimisations to reduce lazy-evaluation overhead.
- **Quote**: "Yale Haskell used strictness analysis and type information to compile the strict part of Haskell into very efficient Lisp code." (line 300)

### yale-haskell-programming-environment
- **What**: The underlying Lisp system let the Yale effort focus on the programming environment; Yale Haskell was the first implementation to support both compiled and interpreted code in the same program, with an emacs-based environment of two-keystroke commands and queued commands.
- **Quote**: "Yale Haskell was the first implementation to support both compiled and interpreted code in the same program" (line 312)

### yale-haskell-scratch-pad
- **What**: Yale Haskell offered a "scratch pad", a logical extension of a module where additional function and value definitions could be added without recompiling the module.
- **Quote**: "A scratch pad was a logical extension of a module in which additional function and value definitions could be added, but whose evaluation did not result in recompilation of the module." (line 319)

### yale-haskell-as-extension-testbed
- **What**: Yale Haskell supported many language extensions (monads, dynamic types, polymorphic recursion, strictness annotations, inlining pragmas, specialising overloaded functions, mutually recursive modules, a flexible foreign function interface), serving as a test bed for new ideas.
- **Quote**: "thus served as an excellent test bed for new ideas. These extensions included monads, dynamic types, polymorphic recursion, strictness annotations, inlining pragmas" (line 322)

### common-lisp-backend-limits
- **What**: The Common Lisp back end ultimately limited Yale Haskell: performance in strict code was comparable but lazy code ran 3 to 5 times slower, because Lisp's imperative nature prevented Haskell-specific optimisations (reusing thunk storage, avoiding the extra indirection of a Lisp cons cell per thunk); with no hope of speedup without replacing the back end and no funding, it was abandoned circa 1995.
- **Quote**: "there was a factor of 3 to 5 in lazy code that could not be overcome due to the limitations of the Lisp back end." (line 336)
- **Also at**: lines 329-334

### jhc-whole-program-no-dictionaries
- **What**: jhc, by John Meacham, focuses on aggressive optimisation via whole-program analysis; this whole-program approach allows a completely different way of implementing type classes without dictionary-passing, using flow analysis to support a defunctionalised representation of thunks.
- **Quote**: "This whole-program approach allows a completely different approach to implementing type classes, without using dictionary-passing." (line 344)

### helium-for-teaching-and-error-messages
- **What**: The Helium compiler at Utrecht focuses especially on teaching and on giving high-quality type error messages.
- **Quote**: "The Helium compiler, based at Utrecht, is focused especially on teaching, and on giving high-quality type error messages" (line 341)

### environments-long-neglected
- **What**: Until recently, with the exception of Yale Haskell, Haskell implementers paid little attention to the programming environment, though that is beginning to change (Haskell Refactorer, Visual Haskell, EclipseFP).
- **Quote**: "Until recently, with the notable exception of Yale Haskell, little attention has been paid by Haskell implementers to the programming environment." (line 350)
