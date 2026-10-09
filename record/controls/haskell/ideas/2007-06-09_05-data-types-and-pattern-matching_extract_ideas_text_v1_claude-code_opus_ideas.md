---
note: 05_data-types-and-pattern-matching.md
note_dir: texts
note_sha256: 5cb6ec843a2223691520063f8e439638a1e2a652d140fffb884983cc84254e36
title: "5. Data types and pattern matching"
author: Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler
created: 2007-06-09T00:00:00
ideas: 42
quotes_found: 40/42
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Haskell; designers=Paul Hudak, John Hughes, Simon Peyton Jones and Philip Wadler
agent: claude-code
model: opus
effort: low
---

## Ideas

### data-types-and-pattern-matching-fundamental
- **What**: Data types and pattern matching are fundamental to most modern functional languages, Scheme being a notable exception.
- **Quote**: "Data types and pattern matching are fundamental to most modern functional languages (with the notable exception of Scheme)." (line 3)

### basic-algebraic-types-straightforward-rest-interesting
- **What**: Including basic algebraic types was easy, but pattern matching, abstract types, tuples, newtypes, records, n+k patterns and views raised interesting issues.
- **Quote**: "The inclusion of basic algebraic types was straightforward, but interesting issues arose for pattern matching, abstract types, tuples, new types, records, n+k patterns, and views." (line 5)

### equations-with-pattern-matching-lineage
- **What**: The style of writing functional programs as equations with pattern matching over algebraic types traces back to Burstall's structural induction and his program-transformation work with Darlington.
- **Quote**: "The style of writing functional programs as a sequence of equations with pattern matching over algebraic types goes back at least to Burstall's work on structural induction ... and his work with his student Darlington on program transformation" (line 7)

### algebraic-types-history
- **What**: Algebraic types first appeared in Burstall's NPL and Hope, were absent from original ML and KRC, and appeared in their successors Standard ML and Miranda; conditional guards came from Turner's KRC.
- **Quote**: "Algebraic types as a programming language feature first appeared in Burstall's NPL ... They were absent from the original ML ... and KRC ..., but appeared in their successors Standard ML ... and Miranda ... Equations with conditional guards were introduced by Turner in KRC" (line 11)

### data-constructors-two-roles
- **What**: Data constructors serve both in pattern matching to decompose a value and in expressions to build a value.
- **Quote**: "Data constructors can be used both in pattern-matching, to decompose a value of Maybe type, and in an expression, to build a value of Maybe type." (line 30)

### pattern-matching-increases-readability
- **What**: Pattern matching against algebraic data types greatly increases readability.
- **Quote**: "The use of pattern matching against algebraic data types greatly increases readability." (line 34)

### sum-of-products-from-miranda
- **What**: Haskell took from Miranda the notion of defining algebraic types as a "sum of products", in contrast to Hope and Standard ML which separated sums and products.
- **Quote**: "Haskell took from Miranda the notion of defining algebraic types as a 'sum of products'. ... In contrast, Hope and Standard ML separated sums (algebraic types) and products (tuple types)" (line 43)

### empty-type-not-appreciated
- **What**: A sum of zero alternatives, a completely empty type, might have been useful but its value was not appreciated at the time.
- **Quote**: "It might have been useful to permit a sum of zero alternatives, which would be a completely empty type, but at the time the value of such a type was not appreciated." (line 52)
- **Open**: whether an empty type should be permitted was left unresolved at the time.

### capitalized-constructors-from-miranda
- **What**: Haskell took from Miranda the rule that constructor names begin with a capital, making constructors easy to distinguish from variables, unlike Standard ML's lower case for both.
- **Quote**: "Haskell also took from Miranda the rule that constructor names always begin with a capital, making it easy to distinguish constructors ... from variables ... In Standard ML, it is common to use lower case for both" (line 55)

### capitalization-rule-extended-to-types
- **What**: Haskell extended the capitalization rule to type constructors and type variables, an unusual uniform rule that differed from Standard ML's tick and Miranda's asterisks.
- **Quote**: "Haskell further extended this rule to apply to type constructors ... and type variables ... This uniform rule was unusual." (line 60)

### lazy-pattern-matching-semantics-complex
- **What**: Pattern matching semantics is more complex in lazy languages because the choice to match first against a variable or a constructor can change whether a program terminates.
- **Quote**: "The semantics of pattern matching in lazy languages is more complex than in strict languages, because laziness means that whether one chooses to first match against a variable ... or a constructor ... can change the semantics of a program, in particular, whether or not the program terminates." (line 66)

### top-to-bottom-left-to-right-matching
- **What**: Haskell adopted top-to-bottom, left-to-right equation matching as in SASL, KRC and Miranda; left-to-right matters in a lazy language since a non-match passes to the next equation, avoiding nontermination.
- **Quote**: "matching is from left to right within each left-hand-side—which is important in a lazy language, since as soon as a non-matching pattern is found, matching proceeds to the next equation, potentially avoiding nontermination or an error in a match further to the right." (line 70)

### rejected-matching-alternatives
- **What**: Tightest match, sequential equations, and uniform patterns were considered at length and rejected.
- **Quote**: "after considering at length and rejecting some other possibilities: • Tightest match ... • Sequential equations ... • Uniform patterns" (line 74)

### matching-tradeoff-equational-reasoning
- **What**: Top-to-bottom matching was simple, fit guards, and was more expressive, but the rejected alternatives had an order-independent semantics that aids equational reasoning; the widely used design was chosen over one programmers might find limiting.
- **Quote**: "But the other alternatives had a semantics in which the order of equations did not matter, which aids equational reasoning ... In the end, it was thought better to adopt the more widely used top-to-bottom design than to choose something that programmers might find limiting." (line 86)
- **Open**: a tension between expressiveness/familiarity and equational reasoning, resolved in favor of the former.

### abstract-types-via-module-system
- **What**: Instead of Miranda's special abstype construct, Haskell uses the module system for data abstraction: declare an algebraic type, export the type but hide its constructors.
- **Quote**: "In Haskell, instead of a special construct, the module system is used to support data abstraction. One constructs an abstract data type by introducing an algebraic type, and then exporting the type but hiding its constructors." (line 105)

### abstract-types-tradeoff
- **What**: Haskell's solution is cluttered by the extra constructor but avoids an extra construct and lets operation types be inferred.
- **Quote**: "Haskell's solution is somewhat cluttered by the Stk constructors, but in exchange an extra construct is avoided, and the types of the operations can be inferred if desired." (line 121)

### abstract-type-distinct-class-instance
- **What**: The most important point is that Haskell's approach allows a different type-class instance for the abstract type than for its representation, which it was unclear how to do with abstype.
- **Quote**: "The most important point is that Haskell's solution allows one to give a different instance to a type-class for the abstract type than for its representation ... It was unclear to us how to achieve this effect with abstype." (line 123)

### bottom-value-every-type
- **What**: An expression that diverges or calls error has the value "bottom" (⊥), a value belonging to every type.
- **Quote**: "An expression that diverges (or calls Haskell's error function) is considered to have the value 'bottom', usually written ⊥, a value that belongs to every type." (line 132)

### lifted-vs-unlifted-tuple-semantics
- **What**: There is a choice whether ⊥ and (⊥, ⊥) are distinct: a lifted tuple semantics distinguishes them, an unlifted semantics treats them as the same.
- **Quote**: "are ⊥ and (⊥, ⊥) distinct values? In the jargon of denotational semantics, a lifted tuple semantics distinguishes the two values, while an unlifted semantics treats them as the same value." (line 135)

### unlifted-distinguished-only-by-pattern-matching
- **What**: Under unlifted semantics the two values are indistinguishable except possibly by pattern matching, which can be instead read as binding via fst and snd so the two remain indistinguishable.
- **Quote**: "The only way in which they might be distinguished is by pattern matching ... One can instead consider this definition to be equivalent to ... in which case f ⊥ = True and the two values are indistinguishable." (line 141)

### miranda-currying-isomorphism
- **What**: The semantic point became a controversy in the committee; Miranda identified ⊥ with (⊥, ⊥), which influenced them and made currying an exact isomorphism.
- **Quote**: "Miranda's design identified ⊥ with (⊥, ⊥), which influenced us considerably. Furthermore, this identification made currying an exact isomorphism" (line 166)

### newtype-single-constructor-choice
- **What**: The lifted/unlifted choice arose for any single-constructor algebraic type; from Haskell 1.0 single-constructor types were lifted, and from 1.3 newtype gave a second way to introduce an unlifted single-constructor single-component type.
- **Quote**: "From Haskell 1.0, it was decided that algebraic types with a single constructor should have a lifted semantics. From Haskell 1.3 onwards ... a second way to introduce a new algebraic type with a single constructor and a single component, with an unlifted semantics." (line 206)
- **Also at**: lines 151

### newtype-motivation-isomorphic-abstract-types
- **What**: newtype's main motivation was abstract data types: lifting made Stack not quite isomorphic to lists by adding a bottom distinct from Stk ⊥, and newtype defines a type isomorphic to an existing one.
- **Quote**: "The main motivation for introducing this had to do with abstract data types. It was unfortunate that the Haskell definition of Stack given above forced the representation of stacks to be not quite isomorphic to lists ... We can view this as a way to define a new type isomorphic to an existing one." (line 152)

### lifted-decision-and-tilde-patterns
- **What**: In the end tuples and algebraic data types were made lifted so pattern matching always induces evaluation, with an uneasy compromise of reintroducing lazy matching via tilde-patterns.
- **Quote**: "we decided to make both tuples and algebraic data types have a lifted semantics, so that pattern matching always induces evaluation. However, in a somewhat uneasy compromise, we also reintroduced lazy pattern-matching, in the form of tilde-patterns" (line 184)

### let-where-always-lazy-wart
- **What**: Pattern matching in let and where clauses is always lazy, unlike case/λ; this difference can be considered a wart that complicates the language description.
- **Quote**: "pattern matching in let and where clauses is always lazy ... (This difference in the semantics of pattern matching between let/where and case/λ can perhaps be considered a wart on the language design—certainly it complicates the language description.)" (line 193)

### records-omitted-despite-usefulness
- **What**: One of the most obvious omissions from early Haskell was records with named fields, despite their usefulness in practice.
- **Quote**: "One of the most obvious omissions from early versions of Haskell was the absence of records, offering named fields. Given that records are extremely useful in practice, why were they omitted?" (line 172)
- **Open**: the text poses the question of why records were omitted, answered in following entries.

### single-constructor-sharing-tuple-properties-difficulty
- **What**: A difficulty was whether single-constructor data types should share tuple properties, with a semantic discontinuity appearing when a second constructor is added.
- **Quote**: "should single constructor data types ... share the same properties as tuples, with a semantic discontinuity induced by adding a second constructor?" (line 176)
- **Open**: left as a difficulty, not resolved in favor of either answer here.

### unlifted-tuples-incompatible-with-seq
- **What**: The unlifted form of tuples is essentially incompatible with seq, since parallel evaluation would be required to implement seq on them; efficiency and space leaks of lazy matching were also concerns.
- **Quote**: "the unlifted form of tuples is essentially incompatible with seq ... because parallel evaluation would be required to implement seq on unlifted tuples." (line 181)

### records-no-right-design
- **What**: The strongest reason records were omitted was that there was no obvious "right" design: many record systems exist, all complicating an already complicated type system, and type classes could encode some of their power.
- **Quote**: "The strongest reason seems to have been that there was no obvious 'right' design. There are a huge number of record systems ... All of them have a complicating effect on the type system ... type classes could be used to encode at least some of the power of records." (line 211)

### minimalist-record-syntax
- **What**: Under user pressure, Haskell 1.3 adopted Mark Jones's minimalist design: record syntax is syntactic sugar for operations on regular algebraic data types, with no record polymorphism or subtyping.
- **Quote**: "the committee eventually adopted a minimalist design originally suggested by Mark Jones: record syntax in Haskell 1.3 ... is simply syntactic sugar for equivalent operation on regular algebraic data types. Neither record-polymorphic operations nor subtyping are supported." (line 216)

### minimal-records-leave-field-open
- **What**: The minimal design left the field open for more sophisticated proposals such as TRex, with new proposals and type-class encodings continuing to appear.
- **Quote**: "This minimal design has left the field open for more sophisticated proposals, of which the best documented is TRex ... New record proposals continue to appear regularly on the Haskell mailing list" (line 222)

### nat-type-inefficient-unary
- **What**: A type isomorphic to the natural numbers allows pattern matching in definitions but its unary representation is far less efficient than built-in integers.
- **Quote**: "This definition has the advantage that one can use pattern matching in definitions, but the disadvantage that the unary representation implied in the definition is far less efficient than the built-in representation of integers." (line 230)

### n-plus-k-patterns
- **What**: Haskell provides n+k patterns to get the benefits of pattern matching without the loss of efficiency; n+k matches m only if m ≥ k and binds n to m − k, and can be seen as a special case of a view with convenient syntax.
- **Quote**: "Haskell provides so-called n+k patterns that provide the benefits of pattern matching without the loss of efficiency. (The n+k pattern feature can be considered a special case of a view ... combined with convenient syntax.)" (line 232)

### n-plus-k-origin
- **What**: n+k patterns were suggested by Wadler, who first saw them in Gödel's incompleteness proof, and were earlier in Darlington's NPL and (at Wadler's instigation) in Miranda.
- **Quote**: "Patterns of the form n+k were suggested for Haskell by Wadler, who first saw them in Gödel's incompleteness proof ... They were earlier incorporated into Darlington's NPL ... and (partially at Wadler's instigation) into Miranda." (line 243)

### n-plus-k-controversy
- **What**: n+k patterns provoked controversy: some found them essential for defining functions by cases over the naturals, others worried that Int did not denote the natural numbers.
- **Quote**: "Some users considered n+k patterns essential, because they allowed function definition by cases over the natural numbers ... But others worried that the Int type did not, in fact, denote the natural numbers." (line 251)

### n-plus-k-overloading-complexity
- **What**: Because numeric literals were overloaded, fib's type consistently became Num a => a -> a (one could apply fib to matrices), substantially increasing the complexity of pattern matching, which now had to invoke overloaded comparison and arithmetic.
- **Quote**: "it seemed only consistent that fib's type should be fib :: Num a => a -> a ... This gave rise to a substantial increase in the complexity of pattern matching, which now had to invoke overloaded comparison and arithmetic operations." (line 255)

### n-plus-k-syntactic-ambiguity
- **What**: n+k produced syntactic niceties where apparently redundant brackets change meaning: n + 1 = 7 defines +, while (n + 1) = 7 defines n.
- **Quote**: "n + 1 = 7 is a (function) definition of +, while (n + 1) = 7 is a (pattern) definition of n—so apparently redundant brackets change the meaning completely!" (line 264)

### n-plus-k-horse-trading
- **What**: The majority of the committee suggested removing n+k patterns; in rare horse-trading, Hudak tried to convince Wadler, who agreed only if another feature went, and in the end n+k patterns stayed.
- **Quote**: "One of the very few bits of horse-trading in the design of Haskell occurred when Hudak ... tried to convince Wadler to agree to remove n+k patterns. Wadler said he would agree to their removal only if some other feature went ... In the end, n+k patterns stayed." (line 270)

### views-ease-abstraction-tension
- **What**: Wadler noticed a tension between the convenience of pattern matching and the advantages of data abstraction, and suggested views to lessen it; a view specifies an isomorphism letting constructors of an algebraic type appear in patterns matching the other type.
- **Quote**: "Wadler had noticed there was a tension between the convenience of pattern matching and the advantages of data abstraction, and suggested views as a programming language feature that lessens this tension. A view specifies an isomorphism between two data types ... and then permits constructors of the second type to appear in patterns that match against the first" (line 277)

### views-removed
- **What**: The original Haskell included views, based on constructors and views being indistinguishable, which complicated export lists and derived type classes; by April 1989 Wadler argued the language could be simplified by removing them.
- **Quote**: "The original design of Haskell included views, and was based on the notion that the constructors and views exported by a module should be indistinguishable. This led to complications in export lists and derived type classes, and by April 1989 Wadler was arguing that the language could be simplified by removing views." (line 284)

### views-never-returned
- **What**: Despite Peyton Jones wanting views in an experimental extension and a detailed 1.3 proposal by Burton and others, views never made it back into the language or into implementations.
- **Quote**: "a detailed proposal to include views in Haskell 1.3 was put forward by Burton and others ... But views never made it back into the language nor appeared among the many extensions available in some implementations." (line 288)

### views-tried-and-true-criterion
- **What**: Views or similar features are discussed for Haskell′ but are unlikely to be included because they do not satisfy the criterion of being "tried and true".
- **Quote**: "they are unlikely to be included as they do not satisfy the criterion of being 'tried and true'." (line 296)
