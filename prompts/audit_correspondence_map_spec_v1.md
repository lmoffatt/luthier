# Prompt: audit_correspondence_map_spec_v1

Your label: {unit}. Direction: specification to implementation. Scope: {files}.

Extract every normative claim of your scope (a rule, a decision, a type former, a form of syntax, a behavior the language must have, a report it must give), one per entry, with its line. For each, find where the implementation does it (impl_refs, file:line) and which test exercises it (test_refs), and give it a status. When the code and the text seem to disagree, write a minimal program under {scratch}/ and run it to see. Motivation, examples and history in the text are not claims unless they state behavior; mark explicitly open questions as spec_open_or_nonnormative.

Your answer is one JSON object, with no text around it, in the shape of the output schema of this call:
- "sections": the sections or files of your scope that you covered.
- "claims": one entry per claim, each with
  - "id": unique within your output, prefixed by your label, for example "{unit}#12";
  - "spec_ref": docs/semantica/<file>:<line>;
  - "claim": the normative claim in one line;
  - "status": one of implemented_tested, implemented_untested, not_implemented_declared (the specification itself says it is not implemented), not_implemented_undeclared, partial, contradicts, spec_open_or_nonnormative;
  - "impl_refs" and "test_refs": lists of file:line;
  - "evidence": what the code does, in one to three lines; for contradicts or partial, the minimal program and its actual result if you ran one;
  - "severity": high, medium or low, by the scale above.
- "notes": anything the report should know that has no entry, for example what you could not check.
