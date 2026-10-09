---
note: 2009-03-31_the-great-or-grand-renaming.md
note_dir: texts
note_sha256: bf245a7ba1a5a53c22dd8660ab8a686198a134c896d4f9db1f8f90ebe3e07fb5
title: "The Great (or Grand) Renaming"
author: Guido van Rossum
created: 2009-03-31T08:44:00
ideas: 8
quotes_found: 8/8
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### python-as-stand-alone-program
- **What**: Python was first conceived as a stand-alone program that would only occasionally link in third-party libraries, and this assumption shaped how its source code defined names.
- **Quote**: "When Python was first created, I always envisioned it as a stand-alone program, occasionally linking in third-party libraries." (line 2)

### freely-defined-global-names
- **What**: Because of the stand-alone assumption, the C source code defined global linker names freely, without a namespace discipline.
- **Quote**: "The source code therefore freely defined global names (in the C/linker sense) like ‘object’, ‘getlistitem’, ‘INCREF’ and so on." (line 2)

### demand-for-embedded-python
- **What**: As Python grew popular, users asked for an embeddable version, Python itself as a library linked into other applications, analogous to how Emacs embeds a Lisp interpreter.
- **Quote**: "people started to ask for an “embedded” version of Python, which would itself be a library that could be linked into other applications – not unlike the way that Emacs incorporates a Lisp interpreter." (line 2)

### name-clashes-block-embedding
- **What**: Embedding was complicated by clashes between Python's freely chosen global names and those of the host application, with ‘object’ a particularly common collision.
- **Quote**: "this embedding was complicated by name clashes between Python’s global names and those defined by the embedding application – the name 'object’ was especially popular." (line 4)

### py-prefix-naming-convention
- **What**: The design decision taken was a naming convention prefixing all Python globals with “Py”, “_Py” for internal names that must be global, and “PY” for macros.
- **Quote**: "a naming convention was chosen, whereby all Python globals would have a name starting with “Py” or “_Py” (for internal names that had to be global for technical reasons) or “PY” (for macros)." (line 4)

### two-phase-transition-with-macros
- **What**: The rename was done in two phases bridged by C preprocessor macros, so that old and new names could be mixed and still compile correctly, for backwards compatibility with existing extension modules and to ease the transition for developers.
- **Quote**: "there were two phases. In phase one the linker saw the old names, but the source code used the new names, which were translated to the old names using a large number of C preprocessor macros. In phase two the linker saw the new names, but ... another set of macros now translated the old names to the new names. In both phases, the code could mix old and new names and work correctly." (line 6)

### renaming-paired-with-unit-tests
- **What**: The renaming effort was accompanied by the task of adding unit tests for much of the standard library.
- **Quote**: "They also helped with the equally tedious task of adding unit tests for much of the standard library." (line 10)

### renamings-are-traumatic-for-communities
- **What**: Large renamings are traumatic for developer communities because they require relearning names, rewriting documentation, and complicate integrating patches made before but applied after the rename, especially across unrenamed branches.
- **Quote**: "Great or Grand Renamings are often traumatic events for software developer communities, since they requires the programmers' brains to be rewired, documentation to be rewritten, and complicate the integration of patches created before the renaming but applied after." (line 14)
