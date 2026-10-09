---
note: 2010-06-23_method-resolution-order.md
note_dir: texts
note_sha256: c16b1a84d50620697db291e8911873a9f9d851ad7d74a919050d4b8933c1b71b
title: "Method Resolution Order"
author: Guido van Rossum
created: 2010-06-23T10:41:00
ideas: 17
quotes_found: 17/17
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### mro-defines-attribute-search-order
- **What**: In languages with multiple inheritance, the Method Resolution Order (MRO) is the order base classes are searched for a method; in Python it also governs lookup of other attributes.
- **Quote**: "the order in which base classes are searched when looking for a method is often called the Method Resolution Order, or MRO. (In Python this also applies to other attributes.)" (line 2)

### mro-trivial-under-single-inheritance
- **What**: MRO only becomes an interesting and subtle problem once multiple inheritance is in play; under single inheritance it is uninteresting.
- **Quote**: "For languages that support single inheritance only, the MRO is uninteresting; but when multiple inheritance comes into play, the choice of an MRO algorithm can be remarkably subtle." (line 2)

### python-had-three-mro-algorithms
- **What**: Python has used three MRO algorithms over time (classic, 2.2 new-style, 2.3 new-style / C3), of which only C3 remains in Python 3.
- **Quote**: "Python has known at least three different MRO algorithms: classic, Python 2.2 new-style, and Python 2.3 new-style (a.k.a. C3). Only the latter survives in Python 3." (line 2)

### classic-mro-depth-first-left-to-right
- **What**: Classic classes resolved methods by a simple depth-first, left-to-right search, returning the first match found.
- **Quote**: "when looking up a method, base classes were searched using a simple depth-first left-to-right scheme.   The first matching object found during this search would be returned." (line 4)

### classic-mro-fails-on-diamond
- **What**: The classic depth-first scheme works for simple cases but breaks under diamond inheritance, where it finds the shared ancestor's method instead of the more specialized override.
- **Quote**: "This scheme works fine for simple cases, but has problems that become apparent when one considers more complicated uses of multiple inheritance.  One problem concerns method lookup under \"diamond inheritance.\"" (line 13)
- **Also at**: line 22

### specialized-override-should-win
- **What**: When a subclass redefines a method inherited through a diamond, the more specialized redefinition is the one that should be called; otherwise the subclass's state is ignored and the program breaks.
- **Quote**: "one can argue that the redefined method C.save() is actually the method that you want to call, since it can be viewed as being \"more specialized\" than the method in A ... if the save() method is being used to save the state of an object, not calling C.save() would break the program since the state of C would be ignored." (line 22)

### new-style-classes-make-diamonds-universal
- **What**: Because all new-style classes inherit from a common base object, every use of multiple inheritance creates a diamond, turning a rare problem into a commonplace one.
- **Quote**: "Although this kind of multiple inheritance was rare in existing code, new-style classes would make it commonplace.   This is because all new-style classes were defined by inheriting from a base class object." (line 24)

### object-methods-make-order-critical
- **What**: Since object defines methods that subtypes sometimes extend (e.g. __setattr__), the resolution order becomes critical so the subtype's override applies.
- **Quote**: "since object defined a number of methods that are sometimes extended by subtypes (e.g., __setattr__()), the resolution order becomes critical." (line 30)

### precompute-and-store-mro
- **What**: For Python 2.2 the MRO was pre-computed at class-definition time and stored as an attribute of the class object, dropping all but the last occurrence of a duplicated class.
- **Quote**: "I adopted a scheme where the MRO would be pre-computed when a class was defined and stored as an attribute of each class object. ... If any class was duplicated in this search, all but the last occurrence would be deleted from the MRO list." (line 32)

### mro-special-case-preserve-first-order
- **What**: The real 2.2 algorithm added a special case that reordered bases to preserve the order in which classes first appeared in the search, departing from the documented algorithm.
- **Quote**: "there was a special case to deal with a situation when two bases classes occurred in a different order in the inheritance list of two different derived classes ... this algorithm tried to preserve the order of classes for bases that appeared first in the search process." (line 34)
- **Also at**: line 39

### documented-wrong-algorithm
- **What**: Van Rossum implemented one algorithm for 2.2 but documented the earlier simpler one, thinking the difference did not matter much; a regret.
- **Quote**: "This is what I implemented for Python 2.2, but I documented the earlier algorithm (naïvely thinking it didn't matter much)." (line 39)

### pedroni-found-inconsistency
- **What**: Samuele Pedroni found that the actual behavior diverged from the documented algorithm, and that inconsistencies arose even outside the known special case, leading to the judgment that the 2.2 MRO was broken.
- **Quote**: "Samuele Pedroni discovered an inconsistency between the documented MRO algorithm and the results that were actually observed in real-code.   Moreover, inconsistencies were occurring even in code that did not fall under the special case observed above." (line 41)

### adopt-c3-linearization
- **What**: After discussion it was decided to replace the 2.2 scheme with the academically published C3 Linearization algorithm from the Dylan paper.
- **Quote**: "it was decided that the MRO adopted for Python 2.2 was broken and that Python should adopt the C3 Linearization algorithm described in the paper \"A Monotonic Superclass Linearization for Dylan\"" (line 41)

### monotonicity-as-the-core-problem
- **What**: The core defect of the 2.2 algorithm was monotonicity: once A is determined to precede B, no later rule should force B before A, or the hierarchy is undefined and should be rejected.
- **Quote**: "if you have already determined that class A should be checked before class B, then you should never encounter a situation that requires class B to be checked before class A (otherwise, the result is undefined and the inheritance hierarchy should be rejected)." (line 45)
- **Also at**: line 43

### inheritance-defines-ordering-rules
- **What**: Each inheritance relationship imposes simple ordering rules (a subclass before its base; earlier-listed bases before later ones), and C3 finds a monotonic ordering satisfying all of them or fails.
- **Quote**: "if you write down all of the ordering rules imposed by inheritance relationships in a complex class hierarchy, the algorithm will determine a monotonic ordering of the classes that satisfies all of them.   If such an ordering can not be determined, the algorithm will fail." (line 45)
- **Also at**: line 43

### c3-rejects-inconsistent-hierarchies
- **What**: A consequence of adopting C3 is that Python now rejects any inheritance hierarchy with an inconsistent ordering of base classes rather than resolving it silently.
- **Quote**: "Python will now reject any inheritance hierarchy that has an inconsistent ordering of base classes." (line 47)

### rejection-matches-zen-errors-not-silent
- **What**: Rejecting inconsistent hierarchies is aligned with the Zen of Python's rule that errors should never pass silently.
- **Quote**: "This, of course, matches the Zen of Python's \"errors should never pass silently\" rule." (line 47)
