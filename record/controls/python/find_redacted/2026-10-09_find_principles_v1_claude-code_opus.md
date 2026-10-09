# Candidate principles of Python, found blind, 2026-10-09

Written by `scripts/find_principles.py` (find_principles v1). Prompt `find_principles_v1` (sha256 892e58875a4e),
model opus at effort low via claude-code (2.1.197 (Claude Code)); the model saw only the
lineages and the criterion of infectability, with names redacted (Python=L; Guido van Rossum=the designer; Guido=the designer; van Rossum=the designer; ABC=the predecessor).
Inputs by sha256: `record/controls/python/ideas/lineages_link_ideas_v2_claude-code_opus.json` f4564d99c9aa; `record/controls/python/ideas/timeline.jsonl` a50956041718.
Each candidate shows apart what the script took from the rows and what is the model's reading.

Lineages: 156; candidate 17, considered 16, not_principle 123.

## Candidates

```
C1  When no correct value can be computed, raise an exception; never return an undefined value or
    let an error pass silently.
Scope:      language
-- from the rows, by the script
Quote:      "I decided that there should be no undefined result values in Python – instead,
            exceptions should always be raised when no correct return value can be computed."
Said by:    Guido van Rossum, 2009-02-03 10:53
Source:     2009-02-03_early-language-design-and-development.md line 38 (row written:2009-02-03_early-language-design-and-development:no-undefined-values)
Lineages:   L-no-undefined-raise, L-c3-rejects
Witnesses:  first 2009-02-03 by Guido van Rossum; 2 witnesses over 2 days
-- the model's reading (opus, effort low)
Strongest:  ethical. it fixes a stance that a language must never hand back a wrong-looking value;
            it refuses to let a computation run on nonsense
Also:       conceptual. it reframes an error as a first-class outcome to raise rather than a
            sentinel value the caller must guess at
Harms:      forces handling of exceptions throughout the code
Harms:      halts on conditions another language would tolerate
Harms:      runtime cost of the checks that raise
Beats:      L-int-float-silent-error (Because Python has no type declarations, passing an integer
            where a float is expected is not caught and yields an answer with a much larger error,
            hard to debug.). l75 only laments that uncaught type errors slip through; it diagnoses
            the harm but never states the rule
Above next: It states the language's deepest stance on correctness and touches more code than
            first-classness, which is structural but quieter in daily use.

C2  Every object that can be named has equal status: it can be assigned, passed, returned and stored
    like any other.
Scope:      language
-- from the rows, by the script
Quote:      "In Python, all objects that can be named are said to be "first class.""
Said by:    Guido van Rossum, 2009-01-13 09:17
Source:     2009-01-13_introduction-and-overview.md line 26 (row written:2009-01-13_introduction-and-overview:everything-first-class)
Lineages:   L-first-class, L-common-c-struct, L-type-is-object
Witnesses:  first 2009-01-13 by Guido van Rossum; 5 witnesses over 3 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. it collapses the hierarchy between values so one mental model covers
            integers, functions, classes and modules alike
Also:       aesthetic. economy: one rule, equal status, no exceptions to carve out
Harms:      uniform object overhead even for small values like integers
Harms:      no privileged primitives, harder to optimize
Beats:      L-introspection-type-object (Python's introspection comes from making the type structure
            itself available at run time as an object like any other.). l53 applies the same idea to
            one case, the type object, so it infects less than the general rule
Above next: Equal status of all objects reorganizes the whole type model, outranking the syntactic
            discipline of C3 which is a means rather than a worldview.

C3  Prefer the minimal solution that reuses existing mechanisms; do not add new syntax when an
    existing construct will serve.
Scope:      language
-- from the rows, by the script
Quote:      "A major design constraint was that I didn't want to add syntax for methods that differed
            from the syntax for functions. Refactoring the grammar and the byte code generator to
            handle such similar cases differently felt like a huge task."
Said by:    Guido van Rossum, 2009-02-18 11:25
Source:     2009-02-18_adding-support-for-user-defined-classes.md line 24 (row written:2009-02-18_adding-support-for-user-defined-classes:no-separate-method-syntax)
Lineages:   L-class-callable-factory, L-no-separate-method-syntax, L-self-explicit,
            L-special-methods, L-everything-statement, L-metaclass-no-syntax-change,
            L-descriptor-no-syntax
Witnesses:  first 2009-02-18 by Guido van Rossum; 12 witnesses over 4 days
-- the model's reading (opus, effort low)
Strongest:  ethical. a discipline that resists growing the language: solve by reusing what exists
            before inventing syntax
Also:       aesthetic. the grammar stays small; one rule covers many cases
Harms:      overloading one construct for many roles can surprise users
Harms:      cut corners leave semantic gaps fixed only later
Harms:      power hidden behind conventions rather than visible syntax
Beats:      L-classes-afterthought (Adding classes to Python was essentially an afterthought,
            implemented in the 'cut corners' philosophy.). l101 names the same cut-corners instinct
            but as a self-deprecating story about classes, not as a rule to follow
Above next: The refusal to grow syntax guides more concrete decisions than dynamic typing, which is
            one choice made once.

C4  Variables are names that refer to objects, needing no declaration; all type checking happens at
    run time.
Scope:      language
-- from the rows, by the script
Quote:      "In Python, variables are simply names that refer to objects. Variables do not need to be
            declared before they are assigned and they can even change type in the middle of a
            program."
Said by:    Guido van Rossum, 2009-01-13 09:17
Source:     2009-01-13_introduction-and-overview.md line 20 (row written:2009-01-13_introduction-and-overview:dynamic-typing-names-refer-to-objects)
Lineages:   L-dynamic-typing
Witnesses:  first 2009-01-13 by Guido van Rossum; 3 witnesses over 2 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. a variable is not a box holding a typed value but a name bound to an object;
            this rebinds how one thinks about assignment and identity
Also:       aesthetic. no declarations, less ceremony to write
Harms:      type errors surface only at run time
Harms:      no compiler guarantees
Harms:      silent wrong results when the wrong type is passed
Beats:      L-dynamic-no-return (Once dynamic typing is chosen there is no going back, because in
            Python a type cannot be deduced from the form of an operation (x+y is ambiguous), unlike
            ABC's operations.). l42 is a consequence of this choice (no going back once chosen), not
            the choice itself
Above next: Names-refer-to-objects reframes assignment itself, above the repr round-trip which is
            narrower.

C5  Every value, when printed or converted to a string, should read back as a valid expression to
    the parser.
Scope:      language
-- from the rows, by the script
Quote:      "One of the rules I took from ABC was that every data type, when printed or converted to
            a string, should be represented by an expression that was a valid input to the
            language's parser."
Said by:    Guido van Rossum, 2009-02-03 10:53
Source:     2009-02-03_early-language-design-and-development.md line 14 (row written:2009-02-03_early-language-design-and-development:printed-repr-valid-input)
Lineages:   L-repr-valid-input, L-tuple-syntax
Witnesses:  first 2009-02-03 by Guido van Rossum; 2 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  aesthetic. a clean round-trip invariant: what you print, you can read back
Also:       conceptual. it ties the printed form to the grammar, making the language its own
            serialization
Harms:      not every object has a sensible literal form, forcing awkward or fake reprs
Harms:      the round-trip promise is hard to keep for complex objects
Beats:      L-constant-convention (A constant such as an all-caps identifier is only a convention
            the parser neither knows nor enforces, distinct from a literal.). l142 is about what the
            parser does and doesn't know of a convention, a narrower observation than the
            print/parse invariant
Above next: The print/parse invariant is a vivid aesthetic rule, slightly above the more abstract
            call to generalize types.

C6  Generalize related types to a common concept so core operations work the same on all of them.
Scope:      language
-- from the rows, by the script
Quote:      "I decided to generalize these to a common concept, the sequence. This generalization
            made it so certain core operations such as getting the length (len(s)), indexing (s[i]),
            slicing (s[i:j]), and iteration (for i in s) worked the same on any sequence type."
Said by:    Guido van Rossum, 2009-02-03 10:53
Source:     2009-02-03_early-language-design-and-development.md line 16 (row written:2009-02-03_early-language-design-and-development:sequence-generalization)
Lineages:   L-sequence-concept
Witnesses:  first 2009-02-03 by Guido van Rossum; 1 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. it finds the shared structure, the sequence, so one set of operations works
            across list, tuple and string
Also:       aesthetic. economy: length, indexing, slicing and iteration defined once
Harms:      forcing disparate types under one concept can hide meaningful differences
Harms:      the abstraction may leak for types that don't fit
Beats:      L-halfopen-slicing-indexing (Python chose 0-based indexing with half-open slice
            intervals and suitable defaults, so common slicing cases (first n items, next n from i)
            come out as a[:n] and a[i:i+n] without +1/-1 corrections.). l134 is one beautiful
            instance of the slicing design, not the general move to abstract a common concept
Above next: Generalization reorganizes the type system, while hiding implementation details guides
            fewer decisions.

C7  Do not require users to care about uninteresting implementation details.
Scope:      language
-- from the rows, by the script
Quote:      "This is one area where Python violated the ABC-inspired philosophy of not requiring
            users to care about a uninteresting implementation details."
Said by:    Guido van Rossum, 2009-02-03 10:53
Source:     2009-02-03_early-language-design-and-development.md line 28 (row written:2009-02-03_early-language-design-and-development:explicit-long-suffix-violates-philosophy)
Lineages:   L-long-suffix-violation
Witnesses:  first 2009-02-03 by Guido van Rossum; 1 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  ethical. a stance that users should not be burdened with implementation concerns that
            don't interest them
Also:       conceptual. it shifts the boundary of what the programmer must hold in mind
Harms:      hiding details can cost performance the user cannot control
Harms:      users lose a mental model of what the machine does
Beats:      L-concise (Seemingly complicated tasks can often be expressed in very little Python
            code.). l1 celebrates conciseness as a result, but doesn't say which way to decide when
            a detail could leak to the user

```

## Considered and left out

- `L-concise` (Guido van Rossum, 1 rows): Seemingly complicated tasks can often be expressed in very little Python code. *expressive conciseness, a result more than a rule*
- `L-indentation` (Guido van Rossum, 7 rows): Python groups statements by indentation instead of braces, an idea taken from ABC that predates it. *readability by removing grouping noise*
- `L-borrow-fix-abc` (Guido van Rossum, 2 rows): The design program for Python was to keep what he liked from ABC while fixing its perceived problems, designing his own language rather than porting one. *borrow-what-you-like-and-fix method*
- `L-abc-design-method` (Guido van Rossum, 1 rows): ABC was designed by first doing a task analysis and then iterating with serious user testing. *task analysis plus user testing as method*
- `L-dynamic-no-return` (Guido van Rossum, 2 rows): Once dynamic typing is chosen there is no going back, because in Python a type cannot be deduced from the form of an operation (x+y is ambiguous), unlike ABC's operations. *once dynamic typing is chosen, no going back*
- `L-class-body-statements` (Guido van Rossum, 2 rows): Any valid Python statements may appear in a class body, extending from allowing variable assignments to allowing arbitrary executable code. *do not artificially limit what might be useful*
- `L-instance-representation` (Guido van Rossum, 1 rows): An instance is the simplest possible design: a built-in object holding a class reference and an instance dictionary. *the simplest possible design*
- `L-introspection-type-object` (Guido van Rossum, 1 rows): Python's introspection comes from making the type structure itself available at run time as an object like any other. *introspection via the type as an object*
- `L-int-float-silent-error` (Guido van Rossum, 2 rows): Because Python has no type declarations, passing an integer where a float is expected is not caught and yields an answer with a much larger error, hard to debug. *type mismatches should be caught*
- `L-classes-afterthought` (Guido van Rossum, 1 rows): Adding classes to Python was essentially an afterthought, implemented in the 'cut corners' philosophy. *the cut-corners philosophy*
- `L-comprehension-design-factors` (Guido van Rossum, 1 rows): Four factors governed the design of these notations: backwards compatibility, avoiding ambiguity, the desire for equivalence, and evolution of the language. *design factors as a method rubric*
- `L-halfopen-slicing-indexing` (Guido van Rossum, 10 rows): Python chose 0-based indexing with half-open slice intervals and suitable defaults, so common slicing cases (first n items, next n from i) come out as a[:n] and a[i:i+n] without +1/-1 corrections. *the half-open slicing invariant*
- `L-builtins-reassignable` (Guido van Rossum, 5 rows): Built-in names are ordinary identifiers the parser gives no special knowledge, looked up at run time and freely reassignable, so adding a new built-in never invalidates code that used that name. *built-ins reassignable, consistency of evolution*
- `L-constant-convention` (Guido van Rossum, 1 rows): A constant such as an all-caps identifier is only a convention the parser neither knows nor enforces, distinct from a literal. *a constant is only a convention the parser ignores*
- `L-keywords-costly` (Guido van Rossum, 2 rows): Every reserved word must be known by everyone using Python since it can never be a name, so the list is kept small and many proposed features were killed or changed to avoid needing a new keyword. *keep the reserved words small*
- `L-no-feature-in-bugfix` (Guido van Rossum, 1 rows): Adding a new feature in a bugfix release (bool in 2.2.1) was the most criticized such instance and would not be done now. *no new feature in a bugfix release*
