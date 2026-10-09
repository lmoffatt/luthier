# Principles of Python, asked naively, 2026-10-10

Written by `scripts/naive_principles.py` (naive_principles v1). Prompt `naive_principles_v1` (sha256 f28d1cbd5fe5),
model opus at effort low via claude-code (2.1.197 (Claude Code)); the model saw every row
of the timeline (date, who, the idea) and was asked for the rules and principles, nothing more.
Inputs by sha256: `record/controls/python/ideas/timeline.jsonl` a50956041718.
Rows shown: 313. The quote is the first row each candidate cites, filled in by the script.

```
C1  Python is dynamically typed: the compiler ignores declarations and all type checking happens at
    run time, a deliberate corner-cutting simplification that stays safe because every type error is
    still caught before the interpreter can malfunction.
Quote:      "In Python, variables are simply names that refer to objects. Variables do not need to be
            declared before they are assigned and they can even change type in the middle of a
            program."
Said by:    Guido van Rossum, 2009-01-13 09:17 (row written:2009-01-13_introduction-and-overview:dynamic-typing-names-refer-to-objects)
Rows:       6

C2  Prefer the simplest possible implementation and let features fall out of it rather than be
    specially designed in, cutting corners wherever the gap to a fuller design is small.
Quote:      "Python simply drops the compile-time type checking completely. This is entirely in line
            with Python’s “corner-cutting” philosophy as it’s a simplification of the implementation
            that does not affect the eventual safety, since all type errors are caught at run time"
Said by:    Guido van Rossum, 2009-02-10 11:27 (row written:2009-02-10_python-s-use-of-dynamic-typing:python-drops-compile-time-checking)
Rows:       9

C3  Everything nameable in Python (functions, classes, methods, modules, types, even the type
    structure itself) is a first-class, introspectable object that can be passed around, stored, and
    inspected at run time.
Quote:      "In Python, all objects that can be named are said to be "first class.""
Said by:    Guido van Rossum, 2009-01-13 09:17 (row written:2009-01-13_introduction-and-overview:everything-first-class)
Rows:       7

C4  Errors are handled through exceptions and no operation ever returns a silently undefined value:
    when no correct result can be computed, an exception is raised rather than letting a bad value
    pass.
Quote:      "For error handling, Python uses (non-resumable) exceptions."
Said by:    Guido van Rossum, 2009-01-13 09:17 (row written:2009-01-13_introduction-and-overview:non-resumable-exceptions)
Rows:       5

C5  Syntax should be clean and human-readable, using indentation (with a clarifying colon) for
    grouping instead of braces, so program text looks neat and suggests its meaning.
Quote:      "instead of using braces for statement grouping, it uses indentation"
Said by:    Guido van Rossum, 2009-01-13 09:17 (row written:2009-01-13_introduction-and-overview:indentation-for-grouping)
Rows:       7

C6  Don't make users care about uninteresting implementation details: unify related concepts
    (sequences, numbers, statements) into a single general mechanism that behaves consistently.
Quote:      "This is one area where Python violated the ABC-inspired philosophy of not requiring
            users to care about a uninteresting implementation details."
Said by:    Guido van Rossum, 2009-02-03 10:53 (row written:2009-02-03_early-language-design-and-development:explicit-long-suffix-violates-philosophy)
Rows:       6

C7  Preserve backwards compatibility and evolve the language gradually, introducing changes through
    opt-ins (from __future__), deprecation campaigns, and reluctantly added keywords.
Quote:      "A truncating division operator (//) was added to the language to provide the same
            functionality. In addition, a mechanism (\"from __future__ import division\") was
            introduced by which the new integer division semantics could be enabled. ... the correct
            behavior has become the default behavior in Py…"
Said by:    Guido van Rossum, 2009-03-10 13:31 (row written:2009-03-10_the-problem-with-integer-division:fixing-integer-division)
Rows:       7

```
