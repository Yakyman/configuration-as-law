# Card 6: regeneration and the removal test

Recorded 2026-11-22 UTC. Bounded contribution to FX-D1-H-2, finding 1; not independent acceptance. Only this memo and `card6-extent.tsv` were written. No probe, new case, frozen-input modification, or new interpretation rule was introduced. The named common rules, task, text, sentence index, review finding, original card, permitted joined/adjudication tables, and prior card audits were read; no classification folders or adjudication work folders were read.

## Disposition: CONFIRMED

The original examples are operational inputs recreated from another source; removal can therefore cease to have an effect when regeneration occurs. S2.2-1 does not independently settle whether the removal test in S2.2-2 includes, excludes, or waits for that regeneration, and the text gives no such scope rule. This is a missing determination of the removal test, not a claim that every generated object is exempt or that S2.2-2 explicitly concludes NOT after a negative result.

S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

S2.2-5: “cache: after it is removed, the computer does the same, only more slowly;”

S2.5-1: “How to treat data and program state, the remains of removed programs, user authority, generations and rollback, the transfer of accumulated state to another computer, when an edit of the declaration takes effect, and how to protect the declaration itself and secrets are questions of the design of a system built on the hypothesis, not conditions of declarativeness.”

S2.5-3: “Nor is the form of the declaration part of the definition: it may be a list or an algorithm that computes what is recorded.”

S3-2: “If what the object does remains unknown, the case yields ?.”

**REFUTED attempted:** the prior argument in `../review/cards-5-8.md` decides MUST from operational dependency alone. That is the same independent, wider S2.2-1 reading that `../fix-d1-h-1/card-audit.md` leaves undecided for card 3. Reading S2.2-2 as the operative test instead leaves its observation and regeneration scope unstated. Neither reading is selected here. S2.2-5 does not rescue the refutation: regeneration alone does not establish its same-behavior-only-slower condition, nor does lack of an established cache exemption choose the meaning of the designated test.

**FACT-WRONG attempted:** `../adjudication/rows.tsv` explicitly records the source/regeneration mechanism for all 20 original rows; the original card and joined member lists agree with their described roles. The prior refutation itself accepts the operational-dependency premise. No contradiction of those facts was found in the permitted record. This retains saved evidence rather than claiming new observation of regeneration or inspection of unlisted sources cited by old notes.

**OUTSIDE attempted:** S2.5-3 concerns how the declaration represents an already-required object. It does not decide whether the generated output is required. S2.5-1 concerns treatment of state and timing of an edit to the declaration; this card asks which runtime operational inputs Section 2.2 requires in the first place. The audit does not promote a system-design preference into a definition defect.

## Extent and search limits

At least 20 rows are retained: 13 Flatcar and 7 Tumbleweed. These include containing directories, counted as original inventory rows rather than as independent physical files; their other members need not share the hole. The accompanying TSV gives every original id/name, the saved role, and evidence pointer. No other membership is newly established.

The entire 16,524-row joined table was scanned, independent of agreement or adjudication status. The name search was case-insensitive `generator|autostart|tmpfiles|resolve|resolv\.conf|static.nodes|libcontainerd|dbus-:`; all original ids were included. A kind/name expansion included L2 `/etc` and `/run/credentials`, `/run/systemd/network`, `/run/systemd/transient`, `/run/systemd/netif` and descendants. Unit-file member states were inspected to distinguish generated/transient output candidates from ordinary producer units. This yielded 161 rows: 20 CONFIRMED, 21 UNRESOLVED_MEMBERSHIP, 120 EXCLUDED. Exclusion concerns membership in this searched candidate population only, not a new MUST/NOT verdict.

The unresolved memberships are Fedora 5, Tumbleweed 7, Flatcar 9. They include five Fedora generated autostart files, seven Tumbleweed service records related to generated/transient unit files, and nine Flatcar stored-object directories. Their names or inventory states establish candidacy, not all facts needed to extend the original saved regeneration argument. They are not mechanically added to object UNKNOWN counts. The 120 exclusions are Fedora 50, Tumbleweed 22, Mint 4 and Flatcar 44; these matches identify producers, consumers, accounts, groups, actions or ordinary units rather than proven regenerated outputs.

This is a documented lower bound and candidate search, not a claim that the exact global extent has been resolved. Other generated inputs may have names outside this search. Finding 4's extent caveat applies to card 6 as well: present 20 as “at least 20,” with 21 unresolved memberships in this search. No new experiment or invented rule was used to close those memberships.

## Original rows retained

| id | machine | kind | name |
|---|---|---|---|
| flatcar-8d354bdc3e8042522678923e | flatcar | L2:stored-outside-packages | /run |
| flatcar-cc7f234ea5320af7c211fb4a | flatcar | L2:stored-outside-packages | /run/docker |
| flatcar-8b99c9cebbd266ab613719ae | flatcar | L2:stored-outside-packages | /run/docker/libcontainerd |
| flatcar-7db1d507b1da0e5b91f46577 | flatcar | L2:stored-outside-packages | /run/systemd |
| flatcar-1e2367e8ee760295626cad00 | flatcar | L2:stored-outside-packages | /run/systemd/generator |
| flatcar-6abd3cc93dfc5b3e66f60427 | flatcar | L2:stored-outside-packages | /run/systemd/generator.late |
| flatcar-6dfbbd5dda8448a06762532d | flatcar | L2:stored-outside-packages | /run/systemd/generator.late/local-fs.target.wants |
| flatcar-ce3302c1526d5bbbdb4b45c4 | flatcar | L2:stored-outside-packages | /run/systemd/generator/emergency.service.d |
| flatcar-d852e5f1577825ced7b1c5da | flatcar | L2:stored-outside-packages | /run/systemd/generator/getty@.service.d |
| flatcar-769ce88f8a54e2150b5cbec9 | flatcar | L2:stored-outside-packages | /run/systemd/generator/serial-getty@.service.d |
| flatcar-e8c3dd1b118f12e4905f5300 | flatcar | L2:stored-outside-packages | /run/systemd/generator/sockets.target.wants |
| flatcar-b9083577b011da27bfb86f15 | flatcar | L2:stored-outside-packages | /run/systemd/resolve |
| flatcar-778d999ce314fbfc50ce240f | flatcar | L2:stored-outside-packages | /run/tmpfiles.d |
| tumbleweed-106b78a49881386e5c2089f8 | tumbleweed | L1:user-unit-file | user:app-org.kde.discover.notifier@autostart.service |
| tumbleweed-f74dc5f7e54391f7f0fe3191 | tumbleweed | L1:user-unit-file | user:app-org.kde.kalendarac@autostart.service |
| tumbleweed-4814ee7bd81e6d76e9a9c2a8 | tumbleweed | L1:user-unit-file | user:app-org.kde.plasma\\x2dfallback\\x2dsession\\x2drestore@autostart.service |
| tumbleweed-0a3bbfcbc0c2cab24bdae201 | tumbleweed | L1:user-unit-file | user:app-org.kde.xwaylandvideobridge@autostart.service |
| tumbleweed-96dc4334164d3db33dd2d4e5 | tumbleweed | L1:user-unit-file | user:app-org.opensuse.opensuse_welcome_launcher@autostart.service |
| tumbleweed-caed67c1406e063dcd99a95f | tumbleweed | L1:user-unit-file | user:dbus-:1.2-org.freedesktop.impl.portal.desktop.kwallet@0.service |
| tumbleweed-8da304e41e03ff1169c907c2 | tumbleweed | L1:user-unit-file | user:dbus-:1.56-org.a11y.atspi.Registry@0.service |

## Bounded sample and overlap follow-up

The 40 resolved and 60 agreed rows in `../fix-d1-h-1/resolved-sample.tsv` and `agreed-sample.tsv` were scanned by kind/name/reason, with the relevant original reasons in `../review/resolved-sample.tsv` and `agreed-sample.tsv` inspected. None of the original 20 card-6 ids occurs in either sample or in `../fix-d1-h-1/confirmed-rows.tsv`; there is no overlap with the prior established card sets.

No sample disposition change is established by this card-6 correction. Resolved sample positions 1, 8, 9, 26, 37 and 39 concern udev claim bookkeeping, and position 2 is private temporary service state. Their retained OUTSIDE classification concerns treatment of program state under S2.5-1; it is not a blanket NOT verdict for every runtime path. This differs from the original card-6 records, which identify generated launch/mount/autologin configuration, resolver configuration, static-node configuration and the recreated containerd connection link. Regeneration alone proves neither program-state exclusion nor the cache condition.

Agreed position 29 (`flatcar-9bf281bd2d8812ec0c3e8b1a`, `/run/docker/libnetwork`) is a live IPC socket; its saved reason is the loss of connections at that pathname after removal. No saved evidence in this bounded review establishes the card-6 premise of regeneration from another source object for this socket. Consequently it is not newly promoted into the hole by analogy with `/run/docker/libcontainerd`. Agreed position 42 (`flatcar-113362e7a33674cb82c3b70f`) contains only an empty package placeholder, not network configuration. The other sampled unit-file rows have ordinary unit states and no established regenerated-output premise. This follow-up preserves sample orders, seeds and all files.
