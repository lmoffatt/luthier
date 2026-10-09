---
note: 2013-11-10_the-story-of-none-true-and-false-and-an-explanatio.md
note_dir: texts
note_sha256: 4bccd9cf81a2e95a7f310315919361a131719db7389b0ca00528e5adbd4e405c
title: "The story of None, True and False (and an explanation of literals, keywords and builtins thrown in)"
author: Guido van Rossum
created: 2013-11-10T14:40:00
ideas: 19
quotes_found: 18/19
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### keyword-is-identifier-shaped-but-a-token
- **What**: A keyword (reserved word) looks like an identifier but the parser treats it as a token of the language; an identifier is letters, digits and underscores not starting with a digit.
- **Quote**: "A keyword, in the context of defining the syntax of a language, also known as a reserved word, is something that looks like an identifier in the language, but from the parser's point of view act like a token of the language." (line 13)

### keyword-cannot-name-a-variable
- **What**: The defining property of a keyword is that it cannot be used to name a variable, function, class, etc.
- **Quote**: "The important thing to remember about keywords is that a keyword cannot be used to name a variable (or function, class, etc.)." (line 15)

### literal-describes-a-constant-value
- **What**: A literal is an element of an expression that describes a constant value, recognized by the parser, with subtle parsing rules.
- **Quote**: "A literal, on the other hand, is an element of an expression that describes a constant value... Literals are recognized by the parser, and the exact rules for how literals are parsed are often quite subtle." (line 17)

### constant-versus-literal
- **What**: A constant is distinct from a literal: an all-caps identifier like MAX_LEVELS is a convention the parser neither knows nor enforces, while 15 is a literal.
- **Quote**: "the all-caps form of the name suggests to the reader that it is probably not changed anywhere in the code... but this is just a convention, and the Python parser doesn't know about that convention, nor does it enforce it." (line 46)

### assignment-target-must-be-a-variable
- **What**: The left-hand side of an assignment must be a variable; a literal is not one. The definition of variable is complex, covering d[k], (a, b), foo.bar but not f(), () or 42, and is shared with the del statement.
- **Quote**: "the left-hand side of the assignment operator (=) must be a variable, and a literal is not a variable. (The exact definition of variable is complex, since some things that look like expressions are also considered to be variables, such as d[k], (a, b), and foo.bar -- but not f() or () or 42." (line 51)

### none-as-singleton-for-absence
- **What**: None is a singleton object used throughout the language and library to represent the absence of some other value.
- **Quote**: "None is a singleton object (meaning there is only one None), used in many places in the language and library to represent the absence of some other value." (line 55)

### builtins-are-ordinary-names-to-the-parser
- **What**: Originally None, like built-in types and exceptions, was just a built-in name; the parser gives these no special knowledge and treats them as identifiers looked up at interpretation time, producing the same parse tree as any name.
- **Quote**: "The parser had no special knowledge of None -- just like it doesn't have special knowledge of built-in types like int, float or str... All of these are treated by the parser as identifiers, and when your code is being interpreted they are looked up just like any other names" (line 55)

### literals-parse-differently-from-names
- **What**: Numeric and string literals produce a different parse tree from names, so `<name> = <name>` is accepted either way round while `<literal> = <name>` is rejected.
- **Quote**: "the parser treats numeric and string literals as different from identifiers... the first three will still be accepted by the parser (<name> = <name>), while the swapped version of the second set will be rejected (<literal> = <name> is invalid)." (line 67)

### builtins-are-reassignable
- **What**: Because built-ins are ordinary names, code can reassign them (e.g. `int = float`), which lets one write confusing code.
- **Quote**: "if you really want to mess with your readers, you can write code that reassigns built-ins" (line 69)

### allowing-builtin-reassignment-for-consistency-and-evolution
- **What**: Assignment to built-in names is allowed by design, for reasons of consistency and the evolution of the language; nobody can list all built-ins, and forbidding their use as names would surprise programmers.
- **Quote**: "The answer is subtle, and has to do with consistency and evolution of the language." (line 80)

### adding-a-builtin-must-not-break-existing-code
- **What**: Adding a new built-in (e.g. `bytes` in 2.6) must not invalidate existing code that used that name as a variable; such code stays valid.
- **Quote**: "In Python 2.6, we added a built-in function named 'bytes'... Should your code now be considered invalid? There's no reason for that, and in fact your code will be fine." (line 91)

### reserved-words-impose-a-global-cost
- **What**: Every reserved word must be known by everyone using Python, since it can never be used as a name anywhere; therefore the list is kept small and new keywords are added reluctantly.
- **Quote**: "everyone using Python has to know about all the reserved words in the language... For this reason, we try to keep the list of reserved words small, and the core developers hem and haw a lot before adding a new reserved word" (line 93)

### new-keywords-kill-or-reshape-features
- **What**: Many proposed features were killed or modified because they would need a new keyword; adding one triggers a deprecation campaign a release ahead, with `from __future__ import` as an opt-in.
- **Quote**: "many proposed new features have been killed because they would require a new keyword; others have been modified to avoid that need." (line 95)

### new-builtins-are-cheap-to-add
- **What**: Unlike keywords, new built-ins don't break working code, so adding them is cheap; the only price is a joker redefining one, which Guido judges minor among the many ways to write unreadable code.
- **Quote**: "at least we don't have to worry about breaking working code by merely adding something to the language. The (small) price we pay for this is the possibility that some joker intentionally redefines a built-in" (line 97)

### none-made-keyword-for-social-reasons
- **What**: None was eventually made a reserved word for mostly social reasons: it is so central that users were horrified assignment to it was allowed; a secondary concern was that evaluating None was slow, needing two dictionary lookups.
- **Quote**: "Why did we eventually make None a reserved word? Frankly, the reasons were perhaps mostly social... None is so central to using Python that you really can't be using Python without knowing about None." (line 99)
- **Open**: Whether the performance concern (two dictionary lookups making None slow) was actually founded is left uncertain.

### none-keyword-decision-had-no-downside
- **What**: Making None a keyword was decided because there was no downside (no code assigns to it) and it might speed up code a little or catch rare typos; the one-time cost to parser and docs was small.
- **Quote**: "In the end we decided that there was no downside to making None a keyword (there is no code that actually assigns to it) and it might make some code a tiny bit faster, or catch rare typos." (line 101)

### true-false-introduced-as-builtins-not-keywords
- **What**: True and False had to be introduced as built-in constants rather than keywords because people had defined their own True/False constants, and backward compatibility (including running on earlier Python versions) forced that choice.
- **Quote**: "we definitely did not want to break any packages that were defining their own True and False constants... essentially our hand was forced in this case, and we had to introduce True and False as built-in constants, not as keywords." (lines 103, 105)

### true-false-became-keywords-in-python-3
- **What**: Once defining one's own True/False became frowned upon, Python 3's cleanup made True and False keywords by analogy to None.
- **Quote**: "by the time Python 3 came around, when we looked at opportunities for cleaning up the language, we found that it was logical to make True and False keywords, by analogy to None." (line 105)

### none-true-false-are-both-keywords-and-literals
- **What**: None/True/False are both keywords (how the parser recognizes them) and literals (their role in expressions, standing for constant values).
- **Quote**: "My answer is that they are both. They are keywords because that's how the parser recognizes them. They are literals because that's their role in expressions and because they stand for constant values." (line 109)
- **Open**: Whether constructs like `{'foo': 42}` are literals is left unsettled; Guido would prefer another name, noting the reference calls these "displays".
