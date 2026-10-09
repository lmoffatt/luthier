---
note: 2009-03-10_the-problem-with-integer-division.md
note_dir: texts
note_sha256: 2e36902c619683d0099d5da384c94ea2fbfb75bbe20e70a2c84b43e39f2e5419
title: "The Problem with Integer Division"
author: Guido van Rossum
created: 2009-03-10T13:31:00
ideas: 11
quotes_found: 11/11
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### integer-division-early-mistake
- **What**: Guido names Python's truncating integer division as an early design mistake with large consequences, and notes he abandoned ABC's approach to numbers when he created Python.
- **Quote**: "Python's handling of integer division is an example of early mistake with huge consequences.   As mentioned earlier, when Python was created, I abandoned the approach to numbers that had been used in ABC." (line 2)
- **Also at**: line 10

### abc-exact-rationals
- **What**: In ABC, dividing two integers gave an exact rational number; in Python integer division truncated instead.
- **Quote**: "in ABC, when you divided two integers, the result was an exact rational number representing the result.  In Python however, integer division truncated the result to an integer." (line 2)

### rationals-did-not-pan-out
- **What**: Exact rational numbers didn't work out as ABC's designers hoped: programs silently used rationals with thousands of digits of precision, running slow, and the fix (starting with an inexact zero) was non-intuitive and hard to debug for beginners.
- **Quote**: "In my experience, rational numbers didn't pan out as ABC's designers had hoped." (line 4)
- **Open**: whether the problem was inherent to rationals or to how beginners met them is left as experience, not settled.

### c-numerical-model
- **What**: For Python he relied on C's numerical model: ints as a C long of at least 32 bits, floats as a C double, plus an arbitrary precision integer type called "long".
- **Quote**: "with Python, I relied on the other numerical model with which I was familiar, C. ... I chose to represent Python integers by a C long (guaranteeing at least 32 bits of precision) and floating point numbers by a C double.   I then added an arbitrary precision integer type which I called \"long.\"" (line 6)

### result-type-follows-operands
- **What**: The major mistake was borrowing C's rule that an arithmetic operation's result is always the same type as its operands, a rule that makes sense in C but not in a very-high-level language.
- **Quote**: "The major mistake was that I also borrowed a rule that makes sense in C but not so much in a very-high-level language. For the standard arithmetic operations, including division, the result would always be the same type as the operands." (line 8)

### forbidding-mixed-mode-arithmetic
- **What**: He initially forbade mixed-mode arithmetic to keep the type implementations independent, so one couldn't add an int to a float or even an int to a long; Tim Peters convinced him this was a bad idea and he introduced mixed-mode arithmetic with the usual coercion rules.
- **Quote**: "I initially used another misguided rule that forbade mixed-mode arithmetic, with the aim of making the type implementations independent from each other. ... After Python was released publicly, Tim Peters quickly convinced me that this was a really bad idea, and I introduced mixed-mode arithmetic with the usual coercion rules." (line 8)

### integer-division-as-rite-of-passage
- **What**: Proposals to change integer division met opposition from those who held that learning integer division was a useful "rite of passage" for programmers.
- **Quote**: "the proposal to change this has had some tough opposition from folks who believed that learning about integer division was one of the more useful \"rites of passage\" for all programmers." (line 10)

### no-type-declarations-no-coercion
- **What**: Because Python has no type declarations, nothing stops a caller from passing integers to an algorithm meant for floats; unlike statically typed C, Python does not coerce the arguments, so the algorithm runs with integers until mixed-mode arithmetic yields floats.
- **Quote**: "since Python doesn’t have type declarations, nothing is there to stop a caller from providing you with integer arguments. In a statically typed language, like C, the compiler will coerce the arguments to floats, but Python does no such thing" (line 12)
- **Also at**: line 16

### silent-truncation-inserts-error
- **What**: Since integers behave like floats for everything except division, one is misled to expect algorithms to behave the same either way; but with two integer operands division silently truncates, inserting a potentially large error, and defensive coercion is tedious, hurts readability and maintainability, and blocks use with complex arguments.
- **Quote**: "when division is involved, and the possibility exists that both operands are integers, the numeric result is silently truncated, essentially inserting a potentially large error into the computation." (line 14)

### close-but-wrong-answer-hard-to-notice
- **What**: Passing an integer where a float is expected yields an answer close to correct but with much larger error, hard to debug or notice, unlike an invalid type such as a string which is caught quickly (multiplication being the exception).
- **Quote**: "passing an integer can cause an answer that is close to the correct answer but has a much larger error – which is difficult to debug or even notice." (line 16)

### fixing-integer-division
- **What**: Fixing integer division was hard because programs relied on truncation; the fix was a truncating operator (//), a per-module opt-in ("from __future__ import division"), and a command line flag (-Qxxx), with the correct behavior becoming the default in Python 3000.
- **Quote**: "A truncating division operator (//) was added to the language to provide the same functionality.   In addition, a mechanism (\"from __future__ import division\") was introduced by which the new integer division semantics could be enabled. ... the correct behavior has become the default behavior in Python 3000." (line 18)
