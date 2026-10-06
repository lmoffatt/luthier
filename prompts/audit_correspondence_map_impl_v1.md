# Prompt: audit_correspondence_map_impl_v1

Your label: {unit}. Direction: implementation to specification. Scope: {files}.

List every behavior of your scope that a user of the language can observe: each error it raises or message it prints, each program it accepts or rejects, each value or result it computes, each option of the command line. For each, find the line of docs/semantica/ that specifies it (spec_ref, or "none"), the test that exercises it, and a status: covered (the specification says it and the code does it), covered_differently (the specification says something else), not_in_spec (the code decides something the specification doesn't say), internal (an implementation detail no user can observe; list these only in aggregate in notes, not as entries). Group trivially similar behaviors (for example several messages of the same rule) into one entry.

Your answer is one JSON object, with no text around it, in the shape of the output schema of this call:
- "sections": the files or parts of files of your scope that you covered.
- "behaviors": one entry per behavior, each with
  - "id": unique within your output, prefixed by your label, for example "{unit}#12";
  - "impl_ref": src/luthier/<file>:<line>;
  - "behavior": what the code accepts, rejects, computes or prints, in one line;
  - "spec_ref": the specification line that names it, or "none";
  - "status": one of covered, covered_differently, not_in_spec, internal;
  - "test_refs": a list of file:line;
  - "evidence": what you read or ran that shows it;
  - "severity": high, medium or low, by the scale above.
- "notes": the internal details in aggregate, and anything the report should know that has no entry.
