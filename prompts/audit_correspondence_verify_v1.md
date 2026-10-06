# Prompt: audit_correspondence_verify_v1

You are an independent skeptic checking the findings of the mapper "{unit}". Direction of the mapper: {direction}. Its scope: {files}. Default to "uncertain" rather than "confirmed" when you couldn't check.

When the direction is spec or docs: each entry below is a claim of the specification (for docs, a statement of the documentation) with the status the mapper gave it. Your job is to try to refute each one: re-read the specification line, the code and the tests yourself, and where the status says the code does not do what the text says (or does it without a test), write a minimal program under {scratch}/ and run it. Also check the "implemented_tested" spot-checks: does the cited test really exercise the claim?

When the direction is impl: each entry is an observable behavior of the code with the specification line the mapper matched (or "none"). Try to refute each: search docs/semantica/ yourself for a line that does specify it (grep for its terms, its error message, its rule number); re-read the code; where useful, run a minimal program under {scratch}/. For "covered" spot-checks, confirm the specification line really says what the code does.

Return one verdict per entry, with your corrected status and severity. Your answer is one JSON object, with no text around it, in the shape of the output schema of this call:
- "verdicts": one per entry, each with
  - "id": the id of the entry;
  - "verdict": confirmed, refuted or uncertain;
  - "corrected_status": the status you would give it, in the same vocabulary as the mapper;
  - "corrected_severity": high, medium or low;
  - "evidence": what you checked and found: file:line, program and result.
- "notes": anything the report should know, for example an entry you could not check and why.

Entries:
{entries}
