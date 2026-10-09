# Candidate principles of Python, found blind, 2026-10-09

Written by `scripts/find_principles.py` (find_principles v1). Prompt `find_principles_v2` (sha256 5eb0cb1b3e6b),
model opus at effort low via claude-code (2.1.197 (Claude Code)); the model saw only the
lineages and the criterion of infectability, with names redacted (Python=L; Guido van Rossum=the designer; Guido=the designer; van Rossum=the designer; ABC=the predecessor).
Inputs by sha256: `record/controls/python/ideas/lineages_link_ideas_v2_claude-code_opus.json` f4564d99c9aa; `record/controls/python/ideas/timeline.jsonl` a50956041718.
Each candidate shows apart what the script took from the rows and what is the model's reading.

Lineages: 156; candidate 14, considered 23, not_principle 119.

## Candidates

```
C1  Give every nameable thing equal status, assignable, passable and storable, rather than
    privileging some kinds of object.
Instead of: privileged built-ins that can't be passed or stored like ordinary values
Scope:      language
-- from the rows, by the script
Quote:      "In Python, all objects that can be named are said to be "first class.""
Said by:    Guido van Rossum, 2009-01-13 09:17
Source:     2009-01-13_introduction-and-overview.md line 26 (row written:2009-01-13_introduction-and-overview:everything-first-class)
Lineages:   L-first-class
Witnesses:  first 2009-01-13 by Guido van Rossum; 2 witnesses over 2 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. equal status for everything nameable dissolves the hierarchy between kinds
            of thing, so functions, classes and modules become data you manipulate
Also:       ethical. a stance that the language should not privilege the implementor's categories
            over the programmer's
Harms:      erases useful distinctions between values and types
Harms:      invites misuse by making everything assignable and storable
Harms:      uniform object overhead even on simple integers
Beats:      L-general-purpose (Python is a general purpose language in the lineage of Lisp or
            Smalltalk, not merely a scripting language.). general-purpose positioning claims a
            scope, it does not reshape how you think
Above next: It reorganizes the entire object model, where the next only governs when a value may be
            absent.

C2  When no correct value can be computed, raise rather than return an undefined or silently clipped
    result, and reject inconsistent constructions outright.
Instead of: silent sentinels, truncation or undefined behavior as in C
Scope:      language
-- from the rows, by the script
Quote:      "I decided that there should be no undefined result values in Python – instead,
            exceptions should always be raised when no correct return value can be computed."
Said by:    Guido van Rossum, 2009-02-03 10:53
Source:     2009-02-03_early-language-design-and-development.md line 38 (row written:2009-02-03_early-language-design-and-development:no-undefined-values)
Lineages:   L-no-undefined-raise, L-overflow-check, L-c3-rejects
Witnesses:  first 2009-02-03 by Guido van Rossum; 5 witnesses over 2 days
-- the model's reading (opus, effort low)
Strongest:  ethical. it refuses the C habit of silent wrong answers; a wrong computation must
            announce itself
Also:       conceptual. it makes the absence of a correct value a first-class event, an exception,
            rather than a sentinel to be forgotten
Harms:      forces exception handling even on fast paths
Harms:      raising on overflow surprised C-trained users
Harms:      can abort a long computation instead of returning a usable partial
Beats:      L-long-suffix-violation (Requiring a trailing L to mark longs violated the ABC-inspired
            philosophy of not making users care about uninteresting implementation details.).
            sparing users uninteresting details is a comfort rule; demanding that no error pass
            silently is a safety stance with teeth
Above next: Its charge about correctness strikes harder than the aesthetic pleasure of a
            round-tripping representation.

C3  Make a value's printed form a valid expression that reconstructs it, rather than a free-form
    description.
Instead of: arbitrary, unparseable string descriptions of objects
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
Strongest:  aesthetic. a printed value you can paste back as code is an economical, closed loop
            between a value and its text
Also:       conceptual. it ties the printed form to the parser, making representation and
            construction one idea
Harms:      not every object has a sensible constructor expression
Harms:      forces ugly forms like the trailing-comma one-tuple
Harms:      the guarantee breaks for cyclic or huge structures
Beats:      L-list-comprehension (A list comprehension produces a list of a sequence's values
            selected by an optional predicate and mapped by a function, a Pythonic interpretation of
            the mathematical set-builder notation, with multiple for-clauses allowed for nested
            loops.). borrowing set-builder notation is a pretty formulation; the repr rule is a
            general invariant every type must satisfy
Above next: Its elegance is real but narrower than the indexing convention that shapes every loop
            and slice.

C4  Index from zero with half-open intervals and suitable defaults so adjacent slices meet without
    off-by-one corrections.
Instead of: 1-based closed intervals needing +1/-1 adjustments
Scope:      language
-- from the rows, by the script
Quote:      "Using / 0-based indexing, half-open intervals, and suitable defaults (as Python / ended
            up having), they are beautiful: a[:n] and a[i:i+n]"
Said by:    Guido van Rossum, 2013-10-24 08:44
Source:     2013-10-24_why-python-uses-0-based-indexing.md line 15 (row written:2013-10-24_why-python-uses-0-based-indexing:zero-based-half-open-defaults-elegant)
Lineages:   L-halfopen-slicing-indexing
Witnesses:  first 2013-10-24 by Guido van Rossum; 10 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  aesthetic. the adjacency invariant, one slice's end is the next's start, removes +1/-1
            noise and is simply beautiful
Also:       conceptual. it reframes an index as a position between elements rather than on one
Harms:      half-open intervals confuse beginners expecting inclusive ends
Harms:      0-based clashes with domains that count from one
Harms:      off-by-one still bites at the boundaries
Beats:      L-comprehension-vs-mapfilter (List comprehensions are an alternative to map() and
            filter() that wins on realistic cases, and Van Rossum finds them more readable than the
            functional notation as complexity grows, rejecting the view that a terser lambda would
            fix map().). preferring comprehensions to map/filter is a taste; the half-open
            convention is a structural invariant you compute with
Above next: A convention every slice obeys spreads wider than how instance variables are named.

C5  Make the instance an explicit first argument and explicit attribute access the only way to reach
    its state, rather than implicit resolution.
Instead of: implicit this and hidden instance-variable lookup as in C++
Scope:      language
-- from the rows, by the script
Quote:      "With explicit references, there is no need to have a special syntax for method
            definitions nor do you have to worry about complicated semantics concerning variable
            lookup. Instead, one simply defines a function whose first argument corresponds to the
            instance, which by convention is named "self.""
Said by:    Guido van Rossum, 2009-02-18 11:25
Source:     2009-02-18_adding-support-for-user-defined-classes.md line 54 (row written:2009-02-18_adding-support-for-user-defined-classes:explicit-self-removes-special-cases)
Lineages:   L-self-explicit
Witnesses:  first 2009-02-18 by Guido van Rossum; 3 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  ethical. it insists the instance be named in the open rather than smuggled in by hidden
            scope rules
Also:       aesthetic. a method becomes just a function whose first argument is the object, needing
            no special method syntax
Harms:      every method pays the visual cost of writing self
Harms:      forgetting self produces confusing errors
Harms:      explicitness reads verbose next to an implicit this
Beats:      L-reject-instancevar-declarations (Explicit instance-variable declarations were rejected
            (he had gotten this far with none), and lexical markers like a sigil did not appeal to
            him.). rejecting instance-variable declarations is the negative of the same choice;
            naming self states the rule positively
Above next: Explicitness reorganizes how one writes methods, where the sequence concept, next,
            unifies how one reads collections.

C6  Generalize related types under a shared concept so the same core operations work uniformly
    across them, rather than per-type operations.
Instead of: separate, incompatible operations for each container type
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
Strongest:  conceptual. one concept, the sequence, lets length, indexing, slicing and iteration mean
            the same across unrelated types
Also:       aesthetic. a single set of operations replaces many type-specific ones
Harms:      one interface onto lists, tuples and strings hides their differences
Harms:      a string behaving as a sequence of characters surprises
Harms:      uniformity tempts operations that don't fit a given type
Beats:      L-everything-statement (Every part of the language is an executable statement that can
            appear anywhere, which simplified the grammar (earlier it restricted declarative
            constructs to the top level).). making every construct an executable statement unifies
            the grammar; the sequence unifies the things the programmer actually handles daily
Above next: A unifying abstraction over data edges out the method-level discipline of avoiding new
            syntax.

C7  Prefer the minimal solution that reuses existing syntax over introducing new syntax for a new
    feature.
Instead of: adding dedicated grammar for each new capability
Scope:      method
-- from the rows, by the script
Quote:      "A major design constraint was that I didn't want to add syntax for methods that differed
            from the syntax for functions. Refactoring the grammar and the byte code generator to
            handle such similar cases differently felt like a huge task."
Said by:    Guido van Rossum, 2009-02-18 11:25
Source:     2009-02-18_adding-support-for-user-defined-classes.md line 24 (row written:2009-02-18_adding-support-for-user-defined-classes:no-separate-method-syntax)
Lineages:   L-class-callable-factory, L-no-separate-method-syntax, L-special-methods,
            L-metaclass-no-syntax-change, L-descriptor-no-syntax
Witnesses:  first 2009-02-18 by Guido van Rossum; 6 witnesses over 3 days
-- the model's reading (opus, effort low)
Strongest:  aesthetic. solving a new need by reusing what exists, with no new grammar, keeps the
            language small
Also:       ethical. the cost of a new construct falls on everyone, so it must be earned before
            being added
Harms:      reusing existing syntax yields awkward forms like dunder names
Harms:      overloading one construct can hide intent from readers
Harms:      avoiding syntax sometimes defers a cleaner solution for years
Beats:      L-class-body-statements (Any valid Python statements may appear in a class body,
            extending from allowing variable assignments to allowing arbitrary executable code.).
            allowing any statement in a class body is one instance of keeping syntax simple; the
            no-new-syntax rule is the general discipline behind many such choices

```

## Considered and left out

- `L-concise` (Guido van Rossum, 1 rows): Seemingly complicated tasks can often be expressed in very little Python code. *expressiveness: much in little code*
- `L-dynamic-typing` (Guido van Rossum, 3 rows): Python is dynamically typed: variables are names referring to objects, need no declaration, and all type checking happens at run time. *dynamic typing / corner-cutting philosophy*
- `L-for-iterable` (Guido van Rossum, 1 rows): Python's for statement loops over any iterable object rather than over a numeric index. *iterate over objects, not indices*
- `L-general-purpose` (Guido van Rossum, 1 rows): Python is a general purpose language in the lineage of Lisp or Smalltalk, not merely a scripting language. *positioned as general purpose*
- `L-borrow-fix-abc` (Guido van Rossum, 2 rows): The design program for Python was to keep what he liked from ABC while fixing its perceived problems, designing his own language rather than porting one. *method: borrow what you like, fix problems*
- `L-abc-design-method` (Guido van Rossum, 1 rows): ABC was designed by first doing a task analysis and then iterating with serious user testing. *method: task analysis then user testing*
- `L-long-suffix-violation` (Guido van Rossum, 1 rows): Requiring a trailing L to mark longs violated the ABC-inspired philosophy of not making users care about uninteresting implementation details. *don't make users care about uninteresting details*
- `L-class-body-statements` (Guido van Rossum, 2 rows): Any valid Python statements may appear in a class body, extending from allowing variable assignments to allowing arbitrary executable code. *keep syntax simple, don't artificially limit*
- `L-introspection-type-object` (Guido van Rossum, 1 rows): Python's introspection comes from making the type structure itself available at run time as an object like any other. *introspection via type as object*
- `L-permissive-vs-smalltalk` (Guido van Rossum, 1 rows): Python's objects are more permissive than Smalltalk's, which restricts an object's attributes to those fixed at creation. *permissiveness over Smalltalk's restriction*
- `L-reject-instancevar-declarations` (Guido van Rossum, 1 rows): Explicit instance-variable declarations were rejected (he had gotten this far with none), and lexical markers like a sigil did not appeal to him. *no instance-variable declarations*
- `L-everything-statement` (Guido van Rossum, 3 rows): Every part of the language is an executable statement that can appear anywhere, which simplified the grammar (earlier it restricted declarative constructs to the top level). *every construct a statement, uniform grammar*
- `L-result-type-rule` (Guido van Rossum, 1 rows): The major mistake was borrowing C's rule that an arithmetic operation's result is always the same type as its operands, which makes sense in C but not in a very-high-level language. *don't borrow low-level rules into a high-level language*
- `L-not-functional` (Guido van Rossum, 2 rows): Van Rossum never viewed Python as a functional language or heavily influenced by them, and its dynamic nature rules out functional-style compile-time optimization such as tail recursion. *embrace the dynamic nature, and that's fine*
- `L-classes-afterthought` (Guido van Rossum, 1 rows): Adding classes to Python was essentially an afterthought, implemented in the 'cut corners' philosophy. *cut-corners philosophy*
- `L-comprehension-design-factors` (Guido van Rossum, 1 rows): Four factors governed the design of these notations: backwards compatibility, avoiding ambiguity, the desire for equivalence, and evolution of the language. *method: design factors for notations*
- `L-comprehension-vs-mapfilter` (Guido van Rossum, 2 rows): List comprehensions are an alternative to map() and filter() that wins on realistic cases, and Van Rossum finds them more readable than the functional notation as complexity grows, rejecting the view that a terser lambda would fix map(). *readability over functional notation*
- `L-list-comprehension` (Guido van Rossum, 2 rows): A list comprehension produces a list of a sequence's values selected by an optional predicate and mapped by a function, a Pythonic interpretation of the mathematical set-builder notation, with multiple for-clauses allowed for nested loops. *notation follows mathematicians' set-builder*
- `L-floor-division` (Guido van Rossum, 10 rows): Python's integer division returns the floor, rounding toward negative infinity rather than truncating toward zero like C, matching number theory's preferred convention and paired with modulo to satisfy a mathematical relationship, with a worry about extending the floor rule to floating-point modulo. *follow number theory's convention over hardware*
- `L-type-is-object` (Guido van Rossum, 2 rows): From its original 1990 design Python made 'type' itself an object: every object's type pointer points to a special object of C function pointers (like a C++ vtable), and a type's own type is a special meta-type recognized by being its own type. *type is itself an object*
- `L-builtins-reassignable` (Guido van Rossum, 5 rows): Built-in names are ordinary identifiers the parser gives no special knowledge, looked up at run time and freely reassignable, so adding a new built-in never invalidates code that used that name. *built-ins are ordinary names, no special parser knowledge*
- `L-keywords-costly` (Guido van Rossum, 2 rows): Every reserved word must be known by everyone using Python since it can never be a name, so the list is kept small and many proposed features were killed or changed to avoid needing a new keyword. *keep reserved words few, they cost everyone*
- `L-no-feature-in-bugfix` (Guido van Rossum, 1 rows): Adding a new feature in a bugfix release (bool in 2.2.1) was the most criticized such instance and would not be done now. *method: no new feature in a bugfix release*
