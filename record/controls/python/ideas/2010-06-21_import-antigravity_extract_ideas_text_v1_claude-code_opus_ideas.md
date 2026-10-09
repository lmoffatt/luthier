---
note: 2010-06-21_import-antigravity.md
note_dir: texts
note_sha256: b3f5160aaedbc0b463b9ab307651f1ef5a796e0eaf80095795316c86c4899d7d
title: "import antigravity"
author: Guido van Rossum
created: 2010-06-21T11:31:00
ideas: 2
quotes_found: 2/2
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### antigravity-as-stdlib-easter-egg
- **What**: Python 3's standard library carries an easter egg module, `antigravity`, referencing the XKCD comic that mentions Python; its inclusion is treated as a deliberate playful element of the distribution rather than functional code. Van Rossum reports it was added to Python 3 by Skip Montanaro and originated as a launch easter egg in Google App Engine.
- **Quote**: "The antigravity module, referencing the XKCD comic mentioning Python, was added to Python 3 by Skip Montanaro." (line 2)
- **Also at**: lines 4, 12

### easter-egg-inside-the-easter-egg
- **What**: The stdlib version nests a second hidden joke in its source: a function that purports to implement the XKCD geohashing algorithm, so the playfulness is layered for anyone who reads the code.
- **Quote**: "The Python 3 stdlib version has an easter egg inside the easter egg, ... it defines a function that purports to implement the XKCD geohashing algorithm." (line 12)
