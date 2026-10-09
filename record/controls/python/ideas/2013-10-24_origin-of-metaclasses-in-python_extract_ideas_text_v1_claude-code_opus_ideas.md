---
note: 2013-10-24_origin-of-metaclasses-in-python.md
note_dir: texts
note_sha256: 8650d86128332a2f6762957216c5379f14a50ce206b5d8cf963462690f07d35c
title: "Origin of metaclasses in Python"
author: Guido van Rossum
created: 2013-10-24T09:58:00
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

### metaclass-design-not-from-ruby
- **What**: Python's metaclass design did not come from Ruby; the author corrects a speculation to the contrary.
- **Quote**: "whether Python's metaclass design came from Ruby. It did not." (line 2)

### ruby-inspired-by-python
- **What**: The author reports that Ruby was inspired by Python, citing what Matz told him: 20% Python, 80% Perl, with Larry Wall as his hero. (reported by Matz)
- **Quote**: "Ruby was in fact\ninspired by Python. Mats once told me that his inspiration was 20%\nPython, 80% Perl, and that Larry Wall is his hero." (line 5)

### new-style-classes-an-iteration
- **What**: New-style classes were the second or third iteration of the metaclass idea in Python, which the author had written about in 1998.
- **Quote**: "New-style classes were just the second or third iteration of the idea." (line 11)

### new-style-classes-inspired-by-forman-danforth
- **What**: The author was inspired to implement new-style classes by the book "Putting Metaclasses to Work" by Ira Forman and Scott Danforth.
- **Quote**: "I was inspired to implement new-style classes by a very\nspecific book, \"Putting Metaclasses to Work\" by Ira Forman and Scott\nDanforth" (line 13)

### type-as-object-from-the-start
- **What**: Even Python's original 1990 design held that 'type' was itself an object; every object's type pointer points to a special object whose data is C function pointers implementing behavior, like a C++ vtable.
- **Quote**: "even Python's original design (in 1990, published in\n1991) had the notion that 'type' was itself an object. The type pointer\nin any object has always been a pointer to a special object, whose\n\"data\" was a bunch of C function pointers implementing the behavior of\nother objects, similar to a C++ vtable." (line 17)

### meta-type-as-its-own-type
- **What**: The type of a type was always a special type object, a meta-type, recognized because it is its own type.
- **Quote**: "The type of a type was always a\nspecial type object, which you could call a meta-type, to be recognized\nbecause it was its own type." (line 21)

### smalltalk-metaclasses-different-and-late
- **What**: The author was only vaguely aware of Smalltalk at the time and found its use of metaclasses, which differs from Python's or Ruby's, surprising when he read about it much later.
- **Quote**: "I was only vaguely aware of Smalltalk at the time; I\nremember being surprised by its use of metaclasses (which is quite different from that in Python or Ruby!) when I read about\nthem much later." (line 25)

### smalltalk-bytecode-influence
- **What**: Smalltalk's bytecode was a bigger influence on Python's bytecode, which the author had read about in a book by Adele Goldberg and others.
- **Quote**: "Smalltalk's bytecode was a bigger influence of Python's\nbytecode though." (line 27)
