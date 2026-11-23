# Pair sweep: beyond the published plan

Candidate outcome: 0 (unresolved pairs found); individual 1 rows mean only that the attempted intersection produced no unresolved opposition, not that every possible object was eliminated. Question-mark rows are boundaries not promoted automatically to cards.

To avoid hiding a rule inside a consequence, the A set contains every operative sentence of Section 2.2: S2.2-1, S2.2-2, S2.2-4, S2.2-5, S2.2-6, S2.2-7, S2.2-9, S2.2-10, S2.2-11, S2.2-12, S2.2-13, S2.2-14, S2.2-15, S2.2-16. This deliberately includes exemptions and mixed sentences as rules, a superset of merely the two opening general rules. The B set is every exemption and explicit consequence: S2.2-4 through S2.2-7 and S2.2-9 through S2.2-16. S2.2-3 and S2.2-8 are headings establishing the exemption and consequence sets, not additional object decisions. Mixed sentences are evaluated clause by clause without inventing new sentence IDs. There are exactly 14 x 12 = 168 ordered rows, including reflexive pairs and both directions where both sets contain a sentence.

The named exemptions can already narrow S2.2-1/2. A general rule versus a named exemption alone is therefore not promoted as a collision. More demanding cases pit an exemption against an explicit positive consequence. After independent review, the cache/code pair survives; the named password-login and saved-network cases are decided by their explicit consequences. The separate external-handler case preserves the broader one-program setting boundary. Distinct outputs and inputs (a log and a firewall ban), distinct subjects (page and renderer), and different predicates (code classification and recording) are not silently identified.

Primary documentation for the concrete intersections:

- CPython bytecode cache: https://docs.python.org/3/tutorial/modules.html#compiled-python-files — “To speed up loading modules, Python caches the compiled version of each module”. Source availability makes regeneration possible; the same section says compiled files affect loading speed rather than execution speed.
- Python module execution: https://docs.python.org/3/reference/import.html#loaders — “Module loaders provide the critical function of loading: module execution.”
- OpenSSH settings: https://man.openbsd.org/sshd_config — PasswordAuthentication: “Specifies whether password authentication is allowed.” The manual describes keyword/argument configuration read by sshd.
- Fail2Ban log versus rule: https://github.com/fail2ban/fail2ban — “Fail2Ban scans log files like `/var/log/auth.log` and bans IP addresses conducting too many failed login attempts.”
- Browser process versus page: https://www.chromium.org/developers/design-documents/multi-process-architecture/ — The architectural overview documents separate renderer/browser processes. The object distinction itself prevents a confident opposite-decision claim.
- Saved boot history: https://www.gnu.org/software/grub/manual/grub/html_node/saved_005fentry.html — “The `saved_entry` variable sets the default boot entry in `grub.cfg` created by `grub-mkconfig`.”

No machine experiments, changes to system mechanisms, installation-channel feasibility claims, or proposed repairs are part of this sweep.

Additional guest-device intersection (S2.2-11/S2.2-16): https://libvirt.org/formatdomain.html#guest-firmware and https://www.qemu.org/docs/master/system/bootindex.html document configurable guest firmware and boot order. This is a device-scope boundary, not a claim that guest firmware is the physical host firmware.

TERMS.tsv records 90 deciding terms or tightly related term groups. A no entry is an audit flag, not by itself a card or a final 0: it must survive the primary-source and exclusion filters. Terms concerning declaration format, dynamic state, permission authority or implementation are not independently promoted where S2.5 excludes the question.

Final integration: the two direct cache/code pair rows retain outcome 0. Code-classification/cache pairs alone have no opposite recording decisions; their three-sentence overlap is merged into the same cache card. Guest firmware and the named authentication/network setting candidates were rejected by review. Initial candidate memos remain an audit trail.
