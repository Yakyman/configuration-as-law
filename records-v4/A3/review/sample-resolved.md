# Resolved-row sample audit

Seed: `2026112302`. Eligible rows: 2500. Algorithm: sort rows whose verdict begins `RESOLVED:` by full id, then `random.Random(2026112302).sample(eligible, 40)`; draw order is preserved in `sample-resolved.tsv`.

Results: 22 upheld, 18 FACT_UNKNOWN, 0 confirmed textual gaps, 0 fact-wrong cards, 0 outside-definition candidates. Every row has an individual reason, exact full sentences, and evidence in the TSV. UPHELD means that an alleged gap is refuted by applying the text to the identified members; it does not certify unobserved integrity or exclusive recording-line necessity.

The failed resolutions have factual rather than definitional limits: nine package-content rows lack a received-content comparison; six Go build-cache groups lack payload contents/executability; one shader-cache payload lacks contents/capability facts; one persistent PrivateTmp entry lacks a demonstrated runtime-only lifecycle; one plugin directory lacks demonstrated creation provenance. A timestamp within an installer run is not an unchanged-content test, and absence of observed execution is not inability to execute. These rows do not establish a counterexample with fixed facts.

S8.2-7 «Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?»

S8.2-9 «Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?»

S8.2-5 «What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.»

The upheld material rows contain the brought checkout itself, not repository history: the explicit projects example in S8.2-15 decides them. The upheld download-cache rows contain archives/metadata or a containing directory, not the extracted installed trees in card 4. For code rows, S8.2-16 allows an own line; this audit does not infer that every other listed line form is forbidden.

## Sample ids in draw order

1. `gaming-6aa4c4f583cd7406507262fb` — FACT_UNKNOWN
2. `developer-94b46e17a7fdba7b45243e7c` — UPHELD
3. `developer-3ab6235a7d81b8e624281974` — UPHELD
4. `developer-4d7b3ef8e06203c9cb37471d` — FACT_UNKNOWN
5. `gaming-b442a015395b03e7e310f16d` — FACT_UNKNOWN
6. `developer-599009507b02a329f47c254e` — UPHELD
7. `developer-2b039a17e2a57d841b207b78` — UPHELD
8. `developer-032e1edbcb1b06028a8ffaa3` — FACT_UNKNOWN
9. `developer-5b16a3bb0b5e4c0f22684448` — FACT_UNKNOWN
10. `gaming-2f48787930753cfda329e60b` — UPHELD
11. `developer-bbc2e5baede0484d47b112a1` — FACT_UNKNOWN
12. `developer-2f1aac18cceca7a98655895b` — UPHELD
13. `server-c97d776897302639e8a3ff64` — FACT_UNKNOWN
14. `gaming-4289cd9fd81aa08409e7bddc` — FACT_UNKNOWN
15. `developer-ab5fe526f69bd0639c68f00f` — FACT_UNKNOWN
16. `developer-1697be08986bd334449fcec2` — UPHELD
17. `developer-8f9616897f4a2f5b2559b68e` — FACT_UNKNOWN
18. `developer-3d4490b8aaf19b8a81cf4774` — FACT_UNKNOWN
19. `developer-c89f81f1f511aef856763cd4` — FACT_UNKNOWN
20. `server-6db1cc6778642fdc9ff68fd2` — FACT_UNKNOWN
21. `developer-52b8e6e14450aa20f0340002` — UPHELD
22. `developer-95586c676e3caba1d88defbc` — FACT_UNKNOWN
23. `developer-9901839eda919eeece7bd12f` — UPHELD
24. `developer-81c791ce6b4ed5c2c6b87748` — UPHELD
25. `developer-0377e290c9adaa8a4697e867` — UPHELD
26. `developer-6be6d490afe16d8d52b02208` — FACT_UNKNOWN
27. `developer-4015d8ac3d923d8552a6e7f1` — UPHELD
28. `developer-7e47ed90433bc7f91ccae7d4` — UPHELD
29. `developer-ae1325646ddd491312883b7c` — UPHELD
30. `developer-a6692d40a92a62f6e2c098f5` — FACT_UNKNOWN
31. `developer-79d6940de5fc340793323b4a` — FACT_UNKNOWN
32. `developer-7fa58793f537e83cdaebaa9e` — UPHELD
33. `developer-54c1c38a2efe6efd041f47c7` — UPHELD
34. `developer-94bb772856ad0b47bc2484f6` — UPHELD
35. `developer-cf2588417916cb42778a118d` — UPHELD
36. `developer-6ceecc894aff65cef477a2a9` — UPHELD
37. `gaming-eace6aea0c237c5cb75ca42f` — UPHELD
38. `developer-20cf01912cfe693081d9e3c0` — UPHELD
39. `developer-bcb3cd08147ef9b0a3e2b2e0` — FACT_UNKNOWN
40. `developer-f008beb8f1c64bf882401b19` — UPHELD
