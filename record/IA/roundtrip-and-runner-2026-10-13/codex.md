# RoundTrip trees and syntax runner (v1)

Inputs: the brief `record/IA/roundtrip-and-runner-2026-10-13/prompt.md` (sha256 2f27eb6dfd2bb8215460cf22f4f17f1d10db16ff813c938f3314c3c6a1db266c),
`CLAUDE.md`, `grammar.lth`'s wf/wfAct/wfProgram and RoundTrip/Canonical, `surface.py`,
`parse.py`, `tests/spec/README.md` and the current fixtures at starting commit
3fe21aa209644a7a41d7ed2c82e33a5a1f1f75d6. Grammar input sha256: 9f7b092dafae33acc6423eb643e1d90af2b5c4e21fc72aabe32a2572046fab04.
Written: `tests/test_roundtrip_trees.py` v1 (direct generator, independent wf transcription,
depth/seed determinism/constructor coverage checks, greedy structural shrinking capped at
100 improvements), and `tests/test_spec.py` v1 (header provenance, verdict overrides, explicit
syntax-rejection allowlist, Files references, and an unconnected checker comparison hook).
Parameters: `random.Random(seed)`, seeds 0..999, sizes 0..6; names and finite literal census
are explicit in the test. Each recursive constructor spends one size unit and divides the
remainder among its arguments; Field/Clause/pair metadata wrappers do not add depth.
No parser, library, fixture, specification or other record changes; no commits made.

Bite 1: 4 passed, 6 strict xfails (sizes 1..6); all 7,000 programs are generated and checked,
including when earlier cases failed. 895 fail RoundTrip and shrink to the 68 distinct trees
below; Canonical passes wherever parsing succeeds (vacuously true on parse failure, as the
law states). Bite 2: 56 passed; 24 accept programs parse, 23 semantic rejects parse with
checker_status=pending, and the explicit spec 2.R5 syntax reject counts as rejected.
All semantic verdicts and messages remain unverified until CHECKER is connected; current
fragments are enforced by the hook, v0.1 fragments are historical, and proposed wording
requires an explicit enforce_proposed policy. Full suite: 271 passed, 6 xfailed in 40.94s.
`python3 scripts/check_spec.py` passes. Validation uses Python 3.14.8 in the temporary
external pytest environment, with PYTHONPATH=src.

The findings are three observable failures: negative term literals print as negation trees
(including -0.0); negative pattern literals permitted by wf have no printed parse; and a
later datum beginning with - or < joins the previous act through layout continuation.
These are counterexamples over wf, not amendments to its domain. No parser fix was made.
Routine decisions taken independently: count depth through recursive constructor arguments,
keep Canonical and generator validity outside xfail, run each complete seed census before
failing, reduce only to a smaller wf tree that still fails, and report checker pending status
as pytest properties rather than infer semantic success from parser acceptance.

## Every distinct shrunk failing tree

Each entry gives the full program tuple, text (Python string representation, preserving
escapes and final newline), actual parse result, and every contributing (seed, size).
Original trees are reproduced exactly by `Trees(seed).program(size)` in the test; repeated
identical shrunk trees are grouped. Shrinking is cheap and locally minimal under the supplied
reductions, not a proof of a globally smallest equivalent counterexample. The seven size
censuses never stop at the first failing seed. Failure counts by family: signed term literal: 810, act-start continuation: 28, signed pattern literal: 57.

### 1. 243 case(s)

```text
Tree: (Datum(value=Literal(literal=FloatLit(value=-0.0))),)
Text: '-0.0\n'
Result: Parsed(program=(Datum(value=Neg(value=Literal(literal=FloatLit(value=0.0)))),))
Seed, size: (23, 1), (25, 1), (50, 1), (122, 1), (184, 1), (187, 1), (207, 1), (325, 1), (375, 1), (691, 1), (704, 1), (744, 1), (840, 1), (867, 1), (881, 1), (911, 1), (50, 2), (53, 2), (130, 2), (170, 2), (175, 2), (211, 2), (262, 2), (328, 2), (375, 2), (441, 2), (485, 2), (534, 2), (601, 2), (605, 2), (669, 2), (761, 2), (816, 2), (850, 2), (857, 2), (931, 2), (947, 2), (41, 3), (53, 3), (75, 3), (106, 3), (108, 3), (116, 3), (134, 3), (138, 3), (184, 3), (193, 3), (220, 3), (242, 3), (263, 3), (280, 3), (307, 3), (312, 3), (339, 3), (375, 3), (441, 3), (442, 3), (501, 3), (502, 3), (602, 3), (615, 3), (634, 3), (643, 3), (674, 3), (719, 3), (773, 3), (787, 3), (799, 3), (840, 3), (911, 3), (969, 3), (996, 3), (39, 4), (81, 4), (116, 4), (184, 4), (191, 4), (220, 4), (242, 4), (251, 4), (262, 4), (263, 4), (270, 4), (292, 4), (307, 4), (312, 4), (322, 4), (328, 4), (332, 4), (339, 4), (374, 4), (377, 4), (383, 4), (441, 4), (442, 4), (484, 4), (495, 4), (501, 4), (502, 4), (539, 4), (587, 4), (602, 4), (615, 4), (628, 4), (637, 4), (638, 4), (680, 4), (717, 4), (719, 4), (756, 4), (757, 4), (773, 4), (786, 4), (787, 4), (806, 4), (807, 4), (828, 4), (911, 4), (947, 4), (969, 4), (996, 4), (0, 5), (27, 5), (39, 5), (53, 5), (81, 5), (99, 5), (108, 5), (138, 5), (184, 5), (191, 5), (251, 5), (262, 5), (263, 5), (270, 5), (292, 5), (312, 5), (322, 5), (332, 5), (345, 5), (351, 5), (395, 5), (442, 5), (484, 5), (502, 5), (507, 5), (584, 5), (601, 5), (602, 5), (608, 5), (628, 5), (631, 5), (635, 5), (637, 5), (680, 5), (682, 5), (704, 5), (749, 5), (754, 5), (756, 5), (773, 5), (784, 5), (786, 5), (787, 5), (798, 5), (807, 5), (816, 5), (832, 5), (840, 5), (857, 5), (861, 5), (898, 5), (924, 5), (928, 5), (947, 5), (964, 5), (969, 5), (979, 5), (980, 5), (996, 5), (16, 6), (27, 6), (50, 6), (53, 6), (81, 6), (99, 6), (107, 6), (108, 6), (117, 6), (138, 6), (144, 6), (184, 6), (191, 6), (243, 6), (251, 6), (263, 6), (270, 6), (292, 6), (308, 6), (312, 6), (321, 6), (322, 6), (329, 6), (331, 6), (345, 6), (358, 6), (369, 6), (377, 6), (395, 6), (401, 6), (418, 6), (441, 6), (482, 6), (502, 6), (504, 6), (535, 6), (537, 6), (602, 6), (610, 6), (612, 6), (628, 6), (631, 6), (634, 6), (637, 6), (638, 6), (674, 6), (704, 6), (749, 6), (786, 6), (787, 6), (792, 6), (798, 6), (819, 6), (828, 6), (832, 6), (840, 6), (857, 6), (891, 6), (898, 6), (928, 6), (936, 6), (969, 6), (996, 6)
```

### 2. 292 case(s)

```text
Tree: (Datum(value=Literal(literal=FloatLit(value=-0.5))),)
Text: '-0.5\n'
Result: Parsed(program=(Datum(value=Neg(value=Literal(literal=FloatLit(value=0.5)))),))
Seed, size: (81, 1), (107, 1), (138, 1), (273, 1), (295, 1), (305, 1), (308, 1), (314, 1), (340, 1), (384, 1), (395, 1), (430, 1), (496, 1), (503, 1), (542, 1), (612, 1), (654, 1), (779, 1), (802, 1), (854, 1), (963, 1), (79, 2), (151, 2), (225, 2), (238, 2), (251, 2), (261, 2), (273, 2), (274, 2), (306, 2), (414, 2), (480, 2), (496, 2), (505, 2), (562, 2), (591, 2), (612, 2), (628, 2), (631, 2), (646, 2), (722, 2), (770, 2), (783, 2), (854, 2), (871, 2), (873, 2), (928, 2), (938, 2), (963, 2), (5, 3), (24, 3), (50, 3), (54, 3), (79, 3), (103, 3), (120, 3), (230, 3), (245, 3), (250, 3), (261, 3), (274, 3), (297, 3), (302, 3), (340, 3), (395, 3), (403, 3), (414, 3), (418, 3), (424, 3), (436, 3), (445, 3), (453, 3), (561, 3), (577, 3), (591, 3), (617, 3), (628, 3), (630, 3), (631, 3), (647, 3), (649, 3), (680, 3), (695, 3), (796, 3), (860, 3), (873, 3), (936, 3), (941, 3), (945, 3), (950, 3), (959, 3), (963, 3), (983, 3), (4, 4), (5, 4), (20, 4), (36, 4), (120, 4), (133, 4), (145, 4), (154, 4), (166, 4), (177, 4), (230, 4), (234, 4), (245, 4), (250, 4), (274, 4), (279, 4), (302, 4), (324, 4), (352, 4), (389, 4), (412, 4), (413, 4), (424, 4), (433, 4), (447, 4), (453, 4), (468, 4), (480, 4), (507, 4), (508, 4), (561, 4), (631, 4), (649, 4), (695, 4), (697, 4), (722, 4), (742, 4), (816, 4), (825, 4), (832, 4), (835, 4), (860, 4), (871, 4), (885, 4), (928, 4), (950, 4), (959, 4), (963, 4), (997, 4), (24, 5), (38, 5), (41, 5), (82, 5), (95, 5), (135, 5), (151, 5), (154, 5), (166, 5), (230, 5), (234, 5), (247, 5), (250, 5), (274, 5), (290, 5), (302, 5), (305, 5), (307, 5), (324, 5), (339, 5), (346, 5), (352, 5), (388, 5), (389, 5), (403, 5), (410, 5), (412, 5), (413, 5), (414, 5), (418, 5), (432, 5), (434, 5), (437, 5), (441, 5), (449, 5), (489, 5), (496, 5), (533, 5), (556, 5), (577, 5), (587, 5), (609, 5), (612, 5), (617, 5), (627, 5), (647, 5), (649, 5), (652, 5), (681, 5), (694, 5), (742, 5), (788, 5), (817, 5), (820, 5), (825, 5), (860, 5), (862, 5), (871, 5), (887, 5), (893, 5), (902, 5), (909, 5), (910, 5), (929, 5), (936, 5), (945, 5), (950, 5), (959, 5), (963, 5), (41, 6), (54, 6), (82, 6), (90, 6), (110, 6), (115, 6), (118, 6), (120, 6), (135, 6), (145, 6), (166, 6), (205, 6), (230, 6), (235, 6), (238, 6), (250, 6), (253, 6), (264, 6), (274, 6), (302, 6), (324, 6), (339, 6), (352, 6), (365, 6), (376, 6), (388, 6), (389, 6), (398, 6), (403, 6), (412, 6), (413, 6), (424, 6), (431, 6), (434, 6), (436, 6), (437, 6), (445, 6), (449, 6), (453, 6), (457, 6), (464, 6), (489, 6), (496, 6), (507, 6), (531, 6), (533, 6), (534, 6), (556, 6), (577, 6), (586, 6), (593, 6), (627, 6), (649, 6), (652, 6), (669, 6), (682, 6), (698, 6), (742, 6), (761, 6), (770, 6), (789, 6), (805, 6), (825, 6), (847, 6), (860, 6), (862, 6), (902, 6), (909, 6), (911, 6), (919, 6), (924, 6), (926, 6), (929, 6), (945, 6), (950, 6), (957, 6), (959, 6), (963, 6), (974, 6), (994, 6), (997, 6)
```

### 3. 275 case(s)

```text
Tree: (Datum(value=Literal(literal=IntLit(value=-1))),)
Text: '-1\n'
Result: Parsed(program=(Datum(value=Neg(value=Literal(literal=IntLit(value=1)))),))
Seed, size: (150, 1), (268, 1), (442, 1), (527, 1), (564, 1), (571, 1), (586, 1), (602, 1), (658, 1), (735, 1), (739, 1), (774, 1), (791, 1), (798, 1), (826, 1), (862, 1), (889, 1), (931, 1), (960, 1), (991, 1), (9, 2), (13, 2), (21, 2), (88, 2), (100, 2), (103, 2), (110, 2), (189, 2), (204, 2), (207, 2), (257, 2), (279, 2), (300, 2), (305, 2), (314, 2), (325, 2), (350, 2), (371, 2), (380, 2), (442, 2), (472, 2), (484, 2), (490, 2), (495, 2), (497, 2), (502, 2), (518, 2), (572, 2), (586, 2), (602, 2), (618, 2), (620, 2), (634, 2), (658, 2), (671, 2), (700, 2), (711, 2), (795, 2), (800, 2), (826, 2), (877, 2), (902, 2), (919, 2), (937, 2), (960, 2), (965, 2), (13, 3), (48, 3), (88, 3), (110, 3), (208, 3), (218, 3), (279, 3), (300, 3), (345, 3), (347, 3), (350, 3), (380, 3), (408, 3), (456, 3), (472, 3), (481, 3), (491, 3), (504, 3), (505, 3), (514, 3), (556, 3), (558, 3), (565, 3), (620, 3), (632, 3), (644, 3), (666, 3), (691, 3), (700, 3), (826, 3), (861, 3), (877, 3), (910, 3), (919, 3), (937, 3), (951, 3), (960, 3), (998, 3), (3, 4), (9, 4), (48, 4), (60, 4), (63, 4), (106, 4), (115, 4), (163, 4), (170, 4), (182, 4), (218, 4), (273, 4), (344, 4), (350, 4), (380, 4), (392, 4), (403, 4), (408, 4), (409, 4), (430, 4), (444, 4), (486, 4), (491, 4), (514, 4), (531, 4), (558, 4), (565, 4), (620, 4), (632, 4), (653, 4), (658, 4), (673, 4), (691, 4), (699, 4), (734, 4), (758, 4), (795, 4), (800, 4), (821, 4), (823, 4), (826, 4), (861, 4), (926, 4), (21, 5), (48, 5), (52, 5), (60, 5), (71, 5), (98, 5), (106, 5), (115, 5), (129, 5), (150, 5), (163, 5), (170, 5), (182, 5), (195, 5), (218, 5), (237, 5), (242, 5), (268, 5), (344, 5), (350, 5), (380, 5), (392, 5), (408, 5), (409, 5), (416, 5), (444, 5), (472, 5), (477, 5), (486, 5), (491, 5), (508, 5), (514, 5), (539, 5), (542, 5), (558, 5), (565, 5), (572, 5), (586, 5), (632, 5), (658, 5), (666, 5), (673, 5), (691, 5), (700, 5), (711, 5), (729, 5), (734, 5), (750, 5), (770, 5), (792, 5), (795, 5), (800, 5), (821, 5), (826, 5), (911, 5), (937, 5), (941, 5), (943, 5), (951, 5), (960, 5), (970, 5), (995, 5), (998, 5), (3, 6), (13, 6), (36, 6), (48, 6), (60, 6), (71, 6), (98, 6), (106, 6), (163, 6), (170, 6), (195, 6), (204, 6), (218, 6), (237, 6), (242, 6), (265, 6), (279, 6), (295, 6), (311, 6), (314, 6), (348, 6), (350, 6), (351, 6), (383, 6), (392, 6), (408, 6), (410, 6), (416, 6), (427, 6), (428, 6), (456, 6), (477, 6), (481, 6), (491, 6), (514, 6), (517, 6), (519, 6), (539, 6), (565, 6), (572, 6), (574, 6), (605, 6), (620, 6), (632, 6), (647, 6), (691, 6), (699, 6), (700, 6), (711, 6), (721, 6), (729, 6), (750, 6), (758, 6), (790, 6), (795, 6), (800, 6), (821, 6), (826, 6), (848, 6), (864, 6), (877, 6), (941, 6), (943, 6), (951, 6), (970, 6)
```

### 4. 1 case(s)

```text
Tree: (ImportAct(path='x.lth', names=(ImportName(name='a', theory=None, asName=None),)), Datum(value=Neg(value=Universe())))
Text: 'import "x.lth" a\n-U\n'
Result: ParseFailed(errors=(ParseError(line=2, column=0, message="expected '\\n'; got '-'"),))
Seed, size: (533, 2)
```

### 5. 1 case(s)

```text
Tree: (ImportAct(path='x.lth', names=(ImportName(name='a', theory=None, asName=None),)), Datum(value=Neg(value=Name(name='T'))))
Text: 'import "x.lth" a\n-T\n'
Result: ParseFailed(errors=(ParseError(line=2, column=0, message="expected '\\n'; got '-'"),))
Seed, size: (195, 3)
```

### 6. 5 case(s)

```text
Tree: (ImportAct(path='', names=(ImportName(name='T', theory=None, asName=None),)), Datum(value=Neg(value=Name(name='a'))))
Text: 'import "" T\n-a\n'
Result: ParseFailed(errors=(ParseError(line=2, column=0, message="expected '\\n'; got '-'"),))
Seed, size: (271, 3), (271, 4), (103, 5), (271, 5), (103, 6)
```

### 7. 4 case(s)

```text
Tree: (ImportAct(path='a"\\\nb.lut', names=(ImportName(name='a', theory=None, asName=None),)), Datum(value=Sum(alternatives=(('a', Universe()),))))
Text: 'import "a\\"\\\\\\nb.lut" a\n< a : U >\n'
Result: ParseFailed(errors=(ParseError(line=2, column=0, message="expected '\\n'; got '<'"),))
Seed, size: (293, 3), (293, 4), (293, 5), (293, 6)
```

### 8. 1 case(s)

```text
Tree: (Datum(value=Name(name='T')), Datum(value=Neg(value=Universe())))
Text: 'T\n-U\n'
Result: Parsed(program=(Datum(value=Binop(operator='-', left=Name(name='T'), right=Universe())),))
Seed, size: (391, 3)
```

### 9. 1 case(s)

```text
Tree: (Datum(value=Lambda(params=(ShapeParam(patterns=(PLit(literal=FloatLit(value=-0.0)), PWild())),), items=(), body=Literal(literal=StringLit(value='')))),)
Text: '\\ (-0.0, _) { "" }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=3, message="expected '(', name; got '-'"),))
Seed, size: (427, 3)
```

### 10. 2 case(s)

```text
Tree: (Datum(value=Subtype(pattern=PLit(literal=FloatLit(value=-0.0)), type=World(), law=Universe())),)
Text: '{ -0.0 : W | U }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=7, message="expected '}'; got ':'"),))
Seed, size: (432, 3), (432, 4)
```

### 11. 1 case(s)

```text
Tree: (Datum(value=MatchOf(value=Literal(literal=IntLit(value=1)), arms=((PLit(literal=FloatLit(value=-0.5)), World()),))),)
Text: 'match 1 { -0.5 -> W }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=10, message="expected '('; got '-'"),))
Seed, size: (831, 3)
```

### 12. 1 case(s)

```text
Tree: (ImportAct(path='a"\\\nb.lut', names=(ImportName(name='a', theory=None, asName=None),)), Datum(value=Neg(value=Name(name='a'))))
Text: 'import "a\\"\\\\\\nb.lut" a\n-a\n'
Result: ParseFailed(errors=(ParseError(line=2, column=0, message="expected '\\n'; got '-'"),))
Seed, size: (848, 3)
```

### 13. 2 case(s)

```text
Tree: (Datum(value=MatchOf(value=Name(name='a'), arms=((PLit(literal=FloatLit(value=-0.5)), Universe()),))),)
Text: 'match a { -0.5 -> U }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=10, message="expected '('; got '-'"),))
Seed, size: (871, 3), (670, 5)
```

### 14. 4 case(s)

```text
Tree: (Datum(value=MatchOf(value=Literal(literal=FloatLit(value=0.5)), arms=((PLit(literal=FloatLit(value=-0.0)), Universe()),))),)
Text: 'match 0.5 { -0.0 -> U }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=12, message="expected '('; got '-'"),))
Seed, size: (894, 3), (894, 4), (894, 5), (894, 6)
```

### 15. 1 case(s)

```text
Tree: (Datum(value=Subtype(pattern=PLit(literal=FloatLit(value=-0.5)), type=Literal(literal=FloatLit(value=0.5)), law=Name(name='a'))),)
Text: '{ -0.5 : 0.5 | a }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=7, message="expected '}'; got ':'"),))
Seed, size: (904, 3)
```

### 16. 1 case(s)

```text
Tree: (ImportAct(path='', names=(ImportName(name='a', theory=None, asName=None),)), Datum(value=Neg(value=Name(name='a'))))
Text: 'import "" a\n-a\n'
Result: ParseFailed(errors=(ParseError(line=2, column=0, message="expected '\\n'; got '-'"),))
Seed, size: (924, 3)
```

### 17. 1 case(s)

```text
Tree: (Datum(value=Subtype(pattern=PLit(literal=FloatLit(value=-0.5)), type=Universe(), law=World())),)
Text: '{ -0.5 : U | W }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=7, message="expected '}'; got ':'"),))
Seed, size: (114, 4)
```

### 18. 1 case(s)

```text
Tree: (Datum(value=Subtype(pattern=PLit(literal=IntLit(value=-1)), type=Universe(), law=Name(name='a'))),)
Text: '{ -1 : U | a }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=5, message="expected '}'; got ':'"),))
Seed, size: (193, 4)
```

### 19. 2 case(s)

```text
Tree: (ImportAct(path='x.lth', names=(ImportName(name='a', theory=None, asName=None),)), Datum(value=Neg(value=Name(name='a'))))
Text: 'import "x.lth" a\n-a\n'
Result: ParseFailed(errors=(ParseError(line=2, column=0, message="expected '\\n'; got '-'"),))
Seed, size: (195, 4), (735, 6)
```

### 20. 2 case(s)

```text
Tree: (Datum(value=Subtype(pattern=PLit(literal=FloatLit(value=-0.0)), type=Universe(), law=Universe())),)
Text: '{ -0.0 : U | U }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=7, message="expected '}'; got ':'"),))
Seed, size: (204, 4), (204, 5)
```

### 21. 1 case(s)

```text
Tree: (Datum(value=Name(name='a')), Datum(value=Neg(value=Universe())))
Text: 'a\n-U\n'
Result: Parsed(program=(Datum(value=Binop(operator='-', left=Name(name='a'), right=Universe())),))
Seed, size: (223, 4)
```

### 22. 1 case(s)

```text
Tree: (Define(name='a', binders=(), type=None, body=ClausesBody(clauses=(Clause(patterns=(PLit(literal=IntLit(value=-1)),), body=Literal(literal=StringLit(value=''))),))),)
Text: 'a | -1 := ""\n'
Result: ParseFailed(errors=(ParseError(line=1, column=4, message="expected '('; got '-'"),))
Seed, size: (300, 4)
```

### 23. 1 case(s)

```text
Tree: (Datum(value=Subtype(pattern=PLit(literal=FloatLit(value=-0.0)), type=Universe(), law=World())),)
Text: '{ -0.0 : U | W }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=7, message="expected '}'; got ':'"),))
Seed, size: (306, 4)
```

### 24. 1 case(s)

```text
Tree: (Datum(value=Name(name='T')), Datum(value=Neg(value=Name(name='a'))))
Text: 'T\n-a\n'
Result: Parsed(program=(Datum(value=Binop(operator='-', left=Name(name='T'), right=Name(name='a'))),))
Seed, size: (391, 4)
```

### 25. 1 case(s)

```text
Tree: (Datum(value=Lambda(params=(ShapeParam(patterns=(PLit(literal=FloatLit(value=-0.0)), PWild())),), items=(), body=World())),)
Text: '\\ (-0.0, _) { W }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=3, message="expected '(', name; got '-'"),))
Seed, size: (427, 4)
```

### 26. 1 case(s)

```text
Tree: (Datum(value=MatchOf(value=World(), arms=((PApp(name='a', patterns=(PLit(literal=IntLit(value=-1)),)), Universe()),))),)
Text: 'match W { a -1 -> U }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=12, message="expected '->'; got '-'"),))
Seed, size: (436, 4)
```

### 27. 1 case(s)

```text
Tree: (Datum(value=MatchOf(value=Universe(), arms=((PLit(literal=FloatLit(value=-0.0)), Name(name='a')),))),)
Text: 'match U { -0.0 -> a }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=10, message="expected '('; got '-'"),))
Seed, size: (448, 4)
```

### 28. 1 case(s)

```text
Tree: (Datum(value=MatchOf(value=World(), arms=((PLit(literal=FloatLit(value=-0.5)), Universe()),))),)
Text: 'match W { -0.5 -> U }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=10, message="expected '('; got '-'"),))
Seed, size: (516, 4)
```

### 29. 1 case(s)

```text
Tree: (Datum(value=Name(name='a')), Datum(value=Sum(alternatives=(('a', Universe()),))))
Text: 'a\n< a : U >\n'
Result: ParseFailed(errors=(ParseError(line=2, column=0, message="expected ':', ':=' or clause, '='; got '<'"),))
Seed, size: (517, 4)
```

### 30. 1 case(s)

```text
Tree: (Datum(value=World()), Datum(value=Neg(value=Name(name='a'))))
Text: 'W\n-a\n'
Result: Parsed(program=(Datum(value=Binop(operator='-', left=World(), right=Name(name='a'))),))
Seed, size: (534, 4)
```

### 31. 2 case(s)

```text
Tree: (Datum(value=Subtype(pattern=PLit(literal=IntLit(value=-1)), type=Name(name='a'), law=World())),)
Text: '{ -1 : a | W }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=5, message="expected '}'; got ':'"),))
Seed, size: (791, 4), (791, 6)
```

### 32. 2 case(s)

```text
Tree: (Datum(value=MatchOf(value=Literal(literal=IntLit(value=1)), arms=((PLit(literal=FloatLit(value=-0.5)), Name(name='a')),))),)
Text: 'match 1 { -0.5 -> a }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=10, message="expected '('; got '-'"),))
Seed, size: (831, 4), (831, 5)
```

### 33. 3 case(s)

```text
Tree: (Datum(value=Subtype(pattern=PLit(literal=IntLit(value=-1)), type=List(values=()), law=Name(name='a'))),)
Text: '{ -1 : [] | a }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=5, message="expected '}'; got ':'"),))
Seed, size: (865, 4), (865, 5), (865, 6)
```

### 34. 1 case(s)

```text
Tree: (Datum(value=Subtype(pattern=PTuple(patterns=(PLit(literal=FloatLit(value=-0.0)), PWild())), type=Name(name='a'), law=Literal(literal=IntLit(value=1)))),)
Text: '{ (-0.0, _) : a | 1 }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=9, message="expected '(', argument atom; got '_'"),))
Seed, size: (900, 4)
```

### 35. 1 case(s)

```text
Tree: (Datum(value=Subtype(pattern=PLit(literal=IntLit(value=-1)), type=Name(name='a'), law=Literal(literal=FloatLit(value=0.5)))),)
Text: '{ -1 : a | 0.5 }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=5, message="expected '}'; got ':'"),))
Seed, size: (120, 5)
```

### 36. 1 case(s)

```text
Tree: (Datum(value=Name(name='a')), Datum(value=Neg(value=Name(name='a'))))
Text: 'a\n-a\n'
Result: Parsed(program=(Datum(value=Binop(operator='-', left=Name(name='a'), right=Name(name='a'))),))
Seed, size: (223, 5)
```

### 37. 1 case(s)

```text
Tree: (Define(name='a', binders=(), type=None, body=ClausesBody(clauses=(Clause(patterns=(PLit(literal=IntLit(value=-1)),), body=Name(name='a')),))),)
Text: 'a | -1 := a\n'
Result: ParseFailed(errors=(ParseError(line=1, column=4, message="expected '('; got '-'"),))
Seed, size: (248, 5)
```

### 38. 1 case(s)

```text
Tree: (Datum(value=Name(name='a')), Datum(value=Sum(alternatives=(('a', Literal(literal=IntLit(value=1))),))))
Text: 'a\n< a : 1 >\n'
Result: ParseFailed(errors=(ParseError(line=2, column=0, message="expected ':', ':=' or clause, '='; got '<'"),))
Seed, size: (333, 5)
```

### 39. 1 case(s)

```text
Tree: (Datum(value=Lambda(params=(ShapeParam(patterns=(PLit(literal=FloatLit(value=-0.0)), PWild())),), items=(), body=Name(name='a'))),)
Text: '\\ (-0.0, _) { a }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=3, message="expected '(', name; got '-'"),))
Seed, size: (427, 5)
```

### 40. 1 case(s)

```text
Tree: (ImportAct(path='x.lth', names=(ImportName(name='T', theory=None, asName=None),)), Datum(value=Sum(alternatives=(('a', Universe()),))))
Text: 'import "x.lth" T\n< a : U >\n'
Result: ParseFailed(errors=(ParseError(line=2, column=0, message="expected '\\n'; got '<'"),))
Seed, size: (506, 5)
```

### 41. 2 case(s)

```text
Tree: (Define(name='a', binders=(), type=None, body=ClausesBody(clauses=(Clause(patterns=(PLit(literal=FloatLit(value=-0.0)),), body=World()),))),)
Text: 'a | -0.0 := W\n'
Result: ParseFailed(errors=(ParseError(line=1, column=4, message="expected '('; got '-'"),))
Seed, size: (527, 5), (426, 6)
```

### 42. 1 case(s)

```text
Tree: (Define(name='a', binders=(), type=None, body=DataBody(constructors=())), Datum(value=Neg(value=Name(name='a'))))
Text: 'a := data { }\n-a\n'
Result: ParseFailed(errors=(ParseError(line=1, column=2, message="expected ':', '='; got ':='"),))
Seed, size: (534, 5)
```

### 43. 1 case(s)

```text
Tree: (Define(name='a', binders=(), type=None, body=DataBody(constructors=())), Datum(value=Sum(alternatives=(('a', Name(name='a')),))))
Text: 'a := data { }\n< a : a >\n'
Result: ParseFailed(errors=(ParseError(line=1, column=2, message="expected ':', '='; got ':='"),))
Seed, size: (641, 5)
```

### 44. 2 case(s)

```text
Tree: (Datum(value=Subtype(pattern=PTuple(patterns=(PWild(), PLit(literal=FloatLit(value=-0.0)))), type=Name(name='a'), law=Name(name='a'))),)
Text: '{ (_, -0.0) : a | a }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=6, message="expected '('; got '-'"),))
Seed, size: (802, 5), (802, 6)
```

### 45. 1 case(s)

```text
Tree: (Define(name='a', binders=(), type=None, body=ClausesBody(clauses=(Clause(patterns=(PLit(literal=FloatLit(value=-0.0)),), body=Name(name='a')),))),)
Text: 'a | -0.0 := a\n'
Result: ParseFailed(errors=(ParseError(line=1, column=4, message="expected '('; got '-'"),))
Seed, size: (827, 5)
```

### 46. 1 case(s)

```text
Tree: (Datum(value=Subtype(pattern=PTuple(patterns=(PTuple(patterns=(PWild(), PLit(literal=IntLit(value=-1)))), PWild())), type=Universe(), law=World())),)
Text: '{ ((_, -1), _) : U | W }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=7, message="expected '('; got '-'"),))
Seed, size: (900, 5)
```

### 47. 1 case(s)

```text
Tree: (Datum(value=MatchOf(value=Universe(), arms=((PLit(literal=FloatLit(value=-0.0)), World()),))),)
Text: 'match U { -0.0 -> W }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=10, message="expected '('; got '-'"),))
Seed, size: (4, 6)
```

### 48. 1 case(s)

```text
Tree: (Define(name='a', binders=(), type=None, body=ClausesBody(clauses=(Clause(patterns=(PLit(literal=FloatLit(value=-0.5)),), body=World()),))),)
Text: 'a | -0.5 := W\n'
Result: ParseFailed(errors=(ParseError(line=1, column=4, message="expected '('; got '-'"),))
Seed, size: (148, 6)
```

### 49. 1 case(s)

```text
Tree: (Datum(value=Lambda(params=(ShapeParam(patterns=(PLit(literal=FloatLit(value=-0.5)), PWild())),), items=(), body=Universe())),)
Text: '\\ (-0.5, _) { U }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=3, message="expected '(', name; got '-'"),))
Seed, size: (153, 6)
```

### 50. 1 case(s)

```text
Tree: (Datum(value=MatchOf(value=Literal(literal=IntLit(value=0)), arms=((PLit(literal=FloatLit(value=-0.0)), Universe()),))),)
Text: 'match 0 { -0.0 -> U }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=10, message="expected '('; got '-'"),))
Seed, size: (187, 6)
```

### 51. 1 case(s)

```text
Tree: (Datum(value=MatchOf(value=World(), arms=((PLit(literal=FloatLit(value=-0.0)), World()),))),)
Text: 'match W { -0.0 -> W }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=10, message="expected '('; got '-'"),))
Seed, size: (223, 6)
```

### 52. 1 case(s)

```text
Tree: (Datum(value=MatchOf(value=Universe(), arms=((PLit(literal=FloatLit(value=-0.5)), Name(name='a')),))),)
Text: 'match U { -0.5 -> a }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=10, message="expected '('; got '-'"),))
Seed, size: (362, 6)
```

### 53. 1 case(s)

```text
Tree: (ImportAct(path='', names=(ImportName(name='a', theory=None, asName=None),)), Datum(value=Sum(alternatives=(('a', Name(name='a')),))))
Text: 'import "" a\n< a : a >\n'
Result: ParseFailed(errors=(ParseError(line=2, column=0, message="expected '\\n'; got '<'"),))
Seed, size: (400, 6)
```

### 54. 1 case(s)

```text
Tree: (ImportAct(path='x.lth', names=(ImportName(name='T', theory=None, asName=None),)), Datum(value=Sum(alternatives=(('a', Name(name='a')),))))
Text: 'import "x.lth" T\n< a : a >\n'
Result: ParseFailed(errors=(ParseError(line=2, column=0, message="expected '\\n'; got '<'"),))
Seed, size: (506, 6)
```

### 55. 1 case(s)

```text
Tree: (Datum(value=Subtype(pattern=PTuple(patterns=(PLit(literal=FloatLit(value=-0.0)), PWild())), type=Name(name='a'), law=Universe())),)
Text: '{ (-0.0, _) : a | U }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=9, message="expected '(', argument atom; got '_'"),))
Seed, size: (587, 6)
```

### 56. 1 case(s)

```text
Tree: (Datum(value=Subtype(pattern=PLit(literal=FloatLit(value=-0.5)), type=World(), law=World())),)
Text: '{ -0.5 : W | W }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=7, message="expected '}'; got ':'"),))
Seed, size: (595, 6)
```

### 57. 1 case(s)

```text
Tree: (Datum(value=MatchOf(value=Universe(), arms=((PLit(literal=IntLit(value=-1)), Universe()),))),)
Text: 'match U { -1 -> U }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=10, message="expected '('; got '-'"),))
Seed, size: (609, 6)
```

### 58. 1 case(s)

```text
Tree: (Datum(value=Subtype(pattern=PLit(literal=FloatLit(value=-0.5)), type=Name(name='a'), law=Name(name='a'))),)
Text: '{ -0.5 : a | a }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=7, message="expected '}'; got ':'"),))
Seed, size: (659, 6)
```

### 59. 1 case(s)

```text
Tree: (Datum(value=Subtype(pattern=PTuple(patterns=(PWild(), PLit(literal=IntLit(value=-1)))), type=Universe(), law=Universe())),)
Text: '{ (_, -1) : U | U }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=6, message="expected '('; got '-'"),))
Seed, size: (666, 6)
```

### 60. 1 case(s)

```text
Tree: (Datum(value=MatchOf(value=Name(name='a'), arms=((PLit(literal=FloatLit(value=-0.0)), Universe()),))),)
Text: 'match a { -0.0 -> U }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=10, message="expected '('; got '-'"),))
Seed, size: (680, 6)
```

### 61. 1 case(s)

```text
Tree: (ImportAct(path='a"\\\nb.lut', names=(ImportName(name='T', theory=None, asName=None),)), Datum(value=Sum(alternatives=(('a', List(values=())),))))
Text: 'import "a\\"\\\\\\nb.lut" T\n< a : [] >\n'
Result: ParseFailed(errors=(ParseError(line=2, column=0, message="expected '\\n'; got '<'"),))
Seed, size: (757, 6)
```

### 62. 1 case(s)

```text
Tree: (Define(name='a', binders=(), type=None, body=ClausesBody(clauses=(Clause(patterns=(PTuple(patterns=(PLit(literal=IntLit(value=-1)), PWild())),), body=Name(name='a')),))),)
Text: 'a | (-1, _) := a\n'
Result: ParseFailed(errors=(ParseError(line=1, column=5, message="expected '('; got '-'"),))
Seed, size: (829, 6)
```

### 63. 1 case(s)

```text
Tree: (Datum(value=Subtype(pattern=PLit(literal=FloatLit(value=-0.0)), type=Literal(literal=IntLit(value=0)), law=Name(name='a'))),)
Text: '{ -0.0 : 0 | a }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=7, message="expected '}'; got ':'"),))
Seed, size: (831, 6)
```

### 64. 1 case(s)

```text
Tree: (Datum(value=Subtype(pattern=PLit(literal=FloatLit(value=-0.0)), type=Name(name='a'), law=Universe())),)
Text: '{ -0.0 : a | U }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=7, message="expected '}'; got ':'"),))
Seed, size: (871, 6)
```

### 65. 1 case(s)

```text
Tree: (Datum(value=MatchOf(value=Name(name='a'), arms=((PLit(literal=FloatLit(value=-0.0)), Name(name='a')),))),)
Text: 'match a { -0.0 -> a }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=10, message="expected '('; got '-'"),))
Seed, size: (889, 6)
```

### 66. 1 case(s)

```text
Tree: (Datum(value=Subtype(pattern=PTuple(patterns=(PTuple(patterns=(PWild(), PLit(literal=IntLit(value=-1)))), PWild())), type=Universe(), law=Name(name='a'))),)
Text: '{ ((_, -1), _) : U | a }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=7, message="expected '('; got '-'"),))
Seed, size: (900, 6)
```

### 67. 1 case(s)

```text
Tree: (Datum(value=MatchOf(value=World(), arms=((PLit(literal=IntLit(value=-1)), Name(name='a')),))),)
Text: 'match W { -1 -> a }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=10, message="expected '('; got '-'"),))
Seed, size: (916, 6)
```

### 68. 1 case(s)

```text
Tree: (Datum(value=MatchOf(value=Literal(literal=FloatLit(value=0.5)), arms=((PLit(literal=FloatLit(value=-0.5)), Name(name='a')),))),)
Text: 'match 0.5 { -0.5 -> a }\n'
Result: ParseFailed(errors=(ParseError(line=1, column=12, message="expected '('; got '-'"),))
Seed, size: (965, 6)
```

