# 8. The demand and the plan

Chapter 8 of the specification, draft 0, 2026-10-13. Sources: `docs/principles.md` L5, L4, L10.5, L10.6, L12.3, O5, O8 and O12; the decisions D-2026-10-10-c, -d and -e, D-2026-10-11-i and -n, D-2026-10-12-h, -m, -r, -ac, -ad and -al; `docs/spec/02-grammar.md` §8, `docs/spec/06-certification.md` §7 and `docs/spec/12-files-and-tools.md` §5 and §6, all at the commit that holds this file; `src/luthier/cli.py`, `machine.py` and `lib/plan.lut`, read only. Written by Claude Sonnet 5.5, as wave 3 of the specification. It realizes L5. The form of the demand is a library's (D-2026-10-12-al), so this chapter states what the core asks of a demand and leaves its representation open. Actions and the world are `spec 10`; specimens and the planner's ranking are `spec 9`.

## §1 Notation

Beyond `spec 1`, this chapter writes: `C` is the type of costs of `spec 6.S4`, with the five operations of `spec 6.S5`; `d` is a demand; `e` is a name or a term, the entry of a demand; `h(e)` is the hash of the dependency cone of `e` in canonical form (`spec 6 §1`); `m` is a mode of evaluation; `s` is a seed.

## §2 What a demand is

**8.S1. A demand is open, and the type demanded reinterprets the cone.** [decided D-2026-10-13-f] A demand is the gate through which parameters change what the program does, and it is not closed: whatever the program declares as a parameter, the demand may set. It carries an entry `e`; the type demanded of it; a cutoff, a bound and an evidence cost in `C` (`spec 6.S15`); a confidence δ for sampled evidence (D-2026-10-12-r); the evidence cost it assigns to assumptions, with no default (`spec 6.S10`); limits on resources if the action wants them; and the values of the program's holes, which `run --set` gives today (`spec 12.S18`). Every threshold or level a certificate needs comes from it and is recorded with it (L5.18). The first demand of all, made by an action nobody called, takes these as declared default arguments, so the root is a parameter too (L5.19). A demand made inside another is passed down from the caller and not recomputed from the cone, because a cutoff does not compose (L12.3). Asking for `t : P T` where the program computes a `T` asks the cone of `t` to build a `P T` instead: a value with its derivative, with an interval that encloses it, with a distribution, or exact in `Rational`, the decorated output of O5. The cone is written generic over a type operator `G`, with `G` the identity by default, and the demand replaces `G` by `P`; spec 11.S3, generic in the number type, is the first instance. [proposed] Whether the generic form is written by hand or derived by Luthier from the cone, which as data can be reinterpreted (L7.4), is open. A certificate obtained at the identity carries over to `P` by parametricity for the laws that hold of any `G` (Wadler, *Theorems for free!*, 1989) when `P` satisfies the laws of the table below; a law over numbers, stated with a distance, is certified again at `P` or carries the distance `P` adds.

**8.S2. What the core asks of a demand and of a decoration.** [decided D-2026-10-13-g] The core uses these operations, and no others; a library may add to them.

| operation | used for | laws |
|---|---|---|
| `entry d` | the name or term to evaluate | none |
| `type d` | the type demanded, possibly `P T` (8.S1) | none |
| `cutoff d` | a pair in `C`, compared with a certificate by `≤` (`spec 6.S15`) | none |
| `delta d` | the confidence of sampled evidence | a value of the type the library's conversion takes (`spec 7.S11`) |
| `assumed d` | the evidence cost of an assumption | none; an absent value refuses every assumed name |
| `key d` | the parameters of a demand that enter the identity of a result: those its cone reads (8.S8) | equal demands give equal keys; the key is a hash of a canonical form, and includes `type d` |
| `map` of `P` | carrying a function of the cone into `P` | the functor laws: `map id = id`, `map (g ∘ f) = map g ∘ map f` |
| `pure` and the product of `P` | carrying constants and functions of several arguments | the applicative laws, so that every operation of the cone has its image in `P` |

Whether the cutoff is a pair or two operations is the library's. The theories that state this table are `lib/demand.lut` and, for the decorations, the library of each `P`; neither is written.

## §3 The plan

**8.S3. Forward on demand.** [decided D-2026-10-10-d] The default strategy is a plan backward from the demand over names, that computes no value; then the live part of the graph is run strictly forward, in topological order, every node once and complete (L5.2). A branch whose use depends on a value marks both branches live. Three conditions bear on it: errors and holes are values that flow, so a live branch nobody uses cannot abort the run; results are memoized in a store keyed by the hash of code, inputs and mode, its retention policy a parameter; tests are actions, so verifying everything is demanding every test and verifying on demand is demanding the tests of what an action uses. What the demand does not need, the complement of its cone, is not produced (L5.13).

**8.S4. The strategy is a parameter.** [decided D-2026-10-10-d] The strategy is separate from the program (L5.2, P11), and only the default is to be implemented. [implemented] Today there is no plan: `run` evaluates the entry by call by need (in `machine.py` a term in an environment is a thunk, computed at first use and remembered), which evaluates only what the entry reaches and so computes the same live subgraph, but interleaved with the run and without a plan as a value. The state of the cone is read before evaluating (12.S18). [decided D-2026-10-13-g] The plan is a value of `lib/plan.lut`, which exists and states a dataflow, a schedule, and the law `Confluent` (any two linearizations agree); what it lacks is the backward pass and the memo key, and a demand's plan is the dataflow of its cone.

**8.S5. A definition has no effects.** [decided D-2026-10-10-c] What a definition computes depends only on its inputs, so every strategy gives one result and independent items commute (`spec 2.S17`). Effects live in actions, whose treatment is `spec 10`; the actions on Luthier's own state, a certificate or a test, are idempotent and memoizable, those on the world never (D-2026-10-12-m).

**8.S6. Mutation as before and after.** [decided D-2026-10-10-e] A mutable parameter is two variables, `x1 = f x0`, and the dependence is an edge of the graph. Changing a value in place is an optimization of the plan, allowed when `x0` has no consumer after `f`, the analysis that also frees a node after its last consumer (L5.14). The surface form that mutates is a library's and translates to the two names. Nothing in the interpreter mutates a parameter today.

**8.S7. What a demand reads.** [decided D-2026-10-12-ad] The checker is a demand for names and types; `run` and `test` are demands for values. Reading a file waits for a demand that needs it: the rule and its consequences for imports and externs are `spec 12.S21` and `spec 3.S40`, not restated. [implemented] The loader reads imports at once, and the checker resolves an extern at check time; the lazy reading of externs waits.

## §4 The memo and the identity of a result

**8.S8. The identity of a result.** [decided D-2026-10-10-d] A result is identified by the hash `h(e)` of its cone, the inputs, the mode, the type demanded and the tolerance, the model its type names, the seed, the plan that produced it, and the certificates' hashes for the part of the cone that is live (L5.6); the host's code behind an extern, read when the demand reaches it, enters through the cone (`spec 6.S8`). So a changed library or platform gives a new result. That results are kept under a hash is D-2026-10-10-d; the list of what enters it is L5.6, and the record that carries it is O12. [decided D-2026-10-13-g] The key is built from `key d` (8.S2), `h(e)`, `m`, `s` and the plan's own hash, and the hashes of certificates are those of `spec 6.S6`. Of the demand, the key holds only the parameters the cone of `e` reads: a parameter is a node of the graph, so a result depends on those in its cone and on no other, and changing a parameter it does not read leaves the key, and the memo, as they were. The type demanded is always read, so a value and its derivative have two keys.

**8.S9. A hit serves a demand only if it meets the demand.** [decided D-2026-10-12-h] For certificates a memo hit is compared with the cutoff of the demand that reaches it, at the hit (`spec 6.S15`, L10.5): a certificate issued for a tight cutoff serves every looser one, and a stricter demand than any entry is a new node of a new plan (L5.9). Writing a certificate is idempotent. [decided D-2026-10-13-g] For results the key of 8.S8 includes the tolerance, so a hit needs equal keys; whether a result computed under a tighter tolerance may serve a looser demand is not settled and is left out until a case needs it (P8).

**8.S10. Two caches.** [decided D-2026-10-10-d] What is derivable from an expression does not depend on the demand; what is produced does. The elaboration (types, derivable laws) is one cache and the memo of results is the other (L5.16). The run database that the planner reads does not enter a result's identity after the plan is chosen (L5.8). [implemented] Today the only memo is a table of results per function over a finite domain (`machine.py`), local to one run and keyed by argument. The result store of D-2026-10-10-d does not exist, and `x.run.json`, which records the hash of the cone, the time, the parameters and the result (12.S18), is written and never read back, so it does not serve as a memo.

**8.S11. Where the plan lives in Luthier.** [decided D-2026-10-13-g] `lib/plan.lut` is the carrier named in L5.6 and L14: a plan is a value, the memo key contains its hash, and its `Confluent` law is what an order of evaluation is certified against (L5.11). The additions it needs are the key of 8.S8, a function from a demand and a program to a plan, and the law that the key of a result changes when any input of 8.S8 changes. They are not written.

## §5 The session

**8.S12. A session is a block over the dataflow.** [implemented] A session builds a block item by item (`spec 2.S18`; the commands are `spec 12.S20`). With `<-` an item explores: it binds a name, and rebinding is allowed; the first binding of a name and its later ones are distinct nodes, `x0`, `x1` (8.S6). With `:=` an item locks: it defines once (`spec 2.R3`, `spec 2.R4`). With the lines `x <- 1`, then `y := x + 10`, then `x <- 2`, `y` stays 11, because it depends on the first `x` (L5).

**8.S13. What a line re-evaluates.** [implemented] Today each line re-evaluates the whole block so far, with no memo (`cmd_session`); the line is wrapped as the block `{ items ; line }`, and it joins the block only if it checked and evaluated. [proposed] A line re-evaluates only the nodes whose cone changed: a node whose key (8.S8) is already in the memo is served, so adding an item does not recompute the earlier ones, and rebinding `x` recomputes exactly what depends on the new `x`. This is O8's memo between items, and it needs no new rule once 8.S8 holds, since a session item is a definition (`spec 2.S17`).

**8.S14. Sessions that differ in the order of independent items.** [decided D-2026-10-11-i] Reordering independent bindings gives an equivalent session, by the law `Confluent`, the law of `lib/plan.lut` that the session block is certified against (L5.11). A session saved to a file becomes the `main` block (L5.12); a file is never a block (`spec 2.S17`).

**8.S15. The trace.** [decided D-2026-10-13-g] L5 names no trace; what exists is the run record of 12.S18. If the planner or the user needs to see what a demand did, the core asks of a library of traces one operation, `record d p r`, that appends the demand, the plan and the result key to a store, with the law that appending never changes an earlier entry (P2, L10.4). The library's form is open (D-2026-10-12-al).

## Open

- O5, the decorated output (L5.4): which model the planner chooses for a demand and how it inserts the bridges, here only as the demanded type of 8.S8.
- O8, the session as a block, and what is kept from item to item (8.S13).
- O12, the record that carries a result's identity, and `lib/plan.lut` as its carrier (8.S8, 8.S11).
