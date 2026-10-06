# Prompt: audit_correspondence_report_v1

You write the report of the correspondence audit for Luciano. Below are the results of every mapper and its skeptic, on the repository at commit {commit}. Use only findings whose verdict is "confirmed", or "uncertain" marked as such; drop the refuted ones, but count them. Where the skeptic corrected a status or severity, use the correction. Spot-checks that the skeptic refuted mean the mapper's "implemented_tested" (or "covered") was wrong: report them.
Units that returned nothing: {failed}.

Each result has "label"; "direction" (spec: specification to implementation; impl: implementation to specification; docs: documentation to specification and implementation); "files", the scope of the unit; "out", what the mapper found; and "verify", the skeptic's verdicts by id. An entry with no verdict was not verified: the skeptic saw only the gaps and a few spot-checks.

The script that runs the audit writes the title and the header of the report (draft and status, who it is for, the commit, the prompt files with their hashes, the model, the units run and failed). Start your text at "## Summary". Write it in Markdown, in English, no em-dashes, in this shape:

## Summary
At most one screen. Counts by status in each direction. The confirmed high-severity findings, one line each with the specification line and the code line. What has a specification and no test. What the code decides that no specification says, in aggregate. What this audit did not cover (sections not read, units with no result) and what it can't see.

## Bites
One per decision Luciano has to take: for each high-severity disagreement, whether the specification or the implementation is right, or whether a rule decided but not enforced should be implemented now. At most ten lines each: what the specification says (line), what the code does (line, and the program that shows it), the options, the model's recommendation, the cost. Numbered references carry their statement, for example "R8 (== exists only where equality is structural)".

## Appendix A. Specification to implementation
One table per specification document: claim, status, specification line, code line, test, severity, verdict.

## Appendix B. Implementation to specification
One table per module group: behavior, status, code line, specification line, test, severity, verdict.

## Appendix C. Documentation
README and examples against the specification and the implementation.

## Appendix D. Counts
Findings per unit: mapped, verified, confirmed, refuted, uncertain.

Return the whole Markdown as your final text, nothing else.

Results:
{results}
