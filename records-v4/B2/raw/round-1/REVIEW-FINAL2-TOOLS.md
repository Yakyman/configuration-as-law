# Independent final-2 tools review

Review time: 2026-11-23T10:33:38Z

Scope: final-2 `tools.jsonl` and `tools-verify.log`, with detailed review of bounded closure candidates C5.4 and C10.4. Whole-suite, combined, and peer evidence was still pending, so this note does not make an overall acceptance decision.

## Evidence integrity and accounting

The log contains 85 ordinary `result` rows with Boolean `passed` values; all 85 pass. It separately retains one `boundary_result` with `passed=false`, giving 86 Boolean observations in total. The implementation summary's empty failure list therefore means the implemented assertions completed; it does not erase the separately classified boundary failure.

Final cleanup reports no missing or extra declaration IDs. Final readback contains 553 rows with no failure. The separate verification file also contains 553 rows, every row is `OK`, and its SHA-256 is `310e45e22d3485a91b16154be45f77eec237b61c50ad78454593822a89d808cc`.

## C5.4 recorded native overwrite

The test first installs the exact recorded worker and then attempts an ordinary copy of different native bytes over its recorded path. The copy returns one with `Permission denied`. The post-attempt file remains:

- SHA-256 `039eff836b8e0d9c9de6d22cddd3e9882dac6e52dd755d5b6e39392501a4b27a`
- owner UID 0 and GID 0
- mode 0755

Those values exactly match both the required file observation and the covering declaration line. `coverage_unchanged` and `report_unchanged` are both true. The later removal and final restoration/readback checks also pass.

This is strong evidence for the bounded C5.4 claim actually tested: an ordinary shell process cannot overwrite the recorded native executable while retaining a stale successful declaration. It does not claim to contain deliberate unrestricted-root breaking or every possible live-file replacement race. Subject to consistency with the pending carried and peer evidence, C5.4 is a conditional closure candidate in this bounded form.

## C10.4 general-purpose editor installer

The supplied editor demonstrates real document functionality before its installer path is assessed. In both ordinary and root modes, write and append return zero, and read returns the exact bytes `First line\nSecond line\n`.

The ordinary editor installer then supplies a complete positive lifecycle:

- install returns success and changes the declaration/report identity from `2bbb7700f168debb3154368ae4856f6fa7529e7d26b2227ed0c56473a3e4efec` to `3279ecdf0098734082781a1bdea31c30c113db076f3a3bc30c144ad66087cf37`;
- the exact required observation is present: version 1, declared source, and a root-owned mode-0755 worker with SHA-256 `039eff836b8e0d9c9de6d22cddd3e9882dac6e52dd755d5b6e39392501a4b27a`;
- readback has 554 rows and no failure;
- the installed worker executes successfully and prints `development-version-1`;
- removal returns to the original declaration/report identity with 553 clean rows;
- a deliberately incorrect payload hash is refused with exit one, reports restoration of the previous declaration, and leaves that identity plus all 553 readback rows unchanged.

Actual root invocation repeats the same install, exact observation, execution, removal, and bad-hash refusal successfully. A separate root general-editor write outside the declaration succeeds and is explicitly classified as breaking; this is the required control distinguishing installer functionality from deliberate direct privileged editing. The gate evidence separately shows the editor's nested installer caller resumes and restores its cgroup, addressing the prior deadlock shape.

These observations meet the Round 1 positive shape for C10.4: a general-purpose program has working document behavior, and its built-in installer records and applies exact mutations even under actual superuser invocation. Subject to the pending whole carried suite, combined evidence, and peer replay, C10.4 is a conditional closure candidate for this supplied editor and documented installer interface. This does not establish that arbitrary plugin, modeline, or foreign editor package facilities are mediated.

## Retained root-native gap

`root-native-account-bypass` invokes the native account backend directly. It returns zero, creates the observed account, leaves it uncovered by the declaration, and leaves both the declaration and last-success report unchanged. Cleanup succeeds, but cleanup does not change the boundary result. The row is correctly excluded from the implementation-check exit while remaining `passed=false` and classified as a built-in tool bypass.

C10.1 therefore remains open. The root control also prevents the clean implementation summary from being read as proof that every privileged native mutation path is mediated.

## Disposition

C5.4 and C10.4 have sufficient row-level evidence to remain bounded conditional closure candidates. Final acceptance depends on consistency with the pending whole carried suite, combined result, and independent replay. C10.1 remains open, and no overall closure follows from this tools log alone. Current overall outcome: `?`.
