# Luthier: the ideas behind it

Draft 6, 2026-10-12, unapproved: the prose rewritten against draft 11 of `docs/principles.md`
(three organizers, thirteen principles, the certificate as an entry of its own), so that it says
what the principles say today and no earlier decision survives in it by inertia. Luciano's
corrections of drafts 1 and 2 are kept where they stood, marked as before. Drafts 2 to 5 are in
the history: draft 0 (f3fb261) received five corrections from Luciano (afdd7c7); draft 1 (43d7796)
wrote them into the text, each marked "(draft 1)"; draft 2 applied his decisions of the same day
(D-2026-10-12-e, -f), marked "(draft 2)"; drafts 3 to 5 only renumbered the citations. Written for
a reader who programs or does science and wants to know what Luthier is for, without the
apparatus. The prose is the model's; Luciano's own words, the sources and the history of each idea
are in `record/principles-language.md`, and every paragraph here names, in parentheses, the entry
it rests on. The version for the people writing the specification is `docs/principles.md`.

## What Luthier is

Luthier is a language for saying what a computation must satisfy, and then checking that an
implementation satisfies it. A theory is a type together with its laws. A model is a value of that
theory, something that claims to satisfy the laws. Luthier verifies models of theories. (Draft 1,
his correction) A type here is not a bare set of values. It has structure: the data it holds and
the functions defined on that data, and the laws are statements about those functions (G1).
(Draft 2, his decision) The common case is a theory with a single symbol: a function type with its
laws, over types that are already modelled, with their equality. Its model is a function in the
ordinary sense, and the laws say what that function must do with respect to what was there (G1).
Version 0 tests; it does not prove.

Here is the whole idea in one example. The integers modulo 7 form a ring. In Luthier you declare
the type `Z7`, write addition, multiplication and negation on it, and then declare
`ringZ7 : CommutativeRing Z7`. That declaration is a claim: these operations satisfy the ring
laws. Running `test ringZ7 exhaustive` checks every law over every element, 343 cases for
associativity, and records the result. Declaring the model declared its tests (G1).

What moves all of this is the wish to state the invariances of a discipline in the language
itself: a species mates within itself, electrons are fermions, a probability integrates to one
(L1).

## The guide

The guide is type theory. A type is, or at least represents, a proposition, and a value of the
type is a proof of it (draft 1, his wording). A law is a proposition about terms, so it carves out
a mathematical object: everything that satisfies the law. Two implementations that satisfy the
same laws are, for the purposes of the law, interchangeable. Type theory guides what is declared;
what governs execution is a demand from outside, read in the same theory: a demanded type is a
judgment to inhabit, and where type theory normalizes a term it already has, Luthier searches for
one (G0). Luthier follows type theory as far as it goes and departs from it in two places, each
time because type theory lacks something a working scientist needs.

## The first departure: a value is known by the laws it satisfies

Type theory knows a function by its term, the code that computes it. Luthier knows it by its
description: the laws it satisfies. The code, native or borrowed from Python, is a specimen under
observation, and the laws are what is known about it. This is the eureka that started the
project: the type of a function is the set of laws that define it (G1). (Draft 1, his correction)
Often, though, a law speaks of several functions at once: associativity needs an operation, an
inverse law needs the operation, the inverse and the unit. Such functions are not isolated; together
they form a model of a theory. So the unit of Luthier is the pair, a model of a theory: the claim,
backed by evidence of some grade, that a set of functions on a data type satisfies the theory's laws
(G1). (Draft 2, his decision) Even a function that seems to stand alone does not: every law is an
equality, and the equality of the type it returns is itself a function with laws, which the new
function must respect. An isolated function has no sense; it has sense in a context, and a function
that looks isolated is one whose inverse and whose theory nobody has yet taken the trouble to find.
The exponential looks like a lone function until you ask for its inverse, the logarithm, and for the
theory it belongs to: it carries addition to multiplication, and that law is what Luthier checks
(G1).

Belonging to a type is therefore a guarantee, and the guarantee says exactly how strong it is. A
value with a sampled or assumed certificate is still a model of its theory, with the cost its
certificate records; the word model promises the evidence, not exactness. The basic building block
is a type carved out of a bigger one by a law, which gives three things at once: the new type, its
only constructor, and the function that says whether a value belongs (L8). A law characterizes an
operation mathematically; it does not re-run a second copy of the code and compare. What produces
the evidence for a law is a certifier, and one law may have several: a theorem cited, by name or by
delegating to a software library that carries its own guarantee (draft 1, his correction), an
exhaustive run over every case, chosen cases, a statistical sample, or an assumption. Checking
that an implementation still gives the same bits as yesterday is a different thing from checking
that it satisfies its laws; Luthier keeps the two certificates apart (L9).

In Luciano's words, a law is evidence of nothing until a wrong model refutes it. So every law
carries, beside its evidence, a negative control: a model broken on purpose, which the law must
refute. A law that no broken model can fail describes nothing, and a run that passes never shows
it; the external review of one layer of Luthier found three such laws, among them a gradient law
that a score of zero passed. A law made of parts joined by "and" is controlled part by part, and
the control does not stop at the first part it refutes: a broken monoid caught by associativity
says nothing about whether the law of the neutral element would have caught it. A theory is done
when every part of every law has a model it refuted (L9).

The certificate is the object everything else leans on. It records what is known of a law: the
domain the check covered, the bound observed, and the evidence, which is a cost: zero for a
theorem or an exhaustive run, zero for chosen cases on the cases listed and infinite elsewhere, a
finite cost for a sample, computed from its statistics, and for an assumption the cost the
demander is willing to pay for it, which no default supplies. The strength of a certificate is
therefore a pair, the domain it covers and the cost of its evidence there, and the five grades
are names for the reader. Three chosen cases say nothing about a fourth input, where a sample
does say something, so neither grade outranks the other; a theorem, an exhaustive run and chosen
cases are one kind, exact on a stated domain. A demand is met by a certificate whose domain covers
its input and whose cost is within the demand's cutoff. The interpreter, whose laws are still
Boolean, ranks the five grades in one line until the cost types exist. For a sample the evidence
is itself a pair: ε̂, a bound on the fraction of the sampled distribution where the law fails, and
δ, the chance that this bound is wrong, which the demand chooses. A single number can be made of
the pair, but that number is a reading of it, and adding such numbers along a chain is sound only
when the failures are declared independent. A certificate is frozen; a later check does not change
it but issues a new one that supersedes it, and progress is the chain of certificates. A
certificate serves every demand whose cutoff it meets, and it travels: if one implementation is
certified and another is certified equal to it within some distance, the second inherits the
first's guarantee, the bound and the evidence cost added up, on the inputs both cover, and on
nothing else. Two sampled links compose when they were sampled over the same distribution, by
adding their chances of failure, capped at one. The sum is the default because it assumes nothing
about how the failures depend on each other: two links at ε̂ = 0.1 compose to 0.2, where
independence would allow 0.19. The rule of composition is a parameter of the demand, and Luciano
asked that Luthier provide the mechanism to define any reasonable rule, provided none can loop;
reasonable means that a composition never knows more than either of its parts. Nothing raises a
grade or widens a domain without new evidence (L10).

Evidence serves what it is about, and nothing else. A law that passes on one model is evidence
about that model; a run on another model of the same theory needs passes of its own. A failure
counts against the model it failed on, with one exception: when a law is stated for every model of
a theory and fails on a model that satisfies the theory's defining laws, the law does not follow
from the theory, and the failure counts against every model. A control is about the law: that the
law refutes a broken model holds whatever model it is later checked on, so one control serves
every model of the theory. What a run observes of one result, the residual on these inputs or the
error a crossing between languages added, is about that result: it goes into the result's
derivation and the run's record, and it changes no certificate of the model. So the certificate of
a model, the evidence of one computation and the derivation of its value are three records; a
derivation names the certificates its route relied on, a certificate names no result, and no
object carries all three. The interpreter has kept passes, failures and controls apart this way
since 2026-10-22; the principle that says it, with the derivation, is proposed (L10.13).

Declaring comes before defining, and defining before inhabiting. A name declared without a body
is a hole: it may be an axiom, an input, an external function, or something not yet written.
Nothing runs until it is defined, and nothing inhabits a type that has not been defined (L2).
Equality has levels: definition, identity, decidable equality, equality by reduction, and each
object carries the one that fits it, Boolean where its carrier is decidable and a distance where it
is not (L3).

## The second departure: laws have a cost

Type theory has two truth values. That works for integers and breaks on floating point, on
linear algebra, on statistics, where a law holds up to an error. Luthier values a law in a
non-negative cost: zero is true, infinity is false, and the Booleans are the special case (G2).
Boolean laws and cost-valued laws coexist and combine: predicates by and, or and quantification,
costs by sum, maximum and weighted sum, and a predicate lifts to a cost by an explicit bridge, so
a Boolean law is a cost law with two values and nothing is promoted silently. How the costs of the
laws of one theory combine is the theory's own algebra; how a demand reads them is the demand's
parameter; and the one thing that does not compose is the cutoff, which is why it lives in the
demand and in no law (L12).

In Luciano's words, what was first called cost is four things: the error, a bound carried by a
value and propagated through the computation; the uncertainty, the value read as a distribution;
the evidence, what a certificate knows on a finite budget; and the resources a run spends. Error
and uncertainty are data, carried with a value when a demand asks for them, and a law is a claim
about them at a bound. Each composes in its own way. Errors add. The evidence of a sample is the
pair described above, composed by the capped sum. The resources are a vector of work, the total
number of steps, span, the longest chain of steps that must run one after another, and peak
memory: work adds in sequence and in parallel, span adds in sequence and takes the maximum in
parallel, and peak memory takes the maximum in sequence and adds in parallel (L6; proposed, except for the
evidence, which is settled).

Code is written over ideal objects, real numbers, and realized by concrete ones, 64-bit floats.
The realization satisfies the ideal laws within a stated tolerance, and the error of each step is
itself a law rather than a false claim of exactness. Rounding from the reals to the doubles is a
functor in Lawvere's sense (draft 1, his reading), non-expansive up to an additive defect, so the
algebra of costs needs both a multiplicative part, where a Lipschitz constant exists, and an
additive one, where rounding enters. That shape is now settled. A numerical law is carried by four
things: a sensitivity L, the algorithm's own error η, a domain D and a radius r; it says that the
output's error is at most L times the input's error plus η, for inputs in D with errors below r.
Two such laws compose along a computation, the sensitivities multiplied and the first error
carried through the second sensitivity before the second error is added. Read backward from a
demand that tolerates an error ε in the output, the input may carry an error of (ε − η)/L; a
tolerance below η cannot be met at any price, and where L is unknown no implementation is
substituted for another (L13). Beyond this and the evidence of a sample, the algebra of costs is
the least developed part of Luthier, and its author calls it a wish as much as a principle.

## The demand decides what runs

In type theory, computation is the normalization of a term you already have. In Luthier nothing
is computed until something outside asks for a value: a print, a file saved, a test. That demand
names the type it wants, possibly decorated, the value with its error, its derivative or its
certificate, the cutoff it accepts on the bound and on the evidence, and the trade-off it is
willing to make between precision and resources. From those Luthier plans backward from the
demand over the names it needs, then runs forward over that live subgraph, each node once and
whole. What the demanded value does not need is not produced, which is how Luthier avoids carrying
the whole history of a computation in its types. The history is still there for a demand that
wants it: a value has a derivation, and a demand may ask for the value with its derivation as it
asks for the value with its error (L5.23). A result is identified by everything that made
it: the code, the inputs, the demanded type and tolerance, the seed, the plan, and the
certificates in its cone, so a changed library is a new result. Three objects, never one: the
meaning of a program, which its laws fix; a realization, the result under a plan; and the
evidence, its certificates. Every threshold, budget and statistical level is a parameter passed
with the demand, never a constant hidden in the code; the kernel's own zero and infinity are not
policies (L5).

What follows in this paragraph is proposed, on Luciano's idea of 2026-10-22, and waits for his
mark on the wording. The derivation of a value is the account of how it was obtained, kept to what
changes what a law or a demand can say of it: the inputs it descends from, the models and
specimens that produced it, the bridges it crossed between languages, the certificates its route
relied on, and the roots of trust it rests on, the parts nothing checks, such as the file system
or the floating-point hardware. It is the trace of the run read only as far as the theories can
observe, so `(a + b) * 1.0` and `a + b` have one derivation wherever no law tells them apart. In
his reading the derivation is the realization itself, a function applied to its input, taken as a
value, so the three objects stay three. Whether two realizations are equal in consequence is a
certified relation between them, computed when a demand asks for it, and a result keeps the
identity of its own realization as its key (L5.22). A value carries no more of its derivation than
its demand asks for: a 64-bit float stays a 64-bit float until a demand wants the value with its
derivation, one more decoration beside the error, the derivative and the certificate. A
requirement on the derivation, say that nothing in it was assumed, is a law over it, so the values
that meet it form a certified subtype a demand can name like any other type (L5.23). The word is
his; it has nothing to do with the derivative, the differential a demand may also ask for.

A program is therefore a graph of definitions, not a sequence of steps. The order of statements
in the file does not matter; dependencies give the only order there is, and inside a block the
text only fixes which binding a name means. A definition has no side effects; effects live only
in actions, and that is the one assumption under which every evaluation strategy gives the same
result. An action is verifiable too (draft 1, his word), by observing the world before and after
it, where the world can be read back; what cannot be read back is logged and audited, never
verified. An action on Luthier's own state, writing a certificate, is memoizable; an action on the
world never is (L4).

## One function, many specimens

A function has many implementations: fast or precise, in memory or on disk, native or borrowed.
Luthier first establishes which of them are equivalent, by their laws and by certified identity
between pairs. In the theory, implementations that compute the same function form a class; in a
model that carries a distance there is no class, since closeness is not transitive, only a graph
of certified substitutions, and the planner moves only along its edges, adding up distances and
evidence as it goes. Among the admissible ones it chooses by the performance the demander asked
for: an efficiency that trades the cost of a law against the resources of a run, time and memory,
with the weight the demand's own, never the planner's opinion. An implementation that has never
been compared is never substituted (L6).

Luthier borrows freely from other languages: values may come from Python or any host through
`extern`, declared over what they really receive and return, validated against their laws the
first time they are asked for, and refused if they fail. In practice Luthier is a coupling
language, the joint where two libraries meet under one theory. Code that does not follow Luthier's
way, say a foreign algorithm taken as is, can still run, inside a named world, its certificates
carrying the cost of an assumption, and nothing from it enters the planner's graph nor a certified
theory until a law is certified for it (L11).

What follows is proposed, on Luciano's idea of 2026-10-22. A value crosses from one language to
another without losing what Luthier knows of it. A crossing changes the representation, the host
or the place where the value is computed; its theory, its evidence and its derivation stay on
Luthier's side and go through with it, so whoever receives the value needs to read only its type
and the evidence that comes with it, never the language that produced it. A bridge between two
languages declares what it preserves, what it adds (the error and the resources of the
conversion), what it takes on trust, and what it can no longer certify, and what is lost is lost
by a declared bridge, never by the crossing itself (L11.10). That is what orchestrating means, in
his image of a conductor. The hosts compute, and may compute most of a program. Luthier states the
theories, knows which implementations in the hosts are their specimens, keeps the evidence, places
the bridges, composes the derivation across them, and answers a demand with a result that meets
the theory, the evidence and the tolerance asked for. Take raw measurements calibrated in Python,
fitted in Julia and solved by LAPACK: the estimate's derivation names the three implementations
with their versions, the two bridges with the error each added, the certificates each step relied
on and the roots of trust, and a demand carries as much of it as it asks for. Of such a value one
can then ask what it means, how it was obtained, what it assumed, and which laws justify using it,
as far as the demand asks and the evidence certifies. Composing derivations across hosts comes
with the planner, which is built after certification since it substitutes only along certified
identities (L11.11).

## The small core

The core is a handful of primitives, small enough that a program can be run with pencil and paper
given a plan of execution; everything else is a library whose translation to the core is
mechanical. A Luthier program is itself a value of Luthier, so programs can build, inspect and run
other programs, and the interpreter is meant to be written in Luthier (L7). More generally, what can be written in Luthier is written in
Luthier: how Luthier runs is itself stated as theories in Luthier, and the Python that runs it today
is one implementation checked against them (L14).

## What is still open

The algebra of costs is not written: two candidate models, how a rounding error and a condition
number enter a certificate, how the conversion from a sample's statistics to a cost is declared
per theory. The syntax by which a demand opts out of certification, and the world as a value so
that an action is never served from a cache, are designed and not implemented. The author's own
analysis of the extension from Boolean logic to Lawvere and Bayes is pending, and he has not yet
said whether it is a third eureka or a rule of good use (G2).
