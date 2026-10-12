# Principles, 2026-10-13: six changes for your marks

At ba8b9ed. All six are `[proposed]` in `record/principles-language.md` and projected into
`docs/principles.md`. Each one already guided a chapter of the specification (P13: a principle is
worth the decisions it guides). Mark as usual: "ok", "no" or a comment under a line.

- Terms, the mind and the world: a program lives in two places, the mind (the definitions and their
  universe `U`: timeless, copied, compared, memoized) and the world `W` (one world, each value of it
  used once, never memoized). The declarative face is the mind's; the executive face acts on the
  world. From your M and W; `U` keeps its name (D-2026-10-13-b).
- L4.11, completed: the world's uniqueness is meant literally. `W` is a primitive beside `U`, with
  no introduction (it enters at `main` or the session), no `==`, and each value used once. The
  three rules are the model's (D-2026-10-13-b).
- L4.12, new: there is one world; its parts belong to Luthier's representation of it, and their
  independence is a theory of that representation, certified like any law and not imposed by the
  language; two actions commute only where such a law says so, and only over what can be read back
  (L4.10) (D-2026-10-13-a, your words).
- L6.12, new: an importer sees a module only through the theory it gives it as type, so its
  representation stays private and another model can replace it; privacy is ascription, not a
  keyword (D-2026-10-13-c).
- L7.5, new: what a library can decide, the core does not; the core asks each library the fewest
  operations and laws it uses, and the library's open choices are taken when it is implemented
  (D-2026-10-12-al, P16).
- L10.10, new: only a certifier builds a certificate; its constructor is in no interface outside
  the theory of certification, so "no evidence for free" (L10.9) is enforced, not trusted
  (D-2026-10-13-c).

The spec follows: 2.S21 lists `W` among the keywords; 10.S4 and 10.S5 say one world and `W` the
core's; chapter 12 proposes the private part by ascription (2f3435b).
