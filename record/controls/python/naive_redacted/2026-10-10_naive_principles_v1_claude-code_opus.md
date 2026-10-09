# Principles of Python, asked naively, 2026-10-10

Written by `scripts/naive_principles.py` (naive_principles v1). Prompt `naive_principles_v1` (sha256 f28d1cbd5fe5),
model opus at effort low via claude-code (2.1.197 (Claude Code)); the model saw every row
of the timeline (date, who, the idea) and was asked for the rules and principles, nothing more; names redacted (Python=L; Guido van Rossum=the designer; Guido=the designer; van Rossum=the designer; ABC=the predecessor).
Inputs by sha256: `record/controls/python/ideas/timeline.jsonl` a50956041718.
Rows shown: 313. The quote is the first row each candidate cites, filled in by the script.

```
C1  L is dynamically typed: variables are untyped names bound to objects and all type checking
    happens at run time rather than at a separate compile step, a deliberate corner-cutting
    simplification that keeps safety because every type error is still caught before the interpreter
    can malfunction.
Quote:      "In Python, variables are simply names that refer to objects. Variables do not need to be
            declared before they are assigned and they can even change type in the middle of a
            program."
Said by:    Guido van Rossum, 2009-01-13 09:17 (row written:2009-01-13_introduction-and-overview:dynamic-typing-names-refer-to-objects)
Rows:       6

C2  Every object nameable in L (integers, strings, functions, classes, methods, modules, types) is
    first-class with equal status, assignable, passable, storable and introspectable at run time,
    made uniform by basing all objects on one common C structure whose type is itself a run-time
    object.
Quote:      "In Python, all objects that can be named are said to be "first class.""
Said by:    Guido van Rossum, 2009-01-13 09:17 (row written:2009-01-13_introduction-and-overview:everything-first-class)
Rows:       6

C3  The implementation consistently chooses the simplest design that works, cutting corners and
    letting useful features fall out of the mechanism rather than being designed in, even for
    subsystems like classes added late as an afterthought.
Quote:      "Python simply drops the compile-time type checking completely. This is entirely in line
            with Python’s “corner-cutting” philosophy as it’s a simplification of the implementation
            that does not affect the eventual safety, since all type errors are caught at run time"
Said by:    Guido van Rossum, 2009-02-10 11:27 (row written:2009-02-10_python-s-use-of-dynamic-typing:python-drops-compile-time-checking)
Rows:       6

C4  Errors are handled through exceptions rather than undefined or silently-clipped results: no
    operation returns an undefined value, an exception is always raised when no correct value can be
    computed, and inconsistent situations are rejected rather than resolved silently.
Quote:      "For error handling, Python uses (non-resumable) exceptions."
Said by:    Guido van Rossum, 2009-01-13 09:17 (row written:2009-01-13_introduction-and-overview:non-resumable-exceptions)
Rows:       6

C5  A data type's printed representation should be a valid parser input that reconstructs it, and
    related indexable types are unified under common abstractions (the sequence; half-open 0-based
    slicing) so operations behave uniformly and compose without off-by-one corrections.
Quote:      "One of the rules I took from ABC was that every data type, when printed or converted to
            a string, should be represented by an expression that was a valid input to the
            language's parser."
Said by:    Guido van Rossum, 2009-02-03 10:53 (row written:2009-02-03_early-language-design-and-development:printed-repr-valid-input)
Rows:       6

C6  Syntax uses indentation for grouping with a colon introducing the block, inherited from the
    predecessor B, dispensing with braces and semicolons, while borrowing keywords and operator
    meanings from C and Algol-family languages.
Quote:      "instead of using braces for statement grouping, it uses indentation"
Said by:    Guido van Rossum, 2009-01-13 09:17 (row written:2009-01-13_introduction-and-overview:indentation-for-grouping)
Rows:       6

C7  The language evolves without needlessly breaking working code: new built-ins and features are
    added back-compatibly (new keywords only reluctantly, via __future__ opt-ins and deprecation),
    favoring the designer's own coding time and users' existing code over premature optimization.
Quote:      "I think I also wanted to optimize testing for exceptions by using pointer comparisons
            instead of string value comparisons in a misguided attempt to prematurely optimize
            execution time (a rare one – I usually optimized for my own coding time!)."
Said by:    Guido van Rossum, 2009-03-06 09:26 (row written:2009-03-06_how-exceptions-came-to-be-classes:premature-optimization-pointer-comparison)
Rows:       6

```
