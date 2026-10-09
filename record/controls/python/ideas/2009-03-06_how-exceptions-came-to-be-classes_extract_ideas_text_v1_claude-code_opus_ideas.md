---
note: 2009-03-06_how-exceptions-came-to-be-classes.md
note_dir: texts
note_sha256: fa3e74cfdd5cafe3e669023d523ac9bdb3a65058ffe236ba9438b5db40a87906
title: "How Exceptions Came to be Classes"
author: Guido van Rossum
created: 2009-03-06T09:26:00
ideas: 12
quotes_found: 12/12
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### exceptions-for-error-handling
- **What**: From the start the author wanted Python to handle errors through exceptions.
- **Quote**: "Early on, I knew I wanted Python to use exceptions for error handling." (line 2)

### scheme-to-identify-kinds-of-exceptions
- **What**: Making exceptions work requires some scheme for distinguishing one kind of exception from another.
- **Quote**: "a critical part of making exceptions work is to come up with some kind of scheme for identifying different kinds of exceptions." (line 2)

### exceptions-as-classes-in-modern-languages
- **What**: In modern languages, and in modern Python, exceptions are defined by user-defined classes.
- **Quote**: "In modern languages (including modern Python :-), exceptions are defined in terms of user-defined classes." (line 2)

### early-choice-strings-for-exceptions
- **What**: In early Python the author identified exceptions by strings, which he judges unfortunate, for two reasons: he learned exceptions from Modula-3 (where they are unique tokens), and he introduced exceptions before user-defined classes existed.
- **Quote**: "In early Python however, I chose to identify exceptions by strings. This was unfortunate, but I had two reasons for taking this approach. First, I learned about exceptions from Modula-3, where exceptions are unique tokens. Second, I introduced exceptions before I introduced user-defined classes." (line 2)

### reuse-existing-builtin-type
- **What**: A new built-in object type for exceptions would have cost considerable C coding, so he reused an existing built-in type; strings seemed natural because exceptions carry error messages.
- **Quote**: "as every built-in object type required a considerable coding effort in C, I decided to reuse an existing built-in type. And, since exceptions are associated with error messages, it seemed natural to use strings to represent exceptions." (line 4)

### identity-not-value-semantics
- **What**: He chose semantics where distinct string objects are distinct exceptions even with equal value, so exceptions are referenced by name (object identity) and never by value (string equality), keeping exceptions in different modules independent.
- **Quote**: "I chose semantics where different string objects would represent different exceptions, even if they had the same value ... The idea was that exceptions would always be referenced by their name, which would imply object identity, never by their value, which would require string equality." (line 6)

### modula-3-token-influence
- **What**: The design was influenced by Modula-3, where each exception declaration creates a unique token that can't be confused with another.
- **Quote**: "This approach was influenced by Modula-3’s exceptions, where each exception declaration creates a unique “exception token” that can’t be confused with any other exception token." (line 8)

### premature-optimization-pointer-comparison
- **What**: He also wanted to test exceptions by pointer comparison rather than string value comparison, which he now calls a misguided premature optimization of execution time, rare for him since he usually optimized his own coding time.
- **Quote**: "I think I also wanted to optimize testing for exceptions by using pointer comparisons instead of string value comparisons in a misguided attempt to prematurely optimize execution time (a rare one – I usually optimized for my own coding time!)." (line 8)

### avoid-name-clashes-between-modules
- **What**: The main reason for the identity semantics was worry about name clashes between unrelated exceptions in different modules; the intended convention was to define an exception as a global constant in a module and refer to it by name everywhere it is raised or caught.
- **Quote**: "The main reason however is that I worried about name clashes between unrelated exceptions defined in different modules. I intended the usage pattern to strictly adhere to the convention of defining an exception as a global constant in some module, and then using it by name in all code raising or catching it." (line 8)

### literal-interning-came-later
- **What**: This design predated the automatic interning of certain string literals.
- **Quote**: "(This was also long before certain string literals would be automatically be “interned”.)" (line 8)

### compiler-unifies-literals-breaks-across-modules
- **What**: In practice the byte code compiler unified string literals within a module, so by accident exceptions could be caught by the error-message literal as well as the name; this worked only within a module and broke mysteriously across modules, causing widespread confusion.
- **Quote**: "Early Python users discovered that within the same module, the byte code compiler would unify string literals ... it only worked for code defined in the same module---if one tried to catch exceptions using the exception error message in a different module, it broke mysteriously. Needless to say, this is the sort of thing that causes widespread confusion." (line 10)

### class-exceptions-introduced-1997
- **What**: In 1997 with Python 1.5 he introduced class exceptions, the recommended approach since; string exceptions stayed for legacy use through Python 2.5 and were removed in 2.6.
- **Quote**: "In 1997, with Python 1.5, I introduced class exceptions into the language. Although class exceptions have been the recommended approach ever since, string exceptions were still supported for use by certain legacy applications through Python 2.5. They were finally removed in Python 2.6." (line 12)
