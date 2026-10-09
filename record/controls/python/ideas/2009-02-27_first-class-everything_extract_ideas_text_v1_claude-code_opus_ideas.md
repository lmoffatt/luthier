---
note: 2009-02-27_first-class-everything.md
note_dir: texts
note_sha256: 8681d606fe718dc31e8ca82f206abd20ad77ae38939ea7e16eb731267e03dd69
title: "First-class Everything"
author: Guido van Rossum
created: 2009-02-27T11:59:00
ideas: 8
quotes_found: 8/8
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### first-class-everything
- **What**: Guido's goal that every object nameable in Python (integers, strings, functions, classes, modules, methods) have equal status: assignable to variables, placed in lists, stored in dictionaries, passed as arguments.
- **Quote**: "One of my goals for Python was to make it so that all objects were "first class."  By this, I meant that I wanted all objects that could be named in the language ... to have equal status." (line 4)

### common-c-data-structure
- **What**: The implementation made first-class-everything simple because all Python objects were based on one common C data structure used everywhere in the interpreter, regardless of whether it held an integer or a class.
- **Quote**: "All of Python's objects were based on a common C data structure that was used everywhere in the interpreter. ... it just didn't matter if the structure happened to represent a simple object such as an integer or something more complicated such as a class." (line 6)

### methods-as-first-class-problem
- **What**: A subtle aspect of making the idea complete was making methods first-class objects, since a method, unlike an ordinary function, expects its first argument to be an instance of its class.
- **Quote**: "there was still one subtle aspect of classes that I still needed to address---namely, the problem of making methods first class objects." (line 8)
- **Also at**: lines 15

### unbound-method
- **What**: Guido created a callable object, the "unbound method," a thin wrapper around the function that enforced the restriction that the first argument be an instance of the class in which the method was defined.
- **Quote**: "I created a type of callable object known as an "unbound method."   An unbound method was really just a thin wrapper around the function object that implemented a method, but it enforced a restriction that the first argument had to be an instance of the class in which the method was defined." (line 17)

### bound-method
- **What**: For a method obtained through an instance, a "bound method" wrapper implicitly stores the original instance so a later call sets it as the first argument.
- **Quote**: "a different callable object known as a "bound method." is used. ... this wrapper implicitly stores the original instance that was used to obtain the method." (line 19)

### one-type-for-both-methods
- **What**: Bound and unbound methods are the same internal object type, distinguished by an instance attribute: None means unbound, otherwise bound.
- **Quote**: "the same internal object type is used to represent bound and unbound methods.   One of the attributes of this object contains a reference to an instance.   If set to None, the method is unbound.  Otherwise, the method is bound." (line 21)

### attribute-lookup-then-call
- **What**: Bound/unbound methods are central to how classes work: "a.spam()" executes in two steps, a lookup of "a.spam" returning a bound method, then a call "()" applied to that object.
- **Quote**: "the execution of that statement actually occurs in two steps.  First, a lookup of "a.spam" occurs.  This returns a bound method--a callable object.    Next, a function call operation "()" is applied to that object to invoke the method" (line 23)

### unbound-methods-removed-py3k
- **What**: In Python 3000 unbound methods were removed and "A.spam" returns a plain function, because the first-argument restriction was rarely helpful for diagnosing problems and often obstructed advanced usages ("duck typing self").
- **Quote**: "In Python 3000, the concept of unbound methods has been removed ... the restriction that the first argument had to be an instance of A was rarely helpful in diagnosing problems, and frequently an obstacle to advanced usages" (line 26)
