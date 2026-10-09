---
note: 10_profiling-and-debugging.md
note_dir: texts
note_sha256: 5670b89adc08a187a8c72b12533d837dccfaa18d8dd6c58e5ee038995c1a2c72
title: "10. Profiling and debugging"
author: Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler
created: 2007-06-09T00:00:00
ideas: 43
quotes_found: 41/43
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Haskell; designers=Paul Hudak, John Hughes, Simon Peyton Jones and Philip Wadler
agent: claude-code
model: opus
effort: low
---

## Ideas

### lazy-evaluation-hides-operational-aspects
- **What**: A disadvantage of lazy evaluation is that operational aspects like evaluation order or memory contents are not predictable from the source and vary between runs, so conventional profiling and debugging are hard to apply.
- **Quote**: "One of the disadvantages of lazy evaluation is that operational aspects such as evaluation order, or the contents of a snapshot of memory at any particular time, are not easily predictable from the source code" (line 3)
- **Also at**: lines 8, 258

### profiling-debugging-took-research
- **What**: Developing successful profiling and debugging tools for Haskell took considerable research, beginning in the early 1990s.
- **Quote**: "Developing successful profiling and debugging tools for Haskell has taken considerable research, beginning in the early 1990s." (line 12)

### ph-eager-haskell-syntax
- **What**: pH adopted Haskell's syntax and type system while keeping Id's eager, parallel evaluation order, I-structures and M-structures, inspired by the MIT dataflow project.
- **Quote**: "In 1993 Arvind and his colleagues decided to adopt Haskell's syntax and type system, while retaining Id's eager, parallel evaluation order, I-structures, and M-structures." (line 20)

### eager-haskell-non-strict-semantics
- **What**: Evaluating Haskell eagerly rather than lazily while retaining non-strict semantics, on a uniprocessor, was explored by Eager Haskell and optimistic evaluation.
- **Quote**: "The idea of evaluating Haskell eagerly rather than lazily (while retaining non-strict semantics), but on a uniprocessor, was also explored by Maessen's Eager Haskell" (line 22)

### haskell-dauntingly-large
- **What**: Haskell had come to seem such a dauntingly large language that no further implementations were expected, yet several new projects started in the last five years.
- **Quote**: "it had begun to seem that Haskell was such a dauntingly large language that no further implementations would emerge." (line 28)

### cost-assignment-for-higher-order-functions
- **What**: The conventional approach of assigning costs to functions works poorly for higher-order functions like map, which Haskell provides many of; knowing map's total share is less useful than knowing which occurrence of it dominates.
- **Quote**: "The conventional approach, of assigning costs to functions and procedures, works poorly for higher-order functions such as map." (line 34)
- **Also at**: lines 42, 45

### cost-centres
- **What**: Sansom and Peyton Jones's new idea was to label source code with cost centres, manually or automatically, and aggregate the costs of one logical task into one count.
- **Quote**: "The new idea Sansom and Peyton Jones introduced was to label the source code with cost centres" (line 47)

### cost-centre-assignment-subtle
- **What**: Assigning costs to cost centres raises subtle questions (closest lexical vs dynamic enclosing, first-class functions, order-independence under call-by-need), which drove the development of a formal cost semantics; a prototype ran with GHC before the semantics was published.
- **Quote**: "Assigning costs to explicitly labelled cost centres is much more subtle than it sounds." (line 56)
- **Also at**: lines 69, 71
- **Open**: left as questions in the text whether the cost of evaluating a function should be assigned to the same cost centre as calling it

### profiler-faster-programs
- **What**: The availability of a profiler led rapidly to faster Haskell programs, speeding up GHC itself by a factor of two.
- **Quote**: "the availability of a profiler led rapidly to faster Haskell programs, in particular speeding up GHC itself by a factor of two." (line 73)

### space-leaks-heap-profiling
- **What**: Lazy programs could exhibit astonishingly poor space behaviour (space leaks); Runciman and Wakeling built a heap profiler classifying heap contents by allocating function or constructor, enabling dramatic space improvements.
- **Quote**: "It had been known for some time that lazy programs could sometimes exhibit astonishingly poor space behaviour—so-called space leaks." (line 79)
- **Also at**: lines 84, 89

### laziness-abstracts-object-lifetimes
- **What**: By abstracting from evaluation order, lazy evaluation also abstracts from object lifetimes, which is why it contributes to space leaks: programmers cannot predict which structures live long, and fast allocation makes peak space high.
- **Quote**: "By abstracting away from evaluation order, lazy evaluation also abstracts away from object lifetimes, and that is why lazy evaluation contributes to space leaks." (line 93)

### lag-drag-void-profiling
- **What**: Extending the heap profiler to object lifetimes let it show data not yet needed (lag), never used again (drag), or never used at all (void).
- **Quote**: "The new profiler could show how much of the heap contained data that was not yet needed (lag), would never be used again (drag), or, indeed, was never used at all (void)" (line 101)

### retainer-profiling
- **What**: Retainer profiling could explain why data was not garbage collected by showing which objects pointed at the data of interest.
- **Quote**: "A further extension introduced retainer profiling, which could explain why data was not garbage collected by showing which objects pointed at the data of interest" (line 104)

### seq-and-strictness-annotations
- **What**: Haskell 1.3 introduced seq (evaluates its first argument then returns its second) and strictness annotations in data definitions, giving the programmer control over evaluation order and letting computations move earlier to shorten lifetimes.
- **Quote**: "In 1996, Haskell 1.3 introduced two features that give the programmer better control over evaluation order" (line 117)

### seq-predates-haskell
- **What**: seq and strict data components were already in Miranda for the same reasons, and seq had been used to fix space leaks since the early 1980s.
- **Quote**: "Both seq and strict components of data structures were already present in Miranda for the same reasons" (line 138)

### seq-introduced-for-speed
- **What**: Although seq is now a common way to fix space leaks, it was primarily introduced to improve speed, by helping the strictness analyser deliver better results on nearly-strict functions; strictness annotations addressed poor analysis of data types and let the compiler optimise representations.
- **Quote**: "interestingly, this was not the main reason for introducing it into Haskell. On the contrary, seq was primarily introduced to improve the speed of Haskell programs!" (line 142)

### hughes-seq-for-space-debugging
- **What**: Through working with Runciman on stubborn space leaks in an LML program where a carefully placed seq repeatedly proved critical, Hughes became concerned that Haskell's seq should support space debugging well.
- **Quote**: "Hughes was very concerned that Haskell's version of seq should support space debugging well." (line 162)

### seq-breaks-semantics
- **What**: seq was controversial for its effect on semantics: not definable in the lambda calculus and the only way to distinguish \x -> ⊥ from ⊥, a distinction Fairbairn was set against.
- **Quote**: "adding seq to Haskell was controversial because of its negative effect on semantic properties." (line 164)

### seq-weakens-parametricity
- **What**: seq does not satisfy the parametricity property for its type and so weakens the parametricity of functions that use it, weakening Wadler's free theorems.
- **Quote**: "seq weakens the parametricity property that polymorphic functions enjoy, because seq does not satisfy the parametricity property for its type ∀a,b.a -> b -> b" (line 166)

### parametricity-justifies-deforestation
- **What**: Parametricity was not just a bonus but the justification for short-cut deforestation (the foldr/build rule), which eliminates intermediate lists cheaply and holds only for sufficiently polymorphic g, guaranteed by a rank-2 type for build.
- **Quote**: "parametricity was by this time not just a nice bonus, but the justification for an important compiler optimisation, namely deforestation" (line 174)
- **Also at**: lines 186, 189

### launchbury-vs-hughes
- **What**: seq cast doubt on this use of parametricity; Launchbury argued parametricity was too important to give up, while Hughes wanted seq applicable to any type including type variables, two virtually incompatible goals.
- **Quote**: "Launchbury argued forcefully that parametricity was too important to give up, for this very reason." (line 190)
- **Also at**: line 192

### eval-class-solution
- **What**: Haskell 1.3's solution made seq overloaded via a class Eval with automatically derived instances, recording uses of seq as Eval a => contexts so parametricity restrictions were visible, keeping short-cut deforestation sound while allowing leaks to be fixed at any type.
- **Quote**: "The solution adopted for Haskell 1.3 was to make seq an overloaded function, rather than a polymorphic one" (line 193)
- **Also at**: lines 204, 207

### eval-class-too-heavyweight
- **What**: A TCP/IP stack in Haskell showed the Eval solution's limits: each seq on a type variable changed many explicit type signatures (forced by the monomorphism restriction), making trial-and-error space debugging too heavyweight, which provided ammunition for removing class Eval in Haskell 98.
- **Quote**: "each insertion of a seq became a nightmare, requiring repeated compilations to find affected type signatures and manual correction of each one." (line 218)
- **Also at**: lines 223, 224

### seq-now-polymorphic-unsound-deforestation
- **What**: Today seq is a simple polymorphic function insertable freely, sacrificing parametricity for agility and optimisation; GHC's short-cut deforestation is consequently unsound.
- **Quote**: "We have sacrificed parametricity in the interests of programming agility and (sometimes dramatic) optimisations. GHC still uses short-cut deforestation, but it is unsound" (line 227)
- **Also at**: line 235

### laziness-also-fixes-leaks
- **What**: Making programs stricter is not the only way to fix space leaks; lifetimes can be shortened by moving last use earlier or creating objects later, and Runciman and Wakeling's first optimisation made the program more lazy, beating a fully strict ML translation.
- **Quote**: "making programs stricter is not the only way to fix space leaks in Haskell. Object lifetimes can be shortened by moving their last use earlier—or by creating them later." (line 236)
- **Also at**: lines 240, 246

### space-sensitivity-two-edged
- **What**: Haskell's extreme sensitivity of space use to evaluation order is a two-edged sword: hard to anticipate when writing, but fixable dramatically by tiny changes with good profiling; the designers are a little ashamed reasoning about space is so intractable, yet the language lets programmers defer space optimisation and then supplies powerful tools.
- **Quote**: "The extreme sensitivity of Haskell's space use to evaluation order is a two-edged sword." (line 247)
- **Also at**: lines 253, 254
- **Open**: whether the deferred-and-tooled approach to space is something to be ashamed of ("Maybe this is nothing to be ashamed of, after all.")

### trace-garbled-output
- **What**: Unpredictable evaluation order makes conventional tracing hard: the trace function's printing of its first argument can trigger another call before the first completes, giving garbled output, so better debuggers abstract from evaluation order.
- **Quote**: "it is not at all uncommon for the printing of the first argument to trigger another call of trace before the printing is complete, leading to very garbled output." (line 262)

### algorithmic-debugging
- **What**: In algorithmic debugging the debugger takes the initiative, presenting calls with arguments and results and asking if correct, descending to children until it finds a call with an incorrect result whose children all behaved correctly, reported as the bug's location.
- **Quote**: "an approach in which the debugger, rather than the user, takes the initiative to explore the program's behaviour." (line 272)

### algorithmic-debugging-laziness-problem
- **What**: Algorithmic debugging suits lazy programs since it depends on input-output behaviour, but computing argument and result values early to display them might itself trigger faults or loops that would otherwise not occur.
- **Quote**: "If they were computed early by an algorithmic debugger, in order to display them in questions to the user, then this itself might trigger faults or loops that would otherwise not have been a problem at all!" (line 284)

### post-mortem-debugging
- **What**: Nilsson solved the problem by waiting until execution completes before debugging: it is then known whether each value was required, so needed values can be used in questions and unneeded ones were irrelevant; this post-mortem approach abstracts from evaluation order and is used by all Haskell debuggers since.
- **Quote**: "This 'post mortem' approach abstracts nicely from evaluation order, and has been used by all Haskell debuggers since." (line 291)

### evaluation-dependence-trees
- **What**: Sparud developed a debugger for Haskell by transforming source to collect debugging information while computing the result, and with Nilsson built evaluation dependence trees providing the information for post-mortem algorithmic debugging.
- **Quote**: "developing efficient methods to build 'evaluation dependence trees' (Nilsson and Sparud, 1997), data structures that provided all the necessary information for post-mortem algorithmic debugging." (line 295)

### redex-trails
- **What**: Redex trails are a form of program trace supporting stepping backwards through execution, so programmers can ask why a function was called with given arguments as well as inspect the call.
- **Quote**: "redex trails, another form of program trace which supports stepping backwards through the execution" (line 340)

### one-trace-many-debuggers
- **What**: Runciman realised that with a little generalisation the same trace could support several different kinds of debugging, the origin of the Hat project, which became a separate source-to-source tool usable with any Haskell 98 compiler and supporting many trace browsers.
- **Quote**: "Runciman realised that, with a little generalisation, the same trace could be used to support several different kinds of debugging" (line 351)

### hat-not-mainstream
- **What**: Despite their power the Hat tools have not become a regular part of programming, probably because Haskell as used remains a moving target with frequent extensions, Hat was long restricted to Haskell 98, and its whole-program source-to-source transformation imposes a substantial performance penalty.
- **Quote**: "This is probably because Haskell, as it is used in practice, has remained a moving target: new extensions appear frequently, and so it is hard for a language-aware tool such as Hat to keep up." (line 306)
- **Also at**: lines 313, 372

### hood-observational-debugging
- **What**: HOOD is a lighter post-mortem debugger where users insert observe calls; unlike trace it prints nothing when called, collecting its second argument tagged by the first, printing all values grouped by tag at the end, which also reveals how much of a lazy input was needed.
- **Quote**: "A more lightweight idea was pursued by Andy Gill, who developed HOOD, the Haskell Object Observation Debugger" (line 317)
- **Also at**: lines 322, 335

### hood-observes-functions
- **What**: HOOD can observe function values as a table of observed arguments and results, the same information an algorithmic debugger would use, but it leaves locating the bug to the programmer.
- **Quote**: "HOOD can even observe function values, displaying them as a table of observed arguments and results" (line 346)
- **Also at**: line 349

### quickcheck-specifications-as-tests
- **What**: QuickCheck's idea is to test programs against specifications written as boolean functions that should always return True, invoked on random data, with counter-examples displayed on failure, letting programmers test many cases for the effort of one property.
- **Quote**: "programs can be tested against specifications by formulating specifications as boolean functions that should always return True, and then invoking these functions on random data." (line 367)
- **Also at**: lines 386, 388

### quickcheck-generators
- **What**: To scale beyond toy examples, QuickCheck lets programmers control random generation via an abstract data type of generators that conceptually represent sets of values with a probability distribution, with a library of combinators to define them.
- **Quote**: "QuickCheck supports this via an abstract data type of 'generators,' which conceptually represent sets of values (together with a probability distribution)." (line 396)

### quickcheck-uses-haskell-features
- **What**: QuickCheck exemplifies Haskell's features: a domain-specific language of testable properties, the class system associating a generator with each type and overloading quickCheck, generators as a monad with syntactic sugar; the language profoundly influenced its design.
- **Quote**: "QuickCheck is not only a useful tool, but also a good example of applying some of Haskell's unique features." (line 433)
- **Also at**: lines 439

### quickcheck-succeeds-by-audience
- **What**: QuickCheck may have succeeded partly because of who Haskell programmers are: many would rather write formal specifications than test code, and QuickCheck lets them test by writing specifications.
- **Quote**: "Perhaps QuickCheck has succeeded in part because of who Haskell programmers are" (line 428)

### quickcheck-emulated-elsewhere
- **What**: QuickCheck's design has been emulated in other languages, including Lindig's random C programs finding compiler calling-convention bugs and an Erlang port finding errors in an Ericsson Media Gateway.
- **Quote**: "This design has been emulated in many other languages." (line 441)

### hunit-traditional-testing
- **What**: HUnit, inspired by JUnit, supports more traditional unit testing: it does not generate test cases but provides ways to define them, structure them hierarchically, and run them automatically with a summary.
- **Quote**: "HUnit supports more traditional unit testing: it does not generate test cases, but rather provides ways to define test cases, structure them into a hierarchy, and run tests automatically with a summary of the results." (line 390)

### impact-as-a-goal
- **What**: A language need not have direct real-world impact to matter historically (Algol), but real-world impact was an important goal of the Haskell Committee; Haskell is not mainstream but has fared well in certain niches, with successes attributable to specific language characteristics.
- **Quote**: "impact on the real world was an important goal of the Haskell Committee, so it is worthwhile to consider how well we have achieved this goal." (line 456)
- **Also at**: lines 459, 461
