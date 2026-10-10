# Default arguments: answer to Luciano's note of 2026-10-11

Source: `record/Lucianos ideas/python style.txt` (committed verbatim at c3c63d9). Written by Claude
in the chat of 2026-10-11. What cites the spec is marked by its section; what is proposed here is
marked *Proposed*. Nothing here is decided.

Luciano's note: Python functions have many parameters with defaults, called by position or by name;
"esto permitiria exponer todos los parametros de un tipo, pero poniendo un alias y un valor de
default para casi todos." Syntax candidates in the note: `(arg:T=value?)` or `(arg<-value:T)` in the
definition, `F (arg<-value)` or `F (arg=value)` at the call.

## Why it fits

P11 (every criterion is a parameter, never a constant in the code) exposes every criterion, and
without defaults every call spells out all of them. Defaults are what make P11 livable.

A default is a hole with a filler given in advance. The spec already has the module-level case: a
file declares `num : NumberModel` and the importer fills it with `num := float64` (`06` §7). The
open item "implicit arguments" (`05` §10: code over theories takes the model as a parameter and
every use spells it out) is partly answered by a default: `(num : NumberModel := float64)`.

## Syntax (*Proposed*)

    f (x : A) (tol : Float64 := 1e-6) (maxIter : Int := 100) : B := ...
    f a (tol := 1e-3)

`:=` already means "defined as" in a definition (`02` §2), in a record value `{ x := a }` and in the
filler of a hole. `=` is taken by the alias (`05` R7), so `F (arg = value)` would read as an alias.
`<-` is free in the grammar, but it is assignment in R and the bind of `do` in Haskell. `(x := v)`
is not a term today, so it does not collide.

## Semantics (*Proposed*)

1. **Defaults belong to the definition, not to the type.** Labels are binders and not part of a
   type's identity (`04` §2), so a function passed as a value of type `A -> Float64 -> B` has no
   names and no defaults; the call by name and the filling of defaults are sugar at the call site
   of a named definition. This is Python's and Scala's behaviour. OCaml puts optional arguments in
   the type and pays with rules about when they are erased.
2. **When defaults are filled.** With currying, `f a` could be a partial application waiting for
   `tol` or a full call with `tol` defaulted. Rule: the defaults are filled once every parameter
   without a default has been given; to keep a defaulted parameter open, write a lambda.
3. **A default may depend on earlier parameters**, `(n : Int) (tol : Float64 := 1e-6 * n)`, which
   dependent types give for free and Python imitates with `None`.
4. **The elaborated call carries every value.** The call is expanded with its defaults before it is
   hashed, so the certificate and the memo key record every parameter (P2, everything derived
   carries how it was derived), and changing a default makes what depends on it stale. In Python a
   default is invisible in the record of a run.
5. **Laws are quantified over the parameter, not tested at its default.** The default is one point
   of the parameter's type; a law of `f` speaks of every `tol`.
6. Python's trap with mutable defaults (evaluated once, shared between calls) does not arise
   without effects (L18, a definition has no effects).

## Luciano's objection, and a revised syntax

Luciano (chat, 2026-10-11): "me hace ruido con la idea de que := sea algo definitorio, puesto asi es
como que abre la puerta a que las definiciones son mutables, lo cual no estaria mal ya que el
lenguaje admite mutaciones."

The objection is right about the declaration and not about the call. Mutation in Luthier is two
names, before and after (D-2026-10-10-e); no name ever changes its value, and that is what lets the
hash of a name stand for its value in the memo and the certificate (L18, L19). A call
`f a (tol := 1e-3)` changes nothing in `f`: it fills the hole `tol` once, for that application, as
`import ... with num := float64` fills the hole of a file (`06` §7). What reads as redefinition is
`(tol : Float64 := 1e-6)` in the declaration, which looks like `tol` is already defined.

*Proposed, revised.* Keep `:=` at the call, where it is the one definition of that parameter in that
application, and mark the default in the declaration with something that does not say "defined":

    f (x : A) (tol : Float64 default 1e-6) : B := ...
    f a (tol := 1e-3)

`default` would be a new keyword; a symbol (`?=`) is the other option.

## Defining a name twice

Luciano (chat, 2026-10-11): "el tema es si vos definis dos veces a un simbolo que pasa? si es
inmutable --> error, si es mutable --> pasa (+warning?)".

Today: an error. The checker reports "x is defined twice" (`src/luthier/checker.py`, checked on a
two-line file). The spec states no rule for it.

*Proposed.* Luciano's rule is compatible with D-2026-10-10-e if the second definition of a mutable
name is surface for a fresh name, as in SSA: `x := 1 ; x := x + 1` is `x0 := 1 ; x1 := x0 + 1`, and
each later `x` means the latest. The core stays immutable and hashes still stand for values. Two
conditions follow.

- **Only where there is order.** A file is a set of acts without order (`05` §2, `03` §1): a use of
  `x` in another definition would mean `x0` or `x1` depending on where it is written, so the file
  would become a sequence. Redefinition fits inside a block, where order exists (local definitions
  in a block are open, `02` §8), and stays an error at the top level of a file. Inside a recursion,
  a redefined name becomes a parameter of the recursive call, as a phi node does in SSA.
- **A marker instead of a warning.** The name is marked mutable where it is first defined
  (`mut x := 1`, keyword to be chosen); then a redefinition is intended and needs no warning, and
  without the marker it is an error. A warning on every intended redefinition would be ignored
  (P8, no more bureaucracy than it pays for).

A default argument is not a redefinition under this rule: the parameter is immutable in the body,
and the call fills it once. The choice between `default` and `?=` is independent.
