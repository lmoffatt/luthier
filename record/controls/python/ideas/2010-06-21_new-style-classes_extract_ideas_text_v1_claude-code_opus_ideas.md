---
note: 2010-06-21_new-style-classes.md
note_dir: texts
note_sha256: 4d876e3e41c876d4375fd1651edd343c9bf48ecac2d57d64f80c295e9ebce2ef
title: "New-style Classes"
author: Guido van Rossum
created: 2010-06-21T11:07:00
ideas: 11
quotes_found: 10/11
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### classes-as-afterthought-cut-corners
- **What**: Guido recalls that adding classes to Python was essentially an afterthought, and the implementation he chose exemplified Python's "cut corners" philosophy.
- **Quote**: "Earlier, I described how the addition of classes to Python was essentially an afterthought. The implementation chosen was definitely an example of Python's "cut corners" philosophy." (line 4)

### class-implementation-a-source-of-griping
- **What**: As Python evolved, the problems with the original class implementation became a frequent complaint among expert users.
- **Quote**: "as Python evolved, various problems with the class implementation became a popular topic of griping from expert Python users." (line 4)

### builtin-types-not-subclassable
- **What**: A concrete defect of the old implementation: built-in types like lists, dictionaries and strings were "special" and could not be specialized by subclassing, which seemed odd for a self-described object oriented language.
- **Quote**: "One problem with the class implementation was that there was no way to subclass built-in types... these objects were somehow "special" and could not be specialized via subclassing. This limitation seemed rather odd for a language that claimed to be "object oriented."" (line 6)

### user-classes-outside-the-type-system
- **What**: The type system was "wrong" for user-defined classes: type(a) == type(b) was True even for instances of unrelated classes, unlike C++ and Java where classes are tightly integrated with the type system.
- **Quote**: "statements such as type(a) == type(b) would evaluate as True even if a and b were instances of completely unrelated classes... in those languages, classes were tightly integrated with the underlying type system." (line 8)

### reimplementation-in-2.2-do-it-right
- **What**: In Python 2.2 Guido reimplemented classes to "do it right", the most ambitious rewrite of a major subsystem to date, which he concedes carried a risk of "second-system syndrome".
- **Quote**: "In Python 2.2, I finally took the time to reimplement classes and "do it right." This change was, by far, the most ambitious rewrite of a major Python subsystem to date and one could certainly accuse me of a certain amount of "second-system syndrome" in this effort." (line 10)

### scope-of-the-rewrite
- **What**: Beyond subclassable built-in types, the rewrite added true metaclasses, attempted to fix the naïve method resolution order for multiple inheritance, and added other features.
- **Quote**: "Not only did I address the immediate problem of allowing built-in types to be subclassed, I also added support for true metaclasses, attempted to fix the naïve method resolution order for multiple inheritance, and added a variety of other features." (line 10)

### metaclass-notion-from-forman-danforth
- **What**: A specific notion of what a metaclass is came from the book "Putting Metaclasses to Work" by Ira Forman and Scott Danforth, distinct from the similar Smalltalk concept.
- **Quote**: "A major influence on this work was the book "Putting Metaclasses to Work" by Ira Forman and Scott Danforth, which provided me with a specific notion of what a metaclass is, different from a similar concept in Smalltalk." (line 10)

### new-style-as-feature-not-replacement
- **What**: New-style classes were introduced as a new language feature rather than a strict replacement; for backwards compatibility the old implementation stayed the default in Python 2, and a new-style class is made by subclassing an existing new-style class such as object.
- **Quote**: "new-style classes were introduced as a new language feature, not as a strict replacement for old-style classes. In fact, for backwards compatibility, the old class implementation remains the default class creation protocol in Python 2." (line 12)

### object-as-root-of-hierarchy
- **What**: To create a new-style class one subclasses an existing new-style class such as object, which is the root of the new-style class hierarchy.
- **Quote**: "you simply have to subclass an existing new-style class such as object (which is the root for the new-style class hierarchy)" (line 12)

### rewrite-judged-a-success
- **What**: Guido judges the change a major success: metaclasses became popular with framework writers, explaining classes got easier with fewer exceptions, and maintained backwards compatibility let old code keep working.
- **Quote**: "The change to new-style classes has been a major success. The new metaclasses have become popular amongst framework writers and explaining classes has actually become easier since there were fewer exceptions." (line 15)

### eventual-removal-and-the-object-idiom
- **What**: Although old-style classes will eventually be removed, users are getting used to writing "class MyClass(object)", which Guido judges "isn't so bad".
- **Quote**: "although the old-style classes will eventually be removed from the languages, users are getting used to writing "class MyClass(object)" to declare a class, which isn't so bad." (line 15)
