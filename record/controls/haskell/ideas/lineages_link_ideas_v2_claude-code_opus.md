# Lineages of the ideas about Luthier

Written by `scripts/link_ideas.py` (link_ideas v1) for Luciano and for the distillation. Prompt `link_ideas_v2`
(sha256 a04a21445ebf), model opus at effort low via claude-code (2.1.197 (Claude Code)); 4 calls. Input: `record/controls/haskell/ideas/timeline.jsonl`, last read with sha256
a487c657e131. Who said an idea first and whether Luciano adopted a model's idea are computed from the rows' times and authors, not by the model.

Rows: 387 in the timeline; placed 387, unplaced 0, pending 0. Lineages: 319.

| scope | first said by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler |
|---|---|
| language | 190 |
| method | 34 |
| other | 95 |

First said by a model and then taken up by Luciano: 0.

## Lineages, by first appearance

### L-account-biased (other)

The authors' account is skewed toward the meetings and conversations they took part in.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [01_introduction.md] `written:2007-06-09_01-introduction:skew-toward-authors-participation`: "our account will be skewed towards the meetings and conversations in which we personally participated"

### L-adt-extended (language)

Algebraic data types were extended with newtypes, strictness annotations, and named fields.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 363] `written:2007-06-09_02-the-genesis-of-haskell:adt-extensions`: "Algebraic data types were extended in several ways: new-"

### L-adt-fundamental (language)

Data types and pattern matching are fundamental to most modern functional languages, Scheme excepted.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 3] `written:2007-06-09_05-data-types-and-pattern-matching:data-types-and-pattern-matching-fundamental`: "Data types and pattern matching are fundamental to most modern functional languages (with the notable exception of Scheme)."

### L-adt-via-modules (language)

Haskell uses the module system, not a special abstype construct, for abstract data types, trading extra clutter for inferable operation types and a distinct type-class instance.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 3 rows, 3 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [05_data-types-and-pattern-matching.md line 123] `written:2007-06-09_05-data-types-and-pattern-matching:abstract-type-distinct-class-instance`: "The most important point is that Haskell's solution allows one to give a different instance to a type-class for the abstract type than for its representation .…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [05_data-types-and-pattern-matching.md line 121] `written:2007-06-09_05-data-types-and-pattern-matching:abstract-types-tradeoff`: "Haskell's solution is somewhat cluttered by the Stk constructors, but in exchange an extra construct is avoided, and the types of the operations can be inferre…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 105] `written:2007-06-09_05-data-types-and-pattern-matching:abstract-types-via-module-system`: "In Haskell, instead of a special construct, the module system is used to support data abstraction. One constructs an abstract data type by introducing an algeb…"

### L-aetion-static-types (other)

Aetion chose Haskell for its rich static type system, open-source compilers and active research community, static typing catching many errors that would otherwise surface in the field.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:rich-static-type-system-as-reason-to-choose`: "They chose Haskell, because of its rich static type system, open-source compilers, and its active research community."

### L-algebraic-types-easy (language)

Basic algebraic types were straightforward, but pattern matching, abstract types, tuples, newtypes, records, n+k patterns and views raised issues.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 5] `written:2007-06-09_05-data-types-and-pattern-matching:basic-algebraic-types-straightforward-rest-interesting`: "The inclusion of basic algebraic types was straightforward, but interesting issues arose for pattern matching, abstract types, tuples, new types, records, n+k…"

### L-algebraic-types-origin (language)

Algebraic data types originated in Burstall's NPL and Hope and reached ML's and Miranda's successors.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 84] `written:2007-06-09_02-the-genesis-of-haskell:hope-algebraic-data-types`: "Hope, the language that introduced algebraic data types"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [05_data-types-and-pattern-matching.md line 11] `written:2007-06-09_05-data-types-and-pattern-matching:algebraic-types-history`: "Algebraic types as a programming language feature first appeared in Burstall's NPL ... They were absent from the original ML ... and KRC ..., but appeared in t…"

### L-algorithmic-debugging (other)

In algorithmic debugging the debugger takes the initiative, descending through calls to locate the bug.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 272] `written:2007-06-09_10-profiling-and-debugging:algorithmic-debugging`: "an approach in which the debugger, rather than the user, takes the initiative to explore the program's behaviour."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [10_profiling-and-debugging.md line 284] `written:2007-06-09_10-profiling-and-debugging:algorithmic-debugging-laziness-problem`: "If they were computed early by an algorithmic debugger, in order to display them in questions to the user, then this itself might trigger faults or loops that…"

### L-application-juxtaposition (language)

Function application is juxtaposition, associating to the left.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 103] `written:2007-06-09_04-syntax:application-by-juxtaposition`: "Function application is denoted by juxtaposition and associates to the left. Thus, f x y is parsed (f x) y."

### L-array-inplace-messier (language)

Array processing and algorithms relying on in-place update are messier in Haskell than in imperative languages.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md line 139] `written:2007-06-09_12-the-impact-of-haskell:in-place-update-messier`: "Array processing and algorithms using in-place update are ... messier in Haskell."

### L-arrows (language)

Arrows, proposed by Hughes, are an abstract view of computation like monads but more general, easier to use with syntactic support.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 525] `written:2007-06-09_07-monads-and-input-output:arrows-generalise-monads`: "Arrows are an abstract view of computation with the same flavour as monads, but in a more general setting."

### L-at-patterns-tight (language)

@-patterns bind more tightly than anything, breaking the simple binding rule, probably a mistake.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 85] `written:2007-06-09_04-syntax:at-patterns-bind-tightly-mistake`: "Sadly, this simple rule is not adhered to by @-patterns, which bind more tightly than anything; this was probably a mistake"

### L-avoid-semicolon (language)

Without side effects there is no sequencing, so the committee avoided the semicolon and its imperative baggage.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 30] `written:2007-06-09_04-syntax:avoid-semicolon-no-sequencing`: "the feeling of the Haskell Committee was that we should avoid the semicolon and its sequential, imperative baggage."

### L-backquote-infix (language)

A function identifier in backquotes is used infix, for generality and readability.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 150] `written:2007-06-09_04-syntax:backquotes-function-to-infix`: "Our simple solution was to enclose a function identifier in backquotes. For example, x 'f' y is the same as f x y."

### L-backus-lecture (other)

Backus's Turing Award lecture recast functional programming as a radical attack on the whole programming enterprise.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 4] `written:2007-06-09_02-the-genesis-of-haskell:functional-programming-as-practical-tool`: "which positioned functional programming as a radical attack on the whole programming enterprise, from hardware architecture upwards"

### L-bind-vs-ml (language)

Bind is analogous to let in ML but the types record the effect, and monads give freedom in defining return and bind where ML fixes one notion of computation.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 176] `written:2007-06-09_07-monads-and-input-output:monads-vs-ml-sequencing`: "monads give quite a bit of freedom in how one defines the operators return and >>=, while ML fixes a single built-in notion of computation and sequencing."

### L-blessed-addenda (method)

The FFI effort spawned "Blessed Addenda", well-specified appendices to the Haskell 98 Report giving precise advice on implementing language extensions.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [08_haskell-in-middle-age.md line 24] `written:2007-06-09_08-haskell-in-middle-age:blessed-addenda`: "the idea of “Blessed Addenda” emerged, a well-specified Appendix to the Haskell 98 Report that contained precise advice regarding the implementation of a varie…"

### L-bluespec-two-level (language)

Bluespec is a two-level language: the full power of Haskell is available at compile time but almost all Haskell constructs are eliminated by a partial evaluator.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:haskell-as-two-level-compile-time-language`: "Bluespec is really a two-level language. The full power of Haskell is available at compile time, but almost all Haskell language constructs are eliminated by a…"

### L-bottom-every-type (language)

A diverging or error expression has the value bottom, which belongs to every type.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 132] `written:2007-06-09_05-data-types-and-pattern-matching:bottom-value-every-type`: "An expression that diverges (or calls Haskell's error function) is considered to have the value 'bottom', usually written ⊥, a value that belongs to every type."

### L-bottom-tuple-distinct (language)

Whether bottom and (bottom, bottom) are distinct depends on lifted versus unlifted tuple semantics.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 135] `written:2007-06-09_05-data-types-and-pattern-matching:lifted-vs-unlifted-tuple-semantics`: "are ⊥ and (⊥, ⊥) distinct values? In the jargon of denotational semantics, a lifted tuple semantics distinguishes the two values, while an unlifted semantics t…"

### L-bytestring-fusion (language)

Data.ByteString represents strings as byte vectors and uses GHC's rewrite rules to program the optimiser so loop fusion happens when bytestring functions compose, the rules' correctness tested by QuickCheck.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:rewrite-rules-for-performance`: "by using GHC’s rewrite rules to program the compiler’s optimiser, so that loop fusion is performed when bytestring functions are composed"

### L-cabal-hackage (other)

Cabal, led by Isaac Jones from 2004, supports constructing and distributing Haskell packages, and Hackage is a Cabal package server for finding and downloading them.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 11] `written:2007-06-09_09-implementations:cabal-and-hackage-for-packaging`: "Isaac Jones took up the challenge of leading an effort to specify and implement a system called Cabal that supports the construction and distribution of Haskel…"

### L-cbv-recursive-combinators (language)

Call-by-value languages disallow recursive combinator definitions, forcing eta-expansion that clutters code and wrecks the abstraction.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 114] `written:2007-06-09_11-applications:call-by-value-cost-of-eta-expansion`: "In call-by-value languages, recursive definitions like this are generally not allowed. Instead, one would have to eta-expand the definition, thereby cluttering…"

### L-class-bounded-quantification (language)

A type-class constraint expresses a form of bounded quantification: a function is typed for any type that is an instance of a given class.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 39] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:bounded-quantification`: "The type signature for member uses a form of bounded quantification: it declares that member has type a -> [a] -> Bool, for any type a that is an instance of t…"

### L-class-irritations (language)

The class system causes minor irritations, sometimes producing puzzling error messages.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md line 136] `written:2007-06-09_12-the-impact-of-haskell:class-system-error-messages`: "The class system causes minor irritations, sometimes leading to ... puzzling error messages for students."

### L-classes-monads-symbiosis (language)

Type classes and monads had a symbiotic relationship: classes made monads accessible and popular while monadic I/O ensured the adoption of higher-kinded polymorphism.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 199] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-classes-supported-monads`: "The fact that type classes so directly supported monads made monads far more accessible and popular; and dually, the usefulness of monadic I/O ensured the adop…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler restates [07_monads-and-input-output.md line 315] `written:2007-06-09_07-monads-and-input-output:monads-typeclasses-symbiosis`: "This happy conjunction of monads and type classes gave the two a symbiotic relationship: each made the other much more attractive."

### L-clean-gui (other)

Clean's graphical I/O library was integral from early on, letting the user specify the interface with call-back data, unlike Haskell's fragmented GUI approach.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 450] `written:2007-06-09_11-applications:clean-integrated-io-vs-fragmented-haskell`: "A notable example is the Clean graphical I/O library, which formed an integral part of the Clean system from a very early stage ... (unlike the fragmented appr…"

### L-combinator-definition (language)

A combinator library, loosely defined, offers functions that combine functions into bigger functions.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 17] `written:2007-06-09_11-applications:combinator-library-definition`: "a combinator library offers functions (the combinators) that combine functions together to make bigger functions."

### L-combinator-dsel-same (language)

A combinator library can be seen as a domain-specific language, with little conceptual difference, the term chosen for historical reasons.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [11_applications.md line 383] `written:2007-06-09_11-applications:combinator-library-and-dsel-same`: "It is probably only for historical reasons that one project might use the term “combinator library” and another the term “DSL” (or “DSEL”)."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 38] `written:2007-06-09_11-applications:combinator-library-as-dsl`: "Another productive way to think of a combinator library is as a domain-specific language (DSL) for describing values of a particular type"

### L-combinator-influential (language)

Combinator libraries embody nothing fundamentally new yet the idea has been extremely influential.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 98] `written:2007-06-09_11-applications:combinator-libraries-not-new-but-influential`: "combinator libraries do not embody anything fundamentally new. Nevertheless, the idea has been extremely influential"

### L-committee-design (method)

Haskell was to be designed by a committee, not an individual.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [01_introduction.md line 10] `written:2007-06-09_01-introduction:design-by-committee`: "It was decided that a committee should be formed to design such a language"

### L-common-libraries (other)

Driven by user desire for cross-implementation compatibility, the Hugs, GHC and nhc teams began in 2001 to build a common open-source library set shipped with each compiler.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 39] `written:2007-06-09_09-implementations:cross-implementation-common-libraries`: "driven by user desire for cross-implementation compatibility, the Hugs, GHC and nhc teams began in 2001 to work together on a common, open-source set of librar…"

### L-community-success (other)

The Haskell community's size and quality is both the indicator of its success and its cause.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [01_introduction.md] `written:2007-06-09_01-introduction:community-as-cause-and-indicator-of-success`: "The size and quality of the Haskell community, its breadth and its depth, are both the indicator of Haskell’s success and its cause"

### L-concurrent-haskell (language)

Concurrent Haskell extends the IO monad with lightweight threads communicating through synchronised mutable MVars, inspired by Id's M-structures.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 481] `written:2007-06-09_07-monads-and-input-output:concurrent-haskell-mvars`: "Concurrent Haskell ... extends the IO monad with the ability to fork lightweight threads, each of which can perform I/O by itself"

### L-cons-not-evaluate (other)

Friedman and Wise framed lazy evaluation from Lisp with the slogan that cons should not evaluate its arguments.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 39] `written:2007-06-09_02-the-genesis-of-haskell:cons-should-not-evaluate-arguments`: "“Cons should not evaluate its arguments”"

### L-conservative-language (method)

The committee intended a conservative language embodying current consensus rather than breaking new ground.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 240] `written:2007-06-09_02-the-genesis-of-haskell:conservative-consensus-intent`: "we intended the language to be quite conservative, rather than to break new ground"

### L-constructors-capitalised (language)

Data constructors are capitalised and variables are not (from Miranda), a rule extended to infix constructors, type constructors and type variables.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 3 rows, 3 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 173] `written:2007-06-09_04-syntax:capitalisation-and-colon-conventions`: "We adopted from Miranda the convention that data constructors are capitalised while variables are not, and added a similar convention for infix constructors, w…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [05_data-types-and-pattern-matching.md line 60] `written:2007-06-09_05-data-types-and-pattern-matching:capitalization-rule-extended-to-types`: "Haskell further extended this rule to apply to type constructors ... and type variables ... This uniform rule was unusual."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler restates [05_data-types-and-pattern-matching.md line 55] `written:2007-06-09_05-data-types-and-pattern-matching:capitalized-constructors-from-miranda`: "Haskell also took from Miranda the rule that constructor names always begin with a capital, making it easy to distinguish constructors ... from variables ... I…"

### L-constructors-pattern-expr (language)

Data constructors serve both in pattern matching and in expressions.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 30] `written:2007-06-09_05-data-types-and-pattern-matching:data-constructors-two-roles`: "Data constructors can be used both in pattern-matching, to decompose a value of Maybe type, and in an expression, to build a value of Maybe type."

### L-continuation-io (language)

In the continuation I/O model each request/response pair is a transaction, a function taking failure and success continuations, and most programmers preferred it for its localised control flow.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 76] `written:2007-06-09_07-monads-and-input-output:continuation-io-transactions`: "a collection of transactions were defined that cap- tured the effect of each request/response pair in a continuationpassing style. Transactions were just funct…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [07_monads-and-input-output.md line 118] `written:2007-06-09_07-monads-and-input-output:continuations-preferred-localised-control`: "the continuation style was preferred by most programmers, since the flow of control was more localised."

### L-core-lint (other)

A Core Lint typechecker checks each pass stays well-typed, a surprisingly strong consistency check that catches most optimiser bugs cheaply, one of the biggest benefits of a typed intermediate language.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 130] `written:2007-06-09_09-implementations:core-lint-consistency-check`: "This consistency checking turned out to be one of the biggest benefits of a typed intermediate language, although it took us a remarkably long time to recognis…"

### L-core-pipeline (other)

After type checking the program is desugared into the explicitly typed Core language and processed by a long sequence of Core-to-Core optimising transformations.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 90] `written:2007-06-09_09-implementations:core-intermediate-language`: "the program is desugared into an explicitly typed intermediate language called simply “Core” and then processed by a long sequence of Core-to-Core analyses and…"

### L-core-systemf (other)

GHC's Core intermediate language was rebased in 1992 on Girard's System F omega plus data types, let and case, apparently the first compiler to use System F as a typed intermediate language.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 104] `written:2007-06-09_09-implementations:core-based-on-system-f`: "we realised in 1992 that a ready-made basis lay to hand, namely Girard’s System F ω ...; all we needed to do was to add data types, let-expressions, and case e…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [09_implementations.md line 108] `written:2007-06-09_09-implementations:underestimating-typed-intermediate-language`: "at the time we thought it was such a simple idea that we did not think it worth publishing ... They understood its significance much better than the GHC team,…"

### L-cost-centres (other)

Sansom and Peyton Jones labelled source with cost centres to aggregate a logical task's costs, raising subtle questions that drove a formal cost semantics.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [10_profiling-and-debugging.md line 56] `written:2007-06-09_10-profiling-and-debugging:cost-centre-assignment-subtle`: "Assigning costs to explicitly labelled cost centres is much more subtle than it sounds."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 47] `written:2007-06-09_10-profiling-and-debugging:cost-centres`: "The new idea Sansom and Peyton Jones introduced was to label the source code with cost centres"

### L-cost-higherorder (other)

Assigning costs to functions works poorly for higher-order functions such as map.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 34] `written:2007-06-09_10-profiling-and-debugging:cost-assignment-for-higher-order-functions`: "The conventional approach, of assigning costs to functions and procedures, works poorly for higher-order functions such as map."

### L-curried-uncurried (language)

Haskell supports both curried and uncurried definitions.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 108] `written:2007-06-09_04-syntax:curried-and-uncurried-both-supported`: "Haskell, like many other languages based on lambda calculus, supports both curried and uncurried definitions:"

### L-currying-history (language)

Following Frege, Schönfinkel and Curry, a two-argument function is a one-argument function returning a function, often more compact.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 99] `written:2007-06-09_04-syntax:currying`: "a function of two arguments may be represented as a function of one argument that itself returns a function of one argument."

### L-debt-to-miranda (other)

Haskell owes a considerable debt to Miranda in general inspiration and specific elements.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 227] `written:2007-06-09_02-the-genesis-of-haskell:debt-to-miranda`: "Haskell owes a considerable debt to Miranda, both for general inspiration and specific language elements that we freely adopted"

### L-defaulting-rule (language)

An ad hoc defaulting rule picks a default type for ambiguous numeric constraints, clumsy but conservative, and relaxed further in GHCi.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [06_haskell-as-a-type-system-laboratory.md line 166] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:defaulting-clumsy-but-conservative`: "This rule is clumsy but conservative: it tries to avoid making an arbitrary choice in all but a few tightly constrained situations."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 159] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-defaulting`: "After much debate, we compromised by adding an ad hoc rule for choosing a particular default type."

### L-design-slow (method)

Language design is a slow process.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 394] `written:2007-06-09_02-the-genesis-of-haskell:language-design-is-slow`: "Language design is a slow process!"

### L-dictionary-passing (language)

Type classes translate into dictionary-passing style by a type-directed transformation, with Gofer using a variant that minimises run-time dictionary construction.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 45] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:dictionary-passing-translation`: "A particularly attractive feature of type classes is that they can be translated into so-called \"dictionary-passing style\" by a typedirected transformation."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [09_implementations.md line 184] `written:2007-06-09_09-implementations:gofer-dictionary-passing-variant`: "an interesting variant of Wadler and Blott’s dictionary-passing translation ... designed to minimise the construction of dictionaries at run time, to work with…"

### L-distribution-maturity (other)

It took more than fifteen years for Haskell to gain enough momentum for distribution and discovery mechanisms to become important.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 17] `written:2007-06-09_09-implementations:distribution-took-fifteen-years`: "it has taken more than fifteen years for Haskell to gain enough momentum that these distribution and discovery mechanisms have become important."

### L-do-notation (language)

Do-notation, not monads themselves, made Haskell programs look conventionally imperative and blurred the line between pure and imperative code.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 371] `written:2007-06-09_07-monads-and-input-output:do-notation-looks-imperative`: "This notation makes (the monadic parts of) Haskell programs appear much more imperative!"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [07_monads-and-input-output.md line 446] `written:2007-06-09_07-monads-and-input-output:do-notation-not-monads-blurred-the-line`: "it was really the advent of do-notation—not monads themselves—that made Haskell programs look more like conventional imperative programs"

### L-dozen-languages (other)

By 1987 more than a dozen non-strict purely functional languages existed, all alike in power and semantics.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [01_introduction.md line 5] `written:2007-06-09_01-introduction:proliferation-of-similar-languages-as-problem`: "there had come into being more than a dozen non-strict, purely functional programming languages, all similar in expressive power and semantic underpinnings"

### L-dsel-definition (language)

A DSEL turns Haskell into a domain-specific embedded language sharing its syntax, types and modules, a term coined by Hudak.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 121] `written:2007-06-09_11-applications:dsel-definition`: "the idea of writing a library that turns Haskell into a domainspecific embedded language (DSEL), a term first coined by Hudak"

### L-dsel-host (language)

Several features make Haskell a friendly host for a DSEL: type classes, higher-order functions, infix syntax, overloaded literals, monads and arrows, and laziness.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 361] `written:2007-06-09_11-applications:six-features-for-dsels`: "No single feature seems dominant, but we may identify the following ways in which Haskell is a particularly friendly host language for a DSEL"

### L-dsel-structure (language)

A DSEL typically defines a data type conceptually a function, with operators combining pieces, executed by decomposing and applying them.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 131] `written:2007-06-09_11-applications:dsel-execution-model`: "The final program is then “executed” by decomposing these larger pieces and applying the embedded functions in a suitable manner."

### L-dsl-nonembedded (language)

A non-embedded DSL can use a conventional parser and interpreter, which Haskell suits too, though it excels at embedded DSLs.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 134] `written:2007-06-09_11-applications:embedded-vs-nonembedded-dsl`: "a non-embedded DSL can be implemented by writing a conventional parser, type checker, and interpreter (or compiler) for the language. Haskell is very well suit…"

### L-dynamic-semantics-overloading (language)

Unlike most statically typed languages, Haskell's dynamic semantics depends on how the type checker resolves type-class overloading, making execution harder to reason about.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 85] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:dynamic-semantics-depends-on-type-checker`: "Not so in Haskell: the dynamic semantics of the program necessarily depends on the way that its type-class overloading is resolved by the type checker."

### L-eager-evaluation (other)

Eager Haskell and optimistic evaluation explored evaluating Haskell eagerly on a uniprocessor while keeping non-strict semantics.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 22] `written:2007-06-09_10-profiling-and-debugging:eager-haskell-non-strict-semantics`: "The idea of evaluating Haskell eagerly rather than lazily (while retaining non-strict semantics), but on a uniprocessor, was also explored by Maessen's Eager H…"

### L-early-impractical (other)

In the early 1980s purely functional languages, though radical and elegant, were impractical: slow, memory-hungry, and lacking input/output.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [13_conclusion.md line 6] `written:2007-06-09_13-conclusion:early-impracticality`: "purely functional languages might have been radical and elegant, but they were also laughably impractical: they were slow, took lots of memory, and had no inpu…"

### L-edison (other)

Edison offers multiple implementations of sequences and collections organised using type classes.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 6] `written:2007-06-09_11-applications:type-classes-organise-data-structures`: "provides multiple implementations of sequences and collections, organised using type classes."

### L-effects-bet (method)

Many of the authors were consciously making a long-term bet that principled control of effects would ultimately prove important, against the mainstream default of effects-by-default.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [13_conclusion.md line 13] `written:2007-06-09_13-conclusion:longterm-bet-on-principled-control-of-effects`: "many of us were consciously making a longterm bet that principled control of effects would ultimately turn out to be important, despite the dominance of effect…"

### L-effects-convergence (method)

A convergence is underway: the functional community has learnt the value of effects and a way to tame them while mainstream languages adopt declarative constructs, driven especially by parallelism, which punishes unrestricted effects cruelly.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [13_conclusion.md line 18] `written:2007-06-09_13-conclusion:convergence-from-both-ends`: "At one end, the purely functional community has learnt both the merit of effects, and at least one way to tame them. At the other end, mainstream languages are…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [13_conclusion.md line 23] `written:2007-06-09_13-conclusion:parallelism-punishes-unrestricted-effects`: "driven especially by the goad of parallelism, which punishes unrestricted effects cruelly."

### L-empty-type (language)

A sum of zero alternatives, an empty type, might have been useful but was not appreciated at the time.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 52] `written:2007-06-09_05-data-types-and-pattern-matching:empty-type-not-appreciated`: "It might have been useful to permit a sum of zero alternatives, which would be a completely empty type, but at the time the value of such a type was not apprec…"

### L-equations-burstall (language)

Writing functional programs as equations with pattern matching traces to Burstall's structural induction and transformation work.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 7] `written:2007-06-09_05-data-types-and-pattern-matching:equations-with-pattern-matching-lineage`: "The style of writing functional programs as a sequence of equations with pattern matching over algebraic types goes back at least to Burstall's work on structu…"

### L-executable-mathematics (language)

Because of referential transparency, Haskell programs can be read as executable mathematics, equations over the category of complete partial orders, so in principle the specification becomes the program.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:referential-transparency-executable-mathematics`: "Because of referential transparency, Haskell programs can be viewed as executable mathematics, as equations over the category of complete partial orders. In pr…"

### L-existential-types (language)

Existential quantification is expressed by letting a data constructor mention type variables in its arguments that do not appear in its result, at almost no new complexity.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 318] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:existential-data-constructors`: "this pattern could be expressed with almost no new language complexity, simply by allowing a data constructor to mention type variables in its arguments that d…"

### L-explicit-braces (language)

Explicit braces and semicolons can override layout, important for programs that generate Haskell.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 70] `written:2007-06-09_04-syntax:override-layout-for-generated-programs`: "we expected people to write programs that generated Haskell programs, and we thought it would be easier to generate explicit separators than layout."

### L-explicit-effects (language)

Being explicit about effects is extremely useful and may be one of Haskell's main impacts on mainstream programming.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 534] `written:2007-06-09_07-monads-and-input-output:being-explicit-about-effects`: "Underlying all these developments is the realisation that being explicit about effects is extremely useful, and this is something that we believe may ultimatel…"

### L-ffi-adhoc (language)

Once the IO monad existed, implementation-specific foreign-call mechanisms appeared quickly, their trouble being that they were tied to one implementation.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [08_haskell-in-middle-age.md line 13] `written:2007-06-09_08-haskell-in-middle-age:early-ad-hoc-ffi-mechanisms`: "Once the IO monad was established, a variety of ad hoc mechanisms rapidly appeared... The difficulty was that these mechanisms tended to be implementation-spec…"

### L-ffi-c (language)

An implementation-independent Foreign Function Interface treats C as a lowest common denominator, since calling C lets you call almost anything else.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [08_haskell-in-middle-age.md line 22] `written:2007-06-09_08-haskell-in-middle-age:ffi-c-as-lowest-common-denominator`: "This so-called Foreign Function Interface (FFI) treats C as a lowest common denominator: once you can call C you can call practically anything else."

### L-ffi-need (language)

A very common application need is to call procedures written in another language from Haskell, and preferably the reverse.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [08_haskell-in-middle-age.md line 11] `written:2007-06-09_08-haskell-in-middle-age:need-to-call-other-languages`: "One feature that very many applications need is the ability to call procedures written in some other language from Haskell, and preferably vice versa."

### L-ffi-process (method)

The FFI process was open to all but depended critically on one person willing to drive it as Editor, differing in kind from the original language development.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [08_haskell-in-middle-age.md line 34] `written:2007-06-09_08-haskell-in-middle-age:ffi-process-different-in-kind`: "it was different in kind to the original development of the Haskell language. The exercise was open to all, but depended critically on the willingness of one p…"

### L-ffi-tools (other)

Pre-processing tools (Green Card, H/Direct, C2Hs) emerged to ease writing the many foreign import declarations a large binding requires.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [08_haskell-in-middle-age.md line 29] `written:2007-06-09_08-haskell-in-middle-age:preprocessing-tools-for-bindings`: "a number of pre-processing tools designed to ease the labour of writing all the foreign import declarations required for a large binding"

### L-first-class-infix (language)

The wish that all values be first class clashed with infix operators not being first class.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 113] `written:2007-06-09_04-syntax:first-class-values-and-infix-ambiguity`: "there was also the feeling that all values in Haskell should be "first class"—especially functions."

### L-fix-leaks (language)

Space leaks can be fixed by shortening object lifetimes, not only by adding strictness; sometimes more laziness wins.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 236] `written:2007-06-09_10-profiling-and-debugging:laziness-also-fixes-leaks`: "making programs stricter is not the only way to fix space leaks in Haskell. Object lifetimes can be shortened by moving their last use earlier—or by creating t…"

### L-flat-namespace (language)

As use grew, the completely flat module name space became irksome, since two libraries could not both use the name Map.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [08_haskell-in-middle-age.md line 61] `written:2007-06-09_08-haskell-in-middle-age:flat-namespace-irksome`: "the fact that the module name space was completely flat became increasingly irksome; for example, if there are two collection libraries, they cannot both use t…"

### L-fp-compilers-productivity (other)

The abstraction and non-interference of functional languages make compilers and translation natural applications with high productivity and little project management.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md line 261] `written:2007-06-09_12-the-impact-of-haskell:abstraction-and-non-interference`: "the abstraction and non-interference properties of functional languages meant that productivity was very high, even with minimal project management overhead"

### L-fran-behaviour (language)

Fran's key idea is a behaviour, a first-class time-varying value, really a function from time to values.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 153] `written:2007-06-09_11-applications:behaviour-as-time-varying-value`: "The key idea in Fran is the notion of a behaviour, a first-class data type that represents a time-varying value."

### L-fran-events (language)

Fran's second idea is a stream of events, with switching combinators connecting continuous behaviours and discrete events for hybrid systems.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 182] `written:2007-06-09_11-applications:events-and-hybrid-systems`: "Various “switching” combinators provide the connection between behaviours and events—i.e. between the continuous and the discrete—thus making Fran-like languag…"

### L-fran-numeric (language)

Haskell's Num and Floating classes let one add two behaviours or take the sine of a behaviour.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 170] `written:2007-06-09_11-applications:num-classes-overload-behaviours`: "Haskell’s Num and Floating classes (for example) allow one to specify how to add two behaviours or take the sine of a behaviour"

### L-functional-dependencies (language)

Functional dependencies declare an explicit dependency between a class's parameters so that fixing some fixes others; informally described yet widely implemented and extremely tricky in detail.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 274] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:functional-dependencies`: "declare an explicit functional dependency between the parameters of a class ... The \"a b -> r\" says that fixing a and b should fix r, resolving the ambiguity."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [06_haskell-as-a-type-system-laboratory.md line 301] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:informal-spec-did-not-stop-use`: "Jones's original paper gave only an informal description of functional dependencies, but (as usual with Haskell) that did not stop them from being implemented…"

### L-gadts (language)

Generalised algebraic data types let a constructor's return type be specified directly, so pattern matching yields type as well as value information.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 418] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:generalised-algebraic-data-types`: "GADTs are a simple but farreaching generalisation of ordinary algebraic data types ... The idea is to allow a data constructor's return type to be specified di…"

### L-generic-programming (language)

A generic function behaves uniformly over any data type with a few type-specific cases, and Haskell hosted many generic-programming experiments.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 461] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:generic-programming`: "A generic function behaves in a uniform way on arguments of any data types, while having a few typespecific cases."

### L-gf-app (other)

Haskell was chosen for GF, particularly for the compilation and partial-evaluation aspects of grammars, using monads and type classes heavily.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 512] `written:2007-06-09_11-applications:haskell-chosen-for-compilation-partial-evaluation`: "Haskell was chosen as a suitable language for this kind of system, particularly for the compilation and partial evaluation aspects (of grammars)."

### L-ghc-complexity (other)

Over fifteen years GHC grew a huge number of features, making it a dauntingly complex beast to understand and modify.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 136] `written:2007-06-09_09-implementations:ghc-grew-complex`: "This makes GHC a dauntingly complex beast to understand and modify"

### L-ghc-extensions-early (other)

GHC's first full release already supported extensions beyond Haskell: monadic I/O, mutable arrays, unboxed data types, and space/time profiling.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 76] `written:2007-06-09_09-implementations:ghc-early-extensions`: "This version of GHC already supported several extensions to Haskell: monadic I/O ..., mutable arrays, unboxed data types ..., and a novel system for space and…"

### L-ghc-frontend-fullsyntax (other)

GHC keeps a large front-end data type reflecting Haskell's full syntax so error messages match what the programmer wrote.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 80] `written:2007-06-09_09-implementations:large-front-end-data-type-for-good-errors`: "GHC uses a very large data type in its front end that accurately reflects the full glory of Haskell’s syntax. ... but has the huge advantage that the error mes…"

### L-ghc-in-haskell (other)

GHC proper, begun autumn 1989, was designed as a complete implementation of Haskell in Haskell, bootstrapped via the prototype, sharing only the parser.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 70] `written:2007-06-09_09-implementations:ghc-complete-implementation-in-haskell`: "It was designed from the ground up as a complete implementation of Haskell in Haskell, bootstrapped via the prototype compiler."

### L-ghc-origin (other)

GHC began in January 1989 at Glasgow; its first version, written in LML by Kevin Hammond, was essentially a new front end to the Chalmers LML compiler.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 56] `written:2007-06-09_09-implementations:ghc-origins-as-lml-front-end`: "The first version of GHC was written in LML by Kevin Hammond, and was essentially a new front end to the Chalmers LML compiler."

### L-gmachine (other)

The G-machine showed lazy functional programs could be compiled to efficient code.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 143] `written:2007-06-09_02-the-genesis-of-haskell:g-machine-laziness-not-interpretation`: "the influential development of the Gmachine, which showed that one could compile lazy functional programs to rather efficient code"

### L-goals-not-met (method)

Several initial goals were not met: the OL basis, embodying only well-tried ideas, and a formal semantics.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 245] `written:2007-06-09_02-the-genesis-of-haskell:goals-not-realised`: "We abandoned the idea of basing Haskell explicitly on OL very early; we violated the goal of embodying only well-tried ideas, notably by the inclusion of type…"

### L-gofer-firsts (language)

Gofer was first to implement several type-class features (constructor classes, do-notation, dictionary-free and multi-parameter classes), some later adopted in Haskell 98.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 191] `written:2007-06-09_09-implementations:gofer-do-notation-and-constructor-classes`: "adding support for constructor classes ... in 1992–93 and producing the first implementation of the do-notation in 1994. Both of these features were subsequent…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [09_implementations.md line 181] `written:2007-06-09_09-implementations:gofer-first-multi-parameter-type-classes`: "Gofer included the first implementation of multi-parameter type classes, as originally suggested by Wadler and Blott"

### L-gofer-small-interpreter (other)

Gofer was a small C interpreter Jones built to learn, fitting on a single floppy.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 174] `written:2007-06-09_09-implementations:gofer-interpreter-small-footprint`: "Gofer was an interpreter, implemented in C, developed on an 8MHz 8086 PC with 640KB of memory, and small enough to fit on a single (360KB) floppy disk."

### L-gofer-to-hugs (other)

Jones rewrote Gofer to track the Haskell standard, renaming it Hugs, whose first release ignored the module system.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 213] `written:2007-06-09_09-implementations:gofer-to-hugs`: "The most prominent missing feature was the Haskell module system; Hugs 1.0 would parse but otherwise ignore module headers and import declarations."

### L-graph-reduction (other)

Lazy languages were implemented by graph reduction, notably Turner's elegant SK combinators.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 62] `written:2007-06-09_02-the-genesis-of-haskell:graph-reduction-and-sk-combinators`: "a variety of techniques based on graph reduction were being explored, and in particular Turner’s inspirationally elegant use of SK combinators"

### L-guards-left (language)

Haskell moved guards to the left of the definition, next to the patterns and suggestive of evaluation order.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 272] `written:2007-06-09_04-syntax:guards-moved-to-left`: "we moved them to the left-hand side of the definition... which had the added benefit of placing the guard right next to the patterns on formal parameters... an…"

### L-gui-bindings-ffi (other)

Pragmatist GUI bindings were hampered by the absence of a well-defined foreign-function interface.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 440] `written:2007-06-09_11-applications:ffi-absence-hampered-bindings`: "These efforts were hampered by the absence of a well defined foreignfunction interface for Haskell, especially as the libraries involved have huge interfaces."

### L-gui-idealists-pragmatists (other)

Haskell GUI work split into idealists seeking a purely declarative interaction and pragmatists binding to existing toolkits, and none of the declarative GUIs became the toolkit of choice.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 3 rows, 3 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [11_applications.md line 389] `written:2007-06-09_11-applications:declarative-gui-radical-question`: "they sought to answer the question, “What is the right way to interact with a GUI in a purely declarative setting?”"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 388] `written:2007-06-09_11-applications:idealists-vs-pragmatists-gui`: "People interested in this area rapidly split into two groups: the idealists and the pragmatists."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [11_applications.md line 429] `written:2007-06-09_11-applications:purity-cost-for-gui`: "Second, the quest for purity always led to programming inconvenience in one form or another."

### L-gui-no-standard (other)

The absence of a single standard Haskell GUI inhibits development, yet no approach has won enough support.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 459] `written:2007-06-09_11-applications:no-standard-gui-inhibits-haskell`: "Lacking such a standard is undoubtedly an inhibiting factor on Haskell’s development. Yet no one approach has garnered enough support to become the design"

### L-haggis-concurrent (language)

Haggis replaced the event loop with lightweight concurrency, and its requirements drove Concurrent Haskell.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 409] `written:2007-06-09_11-applications:haggis-drove-concurrent-haskell`: "The requirements of Haggis directly drove the development of Concurrent Haskell"

### L-hardware-fp (language)

Lazy functional languages suit synchronous hardware: lazy streams model time-varying signals and higher-order functions express circuit structure.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 247] `written:2007-06-09_11-applications:laziness-higher-order-for-hardware`: "first, because lazy streams provide a natural model for discrete time-varying signals, making simulation of functional models very easy; and second, because hi…"

### L-haskell-big-implementations (other)

Haskell is a big language and much work to implement, yet several implementations exist, including new ones once thought unlikely.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 48] `written:2007-06-09_09-implementations:haskell-is-a-big-language-to-implement`: "Haskell is a big language, and it is quite a lot of work to implement. Nevertheless, several implementations are available"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [10_profiling-and-debugging.md line 28] `written:2007-06-09_10-profiling-and-debugging:haskell-dauntingly-large`: "it had begun to seem that Haskell was such a dauntingly large language that no further implementations would emerge."

### L-haskell-overcame-impractical (method)

Haskell helped overcome that impracticality by sticking remorselessly to purity and by building a critical mass of interest and research around a single language.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [13_conclusion.md line 9] `written:2007-06-09_13-conclusion:haskell-contributed-through-purity-and-critical-mass`: "Haskell has contributed to that progress, by sticking remorselessly to the discipline of purity, and by building a critical mass of interest and research effor…"

### L-haskell-pretty (language)

A pleasing consequence of the syntax effort is that Haskell programs look nice.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 18] `written:2007-06-09_04-syntax:haskell-is-a-pretty-language`: "one of the most pleasing consequences of our effort has been comments heard... that "Haskell is a pretty language.""

### L-haskell98-stability (method)

The Haskell 98 Report was a deliberate commitment to stability.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 372] `written:2007-06-09_02-the-genesis-of-haskell:haskell98-commitment-to-stability`: "this was a very significant moment because it represented a commitment to stability."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler restates [12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:haskell98-stability-step`: "the year that Haskell took the step from a frequently changing vehicle for research to a language with a guarantee of long-term stability"

### L-haskore (language)

Haskore expresses music declaratively, combining notes and rests with sequential and parallel combinators, enabled by purity, laziness and higher-order functions.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 328] `written:2007-06-09_11-applications:haskore-declarative-music-model`: "Haskore is a computer music library written in Haskell that allows expressing high-level musical concepts in a purely declarative way"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [11_applications.md line 351] `written:2007-06-09_11-applications:purity-laziness-ho-enable-elegant-music`: "Haskell’s purity, lazy evaluation, and higher-order functions are the key features that make possible this elegant design."

### L-hat-project (other)

Hat generalised a trace to support several kinds of debugging as a source-to-source tool, but has not become a regular part of programming.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [10_profiling-and-debugging.md line 306] `written:2007-06-09_10-profiling-and-debugging:hat-not-mainstream`: "This is probably because Haskell, as it is used in practice, has remained a moving target: new extensions appear frequently, and so it is hard for a language-a…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 351] `written:2007-06-09_10-profiling-and-debugging:one-trace-many-debuggers`: "Runciman realised that, with a little generalisation, the same trace could be used to support several different kinds of debugging"

### L-haxml (other)

HaXml offers a flexible single-type combinator library and a more precise but less flexible data-binding approach.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 209] `written:2007-06-09_11-applications:haxml-two-approaches-tradeoff`: "the combinator library is flexible but all XML data has the same type; the data-binding approach captures more precise types but is less flexible."

### L-hbc-doomed (other)

Being written in LML, hbc was more or less doomed to dwindle though it lived as a test bed for years.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 168] `written:2007-06-09_09-implementations:hbc-doomed-by-lml`: "since the compiler was written in LML it was more or less doomed to dwindle."

### L-hbc-origin (other)

Augustsson and Truvé wrote their own Haskell compiler based on LML rather than wait for the Glasgow compiler.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 149] `written:2007-06-09_09-implementations:hbc-written-out-of-impatience`: "we would write our own Haskell compiler based on the LML compiler."

### L-hbc-stumbling (other)

hbc's hard parts were the module system and especially type checking, done before good papers on it existed.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 163] `written:2007-06-09_09-implementations:hbc-type-checking-hard`: "the big stumbling block was the type checking. It was hard to do. This was way before there were any good papers about how it was supposed to be done."

### L-heap-profiler (other)

Runciman and Wakeling built a heap profiler classifying heap contents by allocating function or constructor, enabling dramatic space improvements against space leaks.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 79] `written:2007-06-09_10-profiling-and-debugging:space-leaks-heap-profiling`: "It had been known for some time that lazy programs could sometimes exhibit astonishingly poor space behaviour—so-called space leaks."

### L-helium (other)

The Helium compiler focuses on teaching and high-quality type error messages.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 341] `written:2007-06-09_09-implementations:helium-for-teaching-and-error-messages`: "The Helium compiler, based at Utrecht, is focused especially on teaching, and on giving high-quality type error messages"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:helium-drops-classes-tradeoff`: "Helium lacks classes, which enables it to give clearer error messages, but then it also lacks textbooks and the ability to “tackle the awkward squad.”"

### L-hierarchical-modules (language)

An effort led by Malcolm Wallace specified hierarchical multi-component module names like Data.Map, borrowing largely from Java, swiftly implemented and surviving unchanged.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [08_haskell-in-middle-age.md line 65] `written:2007-06-09_08-haskell-in-middle-age:hierarchical-module-names`: "an extension to Haskell that would allow multi-component hierarchical module names (e.g., Data.Map), using a design largely borrowed from Java."

### L-high-level-succinct (language)

As a very high-level language Haskell lets programmers write succinct but readable code and concentrate on the problem without boilerplate and housekeeping.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:high-level-concentrate-on-problem`: "they can concentrate on the problem at hand without being distracted by all the attendant programming boilerplate and housekeeping"

### L-higher-kind-unification (language)

Treating higher-kinded constructors as uninterpreted functions and disallowing type-level lambda lets ordinary first-order unification suffice, an ad hoc solution with excellent power-to-weight ratio.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 209] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:first-order-unification-suffices`: "by treating higher-kinded type constructors as uninterpreted functions and not allowing lambda at the type level, Jones's paper ... shows that ordinary first-o…"

### L-higher-kinds (language)

Type classes were generalised to higher kinds, giving constructor classes.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 4 rows, 4 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 360] `written:2007-06-09_02-the-genesis-of-haskell:constructor-classes`: "Type classes were generalised to higher kinds—so-called “constructor classes”"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler restates [06_haskell-as-a-type-system-laboratory.md line 178] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:constructor-classes-higher-kinded`: "Mark Jones ... suggested parameterising a class over a type constructor instead of over a type, an idea he called constructor classes ..."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [06_haskell-as-a-type-system-laboratory.md line 213] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:higher-kinded-as-elegant-generalisation`: "In retrospect, higherkinded quantification is a simple, elegant, and useful generalisation of the conventional Hindley-Milner typing discipline ..."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [06_haskell-as-a-type-system-laboratory.md line 201] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:higher-kinds-independent-utility`: "higher-kinded polymorphism has independent utility: it is entirely possible, and occasionally very useful, to declare data types parameterised over higher kind…"

### L-higher-rank-types (language)

Higher-rank types allow abstracting over a polymorphic function; inference needs a few explicit annotations, first implemented in GHC in 2000.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 409] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:higher-rank-types`: "In the absence of any type annotations, higher-rank types make type inference undecidable; but a few explicit type annotations from the programmer ... transfor…"

### L-hood (other)

HOOD is a lightweight debugger where inserted observe calls collect and print values by tag, showing how much of a lazy input was needed.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 317] `written:2007-06-09_10-profiling-and-debugging:hood-observational-debugging`: "A more lightweight idea was pursued by Andy Gill, who developed HOOD, the Haskell Object Observation Debugger"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [10_profiling-and-debugging.md line 346] `written:2007-06-09_10-profiling-and-debugging:hood-observes-functions`: "HOOD can even observe function values, displaying them as a table of observed arguments and results"

### L-house-os (other)

House implemented a whole operating system in Haskell, using a monad for IA32 access including virtual memory and low-level IO.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 468] `written:2007-06-09_11-applications:house-os-monad-for-hardware-access`: "It uses a monad to provide access to the Intel IA32 architecture, including virtual memory management, protected execution of user binaries, and low-level IO o…"

### L-hugs-merged (other)

The parallel Yale and Nottingham Hugs versions were confusing and were merged in Hugs 98, the first to support Haskell 98.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 241] `written:2007-06-09_09-implementations:parallel-hugs-development-and-merge`: "This problem was finally addressed with the release of Hugs 98 in March 1999, which merged the features of the previous Yale and Nottingham releases into a sin…"

### L-hugs-slowed (other)

Hugs development slowed after Hugs 98, benefiting from Haskell 98's stability while still adding features.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 249] `written:2007-06-09_09-implementations:standardisation-stabilised-hugs`: "benefiting in part from the stability provided by the standardisation of Haskell 98."

### L-hugs-typechecker (language)

Jones overhauled the Hugs type checker with experimental support for advanced type-system features.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 232] `written:2007-06-09_09-implementations:hugs-experimental-type-features`: "experimental support for advanced type system features including rank-2 polymorphism, polymorphic recursion, scoped type variables, existentials, and extensibl…"

### L-hunit (other)

HUnit supports traditional unit testing, providing ways to define, structure and run test cases automatically.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 390] `written:2007-06-09_10-profiling-and-debugging:hunit-traditional-testing`: "HUnit supports more traditional unit testing: it does not generate test cases, but rather provides ways to define test cases, structure them into a hierarchy,…"

### L-imperative-fp-name (language)

Peyton Jones and Wadler named the world-passing token implementation of IO "imperative functional programming".

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 399] `written:2007-06-09_07-monads-and-input-output:imperative-functional-programming`: "Peyton Jones and Wadler dubbed the result “imperative functional programming”"

### L-implicit-parameters (language)

Implicit parameters, a further instance of qualified types, make parameter passing happen implicitly like dictionary passing, understood as selective dynamic scoping.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 373] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:implicit-parameters`: "Implicit parameters arrange that this parameter passing happens implicitly, rather like dictionary passing ..."

### L-industrial-haskell (method)

So many extensions have appeared since Haskell 98 that few real programs adhere to the standard, a problem for users, tool builders and teachers that motivates a new Industrial Haskell standard.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:extensions-vs-standard`: "So many extensions have appeared since the latter was defined that few real programs adhere to the standard nowadays."

### L-infix-binds-less (language)

Infix application always binds less tightly than function application, so f x + g y needs no parentheses.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 81] `written:2007-06-09_04-syntax:infix-binds-less-tightly`: "the former always binds less tightly than the latter. Thus f x + g y never needs parentheses, regardless of what infix operator is used."

### L-infix-from-day-one (language)

Wanting expressions to look like mathematics, the committee adopted infix operators from day one.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 74] `written:2007-06-09_04-syntax:infix-operators-like-mathematics`: "The Haskell Committee wanted expressions to look as much like mathematics as possible, and thus from day one we bought into the idea that Haskell would have in…"

### L-influence-csharp (other)

Features of C# were pioneered by Haskell and other functional languages, with LINQ inspired by monad comprehensions.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 471] `written:2007-06-09_02-the-genesis-of-haskell:haskell-features-in-csharp-and-linq`: "many of the features in C# were pioneered by Haskell and other functional languages, notably polymorphic types and LINQ"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [12_the-impact-of-haskell.md line 570] `written:2007-06-09_12-the-impact-of-haskell:comprehensions-and-monad-comprehensions-as-influence`: "The LINQ (Language INtegrated Query) features of C# 3.0 and Visual Basic 9.0 are based on monad comprehensions from Haskell."

### L-io-a-computation (language)

The key idea of monadic I/O is to treat a value of type IO a as a computation that, when performed, may do input and output before delivering a value of type a.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 346] `written:2007-06-09_07-monads-and-input-output:monadic-io-key-idea`: "The key idea is to treat a value of type IO a as a “computation” that, when performed, might perform input and output before delivering a value of type a."

### L-io-exceptions (language)

The IO monad supports exceptions through ioError and catch, letting programs recover from errors and match failures without giving up deterministic pure semantics.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 498] `written:2007-06-09_07-monads-and-input-output:exceptions-recovered-via-io`: "The IO monad provides a way to achieve this goal without giving up the simple, deterministic semantics of purely functional code"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [07_monads-and-input-output.md line 362] `written:2007-06-09_07-monads-and-input-output:io-monad-exceptions`: "The Haskell IO monad also supports exceptions, offering two new primitives:"

### L-io-implementation (language)

Monadically specified I/O can be implemented with continuations or, in GHC, with a world-passing type where a dummy token ensures sequencing under laziness.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 382] `written:2007-06-09_07-monads-and-input-output:io-two-implementations`: "it is also possible to implement the IO monad in a completely different style, without any recourse to a stream of requests and responses."

### L-io-textbooks (other)

Haskell input/output and the awkward squad are poorly covered by textbooks that present only the purely functional aspects.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md line 142] `written:2007-06-09_12-the-impact-of-haskell:io-and-the-awkward-squad`: "Haskell input/output is not well covered by current textbooks"

### L-ioref (language)

From the beginning the IO monad could support mutable locations and arrays via newIORef, readIORef and writeIORef.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 457] `written:2007-06-09_07-monads-and-input-output:mutable-state-in-io`: "From the very beginning it was clear that the IO monad could also support mutable locations and arrays"

### L-isabelle-class-laws (other)

In Isabelle, declaring a type class can carry the laws its operations obey and declaring an instance requires proving the instance satisfies them.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:type-classes-with-laws`: "When a type class is declared one associates with it the laws obeyed by the operations in a class ... and when an instance is declared one must prove that the…"

### L-jhc (other)

jhc uses whole-program analysis for aggressive optimisation, implementing type classes without dictionary-passing.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 344] `written:2007-06-09_09-implementations:jhc-whole-program-no-dictionaries`: "This whole-program approach allows a completely different approach to implementing type classes, without using dictionary-passing."

### L-keywords-low (language)

Keeping the number of reserved keywords low was a priority, avoiding ones useful as variable names.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 188] `written:2007-06-09_04-syntax:few-reserved-keywords`: "Haskell has 21 reserved keywords that cannot be used as names for values or types... keeping it low was a priority of the Haskell Committee."

### L-kinds-classify (language)

Kinds classify types as types classify values; * is type and *->* a type-level function.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 219] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:kinds-classify-types`: "Kinds classify types just as types classify values. The kind * is pronounced ... \"type\", so if m has kind *->*, then m is a type-level function mapping one t…"

### L-lambda-backslash (language)

Anonymous functions use backslash, closest ASCII to lambda, with -> so the period is reserved for composition.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 43] `written:2007-06-09_04-syntax:anonymous-function-backslash`: "the backslash was the closest single ASCII character to the Greek letter λ. However, "->" was used instead of a period in order to reserve the period for funct…"

### L-lambda-calculus-model (other)

Landin and Strachey established the lambda calculus as fundamental for modelling programming languages.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 12] `written:2007-06-09_02-the-genesis-of-haskell:lambda-calculus-for-modelling-languages`: "identified the fundamental importance of the lambda calculus for modelling programming languages"

### L-lambda-precedence-change (language)

The committee changed lambda's precedence in infix contexts late in design to avoid piling up parentheses in continuation-style code.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 425] `written:2007-06-09_07-monads-and-input-output:lambda-precedence-change`: "the Haskell Committee decided quite late in the design process to change the precedence rules for lambda in the context of infix operators"

### L-lava-classes (language)

Clever use of the class system let Lava use signals-of-lists and lists-of-signals almost interchangeably.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 284] `written:2007-06-09_11-applications:class-system-signals-lists`: "Clever use of the class system enables signals-of-lists and lists-of-signals, for example, to be used almost interchangeably, without a profusion of zips and u…"

### L-lava-sharing (language)

Capturing sharing was tricky since two intended-different fragments are indistinguishable under Haskell's semantics; Lava used a circuit monad.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 300] `written:2007-06-09_11-applications:sharing-vs-duplication-problem`: "yet according to Haskell’s intended semantics, these two fragments should be indistinguishable. For a while, Lava used a “circuit monad” to make the difference…"

### L-layout-complex-spec (language)

The layout rule grew complex enough to be formally specified, yet most users adopt a conforming style.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 90] `written:2007-06-09_04-syntax:complex-layout-rule-programmer-expects`: "Influenced by these constraints and a desire to "do what the programmer expects", Haskell evolved a fairly complex layout rule"

### L-layout-rule-design (language)

Haskell exploits the physical layout of the text via the offside rule, in a design more lenient than Miranda's.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 47] `written:2007-06-09_04-syntax:layout-avoids-clutter`: "Exploiting the physical layout of the program text is a simple and elegant way to avoid syntactic clutter."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [04_syntax.md line 61] `written:2007-06-09_04-syntax:layout-rules-simple-and-lenient`: "We ended up with a design that differed from our most immediate inspiration, Miranda, in supporting larger function definitions with less enforced indentation."

### L-laziness-combinators (language)

Laziness makes Haskell natural for combinator libraries, allowing recursive combinators without fuss and unusual control flow.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 108] `written:2007-06-09_11-applications:laziness-enables-combinator-libraries`: "there seem to be two main factors, both concerning laziness. First, one can write recursive combinators without fuss"

### L-laziness-lifetimes (other)

By abstracting from evaluation order laziness also abstracts from object lifetimes, which is why it contributes to space leaks.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 93] `written:2007-06-09_10-profiling-and-debugging:laziness-abstracts-object-lifetimes`: "By abstracting away from evaluation order, lazy evaluation also abstracts away from object lifetimes, and that is why lazy evaluation contributes to space leak…"

### L-laziness-macros (language)

Lazy evaluation gives much of the power of Lisp macros through ordinary function definitions.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 130] `written:2007-06-09_11-applications:laziness-gives-macro-power`: "in Haskell, thanks to lazy evaluation, much (although emphatically not all) of the power of macros is available through ordinary function definitions."

### L-lazy-appeal (other)

Lazy evaluation appealed through its link to call-by-name lambda calculus, infinite data structures, and simple implementation.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 117] `written:2007-06-09_02-the-genesis-of-haskell:laziness-as-a-drug`: "Lazy evaluation—with its direct connection to the pure, call-by-name lambda calculus, the remarkable possibility of representing and manipulating infinite data…"

### L-lazy-enables-stream (language)

Lazy evaluation lets a program generate a request before processing any responses, which makes the stream I/O model work.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 42] `written:2007-06-09_07-monads-and-input-output:lazy-evaluation-enables-streams`: "Lazy evaluation allows a program to generate a request prior to processing any responses."

### L-lazy-three-times (other)

Lazy evaluation was invented independently three times, igniting interest in lazy functional languages.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 35] `written:2007-06-09_02-the-genesis-of-haskell:lazy-evaluation-invented-three-times`: "Lazy evaluation appears to have been invented independently three times."

### L-lazy-unpredictable (other)

Lazy evaluation's operational aspects are not predictable from the source, making conventional profiling and debugging hard.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 3] `written:2007-06-09_10-profiling-and-debugging:lazy-evaluation-hides-operational-aspects`: "One of the disadvantages of lazy evaluation is that operational aspects such as evaluation order, or the contents of a snapshot of memory at any particular tim…"

### L-legacy-influence (method)

Haskell's most important legacy will be its influence on the languages that succeed it, the ideas and techniques it nurtured proving of enduring value even after Haskell itself is forgotten.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:legacy-is-influence-on-successors`: "We believe the most important legacy of Haskell will be how it influences the languages that succeed it."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler restates [13_conclusion.md line 26] `written:2007-06-09_13-conclusion:enduring-value-through-influence`: "when that day comes, the ideas and techniques that it nurtured will prove to have been of enduring value through their influence on languages of the future."

### L-let-and-where (language)

The assumption of one way to do something was abandoned; both let and where are fully supported.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 242] `written:2007-06-09_04-syntax:abandon-just-one-way`: "In the end, we abandoned the underlying assumption, and provided full syntactic support for both styles."

### L-letwhere-lazy-wart (language)

Pattern matching in let and where is always lazy, unlike case and lambda, a wart in the design.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 193] `written:2007-06-09_05-data-types-and-pattern-matching:let-where-always-lazy-wart`: "pattern matching in let and where clauses is always lazy ... (This difference in the semantics of pattern matching between let/where and case/λ can perhaps be…"

### L-libraries-modest-evolution (other)

The standard libraries are modest while real applications need richer ones, driving an informal library evolution mechanism.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 33] `written:2007-06-09_09-implementations:haskell-98-libraries-still-modest`: "The libraries defined as part of Haskell 98 were still fairly modest in scope. ... But real applications need much richer libraries, and an informal library ev…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler restates [11_applications.md line 3] `written:2007-06-09_11-applications:applications-grew-from-libraries`: "Some of the most important applications of Haskell were originally developed as libraries. The Haskell standard includes a modest selection of libraries, but m…"

### L-library-report (language)

Haskell 1.3 added a Library Report, since programs can hardly be portable without standard libraries.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 353] `written:2007-06-09_02-the-genesis-of-haskell:library-report-for-portability`: "A Library Report was added, reflecting the fact that pro-"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [09_implementations.md line 30] `written:2007-06-09_09-implementations:libraries-grew-into-a-separate-report`: "the volume of standard library code had grown to the extent that it was given a separate companion Library Report, alongside the language definition."

### L-lifetime-profiling (other)

Extending the profiler to object lifetimes revealed data not yet needed (lag), never used again (drag), or never used (void).

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 101] `written:2007-06-09_10-profiling-and-debugging:lag-drag-void-profiling`: "The new profiler could show how much of the heap contained data that was not yet needed (lag), would never be used again (drag), or, indeed, was never used at…"

### L-lifted-tuples (language)

Tuples and algebraic data types were made lifted so matching always evaluates, with lazy matching reintroduced via tilde-patterns.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 184] `written:2007-06-09_05-data-types-and-pattern-matching:lifted-decision-and-tilde-patterns`: "we decided to make both tuples and algebraic data types have a lifted semantics, so that pattern matching always induces evaluation. However, in a somewhat une…"

### L-linspire-uniformity (other)

Haskell has versatility comparable to shell and scripting languages but promotes much greater uniformity, though its idioms for systems programming are not quite as compact as Perl's.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md line 335] `written:2007-06-09_12-the-impact-of-haskell:uniformity-vs-perl-compactness`: "Haskell has comparable versatility but promotes much greater uniformity."

### L-listcomp-lazy-popular (language)

List comprehensions are more popular in lazy languages, found in Miranda and Haskell but not SML or Scheme.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 313] `written:2007-06-09_04-syntax:comprehensions-popular-in-lazy-languages`: "list comprehensions seem to be more popular in lazy languages; for example they are found in Miranda and Haskell, but not in SML or Scheme."

### L-listcomp-monads-reverted (language)

Haskell 1.4 generalised list comprehensions to arbitrary monads, reversed in Haskell 98.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 369] `written:2007-06-09_02-the-genesis-of-haskell:list-comprehensions-over-monads-reversed`: "list comprehensions were generalised to arbitrary monads, a decision that was reversed two years later."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [07_monads-and-input-output.md line 337] `written:2007-06-09_07-monads-and-input-output:syntactic-sugar-for-monads`: "Most users preferred the do-notation, and generalising comprehensions to monads meant that errors in ordinary list comprehensions could be difficult for novice…"

### L-listcomp-notation (language)

List comprehensions give convenient notation for maps, filters and Cartesian products, from Darlington, Turner and named by Wadler.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 294] `written:2007-06-09_04-syntax:list-comprehensions`: "List comprehensions provide a very convenient notation for maps, filters, and Cartesian products."

### L-literate-comments (language)

Haskell added literate comments reversing the usual convention, marking code lines with a special mark.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 339] `written:2007-06-09_04-syntax:literate-comments`: "proposed reversing the usual comment convention: lines of code, rather than lines of comment, should be the ones requiring a special mark."

### L-lolita (language)

In LOLITA laziness was essential to handle the explosion of syntactic and semantic ambiguity from a large grammar.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 494] `written:2007-06-09_11-applications:laziness-essential-for-nlp-ambiguity`: "Laziness was essential in handling the explosion of syntactic ambiguity resulting from a large grammar, and it was much used with semantic ambiguity too."

### L-loops-recursion-hard (other)

Simple loop programs can be harder for students to grasp when expressed using recursion.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md line 133] `written:2007-06-09_12-the-impact-of-haskell:recursion-vs-simple-loops`: "Simple loop programs can be harder for students to grasp when ... expressed using recursion."

### L-many-ways-fit (language)

Haskell offers many ways to define functions, simple and fitting together sensibly.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 95] `written:2007-06-09_04-syntax:many-ways-to-define-functions`: "There are lots of ways to define functions in Haskell...but the ways are simple and all fit together in a sensible manner."

### L-matching-semantics (language)

Haskell chose top-to-bottom equation matching over order-independent alternatives like tightest match, sequential equations and uniform patterns.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 86] `written:2007-06-09_05-data-types-and-pattern-matching:matching-tradeoff-equational-reasoning`: "But the other alternatives had a semantics in which the order of equations did not matter, which aids equational reasoning ... In the end, it was thought bette…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [05_data-types-and-pattern-matching.md line 74] `written:2007-06-09_05-data-types-and-pattern-matching:rejected-matching-alternatives`: "after considering at length and rejecting some other possibilities: • Tightest match ... • Sequential equations ... • Uniform patterns"

### L-math-look-teaching (other)

Haskell's mathematical look and feel makes it a medium for teaching discrete mathematics and logic.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md line 39] `written:2007-06-09_12-the-impact-of-haskell:mathematical-look-and-feel`: "exploiting Haskell’s mathematical look and feel"

### L-minimal-surfaces (language)

Haskell's language, libraries and culture lead to solutions that feel like minimal surfaces: simple expressions comprising significant complexity, with natural forms recurring problem after problem.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:minimal-surfaces`: "solutions that feel like minimal surfaces: simple expressions that comprise significant complexity, with forms that seem natural, recurring in problem after pr…"

### L-minimalist-records (language)

Haskell 1.3 adopted Mark Jones's minimalist record syntax as sugar over algebraic data types, leaving the field open for richer proposals.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [05_data-types-and-pattern-matching.md line 222] `written:2007-06-09_05-data-types-and-pattern-matching:minimal-records-leave-field-open`: "This minimal design has left the field open for more sophisticated proposals, of which the best documented is TRex ... New record proposals continue to appear…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 216] `written:2007-06-09_05-data-types-and-pattern-matching:minimalist-record-syntax`: "the committee eventually adopted a minimalist design originally suggested by Mark Jones: record syntax in Haskell 1.3 ... is simply syntactic sugar for equival…"

### L-miranda-identified-bottom (language)

Miranda identified bottom with (bottom, bottom), making currying an exact isomorphism, which influenced the committee.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 166] `written:2007-06-09_05-data-types-and-pattern-matching:miranda-currying-isomorphism`: "Miranda's design identified ⊥ with (⊥, ⊥), which influenced us considerably. Furthermore, this identification made currying an exact isomorphism"

### L-miranda-mature (other)

Miranda was the most mature lazy language, the natural starting-point candidate.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 209] `written:2007-06-09_02-the-genesis-of-haskell:miranda-most-mature-candidate`: "David Turner’s Miranda was by far the most mature. It was pure, well designed, fulfilled many of our goals"

### L-miranda-typing (other)

Miranda added strong polymorphic typing and type inference, proven in ML, to the untyped SASL and KRC.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 139] `written:2007-06-09_02-the-genesis-of-haskell:miranda-polymorphic-typing`: "Miranda added strong polymorphic typing and type inference, ideas that had proven very successful in ML."

### L-module-interfaces (language)

Early Haskell required module interfaces as well as implementations, surfacing issues of duplication and tension; interfaces were abandoned in Haskell 1.4, leaving the language regrettably without a formally checked interface language.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 3 rows, 3 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [08_haskell-in-middle-age.md line 56] `written:2007-06-09_08-haskell-in-middle-age:interfaces-abandoned`: "In the end, Haskell 1.4 completely abandoned interfaces as a formal part of the language; instead interface files were regarded as a possible artifact of separ…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [08_haskell-in-middle-age.md line 57] `written:2007-06-09_08-haskell-in-middle-age:regret-no-checked-interface-language`: "As a result, Haskell sadly lacks a formally checked language in which a programmer can advertise the interface that the module supports."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [08_haskell-in-middle-age.md line 52] `written:2007-06-09_08-haskell-in-middle-age:tensions-in-interfaces`: "issues such as the duplication of information between interfaces and implementations... whether one can deduce from an interface which module ultimately define…"

### L-module-little-debate (method)

Haskell's module system emerged with surprisingly little debate; the anticipated argument over adopting ML's module system never happened, perhaps for lack of an advocate or tacit agreement it was a bridge too far with type classes.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [08_haskell-in-middle-age.md line 38] `written:2007-06-09_08-haskell-in-middle-age:module-system-emerged-without-debate`: "Haskell’s module system emerged with surprisingly little debate."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [08_haskell-in-middle-age.md line 42] `written:2007-06-09_08-haskell-in-middle-age:why-no-ml-module-debate`: "Perhaps no member of the committee was sufficiently familiar with ML’s module system to advocate it, or perhaps there was a tacit agreement that the combinatio…"

### L-module-namespace-only (language)

They converged on a simple design where the module system is only a namespace-control mechanism, specified separately from the type system.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [08_haskell-in-middle-age.md line 45] `written:2007-06-09_08-haskell-in-middle-age:module-system-as-namespace-control`: "the module system is a namespace control mechanism, nothing more and nothing less. This had the great merit of simplicity and clarity—for example, the module s…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [09_implementations.md line 22] `written:2007-06-09_09-implementations:module-system-of-modesty`: "a module system distinguished by its modesty. It does about as little as it is possible for a language to do and still call itself a practical programming tool…"

### L-module-not-distribution (language)

Modules are a unit of program construction but not of distribution; developers want to ship a group of modules as a package, which the language did not address.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 5] `written:2007-06-09_09-implementations:modules-are-not-a-unit-of-distribution`: "Modules form a reasonable unit of program construction, but not of distribution. Developers want to distribute a related group of modules as a “package,” ... N…"

### L-moggi-monads (other)

Moggi used monads from category theory to modularise denotational semantics, systematising features such as state and exceptions.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 136] `written:2007-06-09_07-monads-and-input-output:moggi-monads-for-semantics`: "Moggi used monads to modularise the structure of a denotational semantics, systematising the treatment of diverse features such as state and exceptions."

### L-monad-as-typeclass (language)

A monad is a programming pattern expressible directly in Haskell as a type class, giving practical use for combinators that work for any monad.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 295] `written:2007-06-09_07-monads-and-input-output:monad-as-type-class`: "A monad is a kind of “programming pattern”. It turned out that this pattern can be directly expressed in Haskell, using a type class"

### L-monad-definition (language)

A monad is a type constructor M with return and bind, where M a is a computation returning a value of type a and bind sequences such computations.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 159] `written:2007-06-09_07-monads-and-input-output:monad-definition`: "A monad consists of a type constructor M and a pair of functions, return and >>= (sometimes pronounced “bind”)."

### L-monad-laws (language)

A true monad's return and bind must satisfy three laws of associative composition with identity, which Haskell provides no mechanism to enforce.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 279] `written:2007-06-09_07-monads-and-input-output:monad-laws-unenforced`: "There are three laws that these definitions should satisfy in order to be a true monad ... These laws guarantee that composition of functions with side effects…"

### L-monad-transformers (language)

Monad transformers abstract over combining monads, but monads do not compose modularly, an open research problem.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 331] `written:2007-06-09_07-monads-and-input-output:monad-transformers-dont-compose`: "Despite the utility of monad transformers, monads do not compose in a nice, modular way, a research problem that is still open"

### L-monadic-advantage (language)

The big advantage of monadic I/O is conceptual: thinking in terms of computations is easier than in terms of continuations, and the abstraction hides changeable details.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 413] `written:2007-06-09_07-monads-and-input-output:monad-abstraction-conceptual-advantage`: "the big advantage is conceptual. It is much easier to think abstractly in terms of computations than concretely in terms of the details of failure and success…"

### L-monadic-dominated (language)

The monadic approach dominated earlier I/O models because its types are more compact, informative and polymorphic.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 402] `written:2007-06-09_07-monads-and-input-output:monadic-types-compact-and-polymorphic`: "The monadic approach rapidly dominated earlier models. The types are more compact, and more informative."

### L-monadic-io (language)

Haskell 1.3 introduced monadic I/O with do syntax, dropping the earlier I/O semantics.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 356] `written:2007-06-09_02-the-genesis-of-haskell:monadic-io-and-do`: "Monadic I/O made its first appearance, including “do” syn-"

### L-monads-io-area (language)

Monads and input/output are a distinctive area of the language's evolution.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [01_introduction.md line 36] `written:2007-06-09_01-introduction:monads-and-io`: "monads and input/output (Section 7)"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [07_monads-and-input-output.md line 3] `written:2007-06-09_07-monads-and-input-output:monads-distinctive-but-not-original`: "monads are one of the most distinctive language design features in Haskell. Monads were not in the original Haskell design, because when Haskell was born a “mo…"

### L-monads-side-effects-examples (language)

Many notions of side effect are definable as monads: state transformer, state reader, exception, continuation, list, and parser.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 179] `written:2007-06-09_07-monads-and-input-output:varieties-of-monads`: "Here are a few examples of the notions of side effects that one can define with monads:"

### L-monomorphism-restriction (language)

The monomorphism restriction forces a definition that does not look like a function to be monomorphic in overloaded variables, adopted to avoid silently duplicating computation but judged a wart.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 4 rows, 4 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 113] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:monomorphism-restriction`: "it says that a definition that does not look like a function ... should be monomorphic in any overloaded type variables."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [06_haskell-as-a-type-system-laboratory.md line 121] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:monomorphism-restriction-a-wart`: "The monomorphism restriction is manifestly a wart on the language. It seems to bite every new Haskell programmer ..."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [06_haskell-as-a-type-system-laboratory.md line 110] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:reluctance-on-compiler-dependent-performance`: "we were reluctant to make performance differences as big as this dependent on compiler optimisations."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [06_haskell-as-a-type-system-laboratory.md line 109] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:silent-duplication-of-computation`: "Hughes argued strongly that it was unacceptable to silently duplicate computation in this way. His argument was motivated by a program he had written that ran…"

### L-multiparam-resisted (language)

Type classes can be generalised from a predicate over one type to a relation over several, but the committee resisted multi-parameter classes as an unforced step into ambiguity and kept the single-parameter restriction.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 3 rows, 3 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 240] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:committee-resistant-to-multi-parameter`: "Going beyond that would be an unforced step into the dark, and we were anxious about questions of overlap, confluence, and decidability of type inference."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [06_haskell-as-a-type-system-laboratory.md line 249] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:multi-parameter-ambiguity`: "The trouble with multi-parameter type classes is that it is very easy to write ambiguous types."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [06_haskell-as-a-type-system-laboratory.md line 230] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:multi-parameter-type-classes`: "a single-parameter type class can be viewed as a predicate over types ..., a multi-parameter class can be viewed a relation between types ..."

### L-namespaces (language)

Namespaces were defined orthogonal when needed and overlapping when context sufficed, so one capitalised name can mean several things.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 161] `written:2007-06-09_04-syntax:namespaces-orthogonal-and-overlapping`: "we carefully defined a set of lexemes for each namespace that were orthogonal when they needed to be, and overlapped when context was sufficient to distinguish…"

### L-naming-moment (method)

The moment a language is named is a small but important moment in its evolution.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 268] `written:2007-06-09_02-the-genesis-of-haskell:moment-of-naming`: "a small but important moment in any language’s evolution is the moment it is named"

### L-naturals-unary (language)

A type isomorphic to the naturals allows pattern matching but its unary representation is inefficient.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 230] `written:2007-06-09_05-data-types-and-pattern-matching:nat-type-inefficient-unary`: "This definition has the advantage that one can use pattern matching in definitions, but the disadvantage that the unary representation implied in the definitio…"

### L-need-common-language (method)

The lack of a common language held back functional programming, motivating a single language all the groups could share.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 3 rows, 3 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [01_introduction.md line 8] `written:2007-06-09_01-introduction:lack-of-common-language-hampers-use`: "more widespread use of this class of functional languages was being hampered by the lack of a common language"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [01_introduction.md line 11] `written:2007-06-09_01-introduction:motivation-common-language`: "providing faster communication of new ideas, a stable foundation for real applications development, and a vehicle through which others would be encouraged to u…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler restates [02_the-genesis-of-haskell.md line 180] `written:2007-06-09_02-the-genesis-of-haskell:tower-of-babel-common-language`: "we felt that they were all roughly the same, bar the syntax, and we started to wonder why we didn’t have a single, common language that we could all benefit fr…"

### L-newtype (language)

newtype introduces a type isomorphic to an existing one, an unlifted single-constructor type motivated by abstract data types.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 152] `written:2007-06-09_05-data-types-and-pattern-matching:newtype-motivation-isomorphic-abstract-types`: "The main motivation for introducing this had to do with abstract data types. It was unfortunate that the Haskell definition of Stack given above forced the rep…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [05_data-types-and-pattern-matching.md line 206] `written:2007-06-09_05-data-types-and-pattern-matching:newtype-single-constructor-choice`: "From Haskell 1.0, it was decided that algebraic types with a single constructor should have a lifted semantics. From Haskell 1.3 onwards ... a second way to in…"

### L-nhc-space-motivation (other)

Röjemo built nhc to be space-efficient and bootstrap in much smaller memory than hbc or GHC.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 261] `written:2007-06-09_09-implementations:nhc-space-efficiency-goal`: "His motivation from the start was to have a space-efficient compiler ... that could be bootstrapped in a much smaller memory space than required by systems suc…"

### L-nhc-york-profiling (other)

nhc's development used York heap-profiling tools, bringing Röjemo to York and more space-efficient methods.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 267] `written:2007-06-09_09-implementations:nhc-heap-profiling-link`: "he made use during development of the first-generation heap-profiling tools—which had previously been developed at York and used to reveal space-leaks in hbc"

### L-nk-brackets (language)

With n+k, apparently redundant brackets change meaning: n + 1 = 7 defines +, (n + 1) = 7 defines n.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 264] `written:2007-06-09_05-data-types-and-pattern-matching:n-plus-k-syntactic-ambiguity`: "n + 1 = 7 is a (function) definition of +, while (n + 1) = 7 is a (pattern) definition of n—so apparently redundant brackets change the meaning completely!"

### L-nk-controversy (language)

n+k patterns were controversial and nearly removed, but stayed in the language.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 251] `written:2007-06-09_05-data-types-and-pattern-matching:n-plus-k-controversy`: "Some users considered n+k patterns essential, because they allowed function definition by cases over the natural numbers ... But others worried that the Int ty…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [05_data-types-and-pattern-matching.md line 270] `written:2007-06-09_05-data-types-and-pattern-matching:n-plus-k-horse-trading`: "One of the very few bits of horse-trading in the design of Haskell occurred when Hudak ... tried to convince Wadler to agree to remove n+k patterns. Wadler sai…"

### L-nk-efficiency (language)

n+k patterns give pattern matching's benefits without loss of efficiency, a special case of a view.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 232] `written:2007-06-09_05-data-types-and-pattern-matching:n-plus-k-patterns`: "Haskell provides so-called n+k patterns that provide the benefits of pattern matching without the loss of efficiency. (The n+k pattern feature can be considere…"

### L-nk-wadler-history (language)

n+k patterns were suggested by Wadler, first seen in Gödel's proof, earlier in NPL and Miranda.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 243] `written:2007-06-09_05-data-types-and-pattern-matching:n-plus-k-origin`: "Patterns of the form n+k were suggested for Haskell by Wadler, who first saw them in Gödel's incompleteness proof ... They were earlier incorporated into Darli…"

### L-non-strict-pure (language)

The language to be designed was fixed as non-strict and purely functional.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [01_introduction.md line 16] `written:2007-06-09_01-introduction:nature-non-strict-purely-functional`: "the nature of the language to be designed (non-strict, purely functional)"

### L-non-von-neumann (other)

The hope that laziness would lead to non-von Neumann hardware proved largely a dead end.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 68] `written:2007-06-09_02-the-genesis-of-haskell:non-von-neumann-hardware-dead-end`: "the possibility that all this would lead to a radically different non-von Neumann hardware architectures"

### L-not-from-miranda (method)

Not starting from Miranda forced a new design but allowed more radical approaches such as type classes.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 225] `written:2007-06-09_02-the-genesis-of-haskell:fork-freedom-enabled-type-classes`: "it allowed us the freedom to contemplate more radical approaches to many aspects of the language design. For example, if we had started from Miranda it seems u…"

### L-numeric-classes (language)

The collection of numeric type classes reflects an uneasy compromise between algebraic purity (more classes) and pragmatism (fewer).

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 80] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:numeric-classes-compromise`: "The rather daunting collection of type classes used to categorise the numeric operations reflected a slightly uneasy compromise between algebraic purity ... an…"

### L-numeric-kinds (language)

Haskell's type system was extended in Bluespec with types of numeric kind so the class system can do statically checked arithmetic, giving accurate types to bit vectors.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:types-of-numeric-kind`: "The type system has been extended with types of numeric kind. ... Their purpose is to give accurate types to things like bit vectors (instead of using lists wh…"

### L-observable-sharing (language)

Claessen used unsafePerformIO for observable sharing, which has a tractable theory despite its unsafe implementation.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 315] `written:2007-06-09_11-applications:observable-sharing-unsafe-but-tractable`: "Claessen used unsafePerformIO to implement “observable sharing” ... Despite its unsafe implementation, observable sharing turns out to have a rather tractable…"

### L-ol-default (method)

OL's design was the default to be kept for any topic lacking a clearly better solution.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 256] `written:2007-06-09_02-the-genesis-of-haskell:ol-as-default-solution`: "OL will be the default if no clearly better solution exists."

### L-one-prefix-operator (language)

Haskell has only one prefix operator, negation; the committee wanted none but would not force minus 42.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 54] `written:2007-06-09_04-syntax:one-prefix-operator-negation`: "The Haskell Committee in fact did not want any prefix operators, but we couldn't bring ourselves to force users to write something like minus 42 or ~42 for the…"

### L-open-participation (method)

After the committee ceased, anyone on the mailing list could participate, with Peyton Jones as editor.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 377] `written:2007-06-09_02-the-genesis-of-haskell:open-participation-benign-dictator`: "Decisions were no longer limited to a small committee; now anyone reading the Haskell mailing list could participate."

### L-overloaded-literals (language)

Overloaded numeric literals gave fib the type Num a => a -> a, raising pattern matching's complexity.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 255] `written:2007-06-09_05-data-types-and-pattern-matching:n-plus-k-overloading-complexity`: "it seemed only consistent that fib's type should be fib :: Num a => a -> a ... This gave rise to a substantial increase in the complexity of pattern matching,…"

### L-paper-is-history (other)

The paper is meant as a history rather than a technical description or tutorial.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [01_introduction.md] `written:2007-06-09_01-introduction:history-not-technical-description`: "the paper is supposed to be a history rather than a technical description or a tutorial"

### L-parametricity-debate (method)

Launchbury held parametricity too important to give up while Hughes wanted seq applicable to any type, two virtually incompatible goals.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 190] `written:2007-06-09_10-profiling-and-debugging:launchbury-vs-hughes`: "Launchbury argued forcefully that parametricity was too important to give up, for this very reason."

### L-parametricity-deforestation (language)

Parametricity justifies short-cut deforestation (the foldr/build rule), which needs a rank-2 type for build.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 174] `written:2007-06-09_10-profiling-and-debugging:parametricity-justifies-deforestation`: "parametricity was by this time not just a nice bonus, but the justification for an important compiler optimisation, namely deforestation"

### L-parser-bnf (language)

Parser combinators allow an extraordinarily direct transcription of BNF into executable code.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 54] `written:2007-06-09_11-applications:bnf-to-executable-code`: "doing so allows an extraordinarily direct transcription of BNF into executable code."

### L-parser-history (other)

Parser combinators go back to Burge and were brought to wider attention by Wadler's list-of-successes paper.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 47] `written:2007-06-09_11-applications:parser-combinators-history`: "it was probably Wadler’s paper “How to replace failure by a list of successes” ... that brought it wider attention, although he did not use the word “combinato…"

### L-parser-monad (language)

Wanting a parser to return a value dovetails with the monad, giving a parameterised Parser and do-notation.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 74] `written:2007-06-09_11-applications:parsers-and-monads`: "a requirement that dovetails precisely with Haskell’s notion of a monad (Section 7)."

### L-parser-new-combinators (language)

Programmers can easily build new parser combinators from existing ones.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 71] `written:2007-06-09_11-applications:programmer-makes-new-combinators`: "It is easy for the programmer to make new parser combinators by combining existing ones."

### L-parser-type (language)

A parser can be modelled as a function from a string to a list of depleted input strings, failure being the empty list.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 50] `written:2007-06-09_11-applications:parser-as-function-type`: "type Parser = String -> [String]"

### L-pattern-match-lazy-complex (language)

Pattern matching semantics is more complex in lazy languages, since match order can change termination.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 66] `written:2007-06-09_05-data-types-and-pattern-matching:lazy-pattern-matching-semantics-complex`: "The semantics of pattern matching in lazy languages is more complex than in strict languages, because laziness means that whether one chooses to first match ag…"

### L-pattern-readability (language)

Pattern matching against algebraic data types greatly increases readability.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 34] `written:2007-06-09_05-data-types-and-pattern-matching:pattern-matching-increases-readability`: "The use of pattern matching against algebraic data types greatly increases readability."

### L-ph (other)

pH adopted Haskell's syntax and type system but kept Id's eager, parallel evaluation, I-structures and M-structures.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 20] `written:2007-06-09_10-profiling-and-debugging:ph-eager-haskell-syntax`: "In 1993 Arvind and his colleagues decided to adopt Haskell's syntax and type system, while retaining Id's eager, parallel evaluation order, I-structures, and M…"

### L-polymorphic-recursion (language)

Polymorphic recursion lets a function be used polymorphically in its own definition; hard to infer but easy to check, so allowed only with an explicit signature.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 390] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:polymorphic-recursion`: "So Haskell 98 allows polymorphic recursion when (and only when) the programmer explicitly specifies the type signature of the function."

### L-postmortem-debugging (other)

Post-mortem debugging waits until execution completes so needed values are known, abstracting from evaluation order.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [10_profiling-and-debugging.md line 295] `written:2007-06-09_10-profiling-and-debugging:evaluation-dependence-trees`: "developing efficient methods to build 'evaluation dependence trees' (Nilsson and Sparud, 1997), data structures that provided all the necessary information for…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 291] `written:2007-06-09_10-profiling-and-debugging:post-mortem-debugging`: "This 'post mortem' approach abstracts nicely from evaluation order, and has been used by all Haskell debuggers since."

### L-practical-areas (method)

As Haskell found real use, attention turned to practically important areas the original designers had neglected, still recent and in flux.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [08_haskell-in-middle-age.md line 4] `written:2007-06-09_08-haskell-in-middle-age:areas-neglected-by-original-designers`: "more and more attention has been paid to areas that received short shrift from the original designers of the language. These areas are of enormous practical im…"

### L-pretty-doc (language)

A pretty-printing document is an abstract type conceptually a function from available width to a layout, though it need not be implemented as one.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [11_applications.md line 37] `written:2007-06-09_11-applications:conceptual-vs-implementation-representation`: "While a Doc can be thought of as a function, it may not be implemented as a function; indeed, this trade-off is a theme of Hughes’s paper."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 22] `written:2007-06-09_11-applications:smart-document-as-abstract-type`: "a “smart document” was an abstract type that can be thought of like this: ... type Doc = Int -> String"

### L-profiler-faster (other)

The profiler quickly led to faster Haskell programs, speeding up GHC itself twofold.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 73] `written:2007-06-09_10-profiling-and-debugging:profiler-faster-programs`: "the availability of a profiler led rapidly to faster Haskell programs, in particular speeding up GHC itself by a factor of two."

### L-programming-environment (other)

Until recently, Yale Haskell excepted, implementers paid little attention to the programming environment, though that is beginning to change.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 350] `written:2007-06-09_09-implementations:environments-long-neglected`: "Until recently, with the notable exception of Yale Haskell, little attention has been paid by Haskell implementers to the programming environment."

### L-programming-large (language)

Support for programming in the large (modules, packages, foreign-function interface) is a technical area of Haskell.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [01_introduction.md] `written:2007-06-09_01-introduction:programming-in-the-large`: "support for programming in the large, such as modules and packages, and the foreign-function interface (Section 8)"

### L-prototype-haskell10 (other)

The prototype compiler implemented essentially all of Haskell 1.0 including views, type classes, deriving, the module system, binary I/O, streams and continuations.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 59] `written:2007-06-09_09-implementations:prototype-implemented-all-of-haskell-1-0`: "The prototype compiler implemented essentially all of Haskell 1.0 including views (later removed), type classes, the deriving mechanism, the full module system…"

### L-public-lists (method)

Discomfort with public and private mailing lists moved debate fully public, though the committee still decided.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 330] `written:2007-06-09_02-the-genesis-of-haskell:public-vs-private-governance`: "Members of the committee became increasingly uncomfortable with the “us-and-them” overtones of having both public and private mailing lists"

### L-pure-not-right-way (method)

Purely functional programming is not necessarily the right way to write programs.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [13_conclusion.md line 12] `written:2007-06-09_13-conclusion:purity-not-the-one-right-way`: "Purely functional programming is not necessarily the Right Way to write programs."

### L-pure-principled-attack (method)

Functional programming, particularly in its purely functional form, is a radical and principled attack on the challenge of writing programs that work.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [13_conclusion.md line 3] `written:2007-06-09_13-conclusion:purely-functional-as-principled-attack`: "Functional programming, particularly in its purely functional form, is a radical and principled attack on the challenge of writing programs that work."

### L-purity-io-problem (language)

The committee's firm commitment to a pure language made the design of the I/O system a central problem, fearing a weak solution would make Haskell look like a toy.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 11] `written:2007-06-09_07-monads-and-input-output:purity-drove-io-design`: "The Haskell Committee was resolute in its decision to keep the language pure—meaning no side effects— so the design of the I/O system was an important issue."

### L-qualified-types (language)

Type classes are one instance of Jones's more general framework of qualified types, which also yields polymorphic extensible records with lacks predicates witnessed at run time.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 338] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:extensible-records-trex`: "Mark Jones showed that type classes were an example of a more general framework he called qualified types ... he developed a second instance of the qualified-t…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [06_haskell-as-a-type-system-laboratory.md line 356] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:lacks-predicate-witnessed-at-runtime`: "so each lacks predicate is also witnessed by a runtime argument. The witness for the predicate (r\\l) is the offset in r at which a field labelled l would be i…"

### L-quickcheck (language)

QuickCheck tests programs against specifications written as boolean functions invoked on random data, displaying counter-examples on failure.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [10_profiling-and-debugging.md line 396] `written:2007-06-09_10-profiling-and-debugging:quickcheck-generators`: "QuickCheck supports this via an abstract data type of 'generators,' which conceptually represent sets of values (together with a probability distribution)."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 367] `written:2007-06-09_10-profiling-and-debugging:quickcheck-specifications-as-tests`: "programs can be tested against specifications by formulating specifications as boolean functions that should always return True, and then invoking these functi…"

### L-quickcheck-emulated (other)

QuickCheck's design has been emulated in other languages, finding real bugs.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 441] `written:2007-06-09_10-profiling-and-debugging:quickcheck-emulated-elsewhere`: "This design has been emulated in many other languages."

### L-quickcheck-exemplifies (language)

QuickCheck exemplifies Haskell's features: a DSL of testable properties, the class system, and monadic generators.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 433] `written:2007-06-09_10-profiling-and-debugging:quickcheck-uses-haskell-features`: "QuickCheck is not only a useful tool, but also a good example of applying some of Haskell's unique features."

### L-quickcheck-programmers (other)

QuickCheck succeeded partly because Haskell programmers prefer writing formal specifications to writing test code.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 428] `written:2007-06-09_10-profiling-and-debugging:quickcheck-succeeds-by-audience`: "Perhaps QuickCheck has succeeded in part because of who Haskell programmers are"

### L-quirky-elegance (method)

What first drew many of the authors to the field was the quirky elegance of the purely functional approach.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [13_conclusion.md line 4] `written:2007-06-09_13-conclusion:quirky-elegance-drew-designers`: "It was precisely this quirky elegance that attracted many of us to the field."

### L-random-seed (language)

The Haskell 98 Random library uses the IO monad as a source of seeds.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 479] `written:2007-06-09_07-monads-and-input-output:random-numbers-use-io`: "Random numbers need a seed, and the Haskell 98 Random library uses the IO monad as a source of such seeds."

### L-realworld-impact (method)

Real-world impact was an important goal of the Committee; Haskell is not mainstream but fares well in niches owing to specific language characteristics.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 456] `written:2007-06-09_10-profiling-and-debugging:impact-as-a-goal`: "impact on the real world was an important goal of the Haskell Committee, so it is worthwhile to consider how well we have achieved this goal."

### L-records-omitted (language)

Records with named fields were omitted from early Haskell because there was no obvious right design.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [05_data-types-and-pattern-matching.md line 211] `written:2007-06-09_05-data-types-and-pattern-matching:records-no-right-design`: "The strongest reason seems to have been that there was no obvious 'right' design. There are a huge number of record systems ... All of them have a complicating…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 172] `written:2007-06-09_05-data-types-and-pattern-matching:records-omitted-despite-usefulness`: "One of the most obvious omissions from early versions of Haskell was the absence of records, offering named fields. Given that records are extremely useful in…"

### L-redex-trails (other)

Redex trails let programmers step backwards through execution.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 340] `written:2007-06-09_10-profiling-and-debugging:redex-trails`: "redex trails, another form of program trace which supports stepping backwards through the execution"

### L-report-book-online (method)

Publishing the Report as a book while keeping it free online defused a debate about freedom and intellectual property.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 388] `written:2007-06-09_02-the-genesis-of-haskell:free-online-text-defuses-ip-debate`: "the entire text could still be available online and be freely usable in that form by anyone"

### L-retainer-profiling (other)

Retainer profiling explains why data was not garbage-collected by showing which objects point at it.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 104] `written:2007-06-09_10-profiling-and-debugging:retainer-profiling`: "A further extension introduced retainer profiling, which could explain why data was not garbage collected by showing which objects pointed at the data of inter…"

### L-runst (language)

Imperative computations can be securely encapsulated in a pure function via a state monad parameterised by a type s, encapsulated by runST with a rank-2 type and parametricity preventing reference leaks.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 463] `written:2007-06-09_07-monads-and-input-output:runST-encapsulates-imperative`: "An exciting and entirely unexpected development was Launchbury and Peyton Jones’s discovery that imperative computations could be securely encapsulated inside…"

### L-sasl-higher-order (other)

Turner's SASL was a pure higher-order functional language, a sugared lambda calculus with lexical scoping and pattern matching.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 20] `written:2007-06-09_02-the-genesis-of-haskell:sasl-sugared-lambda-with-pattern-matching`: "a pure higher-order functional language with lexically scoped variables"

### L-sasl-os (other)

SASL was used at Burroughs to build an entire operating system, likely the first large-scale pure lazy functional programming.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 57] `written:2007-06-09_02-the-genesis-of-haskell:pure-lazy-fp-in-the-large`: "SASL was even used at Burroughs to develop an entire operating system—almost certainly the first exercise of pure, lazy, functional programming “in the large”."

### L-scheme-cbv (other)

Scheme stayed call-by-value because simulating call-by-name via thunks is easier than the reverse.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 124] `written:2007-06-09_02-the-genesis-of-haskell:simulate-call-by-name-easier`: "reasoning that it seemed to be much easier to simulate call-by-name in a call-by-value language (using lambda-expressions as thunks) than to simulate call-by-v…"

### L-scoped-type-variables (language)

Lexically scoped type variables are required to write signatures for inner functions; their omission from Haskell 98 was in retrospect a mistake since polymorphic recursion and higher-rank types need signatures.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 452] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:lexically-scoped-type-variables`: "some kind of lexically scoped type variables are required, so that \"a\" is bound by prefix and used in the signature for xcons."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [06_haskell-as-a-type-system-laboratory.md line 453] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:omission-of-scoped-type-variables-a-mistake`: "In retrospect, the omission of lexically scoped type variables was a mistake, because polymorphic recursion and (more recently) higher-rank types absolutely re…"

### L-section-negation (language)

Sections introduced an ambiguity around negation, seen as a problem with prefix operators rather than sections.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 140] `written:2007-06-09_04-syntax:minus-42-section-problem`: "what is the meaning of (-42)? The answer is negative 42!"

### L-sections (language)

A section is a partial application of an infix operator, parenthesised into a first-class value.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 121] `written:2007-06-09_04-syntax:sections`: "A section is a partial application of an infix operator to no arguments, the left argument, or the right argument—and by surrounding the result in parentheses,…"

### L-segregate-formats (language)

Explicitly segregating legacy data formats into separate data types prevented the mysterious errors that propagate through shell programs when a format changes.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:separate-data-types-for-legacy-formats`: "Explicitly segregating these formats into separate data types prevented the mysterious errors that always seem to propagate through shell programs when the for…"

### L-seq-controversial (language)

seq was controversial for its effect on semantics, not definable in the lambda calculus and the only way to distinguish a divergent function from bottom.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 164] `written:2007-06-09_10-profiling-and-debugging:seq-breaks-semantics`: "adding seq to Haskell was controversial because of its negative effect on semantic properties."

### L-seq-eval-class (language)

Haskell 1.3 made seq overloaded via a class Eval recording its uses so parametricity restrictions were visible, later removed in Haskell 98.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 193] `written:2007-06-09_10-profiling-and-debugging:eval-class-solution`: "The solution adopted for Haskell 1.3 was to make seq an overloaded function, rather than a polymorphic one"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [10_profiling-and-debugging.md line 218] `written:2007-06-09_10-profiling-and-debugging:eval-class-too-heavyweight`: "each insertion of a seq became a nightmare, requiring repeated compilations to find affected type signatures and manual correction of each one."

### L-seq-for-speed (language)

seq was introduced primarily to improve speed by helping the strictness analyser, not to fix space leaks.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 142] `written:2007-06-09_10-profiling-and-debugging:seq-introduced-for-speed`: "interestingly, this was not the main reason for introducing it into Haskell. On the contrary, seq was primarily introduced to improve the speed of Haskell prog…"

### L-seq-introduced (language)

Haskell 1.3 introduced seq and strictness annotations to give the programmer control over evaluation order.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 117] `written:2007-06-09_10-profiling-and-debugging:seq-and-strictness-annotations`: "In 1996, Haskell 1.3 introduced two features that give the programmer better control over evaluation order"

### L-seq-miranda (language)

seq and strict data components were already present in Miranda for the same reasons.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 138] `written:2007-06-09_10-profiling-and-debugging:seq-predates-haskell`: "Both seq and strict components of data structures were already present in Miranda for the same reasons"

### L-seq-parametricity (language)

seq does not satisfy the parametricity property for its type and so weakens the parametricity and free theorems of functions that use it.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 166] `written:2007-06-09_10-profiling-and-debugging:seq-weakens-parametricity`: "seq weakens the parametricity property that polymorphic functions enjoy, because seq does not satisfy the parametricity property for its type ∀a,b.a -> b -> b"

### L-seq-polymorphic-today (language)

seq today is a simple polymorphic function, sacrificing parametricity for agility and leaving GHC's short-cut deforestation unsound.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 227] `written:2007-06-09_10-profiling-and-debugging:seq-now-polymorphic-unsound-deforestation`: "We have sacrificed parametricity in the interests of programming agility and (sometimes dramatic) optimisations. GHC still uses short-cut deforestation, but it…"

### L-seq-space-debugging (language)

Hughes wanted Haskell's seq to support space debugging well.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 162] `written:2007-06-09_10-profiling-and-debugging:hughes-seq-for-space-debugging`: "Hughes was very concerned that Haskell's version of seq should support space debugging well."

### L-shadowing-allowed (language)

Haskell allowed variable shadowing, since outlawing it is inconsistent with alpha renaming.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 184] `written:2007-06-09_04-syntax:shadowing-allowed`: "outlawing shadowing is inconsistent with alpha renaming... So, in the end, Haskell allowed shadowing."

### L-single-constructor-tuple (language)

Whether single-constructor data types share tuple properties raises a semantic discontinuity when a second constructor is added.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 176] `written:2007-06-09_05-data-types-and-pattern-matching:single-constructor-sharing-tuple-properties-difficulty`: "should single constructor data types ... share the same properties as tuples, with a semantic discontinuity induced by adding a second constructor?"

### L-space-sensitivity (language)

Haskell's space use is extremely sensitive to evaluation order, hard to anticipate but fixable by tiny changes with good profiling.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 247] `written:2007-06-09_10-profiling-and-debugging:space-sensitivity-two-edged`: "The extreme sensitivity of Haskell's space use to evaluation order is a two-edged sword."

### L-start-from-existing (method)

The easiest way forward was to begin with an existing language and evolve it.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 204] `written:2007-06-09_02-the-genesis-of-haskell:begin-from-existing-language`: "the easiest way to move forward was to begin with an existing language, and evolve it in whatever direction suited us."

### L-state-monad-plumbing (language)

Lacking reference cells, threading a counter by hand to generate fresh names is tedious and error-prone; a state transformer monad hides the plumbing.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 155] `written:2007-06-09_07-monads-and-input-output:state-monad-hides-plumbing`: "Using a state transformer monad would let you hide all the “plumbing.” The monad itself would be responsible for passing counter values, so there is no chance…"

### L-stm (language)

MVars make programs non-composable, and software transactional memory is a promising approach to that composition problem that fits Haskell particularly well.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 487] `written:2007-06-09_07-monads-and-input-output:stm-fits-haskell`: "Software transactional memory is a recent and apparently very promising new approach to this problem, and one that fits particularly beautifully into Haskell"

### L-stream-cont-equivalent (language)

Stream and continuation I/O turned out to be functionally equivalent, each expressible in terms of the other.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 21] `written:2007-06-09_07-monads-and-input-output:streams-and-continuations-equivalent`: "we realised that in fact they were functionally equivalent—that is, it was possible to completely model stream I/O with continuations, and vice versa."

### L-stream-model (language)

In the stream model a program is a value of type Behaviour mapping responses to requests, needing no special I/O syntax and defined by how the OS interprets it.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 67] `written:2007-06-09_07-monads-and-input-output:no-special-io-syntax`: "With this treatment of I/O there was no need for any specialpurpose I/O syntax or I/O constructs."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [07_monads-and-input-output.md line 39] `written:2007-06-09_07-monads-and-input-output:stream-io-as-behaviour`: "type Behaviour = [Response] -> [Request]"

### L-stream-primitive-efficiency (language)

Defining streams from continuations was inefficient (linear space, quadratic time), so Haskell 1.0 took streams as primitive and defined continuations from them though continuations were easier to use.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 126] `written:2007-06-09_07-monads-and-input-output:streams-primitive-for-efficiency`: "the definition of streams in terms of continuations was inefficient, requiring linear space and quadratic time ... For this reason, Haskell 1.0 defined streams…"

### L-strict-lazy-mix (language)

A main difficulty is constructing software that uses both strict and lazy evaluation well.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:strict-and-lazy-evaluation-difficulty`: "how to construct software that uses both strict and lazy evaluation well"

### L-sum-of-products (language)

Haskell took from Miranda defining algebraic types as a sum of products, unlike Hope and SML which separated sums and products.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 43] `written:2007-06-09_05-data-types-and-pattern-matching:sum-of-products-from-miranda`: "Haskell took from Miranda the notion of defining algebraic types as a 'sum of products'. ... In contrast, Hope and Standard ML separated sums (algebraic types)…"

### L-syntax-effort (method)

The committee worked hard on syntax, which as the user interface is personal and provoked heated debate.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 14] `written:2007-06-09_04-syntax:syntax-as-personal-user-interface`: "We also found that syntax, being the user interface of a language, could become very personal."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler restates [04_syntax.md line 8] `written:2007-06-09_04-syntax:syntax-taken-seriously-despite-dismissal`: "Despite this, the Haskell Committee worked very hard...on designing (and arguing about) the syntax of Haskell."

### L-syntax-io-retrospect (language)

In retrospect the authors ask whether a syntactic device like do-notation could have made stream or continuation I/O look more natural.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 450] `written:2007-06-09_07-monads-and-input-output:retrospective-syntax-for-streams`: "In retrospect it is worth asking whether this same (or similar) syntactic device could have been used to make stream or continuation-based I/O look more natura…"

### L-teaching-effective (other)

Teaching with Haskell drives fundamental concepts like types and recursion home early and lets students tackle more ambitious problems sooner than in a language like Java.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md line 127] `written:2007-06-09_12-the-impact-of-haskell:types-and-recursion-early`: "Fundamental concepts such as types and recursion are ham- mered home early."

### L-teaching-goal (method)

Suitability for teaching was one of the explicit goals the designers set for Haskell.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md line 9] `written:2007-06-09_12-the-impact-of-haskell:teaching-as-explicit-design-goal`: "One of the explicit goals of Haskell’s designers was to create a language suitable for teaching."

### L-template-haskell (language)

GHC supports type-safe meta-programming, inspired by C++ template meta-programming and MetaML's staged type system.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 474] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:template-meta-programming`: "Inspired by the template metaprogramming of C++ and the staged type system of MetaML ..., GHC supports a form of type-safe metaprogramming ..."

### L-tools-research (method)

Developing successful profiling and debugging tools for Haskell took considerable research from the early 1990s.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 12] `written:2007-06-09_10-profiling-and-debugging:profiling-debugging-took-research`: "Developing successful profiling and debugging tools for Haskell has taken considerable research, beginning in the early 1990s."

### L-top-to-bottom-left-right (language)

Matching is top-to-bottom and left-to-right, important in a lazy language since a non-match passes to the next equation.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 70] `written:2007-06-09_05-data-types-and-pattern-matching:top-to-bottom-left-to-right-matching`: "matching is from left to right within each left-hand-side—which is important in a lazy language, since as soon as a non-matching pattern is found, matching pro…"

### L-trace-garbled (other)

Unpredictable evaluation order makes conventional trace printing garble its output.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [10_profiling-and-debugging.md line 262] `written:2007-06-09_10-profiling-and-debugging:trace-garbled-output`: "it is not at all uncommon for the printing of the first argument to trigger another call of trace before the printing is complete, leading to very garbled outp…"

### L-turner-declined (method)

Turner declined to let Miranda be the basis, committed to a single standard while the committee wanted freedom to extend and distribute.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 217] `written:2007-06-09_02-the-genesis-of-haskell:turner-declined-goals-differed`: "we sought the freedom for anyone to extend or modify the language, and to build and distribute an implementation. Turner, by contrast, was strongly committed t…"

### L-turner-lazy-lists (other)

Turner showed the elegance of lazy evaluation and lazy lists emulating many behaviours.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [02_the-genesis-of-haskell.md line 54] `written:2007-06-09_02-the-genesis-of-haskell:lazy-lists-emulate-behaviours`: "Turner showed the elegance of programming with lazy evaluation, and in particular the use of lazy lists to emulate many kinds of behaviours"

### L-two-comment-styles (language)

Haskell had two comment styles, line comments and nestable block comments for commenting out code.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 333] `written:2007-06-09_04-syntax:two-comment-styles`: "The longer form was designed to make it easy to comment out segments of code, including code containing comments."

### L-two-styles (language)

Two styles emerged: declaration style (equations, pattern matching, guards) and expression style (let, lambda, case, if).

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 196] `written:2007-06-09_04-syntax:declaration-vs-expression-style`: "there were two different styles in which functional programs could be written: "declaration style" and "expression style"."

### L-type-class-ambiguity (language)

Type classes brought ambiguity: when nothing fixes an intermediate type and the choice matters, the program is rejected pending a signature.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 129] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:ambiguity-in-type-classes`: "we rapidly discovered a second source of difficulty with type classes, namely ambiguity."

### L-type-class-applications (language)

Once adopted, type classes were immediately applied to equality and ordering, string conversion, enumerations, numeric operations and array indexing.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 77] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-classes-first-applications`: "they were immediately applied to support the following main groups of operations: equality (Eq) and ordering (Ord); converting values to and from strings (Read…"

### L-type-class-basics (language)

A class declaration specifies methods and their types; a type is made an instance via an instance declaration providing an implementation.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 41] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-class-basic-idea`: "A class declaration specifies the methods of the class ... and their types. A type is made into an instance of the class using an instance declaration, which p…"

### L-type-class-chaos (language)

The world of type classes grew chaotically complex, and despite attempts to bring order a unifying simplifying insight is still awaited.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 486] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:attempts-to-bring-order`: "Some notable attempts have been made to bring order to this chaos."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [06_haskell-as-a-type-system-laboratory.md line 500] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:awaiting-unifying-insight`: "we are still awaiting a unifying insight that will not only explain but also simplify the chaotic world of type classes, without throwing the baby out with the…"

### L-type-class-generalisations (language)

Over time type classes were generalised in varied and surprising ways, some summarised in a 1997 paper on the design space.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 7] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-classes-generalised-over-time`: "type classes began to be generalised in a variety of interesting and surprising ways, some of them summarised in a 1997 paper ..."

### L-type-class-origin (language)

Type classes were proposed early by Wadler and Blott as a principled solution to a small problem, overloading for numeric operations and equality.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 4] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-classes-origin-small-problem`: "They were originally proposed early in the design process, by Wadler and Blott ... as a ... principled solution to a relatively small problem (operator overloa…"

### L-type-class-serendipity (language)

Type classes were serendipitous: invented at the right moment, rapidly pervasive, and opening far richer opportunities than their initial purpose.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 89] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-classes-serendipity`: "Type classes were extremely serendipitous: they were invented at exactly the right moment to catch the imagination of the Haskell Committee ..."

### L-type-classes-distinctive (language)

The type system, and type classes in particular, are a distinctive contribution of Haskell.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [01_introduction.md] `written:2007-06-09_01-introduction:type-classes-as-distinctive`: "the type system, and type classes in particular (Section 6)"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler restates [06_haskell-as-a-type-system-laboratory.md line 3] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-classes-as-distinctive-feature`: "Aside from laziness, type classes are undoubtedly Haskell's most distinctive feature."

### L-type-classes-influence (other)

Type classes were picked up elsewhere: Java 5's bounded generic types and Scala's view bounds and implicit parameters are closely related to them.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:type-classes-as-influence`: "The use of bounded types in that system is closely related to type classes in Haskell."

### L-type-lab (method)

Haskell became an unforeseen laboratory for designing, implementing and applying type-system extensions, for technical reasons (purity, qualified types, abandoned full inference) and nontechnical ones (an innovation-friendly committee, experimenting implementations, a geeky user base).

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 3 rows, 3 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 9] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:haskell-as-type-system-laboratory`: "An entirely unforeseen development—perhaps encouraged by type classes—is that Haskell has become a kind of laboratory in which numerous type-system extensions…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [06_haskell-as-a-type-system-laboratory.md line 521] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:why-haskell-friendly-to-innovation-nontechnical`: "The Haskell Committee encouraged innovation right from the beginning and, far from exercising control over the language, disbanded itself in 1999 ..."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [06_haskell-as-a-type-system-laboratory.md line 506] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:why-haskell-friendly-to-innovation-technical`: "The purity of the language removed a significant technical obstacle to many type-system innovations, namely dealing with mutable state."

### L-type-level-programming (language)

Multi-parameter classes with functional dependencies allow arbitrary logic-programming-style computation at the type level, at the risk of non-termination in the type checker.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 294] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:type-level-programming`: "it turned out that one could write arbitrary computations at the type level, in logic-programming style."

### L-type-system-anarchic (method)

Haskell's type system developed anarchically, features used before formalisation, speeding exploration at the cost of complexity.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [06_haskell-as-a-type-system-laboratory.md line 477] `written:2007-06-09_06-haskell-as-a-type-system-laboratory:anarchic-development`: "Haskell's type system has developed extremely anarchically. Many of the new features described above were sketched, implemented, and applied well before they w…"

### L-typeclass-compiler-cost (other)

Type classes made the LML-based compiler bigger and slower, and this experience drove the monomorphism restriction and the removal of views.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 62] `written:2007-06-09_09-implementations:type-classes-cost-size-and-speed`: "the added complexity of type classes meant the compiler was quite a lot bigger and slower than the base LML compiler."

### L-unlifted-indistinguishable (language)

Under unlifted semantics bottom and (bottom, bottom) stay indistinguishable, pattern matching read as binding via fst and snd.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 141] `written:2007-06-09_05-data-types-and-pattern-matching:unlifted-distinguished-only-by-pattern-matching`: "The only way in which they might be distinguished is by pattern matching ... One can instead consider this definition to be equivalent to ... in which case f ⊥…"

### L-unlifted-seq (language)

Unlifted tuples are incompatible with seq, which would require parallel evaluation.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 181] `written:2007-06-09_05-data-types-and-pattern-matching:unlifted-tuples-incompatible-with-seq`: "the unlifted form of tuples is essentially incompatible with seq ... because parallel evaluation would be required to implement seq on unlifted tuples."

### L-unsafeperformio (language)

Unlike runST there is no safe escape from the IO monad, yet all implementations provide unsafePerformIO, whose use is a promise that repetition and ordering do not matter.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 503] `written:2007-06-09_07-monads-and-input-output:unsafePerformIO-no-safe-escape`: "unlike runST, which safely encapsulates an imperative computation, there is no safe way to escape from the IO monad."

### L-user-infix-operators (language)

Infix operators are user-definable, including precedence and associativity.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 77] `written:2007-06-09_04-syntax:user-definable-infix-operators`: "It was also important to us that infix operators be definable by the user, including declarations of precedence and associativity."

### L-views-excluded (language)

Views were in the original design, were removed, and have not been readmitted.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 3 rows, 3 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler restates [05_data-types-and-pattern-matching.md line 288] `written:2007-06-09_05-data-types-and-pattern-matching:views-never-returned`: "a detailed proposal to include views in Haskell 1.3 was put forward by Burton and others ... But views never made it back into the language nor appeared among…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 284] `written:2007-06-09_05-data-types-and-pattern-matching:views-removed`: "The original design of Haskell included views, and was based on the notion that the constructors and views exported by a module should be indistinguishable. Th…"
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [05_data-types-and-pattern-matching.md line 296] `written:2007-06-09_05-data-types-and-pattern-matching:views-tried-and-true-criterion`: "they are unlikely to be included as they do not satisfy the criterion of being 'tried and true'."

### L-views-tension (language)

Wadler suggested views to ease the tension between pattern matching and data abstraction, via an isomorphism.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [05_data-types-and-pattern-matching.md line 277] `written:2007-06-09_05-data-types-and-pattern-matching:views-ease-abstraction-tension`: "Wadler had noticed there was a tension between the convenience of pattern matching and the advantages of data abstraction, and suggested views as a programming…"

### L-wadler-monads-programs (other)

Wadler recognised that Moggi's semantic technique could structure ordinary functional programs, using monads to express the features Moggi used them to describe.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 140] `written:2007-06-09_07-monads-and-input-output:wadler-monads-for-programs`: "Wadler recognised that the technique Moggi had used to structure semantics could be fruitfully applied to structure other functional programs"

### L-wadlers-law (method)

Wadler's law: effort was spent more on lower-level syntax, most of all on the syntax of comments.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 322] `written:2007-06-09_04-syntax:wadlers-law-of-effort`: "semantics is discussed half as much as syntax, syntax is discussed half as much as lexical syntax, and lexical syntax is discussed half as much as the syntax o…"

### L-web-invert (language)

A web application is better written as a single program calling a primitive that takes an HTML form and returns the responses.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [11_applications.md line 221] `written:2007-06-09_11-applications:continuations-or-monads-for-web`: "this idea can be supported using concepts available in functional languages, either continuations or monads (the two approaches are quite similar)."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 216] `written:2007-06-09_11-applications:web-app-invert-the-view`: "Arguably, it is better to invert this view, and instead to write a single program containing calls to a primitive that takes an HTML form as argument and retur…"

### L-web-static-types (language)

The web approach works with a static type system guaranteeing the form's returned type matches what the application expects.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 235] `written:2007-06-09_11-applications:static-typing-for-web-forms`: "the same approach works with a static type system that can guarantee that the type of information returned by the form matches the type of information that the…"

### L-where-clause (language)

A where clause attaches to a declaration, scopes over guards and right-hand sides, with lazy bindings.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [04_syntax.md line 279] `written:2007-06-09_04-syntax:where-attached-to-declaration`: "a where clause is attached to a declaration, not an expression, and scopes over the guards as well as the right-hand sides of the declarations."

### L-world-passing-rejected (language)

A world-passing model updating world state as data was rejected for lack of an easy way to ensure single-threaded access, later solved by Clean's uniqueness types.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 2 rows, 2 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [07_monads-and-input-output.md line 29] `written:2007-06-09_07-monads-and-input-output:world-passing-rejected`: "This “world-passing” model was never a serious contender for Haskell, however, because we saw no easy way to ensure “single-threaded” access to the world state."
- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler refines [12_the-impact-of-haskell.md] `written:2007-06-09_12-the-impact-of-haskell:uniqueness-types-as-io-alternative`: "instead of using monads for input-output it uses an approach based on uniqueness (or linear) types"

### L-yale-environment (other)

The Lisp base let Yale focus on the environment, first to support compiled and interpreted code together with an emacs interface.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 312] `written:2007-06-09_09-implementations:yale-haskell-programming-environment`: "Yale Haskell was the first implementation to support both compiled and interpreted code in the same program"

### L-yale-extensions (other)

Yale Haskell supported many language extensions and served as a test bed for new ideas.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 322] `written:2007-06-09_09-implementations:yale-haskell-as-extension-testbed`: "thus served as an excellent test bed for new ideas. These extensions included monads, dynamic types, polymorphic recursion, strictness annotations, inlining pr…"

### L-yale-haskell (other)

Yale Haskell's Common Lisp back end limited it: lazy code ran 3 to 5 times slower because Lisp's imperative nature prevented Haskell-specific optimisations.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 336] `written:2007-06-09_09-implementations:common-lisp-backend-limits`: "there was a factor of 3 to 5 in lazy code that could not be overcome due to the limitations of the Lisp back end."

### L-yale-scheme-backend (other)

Hudak compiled Haskell into Scheme or T and used a Scheme compiler as a back end rather than a stand-alone compiler.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 291] `written:2007-06-09_09-implementations:yale-haskell-via-scheme-techniques`: "rather than port the ideas to a stand-alone Haskell compiler, it seemed easier to compile Haskell into Scheme or T, and then use a Scheme compiler as a back en…"

### L-yale-scratchpad (other)

Yale Haskell offered a scratch pad extending a module with definitions without recompiling it.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 319] `written:2007-06-09_09-implementations:yale-haskell-scratch-pad`: "A scratch pad was a logical extension of a module in which additional function and value definitions could be added, but whose evaluation did not result in rec…"

### L-yale-strictness-compilation (other)

Yale Haskell used strictness analysis and type information to compile the strict part of Haskell into efficient Lisp.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [09_implementations.md line 300] `written:2007-06-09_09-implementations:yale-haskell-strictness-for-performance`: "Yale Haskell used strictness analysis and type information to compile the strict part of Haskell into very efficient Lisp code."

### L-yampa (other)

Yampa, an arrow-based version of FRP, improved both modularity and performance.

first 2007-06-09 00:00 by Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler; 1 rows, 1 witnesses, 1 days, last 2007-06-09

- 2007-06-09 00:00 Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler states [11_applications.md line 192] `written:2007-06-09_11-applications:arrows-improve-frp`: "the development of an arrowbased version of FRP called Yampa in 2002, that improves both the modularity and performance of previous implementations"

## Unplaced rows

