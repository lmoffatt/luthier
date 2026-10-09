---
note: 13_conclusion.md
note_dir: texts
note_sha256: e3e7ccb3555612cd13394e77b5d71cb0f63cd04e12335e660d5e7953c8b41f14
title: "13. Conclusion"
author: Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler
created: 2007-06-09T00:00:00
ideas: 9
quotes_found: 9/9
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Haskell; designers=Paul Hudak, John Hughes, Simon Peyton Jones and Philip Wadler
agent: claude-code
model: opus
effort: low
---

## Ideas

### purely-functional-as-principled-attack
- **What**: Functional programming in its purely functional form is characterized as a deliberate, principled attempt to meet the difficulty of writing programs that work.
- **Quote**: "Functional programming, particularly in its purely functional form, is a radical and principled attack on the challenge of writing programs that work." (line 3)

### quirky-elegance-drew-designers
- **What**: The authors say what first drew many of them to the field was the odd elegance of the purely functional approach.
- **Quote**: "It was precisely this quirky elegance that attracted many of us to the field." (line 4)

### early-impracticality
- **What**: In the early 1980s purely functional languages, though radical and elegant, were impractical: slow, memory-hungry, and lacking input/output.
- **Quote**: "purely functional languages might have been radical and elegant, but they were also laughably impractical: they were slow, took lots of memory, and had no input/output." (line 6)

### haskell-contributed-through-purity-and-critical-mass
- **What**: The authors credit Haskell with helping overcome that impracticality by holding strictly to purity and by gathering a critical mass of interest and research around one language.
- **Quote**: "Haskell has contributed to that progress, by sticking remorselessly to the discipline of purity, and by building a critical mass of interest and research effort behind a single language." (line 9)

### purity-not-the-one-right-way
- **What**: The authors disclaim that purely functional programming is necessarily the correct way to write programs.
- **Quote**: "Purely functional programming is not necessarily the Right Way to write programs." (line 12)

### longterm-bet-on-principled-control-of-effects
- **What**: Beyond instinct, the authors describe a conscious long-term bet that principled control of effects would prove important, against the mainstream default of unrestricted effects.
- **Quote**: "many of us were consciously making a longterm bet that principled control of effects would ultimately turn out to be important, despite the dominance of effects-by-default in mainstream languages." (line 13)
- **Open**: Whether the bet pays off is stated as still unresolved: "Whether that bet will truly pay off remains to be seen." (line 17)

### convergence-from-both-ends
- **What**: The authors observe a convergence: the functional community has learned the value of effects and a way to tame them, while mainstream languages adopt declarative constructs.
- **Quote**: "At one end, the purely functional community has learnt both the merit of effects, and at least one way to tame them. At the other end, mainstream languages are adopting more and more declarative constructs: comprehensions, iterators, database query expressions, first-class functions, and more besides." (line 18)

### parallelism-punishes-unrestricted-effects
- **What**: The authors expect the convergence to continue, driven especially by parallelism, which they say penalizes unrestricted effects severely.
- **Quote**: "driven especially by the goad of parallelism, which punishes unrestricted effects cruelly." (line 23)

### enduring-value-through-influence
- **What**: The authors anticipate that even after Haskell itself is forgotten, the ideas and techniques it nurtured will have lasting value through their influence on future languages.
- **Quote**: "when that day comes, the ideas and techniques that it nurtured will prove to have been of enduring value through their influence on languages of the future." (line 26)
