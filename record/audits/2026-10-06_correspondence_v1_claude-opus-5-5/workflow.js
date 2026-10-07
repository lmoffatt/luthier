export const meta = {
  name: 'luthier-correspondence-audit',
  description: 'Audit whether the Luthier specification matches its implementation and its documentation, both directions, with adversarial verification',
  phases: [
    { title: 'Map', detail: 'spec to implementation (per spec document), implementation to spec (per module group), docs and examples to spec' },
    { title: 'Verify', detail: 'one skeptic per mapper re-checks every gap and spot-checks the matches' },
    { title: 'Synthesize', detail: 'one report for Luciano: a screen of summary, bites for decisions, tables' },
  ],
}

const LUT = '/home/lmoffatt/Projects/luthier'
const SCRATCH = '/tmp/claude-1000/-home-lmoffatt-Projects-luthier/8d5ce152-b54e-48c4-a388-e7a9ccb80792/scratchpad/audit'
const HEAD = args.head

const COMMON = `
You are part of a correspondence audit of Luthier, a language where a type carries the laws its values must satisfy. Repository: ${LUT}, at commit ${HEAD}. The specification is docs/semantica/ (00-fundamental-elements, 01-construction-pattern, 02-grammar, 03-libraries, 04-kernel, 05-static-semantics, 06-numbers, 07-characterizations, 08-tests; 02-que-robar.md is a survey of prior art, not specification). The implementation is src/luthier/*.py and the base library src/luthier/core.lut and src/luthier/lib/*.lut. Tests: tests/ (tests/spec/*.accept.lut and *.reject.lut are run by tests/test_spec.py: an accept file must load, a reject file must fail with the fragment of its "-- expect:" comment). The documentation for users is README.md and examples/.
Luciano asked: is the specification a faithful reflection of the implementation and of the documentation? Your evidence must be concrete: file:line on both sides, and when you can, a minimal program that shows the behavior.
Rules:
- READ ONLY. Do not modify, create or delete anything under ${LUT}. Do not run git commands that change state. Never run "luthier certify". Run "luthier check", "luthier test", "luthier eval" or "luthier run" only on files you write under ${SCRATCH}/<your label>/ (copies or small programs); a library import resolves through LUTHIER_PATH or the base library, see src/luthier/cli.py.
- Statuses of the specification matter: a rule marked "decided, not implemented" or "open" is declared as such; report it with that status, not as a defect.
- Be exhaustive within your scope, and say in "sections" exactly which sections or files you covered.
- Severity. high: the implementation accepts what the specification rejects or rejects what it accepts, or a decided rule is silently not enforced, or the documentation promises behavior that doesn't happen. medium: implemented but no test exercises it; or the specification is ambiguous enough that two readings give different behavior. low: wording, naming, a missing cross-reference.
- English. No em-dashes.
`

const CLAIM = {
  type: 'object',
  properties: {
    id: { type: 'string', description: 'unique within your output, prefixed by your label, e.g. "05#12"' },
    spec_ref: { type: 'string', description: 'docs/semantica/<file>:<line>' },
    claim: { type: 'string', description: 'the normative claim in one line' },
    status: { type: 'string', enum: ['implemented_tested', 'implemented_untested', 'not_implemented_declared', 'not_implemented_undeclared', 'partial', 'contradicts', 'spec_open_or_nonnormative'] },
    impl_refs: { type: 'array', items: { type: 'string' } },
    test_refs: { type: 'array', items: { type: 'string' } },
    evidence: { type: 'string', description: 'what the code does, in one to three lines; for contradicts or partial, the minimal program and its actual result if you ran one' },
    severity: { type: 'string', enum: ['high', 'medium', 'low'] },
  },
  required: ['id', 'spec_ref', 'claim', 'status', 'impl_refs', 'test_refs', 'evidence', 'severity'],
}
const CLAIMS_SCHEMA = {
  type: 'object',
  properties: {
    sections: { type: 'array', items: { type: 'string' } },
    claims: { type: 'array', items: CLAIM },
    notes: { type: 'string' },
  },
  required: ['sections', 'claims', 'notes'],
}
const BEHAVIOR = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    impl_ref: { type: 'string', description: 'src/luthier/<file>:<line>' },
    behavior: { type: 'string', description: 'what the code accepts, rejects, computes or prints, in one line' },
    spec_ref: { type: 'string', description: 'the specification line that names it, or "none"' },
    status: { type: 'string', enum: ['covered', 'covered_differently', 'not_in_spec', 'internal'] },
    test_refs: { type: 'array', items: { type: 'string' } },
    evidence: { type: 'string' },
    severity: { type: 'string', enum: ['high', 'medium', 'low'] },
  },
  required: ['id', 'impl_ref', 'behavior', 'spec_ref', 'status', 'test_refs', 'evidence', 'severity'],
}
const BEHAVIORS_SCHEMA = {
  type: 'object',
  properties: {
    sections: { type: 'array', items: { type: 'string' } },
    behaviors: { type: 'array', items: BEHAVIOR },
    notes: { type: 'string' },
  },
  required: ['sections', 'behaviors', 'notes'],
}
const VERDICTS_SCHEMA = {
  type: 'object',
  properties: {
    verdicts: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          verdict: { type: 'string', enum: ['confirmed', 'refuted', 'uncertain'] },
          corrected_status: { type: 'string', description: 'the status you would give it, same vocabulary as the mapper' },
          corrected_severity: { type: 'string', enum: ['high', 'medium', 'low'] },
          evidence: { type: 'string', description: 'what you checked and found: file:line, program and result' },
        },
        required: ['id', 'verdict', 'corrected_status', 'corrected_severity', 'evidence'],
      },
    },
    notes: { type: 'string' },
  },
  required: ['verdicts', 'notes'],
}

const SPEC_UNITS = [
  { label: 'spec-00-01', files: 'docs/semantica/00-fundamental-elements.md and docs/semantica/01-construction-pattern.md' },
  { label: 'spec-02-03', files: 'docs/semantica/02-grammar.md and docs/semantica/03-libraries.md (check the grammar against src/luthier/lexer.py, parser.py, syntax.py, and the libraries against src/luthier/lib/)' },
  { label: 'spec-04', files: 'docs/semantica/04-kernel.md' },
  { label: 'spec-05', files: 'docs/semantica/05-static-semantics.md, every section (rules R1 to R11, reports, certification, presentations, open)' },
  { label: 'spec-06', files: 'docs/semantica/06-numbers.md' },
  { label: 'spec-07', files: 'docs/semantica/07-characterizations.md' },
  { label: 'spec-08', files: 'docs/semantica/08-tests.md' },
]
const IMPL_UNITS = [
  { label: 'impl-checker', files: 'src/luthier/checker.py' },
  { label: 'impl-eval', files: 'src/luthier/evaluator.py, machine.py, subst.py' },
  { label: 'impl-front', files: 'src/luthier/lexer.py, parser.py, syntax.py, pretty.py, api.py, and src/luthier/core.lut' },
  { label: 'impl-tools', files: 'src/luthier/cli.py, certify.py, testing.py, generators.py, graph.py, arrays.py, tables.py, rational.py, text.py' },
]

const mapSpec = (u) => agent(`${COMMON}
Your label: ${u.label}. Direction: specification to implementation. Scope: ${u.files}.
Extract every normative claim of your scope (a rule, a decision, a type former, a form of syntax, a behavior the language must have, a report it must give), one per entry, with its line. For each, find where the implementation does it (impl_refs, file:line) and which test exercises it (test_refs), and give it a status. When the code and the text seem to disagree, write a minimal program under ${SCRATCH}/${u.label}/ and run it to see. Motivation, examples and history in the text are not claims unless they state behavior; mark explicitly open questions as spec_open_or_nonnormative.`,
  { label: `map ${u.label}`, phase: 'Map', schema: CLAIMS_SCHEMA })

const mapImpl = (u) => agent(`${COMMON}
Your label: ${u.label}. Direction: implementation to specification. Scope: ${u.files}.
List every behavior of your scope that a user of the language can observe: each error it raises or message it prints, each program it accepts or rejects, each value or result it computes, each option of the command line. For each, find the line of docs/semantica/ that specifies it (spec_ref, or "none"), the test that exercises it, and a status: covered (the specification says it and the code does it), covered_differently (the specification says something else), not_in_spec (the code decides something the specification doesn't say), internal (an implementation detail no user can observe; list these only in aggregate in notes, not as entries). Group trivially similar behaviors (for example several messages of the same rule) into one entry.`,
  { label: `map ${u.label}`, phase: 'Map', schema: BEHAVIORS_SCHEMA })

const mapDocs = () => agent(`${COMMON}
Your label: docs. Direction: documentation to specification and implementation. Scope: README.md and examples/ (and docs/semantica/README if any).
For every statement of README.md about what Luthier does, and every example program, check it against the specification (spec_ref) and against the implementation: run each example and each command the README shows on copies under ${SCRATCH}/docs/ and compare the output with what the README shows. One entry per statement or example, as a claim whose spec_ref is the README line (use "README.md:<line>" in spec_ref and put the specification line in impl_refs next to the code).`,
  { label: 'map docs', phase: 'Map', schema: CLAIMS_SCHEMA })

const verifyClaims = (label, out) => {
  const items = (out && out.claims) ? out.claims : []
  const gaps = items.filter(c => !['implemented_tested', 'spec_open_or_nonnormative'].includes(c.status))
  const spot = items.filter(c => c.status === 'implemented_tested').slice(0, 4)
  const todo = gaps.concat(spot)
  if (todo.length === 0) return Promise.resolve({ verdicts: [], notes: 'nothing to verify' })
  return agent(`${COMMON}
You are an independent skeptic checking the findings of the mapper "${label}". Each entry below is a claim of the specification with the status the mapper gave it. Your job is to try to refute each one: re-read the specification line, the code and the tests yourself, and where the status says the code does not do what the text says (or does it without a test), write a minimal program under ${SCRATCH}/verify-${label}/ and run it. Default to "uncertain" rather than "confirmed" when you couldn't check. Also check the "implemented_tested" spot-checks: does the cited test really exercise the claim?
Return one verdict per entry, with your corrected status and severity.
Entries:
${JSON.stringify(todo, null, 1)}`,
    { label: `verify ${label}`, phase: 'Verify', schema: VERDICTS_SCHEMA })
}

const verifyBehaviors = (label, out) => {
  const items = (out && out.behaviors) ? out.behaviors : []
  const todo = items.filter(b => b.status !== 'covered').concat(items.filter(b => b.status === 'covered').slice(0, 3))
  if (todo.length === 0) return Promise.resolve({ verdicts: [], notes: 'nothing to verify' })
  return agent(`${COMMON}
You are an independent skeptic checking the findings of the mapper "${label}" (implementation to specification). Each entry is an observable behavior of the code with the specification line the mapper matched (or "none"). Try to refute each: search docs/semantica/ yourself for a line that does specify it (grep for its terms, its error message, its rule number); re-read the code; where useful, run a minimal program under ${SCRATCH}/verify-${label}/. Default to "uncertain" when you couldn't check. For "covered" spot-checks, confirm the specification line really says what the code does.
Return one verdict per entry, with your corrected status and severity.
Entries:
${JSON.stringify(todo, null, 1)}`,
    { label: `verify ${label}`, phase: 'Verify', schema: VERDICTS_SCHEMA })
}

phase('Map')
const specResults = pipeline(SPEC_UNITS,
  (u) => mapSpec(u),
  (out, u) => verifyClaims(u.label, out).then(v => ({ label: u.label, kind: 'spec', out, verify: v })))
const implResults = pipeline(IMPL_UNITS,
  (u) => mapImpl(u),
  (out, u) => verifyBehaviors(u.label, out).then(v => ({ label: u.label, kind: 'impl', out, verify: v })))
const docsResult = mapDocs().then(out => verifyClaims('docs', out).then(v => ({ label: 'docs', kind: 'docs', out, verify: v })))

const all = [].concat(await specResults, await implResults, [await docsResult]).filter(Boolean)
log(`mapped and verified ${all.length} units`)

const missing = SPEC_UNITS.concat(IMPL_UNITS).map(u => u.label).concat(['docs']).filter(l => !all.find(r => r.label === l))
if (missing.length) log(`units with no result: ${missing.join(', ')}`)

phase('Synthesize')
const report = await agent(`${COMMON}
You write the report of the correspondence audit for Luciano. Below are the results of every mapper and its skeptic. Use only findings whose verdict is "confirmed", or "uncertain" marked as such; drop the refuted ones, but count them. Where the skeptic corrected a status or severity, use the correction. Spot-checks that the skeptic refuted mean the mapper's "implemented_tested" was wrong: report them.
Units that returned nothing: ${JSON.stringify(missing)}.

Write the report in Markdown, in English, no em-dashes, in this shape:

# Correspondence audit of Luthier

Draft 0, 2026-10-06. Status: for Luciano; the bites need his answer.
Written for Luciano. (one line on the question: is the specification a faithful reflection of the implementation and of the documentation)
Sources: the repository at ${HEAD}; the audit was run by agents that mapped each direction and skeptics that tried to refute each finding.

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
${JSON.stringify(all)}`,
  { label: 'synthesize report', phase: 'Synthesize' })

return { report, units: all.map(r => ({ label: r.label, mapped: (r.out && (r.out.claims || r.out.behaviors) || []).length, verdicts: (r.verify && r.verify.verdicts || []).length })), missing }
