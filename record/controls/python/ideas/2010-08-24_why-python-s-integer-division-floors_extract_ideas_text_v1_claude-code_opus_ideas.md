---
note: 2010-08-24_why-python-s-integer-division-floors.md
note_dir: texts
note_sha256: 879645e09678df72ae1097768692d6f31f6fc083917527ccbba6e86c262adf81
title: "Why Python's Integer Division Floors"
author: Guido van Rossum
created: 2010-08-24T09:49:00
ideas: 11
quotes_found: 10/11
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### integer-division-floors
- **What**: Integer division in Python returns the floor of the result instead of truncating towards zero as C does.
- **Quote**: "explain why integer division in Python returns the floor of the result instead of truncating towards zero like C" (line 2)

### floor-affects-only-negative-operands
- **What**: For positive operands the result is unsurprising; the flooring behavior shows up (rounding away from zero, towards negative infinity) only when an operand is negative.
- **Quote**: "if one of the operands is negative, the result is floored, i.e., rounded away from zero (towards negative infinity)" (line 10)

### div-and-mod-go-together
- **What**: Integer division (//) and modulo (%) are treated as a pair that must satisfy one mathematical relationship.
- **Quote**: "The integer division operation (//) and its sibling, the modulo operation (%), go together and satisfy a nice mathematical relationship (all variables are integers)" (line 20)

### the-invariant
- **What**: The relationship chosen is b*q + r = a with 0 <= r < b, stated for non-negative a and b.
- **Quote**: "b*q + r = a and 0 <= r < b" (line 26)

### two-choices-for-negative-a
- **What**: Extending the relation to negative a (with b positive) forces a choice: truncating q towards zero makes r negative and changes the invariant, or flooring q towards negative infinity keeps the invariant 0 <= r < b.
- **Quote**: "if you truncate q towards zero, r will become negative, so that the invariant changes to 0 <= abs(r) < otherwise, you can floor q towards negative infinity, and the invariant remains 0 <= r < b" (line 30)

### follows-number-theory-convention
- **What**: The flooring choice follows what mathematicians in number theory always prefer, and Guido made the same choice for Python.
- **Quote**: "In mathematical number theory, mathematicians always prefer the latter choice (see e.g. Wikipedia). For Python, I made the same choice" (line 32)

### modulo-where-sign-is-uninteresting
- **What**: The reason given is that in some applications of modulo the sign of a is uninteresting; the POSIX-timestamp-to-time-of-day computation (t % 86400) works out with the floor rule even for times before 1970 expressed as negative numbers, where truncation would give a meaningless result.
- **Quote**: "there are some interesting applications of the modulo operation where the sign of a is uninteresting" (line 32)
- **Also at**: lines 34

### negative-b-flips-invariant
- **What**: For negative b everything flips and the invariant becomes 0 >= r > b.
- **Quote**: "For negative b, by the way, everything just flips, and the invariant becomes:" (line 36)

### why-c-differs
- **What**: C probably truncates because the hardware did so when C was designed, which in turn stems from old hardware representing negatives as sign+magnitude or one's complement rather than two's complement.
- **Quote**: "Probably the hardware didn't do this at the time C was designed. And the hardware probably didn't do it this way because in the oldest hardware, negative numbers were represented as \"sign + magnitude\" rather than the two's complement representation" (line 40)

### floating-point-modulo-hesitation
- **What**: Tim Peters worried about extending these rules to floating point modulo; Guido concedes the floor rule can cause precision loss for x%1.0 when x is a very small negative number, but keeps integer modulo (and //, tightly coupled to it) unchanged.
- **Quote**: "Tim Peters ... has expressed some worry about my desire to extend these rules to floating point modulo. He's probably right; the truncate-towards-negative-infinity rule can cause precision loss for x%1.0 when x is a very small negative number. But that's not enough for me to break integer modulo, and // is tightly coupled to that" (line 42)
- **Open**: whether the floor rule should extend to floating point modulo is left unresolved.

### floor-vs-ambiguous-slash
- **What**: // is used instead of / deliberately: it is Python 3 syntax, also allowed in Python 2 to make clear one is invoking integer division, whereas / in Python 2 is ambiguous because it returns different results for two integers than for mixed int/float operands.
- **Quote**: "I am using // instead of / -- this is Python 3 syntax, and also allowed in Python 2 to emphasize that you know you are invoking integer division. The / operator in Python 2 is ambiguous, since it returns a different result for two integer operands than for an int and a float or two floats" (line 44)
