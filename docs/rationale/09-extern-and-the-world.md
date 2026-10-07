# Extern and the world: pointers, traces, classes

Draft 0, 2026-10-07. Status: for Luciano to annotate. This note writes down the chain of
reflections of the chat of 2026-10-07 (session 182f2465) on what the fundamental elements of `00`
left out: input and output, time, internal memory and its modification, computing resources, and
calls to external programs. What comes from Luciano is cited by transcript line
(`chat:182f2465:<line>`) or by voice note; what the model adds is marked *proposed*. Section 11
proposes the edits to the list of elements of `00`; nothing in `00`, `04` or `05` changes until he
marks this note.

## 0. Notation

Every symbol and abbreviation used in this note.

- `x : T`, hole, procedure, datum: as in `00`, *Declared, defined, computable*. A hole is a
  declared name with no body; a procedure is a body whose normal form is a function over an
  infinite domain, which answers finite questions; a datum is a body whose normal form has the
  structural equality `==`.
- `extern "python:m.f"`: a body the environment holds (`04 §3`).
- A *pointer* is a value that designates a part of the world. A *token* is the value of a pointer
  after an operation on it; it carries the order of the operations.
- A *trace* is the record of a run: its operations on the world, partially ordered by the
  dependencies between them, with their results and their costs.
- An *observation* is a function from a part of the world to a value. A *functor of observation*
  is an observation that commutes with the composition of operations (section 8).
- The grades of a certificate are those of `05 §7`: point, sampled, bounded, exhaustive,
  witnessed, proved, assumed.
- IO is input and output. GPU is a graphics processing unit. IEEE 754 is the standard of floating
  point arithmetic. FFI is a foreign function interface, the mechanism by which a language calls
  code written in another.
- P2, P10, P14 and R5, R8, R11 are principles and rules of the record and of `05`; each carries
  its statement where it is used.

## 1. The question

Luciano (chat:182f2465:624): left entirely out of the elements are IO, external memory with
write and read and the execution time, internal memory and its modification, the functions that
modify, computing resources, and the possibility of calling extern functions, but inside types;
perhaps the same model can say how external things interact with the program; they have to do
with execution, and execution is an element. And (chat:182f2465:640): extern is a fundamental part
of Luthier, because Luthier is meant to serve also as an orchestrator and verifier of other
programs. The voice note 2026-10-07 17.02.25 says the same at [10:36] to [10:53]: that the code
pass through Luthier, or that Luthier be an orchestrator further out, or both, and both is right.

What `00 §6` says today: pointers, mutation, sequence and control flow do not exist, and what the
environment computes enters as values given by `extern`, never as types (`05` R5, an extern gives a
value, never a type). That is true of the kernel and silent about the world.

## 2. How other languages answered

Background, in the model's words; the sources are named, not quoted, and are the usual ones.

- *Monads* (Haskell; Peyton Jones and Wadler, 1993). The effect goes into the type: `A -> B`
  cannot do IO, `A -> IO B` can, and `IO B` is a recipe that the runtime executes; the program is
  one value, `main : IO ()`. Internal memory is `State s` or `ST s`, with a typing trick so that a
  reference cannot escape. The FFI declares each foreign function with its type, and in `IO` when
  it is impure. The cost is one new construct, bind, and the sequence written by hand. Luciano
  names them in the voice note 2026-10-07 17.02.25 at [11:06] to [11:19] as something he would
  rather not have to write.
- *Algebraic effects and handlers* (Plotkin and Power, 2002; Plotkin and Pretnar, 2009; Koka, Eff,
  OCaml 5, Unison). An effect is a signature of operations without bodies, with equations; a
  handler gives them a meaning. In the words of `05 §1`: an effect is a declared theory and a
  handler is a model, and the program is written against the theory. Koka treats divergence as one
  more effect.
- *Uniqueness and linear types, ownership* (Clean, Barendsen and Smetsers, 1996; Rust; Idris 2,
  Atkey, 2018; Granule). A resource is a value used exactly once: `write : File -> String -> File`
  returns the new file, and Clean threads one unique `World` through the whole program. Mutation
  is consuming the old value and returning the new one, and since nobody holds the old one the
  implementation may update in place.
- *State threaded as a value* (Erlang; Clojure, Hickey's epochal time model). A process is
  `loop(State) -> loop(f(State, Msg))`: mutation is recursion over the state. Clojure separates
  identity from value: a reference is an identity whose value at each instant is immutable.
- *Specification and refinement* (Hoare; Abrial's B; TLA+; F*; session types). The world is a
  state machine with invariants; each operation has a precondition and a postcondition on the
  state; an abstract machine is refined by a concrete one under a proof obligation.
- *Resources*. Two schools: static bounds in the types (Hoffmann's Resource Aware ML; graded
  types; Koka's divergence effect; totality checkers) and measurement (profilers and benchmarks).
  Perceus (Reinking, Xie, de Moura and Leijen, 2021) updates in place when a reference count is
  one at run time, which is measuring rather than proving.
- *Traces* (Mazurkiewicz, 1977). Two sequences of operations that differ only in the order of
  independent operations are one trace.
- *Equality saturation* (egg; Willsey and others, 2021). An equivalence class of programs with a
  cost function that extracts the best one. The mentor note of May already pointed to it
  (`record/ideas/_mentor_mentor_disenio_v1_claude-code_opus.md`, line 31).
- *Explicit assumptions* (Kanig and others, 2014, for SPARK), already in `02-que-robar`, lines 49
  to 51: a verification yields "C holds if H1 ... Hn hold", with a table of what discharges each
  hypothesis.

Which family answers which of the four questions: external memory, the effects and handlers and
the state machines; internal memory and mutation, the unique types and the threaded state; time
and resources, the two schools of section 2, static and measured; calls to external programs, the
FFI of each, typed and with the trust made explicit.

## 3. The world as declared types

Luciano (chat:182f2465:640): "una forma de pensar IO es simplemente como cosas que existen (como
los Reales) y que podemos formular leyes acerca de ellos. Serian como tipos no computables, pero
las funciones que interactuan si."

In the terms of `00`: a part of the world is a hole, a type that exists and that nothing
constructs, with no `==`; the functions that interact with it are procedures, externs, that answer
finite questions; and what is known of it is a theory, whose laws are tested by running the
externs on the world. The precedent is `Codec` (`05 §8`): `parse` and `render` are externs,
certified by the law of the round trip. The shape, with the state of the world as a value:

    World : U := primitive "the world"        -- exists, nothing constructs it, no ==
    Disk : { read : World -> Path -> Maybe String, write : World -> Path -> String -> World }
    ReadAfterWrite (d : Disk) (w : World) (p : Path) (s : String) : Bool :=
      match d.read (d.write w p s) p { nothing -> false ; just t -> t == s }
    Disk := ReadAfterWrite
    disk : Disk := { read := extern "...", write := extern "..." }
    test disk with 50                          -- an experiment on the real disk

*Proposed*: the token. The value that `write` returns must be a new value, so that each reading
is a different term with a dependency, and the order and the number of readings are in the graph,
which is `00 §6`, a sequence is a dependency. Without it, `read unit p` before and after a write
are the same term, and the evaluator shares what is equal because it assumes purity (`04 §6`,
rule 4, each entry once). This is Clean's `World` without the uniqueness check: nothing forbids
keeping an old token, because what is stated of the world is only the laws that hold, and "reading
with the old token gives the old content" is not one of them; the disk has no old states.

*Proposed*: what R5 (an extern gives a value, never a type) has to admit. Today a type without
constructors is either `primitive` in `core.lut` (`04 §1`) or `extern provisional`, which is debt.
This asks for a third kind: a type that exists and that nobody constructs, legitimate when a
theory defines it by its laws, provisional when none does. Under P14 (a type is a concept:
declared, then defined, and only then inhabited) it reads: a pointer type is declared, defined by
the theory of its operations, and inhabited by externs.

## 4. Many pointers

Luciano (chat:182f2465:650): "uno puede definir distintos punteros al mundo, no es un unico
mundo."

Each part of the world is a type of its own, `File`, `Dir`, `Clock`, `Process`, `Cell` (a region of
the environment's memory), and a value is a pointer an extern gives. His candidate of 2026-09-29
for the fundamental elements, "direccion/dato (puntero)" (among the candidates listed then; the
chat line is not located), returns outside the kernel as what the environment hands over.

What it buys. A law: the second law of `Store` in `01 §7`, writing on one key leaves the others as
they were, `k /= k' -> read (write s k a) k' == read s k'`, now with pointers as keys. A
structure: the dependency graph splits into one chain per pointer; chains on different pointers
are independent, may run in any order or in parallel, and the graph is the schedule, where the
computing resources of May enter (voice note 2026-05-26 12.32.24 [03:10], where each path runs).
The finest level of equivalence of the voice note 2026-05-30 18.01.53 [02:56], "misma ubicacion
en memoria", is two pointers to the same part of the world, a symlink or a view of an array; it
breaks independence, and a law detects it, since "the same part" is not decided but tested.
Generators of fresh worlds exist already: `gen GraphDir` of sonolocalización writes a new
directory and returns its path (`record/ideas/generators-inventory-2026-10-06.md`), one fresh
world per case. And the boundary check of `00` (*What types are for*, third moment) turns the
`String` of `run --set dir=...` into a `Dir` whose type certifies that it exists.

*Proposed*: identity and state. A pointer has a stable identity and a state that changes; if
`write f s` returned the same `f`, reading before and after would be one term and the dependency
would be lost, so an operation returns a new token of the same pointer, Clojure's identity and
value by epoch. There is no `==` on pointers (R8, `==` only where equality is structural); "the
same pointer" is a relation an extern answers and a law uses.

## 5. Files as the first pointer

Luciano (chat:182f2465:657): "me suena que extern es un elemento importante. Y podriamos decir que
files son externs (de hecho se refieren a files para las funciones extern), o sea quizas el
concepto de file volviendo a tener relevancia?"

Three mechanisms are one act. `import "x.lut"` reads a file whose content is a program and makes it
a record (`03 §1`); `extern "python:m.f"` reads a file whose content is a function that can be
applied and not read; `parseTable` reads a file whose content is a datum. The certificate treats
them alike already: its hash covers the cone of definitions, the Python sources behind each extern
and the interpreter (`05 §7`).

*Proposed*: `File` is the first pointer type, `read` and `hash` are its operations, and "what was
read is what was certified" is a law, the hash matches. That is P2 (everything derived carries how
it was derived) made a type, and it brings the mechanics of `03 §4` down to a theory. The triad
hole, procedure, datum applies also to the origin of a body: defined here, a term that is read and
reduced; imported, a term of another file that the checker reads; extern, an opaque procedure.
Under P14 an extern is always a model of a theory, never loose; `exp : Float64 -> Float64` in
`real.lut` is the case that violates it (D-2026-10-07-e).

The caveat is Unix's: "everything is a file" broke on sockets, devices and processes. A clock, a
running process and a GPU are not files. The file is the first pointer, not the only one, and the
class of pointers stays open, since every external program that Luthier orchestrates is one.

## 6. Mutation and destruction as realization

Luciano (chat:182f2465:667): "Y tambien variables mutables, porque son una herramienta de
optimizacion muy importante. Y la destruccion de variables, que tampoco esta aqui."

Each has two faces. Mutation as semantics: a cell is a pointer to internal memory, with `load` and
`store` and the laws of `Store`, the token threaded, no `==`; it is covered by section 4 and needs
no element. Mutation as optimization, which is the face he names: the pure program is the ideal
and the implementation that updates in place is a realization, valid when nobody observes the old
value. The relation is `Realizes` (`examples/exp.lut`), the arrow from the ideal to what runs, the
same as the arrow from `Real` to `Float64`. Rust and Clean prove the condition by types; Haskell
hides it under `ST`; Koka's Perceus decides it at run time by a reference count, which is the
version-0 way: two paths, the pure one and the mutating one, the law that they agree, and the
measured time and memory choose. Rule 4 of `04 §6`, each entry of a table computed once, is the
first step in that direction. Linearity as a static guarantee belongs to the proof layer;
`02-que-robar` names the quantities of Idris 2 for it.

Destruction. For a value of the program there is nothing to add: its life runs from its definition
to its last use, which the dependency graph gives, and the realization frees at the last use, what
a compiler computes as liveness and Rust makes deterministic at the end of a scope. For a pointer
to the world, closing is an operation of its theory, `close : File -> Unit`, with the state in the
type, `{ f : File | open f }`, so that using a closed pointer is a type error and not a run-time
one, as in Idris's indexed state and in session types; in Luthier it is R11 (a condition refines in
its branch). The resource law, what is opened is closed, is counted per run and recorded in the
run's certificate until linear types prove it.

## 7. Execution as a trace

Luciano (chat:182f2465:674): "desde el punto de vista de Luthier se podria pensar en la ejecucion
como una lista de operaciones que pueden tener dos tipos de igualdad: igualdad de consecuencia y
comparacion de tiempo de ejecucion y de uso de recursos computacionales."

*Proposed*, two sharpenings. The list is a partial order: the pure part of a run is the reduction,
the world part is the calls to externs ordered by the dependencies of data, one chain per pointer
and no order between pointers; that is what makes two runs that differ only in the interleaving of
independent operations the same, a trace in Mazurkiewicz's sense. The trace is data, what the
pencil writes when a program is executed by hand, and what `02 §8` leaves open as a saved
evaluation, a term with its value.

The two comparisons are of different kinds. Equality of consequence is an equivalence: two traces
are equal when no observation that the theories name distinguishes them, the result under the
equality of the presentation and the state of each pointer touched under the laws of its theory. It
is observational, a component and not `==` (R8), and it is `Realizes`: the pure path and the
mutating one, the ideal and the double, are equal in consequence. The comparison of time and
resources is an order, and a weak one: partial, since less time and more memory do not compare,
and statistical, since it is measured with variance and compared at a level, as the invariant of
stochasticity of D-2026-10-06-z. The split between the two is the forgetful functor of May: the
decorations, efficiency and cost, are what is not equivalent (voice note 2026-05-30 18.01.53
[03:18]); consequence is what the theory sees, cost is what the theory forgets and the run
measures. If time entered the consequence nothing would equal anything.

The certificate of a run therefore has parts of two natures: the equivalence of consequence, a law
that passed, and the costs, measured data. Choosing a path is extracting from an equivalence
class by cost, which is what egg does with its e-graphs; Luthier would have it with the traces as
the class and the measurements as the cost.

## 8. Observations as functors; laws accepted without proof

Luciano (chat:182f2465:684): "los efectos sobre el mundo se ven con los functores sobre el mismo,
las igualdades serian sobre estos functores pero tambien puede haber leyes que se acepten sin
prueba quizas?"

A pointer theory is its operations and its observations: what one looks at of a disk is the
content, or the content and the date, or the hash alone. Observing is a functor from the world to
values, and what makes it a functor is the law of the voice note 2026-05-29 15.04.28 [00:39]:
forgetting composed with the series of functions is the series of functions and then forgetting.
Equality of consequence is equality under that functor. Several functors give several equalities,
ordered by fineness: same pointer, same bits, same value within a tolerance, same distribution,
each forgetting more than the one before; and a law tested at a fine level transports for free to
the coarser ones. This is the list of levels of equivalence of the voice note 2026-05-30 18.01.53
[02:56] made a structure.

Laws accepted without proof exist with a name: the grade assumed (`05 §7`), the body `axiom`
(`06 §3`, `realField`), and SPARK's explicit assumptions in `02-que-robar`, lines 49 to 51, where
a certificate says "L holds if H1 ... Hn hold" and the certificate of a program is the closure of
those clauses. For the world they are natural, since some laws cannot be tested: the disk persists
while the program is off, nobody else writes this file, the clock is monotonic, the extern is
deterministic, the processor conforms to IEEE 754. Each is a law of a pointer theory with the grade
assumed, listed by `check -v` as the axioms and the provisionals are, and the certificate of a run
says "valid under these hypotheses".

## 9. Classes and statistics

The model's first reading, now corrected: a tested law of the world is perishable, dated and
located, since a clock or a GPU has no hash. Luciano (chat:182f2465:691): "una GPU no tiene un
hash pero pertenece a una clase y podes hacer estadistica sobre esta."

So the hash pins identity, and where there is none the descriptor pins the class: model, driver,
system version, the fingerprint of the machine that `check -v` keeps. The class is a type, a
concept with its laws; the instance is a value, a draw from the class; and the laws of the class
are statistical, certified with the grade sampled, with the instances at hand as the generator and
the run as the seed. No third kind of certificate is needed. The equality is the coarsest of the
list, equality in distribution, which `00 §4` describes as a test that does not separate two
samplers: two GPUs are the same when the laws do not separate them. P10 (the mathematical object
that best represents a concept is the invariant of its type): the invariant of `GPU` is the
distribution of its observables.

This closes with his own project. The empirical memory of May, the database of runs with time and
memory per path and per machine (voice notes 2026-05-26 12.41.09 [00:28] and [03:05], 2026-05-27
13.39.04 [01:04]), is a belief over the class, `BeliefFamily` of `belief.lut`, with its chain of
evidence and its calibration, updated by each run; and choosing a path is a decision under that
belief, expected cost and risk, which is the Bayesian extension the voice notes asked for. The
laws of beliefs are written and certified; only what they are applied to changes.

What it needs: the class declared with its descriptor, what defines membership, since statistics
over "GPUs" alone says nothing, and the date and the driver as covariates of the class, not noise;
and first of all the invariant of stochasticity with its tests at a level (D-2026-10-06-z), without
which no law of a class is certified. That pending item is the one that unblocks everything of the
world.

## 10. Kernel, library, tool

Luciano (chat:182f2465:698): "se puede pensar como librerias quizas, aunque extern seria un
concepto primitivo me parece." Agreed, with the split made explicit (*proposed*):

- kernel: `extern` as a body (`04 §1`, `04 §3`), R5 with the amendment of section 3 that admits a
  pointer type declared in a library and defined by a theory, the token as a value, and no `==` on
  pointers (R8);
- library, `lib/world.lut`: the theories `File`, `Dir`, `Clock`, `Process` and `Cell` with their
  laws, their hypotheses marked assumed, and their models as records of externs; `Realizes` as the
  one law of realization, shared with the numbers;
- tool: `run` producing the trace; the certificate of a run with its four parts, the equivalence
  of consequence, the measured costs, the hypotheses assumed and the observations made; the
  registry of classes with their descriptors and their beliefs;
- prerequisite: the library of stochasticity (D-2026-10-06-z).

## 11. Proposed edits to the elements of `00`

Four bullets after *Apply and reduce*, sixteen elements in all. Written in full so that each can
be marked.

- **Extern.** A body the environment holds: `x : T := extern "python:math.exp"`. A model given
  from outside, at a defined type and never a type (`05` R5), opaque: a procedure one applies and
  does not read. What its type claims becomes obligations tested when the value crosses;
  provisional when nobody described its type, which is debt. It is how Luthier verifies and
  orchestrates other programs (chat:182f2465:640).
- **World and pointer.** A type that exists and that nothing constructs, like `Real`, with no
  `==`: its values are pointers that externs give, threaded as tokens so that the order of the
  operations is in the graph; what is known of it is a theory, tested by running on the world,
  with the laws that cannot be tested marked assumed. `File` is the first: code, functions and
  data are read from it, and the hash pins what was read. `Dir`, `Clock`, `Process`, `Cell` follow
  (chat:182f2465:640, 650, 657).
- **Execution.** `run`: fill the holes of the entry with the models of the world, the pointers
  given by `--set` and the externs, reduce, and leave a trace, the partial order of the operations
  with their results and their costs. Two traces compare by consequence, an equivalence the
  theories give through their observations, and by cost, a partial order measured at a level;
  where the world has no hash it has a class, and the laws of the class are statistics over its
  instances (chat:182f2465:674, 684, 691).
- **Realization.** The ideal and what runs it, related by a law and a cost. A real number
  realized by a double within a tolerance; a pure value realized by an update in place when nobody
  holds the old one; a value destroyed at its last use, which the graph knows, and a pointer closed
  by an operation of its theory with the state in the type. Between two realizations of the same
  thing, the time and the memory measured per path choose (chat:182f2465:667).

Two touches elsewhere in `00`. In §6, the last bullet would read: pointers, mutation, sequence,
classes, inheritance and control flow do not exist in the kernel; pointers to the world are
values externs give (*World and pointer*), mutation is a realization (*Realization*), a sequence is
a dependency, `if` is a `match` on `Bool`, a loop is recursion. And the section *Declared,
defined, computable* would say in one sentence that an extern is a procedure whose body is
outside the program.

In `05`, R5 would carry a note, decided and not implemented, as R2 does since D-2026-10-07-e: a
type declared in a library with no constructors is accepted when a theory defines it by its laws,
and is provisional otherwise.

### Decisions for Luciano

Each one is a yes or a no.

1. R5 admits a pointer type declared in a library and defined by a theory (section 3), instead of
   a fixed set of primitives in `core.lut`.
2. The four bullets of section 11 enter the elements, or fewer: *Execution* and *Realization*
   could be one, and *Extern* could stay inside *World and pointer*.
3. `File` is the first pointer type, with the hash as its law of trust (section 5).
4. The laws of the world have two grades, assumed and sampled over a class (sections 8 and 9), and
   the certificate of a run has the four parts of section 10.
5. The order of work: the invariant of stochasticity first (D-2026-10-06-z), then `lib/world.lut`,
   then the trace of `run`.

## 12. Open

- The consequence of each pointer theory: what is observed of a disk, of a process, of a cell.
- The format of the saved trace (`02 §8`).
- The descriptor of a class, and whether the date is part of it.
- Exploration against exploitation when choosing a path under a belief, the tension the May notes
  leave open (`record/ideas/_luthier_ideas_consolidate_ideas_v1_claude-code_opus.md`, under
  *memoria-empirica*).
- Whether an old token may be used at all, or whether the checker warns, since the laws of the
  world say nothing about it.
