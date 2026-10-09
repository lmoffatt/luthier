# Candidate principles of Python, found blind, 2026-10-09

Written by `scripts/find_principles.py` (find_principles v1). Prompt `find_principles_v1` (sha256 892e58875a4e),
model opus at effort low via claude-code (2.1.197 (Claude Code)); the model saw only the
lineages and the criterion of infectability.
Inputs by sha256: `record/controls/python/ideas/lineages_link_ideas_v2_claude-code_opus.json` f4564d99c9aa; `record/controls/python/ideas/timeline.jsonl` a50956041718.
Each candidate shows apart what the script took from the rows and what is the model's reading.

Lineages: 156; candidate 14, considered 24, not_principle 118.

## Candidates

```
C1  Every object that can be named has equal, first-class status: assignable, passable, storable,
    including types themselves.
Scope:      language
-- from the rows, by the script
Quote:      "One of my goals for Python was to make it so that all objects were "first class." By
            this, I meant that I wanted all objects that could be named in the language ... to have
            equal status."
Said by:    Guido van Rossum, 2009-02-27 11:59
Source:     2009-02-27_first-class-everything.md line 4 (row written:2009-02-27_first-class-everything:first-class-everything)
Lineages:   L-first-class, L-introspection-type-object, L-type-is-object
Witnesses:  first 2009-01-13 by Guido van Rossum; 5 witnesses over 4 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. treating every nameable thing as an object of equal status reorganizes the
            whole mental model of the language
Also:       aesthetic. one uniform rule replaces a hierarchy of special cases
Harms:      erases useful distinctions between kinds of value, so less can be caught statically
Harms:      boxing everything in one object structure has a run-time cost
Beats:      L-sequence-concept (List, tuple, and string were generalized to a common sequence
            concept so length, indexing, slicing, and iteration work the same on any of them.). the
            sequence concept generalizes across a few types; first-class generalizes across all
            objects
Above next: a frame for the entire object model reaches further than a single typing discipline

C2  Variables are names referring to objects, needing no declaration, and all type checking happens
    at run time.
Scope:      language
-- from the rows, by the script
Quote:      "In Python, variables are simply names that refer to objects. Variables do not need to be
            declared before they are assigned and they can even change type in the middle of a
            program."
Said by:    Guido van Rossum, 2009-01-13 09:17
Source:     2009-01-13_introduction-and-overview.md line 20 (row written:2009-01-13_introduction-and-overview:dynamic-typing-names-refer-to-objects)
Lineages:   L-dynamic-typing, L-dynamic-no-return
Witnesses:  first 2009-01-13 by Guido van Rossum; 4 witnesses over 2 days
-- the model's reading (opus, effort low)
Strongest:  conceptual. types live on values, not on variables, so a name is just a binding to an
            object; this rewires how one thinks about variables
Also:       ethical. dropping compile-time checking is cast as corner-cutting that costs no eventual
            safety
Harms:      type errors surface only at run time, sometimes far from their cause
Harms:      no compiler coercion, so passing an int for a float can pass silently (l75)
Beats:      L-builtins-reassignable (Built-in names are ordinary identifiers the parser gives no
            special knowledge, looked up at run time and freely reassignable, so adding a new
            built-in never invalidates code that used that name.). reassignable built-ins is one
            consequence of late binding, narrower than the whole typing model
Above next: the typing discipline shapes every line a programmer writes, where indentation shapes
            the surface

C3  Statements are grouped by indentation rather than by braces or keywords.
Scope:      language
-- from the rows, by the script
Quote:      "instead of using braces for statement grouping, it uses indentation"
Said by:    Guido van Rossum, 2009-01-13 09:17
Source:     2009-01-13_introduction-and-overview.md line 11 (row written:2009-01-13_introduction-and-overview:indentation-for-grouping)
Lineages:   L-indentation
Witnesses:  first 2009-01-13 by Guido van Rossum; 5 witnesses over 3 days
-- the model's reading (opus, effort low)
Strongest:  aesthetic. removing braces makes the visible structure the actual structure, an economy
            that sticks on sight
Also:       ethical. the layout you read is the layout the machine runs; no divergence allowed
Harms:      whitespace becomes semantically load-bearing, so invisible characters change meaning
Harms:      mixed tabs and spaces can break code silently
Beats:      L-colon (The colon separating the lead-in clause from the indented block, invented by
            ABC's authors, was kept because user testing showed it clarifies the indentation for
            beginners.). the colon only clarifies where a block begins; indentation carries the
            whole grouping
Above next: indentation infects on sight, before code is even run, where a correctness policy shows
            only when something goes wrong

C4  There are no undefined result values: an exception is always raised when no correct value can be
    computed, and errors never pass silently.
Scope:      language
-- from the rows, by the script
Quote:      "I decided that there should be no undefined result values in Python – instead,
            exceptions should always be raised when no correct return value can be computed."
Said by:    Guido van Rossum, 2009-02-03 10:53
Source:     2009-02-03_early-language-design-and-development.md line 38 (row written:2009-02-03_early-language-design-and-development:no-undefined-values)
Lineages:   L-no-undefined-raise, L-c3-rejects
Witnesses:  first 2009-02-03 by Guido van Rossum; 2 witnesses over 2 days
-- the model's reading (opus, effort low)
Strongest:  ethical. a stand that a wrong answer is worse than a stopped program
Also:       conceptual. forbidding undefined result values reframes what a function may legitimately
            return
Harms:      forces handling or crashing where a caller might prefer a sentinel
Harms:      exceptions used as control flow can hide costly paths
Beats:      L-long-suffix-violation (Requiring a trailing L to mark longs violated the ABC-inspired
            philosophy of not making users care about uninteresting implementation details.). not
            bothering users with implementation details is a comfort rule; never passing silently is
            a safety stance that bites harder
Above next: a correctness stance outranks the explicitness convention that follows it

C5  A method is just a function whose first argument, by convention self, is the instance; explicit
    reference is the only way to reach instance variables.
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
Strongest:  ethical. making the instance an explicit argument is a stand for explicitness over
            hidden lookup magic
Also:       aesthetic. a method is just a function; x.f(a) equals C.f(x, a), one rule with no
            special method syntax
Harms:      every method carries a visible self, which users read as redundant boilerplate
Harms:      ties the model to the function-with-first-argument equivalence
Beats:      L-reject-instancevar-declarations (Explicit instance-variable declarations were rejected
            (he had gotten this far with none), and lexical markers like a sigil did not appeal to
            him.). rejecting instance-variable declarations is the absence of a feature; explicit
            self is a positive rule seen everywhere
Above next: explicitness as a named rule outranks the design-economy principle that comes next

C6  Prefer the minimal solution that reuses existing mechanisms over adding new syntax.
Scope:      language
-- from the rows, by the script
Quote:      "making the class object itself callable was the right, "minimal" solution, requiring no
            new syntax... what I had done was simply to turn each class into its own factory."
Said by:    Guido van Rossum, 2009-02-18 11:25
Source:     2009-02-18_adding-support-for-user-defined-classes.md line 73 (row written:2009-02-18_adding-support-for-user-defined-classes:callable-class-no-new-operator)
Lineages:   L-class-callable-factory, L-no-separate-method-syntax, L-special-methods,
            L-metaclass-no-syntax-change
Witnesses:  first 2009-02-18 by Guido van Rossum; 5 witnesses over 2 days
-- the model's reading (opus, effort low)
Strongest:  aesthetic. solve by reusing what already exists rather than adding grammar, an economy
            of means
Also:       ethical. restraint about growing the language, keeping the surface small
Harms:      reusing mechanisms can overload them past clarity (a class body runs arbitrary code)
Harms:      avoiding syntax pushes complexity into conventions and __dunder__ names
Beats:      L-everything-statement (Every part of the language is an executable statement that can
            appear anywhere, which simplified the grammar (earlier it restricted declarative
            constructs to the top level).). everything-is-a-statement is one instance of this
            restraint, not the rule itself
Above next: a design-method principle guides more choices than a single slicing convention

C7  Index from 0 with half-open intervals and suitable defaults, so common slices need no +1/-1
    corrections.
Scope:      language
-- from the rows, by the script
Quote:      "Using / 0-based indexing, half-open intervals, and suitable defaults (as Python / ended
            up having), they are beautiful: a[:n] and a[i:i+n]"
Said by:    Guido van Rossum, 2013-10-24 08:44
Source:     2013-10-24_why-python-uses-0-based-indexing.md line 15 (row written:2013-10-24_why-python-uses-0-based-indexing:zero-based-half-open-defaults-elegant)
Lineages:   L-halfopen-slicing-indexing
Witnesses:  first 2013-10-24 by Guido van Rossum; 10 witnesses over 1 days
-- the model's reading (opus, effort low)
Strongest:  aesthetic. the adjacency invariant, one slice's end being the next one's start, is a
            small beauty that lodges in the head
Also:       conceptual. it reframes indices as boundaries between items rather than the items
            themselves
Harms:      half-open intervals confuse newcomers who expect the last index included
Harms:      0-based plus half-open is two conventions to internalize at once
Beats:      L-list-comprehension (A list comprehension produces a list of a sequence's values
            selected by an optional predicate and mapped by a function, a Pythonic interpretation of
            the mathematical set-builder notation, with multiple for-clauses allowed for nested
            loops.). the list comprehension's beauty is borrowed from set-builder notation; the
            slicing invariant is Python's own

```

## Considered and left out

- `L-concise` (Guido van Rossum, 1 rows): Seemingly complicated tasks can often be expressed in very little Python code. *complicated tasks expressible in little code, a value*
- `L-for-iterable` (Guido van Rossum, 1 rows): Python's for statement loops over any iterable object rather than over a numeric index. *loop over any iterable, not an index*
- `L-borrow-fix-abc` (Guido van Rossum, 2 rows): The design program for Python was to keep what he liked from ABC while fixing its perceived problems, designing his own language rather than porting one. *method: borrow what's good, fix problems*
- `L-abc-design-method` (Guido van Rossum, 1 rows): ABC was designed by first doing a task analysis and then iterating with serious user testing. *method: task analysis then user testing*
- `L-colon` (Guido van Rossum, 3 rows): The colon separating the lead-in clause from the indented block, invented by ABC's authors, was kept because user testing showed it clarifies the indentation for beginners. *colon clarifies the block*
- `L-long-suffix-violation` (Guido van Rossum, 1 rows): Requiring a trailing L to mark longs violated the ABC-inspired philosophy of not making users care about uninteresting implementation details. *users shouldn't care about uninteresting implementation details*
- `L-repr-valid-input` (Guido van Rossum, 1 rows): Every data type, when printed or converted to a string, should be represented by an expression valid as input to the parser (a rule from ABC). *printed form valid as parser input*
- `L-sequence-concept` (Guido van Rossum, 1 rows): List, tuple, and string were generalized to a common sequence concept so length, indexing, slicing, and iteration work the same on any of them. *generalize types to a common sequence concept*
- `L-assignment-no-search` (Guido van Rossum, 1 rows): Variable reference searches locals, globals, built-ins in order, but assignment never searches: it creates or replaces in the first (local) dictionary, with a global declaration the only override. *assignment creates in local scope, never searches*
- `L-class-body-statements` (Guido van Rossum, 2 rows): Any valid Python statements may appear in a class body, extending from allowing variable assignments to allowing arbitrary executable code. *don't artificially limit what's allowed in a class body*
- `L-class-dynamic-modification` (Guido van Rossum, 2 rows): Classes and instances can be modified dynamically by updating their dictionaries, though new-style classes require attribute assignment rather than using __dict__ directly. *classes and instances modifiable dynamically*
- `L-no-method-checking` (Guido van Rossum, 1 rows): Method lookup does no error or conformance checking: an override need not match the base method's arguments, and the first method found is called. *no conformance checking, call first found*
- `L-permissive-vs-smalltalk` (Guido van Rossum, 1 rows): Python's objects are more permissive than Smalltalk's, which restricts an object's attributes to those fixed at creation. *objects more permissive than Smalltalk*
- `L-reject-instancevar-declarations` (Guido van Rossum, 1 rows): Explicit instance-variable declarations were rejected (he had gotten this far with none), and lexical markers like a sigil did not appeal to him. *no declarations for instance variables*
- `L-everything-statement` (Guido van Rossum, 3 rows): Every part of the language is an executable statement that can appear anywhere, which simplified the grammar (earlier it restricted declarative constructs to the top level). *every part an executable statement*
- `L-not-functional` (Guido van Rossum, 2 rows): Van Rossum never viewed Python as a functional language or heavily influenced by them, and its dynamic nature rules out functional-style compile-time optimization such as tail recursion. *accept the language's dynamic nature, no functional optimization*
- `L-descriptor-no-syntax` (Guido van Rossum, 1 rows): Descriptors were introduced without new syntax because adding a major feature and new syntax at once was deemed too controversial, so users wrapped methods with extra assignment statements. *don't introduce a feature and new syntax at once*
- `L-comprehension-design-factors` (Guido van Rossum, 1 rows): Four factors governed the design of these notations: backwards compatibility, avoiding ambiguity, the desire for equivalence, and evolution of the language. *method: factors governing comprehension design*
- `L-comprehension-vs-mapfilter` (Guido van Rossum, 2 rows): List comprehensions are an alternative to map() and filter() that wins on realistic cases, and Van Rossum finds them more readable than the functional notation as complexity grows, rejecting the view that a terser lambda would fix map(). *readability over functional notation*
- `L-genexp-syntax` (Guido van Rossum, 3 rows): A generator expression's parentheses belong to the surrounding call, so a bare comma sequence after 'in' would be ambiguous; Python required a single expression there, unlike Python 2 list comprehensions, choosing not to guess and not to break existing list-comprehension code. *don't guess, don't break existing code*
- `L-list-comprehension` (Guido van Rossum, 2 rows): A list comprehension produces a list of a sequence's values selected by an optional predicate and mapped by a function, a Pythonic interpretation of the mathematical set-builder notation, with multiple for-clauses allowed for nested loops. *Pythonic set-builder notation*
- `L-builtins-reassignable` (Guido van Rossum, 5 rows): Built-in names are ordinary identifiers the parser gives no special knowledge, looked up at run time and freely reassignable, so adding a new built-in never invalidates code that used that name. *adding to the language never breaks code; names resolved at run time*
- `L-keywords-costly` (Guido van Rossum, 2 rows): Every reserved word must be known by everyone using Python since it can never be a name, so the list is kept small and many proposed features were killed or changed to avoid needing a new keyword. *keep reserved words few*
- `L-no-feature-in-bugfix` (Guido van Rossum, 1 rows): Adding a new feature in a bugfix release (bool in 2.2.1) was the most criticized such instance and would not be done now. *method: no features in a bugfix release*
