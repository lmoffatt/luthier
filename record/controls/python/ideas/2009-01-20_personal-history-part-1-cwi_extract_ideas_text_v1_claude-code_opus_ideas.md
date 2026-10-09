---
note: 2009-01-20_personal-history-part-1-cwi.md
note_dir: texts
note_sha256: 56f816a0ab37b0d040e066a50eb52578af3a2af5a662c0b586cfb88df247a782
title: "Personal History - part 1, CWI"
author: Guido van Rossum
created: 2009-01-20T15:19:00
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

### bridge-the-gap-between-c-and-the-shell
- **What**: Python's original motivation was the need for a higher-level language in the Amoeba project, because writing system administration utilities in C took too long and the Bourne shell wouldn't work; the aim was a language to bridge C and the shell.
- **Quote**: "there was a need for a language that would “bridge the gap between C and the shell.”  For a long time, this was Python’s main catchphrase." (line 8)

### amoeba-primitives-unlike-the-shell
- **What**: The decisive reason the Bourne shell wouldn't do was that Amoeba, as a distributed micro-kernel system with a radically new design, had primitive operations very different and finer-grained than those of the traditional shell.
- **Quote**: "Amoeba’s primitive operations were very different (and finer-grain) than the traditional primitive operations available in the Bourne shell" (line 8)

### abc-inspiration-amoeba-motivation
- **What**: ABC gave the key inspiration for Python, Amoeba the immediate motivation, and the multimedia group its growth; Python is a direct product of this experience at CWI.
- **Quote**: "ABC gave me the key inspiration for Python, Amoeba the immediate motivation, and the multimedia group fostered its growth" (line 6)

### design-new-rather-than-port
- **What**: Rather than port an existing language, van Rossum decided to design his own, because there weren't many suitable languages around; Perl 3 was even more tied to Unix than the Bourne shell.
- **Quote**: "I decided to design a language of my own which would borrow everything I liked from ABC while at the same time fixing all its problems (as I perceived them)" (line 10)
- **Also at**: line 10

### syntax-taste-from-algol-pascal-abc
- **What**: His tastes in programming-language syntax, which shaped his dislike of Perl's syntax, were strongly influenced by Algol 60, Pascal, Algol 68, and ABC.
- **Quote**: "my tastes in programming language syntax were strongly influenced by languages like Algol 60, Pascal, Algol 68 ..., and last but not least, ABC" (line 10)

### borrow-from-abc-fix-its-problems
- **What**: The design program for Python was to keep what he liked from ABC while fixing the problems he perceived in it; the first problem he chose to fix was the name.
- **Quote**: "borrow everything I liked from ABC while at the same time fixing all its problems (as I perceived them)" (line 10)
- **Also at**: line 12

### under-analyze-the-name
- **What**: Rather than over-analyzing the naming problem (as the ABC team had with "as simple as ABC"), he deliberately under-analyzed it and picked the first thing that came to mind, Monty Python.
- **Quote**: "rather than over-analyzing the naming problem, I decided to under-analyze it. I picked the first thing that came to mind" (line 14)

### name-irreverent-and-in-tradition
- **What**: "Python" was chosen as suitably irreverent for a skunkworks project, catchy and edgy, while still fitting the tradition of naming languages after famous people (Pascal, Ada, Eiffel) and the Amoeba group's habit of naming programs after TV shows.
- **Quote**: "it fit in the tradition of naming languages after famous people, like Pascal, Ada, and Eiffel" (line 14)

### resisting-the-snake
- **What**: For many years he resisted associating the language with snakes, giving up only when O'Reilly's animal-cover tradition made a snake the cover of the first Python book.
- **Quote**: "For many years I resisted attempts to associate the language with snakes. I finally gave up when O’Reilly wanted to put a snake on the front of their first Python book" (line 16)

### pgen-first-code-least-changed
- **What**: The first piece of code written for Python's implementation was a simple LL(1) parser generator, "pgen," which is still part of the source distribution and the least changed of all the code.
- **Quote**: "the first piece of code I wrote for Python’s implementation was a simple LL(1) parser generator I called “pgen." ... still part of the Python source distribution and probably the least changed of all the code" (line 18)

### open-source-before-the-term
- **What**: Python's first public release (0.9.0) used a license that was an almost verbatim copy of the X11 MIT license, so Python was open source before the term itself was coined.
- **Quote**: "Python was open source before the term was even invented by Eric Raymond and Bruce Perens in late 1997" (line 20)

### releases-driven-by-feedback
- **What**: Immediate feedback and encouragement led him to keep a steady stream of releases, adopting CVS to track changes and share coding responsibilities.
- **Quote**: "There was immediately a lot of feedback and with this encouragement I kept a steady stream of releases coming for the next few years" (line 22)
