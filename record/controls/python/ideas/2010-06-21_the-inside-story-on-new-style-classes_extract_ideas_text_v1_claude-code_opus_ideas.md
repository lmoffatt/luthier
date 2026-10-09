---
note: 2010-06-21_the-inside-story-on-new-style-classes.md
note_dir: texts
note_sha256: 49c435c2a914aea5ba8ddb92dd2b47f871b6b4c5991e513eb4d9e5857ee7263d
title: "The Inside Story on New-Style Classes"
author: Guido van Rossum
created: 2010-06-21T11:18:00
ideas: 18
quotes_found: 18/18
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### new-style-classes-introduced-new-concepts
- **What**: New-style classes look similar to the original class implementation on the surface, but introduced several new concepts: `__new__()`, descriptors, static and class methods, properties, decorators, slots, and a new Method Resolution Order.
- **Quote**: "On the surface, new-style classes appear very similar to the original class implementation. However, new-style classes also introduced a number of new concepts:" (line 4)

### new-hook-for-customizing-object-creation
- **What**: Old-style classes gave `__init__()` for initializing an instance after creation but never provided a real hook to customize how instances are created; `__new__()` was introduced as a class method so the author can control instance creation.
- **Quote**: "Old-style classes never really provided a hook for customizing the creation of objects although there were library modules allowed certain kinds of objects to be created in non-standard ways (e.g., the \"new\" module)." (line 24)
- **Also at**: lines 22, 26

### new-enables-creation-patterns-and-unpickling
- **What**: Overriding `__new__()` lets a class implement patterns like Singleton, return a previously created instance, or return an instance of a different class; it is also used in pickle to create instances while unserializing without invoking `__init__`.
- **Quote**: "By overriding __new__() a class author can implement patterns like the Singleton Pattern, return a previously created instance (e.g., from a free list), or to return an instance of a different class (e.g., a subclass)." (line 26)

### new-for-subclassing-immutable-types
- **What**: Immutable objects cannot be initialized through a standard `__init__()`, so `__new__` lets their subclasses perform any special initialization as the object is created, e.g. passing a modified value to the base class `__new__`.
- **Quote**: "Another use of __new__ is to help with the subclassing of immutable types. By the nature of their immutability, these kinds of objects can not be initialized through a standard __init__() method." (line 28)

### descriptors-generalize-bound-methods
- **What**: Descriptors generalize the concept of bound methods, which was central to classic classes; in classic classes a function found in a class dictionary during attribute lookup was returned as a currying wrapper that inserts the instance in front of the argument list.
- **Quote**: "Descriptors are a generalization of the concept of bound methods, which was central to the implementation of classic classes." (line 32)
- **Also at**: lines 34, 36

### self-argument-mechanism
- **What**: The wrapper returned by attribute lookup is the fundamental mechanism by which methods obtain their "self" argument, calling the original function with the instance inserted in front.
- **Quote**: "This is the fundamental mechanism by which methods in classes obtain their \"self\" argument." (line 36)

### x-f-equals-C-f-x
- **What**: Asking the class for the function attribute returns the unwrapped function, so `x.f(0)` is equivalent to `C.f(x, 0)`, a fundamental equivalence in Python.
- **Quote**: "In other words, x.f(0) is equivalent to C.f(x, 0). This is a pretty fundamental equivalence in Python." (line 38)

### class-attributes-as-default-values
- **What**: For classic classes, non-function class attributes are returned unchanged, allowing class attributes to serve as "default" values for instance variables; assignment to the instance shadows the class value and deletion reveals it again.
- **Quote**: "This makes it possible to use class attributes as “default” values for instance variables." (line 40)

### limitation-of-hard-coded-wrapping
- **What**: The old scheme only wrapped Python function objects and this was hard-coded, preventing "hybrid" classes mixing Python and C methods and giving no obvious way to define other kinds of methods such as static member functions.
- **Quote**: "One limitation was that it was prevented the creation of “hybrid” classes that had some methods implemented in Python and others in C, because only Python functions were being wrapped in such a way as to provide the method with access to the instance, and this behavior was hard-coded in the language." (line 42)

### descriptor-protocol-get
- **What**: Python 2.2 generalized the wrapping behavior: instead of hard-coding which objects get wrapped, the object found by the attribute search decides via a `__get__` method; function objects gained a `__get__` so users can define their own descriptor classes.
- **Quote**: "Instead of hard-coding the behavior that Python function objects are wrapped and other objects aren’t, the wrapping is now left up to the object found by the attribute search ... If the object found by an attribute search happens to have a special method named __get__, it is considered to be a \"descriptor\" object." (line 44)

### descriptor-set-and-delete
- **What**: The same idea was extended to setting and deleting attributes through `__set__` and `__delete__`, giving a descriptor complete control over get/set/delete; this customization applies only when the descriptor appears in a class dictionary, not an instance dictionary.
- **Quote**: "Thus, by redefining these methods, a descriptor object can have complete control over what it means to get, set, and delete an attribute. However, it's important emphasize that this customization only applies when a descriptor instance appears in a class dictionary—not the instance dictionary of an object." (line 46)

### classmethod-staticmethod-property-built-on-descriptors
- **What**: Python 2.2 added classmethod, staticmethod, and property as predefined classes built on the descriptor machinery; staticmethod calls the function unchanged, classmethod passes the class as first argument, and property turns a getter/setter pair into an attribute.
- **Quote**: "Python 2.2 added three predefined classes: classmethod, staticmethod, and property, that utilized the new descriptor machinery." (line 50)
- **Also at**: lines 52, 57

### no-new-syntax-at-first
- **What**: These descriptors were introduced without special syntax because it was deemed too controversial to add a major feature and new syntax at once; users wrapped methods with extra assignment statements instead.
- **Quote**: "At the time, it was deemed too controversial to simultaneously introduce a major new feature along with new syntax (which always leads to a heated debate)." (line 59)

### decorators-address-readability-downside
- **What**: The wrapping-by-assignment approach forced the reader to reach the end of a method before learning its kind; Python 2.4 introduced decorator syntax (`@expression` before a declaration) to fix this.
- **Quote**: "A downside of this approach is that the reader of a class had to read all the way till the end of a method declaration before finding out whether it was a class or static method (or some user-defined variation)." (line 75)
- **Also at**: line 82

### decorator-syntax-chosen-by-bdfl-pronouncement
- **What**: The decorator syntax, derived from Java's annotations, was debated endlessly and decided by "BDFL pronouncement"; decorator is not to be confused with descriptor.
- **Quote**: "The particular choice of decorator syntax (derived from Java's annotations) was debated endlessly before it was decided by “BDFL pronouncement”." (line 82)

### decorators-exceeded-expectations
- **What**: Decorators became one of the more successful features, with custom uses exceeding Guido's widest expectations (especially web frameworks), leading to their extension to class definitions in Python 2.6.
- **Quote**: "The decorator feature has become one of the more successful language features, and the use of custom decorators has exceeded my widest expectations." (line 84)

### slots-as-descriptor-application
- **What**: `__slots__` is another application of descriptors: it restricts valid attribute names, removes the instance `__dict__`, and stores attributes in array locations, each slot being a descriptor that gets/sets via an array index, implemented entirely in C.
- **Quote**: "Another enhancement made possible with descriptors was the introduction of the __slots__ attribute on classes." (line 88)
- **Also at**: line 91

### slots-ultimate-goal-was-performance
- **What**: Contrary to the assumption that `__slots__` is for code safety, its ultimate goal was performance; Guido feared the class-system changes (the extra data-descriptor check on every attribute access) would hurt performance, so `__slots__` was a fallback optimization. It turned out unnecessary but was too late to remove, though used properly it can reduce memory footprint.
- **Quote**: "Some people mistakenly assume that the intended purpose of __slots__ is to increase code safety (by restricting the attribute names). In reality, my ultimate goal was performance." (line 93)
- **Open**: The performance fear turned out unnecessary ("This turned out unnecessary"), yet `__slots__` remained because it was too late to remove it.
