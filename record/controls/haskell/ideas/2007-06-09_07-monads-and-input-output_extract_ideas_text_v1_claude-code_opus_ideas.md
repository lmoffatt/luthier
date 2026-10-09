---
note: 07_monads-and-input-output.md
note_dir: texts
note_sha256: d834bc5e1ca36274008b71d9f5f8192ec9c3236f199ef4fa2459ee78d660cf98
title: "7. Monads and input/output"
author: Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler
created: 2007-06-09T00:00:00
ideas: 40
quotes_found: 39/40
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Haskell; designers=Paul Hudak, John Hughes, Simon Peyton Jones and Philip Wadler
agent: claude-code
model: opus
effort: low
---

## Ideas

### monads-distinctive-but-not-original
- **What**: Monads are among the most distinctive design features of Haskell, yet were absent from the original design because the concept's relevance to programming was unrecognised at the time.
- **Quote**: "monads are one of the most distinctive language design features in Haskell. Monads were not in the original Haskell design, because when Haskell was born a “monad” was an obscure feature of category theory whose implications for programming were largely unrecognised." (line 3)

### purity-drove-io-design
- **What**: The committee's firm commitment to a pure language, meaning no side effects, made the design of the I/O system a central problem; they feared a weak solution would make Haskell look like a toy.
- **Quote**: "The Haskell Committee was resolute in its decision to keep the language pure—meaning no side effects— so the design of the I/O system was an important issue." (line 11)
- **Also at**: lines 16-18

### streams-and-continuations-equivalent
- **What**: The two leading pure solutions, streams and continuations, turned out to be functionally equivalent, so Haskell 1.0 defined I/O by streams and included an equivalent continuation design.
- **Quote**: "we realised that in fact they were functionally equivalent—that is, it was possible to completely model stream I/O with continuations, and vice versa." (line 21)
- **Also at**: lines 19-20, 23-25

### world-passing-rejected
- **What**: A third model passing and updating world state like any data structure was considered but rejected, because they saw no easy way to ensure single-threaded access to the world state; the Clean designers later solved this with uniqueness types.
- **Quote**: "This “world-passing” model was never a serious contender for Haskell, however, because we saw no easy way to ensure “single-threaded” access to the world state." (line 29)
- **Also at**: lines 31-34

### stream-io-as-behaviour
- **What**: In the stream model a program is a value of type Behaviour mapping responses to requests; the program issues a Request to the OS and the OS reacts with a Response.
- **Quote**: "type Behaviour = [Response] -> [Request]" (line 39)
- **Also at**: lines 40-41

### lazy-evaluation-enables-streams
- **What**: Lazy evaluation lets a program generate a request before processing any responses, which makes the stream model work.
- **Quote**: "Lazy evaluation allows a program to generate a request prior to processing any responses." (line 42)
- **Open**: The reliance on lazy patterns (marked `~`) is needed so a response is not looked at before its request is generated (lines 64-66).

### no-special-io-syntax
- **What**: With stream I/O no special-purpose syntax or constructs were needed; the system was defined entirely by how the OS interpreted a program of the given type, specified abstractly as an OS function with a nondeterministic merge over parallel programs.
- **Quote**: "With this treatment of I/O there was no need for any specialpurpose I/O syntax or I/O constructs." (line 67)
- **Also at**: lines 68-73

### continuation-io-transactions
- **What**: In the continuation model the program is still of type Behaviour, but each request/response pair is captured by a transaction, a function taking failure and success continuations.
- **Quote**: "a collection of transactions were defined that cap- tured the effect of each request/response pair in a continuationpassing style. Transactions were just functions." (line 76)
- **Also at**: lines 79-85

### continuations-preferred-localised-control
- **What**: Though the two styles looked similar, most programmers preferred continuations because control flow was more localised, whereas stream pattern matching forced the reader's focus to jump between responses and requests.
- **Quote**: "the continuation style was preferred by most programmers, since the flow of control was more localised." (line 118)
- **Also at**: lines 119-121

### streams-primitive-for-efficiency
- **What**: Streams can be defined from continuations too, but that definition was inefficient (linear space, quadratic time), so Haskell 1.0 took streams as primitive and defined continuations from them, even though continuations were easier to use.
- **Quote**: "the definition of streams in terms of continuations was inefficient, requiring linear space and quadratic time ... For this reason, Haskell 1.0 defined streams as primitive, and continuations in terms of them, even though continuations were considered easier to use for most purposes." (line 126)
- **Also at**: lines 122-125

### moggi-monads-for-semantics
- **What**: The text reports that Moggi published the use of monads from category theory to modularise denotational semantics, systematising features such as state and exceptions.
- **Quote**: "Moggi used monads to modularise the structure of a denotational semantics, systematising the treatment of diverse features such as state and exceptions." (line 136)
- **Also at**: lines 133-135

### wadler-monads-for-programs
- **What**: The text reports that Wadler recognised Moggi's semantic technique could structure ordinary functional programs, using monads to express the very features Moggi used them to describe.
- **Quote**: "Wadler recognised that the technique Moggi had used to structure semantics could be fruitfully applied to structure other functional programs" (line 140)
- **Also at**: lines 141-142

### state-monad-hides-plumbing
- **What**: Lacking reference cells, Haskell must thread a counter by hand to generate fresh names, which is tedious and error-prone; a state transformer monad hides the plumbing so the names cannot be misspelled.
- **Quote**: "Using a state transformer monad would let you hide all the “plumbing.” The monad itself would be responsible for passing counter values, so there is no chance to misspell the associated names." (line 155)
- **Also at**: lines 144-154

### monad-definition
- **What**: A monad is a type constructor M together with return and >>= (bind); M a is read as a computation returning a value of type a and perhaps performing side effects, and bind sequences such computations.
- **Quote**: "A monad consists of a type constructor M and a pair of functions, return and >>= (sometimes pronounced “bind”)." (line 159)
- **Also at**: lines 162-172

### monads-vs-ml-sequencing
- **What**: Bind is analogous to let in a side-effecting language like ML, but the types record the effect (M a rather than a), and monads give freedom in defining return and >>=, whereas ML fixes one built-in notion of computation and sequencing.
- **Quote**: "monads give quite a bit of freedom in how one defines the operators return and >>=, while ML fixes a single built-in notion of computation and sequencing." (line 176)
- **Also at**: lines 171-175

### varieties-of-monads
- **What**: Many notions of side effect are definable as monads: state transformer, state reader, exception, continuation, list (for nondeterminism), and parser (a combination of state transformer and list).
- **Quote**: "Here are a few examples of the notions of side effects that one can define with monads:" (line 179)
- **Also at**: lines 181-206, 269-277

### monad-laws-unenforced
- **What**: A true monad's return and >>= must satisfy three laws guaranteeing associative composition with an identity, but Haskell provides no mechanism to ensure them, and some programmers use monadic patterns where the laws do not hold.
- **Quote**: "There are three laws that these definitions should satisfy in order to be a true monad ... These laws guarantee that composition of functions with side effects is associative and has an identity" (line 279)
- **Also at**: lines 290-294

### monad-as-type-class
- **What**: A monad is a programming pattern, and that pattern can be expressed directly in Haskell as a type class, giving concrete expression to the mathematical idea that any suitably typed type constructor is a monad, with direct practical use for writing combinators that work for any monad.
- **Quote**: "A monad is a kind of “programming pattern”. It turned out that this pattern can be directly expressed in Haskell, using a type class" (line 295)
- **Also at**: lines 301-305

### monads-typeclasses-symbiosis
- **What**: Intellectual reuse of the monad idea becomes actual code reuse through libraries of monadic functions; the conjunction of monads and type classes made each more attractive.
- **Quote**: "This happy conjunction of monads and type classes gave the two a symbiotic relationship: each made the other much more attractive." (line 315)
- **Also at**: lines 313-314

### monad-transformers-dont-compose
- **What**: Monads are often combined, and abstracting further yields monad transformers; the first modular interpreter in Haskell used them but needed type class extensions only in Gofer, which motivated extensions to type classes. Despite their utility, monads do not compose modularly, an open research problem.
- **Quote**: "Despite the utility of monad transformers, monads do not compose in a nice, modular way, a research problem that is still open" (line 331)
- **Also at**: lines 318-330
- **Open**: How to make monads compose modularly is stated as still open.

### syntactic-sugar-for-monads
- **What**: Two syntactic sugars appeared at different times: Haskell 1.3's do-notation (from Launchbury's work) and Haskell 1.4's monad comprehensions; comprehensions were proposed first, yet users preferred do-notation and generalising comprehensions confused novices, so comprehensions were removed in Haskell 98.
- **Quote**: "Most users preferred the do-notation, and generalising comprehensions to monads meant that errors in ordinary list comprehensions could be difficult for novices to understand, so monad comprehensions were removed in Haskell 98." (line 337)
- **Also at**: lines 334-336

### monadic-io-key-idea
- **What**: The key idea of monadic I/O is to treat a value of type IO a as a computation that, when performed, may do input and output before delivering a value of type a.
- **Quote**: "The key idea is to treat a value of type IO a as a “computation” that, when performed, might perform input and output before delivering a value of type a." (line 346)
- **Also at**: lines 349-351

### io-monad-exceptions
- **What**: The IO monad supports exceptions through ioError, which fails throwing an exception, and catch, which runs a computation and passes any exception to a handler.
- **Quote**: "The Haskell IO monad also supports exceptions, offering two new primitives:" (line 362)
- **Also at**: lines 364-370

### do-notation-looks-imperative
- **What**: Rewriting the example in do-notation makes the monadic parts of Haskell programs appear much more imperative.
- **Quote**: "This notation makes (the monadic parts of) Haskell programs appear much more imperative!" (line 371)

### io-two-implementations
- **What**: Haskell's I/O is specified monadically and can be implemented with continuations (FailCont -> SuccCont a -> Behaviour) or, in GHC, with a world-passing type World -> (a, World), where a dummy token ensures sequencing under lazy evaluation and real side effects are performed.
- **Quote**: "it is also possible to implement the IO monad in a completely different style, without any recourse to a stream of requests and responses." (line 382)
- **Also at**: lines 375-379, 386-399

### imperative-functional-programming
- **What**: The text reports that Peyton Jones and Wadler named the world-passing-with-token implementation of IO "imperative functional programming".
- **Quote**: "Peyton Jones and Wadler dubbed the result “imperative functional programming”" (line 399)

### monadic-types-compact-and-polymorphic
- **What**: The monadic approach dominated earlier models because the types are more compact and informative, uncluttered by passed continuations, showing the result type, and allowing polymorphic IO types that a fixed Request/Response type could not express.
- **Quote**: "The monadic approach rapidly dominated earlier models. The types are more compact, and more informative." (line 402)
- **Also at**: lines 405-412

### monad-abstraction-conceptual-advantage
- **What**: The big advantage of monadic I/O is conceptual: thinking abstractly in terms of computations is easier than thinking in terms of failure and success continuations, and the abstraction makes the underlying details easy to change later.
- **Quote**: "the big advantage is conceptual. It is much easier to think abstractly in terms of computations than concretely in terms of the details of failure and success continuations." (line 413)
- **Also at**: lines 415-417

### lambda-precedence-change
- **What**: To avoid the piling up of parentheses when lambdas nest in the continuation style, the committee changed, late in the design, the precedence rules for lambda in the context of infix operators, letting continuation code look strikingly like the monadic code.
- **Quote**: "the Haskell Committee decided quite late in the design process to change the precedence rules for lambda in the context of infix operators" (line 425)
- **Also at**: lines 420-424, 441-444

### do-notation-not-monads-blurred-the-line
- **What**: It was do-notation, rather than monads themselves, that made Haskell programs look like conventional imperative programs and seriously blurred the line between pure and imperative code, yet the committee heartily adopted it.
- **Quote**: "it was really the advent of do-notation—not monads themselves—that made Haskell programs look more like conventional imperative programs" (line 446)
- **Also at**: lines 448-450

### retrospective-syntax-for-streams
- **What**: In retrospect the authors ask whether the same or a similar syntactic device could have been used to make stream or continuation I/O look more natural.
- **Quote**: "In retrospect it is worth asking whether this same (or similar) syntactic device could have been used to make stream or continuation-based I/O look more natural." (line 450)
- **Open**: Left as an open retrospective question.

### mutable-state-in-io
- **What**: From the beginning it was clear the IO monad could support mutable locations and arrays via newIORef, readIORef and writeIORef.
- **Quote**: "From the very beginning it was clear that the IO monad could also support mutable locations and arrays" (line 457)
- **Also at**: lines 459-462

### runST-encapsulates-imperative
- **What**: An unexpected development was that imperative computations could be securely encapsulated inside a pure function: a state monad parameterised by a type s that infects its references, encapsulated by runST with a rank-2 type, with parametricity ensuring no references leak between encapsulated computations.
- **Quote**: "An exciting and entirely unexpected development was Launchbury and Peyton Jones’s discovery that imperative computations could be securely encapsulated inside a pure function." (line 463)
- **Also at**: lines 464-478

### random-numbers-use-io
- **What**: The Haskell 98 Random library uses the IO monad as a source of seeds, since random numbers need a seed.
- **Quote**: "Random numbers need a seed, and the Haskell 98 Random library uses the IO monad as a source of such seeds." (line 479)

### concurrent-haskell-mvars
- **What**: Concurrent Haskell extends the IO monad with lightweight threads, each able to do I/O, making the semantics nondeterministic by design; threads communicate through synchronised mutable locations called MVars, inspired by the M-structures of Id.
- **Quote**: "Concurrent Haskell ... extends the IO monad with the ability to fork lightweight threads, each of which can perform I/O by itself" (line 481)
- **Also at**: lines 483

### stm-fits-haskell
- **What**: MVars make programs non-composable; software transactional memory is a promising approach to this composition problem that fits particularly well into Haskell.
- **Quote**: "Software transactional memory is a recent and apparently very promising new approach to this problem, and one that fits particularly beautifully into Haskell" (line 487)
- **Also at**: lines 484-486

### exceptions-recovered-via-io
- **What**: Exceptions were in the IO monad from the start, but pure code originally had only error, which halts the whole program; the IO monad lets programs catch and recover from error and pattern-match failures without giving up the deterministic semantics of pure code.
- **Quote**: "The IO monad provides a way to achieve this goal without giving up the simple, deterministic semantics of purely functional code" (line 498)
- **Also at**: lines 491-497

### unsafePerformIO-no-safe-escape
- **What**: Unlike runST there is no safe way to escape the IO monad, yet all implementations provide unsafePerformIO; its use is a programmer's promise that the I/O's repetition and ordering do not matter, and it can even subvert the type system, so it arguably deserves a longer name.
- **Quote**: "unlike runST, which safely encapsulates an imperative computation, there is no safe way to escape from the IO monad." (line 503)
- **Also at**: lines 501-502, 508-524

### arrows-generalise-monads
- **What**: The text reports that arrows, proposed by Hughes, are an abstract view of computation with the same flavour as monads but more general, with applications in GUIs, reactive and polytypic programming; like monads, arrow programming is much easier with syntactic support, handled directly by the type checker.
- **Quote**: "Arrows are an abstract view of computation with the same flavour as monads, but in a more general setting." (line 525)
- **Also at**: lines 526-533

### being-explicit-about-effects
- **What**: Underlying all these developments is the realisation that being explicit about effects is extremely useful, which the authors believe may be one of Haskell's main impacts on mainstream programming; transactional memory is an example, since the crude IO effect system means most memory operations need not be logged, and transposing STM into Haskell revealed two new composition operators (retry and orElse).
- **Quote**: "Underlying all these developments is the realisation that being explicit about effects is extremely useful, and this is something that we believe may ultimately be seen as one of Haskell’s main impacts on mainstream programming" (line 534)
- **Also at**: lines 536-544
