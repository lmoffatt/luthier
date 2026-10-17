# Report: controls for the uncontrolled laws (L9.14)

By Claude Sonnet 5.5, on prompt-controls.md, 2026-10-17. `luthier check -v` over every
`*_laws.test.lut` with its `*_controls.test.lut` listed five uncontrolled laws outside tables.

Controls written, in tests/tester/certification_controls.test.lut (the broken models sit beside the
existing ones there, as the file's other controls do), each refuted on `certify`:

- ANewIdentityGoesInFront: `droppingNew`, a store that writes nothing for an identity it has not
  seen. Refuted at e = passOne, es = nil.
- AnAgreeingReplayAddsNothing: `writingAgreeing`, a store that writes an exact replay that agrees
  where no disagreement stands. Refuted at e = passOne, es = [passOne].
- AnAgreeingPairSettles: `keepingDispute`, a store that leaves a standing disagreement as it is when
  an agreeing replay arrives. Refuted at e = failOne, es = [failOne, passOne].

Findings (no control, L9.14): KeyReadsOnlyTheCone and KeyReadsTheType (plan.lth §4). Both follow
from the definition of `demandKey` for every planner: the first law's key is computed from the same
`live` the planner gives, so any live set, wider or narrower, leaves it true; the second reads a
field `demandKey` sets itself. A planner is the only model they take, and it does not enter either
conclusion. plan.lth already says so in its comment, and plan_controls.test.lut records it; the law
a model can fail is `Keying`'s. They stay uncontrolled by reason, not by omission.

Also: tests/test_certify.py's list of the laws of certification_laws.test.lut lacked
NoCutoffAcceptsAFailure (added by 0f14ee5 from the other agent) and the list of controls lacked
mine; both updated. certification_model.cert.json re-certified by `certify`.
