---
note: 2009-02-03_early-language-design-and-development.md
note_dir: texts
note_sha256: 38f4f94b1b3813cb1e644ed7807116f091691570b92e59621274fb96868cf9f7
title: "Early Language Design and Development"
author: Guido van Rossum
created: 2009-02-03T10:53:00
ideas: 18
quotes_found: 18/18
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### abc-foremost-influence
- **What**: Python's first and foremost influence was ABC, a teaching language designed at CWI by first analyzing the programming task and then iterating with serious user testing; van Rossum's role was implementing the language and its editing environment.
- **Quote**: "Python's first and foremost influence was ABC... It was designed by first doing a task analysis of the programming task and then doing several iterations that included serious user testing." (line 4)

### indentation-from-abc
- **What**: Python's indentation comes from ABC, though the idea predates ABC (promoted by Knuth, used by occam); it is a well-known concept of programming style.
- **Quote**: "Python's use of indentation comes directly from ABC, but this idea didn't originate with ABC--it had already been promoted by Donald Knuth and was a well-known concept of programming style." (line 6)

### colon-before-indented-block
- **What**: ABC's authors invented the colon separating the lead-in clause from the indented block; user testing without it showed the indentation's meaning was unclear to beginners, and the colon clarified it by drawing attention to what follows and tying the phrases together.
- **Quote**: "ABC's authors did invent the use of the colon that separates the lead-in clause from the indented block. After early user testing without the colon, it was discovered that the meaning of the indentation was unclear to beginners... The addition of the colon clarified it significantly" (line 6)

### list-as-flexible-array
- **What**: ABC's lists were sorted bags unsuitable for representing a sequence of lines read from a file, so van Rossum changed the list into a flexible array with insert and delete operations, giving users complete control over item ordering, with a sort method for occasional sorted results.
- **Quote**: "So I changed the list type into a flexible array with insert and delete operations, giving users complete control over the ordering of items in a list. A sort method supported the occasional need for sorted results." (line 8)

### hash-table-over-btree
- **What**: He replaced ABC's sorted tables with a hash table, believing it faster and easier to implement than ABC's asymptotically optimal B-tree, which proved hard to implement correctly and sub-optimal for small sizes.
- **Quote**: "I also replaced the sorted tables with a hash table implementation. I chose a hash table because I believed this to be faster and easier to implement than ABC's B-tree implementation." (line 10)

### tuple-kept-with-indexing
- **What**: He kept ABC's immutable tuple (with packing and unpacking taken directly from ABC) and, since tuples are internally arrays, added array-like indexing and slicing.
- **Quote**: "I kept ABC's immutable tuple data type... Since tuples are internally represented by arrays, I decided to add array-like indexing and slicing." (line 12)

### printed-repr-valid-input
- **What**: A rule taken from ABC is that every data type, when printed or converted to a string, should be represented by an expression that is valid input to the parser.
- **Quote**: "One of the rules I took from ABC was that every data type, when printed or converted to a string, should be represented by an expression that was a valid input to the language's parser." (line 14)

### empty-and-one-tuple-notation
- **What**: Adding indexing forced resolving tuples of length 0 and 1; to keep the printed-repr rule yet not lose the distinction between a one-tuple and a parenthesized expression, he used a trailing comma for one-tuples and "()" for the empty tuple, requiring parentheses only there so that representing the empty tuple as nothing would not mask typos.
- **Quote**: "I settled for an ugly but pragmatic approach where a trailing comma would turn an expression into a one-tuple and \"()\" would represent a zero-tuple... I felt representing the empty tuple by \"nothing\" could too easily mask genuine typos." (line 14)
- **Open**: he calls the approach "ugly but pragmatic"

### sequence-generalization
- **What**: Having three indexable types (list, tuple, string), he generalized them to a common concept, the sequence, so that length, indexing, slicing, and iteration work the same on any sequence type.
- **Quote**: "I decided to generalize these to a common concept, the sequence. This generalization made it so certain core operations such as getting the length (len(s)), indexing (s[i]), slicing (s[i:j]), and iteration (for i in s) worked the same on any sequence type." (line 16)

### machine-numbers-over-rationals
- **What**: Numbers are where he strayed most from ABC: ABC's exact arbitrary-precision rationals didn't pan out (a tax computation ran on numbers with thousands of digits), so Python chose a traditional model of machine integers and binary floating point, represented by the C types long and double.
- **Quote**: "The rational numbers didn't pan out in my view... For Python I therefore chose a more traditional model with machine integers and machine binary floating point." (line 18)

### bignum-long-type
- **What**: Feeling there was still a use case for unbounded exact numbers, he added a bignum type called long, reusing a bignum implementation left from an earlier unfinished attempt to improve ABC.
- **Quote**: "Feeling that there was still an important use case for unbounded exact numbers, I added a bignum data type, which I called long." (line 20)

### machine-ints-for-common-case
- **What**: Although he added bignums, he did not want them for all integer operations: profiling showed integer operations are a significant fraction of running time and the most common use is indexing sequences that fit in memory, so machine integers serve the common cases and bignums only "serious math."
- **Quote**: "I didn't want to use bignums for all integer operations... I envisioned machine integers being used for all of the most-common cases and the extra range of bignums only coming into play when doing \"serious math\"" (line 22)

### explicit-long-suffix-violates-philosophy
- **What**: Having two integer types forced a way to distinguish them; requiring a trailing L to mark longs violated the ABC-inspired philosophy of not making users care about uninteresting implementation details.
- **Quote**: "This is one area where Python violated the ABC-inspired philosophy of not requiring users to care about a uninteresting implementation details." (line 28)

### int-long-divergent-semantics
- **What**: A more egregious error was that int and long had slightly different semantics: machine ints silently clipped on overflow and were treated as unsigned by bitwise, shift, and octal/hex conversions, while longs were always signed, so the same operation could differ by representation.
- **Quote**: "A more egregious error was that my implementation of integers and longs had slightly different semantics in certain cases!" (line 30)

### overflow-raises-exception
- **What**: To resolve this he changed most arithmetic operations to raise OverflowError rather than silently clip (except bitwise operations, where C behavior was expected), reasoning that otherwise users would come to rely on signed modulo-2**32 semantics and fixing it later would be a painful transition.
- **Quote**: "I changed most arithmetic operations to raise an OverflowError exception when the result didn't fit... Had I not added this check, Python users would have undoubtedly started writing code that relied on the semantics of signed binary arithmetic modulo 2**32 (like C users do), and fixing the mistake would have been a much more painful transition to the community." (line 32)
- **Also at**: line 34

### overflow-check-cost-dwarfed
- **What**: A painful debugging of "Meertens numbers," whose intermediate results exceeded 32 bits, convinced him to check all integer operations for overflow; the extra cost was dwarfed by the overhead already incurred from allocating a new object for each result.
- **Quote**: "The extra cost of the overflow check would be dwarfed by the overhead I was already incurring due to the implementation choice of allocating a new object for the result." (line 34)

### should-have-promoted-to-long
- **What**: Raising an overflow exception was still not right; stuck on C's rule that operations on type T return type T, he should have had overflowing integer operations promote their result to longs, as Python does today, though the transition took a long time.
- **Quote**: "In hindsight, I should have made integer operations that overflow promote their result to longs. This is the way that Python works today, but it took a long time to make this transition." (line 36)
- **Open**: the same C rule "T returns T" also caused the integer-division truncation mistake, discussed in a later post

### no-undefined-values
- **What**: The positive lesson: there should be no undefined result values in Python; an exception is always raised when no correct value can be computed, so programs never fail from silently passed undefined values, a principle still held in the language and standard library.
- **Quote**: "I decided that there should be no undefined result values in Python – instead, exceptions should always be raised when no correct return value can be computed." (line 38)
