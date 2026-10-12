# 10. Actions and the world

Chapter 10 of the specification, draft 0, 2026-10-13. Sources: `docs/principles.md` L4, L11, L10.6 and O3; the decisions D-2026-10-10-c, D-2026-10-11-i, D-2026-10-12-m, -ab, -ac, -al; `docs/rationale/09-extern-and-the-world.md` (draft 0, 2026-10-07); `docs/spec/02-grammar.md`, `03-kernel.md`, `04-static-semantics.md` and `12-files-and-tools.md` at e8409ef; `src/luthier/` (cli.py, certify.py, evaluator.py, machine.py), read only. Written by Claude Sonnet 5.5, in wave 3. It realizes L4 (the part on actions) and L11. What a demand is and how a plan is run is `spec 8`; what the planner may substitute is `spec 9`; what a certificate holds is `spec 6`.

## §1 Notation

The notation common to all chapters is in `spec 1`. Here, `W` is a type, the world's token (§3), and `w`, `w0`, `w1` are values of it. An *action* is a function that takes a token and gives a token together with a result. A *world action* acts on something Luthier does not own (a terminal, a file, a clock, a foreign process); a *state action* acts on Luthier's own store (a certificate, the record of a test). `h` is the hash of the bytes of a file.

## §2 What an action is

**10.S1. Evaluation has no effect; an action does.** [decided D-2026-10-10-c] What a definition gives is a function of its inputs alone (L4.7), so no definition holds an effect. An effect lives in an action: printing, saving, writing a certificate, running a host program. The consequence is that evaluation may proceed in any order the dependencies allow, and a memo may serve a result without running anything (`spec 8`).

**10.S2. Where an action may occur.** [implemented] An action occurs in a block, in `main`, or in the session, the three places `spec 2.S17` names for a block; it is refused at a file's top level, where nothing orders the acts (spec 4.R12). Inside a block an action is an item with its result bound, as in `w1 <- a w0 x` (D-2026-10-11-i). Each `<-` makes a fresh name (spec 4.R12), so the block is a sub-DAG whose dependencies fix the order, and two items that share no name commute (spec 2.S17). Today the actions that exist are those of the commands: `run` prints a result and appends to `x.run.json`, and `test` writes `x.cert.json` (spec 12.S10, 12.S18). The language has no action a program can name: the block item `w1 <- print w0 "x"` is a grammar example, and no library defines `print`.

**10.S3. An action is declared by its type.** [proposed] L11.4 asks that the declaration of an extern say which of the two it is, definition or action. The proposal is that the type says it: a function whose type takes and gives a `W` is an action, and one that mentions no `W` is a definition and holds no effect (10.S1). The check is then the type's, and spec 4 needs no new rule for it.

## §3 The world

**10.S4. The world is a token threaded through actions.** [proposed] The sources fix that an action on the world is never served from the memo (D-2026-10-12-m) and leave the form to O3: an opaque, unique value. The proposal follows the rationale (its section 3): an action takes the token before and returns the token after, so two readings of one place, before and after a write, are two terms with a dependency between them, and the number and order of operations are in the graph (L4.5 does the same for a mutable parameter). The token has no `==` (spec 4.R8). There is one world (D-2026-10-13-a): its parts exist in Luthier's representation of it, and their independence, if any, is a theory of that representation in a library, never a second token.

**10.S5. What the core asks of a world.** [proposed] Under D-2026-10-12-al the form of the world is a library's, as `Cost` is (spec 6.S4). The core uses the following and nothing more; it chooses no representation, no names and no set of parts of the world.

| operation | used for | laws |
|---|---|---|
| `W` | the token an action takes and gives; a keyword of the core beside `U` (D-2026-10-13-b), the library gives its representation and observations | no `==` (spec 4.R8); a program does not construct one, it enters at `main` or the session |
| `act` | applying an action to a token | gives a new token each time, so two applications to one token are two nodes the memo never merges |
| `own` | saying that an action concerns Luthier's own store | a predicate on actions; an action with `own` is idempotent (10.S6) |

Nothing undoes an action in the language: undoing a change is the history of the repository (P6). Which parts of the world exist, what an observation of one is, and how a class of machines is described belong to the library (§6).

## §4 Two kinds of action

**10.S6. State actions are idempotent and memoizable; world actions never are.** [decided D-2026-10-12-m] Writing a certificate or recording a test acts on Luthier's own state and is verified by reading the store back (Terms). Doing it twice with the same inputs leaves the same store, so it may be memoized, keyed by the hash of the cone (spec 6.S8). An action on the world runs each time it is demanded. [proposed] What separates the two is `own` of 10.S5, taken from the action's declaration and not guessed from its effect; an action with no such declaration counts as a world action, the safer reading.

**10.S7. What an action may change.** [decided D-2026-10-10-c] An action may change the world and Luthier's store, and nothing else: not a definition, not a binding of another block, not a certificate already issued (a new check issues a new certificate and keeps the old, spec 6.S8). A parameter that changes is split in two, its value before and its value after (L4.5); the planner may overwrite in place when nothing else reads the earlier one (`spec 9`), never a semantics. [proposed] That an action changes only what its declaration says is a law of the world's library over the observations it defines, certified as any law (spec 6); until a world library exists nothing checks it.

## §5 Externs as routes

**10.S8. An extern is a route, read when a demand reaches it.** [decided D-2026-10-12-ac] An extern has a name, a declared type and a route to a host function, which is data (spec 3.S40). The file behind the route is read when a demand reaches the node, once per plan; a file that no demand reaches stays unread and may be absent while the program is checked (L11.7). The checker records the target and the type and does not resolve it (spec 4.S24). Because it opens a file, `extern` is an action (D-2026-10-12-ab). [implemented] Today the checker imports the host module, and a target that does not resolve is an error, whether or not a demand reaches it (`checker.py` imports the module at check time); D-2026-10-12-ac changes this.

**10.S9. The file's hash is in the identity of what the extern produces.** [decided D-2026-10-12-ac] The hash `h` of the bytes read, computed by the core and not asked of the world's library, enters the identity of the result and of the extern's certificate (`spec 8` gives the identity of a result, spec 6.S8 the certificate's). [implemented] Today the certificate's hash covers the source files of the module behind each extern in the cone (for a library, the package installed with its version) together with the interpreter (spec 6.S8); it is computed when the certificate is, not when a demand reaches the node.

**10.S10. An extern is validated against its type's laws, then applied.** [decided D-2026-10-11-n] The first time an action asks for an extern, before it is applied, it is tested against the laws of its declared type like any function, and refused if it fails (L11.2). Its certificate stays by hash (spec 6.S8). An extern with no type to validate against is not applied; `extern provisional` is the declared exception, recorded as debt, listed by `check -v` and never certified (spec 4.R5). The agreement test with a native definition comes in addition, and substitution follows D-2026-10-11-m (`spec 9`). [implemented] Today `test` certifies the laws of an extern's type as it does any function's, and `run --checked` tests each value that an extern gives back, as it crosses, against the Bool laws of its type (spec 12.S18, 4.R5); `test` takes the laws quantified over a domain, and a function handed back by an extern is tested at each call. Without `--checked` an uncertified extern in the cone is listed and refused only under `--require-certified` (spec 12.S17). The moment of the validation, the first action that asks, is not what runs today.

**10.S11. The bridge.** [implemented] How a value crosses between the host and the kernel, and what is certified at the crossing, is spec 3.S22 to 3.S28. This chapter adds only that a crossing is where each refinement of the declared type becomes an obligation (spec 4.R5).

**10.S12. A foreign algorithm runs in a named world.** [proposed] L11.6 is a candidate and this statement follows it. An extern with no law yet may run in a named world; each certificate it earns is priced as an assumption (L10.2, spec 6.S10), the plan shows which world it ran in, and until a law is certified the planner's graph and every certified theory stay closed to it. L11.4 says what the extern's certificate binds in the host: library version, platform. The name of the world is a parameter of the demand (P11).

## §6 The theory of actions in Luthier

**10.S13. `lib/world.lut`.** [proposed] L14 asks that what can be written in Luthier be written there. The file would state a theory of the world with the table of 10.S5 as its structure and laws; the theory of an action as a function over `W` together with its result, with the law of 10.S7; and, for each part of the world the library chooses, a theory with its observations and its laws, those that cannot be tested marked `assumed` (the disk persists while the program is off, the clock is monotone) so that the certificate of a run says under what hypotheses it holds (spec 6.S10). The file does not exist: `src/luthier/lib/` holds no world theory and `tests/spec/` no program that states one, so no rule of this chapter has files. A library may offer more than the table; the core uses only the table.

**10.S14. What this chapter leaves out.** [proposed] The rationale also treats the trace of a run, equality of consequence, observations as functors and classes of machines described statistically. They need a form of the record of a run that `spec 8` and the libraries decide; the interface of 10.S5 names none of them, so that adding them later changes a library and not the core (P16).

## Open

- O3: the opt-out of certification, and the world as an opaque, unique value, which 10.S4 and 10.S5 state as an interface and not as a representation.
- O1: the algebra of costs, on which the cost an assumed foreign algorithm carries rests (10.S12).
- O12: what identifies a memoized result, where the hash of an extern's file enters (10.S9).
