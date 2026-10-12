# Principles, 2026-10-13: nine changes for your marks

At a6eef20 and after. All nine are `[proposed]` in `record/principles-language.md` and projected into
`docs/principles.md`. Each one already guided a chapter of the specification (P13: a principle is
worth the decisions it guides). Mark as usual: "ok", "no" or a comment under a line.

- Terms, the two faces apart: the declarative face has no time, its definitions live in `U` and
  are copied, compared and memoized; the executive face acts on the world `W`, one world, each
  value used once, never memoized. Mind and world (McDowell) stays as a metaphor in parentheses, not
  as a term, on your reading of 2026-10-13 (D-2026-10-13-b).
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
- Terms, the triad, on your question of a keyword for certifiers: what is said (`U`), what is
  done (`W`), what is certified. A certifier is the one action on Luthier's own state whose result
  comes back to the declarative face as a trusted value. Not a keyword: its five kernel forms are
  names of core (D-2026-10-13-d).
        Aca hay sutilezas, cualquier lectura del mundo cambia el estado interno de Luthier, 
        lo que cambia aqui es la creencia de que un valor pertenece a un tipo. 


- L7.3, completed: the five certifiers of L9.1 belong to the kernel layer, names the checker
  recognizes as it does `extern` and `axiom`, checked by hand (D-2026-10-13-d).
- L9.10, new: a certifier is a value, as a generator is; beyond the five primitive ones, a
  certifier is a value of a theory `Certifier`, certified against its own law (its level on laws
  that hold, its power on controls, spec 7.S17 to 7.S19), and a certificate it emits carries the
  certifier's certificate in its cone (D-2026-10-13-d). L10.10 now names LCF's `thm` as the
  precedent for the abstract `Certificate`.

The spec follows: 2.S21 lists `W` among the keywords; 10.S4 and 10.S5 say one world and `W` the
core's; chapter 12 proposes the private part by ascription (2f3435b).
OK
