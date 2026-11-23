VERDICT: DISAGREE

Review of `RESULT.md` (check 1, Section 4.2), recorded 2026-11-22 UTC. Inputs read: (not published: outside selected checks and direct evidence), `../TEXT.md` Sections 2–4, `../SENTENCES.md`, `RESULT.md`, `compare/STATS.md`, `adjudication/HOLES.md`, the whole of `adjudication/rows.tsv` and `compare/joined.tsv` (for the recount), and, for eight sampled claims only, the evidence files those claims cite. The combined outcome `OUTCOME: 0` is correct and the numbers match the data (finding 9). The disagreement concerns how 924 adjudicated HOLE rows were narrowed to "1 confirmed holes" and how the per-machine outcomes were set: several steps choose between readings of the text or add a rule, which (not published: outside selected checks and direct evidence) and Section 4.2 do not allow.

1. **The per-machine outcomes override the adjudication, which Section 4.1 does not allow.**
   Where: `RESULT.md`, lines 1–6 and the machine table (Fedora, Tumbleweed and Flatcar are given `?`).
   Evidence: `adjudication/rows.tsv` has 924 `HOLE` verdicts (Fedora 328, Tumbleweed 363, Mint 136, Flatcar 97; recounted). Section 4.1: "When they differ, a separate adjudication, made by neither classification, decides whether the text of Sections 2 and 3 resolves the case … if no sentence resolves it, the case yields 0." The published text has no later stage that can overturn an adjudication verdict. The only "separate review" in Section 4.1 is for testbed-failure arguments (check 2).
   Minimal fix: report the Section 4.1 case outcome for each machine from the adjudication (Fedora 0, Tumbleweed 0, Mint 0, Flatcar 0, Talos ?). Present the narrowing to one row as a separately labelled verification layer, not as the outcome of those cases.

2. **The "package metadata" ground adds a rule and was used to refute most of cards 1, 2, 5 and 7.**
   Where: `RESULT.md`, the paragraph "The strongest successful refutation of most other card-1/card-2 rows is package metadata…", the Card 2/5/7 lines, and the nine "Corrected to MUST" resolved rows and three "incorrect agreements".
   Evidence: in `review/cards-1-4.md`, `tumbleweed-25d4e59fef6a08262890c4c4` (google-roboto-fonts) is MUST because "Whole package has operational requirement(s): /bin/sh, /bin/sh, aaa_base, coreutils, coreutils, perl", and `fedora-e94d6040fe6b71468614c285` because of "/bin/sh". `review/resolved-sample.tsv` row 11 (`displaymanager-sysconfig`) is MUST because it "requires /bin/sh, /usr/bin/mkdir, /usr/bin/touch and fillup". In `review/cards-5-8.md`, media-player-info "requires /bin/sh". Removing a package that only *requires* something stops nothing and makes nothing impossible. It only frees the required package for removal, so the removal test S2.2-2 ("The test is removal: …") is negative. MUST follows only if S2.2-1 is read as a separate test, wider than the test S2.2-2 names. That is a choice between readings. The adjudication recorded exactly this open question in card 3 ("the text does not say whether package metadata that steers the package manager counts as something the computer's behaviour depends on"). `review/cards14-raw/metadata-audit.tsv` lines 111 and 232 show the effect: the Fedora emoji font package (`google-noto-color-emoji-fonts`) is MUST only through "fontpackages-filesystem", while the Mint emoji font, whose payload has the same role, is the one confirmed hole. So the decision turns on a packaging field that has no removal effect.
   Minimal fix: do not refute with this reading. Record it as a question for the author, or keep the cards it would refute, and recompute the extents of cards 1, 2, 5 and 7 without it. The "exact established extent" of one row holds only under this reading and should say so.

3. **Card 3 "REFUTED" adds an action to the removal test.**
   Where: `RESULT.md`, Card 3 line ("S2.2-2 contains no immediate-only restriction"); `review/cards-1-4.md`, "Card 3: REFUTED".
   Evidence: on the card's own facts, removing a metapackage changes nothing until a further package-manager run (autoremove or a new selection). The effect follows that later action, not the removal. The fallback argument ("the constraints already affect what the package manager may do") points the other way: removal makes more things possible, while S2.2-2 asks whether something "stops" or "becomes impossible". Deciding MUST means reading S2.2-2 as "after removal and a later package-manager run", which adds words.
   Minimal fix: restore card 3 as CONFIRMED (two readings, no deciding sentence), or record it as a question for the author. Do not report it as REFUTED.

4. **Card 5: the result admits two readings but still reports REFUTED, and S3-2 is misapplied.**
   Where: `RESULT.md`, Card 5 line and the 114-row UNKNOWN set; `review/card5-challenge.md`.
   Evidence: `review/card5-challenge.md` says that "the semantic counterexample has two explicit readings, and no quoted sentence selects one". That is the Section 4.2 failure condition ("allows deciding both ways"). The two remaining rows (`fedora-eaecd855d3b238f815d51e72`, `fedora-369a1218fca1b15b045403ef`, alsa-sof-firmware) were moved to UNKNOWN under S3-2 ("If what the object does remains unknown, the case yields ?"). But what they do is established: the `adjudication/rows.tsv` note reads "Device firmware files only (F45 filelists); present devices are virtio, bochs, PIIX, i8042, no USB or sound". The only open point is whether a hardware addition belongs in the removal test, and that is a question about the text, not a missing fact. REFUTED under the task's own definition also requires a sentence that literally decides, and none is quoted.
   Minimal fix: mark card 5 as CONFIRMED with at least these two rows, take them out of the UNKNOWN set (114 → 112), and update the confirmed-hole count.

5. **The Xen boot rows were upheld as NOT using one of the two card-5 readings.**
   Where: `RESULT.md`, seeded samples ("Upheld 21"); `review/resolved-sample.tsv` rows 13–15 (`flatcar-148193fc319dd99b4186c9e5`, `flatcar-2a8ca562df17fe66a53a012d`, `flatcar-86b4b62afd038f8594ff2eb3`).
   Evidence: these rows were upheld as NOT because "the observed machine uses QEMU/KVM". That is the fixed-environment reading, which the same review says in `review/card5-challenge.md` no sentence selects. Its last section admits the parallel ("would introduce the same unevidenced change of setup") but still upholds the rows.
   Minimal fix: treat these rows as hole candidates of the same unresolved reading, not as upheld.

6. **Card 8: two rows decided NOT conflict with the review's own reverse-dependency ground.**
   Where: `RESULT.md`, Card 8 line ("Guest-only images and ROMs themselves are explicitly exempt under S2.2-11/12"); `review/cards-5-8.md`, card 8 table (`fedora-21a722be1d318ec0f86e5189` ipxe-roms-qemu NOT; `fedora-d42127df5b3b98e4059e07bb` seavgabios-bin NOT).
   Evidence: in (not published: adjudication scratch), installed qemu-common requires `ipxe-roms-qemu`, and installed qemu-system-x86-core requires `seabios-bin` and `seavgabios-bin`. Both are installed (`in/raw/fedora/raw/004-packages-root-rpm.out`: qemu-common 11.1.2-1.fc45, qemu-system-x86-core 11.1.2-1.fc45). The review used the same kind of installed reverse requirement to decide MUST for gnulib-l10n, libwacom-data, rdma-core-common and libreoffice-uiconfig-common. Within its own framework, S2.2-11 gives NOT and S2.2-1 gives MUST for these two packages, and that is the collision card 8 describes.
   Minimal fix: report card 8 as CONFIRMED for these two rows, or drop the metadata ground everywhere (finding 2). Do not apply it to some rows and not others.

7. **The review read and relied on a folder its task does not name.**
   Where: `RESULT.md` and the review records it cites (`review/cards-1-4.md`, `review/cards-5-8.md`, `review/card5-challenge.md`, sample TSVs).
   Evidence: the review cites files under `(not published: adjudication scratch)`: (not published: external working record) 19 times, plus (not published: external working record), (not published: external working record), `c/dl/fl/…`, `c/dl/mint/Packages-upstream.gz` and `b_decide.py`. Its task names only `compare/STATS.md`, `adjudication/HOLES.md`, `adjudication/rows.tsv`, `compare/joined.tsv` and `D1/in/raw/`. (not published: outside selected checks and direct evidence): "Do not read the folders of other tasks unless your task names them." No reads of `D1/c1/` or `D1/c2/` were found.
   Minimal fix: cite the public repository sources directly (URLs, with fetched copies under `D1/review/raw/`), or record the read as a deviation in `RESULT.md`.

8. **The headline count depends on findings 2–6.**
   Where: `RESULT.md`, line 1 ("CHECK 1: 1 confirmed holes") and "Original-card dispositions: one CONFIRMED …, five REFUTED, two FACT-WRONG".
   Evidence: without the dependency-metadata reading and the S3-2 substitution, at least cards 3 and 5 stay confirmed, and card 8 for two rows. The count of 1 is not supported by a literal reading.
   Minimal fix: recount the confirmed cards after fixing findings 2–6. `OUTCOME: 0` does not change.

9. **Verified without defect: outcome, numbers and the other sampled claims.**
   - `OUTCOME: 0` follows from Section 4.2 and the Section 4.1 combination rule under either count. Talos is correctly given `?`, and it is correct that no machine is reported as having withstood the check.
   - Recount from `compare/joined.tsv` and `adjudication/rows.tsv`: 16524 objects, 15025 matching (90.93 %), κ = 0.55586, 1843 adjudicated. Per machine (objects / matching / κ / adjudicated / verdicts / agreed UNKNOWN):
     - Fedora: 5887 / 5444 / 0.54997 / 455 / 41 MUST, 75 NOT, 328 HOLE, 11 UNKNOWN / 0
     - Tumbleweed: 6779 / 6542 / 0.78126 / 490 / 34 MUST, 93 NOT, 363 HOLE, 0 UNKNOWN / 0
     - Mint: 2031 / 1816 / 0.44824 / 250 / 83 MUST, 19 NOT, 136 HOLE, 12 UNKNOWN / 1
     - Flatcar: 1827 / 1223 / 0.30104 / 648 / 137 MUST, 406 NOT, 97 HOLE, 8 UNKNOWN / 57

     All match `RESULT.md` and `compare/STATS.md`. The sample populations 888 and 14681, the disposition counts (21/9/7/3 and 57/3), the 114-row UNKNOWN file (13/1/32/68) and the ordinary-action counts 15/15/17 (`in/READY.md`) also match.
   - Sampled claims confirmed:
     - the emoji font's installed version (`in/raw/mint/raw/003-packages-root-dpkg-query.out` line 193);
     - the empty fields and scripts in its control record ((not published: downloaded distribution package metadata));
     - no reverse dependency or recommendation on it in the saved Mint metadata (`mint-meta-cinnamon` and `mint-meta-core` do not name it);
     - the seabios-bin firmware descriptors ((not published: adjudication scratch)) and the installed libvirt QEMU driver and qemu-kvm;
     - the Talos termination figures (`in/control/talos/host-read-observation.json`: rchar 139,946,649,722 bytes after 1112 s; 359 pagemap paths and 114,323 files);
     - the process-12 record merge (`in/raw/tumbleweed/raw/076-process.out` line 5: `12	1210	/usr/bin/startplasma-wayland`).
   - Quote check of `RESULT.md`: 11 quotes checked, 0 not found.
