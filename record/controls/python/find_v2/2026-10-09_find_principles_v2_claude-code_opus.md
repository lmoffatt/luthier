# Candidate principles of Python, found blind, 2026-10-09

Written by `scripts/find_principles.py` (find_principles v1). Prompt `find_principles_v2` (sha256 5eb0cb1b3e6b),
model opus at effort low via claude-code (2.1.197 (Claude Code)); the model saw only the
lineages and the criterion of infectability.
Inputs by sha256: `record/controls/python/ideas/lineages_link_ideas_v2_claude-code_opus.json` f4564d99c9aa; `record/controls/python/ideas/timeline.jsonl` a50956041718.
Each candidate shows apart what the script took from the rows and what is the model's reading.

Lineages: 156; candidate 16, considered 23, not_principle 117.

## Candidates

```
C1  Make every object that can be named a first-class citizen with equal status: assignable,
    passable, storable, callable.
Instead of: reserving special status for functions, classes or types so some things can be named but
            not handled like the rest
Scope:      language
-- from the rows, by the script
Quote:      "One of my goals for Python was to make it so that all objects were "first class." By
            this, I meant that I wanted all objects that could be named in the language ... to have
            equal status."
Said by:    Guido van Rossum, 2009-02-27 11:59
Source:     2009-02-27_first-class-everything.md line 4 (row written:2009-02-27_first-class-everything:first-class-everything)
Lineages:   L-first-class, L-common-c-struct
Witnesses:  first 2009-01-13 by Guido van Rossum; 3 witnesses over 2 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. collapsing the hierarchy of citizen-kinds into one equal status reorganizes
            how one thinks about what a value is, so functions, classes and types become ordinary
            things to pass and store
Also:       aesthetic. one rule covering all objects is an economy that removes a whole class of
            special cases
Harms:      blurs the line between data and code, surprising newcomers
Harms:      makes everything mutable/replaceable, so few guarantees hold
Harms:      runtime cost of boxing every value as an object
Beats:      L-introspection-type-object (Python's introspection comes from making the type structure
            itself available at run time as an object like any other.). making the type itself a
            run-time object is one striking consequence of equal status, not the rule itself, so it
            infects less
Above next: it opens a wider frame (what a value is) than the rule about what should happen when no
            value can be computed

C2  Never return an undefined or silently wrong value; raise an exception whenever no correct result
    can be computed.
Instead of: returning sentinels, undefined values or silently wrapped results that let an error pass
            unnoticed
Scope:      language
-- from the rows, by the script
Quote:      "I decided that there should be no undefined result values in Python – instead,
            exceptions should always be raised when no correct return value can be computed."
Said by:    Guido van Rossum, 2009-02-03 10:53
Source:     2009-02-03_early-language-design-and-development.md line 38 (row written:2009-02-03_early-language-design-and-development:no-undefined-values)
Lineages:   L-no-undefined-raise, L-c3-rejects, L-exceptions-errorhandling
Witnesses:  first 2009-01-13 by Guido van Rossum; 4 witnesses over 4 days
-- the model's reading (opus, effort low)
Strongest:  ethical. it takes a stance that silence about failure is itself a failure: the language
            refuses to hand back a value it cannot justify
Also:       conceptual. it unifies all failure into one mechanism, so there is never an undefined or
            garbage result to reason about
Harms:      forces callers to handle exceptions everywhere, more verbose control flow
Harms:      a raise can abort a long computation that a sentinel would have let continue
Harms:      hides no-value cases as control flow rather than data
Beats:      L-overflow-check (Integer operations check for overflow and raise OverflowError rather
            than silently clipping; in hindsight they should instead promote the result to long.).
            checking overflow and raising rather than clipping is this rule applied to one
            operation, narrower than the rule itself
Above next: a stance on what the language must never do cuts deeper than a stance about sparing the
            user implementation trivia

C3  Don't make users care about uninteresting implementation details.
Instead of: requiring markers, suffixes or declarations that exist only to serve the implementation
Scope:      language
-- from the rows, by the script
Quote:      "This is one area where Python violated the ABC-inspired philosophy of not requiring
            users to care about a uninteresting implementation details."
Said by:    Guido van Rossum, 2009-02-03 10:53
Source:     2009-02-03_early-language-design-and-development.md line 28 (row written:2009-02-03_early-language-design-and-development:explicit-long-suffix-violates-philosophy)
Lineages:   L-long-suffix-violation
Witnesses:  first 2009-02-03 by Guido van Rossum; 1 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  ethical. it is a position on whose convenience the language serves: the programmer's
            attention, not the implementer's bookkeeping
Also:       emotive. the word 'violated' shows an author who feels the philosophy as an obligation
            he's ashamed to have broken
Harms:      hiding the implementation can cost performance the user can't then control
Harms:      the line of what counts as 'uninteresting' is the designer's, not the user's
Harms:      leaky abstractions bite harder when the detail was meant to be invisible
Beats:      L-reject-instancevar-declarations (Explicit instance-variable declarations were rejected
            (he had gotten this far with none), and lexical markers like a sigil did not appeal to
            him.). refusing instance-variable declarations is one case of sparing the user, not the
            general rule, so it infects less
Above next: it is a rule about the whole user-facing surface, wider than the rule about unifying
            kinds under one concept

C4  When several types share operations, generalize them to one common concept so the same
    operations work the same on all.
Instead of: giving each type its own separate operations with their own names and behavior
Scope:      language
-- from the rows, by the script
Quote:      "I decided to generalize these to a common concept, the sequence. This generalization
            made it so certain core operations such as getting the length (len(s)), indexing (s[i]),
            slicing (s[i:j]), and iteration (for i in s) worked the same on any sequence type."
Said by:    Guido van Rossum, 2009-02-03 10:53
Source:     2009-02-03_early-language-design-and-development.md line 16 (row written:2009-02-03_early-language-design-and-development:sequence-generalization)
Lineages:   L-sequence-concept, L-for-iterable
Witnesses:  first 2009-01-13 by Guido van Rossum; 2 witnesses over 2 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. naming the shared concept behind list, tuple and string reframes operations
            as belonging to a protocol, not to a type, the seed of Python's whole protocol style
Also:       aesthetic. len, indexing, slicing and iteration reading the same on every sequence is an
            economy a reader feels at once
Harms:      forces unrelated types into one interface that may not fit all of them
Harms:      a general concept can be slower than a specialized one
Harms:      duck typing lets a wrong object pass if it happens to answer the same operations
Beats:      L-bound-unbound-methods (Calling a.spam() is a lookup returning a bound-method wrapper
            that stores the instance, then a call; bound and unbound methods share one internal
            type, and unbound methods were removed in Python 3000.). the x.f(0) == C.f(x,0)
            equivalence is one neat uniformity, not a general call to find and name the common
            concept
Above next: finding the concept behind many types reorganizes the frame more than the method
            constraint of not inventing syntax

C5  Prefer the minimal solution that reuses existing constructs; don't add new syntax when an
    existing one will do.
Instead of: inventing dedicated syntax for each new feature (a method keyword, operator
            declarations, a metaclass clause)
Scope:      language
-- from the rows, by the script
Quote:      "A major design constraint was that I didn't want to add syntax for methods that differed
            from the syntax for functions. Refactoring the grammar and the byte code generator to
            handle such similar cases differently felt like a huge task."
Said by:    Guido van Rossum, 2009-02-18 11:25
Source:     2009-02-18_adding-support-for-user-defined-classes.md line 24 (row written:2009-02-18_adding-support-for-user-defined-classes:no-separate-method-syntax)
Lineages:   L-no-separate-method-syntax, L-special-methods, L-metaclass-no-syntax-change,
            L-class-callable-factory, L-everything-statement, L-class-body-statements
Witnesses:  first 2009-02-18 by Guido van Rossum; 10 witnesses over 3 days
-- the model's reading (opus, effort low)
Strongest:  aesthetic. it is a discipline of economy: reach the feature with the construct you
            already have rather than growing the grammar
Also:       ethical. a stance that the language stays small on purpose, that new syntax is a debt
            the whole community pays
Harms:      overloading one syntax for many roles can hide important distinctions from the reader
Harms:      refusing new syntax forces awkward conventions (self, __dunder__, decorators by
            assignment) onto users
Harms:      'minimal' for the implementer can mean surprising for the learner
Beats:      L-descriptor-no-syntax (Descriptors were introduced without new syntax because adding a
            major feature and new syntax at once was deemed too controversial, so users wrapped
            methods with extra assignment statements.). holding descriptors back until syntax could
            follow is one instance of the restraint, not the standing rule to prefer the minimal
            no-new-syntax solution
Above next: a restraint running through the whole grammar outranks a single aesthetic rule about one
            data type's printed form

C6  Make a value's printed representation an expression that is valid input to the parser.
Instead of: printing values in an ad-hoc display form that can't be read back as code
Scope:      language
-- from the rows, by the script
Quote:      "One of the rules I took from ABC was that every data type, when printed or converted to
            a string, should be represented by an expression that was a valid input to the
            language's parser."
Said by:    Guido van Rossum, 2009-02-03 10:53
Source:     2009-02-03_early-language-design-and-development.md line 14 (row written:2009-02-03_early-language-design-and-development:printed-repr-valid-input)
Lineages:   L-repr-valid-input
Witnesses:  first 2009-02-03 by Guido van Rossum; 1 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  aesthetic. a value's printed form being valid input back into the language is a clean
            closure, the output and the source made one
Also:       conceptual. it ties display to the parser, so the reader learns a type's syntax just by
            printing a value of it
Harms:      forces ugly compromises (the trailing comma for one-tuples) to keep output parseable
Harms:      not every object has a sensible literal form, so the rule can't always hold
Harms:      a faithful repr can leak internals the user shouldn't rely on
Beats:      L-tuple-syntax (A trailing comma makes a one-tuple and "()" the empty tuple, so
            representations remain valid parser input.). the trailing-comma tuple syntax exists to
            honor this rule, so it's the rule applied, weaker than the rule
Above next: a rule covering every data type's representation reaches further than one chosen
            indexing convention

C7  Choose the convention whose invariant makes the common cases come out clean, without +1/-1
    corrections.
Instead of: 1-based indexing with closed intervals that force awkward +1/-1 compensation on everyday
            slicing
Scope:      language
-- from the rows, by the script
Quote:      "the invariant that when two / slices are adjacent, the first slice's end index is the
            second slice's / start index is just too beautiful to ignore."
Said by:    Guido van Rossum, 2013-10-24 08:44
Source:     2013-10-24_why-python-uses-0-based-indexing.md line 33 (row written:2013-10-24_why-python-uses-0-based-indexing:adjacency-invariant)
Lineages:   L-halfopen-slicing-indexing
Witnesses:  first 2013-10-24 by Guido van Rossum; 10 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  aesthetic. choosing the convention because adjacent slices share an index is 'too
            beautiful to ignore', design settled by the beauty of the invariant
Also:       conceptual. it reframes indexing around the invariant between slices rather than the
            position of elements, so corrections (+1/-1) disappear
Harms:      0-based half-open trips up people from 1-based math and everyday counting
Harms:      the elegance argument can override what a given domain finds natural
Harms:      off-by-one still bites when the invariant isn't internalized
Beats:      L-floor-division (Python's integer division returns the floor, rounding toward negative
            infinity rather than truncating toward zero like C, matching number theory's preferred
            convention and paired with modulo to satisfy a mathematical relationship, with a worry
            about extending the floor rule to floating-point modulo.). flooring integer division to
            satisfy a math relation is a kindred beauty-of-the-invariant choice but touches one
            operator, narrower

```

## Considered and left out

- `L-concise` (Guido van Rossum, 1 rows): Seemingly complicated tasks can often be expressed in very little Python code. *expressiveness: complicated tasks in little code*
- `L-dynamic-typing` (Guido van Rossum, 3 rows): Python is dynamically typed: variables are names referring to objects, need no declaration, and all type checking happens at run time. *dynamic typing as a stance, but stated as a fact*
- `L-general-purpose` (Guido van Rossum, 1 rows): Python is a general purpose language in the lineage of Lisp or Smalltalk, not merely a scripting language. *a general-purpose language, not a scripting toy*
- `L-borrow-fix-abc` (Guido van Rossum, 2 rows): The design program for Python was to keep what he liked from ABC while fixing its perceived problems, designing his own language rather than porting one. *method: keep what's good from ABC, fix the rest*
- `L-abc-design-method` (Guido van Rossum, 1 rows): ABC was designed by first doing a task analysis and then iterating with serious user testing. *method: task analysis then user testing*
- `L-overflow-check` (Guido van Rossum, 3 rows): Integer operations check for overflow and raise OverflowError rather than silently clipping; in hindsight they should instead promote the result to long. *raise on overflow rather than silently clip*
- `L-tuple-syntax` (Guido van Rossum, 1 rows): A trailing comma makes a one-tuple and "()" the empty tuple, so representations remain valid parser input. *tuple syntax so representations stay valid input*
- `L-instance-representation` (Guido van Rossum, 1 rows): An instance is the simplest possible design: a built-in object holding a class reference and an instance dictionary. *the simplest possible design for instances*
- `L-introspection-type-object` (Guido van Rossum, 1 rows): Python's introspection comes from making the type structure itself available at run time as an object like any other. *introspection: type structure as an object*
- `L-no-method-checking` (Guido van Rossum, 1 rows): Method lookup does no error or conformance checking: an override need not match the base method's arguments, and the first method found is called. *no conformance checking, trust the caller*
- `L-permissive-vs-smalltalk` (Guido van Rossum, 1 rows): Python's objects are more permissive than Smalltalk's, which restricts an object's attributes to those fixed at creation. *objects more permissive than Smalltalk's*
- `L-reject-instancevar-declarations` (Guido van Rossum, 1 rows): Explicit instance-variable declarations were rejected (he had gotten this far with none), and lexical markers like a sigil did not appeal to him. *no instance-variable declarations*
- `L-self-explicit` (Guido van Rossum, 3 rows): A method is just a function whose first argument, named self by convention, is the instance; explicit reference is the only way to reach instance variables, since implicit C++-style resolution is impossible without declarations. *explicit self references over implicit resolution*
- `L-bound-unbound-methods` (Guido van Rossum, 8 rows): Calling a.spam() is a lookup returning a bound-method wrapper that stores the instance, then a call; bound and unbound methods share one internal type, and unbound methods were removed in Python 3000. *x.f(0) == C.f(x,0) equivalence*
- `L-descriptor-no-syntax` (Guido van Rossum, 1 rows): Descriptors were introduced without new syntax because adding a major feature and new syntax at once was deemed too controversial, so users wrapped methods with extra assignment statements. *avoid adding feature and syntax at once*
- `L-comprehension-design-factors` (Guido van Rossum, 1 rows): Four factors governed the design of these notations: backwards compatibility, avoiding ambiguity, the desire for equivalence, and evolution of the language. *method: comprehension design factors*
- `L-comprehension-vs-mapfilter` (Guido van Rossum, 2 rows): List comprehensions are an alternative to map() and filter() that wins on realistic cases, and Van Rossum finds them more readable than the functional notation as complexity grows, rejecting the view that a terser lambda would fix map(). *readability over functional notation*
- `L-list-comprehension` (Guido van Rossum, 2 rows): A list comprehension produces a list of a sequence's values selected by an optional predicate and mapped by a function, a Pythonic interpretation of the mathematical set-builder notation, with multiple for-clauses allowed for nested loops. *pythonic reading of set-builder notation*
- `L-floor-division` (Guido van Rossum, 10 rows): Python's integer division returns the floor, rounding toward negative infinity rather than truncating toward zero like C, matching number theory's preferred convention and paired with modulo to satisfy a mathematical relationship, with a worry about extending the floor rule to floating-point modulo. *floor division to satisfy math relation*
- `L-type-is-object` (Guido van Rossum, 2 rows): From its original 1990 design Python made 'type' itself an object: every object's type pointer points to a special object of C function pointers (like a C++ vtable), and a type's own type is a special meta-type recognized by being its own type. *type is itself an object from the start*
- `L-builtins-reassignable` (Guido van Rossum, 5 rows): Built-in names are ordinary identifiers the parser gives no special knowledge, looked up at run time and freely reassignable, so adding a new built-in never invalidates code that used that name. *built-ins are ordinary names, evolve without breaking code*
- `L-keywords-costly` (Guido van Rossum, 2 rows): Every reserved word must be known by everyone using Python since it can never be a name, so the list is kept small and many proposed features were killed or changed to avoid needing a new keyword. *keep reserved words small, every user pays*
- `L-no-feature-in-bugfix` (Guido van Rossum, 1 rows): Adding a new feature in a bugfix release (bool in 2.2.1) was the most criticized such instance and would not be done now. *method: no features in a bugfix release*
