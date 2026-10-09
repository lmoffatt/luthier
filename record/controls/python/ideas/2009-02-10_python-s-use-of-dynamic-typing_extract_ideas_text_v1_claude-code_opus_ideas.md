---
note: 2009-02-10_python-s-use-of-dynamic-typing.md
note_dir: texts
note_sha256: f70292d5e4add6370268af5dc690432dd502499972917e82c5721bd5e7e0f5df
title: "Python's Use of Dynamic Typing"
author: Guido van Rossum
created: 2009-02-10T11:27:00
ideas: 9
quotes_found: 8/9
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### python-is-dynamically-typed
- **What**: Python is dynamically typed: the compiler ignores the types in a program and all type checking happens at run time, in contrast to ABC's static typing.
- **Quote**: "In contrast, Python is dynamically typed.  The Python compiler is blissfully unaware of the types used in a program, and all type checking is done at run time." (line 2)

### abc-static-typing-with-inference
- **What**: ABC was statically typed, rejecting inconsistent programs before execution, and unlike most statically typed languages of its time used type inference rather than explicit declarations, like Haskell rather than C.
- **Quote**: "ABC is statically typed which meant that the ABC compiler analyzes the use of types in a program and decides whether they are used consistently. If not, the program is rejected ... ABC used type inference (not unlike Haskell) instead of explicit type declarations" (line 2)

### abc-also-checked-types-at-runtime
- **What**: ABC did not rely only on static checking; its run-time library re-checked argument types on every operation, so the gap between ABC and Python is smaller than it seems.
- **Quote**: "ABC doesn't ... exclusively rely on static type checking to keep the program from crashing, but has a run-time library that checks the argument types for all operations again each time they are executed." (line 4)

### runtime-checking-as-sanity-check-and-debugging-aid
- **What**: ABC's run-time type checking served as a sanity check for the compiler's not-fully-implemented type-checking algorithms and as a debugging aid producing readable error messages instead of core dumps.
- **Quote**: "This was done in part as a sanity check for the compiler’s type-checking algorithms ... The runtime library was also useful as a debugging aid since explicit run time type checking could produce nice error messages ... instead of the core dumps" (line 4)

### interactivity-forces-dynamic-typing
- **What**: The most important reason ABC had run-time type checking is that it is interactive: across separately entered statements it is unreasonable to forbid reusing a variable name with a different type.
- **Quote**: "the most important reason why ABC has run time type checking in addition to static type checking is that it is interactive." (line 6)

### abc-compromise-global-dynamic-local-static
- **What**: ABC compromised by using dynamic type checking for global variables and static checking for local ones, though to simplify implementation local variables were dynamically checked as well.
- **Quote**: "ABC uses dynamic type checking for global variables, but static type checking for local variables. To simplify the implementation, local variables are dynamically type checked as well." (line 6)

### python-drops-compile-time-checking
- **What**: Python's approach is a small step from ABC's: it drops compile-time type checking completely, in line with Python's "corner-cutting" philosophy, a simplification that does not affect safety since all type errors are still caught at run time before the interpreter can malfunction.
- **Quote**: "Python simply drops the compile-time type checking completely. This is entirely in line with Python’s “corner-cutting” philosophy as it’s a simplification of the implementation that does not affect the eventual safety, since all type errors are caught at run time" (line 8)

### dynamic-typing-is-irreversible
- **What**: Once dynamic typing is chosen there is no going back, because ABC's operations were designed so argument types could be deduced from the form of the operation, while in Python such deductions generally cannot be made.
- **Quote**: "once you decide on dynamic typing, there is no way to go back. ABC’s built-in operations were carefully designed so that the type of the arguments could be deduced from the form of the operation ... In Python, such deductions cannot generally be made." (line 10)

### operator-overloading-blocks-type-deduction
- **What**: In Python an expression like "x+y" is ambiguous between string concatenation, numeric addition, or an overloaded operation on user-defined types, so the type cannot be deduced from the operation's form.
- **Quote**: "the expression “x+y” could be a string concatenation, a numeric addition, or an overloaded operation on user-defined types." (line 10)
