# Reference for the control on Python

What the filter should find, from Guido van Rossum, "Python's Design Philosophy", *The History of
Python*, 2009-01-13, https://python-history.blogspot.com/2009/01/pythons-design-philosophy.html
(in the feed pinned in `../README.md`). Never shown to the filter. Quoted as he wrote it.

Timesaving rules ("a one-person skunkworks project"):

- G1 Borrow ideas from elsewhere whenever it makes sense.
- G2 "Things should be as simple as possible, but no simpler." (Einstein)
- G3 Do one thing well (The "UNIX philosophy").
- G4 Don't fret too much about performance--plan to optimize later when needed.
- G5 Don't fight the environment and go with the flow.
- G6 Don't try for perfection because "good enough" is often just that.
- G7 (Hence) it's okay to cut corners sometimes, especially if you can do it right later.

Other principles:

- G8 The Python implementation should not be tied to a particular platform.
- G9 Don't bother users with details that the machine can handle.
- G10 Support and encourage platform-independent user code, but don't cut off access to platform capabilities or properties.
- G11 A large complex system should have multiple levels of extensibility.
- G12 Errors should not be fatal.
- G13 At the same time, errors should not pass silently.
- G14 A bug in the user's Python code should not be allowed to lead to undefined behavior of the Python interpreter.
- G15 Punctuation characters should be used conservatively, in line with their common use in written English or high-school algebra.

The Zen of Python (Tim Peters), as he quotes it:

- Z1 Beautiful is better than ugly.
- Z2 Explicit is better than implicit.
- Z3 Simple is better than complex.
- Z4 Complex is better than complicated.
- Z5 Flat is better than nested.
- Z6 Sparse is better than dense.
- Z7 Readability counts.
- Z8 Special cases aren't special enough to break the rules.
- Z9 Although practicality beats purity.
- Z10 Errors should never pass silently.
- Z11 Unless explicitly silenced.
- Z12 In the face of ambiguity, refuse the temptation to guess.
- Z13 There should be one-- and preferably only one --obvious way to do it.
- Z14 Although that way may not be obvious at first unless you're Dutch.
- Z15 Now is better than never.
- Z16 Although never is often better than right now.
- Z17 If the implementation is hard to explain, it's a bad idea.
- Z18 If the implementation is easy to explain, it may be a good idea.
- Z19 Namespaces are one honking great idea -- let's do more of those!

Departures from ABC ("In many ways, Python is a conscious departure from these"), stated as what
Python does instead:

- A1 Not striving for perfection (ABC "strived for perfection").
- A2 Not isolating the user from the world of computers: files, other programs (ABC wanted to isolate the user "as completely as possible").
- A3 Standard programming terminology (ABC introduced "newbie-friendly" terms).
- A4 An evolutionary path with user participation, users encouraged to look under the hood (ABC was "a closed system").
