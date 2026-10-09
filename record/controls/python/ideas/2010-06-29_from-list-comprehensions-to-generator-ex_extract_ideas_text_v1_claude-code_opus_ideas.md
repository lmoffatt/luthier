---
note: 2010-06-29_from-list-comprehensions-to-generator-expressions.md
note_dir: texts
note_sha256: 42deca8eb880acaba0a8f190881cbb5cac016d25d3fe6bf1fea0b416498ebda1
title: "From List Comprehensions to Generator Expressions"
author: Guido van Rossum
created: 2010-06-29T08:39:00
ideas: 19
quotes_found: 19/19
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### list-comprehensions-from-set-notation
- **What**: List comprehensions are a Pythonic interpretation of the mathematical set-builder notation.
- **Quote**: "they are a Pythonic interpretation of a well-known notation for sets used by mathematicians" (line 2)

### no-universal-set-in-python
- **What**: The mathematical set-builder form implies a universal set understood from context; Python has no such concept, and at the time (2.0) no sets at all, which forced a different notation.
- **Quote**: "In math, this form implies a universal set that is understood by the reader ... In Python, there is no concept of a universal set, and in Python 2.0, there were no sets." (line 4)

### comprehension-syntax
- **What**: The chosen Python notation produces a list of the values of a sequence, selected by an optional predicate and mapped by a function, with multiple for-clauses allowed for nested loops.
- **Quote**: "[f(x) for x in S if P(x)] This produces a list containing the values of the sequence S selected by the predicate P and mapped by the function f." (line 7)
- **Open**: nested for-clauses are allowed but "rarely used though, since it typically maps a multi-dimensional entity to a one-dimensional list" (line 8).

### comprehensions-vs-map-filter
- **What**: List comprehensions are an alternative to map() and filter(); on toy cases map/filter look more compact, but on realistic cases the comprehension wins.
- **Quote**: "List comprehensions provide an alternative to using the built-in map() and filter() functions." (line 10)

### lambda-too-verbose-disagreement
- **What**: Some argue the real problem is that lambda is too verbose and a terser anonymous-function syntax would make map() more attractive; Guido disagrees, preferring the comprehension's readability as expression complexity grows.
- **Quote**: "It has been argued that the real problem here is that Python's lambda notation is too verbose ... Personally, I disagree—I find the list comprehension notation much easier to read than the functional notation" (line 12)

### comprehensions-faster-no-stack-frame
- **What**: Comprehensions run faster than map+lambda because a lambda call creates a new stack frame while the comprehension's expression is evaluated without one.
- **Quote**: "the list comprehension executes much faster ... because calling a lambda function creates a new stack frame while the expression in the list comprehension is evaluated without creating a new stack frame." (line 12)

### generator-expressions-lazy
- **What**: Generator expressions, added in 2.4 and enabled by generators, represent a sequence of results without building a concrete list, saving memory for large collections.
- **Quote**: "a similar notation that represents a sequence of results without turning it into a concrete list. The new feature is called a "generator expression"." (line 14)
- **Also at**: line 16

### genexp-syntax-stricter-than-listcomp
- **What**: In Python 2 a list comprehension could take a bare comma sequence after 'in', but a generator expression could not, requiring parentheses.
- **Quote**: "in Python 2, this is a valid list comprehension: ... However this is not a valid generator expression" (line 18)

### design-factors-four
- **What**: Four factors governed the design of these notations: backwards compatibility, avoiding ambiguity, the desire for equivalence, and evolution of the language.
- **Quote**: "The factors affecting the design were backwards compatibility, avoiding ambiguity, the desire for equivalence, and evolution of the language." (line 28)

### bare-sequence-after-in-from-for-loop
- **What**: The original explicit for-loop had no ambiguity after 'in' because a colon always followed, so Guido decided looping over known values shouldn't require parentheses.
- **Quote**: "if you wanted to loop over a bunch of known values, you shouldn't be bothered with having to put parentheses around them." (line 28)

### algol-60-inspiration
- **What**: The bare comma-separated for-loop reminded Guido of Algol-60's for-loop form.
- **Quote**: "This also reminded me of Algol-60, where you can write: for i := 1, 2, 3 do Statement" (line 28)
- **Open**: a wish that Python for-loops could iterate over multiple sequences as Algol-60's step-until could: "In retrospect it would have been cool if Python for-loops had the ability to iterate over multiple sequences as well. Alas..." (line 32)

### genexp-ambiguity-parentheses-not-part-of-syntax
- **What**: The parentheses around a generator expression belong to the surrounding call, not to the genexp syntax, so a bare comma sequence after 'in' would have two interpretations.
- **Quote**: "the parentheses around a generator expression are not technically part of the generator expression syntax ... there would be two interpretations" (line 36)

### refuse-to-guess-ambiguity
- **What**: Faced with the ambiguity, they chose not to guess and required a single expression after the genexp's 'in', while not breaking existing list-comprehension code.
- **Quote**: "we decided not to guess in this case, and the generator comprehension was required to have a single expression ... after its 'in' keyword. But at the time we didn't want to break existing code using the (already hugely popular) list comprehensions." (line 44)

### listcomp-equivalent-to-list-of-genexp
- **What**: In Python 3 they decided a list comprehension should be fully equivalent to list() applied to the corresponding generator expression, so they gave list comprehensions the stricter genexp syntax.
- **Quote**: "we wanted the list comprehension ... to be fully equivalent to the following expansion using the built-in list() function applied to a generator expression ... Thus we decided to use the slightly more restrictive syntax of generator expressions for list comprehensions as well." (line 46)

### loop-variable-leak-dirty-secret
- **What**: In Python 2 a list comprehension leaks its loop control variable into the surrounding scope, an artifact of the original implementation, an intentional compromise for speed that occasionally stung people.
- **Quote**: "the list comprehension "leaks" the loop control variable into the surrounding scope ... It started out as an intentional compromise to make list comprehensions blindingly fast ... it definitely stung people occasionally." (line 52)
- **Also at**: lines 56

### genexp-needs-own-frame
- **What**: Generator expressions cannot leak the variable because they run in a separate execution frame, which made them less efficient than list comprehensions in Python 2.
- **Quote**: "Generator expressions are implemented using generators, whose execution requires a separate execution frame. Thus, generator expressions ... were less efficient than list comprehensions." (line 56)

### python3-fix-leak-via-genexp-strategy
- **What**: Python 3 fixed the leak by implementing list comprehensions with the same strategy as generator expressions, so the loop variable only shadows the outer one.
- **Quote**: "in Python 3, we decided to fix the "dirty little secret" of list comprehensions by using the same implementation strategy as for generator expressions ... the 'x' in the list comprehension temporarily shadows but does not override the 'x' in the surrounding scope." (line 58)

### python3-both-faster-no-gap
- **What**: Thanks to general Python 3 speed work, both forms became faster than in Python 2 and the speed difference between them disappeared, removing the performance argument for the leak.
- **Quote**: "both list comprehensions and generator expressions in Python 3 are actually faster than they were in Python 2! (And there is no longer a speed difference between the two.)" (line 60)

### set-and-dict-comprehensions
- **What**: Python 3 also supports set and dict comprehensions as straightforward extensions of the list comprehension idea.
- **Quote**: "Python 3 also supports set comprehensions and dictionary comprehensions. These are straightforward extensions of the list comprehension idea." (line 62)
