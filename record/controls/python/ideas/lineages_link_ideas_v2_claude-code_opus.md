# Lineages of the ideas about Luthier

Written by `scripts/link_ideas.py` (link_ideas v1) for Luciano and for the distillation. Prompt `link_ideas_v2`
(sha256 a04a21445ebf), model opus at effort low via claude-code (2.1.197 (Claude Code)); 3 calls. Input: `record/controls/python/ideas/timeline.jsonl`, last read with sha256
a50956041718. Who said an idea first and whether Luciano adopted a model's idea are computed from the rows' times and authors, not by the model.

Rows: 313 in the timeline; placed 313, unplaced 0, pending 0. Lineages: 156.

| scope | first said by Guido van Rossum |
|---|---|
| language | 132 |
| method | 7 |
| other | 17 |

First said by a model and then taken up by Luciano: 0.

## Lineages, by first appearance

### L-concise (language)

Seemingly complicated tasks can often be expressed in very little Python code.

first 2009-01-13 09:17 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-01-13

- 2009-01-13 09:17 Guido van Rossum states [2009-01-13_introduction-and-overview.md line 32] `written:2009-01-13_introduction-and-overview:expressiveness-little-code`: "seemingly complicated tasks can often be expressed with very little code"

### L-dynamic-typing (language)

Python is dynamically typed: variables are names referring to objects, need no declaration, and all type checking happens at run time.

first 2009-01-13 09:17 by Guido van Rossum; 3 rows, 3 witnesses, 2 days, last 2009-02-10

- 2009-01-13 09:17 Guido van Rossum states [2009-01-13_introduction-and-overview.md line 20] `written:2009-01-13_introduction-and-overview:dynamic-typing-names-refer-to-objects`: "In Python, variables are simply names that refer to objects. Variables do not need to be declared before they are assigned and they can even change type in the…"
- 2009-02-10 11:27 Guido van Rossum refines [2009-02-10_python-s-use-of-dynamic-typing.md line 8] `written:2009-02-10_python-s-use-of-dynamic-typing:python-drops-compile-time-checking`: "Python simply drops the compile-time type checking completely. This is entirely in line with Python’s “corner-cutting” philosophy as it’s a simplification of t…"
- 2009-02-10 11:27 Guido van Rossum restates [2009-02-10_python-s-use-of-dynamic-typing.md line 2] `written:2009-02-10_python-s-use-of-dynamic-typing:python-is-dynamically-typed`: "In contrast, Python is dynamically typed. The Python compiler is blissfully unaware of the types used in a program, and all type checking is done at run time."

### L-exceptions-errorhandling (language)

Python handles errors through exceptions, raised and caught with try/except/finally.

first 2009-01-13 09:17 by Guido van Rossum; 2 rows, 2 witnesses, 2 days, last 2009-03-06

- 2009-01-13 09:17 Guido van Rossum states [2009-01-13_introduction-and-overview.md line 24] `written:2009-01-13_introduction-and-overview:non-resumable-exceptions`: "For error handling, Python uses (non-resumable) exceptions."
- 2009-03-06 09:26 Guido van Rossum restates [2009-03-06_how-exceptions-came-to-be-classes.md line 2] `written:2009-03-06_how-exceptions-came-to-be-classes:exceptions-for-error-handling`: "Early on, I knew I wanted Python to use exceptions for error handling."

### L-first-class (language)

Every object that can be named in Python is first class, with equal status: assignable, passable, storable in data structures.

first 2009-01-13 09:17 by Guido van Rossum; 2 rows, 2 witnesses, 2 days, last 2009-02-27

- 2009-01-13 09:17 Guido van Rossum states [2009-01-13_introduction-and-overview.md line 26] `written:2009-01-13_introduction-and-overview:everything-first-class`: "In Python, all objects that can be named are said to be "first class.""
- 2009-02-27 11:59 Guido van Rossum restates [2009-02-27_first-class-everything.md line 4] `written:2009-02-27_first-class-everything:first-class-everything`: "One of my goals for Python was to make it so that all objects were "first class." By this, I meant that I wanted all objects that could be named in the languag…"

### L-for-iterable (language)

Python's for statement loops over any iterable object rather than over a numeric index.

first 2009-01-13 09:17 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-01-13

- 2009-01-13 09:17 Guido van Rossum states [2009-01-13_introduction-and-overview.md line 24] `written:2009-01-13_introduction-and-overview:for-loops-over-iterables`: "a high-level for statement that loops over any "iterable" object"

### L-general-purpose (language)

Python is a general purpose language in the lineage of Lisp or Smalltalk, not merely a scripting language.

first 2009-01-13 09:17 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-01-13

- 2009-01-13 09:17 Guido van Rossum states [2009-01-13_introduction-and-overview.md line 4] `written:2009-01-13_introduction-and-overview:python-general-purpose-not-scripting`: "Although it is often viewed as a "scripting" language, it is really a general purpose programming language along the lines of Lisp or Smalltalk"

### L-immutable-primitives (language)

Python's primitive built-in types (Booleans, numbers, strings) are immutable.

first 2009-01-13 09:17 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-01-13

- 2009-01-13 09:17 Guido van Rossum states [2009-01-13_introduction-and-overview.md line 22] `written:2009-01-13_introduction-and-overview:immutable-primitive-types`: "These are all immutable types, meaning that values are represented by objects that cannot be modified after their creation."

### L-impl-bytecode (language)

Python is implemented as a bytecode compiler plus a stack-based interpreter written in C, with compilation done implicitly as modules load.

first 2009-01-13 09:17 by Guido van Rossum; 2 rows, 2 witnesses, 2 days, last 2009-02-18

- 2009-01-13 09:17 Guido van Rossum states [2009-01-13_introduction-and-overview.md line 49] `written:2009-01-13_introduction-and-overview:bytecode-compiler-and-interpreter`: "Python is typically implemented using a combination of a bytecode compiler and interpreter. Compilation is implicitly performed as modules are loaded, and seve…"
- 2009-02-18 11:25 Guido van Rossum restates [2009-02-18_adding-support-for-user-defined-classes.md line 4] `written:2009-02-18_adding-support-for-user-defined-classes:c-centric-object-implementation`: "Python is implemented in C as a classic stack-based byte code interpreter or "virtual machine" along with a collection of primitive types also implemented in C…"

### L-indentation (language)

Python groups statements by indentation instead of braces, an idea taken from ABC that predates it.

first 2009-01-13 09:17 by Guido van Rossum; 7 rows, 5 witnesses, 3 days, last 2011-07-08

- 2009-01-13 09:17 Guido van Rossum states [2009-01-13_introduction-and-overview.md line 11] `written:2009-01-13_introduction-and-overview:indentation-for-grouping`: "instead of using braces for statement grouping, it uses indentation"
- 2009-02-03 10:53 Guido van Rossum refines [2009-02-03_early-language-design-and-development.md line 6] `written:2009-02-03_early-language-design-and-development:indentation-from-abc`: "Python's use of indentation comes directly from ABC, but this idea didn't originate with ABC--it had already been promoted by Donald Knuth and was a well-known…"
- 2011-07-08 16:13 Guido van Rossum refines [2011-07-08_karin-dewar-indentation-and-the-colon.md line 10] `written:2011-07-08_karin-dewar-indentation-and-the-colon:B-first-published-language-with-indentation-grouping`: "As far as I am aware, B was the first actually published (and implemented) language to use indentation for grouping."
- 2011-07-08 16:13 Guido van Rossum refines [2011-07-08_karin-dewar-indentation-and-the-colon.md line 8] `written:2011-07-08_karin-dewar-indentation-and-the-colon:begin-end-superfluous-under-mandatory-indentation`: "the latter delimiters were also dropped in B2, leaving pure indentation as the sole indicator of grouping."
- 2011-07-08 16:13 Guido van Rossum refines [2011-07-08_karin-dewar-indentation-and-the-colon.md line 10] `written:2011-07-08_karin-dewar-indentation-and-the-colon:indentation-to-make-text-neat-and-suggestive`: "the desire to have the program text look neat and be suggestive of the meaning, codifying what was already common practice but not enforced."
- 2011-07-08 16:13 Guido van Rossum refines [2011-07-08_karin-dewar-indentation-and-the-colon.md line 6] `written:2011-07-08_karin-dewar-indentation-and-the-colon:mandatory-indentation-in-B0-controlled-by-editor`: "The indentation was supposed to be added, like pretty printing, by a dedicated B editor, and the user had no control over this"
- 2011-07-08 16:13 Guido van Rossum refines [2011-07-08_karin-dewar-indentation-and-the-colon.md line 10] `written:2011-07-08_karin-dewar-indentation-and-the-colon:removing-begin-end-influenced-by-plauger`: "The decision to remove the noise of BEGIN ... END may have been influenced by [PL75], which actually advocated using pure indentation for grouping."

### L-multiple-impls (language)

Besides the C reference implementation, Python has several other implementations (Jython on the JVM, IronPython on .NET, PyPy, Stackless).

first 2009-01-13 09:17 by Guido van Rossum; 3 rows, 2 witnesses, 2 days, last 2009-01-27

- 2009-01-13 09:17 Guido van Rossum states [2009-01-13_introduction-and-overview.md line 49] `written:2009-01-13_introduction-and-overview:multiple-implementations`: "several other implementations have become popular. Jython is a version that runs on the JVM and has seamless Java integration."
- 2009-01-27 14:01 Guido van Rossum refines [2009-01-27_personal-history-part-2-cnri-and-beyond.md line 14] `written:2009-01-27_personal-history-part-2-cnri-and-beyond:ironpython-port-to-dotnet`: "Jim would also author IronPython, the Python port to Microsoft's .NET"
- 2009-01-27 14:01 Guido van Rossum refines [2009-01-27_personal-history-part-2-cnri-and-beyond.md line 14] `written:2009-01-27_personal-history-part-2-cnri-and-beyond:jython-python-in-and-for-java`: "the development of JPython (later shortened to Jython), a Python implementation in and for Java"

### L-oop-support (language)

Python has full object-oriented support: user-defined classes, inheritance, and run-time binding of methods.

first 2009-01-13 09:17 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-01-13

- 2009-01-13 09:17 Guido van Rossum states [2009-01-13_introduction-and-overview.md line 26] `written:2009-01-13_introduction-and-overview:full-oo-support`: "Python also has full support for object-oriented programming including user-defined classes, inheritance, and run-time binding of methods."

### L-stdlib (language)

Python's extensive, always-evolving standard library is one of the main reasons for its popularity.

first 2009-01-13 09:17 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-01-13

- 2009-01-13 09:17 Guido van Rossum states [2009-01-13_introduction-and-overview.md line 28] `written:2009-01-13_introduction-and-overview:extensive-standard-library`: "Python has an extensive standard library, which is one of the main reasons for its popularity."

### L-syntax-from-c (language)

Python's surface syntax borrows heavily from C in keywords, naming rules, and operators.

first 2009-01-13 09:17 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-01-13

- 2009-01-13 09:17 Guido van Rossum states [2009-01-13_introduction-and-overview.md line 11] `written:2009-01-13_introduction-and-overview:syntax-borrows-from-c`: "This is no accident---the syntax of Python borrows heavily from C."

### L-borrow-fix-abc (method)

The design program for Python was to keep what he liked from ABC while fixing its perceived problems, designing his own language rather than porting one.

first 2009-01-20 15:19 by Guido van Rossum; 2 rows, 1 witnesses, 1 days, last 2009-01-20

- 2009-01-20 15:19 Guido van Rossum states [2009-01-20_personal-history-part-1-cwi.md line 10] `written:2009-01-20_personal-history-part-1-cwi:borrow-from-abc-fix-its-problems`: "borrow everything I liked from ABC while at the same time fixing all its problems (as I perceived them)"
- 2009-01-20 15:19 Guido van Rossum restates [2009-01-20_personal-history-part-1-cwi.md line 10] `written:2009-01-20_personal-history-part-1-cwi:design-new-rather-than-port`: "I decided to design a language of my own which would borrow everything I liked from ABC while at the same time fixing all its problems (as I perceived them)"

### L-bridge-c-shell (other)

Python's original motivation was the need for a higher-level language to bridge the gap between C and the shell.

first 2009-01-20 15:19 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-01-20

- 2009-01-20 15:19 Guido van Rossum states [2009-01-20_personal-history-part-1-cwi.md line 8] `written:2009-01-20_personal-history-part-1-cwi:bridge-the-gap-between-c-and-the-shell`: "there was a need for a language that would “bridge the gap between C and the shell.” For a long time, this was Python’s main catchphrase."

### L-name-python (other)

The name Python was chosen under-analyzed as irreverent, fitting the tradition of naming languages after people, and only later associated with snakes.

first 2009-01-20 15:19 by Guido van Rossum; 3 rows, 2 witnesses, 1 days, last 2009-01-20

- 2009-01-20 15:19 Guido van Rossum states [2009-01-20_personal-history-part-1-cwi.md line 14] `written:2009-01-20_personal-history-part-1-cwi:name-irreverent-and-in-tradition`: "it fit in the tradition of naming languages after famous people, like Pascal, Ada, and Eiffel"
- 2009-01-20 15:19 Guido van Rossum refines [2009-01-20_personal-history-part-1-cwi.md line 16] `written:2009-01-20_personal-history-part-1-cwi:resisting-the-snake`: "For many years I resisted attempts to associate the language with snakes. I finally gave up when O’Reilly wanted to put a snake on the front of their first Pyt…"
- 2009-01-20 15:19 Guido van Rossum refines [2009-01-20_personal-history-part-1-cwi.md line 14] `written:2009-01-20_personal-history-part-1-cwi:under-analyze-the-name`: "rather than over-analyzing the naming problem, I decided to under-analyze it. I picked the first thing that came to mind"

### L-open-source-early (other)

Python's first public release used an MIT-style license, so it was open source before the term was coined.

first 2009-01-20 15:19 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-01-20

- 2009-01-20 15:19 Guido van Rossum states [2009-01-20_personal-history-part-1-cwi.md line 20] `written:2009-01-20_personal-history-part-1-cwi:open-source-before-the-term`: "Python was open source before the term was even invented by Eric Raymond and Bruce Perens in late 1997"

### L-pgen (other)

The first code written for Python was a simple LL(1) parser generator, pgen, still in the distribution and the least changed.

first 2009-01-20 15:19 by Guido van Rossum; 2 rows, 2 witnesses, 2 days, last 2018-05-12

- 2009-01-20 15:19 Guido van Rossum states [2009-01-20_personal-history-part-1-cwi.md line 18] `written:2009-01-20_personal-history-part-1-cwi:pgen-first-code-least-changed`: "the first piece of code I wrote for Python’s implementation was a simple LL(1) parser generator I called “pgen." ... still part of the Python source distributi…"
- 2018-05-12 09:37 Guido van Rossum restates [2018-05-12_the-origins-of-pgen.md line 6] `written:2018-05-12_the-origins-of-pgen:pgen-first-code-for-python`: "The original was actually the first code I wrote for Python. Although technically I had to write the lexer first (pgen and Python share their lexer, pgen just…"

### L-python-origins-cwi (other)

Python grew from experience at CWI: ABC gave the inspiration, Amoeba the motivation, the multimedia group its growth.

first 2009-01-20 15:19 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-01-20

- 2009-01-20 15:19 Guido van Rossum states [2009-01-20_personal-history-part-1-cwi.md line 6] `written:2009-01-20_personal-history-part-1-cwi:abc-inspiration-amoeba-motivation`: "ABC gave me the key inspiration for Python, Amoeba the immediate motivation, and the multimedia group fostered its growth"

### L-releases-cvs (method)

Encouraged by feedback, he kept a steady stream of releases and adopted CVS to track changes and share coding.

first 2009-01-20 15:19 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-01-20

- 2009-01-20 15:19 Guido van Rossum states [2009-01-20_personal-history-part-1-cwi.md line 22] `written:2009-01-20_personal-history-part-1-cwi:releases-driven-by-feedback`: "There was immediately a lot of feedback and with this encouragement I kept a steady stream of releases coming for the next few years"

### L-syntax-tastes (other)

His tastes in syntax were strongly influenced by Algol 60, Pascal, Algol 68, and ABC.

first 2009-01-20 15:19 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-01-20

- 2009-01-20 15:19 Guido van Rossum states [2009-01-20_personal-history-part-1-cwi.md line 10] `written:2009-01-20_personal-history-part-1-cwi:syntax-taste-from-algol-pascal-abc`: "my tastes in programming language syntax were strongly influenced by languages like Algol 60, Pascal, Algol 68 ..., and last but not least, ABC"

### L-why-not-shell (other)

The Bourne shell wouldn't do because Amoeba's primitive operations were finer-grained and different from the shell's.

first 2009-01-20 15:19 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-01-20

- 2009-01-20 15:19 Guido van Rossum states [2009-01-20_personal-history-part-1-cwi.md line 8] `written:2009-01-20_personal-history-part-1-cwi:amoeba-primitives-unlike-the-shell`: "Amoeba’s primitive operations were very different (and finer-grain) than the traditional primitive operations available in the Bourne shell"

### L-python-like-lisp (language)

Python has much in common with Lisp in deep structure despite being completely different at the surface syntactic level.

first 2009-01-27 14:01 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-01-27

- 2009-01-27 14:01 Guido van Rossum states [2009-01-27_personal-history-part-2-cnri-and-beyond.md line 2] `written:2009-01-27_personal-history-part-2-cnri-and-beyond:python-shares-much-with-lisp`: "Bob Kahn, was the first to point out to me how much Python has in common with Lisp, despite being completely different at a superficial (syntactic) level"

### L-abc-design-method (method)

ABC was designed by first doing a task analysis and then iterating with serious user testing.

first 2009-02-03 10:53 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-03

- 2009-02-03 10:53 Guido van Rossum states [2009-02-03_early-language-design-and-development.md line 4] `written:2009-02-03_early-language-design-and-development:abc-foremost-influence`: "Python's first and foremost influence was ABC... It was designed by first doing a task analysis of the programming task and then doing several iterations that…"

### L-colon (language)

The colon separating the lead-in clause from the indented block, invented by ABC's authors, was kept because user testing showed it clarifies the indentation for beginners.

first 2009-02-03 10:53 by Guido van Rossum; 3 rows, 3 witnesses, 2 days, last 2011-07-08

- 2009-02-03 10:53 Guido van Rossum states [2009-02-03_early-language-design-and-development.md line 6] `written:2009-02-03_early-language-design-and-development:colon-before-indented-block`: "ABC's authors did invent the use of the colon that separates the lead-in clause from the indented block. After early user testing without the colon, it was dis…"
- 2011-07-08 16:13 Guido van Rossum refines [2011-07-08_karin-dewar-indentation-and-the-colon.md line 2] `written:2011-07-08_karin-dewar-indentation-and-the-colon:colon-not-indentation-is-the-dewar-contribution`: "Karin Dewar provided the inspiration for the use of the colon in ABC (and hence in Python) leading up to the indentation, not for indentation itself."
- 2011-07-08 16:13 Guido van Rossum refines [2011-07-08_karin-dewar-indentation-and-the-colon.md line 15] `written:2011-07-08_karin-dewar-indentation-and-the-colon:colon-resolves-the-for-line-misunderstanding`: "here the scientists realized that the misunderstanding would have been avoided if there had been a colon at the end of that line."

### L-hashtable (language)

He replaced ABC's sorted-table (B-tree) mapping with a hash table, as faster and easier to implement.

first 2009-02-03 10:53 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-03

- 2009-02-03 10:53 Guido van Rossum states [2009-02-03_early-language-design-and-development.md line 10] `written:2009-02-03_early-language-design-and-development:hash-table-over-btree`: "I also replaced the sorted tables with a hash table implementation. I chose a hash table because I believed this to be faster and easier to implement than ABC'…"

### L-int-long-different-semantics (language)

Machine ints and longs had slightly different semantics: ints clipped on overflow and were treated as unsigned by bitwise/shift/conversion, longs always signed.

first 2009-02-03 10:53 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-03

- 2009-02-03 10:53 Guido van Rossum states [2009-02-03_early-language-design-and-development.md line 30] `written:2009-02-03_early-language-design-and-development:int-long-divergent-semantics`: "A more egregious error was that my implementation of integers and longs had slightly different semantics in certain cases!"

### L-list-flexible-array (language)

He changed ABC's sorted-bag list into a flexible array with insert/delete, giving users full control of ordering, with a sort method.

first 2009-02-03 10:53 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-03

- 2009-02-03 10:53 Guido van Rossum states [2009-02-03_early-language-design-and-development.md line 8] `written:2009-02-03_early-language-design-and-development:list-as-flexible-array`: "So I changed the list type into a flexible array with insert and delete operations, giving users complete control over the ordering of items in a list. A sort…"

### L-long-bignum (language)

He added an unbounded exact integer type, long, for the use case of arbitrary-precision numbers.

first 2009-02-03 10:53 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-03

- 2009-02-03 10:53 Guido van Rossum states [2009-02-03_early-language-design-and-development.md line 20] `written:2009-02-03_early-language-design-and-development:bignum-long-type`: "Feeling that there was still an important use case for unbounded exact numbers, I added a bignum data type, which I called long."

### L-long-suffix-violation (language)

Requiring a trailing L to mark longs violated the ABC-inspired philosophy of not making users care about uninteresting implementation details.

first 2009-02-03 10:53 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-03

- 2009-02-03 10:53 Guido van Rossum states [2009-02-03_early-language-design-and-development.md line 28] `written:2009-02-03_early-language-design-and-development:explicit-long-suffix-violates-philosophy`: "This is one area where Python violated the ABC-inspired philosophy of not requiring users to care about a uninteresting implementation details."

### L-machine-ints-common (language)

He did not want bignums for all integer operations: machine integers serve the common cases, bignums only serious math.

first 2009-02-03 10:53 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-03

- 2009-02-03 10:53 Guido van Rossum states [2009-02-03_early-language-design-and-development.md line 22] `written:2009-02-03_early-language-design-and-development:machine-ints-for-common-case`: "I didn't want to use bignums for all integer operations... I envisioned machine integers being used for all of the most-common cases and the extra range of big…"

### L-no-undefined-raise (language)

There are no undefined result values in Python: an exception is always raised when no correct value can be computed.

first 2009-02-03 10:53 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-03

- 2009-02-03 10:53 Guido van Rossum states [2009-02-03_early-language-design-and-development.md line 38] `written:2009-02-03_early-language-design-and-development:no-undefined-values`: "I decided that there should be no undefined result values in Python – instead, exceptions should always be raised when no correct return value can be computed."

### L-overflow-check (language)

Integer operations check for overflow and raise OverflowError rather than silently clipping; in hindsight they should instead promote the result to long.

first 2009-02-03 10:53 by Guido van Rossum; 3 rows, 3 witnesses, 1 days, last 2009-02-03

- 2009-02-03 10:53 Guido van Rossum states [2009-02-03_early-language-design-and-development.md line 34] `written:2009-02-03_early-language-design-and-development:overflow-check-cost-dwarfed`: "The extra cost of the overflow check would be dwarfed by the overhead I was already incurring due to the implementation choice of allocating a new object for t…"
- 2009-02-03 10:53 Guido van Rossum refines [2009-02-03_early-language-design-and-development.md line 32] `written:2009-02-03_early-language-design-and-development:overflow-raises-exception`: "I changed most arithmetic operations to raise an OverflowError exception when the result didn't fit... Had I not added this check, Python users would have undo…"
- 2009-02-03 10:53 Guido van Rossum corrects [2009-02-03_early-language-design-and-development.md line 36] `written:2009-02-03_early-language-design-and-development:should-have-promoted-to-long`: "In hindsight, I should have made integer operations that overflow promote their result to longs. This is the way that Python works today, but it took a long ti…"

### L-repr-valid-input (language)

Every data type, when printed or converted to a string, should be represented by an expression valid as input to the parser (a rule from ABC).

first 2009-02-03 10:53 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-03

- 2009-02-03 10:53 Guido van Rossum states [2009-02-03_early-language-design-and-development.md line 14] `written:2009-02-03_early-language-design-and-development:printed-repr-valid-input`: "One of the rules I took from ABC was that every data type, when printed or converted to a string, should be represented by an expression that was a valid input…"

### L-sequence-concept (language)

List, tuple, and string were generalized to a common sequence concept so length, indexing, slicing, and iteration work the same on any of them.

first 2009-02-03 10:53 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-03

- 2009-02-03 10:53 Guido van Rossum states [2009-02-03_early-language-design-and-development.md line 16] `written:2009-02-03_early-language-design-and-development:sequence-generalization`: "I decided to generalize these to a common concept, the sequence. This generalization made it so certain core operations such as getting the length (len(s)), in…"

### L-traditional-number-model (language)

Python chose a traditional numeric model of machine integers (C long) and binary floating point (C double) plus an arbitrary-precision long, rather than ABC's rationals.

first 2009-02-03 10:53 by Guido van Rossum; 2 rows, 2 witnesses, 2 days, last 2009-03-10

- 2009-02-03 10:53 Guido van Rossum states [2009-02-03_early-language-design-and-development.md line 18] `written:2009-02-03_early-language-design-and-development:machine-numbers-over-rationals`: "The rational numbers didn't pan out in my view... For Python I therefore chose a more traditional model with machine integers and machine binary floating point."
- 2009-03-10 13:31 Guido van Rossum restates [2009-03-10_the-problem-with-integer-division.md line 6] `written:2009-03-10_the-problem-with-integer-division:c-numerical-model`: "with Python, I relied on the other numerical model with which I was familiar, C. ... I chose to represent Python integers by a C long (guaranteeing at least 32…"

### L-tuple-from-abc (language)

He kept ABC's immutable tuple with packing and unpacking, adding array-like indexing and slicing.

first 2009-02-03 10:53 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-03

- 2009-02-03 10:53 Guido van Rossum states [2009-02-03_early-language-design-and-development.md line 12] `written:2009-02-03_early-language-design-and-development:tuple-kept-with-indexing`: "I kept ABC's immutable tuple data type... Since tuples are internally represented by arrays, I decided to add array-like indexing and slicing."

### L-tuple-syntax (language)

A trailing comma makes a one-tuple and "()" the empty tuple, so representations remain valid parser input.

first 2009-02-03 10:53 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-03

- 2009-02-03 10:53 Guido van Rossum states [2009-02-03_early-language-design-and-development.md line 14] `written:2009-02-03_early-language-design-and-development:empty-and-one-tuple-notation`: "I settled for an ugly but pragmatic approach where a trailing comma would turn an expression into a one-tuple and \"()\" would represent a zero-tuple... I felt…"

### L-abc-mixed-checking (language)

ABC used dynamic type checking for global variables and static for locals (locals dynamically checked too, to simplify implementation).

first 2009-02-10 11:27 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-10

- 2009-02-10 11:27 Guido van Rossum states [2009-02-10_python-s-use-of-dynamic-typing.md line 6] `written:2009-02-10_python-s-use-of-dynamic-typing:abc-compromise-global-dynamic-local-static`: "ABC uses dynamic type checking for global variables, but static type checking for local variables. To simplify the implementation, local variables are dynamica…"

### L-abc-runtime-checking (language)

ABC also re-checked argument types at run time, as a sanity check for its compiler and for readable error messages, needed because ABC is interactive.

first 2009-02-10 11:27 by Guido van Rossum; 3 rows, 2 witnesses, 1 days, last 2009-02-10

- 2009-02-10 11:27 Guido van Rossum states [2009-02-10_python-s-use-of-dynamic-typing.md line 4] `written:2009-02-10_python-s-use-of-dynamic-typing:abc-also-checked-types-at-runtime`: "ABC doesn't ... exclusively rely on static type checking to keep the program from crashing, but has a run-time library that checks the argument types for all o…"
- 2009-02-10 11:27 Guido van Rossum refines [2009-02-10_python-s-use-of-dynamic-typing.md line 6] `written:2009-02-10_python-s-use-of-dynamic-typing:interactivity-forces-dynamic-typing`: "the most important reason why ABC has run time type checking in addition to static type checking is that it is interactive."
- 2009-02-10 11:27 Guido van Rossum refines [2009-02-10_python-s-use-of-dynamic-typing.md line 4] `written:2009-02-10_python-s-use-of-dynamic-typing:runtime-checking-as-sanity-check-and-debugging-aid`: "This was done in part as a sanity check for the compiler’s type-checking algorithms ... The runtime library was also useful as a debugging aid since explicit r…"

### L-abc-static-typed (language)

ABC was statically typed, rejecting inconsistent programs, using type inference rather than explicit declarations.

first 2009-02-10 11:27 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-10

- 2009-02-10 11:27 Guido van Rossum states [2009-02-10_python-s-use-of-dynamic-typing.md line 2] `written:2009-02-10_python-s-use-of-dynamic-typing:abc-static-typing-with-inference`: "ABC is statically typed which meant that the ABC compiler analyzes the use of types in a program and decides whether they are used consistently. If not, the pr…"

### L-dynamic-no-return (language)

Once dynamic typing is chosen there is no going back, because in Python a type cannot be deduced from the form of an operation (x+y is ambiguous), unlike ABC's operations.

first 2009-02-10 11:27 by Guido van Rossum; 2 rows, 1 witnesses, 1 days, last 2009-02-10

- 2009-02-10 11:27 Guido van Rossum states [2009-02-10_python-s-use-of-dynamic-typing.md line 10] `written:2009-02-10_python-s-use-of-dynamic-typing:dynamic-typing-is-irreversible`: "once you decide on dynamic typing, there is no way to go back. ABC’s built-in operations were carefully designed so that the type of the arguments could be ded…"
- 2009-02-10 11:27 Guido van Rossum refines [2009-02-10_python-s-use-of-dynamic-typing.md line 10] `written:2009-02-10_python-s-use-of-dynamic-typing:operator-overloading-blocks-type-deduction`: "the expression “x+y” could be a string concatenation, a numeric addition, or an overloaded operation on user-defined types."

### L-assignment-instance-bootstrap (language)

Assignment can't default to an existing instance variable because of a bootstrap problem: there would be no way to create an instance variable the first time.

first 2009-02-18 11:25 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 50] `written:2009-02-18_adding-support-for-user-defined-classes:assign-if-exists-has-bootstrap-problem`: "Changing the semantics of assignment to assign to an instance variable if one already existed and to a local otherwise wouldn't work either, since this would c…"

### L-assignment-no-search (language)

Variable reference searches locals, globals, built-ins in order, but assignment never searches: it creates or replaces in the first (local) dictionary, with a global declaration the only override.

first 2009-02-18 11:25 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 40] `written:2009-02-18_adding-support-for-user-defined-classes:assignment-always-creates-in-first-dict`: "Python's assignment doesn't search for the variable name in the dictionaries, but simply adds or replaces the variable in the first dictionary in the search or…"

### L-class-body-statements (language)

Any valid Python statements may appear in a class body, extending from allowing variable assignments to allowing arbitrary executable code.

first 2009-02-18 11:25 by Guido van Rossum; 2 rows, 2 witnesses, 2 days, last 2009-03-03

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 71] `written:2009-02-18_adding-support-for-user-defined-classes:any-statements-in-class-body`: "Users are often surprised to learn that any sequence of valid Python statements can appear in a class body. This capability was really just a straightforward e…"
- 2009-03-03 12:02 Guido van Rossum refines [2009-03-03_how-everything-became-an-executable-statement.md line 6] `written:2009-03-03_how-everything-became-an-executable-stat:class-body-as-arbitrary-code`: "Rather than defining the class body as a series of function declarations only, it seemed to make sense to also allow regular variable assignments there. Howeve…"

### L-class-callable-factory (language)

The class object itself is callable for instantiation, the minimal solution requiring no new syntax, making each class its own factory.

first 2009-02-18 11:25 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 73] `written:2009-02-18_adding-support-for-user-defined-classes:callable-class-no-new-operator`: "making the class object itself callable was the right, "minimal" solution, requiring no new syntax... what I had done was simply to turn each class into its ow…"

### L-class-dictionary (language)

The class object holds what is shared across instances in a class dictionary keyed by name; any object there (not just methods) becomes a class variable.

first 2009-02-18 11:25 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 10] `written:2009-02-18_adding-support-for-user-defined-classes:class-dictionary-holds-methods`: "the set of methods of a class were stored in a dictionary whose keys are the method names. This, I dubbed the class dictionary."
- 2009-02-18 11:25 Guido van Rossum refines [2009-02-18_adding-support-for-user-defined-classes.md line 18] `written:2009-02-18_adding-support-for-user-defined-classes:class-variables-fall-out`: "there was no inherent reason why other kinds of objects couldn't be placed there as well. Thus, if objects such as integers or strings are stored in the class…"

### L-class-dynamic-modification (language)

Classes and instances can be modified dynamically by updating their dictionaries, though new-style classes require attribute assignment rather than using __dict__ directly.

first 2009-02-18 11:25 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 20] `written:2009-02-18_adding-support-for-user-defined-classes:dynamic-modifiability-of-classes-and-objects`: "it also makes it possible to modify a class dynamically... methods can be added or modified by simply updating the class dictionary after a class object has al…"
- 2009-02-18 11:25 Guido van Rossum refines [2009-02-18_adding-support-for-user-defined-classes.md line 84] `written:2009-02-18_adding-support-for-user-defined-classes:new-style-classes-constrain-dict`: "Eventually, new-style classes made it necessary to control changes to the class __dict__; you can still dynamically modify a class, but you must use attribute…"

### L-classbody-namespace-mechanism (language)

The class body is executed as statements in a new namespace whose resulting dictionary of locals initializes the class dictionary.

first 2009-02-18 11:25 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 71] `written:2009-02-18_adding-support-for-user-defined-classes:class-body-as-executed-namespace`: "it made sense to me to simply interpret the class body as a series of statements that were executed in a new namespace. The dictionary of this namespace would…"

### L-classes-added-late (other)

Classes were added late in Python's first year at CWI, but before the first public release.

first 2009-02-18 11:25 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 2] `written:2009-02-18_adding-support-for-user-defined-classes:classes-added-late-but-pre-release`: "classes were added late during Python's first year of development at CWI, though well before the first public release"

### L-dict-based-lookup (language)

Attribute access is plain dictionary operations: setting updates the instance dictionary; lookup checks the instance dictionary, then the class, then the base classes.

first 2009-02-18 11:25 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 12] `written:2009-02-18_adding-support-for-user-defined-classes:attribute-lookup-by-dictionary-search`: "Whenever changes are made to instance or class variables, those changes are simply reflected in the underlying dictionary object... lookups are performed in th…"

### L-instance-representation (language)

An instance is the simplest possible design: a built-in object holding a class reference and an instance dictionary.

first 2009-02-18 11:25 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 8] `written:2009-02-18_adding-support-for-user-defined-classes:instance-as-classref-plus-dict`: "I settled on the simplest possible design; a scheme where objects were represented by a new kind of built-in object that stored a class reference pointing to a…"

### L-introspection-type-object (language)

Python's introspection comes from making the type structure itself available at run time as an object like any other.

first 2009-02-18 11:25 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 4] `written:2009-02-18_adding-support-for-user-defined-classes:type-structure-as-runtime-object`: "Python's unique approach to introspection comes from its ability to make the type structure itself available at run-time as an object like all others."

### L-method-resolution-mro (language)

Method resolution walks the class then each base recursively, the depth-first, left-to-right rule, the default MRO in most versions.

first 2009-02-18 11:25 by Guido van Rossum; 2 rows, 2 witnesses, 2 days, last 2010-06-23

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 14] `written:2009-02-18_adding-support-for-user-defined-classes:depth-first-left-to-right-mro`: "This is commonly referred to as the depth-first, left-to-right rule, and has been the default method resolution order (MRO) used in most versions of Python. Mo…"
- 2010-06-23 10:41 Guido van Rossum restates [2010-06-23_method-resolution-order.md line 4] `written:2010-06-23_method-resolution-order:classic-mro-depth-first-left-to-right`: "when looking up a method, base classes were searched using a simple depth-first left-to-right scheme. The first matching object found during this search would…"

### L-modula3-method-model (language)

The self approach, and Python's import and exception syntax, resemble Modula-3, where x.m(args) equals f(x,args).

first 2009-02-18 11:25 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 59] `written:2009-02-18_adding-support-for-user-defined-classes:modula-3-precedent`: "This approach resembles something I had seen in Modula-3, which had already provided me with the syntax for import and exception handling... calling x.m(args)…"

### L-multiple-inheritance (language)

Class objects hold references to one or more base classes, supporting a simple-minded multiple inheritance.

first 2009-02-18 11:25 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 10] `written:2009-02-18_adding-support-for-user-defined-classes:multiple-inheritance-because-it-was-cheap`: "as long as I was going to support inheritance, I might as well support a simple-minded version of multiple inheritance. Thus, every class object could have one…"

### L-no-method-checking (language)

Method lookup does no error or conformance checking: an override need not match the base method's arguments, and the first method found is called.

first 2009-02-18 11:25 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 16] `written:2009-02-18_adding-support-for-user-defined-classes:no-conformance-checking`: "Python performs no advanced error checking or conformance checking when locating methods... no checks are performed to make sure that the redefined method has…"

### L-no-separate-method-syntax (language)

A major constraint was not to add a method-definition syntax different from the function syntax.

first 2009-02-18 11:25 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 24] `written:2009-02-18_adding-support-for-user-defined-classes:no-separate-method-syntax`: "A major design constraint was that I didn't want to add syntax for methods that differed from the syntax for functions. Refactoring the grammar and the byte co…"

### L-object-type-struct (language)

An object type is a statically allocated structure of function pointers, one per standard operation, with optional ones left NULL.

first 2009-02-18 11:25 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 4] `written:2009-02-18_adding-support-for-user-defined-classes:type-as-table-of-function-pointers`: "An object type is then represented by a statically allocated structure containing a series of function pointers, one for each standard operation... some operat…"

### L-permissive-vs-smalltalk (language)

Python's objects are more permissive than Smalltalk's, which restricts an object's attributes to those fixed at creation.

first 2009-02-18 11:25 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 20] `written:2009-02-18_adding-support-for-user-defined-classes:more-permissive-than-smalltalk`: "a feature that I later learned made Python's implementation of objects more permissive than that found in Smalltalk which restricts the set of attributes to th…"

### L-reject-instancevar-declarations (language)

Explicit instance-variable declarations were rejected (he had gotten this far with none), and lexical markers like a sigil did not appeal to him.

first 2009-02-18 11:25 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 50] `written:2009-02-18_adding-support-for-user-defined-classes:rejected-declarations-and-sigils`: "Requiring a special specification for instance variables, on the other hand, would have to be used almost everywhere in a class. Another possible solution woul…"

### L-self-explicit (language)

A method is just a function whose first argument, named self by convention, is the instance; explicit reference is the only way to reach instance variables, since implicit C++-style resolution is impossible without declarations.

first 2009-02-18 11:25 by Guido van Rossum; 3 rows, 3 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 54] `written:2009-02-18_adding-support-for-user-defined-classes:explicit-self-removes-special-cases`: "With explicit references, there is no need to have a special syntax for method definitions nor do you have to worry about complicated semantics concerning vari…"
- 2009-02-18 11:25 Guido van Rossum restates [2009-02-18_adding-support-for-user-defined-classes.md line 52] `written:2009-02-18_adding-support-for-user-defined-classes:explicit-self-the-decision`: "I decided to make such explicit references the only way to reference instance variables... rather than making the current object ("this") a special keyword, I…"
- 2009-02-18 11:25 Guido van Rossum refines [2009-02-18_adding-support-for-user-defined-classes.md line 34] `written:2009-02-18_adding-support-for-user-defined-classes:implicit-instance-variables-impossible`: "it quickly became clear that such an approach would be impossible because there was no way to elegantly distinguish instance variables from local variables in…"

### L-siebren-classes-suggestion (other)

Siebren van der Zee first suggested Python allow C++-like class definitions so objects could be implemented in Python, not only C.

first 2009-02-18 11:25 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 6] `written:2009-02-18_adding-support-for-user-defined-classes:objects-defined-in-python-the-motivation`: "I believe my colleague Siebren van der Zee was the first to suggest that Python should allow class definitions similar to those in C++ so that objects could al…"

### L-special-methods (language)

Special behaviors (initializers, destructors, operators) are handled by methods with special underscore names mapped to the C function-pointer tables, rather than new syntax.

first 2009-02-18 11:25 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2009-02-18

- 2009-02-18 11:25 Guido van Rossum states [2009-02-18_adding-support-for-user-defined-classes.md line 61] `written:2009-02-18_adding-support-for-user-defined-classes:dunder-special-method-names`: "I decided that these features could be handled by simply requiring the user to implement methods with special names such as __init__, __del__, and so forth. Th…"
- 2009-02-18 11:25 Guido van Rossum refines [2009-02-18_adding-support-for-user-defined-classes.md line 81] `written:2009-02-18_adding-support-for-user-defined-classes:special-methods-map-c-function-pointers`: "I mapped the various function pointers to special method names such as __getattr__, __add__, and __call__. There is a direct correspondence between these names…"

### L-bound-unbound-methods (language)

Calling a.spam() is a lookup returning a bound-method wrapper that stores the instance, then a call; bound and unbound methods share one internal type, and unbound methods were removed in Python 3000.

first 2009-02-27 11:59 by Guido van Rossum; 8 rows, 8 witnesses, 2 days, last 2010-06-21

- 2009-02-27 11:59 Guido van Rossum states [2009-02-27_first-class-everything.md line 23] `written:2009-02-27_first-class-everything:attribute-lookup-then-call`: "the execution of that statement actually occurs in two steps. First, a lookup of "a.spam" occurs. This returns a bound method--a callable object. Next, a funct…"
- 2009-02-27 11:59 Guido van Rossum refines [2009-02-27_first-class-everything.md line 19] `written:2009-02-27_first-class-everything:bound-method`: "a different callable object known as a "bound method." is used. ... this wrapper implicitly stores the original instance that was used to obtain the method."
- 2009-02-27 11:59 Guido van Rossum refines [2009-02-27_first-class-everything.md line 8] `written:2009-02-27_first-class-everything:methods-as-first-class-problem`: "there was still one subtle aspect of classes that I still needed to address---namely, the problem of making methods first class objects."
- 2009-02-27 11:59 Guido van Rossum refines [2009-02-27_first-class-everything.md line 21] `written:2009-02-27_first-class-everything:one-type-for-both-methods`: "the same internal object type is used to represent bound and unbound methods. One of the attributes of this object contains a reference to an instance. If set…"
- 2009-02-27 11:59 Guido van Rossum refines [2009-02-27_first-class-everything.md line 17] `written:2009-02-27_first-class-everything:unbound-method`: "I created a type of callable object known as an "unbound method." An unbound method was really just a thin wrapper around the function object that implemented…"
- 2009-02-27 11:59 Guido van Rossum corrects [2009-02-27_first-class-everything.md line 26] `written:2009-02-27_first-class-everything:unbound-methods-removed-py3k`: "In Python 3000, the concept of unbound methods has been removed ... the restriction that the first argument had to be an instance of A was rarely helpful in di…"
- 2010-06-21 11:18 Guido van Rossum refines [2010-06-21_the-inside-story-on-new-style-classes.md line 36] `written:2010-06-21_the-inside-story-on-new-style-classes:self-argument-mechanism`: "This is the fundamental mechanism by which methods in classes obtain their \"self\" argument."
- 2010-06-21 11:18 Guido van Rossum restates [2010-06-21_the-inside-story-on-new-style-classes.md line 38] `written:2010-06-21_the-inside-story-on-new-style-classes:x-f-equals-C-f-x`: "In other words, x.f(0) is equivalent to C.f(x, 0). This is a pretty fundamental equivalence in Python."

### L-common-c-struct (language)

All Python objects are based on one common C data structure used everywhere in the interpreter, which made first-class-everything simple.

first 2009-02-27 11:59 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-02-27

- 2009-02-27 11:59 Guido van Rossum states [2009-02-27_first-class-everything.md line 6] `written:2009-02-27_first-class-everything:common-c-data-structure`: "All of Python's objects were based on a common C data structure that was used everywhere in the interpreter. ... it just didn't matter if the structure happene…"

### L-everything-statement (language)

Every part of the language is an executable statement that can appear anywhere, which simplified the grammar (earlier it restricted declarative constructs to the top level).

first 2009-03-03 12:02 by Guido van Rossum; 3 rows, 3 witnesses, 1 days, last 2009-03-03

- 2009-03-03 12:02 Guido van Rossum refines [2009-03-03_how-everything-became-an-executable-statement.md line 4] `written:2009-03-03_how-everything-became-an-executable-stat:early-grammar-restricted-declarative-elements`: "grammar elements that had a “declarative flavor”, like import statements and function definitions, were allowed only at the top level in a module or script ...…"
- 2009-03-03 12:02 Guido van Rossum states [2009-03-03_how-everything-became-an-executable-statement.md line 2] `written:2009-03-03_how-everything-became-an-executable-stat:everything-is-an-executable-statement`: "every part of the language is an executable statement, including function and class definitions. That means that any statement can appear anywhere in a program."
- 2009-03-03 12:02 Guido van Rossum refines [2009-03-03_how-everything-became-an-executable-statement.md line 6] `written:2009-03-03_how-everything-became-an-executable-stat:uniform-statements-simplify-grammar-and-compiler`: "this enabled a simplification of the grammar, since now all uses of statements (whether indented or not) could share the same grammar rule, and hence the compi…"

### L-grammar-overpermissive (language)

The grammar accepted constructs the semantics didn't support, such as nested functions without nested scopes, which worked in broken ways until later fixed.

first 2009-03-03 12:02 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-03-03

- 2009-03-03 12:02 Guido van Rossum states [2009-03-03_how-everything-became-an-executable-statement.md line 8] `written:2009-03-03_how-everything-became-an-executable-stat:syntax-allows-what-semantics-did-not-support`: "the Python grammar technically allowed users to write things such as nested functions even though the underlying semantics of Python didn't support nested scop…"

### L-class-exceptions-introduced (language)

Class exceptions were introduced in Python 1.5 (1997) and became the recommended, modern approach, with string exceptions later removed.

first 2009-03-06 09:26 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2009-03-06

- 2009-03-06 09:26 Guido van Rossum states [2009-03-06_how-exceptions-came-to-be-classes.md line 12] `written:2009-03-06_how-exceptions-came-to-be-classes:class-exceptions-introduced-1997`: "In 1997, with Python 1.5, I introduced class exceptions into the language. Although class exceptions have been the recommended approach ever since, string exce…"
- 2009-03-06 09:26 Guido van Rossum restates [2009-03-06_how-exceptions-came-to-be-classes.md line 2] `written:2009-03-06_how-exceptions-came-to-be-classes:exceptions-as-classes-in-modern-languages`: "In modern languages (including modern Python :-), exceptions are defined in terms of user-defined classes."

### L-distinguish-exceptions (language)

Making exceptions work requires some scheme for distinguishing one kind of exception from another.

first 2009-03-06 09:26 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-03-06

- 2009-03-06 09:26 Guido van Rossum states [2009-03-06_how-exceptions-came-to-be-classes.md line 2] `written:2009-03-06_how-exceptions-came-to-be-classes:scheme-to-identify-kinds-of-exceptions`: "a critical part of making exceptions work is to come up with some kind of scheme for identifying different kinds of exceptions."

### L-exception-identity-nameclash (language)

Exceptions were given identity semantics (distinct string objects are distinct exceptions, referenced by name not value) to avoid name clashes across modules, influenced by Modula-3's unique exception tokens and predating string interning.

first 2009-03-06 09:26 by Guido van Rossum; 4 rows, 2 witnesses, 1 days, last 2009-03-06

- 2009-03-06 09:26 Guido van Rossum states [2009-03-06_how-exceptions-came-to-be-classes.md line 8] `written:2009-03-06_how-exceptions-came-to-be-classes:avoid-name-clashes-between-modules`: "The main reason however is that I worried about name clashes between unrelated exceptions defined in different modules. I intended the usage pattern to strictl…"
- 2009-03-06 09:26 Guido van Rossum refines [2009-03-06_how-exceptions-came-to-be-classes.md line 6] `written:2009-03-06_how-exceptions-came-to-be-classes:identity-not-value-semantics`: "I chose semantics where different string objects would represent different exceptions, even if they had the same value ... The idea was that exceptions would a…"
- 2009-03-06 09:26 Guido van Rossum refines [2009-03-06_how-exceptions-came-to-be-classes.md line 8] `written:2009-03-06_how-exceptions-came-to-be-classes:literal-interning-came-later`: "(This was also long before certain string literals would be automatically be “interned”.)"
- 2009-03-06 09:26 Guido van Rossum refines [2009-03-06_how-exceptions-came-to-be-classes.md line 8] `written:2009-03-06_how-exceptions-came-to-be-classes:modula-3-token-influence`: "This approach was influenced by Modula-3’s exceptions, where each exception declaration creates a unique “exception token” that can’t be confused with any othe…"

### L-exception-pointer-optimization (language)

He wanted to test exceptions by pointer comparison rather than string value, a misguided premature optimization of execution time.

first 2009-03-06 09:26 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-03-06

- 2009-03-06 09:26 Guido van Rossum states [2009-03-06_how-exceptions-came-to-be-classes.md line 8] `written:2009-03-06_how-exceptions-came-to-be-classes:premature-optimization-pointer-comparison`: "I think I also wanted to optimize testing for exceptions by using pointer comparisons instead of string value comparisons in a misguided attempt to prematurely…"

### L-exceptions-as-strings (language)

Early Python identified exceptions by strings, an unfortunate choice made because a new built-in type would cost much C coding and strings carry error messages.

first 2009-03-06 09:26 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2009-03-06

- 2009-03-06 09:26 Guido van Rossum states [2009-03-06_how-exceptions-came-to-be-classes.md line 2] `written:2009-03-06_how-exceptions-came-to-be-classes:early-choice-strings-for-exceptions`: "In early Python however, I chose to identify exceptions by strings. This was unfortunate, but I had two reasons for taking this approach. First, I learned abou…"
- 2009-03-06 09:26 Guido van Rossum refines [2009-03-06_how-exceptions-came-to-be-classes.md line 4] `written:2009-03-06_how-exceptions-came-to-be-classes:reuse-existing-builtin-type`: "as every built-in object type required a considerable coding effort in C, I decided to reuse an existing built-in type. And, since exceptions are associated wi…"

### L-string-literal-unification-bug (language)

The bytecode compiler unified string literals within a module, so exceptions could accidentally be caught by their message, which broke across modules and caused confusion.

first 2009-03-06 09:26 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-03-06

- 2009-03-06 09:26 Guido van Rossum states [2009-03-06_how-exceptions-came-to-be-classes.md line 10] `written:2009-03-06_how-exceptions-came-to-be-classes:compiler-unifies-literals-breaks-across-modules`: "Early Python users discovered that within the same module, the byte code compiler would unify string literals ... it only worked for code defined in the same m…"

### L-int-float-silent-error (language)

Because Python has no type declarations, passing an integer where a float is expected is not caught and yields an answer with a much larger error, hard to debug.

first 2009-03-10 13:31 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2009-03-10

- 2009-03-10 13:31 Guido van Rossum refines [2009-03-10_the-problem-with-integer-division.md line 16] `written:2009-03-10_the-problem-with-integer-division:close-but-wrong-answer-hard-to-notice`: "passing an integer can cause an answer that is close to the correct answer but has a much larger error – which is difficult to debug or even notice."
- 2009-03-10 13:31 Guido van Rossum states [2009-03-10_the-problem-with-integer-division.md line 12] `written:2009-03-10_the-problem-with-integer-division:no-type-declarations-no-coercion`: "since Python doesn’t have type declarations, nothing is there to stop a caller from providing you with integer arguments. In a statically typed language, like…"

### L-integer-division (language)

Python's truncating integer division, departing from ABC's exact rationals, was an early mistake with large consequences, fixed with //, a future import, and a flag, becoming default in Python 3000 despite opposition.

first 2009-03-10 13:31 by Guido van Rossum; 6 rows, 5 witnesses, 2 days, last 2010-08-24

- 2009-03-10 13:31 Guido van Rossum states [2009-03-10_the-problem-with-integer-division.md line 2] `written:2009-03-10_the-problem-with-integer-division:abc-exact-rationals`: "in ABC, when you divided two integers, the result was an exact rational number representing the result. In Python however, integer division truncated the resul…"
- 2009-03-10 13:31 Guido van Rossum refines [2009-03-10_the-problem-with-integer-division.md line 18] `written:2009-03-10_the-problem-with-integer-division:fixing-integer-division`: "A truncating division operator (//) was added to the language to provide the same functionality. In addition, a mechanism (\"from __future__ import division\")…"
- 2009-03-10 13:31 Guido van Rossum refines [2009-03-10_the-problem-with-integer-division.md line 10] `written:2009-03-10_the-problem-with-integer-division:integer-division-as-rite-of-passage`: "the proposal to change this has had some tough opposition from folks who believed that learning about integer division was one of the more useful \"rites of pa…"
- 2009-03-10 13:31 Guido van Rossum refines [2009-03-10_the-problem-with-integer-division.md line 2] `written:2009-03-10_the-problem-with-integer-division:integer-division-early-mistake`: "Python's handling of integer division is an example of early mistake with huge consequences. As mentioned earlier, when Python was created, I abandoned the app…"
- 2009-03-10 13:31 Guido van Rossum refines [2009-03-10_the-problem-with-integer-division.md line 14] `written:2009-03-10_the-problem-with-integer-division:silent-truncation-inserts-error`: "when division is involved, and the possibility exists that both operands are integers, the numeric result is silently truncated, essentially inserting a potent…"
- 2010-08-24 09:49 Guido van Rossum refines [2010-08-24_why-python-s-integer-division-floors.md line 44] `written:2010-08-24_why-python-s-integer-division-floors:floor-vs-ambiguous-slash`: "I am using // instead of / -- this is Python 3 syntax, and also allowed in Python 2 to emphasize that you know you are invoking integer division. The / operato…"

### L-mixed-mode-arithmetic (language)

He initially forbade mixed-mode arithmetic to keep type implementations independent, until Tim Peters convinced him to add it with the usual coercion rules.

first 2009-03-10 13:31 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-03-10

- 2009-03-10 13:31 Guido van Rossum states [2009-03-10_the-problem-with-integer-division.md line 8] `written:2009-03-10_the-problem-with-integer-division:forbidding-mixed-mode-arithmetic`: "I initially used another misguided rule that forbade mixed-mode arithmetic, with the aim of making the type implementations independent from each other. ... Af…"

### L-rationals-failed (language)

ABC's exact rational numbers didn't pan out: programs silently ran on numbers with thousands of digits, slow, and the fix was non-intuitive for beginners.

first 2009-03-10 13:31 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-03-10

- 2009-03-10 13:31 Guido van Rossum states [2009-03-10_the-problem-with-integer-division.md line 4] `written:2009-03-10_the-problem-with-integer-division:rationals-did-not-pan-out`: "In my experience, rational numbers didn't pan out as ABC's designers had hoped."

### L-result-type-rule (language)

The major mistake was borrowing C's rule that an arithmetic operation's result is always the same type as its operands, which makes sense in C but not in a very-high-level language.

first 2009-03-10 13:31 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-03-10

- 2009-03-10 13:31 Guido van Rossum states [2009-03-10_the-problem-with-integer-division.md line 8] `written:2009-03-10_the-problem-with-integer-division:result-type-follows-operands`: "The major mistake was that I also borrowed a rule that makes sense in C but not so much in a very-high-level language. For the standard arithmetic operations,…"

### L-c-extensions-easy (language)

Python's implementation architecture made writing extension modules in C easy from the start.

first 2009-03-17 13:07 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-03-17

- 2009-03-17 13:07 Guido van Rossum states [2009-03-17_dynamically-loaded-modules.md line 2] `written:2009-03-17_dynamically-loaded-modules:c-extension-modules-easy-from-the-start`: "Python's implementation architecture made it easy to write extension modules written in C right from the start."

### L-distutils (language)

The distutils tool let users build and install extension modules from anywhere and became a standard library module, but its complexity and lack of maintenance led to third-party alternatives and community fragmentation.

first 2009-03-17 13:07 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2009-03-17

- 2009-03-17 13:07 Guido van Rossum states [2009-03-17_dynamically-loaded-modules.md line 10] `written:2009-03-17_dynamically-loaded-modules:distutils-builds-from-anywhere-via-saved-options`: "a Python extension building tool called distutils was invented that allowed building and installing extension modules from anywhere. The necessary compiler and…"
- 2009-03-17 13:07 Guido van Rossum refines [2009-03-17_dynamically-loaded-modules.md line 12] `written:2009-03-17_dynamically-loaded-modules:distutils-scope-complexity-and-fragmentation`: "distutils does far more than simply building extension modules from C source code."

### L-dynamic-loading (language)

Python's import was interfaced with each platform's dynamic linking API so extension modules could be compiled and loaded separately as shared libraries, replacing early static linking into the interpreter and creating a cross-platform maintenance burden.

first 2009-03-17 13:07 by Guido van Rossum; 5 rows, 4 witnesses, 1 days, last 2009-03-17

- 2009-03-17 13:07 Guido van Rossum refines [2009-03-17_dynamically-loaded-modules.md line 8] `written:2009-03-17_dynamically-loaded-modules:building-modules-remained-a-mystery`: "the procedure for building such modules often remained a mystery to many users."
- 2009-03-17 13:07 Guido van Rossum states [2009-03-17_dynamically-loaded-modules.md line 4] `written:2009-03-17_dynamically-loaded-modules:community-growth-demanded-separate-loading`: "the Python community started producing new extension modules at an unanticipated rate, and demanded that extension modules could be compiled and loaded separat…"
- 2009-03-17 13:07 Guido van Rossum refines [2009-03-17_dynamically-loaded-modules.md line 6] `written:2009-03-17_dynamically-loaded-modules:dynamic-linking-maintenance-nightmare`: "The dynamic linking support proved to be very useful, but also introduced a maintenance nightmare. Each platform used a different API and some platforms had ad…"
- 2009-03-17 13:07 Guido van Rossum refines [2009-03-17_dynamically-loaded-modules.md line 2] `written:2009-03-17_dynamically-loaded-modules:early-static-linking-of-extensions`: "in the early days, dynamic loading technology was obscure enough that such extensions had to be statically linked into Python interpreter at build time."
- 2009-03-17 13:07 Guido van Rossum refines [2009-03-17_dynamically-loaded-modules.md line 6] `written:2009-03-17_dynamically-loaded-modules:restructuring-dynamic-linking-code`: "the dynamic linking support was restructured so that all the dynamic linking code was concentrated in a single source file. However, the approach resulted in a…"

### L-embedding (language)

Users asked for an embeddable Python, a library linkable into other applications, as Emacs embeds a Lisp interpreter.

first 2009-03-31 08:44 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-03-31

- 2009-03-31 08:44 Guido van Rossum states [2009-03-31_the-great-or-grand-renaming.md line 2] `written:2009-03-31_the-great-or-grand-renaming:demand-for-embedded-python`: "people started to ask for an “embedded” version of Python, which would itself be a library that could be linked into other applications – not unlike the way th…"

### L-grand-renaming (method)

The Py-prefix rename, a traumatic kind of event for developer communities, was done in two phases bridged by preprocessor macros for backwards compatibility, accompanied by adding unit tests to much of the standard library.

first 2009-03-31 08:44 by Guido van Rossum; 3 rows, 3 witnesses, 1 days, last 2009-03-31

- 2009-03-31 08:44 Guido van Rossum refines [2009-03-31_the-great-or-grand-renaming.md line 10] `written:2009-03-31_the-great-or-grand-renaming:renaming-paired-with-unit-tests`: "They also helped with the equally tedious task of adding unit tests for much of the standard library."
- 2009-03-31 08:44 Guido van Rossum refines [2009-03-31_the-great-or-grand-renaming.md line 14] `written:2009-03-31_the-great-or-grand-renaming:renamings-are-traumatic-for-communities`: "Great or Grand Renamings are often traumatic events for software developer communities, since they requires the programmers' brains to be rewired, documentatio…"
- 2009-03-31 08:44 Guido van Rossum states [2009-03-31_the-great-or-grand-renaming.md line 6] `written:2009-03-31_the-great-or-grand-renaming:two-phase-transition-with-macros`: "there were two phases. In phase one the linker saw the old names, but the source code used the new names, which were translated to the old names using a large…"

### L-py-prefix (language)

A naming convention was adopted prefixing all Python C globals with Py, _Py for internal names, and PY for macros, to avoid clashes.

first 2009-03-31 08:44 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-03-31

- 2009-03-31 08:44 Guido van Rossum states [2009-03-31_the-great-or-grand-renaming.md line 4] `written:2009-03-31_the-great-or-grand-renaming:py-prefix-naming-convention`: "a naming convention was chosen, whereby all Python globals would have a name starting with “Py” or “_Py” (for internal names that had to be global for technica…"

### L-standalone-globals (other)

Python was first conceived as a stand-alone program, so its C source freely defined global linker names without namespace discipline, which clashed with host applications when embedding.

first 2009-03-31 08:44 by Guido van Rossum; 3 rows, 2 witnesses, 1 days, last 2009-03-31

- 2009-03-31 08:44 Guido van Rossum refines [2009-03-31_the-great-or-grand-renaming.md line 2] `written:2009-03-31_the-great-or-grand-renaming:freely-defined-global-names`: "The source code therefore freely defined global names (in the C/linker sense) like ‘object’, ‘getlistitem’, ‘INCREF’ and so on."
- 2009-03-31 08:44 Guido van Rossum refines [2009-03-31_the-great-or-grand-renaming.md line 4] `written:2009-03-31_the-great-or-grand-renaming:name-clashes-block-embedding`: "this embedding was complicated by name clashes between Python’s global names and those defined by the embedding application – the name 'object’ was especially…"
- 2009-03-31 08:44 Guido van Rossum states [2009-03-31_the-great-or-grand-renaming.md line 2] `written:2009-03-31_the-great-or-grand-renaming:python-as-stand-alone-program`: "When Python was first created, I always envisioned it as a stand-alone program, occasionally linking in third-party libraries."

### L-closures (language)

Inner functions should implicitly carry references to the enclosing scope's referenced local variables (closures); lambda originally couldn't, needing default-argument workarounds, and closures were added in 2.1/2.2, proving useful for new-style classes and decorators.

first 2009-04-21 11:05 by Guido van Rossum; 4 rows, 4 witnesses, 1 days, last 2009-04-21

- 2009-04-21 11:05 Guido van Rossum refines [2009-04-21_origins-of-python-s-functional-features.md line 70] `written:2009-04-21_origins-of-python-s-functional-features:closures-as-correct-solution`: "The \"correct\" solution to this problem was for inner functions to implicitly carry references to all of the local variables in the surrounding scope that are…"
- 2009-04-21 11:05 Guido van Rossum refines [2009-04-21_origins-of-python-s-functional-features.md line 74] `written:2009-04-21_origins-of-python-s-functional-features:closures-enabled-other-advanced-features`: "the introduction of closures has been useful in the development of many other advanced programming features. For example, certain aspects of new-style classes,…"
- 2009-04-21 11:05 Guido van Rossum refines [2009-04-21_origins-of-python-s-functional-features.md line 64] `written:2009-04-21_origins-of-python-s-functional-features:default-argument-workaround`: "There were workarounds to this problem, but they counter-intuitively involved setting default arguments and passing hidden arguments into the lambda expression."
- 2009-04-21 11:05 Guido van Rossum states [2009-04-21_origins-of-python-s-functional-features.md line 58] `written:2009-04-21_origins-of-python-s-functional-features:lambda-could-not-reference-enclosing-scope`: "a subtle problem with lambda is that the expression supplied couldn't refer to variables in the surrounding scope."

### L-functional-added (language)

In January 1994 map(), filter(), reduce(), and the lambda operator for anonymous functions were added, a significant early chunk of contributed code.

first 2009-04-21 11:05 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2009-04-21

- 2009-04-21 11:05 Guido van Rossum states [2009-04-21_origins-of-python-s-functional-features.md line 49] `written:2009-04-21_origins-of-python-s-functional-features:addition-of-map-filter-reduce-and-lambda`: "the map(), filter(), and reduce() functions were added to the standard library. In addition, the lambda operator was introduced for creating anonymous function…"
- 2009-04-21 11:05 Guido van Rossum refines [2009-04-21_origins-of-python-s-functional-features.md line 54] `written:2009-04-21_origins-of-python-s-functional-features:features-were-contributed-code`: "These additions represented a significant, early chunk of contributed code."

### L-functional-superseded (language)

The map, filter, and reduce functions were largely superseded by list comprehensions and generator expressions; reduce was removed from the built-ins in Python 3 while lambda, map and filter stay.

first 2009-04-21 11:05 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-04-21

- 2009-04-21 11:05 Guido van Rossum states [2009-04-21_origins-of-python-s-functional-features.md line 72] `written:2009-04-21_origins-of-python-s-functional-features:map-filter-reduce-superseded-by-comprehensions`: "the map, filter, and reduce functions that originally motivated the introduction of lambda and other functional features have to a large extent been superseded…"

### L-lambda-intent (language)

Lambda was intended only as a syntactic tool for defining anonymous functions, not a full functional construct.

first 2009-04-21 11:05 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-04-21

- 2009-04-21 11:05 Guido van Rossum states [2009-04-21_origins-of-python-s-functional-features.md line 58] `written:2009-04-21_origins-of-python-s-functional-features:lambda-only-a-syntactic-tool`: "Lambda was really only intended to be a syntactic tool for defining anonymous functions."

### L-lambda-motivation (language)

Users wanted a way to create anonymous functions in-line rather than defining a separate named function (as Lisp and Scheme allow), since Python had no such mechanism despite first-class functions, and the exec-string workaround was hacky.

first 2009-04-21 11:05 by Guido van Rossum; 7 rows, 7 witnesses, 1 days, last 2009-04-21

- 2009-04-21 11:05 Guido van Rossum refines [2009-04-21_origins-of-python-s-functional-features.md line 49] `written:2009-04-21_origins-of-python-s-functional-features:code-strings-via-exec-seen-as-hacky`: "it seemed pretty \"hacky\" to be specifying anonymous functions as code strings that you had to manually process through exec."
- 2009-04-21 11:05 Guido van Rossum refines [2009-04-21_origins-of-python-s-functional-features.md line 28] `written:2009-04-21_origins-of-python-s-functional-features:dislike-of-separate-named-function`: "many people didn't like the fact that you to define the operation that you were applying to the list elements as a completely separate function."
- 2009-04-21 11:05 Guido van Rossum refines [2009-04-21_origins-of-python-s-functional-features.md line 34] `written:2009-04-21_origins-of-python-s-functional-features:exec-based-anonymous-function-hacks`: "Mark Lutz... posted some code for a function that created functions using exec."
- 2009-04-21 11:05 Guido van Rossum refines [2009-04-21_origins-of-python-s-functional-features.md line 14] `written:2009-04-21_origins-of-python-s-functional-features:lisp-scheme-users-reimplemented-builtins`: "In functional languages such as Lisp and Scheme, operations such as this were provided as built-in functions of the language. Thus, early users familiar with s…"
- 2009-04-21 11:05 Guido van Rossum refines [2009-04-21_origins-of-python-s-functional-features.md line 4] `written:2009-04-21_origins-of-python-s-functional-features:mapping-over-lists-as-common-operation`: "A common operation on lists was that of mapping a function to each of the elements of a list and creating a new list."
- 2009-04-21 11:05 Guido van Rossum states [2009-04-21_origins-of-python-s-functional-features.md line 32] `written:2009-04-21_origins-of-python-s-functional-features:no-anonymous-functions-in-python`: "Although Python made functions first-class objects, it didn't have any similar mechanism for creating anonymous functions."
- 2009-04-21 11:05 Guido van Rossum refines [2009-04-21_origins-of-python-s-functional-features.md line 2] `written:2009-04-21_origins-of-python-s-functional-features:user-demand-drove-list-and-function-features`: "earlier on, it was clear that users wanted to do much more with lists and functions."

### L-lambda-terminology (language)

The 'lambda' terminology, adopted for lack of a better alternative despite Van Rossum's unease, led functional-language users to expect semantics and advanced features Python lacked.

first 2009-04-21 11:05 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2009-04-21

- 2009-04-21 11:05 Guido van Rossum refines [2009-04-21_origins-of-python-s-functional-features.md line 58] `written:2009-04-21_origins-of-python-s-functional-features:terminology-raised-unmet-expectations`: "the choice of terminology had many unintended consequences... they found Python's implementation to be sorely lacking in advanced features."
- 2009-04-21 11:05 Guido van Rossum states [2009-04-21_origins-of-python-s-functional-features.md line 56] `written:2009-04-21_origins-of-python-s-functional-features:unhappy-with-lambda-terminology`: "I was never all that happy with the use of the \"lambda\" terminology, but for lack of a better and obvious alternative, it was adopted for Python."

### L-less-discussion-early (method)

In the early days big changes required much less discussion than later, for better and worse.

first 2009-04-21 11:05 by Guido van Rossum; 2 rows, 2 witnesses, 2 days, last 2013-11-11

- 2009-04-21 11:05 Guido van Rossum states [2009-04-21_origins-of-python-s-functional-features.md line 56] `written:2009-04-21_origins-of-python-s-functional-features:big-changes-required-less-discussion-then`: "at the time big changes required much less discussion than nowadays, for better and for worse."
- 2013-11-11 16:29 Guido van Rossum restates [2013-11-11_the-history-of-bool-true-and-false.md line 24] `written:2013-11-11_the-history-of-bool-true-and-false:breakneck-development-pace`: "That's a breakneck pace compared to how we do things a decade later!"

### L-not-functional (language)

Van Rossum never viewed Python as a functional language or heavily influenced by them, and its dynamic nature rules out functional-style compile-time optimization such as tail recursion.

first 2009-04-21 11:05 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2009-04-21

- 2009-04-21 11:05 Guido van Rossum refines [2009-04-21_origins-of-python-s-functional-features.md line 76] `written:2009-04-21_origins-of-python-s-functional-features:dynamism-precludes-functional-optimizations`: "because Python's extremely dynamic nature, it is impossible to do the kind of compile-time optimization known from functional languages like Haskell or ML. And…"
- 2009-04-21 11:05 Guido van Rossum states [2009-04-21_origins-of-python-s-functional-features.md line 2] `written:2009-04-21_origins-of-python-s-functional-features:python-not-functional-despite-first-class-functions`: "I have never considered Python to be heavily influenced by functional languages... although I had made functions first-class objects, I didn't view Python as a…"

### L-beaudry-hook (language)

Don Beaudry's insight that custom kinds of class objects should be creatable led to a hook: a callable type used as a base class makes class creation call that type, letting C (and later Python via a __class__ attribute) extensions define class behavior; it felt like a hack because type objects weren't yet callable, and it seeded metaclasses and new-style classes.

first 2009-04-24 09:14 by Guido van Rossum; 7 rows, 5 witnesses, 1 days, last 2009-04-24

- 2009-04-24 09:14 Guido van Rossum refines [2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 12] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:beaudry-insight-led-to-new-style-classes`: "Don Beaudry is eventually responsible for planting the insight in my head that led first to metaclasses and later to new-style classes and the eventual death o…"
- 2009-04-24 09:14 Guido van Rossum refines [2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 10] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:callable-base-class-triggers-hook`: "when an instance of such a callable type was used as a base class in a class statement, the class creation code would magically call that type object instead o…"
- 2009-04-24 09:14 Guido van Rossum refines [2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 16] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:class-attribute-removes-c-requirement`: "In Python 1.5, I removed the requirement to write a C extension in order to use the Don Beaudry hook. In addition to check for a callable base class type, the…"
- 2009-04-24 09:14 Guido van Rossum refines [2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 6] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:don-beaudry-hook`: "He then suggested a very slight modification to the interpreter that would allow new kinds of class objects to be created by C code extension modules."
- 2009-04-24 09:14 Guido van Rossum states [2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 6] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:missed-opportunity-for-custom-classes`: "Don Beaudry was the first to point out that this was a missed opportunity for expert users. Specifically, if classes were simply special kinds of objects, why…"
- 2009-04-24 09:14 Guido van Rossum refines [2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 12] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:types-were-not-callable-at-the-time`: "at the time, type objects were not callable -- e.g. 'int' was not a built-in type but a built-in function that returned an instance of the int object, and the…"
- 2009-04-24 09:14 Guido van Rossum refines [2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 8] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:user-supplied-final-construction-function`: "expert users would be able to create custom class objects if there was some way to supply a user-supplied function in the final step of class creation."

### L-class-creation-api (language)

Defining a class executes its body in a local dictionary, then calls a class creation function with the name, a tuple of base classes, and that dictionary; originally internal, it became a public API and carried over unchanged into the Python 2.2 metaclass machinery.

first 2009-04-24 09:14 by Guido van Rossum; 3 rows, 3 witnesses, 1 days, last 2009-04-24

- 2009-04-24 09:14 Guido van Rossum refines [2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 18] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:class-creation-api-three-arguments`: "the most lasting contribution of the Don Beaudry hook is the API for the class creation function, which was carried over to the new metaclass machinery in Pyth…"
- 2009-04-24 09:14 Guido van Rossum states [2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 4] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:class-creation-as-hidden-internal-step`: "The name of the class, a tuple of base classes, and this local dictionary would then be passed to an internal class creation function that was responsible for…"
- 2009-04-24 09:14 Guido van Rossum refines [2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 20] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:internal-api-became-public`: "Originally, this was simply the internal API for creating classes. The Don Beaudry hook used the same call signature and hence it became a public API."

### L-class-creation-hidden (language)

In Python's original design classes were first-class objects, yet the act of creating a class was a fixed step hidden from users as an implementation detail.

first 2009-04-24 09:14 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-04-24

- 2009-04-24 09:14 Guido van Rossum states [2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 2] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:classes-as-first-class-objects`: "In Python’s original implementation, classes were first class objects that could be manipulated just like any other object. However, the process of creating a…"

### L-metaclass-namespace-limit (language)

The class body is executed before the class creation function runs, so a metaclass could not influence the namespace the definitions run in; Python 3000 fixed this by letting a metaclass provide an alternative mapping, specified with keyword-argument syntax in the base-class list.

first 2009-04-24 09:14 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2009-04-24

- 2009-04-24 09:14 Guido van Rossum states [2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 20] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:body-executed-before-creation-limits-metaclasses`: "The most important aspect of this API is that the block containing the method definitions is executed before the class creation function is called. This places…"
- 2009-04-24 09:14 Guido van Rossum corrects [2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 22] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:python-3000-alternative-namespace-mapping`: "This was changed in Python 3000, so that now a metaclass can provide an alternative mapping object in which the class body is executed. In order to support thi…"

### L-metaclass-no-syntax-change (language)

A self-imposed constraint was that the metaclass mechanism must work without changing the already well-established class syntax.

first 2009-04-24 09:14 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2009-04-24

- 2009-04-24 09:14 Guido van Rossum states [2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md line 8] `written:2009-04-24_metaclasses-and-extension-classes-a-k-a-:no-change-to-class-syntax`: "The only catch was that I didn't want to make any changes to the class syntax which had already been well-established."

### L-class-impl-problems (language)

The original class implementation's problems became a frequent complaint among expert users: built-in types could not be subclassed, and the type system treated instances of unrelated classes as the same type.

first 2010-06-21 11:07 by Guido van Rossum; 3 rows, 3 witnesses, 1 days, last 2010-06-21

- 2010-06-21 11:07 Guido van Rossum refines [2010-06-21_new-style-classes.md line 6] `written:2010-06-21_new-style-classes:builtin-types-not-subclassable`: "One problem with the class implementation was that there was no way to subclass built-in types... these objects were somehow "special" and could not be special…"
- 2010-06-21 11:07 Guido van Rossum states [2010-06-21_new-style-classes.md line 4] `written:2010-06-21_new-style-classes:class-implementation-a-source-of-griping`: "as Python evolved, various problems with the class implementation became a popular topic of griping from expert Python users."
- 2010-06-21 11:07 Guido van Rossum refines [2010-06-21_new-style-classes.md line 8] `written:2010-06-21_new-style-classes:user-classes-outside-the-type-system`: "statements such as type(a) == type(b) would evaluate as True even if a and b were instances of completely unrelated classes... in those languages, classes were…"

### L-classes-afterthought (other)

Adding classes to Python was essentially an afterthought, implemented in the 'cut corners' philosophy.

first 2010-06-21 11:07 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2010-06-21

- 2010-06-21 11:07 Guido van Rossum states [2010-06-21_new-style-classes.md line 4] `written:2010-06-21_new-style-classes:classes-as-afterthought-cut-corners`: "Earlier, I described how the addition of classes to Python was essentially an afterthought. The implementation chosen was definitely an example of Python's "cu…"

### L-metaclass-influence (other)

The specific notion of metaclass came from the book 'Putting Metaclasses to Work' by Ira Forman and Scott Danforth, distinct from Smalltalk's similar concept.

first 2010-06-21 11:07 by Guido van Rossum; 2 rows, 2 witnesses, 2 days, last 2013-10-24

- 2010-06-21 11:07 Guido van Rossum states [2010-06-21_new-style-classes.md line 10] `written:2010-06-21_new-style-classes:metaclass-notion-from-forman-danforth`: "A major influence on this work was the book "Putting Metaclasses to Work" by Ira Forman and Scott Danforth, which provided me with a specific notion of what a…"
- 2013-10-24 09:58 Guido van Rossum restates [2013-10-24_origin-of-metaclasses-in-python.md line 13] `written:2013-10-24_origin-of-metaclasses-in-python:new-style-classes-inspired-by-forman-danforth`: "I was inspired to implement new-style classes by a very\nspecific book, \"Putting Metaclasses to Work\" by Ira Forman and Scott\nDanforth"

### L-new-style-coexist (language)

New-style classes were introduced as a feature coexisting with old-style ones for backwards compatibility (old remaining the default in Python 2), created by subclassing an existing new-style class such as object, the root of the hierarchy; old-style classes will eventually be removed.

first 2010-06-21 11:07 by Guido van Rossum; 3 rows, 2 witnesses, 1 days, last 2010-06-21

- 2010-06-21 11:07 Guido van Rossum refines [2010-06-21_new-style-classes.md line 15] `written:2010-06-21_new-style-classes:eventual-removal-and-the-object-idiom`: "although the old-style classes will eventually be removed from the languages, users are getting used to writing "class MyClass(object)" to declare a class, whi…"
- 2010-06-21 11:07 Guido van Rossum states [2010-06-21_new-style-classes.md line 12] `written:2010-06-21_new-style-classes:new-style-as-feature-not-replacement`: "new-style classes were introduced as a new language feature, not as a strict replacement for old-style classes. In fact, for backwards compatibility, the old c…"
- 2010-06-21 11:07 Guido van Rossum refines [2010-06-21_new-style-classes.md line 12] `written:2010-06-21_new-style-classes:object-as-root-of-hierarchy`: "you simply have to subclass an existing new-style class such as object (which is the root for the new-style class hierarchy)"

### L-new-style-rewrite (language)

In Python 2.2 Van Rossum reimplemented classes 'to do it right', the most ambitious subsystem rewrite to date (risking second-system syndrome), adding subclassable built-in types, true metaclasses, a fixed MRO and more, and it proved a major success.

first 2010-06-21 11:07 by Guido van Rossum; 3 rows, 2 witnesses, 1 days, last 2010-06-21

- 2010-06-21 11:07 Guido van Rossum states [2010-06-21_new-style-classes.md line 10] `written:2010-06-21_new-style-classes:reimplementation-in-2.2-do-it-right`: "In Python 2.2, I finally took the time to reimplement classes and "do it right." This change was, by far, the most ambitious rewrite of a major Python subsyste…"
- 2010-06-21 11:07 Guido van Rossum refines [2010-06-21_new-style-classes.md line 15] `written:2010-06-21_new-style-classes:rewrite-judged-a-success`: "The change to new-style classes has been a major success. The new metaclasses have become popular amongst framework writers and explaining classes has actually…"
- 2010-06-21 11:07 Guido van Rossum refines [2010-06-21_new-style-classes.md line 10] `written:2010-06-21_new-style-classes:scope-of-the-rewrite`: "Not only did I address the immediate problem of allowing built-in types to be subclassed, I also added support for true metaclasses, attempted to fix the naïve…"

### L-class-attr-defaults (language)

Non-function class attributes serve as default values for instance variables: assignment to the instance shadows the class value and deletion reveals it again.

first 2010-06-21 11:18 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2010-06-21

- 2010-06-21 11:18 Guido van Rossum states [2010-06-21_the-inside-story-on-new-style-classes.md line 40] `written:2010-06-21_the-inside-story-on-new-style-classes:class-attributes-as-default-values`: "This makes it possible to use class attributes as “default” values for instance variables."

### L-decorator-syntax (language)

The @-decorator syntax (Python 2.4, derived from Java's annotations, decided by BDFL pronouncement) replaced wrapping-by-assignment, which had forced the reader to the end of a method to learn its kind.

first 2010-06-21 11:18 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2010-06-21

- 2010-06-21 11:18 Guido van Rossum refines [2010-06-21_the-inside-story-on-new-style-classes.md line 82] `written:2010-06-21_the-inside-story-on-new-style-classes:decorator-syntax-chosen-by-bdfl-pronouncement`: "The particular choice of decorator syntax (derived from Java's annotations) was debated endlessly before it was decided by “BDFL pronouncement”."
- 2010-06-21 11:18 Guido van Rossum states [2010-06-21_the-inside-story-on-new-style-classes.md line 75] `written:2010-06-21_the-inside-story-on-new-style-classes:decorators-address-readability-downside`: "A downside of this approach is that the reader of a class had to read all the way till the end of a method declaration before finding out whether it was a clas…"

### L-decorators-success (language)

Decorators became one of the most successful features, exceeding expectations especially in web frameworks, and were extended to class definitions in Python 2.6.

first 2010-06-21 11:18 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2010-06-21

- 2010-06-21 11:18 Guido van Rossum states [2010-06-21_the-inside-story-on-new-style-classes.md line 84] `written:2010-06-21_the-inside-story-on-new-style-classes:decorators-exceeded-expectations`: "The decorator feature has become one of the more successful language features, and the use of custom decorators has exceeded my widest expectations."

### L-descriptor-classes (language)

Python 2.2 added classmethod, staticmethod, and property as predefined classes built on the descriptor machinery.

first 2010-06-21 11:18 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2010-06-21

- 2010-06-21 11:18 Guido van Rossum states [2010-06-21_the-inside-story-on-new-style-classes.md line 50] `written:2010-06-21_the-inside-story-on-new-style-classes:classmethod-staticmethod-property-built-on-descriptors`: "Python 2.2 added three predefined classes: classmethod, staticmethod, and property, that utilized the new descriptor machinery."

### L-descriptor-no-syntax (language)

Descriptors were introduced without new syntax because adding a major feature and new syntax at once was deemed too controversial, so users wrapped methods with extra assignment statements.

first 2010-06-21 11:18 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2010-06-21

- 2010-06-21 11:18 Guido van Rossum states [2010-06-21_the-inside-story-on-new-style-classes.md line 59] `written:2010-06-21_the-inside-story-on-new-style-classes:no-new-syntax-at-first`: "At the time, it was deemed too controversial to simultaneously introduce a major new feature along with new syntax (which always leads to a heated debate)."

### L-descriptors (language)

Python 2.2 generalized method wrapping into descriptors: the object found by attribute search decides via __get__ (and __set__/__delete__) what get, set, and delete mean, replacing the hard-coded scheme that only wrapped Python functions (which blocked hybrid classes); the customization applies only in a class dictionary.

first 2010-06-21 11:18 by Guido van Rossum; 4 rows, 4 witnesses, 1 days, last 2010-06-21

- 2010-06-21 11:18 Guido van Rossum refines [2010-06-21_the-inside-story-on-new-style-classes.md line 44] `written:2010-06-21_the-inside-story-on-new-style-classes:descriptor-protocol-get`: "Instead of hard-coding the behavior that Python function objects are wrapped and other objects aren’t, the wrapping is now left up to the object found by the a…"
- 2010-06-21 11:18 Guido van Rossum refines [2010-06-21_the-inside-story-on-new-style-classes.md line 46] `written:2010-06-21_the-inside-story-on-new-style-classes:descriptor-set-and-delete`: "Thus, by redefining these methods, a descriptor object can have complete control over what it means to get, set, and delete an attribute. However, it's importa…"
- 2010-06-21 11:18 Guido van Rossum states [2010-06-21_the-inside-story-on-new-style-classes.md line 32] `written:2010-06-21_the-inside-story-on-new-style-classes:descriptors-generalize-bound-methods`: "Descriptors are a generalization of the concept of bound methods, which was central to the implementation of classic classes."
- 2010-06-21 11:18 Guido van Rossum refines [2010-06-21_the-inside-story-on-new-style-classes.md line 42] `written:2010-06-21_the-inside-story-on-new-style-classes:limitation-of-hard-coded-wrapping`: "One limitation was that it was prevented the creation of “hybrid” classes that had some methods implemented in Python and others in C, because only Python func…"

### L-new-method (language)

__new__ was introduced as a class method hook for customizing instance creation, which old-style classes lacked, enabling patterns like Singleton, returning existing or different-class instances, use in pickle, and initializing immutable subclasses.

first 2010-06-21 11:18 by Guido van Rossum; 3 rows, 3 witnesses, 1 days, last 2010-06-21

- 2010-06-21 11:18 Guido van Rossum refines [2010-06-21_the-inside-story-on-new-style-classes.md line 26] `written:2010-06-21_the-inside-story-on-new-style-classes:new-enables-creation-patterns-and-unpickling`: "By overriding __new__() a class author can implement patterns like the Singleton Pattern, return a previously created instance (e.g., from a free list), or to…"
- 2010-06-21 11:18 Guido van Rossum refines [2010-06-21_the-inside-story-on-new-style-classes.md line 28] `written:2010-06-21_the-inside-story-on-new-style-classes:new-for-subclassing-immutable-types`: "Another use of __new__ is to help with the subclassing of immutable types. By the nature of their immutability, these kinds of objects can not be initialized t…"
- 2010-06-21 11:18 Guido van Rossum states [2010-06-21_the-inside-story-on-new-style-classes.md line 24] `written:2010-06-21_the-inside-story-on-new-style-classes:new-hook-for-customizing-object-creation`: "Old-style classes never really provided a hook for customizing the creation of objects although there were library modules allowed certain kinds of objects to…"

### L-new-style-concepts (language)

New-style classes look similar to the original implementation on the surface but introduced __new__, descriptors, static and class methods, properties, decorators, slots, and a new Method Resolution Order.

first 2010-06-21 11:18 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2010-06-21

- 2010-06-21 11:18 Guido van Rossum states [2010-06-21_the-inside-story-on-new-style-classes.md line 4] `written:2010-06-21_the-inside-story-on-new-style-classes:new-style-classes-introduced-new-concepts`: "On the surface, new-style classes appear very similar to the original class implementation. However, new-style classes also introduced a number of new concepts:"

### L-slots (language)

__slots__ is an application of descriptors that stores attributes in array slots and removes the instance __dict__; its real goal was performance (a fallback against a feared attribute-access slowdown), not attribute-name safety.

first 2010-06-21 11:18 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2010-06-21

- 2010-06-21 11:18 Guido van Rossum states [2010-06-21_the-inside-story-on-new-style-classes.md line 88] `written:2010-06-21_the-inside-story-on-new-style-classes:slots-as-descriptor-application`: "Another enhancement made possible with descriptors was the introduction of the __slots__ attribute on classes."
- 2010-06-21 11:18 Guido van Rossum refines [2010-06-21_the-inside-story-on-new-style-classes.md line 93] `written:2010-06-21_the-inside-story-on-new-style-classes:slots-ultimate-goal-was-performance`: "Some people mistakenly assume that the intended purpose of __slots__ is to increase code safety (by restricting the attribute names). In reality, my ultimate g…"

### L-antigravity-easteregg (other)

Python 3's standard library includes an easter-egg antigravity module referencing the XKCD comic, with a second hidden joke, a purported geohashing implementation, inside.

first 2010-06-21 11:31 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2010-06-21

- 2010-06-21 11:31 Guido van Rossum states [2010-06-21_import-antigravity.md line 2] `written:2010-06-21_import-antigravity:antigravity-as-stdlib-easter-egg`: "The antigravity module, referencing the XKCD comic mentioning Python, was added to Python 3 by Skip Montanaro."
- 2010-06-21 11:31 Guido van Rossum refines [2010-06-21_import-antigravity.md line 12] `written:2010-06-21_import-antigravity:easter-egg-inside-the-easter-egg`: "The Python 3 stdlib version has an easter egg inside the easter egg, ... it defines a function that purports to implement the XKCD geohashing algorithm."

### L-c3-adoption (language)

Python adopted the C3 Linearization algorithm from the Dylan paper, which writes down all ordering rules imposed by inheritance and finds a monotonic ordering satisfying them all or fails.

first 2010-06-23 10:41 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2010-06-23

- 2010-06-23 10:41 Guido van Rossum states [2010-06-23_method-resolution-order.md line 41] `written:2010-06-23_method-resolution-order:adopt-c3-linearization`: "it was decided that the MRO adopted for Python 2.2 was broken and that Python should adopt the C3 Linearization algorithm described in the paper \"A Monotonic…"
- 2010-06-23 10:41 Guido van Rossum refines [2010-06-23_method-resolution-order.md line 45] `written:2010-06-23_method-resolution-order:inheritance-defines-ordering-rules`: "if you write down all of the ordering rules imposed by inheritance relationships in a complex class hierarchy, the algorithm will determine a monotonic orderin…"

### L-c3-rejects (language)

C3 makes Python reject any inheritance hierarchy with an inconsistent ordering of base classes rather than resolving it silently, matching the Zen of Python's rule that errors should never pass silently.

first 2010-06-23 10:41 by Guido van Rossum; 2 rows, 1 witnesses, 1 days, last 2010-06-23

- 2010-06-23 10:41 Guido van Rossum states [2010-06-23_method-resolution-order.md line 47] `written:2010-06-23_method-resolution-order:c3-rejects-inconsistent-hierarchies`: "Python will now reject any inheritance hierarchy that has an inconsistent ordering of base classes."
- 2010-06-23 10:41 Guido van Rossum refines [2010-06-23_method-resolution-order.md line 47] `written:2010-06-23_method-resolution-order:rejection-matches-zen-errors-not-silent`: "This, of course, matches the Zen of Python's \"errors should never pass silently\" rule."

### L-mro-22-algorithm (language)

For Python 2.2 the MRO was pre-computed at class-definition time and stored as a class attribute, dropping all but the last occurrence of a duplicated class.

first 2010-06-23 10:41 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2010-06-23

- 2010-06-23 10:41 Guido van Rossum states [2010-06-23_method-resolution-order.md line 32] `written:2010-06-23_method-resolution-order:precompute-and-store-mro`: "I adopted a scheme where the MRO would be pre-computed when a class was defined and stored as an attribute of each class object. ... If any class was duplicate…"

### L-mro-22-broken (language)

The MRO Van Rossum implemented for Python 2.2, with a special case reordering bases, diverged from the simpler algorithm he documented, and Samuele Pedroni found inconsistencies violating monotonicity, so it was judged broken, a regret.

first 2010-06-23 10:41 by Guido van Rossum; 4 rows, 4 witnesses, 1 days, last 2010-06-23

- 2010-06-23 10:41 Guido van Rossum refines [2010-06-23_method-resolution-order.md line 39] `written:2010-06-23_method-resolution-order:documented-wrong-algorithm`: "This is what I implemented for Python 2.2, but I documented the earlier algorithm (naïvely thinking it didn't matter much)."
- 2010-06-23 10:41 Guido van Rossum refines [2010-06-23_method-resolution-order.md line 45] `written:2010-06-23_method-resolution-order:monotonicity-as-the-core-problem`: "if you have already determined that class A should be checked before class B, then you should never encounter a situation that requires class B to be checked b…"
- 2010-06-23 10:41 Guido van Rossum refines [2010-06-23_method-resolution-order.md line 34] `written:2010-06-23_method-resolution-order:mro-special-case-preserve-first-order`: "there was a special case to deal with a situation when two bases classes occurred in a different order in the inheritance list of two different derived classes…"
- 2010-06-23 10:41 Guido van Rossum states [2010-06-23_method-resolution-order.md line 41] `written:2010-06-23_method-resolution-order:pedroni-found-inconsistency`: "Samuele Pedroni discovered an inconsistency between the documented MRO algorithm and the results that were actually observed in real-code. Moreover, inconsiste…"

### L-mro-concept (language)

The Method Resolution Order (MRO) is the order base classes are searched for a method, and in Python also for other attributes; it is interesting and subtle only under multiple inheritance.

first 2010-06-23 10:41 by Guido van Rossum; 2 rows, 1 witnesses, 1 days, last 2010-06-23

- 2010-06-23 10:41 Guido van Rossum states [2010-06-23_method-resolution-order.md line 2] `written:2010-06-23_method-resolution-order:mro-defines-attribute-search-order`: "the order in which base classes are searched when looking for a method is often called the Method Resolution Order, or MRO. (In Python this also applies to oth…"
- 2010-06-23 10:41 Guido van Rossum refines [2010-06-23_method-resolution-order.md line 2] `written:2010-06-23_method-resolution-order:mro-trivial-under-single-inheritance`: "For languages that support single inheritance only, the MRO is uninteresting; but when multiple inheritance comes into play, the choice of an MRO algorithm can…"

### L-mro-diamond-problem (language)

The classic depth-first, left-to-right search breaks under diamond inheritance by finding a shared ancestor's method instead of the more specialized override; since all new-style classes inherit from object, every use of multiple inheritance becomes a diamond, making this commonplace and the order critical.

first 2010-06-23 10:41 by Guido van Rossum; 4 rows, 4 witnesses, 1 days, last 2010-06-23

- 2010-06-23 10:41 Guido van Rossum states [2010-06-23_method-resolution-order.md line 13] `written:2010-06-23_method-resolution-order:classic-mro-fails-on-diamond`: "This scheme works fine for simple cases, but has problems that become apparent when one considers more complicated uses of multiple inheritance. One problem co…"
- 2010-06-23 10:41 Guido van Rossum refines [2010-06-23_method-resolution-order.md line 24] `written:2010-06-23_method-resolution-order:new-style-classes-make-diamonds-universal`: "Although this kind of multiple inheritance was rare in existing code, new-style classes would make it commonplace. This is because all new-style classes were d…"
- 2010-06-23 10:41 Guido van Rossum refines [2010-06-23_method-resolution-order.md line 30] `written:2010-06-23_method-resolution-order:object-methods-make-order-critical`: "since object defined a number of methods that are sometimes extended by subtypes (e.g., __setattr__()), the resolution order becomes critical."
- 2010-06-23 10:41 Guido van Rossum refines [2010-06-23_method-resolution-order.md line 22] `written:2010-06-23_method-resolution-order:specialized-override-should-win`: "one can argue that the redefined method C.save() is actually the method that you want to call, since it can be viewed as being \"more specialized\" than the me…"

### L-mro-three-algorithms (language)

Python has used three MRO algorithms over time (classic, 2.2 new-style, and 2.3 new-style / C3), of which only C3 survives in Python 3.

first 2010-06-23 10:41 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2010-06-23

- 2010-06-23 10:41 Guido van Rossum states [2010-06-23_method-resolution-order.md line 2] `written:2010-06-23_method-resolution-order:python-had-three-mro-algorithms`: "Python has known at least three different MRO algorithms: classic, Python 2.2 new-style, and Python 2.3 new-style (a.k.a. C3). Only the latter survives in Pyth…"

### L-comprehension-design-factors (method)

Four factors governed the design of these notations: backwards compatibility, avoiding ambiguity, the desire for equivalence, and evolution of the language.

first 2010-06-29 08:39 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2010-06-29

- 2010-06-29 08:39 Guido van Rossum states [2010-06-29_from-list-comprehensions-to-generator-expressions.md line 28] `written:2010-06-29_from-list-comprehensions-to-generator-ex:design-factors-four`: "The factors affecting the design were backwards compatibility, avoiding ambiguity, the desire for equivalence, and evolution of the language."

### L-comprehension-extensions (language)

Python 3 added set and dict comprehensions as straightforward extensions of the list comprehension idea.

first 2010-06-29 08:39 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2010-06-29

- 2010-06-29 08:39 Guido van Rossum states [2010-06-29_from-list-comprehensions-to-generator-expressions.md line 62] `written:2010-06-29_from-list-comprehensions-to-generator-ex:set-and-dict-comprehensions`: "Python 3 also supports set comprehensions and dictionary comprehensions. These are straightforward extensions of the list comprehension idea."

### L-comprehension-forloop-origin (language)

The bare comma-separated values after 'in' recall Algol-60's for-loop, and since a colon always followed there was no ambiguity, so looping over known values shouldn't require parentheses.

first 2010-06-29 08:39 by Guido van Rossum; 2 rows, 1 witnesses, 1 days, last 2010-06-29

- 2010-06-29 08:39 Guido van Rossum states [2010-06-29_from-list-comprehensions-to-generator-expressions.md line 28] `written:2010-06-29_from-list-comprehensions-to-generator-ex:algol-60-inspiration`: "This also reminded me of Algol-60, where you can write: for i := 1, 2, 3 do Statement"
- 2010-06-29 08:39 Guido van Rossum refines [2010-06-29_from-list-comprehensions-to-generator-expressions.md line 28] `written:2010-06-29_from-list-comprehensions-to-generator-ex:bare-sequence-after-in-from-for-loop`: "if you wanted to loop over a bunch of known values, you shouldn't be bothered with having to put parentheses around them."

### L-comprehension-performance (language)

List comprehensions run faster than map plus lambda because a lambda call creates a new stack frame while the comprehension's expression is evaluated without one.

first 2010-06-29 08:39 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2010-06-29

- 2010-06-29 08:39 Guido van Rossum states [2010-06-29_from-list-comprehensions-to-generator-expressions.md line 12] `written:2010-06-29_from-list-comprehensions-to-generator-ex:comprehensions-faster-no-stack-frame`: "the list comprehension executes much faster ... because calling a lambda function creates a new stack frame while the expression in the list comprehension is e…"

### L-comprehension-vs-mapfilter (language)

List comprehensions are an alternative to map() and filter() that wins on realistic cases, and Van Rossum finds them more readable than the functional notation as complexity grows, rejecting the view that a terser lambda would fix map().

first 2010-06-29 08:39 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2010-06-29

- 2010-06-29 08:39 Guido van Rossum states [2010-06-29_from-list-comprehensions-to-generator-expressions.md line 10] `written:2010-06-29_from-list-comprehensions-to-generator-ex:comprehensions-vs-map-filter`: "List comprehensions provide an alternative to using the built-in map() and filter() functions."
- 2010-06-29 08:39 Guido van Rossum refines [2010-06-29_from-list-comprehensions-to-generator-expressions.md line 12] `written:2010-06-29_from-list-comprehensions-to-generator-ex:lambda-too-verbose-disagreement`: "It has been argued that the real problem here is that Python's lambda notation is too verbose ... Personally, I disagree—I find the list comprehension notation…"

### L-genexp (language)

Generator expressions, added in 2.4 and enabled by generators, represent a sequence of results without building a concrete list, saving memory, running in a separate frame so they don't leak the variable but were less efficient than list comprehensions in Python 2.

first 2010-06-29 08:39 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2010-06-29

- 2010-06-29 08:39 Guido van Rossum states [2010-06-29_from-list-comprehensions-to-generator-expressions.md line 14] `written:2010-06-29_from-list-comprehensions-to-generator-ex:generator-expressions-lazy`: "a similar notation that represents a sequence of results without turning it into a concrete list. The new feature is called a "generator expression"."
- 2010-06-29 08:39 Guido van Rossum refines [2010-06-29_from-list-comprehensions-to-generator-expressions.md line 56] `written:2010-06-29_from-list-comprehensions-to-generator-ex:genexp-needs-own-frame`: "Generator expressions are implemented using generators, whose execution requires a separate execution frame. Thus, generator expressions ... were less efficien…"

### L-genexp-syntax (language)

A generator expression's parentheses belong to the surrounding call, so a bare comma sequence after 'in' would be ambiguous; Python required a single expression there, unlike Python 2 list comprehensions, choosing not to guess and not to break existing list-comprehension code.

first 2010-06-29 08:39 by Guido van Rossum; 3 rows, 3 witnesses, 1 days, last 2010-06-29

- 2010-06-29 08:39 Guido van Rossum states [2010-06-29_from-list-comprehensions-to-generator-expressions.md line 36] `written:2010-06-29_from-list-comprehensions-to-generator-ex:genexp-ambiguity-parentheses-not-part-of-syntax`: "the parentheses around a generator expression are not technically part of the generator expression syntax ... there would be two interpretations"
- 2010-06-29 08:39 Guido van Rossum refines [2010-06-29_from-list-comprehensions-to-generator-expressions.md line 18] `written:2010-06-29_from-list-comprehensions-to-generator-ex:genexp-syntax-stricter-than-listcomp`: "in Python 2, this is a valid list comprehension: ... However this is not a valid generator expression"
- 2010-06-29 08:39 Guido van Rossum refines [2010-06-29_from-list-comprehensions-to-generator-expressions.md line 44] `written:2010-06-29_from-list-comprehensions-to-generator-ex:refuse-to-guess-ambiguity`: "we decided not to guess in this case, and the generator comprehension was required to have a single expression ... after its 'in' keyword. But at the time we d…"

### L-list-comprehension (language)

A list comprehension produces a list of a sequence's values selected by an optional predicate and mapped by a function, a Pythonic interpretation of the mathematical set-builder notation, with multiple for-clauses allowed for nested loops.

first 2010-06-29 08:39 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2010-06-29

- 2010-06-29 08:39 Guido van Rossum states [2010-06-29_from-list-comprehensions-to-generator-expressions.md line 7] `written:2010-06-29_from-list-comprehensions-to-generator-ex:comprehension-syntax`: "[f(x) for x in S if P(x)] This produces a list containing the values of the sequence S selected by the predicate P and mapped by the function f."
- 2010-06-29 08:39 Guido van Rossum refines [2010-06-29_from-list-comprehensions-to-generator-expressions.md line 2] `written:2010-06-29_from-list-comprehensions-to-generator-ex:list-comprehensions-from-set-notation`: "they are a Pythonic interpretation of a well-known notation for sets used by mathematicians"

### L-listcomp-genexp-equivalence (language)

In Python 3 a list comprehension was made fully equivalent to list() applied to the corresponding generator expression, so it was given the stricter genexp syntax.

first 2010-06-29 08:39 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2010-06-29

- 2010-06-29 08:39 Guido van Rossum states [2010-06-29_from-list-comprehensions-to-generator-expressions.md line 46] `written:2010-06-29_from-list-comprehensions-to-generator-ex:listcomp-equivalent-to-list-of-genexp`: "we wanted the list comprehension ... to be fully equivalent to the following expansion using the built-in list() function applied to a generator expression ...…"

### L-listcomp-leak (language)

Python 2 list comprehensions leaked the loop control variable into the surrounding scope, an intentional speed compromise; Python 3 fixed this by using the generator-expression implementation strategy, and with general speedups both forms became faster with no speed difference, removing the performance argument.

first 2010-06-29 08:39 by Guido van Rossum; 3 rows, 3 witnesses, 1 days, last 2010-06-29

- 2010-06-29 08:39 Guido van Rossum states [2010-06-29_from-list-comprehensions-to-generator-expressions.md line 52] `written:2010-06-29_from-list-comprehensions-to-generator-ex:loop-variable-leak-dirty-secret`: "the list comprehension "leaks" the loop control variable into the surrounding scope ... It started out as an intentional compromise to make list comprehensions…"
- 2010-06-29 08:39 Guido van Rossum refines [2010-06-29_from-list-comprehensions-to-generator-expressions.md line 60] `written:2010-06-29_from-list-comprehensions-to-generator-ex:python3-both-faster-no-gap`: "both list comprehensions and generator expressions in Python 3 are actually faster than they were in Python 2! (And there is no longer a speed difference betwe…"
- 2010-06-29 08:39 Guido van Rossum refines [2010-06-29_from-list-comprehensions-to-generator-expressions.md line 58] `written:2010-06-29_from-list-comprehensions-to-generator-ex:python3-fix-leak-via-genexp-strategy`: "in Python 3, we decided to fix the "dirty little secret" of list comprehensions by using the same implementation strategy as for generator expressions ... the…"

### L-setbuilder-difference (language)

Mathematical set-builder notation implies a universal set understood from context; Python has no universal set and, in Python 2.0, no sets at all, which forced a different notation.

first 2010-06-29 08:39 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2010-06-29

- 2010-06-29 08:39 Guido van Rossum states [2010-06-29_from-list-comprehensions-to-generator-expressions.md line 4] `written:2010-06-29_from-list-comprehensions-to-generator-ex:no-universal-set-in-python`: "In math, this form implies a universal set that is understood by the reader ... In Python, there is no concept of a universal set, and in Python 2.0, there wer…"

### L-floor-division (language)

Python's integer division returns the floor, rounding toward negative infinity rather than truncating toward zero like C, matching number theory's preferred convention and paired with modulo to satisfy a mathematical relationship, with a worry about extending the floor rule to floating-point modulo.

first 2010-08-24 09:49 by Guido van Rossum; 10 rows, 9 witnesses, 1 days, last 2010-08-24

- 2010-08-24 09:49 Guido van Rossum refines [2010-08-24_why-python-s-integer-division-floors.md line 20] `written:2010-08-24_why-python-s-integer-division-floors:div-and-mod-go-together`: "The integer division operation (//) and its sibling, the modulo operation (%), go together and satisfy a nice mathematical relationship (all variables are inte…"
- 2010-08-24 09:49 Guido van Rossum refines [2010-08-24_why-python-s-integer-division-floors.md line 42] `written:2010-08-24_why-python-s-integer-division-floors:floating-point-modulo-hesitation`: "Tim Peters ... has expressed some worry about my desire to extend these rules to floating point modulo. He's probably right; the truncate-towards-negative-infi…"
- 2010-08-24 09:49 Guido van Rossum refines [2010-08-24_why-python-s-integer-division-floors.md line 10] `written:2010-08-24_why-python-s-integer-division-floors:floor-affects-only-negative-operands`: "if one of the operands is negative, the result is floored, i.e., rounded away from zero (towards negative infinity)"
- 2010-08-24 09:49 Guido van Rossum refines [2010-08-24_why-python-s-integer-division-floors.md line 32] `written:2010-08-24_why-python-s-integer-division-floors:follows-number-theory-convention`: "In mathematical number theory, mathematicians always prefer the latter choice (see e.g. Wikipedia). For Python, I made the same choice"
- 2010-08-24 09:49 Guido van Rossum states [2010-08-24_why-python-s-integer-division-floors.md line 2] `written:2010-08-24_why-python-s-integer-division-floors:integer-division-floors`: "explain why integer division in Python returns the floor of the result instead of truncating towards zero like C"
- 2010-08-24 09:49 Guido van Rossum refines [2010-08-24_why-python-s-integer-division-floors.md line 32] `written:2010-08-24_why-python-s-integer-division-floors:modulo-where-sign-is-uninteresting`: "there are some interesting applications of the modulo operation where the sign of a is uninteresting"
- ... 2 more rows
- 2010-08-24 09:49 Guido van Rossum refines [2010-08-24_why-python-s-integer-division-floors.md line 30] `written:2010-08-24_why-python-s-integer-division-floors:two-choices-for-negative-a`: "if you truncate q towards zero, r will become negative, so that the invariant changes to 0 <= abs(r) < otherwise, you can floor q towards negative infinity, an…"
- 2010-08-24 09:49 Guido van Rossum refines [2010-08-24_why-python-s-integer-division-floors.md line 40] `written:2010-08-24_why-python-s-integer-division-floors:why-c-differs`: "Probably the hardware didn't do this at the time C was designed. And the hardware probably didn't do it this way because in the oldest hardware, negative numbe…"

### L-halfopen-slicing-indexing (language)

Python chose 0-based indexing with half-open slice intervals and suitable defaults, so common slicing cases (first n items, next n from i) come out as a[:n] and a[i:i+n] without +1/-1 corrections.

first 2013-10-24 08:44 by Guido van Rossum; 10 rows, 10 witnesses, 1 days, last 2013-10-24

- 2013-10-24 08:44 Guido van Rossum refines [2013-10-24_why-python-uses-0-based-indexing.md line 33] `written:2013-10-24_why-python-uses-0-based-indexing:adjacency-invariant`: "the invariant that when two / slices are adjacent, the first slice's end index is the second slice's / start index is just too beautiful to ignore."
- 2013-10-24 08:44 Guido van Rossum refines [2013-10-24_why-python-uses-0-based-indexing.md line 12] `written:2013-10-24_why-python-uses-0-based-indexing:avoid-plus-minus-one-compensations`: "It would be nice if both of these could be / expressed as without awkward +1 or -1 compensations."
- 2013-10-24 08:44 Guido van Rossum refines [2013-10-24_why-python-uses-0-based-indexing.md line 24] `written:2013-10-24_why-python-uses-0-based-indexing:closed-intervals-force-minus-one`: "Using closed intervals, you'd have to / write a[i:i+n-1] for the n items starting at i."
- 2013-10-24 08:44 Guido van Rossum refines [2013-10-24_why-python-uses-0-based-indexing.md line 10] `written:2013-10-24_why-python-uses-0-based-indexing:common-slicing-use-cases`: "most common use cases for slicing are \"get the first n items\" and \"get / the next n items starting at i\""
- 2013-10-24 08:44 Guido van Rossum refines [2013-10-24_why-python-uses-0-based-indexing.md line 31] `written:2013-10-24_why-python-uses-0-based-indexing:fuzzy-memory-on-other-use-cases`: "TBH / this is where my memory gets fuzzy, but I think I was swayed by the / elegance of half-open intervals."
- 2013-10-24 08:44 Guido van Rossum refines [2013-10-24_why-python-uses-0-based-indexing.md line 25] `written:2013-10-24_why-python-uses-0-based-indexing:index-length-notation-as-abc-did`: "So perhaps using the / slice length would be more elegant with 1-based indexing? ... And this is in fact what ABC did -- it used a different / notation so you…"
- ... 2 more rows
- 2013-10-24 08:44 Guido van Rossum states [2013-10-24_why-python-uses-0-based-indexing.md line 6] `written:2013-10-24_why-python-uses-0-based-indexing:slice-notation-decided-indexing-base`: "I think that one of the issues that helped me decide / was slice notation."
- 2013-10-24 08:44 Guido van Rossum states [2013-10-24_why-python-uses-0-based-indexing.md line 15] `written:2013-10-24_why-python-uses-0-based-indexing:zero-based-half-open-defaults-elegant`: "Using / 0-based indexing, half-open intervals, and suitable defaults (as Python / ended up having), they are beautiful: a[:n] and a[i:i+n]"

### L-metaclass-not-ruby (language)

Python's metaclass design did not come from Ruby.

first 2013-10-24 09:58 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2013-10-24

- 2013-10-24 09:58 Guido van Rossum states [2013-10-24_origin-of-metaclasses-in-python.md line 2] `written:2013-10-24_origin-of-metaclasses-in-python:metaclass-design-not-from-ruby`: "whether Python's metaclass design came from Ruby. It did not."

### L-newstyle-iteration (language)

New-style classes were only the second or third iteration of the metaclass idea, which Van Rossum had already written about in 1998.

first 2013-10-24 09:58 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2013-10-24

- 2013-10-24 09:58 Guido van Rossum states [2013-10-24_origin-of-metaclasses-in-python.md line 11] `written:2013-10-24_origin-of-metaclasses-in-python:new-style-classes-an-iteration`: "New-style classes were just the second or third iteration of the idea."

### L-ruby-inspired-by-python (other)

Ruby was inspired by Python; Matz told Van Rossum his inspiration was 20% Python, 80% Perl, with Larry Wall as his hero.

first 2013-10-24 09:58 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2013-10-24

- 2013-10-24 09:58 Guido van Rossum states [2013-10-24_origin-of-metaclasses-in-python.md line 5] `written:2013-10-24_origin-of-metaclasses-in-python:ruby-inspired-by-python`: "Ruby was in fact\ninspired by Python. Mats once told me that his inspiration was 20%\nPython, 80% Perl, and that Larry Wall is his hero."

### L-smalltalk-bytecode-influence (language)

Smalltalk's bytecode, which Van Rossum read about in a book by Adele Goldberg and others, was a bigger influence on Python's bytecode.

first 2013-10-24 09:58 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2013-10-24

- 2013-10-24 09:58 Guido van Rossum states [2013-10-24_origin-of-metaclasses-in-python.md line 27] `written:2013-10-24_origin-of-metaclasses-in-python:smalltalk-bytecode-influence`: "Smalltalk's bytecode was a bigger influence of Python's\nbytecode though."

### L-smalltalk-metaclass-unaware (other)

Van Rossum was only vaguely aware of Smalltalk at the time and was surprised, reading about it much later, by its use of metaclasses, which differs from Python's or Ruby's.

first 2013-10-24 09:58 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2013-10-24

- 2013-10-24 09:58 Guido van Rossum states [2013-10-24_origin-of-metaclasses-in-python.md line 25] `written:2013-10-24_origin-of-metaclasses-in-python:smalltalk-metaclasses-different-and-late`: "I was only vaguely aware of Smalltalk at the time; I\nremember being surprised by its use of metaclasses (which is quite different from that in Python or Ruby!…"

### L-type-is-object (language)

From its original 1990 design Python made 'type' itself an object: every object's type pointer points to a special object of C function pointers (like a C++ vtable), and a type's own type is a special meta-type recognized by being its own type.

first 2013-10-24 09:58 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2013-10-24

- 2013-10-24 09:58 Guido van Rossum states [2013-10-24_origin-of-metaclasses-in-python.md line 21] `written:2013-10-24_origin-of-metaclasses-in-python:meta-type-as-its-own-type`: "The type of a type was always a\nspecial type object, which you could call a meta-type, to be recognized\nbecause it was its own type."
- 2013-10-24 09:58 Guido van Rossum refines [2013-10-24_origin-of-metaclasses-in-python.md line 17] `written:2013-10-24_origin-of-metaclasses-in-python:type-as-object-from-the-start`: "even Python's original design (in 1990, published in\n1991) had the notion that 'type' was itself an object. The type pointer\nin any object has always been a…"

### L-builtins-reassignable (language)

Built-in names are ordinary identifiers the parser gives no special knowledge, looked up at run time and freely reassignable, so adding a new built-in never invalidates code that used that name.

first 2013-11-10 14:40 by Guido van Rossum; 5 rows, 5 witnesses, 1 days, last 2013-11-10

- 2013-11-10 14:40 Guido van Rossum states [2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 91] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:adding-a-builtin-must-not-break-existing-code`: "In Python 2.6, we added a built-in function named 'bytes'... Should your code now be considered invalid? There's no reason for that, and in fact your code will…"
- 2013-11-10 14:40 Guido van Rossum restates [2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 80] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:allowing-builtin-reassignment-for-consistency-and-evolution`: "The answer is subtle, and has to do with consistency and evolution of the language."
- 2013-11-10 14:40 Guido van Rossum refines [2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 55] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:builtins-are-ordinary-names-to-the-parser`: "The parser had no special knowledge of None -- just like it doesn't have special knowledge of built-in types like int, float or str... All of these are treated…"
- 2013-11-10 14:40 Guido van Rossum refines [2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 69] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:builtins-are-reassignable`: "if you really want to mess with your readers, you can write code that reassigns built-ins"
- 2013-11-10 14:40 Guido van Rossum refines [2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 97] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:new-builtins-are-cheap-to-add`: "at least we don't have to worry about breaking working code by merely adding something to the language. The (small) price we pay for this is the possibility th…"

### L-constant-convention (language)

A constant such as an all-caps identifier is only a convention the parser neither knows nor enforces, distinct from a literal.

first 2013-11-10 14:40 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2013-11-10

- 2013-11-10 14:40 Guido van Rossum states [2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 46] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:constant-versus-literal`: "the all-caps form of the name suggests to the reader that it is probably not changed anywhere in the code... but this is just a convention, and the Python pars…"

### L-keyword-definition (language)

A keyword (reserved word) looks like an identifier but the parser treats it as a token of the language, and so it can never be used to name a variable, function, or class.

first 2013-11-10 14:40 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2013-11-10

- 2013-11-10 14:40 Guido van Rossum refines [2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 15] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:keyword-cannot-name-a-variable`: "The important thing to remember about keywords is that a keyword cannot be used to name a variable (or function, class, etc.)."
- 2013-11-10 14:40 Guido van Rossum states [2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 13] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:keyword-is-identifier-shaped-but-a-token`: "A keyword, in the context of defining the syntax of a language, also known as a reserved word, is something that looks like an identifier in the language, but…"

### L-keywords-costly (language)

Every reserved word must be known by everyone using Python since it can never be a name, so the list is kept small and many proposed features were killed or changed to avoid needing a new keyword.

first 2013-11-10 14:40 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2013-11-10

- 2013-11-10 14:40 Guido van Rossum refines [2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 95] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:new-keywords-kill-or-reshape-features`: "many proposed new features have been killed because they would require a new keyword; others have been modified to avoid that need."
- 2013-11-10 14:40 Guido van Rossum states [2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 93] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:reserved-words-impose-a-global-cost`: "everyone using Python has to know about all the reserved words in the language... For this reason, we try to keep the list of reserved words small, and the cor…"

### L-literal-definition (language)

A literal is an element of an expression describing a constant value, recognized by the parser and producing a different parse tree from a name, so the left-hand side of an assignment must be a variable and a literal is not one.

first 2013-11-10 14:40 by Guido van Rossum; 3 rows, 3 witnesses, 1 days, last 2013-11-10

- 2013-11-10 14:40 Guido van Rossum refines [2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 51] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:assignment-target-must-be-a-variable`: "the left-hand side of the assignment operator (=) must be a variable, and a literal is not a variable. (The exact definition of variable is complex, since some…"
- 2013-11-10 14:40 Guido van Rossum states [2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 17] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:literal-describes-a-constant-value`: "A literal, on the other hand, is an element of an expression that describes a constant value... Literals are recognized by the parser, and the exact rules for…"
- 2013-11-10 14:40 Guido van Rossum refines [2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 67] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:literals-parse-differently-from-names`: "the parser treats numeric and string literals as different from identifiers... the first three will still be accepted by the parser (<name> = <name>), while th…"

### L-none-keyword (language)

None was eventually made a reserved word for mostly social reasons (its centrality, users horrified that assignment to it was allowed), with minor benefits in speed and catching typos and no downside since nothing assigns to it.

first 2013-11-10 14:40 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2013-11-10

- 2013-11-10 14:40 Guido van Rossum refines [2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 101] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:none-keyword-decision-had-no-downside`: "In the end we decided that there was no downside to making None a keyword (there is no code that actually assigns to it) and it might make some code a tiny bit…"
- 2013-11-10 14:40 Guido van Rossum states [2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 99] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:none-made-keyword-for-social-reasons`: "Why did we eventually make None a reserved word? Frankly, the reasons were perhaps mostly social... None is so central to using Python that you really can't be…"

### L-none-singleton (language)

None is a singleton object used throughout the language and library to represent the absence of some other value.

first 2013-11-10 14:40 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2013-11-10

- 2013-11-10 14:40 Guido van Rossum states [2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 55] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:none-as-singleton-for-absence`: "None is a singleton object (meaning there is only one None), used in many places in the language and library to represent the absence of some other value."

### L-none-true-false-both (language)

None, True and False are both keywords (how the parser recognizes them) and literals (their role standing for constant values in expressions).

first 2013-11-10 14:40 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2013-11-10

- 2013-11-10 14:40 Guido van Rossum states [2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 109] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:none-true-false-are-both-keywords-and-literals`: "My answer is that they are both. They are keywords because that's how the parser recognizes them. They are literals because that's their role in expressions an…"

### L-true-false-keywords (language)

True and False were first introduced as built-in constants rather than keywords to keep backward compatibility with code defining its own, then made keywords in Python 3 by analogy to None.

first 2013-11-10 14:40 by Guido van Rossum; 3 rows, 3 witnesses, 2 days, last 2013-11-11

- 2013-11-10 14:40 Guido van Rossum refines [2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md line 105] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:true-false-became-keywords-in-python-3`: "by the time Python 3 came around, when we looked at opportunities for cleaning up the language, we found that it was logical to make True and False keywords, b…"
- 2013-11-10 14:40 Guido van Rossum states [2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md] `written:2013-11-10_the-story-of-none-true-and-false-and-an-:true-false-introduced-as-builtins-not-keywords`: "we definitely did not want to break any packages that were defining their own True and False constants... essentially our hand was forced in this case, and we…"
- 2013-11-11 16:29 Guido van Rossum refines [2013-11-11_the-history-of-bool-true-and-false.md line 2] `written:2013-11-11_the-history-of-bool-true-and-false:true-false-not-reserved-words`: "Writing up the reasons why True and False, when introduced, weren't reserved words"

### L-bool-type-history (language)

The bool type was formally introduced in Python 2.3 via PEP 285, with bool() and True/False backported into the 2.2.1 bugfix release (where they were a function and plain ints) to ease backporting of 2.3 code.

first 2013-11-11 16:29 by Guido van Rossum; 3 rows, 3 witnesses, 1 days, last 2013-11-11

- 2013-11-11 16:29 Guido van Rossum refines [2013-11-11_the-history-of-bool-true-and-false.md line 16] `written:2013-11-11_the-history-of-bool-true-and-false:bool-added-in-bugfix-release-2-2-1`: "Added new builtin function bool() and new builtin constants True and ... False to ease backporting of code developed for Python 2.3."
- 2013-11-11 16:29 Guido van Rossum refines [2013-11-11_the-history-of-bool-true-and-false.md line 22] `written:2013-11-11_the-history-of-bool-true-and-false:bool-differs-between-2-2-1-and-2-3`: "in 2.3, bool is a new type; in 2.2.1, bool() is a built-in function and the constants are just ints."
- 2013-11-11 16:29 Guido van Rossum states [2013-11-11_the-history-of-bool-true-and-false.md line 4] `written:2013-11-11_the-history-of-bool-true-and-false:bool-formally-introduced-2-3-pep-285`: "It was formally introduced in Python 2.3, as a new type with two constants, and the type was introduced in PEP 285 ("Adding a bool type")."

### L-no-feature-in-bugfix (method)

Adding a new feature in a bugfix release (bool in 2.2.1) was the most criticized such instance and would not be done now.

first 2013-11-11 16:29 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2013-11-11

- 2013-11-11 16:29 Guido van Rossum states [2013-11-11_the-history-of-bool-true-and-false.md line 22] `written:2013-11-11_the-history-of-bool-true-and-false:feature-in-bugfix-release-regret`: "This was the last (and the most criticized) time we added a new feature in a bugfix release -- we'd never do that these days."

### L-handwritten-lexer (language)

Van Rossum chose not to use a lexer generator, writing the lexer by hand, because the Lex he knew would segfault on long tokens and he figured indentation would be hard to teach a generator.

first 2018-05-12 09:37 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2018-05-12

- 2018-05-12 09:37 Guido van Rossum states [2018-05-12_the-origins-of-pgen.md line 12] `written:2018-05-12_the-origins-of-pgen:no-generator-for-lexer`: "For the lexer I decided I would not use a generator ... the version of Lex that I was familiar with would just segfault when trying to scan a token longer than…"

### L-lalr-regret (language)

In hindsight Van Rossum might choose a more powerful LALR(1) parsing engine, since several grammar areas (e.g. keyword arguments) need more power than LL(1).

first 2018-05-12 09:37 by Guido van Rossum; 1 rows, 1 witnesses, 1 days, last 2018-05-12

- 2018-05-12 09:37 Guido van Rossum states [2018-05-12_the-origins-of-pgen.md line 53] `written:2018-05-12_the-origins-of-pgen:would-choose-more-powerful-engine`: "If I had to do it all over again I might opt for a more powerful parsing engine, perhaps a version of LALR(1) ... the rule 'arg: [NAME =] expr' is not a valid…"

### L-own-parser-generator (other)

Van Rossum wrote his own LL(1) parser generator because the landscape of parser generators was sparse, he disliked Yacc, and he was unfamiliar with or distrusted more advanced techniques as too inefficient.

first 2018-05-12 09:37 by Guido van Rossum; 2 rows, 2 witnesses, 1 days, last 2018-05-12

- 2018-05-12 09:37 Guido van Rossum refines [2018-05-12_the-origins-of-pgen.md line 10] `written:2018-05-12_the-origins-of-pgen:avoided-advanced-techniques`: "I was not familiar with more advanced techniques, or I deemed them too inefficient."
- 2018-05-12 09:37 Guido van Rossum states [2018-05-12_the-origins-of-pgen.md line 8] `written:2018-05-12_the-origins-of-pgen:why-own-parser-generator`: "The reason for writing my own parser generator was that at the time the landscape of parser generators ... was pretty sparse ... I had used Yacc in college ...…"

### L-pgen2 (other)

A Python rewrite of pgen (pgen2, under lib2to3) was created at Elemental Security with an input format identical to the original, was used for 2to3, and in Python 3.8 replaced the C pgen.

first 2018-05-12 09:37 by Guido van Rossum; 4 rows, 3 witnesses, 1 days, last 2018-05-12

- 2018-05-12 09:37 Guido van Rossum refines [2018-05-12_the-origins-of-pgen.md line 14] `written:2018-05-12_the-origins-of-pgen:pgen2-origin-at-elemental`: "I decided to design something vaguely like Python, implemented in Python, and decided that I wanted to reuse pgen, but with a backend in Python, using tokenize…"
- 2018-05-12 09:37 Guido van Rossum refines [2018-05-12_the-origins-of-pgen.md line 14] `written:2018-05-12_the-origins-of-pgen:pgen2-reused-for-2to3`: "it made sense to use those tools for 2to3. (It was easy to generate a Python parser with it because the input format was identical to the original pgen -- I ju…"
- 2018-05-12 09:37 Guido van Rossum refines [2018-05-12_the-origins-of-pgen.md line 63] `written:2018-05-12_the-origins-of-pgen:python38-drops-c-pgen`: "UPDATE March 2019: Python 3.8 will drop the C version of pgen, in favor of a tweaked version of pgen2."
- 2018-05-12 09:37 Guido van Rossum states [2018-05-12_the-origins-of-pgen.md line 4] `written:2018-05-12_the-origins-of-pgen:two-pgens-c-and-python`: "There are actually two pgens. The original, in C, and a rewrite in Python, under lib2to3/pgen2."

### L-regex-ebnf-grammar (language)

pgen used regular-expression (EBNF) notation instead of standard BNF to make the grammar easier to read and resolve conflicts without awkwardly named helper rules, without changing the LL(1) power, with parse-tree nodes of variable arity and tables derived by regex->NFA->DFA.

first 2018-05-12 09:37 by Guido van Rossum; 7 rows, 7 witnesses, 1 days, last 2018-05-12

- 2018-05-12 09:37 Guido van Rossum refines [2018-05-12_the-origins-of-pgen.md line 49] `written:2018-05-12_the-origins-of-pgen:ebnf-to-bnf-not-improvement`: "Converting EBNF to BNF and taking it from there would cause awkward extra parse tree node types, so I don't think that would have been an improvement."
- 2018-05-12 09:37 Guido van Rossum refines [2018-05-12_the-origins-of-pgen.md line 23] `written:2018-05-12_the-origins-of-pgen:parsing-engine-and-empty-productions`: "the parsing engine ... still works with parsing tables derived from such rules through the regex -> NFA -> DFA transformation; I think the requirement not to h…"
- 2018-05-12 09:37 Guido van Rossum refines [2018-05-12_the-origins-of-pgen.md line 44] `written:2018-05-12_the-origins-of-pgen:power-unchanged-ll1`: "It certainly did not change the power beyond LL(1), nor did it reduce the power. And yes by "regular expressions" I meant the EBNF conventions -- I'm not sure…"
- 2018-05-12 09:37 Guido van Rossum refines [2018-05-12_the-origins-of-pgen.md line 38] `written:2018-05-12_the-origins-of-pgen:regex-for-readability`: "the reason I used regular expressions was probably to make the grammar easier to read ... no helper rules with awkward names, and [optional] parts or repeated*…"
- 2018-05-12 09:37 Guido van Rossum states [2018-05-12_the-origins-of-pgen.md line 8] `written:2018-05-12_the-origins-of-pgen:regex-instead-of-bnf`: "I had one improvement over that that I wanted to try out: using regular expressions (sort of) instead of the standard BNF format. The Dragon book had also taug…"
- 2018-05-12 09:37 Guido van Rossum refines [2018-05-12_the-origins-of-pgen.md line 19] `written:2018-05-12_the-origins-of-pgen:regex-to-resolve-conflicts`: "I may have seen this as a new (to me) way of addressing the various conflicts that may occur without adding helper rules. E.g. what that page calls left-factor…"
- 2018-05-12 09:37 Guido van Rossum refines [2018-05-12_the-origins-of-pgen.md line 28] `written:2018-05-12_the-origins-of-pgen:variable-number-of-children`: "the parse tree nodes produced by the parsing engine would have a variable number of children ... A simple check in the code generator would then be needed to d…"

## Unplaced rows

