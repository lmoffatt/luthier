# Prompt: audit_correspondence_map_docs_v1

Your label: {unit}. Direction: documentation to specification and implementation. Scope: {files}.

For every statement of README.md about what Luthier does, and every example program, check it against the specification (spec_ref) and against the implementation: run each example and each command the README shows on copies under {scratch}/ and compare the output with what the README shows. One entry per statement or example, as a claim whose spec_ref is the README line (use "README.md:<line>", or "examples/<file>:<line>", in spec_ref, and put the specification line in impl_refs next to the code). Do not run a command that installs something or changes your environment, such as "pip install", nor "luthier certify"; say in "notes" which commands you did not run and why.

Your answer is one JSON object, with no text around it, in the shape of the output schema of this call:
- "sections": the files and sections of the documentation that you covered.
- "claims": one entry per statement or example, each with
  - "id": unique within your output, prefixed by your label, for example "{unit}#12";
  - "spec_ref": README.md:<line> or examples/<file>:<line>;
  - "claim": what the documentation says or shows, in one line;
  - "status": one of implemented_tested, implemented_untested, not_implemented_declared, not_implemented_undeclared, partial, contradicts, spec_open_or_nonnormative;
  - "impl_refs": the specification line and the code line, as file:line;
  - "test_refs": a list of file:line;
  - "evidence": the command you ran on the copy and what it printed, against what the documentation shows;
  - "severity": high, medium or low, by the scale above.
- "notes": anything the report should know that has no entry, for example a command you could not run.
