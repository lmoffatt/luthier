# Source of this graph

`nodes.csv` and `measurements.csv` are copies, byte for byte, of
`prototipo-cero/2026-09-07/derived/A/graph/nodes.csv` and `measurements.csv` in the sonolocalización
repository (`/home/lmoffatt/Projects/sonolocalizacion`), read at its commit
5ffc36ef70e16e11182bc09e4a927c381e35df1c. Both files were last changed there in commit
fecdae987bbdad11432f05347c598e7814ce8581 (2026-10-04).

| file | sha256 |
|---|---|
| nodes.csv | b2a97cb0008e67ee0c11ceffef506a3f5e0b2ee9ba7d9ba7e340ecbcdd05be45 |
| measurements.csv | 9355ef13a67f56a685bacafaf8e0c30f712b5c66e7c9d8db792cb47adc6c0fc4 |

Session A of experiment zero: 10 nodes and 22 measurements, the A2 block included (parlante_A2 to
mic3, mic2 and mic1 at 1.13, 3.35 and 2.02 m, which the sonolocalización session calls
geometrically impossible). This graph predates D-2026-10-06-sa (the model horizontal) and
D-2026-10-06-sb (mic1's rows as measurements) of sonolocalización: it lacks the four
mic1-to-peripheral 3.50 m measurements, and fixes mic1 at the origin through its prior. Its file
schema did not change with sa, so it still parses and validates, but it is not the corrected input
(`record/IA/sonolocalizacion-inventory-2026-10-13/answers-2026-10-14.md`, item 1). The corrected
graph is made by `prepare_experiment_zero.py` there, a data script for Luciano to run.

Copied 2026-10-14 for the port of `validate_graph.lut` (`record/IA/slice-port-2026-10-14/prompt.md`).
