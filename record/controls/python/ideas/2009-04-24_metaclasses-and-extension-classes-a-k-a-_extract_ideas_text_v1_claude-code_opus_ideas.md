---
note: 2009-04-24_metaclasses-and-extension-classes-a-k-a-the-killer.md
note_dir: texts
note_sha256: 263a946463a2dae7538b75136927c4be6109c5fe4ec7a3487b3f087f4103c5b5
title: "Metaclasses and Extension Classes (a.k.a. “The Killer Joke”)"
author: Guido van Rossum
created: 2009-04-24T09:14:00
ideas: 14
quotes_found: 14/14
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### classes-as-first-class-objects
- **What**: In Python's original design, classes were first class objects that could be manipulated like any other object, yet the act of creating a class was fixed and hidden from users.
- **Quote**: "In Python’s original implementation, classes were first class objects that could be manipulated just like any other object.    However, the process of creating a class object was something that was set in stone." (line 2)

### class-creation-as-hidden-internal-step
- **What**: Defining a class executes its body in a local dictionary, then passes the name, a tuple of base classes, and that dictionary to an internal class creation function; this machinery was hidden as an implementation detail users didn't need to know.
- **Quote**: "The name of the class, a tuple of base classes, and this local dictionary would then be passed to an internal class creation function that was responsible for creating the class object.  Since all of this machinery was hidden away behind the scenes, it was an implementation detail that users didn’t need to worry about." (line 4)

### missed-opportunity-for-custom-classes
- **What**: Beaudry's point (reported by the author) that hiding class creation was a missed opportunity: if classes are special kinds of objects, one could create new kinds of classes that behave differently.
- **Quote**: "Don Beaudry was the first to point out that this was a missed opportunity for expert users.   Specifically, if classes were simply special kinds of objects, why couldn’t you create new kinds of classes that could be customized to behave in different ways?" (line 6)

### don-beaudry-hook
- **What**: Beaudry proposed (reported by the author) a slight interpreter modification letting C extension modules create new kinds of class objects; it entered in 1995, was generalized by Jim Fulton, and remained until replaced by metaclasses in 2.2.
- **Quote**: "He then suggested a very slight modification to the interpreter that would allow new kinds of class objects to be created by C code extension modules." (line 6)

### user-supplied-final-construction-function
- **What**: The core idea: expert users could make custom class objects if a user-supplied function could stand in at the final step of class creation, receiving the name, bases, and dictionary and doing whatever it wanted with them.
- **Quote**: "expert users would be able to create custom class objects if there was some way to supply a user-supplied function in the final step of class creation." (line 8)

### no-change-to-class-syntax
- **What**: A constraint the author placed on himself: the mechanism had to work without changing the already well-established class syntax.
- **Quote**: "The only catch was that I didn't want to make any changes to the class syntax which had already been well-established." (line 8)

### callable-base-class-triggers-hook
- **What**: The hook's mechanism: a callable type object used as a base class makes the class creation code call that type instead of creating a standard class; the behavior of such classes and their instances is entirely up to the extension module.
- **Quote**: "when an instance of such a callable type was used as a base class in a class statement, the class creation code would magically call that type object instead of creating a standard class object.  The behavior of classes created this way (and their instances) was completely up to the extension module providing the callable type object." (line 10)

### types-were-not-callable-at-the-time
- **What**: Why the hook felt like a hack: type objects were not callable then ('int' was a built-in function, not a callable type), and user-defined classes were callable only through special-casing in the CALL instruction, built-in types being implemented differently.
- **Quote**: "at the time, type objects were not callable -- e.g. 'int' was not a built-in type but a built-in function that returned an instance of the int object, and the int type was neither easily accessible nor callable.  User-defined classes were of course callable, but this was originally special-cased by the CALL instruction, as these were implemented in a completely different way than built-in types." (line 12)

### beaudry-insight-led-to-new-style-classes
- **What**: The author credits Beaudry with planting the insight that led to metaclasses, then to new-style classes, and the eventual death of classic classes.
- **Quote**: "Don Beaudry is eventually responsible for planting the insight in my head that led first to metaclasses and later to new-style classes and the eventual death of classic classes." (line 12)

### class-attribute-removes-c-requirement
- **What**: In Python 1.5 the author removed the need to write a C extension to use the hook: class creation also checked for a "__class__" attribute on the base class and called it if present.
- **Quote**: "In Python 1.5, I removed the requirement to write a C extension in order to use the Don Beaudry hook. In addition to check for a callable base class type, the class creation code now also checked for an attribute named “__class__” on the base class, and would call this if present." (line 16)

### class-creation-api-three-arguments
- **What**: The lasting contribution of the hook: the class creation function's API (name string, tuple of base classes, namespace dictionary; its return value bound to the class name), carried over unchanged into the 2.2 metaclass machinery.
- **Quote**: "the most lasting contribution of the Don Beaudry hook is the API for the class creation function, which was carried over to the new metaclass machinery in Python 2.2. ... the class creation function is called with three arguments: a string giving the class name, a tuple giving the base classes ..., and a dictionary giving the contents of the namespace ... The return value of the class creation function is assigned to a variable whose name is the class name." (line 18)

### internal-api-became-public
- **What**: What was simply the internal API for creating classes became a public API because the hook reused the same call signature.
- **Quote**: "Originally, this was simply the internal API for creating classes. The Don Beaudry hook used the same call signature and hence it became a public API." (line 20)

### body-executed-before-creation-limits-metaclasses
- **What**: A restriction of the design: the method-definition block is executed before the class creation function is called, so a metaclass cannot influence the initial contents of the namespace the method definitions run in.
- **Quote**: "The most important aspect of this API is that the block containing the method definitions is executed before the class creation function is called. This places certain restrictions on the effectiveness of metaclasses, since a metaclass cannot influence the initial contents of the namespace in which the method definitions are executed." (line 20)

### python-3000-alternative-namespace-mapping
- **What**: Python 3000 lifted that restriction, letting a metaclass provide an alternative mapping object in which the class body is executed; to support this, the metaclass is now specified with keyword argument syntax in the base class list, introduced for this purpose.
- **Quote**: "This was changed in Python 3000, so that now a metaclass can provide an alternative mapping object in which the class body is executed.  In order to support this, the syntax for specifying an explicit metaclass is also changed: it uses keyword argument syntax in the list of base classes, which was introduced for this purpose." (line 22)
