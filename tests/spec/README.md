# Specification suite

One pair of programs per rule of `docs/semantica/04-static-semantics.md`: a file the checker
must accept and a file it must reject. A rejected file carries the fragment of the error
message it must produce in a comment `-- expect: ...`. Files whose name ends in
`.theory.lut` or that are imported by others are not run on their own.

`tests/test_spec.py` runs the suite. Until the static semantics of `04` is implemented every
case is expected to fail (`xfail`); as rules land, their cases turn green and the marks go.

State on 2026-10-04, with the checker of commit `294f992`: four cases already pass
(`r1_declaration` both ways, `r2_definition.accept`, `r5_fill_all.accept`), because today's
checker accepts whatever the new rules also accept there; the other twelve fail, eight of
them already at the parser (braces without `|`, `extern provisional`).
