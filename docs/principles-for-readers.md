# Luthier: the ideas behind it

Draft 1, 2026-10-12, unapproved. Draft 0 (f3fb261) received five corrections from Luciano
(afdd7c7); draft 1 writes them into the text, each marked "(draft 1)". Written for a reader who programs or does science and wants to
know what Luthier is for, without the apparatus. The prose is the model's; Luciano's own words,
the sources and the history of each idea are in `record/principles-language.md`, and every
paragraph here names, in parentheses, the entry it rests on. The version for the people writing
the specification is `docs/principles.md`.

## What Luthier is

Luthier is a language for saying what a computation must satisfy, and then checking that an
implementation satisfies it. A theory is a type together with its laws. A model is a value of that
theory, something that claims to satisfy the laws. Luthier verifies models of theories. A single
function is the smallest case: a theory with one symbol, whose laws say what the function must do
(G2). (Draft 1, his correction) A type here is not a bare set of values. It has structure: the
data it holds and the functions defined on that data, and the laws are statements about those
functions (G2). Version 0 tests; it does not prove.

Here is the whole idea in one example. The integers modulo 7 form a ring. In Luthier you declare
the type `Z7`, write addition, multiplication and negation on it, and then declare
`ringZ7 : CommutativeRing Z7`. That declaration is a claim: these operations satisfy the ring
laws. Running `test ringZ7 exhaustive` checks every law over every element, 343 cases for
associativity, and records the result. Defining the model defined its test (L3).

## The guide

The guide is type theory. A type is, or at least represents, a proposition, and a value of the
type is a proof of it (draft 1, his wording). A law
is a proposition about terms, so it carves out a mathematical object: everything that satisfies
the law. Two implementations that satisfy the same laws are, for the purposes of the law,
interchangeable (G0). Luthier follows type theory as far as it goes and departs from it in three
places, each time because type theory lacks something a working scientist needs.

## The first departure: a function is known by its laws

Type theory knows a function by its term, the code that computes it. Luthier knows a function by
its description: the laws it satisfies. The code, native or borrowed from Python, is a specimen
under observation, and the laws are what is known about it. This is the eureka that started the
project: the type of a function is the set of laws that define it (G2). (Draft 1, his correction)
Often, though, a law speaks of several functions at once: associativity needs an operation, an
inverse law needs the operation, the inverse and the unit. Such functions are not isolated; together
they form a model of a theory. So the unit of Luthier is the pair, a model of a theory: the claim,
backed by evidence of some grade, that a set of functions on a data type satisfies the theory's laws
(G2). A function is declared inside a theory and is written once for every model of that theory, so
the code that works for one ring works for every ring (L20).

Belonging to a type is therefore a guarantee, and the guarantee says exactly how strong it is. A
value carries a certificate for each law it was checked against, with a grade: proved, by citing a
theorem or by delegating to a software library that carries its own guarantee (draft 1, his
correction), exhaustive over every case, checked on chosen cases, sampled statistically at a stated
level, or merely assumed (L2, L11). The basic building block is a type carved out of a bigger one
by a predicate, which gives three things at once: the new type, its only constructor, and the
function that says whether a value belongs (L4). A law characterizes an operation
mathematically; it does not re-run a second copy of the code and compare (L5). And checking that
an implementation still gives the same bits as yesterday is a different thing from checking that
it satisfies its laws; Luthier keeps the two certificates apart, and lets a certificate of the
law travel along a certificate of identity, at the weaker of the two grades (L21).

Declaring comes before defining, and defining before inhabiting. A name declared without a body
is a hole: it may be an axiom, an input, an external function, or something not yet written.
Nothing runs until it is defined, and nothing inhabits a type that has not been defined (L8).

## The second departure: the demand decides what runs

In type theory, computation is the normalization of a term you already have. Luthier adds an
executive face. A program states what is known, as universally as possible. Nothing is computed
until something outside asks for a value: a print, a file saved, a test. That demand names the
type it wants and the tolerance it accepts, and from those Luthier works out which path to
compute and which types are actually produced (G1).

A program is therefore a graph of definitions, not a sequence of steps. The order of statements
in the file does not matter; dependencies give the only order there is (L9). A definition has no
side effects; effects live only in actions, and that is the one assumption under which every
evaluation strategy gives the same result (L18). The default strategy plans backward from the
actions over the names they need, then runs forward over that live subgraph, each node once; a
test is an action too, so verifying is a form of demanding (L19). What the demanded value does
not need is forgotten, which is how Luthier avoids carrying the whole history of a computation in
its types (L13). Every threshold, budget and statistical level is a parameter passed with the
demand, never a constant hidden in the code (L17).

Evaluation is verification: Luthier checks equivalences rather than executing instructions.
Execution proper is an action on the world, and an action is verifiable too (draft 1, his word), by
observing the world before and after it (L12). Code that does not follow Luthier's way, say a foreign algorithm taken
as is, can still run, inside a named world, with its certificates marked as assumed, until a law
is certified for it (L22).

## The third departure: laws have a cost, and a run teaches something

Type theory has two truth values. That works for integers and breaks on floating point, on
linear algebra, on statistics, where a law holds up to an error. Luthier values a law in a
non-negative cost: zero is true, infinity is false, and the demand supplies the tolerance it will
accept. Boolean laws and cost-valued laws coexist, and the bridge between them is explicit. Over
floats the cost itself is estimated, so the evidence for a law is uncertain and composes as Bayes
composes evidence, and what a run teaches is kept for the next one (G3). This is the least
developed part of Luthier, and its author calls it a wish as much as a principle.

Code is written over ideal objects, real numbers, and realized by concrete ones, 64-bit floats.
The realization satisfies the ideal laws within a stated tolerance, and the error of each step is
itself a law rather than a false claim of exactness (L15). Equality has levels: definition,
identity, decidable equality, equality by reduction, and each object carries the one that fits it
(L16).

## One function, many paths

A function has many implementations: fast or precise, in memory or on disk, native or borrowed.
Luthier first establishes which of them are equivalent, by their laws and by certified identity
between pairs, and only then chooses among them by cost: expected error, time, memory, each a
parameter of the demand rather than the planner's own opinion. An implementation that has never
been compared is never substituted (L10). Luthier borrows freely from other languages: values may
come from Python or any host through `extern`, declared over what they really receive and
return, validated against their laws the first time they are asked for, and refused if they fail.
In practice Luthier is a coupling language, the joint where two libraries meet under one theory
(L14).

## The small core

The core is a handful of primitives, small enough that a program can be run with pencil and paper
given a plan of execution; everything else is a library whose translation to the core is
mechanical (L7). A Luthier program is itself a value of Luthier, so programs can build, inspect
and run other programs, and the interpreter is meant to be written in Luthier (L6). What moves
all of this is the wish to state the invariances of a discipline in the language itself: a
species mates within itself, electrons are fermions, a probability integrates to one (L1).

## What is still open

The algebra of costs is not written: how tolerances compose along a chain of computations, how a
rounding error and a condition number enter a certificate, how evidence from many runs is kept.
Actions on the world and the world itself as a value are designed but not implemented. The
author's own analysis of the extension from Boolean logic to Lawvere and Bayes is pending, and he
has not yet said whether it is a third eureka or a rule of good use (G3).
