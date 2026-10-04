# Static semantics: names, states, and the dependency graph

Draft 0, 2026-10-04, revised the same day after the voice notes of 12:16 and 12:17. What the
checker decides about a program before anything runs. It settles what the voice note of
10:28 asked for: that declaring a type and defining it be two different acts, that a
definition verify something, and that the objects of a program be the groups of names
whose laws hold them together. Everything here was discussed and decided in the session of
that day; where a point stayed open it is listed in section 7.

This document supersedes the parts of `00`, `01`, `02` and `03` it contradicts; those files
carry notes pointing here. Written in English, as everything written from 2026-10-01 on; the
earlier documents stay in Spanish until they are rewritten.

## 0. Notation

Every symbol used in this document.

- `x : T` reads "x refines T". It is the one relation of the language (section 1). `x : T := t`
  gives `x` a body `t`. A name with a type and no body is a hole.
- `x = t` makes `x` an alias of the term `t` (rule R8): an abbreviation, not a name with states.
- `U` is the universe, the type whose inhabitants are types. `Bool` is the two-valued data
  type; `Law` is the type of a conjunction of quantified Bool-valued laws (`p & q`).
- A *name* is a top-level definition, qualified by its module prefix (`03 §2`).
- `D(n)` is the set of names that occur in the declared type of `n`; `B(n)` the set that occur
  in its body. Occurrence is syntactic, after elaboration and after expanding aliases
  (constructors stand for their data type; a projection `e.f` counts the names in `e`).
- The *dependency graph* is directed: the names are its nodes and `n -> m` is an edge whenever
  `m ∈ D(n) ∪ B(n)`. It gives the order of checking and the cone of a certificate (`03 §4`).
- A *law* is a Bool- or Law-valued definition, or one conjunct (split at `&`) of the predicate
  that defines a type. A law *touches* the names that occur free in it.
- The *law hypergraph* is undirected: its nodes are the holes, the types defined by a
  predicate, and the labels of their bases; each law is a hyperedge over the nodes it touches.
- A *cluster* is a connected component of the law hypergraph. A node no law touches is a
  cluster of one, with no law.
- `data { ... }` declares an inductive type by its constructors (`00 §3`).
- `extern "python:mod.fn"` gives a name the environment's implementation (`03 §3`).

## 1. One relation, four states

Everything is a type; a value is a type with exactly one inhabitant. `4` is
`{ n : Int | n == 4 }`. `x : T` says that `x` is a refinement of `T`: a subset of its
inhabitants, possibly a singleton. The distinction between types and values does not
disappear from the surface (the reader needs to know what reduces), but it is not a
distinction in kind: it is a difference in how far a name is determined.

A name has four states, the same at every level (`T : U` and `t : T` alike):

| state | what is known | how it is reached |
|---|---|---|
| declared | its base: `x : T` | a definition without body |
| defined | its cluster has laws, and they reach every node of the cluster (R3) | the laws are stated, in the same file as the declaration or another |
| determined | it has a body: a term, a `data`, or an `extern` | `:=` |
| certified | its laws passed a `test` whose hash still matches (`03 §4`) | `luthier test` |

Defined and determined are independent axes. A hole can be defined (its laws are written, no
implementation yet); an `extern` can be determined without being defined (the environment
provides a function nobody wrote laws for). Certification requires both.

What a body does depends on its type, and there is never a choice to make:

- `x : T := t` with `t : T` determines `x` to the inhabitant `t`. The body is itself the law
  `== t`, so `x` is defined by its body.
- `x : T := p` with `p : T -> Bool`, or `p` a `Law` quantified over a `T`, makes `x` the subtype
  `{ y : T | p y }`. Then `x : U`. The two types `T` and `T -> Bool` never coincide, so no
  marker is needed to tell a value definition from a type definition. With `T = U`, `p` is a
  class of types; the same rule applies.
- `x : U := data { ... }` determines and defines `x`: its constructors are its laws.
- `x : T := extern "..."` determines `x` and defines nothing. If `x`'s cluster has no laws, `x`
  is determined but not defined, and rule R2 forbids building on it (rule R6 gives the
  escape hatch).

A declaration of a type gives its base with its labels: `Codec : { parse : String -> Maybe T,
render : T -> String }` declares `Codec` as a refinement of that product, laws pending. The
labels are binder names, like the parameter names of a function: they let the laws say
`c.parse`, and they are not part of the type's identity (rule R4). The definition comes later,
in the same file or another: `Codec := RoundTrip & Canonical & Tolerant & Rejects`.

Operational asymmetry, kept explicit: a body computes, a law only checks. Whether a set of
laws pins down a unique inhabitant is undecidable and is never asked; "determined" means "has
a body". Two bodies for one name (`f#1`, `f#2` of `00 §1`) are two determinations, and their
agreement is a law to test, as the `Agrees` laws of the libraries already do.

## 2. The two graphs

A program is a set of definitions without order (`00 §1`). Order in the file is not
significant, so the checker reads the whole program, imports included, before it checks any
definition:

1. parse every file; collect each name with its declared type and body as written; expand
   aliases (R8);
2. resolve names and build the dependency graph from `D(n) ∪ B(n)`; a cycle in it is not an
   error (a type defined by laws that mention it, as `Codec` in section 6);
3. build the law hypergraph and its clusters;
4. check in an order compatible with the dependency graph (a dependency before what depends
   on it, cycles taken as blocks); inside a block, first every declared type, then every law,
   then every body.

Connected, not circular. The voice note of 12:16 draws the line: a type is an assembly of
other types under laws, and what makes the assembly one type is that the laws reach every
part, whether or not the parts depend on each other in a cycle. Two operations tied by one
law, and a third that both laws mention but that nothing depends on, are one cluster and one
type. The directed graph is for order and for hashes; the units of definition and of closure
(R3, R5) are the clusters. In the style where a file declares holes and another fills them
(section 4), there is no directed cycle at all: the laws depend on the operations, the
operations on the carrier, the carrier on nothing. The cluster is what holds them together.

Dependence is syntactic in this version: a law touches `m` when `m` occurs free in its
elaborated body, without unfolding definitions. A law that mentions a component only
vacuously (`g x and (y == y)`) counts as touching `y`. The semantic criterion (the law is not
separable into a conjunction of laws over disjoint components) is stated in section 7 as a
witness law to add.

## 3. Well-formedness rules

Each rule names its files under `tests/spec/`: one program the checker must accept and one it
must reject, with the fragment of the error message the rejection carries in a
`-- expect:` comment. The suite is the specification applied to the interpreter.

**R1. A declaration mentions declared names.** For a hole `n : T`, every name in `D(n)` is at
least declared: types, type operators applied to declared types, predicates. This is what
allows the forward declarations an object needs.
Files: `r1_declaration.accept.lut`, `r1_declaration.reject.lut`.

**R2. A definition builds on defined names.** For a name with a body, every name in
`D(n) ∪ B(n)` is defined, except when `n` is a law of the cluster that name belongs to. The
exception is what lets the laws of a cluster mention the names they define. A definition that
is not a law, over a type that is merely declared, is generic code, and must take the type
(and what it needs of it, such as its equality) as parameters.
Files: `r2_definition.accept.lut`, `r2_definition.reject.lut`.

**R3. Defined means connected.** A cluster is *defined* when it has at least one law; by
construction its laws then reach every node of it. A node no law touches is a cluster of one
without laws, and is only declared. For a type defined by a predicate over a labeled base,
every label of the base is a node, so every label must be touched. Consequences:
- `{ x : T | true }` is not a definition: `true` touches no node. The `| true` records of the
  first libraries disappear.
- `{ add : A -> A -> A, mul : A -> A -> A | Associative add }` is rejected: `mul` is a label no
  law touches. It is a semigroup juxtaposed to a bare function.
- `Table : U := extern "..."` alone is rejected: an opaque carrier is defined only by laws that
  quantify over its values.
- A `data` needs no law: its constructors define it.
- A value with a term body is defined by that body.
Files: `r3_connected.accept.lut`, `r3_dangling_component.reject.lut`,
`r3_true_predicate.reject.lut`, `r3_extern_type_without_laws.reject.lut`.

**R4. Juxtaposition is not a new type.** A type operator that is defined, applied to defined
types, is a defined type (`A * B`, `List A`, `Maybe (VecOf n)`): a *derived* type, with no laws
of its own. A labeled product without laws, `{ a : A, b : B }`, is the product `A * B` with
names for its positions; it is structural, and two such products that differ only in their
labels are the same type. Giving it a name with `:=` (`C : U := { a : A, b : B }`) is
rejected: it introduces a name that claims nothing. Either declare `C : { a : A, b : B }`
and owe it laws, write the product where it is used, or abbreviate it with `=` (R8).
Files: `r4_product_inline.accept.lut`, `r4_product_named.reject.lut`.

**R5. A cluster is determined all at once.** The holes of a cluster are filled together: at the
end of a file, either none of them has received a body in that file or all of them have. No
new syntax: each `:=` stays one per name, and the rule is judged when the file ends. The file
is the unit that closes an object, which is the reading of a file as a structure in `03 §1`.
Files: `r5_fill_all.accept.lut` (with `r5_theory.lut`), `r5_fill_partial.reject.lut`.

**R6. An extern is a definition, with one escape hatch.** R2 applies to `extern` as to any
body. `extern provisional "python:..."` lifts R2 for the names in `D(n)` that are declared
but not defined: it is the form for working in a hurry on a type whose laws nobody has
written yet. The checker records every provisional definition in the certificate under
`provisional`, with the names it builds on, and `luthier check -v` lists them, so the debt is
visible. A provisional definition is never certified.
Files: `r6_extern_provisional.accept.lut`, `r6_extern_over_declared.reject.lut`.

**R7. The body of a type definition is a predicate over its declared base.** If `C` is declared
`C : T` and later given a body, the body has type `T` (a value) or `T -> Bool` / a `Law` over
`T` (a type definition). Any other type is an error, reported against the declaration.
Files: `r7_predicate_body.accept.lut`, `r7_body_type.reject.lut`.

**R8. An alias is written with `=` and has no state.** `AB = A * B` makes `AB` stand for the
term on the right everywhere it occurs; the checker expands it before anything else, so `AB`
is never declared, defined, determined or certified: it is as defined as what it abbreviates.
An alias may not be declared with `:` nor given a body with `:=`; a name that is both an alias
and a definition is an error. This is the form for naming a derived type without claiming
anything about it (voice note of 12:17).
Files: `r8_alias.accept.lut`, `r8_alias_defined.reject.lut`.

Note on `=`. `00 §0` and `01 §0` reserve `=` for the propositional equality of a later
proof layer. Version 0 has no such layer, and a definition-level `x = t` is distinguishable
from a term-level `a = b` by position, but the two readings will have to be reconciled when
proofs arrive; listed in section 7.

## 4. Two ways to close a cluster

Both exist today in `lib/` and both stay; the rules above only say what each one must
contain.

**Theory as a type, model as a value.** `Ring (A : U)` is a type operator whose definition
is a predicate over a labeled product; `ringZ7 : Ring Z7 := (addMod7, mulMod7, 0, 1, negMod7)`
is a value of it, and `test ringZ7` runs the laws on that value. The cluster of `Ring` holds
`Ring`, the labels `add`, `mul`, `zero`, `one`, `neg`, and the laws; R3 asks that every label
be touched. Nothing is a hole; R5 is vacuous. Here the dependency graph does have a cycle
(`Ring` is defined by laws whose parameter is a `Ring`), and that is fine.

**Holes filled by another file.** `table.lut` declares `Table : U`, `nRows : Table -> Int`,
`intAt : Table -> String -> Int -> Int`, ... and states their laws (row bounds, column types,
what `sameTable` respects). Those laws make one cluster of the carrier and its operations:
defined in `table.lut`, determined by nobody. `table_python.lut` fills every hole of the
cluster with externs (R5), inheriting the laws as obligations; `test` certifies them against
that implementation. A second file could fill the same holes with another implementation
and be certified separately. There is no directed cycle in this style; the cluster is the
object.

The cost of R2, on real code. In today's `table.lut`, `Table` has no laws, so `RoundTrip`,
`sameParse` and `forallBelow` are definitions over a merely declared type and would be
rejected. Two ways out, both intended: state the laws of `Table` in `table.lut` (then the
cluster of `Table` is defined and the codec can build on it), or make the codec generic over
its carrier, `Codec (T : U) (eq : T -> T -> Bool) : { parse : String -> Maybe T, render : T -> String }`.
The first is what the voice note asked for.

## 5. What `test` and `run` do with the states

- The obligations of a name are the laws of its cluster applied to its determination,
  quantified over the laws' parameters (as today, through `Obligation` in the checker).
  `test n` runs the obligations of every member of `n`'s cluster and writes one certificate
  entry per member, each with the hash of its own dependency cone.
- `test` moves a determined and defined cluster to certified. It has nothing to run on a
  cluster that is not determined (a law over a hole does not reduce) and reports it as
  pending.
- `run` and `eval` require every name in the cone of the entry to be determined (`00 §1`:
  what depends on a hole does not reduce). They do not require certification; a run whose
  cone contains uncertified or provisional names records that in its `.run.json`, as the
  certificate hash already lets `check -v` show.
- Importing a file accepts its certificate entries by hash, unchanged (`03 §4`). A
  provisional definition has no entry to accept.

## 6. Example: `Codec`, one name, three states

    import "table"

    -- declared: base and labels, no law yet
    Codec : { parse : String -> Maybe Table, render : Table -> String }

    -- the laws: definitions over Codec, legal by the R2 exception (they are its cluster's laws)
    RoundTrip (c : Codec) (t : Table) : Bool := sameParse (c.parse (c.render t)) (just Table t)
    Canonical (c : Codec) (s : TableText) : Bool :=
      match c.parse s { nothing -> true ; just t -> sameParse (c.parse (c.render t)) (just Table t) }
    Tolerant (c : Codec) (p : Perturbed) : Bool := sameParse (c.parse p.text) (just Table p.table)
    Rejects (c : Codec) (b : BrokenText) : Bool := match c.parse b { nothing -> true ; just t -> false }

    -- defined: the body is a Law over Codec, so Codec is the subtype it names (R7, R3)
    Codec := RoundTrip & Canonical & Tolerant & Rejects

    -- a value of Codec: determined; its obligations are the four laws
    csv : Codec := { parse := parseTable, render := renderTable }
    test csv with 200

`RoundTrip` touches `parse` and `render`; both labels are reached, so R3 holds. The former
pair `Codec` / `LawfulCodec` is one name. `Perturbed`, today
`{ table : Table, text : String | true }`, is rejected by R3: its invariant ("the text has the
content of the table") lives in its generator and has to be written as its law; otherwise
`Perturbed = Table * String` is the alias to write (R8).

## 7. Open

- The semantic criterion of dependence. A law `P` over components `x`, `y` is separable when
  `P(x, y') and P(x', y)` implies `P(x, y) and P(x', y')` for all `x, x', y, y'`. "P connects x
  and y" is the existence of a witness where that fails. It is testable, but it is an
  existential: the test looks for a witness, not a counterexample, and the certificate needs
  a verdict `witnessed` beside `sampled n`. Version 0 uses the syntactic criterion of
  section 2.
- `=` as alias (R8) against `=` as the identity type of `00 §4`, when the proof layer comes.
- Implicit arguments. R2 makes code over a declared type generic, and without implicit
  arguments every use spells the type parameters out. Pending since 2026-10-03.
- Whether a file that imports a provisional definition may itself be certified, or inherits
  the mark.
- Generators as components. A declared type comes with the way to sample it; the model could
  provide the generator as one more component of the structure, so laws are testable as soon
  as the cluster closes.
- Whether an alias may abbreviate a value (`two = 1 + 1`) as well as a type. The voice note
  asks for types; nothing in R8 prevents terms.
