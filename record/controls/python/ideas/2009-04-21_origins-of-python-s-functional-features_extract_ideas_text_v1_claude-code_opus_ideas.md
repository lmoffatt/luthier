---
note: 2009-04-21_origins-of-python-s-functional-features.md
note_dir: texts
note_sha256: fdd603980ceb35f01ce430233919fc44d008664d536136c9fa1407758da5380a
title: "Origins of Python's 'Functional' Features"
author: Guido van Rossum
created: 2009-04-21T11:05:00
ideas: 20
quotes_found: 19/20
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### python-not-functional-despite-first-class-functions
- **What**: Van Rossum did not consider Python a functional language or heavily influenced by functional languages, even though he had made functions first-class objects; he came from imperative languages.
- **Quote**: "I have never considered Python to be heavily influenced by functional languages... although I had made functions first-class objects, I didn't view Python as a functional programming language." (line 2)
- **Also at**: lines 32, 74

### user-demand-drove-list-and-function-features
- **What**: The push to do more with lists and functions came from users, not from a functional vision of the language.
- **Quote**: "earlier on, it was clear that users wanted to do much more with lists and functions." (line 2)
- **Also at**: line 49

### mapping-over-lists-as-common-operation
- **What**: Mapping a function over each element of a list to build a new list was a common operation that users wrote by hand with a loop.
- **Quote**: "A common operation on lists was that of mapping a function to each of the elements of a list and creating a new list." (line 4)

### lisp-scheme-users-reimplemented-builtins
- **What**: Because Lisp and Scheme provided such operations as built-ins, users from those languages reimplemented comparable functionality in Python.
- **Quote**: "In functional languages such as Lisp and Scheme, operations such as this were provided as built-in functions of the language. Thus, early users familiar with such languages found themselves implementing comparable functionality in Python." (line 14)

### dislike-of-separate-named-function
- **What**: Many users disliked having to define the operation applied to list elements as a wholly separate named function.
- **Quote**: "many people didn't like the fact that you to define the operation that you were applying to the list elements as a completely separate function." (line 28)

### no-anonymous-functions-in-python
- **What**: Although functions were first-class, Python lacked any mechanism for creating anonymous functions, unlike Lisp/Scheme's on-the-fly lambda.
- **Quote**: "Although Python made functions first-class objects, it didn't have any similar mechanism for creating anonymous functions." (line 32)

### exec-based-anonymous-function-hacks
- **What**: Before lambda, users (Mark Lutz, then Tim Peters) proposed building anonymous functions from code strings processed through exec; Van Rossum reports their proposals.
- **Quote**: "Mark Lutz... posted some code for a function that created functions using exec." (line 34)
- **Also at**: line 44

### code-strings-via-exec-seen-as-hacky
- **What**: Specifying anonymous functions as code strings manually processed through exec seemed hacky, motivating a proper mechanism.
- **Quote**: "it seemed pretty \"hacky\" to be specifying anonymous functions as code strings that you had to manually process through exec." (line 49)

### addition-of-map-filter-reduce-and-lambda
- **What**: In January 1994 map(), filter(), and reduce() were added to the standard library and the lambda operator was introduced for anonymous functions as expressions.
- **Quote**: "the map(), filter(), and reduce() functions were added to the standard library. In addition, the lambda operator was introduced for creating anonymous functions (as expressions)..." (line 49)

### features-were-contributed-code
- **What**: These functional additions were a significant early chunk of contributed code, by Amrit Prem.
- **Quote**: "These additions represented a significant, early chunk of contributed code." (line 54)

### unhappy-with-lambda-terminology
- **What**: Van Rossum was never happy with the "lambda" terminology but adopted it for lack of a better, obvious alternative, following the contributor's choice.
- **Quote**: "I was never all that happy with the use of the \"lambda\" terminology, but for lack of a better and obvious alternative, it was adopted for Python." (line 56)

### big-changes-required-less-discussion-then
- **What**: At the time, big changes required much less discussion than later, which Van Rossum frames as both good and bad.
- **Quote**: "at the time big changes required much less discussion than nowadays, for better and for worse." (line 56)

### lambda-only-a-syntactic-tool
- **What**: Lambda was intended only as a syntactic tool for defining anonymous functions, not a full functional construct.
- **Quote**: "Lambda was really only intended to be a syntactic tool for defining anonymous functions." (line 58)

### terminology-raised-unmet-expectations
- **What**: The lambda terminology led users from functional languages to expect matching semantics and advanced features, which Python's implementation lacked.
- **Quote**: "the choice of terminology had many unintended consequences... they found Python's implementation to be sorely lacking in advanced features." (line 58)

### lambda-could-not-reference-enclosing-scope
- **What**: A subtle problem: a lambda expression could not refer to variables in the surrounding scope, breaking code that relied on it.
- **Quote**: "a subtle problem with lambda is that the expression supplied couldn't refer to variables in the surrounding scope." (line 58)

### default-argument-workaround
- **What**: Workarounds existed but counter-intuitively required setting default arguments to pass hidden arguments into the lambda.
- **Quote**: "There were workarounds to this problem, but they counter-intuitively involved setting default arguments and passing hidden arguments into the lambda expression." (line 64)

### closures-as-correct-solution
- **What**: The correct solution was for inner functions to implicitly carry references to referenced local variables of the enclosing scope, i.e. closures, an essential aspect of functional languages; added only in Python 2.2 (importable from the future in 2.1).
- **Quote**: "The \"correct\" solution to this problem was for inner functions to implicitly carry references to all of the local variables in the surrounding scope that are referenced by the function. This is known as a \"closure\"..." (line 70)

### map-filter-reduce-superseded-by-comprehensions
- **What**: The map, filter, and reduce functions that originally motivated lambda were largely superseded by list comprehensions and generator expressions; reduce was removed from built-ins in Python 3.0, while lambda, map and filter stay.
- **Quote**: "the map, filter, and reduce functions that originally motivated the introduction of lambda and other functional features have to a large extent been superseded by list comprehensions and generator expressions." (line 72)

### closures-enabled-other-advanced-features
- **What**: Though Python was not envisioned as functional, closures proved useful for developing other advanced features such as new-style classes and decorators.
- **Quote**: "the introduction of closures has been useful in the development of many other advanced programming features. For example, certain aspects of new-style classes, decorators, and other modern features rely upon this capability." (line 74)

### dynamism-precludes-functional-optimizations
- **What**: Python still lacks features of "real" functional languages, such as tail-recursion optimization; its extremely dynamic nature makes compile-time optimization like Haskell's or ML's impossible, and Van Rossum accepts that.
- **Quote**: "because Python's extremely dynamic nature, it is impossible to do the kind of compile-time optimization known from functional languages like Haskell or ML. And that's fine." (line 76)
