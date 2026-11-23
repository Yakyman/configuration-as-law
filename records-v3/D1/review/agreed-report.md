# Review of the agreed-row sample

Seed: `2026112202`. Selection: `random.Random(2026112202).sample(eligible, 60)`, retaining source order in `../compare/joined.tsv`; eligible rows have equal decisions and no id in `../adjudication/rows.tsv`. TSV parsing used `csv.QUOTE_NONE`. Every individual assessment and ordered id is in `agreed-sample.tsv`.

Counts: 60 reviewed; 57 agreed decisions upheld; 3 agreed NOT decisions unsupported; 3 resulting candidates REFUTED by a sentence deciding MUST; 0 confirmed new holes; 0 UNKNOWN. All three candidates concern package metadata as in existing card 3, not distinct gaps.

Per-machine sample counts: fedora: 26, flatcar: 3, mint: 7, tumbleweed: 24.

## Dependency-metadata candidates

- `fedora-fe662177103b7d48f6e25461`, `user:default-fonts-syr`: requires `google-noto-sans-syriac-vf-fonts`.
- `fedora-4ffd8592f62f9410b26561b5`, `root:default-fonts-el`: requires `abattis-cantarell-vf-fonts` and `google-noto-sans-vf-fonts`.

Evidence: `agreed-evidence/font-dependencies.json`, extracted from (not published: adjudication scratch); versions match the inventory. For the two font metapackages, both classifications restrict removal to immediate runtime changes or surviving dependency files. S2.2-1 has no such restriction: package selection and retention depend on these requirements, deciding both examples MUST.

S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

Verdict: REFUTED as a hole candidate. S2.2-2 has no immediate-effect restriction either; temporarily unchanged runtime does not negate S2.2-1. These are classification errors, not an undecidable definition.

## Additional factual checks

`mint-707cb6be107ec462ef11c223` (`root:gnome-terminal-data`) is the third REFUTED candidate, resolved MUST by S2.2-1. The exact installed-version archive was downloaded and its SHA256 matches the saved distribution index; its payload contains only documentation/help and figures, but the inventory row represents the package, including metadata. The exact-version package Recommends `gnome-terminal`, and the installed `gnome-terminal` package Depends on `gnome-terminal-data (<< 3.54)` and `gnome-terminal-data (>= 3.52)`. Package-manager selection and valid installed dependencies therefore depend on this package record. Evidence: `agreed-evidence/gnome-terminal-dependencies.json`, extracted from `(not published: adjudication scratch)`; installed version in `../in/raw/mint/raw/003-packages-root-dpkg-query.out`. S2.2-4 exempts the documentation payload, not the dependency metadata that accompanies it.

S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”

`fedora-326ef74881e5a0fc2709f47d` remains MUST on the c1 reasoning: raw nftables data shows the empty chain is a target of an existing jump. c2 incorrectly says it holds rules, but the required jump target independently supports c1's cited removal rule.

Inactive/disabled/static service rows remain MUST because the unit enables a manager activation route for a separate process. The definition includes what can be done, not only running processes. A saved wired-network profile similarly affects other processes, so the one-program settings exemption does not apply.

## Ordered selected ids

1. `tumbleweed-9f79d7376d1f97ff2e44a834`
2. `fedora-3ec0c644b542f85244ed4838`
3. `mint-97c5486cec105a00e80891bb`
4. `mint-dc99cfca67e04dc9a463e60a`
5. `fedora-8d3a021b56d26bf21a06a54c`
6. `fedora-12da29ca3a02120dce8ff699`
7. `tumbleweed-b4fcc756cd30803fd88aea98`
8. `tumbleweed-7b2a1f522c63882a2fc6ebf8`
9. `tumbleweed-0726f781d916a92bf02c6d7f`
10. `fedora-51a77ef359241936e64f68df`
11. `fedora-c4ea272afcadfbd48f344c75`
12. `fedora-c705409e9477a35f5cc89447`
13. `fedora-4aa54f4efcabe5d9a294458a`
14. `fedora-bf3968c3ee4b6b46b56352b9`
15. `fedora-212a1e3ba67399a001c579b4`
16. `mint-63e879ba5ee8c49695c94ea9`
17. `fedora-5942249d5e655e1d1a7c0d56`
18. `tumbleweed-fa240a387865efac1dd43666`
19. `tumbleweed-4d4f0b8c774b07bb513afac9`
20. `tumbleweed-91003489d9c6d84b6bd5a5e7`
21. `tumbleweed-c95df4a564bfa0e3f2f09a73`
22. `tumbleweed-c4ef395d38d3a614ca9f8302`
23. `fedora-5b68e3dc04b7b8b5cfd0afa5`
24. `fedora-28c216a71283786282775416`
25. `mint-bc41331ff129903dc0b09a21`
26. `fedora-5acaf8447708970114d3dc27`
27. `fedora-0afcc521a3e91400b3a89dd2`
28. `mint-6b6a8fe60f6058d0de0c6c1d`
29. `flatcar-9bf281bd2d8812ec0c3e8b1a`
30. `fedora-d038b9f2df0f708c6eb72d44`
31. `tumbleweed-245847a7ea30f82c067d5994`
32. `fedora-08f178c642f191fd49e710a6`
33. `tumbleweed-201081d4670a9aef147c1943`
34. `fedora-326ef74881e5a0fc2709f47d`
35. `flatcar-a8c2abafb3d21cfe62d7580a`
36. `fedora-0f9482f3584c68fd2cac1635`
37. `tumbleweed-6a56c03b8ce3a8e6f0bffa35`
38. `tumbleweed-9e3fcb44dad250c4700e2fb3`
39. `tumbleweed-6496d8e20d115e3518636540`
40. `mint-5e1387f5416db3badd95a123`
41. `fedora-17cb7bd3fd73ff65cad3ee5e`
42. `flatcar-113362e7a33674cb82c3b70f`
43. `fedora-9098ac5dad67558e0061a2a8`
44. `fedora-1f3528bf8bedb8b64670f909`
45. `mint-707cb6be107ec462ef11c223`
46. `tumbleweed-a9b7a289416b73756ee0aea3`
47. `tumbleweed-f8ffef08623a44ad4fa7ad4b`
48. `tumbleweed-01f25b99aa695227cbb23a44`
49. `tumbleweed-af69fb9a758bbeccfd138777`
50. `fedora-fe662177103b7d48f6e25461`
51. `fedora-71515af2ff1175eb48fdabbb`
52. `fedora-369e8b2526e051513f79365b`
53. `fedora-4ffd8592f62f9410b26561b5`
54. `tumbleweed-21813a8e17f874a2efb43d95`
55. `tumbleweed-56fa5e5b00aa8c2e22d59728`
56. `fedora-6f26bf26bf66cfb47746c256`
57. `tumbleweed-f278fd47c907b03f8e0daa91`
58. `tumbleweed-9f9ce322794880bf1d360e92`
59. `tumbleweed-d713b2116a5f560887330aa9`
60. `tumbleweed-13c258c87ec0f6ae7ed58bf6`

Revision recorded 2026-11-22 UTC: initial payload-only review upheld gnome-terminal-data as NOT; the full-package metadata check corrects this to MUST. Counts above and the row assessment include this correction. The original agreed NOT remains visible in the sample table. The sole upheld NOT is the nonpackage Flatcar .keep marker.
