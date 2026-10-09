---
note: 04_syntax.md
note_dir: texts
note_sha256: 4d91b8909bea16302416d88fb9b207b85e0f19130097f2bcfdf1e4c7e098a082
title: "4. Syntax"
author: Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler
created: 2007-06-09T00:00:00
ideas: 35
quotes_found: 35/35
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Haskell; designers=Paul Hudak, John Hughes, Simon Peyton Jones and Philip Wadler
agent: claude-code
model: opus
effort: low
---

## Ideas

### syntax-taken-seriously-despite-dismissal
- **What**: Against the common view that syntax is trivial and semantics is where the real work lies, the Haskell Committee worked very hard on designing the syntax.
- **Quote**: "Despite this, the Haskell Committee worked very hard...on designing (and arguing about) the syntax of Haskell." (line 8)
- **Also at**: lines 3, 6

### syntax-as-personal-user-interface
- **What**: Syntax is the user interface of a language and can become very personal, which is why some of the committee's most heated debates were over syntax.
- **Quote**: "We also found that syntax, being the user interface of a language, could become very personal." (line 14)
- **Also at**: line 15

### haskell-is-a-pretty-language
- **What**: A pleasing, though not explicit, consequence of the effort on syntax is the repeated comment that Haskell programs look nice.
- **Quote**: "one of the most pleasing consequences of our effort has been comments heard... that "Haskell is a pretty language."" (line 18)
- **Also at**: lines 22, 24

### avoid-semicolon-no-sequencing
- **What**: Because a language without side effects has no notion of sequencing, the committee chose to avoid the semicolon and its imperative baggage, while still separating declarations.
- **Quote**: "the feeling of the Haskell Committee was that we should avoid the semicolon and its sequential, imperative baggage." (line 30)
- **Also at**: lines 28, 29

### anonymous-function-backslash
- **What**: The `\x -> exp` syntax for anonymous functions was chosen to resemble lambda, with backslash as the closest ASCII to λ, and `->` used instead of a period so the period could be reserved for function composition.
- **Quote**: "the backslash was the closest single ASCII character to the Greek letter λ. However, "->" was used instead of a period in order to reserve the period for function composition." (line 43)
- **Also at**: lines 41, 42

### layout-avoids-clutter
- **What**: Exploiting the physical layout of the program, via the offside rule, is a simple and elegant way to avoid syntactic clutter; the idea was familiar from SASL and Miranda and goes back to CPL and ISWIM.
- **Quote**: "Exploiting the physical layout of the program text is a simple and elegant way to avoid syntactic clutter." (line 47)
- **Also at**: lines 48, 49, 50, 51

### one-prefix-operator-negation
- **What**: Haskell has only one prefix operator, arithmetic negation; the committee wanted none but couldn't force users to write `minus 42` or `~42` instead of `-42`, and the scarcity of prefix operators makes parsing easier.
- **Quote**: "The Haskell Committee in fact did not want any prefix operators, but we couldn't bring ourselves to force users to write something like minus 42 or ~42 for the more conventional -42." (line 54)
- **Also at**: lines 53, 57

### layout-rules-simple-and-lenient
- **What**: The layout rules had to be very simple, and after exploring variations the committee adopted a design more lenient than Miranda's, supporting larger function definitions with less enforced indentation, because programmers would want large definitions and layout shouldn't get in the way.
- **Quote**: "We ended up with a design that differed from our most immediate inspiration, Miranda, in supporting larger function definitions with less enforced indentation." (line 61)
- **Also at**: lines 60, 62, 64, 66

### override-layout-for-generated-programs
- **What**: Like Miranda, Haskell lets the user override implicit layout with explicit curly braces and semicolons, thought important because people were expected to write programs that generate Haskell programs, for which explicit separators are easier to generate than layout.
- **Quote**: "we expected people to write programs that generated Haskell programs, and we thought it would be easier to generate explicit separators than layout." (line 70)
- **Also at**: lines 67, 68, 69

### infix-operators-like-mathematics
- **What**: Wanting expressions to look like mathematics, the committee adopted infix operators from day one, in contrast to Scheme's consistent prefix application.
- **Quote**: "The Haskell Committee wanted expressions to look as much like mathematics as possible, and thus from day one we bought into the idea that Haskell would have infix operators." (line 74)
- **Also at**: lines 133, 134, 135

### user-definable-infix-operators
- **What**: It was important that infix operators be definable by the user, including declarations of precedence and associativity.
- **Quote**: "It was also important to us that infix operators be definable by the user, including declarations of precedence and associativity." (line 77)

### infix-binds-less-tightly
- **What**: Infix application always binds less tightly than conventional function application, so expressions like `f x + g y` never need parentheses; this decision proved good for readability.
- **Quote**: "the former always binds less tightly than the latter. Thus f x + g y never needs parentheses, regardless of what infix operator is used." (line 81)
- **Also at**: lines 83, 84

### at-patterns-bind-tightly-mistake
- **What**: The simple binding rule is not followed by @-patterns, which bind more tightly than anything; this was probably a mistake, though not a major problem given their limited use.
- **Quote**: "Sadly, this simple rule is not adhered to by @-patterns, which bind more tightly than anything; this was probably a mistake" (line 85)
- **Also at**: lines 87, 88
- **Open**: Whether @-patterns binding tightly was a mistake is stated as probable, not settled.

### complex-layout-rule-programmer-expects
- **What**: Driven by the constraints and a desire to do what the programmer expects, Haskell evolved a fairly complex layout rule, complex enough to be formally specified first in the Haskell 98 Report, yet most users adopt a conforming style.
- **Quote**: "Influenced by these constraints and a desire to "do what the programmer expects", Haskell evolved a fairly complex layout rule" (line 90)
- **Also at**: lines 91, 92

### many-ways-to-define-functions
- **What**: Haskell offers many ways to define functions, but they are simple and all fit together sensibly.
- **Quote**: "There are lots of ways to define functions in Haskell...but the ways are simple and all fit together in a sensible manner." (line 95)
- **Also at**: lines 96, 97

### currying
- **What**: Following a tradition from Frege, honed by Schönfinkel and Curry, a function of two arguments is represented as a one-argument function returning a one-argument function; one advantage is that curried form is often more compact.
- **Quote**: "a function of two arguments may be represented as a function of one argument that itself returns a function of one argument." (line 99)
- **Also at**: lines 38, 39, 40, 101, 102

### application-by-juxtaposition
- **What**: Function application is denoted by juxtaposition and associates to the left, so `f x y` parses as `(f x) y`, leading to concise and powerful code.
- **Quote**: "Function application is denoted by juxtaposition and associates to the left. Thus, f x y is parsed (f x) y." (line 103)
- **Also at**: lines 105, 106, 107

### curried-and-uncurried-both-supported
- **What**: Like other lambda-calculus-based languages, Haskell supports both curried and uncurried definitions.
- **Quote**: "Haskell, like many other languages based on lambda calculus, supports both curried and uncurried definitions:" (line 108)

### first-class-values-and-infix-ambiguity
- **What**: The feeling that all values, especially functions, should be first class clashed with infix operators not being first class, a problem made apparent by the ambiguity of `f + x`.
- **Quote**: "there was also the feeling that all values in Haskell should be "first class"—especially functions." (line 113)
- **Also at**: lines 114, 115, 116, 117

### sections
- **What**: The solution was a generalised notion of sections (from Wile's dissertation, via IFIP WG2.1 to Bird and Turner/Miranda): a partial application of an infix operator that, parenthesised, yields a first-class functional value, consistent with partial application of curried functions.
- **Quote**: "A section is a partial application of an infix operator to no arguments, the left argument, or the right argument—and by surrounding the result in parentheses, one then has a first-class functional value." (line 121)
- **Also at**: lines 118, 119, 120, 130, 131, 132

### minus-42-section-problem
- **What**: Sections introduced an ambiguity around negation: `(-42)` means negative 42, so one must write `\x-> x-42` or `(subtract 42)`; this was viewed as a problem with prefix operators rather than sections, and the committee chose not to buck convention on negation.
- **Quote**: "what is the meaning of (-42)? The answer is negative 42!" (line 140)
- **Also at**: lines 142, 143, 144, 145, 146

### backquotes-function-to-infix
- **What**: Having converted infix operators into values via sections, the committee added the reverse: enclosing a function identifier in backquotes makes it infix, as in `x \`elem\` xs`, valued for generality and readability; Miranda used a similar `$elem` notation from PAL.
- **Quote**: "Our simple solution was to enclose a function identifier in backquotes. For example, x 'f' y is the same as f x y." (line 150)
- **Also at**: lines 153, 154, 155, 156, 157

### namespaces-orthogonal-and-overlapping
- **What**: Namespaces were defined to give users freedom while avoiding ambiguity: lexemes orthogonal when they needed to be and overlapping when context was sufficient, so a capitalised name like `Foo` can refer to type constructor, data constructor, and module at once.
- **Quote**: "we carefully defined a set of lexemes for each namespace that were orthogonal when they needed to be, and overlapped when context was sufficient to distinguish their meaning." (line 161)
- **Also at**: lines 164, 165, 166, 167, 168

### capitalisation-and-colon-conventions
- **What**: From Miranda, data constructors are capitalised and variables are not; infix constructors must start with a colon, chosen for consistency with using single colon `:` for list cons, with `::` for type signatures, a choice opposite to ML and still controversial.
- **Quote**: "We adopted from Miranda the convention that data constructors are capitalised while variables are not, and added a similar convention for infix constructors, which in Haskell must start with a colon." (line 173)
- **Also at**: lines 176, 177, 178, 179, 180
- **Open**: The choice of `:` for cons and `::` for type signatures is described as remaining controversial to this day.

### shadowing-allowed
- **What**: A minority argued against allowing variable shadowing to avoid accidental capture, but outlawing it is inconsistent with alpha renaming, so in the end Haskell allowed shadowing.
- **Quote**: "outlawing shadowing is inconsistent with alpha renaming... So, in the end, Haskell allowed shadowing." (line 184)
- **Also at**: lines 181, 182, 183, 187

### few-reserved-keywords
- **What**: Keeping the number of reserved keywords low (21, against higher counts in other languages) was a priority, and the committee tried to avoid keywords like "as" that might be useful variable names.
- **Quote**: "Haskell has 21 reserved keywords that cannot be used as names for values or types... keeping it low was a priority of the Haskell Committee." (line 188)
- **Also at**: lines 191, 192, 193

### declaration-vs-expression-style
- **What**: Two styles of writing functional programs emerged: declaration style (multiple equations with pattern matching and guards, where clauses, arguments on the left) and expression style (composing expressions, with let, lambda, case, if).
- **Quote**: "there were two different styles in which functional programs could be written: "declaration style" and "expression style"." (line 196)
- **Also at**: lines 216, 217, 219, 225, 231, 234

### abandon-just-one-way
- **What**: An underlying assumption that there should be "just one way to do something" (making let and where redundant) was abandoned; full support for both styles was provided and is now regarded as a strength, its extra complexity superficial and explained by syntactic transformations.
- **Quote**: "In the end, we abandoned the underlying assumption, and provided full syntactic support for both styles." (line 242)
- **Also at**: lines 238, 239, 240, 244, 245, 249, 250, 251, 252

### guards-moved-to-left
- **What**: Where Miranda placed guards on the far right of equations resembling mathematics, Haskell moved them to the left-hand side, better for long definitions, placing the guard next to the patterns and in a place suggestive of evaluation order, viewed as an improvement over mathematical notation.
- **Quote**: "we moved them to the left-hand side of the definition... which had the added benefit of placing the guard right next to the patterns on formal parameters... and in a place more suggestive of the evaluation order" (line 272)
- **Also at**: lines 258, 259, 271, 277, 278

### where-attached-to-declaration
- **What**: Adopted from Miranda, a where clause is attached to a declaration (not an expression) and scopes over the guards as well as the right-hand sides; its bindings are lazy, so a binding used in only one clause is fine.
- **Quote**: "a where clause is attached to a declaration, not an expression, and scopes over the guards as well as the right-hand sides of the declarations." (line 279)
- **Also at**: lines 289, 290, 291, 292

### list-comprehensions
- **What**: List comprehensions give a convenient notation for maps, filters, and Cartesian products; first suggested by Darlington, popularised and generalised to lazy lists by Turner in KRC as "ZF expression", and named "list comprehension" by Wadler.
- **Quote**: "List comprehensions provide a very convenient notation for maps, filters, and Cartesian products." (line 294)
- **Also at**: lines 305, 306, 307, 310, 311

### comprehensions-popular-in-lazy-languages
- **What**: For some reason list comprehensions seem more popular in lazy languages, found in Miranda and Haskell but not SML or Scheme, though present in Erlang and later added to Python and planned for Javascript.
- **Quote**: "list comprehensions seem to be more popular in lazy languages; for example they are found in Miranda and Haskell, but not in SML or Scheme." (line 313)
- **Also at**: lines 315, 316, 317
- **Open**: The reason for their greater popularity in lazy languages is left unexplained ("For some reason").

### wadlers-law-of-effort
- **What**: Wadler's law describes how committee effort was allotted: semantics discussed half as much as syntax, syntax half as much as lexical syntax, lexical syntax half as much as the syntax of comments, an exaggeration that still reflected strong views on low-level details.
- **Quote**: "semantics is discussed half as much as syntax, syntax is discussed half as much as lexical syntax, and lexical syntax is discussed half as much as the syntax of comments." (line 322)
- **Also at**: lines 320, 325, 326, 328, 329

### two-comment-styles
- **What**: Haskell originally supported two comment styles, short comments with `--` to newline and longer nestable comments with `{-` and `-}`, the longer form designed to make it easy to comment out code, including code containing comments.
- **Quote**: "The longer form was designed to make it easy to comment out segments of code, including code containing comments." (line 333)
- **Also at**: lines 330, 332

### literate-comments
- **What**: Haskell added literate comments (from OL, suggested by Bird, inspired by Knuth's literate programming): reversing the usual convention so code lines carry a special mark, a `>` ("Bird tracks"), with a later Latex-style form marking code by `\begin{code}` and `\end{code}` so one file serves as both typeset paper and program.
- **Quote**: "proposed reversing the usual comment convention: lines of code, rather than lines of comment, should be the ones requiring a special mark." (line 339)
- **Also at**: lines 336, 338, 342, 343, 344, 345, 346
