---
note: 2009-02-18_adding-support-for-user-defined-classes.md
note_dir: texts
note_sha256: 004c02bc7f9bbfa5457852abd187da1639fef5a0cae6daab1e6fab317b42ca06
title: "Adding Support for User-defined Classes"
author: Guido van Rossum
created: 2009-02-18T11:25:00
ideas: 28
quotes_found: 28/28
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

I have enough context. Here is the extraction.

---
generated_by: extract_ideas_text_v1
mode: editor
---

## Ideas

### classes-added-late-but-pre-release
- **What**: Classes were not part of Python's earliest design; they were added late in the first year of development at CWI, yet before the first public release.
- **Quote**: "classes were added late during Python's first year of development at CWI, though well before the first public release" (line 2)

### c-centric-object-implementation
- **What**: Python is a stack-based bytecode interpreter written in C, with primitive types in C; objects are built from C structures and function pointers because C has no direct object support.
- **Quote**: "Python is implemented in C as a classic stack-based byte code interpreter or "virtual machine" along with a collection of primitive types also implemented in C. The underlying architecture uses "objects" throughout, but since C has no direct support for objects, they are implemented using structures and function pointers." (line 4)
- **Also at**: line 6

### type-as-table-of-function-pointers
- **What**: An object type is a statically allocated structure of function pointers, one per standard operation; optional operations may be left NULL, in which case the VM errors or supplies a default.
- **Quote**: "An object type is then represented by a statically allocated structure containing a series of function pointers, one for each standard operation... some operations are optional, and the object type may leave the function pointer NULL if it chooses not to implement that operation. In this case, the virtual machine either generates a run-time error or, in some cases, provides a default implementation" (line 4)

### type-structure-as-runtime-object
- **What**: Python's introspection comes from making the type structure itself available at run-time as an object like any other.
- **Quote**: "Python's unique approach to introspection comes from its ability to make the type structure itself available at run-time as an object like all others." (line 4)
- **Also at**: line 20

### objects-defined-in-python-the-motivation
- **What**: Siebren van der Zee suggested Python should allow class definitions like C++ so that objects could be implemented in Python, not only in C; this motivated user-defined classes.
- **Quote**: "I believe my colleague Siebren van der Zee was the first to suggest that Python should allow class definitions similar to those in C++ so that objects could also be implemented in Python." (line 6)
- **Open**: the author marks the attribution as a belief ("I believe")

### instance-as-classref-plus-dict
- **What**: The chosen design for user-defined objects is the simplest possible: an instance is a built-in object holding a class reference and an "instance dictionary" of instance variables.
- **Quote**: "I settled on the simplest possible design; a scheme where objects were represented by a new kind of built-in object that stored a class reference pointing to a "class object" shared by all instances of the same class, and a dictionary, dubbed the "instance dictionary", that contained the instance variables." (line 8)

### class-dictionary-holds-methods
- **What**: The class object holds what is shared across instances, chiefly methods, in a "class dictionary" keyed by method name; again the simplest possible design.
- **Quote**: "the set of methods of a class were stored in a dictionary whose keys are the method names. This, I dubbed the class dictionary." (line 10)

### multiple-inheritance-because-it-was-cheap
- **What**: Class objects store references to base classes for inheritance; being naïve about classes but aware of C++'s recent multiple inheritance, the author supported a simple-minded multiple inheritance since he was adding inheritance anyway.
- **Quote**: "as long as I was going to support inheritance, I might as well support a simple-minded version of multiple inheritance. Thus, every class object could have one or more base classes." (line 10)

### attribute-lookup-by-dictionary-search
- **What**: The mechanics are plain dictionary operations: setting a variable updates the instance dictionary; a lookup checks the instance dictionary, then the class dictionary, then the base classes' dictionaries.
- **Quote**: "Whenever changes are made to instance or class variables, those changes are simply reflected in the underlying dictionary object... lookups are performed in the class dictionary and then in the class dictionaries of each of the base classes." (line 12)

### depth-first-left-to-right-mro
- **What**: Method resolution walks the class dictionary then each base class recursively, stopping at the first hit: the depth-first, left-to-right rule, the default MRO in most versions of Python.
- **Quote**: "This is commonly referred to as the depth-first, left-to-right rule, and has been the default method resolution order (MRO) used in most versions of Python. More modern releases have adapted a more sophisticated MRO" (line 14)
- **Open**: the later, more sophisticated MRO is deferred to a later blog and not described here

### no-conformance-checking
- **What**: To keep things simple, method lookup does no error or conformance checking; an overriding method need not match the base method's arguments, and the first method found is called with whatever arguments the user supplied.
- **Quote**: "Python performs no advanced error checking or conformance checking when locating methods... no checks are performed to make sure that the redefined method has the same number of arguments... The above method resolution algorithm merely returns the first method found and calls it with whatever arguments the user has supplied." (line 16)

### class-variables-fall-out
- **What**: Because the class dictionary can hold any object, storing non-method objects there yields class variables, shared by all instances; this feature falls out of the design rather than being designed in.
- **Quote**: "there was no inherent reason why other kinds of objects couldn't be placed there as well. Thus, if objects such as integers or strings are stored in the class dictionary, they become what are known as class variables" (line 18)

### dynamic-modifiability-of-classes-and-objects
- **What**: The simple implementation makes classes first-class, introspectable objects and allows dynamic modification: methods added or changed by updating the class dictionary take immediate effect on all instances and subclasses; instances too can gain, change or lose variables.
- **Quote**: "it also makes it possible to modify a class dynamically... methods can be added or modified by simply updating the class dictionary after a class object has already been created!... individual objects can be modified dynamically by adding, modifying, and deleting instance variables" (line 20)

### more-permissive-than-smalltalk
- **What**: Python's objects are more permissive than Smalltalk's, which restricts an object's attributes to those fixed at creation; the author learned this only later.
- **Quote**: "a feature that I later learned made Python's implementation of objects more permissive than that found in Smalltalk which restricts the set of attributes to those specified at the time of object creation" (line 20)

### no-separate-method-syntax
- **What**: A major design constraint was to not add a method syntax different from function syntax, because refactoring the grammar and bytecode generator to treat the similar cases differently felt like a huge task.
- **Quote**: "A major design constraint was that I didn't want to add syntax for methods that differed from the syntax for functions. Refactoring the grammar and the byte code generator to handle such similar cases differently felt like a huge task." (line 24)

### implicit-instance-variables-impossible
- **What**: The author first hoped to emulate C++'s implicit instance variables, where a method's unqualified reference resolves to the instance variable; this proved impossible in a language without variable declarations, since instance and local variables could not be elegantly distinguished.
- **Quote**: "it quickly became clear that such an approach would be impossible because there was no way to elegantly distinguish instance variables from local variables in a language without variable declarations." (line 34)
- **Also at**: lines 24, 36, 38

### assignment-always-creates-in-first-dict
- **What**: Variable reference searches locals, globals, built-ins in order, but assignment does not search: it always creates or replaces in the first dictionary (locals), with a per-variable global declaration as the only override. This is why putting the instance dictionary first breaks assignment to locals, and swapping the order merely reverses the problem.
- **Quote**: "Python's assignment doesn't search for the variable name in the dictionaries, but simply adds or replaces the variable in the first dictionary in the search order, normally the local variables... making the instance dictionary the first item in the search order would make it impossible to assign to local variables in a method." (line 40)
- **Also at**: lines 42, 48

### assign-if-exists-has-bootstrap-problem
- **What**: Changing assignment to target an existing instance variable and otherwise a local fails too, because of a bootstrap problem: there would be no way for an instance variable to be created the first time.
- **Quote**: "Changing the semantics of assignment to assign to an instance variable if one already existed and to a local otherwise wouldn't work either, since this would create a bootstrap problem: how does an instance variable get created initially?" (line 50)

### rejected-declarations-and-sigils
- **What**: Requiring explicit instance-variable declarations was rejected because the author had gotten this far with no declarations and they would be needed almost everywhere in a class; lexically distinct instance variables (a sigil like Ruby's @, or a naming convention) also did not appeal to him, then or now.
- **Quote**: "Requiring a special specification for instance variables, on the other hand, would have to be used almost everywhere in a class. Another possible solution would have been to make instance variables lexically distinct... Neither of these appealed to me (and they still don't)." (line 50)

### explicit-self-the-decision
- **What**: The author gave up implicit instance-variable references and made explicit reference the only way, following C++'s this->foo; rather than making the current object a keyword, he made it the first named argument to a method, so instance variables are always attributes of that argument.
- **Quote**: "I decided to make such explicit references the only way to reference instance variables... rather than making the current object ("this") a special keyword, I would simply make "this" (or its equivalent) the first named argument to a method. Instance variables would just always be referenced as attributes of that argument." (line 52)
- **Also at**: line 54

### explicit-self-removes-special-cases
- **What**: With explicit references, no special method-definition syntax and no complicated variable-lookup semantics are needed: a method is just a function whose first argument, by convention named "self," is the instance.
- **Quote**: "With explicit references, there is no need to have a special syntax for method definitions nor do you have to worry about complicated semantics concerning variable lookup. Instead, one simply defines a function whose first argument corresponds to the instance, which by convention is named "self."" (line 54)
- **Also at**: line 61

### modula-3-precedent
- **What**: The self approach resembles Modula-3, which also gave Python its import and exception-handling syntax; Modula-3's record types hold function-pointer members with sugar so that x.m(args) equals f(x, args), matching the typical object implementation and letting instance variables equate to attributes of the first argument.
- **Quote**: "This approach resembles something I had seen in Modula-3, which had already provided me with the syntax for import and exception handling... calling x.m(args) is equivalent to calling f(x, args). This matches the typical implementation of objects and methods" (line 59)

### dunder-special-method-names
- **What**: Rather than new syntax for special class methods like initializers and destructors, the user implements methods with special names such as __init__ and __del__; the underscore convention was taken from C, where leading-underscore identifiers are reserved and often special (e.g. __FILE__).
- **Quote**: "I decided that these features could be handled by simply requiring the user to implement methods with special names such as __init__, __del__, and so forth. This naming convention was taken from C where identifiers starting with underscores are reserved by the compiler and often have special meaning" (line 61)
- **Also at**: lines 79, 81

### class-body-as-executed-namespace
- **What**: To reuse existing code, the class body is interpreted as statements executed in a new namespace; its resulting dictionary of locals initializes the class dictionary. Concretely the body becomes an anonymous function returning its local dictionary, passed to a helper that creates the class object, which is then bound to the class name in the surrounding scope.
- **Quote**: "it made sense to me to simply interpret the class body as a series of statements that were executed in a new namespace. The dictionary of this namespace would then be captured and used to initialize the class dictionary and create a class object." (line 71)

### any-statements-in-class-body
- **What**: Because the class body is just executed statements, any valid Python statements may appear in it, which surprises users; this followed from keeping the syntax simple and not artificially limiting what might be useful.
- **Quote**: "Users are often surprised to learn that any sequence of valid Python statements can appear in a class body. This capability was really just a straightforward extension of my desire to keep the syntax simple as well as not artificially limiting what might possibly be useful." (line 71)

### callable-class-no-new-operator
- **What**: Unlike C++ and Java's "new" operator, Python makes the class object itself callable for instantiation, the minimal solution requiring no new syntax, since the parser does not care what kind of object is called; each class is thereby its own factory, anticipating the later factory-function pattern.
- **Quote**: "making the class object itself callable was the right, "minimal" solution, requiring no new syntax... what I had done was simply to turn each class into its own factory." (line 73)

### special-methods-map-c-function-pointers
- **What**: The special-method technique also lets user classes redefine Python's operators: the C-level function pointers (get attribute, add, call) are mapped to special method names (__getattr__, __add__, __call__), with a direct correspondence to the function-pointer tables defined when implementing objects in C.
- **Quote**: "I mapped the various function pointers to special method names such as __getattr__, __add__, and __call__. There is a direct correspondence between these names and the tables of function pointers one has to define when implementing new Python objects in C." (line 81)

### new-style-classes-constrain-dict
- **What**: New-style classes later required controlling changes to a class's __dict__: a class can still be modified dynamically, but through attribute assignment rather than by using the class __dict__ directly.
- **Quote**: "Eventually, new-style classes made it necessary to control changes to the class __dict__; you can still dynamically modify a class, but you must use attribute assignment rather than using the class __dict__ directly." (line 84)
