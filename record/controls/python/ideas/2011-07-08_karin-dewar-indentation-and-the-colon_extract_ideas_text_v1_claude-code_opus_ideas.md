---
note: 2011-07-08_karin-dewar-indentation-and-the-colon.md
note_dir: texts
note_sha256: c849d5fb1bb3ef7d1703d293e5783c941ed865c24185457a135d0a915dd9335b
title: "Karin Dewar, Indentation and the Colon"
author: Guido van Rossum
created: 2011-07-08T16:13:00
ideas: 7
quotes_found: 6/7
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### colon-not-indentation-is-the-dewar-contribution
- **What**: Guido corrects an earlier account: the Dewar story is the origin of the colon in ABC (and hence Python), not of the indentation. He reports this from Lambert Meertens' email.
- **Quote**: "Karin Dewar provided the inspiration for the use  of the colon in ABC (and hence in Python) leading up to the indentation, not for indentation itself." (line 2)
- **Also at**: line 4

### mandatory-indentation-in-B0-controlled-by-editor
- **What**: Meertens reports that B0, the first design in the sequence leading to ABC, had non-optional indentation for grouping, added by a dedicated editor, with the user unable to turn it off or modify it; it was supplemented by BEGIN/END delimiters.
- **Quote**: "Already B0, ... had non-optional indentation for grouping, supplemented by     enclosing the group between BEGIN and END     delimiters." (line 6)
- **Quote**: "The indentation was supposed to be added, like pretty printing, by a     dedicated B editor, and the user had no control over this" (line 6)

### begin-end-superfluous-under-mandatory-indentation
- **What**: Meertens reports that once indentation was mandatory the separate delimiters were redundant, so they were progressively dropped (no BEGIN in B1, END IF/END FOR dropped in B2), leaving pure indentation as the sole indicator of grouping.
- **Quote**: "Given the mandatory indentation, separate BEGIN and END     delimiters are of course superfluous" (line 8)
- **Quote**: "the latter delimiters were also dropped in      B2, leaving pure     indentation as the sole indicator of grouping." (line 8)

### indentation-to-make-text-neat-and-suggestive
- **What**: Meertens states the origin of indentation in ABC was the desire for the program text to look neat and suggest its meaning, codifying a practice that was already common but not enforced.
- **Quote**: "the desire to have     the program text look neat and be suggestive of the meaning,     codifying what was already common practice but not enforced." (line 10)

### removing-begin-end-influenced-by-plauger
- **What**: Meertens notes the decision to remove the BEGIN...END "noise" may have been influenced by Plauger's [PL75], which advocated pure indentation for grouping.
- **Quote**: "The     decision to remove the noise of BEGIN ... END     may have been influenced by [PL75], which actually advocated using     pure indentation for grouping." (line 10)
- **Open**: stated as a possible influence ("may have been"), not settled.

### B-first-published-language-with-indentation-grouping
- **What**: Meertens claims B was, as far as he is aware, the first published and implemented language to use indentation for grouping, noting occam (1983) and Miranda (1985) came later and so could not be the source.
- **Quote**: "As far as I am aware, B was the first actually     published (and implemented) language to use indentation for     grouping." (line 10)
- **Open**: qualified with "As far as I am aware".

### colon-resolves-the-for-line-misunderstanding
- **What**: Meertens recounts the Jabłonna design session where Robert Dewar's wife, reading a syntax, asked whether 'FOR i ...' applied to the following lines and not just that line; the scientists realized a colon at the end of the line would have avoided the misunderstanding, which is how the colon was conceived.
- **Quote**: "here the scientists realized that the misunderstanding would have been avoided if there had been a colon at the end of that line." (line 15)
