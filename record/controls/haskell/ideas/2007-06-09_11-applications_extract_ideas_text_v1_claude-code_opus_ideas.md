---
note: 11_applications.md
note_dir: texts
note_sha256: 7db780a24c20e62c549067c943c7dc0b42591f16cd0d55727acd944829e69a7f
title: "11. Applications"
author: Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler
created: 2007-06-09T00:00:00
ideas: 44
quotes_found: 43/44
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Haskell; designers=Paul Hudak, John Hughes, Simon Peyton Jones and Philip Wadler
agent: claude-code
model: opus
effort: low
---

## Ideas

### applications-grew-from-libraries
- **What**: Some of Haskell's most important applications began life as libraries; the standard set is modest but many more exist.
- **Quote**: "Some of the most important applications of Haskell were originally developed as libraries. The Haskell standard includes a modest selection of libraries, but many more are available." (line 3)

### type-classes-organise-data-structures
- **What**: The Edison library offers multiple implementations of sequences and collections, organised using type classes.
- **Quote**: "provides multiple implementations of sequences and collections, organised using type classes." (line 6)

### combinator-library-definition
- **What**: The term "combinator library" has no settled definition in the literature; its key idea is a library of functions that combine functions into bigger functions.
- **Quote**: "a combinator library offers functions (the combinators) that combine functions together to make bigger functions." (line 17)
- **Open**: The authors note the term is heavily used yet undefined ("The reader will search in vain for a definition", line 16).

### smart-document-as-abstract-type
- **What**: In Hughes's pretty-printing library a "smart document" is an abstract type conceptually a function from available width to a layout string.
- **Quote**: "a “smart document” was an abstract type that can be thought of like this: ... type Doc = Int -> String" (line 22)

### conceptual-vs-implementation-representation
- **What**: Though a Doc can be thought of as a function, it need not be implemented as one; this trade-off is a theme of Hughes's paper.
- **Quote**: "While a Doc can be thought of as a function, it may not be implemented as a function; indeed, this trade-off is a theme of Hughes’s paper." (line 37)
- **Also at**: lines 177-180 (same point restated for Fran behaviours)

### combinator-library-as-dsl
- **What**: A combinator library can be viewed as a domain-specific language for describing values of a particular type.
- **Quote**: "Another productive way to think of a combinator library is as a domain-specific language (DSL) for describing values of a particular type" (line 38)

### parser-combinators-history
- **What**: Parser combinators, a fertile use of combinator libraries, go back to Burge (1975) and were brought to wider attention by Wadler's "list of successes" paper, though he called it folklore and did not use the word "combinator".
- **Quote**: "it was probably Wadler’s paper “How to replace failure by a list of successes” ... that brought it wider attention, although he did not use the word “combinator” and described the work as “folklore”." (line 47)

### parser-as-function-type
- **What**: A parser can be modelled as a function from a string to a list of depleted input strings, with failure as the empty list.
- **Quote**: "type Parser = String -> [String]" (line 50)
- **Also at**: lines 51-53

### bnf-to-executable-code
- **What**: Parser combinators allow an extraordinarily direct transcription of BNF into executable code.
- **Quote**: "doing so allows an extraordinarily direct transcription of BNF into executable code." (line 54)

### programmer-makes-new-combinators
- **What**: Programmers can easily build new parser combinators by combining existing ones.
- **Quote**: "It is easy for the programmer to make new parser combinators by combining existing ones." (line 71)

### parsers-and-monads
- **What**: Wanting a parser to return a value, not just recognise, dovetails precisely with Haskell's notion of a monad, giving parameterised Parser t and do-notation.
- **Quote**: "a requirement that dovetails precisely with Haskell’s notion of a monad (Section 7)." (line 74)

### combinator-libraries-not-new-but-influential
- **What**: Combinator libraries embody nothing fundamentally new, yet the idea has been extremely influential across widely different areas.
- **Quote**: "combinator libraries do not embody anything fundamentally new. Nevertheless, the idea has been extremely influential" (line 98)

### laziness-enables-combinator-libraries
- **What**: Beyond higher-order functions and data abstraction, two main factors make Haskell a natural fit for combinator libraries, both about laziness: writing recursive combinators without fuss, and unusual control flow.
- **Quote**: "there seem to be two main factors, both concerning laziness. First, one can write recursive combinators without fuss" (line 108)
- **Also at**: lines 116 (second factor: unusual control flow)

### call-by-value-cost-of-eta-expansion
- **What**: In call-by-value languages recursive combinator definitions are generally disallowed, forcing eta-expansion that clutters code and wrecks the abstraction.
- **Quote**: "In call-by-value languages, recursive definitions like this are generally not allowed. Instead, one would have to eta-expand the definition, thereby cluttering the code and (much more importantly) wrecking the abstraction" (line 114)

### dsel-definition
- **What**: A DSEL turns Haskell into a domain-specific embedded language, a term first coined by Hudak; the embedded language is simply an extension of Haskell sharing its syntax, function definition, type system and modules.
- **Quote**: "the idea of writing a library that turns Haskell into a domainspecific embedded language (DSEL), a term first coined by Hudak" (line 121)
- **Also at**: lines 125-128

### laziness-gives-macro-power
- **What**: In Haskell, thanks to lazy evaluation, much (though not all) of the power of Lisp macros is available through ordinary function definitions.
- **Quote**: "in Haskell, thanks to lazy evaluation, much (although emphatically not all) of the power of macros is available through ordinary function definitions." (line 130)

### dsel-execution-model
- **What**: A DSEL typically defines a data type whose nature is conceptually a function, with operators combining these into larger ones, the final program "executed" by decomposing and applying the embedded functions.
- **Quote**: "The final program is then “executed” by decomposing these larger pieces and applying the embedded functions in a suitable manner." (line 131)

### embedded-vs-nonembedded-dsl
- **What**: A non-embedded DSL can instead be implemented with a conventional parser, type checker and interpreter or compiler, an approach Haskell also suits well, but Haskell has been particularly successful at embedded DSLs.
- **Quote**: "a non-embedded DSL can be implemented by writing a conventional parser, type checker, and interpreter (or compiler) for the language. Haskell is very well suited to such approaches as well. However, Haskell has been particularly successful for domain-specific embedded languages." (line 134)

### behaviour-as-time-varying-value
- **What**: The key idea in Fran is a behaviour, a first-class data type representing a time-varying value, really a function from time to values.
- **Quote**: "The key idea in Fran is the notion of a behaviour, a first-class data type that represents a time-varying value." (line 153)
- **Also at**: lines 162-164

### num-classes-overload-behaviours
- **What**: Since many Fran behaviours are numeric, Haskell's Num and Floating classes let one specify how to add behaviours or take their sine.
- **Quote**: "Haskell’s Num and Floating classes (for example) allow one to specify how to add two behaviours or take the sine of a behaviour" (line 170)

### events-and-hybrid-systems
- **What**: Fran's second key idea is an infinite stream of events; switching combinators connect behaviours and events (continuous and discrete), making Fran-like languages suitable for hybrid systems.
- **Quote**: "Various “switching” combinators provide the connection between behaviours and events—i.e. between the continuous and the discrete—thus making Fran-like languages suitable for socalled “hybrid systems.”" (line 182)

### arrows-improve-frp
- **What**: An arrow-based version of FRP called Yampa improved both the modularity and performance of previous implementations.
- **Quote**: "the development of an arrowbased version of FRP called Yampa in 2002, that improves both the modularity and performance of previous implementations" (line 192)

### haxml-two-approaches-tradeoff
- **What**: HaXml gave two XML approaches with complementary strengths: a flexible combinator library where all XML has one type, and a data-binding approach capturing more precise types but less flexible.
- **Quote**: "the combinator library is flexible but all XML data has the same type; the data-binding approach captures more precise types but is less flexible." (line 209)

### web-app-invert-the-view
- **What**: Rather than split a web application into one program per client-server interaction, it is better to invert the view and write a single program calling a primitive that takes an HTML form and returns the responses.
- **Quote**: "Arguably, it is better to invert this view, and instead to write a single program containing calls to a primitive that takes an HTML form as argument and returns the responses as the result" (line 216)

### continuations-or-monads-for-web
- **What**: The inverted web approach needs no new language; it can be supported with continuations or monads (the two quite similar), and arrows arose independently as a generalisation.
- **Quote**: "this idea can be supported using concepts available in functional languages, either continuations or monads (the two approaches are quite similar)." (line 221)
- **Also at**: lines 228 (continuations as a special case of monads or arrows)

### static-typing-for-web-forms
- **What**: Thiemann's work showed the web approach works with a static type system guaranteeing the form's returned type matches what the application expects, and used type classes to ensure HTML/XML satisfies DTD-imposed regular expression types.
- **Quote**: "the same approach works with a static type system that can guarantee that the type of information returned by the form matches the type of information that the application expects." (line 235)

### laziness-higher-order-for-hardware
- **What**: Lazy functional languages suit synchronous hardware for two fundamental reasons: lazy streams model discrete time-varying signals for easy simulation, and higher-order functions express regular circuit structure.
- **Quote**: "first, because lazy streams provide a natural model for discrete time-varying signals, making simulation of functional models very easy; and second, because higher-order functions are ideal for expressing the regular structure of many circuits." (line 247)

### class-system-signals-lists
- **What**: Clever use of Haskell's class system let Lava use signals-of-lists and lists-of-signals almost interchangeably, without a profusion of zips and unzips.
- **Quote**: "Clever use of the class system enables signals-of-lists and lists-of-signals, for example, to be used almost interchangeably, without a profusion of zips and unzips." (line 284)

### sharing-vs-duplication-problem
- **What**: Capturing sharing was tricky because two code fragments the designer intends differently (two gates vs one shared gate) are indistinguishable under Haskell's intended semantics, though their net-lists should differ.
- **Quote**: "yet according to Haskell’s intended semantics, these two fragments should be indistinguishable. For a while, Lava used a “circuit monad” to make the difference observable" (line 300)
- **Open**: The monad solution imposes a heavy cost given its only purpose is to distinguish sharing from duplication (line 311).

### observable-sharing-unsafe-but-tractable
- **What**: Claessen used unsafePerformIO for "observable sharing", keeping the natural syntax while distinguishing sharing from duplication; despite its unsafe implementation it has a tractable theory and extended Haskell's power.
- **Quote**: "Claessen used unsafePerformIO to implement “observable sharing” ... Despite its unsafe implementation, observable sharing turns out to have a rather tractable theory" (line 315)

### haskore-declarative-music-model
- **What**: Haskore expresses high-level musical concepts purely declaratively, combining primitive notes and rests with combinators for sequential and parallel composition into larger musical values.
- **Quote**: "Haskore is a computer music library written in Haskell that allows expressing high-level musical concepts in a purely declarative way" (line 328)

### purity-laziness-ho-enable-elegant-music
- **What**: Haskore rests on a simple declarative model of music with nice algebraic properties, generalizable to other time-varying media; purity, lazy evaluation and higher-order functions are the key features making the design possible.
- **Quote**: "Haskell’s purity, lazy evaluation, and higher-order functions are the key features that make possible this elegant design." (line 351)

### six-features-for-dsels
- **What**: No single feature dominates, but six ways make Haskell a friendly host for a DSEL: type classes (overloading), higher-order functions (glue), infix syntax, over-loaded numeric literals, monads and arrows, and lazy evaluation.
- **Quote**: "No single feature seems dominant, but we may identify the following ways in which Haskell is a particularly friendly host language for a DSEL" (line 361)
- **Also at**: lines 364-377

### combinator-library-and-dsel-same
- **What**: There is little conceptual difference between combinator libraries and DSELs; which term a project uses is probably only historical.
- **Quote**: "It is probably only for historical reasons that one project might use the term “combinator library” and another the term “DSL” (or “DSEL”)." (line 383)

### idealists-vs-pragmatists-gui
- **What**: For GUIs, Haskell people split into idealists seeking the right purely declarative way to interact, and pragmatists wanting to get the job done by binding to an existing toolkit.
- **Quote**: "People interested in this area rapidly split into two groups: the idealists and the pragmatists." (line 388)

### declarative-gui-radical-question
- **What**: The idealists rejected the imperative event-loop model and asked what the right way is to interact with a GUI in a purely declarative setting, yielding unusual systems (Fudgets, Haggis, FranTk, Fruit).
- **Quote**: "they sought to answer the question, “What is the right way to interact with a GUI in a purely declarative setting?”" (line 389)

### haggis-drove-concurrent-haskell
- **What**: Haggis replaced the event loop with lightweight concurrency, and its requirements directly drove the development of Concurrent Haskell.
- **Quote**: "The requirements of Haggis directly drove the development of Concurrent Haskell" (line 409)

### purity-cost-for-gui
- **What**: None of the declarative GUIs became the toolkit of choice; developing a full GUI is huge, and the quest for purity always led to programming inconvenience in some form.
- **Quote**: "Second, the quest for purity always led to programming inconvenience in one form or another." (line 429)
- **Open**: "The search for an elegant, usable, declarative GUI toolkit remains open." (line 431)

### ffi-absence-hampered-bindings
- **What**: Pragmatist bindings were hampered by the absence of a well-defined foreign-function interface, making early bindings compiler-specific and partial; later ones generate the binding automatically into the Haskell 98 FFI.
- **Quote**: "These efforts were hampered by the absence of a well defined foreignfunction interface for Haskell, especially as the libraries involved have huge interfaces." (line 440)

### clean-integrated-io-vs-fragmented-haskell
- **What**: Clean's graphical I/O library was integral from an early stage, letting the user specify the interface by a data structure of call-back functions, contrasted with the fragmented approach Haskell took to GUIs.
- **Quote**: "A notable example is the Clean graphical I/O library, which formed an integral part of the Clean system from a very early stage ... (unlike the fragmented approach to GUIs taken by Haskell)." (line 450)

### no-standard-gui-inhibits-haskell
- **What**: The community periodically agonises over the absence of a single standard Haskell GUI; lacking it is undoubtedly an inhibiting factor on Haskell's development, yet no approach has garnered enough support.
- **Quote**: "Lacking such a standard is undoubtedly an inhibiting factor on Haskell’s development. Yet no one approach has garnered enough support to become the design" (line 459)
- **Open**: The standard GUI question remains unsettled.

### house-os-monad-for-hardware-access
- **What**: House implemented a system (kernel, window system, device drivers) entirely in Haskell, using a monad to provide access to the Intel IA32 architecture including virtual memory and low-level IO.
- **Quote**: "It uses a monad to provide access to the Intel IA32 architecture, including virtual memory management, protected execution of user binaries, and low-level IO operations." (line 468)

### laziness-essential-for-nlp-ambiguity
- **What**: In LOLITA, handling unrestricted text made ambiguity unavoidable and significant; laziness was essential to handle the explosion of syntactic ambiguity from a large grammar, and much used for semantic ambiguity too.
- **Quote**: "Laziness was essential in handling the explosion of syntactic ambiguity resulting from a large grammar, and it was much used with semantic ambiguity too." (line 494)

### haskell-chosen-for-compilation-partial-evaluation
- **What**: Haskell was chosen for GF as suitable particularly for the compilation and partial evaluation aspects of grammars, with monads and type classes extensively used.
- **Quote**: "Haskell was chosen as a suitable language for this kind of system, particularly for the compilation and partial evaluation aspects (of grammars)." (line 512)
