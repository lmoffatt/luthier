---
note: 2013-11-11_the-history-of-bool-true-and-false.md
note_dir: texts
note_sha256: 3ec5490b2e89c086bde7136c646b6f0607e4d44a4e422a7f3593431c55c66ced
title: "The history of bool, True and False"
author: Guido van Rossum
created: 2013-11-11T16:29:00
ideas: 6
quotes_found: 6/6
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### true-false-not-reserved-words
- **What**: When True and False were introduced, they were deliberately not made reserved words; Guido notes he was writing up the reasons for this choice.
- **Quote**: "Writing up the reasons why True and False, when introduced, weren't reserved words" (line 2)

### bool-formally-introduced-2-3-pep-285
- **What**: The bool type was formally introduced in Python 2.3 as a new type with two constants, through PEP 285.
- **Quote**: "It was formally introduced in Python 2.3, as a new type with two constants, and the type was introduced in PEP 285 ("Adding a bool type")." (line 4)

### bool-added-in-bugfix-release-2-2-1
- **What**: bool, True and False were also added in Python 2.2.1, which was a bugfix release, to ease backporting of code developed for Python 2.3.
- **Quote**: "Added new builtin function bool() and new builtin constants True and ... False to ease backporting of code developed for Python 2.3." (line 16)
- **Also at**: lines 6, 18

### feature-in-bugfix-release-regret
- **What**: Adding a new feature in a bugfix release was the most criticized such instance and would not be done now; expressed as a change in practice.
- **Quote**: "This was the last (and the most criticized) time we added a new feature in a bugfix release -- we'd never do that these days." (line 22)

### bool-differs-between-2-2-1-and-2-3
- **What**: The bool in 2.2.1 differed from 2.3: in 2.3 bool is a new type, while in 2.2.1 bool() is a built-in function and True/False are just ints equal to 1 and 0.
- **Quote**: "in 2.3, bool is a new type; in 2.2.1, bool() is a built-in function and the constants are just ints." (line 22)
- **Also at**: line 20

### breakneck-development-pace
- **What**: The compressed chronology of PEP 285's creation, acceptance and finalization against the release dates reflects a much faster pace of doing things than a decade later.
- **Quote**: "That's a breakneck pace compared to how we do things a decade later!" (line 24)
