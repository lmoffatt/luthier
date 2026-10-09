---
note: 2009-03-03_how-everything-became-an-executable-statement.md
note_dir: texts
note_sha256: 15bb85def6d1bf443a136ac02f6938f3feb27a2ab9ab5bd04dd174d8239f5b2d
title: "How Everything Became an Executable Statement"
author: Guido van Rossum
created: 2009-03-03T12:02:00
ideas: 5
quotes_found: 5/5
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### everything-is-an-executable-statement
- **What**: Every part of Python is an executable statement, including function and class definitions, so any statement can appear anywhere in a program.
- **Quote**: "every part of the language is an executable statement, including function and class definitions.  That means that any statement can appear anywhere in a program." (line 2)

### early-grammar-restricted-declarative-elements
- **What**: In a very early version of the grammar, declarative-flavored elements like import statements and function definitions were allowed only at the top level of a module or script; adding classes, van Rossum judged this too restrictive.
- **Quote**: "grammar elements that had a “declarative flavor”, like import statements and function definitions, were allowed only at the top level in a module or script ... However, at the time I was adding support for classes, I decided that this was too restrictive." (line 4)

### class-body-as-arbitrary-code
- **What**: The reasoning began with allowing regular variable assignments in a class body, not just function declarations, then extended to allowing arbitrary executable code anywhere.
- **Quote**: "Rather than defining the class body as a series of function declarations only, it seemed to make sense to also allow regular variable assignments there. However, if I was going to allow that, why not go one step further and allow arbitrary executable code?" (line 6)

### uniform-statements-simplify-grammar-and-compiler
- **What**: Allowing statements anywhere simplified the grammar, since all uses of statements could share one grammar rule and the compiler could use the same byte code generation function for all of them.
- **Quote**: "this enabled a simplification of the grammar, since now all uses of statements (whether indented or not) could share the same grammar rule, and hence the compiler could use the same byte code generation function for all of them." (line 6)

### syntax-allows-what-semantics-did-not-support
- **What**: The feature let the grammar accept constructs the semantics did not support, so e.g. nested functions could be written even though Python lacked nested scopes, often operating in broken or unexpected ways; many such cases were later fixed, with nested function definitions working more sanely in Python 2.1.
- **Quote**: "the Python grammar technically allowed users to write things such as nested functions even though the underlying semantics of Python didn't support nested scopes. ... many of these "broken" features have been fixed.  For example, nested function definitions only began to work more sanely in Python 2.1." (line 8)
