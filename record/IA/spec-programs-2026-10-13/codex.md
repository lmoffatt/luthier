# Specification program migration (spec-programs v1)

Sources: `tests/spec/v0.1/` and `docs/spec/` at 310a9ba6682e982150584caea8f26dba643aa1e7; migration brief
`record/IA/spec-programs-2026-10-13/prompt.md`, sha256
`3df1bcbaff582a792f9a787864ffd94b3cc376d8cc01c56becf13e555aa68e5c`; `CLAUDE.md`;
`docs/principles.md` L2.7 (a constructor has a role stated by laws); and the reference
statement at `v0.1-final:src/luthier/lib/reference.lut`. Each program records its original
file's SHA-256. Derived by Codex following that brief, version spec-programs v1,
with the original filenames, current cited items, and no seed or other parameters.
The additions below are proposals where explicitly labelled, not additions to the specification.

The source has **48 programs**, not 50, plus its README and bibliography: the table lists
all 50 source files. `kept` means the executable case is unchanged; every program's header
and diagnostic provenance have been migrated. Original error fragments are not
invented: each fragment that existed is preserved verbatim, normally as `-- expect (v0.1):`.
Only spec 4.R12 supplies the current repeated-definition diagnostic literally.

| File | Result |
|---|---|
| `cite_not_reference.reject.lut` | rewritten |
| `cite_proved.accept.lut` | rewritten |
| `k_bool_is_sum.accept.lut` | kept |
| `k_dependent_product.accept.lut` | kept |
| `k_empty_unit.accept.lut` | kept |
| `k_label_order.reject.lut` | kept |
| `k_named_product.accept.lut` | kept |
| `k_recursor.accept.lut` | rewritten |
| `k_sum.accept.lut` | kept |
| `k_union.accept.lut` | kept |
| `n1_numbers.accept.lut` | kept |
| `n2_r_gone.reject.lut` | kept |
| `n3_primitive_outside_core.reject.lut` | kept |
| `n4_axiom_outside_lib.reject.lut` | kept |
| `n5_arrays.accept.lut` | rewritten |
| `r12_block.accept.lut` | kept |
| `r12_defaults.accept.lut` | kept |
| `r12_defined_twice.reject.lut` | kept |
| `r12_named_unknown.reject.lut` | kept |
| `r12_rebind_defined.reject.lut` | kept |
| `r12_toplevel_arrow.reject.lut` | kept |
| `r12_unused_rebinding.reject.lut` | kept |
| `r13_operator_by_type.accept.lut` | kept |
| `r13_two_models.reject.lut` | kept |
| `r1_declaration.accept.lut` | kept |
| `r1_declaration.reject.lut` | kept |
| `r2_definition.accept.lut` | kept |
| `r2_definition.reject.lut` | kept |
| `r2_unclaimed_laws.reject.lut` | kept |
| `r3_connected.accept.lut` | rewritten (layout continuation; spec 2.S4) |
| `r3_dangling_label.reject.lut` | kept |
| `r3_true_predicate.reject.lut` | kept |
| `r4_data_nonrecursive.reject.lut` | verdict flipped (reject → accept; spec 4.R4, spec 3.R3; roles satisfy spec 4.R3) |
| `r4_product_inline.accept.lut` | kept |
| `r4_product_named.reject.lut` | kept |
| `r4_recursive_data.accept.lut` | rewritten |
| `r5_extern_over_declared.reject.lut` | kept |
| `r5_extern_provisional.accept.lut` | rewritten |
| `r5_extern_type.reject.lut` | kept |
| `r5_extern_value.accept.lut` | kept |
| `r6_body_type.reject.lut` | kept |
| `r6_predicate_body.accept.lut` | kept |
| `r7_alias.accept.lut` | kept |
| `r7_alias_defined.reject.lut` | kept |
| `r8_equality_function.reject.lut` | kept |
| `r8_equality_parameter.accept.lut` | kept |
| `r9_variance.accept.lut` | kept |
| `r9_variance.reject.lut` | kept |
| `README.md` | rewritten (current suite, verdict override, diagnostics and proposals) |
| `cite_sources.bib` | kept (byte-for-byte copy) |

Validation: all 48 filenames and original diagnostic fragments preserved, all source hashes
verified, bibliography unchanged, and no tracked changes to `tests/spec/v0.1/`. Python CLI
parses 47 programs. The all-files parse command exits 1 on the remaining intentional
syntax-negative case; `python3 scripts/check_spec.py` passes. No parser, source, script,
specification or original fixture was changed; no commits were made. Semantic verdicts
remain unverified because the new checker does not exist.

## Questions where the specification does not determine the program or check

1. The brief says 50 programs, but the source has 48 programs and two auxiliary files:
   were two further programs intended, or does 50 mean those 50 files?
2. Should `r12_toplevel_arrow.reject.lut` remain a syntax-negative case (the migration
   keeps it), given that preserving its `x <- 1` case under spec 2.R5 prevents the requested
   all-files parse check from passing?
3. What is `cite`'s precise signature under spec 6.R1's O10 and spec 10.S2 to spec 10.S5:
   does it take `W` first, return `W * Unit`, and take `checked` as text (`"human"`,
   `"ai+human"`), as the two citation programs explicitly propose?
4. How does spec 12.R1's `.bib` import fit spec 12.S22's named imports: may a local
   native `Reference` theory be the annotation in `import "cite_sources.bib"
   kantorovich1948 : Reference higham2002 : Reference`, as proposed in the accept case?
5. Is the retired reference library's identifier record and `Resolvable` law the intended
   current `Reference` interface, or what native statement should replace it in these
   self-contained citation cases?
6. Which diagnostic fragments should the new checker emit for the historical
   `-- expect (v0.1):` cases, where the cited current items state the rejection but give
   no exact message (the flipped Color case's old fragment is history only)?
7. Should spec 11.R3's positive axiom control name another file, since its `Files:` line
   names `n5_arrays.accept.lut`, whose actual case is arrays (spec 11.S9) and contains
   no permitted axiom? Its migrated header cites both items and its array case is preserved.

## Parse exception

The sole failing text is the intentionally forbidden act:

```luthier
x <- 1
```

Exact CLI error:

```text
tests/spec/r12_toplevel_arrow.reject.lut:6:2: expected ':', ':=' or clause, '='; got '<-'
```

This agrees with chapter 2 and is not a suspected parser defect. No other text believed
valid by chapter 2 was rejected. The group case's old line break after `|` was changed
into a space because it was not indented deeper than the first brace item (spec 2.S4).

## Decisions taken independently

Preserve the source suite and filenames; cite prose items when there is no `Files:` line;
keep historical diagnostics visibly historical; add fold theories for N and Tree and an
alternation theory for Color to state constructor roles; mark Color's acceptance explicitly
while retaining its requested filename; state Vec and Reference locally; label the citation
signature and typed bibliography import as proposals; and retain the intentional syntax
rejection rather than change its rule or the parser. No decisions were written into the
specification or decision record.
