# Theory fixes 2026-10-14: report

Written by a Claude agent (Claude Opus 5.5) from the brief `prompt.md`, on the tree at d6de77d;
saved verbatim by the coordinator from the agent's final message. Three commits, one per file:
02aa8af program.lth (4.R3 untouched by projection and binders as reads, 4.R13 rivalModel by the
declared type with the binders' types, 4.R4 primitive as extern); c777ab9 algebra.lth
(`OrderedField`'s record inlined in `FieldIsOrdered`, `asOrderedRing` removed); 7e58669 tables.lth
(`Codec`'s laws compare through `c.eq` inline, `sameParse` removed). arrays.lth unchanged: with
1(a) mirrored no shape refinement is refused; the `Orthogonal` capture (substituting `n := k`
under a record whose own field is `n`) is the checker's: check.py must stop the substitution at
a record field or binder that binds the name.

What check.py must mirror: (a) `violatesR3` compares the labels with the law's names plus the
`namePrefix` of each name; (b) 4.R13 compares the elaborated declared types of the two targets
(binders' types in order, then the type), not the declaration alone; (c) `violatesR4` accepts
`primitive` as head; 11.R2 (`primitive` only in core.lut) is check.py's, which knows the file
name; (d) `law_reads` adds `fields_read` of each binder's type and default. With a scratch mirror
of (a), (d) and group 1's `fieldsRead`: arrays.lth's seven 4.R3 refusals pass, tables.lth and
algebra.lth are clean; 39 4.R9 refusals in arrays.lth remain, all the checker's (the leftovers
report's causes a, b, c). Decisions of the agent: binder types in `rivalModel`'s comparison
([proposed]); the helpers removed after inlining; no rename in arrays.lth.
