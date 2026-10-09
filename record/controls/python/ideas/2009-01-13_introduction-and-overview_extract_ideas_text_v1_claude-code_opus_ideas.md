---
note: 2009-01-13_introduction-and-overview.md
note_dir: texts
note_sha256: 67a120bf12b5284d84bc612ff6e36201fa842b7eafb8cb4ef494075b73b7b9a5
title: "Introduction and Overview"
author: Guido van Rossum
created: 2009-01-13T09:17:00
ideas: 13
quotes_found: 13/13
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### python-general-purpose-not-scripting
- **What**: Though often seen as a scripting language, Python is really a general purpose language in the lineage of Lisp or Smalltalk, usable across the whole range from throw-away scripts to large 24x7 web servers.
- **Quote**: "Although it is often viewed as a "scripting" language, it is really a general purpose programming language along the lines of Lisp or Smalltalk" (line 4)

### syntax-borrows-from-c
- **What**: Python's surface syntax deliberately borrows heavily from C: keywords, identifier naming rules, and operator meanings are shared, so the resemblance to C or Pascal is no accident.
- **Quote**: "This is no accident---the syntax of Python borrows heavily from C." (line 11)

### indentation-for-grouping
- **What**: Python departs from C-like languages by using indentation for statement grouping instead of braces, dispensing with braces and trailing semicolons.
- **Quote**: "instead of using braces for statement grouping, it uses indentation" (line 11)
- **Also at**: line 16

### dynamic-typing-names-refer-to-objects
- **What**: Python uses dynamic typing: variables are just names referring to objects, need no declaration, can change type mid-program, and all type checking happens at run-time by an interpreter rather than at a separate compile step.
- **Quote**: "In Python, variables are simply names that refer to objects.   Variables do not need to be declared before they are assigned and they can even change type in the middle of a program." (line 20)
- **Also at**: line 20

### immutable-primitive-types
- **What**: Python's primitive built-in types (Booleans, numbers, strings) are immutable: their values are objects that cannot be modified after creation.
- **Quote**: "These are all immutable types, meaning that values are represented by objects that cannot be modified after their creation." (line 22)

### non-resumable-exceptions
- **What**: Error handling is done through non-resumable exceptions, raised by a raise statement and handled by try/except/finally, with built-in operations throwing exceptions on error conditions.
- **Quote**: "For error handling, Python uses (non-resumable) exceptions." (line 24)

### for-loops-over-iterables
- **What**: The for statement is high-level, looping over any "iterable" object rather than over a numeric index.
- **Quote**: "a high-level for statement that loops over any "iterable" object" (line 24)

### everything-first-class
- **What**: All objects that can be named in Python are "first class", so functions, classes, methods, modules and other named objects can be passed around, inspected, and placed in data structures at run-time.
- **Quote**: "In Python, all objects that can be named are said to be "first class."" (line 26)

### full-oo-support
- **What**: Python provides full object-oriented programming support, including user-defined classes, inheritance, and run-time binding of methods.
- **Quote**: "Python also has full support for object-oriented programming including user-defined classes, inheritance, and run-time binding of methods." (line 26)

### extensive-standard-library
- **What**: An extensive, always-evolving standard library of more than 100 modules is named as one of the main reasons for Python's popularity.
- **Quote**: "Python has an extensive standard library, which is one of the main reasons for its popularity." (line 28)

### expressiveness-little-code
- **What**: A major appeal of Python and other dynamic languages is that seemingly complicated tasks can often be expressed with very little code.
- **Quote**: "seemingly complicated tasks can often be expressed with very little code" (line 32)

### bytecode-compiler-and-interpreter
- **What**: Python is typically implemented as a bytecode compiler plus interpreter, with compilation done implicitly as modules load, and several language primitives requiring the compiler to be present at run-time.
- **Quote**: "Python is typically implemented using a combination of a bytecode compiler and interpreter. Compilation is implicitly performed as modules are loaded, and several language primitives require the compiler to be available at run-time." (line 49)

### multiple-implementations
- **What**: Beyond the C reference implementation, several implementations exist for different platforms and goals (Jython on the JVM, IronPython on .NET, PyPy as a Python-written optimizing compiler, Stackless reducing C-stack reliance to enable co-routines, continuations and microthreads).
- **Quote**: "several other implementations have become popular. Jython is a version that runs on the JVM and has seamless Java integration." (line 49)
