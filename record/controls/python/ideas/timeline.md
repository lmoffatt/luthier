# Timeline of ideas about Luthier

Written by `scripts/ideas_timeline.py` (ideas_timeline v1) on 2026-10-09, for Luciano and for the tools that read it.
One row per idea as the extractors found it, in time order; the local times are in America/Argentina/Buenos_Aires, a chat turn's
time is its UTC converted. A note extracted both per note and by day gives two rows, each marked, so a
restatement across notes is told from the same note read twice. Nothing here was judged or merged.

Rows: 313 (written 313). Inputs: 27 files, listed at the end with their sha256.

| month | Guido van Rossum | total |
|---|---|---|
| 2009-01 | 28 | 28 |
| 2009-02 | 63 | 63 |
| 2009-03 | 44 | 44 |
| 2009-04 | 34 | 34 |
| 2010-06 | 67 | 67 |
| 2010-08 | 11 | 11 |
| 2011-07 | 7 | 7 |
| 2013-10 | 18 | 18 |
| 2013-11 | 25 | 25 |
| 2018-05 | 16 | 16 |

## Ideas, by day

### 2009-01-13

- **09:17** Guido van Rossum [written: 2009-01-13_introduction-and-overview.md line 49] `written:2009-01-13_introduction-and-overview:bytecode-compiler-and-interpreter`
  Python is typically implemented as a bytecode compiler plus interpreter, with compilation done implicitly as modules load, and several language primitives requiring the compiler to be present at run-time.
  > Python is typically implemented using a combination of a bytecode compiler and interpreter. Compilation is implicitly performed as modules are loaded, and several language primitives require the compiler to be available at run-time.

- **09:17** Guido van Rossum [written: 2009-01-13_introduction-and-overview.md line 20] `written:2009-01-13_introduction-and-overview:dynamic-typing-names-refer-to-objects`
  Python uses dynamic typing: variables are just names referring to objects, need no declaration, can change type mid-program, and all type checking happens at run-time by an interpreter rather than at a separate compile step.
  > In Python, variables are simply names that refer to objects.   Variables do not need to be declared before they are assigned and they can even change type in the middle of a program.

- **09:17** Guido van Rossum [written: 2009-01-13_introduction-and-overview.md line 26] `written:2009-01-13_introduction-and-overview:everything-first-class`
  All objects that can be named in Python are "first class", so functions, classes, methods, modules and other named objects can be passed around, inspected, and placed in data structures at run-time.
  > In Python, all objects that can be named are said to be "first class."

- **09:17** Guido van Rossum [written: 2009-01-13_introduction-and-overview.md line 32] `written:2009-01-13_introduction-and-overview:expressiveness-little-code`
  A major appeal of Python and other dynamic languages is that seemingly complicated tasks can often be expressed with very little code.
  > seemingly complicated tasks can often be expressed with very little code

- **09:17** Guido van Rossum [written: 2009-01-13_introduction-and-overview.md line 28] `written:2009-01-13_introduction-and-overview:extensive-standard-library`
  An extensive, always-evolving standard library of more than 100 modules is named as one of the main reasons for Python's popularity.
  > Python has an extensive standard library, which is one of the main reasons for its popularity.

- **09:17** Guido van Rossum [written: 2009-01-13_introduction-and-overview.md line 24] `written:2009-01-13_introduction-and-overview:for-loops-over-iterables`
  The for statement is high-level, looping over any "iterable" object rather than over a numeric index.
  > a high-level for statement that loops over any "iterable" object

- **09:17** Guido van Rossum [written: 2009-01-13_introduction-and-overview.md line 26] `written:2009-01-13_introduction-and-overview:full-oo-support`
  Python provides full object-oriented programming support, including user-defined classes, inheritance, and run-time binding of methods.
  > Python also has full support for object-oriented programming including user-defined classes, inheritance, and run-time binding of methods.

- **09:17** Guido van Rossum [written: 2009-01-13_introduction-and-overview.md line 22] `written:2009-01-13_introduction-and-overview:immutable-primitive-types`
  Python's primitive built-in types (Booleans, numbers, strings) are immutable: their values are objects that cannot be modified after creation.
  > These are all immutable types, meaning that values are represented by objects that cannot be modified after their creation.

- **09:17** Guido van Rossum [written: 2009-01-13_introduction-and-overview.md line 11] `written:2009-01-13_introduction-and-overview:indentation-for-grouping`
  Python departs from C-like languages by using indentation for statement grouping instead of braces, dispensing with braces and trailing semicolons.
  > instead of using braces for statement grouping, it uses indentation

- **09:17** Guido van Rossum [written: 2009-01-13_introduction-and-overview.md line 49] `written:2009-01-13_introduction-and-overview:multiple-implementations`
  Beyond the C reference implementation, several implementations exist for different platforms and goals (Jython on the JVM, IronPython on .NET, PyPy as a Python-written optimizing compiler, Stackless reducing C-stack reliance to enable co-routines, continuations and microthreads).
  > several other implementations have become popular. Jython is a version that runs on the JVM and has seamless Java integration.

- **09:17** Guido van Rossum [written: 2009-01-13_introduction-and-overview.md line 24] `written:2009-01-13_introduction-and-overview:non-resumable-exceptions`
  Error handling is done through non-resumable exceptions, raised by a raise statement and handled by try/except/finally, with built-in operations throwing exceptions on error conditions.
  > For error handling, Python uses (non-resumable) exceptions.

- **09:17** Guido van Rossum [written: 2009-01-13_introduction-and-overview.md line 4] `written:2009-01-13_introduction-and-overview:python-general-purpose-not-scripting`
  Though often seen as a scripting language, Python is really a general purpose language in the lineage of Lisp or Smalltalk, usable across the whole range from throw-away scripts to large 24x7 web servers.
  > Although it is often viewed as a "scripting" language, it is really a general purpose programming language along the lines of Lisp or Smalltalk

- **09:17** Guido van Rossum [written: 2009-01-13_introduction-and-overview.md line 11] `written:2009-01-13_introduction-and-overview:syntax-borrows-from-c`
  Python's surface syntax deliberately borrows heavily from C: keywords, identifier naming rules, and operator meanings are shared, so the resemblance to C or Pascal is no accident.
  > This is no accident---the syntax of Python borrows heavily from C.

### 2009-01-20

- **15:19** Guido van Rossum [written: 2009-01-20_personal-history-part-1-cwi.md line 6] `written:2009-01-20_personal-history-part-1-cwi:abc-inspiration-amoeba-motivation`
  ABC gave the key inspiration for Python, Amoeba the immediate motivation, and the multimedia group its growth; Python is a direct product of this experience at CWI.
  > ABC gave me the key inspiration for Python, Amoeba the immediate motivation, and the multimedia group fostered its growth

- **15:19** Guido van Rossum [written: 2009-01-20_personal-history-part-1-cwi.md line 8] `written:2009-01-20_personal-history-part-1-cwi:amoeba-primitives-unlike-the-shell`
  The decisive reason the Bourne shell wouldn't do was that Amoeba, as a distributed micro-kernel system with a radically new design, had primitive operations very different and finer-grained than those of the traditional shell.
  > Amoeba’s primitive operations were very different (and finer-grain) than the traditional primitive operations available in the Bourne shell

- **15:19** Guido van Rossum [written: 2009-01-20_personal-history-part-1-cwi.md line 10] `written:2009-01-20_personal-history-part-1-cwi:borrow-from-abc-fix-its-problems`
  The design program for Python was to keep what he liked from ABC while fixing the problems he perceived in it; the first problem he chose to fix was the name.
  > borrow everything I liked from ABC while at the same time fixing all its problems (as I perceived them)

- **15:19** Guido van Rossum [written: 2009-01-20_personal-history-part-1-cwi.md line 8] `written:2009-01-20_personal-history-part-1-cwi:bridge-the-gap-between-c-and-the-shell`
  Python's original motivation was the need for a higher-level language in the Amoeba project, because writing system administration utilities in C took too long and the Bourne shell wouldn't work; the aim was a language to bridge C and the shell.
  > there was a need for a language that would “bridge the gap between C and the shell.”  For a long time, this was Python’s main catchphrase.

- **15:19** Guido van Rossum [written: 2009-01-20_personal-history-part-1-cwi.md line 10] `written:2009-01-20_personal-history-part-1-cwi:design-new-rather-than-port`
  Rather than port an existing language, van Rossum decided to design his own, because there weren't many suitable languages around; Perl 3 was even more tied to Unix than the Bourne shell.
  > I decided to design a language of my own which would borrow everything I liked from ABC while at the same time fixing all its problems (as I perceived them)

- **15:19** Guido van Rossum [written: 2009-01-20_personal-history-part-1-cwi.md line 14] `written:2009-01-20_personal-history-part-1-cwi:name-irreverent-and-in-tradition`
  "Python" was chosen as suitably irreverent for a skunkworks project, catchy and edgy, while still fitting the tradition of naming languages after famous people (Pascal, Ada, Eiffel) and the Amoeba group's habit of naming programs after TV shows.
  > it fit in the tradition of naming languages after famous people, like Pascal, Ada, and Eiffel

- **15:19** Guido van Rossum [written: 2009-01-20_personal-history-part-1-cwi.md line 20] `written:2009-01-20_personal-history-part-1-cwi:open-source-before-the-term`
  Python's first public release (0.9.0) used a license that was an almost verbatim copy of the X11 MIT license, so Python was open source before the term itself was coined.
  > Python was open source before the term was even invented by Eric Raymond and Bruce Perens in late 1997

- **15:19** Guido van Rossum [written: 2009-01-20_personal-history-part-1-cwi.md line 18] `written:2009-01-20_personal-history-part-1-cwi:pgen-first-code-least-changed`
  The first piece of code written for Python's implementation was a simple LL(1) parser generator, "pgen," which is still part of the source distribution and the least changed of all the code.
  > the first piece of code I wrote for Python’s implementation was a simple LL(1) parser generator I called “pgen." ... still part of the Python source distribution and probably the least changed of all the code

- **15:19** Guido van Rossum [written: 2009-01-20_personal-history-part-1-cwi.md line 22] `written:2009-01-20_personal-history-part-1-cwi:releases-driven-by-feedback`
  Immediate feedback and encouragement led him to keep a steady stream of releases, adopting CVS to track changes and share coding responsibilities.
  > There was immediately a lot of feedback and with this encouragement I kept a steady stream of releases coming for the next few years

- **15:19** Guido van Rossum [written: 2009-01-20_personal-history-part-1-cwi.md line 16] `written:2009-01-20_personal-history-part-1-cwi:resisting-the-snake`
  For many years he resisted associating the language with snakes, giving up only when O'Reilly's animal-cover tradition made a snake the cover of the first Python book.
  > For many years I resisted attempts to associate the language with snakes. I finally gave up when O’Reilly wanted to put a snake on the front of their first Python book

- **15:19** Guido van Rossum [written: 2009-01-20_personal-history-part-1-cwi.md line 10] `written:2009-01-20_personal-history-part-1-cwi:syntax-taste-from-algol-pascal-abc`
  His tastes in programming-language syntax, which shaped his dislike of Perl's syntax, were strongly influenced by Algol 60, Pascal, Algol 68, and ABC.
  > my tastes in programming language syntax were strongly influenced by languages like Algol 60, Pascal, Algol 68 ..., and last but not least, ABC

- **15:19** Guido van Rossum [written: 2009-01-20_personal-history-part-1-cwi.md line 14] `written:2009-01-20_personal-history-part-1-cwi:under-analyze-the-name`
  Rather than over-analyzing the naming problem (as the ABC team had with "as simple as ABC"), he deliberately under-analyzed it and picked the first thing that came to mind, Monty Python.
  > rather than over-analyzing the naming problem, I decided to under-analyze it. I picked the first thing that came to mind

### 2009-01-27

- **14:01** Guido van Rossum [written: 2009-01-27_personal-history-part-2-cnri-and-beyond.md line 14] `written:2009-01-27_personal-history-part-2-cnri-and-beyond:ironpython-port-to-dotnet`
  Van Rossum notes a further Python implementation, authored by Jim Hugunin, porting the language to Microsoft's .NET.
  > Jim would also author IronPython, the Python port to Microsoft's .NET

- **14:01** Guido van Rossum [written: 2009-01-27_personal-history-part-2-cnri-and-beyond.md line 14] `written:2009-01-27_personal-history-part-2-cnri-and-beyond:jython-python-in-and-for-java`
  A Python implementation written in and targeting Java, first created by Jim Hugunin, establishing that Python could be realized on a platform other than C.
  > the development of JPython (later shortened to Jython), a Python implementation in and for Java

- **14:01** Guido van Rossum [written: 2009-01-27_personal-history-part-2-cnri-and-beyond.md line 2] `written:2009-01-27_personal-history-part-2-cnri-and-beyond:python-shares-much-with-lisp`
  Van Rossum reports Bob Kahn's observation that Python has much in common with Lisp despite being completely different at the superficial, syntactic level, distinguishing a language's deep structure from its surface syntax.
  > Bob Kahn, was the first to point out to me how much Python has in common with Lisp, despite being completely different at a superficial (syntactic) level

### 2009-02-03

- **10:53** Guido van Rossum [written: 2009-02-03_early-language-design-and-development.md line 4] `written:2009-02-03_early-language-design-and-development:abc-foremost-influence`
  Python's first and foremost influence was ABC, a teaching language designed at CWI by first analyzing the programming task and then iterating with serious user testing; van Rossum's role was implementing the language and its editing environment.
  > Python's first and foremost influence was ABC... It was designed by first doing a task analysis of the programming task and then doing several iterations that included serious user testing.

- **10:53** Guido van Rossum [written: 2009-02-03_early-language-design-and-development.md line 20] `written:2009-02-03_early-language-design-and-development:bignum-long-type`
  Feeling there was still a use case for unbounded exact numbers, he added a bignum type called long, reusing a bignum implementation left from an earlier unfinished attempt to improve ABC.
  > Feeling that there was still an important use case for unbounded exact numbers, I added a bignum data type, which I called long.

- **10:53** Guido van Rossum [written: 2009-02-03_early-language-design-and-development.md line 6] `written:2009-02-03_early-language-design-and-development:colon-before-indented-block`
  ABC's authors invented the colon separating the lead-in clause from the indented block; user testing without it showed the indentation's meaning was unclear to beginners, and the colon clarified it by drawing attention to what follows and tying the phrases together.
  > ABC's authors did invent the use of the colon that separates the lead-in clause from the indented block. After early user testing without the colon, it was discovered that the meaning of the indentation was unclear to beginners... The addition of the colon clarified it significantly

- **10:53** Guido van Rossum [written: 2009-02-03_early-language-design-and-development.md line 14] `written:2009-02-03_early-language-design-and-development:empty-and-one-tuple-notation`
  Adding indexing forced resolving tuples of length 0 and 1; to keep the printed-repr rule yet not lose the distinction between a one-tuple and a parenthesized expression, he used a trailing comma for one-tuples and "()" for the empty tuple, requiring parentheses only there so that representing the empty tuple as nothing would not mask typos.
  > I settled for an ugly but pragmatic approach where a trailing comma would turn an expression into a one-tuple and \"()\" would represent a zero-tuple... I felt representing the empty tuple by \"nothing\" could too easily mask genuine typos.

- **10:53** Guido van Rossum [written: 2009-02-03_early-language-design-and-development.md line 28] `written:2009-02-03_early-language-design-and-development:explicit-long-suffix-violates-philosophy`
  Having two integer types forced a way to distinguish them; requiring a trailing L to mark longs violated the ABC-inspired philosophy of not making users care about uninteresting implementation details.
  > This is one area where Python violated the ABC-inspired philosophy of not requiring users to care about a uninteresting implementation details.

- **10:53** Guido van Rossum [written: 2009-02-03_early-language-design-and-development.md line 10] `written:2009-02-03_early-language-design-and-development:hash-table-over-btree`
  He replaced ABC's sorted tables with a hash table, believing it faster and easier to implement than ABC's asymptotically optimal B-tree, which proved hard to implement correctly and sub-optimal for small sizes.
  > I also replaced the sorted tables with a hash table implementation. I chose a hash table because I believed this to be faster and easier to implement than ABC's B-tree implementation.

- **10:53** Guido van Rossum [written: 2009-02-03_early-language-design-and-development.md line 6] `written:2009-02-03_early-language-design-and-development:indentation-from-abc`
  Python's indentation comes from ABC, though the idea predates ABC (promoted by Knuth, used by occam); it is a well-known concept of programming style.
  > Python's use of indentation comes directly from ABC, but this idea didn't originate with ABC--it had already been promoted by Donald Knuth and was a well-known concept of programming style.

- **10:53** Guido van Rossum [written: 2009-02-03_early-language-design-and-development.md line 30] `written:2009-02-03_early-language-design-and-development:int-long-divergent-semantics`
  A more egregious error was that int and long had slightly different semantics: machine ints silently clipped on overflow and were treated as unsigned by bitwise, shift, and octal/hex conversions, while longs were always signed, so the same operation could differ by representation.
  > A more egregious error was that my implementation of integers and longs had slightly different semantics in certain cases!

- **10:53** Guido van Rossum [written: 2009-02-03_early-language-design-and-development.md line 8] `written:2009-02-03_early-language-design-and-development:list-as-flexible-array`
  ABC's lists were sorted bags unsuitable for representing a sequence of lines read from a file, so van Rossum changed the list into a flexible array with insert and delete operations, giving users complete control over item ordering, with a sort method for occasional sorted results.
  > So I changed the list type into a flexible array with insert and delete operations, giving users complete control over the ordering of items in a list. A sort method supported the occasional need for sorted results.

- **10:53** Guido van Rossum [written: 2009-02-03_early-language-design-and-development.md line 22] `written:2009-02-03_early-language-design-and-development:machine-ints-for-common-case`
  Although he added bignums, he did not want them for all integer operations: profiling showed integer operations are a significant fraction of running time and the most common use is indexing sequences that fit in memory, so machine integers serve the common cases and bignums only "serious math."
  > I didn't want to use bignums for all integer operations... I envisioned machine integers being used for all of the most-common cases and the extra range of bignums only coming into play when doing \"serious math\"

- **10:53** Guido van Rossum [written: 2009-02-03_early-language-design-and-development.md line 18] `written:2009-02-03_early-language-design-and-development:machine-numbers-over-rationals`
  Numbers are where he strayed most from ABC: ABC's exact arbitrary-precision rationals didn't pan out (a tax computation ran on numbers with thousands of digits), so Python chose a traditional model of machine integers and binary floating point, represented by the C types long and double.
  > The rational numbers didn't pan out in my view... For Python I therefore chose a more traditional model with machine integers and machine binary floating point.

- **10:53** Guido van Rossum [written: 2009-02-03_early-language-design-and-development.md line 38] `written:2009-02-03_early-language-design-and-development:no-undefined-values`
  The positive lesson: there should be no undefined result values in Python; an exception is always raised when no correct value can be computed, so programs never fail from silently passed undefined values, a principle still held in the language and standard library.
  > I decided that there should be no undefined result values in Python – instead, exceptions should always be raised when no correct return value can be computed.

- **10:53** Guido van Rossum [written: 2009-02-03_early-language-design-and-development.md line 34] `written:2009-02-03_early-language-design-and-development:overflow-check-cost-dwarfed`
  A painful debugging of "Meertens numbers," whose intermediate results exceeded 32 bits, convinced him to check all integer operations for overflow; the extra cost was dwarfed by the overhead already incurred from allocating a new object for each result.
  > The extra cost of the overflow check would be dwarfed by the overhead I was already incurring due to the implementation choice of allocating a new object for the result.

- **10:53** Guido van Rossum [written: 2009-02-03_early-language-design-and-development.md line 32] `written:2009-02-03_early-language-design-and-development:overflow-raises-exception`
  To resolve this he changed most arithmetic operations to raise OverflowError rather than silently clip (except bitwise operations, where C behavior was expected), reasoning that otherwise users would come to rely on signed modulo-2**32 semantics and fixing it later would be a painful transition.
  > I changed most arithmetic operations to raise an OverflowError exception when the result didn't fit... Had I not added this check, Python users would have undoubtedly started writing code that relied on the semantics of signed binary arithmetic modulo 2**32 (like C users do), and fixing the mistake would have been a much more painful transition to the community.

- **10:53** Guido van Rossum [written: 2009-02-03_early-language-design-and-development.md line 14] `written:2009-02-03_early-language-design-and-development:printed-repr-valid-input`
  A rule taken from ABC is that every data type, when printed or converted to a string, should be represented by an expression that is valid input to the parser.
  > One of the rules I took from ABC was that every data type, when printed or converted to a string, should be represented by an expression that was a valid input to the language's parser.

- **10:53** Guido van Rossum [written: 2009-02-03_early-language-design-and-development.md line 16] `written:2009-02-03_early-language-design-and-development:sequence-generalization`
  Having three indexable types (list, tuple, string), he generalized them to a common concept, the sequence, so that length, indexing, slicing, and iteration work the same on any sequence type.
  > I decided to generalize these to a common concept, the sequence. This generalization made it so certain core operations such as getting the length (len(s)), indexing (s[i]), slicing (s[i:j]), and iteration (for i in s) worked the same on any sequence type.

- **10:53** Guido van Rossum [written: 2009-02-03_early-language-design-and-development.md line 36] `written:2009-02-03_early-language-design-and-development:should-have-promoted-to-long`
  Raising an overflow exception was still not right; stuck on C's rule that operations on type T return type T, he should have had overflowing integer operations promote their result to longs, as Python does today, though the transition took a long time.
  > In hindsight, I should have made integer operations that overflow promote their result to longs. This is the way that Python works today, but it took a long time to make this transition.

- **10:53** Guido van Rossum [written: 2009-02-03_early-language-design-and-development.md line 12] `written:2009-02-03_early-language-design-and-development:tuple-kept-with-indexing`
  He kept ABC's immutable tuple (with packing and unpacking taken directly from ABC) and, since tuples are internally arrays, added array-like indexing and slicing.
  > I kept ABC's immutable tuple data type... Since tuples are internally represented by arrays, I decided to add array-like indexing and slicing.

### 2009-02-10

- **11:27** Guido van Rossum [written: 2009-02-10_python-s-use-of-dynamic-typing.md line 4] `written:2009-02-10_python-s-use-of-dynamic-typing:abc-also-checked-types-at-runtime`
  ABC did not rely only on static checking; its run-time library re-checked argument types on every operation, so the gap between ABC and Python is smaller than it seems.
  > ABC doesn't ... exclusively rely on static type checking to keep the program from crashing, but has a run-time library that checks the argument types for all operations again each time they are executed.

- **11:27** Guido van Rossum [written: 2009-02-10_python-s-use-of-dynamic-typing.md line 6] `written:2009-02-10_python-s-use-of-dynamic-typing:abc-compromise-global-dynamic-local-static`
  ABC compromised by using dynamic type checking for global variables and static checking for local ones, though to simplify implementation local variables were dynamically checked as well.
  > ABC uses dynamic type checking for global variables, but static type checking for local variables. To simplify the implementation, local variables are dynamically type checked as well.

- **11:27** Guido van Rossum [written: 2009-02-10_python-s-use-of-dynamic-typing.md line 2] `written:2009-02-10_python-s-use-of-dynamic-typing:abc-static-typing-with-inference`
  ABC was statically typed, rejecting inconsistent programs before execution, and unlike most statically typed languages of its time used type inference rather than explicit declarations, like Haskell rather than C.
  > ABC is statically typed which meant that the ABC compiler analyzes the use of types in a program and decides whether they are used consistently. If not, the program is rejected ... ABC used type inference (not unlike Haskell) instead of explicit type declarations

- **11:27** Guido van Rossum [written: 2009-02-10_python-s-use-of-dynamic-typing.md line 10] `written:2009-02-10_python-s-use-of-dynamic-typing:dynamic-typing-is-irreversible`
  Once dynamic typing is chosen there is no going back, because ABC's operations were designed so argument types could be deduced from the form of the operation, while in Python such deductions generally cannot be made.
  > once you decide on dynamic typing, there is no way to go back. ABC’s built-in operations were carefully designed so that the type of the arguments could be deduced from the form of the operation ... In Python, such deductions cannot generally be made.

- **11:27** Guido van Rossum [written: 2009-02-10_python-s-use-of-dynamic-typing.md line 6] `written:2009-02-10_python-s-use-of-dynamic-typing:interactivity-forces-dynamic-typing`
  The most important reason ABC had run-time type checking is that it is interactive: across separately entered statements it is unreasonable to forbid reusing a variable name with a different type.
  > the most important reason why ABC has run time type checking in addition to static type checking is that it is interactive.

- **11:27** Guido van Rossum [written: 2009-02-10_python-s-use-of-dynamic-typing.md line 10] `written:2009-02-10_python-s-use-of-dynamic-typing:operator-overloading-blocks-type-deduction`
  In Python an expression like "x+y" is ambiguous between string concatenation, numeric addition, or an overloaded operation on user-defined types, so the type cannot be deduced from the operation's form.
  > the expression “x+y” could be a string concatenation, a numeric addition, or an overloaded operation on user-defined types.

- **11:27** Guido van Rossum [written: 2009-02-10_python-s-use-of-dynamic-typing.md line 8] `written:2009-02-10_python-s-use-of-dynamic-typing:python-drops-compile-time-checking`
  Python's approach is a small step from ABC's: it drops compile-time type checking completely, in line with Python's "corner-cutting" philosophy, a simplification that does not affect safety since all type errors are still caught at run time before the interpreter can malfunction.
  > Python simply drops the compile-time type checking completely. This is entirely in line with Python’s “corner-cutting” philosophy as it’s a simplification of the implementation that does not affect the eventual safety, since all type errors are caught at run time

- **11:27** Guido van Rossum [written: 2009-02-10_python-s-use-of-dynamic-typing.md line 2] `written:2009-02-10_python-s-use-of-dynamic-typing:python-is-dynamically-typed`
  Python is dynamically typed: the compiler ignores the types in a program and all type checking happens at run time, in contrast to ABC's static typing.
  > In contrast, Python is dynamically typed.  The Python compiler is blissfully unaware of the types used in a program, and all type checking is done at run time.

- **11:27** Guido van Rossum [written: 2009-02-10_python-s-use-of-dynamic-typing.md line 4] `written:2009-02-10_python-s-use-of-dynamic-typing:runtime-checking-as-sanity-check-and-debugging-aid`
  ABC's run-time type checking served as a sanity check for the compiler's not-fully-implemented type-checking algorithms and as a debugging aid producing readable error messages instead of core dumps.
  > This was done in part as a sanity check for the compiler’s type-checking algorithms ... The runtime library was also useful as a debugging aid since explicit run time type checking could produce nice error messages ... instead of the core dumps

### 2009-02-18

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 71] `written:2009-02-18_adding-support-for-user-defined-classes:any-statements-in-class-body`
  Because the class body is just executed statements, any valid Python statements may appear in it, which surprises users; this followed from keeping the syntax simple and not artificially limiting what might be useful.
  > Users are often surprised to learn that any sequence of valid Python statements can appear in a class body. This capability was really just a straightforward extension of my desire to keep the syntax simple as well as not artificially limiting what might possibly be useful.

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 50] `written:2009-02-18_adding-support-for-user-defined-classes:assign-if-exists-has-bootstrap-problem`
  Changing assignment to target an existing instance variable and otherwise a local fails too, because of a bootstrap problem: there would be no way for an instance variable to be created the first time.
  > Changing the semantics of assignment to assign to an instance variable if one already existed and to a local otherwise wouldn't work either, since this would create a bootstrap problem: how does an instance variable get created initially?

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 40] `written:2009-02-18_adding-support-for-user-defined-classes:assignment-always-creates-in-first-dict`
  Variable reference searches locals, globals, built-ins in order, but assignment does not search: it always creates or replaces in the first dictionary (locals), with a per-variable global declaration as the only override. This is why putting the instance dictionary first breaks assignment to locals, and swapping the order merely reverses the problem.
  > Python's assignment doesn't search for the variable name in the dictionaries, but simply adds or replaces the variable in the first dictionary in the search order, normally the local variables... making the instance dictionary the first item in the search order would make it impossible to assign to local variables in a method.

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 12] `written:2009-02-18_adding-support-for-user-defined-classes:attribute-lookup-by-dictionary-search`
  The mechanics are plain dictionary operations: setting a variable updates the instance dictionary; a lookup checks the instance dictionary, then the class dictionary, then the base classes' dictionaries.
  > Whenever changes are made to instance or class variables, those changes are simply reflected in the underlying dictionary object... lookups are performed in the class dictionary and then in the class dictionaries of each of the base classes.

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 4] `written:2009-02-18_adding-support-for-user-defined-classes:c-centric-object-implementation`
  Python is a stack-based bytecode interpreter written in C, with primitive types in C; objects are built from C structures and function pointers because C has no direct object support.
  > Python is implemented in C as a classic stack-based byte code interpreter or "virtual machine" along with a collection of primitive types also implemented in C. The underlying architecture uses "objects" throughout, but since C has no direct support for objects, they are implemented using structures and function pointers.

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 73] `written:2009-02-18_adding-support-for-user-defined-classes:callable-class-no-new-operator`
  Unlike C++ and Java's "new" operator, Python makes the class object itself callable for instantiation, the minimal solution requiring no new syntax, since the parser does not care what kind of object is called; each class is thereby its own factory, anticipating the later factory-function pattern.
  > making the class object itself callable was the right, "minimal" solution, requiring no new syntax... what I had done was simply to turn each class into its own factory.

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 71] `written:2009-02-18_adding-support-for-user-defined-classes:class-body-as-executed-namespace`
  To reuse existing code, the class body is interpreted as statements executed in a new namespace; its resulting dictionary of locals initializes the class dictionary. Concretely the body becomes an anonymous function returning its local dictionary, passed to a helper that creates the class object, which is then bound to the class name in the surrounding scope.
  > it made sense to me to simply interpret the class body as a series of statements that were executed in a new namespace. The dictionary of this namespace would then be captured and used to initialize the class dictionary and create a class object.

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 10] `written:2009-02-18_adding-support-for-user-defined-classes:class-dictionary-holds-methods`
  The class object holds what is shared across instances, chiefly methods, in a "class dictionary" keyed by method name; again the simplest possible design.
  > the set of methods of a class were stored in a dictionary whose keys are the method names. This, I dubbed the class dictionary.

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 18] `written:2009-02-18_adding-support-for-user-defined-classes:class-variables-fall-out`
  Because the class dictionary can hold any object, storing non-method objects there yields class variables, shared by all instances; this feature falls out of the design rather than being designed in.
  > there was no inherent reason why other kinds of objects couldn't be placed there as well. Thus, if objects such as integers or strings are stored in the class dictionary, they become what are known as class variables

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 2] `written:2009-02-18_adding-support-for-user-defined-classes:classes-added-late-but-pre-release`
  Classes were not part of Python's earliest design; they were added late in the first year of development at CWI, yet before the first public release.
  > classes were added late during Python's first year of development at CWI, though well before the first public release

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 14] `written:2009-02-18_adding-support-for-user-defined-classes:depth-first-left-to-right-mro`
  Method resolution walks the class dictionary then each base class recursively, stopping at the first hit: the depth-first, left-to-right rule, the default MRO in most versions of Python.
  > This is commonly referred to as the depth-first, left-to-right rule, and has been the default method resolution order (MRO) used in most versions of Python. More modern releases have adapted a more sophisticated MRO

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 61] `written:2009-02-18_adding-support-for-user-defined-classes:dunder-special-method-names`
  Rather than new syntax for special class methods like initializers and destructors, the user implements methods with special names such as __init__ and __del__; the underscore convention was taken from C, where leading-underscore identifiers are reserved and often special (e.g. __FILE__).
  > I decided that these features could be handled by simply requiring the user to implement methods with special names such as __init__, __del__, and so forth. This naming convention was taken from C where identifiers starting with underscores are reserved by the compiler and often have special meaning

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 20] `written:2009-02-18_adding-support-for-user-defined-classes:dynamic-modifiability-of-classes-and-objects`
  The simple implementation makes classes first-class, introspectable objects and allows dynamic modification: methods added or changed by updating the class dictionary take immediate effect on all instances and subclasses; instances too can gain, change or lose variables.
  > it also makes it possible to modify a class dynamically... methods can be added or modified by simply updating the class dictionary after a class object has already been created!... individual objects can be modified dynamically by adding, modifying, and deleting instance variables

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 54] `written:2009-02-18_adding-support-for-user-defined-classes:explicit-self-removes-special-cases`
  With explicit references, no special method-definition syntax and no complicated variable-lookup semantics are needed: a method is just a function whose first argument, by convention named "self," is the instance.
  > With explicit references, there is no need to have a special syntax for method definitions nor do you have to worry about complicated semantics concerning variable lookup. Instead, one simply defines a function whose first argument corresponds to the instance, which by convention is named "self."

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 52] `written:2009-02-18_adding-support-for-user-defined-classes:explicit-self-the-decision`
  The author gave up implicit instance-variable references and made explicit reference the only way, following C++'s this->foo; rather than making the current object a keyword, he made it the first named argument to a method, so instance variables are always attributes of that argument.
  > I decided to make such explicit references the only way to reference instance variables... rather than making the current object ("this") a special keyword, I would simply make "this" (or its equivalent) the first named argument to a method. Instance variables would just always be referenced as attributes of that argument.

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 34] `written:2009-02-18_adding-support-for-user-defined-classes:implicit-instance-variables-impossible`
  The author first hoped to emulate C++'s implicit instance variables, where a method's unqualified reference resolves to the instance variable; this proved impossible in a language without variable declarations, since instance and local variables could not be elegantly distinguished.
  > it quickly became clear that such an approach would be impossible because there was no way to elegantly distinguish instance variables from local variables in a language without variable declarations.

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 8] `written:2009-02-18_adding-support-for-user-defined-classes:instance-as-classref-plus-dict`
  The chosen design for user-defined objects is the simplest possible: an instance is a built-in object holding a class reference and an "instance dictionary" of instance variables.
  > I settled on the simplest possible design; a scheme where objects were represented by a new kind of built-in object that stored a class reference pointing to a "class object" shared by all instances of the same class, and a dictionary, dubbed the "instance dictionary", that contained the instance variables.

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 59] `written:2009-02-18_adding-support-for-user-defined-classes:modula-3-precedent`
  The self approach resembles Modula-3, which also gave Python its import and exception-handling syntax; Modula-3's record types hold function-pointer members with sugar so that x.m(args) equals f(x, args), matching the typical object implementation and letting instance variables equate to attributes of the first argument.
  > This approach resembles something I had seen in Modula-3, which had already provided me with the syntax for import and exception handling... calling x.m(args) is equivalent to calling f(x, args). This matches the typical implementation of objects and methods

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 20] `written:2009-02-18_adding-support-for-user-defined-classes:more-permissive-than-smalltalk`
  Python's objects are more permissive than Smalltalk's, which restricts an object's attributes to those fixed at creation; the author learned this only later.
  > a feature that I later learned made Python's implementation of objects more permissive than that found in Smalltalk which restricts the set of attributes to those specified at the time of object creation

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 10] `written:2009-02-18_adding-support-for-user-defined-classes:multiple-inheritance-because-it-was-cheap`
  Class objects store references to base classes for inheritance; being naïve about classes but aware of C++'s recent multiple inheritance, the author supported a simple-minded multiple inheritance since he was adding inheritance anyway.
  > as long as I was going to support inheritance, I might as well support a simple-minded version of multiple inheritance. Thus, every class object could have one or more base classes.

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 84] `written:2009-02-18_adding-support-for-user-defined-classes:new-style-classes-constrain-dict`
  New-style classes later required controlling changes to a class's __dict__: a class can still be modified dynamically, but through attribute assignment rather than by using the class __dict__ directly.
  > Eventually, new-style classes made it necessary to control changes to the class __dict__; you can still dynamically modify a class, but you must use attribute assignment rather than using the class __dict__ directly.

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 16] `written:2009-02-18_adding-support-for-user-defined-classes:no-conformance-checking`
  To keep things simple, method lookup does no error or conformance checking; an overriding method need not match the base method's arguments, and the first method found is called with whatever arguments the user supplied.
  > Python performs no advanced error checking or conformance checking when locating methods... no checks are performed to make sure that the redefined method has the same number of arguments... The above method resolution algorithm merely returns the first method found and calls it with whatever arguments the user has supplied.

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 24] `written:2009-02-18_adding-support-for-user-defined-classes:no-separate-method-syntax`
  A major design constraint was to not add a method syntax different from function syntax, because refactoring the grammar and bytecode generator to treat the similar cases differently felt like a huge task.
  > A major design constraint was that I didn't want to add syntax for methods that differed from the syntax for functions. Refactoring the grammar and the byte code generator to handle such similar cases differently felt like a huge task.

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 6] `written:2009-02-18_adding-support-for-user-defined-classes:objects-defined-in-python-the-motivation`
  Siebren van der Zee suggested Python should allow class definitions like C++ so that objects could be implemented in Python, not only in C; this motivated user-defined classes.
  > I believe my colleague Siebren van der Zee was the first to suggest that Python should allow class definitions similar to those in C++ so that objects could also be implemented in Python.

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 50] `written:2009-02-18_adding-support-for-user-defined-classes:rejected-declarations-and-sigils`
  Requiring explicit instance-variable declarations was rejected because the author had gotten this far with no declarations and they would be needed almost everywhere in a class; lexically distinct instance variables (a sigil like Ruby's @, or a naming convention) also did not appeal to him, then or now.
  > Requiring a special specification for instance variables, on the other hand, would have to be used almost everywhere in a class. Another possible solution would have been to make instance variables lexically distinct... Neither of these appealed to me (and they still don't).

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 81] `written:2009-02-18_adding-support-for-user-defined-classes:special-methods-map-c-function-pointers`
  The special-method technique also lets user classes redefine Python's operators: the C-level function pointers (get attribute, add, call) are mapped to special method names (__getattr__, __add__, __call__), with a direct correspondence to the function-pointer tables defined when implementing objects in C.
  > I mapped the various function pointers to special method names such as __getattr__, __add__, and __call__. There is a direct correspondence between these names and the tables of function pointers one has to define when implementing new Python objects in C.

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 4] `written:2009-02-18_adding-support-for-user-defined-classes:type-as-table-of-function-pointers`
  An object type is a statically allocated structure of function pointers, one per standard operation; optional operations may be left NULL, in which case the VM errors or supplies a default.
  > An object type is then represented by a statically allocated structure containing a series of function pointers, one for each standard operation... some operations are optional, and the object type may leave the function pointer NULL if it chooses not to implement that operation. In this case, the virtual machine either generates a run-time error or, in some cases, provides a default implementation

- **11:25** Guido van Rossum [written: 2009-02-18_adding-support-for-user-defined-classes.md line 4] `written:2009-02-18_adding-support-for-user-defined-classes:type-structure-as-runtime-object`
  Python's introspection comes from making the type structure itself available at run-time as an object like any other.
  > Python's unique approach to introspection comes from its ability to make the type structure itself available at run-time as an object like all others.

### 2009-02-27

- **11:59** Guido van Rossum [written: 2009-02-27_first-class-everything.md line 23] `written:2009-02-27_first-class-everything:attribute-lookup-then-call`
  Bound/unbound methods are central to how classes work: "a.spam()" executes in two steps, a lookup of "a.spam" returning a bound method, then a call "()" applied to that object.
  > the execution of that statement actually occurs in two steps.  First, a lookup of "a.spam" occurs.  This returns a bound method--a callable object.    Next, a function call operation "()" is applied to that object to invoke the method

- **11:59** Guido van Rossum [written: 2009-02-27_first-class-everything.md line 19] `written:2009-02-27_first-class-everything:bound-method`
  For a method obtained through an instance, a "bound method" wrapper implicitly stores the original instance so a later call sets it as the first argument.
  > a different callable object known as a "bound method." is used. ... this wrapper implicitly stores the original instance that was used to obtain the method.

- **11:59** Guido van Rossum [written: 2009-02-27_first-class-everything.md line 6] `written:2009-02-27_first-class-everything:common-c-data-structure`
  The implementation made first-class-everything simple because all Python objects were based on one common C data structure used everywhere in the interpreter, regardless of whether it held an integer or a class.
  > All of Python's objects were based on a common C data structure that was used everywhere in the interpreter. ... it just didn't matter if the structure happened to represent a simple object such as an integer or something more complicated such as a class.

- **11:59** Guido van Rossum [written: 2009-02-27_first-class-everything.md line 4] `written:2009-02-27_first-class-everything:first-class-everything`
  Guido's goal that every object nameable in Python (integers, strings, functions, classes, modules, methods) have equal status: assignable to variables, placed in lists, stored in dictionaries, passed as arguments.
  > One of my goals for Python was to make it so that all objects were "first class."  By this, I meant that I wanted all objects that could be named in the language ... to have equal status.

- **11:59** Guido van Rossum [written: 2009-02-27_first-class-everything.md line 8] `written:2009-02-27_first-class-everything:methods-as-first-class-problem`
  A subtle aspect of making the idea complete was making methods first-class objects, since a method, unlike an ordinary function, expects its first argument to be an instance of its class.
  > there was still one subtle aspect of classes that I still needed to address---namely, the problem of making methods first class objects.

- **11:59** Guido van Rossum [written: 2009-02-27_first-class-everything.md line 21] `written:2009-02-27_first-class-everything:one-type-for-both-methods`
  Bound and unbound methods are the same internal object type, distinguished by an instance attribute: None means unbound, otherwise bound.
  > the same internal object type is used to represent bound and unbound methods.   One of the attributes of this object contains a reference to an instance.   If set to None, the method is unbound.  Otherwise, the method is bound.

- **11:59** Guido van Rossum [written: 2009-02-27_first-class-everything.md line 17] `written:2009-02-27_first-class-everything:unbound-method`
  Guido created a callable object, the "unbound method," a thin wrapper around the function that enforced the restriction that the first argument be an instance of the class in which the method was defined.
  > I created a type of callable object known as an "unbound method."   An unbound method was really just a thin wrapper around the function object that implemented a method, but it enforced a restriction that the first argument had to be an instance of the class in which the method was defined.

- **11:59** Guido van Rossum [written: 2009-02-27_first-class-everything.md line 26] `written:2009-02-27_first-class-everything:unbound-methods-removed-py3k`
  In Python 3000 unbound methods were removed and "A.spam" returns a plain function, because the first-argument restriction was rarely helpful for diagnosing problems and often obstructed advanced usages ("duck typing self").
  > In Python 3000, the concept of unbound methods has been removed ... the restriction that the first argument had to be an instance of A was rarely helpful in diagnosing problems, and frequently an obstacle to advanced usages

### 2009-03-03

- **12:02** Guido van Rossum [written: 2009-03-03_how-everything-became-an-executable-statement.md line 6] `written:2009-03-03_how-everything-became-an-executable-stat:class-body-as-arbitrary-code`
  The reasoning began with allowing regular variable assignments in a class body, not just function declarations, then extended to allowing arbitrary executable code anywhere.
  > Rather than defining the class body as a series of function declarations only, it seemed to make sense to also allow regular variable assignments there. However, if I was going to allow that, why not go one step further and allow arbitrary executable code?

- **12:02** Guido van Rossum [written: 2009-03-03_how-everything-became-an-executable-statement.md line 4] `written:2009-03-03_how-everything-became-an-executable-stat:early-grammar-restricted-declarative-elements`
  In a very early version of the grammar, declarative-flavored elements like import statements and function definitions were allowed only at the top level of a module or script; adding classes, van Rossum judged this too restrictive.
  > grammar elements that had a “declarative flavor”, like import statements and function definitions, were allowed only at the top level in a module or script ... However, at the time I was adding support for classes, I decided that this was too restrictive.

- **12:02** Guido van Rossum [written: 2009-03-03_how-everything-became-an-executable-statement.md line 2] `written:2009-03-03_how-everything-became-an-executable-stat:everything-is-an-executable-statement`
  Every part of Python is an executable statement, including function and class definitions, so any statement can appear anywhere in a program.
  > every part of the language is an executable statement, including function and class definitions.  That means that any statement can appear anywhere in a program.

- **12:02** Guido van Rossum [written: 2009-03-03_how-everything-became-an-executable-statement.md line 8] `written:2009-03-03_how-everything-became-an-executable-stat:syntax-allows-what-semantics-did-not-support`
  The feature let the grammar accept constructs the semantics did not support, so e.g. nested functions could be written even though Python lacked nested scopes, often operating in broken or unexpected ways; many such cases were later fixed, with nested function definitions working more sanely in Python 2.1.
  > the Python grammar technically allowed users to write things such as nested functions even though the underlying semantics of Python didn't support nested scopes. ... many of these "broken" features have been fixed.  For example, nested function definitions only began to work more sanely in Python 2.1.

- **12:02** Guido van Rossum [written: 2009-03-03_how-everything-became-an-executable-statement.md line 6] `written:2009-03-03_how-everything-became-an-executable-stat:uniform-statements-simplify-grammar-and-compiler`
  Allowing statements anywhere simplified the grammar, since all uses of statements could share one grammar rule and the compiler could use the same byte code generation function for all of them.
  > this enabled a simplification of the grammar, since now all uses of statements (whether indented or not) could share the same grammar rule, and hence the compiler could use the same byte code generation function for all of them.

### 2009-03-06

- **09:26** Guido van Rossum [written: 2009-03-06_how-exceptions-came-to-be-classes.md line 8] `written:2009-03-06_how-exceptions-came-to-be-classes:avoid-name-clashes-between-modules`
  The main reason for the identity semantics was worry about name clashes between unrelated exceptions in different modules; the intended convention was to define an exception as a global constant in a module and refer to it by name everywhere it is raised or caught.
  > The main reason however is that I worried about name clashes between unrelated exceptions defined in different modules. I intended the usage pattern to strictly adhere to the convention of defining an exception as a global constant in some module, and then using it by name in all code raising or catching it.

- **09:26** Guido van Rossum [written: 2009-03-06_how-exceptions-came-to-be-classes.md line 12] `written:2009-03-06_how-exceptions-came-to-be-classes:class-exceptions-introduced-1997`
  In 1997 with Python 1.5 he introduced class exceptions, the recommended approach since; string exceptions stayed for legacy use through Python 2.5 and were removed in 2.6.
  > In 1997, with Python 1.5, I introduced class exceptions into the language. Although class exceptions have been the recommended approach ever since, string exceptions were still supported for use by certain legacy applications through Python 2.5. They were finally removed in Python 2.6.

- **09:26** Guido van Rossum [written: 2009-03-06_how-exceptions-came-to-be-classes.md line 10] `written:2009-03-06_how-exceptions-came-to-be-classes:compiler-unifies-literals-breaks-across-modules`
  In practice the byte code compiler unified string literals within a module, so by accident exceptions could be caught by the error-message literal as well as the name; this worked only within a module and broke mysteriously across modules, causing widespread confusion.
  > Early Python users discovered that within the same module, the byte code compiler would unify string literals ... it only worked for code defined in the same module---if one tried to catch exceptions using the exception error message in a different module, it broke mysteriously. Needless to say, this is the sort of thing that causes widespread confusion.

- **09:26** Guido van Rossum [written: 2009-03-06_how-exceptions-came-to-be-classes.md line 2] `written:2009-03-06_how-exceptions-came-to-be-classes:early-choice-strings-for-exceptions`
  In early Python the author identified exceptions by strings, which he judges unfortunate, for two reasons: he learned exceptions from Modula-3 (where they are unique tokens), and he introduced exceptions before user-defined classes existed.
  > In early Python however, I chose to identify exceptions by strings. This was unfortunate, but I had two reasons for taking this approach. First, I learned about exceptions from Modula-3, where exceptions are unique tokens. Second, I introduced exceptions before I introduced user-defined classes.

- **09:26** Guido van Rossum [written: 2009-03-06_how-exceptions-came-to-be-classes.md line 2] `written:2009-03-06_how-exceptions-came-to-be-classes:exceptions-as-classes-in-modern-languages`
  In modern languages, and in modern Python, exceptions are defined by user-defined classes.
  > In modern languages (including modern Python :-), exceptions are defined in terms of user-defined classes.

- **09:26** Guido van Rossum [written: 2009-03-06_how-exceptions-came-to-be-classes.md line 2] `written:2009-03-06_how-exceptions-came-to-be-classes:exceptions-for-error-handling`
  From the start the author wanted Python to handle errors through exceptions.
  > Early on, I knew I wanted Python to use exceptions for error handling.

- **09:26** Guido van Rossum [written: 2009-03-06_how-exceptions-came-to-be-classes.md line 6] `written:2009-03-06_how-exceptions-came-to-be-classes:identity-not-value-semantics`
  He chose semantics where distinct string objects are distinct exceptions even with equal value, so exceptions are referenced by name (object identity) and never by value (string equality), keeping exceptions in different modules independent.
  > I chose semantics where different string objects would represent different exceptions, even if they had the same value ... The idea was that exceptions would always be referenced by their name, which would imply object identity, never by their value, which would require string equality.

- **09:26** Guido van Rossum [written: 2009-03-06_how-exceptions-came-to-be-classes.md line 8] `written:2009-03-06_how-exceptions-came-to-be-classes:literal-interning-came-later`
  This design predated the automatic interning of certain string literals.
  > (This was also long before certain string literals would be automatically be “interned”.)

- **09:26** Guido van Rossum [written: 2009-03-06_how-exceptions-came-to-be-classes.md line 8] `written:2009-03-06_how-exceptions-came-to-be-classes:modula-3-token-influence`
  The design was influenced by Modula-3, where each exception declaration creates a unique token that can't be confused with another.
  > This approach was influenced by Modula-3’s exceptions, where each exception declaration creates a unique “exception token” that can’t be confused with any other exception token.

- **09:26** Guido van Rossum [written: 2009-03-06_how-exceptions-came-to-be-classes.md line 8] `written:2009-03-06_how-exceptions-came-to-be-classes:premature-optimization-pointer-comparison`
  He also wanted to test exceptions by pointer comparison rather than string value comparison, which he now calls a misguided premature optimization of execution time, rare for him since he usually optimized his own coding time.
  > I think I also wanted to optimize testing for exceptions by using pointer comparisons instead of string value comparisons in a misguided attempt to prematurely optimize execution time (a rare one – I usually optimized for my own coding time!).

- **09:26** Guido van Rossum [written: 2009-03-06_how-exceptions-came-to-be-classes.md line 4] `written:2009-03-06_how-exceptions-came-to-be-classes:reuse-existing-builtin-type`
  A new built-in object type for exceptions would have cost considerable C coding, so he reused an existing built-in type; strings seemed natural because exceptions carry error messages.
  > as every built-in object type required a considerable coding effort in C, I decided to reuse an existing built-in type. And, since exceptions are associated with error messages, it seemed natural to use strings to represent exceptions.

- **09:26** Guido van Rossum [written: 2009-03-06_how-exceptions-came-to-be-classes.md line 2] `written:2009-03-06_how-exceptions-came-to-be-classes:scheme-to-identify-kinds-of-exceptions`
  Making exceptions work requires some scheme for distinguishing one kind of exception from another.
  > a critical part of making exceptions work is to come up with some kind of scheme for identifying different kinds of exceptions.

### 2009-03-10

- **13:31** Guido van Rossum [written: 2009-03-10_the-problem-with-integer-division.md line 2] `written:2009-03-10_the-problem-with-integer-division:abc-exact-rationals`
  In ABC, dividing two integers gave an exact rational number; in Python integer division truncated instead.
  > in ABC, when you divided two integers, the result was an exact rational number representing the result.  In Python however, integer division truncated the result to an integer.

- **13:31** Guido van Rossum [written: 2009-03-10_the-problem-with-integer-division.md line 6] `written:2009-03-10_the-problem-with-integer-division:c-numerical-model`
  For Python he relied on C's numerical model: ints as a C long of at least 32 bits, floats as a C double, plus an arbitrary precision integer type called "long".
  > with Python, I relied on the other numerical model with which I was familiar, C. ... I chose to represent Python integers by a C long (guaranteeing at least 32 bits of precision) and floating point numbers by a C double.   I then added an arbitrary precision integer type which I called \"long.\"

- **13:31** Guido van Rossum [written: 2009-03-10_the-problem-with-integer-division.md line 16] `written:2009-03-10_the-problem-with-integer-division:close-but-wrong-answer-hard-to-notice`
  Passing an integer where a float is expected yields an answer close to correct but with much larger error, hard to debug or notice, unlike an invalid type such as a string which is caught quickly (multiplication being the exception).
  > passing an integer can cause an answer that is close to the correct answer but has a much larger error – which is difficult to debug or even notice.

- **13:31** Guido van Rossum [written: 2009-03-10_the-problem-with-integer-division.md line 18] `written:2009-03-10_the-problem-with-integer-division:fixing-integer-division`
  Fixing integer division was hard because programs relied on truncation; the fix was a truncating operator (//), a per-module opt-in ("from __future__ import division"), and a command line flag (-Qxxx), with the correct behavior becoming the default in Python 3000.
  > A truncating division operator (//) was added to the language to provide the same functionality.   In addition, a mechanism (\"from __future__ import division\") was introduced by which the new integer division semantics could be enabled. ... the correct behavior has become the default behavior in Python 3000.

- **13:31** Guido van Rossum [written: 2009-03-10_the-problem-with-integer-division.md line 8] `written:2009-03-10_the-problem-with-integer-division:forbidding-mixed-mode-arithmetic`
  He initially forbade mixed-mode arithmetic to keep the type implementations independent, so one couldn't add an int to a float or even an int to a long; Tim Peters convinced him this was a bad idea and he introduced mixed-mode arithmetic with the usual coercion rules.
  > I initially used another misguided rule that forbade mixed-mode arithmetic, with the aim of making the type implementations independent from each other. ... After Python was released publicly, Tim Peters quickly convinced me that this was a really bad idea, and I introduced mixed-mode arithmetic with the usual coercion rules.

- **13:31** Guido van Rossum [written: 2009-03-10_the-problem-with-integer-division.md line 10] `written:2009-03-10_the-problem-with-integer-division:integer-division-as-rite-of-passage`
  Proposals to change integer division met opposition from those who held that learning integer division was a useful "rite of passage" for programmers.
  > the proposal to change this has had some tough opposition from folks who believed that learning about integer division was one of the more useful \"rites of passage\" for all programmers.

- **13:31** Guido van Rossum [written: 2009-03-10_the-problem-with-integer-division.md line 2] `written:2009-03-10_the-problem-with-integer-division:integer-division-early-mistake`
  Guido names Python's truncating integer division as an early design mistake with large consequences, and notes he abandoned ABC's approach to numbers when he created Python.
  > Python's handling of integer division is an example of early mistake with huge consequences.   As mentioned earlier, when Python was created, I abandoned the approach to numbers that had been used in ABC.

- **13:31** Guido van Rossum [written: 2009-03-10_the-problem-with-integer-division.md line 12] `written:2009-03-10_the-problem-with-integer-division:no-type-declarations-no-coercion`
  Because Python has no type declarations, nothing stops a caller from passing integers to an algorithm meant for floats; unlike statically typed C, Python does not coerce the arguments, so the algorithm runs with integers until mixed-mode arithmetic yields floats.
  > since Python doesn’t have type declarations, nothing is there to stop a caller from providing you with integer arguments. In a statically typed language, like C, the compiler will coerce the arguments to floats, but Python does no such thing

- **13:31** Guido van Rossum [written: 2009-03-10_the-problem-with-integer-division.md line 4] `written:2009-03-10_the-problem-with-integer-division:rationals-did-not-pan-out`
  Exact rational numbers didn't work out as ABC's designers hoped: programs silently used rationals with thousands of digits of precision, running slow, and the fix (starting with an inexact zero) was non-intuitive and hard to debug for beginners.
  > In my experience, rational numbers didn't pan out as ABC's designers had hoped.

- **13:31** Guido van Rossum [written: 2009-03-10_the-problem-with-integer-division.md line 8] `written:2009-03-10_the-problem-with-integer-division:result-type-follows-operands`
  The major mistake was borrowing C's rule that an arithmetic operation's result is always the same type as its operands, a rule that makes sense in C but not in a very-high-level language.
  > The major mistake was that I also borrowed a rule that makes sense in C but not so much in a very-high-level language. For the standard arithmetic operations, including division, the result would always be the same type as the operands.

- **13:31** Guido van Rossum [written: 2009-03-10_the-problem-with-integer-division.md line 14] `written:2009-03-10_the-problem-with-integer-division:silent-truncation-inserts-error`
  Since integers behave like floats for everything except division, one is misled to expect algorithms to behave the same either way; but with two integer operands division silently truncates, inserting a potentially large error, and defensive coercion is tedious, hurts readability and maintainability, and blocks use with complex arguments.
  > when division is involved, and the possibility exists that both operands are integers, the numeric result is silently truncated, essentially inserting a potentially large error into the computation.

### 2009-03-17

- **13:07** Guido van Rossum [written: 2009-03-17_dynamically-loaded-modules.md line 8] `written:2009-03-17_dynamically-loaded-modules:building-modules-remained-a-mystery`
  Even with support for dynamically loadable modules, the procedure for building them stayed obscure to many users, and distributing an extension faced major hurdles across the combinations of platforms, compilers, and linkers.
  > the procedure for building such modules often remained a mystery to many users.

- **13:07** Guido van Rossum [written: 2009-03-17_dynamically-loaded-modules.md line 2] `written:2009-03-17_dynamically-loaded-modules:c-extension-modules-easy-from-the-start`
  Python's implementation architecture was built so that extension modules written in C were easy to write from the beginning.
  > Python's implementation architecture made it easy to write extension modules written in C right from the start.

- **13:07** Guido van Rossum [written: 2009-03-17_dynamically-loaded-modules.md line 4] `written:2009-03-17_dynamically-loaded-modules:community-growth-demanded-separate-loading`
  As the community produced new extension modules faster than anticipated, it demanded that modules could be compiled and loaded separately, which led to interfacing the import statement with the platform's dynamic linking API so import could look for a shared library as well as a ".py" file.
  > the Python community started producing new extension modules at an unanticipated rate, and demanded that extension modules could be compiled and loaded separately.

- **13:07** Guido van Rossum [written: 2009-03-17_dynamically-loaded-modules.md line 10] `written:2009-03-17_dynamically-loaded-modules:distutils-builds-from-anywhere-via-saved-options`
  The distutils tool, largely by Greg Ward, let users build and install extension modules from anywhere; Python's makefile wrote the needed compiler and linker options to a data file that distutils then consulted, and it was integrated as a standard library module starting with Python 1.6.
  > a Python extension building tool called distutils was invented that allowed building and installing extension modules from anywhere. The necessary compiler and linker options were written by Python's makefile to a data file, which was then consulted by distutils when building extension modules.

- **13:07** Guido van Rossum [written: 2009-03-17_dynamically-loaded-modules.md line 12] `written:2009-03-17_dynamically-loaded-modules:distutils-scope-complexity-and-fragmentation`
  distutils does far more than build C extensions (installing pure Python modules and packages, creating Windows installers, running tools like SWIG), but its complexity and lack of maintenance led to third-party alternatives (ez_install / "eggs") and fragmentation in the community; Guido reflects that the problem in full generality seems inherently difficult.
  > distutils does far more than simply building extension modules from C source code.

- **13:07** Guido van Rossum [written: 2009-03-17_dynamically-loaded-modules.md line 6] `written:2009-03-17_dynamically-loaded-modules:dynamic-linking-maintenance-nightmare`
  The dynamic linking support was very useful but introduced a maintenance problem, because each platform used a different API and some had additional constraints.
  > The dynamic linking support proved to be very useful, but also introduced a maintenance nightmare.  Each platform used a different API and some platforms had additional constraints.

- **13:07** Guido van Rossum [written: 2009-03-17_dynamically-loaded-modules.md line 2] `written:2009-03-17_dynamically-loaded-modules:early-static-linking-of-extensions`
  In the early days, because dynamic loading technology was obscure, C extensions had to be statically linked into the interpreter at build time, which required adding them to a shell script that generated the Makefile.
  > in the early days, dynamic loading technology was obscure enough that such extensions had to be statically linked into Python interpreter at build time.

- **13:07** Guido van Rossum [written: 2009-03-17_dynamically-loaded-modules.md line 6] `written:2009-03-17_dynamically-loaded-modules:restructuring-dynamic-linking-code`
  The dynamic linking code was restructured over time: first concentrated into a single source file (which then became cluttered with #ifdef conditional compilation), later split so each platform's code sits in its own file, with Greg Stein's help.
  > the dynamic linking support was restructured so that all the dynamic linking code was concentrated in a single source file.  However, the approach resulted in a large file cluttered with conditional compilation directives (#ifdef).

### 2009-03-31

- **08:44** Guido van Rossum [written: 2009-03-31_the-great-or-grand-renaming.md line 2] `written:2009-03-31_the-great-or-grand-renaming:demand-for-embedded-python`
  As Python grew popular, users asked for an embeddable version, Python itself as a library linked into other applications, analogous to how Emacs embeds a Lisp interpreter.
  > people started to ask for an “embedded” version of Python, which would itself be a library that could be linked into other applications – not unlike the way that Emacs incorporates a Lisp interpreter.

- **08:44** Guido van Rossum [written: 2009-03-31_the-great-or-grand-renaming.md line 2] `written:2009-03-31_the-great-or-grand-renaming:freely-defined-global-names`
  Because of the stand-alone assumption, the C source code defined global linker names freely, without a namespace discipline.
  > The source code therefore freely defined global names (in the C/linker sense) like ‘object’, ‘getlistitem’, ‘INCREF’ and so on.

- **08:44** Guido van Rossum [written: 2009-03-31_the-great-or-grand-renaming.md line 4] `written:2009-03-31_the-great-or-grand-renaming:name-clashes-block-embedding`
  Embedding was complicated by clashes between Python's freely chosen global names and those of the host application, with ‘object’ a particularly common collision.
  > this embedding was complicated by name clashes between Python’s global names and those defined by the embedding application – the name 'object’ was especially popular.

- **08:44** Guido van Rossum [written: 2009-03-31_the-great-or-grand-renaming.md line 4] `written:2009-03-31_the-great-or-grand-renaming:py-prefix-naming-convention`
  The design decision taken was a naming convention prefixing all Python globals with “Py”, “_Py” for internal names that must be global, and “PY” for macros.
  > a naming convention was chosen, whereby all Python globals would have a name starting with “Py” or “_Py” (for internal names that had to be global for technical reasons) or “PY” (for macros).

- **08:44** Guido van Rossum [written: 2009-03-31_the-great-or-grand-renaming.md line 2] `written:2009-03-31_the-great-or-grand-renaming:python-as-stand-alone-program`
  Python was first conceived as a stand-alone program that would only occasionally link in third-party libraries, and this assumption shaped how its source code defined names.
  > When Python was first created, I always envisioned it as a stand-alone program, occasionally linking in third-party libraries.

- **08:44** Guido van Rossum [written: 2009-03-31_the-great-or-grand-renaming.md line 10] `written:2009-03-31_the-great-or-grand-renaming:renaming-paired-with-unit-tests`
  The renaming effort was accompanied by the task of adding unit tests for much of the standard library.
  > They also helped with the equally tedious task of adding unit tests for much of the standard library.

- **08:44** Guido van Rossum [written: 2009-03-31_the-great-or-grand-renaming.md line 14] `written:2009-03-31_the-great-or-grand-renaming:renamings-are-traumatic-for-communities`
  Large renamings are traumatic for developer communities because they require relearning names, rewriting documentation, and complicate integrating patches made before but applied after the rename, especially across unrenamed branches.
  > Great or Grand Renamings are often traumatic events for software developer communities, since they requires the programmers' brains to be rewired, documentation to be rewritten, and complicate the integration of patches created before the renaming but applied after.

- **08:44** Guido van Rossum [written: 2009-03-31_the-great-or-grand-renaming.md line 6] `written:2009-03-31_the-great-or-grand-renaming:two-phase-transition-with-macros`
  The rename was done in two phases bridged by C preprocessor macros, so that old and new names could be mixed and still compile correctly, for backwards compatibility with existing extension modules and to ease the transition for developers.
  > there were two phases. In phase one the linker saw the old names, but the source code used the new names, which were translated to the old names using a large number of C preprocessor macros. In phase two the linker saw the new names, but ... another set of macros now translated the old names to the new names. In both phases, the code could mix old and new names and work correctly.

### 2009-04-21

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 49] `written:2009-04-21_origins-of-python-s-functional-features:addition-of-map-filter-reduce-and-lambda`
  In January 1994 map(), filter(), and reduce() were added to the standard library and the lambda operator was introduced for anonymous functions as expressions.
  > the map(), filter(), and reduce() functions were added to the standard library. In addition, the lambda operator was introduced for creating anonymous functions (as expressions)...

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 56] `written:2009-04-21_origins-of-python-s-functional-features:big-changes-required-less-discussion-then`
  At the time, big changes required much less discussion than later, which Van Rossum frames as both good and bad.
  > at the time big changes required much less discussion than nowadays, for better and for worse.

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 70] `written:2009-04-21_origins-of-python-s-functional-features:closures-as-correct-solution`
  The correct solution was for inner functions to implicitly carry references to referenced local variables of the enclosing scope, i.e. closures, an essential aspect of functional languages; added only in Python 2.2 (importable from the future in 2.1).
  > The \"correct\" solution to this problem was for inner functions to implicitly carry references to all of the local variables in the surrounding scope that are referenced by the function. This is known as a \"closure\"...

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 74] `written:2009-04-21_origins-of-python-s-functional-features:closures-enabled-other-advanced-features`
  Though Python was not envisioned as functional, closures proved useful for developing other advanced features such as new-style classes and decorators.
  > the introduction of closures has been useful in the development of many other advanced programming features. For example, certain aspects of new-style classes, decorators, and other modern features rely upon this capability.

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 49] `written:2009-04-21_origins-of-python-s-functional-features:code-strings-via-exec-seen-as-hacky`
  Specifying anonymous functions as code strings manually processed through exec seemed hacky, motivating a proper mechanism.
  > it seemed pretty \"hacky\" to be specifying anonymous functions as code strings that you had to manually process through exec.

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 64] `written:2009-04-21_origins-of-python-s-functional-features:default-argument-workaround`
  Workarounds existed but counter-intuitively required setting default arguments to pass hidden arguments into the lambda.
  > There were workarounds to this problem, but they counter-intuitively involved setting default arguments and passing hidden arguments into the lambda expression.

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 28] `written:2009-04-21_origins-of-python-s-functional-features:dislike-of-separate-named-function`
  Many users disliked having to define the operation applied to list elements as a wholly separate named function.
  > many people didn't like the fact that you to define the operation that you were applying to the list elements as a completely separate function.

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 76] `written:2009-04-21_origins-of-python-s-functional-features:dynamism-precludes-functional-optimizations`
  Python still lacks features of "real" functional languages, such as tail-recursion optimization; its extremely dynamic nature makes compile-time optimization like Haskell's or ML's impossible, and Van Rossum accepts that.
  > because Python's extremely dynamic nature, it is impossible to do the kind of compile-time optimization known from functional languages like Haskell or ML. And that's fine.

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 34] `written:2009-04-21_origins-of-python-s-functional-features:exec-based-anonymous-function-hacks`
  Before lambda, users (Mark Lutz, then Tim Peters) proposed building anonymous functions from code strings processed through exec; Van Rossum reports their proposals.
  > Mark Lutz... posted some code for a function that created functions using exec.

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 54] `written:2009-04-21_origins-of-python-s-functional-features:features-were-contributed-code`
  These functional additions were a significant early chunk of contributed code, by Amrit Prem.
  > These additions represented a significant, early chunk of contributed code.

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 58] `written:2009-04-21_origins-of-python-s-functional-features:lambda-could-not-reference-enclosing-scope`
  A subtle problem: a lambda expression could not refer to variables in the surrounding scope, breaking code that relied on it.
  > a subtle problem with lambda is that the expression supplied couldn't refer to variables in the surrounding scope.

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 58] `written:2009-04-21_origins-of-python-s-functional-features:lambda-only-a-syntactic-tool`
  Lambda was intended only as a syntactic tool for defining anonymous functions, not a full functional construct.
  > Lambda was really only intended to be a syntactic tool for defining anonymous functions.

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 14] `written:2009-04-21_origins-of-python-s-functional-features:lisp-scheme-users-reimplemented-builtins`
  Because Lisp and Scheme provided such operations as built-ins, users from those languages reimplemented comparable functionality in Python.
  > In functional languages such as Lisp and Scheme, operations such as this were provided as built-in functions of the language. Thus, early users familiar with such languages found themselves implementing comparable functionality in Python.

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 72] `written:2009-04-21_origins-of-python-s-functional-features:map-filter-reduce-superseded-by-comprehensions`
  The map, filter, and reduce functions that originally motivated lambda were largely superseded by list comprehensions and generator expressions; reduce was removed from built-ins in Python 3.0, while lambda, map and filter stay.
  > the map, filter, and reduce functions that originally motivated the introduction of lambda and other functional features have to a large extent been superseded by list comprehensions and generator expressions.

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 4] `written:2009-04-21_origins-of-python-s-functional-features:mapping-over-lists-as-common-operation`
  Mapping a function over each element of a list to build a new list was a common operation that users wrote by hand with a loop.
  > A common operation on lists was that of mapping a function to each of the elements of a list and creating a new list.

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 32] `written:2009-04-21_origins-of-python-s-functional-features:no-anonymous-functions-in-python`
  Although functions were first-class, Python lacked any mechanism for creating anonymous functions, unlike Lisp/Scheme's on-the-fly lambda.
  > Although Python made functions first-class objects, it didn't have any similar mechanism for creating anonymous functions.

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 2] `written:2009-04-21_origins-of-python-s-functional-features:python-not-functional-despite-first-class-functions`
  Van Rossum did not consider Python a functional language or heavily influenced by functional languages, even though he had made functions first-class objects; he came from imperative languages.
  > I have never considered Python to be heavily influenced by functional languages... although I had made functions first-class objects, I didn't view Python as a functional programming language.

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 58] `written:2009-04-21_origins-of-python-s-functional-features:terminology-raised-unmet-expectations`
  The lambda terminology led users from functional languages to expect matching semantics and advanced features, which Python's implementation lacked.
  > the choice of terminology had many unintended consequences... they found Python's implementation to be sorely lacking in advanced features.

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 56] `written:2009-04-21_origins-of-python-s-functional-features:unhappy-with-lambda-terminology`
  Van Rossum was never happy with the "lambda" terminology but adopted it for lack of a better, obvious alternative, following the contributor's choice.
  > I was never all that happy with the use of the \"lambda\" terminology, but for lack of a better and obvious alternative, it was adopted for Python.

- **11:05** Guido van Rossum [written: 2009-04-21_origins-of-python-s-functional-features.md line 2] `written:2009-04-21_origins-of-python-s-functional-features:user-demand-drove-list-and-function-features`
  The push to do more with lists and functions came from users, not from a functional vision of the language.
  > earlier on, it was clear that users wanted to do much more with lists and functions.

### 2009-04-24

- **09:14** Guido van Rossum [written: 2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 12] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:beaudry-insight-led-to-new-style-classes`
  The author credits Beaudry with planting the insight that led to metaclasses, then to new-style classes, and the eventual death of classic classes.
  > Don Beaudry is eventually responsible for planting the insight in my head that led first to metaclasses and later to new-style classes and the eventual death of classic classes.

- **09:14** Guido van Rossum [written: 2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 20] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:body-executed-before-creation-limits-metaclasses`
  A restriction of the design: the method-definition block is executed before the class creation function is called, so a metaclass cannot influence the initial contents of the namespace the method definitions run in.
  > The most important aspect of this API is that the block containing the method definitions is executed before the class creation function is called. This places certain restrictions on the effectiveness of metaclasses, since a metaclass cannot influence the initial contents of the namespace in which the method definitions are executed.

- **09:14** Guido van Rossum [written: 2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 10] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:callable-base-class-triggers-hook`
  The hook's mechanism: a callable type object used as a base class makes the class creation code call that type instead of creating a standard class; the behavior of such classes and their instances is entirely up to the extension module.
  > when an instance of such a callable type was used as a base class in a class statement, the class creation code would magically call that type object instead of creating a standard class object.  The behavior of classes created this way (and their instances) was completely up to the extension module providing the callable type object.

- **09:14** Guido van Rossum [written: 2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 16] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:class-attribute-removes-c-requirement`
  In Python 1.5 the author removed the need to write a C extension to use the hook: class creation also checked for a "__class__" attribute on the base class and called it if present.
  > In Python 1.5, I removed the requirement to write a C extension in order to use the Don Beaudry hook. In addition to check for a callable base class type, the class creation code now also checked for an attribute named “__class__” on the base class, and would call this if present.

- **09:14** Guido van Rossum [written: 2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 18] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:class-creation-api-three-arguments`
  The lasting contribution of the hook: the class creation function's API (name string, tuple of base classes, namespace dictionary; its return value bound to the class name), carried over unchanged into the 2.2 metaclass machinery.
  > the most lasting contribution of the Don Beaudry hook is the API for the class creation function, which was carried over to the new metaclass machinery in Python 2.2. ... the class creation function is called with three arguments: a string giving the class name, a tuple giving the base classes ..., and a dictionary giving the contents of the namespace ... The return value of the class creation function is assigned to a variable whose name is the class name.

- **09:14** Guido van Rossum [written: 2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 4] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:class-creation-as-hidden-internal-step`
  Defining a class executes its body in a local dictionary, then passes the name, a tuple of base classes, and that dictionary to an internal class creation function; this machinery was hidden as an implementation detail users didn't need to know.
  > The name of the class, a tuple of base classes, and this local dictionary would then be passed to an internal class creation function that was responsible for creating the class object.  Since all of this machinery was hidden away behind the scenes, it was an implementation detail that users didn’t need to worry about.

- **09:14** Guido van Rossum [written: 2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 2] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:classes-as-first-class-objects`
  In Python's original design, classes were first class objects that could be manipulated like any other object, yet the act of creating a class was fixed and hidden from users.
  > In Python’s original implementation, classes were first class objects that could be manipulated just like any other object.    However, the process of creating a class object was something that was set in stone.

- **09:14** Guido van Rossum [written: 2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 6] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:don-beaudry-hook`
  Beaudry proposed (reported by the author) a slight interpreter modification letting C extension modules create new kinds of class objects; it entered in 1995, was generalized by Jim Fulton, and remained until replaced by metaclasses in 2.2.
  > He then suggested a very slight modification to the interpreter that would allow new kinds of class objects to be created by C code extension modules.

- **09:14** Guido van Rossum [written: 2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 20] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:internal-api-became-public`
  What was simply the internal API for creating classes became a public API because the hook reused the same call signature.
  > Originally, this was simply the internal API for creating classes. The Don Beaudry hook used the same call signature and hence it became a public API.

- **09:14** Guido van Rossum [written: 2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 6] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:missed-opportunity-for-custom-classes`
  Beaudry's point (reported by the author) that hiding class creation was a missed opportunity: if classes are special kinds of objects, one could create new kinds of classes that behave differently.
  > Don Beaudry was the first to point out that this was a missed opportunity for expert users.   Specifically, if classes were simply special kinds of objects, why couldn’t you create new kinds of classes that could be customized to behave in different ways?

- **09:14** Guido van Rossum [written: 2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 8] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:no-change-to-class-syntax`
  A constraint the author placed on himself: the mechanism had to work without changing the already well-established class syntax.
  > The only catch was that I didn't want to make any changes to the class syntax which had already been well-established.

- **09:14** Guido van Rossum [written: 2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 22] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:python-3000-alternative-namespace-mapping`
  Python 3000 lifted that restriction, letting a metaclass provide an alternative mapping object in which the class body is executed; to support this, the metaclass is now specified with keyword argument syntax in the base class list, introduced for this purpose.
  > This was changed in Python 3000, so that now a metaclass can provide an alternative mapping object in which the class body is executed.  In order to support this, the syntax for specifying an explicit metaclass is also changed: it uses keyword argument syntax in the list of base classes, which was introduced for this purpose.

- **09:14** Guido van Rossum [written: 2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 12] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:types-were-not-callable-at-the-time`
  Why the hook felt like a hack: type objects were not callable then ('int' was a built-in function, not a callable type), and user-defined classes were callable only through special-casing in the CALL instruction, built-in types being implemented differently.
  > at the time, type objects were not callable -- e.g. 'int' was not a built-in type but a built-in function that returned an instance of the int object, and the int type was neither easily accessible nor callable.  User-defined classes were of course callable, but this was originally special-cased by the CALL instruction, as these were implemented in a completely different way than built-in types.

- **09:14** Guido van Rossum [written: 2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 8] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:user-supplied-final-construction-function`
  The core idea: expert users could make custom class objects if a user-supplied function could stand in at the final step of class creation, receiving the name, bases, and dictionary and doing whatever it wanted with them.
  > expert users would be able to create custom class objects if there was some way to supply a user-supplied function in the final step of class creation.

### 2010-06-21

- **11:07** Guido van Rossum [written: 2010-06-21_new-style-classes.md line 6] `written:2010-06-21_new-style-classes:builtin-types-not-subclassable`
  A concrete defect of the old implementation: built-in types like lists, dictionaries and strings were "special" and could not be specialized by subclassing, which seemed odd for a self-described object oriented language.
  > One problem with the class implementation was that there was no way to subclass built-in types... these objects were somehow "special" and could not be specialized via subclassing. This limitation seemed rather odd for a language that claimed to be "object oriented."

- **11:07** Guido van Rossum [written: 2010-06-21_new-style-classes.md line 4] `written:2010-06-21_new-style-classes:class-implementation-a-source-of-griping`
  As Python evolved, the problems with the original class implementation became a frequent complaint among expert users.
  > as Python evolved, various problems with the class implementation became a popular topic of griping from expert Python users.

- **11:07** Guido van Rossum [written: 2010-06-21_new-style-classes.md line 4] `written:2010-06-21_new-style-classes:classes-as-afterthought-cut-corners`
  Guido recalls that adding classes to Python was essentially an afterthought, and the implementation he chose exemplified Python's "cut corners" philosophy.
  > Earlier, I described how the addition of classes to Python was essentially an afterthought. The implementation chosen was definitely an example of Python's "cut corners" philosophy.

- **11:07** Guido van Rossum [written: 2010-06-21_new-style-classes.md line 15] `written:2010-06-21_new-style-classes:eventual-removal-and-the-object-idiom`
  Although old-style classes will eventually be removed, users are getting used to writing "class MyClass(object)", which Guido judges "isn't so bad".
  > although the old-style classes will eventually be removed from the languages, users are getting used to writing "class MyClass(object)" to declare a class, which isn't so bad.

- **11:07** Guido van Rossum [written: 2010-06-21_new-style-classes.md line 10] `written:2010-06-21_new-style-classes:metaclass-notion-from-forman-danforth`
  A specific notion of what a metaclass is came from the book "Putting Metaclasses to Work" by Ira Forman and Scott Danforth, distinct from the similar Smalltalk concept.
  > A major influence on this work was the book "Putting Metaclasses to Work" by Ira Forman and Scott Danforth, which provided me with a specific notion of what a metaclass is, different from a similar concept in Smalltalk.

- **11:07** Guido van Rossum [written: 2010-06-21_new-style-classes.md line 12] `written:2010-06-21_new-style-classes:new-style-as-feature-not-replacement`
  New-style classes were introduced as a new language feature rather than a strict replacement; for backwards compatibility the old implementation stayed the default in Python 2, and a new-style class is made by subclassing an existing new-style class such as object.
  > new-style classes were introduced as a new language feature, not as a strict replacement for old-style classes. In fact, for backwards compatibility, the old class implementation remains the default class creation protocol in Python 2.

- **11:07** Guido van Rossum [written: 2010-06-21_new-style-classes.md line 12] `written:2010-06-21_new-style-classes:object-as-root-of-hierarchy`
  To create a new-style class one subclasses an existing new-style class such as object, which is the root of the new-style class hierarchy.
  > you simply have to subclass an existing new-style class such as object (which is the root for the new-style class hierarchy)

- **11:07** Guido van Rossum [written: 2010-06-21_new-style-classes.md line 10] `written:2010-06-21_new-style-classes:reimplementation-in-2.2-do-it-right`
  In Python 2.2 Guido reimplemented classes to "do it right", the most ambitious rewrite of a major subsystem to date, which he concedes carried a risk of "second-system syndrome".
  > In Python 2.2, I finally took the time to reimplement classes and "do it right." This change was, by far, the most ambitious rewrite of a major Python subsystem to date and one could certainly accuse me of a certain amount of "second-system syndrome" in this effort.

- **11:07** Guido van Rossum [written: 2010-06-21_new-style-classes.md line 15] `written:2010-06-21_new-style-classes:rewrite-judged-a-success`
  Guido judges the change a major success: metaclasses became popular with framework writers, explaining classes got easier with fewer exceptions, and maintained backwards compatibility let old code keep working.
  > The change to new-style classes has been a major success. The new metaclasses have become popular amongst framework writers and explaining classes has actually become easier since there were fewer exceptions.

- **11:07** Guido van Rossum [written: 2010-06-21_new-style-classes.md line 10] `written:2010-06-21_new-style-classes:scope-of-the-rewrite`
  Beyond subclassable built-in types, the rewrite added true metaclasses, attempted to fix the naïve method resolution order for multiple inheritance, and added other features.
  > Not only did I address the immediate problem of allowing built-in types to be subclassed, I also added support for true metaclasses, attempted to fix the naïve method resolution order for multiple inheritance, and added a variety of other features.

- **11:07** Guido van Rossum [written: 2010-06-21_new-style-classes.md line 8] `written:2010-06-21_new-style-classes:user-classes-outside-the-type-system`
  The type system was "wrong" for user-defined classes: type(a) == type(b) was True even for instances of unrelated classes, unlike C++ and Java where classes are tightly integrated with the type system.
  > statements such as type(a) == type(b) would evaluate as True even if a and b were instances of completely unrelated classes... in those languages, classes were tightly integrated with the underlying type system.

- **11:18** Guido van Rossum [written: 2010-06-21_the-inside-story-on-new-style-classes.md line 40] `written:2010-06-21_the-inside-story-on-new-style-classes:class-attributes-as-default-values`
  For classic classes, non-function class attributes are returned unchanged, allowing class attributes to serve as "default" values for instance variables; assignment to the instance shadows the class value and deletion reveals it again.
  > This makes it possible to use class attributes as “default” values for instance variables.

- **11:18** Guido van Rossum [written: 2010-06-21_the-inside-story-on-new-style-classes.md line 50] `written:2010-06-21_the-inside-story-on-new-style-classes:classmethod-staticmethod-property-built-on-descriptors`
  Python 2.2 added classmethod, staticmethod, and property as predefined classes built on the descriptor machinery; staticmethod calls the function unchanged, classmethod passes the class as first argument, and property turns a getter/setter pair into an attribute.
  > Python 2.2 added three predefined classes: classmethod, staticmethod, and property, that utilized the new descriptor machinery.

- **11:18** Guido van Rossum [written: 2010-06-21_the-inside-story-on-new-style-classes.md line 82] `written:2010-06-21_the-inside-story-on-new-style-classes:decorator-syntax-chosen-by-bdfl-pronouncement`
  The decorator syntax, derived from Java's annotations, was debated endlessly and decided by "BDFL pronouncement"; decorator is not to be confused with descriptor.
  > The particular choice of decorator syntax (derived from Java's annotations) was debated endlessly before it was decided by “BDFL pronouncement”.

- **11:18** Guido van Rossum [written: 2010-06-21_the-inside-story-on-new-style-classes.md line 75] `written:2010-06-21_the-inside-story-on-new-style-classes:decorators-address-readability-downside`
  The wrapping-by-assignment approach forced the reader to reach the end of a method before learning its kind; Python 2.4 introduced decorator syntax (`@expression` before a declaration) to fix this.
  > A downside of this approach is that the reader of a class had to read all the way till the end of a method declaration before finding out whether it was a class or static method (or some user-defined variation).

- **11:18** Guido van Rossum [written: 2010-06-21_the-inside-story-on-new-style-classes.md line 84] `written:2010-06-21_the-inside-story-on-new-style-classes:decorators-exceeded-expectations`
  Decorators became one of the more successful features, with custom uses exceeding Guido's widest expectations (especially web frameworks), leading to their extension to class definitions in Python 2.6.
  > The decorator feature has become one of the more successful language features, and the use of custom decorators has exceeded my widest expectations.

- **11:18** Guido van Rossum [written: 2010-06-21_the-inside-story-on-new-style-classes.md line 44] `written:2010-06-21_the-inside-story-on-new-style-classes:descriptor-protocol-get`
  Python 2.2 generalized the wrapping behavior: instead of hard-coding which objects get wrapped, the object found by the attribute search decides via a `__get__` method; function objects gained a `__get__` so users can define their own descriptor classes.
  > Instead of hard-coding the behavior that Python function objects are wrapped and other objects aren’t, the wrapping is now left up to the object found by the attribute search ... If the object found by an attribute search happens to have a special method named __get__, it is considered to be a \"descriptor\" object.

- **11:18** Guido van Rossum [written: 2010-06-21_the-inside-story-on-new-style-classes.md line 46] `written:2010-06-21_the-inside-story-on-new-style-classes:descriptor-set-and-delete`
  The same idea was extended to setting and deleting attributes through `__set__` and `__delete__`, giving a descriptor complete control over get/set/delete; this customization applies only when the descriptor appears in a class dictionary, not an instance dictionary.
  > Thus, by redefining these methods, a descriptor object can have complete control over what it means to get, set, and delete an attribute. However, it's important emphasize that this customization only applies when a descriptor instance appears in a class dictionary—not the instance dictionary of an object.

- **11:18** Guido van Rossum [written: 2010-06-21_the-inside-story-on-new-style-classes.md line 32] `written:2010-06-21_the-inside-story-on-new-style-classes:descriptors-generalize-bound-methods`
  Descriptors generalize the concept of bound methods, which was central to classic classes; in classic classes a function found in a class dictionary during attribute lookup was returned as a currying wrapper that inserts the instance in front of the argument list.
  > Descriptors are a generalization of the concept of bound methods, which was central to the implementation of classic classes.

- **11:18** Guido van Rossum [written: 2010-06-21_the-inside-story-on-new-style-classes.md line 42] `written:2010-06-21_the-inside-story-on-new-style-classes:limitation-of-hard-coded-wrapping`
  The old scheme only wrapped Python function objects and this was hard-coded, preventing "hybrid" classes mixing Python and C methods and giving no obvious way to define other kinds of methods such as static member functions.
  > One limitation was that it was prevented the creation of “hybrid” classes that had some methods implemented in Python and others in C, because only Python functions were being wrapped in such a way as to provide the method with access to the instance, and this behavior was hard-coded in the language.

- **11:18** Guido van Rossum [written: 2010-06-21_the-inside-story-on-new-style-classes.md line 26] `written:2010-06-21_the-inside-story-on-new-style-classes:new-enables-creation-patterns-and-unpickling`
  Overriding `__new__()` lets a class implement patterns like Singleton, return a previously created instance, or return an instance of a different class; it is also used in pickle to create instances while unserializing without invoking `__init__`.
  > By overriding __new__() a class author can implement patterns like the Singleton Pattern, return a previously created instance (e.g., from a free list), or to return an instance of a different class (e.g., a subclass).

- **11:18** Guido van Rossum [written: 2010-06-21_the-inside-story-on-new-style-classes.md line 28] `written:2010-06-21_the-inside-story-on-new-style-classes:new-for-subclassing-immutable-types`
  Immutable objects cannot be initialized through a standard `__init__()`, so `__new__` lets their subclasses perform any special initialization as the object is created, e.g. passing a modified value to the base class `__new__`.
  > Another use of __new__ is to help with the subclassing of immutable types. By the nature of their immutability, these kinds of objects can not be initialized through a standard __init__() method.

- **11:18** Guido van Rossum [written: 2010-06-21_the-inside-story-on-new-style-classes.md line 24] `written:2010-06-21_the-inside-story-on-new-style-classes:new-hook-for-customizing-object-creation`
  Old-style classes gave `__init__()` for initializing an instance after creation but never provided a real hook to customize how instances are created; `__new__()` was introduced as a class method so the author can control instance creation.
  > Old-style classes never really provided a hook for customizing the creation of objects although there were library modules allowed certain kinds of objects to be created in non-standard ways (e.g., the \"new\" module).

- **11:18** Guido van Rossum [written: 2010-06-21_the-inside-story-on-new-style-classes.md line 4] `written:2010-06-21_the-inside-story-on-new-style-classes:new-style-classes-introduced-new-concepts`
  New-style classes look similar to the original class implementation on the surface, but introduced several new concepts: `__new__()`, descriptors, static and class methods, properties, decorators, slots, and a new Method Resolution Order.
  > On the surface, new-style classes appear very similar to the original class implementation. However, new-style classes also introduced a number of new concepts:

- **11:18** Guido van Rossum [written: 2010-06-21_the-inside-story-on-new-style-classes.md line 59] `written:2010-06-21_the-inside-story-on-new-style-classes:no-new-syntax-at-first`
  These descriptors were introduced without special syntax because it was deemed too controversial to add a major feature and new syntax at once; users wrapped methods with extra assignment statements instead.
  > At the time, it was deemed too controversial to simultaneously introduce a major new feature along with new syntax (which always leads to a heated debate).

- **11:18** Guido van Rossum [written: 2010-06-21_the-inside-story-on-new-style-classes.md line 36] `written:2010-06-21_the-inside-story-on-new-style-classes:self-argument-mechanism`
  The wrapper returned by attribute lookup is the fundamental mechanism by which methods obtain their "self" argument, calling the original function with the instance inserted in front.
  > This is the fundamental mechanism by which methods in classes obtain their \"self\" argument.

- **11:18** Guido van Rossum [written: 2010-06-21_the-inside-story-on-new-style-classes.md line 88] `written:2010-06-21_the-inside-story-on-new-style-classes:slots-as-descriptor-application`
  `__slots__` is another application of descriptors: it restricts valid attribute names, removes the instance `__dict__`, and stores attributes in array locations, each slot being a descriptor that gets/sets via an array index, implemented entirely in C.
  > Another enhancement made possible with descriptors was the introduction of the __slots__ attribute on classes.

- **11:18** Guido van Rossum [written: 2010-06-21_the-inside-story-on-new-style-classes.md line 93] `written:2010-06-21_the-inside-story-on-new-style-classes:slots-ultimate-goal-was-performance`
  Contrary to the assumption that `__slots__` is for code safety, its ultimate goal was performance; Guido feared the class-system changes (the extra data-descriptor check on every attribute access) would hurt performance, so `__slots__` was a fallback optimization. It turned out unnecessary but was too late to remove, though used properly it can reduce memory footprint.
  > Some people mistakenly assume that the intended purpose of __slots__ is to increase code safety (by restricting the attribute names). In reality, my ultimate goal was performance.

- **11:18** Guido van Rossum [written: 2010-06-21_the-inside-story-on-new-style-classes.md line 38] `written:2010-06-21_the-inside-story-on-new-style-classes:x-f-equals-C-f-x`
  Asking the class for the function attribute returns the unwrapped function, so `x.f(0)` is equivalent to `C.f(x, 0)`, a fundamental equivalence in Python.
  > In other words, x.f(0) is equivalent to C.f(x, 0). This is a pretty fundamental equivalence in Python.

- **11:31** Guido van Rossum [written: 2010-06-21_import-antigravity.md line 2] `written:2010-06-21_import-antigravity:antigravity-as-stdlib-easter-egg`
  Python 3's standard library carries an easter egg module, `antigravity`, referencing the XKCD comic that mentions Python; its inclusion is treated as a deliberate playful element of the distribution rather than functional code. Van Rossum reports it was added to Python 3 by Skip Montanaro and originated as a launch easter egg in Google App Engine.
  > The antigravity module, referencing the XKCD comic mentioning Python, was added to Python 3 by Skip Montanaro.

- **11:31** Guido van Rossum [written: 2010-06-21_import-antigravity.md line 12] `written:2010-06-21_import-antigravity:easter-egg-inside-the-easter-egg`
  The stdlib version nests a second hidden joke in its source: a function that purports to implement the XKCD geohashing algorithm, so the playfulness is layered for anyone who reads the code.
  > The Python 3 stdlib version has an easter egg inside the easter egg, ... it defines a function that purports to implement the XKCD geohashing algorithm.

### 2010-06-23

- **10:41** Guido van Rossum [written: 2010-06-23_method-resolution-order.md line 41] `written:2010-06-23_method-resolution-order:adopt-c3-linearization`
  After discussion it was decided to replace the 2.2 scheme with the academically published C3 Linearization algorithm from the Dylan paper.
  > it was decided that the MRO adopted for Python 2.2 was broken and that Python should adopt the C3 Linearization algorithm described in the paper \"A Monotonic Superclass Linearization for Dylan\"

- **10:41** Guido van Rossum [written: 2010-06-23_method-resolution-order.md line 47] `written:2010-06-23_method-resolution-order:c3-rejects-inconsistent-hierarchies`
  A consequence of adopting C3 is that Python now rejects any inheritance hierarchy with an inconsistent ordering of base classes rather than resolving it silently.
  > Python will now reject any inheritance hierarchy that has an inconsistent ordering of base classes.

- **10:41** Guido van Rossum [written: 2010-06-23_method-resolution-order.md line 4] `written:2010-06-23_method-resolution-order:classic-mro-depth-first-left-to-right`
  Classic classes resolved methods by a simple depth-first, left-to-right search, returning the first match found.
  > when looking up a method, base classes were searched using a simple depth-first left-to-right scheme.   The first matching object found during this search would be returned.

- **10:41** Guido van Rossum [written: 2010-06-23_method-resolution-order.md line 13] `written:2010-06-23_method-resolution-order:classic-mro-fails-on-diamond`
  The classic depth-first scheme works for simple cases but breaks under diamond inheritance, where it finds the shared ancestor's method instead of the more specialized override.
  > This scheme works fine for simple cases, but has problems that become apparent when one considers more complicated uses of multiple inheritance.  One problem concerns method lookup under \"diamond inheritance.\"

- **10:41** Guido van Rossum [written: 2010-06-23_method-resolution-order.md line 39] `written:2010-06-23_method-resolution-order:documented-wrong-algorithm`
  Van Rossum implemented one algorithm for 2.2 but documented the earlier simpler one, thinking the difference did not matter much; a regret.
  > This is what I implemented for Python 2.2, but I documented the earlier algorithm (naïvely thinking it didn't matter much).

- **10:41** Guido van Rossum [written: 2010-06-23_method-resolution-order.md line 45] `written:2010-06-23_method-resolution-order:inheritance-defines-ordering-rules`
  Each inheritance relationship imposes simple ordering rules (a subclass before its base; earlier-listed bases before later ones), and C3 finds a monotonic ordering satisfying all of them or fails.
  > if you write down all of the ordering rules imposed by inheritance relationships in a complex class hierarchy, the algorithm will determine a monotonic ordering of the classes that satisfies all of them.   If such an ordering can not be determined, the algorithm will fail.

- **10:41** Guido van Rossum [written: 2010-06-23_method-resolution-order.md line 45] `written:2010-06-23_method-resolution-order:monotonicity-as-the-core-problem`
  The core defect of the 2.2 algorithm was monotonicity: once A is determined to precede B, no later rule should force B before A, or the hierarchy is undefined and should be rejected.
  > if you have already determined that class A should be checked before class B, then you should never encounter a situation that requires class B to be checked before class A (otherwise, the result is undefined and the inheritance hierarchy should be rejected).

- **10:41** Guido van Rossum [written: 2010-06-23_method-resolution-order.md line 2] `written:2010-06-23_method-resolution-order:mro-defines-attribute-search-order`
  In languages with multiple inheritance, the Method Resolution Order (MRO) is the order base classes are searched for a method; in Python it also governs lookup of other attributes.
  > the order in which base classes are searched when looking for a method is often called the Method Resolution Order, or MRO. (In Python this also applies to other attributes.)

- **10:41** Guido van Rossum [written: 2010-06-23_method-resolution-order.md line 34] `written:2010-06-23_method-resolution-order:mro-special-case-preserve-first-order`
  The real 2.2 algorithm added a special case that reordered bases to preserve the order in which classes first appeared in the search, departing from the documented algorithm.
  > there was a special case to deal with a situation when two bases classes occurred in a different order in the inheritance list of two different derived classes ... this algorithm tried to preserve the order of classes for bases that appeared first in the search process.

- **10:41** Guido van Rossum [written: 2010-06-23_method-resolution-order.md line 2] `written:2010-06-23_method-resolution-order:mro-trivial-under-single-inheritance`
  MRO only becomes an interesting and subtle problem once multiple inheritance is in play; under single inheritance it is uninteresting.
  > For languages that support single inheritance only, the MRO is uninteresting; but when multiple inheritance comes into play, the choice of an MRO algorithm can be remarkably subtle.

- **10:41** Guido van Rossum [written: 2010-06-23_method-resolution-order.md line 24] `written:2010-06-23_method-resolution-order:new-style-classes-make-diamonds-universal`
  Because all new-style classes inherit from a common base object, every use of multiple inheritance creates a diamond, turning a rare problem into a commonplace one.
  > Although this kind of multiple inheritance was rare in existing code, new-style classes would make it commonplace.   This is because all new-style classes were defined by inheriting from a base class object.

- **10:41** Guido van Rossum [written: 2010-06-23_method-resolution-order.md line 30] `written:2010-06-23_method-resolution-order:object-methods-make-order-critical`
  Since object defines methods that subtypes sometimes extend (e.g. __setattr__), the resolution order becomes critical so the subtype's override applies.
  > since object defined a number of methods that are sometimes extended by subtypes (e.g., __setattr__()), the resolution order becomes critical.

- **10:41** Guido van Rossum [written: 2010-06-23_method-resolution-order.md line 41] `written:2010-06-23_method-resolution-order:pedroni-found-inconsistency`
  Samuele Pedroni found that the actual behavior diverged from the documented algorithm, and that inconsistencies arose even outside the known special case, leading to the judgment that the 2.2 MRO was broken.
  > Samuele Pedroni discovered an inconsistency between the documented MRO algorithm and the results that were actually observed in real-code.   Moreover, inconsistencies were occurring even in code that did not fall under the special case observed above.

- **10:41** Guido van Rossum [written: 2010-06-23_method-resolution-order.md line 32] `written:2010-06-23_method-resolution-order:precompute-and-store-mro`
  For Python 2.2 the MRO was pre-computed at class-definition time and stored as an attribute of the class object, dropping all but the last occurrence of a duplicated class.
  > I adopted a scheme where the MRO would be pre-computed when a class was defined and stored as an attribute of each class object. ... If any class was duplicated in this search, all but the last occurrence would be deleted from the MRO list.

- **10:41** Guido van Rossum [written: 2010-06-23_method-resolution-order.md line 2] `written:2010-06-23_method-resolution-order:python-had-three-mro-algorithms`
  Python has used three MRO algorithms over time (classic, 2.2 new-style, 2.3 new-style / C3), of which only C3 remains in Python 3.
  > Python has known at least three different MRO algorithms: classic, Python 2.2 new-style, and Python 2.3 new-style (a.k.a. C3). Only the latter survives in Python 3.

- **10:41** Guido van Rossum [written: 2010-06-23_method-resolution-order.md line 47] `written:2010-06-23_method-resolution-order:rejection-matches-zen-errors-not-silent`
  Rejecting inconsistent hierarchies is aligned with the Zen of Python's rule that errors should never pass silently.
  > This, of course, matches the Zen of Python's \"errors should never pass silently\" rule.

- **10:41** Guido van Rossum [written: 2010-06-23_method-resolution-order.md line 22] `written:2010-06-23_method-resolution-order:specialized-override-should-win`
  When a subclass redefines a method inherited through a diamond, the more specialized redefinition is the one that should be called; otherwise the subclass's state is ignored and the program breaks.
  > one can argue that the redefined method C.save() is actually the method that you want to call, since it can be viewed as being \"more specialized\" than the method in A ... if the save() method is being used to save the state of an object, not calling C.save() would break the program since the state of C would be ignored.

### 2010-06-29

- **08:39** Guido van Rossum [written: 2010-06-29_from-list-comprehensions-to-generator-expressions.md line 28] `written:2010-06-29_from-list-comprehensions-to-generator-ex:algol-60-inspiration`
  The bare comma-separated for-loop reminded Guido of Algol-60's for-loop form.
  > This also reminded me of Algol-60, where you can write: for i := 1, 2, 3 do Statement

- **08:39** Guido van Rossum [written: 2010-06-29_from-list-comprehensions-to-generator-expressions.md line 28] `written:2010-06-29_from-list-comprehensions-to-generator-ex:bare-sequence-after-in-from-for-loop`
  The original explicit for-loop had no ambiguity after 'in' because a colon always followed, so Guido decided looping over known values shouldn't require parentheses.
  > if you wanted to loop over a bunch of known values, you shouldn't be bothered with having to put parentheses around them.

- **08:39** Guido van Rossum [written: 2010-06-29_from-list-comprehensions-to-generator-expressions.md line 7] `written:2010-06-29_from-list-comprehensions-to-generator-ex:comprehension-syntax`
  The chosen Python notation produces a list of the values of a sequence, selected by an optional predicate and mapped by a function, with multiple for-clauses allowed for nested loops.
  > [f(x) for x in S if P(x)] This produces a list containing the values of the sequence S selected by the predicate P and mapped by the function f.

- **08:39** Guido van Rossum [written: 2010-06-29_from-list-comprehensions-to-generator-expressions.md line 12] `written:2010-06-29_from-list-comprehensions-to-generator-ex:comprehensions-faster-no-stack-frame`
  Comprehensions run faster than map+lambda because a lambda call creates a new stack frame while the comprehension's expression is evaluated without one.
  > the list comprehension executes much faster ... because calling a lambda function creates a new stack frame while the expression in the list comprehension is evaluated without creating a new stack frame.

- **08:39** Guido van Rossum [written: 2010-06-29_from-list-comprehensions-to-generator-expressions.md line 10] `written:2010-06-29_from-list-comprehensions-to-generator-ex:comprehensions-vs-map-filter`
  List comprehensions are an alternative to map() and filter(); on toy cases map/filter look more compact, but on realistic cases the comprehension wins.
  > List comprehensions provide an alternative to using the built-in map() and filter() functions.

- **08:39** Guido van Rossum [written: 2010-06-29_from-list-comprehensions-to-generator-expressions.md line 28] `written:2010-06-29_from-list-comprehensions-to-generator-ex:design-factors-four`
  Four factors governed the design of these notations: backwards compatibility, avoiding ambiguity, the desire for equivalence, and evolution of the language.
  > The factors affecting the design were backwards compatibility, avoiding ambiguity, the desire for equivalence, and evolution of the language.

- **08:39** Guido van Rossum [written: 2010-06-29_from-list-comprehensions-to-generator-expressions.md line 14] `written:2010-06-29_from-list-comprehensions-to-generator-ex:generator-expressions-lazy`
  Generator expressions, added in 2.4 and enabled by generators, represent a sequence of results without building a concrete list, saving memory for large collections.
  > a similar notation that represents a sequence of results without turning it into a concrete list. The new feature is called a "generator expression".

- **08:39** Guido van Rossum [written: 2010-06-29_from-list-comprehensions-to-generator-expressions.md line 36] `written:2010-06-29_from-list-comprehensions-to-generator-ex:genexp-ambiguity-parentheses-not-part-of-syntax`
  The parentheses around a generator expression belong to the surrounding call, not to the genexp syntax, so a bare comma sequence after 'in' would have two interpretations.
  > the parentheses around a generator expression are not technically part of the generator expression syntax ... there would be two interpretations

- **08:39** Guido van Rossum [written: 2010-06-29_from-list-comprehensions-to-generator-expressions.md line 56] `written:2010-06-29_from-list-comprehensions-to-generator-ex:genexp-needs-own-frame`
  Generator expressions cannot leak the variable because they run in a separate execution frame, which made them less efficient than list comprehensions in Python 2.
  > Generator expressions are implemented using generators, whose execution requires a separate execution frame. Thus, generator expressions ... were less efficient than list comprehensions.

- **08:39** Guido van Rossum [written: 2010-06-29_from-list-comprehensions-to-generator-expressions.md line 18] `written:2010-06-29_from-list-comprehensions-to-generator-ex:genexp-syntax-stricter-than-listcomp`
  In Python 2 a list comprehension could take a bare comma sequence after 'in', but a generator expression could not, requiring parentheses.
  > in Python 2, this is a valid list comprehension: ... However this is not a valid generator expression

- **08:39** Guido van Rossum [written: 2010-06-29_from-list-comprehensions-to-generator-expressions.md line 12] `written:2010-06-29_from-list-comprehensions-to-generator-ex:lambda-too-verbose-disagreement`
  Some argue the real problem is that lambda is too verbose and a terser anonymous-function syntax would make map() more attractive; Guido disagrees, preferring the comprehension's readability as expression complexity grows.
  > It has been argued that the real problem here is that Python's lambda notation is too verbose ... Personally, I disagree—I find the list comprehension notation much easier to read than the functional notation

- **08:39** Guido van Rossum [written: 2010-06-29_from-list-comprehensions-to-generator-expressions.md line 2] `written:2010-06-29_from-list-comprehensions-to-generator-ex:list-comprehensions-from-set-notation`
  List comprehensions are a Pythonic interpretation of the mathematical set-builder notation.
  > they are a Pythonic interpretation of a well-known notation for sets used by mathematicians

- **08:39** Guido van Rossum [written: 2010-06-29_from-list-comprehensions-to-generator-expressions.md line 46] `written:2010-06-29_from-list-comprehensions-to-generator-ex:listcomp-equivalent-to-list-of-genexp`
  In Python 3 they decided a list comprehension should be fully equivalent to list() applied to the corresponding generator expression, so they gave list comprehensions the stricter genexp syntax.
  > we wanted the list comprehension ... to be fully equivalent to the following expansion using the built-in list() function applied to a generator expression ... Thus we decided to use the slightly more restrictive syntax of generator expressions for list comprehensions as well.

- **08:39** Guido van Rossum [written: 2010-06-29_from-list-comprehensions-to-generator-expressions.md line 52] `written:2010-06-29_from-list-comprehensions-to-generator-ex:loop-variable-leak-dirty-secret`
  In Python 2 a list comprehension leaks its loop control variable into the surrounding scope, an artifact of the original implementation, an intentional compromise for speed that occasionally stung people.
  > the list comprehension "leaks" the loop control variable into the surrounding scope ... It started out as an intentional compromise to make list comprehensions blindingly fast ... it definitely stung people occasionally.

- **08:39** Guido van Rossum [written: 2010-06-29_from-list-comprehensions-to-generator-expressions.md line 4] `written:2010-06-29_from-list-comprehensions-to-generator-ex:no-universal-set-in-python`
  The mathematical set-builder form implies a universal set understood from context; Python has no such concept, and at the time (2.0) no sets at all, which forced a different notation.
  > In math, this form implies a universal set that is understood by the reader ... In Python, there is no concept of a universal set, and in Python 2.0, there were no sets.

- **08:39** Guido van Rossum [written: 2010-06-29_from-list-comprehensions-to-generator-expressions.md line 60] `written:2010-06-29_from-list-comprehensions-to-generator-ex:python3-both-faster-no-gap`
  Thanks to general Python 3 speed work, both forms became faster than in Python 2 and the speed difference between them disappeared, removing the performance argument for the leak.
  > both list comprehensions and generator expressions in Python 3 are actually faster than they were in Python 2! (And there is no longer a speed difference between the two.)

- **08:39** Guido van Rossum [written: 2010-06-29_from-list-comprehensions-to-generator-expressions.md line 58] `written:2010-06-29_from-list-comprehensions-to-generator-ex:python3-fix-leak-via-genexp-strategy`
  Python 3 fixed the leak by implementing list comprehensions with the same strategy as generator expressions, so the loop variable only shadows the outer one.
  > in Python 3, we decided to fix the "dirty little secret" of list comprehensions by using the same implementation strategy as for generator expressions ... the 'x' in the list comprehension temporarily shadows but does not override the 'x' in the surrounding scope.

- **08:39** Guido van Rossum [written: 2010-06-29_from-list-comprehensions-to-generator-expressions.md line 44] `written:2010-06-29_from-list-comprehensions-to-generator-ex:refuse-to-guess-ambiguity`
  Faced with the ambiguity, they chose not to guess and required a single expression after the genexp's 'in', while not breaking existing list-comprehension code.
  > we decided not to guess in this case, and the generator comprehension was required to have a single expression ... after its 'in' keyword. But at the time we didn't want to break existing code using the (already hugely popular) list comprehensions.

- **08:39** Guido van Rossum [written: 2010-06-29_from-list-comprehensions-to-generator-expressions.md line 62] `written:2010-06-29_from-list-comprehensions-to-generator-ex:set-and-dict-comprehensions`
  Python 3 also supports set and dict comprehensions as straightforward extensions of the list comprehension idea.
  > Python 3 also supports set comprehensions and dictionary comprehensions. These are straightforward extensions of the list comprehension idea.

### 2010-08-24

- **09:49** Guido van Rossum [written: 2010-08-24_why-python-s-integer-division-floors.md line 20] `written:2010-08-24_why-python-s-integer-division-floors:div-and-mod-go-together`
  Integer division (//) and modulo (%) are treated as a pair that must satisfy one mathematical relationship.
  > The integer division operation (//) and its sibling, the modulo operation (%), go together and satisfy a nice mathematical relationship (all variables are integers)

- **09:49** Guido van Rossum [written: 2010-08-24_why-python-s-integer-division-floors.md line 42] `written:2010-08-24_why-python-s-integer-division-floors:floating-point-modulo-hesitation`
  Tim Peters worried about extending these rules to floating point modulo; Guido concedes the floor rule can cause precision loss for x%1.0 when x is a very small negative number, but keeps integer modulo (and //, tightly coupled to it) unchanged.
  > Tim Peters ... has expressed some worry about my desire to extend these rules to floating point modulo. He's probably right; the truncate-towards-negative-infinity rule can cause precision loss for x%1.0 when x is a very small negative number. But that's not enough for me to break integer modulo, and // is tightly coupled to that

- **09:49** Guido van Rossum [written: 2010-08-24_why-python-s-integer-division-floors.md line 10] `written:2010-08-24_why-python-s-integer-division-floors:floor-affects-only-negative-operands`
  For positive operands the result is unsurprising; the flooring behavior shows up (rounding away from zero, towards negative infinity) only when an operand is negative.
  > if one of the operands is negative, the result is floored, i.e., rounded away from zero (towards negative infinity)

- **09:49** Guido van Rossum [written: 2010-08-24_why-python-s-integer-division-floors.md line 44] `written:2010-08-24_why-python-s-integer-division-floors:floor-vs-ambiguous-slash`
  // is used instead of / deliberately: it is Python 3 syntax, also allowed in Python 2 to make clear one is invoking integer division, whereas / in Python 2 is ambiguous because it returns different results for two integers than for mixed int/float operands.
  > I am using // instead of / -- this is Python 3 syntax, and also allowed in Python 2 to emphasize that you know you are invoking integer division. The / operator in Python 2 is ambiguous, since it returns a different result for two integer operands than for an int and a float or two floats

- **09:49** Guido van Rossum [written: 2010-08-24_why-python-s-integer-division-floors.md line 32] `written:2010-08-24_why-python-s-integer-division-floors:follows-number-theory-convention`
  The flooring choice follows what mathematicians in number theory always prefer, and Guido made the same choice for Python.
  > In mathematical number theory, mathematicians always prefer the latter choice (see e.g. Wikipedia). For Python, I made the same choice

- **09:49** Guido van Rossum [written: 2010-08-24_why-python-s-integer-division-floors.md line 2] `written:2010-08-24_why-python-s-integer-division-floors:integer-division-floors`
  Integer division in Python returns the floor of the result instead of truncating towards zero as C does.
  > explain why integer division in Python returns the floor of the result instead of truncating towards zero like C

- **09:49** Guido van Rossum [written: 2010-08-24_why-python-s-integer-division-floors.md line 32] `written:2010-08-24_why-python-s-integer-division-floors:modulo-where-sign-is-uninteresting`
  The reason given is that in some applications of modulo the sign of a is uninteresting; the POSIX-timestamp-to-time-of-day computation (t % 86400) works out with the floor rule even for times before 1970 expressed as negative numbers, where truncation would give a meaningless result.
  > there are some interesting applications of the modulo operation where the sign of a is uninteresting

- **09:49** Guido van Rossum [written: 2010-08-24_why-python-s-integer-division-floors.md line 36] `written:2010-08-24_why-python-s-integer-division-floors:negative-b-flips-invariant`
  For negative b everything flips and the invariant becomes 0 >= r > b.
  > For negative b, by the way, everything just flips, and the invariant becomes:

- **09:49** Guido van Rossum [written: 2010-08-24_why-python-s-integer-division-floors.md line 26] `written:2010-08-24_why-python-s-integer-division-floors:the-invariant`
  The relationship chosen is b*q + r = a with 0 <= r < b, stated for non-negative a and b.
  > b*q + r = a and 0 <= r < b

- **09:49** Guido van Rossum [written: 2010-08-24_why-python-s-integer-division-floors.md line 30] `written:2010-08-24_why-python-s-integer-division-floors:two-choices-for-negative-a`
  Extending the relation to negative a (with b positive) forces a choice: truncating q towards zero makes r negative and changes the invariant, or flooring q towards negative infinity keeps the invariant 0 <= r < b.
  > if you truncate q towards zero, r will become negative, so that the invariant changes to 0 <= abs(r) < otherwise, you can floor q towards negative infinity, and the invariant remains 0 <= r < b

- **09:49** Guido van Rossum [written: 2010-08-24_why-python-s-integer-division-floors.md line 40] `written:2010-08-24_why-python-s-integer-division-floors:why-c-differs`
  C probably truncates because the hardware did so when C was designed, which in turn stems from old hardware representing negatives as sign+magnitude or one's complement rather than two's complement.
  > Probably the hardware didn't do this at the time C was designed. And the hardware probably didn't do it this way because in the oldest hardware, negative numbers were represented as \"sign + magnitude\" rather than the two's complement representation

### 2011-07-08

- **16:13** Guido van Rossum [written: 2011-07-08_karin-dewar-indentation-and-the-colon.md line 10] `written:2011-07-08_karin-dewar-indentation-and-the-colon:B-first-published-language-with-indentation-grouping`
  Meertens claims B was, as far as he is aware, the first published and implemented language to use indentation for grouping, noting occam (1983) and Miranda (1985) came later and so could not be the source.
  > As far as I am aware, B was the first actually     published (and implemented) language to use indentation for     grouping.

- **16:13** Guido van Rossum [written: 2011-07-08_karin-dewar-indentation-and-the-colon.md line 8] `written:2011-07-08_karin-dewar-indentation-and-the-colon:begin-end-superfluous-under-mandatory-indentation`
  Meertens reports that once indentation was mandatory the separate delimiters were redundant, so they were progressively dropped (no BEGIN in B1, END IF/END FOR dropped in B2), leaving pure indentation as the sole indicator of grouping.
  > the latter delimiters were also dropped in      B2, leaving pure     indentation as the sole indicator of grouping.

- **16:13** Guido van Rossum [written: 2011-07-08_karin-dewar-indentation-and-the-colon.md line 2] `written:2011-07-08_karin-dewar-indentation-and-the-colon:colon-not-indentation-is-the-dewar-contribution`
  Guido corrects an earlier account: the Dewar story is the origin of the colon in ABC (and hence Python), not of the indentation. He reports this from Lambert Meertens' email.
  > Karin Dewar provided the inspiration for the use  of the colon in ABC (and hence in Python) leading up to the indentation, not for indentation itself.

- **16:13** Guido van Rossum [written: 2011-07-08_karin-dewar-indentation-and-the-colon.md line 15] `written:2011-07-08_karin-dewar-indentation-and-the-colon:colon-resolves-the-for-line-misunderstanding`
  Meertens recounts the Jabłonna design session where Robert Dewar's wife, reading a syntax, asked whether 'FOR i ...' applied to the following lines and not just that line; the scientists realized a colon at the end of the line would have avoided the misunderstanding, which is how the colon was conceived.
  > here the scientists realized that the misunderstanding would have been avoided if there had been a colon at the end of that line.

- **16:13** Guido van Rossum [written: 2011-07-08_karin-dewar-indentation-and-the-colon.md line 10] `written:2011-07-08_karin-dewar-indentation-and-the-colon:indentation-to-make-text-neat-and-suggestive`
  Meertens states the origin of indentation in ABC was the desire for the program text to look neat and suggest its meaning, codifying a practice that was already common but not enforced.
  > the desire to have     the program text look neat and be suggestive of the meaning,     codifying what was already common practice but not enforced.

- **16:13** Guido van Rossum [written: 2011-07-08_karin-dewar-indentation-and-the-colon.md line 6] `written:2011-07-08_karin-dewar-indentation-and-the-colon:mandatory-indentation-in-B0-controlled-by-editor`
  Meertens reports that B0, the first design in the sequence leading to ABC, had non-optional indentation for grouping, added by a dedicated editor, with the user unable to turn it off or modify it; it was supplemented by BEGIN/END delimiters.
  > The indentation was supposed to be added, like pretty printing, by a     dedicated B editor, and the user had no control over this

- **16:13** Guido van Rossum [written: 2011-07-08_karin-dewar-indentation-and-the-colon.md line 10] `written:2011-07-08_karin-dewar-indentation-and-the-colon:removing-begin-end-influenced-by-plauger`
  Meertens notes the decision to remove the BEGIN...END "noise" may have been influenced by Plauger's [PL75], which advocated pure indentation for grouping.
  > The     decision to remove the noise of BEGIN ... END     may have been influenced by [PL75], which actually advocated using     pure indentation for grouping.

### 2013-10-24

- **08:44** Guido van Rossum [written: 2013-10-24_why-python-uses-0-based-indexing.md line 33] `written:2013-10-24_why-python-uses-0-based-indexing:adjacency-invariant`
  The decisive beauty is the invariant that for adjacent slices the first slice's end index equals the second slice's start index, illustrated by splitting a string at i and j into a[:i], a[i:j], a[j:].
  > the invariant that when two / slices are adjacent, the first slice's end index is the second slice's / start index is just too beautiful to ignore.

- **08:44** Guido van Rossum [written: 2013-10-24_why-python-uses-0-based-indexing.md line 12] `written:2013-10-24_why-python-uses-0-based-indexing:avoid-plus-minus-one-compensations`
  A criterion for a good notation is that these use cases be expressible without awkward +1 or -1 corrections.
  > It would be nice if both of these could be / expressed as without awkward +1 or -1 compensations.

- **08:44** Guido van Rossum [written: 2013-10-24_why-python-uses-0-based-indexing.md line 24] `written:2013-10-24_why-python-uses-0-based-indexing:closed-intervals-force-minus-one`
  Under 1-based indexing with closed intervals, the n items starting at i require the awkward a[i:i+n-1].
  > Using closed intervals, you'd have to / write a[i:i+n-1] for the n items starting at i.

- **08:44** Guido van Rossum [written: 2013-10-24_why-python-uses-0-based-indexing.md line 10] `written:2013-10-24_why-python-uses-0-based-indexing:common-slicing-use-cases`
  He frames the decision around the two most common slicing use cases: getting the first n items and getting the next n items starting at i, the former being a special case of the latter.
  > most common use cases for slicing are \"get the first n items\" and \"get / the next n items starting at i\"

- **08:44** Guido van Rossum [written: 2013-10-24_why-python-uses-0-based-indexing.md line 31] `written:2013-10-24_why-python-uses-0-based-indexing:fuzzy-memory-on-other-use-cases`
  When pushing the index:length convention against other use cases his memory is uncertain, but he believes the elegance of half-open intervals swayed him.
  > TBH / this is where my memory gets fuzzy, but I think I was swayed by the / elegance of half-open intervals.

- **08:44** Guido van Rossum [written: 2013-10-24_why-python-uses-0-based-indexing.md line 25] `written:2013-10-24_why-python-uses-0-based-indexing:index-length-notation-as-abc-did`
  An alternative he considered is a start-and-length (index:length) slice convention, which might suit 1-based indexing; ABC in fact did this with its own notation a@i|n.
  > So perhaps using the / slice length would be more elegant with 1-based indexing? ... And this is in fact what ABC did -- it used a different / notation so you could write a@i|n.

- **08:44** Guido van Rossum [written: 2013-10-24_why-python-uses-0-based-indexing.md line 23] `written:2013-10-24_why-python-uses-0-based-indexing:one-based-half-open-inelegant`
  With 1-based indexing, half-open intervals are not elegant; getting the first n elements forces either closed intervals or a start-and-length slice notation.
  > Using half-open intervals just isn't very elegant when / combined with 1-based indexing.

- **08:44** Guido van Rossum [written: 2013-10-24_why-python-uses-0-based-indexing.md line 3] `written:2013-10-24_why-python-uses-0-based-indexing:predecessors-pulled-both-ways`
  Python's two main predecessors pulled in opposite directions on indexing: ABC used 1-based, C used 0-based; his earlier languages (Algol, Fortran, Pascal) used 1-based or variable-based.
  > ABC, one of Python's predecessors, / used 1-based indexing, while C, the other big influence, used 0-based.

- **08:44** Guido van Rossum [written: 2013-10-24_why-python-uses-0-based-indexing.md line 6] `written:2013-10-24_why-python-uses-0-based-indexing:slice-notation-decided-indexing-base`
  Van Rossum attributes his choice of Python's indexing base largely to how slice notation would work out; slicing was the deciding issue.
  > I think that one of the issues that helped me decide / was slice notation.

- **08:44** Guido van Rossum [written: 2013-10-24_why-python-uses-0-based-indexing.md line 15] `written:2013-10-24_why-python-uses-0-based-indexing:zero-based-half-open-defaults-elegant`
  The combination Python adopted, 0-based indexing with half-open intervals and suitable defaults, makes those use cases come out cleanly as a[:n] and a[i:i+n].
  > Using / 0-based indexing, half-open intervals, and suitable defaults (as Python / ended up having), they are beautiful: a[:n] and a[i:i+n]

- **09:58** Guido van Rossum [written: 2013-10-24_origin-of-metaclasses-in-python.md line 21] `written:2013-10-24_origin-of-metaclasses-in-python:meta-type-as-its-own-type`
  The type of a type was always a special type object, a meta-type, recognized because it is its own type.
  > The type of a type was always a\nspecial type object, which you could call a meta-type, to be recognized\nbecause it was its own type.

- **09:58** Guido van Rossum [written: 2013-10-24_origin-of-metaclasses-in-python.md line 2] `written:2013-10-24_origin-of-metaclasses-in-python:metaclass-design-not-from-ruby`
  Python's metaclass design did not come from Ruby; the author corrects a speculation to the contrary.
  > whether Python's metaclass design came from Ruby. It did not.

- **09:58** Guido van Rossum [written: 2013-10-24_origin-of-metaclasses-in-python.md line 11] `written:2013-10-24_origin-of-metaclasses-in-python:new-style-classes-an-iteration`
  New-style classes were the second or third iteration of the metaclass idea in Python, which the author had written about in 1998.
  > New-style classes were just the second or third iteration of the idea.

- **09:58** Guido van Rossum [written: 2013-10-24_origin-of-metaclasses-in-python.md line 13] `written:2013-10-24_origin-of-metaclasses-in-python:new-style-classes-inspired-by-forman-danforth`
  The author was inspired to implement new-style classes by the book "Putting Metaclasses to Work" by Ira Forman and Scott Danforth.
  > I was inspired to implement new-style classes by a very\nspecific book, \"Putting Metaclasses to Work\" by Ira Forman and Scott\nDanforth

- **09:58** Guido van Rossum [written: 2013-10-24_origin-of-metaclasses-in-python.md line 5] `written:2013-10-24_origin-of-metaclasses-in-python:ruby-inspired-by-python`
  The author reports that Ruby was inspired by Python, citing what Matz told him: 20% Python, 80% Perl, with Larry Wall as his hero. (reported by Matz)
  > Ruby was in fact\ninspired by Python. Mats once told me that his inspiration was 20%\nPython, 80% Perl, and that Larry Wall is his hero.

- **09:58** Guido van Rossum [written: 2013-10-24_origin-of-metaclasses-in-python.md line 27] `written:2013-10-24_origin-of-metaclasses-in-python:smalltalk-bytecode-influence`
  Smalltalk's bytecode was a bigger influence on Python's bytecode, which the author had read about in a book by Adele Goldberg and others.
  > Smalltalk's bytecode was a bigger influence of Python's\nbytecode though.

- **09:58** Guido van Rossum [written: 2013-10-24_origin-of-metaclasses-in-python.md line 25] `written:2013-10-24_origin-of-metaclasses-in-python:smalltalk-metaclasses-different-and-late`
  The author was only vaguely aware of Smalltalk at the time and found its use of metaclasses, which differs from Python's or Ruby's, surprising when he read about it much later.
  > I was only vaguely aware of Smalltalk at the time; I\nremember being surprised by its use of metaclasses (which is quite different from that in Python or Ruby!) when I read about\nthem much later.

- **09:58** Guido van Rossum [written: 2013-10-24_origin-of-metaclasses-in-python.md line 17] `written:2013-10-24_origin-of-metaclasses-in-python:type-as-object-from-the-start`
  Even Python's original 1990 design held that 'type' was itself an object; every object's type pointer points to a special object whose data is C function pointers implementing behavior, like a C++ vtable.
  > even Python's original design (in 1990, published in\n1991) had the notion that 'type' was itself an object. The type pointer\nin any object has always been a pointer to a special object, whose\n\"data\" was a bunch of C function pointers implementing the behavior of\nother objects, similar to a C++ vtable.

### 2013-11-10

- **14:40** Guido van Rossum [written: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 91] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:adding-a-builtin-must-not-break-existing-code`
  Adding a new built-in (e.g. `bytes` in 2.6) must not invalidate existing code that used that name as a variable; such code stays valid.
  > In Python 2.6, we added a built-in function named 'bytes'... Should your code now be considered invalid? There's no reason for that, and in fact your code will be fine.

- **14:40** Guido van Rossum [written: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 80] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:allowing-builtin-reassignment-for-consistency-and-evolution`
  Assignment to built-in names is allowed by design, for reasons of consistency and the evolution of the language; nobody can list all built-ins, and forbidding their use as names would surprise programmers.
  > The answer is subtle, and has to do with consistency and evolution of the language.

- **14:40** Guido van Rossum [written: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 51] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:assignment-target-must-be-a-variable`
  The left-hand side of an assignment must be a variable; a literal is not one. The definition of variable is complex, covering d[k], (a, b), foo.bar but not f(), () or 42, and is shared with the del statement.
  > the left-hand side of the assignment operator (=) must be a variable, and a literal is not a variable. (The exact definition of variable is complex, since some things that look like expressions are also considered to be variables, such as d[k], (a, b), and foo.bar -- but not f() or () or 42.

- **14:40** Guido van Rossum [written: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 55] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:builtins-are-ordinary-names-to-the-parser`
  Originally None, like built-in types and exceptions, was just a built-in name; the parser gives these no special knowledge and treats them as identifiers looked up at interpretation time, producing the same parse tree as any name.
  > The parser had no special knowledge of None -- just like it doesn't have special knowledge of built-in types like int, float or str... All of these are treated by the parser as identifiers, and when your code is being interpreted they are looked up just like any other names

- **14:40** Guido van Rossum [written: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 69] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:builtins-are-reassignable`
  Because built-ins are ordinary names, code can reassign them (e.g. `int = float`), which lets one write confusing code.
  > if you really want to mess with your readers, you can write code that reassigns built-ins

- **14:40** Guido van Rossum [written: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 46] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:constant-versus-literal`
  A constant is distinct from a literal: an all-caps identifier like MAX_LEVELS is a convention the parser neither knows nor enforces, while 15 is a literal.
  > the all-caps form of the name suggests to the reader that it is probably not changed anywhere in the code... but this is just a convention, and the Python parser doesn't know about that convention, nor does it enforce it.

- **14:40** Guido van Rossum [written: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 15] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:keyword-cannot-name-a-variable`
  The defining property of a keyword is that it cannot be used to name a variable, function, class, etc.
  > The important thing to remember about keywords is that a keyword cannot be used to name a variable (or function, class, etc.).

- **14:40** Guido van Rossum [written: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 13] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:keyword-is-identifier-shaped-but-a-token`
  A keyword (reserved word) looks like an identifier but the parser treats it as a token of the language; an identifier is letters, digits and underscores not starting with a digit.
  > A keyword, in the context of defining the syntax of a language, also known as a reserved word, is something that looks like an identifier in the language, but from the parser's point of view act like a token of the language.

- **14:40** Guido van Rossum [written: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 17] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:literal-describes-a-constant-value`
  A literal is an element of an expression that describes a constant value, recognized by the parser, with subtle parsing rules.
  > A literal, on the other hand, is an element of an expression that describes a constant value... Literals are recognized by the parser, and the exact rules for how literals are parsed are often quite subtle.

- **14:40** Guido van Rossum [written: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 67] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:literals-parse-differently-from-names`
  Numeric and string literals produce a different parse tree from names, so `<name> = <name>` is accepted either way round while `<literal> = <name>` is rejected.
  > the parser treats numeric and string literals as different from identifiers... the first three will still be accepted by the parser (<name> = <name>), while the swapped version of the second set will be rejected (<literal> = <name> is invalid).

- **14:40** Guido van Rossum [written: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 97] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:new-builtins-are-cheap-to-add`
  Unlike keywords, new built-ins don't break working code, so adding them is cheap; the only price is a joker redefining one, which Guido judges minor among the many ways to write unreadable code.
  > at least we don't have to worry about breaking working code by merely adding something to the language. The (small) price we pay for this is the possibility that some joker intentionally redefines a built-in

- **14:40** Guido van Rossum [written: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 95] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:new-keywords-kill-or-reshape-features`
  Many proposed features were killed or modified because they would need a new keyword; adding one triggers a deprecation campaign a release ahead, with `from __future__ import` as an opt-in.
  > many proposed new features have been killed because they would require a new keyword; others have been modified to avoid that need.

- **14:40** Guido van Rossum [written: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 55] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:none-as-singleton-for-absence`
  None is a singleton object used throughout the language and library to represent the absence of some other value.
  > None is a singleton object (meaning there is only one None), used in many places in the language and library to represent the absence of some other value.

- **14:40** Guido van Rossum [written: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 101] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:none-keyword-decision-had-no-downside`
  Making None a keyword was decided because there was no downside (no code assigns to it) and it might speed up code a little or catch rare typos; the one-time cost to parser and docs was small.
  > In the end we decided that there was no downside to making None a keyword (there is no code that actually assigns to it) and it might make some code a tiny bit faster, or catch rare typos.

- **14:40** Guido van Rossum [written: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 99] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:none-made-keyword-for-social-reasons`
  None was eventually made a reserved word for mostly social reasons: it is so central that users were horrified assignment to it was allowed; a secondary concern was that evaluating None was slow, needing two dictionary lookups.
  > Why did we eventually make None a reserved word? Frankly, the reasons were perhaps mostly social... None is so central to using Python that you really can't be using Python without knowing about None.

- **14:40** Guido van Rossum [written: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 109] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:none-true-false-are-both-keywords-and-literals`
  None/True/False are both keywords (how the parser recognizes them) and literals (their role in expressions, standing for constant values).
  > My answer is that they are both. They are keywords because that's how the parser recognizes them. They are literals because that's their role in expressions and because they stand for constant values.

- **14:40** Guido van Rossum [written: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 93] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:reserved-words-impose-a-global-cost`
  Every reserved word must be known by everyone using Python, since it can never be used as a name anywhere; therefore the list is kept small and new keywords are added reluctantly.
  > everyone using Python has to know about all the reserved words in the language... For this reason, we try to keep the list of reserved words small, and the core developers hem and haw a lot before adding a new reserved word

- **14:40** Guido van Rossum [written: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 105] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:true-false-became-keywords-in-python-3`
  Once defining one's own True/False became frowned upon, Python 3's cleanup made True and False keywords by analogy to None.
  > by the time Python 3 came around, when we looked at opportunities for cleaning up the language, we found that it was logical to make True and False keywords, by analogy to None.

- **14:40** Guido van Rossum [written: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:true-false-introduced-as-builtins-not-keywords`
  True and False had to be introduced as built-in constants rather than keywords because people had defined their own True/False constants, and backward compatibility (including running on earlier Python versions) forced that choice.
  > we definitely did not want to break any packages that were defining their own True and False constants... essentially our hand was forced in this case, and we had to introduce True and False as built-in constants, not as keywords.

### 2013-11-11

- **16:29** Guido van Rossum [written: 2013-11-11_the-history-of-bool-true-and-false.md line 16] `written:2013-11-11_the-history-of-bool-true-and-false:bool-added-in-bugfix-release-2-2-1`
  bool, True and False were also added in Python 2.2.1, which was a bugfix release, to ease backporting of code developed for Python 2.3.
  > Added new builtin function bool() and new builtin constants True and ... False to ease backporting of code developed for Python 2.3.

- **16:29** Guido van Rossum [written: 2013-11-11_the-history-of-bool-true-and-false.md line 22] `written:2013-11-11_the-history-of-bool-true-and-false:bool-differs-between-2-2-1-and-2-3`
  The bool in 2.2.1 differed from 2.3: in 2.3 bool is a new type, while in 2.2.1 bool() is a built-in function and True/False are just ints equal to 1 and 0.
  > in 2.3, bool is a new type; in 2.2.1, bool() is a built-in function and the constants are just ints.

- **16:29** Guido van Rossum [written: 2013-11-11_the-history-of-bool-true-and-false.md line 4] `written:2013-11-11_the-history-of-bool-true-and-false:bool-formally-introduced-2-3-pep-285`
  The bool type was formally introduced in Python 2.3 as a new type with two constants, through PEP 285.
  > It was formally introduced in Python 2.3, as a new type with two constants, and the type was introduced in PEP 285 ("Adding a bool type").

- **16:29** Guido van Rossum [written: 2013-11-11_the-history-of-bool-true-and-false.md line 24] `written:2013-11-11_the-history-of-bool-true-and-false:breakneck-development-pace`
  The compressed chronology of PEP 285's creation, acceptance and finalization against the release dates reflects a much faster pace of doing things than a decade later.
  > That's a breakneck pace compared to how we do things a decade later!

- **16:29** Guido van Rossum [written: 2013-11-11_the-history-of-bool-true-and-false.md line 22] `written:2013-11-11_the-history-of-bool-true-and-false:feature-in-bugfix-release-regret`
  Adding a new feature in a bugfix release was the most criticized such instance and would not be done now; expressed as a change in practice.
  > This was the last (and the most criticized) time we added a new feature in a bugfix release -- we'd never do that these days.

- **16:29** Guido van Rossum [written: 2013-11-11_the-history-of-bool-true-and-false.md line 2] `written:2013-11-11_the-history-of-bool-true-and-false:true-false-not-reserved-words`
  When True and False were introduced, they were deliberately not made reserved words; Guido notes he was writing up the reasons for this choice.
  > Writing up the reasons why True and False, when introduced, weren't reserved words

### 2018-05-12

- **09:37** Guido van Rossum [written: 2018-05-12_the-origins-of-pgen.md line 10] `written:2018-05-12_the-origins-of-pgen:avoided-advanced-techniques`
  He did not use more advanced parsing techniques, being unfamiliar with them or judging them too inefficient, as he believes most parser workers did then.
  > I was not familiar with more advanced techniques, or I deemed them too inefficient.

- **09:37** Guido van Rossum [written: 2018-05-12_the-origins-of-pgen.md line 49] `written:2018-05-12_the-origins-of-pgen:ebnf-to-bnf-not-improvement`
  Converting EBNF to BNF and working from there would cause awkward extra parse-tree node types, so he does not think that would have been an improvement.
  > Converting EBNF to BNF and taking it from there would cause awkward extra parse tree node types, so I don't think that would have been an improvement.

- **09:37** Guido van Rossum [written: 2018-05-12_the-origins-of-pgen.md line 12] `written:2018-05-12_the-origins-of-pgen:no-generator-for-lexer`
  He chose not to use a generator for the lexer: he thought less of Lex than of Yacc (the Lex he knew would segfault on tokens longer than 255 bytes), and figured indentation would be hard to teach a lexer generator.
  > For the lexer I decided I would not use a generator ... the version of Lex that I was familiar with would just segfault when trying to scan a token longer than 255 bytes (really!). Also I figured that indentation would be hard to teach to a lexer generator.

- **09:37** Guido van Rossum [written: 2018-05-12_the-origins-of-pgen.md line 23] `written:2018-05-12_the-origins-of-pgen:parsing-engine-and-empty-productions`
  He believes the parsing engine still works with parsing tables derived from such rules through the regex -> NFA -> DFA transformation, with a requirement of no empty productions.
  > the parsing engine ... still works with parsing tables derived from such rules through the regex -> NFA -> DFA transformation; I think the requirement not to have any empty productions was required here.

- **09:37** Guido van Rossum [written: 2018-05-12_the-origins-of-pgen.md line 6] `written:2018-05-12_the-origins-of-pgen:pgen-first-code-for-python`
  The original pgen was the first code written for Python, though the lexer had to come first because pgen and Python share a lexer.
  > The original was actually the first code I wrote for Python. Although technically I had to write the lexer first (pgen and Python share their lexer, pgen just doesn't have any uses for most tokens).

- **09:37** Guido van Rossum [written: 2018-05-12_the-origins-of-pgen.md line 14] `written:2018-05-12_the-origins-of-pgen:pgen2-origin-at-elemental`
  pgen2 arose at a startup (Elemental Security) where, tasked to design a custom security-assertion language, he designed something vaguely like Python, implemented in Python, and rewrote pgen's exact algorithm in Python using tokenize.py as the lexer.
  > I decided to design something vaguely like Python, implemented in Python, and decided that I wanted to reuse pgen, but with a backend in Python, using tokenize.py as the lexer. So I just rewrote the exact algorithm from pgen in Python

- **09:37** Guido van Rossum [written: 2018-05-12_the-origins-of-pgen.md line 14] `written:2018-05-12_the-origins-of-pgen:pgen2-reused-for-2to3`
  Because pgen2's input format was identical to the original pgen, it was easy to generate a Python parser by feeding it the Grammar file, and the open-sourced tooling was later used for 2to3.
  > it made sense to use those tools for 2to3. (It was easy to generate a Python parser with it because the input format was identical to the original pgen -- I just had to feed the Grammar file into the tool. :-)

- **09:37** Guido van Rossum [written: 2018-05-12_the-origins-of-pgen.md line 44] `written:2018-05-12_the-origins-of-pgen:power-unchanged-ll1`
  The regex notation did not change the parsing power beyond LL(1), nor reduce it; by "regular expressions" he meant the EBNF conventions, noting EBNF may not have been a well-defined notation at the time.
  > It certainly did not change the power beyond LL(1), nor did it reduce the power. And yes by "regular expressions" I meant the EBNF conventions -- I'm not sure that at the time "EBNF" was a well-defined notation

- **09:37** Guido van Rossum [written: 2018-05-12_the-origins-of-pgen.md line 63] `written:2018-05-12_the-origins-of-pgen:python38-drops-c-pgen`
  Python 3.8 will drop the C version of pgen in favor of a tweaked version of pgen2.
  > UPDATE March 2019: Python 3.8 will drop the C version of pgen, in favor of a tweaked version of pgen2.

- **09:37** Guido van Rossum [written: 2018-05-12_the-origins-of-pgen.md line 38] `written:2018-05-12_the-origins-of-pgen:regex-for-readability`
  The reason he used regular expressions was probably to make the grammar easier to read: after resolving conflicts with rewrites the grammar was not easy to read, and regex avoided helper rules with awkward names, with [optional] and repeated* parts closer to how he thinks about a language's syntax.
  > the reason I used regular expressions was probably to make the grammar easier to read ... no helper rules with awkward names, and [optional] parts or repeated* parts are closer to how I think about a typical language's syntax.

- **09:37** Guido van Rossum [written: 2018-05-12_the-origins-of-pgen.md line 8] `written:2018-05-12_the-origins-of-pgen:regex-instead-of-bnf`
  Building on LL(1) parser-generation and the Dragon book's regex-to-DFA technique, he wanted to try one improvement: using regular expressions instead of the standard BNF format, and from combining these pgen was born.
  > I had one improvement over that that I wanted to try out: using regular expressions (sort of) instead of the standard BNF format. The Dragon book had also taught me how to turn regular expressions into DFAs, so I combined all that and pgen was born.

- **09:37** Guido van Rossum [written: 2018-05-12_the-origins-of-pgen.md line 19] `written:2018-05-12_the-origins-of-pgen:regex-to-resolve-conflicts`
  Looking back, he may have seen the regex approach as a new way of addressing grammar conflicts without adding helper rules, e.g. rewriting left-factoring (A -> X | X Y Z becoming A -> X B; B -> Y Z | empty) instead as A -> X [Y Z].
  > I may have seen this as a new (to me) way of addressing the various conflicts that may occur without adding helper rules. E.g. what that page calls left-factoring ... I would rewrite instead as A -> X [Y Z].

- **09:37** Guido van Rossum [written: 2018-05-12_the-origins-of-pgen.md line 4] `written:2018-05-12_the-origins-of-pgen:two-pgens-c-and-python`
  There are two parser generators for Python, the original written in C and a later rewrite in Python living under lib2to3/pgen2, both written by the author.
  > There are actually two pgens. The original, in C, and a rewrite in Python, under lib2to3/pgen2.

- **09:37** Guido van Rossum [written: 2018-05-12_the-origins-of-pgen.md line 28] `written:2018-05-12_the-origins-of-pgen:variable-number-of-children`
  Another idea was that parse-tree nodes have a variable number of children (e.g. A -> X [Y Z] yields a node with 1 or 3 children), with a simple check in the code generator to tell which alternative was parsed.
  > the parse tree nodes produced by the parsing engine would have a variable number of children ... A simple check in the code generator would then be needed to determine which alternative the parser had encountered.

- **09:37** Guido van Rossum [written: 2018-05-12_the-origins-of-pgen.md line 8] `written:2018-05-12_the-origins-of-pgen:why-own-parser-generator`
  The author wrote his own parser generator because the available options were sparse (Yacc, or hand-written parsers) and he disliked Yacc, finding it hard to reason about the limits of an LALR(1) grammar.
  > The reason for writing my own parser generator was that at the time the landscape of parser generators ... was pretty sparse ... I had used Yacc in college ... but for some reason I didn't like it much; IIRC I found it hard to reason about what the limitations on an LALR(1) grammar would be.

- **09:37** Guido van Rossum [written: 2018-05-12_the-origins-of-pgen.md line 53] `written:2018-05-12_the-origins-of-pgen:would-choose-more-powerful-engine`
  Doing it over, he might choose a more powerful parsing engine such as LALR(1)/Yacc/Bison, since several grammar areas need more power than LL(1), e.g. keyword args where 'arg: [NAME =] expr' is not valid because NAME is in the FIRST-set of expr; LALR(1) can handle it, but keyword args came years later and he did not want to redo the parser then.
  > If I had to do it all over again I might opt for a more powerful parsing engine, perhaps a version of LALR(1) ... the rule 'arg: [NAME =] expr' is not a valid rule, since NAME occurs in the FIRST-set of expr and the algorithm doesn't handle that. IIRC LALR(1) can handle it. But keyword args were several years in the future ... and I didn't want to redo the parser at that point.

## Inputs

| file | prompt | model | effort | rows | quotes found | sha256 |
|---|---|---|---|---|---|---|
| 2009-01-13_introduction-and-overview_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 13 | 13/13 | 4272696a3316 |
| 2009-01-20_a-brief-timeline-of-python_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 0 | 0/0 | b1874177d1fa |
| 2009-01-20_personal-history-part-1-cwi_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 12 | 12/12 | 24e086543c83 |
| 2009-01-27_personal-history-part-2-cnri-and-beyond_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 3 | 3/3 | a71210a102d5 |
| 2009-02-03_early-language-design-and-development_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 18 | 18/18 | 8080d14d8cbb |
| 2009-02-10_python-s-use-of-dynamic-typing_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 9 | 8/9 | a929641e7bc8 |
| 2009-02-18_adding-support-for-user-defined-classes_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 28 | 28/28 | 8a92f9d20b9f |
| 2009-02-27_first-class-everything_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 8 | 8/8 | 80e2c8011b86 |
| 2009-03-03_how-everything-became-an-executable-stat_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 5 | 5/5 | ddb2ad924401 |
| 2009-03-06_how-exceptions-came-to-be-classes_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 12 | 12/12 | 18a9ce593a50 |
| 2009-03-10_the-problem-with-integer-division_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 11 | 11/11 | 91c912f407d5 |
| 2009-03-17_dynamically-loaded-modules_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 8 | 8/8 | b0194139bb17 |
| 2009-03-31_the-great-or-grand-renaming_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 8 | 8/8 | fe8449f48626 |
| 2009-04-21_origins-of-python-s-functional-features_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 20 | 19/20 | 44eaef6a69b3 |
| 2009-04-24_metaclasses-and-extension-classes-a-k-a-_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 14 | 14/14 | 4c7e7d6ac32a |
| 2010-06-21_import-antigravity_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 2 | 2/2 | d6b2b0998433 |
| 2010-06-21_new-style-classes_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 11 | 10/11 | caa9f87400a8 |
| 2010-06-21_the-inside-story-on-new-style-classes_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 18 | 18/18 | 35dd45ff70f5 |
| 2010-06-23_method-resolution-order_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 17 | 17/17 | adf1d84253b6 |
| 2010-06-29_from-list-comprehensions-to-generator-ex_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 19 | 19/19 | e0ff2a2fe9f9 |
| 2010-08-24_why-python-s-integer-division-floors_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 11 | 10/11 | d2d1cb8d75e2 |
| 2011-07-08_karin-dewar-indentation-and-the-colon_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 7 | 6/7 | 2fd70776a174 |
| 2013-10-24_origin-of-metaclasses-in-python_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 8 | 8/8 | 72090f8d18a0 |
| 2013-10-24_why-python-uses-0-based-indexing_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 10 | 10/10 | ed76b62e76be |
| 2013-11-10_the-story-of-none-true-and-false-and-an-_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 19 | 18/19 | a8cb1663b824 |
| 2013-11-11_the-history-of-bool-true-and-false_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 6 | 6/6 | 45dc9214d685 |
| 2018-05-12_the-origins-of-pgen_extract_ideas_text_v1_claude-code_opus_ideas.md | extract_ideas_text_v1 | opus | low | 16 | 15/16 | c57612b1f374 |
