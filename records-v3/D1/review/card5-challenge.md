# Independent challenge of card 5: absent hardware

Final disposition: REFUTED as an established inventory counterexample, by the insufficient-information indicator S3-2. No actual row has a proved card-5 extent from the saved evidence. The hardware-scope reading remains a semantic concern; this report does not claim S2.2-1 unambiguously settles it. The attempted textual challenge and subsequent whole-table factual check are distinguished below.

## Strongest attempted refutation

S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

One can argue that the computer already has the capability to handle a compatible device when connected. Removing its firmware or udev data takes that capability away, even though no device currently triggers it. On that reading S2.2-1 and the removal test decide MUST; the rule contains no word restricting behavior to this instant. The card is therefore wrong if its only complaint is that the effect happens later.

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

The difficulty is not elapsed time. To obtain the claimed behavior, the test adds a previously absent hardware dependency. With the machine's inventoried hardware held fixed, neither before nor after removal can it operate that device. With later hardware additions admitted, the supported behavior is available before removal and unavailable afterwards. Neither sentence says whether that hardware change belongs inside the capability comparison. Calling one of these scopes the literal meaning would supply the disputed boundary rather than quote it.

This differs from dependency metadata controlling a later package-manager run: that manager and its ability to evaluate the metadata already exist on the inventoried machine. Merely waiting or invoking the installed manager does not add a missing physical precondition. The lack of an immediate effect alone is therefore insufficient to sustain card 3, while the hardware precondition remains a separate issue for card 5.

## Firmware-specific attempted refutation

S2.2-16: “the boot order and device firmware must be recorded where the system is able to change them.”

For an absent modem or tablet, the machine cannot presently set firmware on that device; after attachment it might. Thus the qualifier in S2.2-16 has the same unresolved domain, rather than unconditionally classifying every stored firmware image. The sentence also does not explicitly equate an inert firmware file with firmware set on a device. S2.1-3 describes firmware in force as set on the device, but concerns in-force status of objects already determined to require recording; it cannot independently settle the recording scope.

## Other disposal attempts

The issue is whether an installed hardware-support object must be recorded, not how to protect secrets, treat accumulated program state, transfer state, or implement rollback. S2.5-1 therefore does not put this classification question outside the definition. S2.4-3 excludes hardware-explained differences from reproducibility; it supplies no hardware scope for the removal test in check 1.

S2.2-9 and S2.2-10 can independently decide packages containing host-executed programs or scripts. Such rows must not enter this hole solely because they also contain unused hardware support. Likewise, a table that has an established present consumer is decided from that function rather than from absent devices. This challenge does not establish the extent of a confirmed card.

## Factual limit

`../adjudication/rows.tsv` card-5 notes and the driver/module inventories (`../in/raw/fedora/raw/078-driver.out`, `077-module.out`, and corresponding Tumbleweed files) support absence of listed devices, not the assertion that each could actually be attached to these particular disposable machines. Some notes explicitly say that no USB controller is present. A hypothetical VM reconfiguration is a hardware change; it is not evidence of an already available hot-plug path. The saved file lists ((not published: adjudication scratch), (not published: adjudication scratch)) support package content, but do not settle that attachment premise.

Accordingly, the semantic counterexample has two explicit readings, and no quoted sentence selects one. The original blanket row count must still be challenged independently. If a row has unknown package content, consumer, or relevant hardware behavior, S3-2 makes that row UNKNOWN; lack of facts cannot itself confirm the hole.


## Whole-table extent follow-up

`card5-extent.tsv` searches all 16524 joined rows, selecting names matching `firmware|microcode|wireless-regdb|usb_modeswitch|libwacom|media-player-info|alsa-(?:ucm|topology)|b43-openfwwf|hwdata|grub|xen|udev` plus every L1 driver/module kind. It records 1314 candidates: 1233 excluded from this particular card, 81 with unknown membership, and **0 proven included**. Excluded is a card-membership finding, not a replacement classification for every broad name match. All 58 original card rows were found; the additional matches include agreed firmware/support packages and Flatcar Xen boot code.

Counts by machine/status: {('fedora', 'EXCLUDED'): 192, ('fedora', 'UNKNOWN'): 54, ('flatcar', 'EXCLUDED'): 750, ('mint', 'UNKNOWN'): 9, ('mint', 'EXCLUDED'): 17, ('tumbleweed', 'EXCLUDED'): 216, ('tumbleweed', 'UNKNOWN'): 76}.

The saved driver lists describe current bound drivers, not every device a VM operator could configure or pass through. Many additional agreed firmware package payloads have no saved file list in the adjudication caches, so their names cannot establish a hardware-only payload either. It is therefore not defensible to claim any actual inventory row as CONFIRMED for card 5 from these records. The previous semantic challenge survives as a question, but does not supply the missing factual counterexample. This is insufficient evidence for confirmation, not a proof that the wording explicitly chooses the current-hardware reading.

For consistency with the sample: the Flatcar Xen module NOT findings concern the observed KVM boot environment, where those platform modules are not executed. Asserting that moving the installation to a different hypervisor must be included in the removal test would introduce the same unevidenced change of setup. No Xen path is counted as a confirmed card-5 case.

The UNKNOWN membership labels in this extent file must not automatically be added to the classification's UNKNOWN totals: they mean insufficient evidence to include a row in this proposed hole, not that the whole row has no independent deciding function.

S3-2: “If what the object does remains unknown, the case yields ?.”

All seven original example ids and all 58 original card-5 rows appear in the extent table. Further metadata review excludes 48 of the 52 Fedora original rows: (not published: adjudication scratch) records exact-version requirements that the installed package manager evaluates. This independently establishes behavior under S2.2-1 without relying on absent hardware. For example, qcom-wwan-firmware requires linux-firmware-whence; b43-openfwwf requires module-init-tools and udev; usb_modeswitch-data requires /bin/sh, systemd and usb_modeswitch; alsa-ucm requires alsa-lib. The package is the inventoried object, so its operative dependency metadata cannot be omitted from its function.

A final reverse-dependency audit excludes six more originals: installed Fedora libwacom 2.19.0-2.fc45 requires libwacom-data; installed Tumbleweed libwacom9 2.20.0-1.1 requires libwacom-data; installed patterns-base-enhanced_base 20241218-37.1 recommends wireless-regdb. These exact installed versions are in each raw004 package inventory; dependencies are in (not published: adjudication scratch) and (not published: downloaded distribution package metadata). These relationships give package-manager behavior even when a data package has no requirements of its own.

Final original-card extent: **56 excluded by operative package metadata; 2 residual uncertain rows; 0 confirmed.** The two residuals are Fedora root and user alsa-sof-firmware (`fedora-eaecd855d3b238f815d51e72`, `fedora-369a1218fca1b15b045403ef`). These have no independently established dependency function in this review, and the absent-device behavior remains insufficiently established. The whole-search count of 81 uncertain membership matches does not create 81 UNKNOWN classifications; only these two residual original-card rows enter the root result as additional object uncertainty with explicit provenance.


Membership uncertainty does not replace object decisions with UNKNOWN or add Xen search matches to object-uncertainty totals.
