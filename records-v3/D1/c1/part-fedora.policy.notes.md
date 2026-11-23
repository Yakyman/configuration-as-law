# c1: system groups, authorization actions, and firewall objects

Scope: 847 rows in the six assigned kinds. Only the supplied part, its raw inventory, the fixed text, and primary documentation were consulted. No objects were removed. The classifier appends and flushes each completed row, preserving existing IDs.

## Deciding text

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-15: “accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;”

S3-1 supplies the evidence standard; S3-2 was considered, but the generic operative functions needed for these decisions are established. Neither an actual permission grant nor an actively used group membership is inferred merely from a name.

## Primary documentation

- https://man7.org/linux/man-pages/man5/group.5.html — “The /etc/group file is a text file that defines the groups on the system.” The entry fields identify a system group and its members.
- https://man7.org/linux/man-pages/man3/getgrnam.3.html — “getgrnam, getgrnam_r, getgrgid, getgrgid_r - get group file entry”. The documented lookup maps group names to records and reports absence when no matching record exists.
- https://man7.org/linux/man-pages/man1/chgrp.1.html — “Change the group of each FILE to GROUP.” Its named-group example establishes an operational use of this mapping. This is the upstream command manual reproduced in the manual collection.
- https://polkit.pages.freedesktop.org/polkit/pkaction.1.html — “pkaction is used to obtain information about registered polkit actions.” The raw command is exactly `pkaction`; without verbose output it lists registered identifiers, not successful authorization results.
- https://polkit.pages.freedesktop.org/polkit/polkit.8.html — “A mechanism needs to declare a set of actions in order to use polkit.” The manual describes cross-process authorization between requesting clients and privileged mechanisms, with action defaults and separate authorization rules.
- https://netfilter.org/projects/nftables/manpage.html — “Chains are containers for rules.” Also: “The chain must not contain any rules or be used as jump target.” The latter is the deletion precondition. Tables contain chains and other firewall objects; base chains connect rules to network hooks; helper objects supply named protocol-specific connection tracking.

The two requests to the upstream web version of the group-ownership command manual timed out; its reproduced upstream manual above was available. No experimental probe was needed.

## Homogeneous rule G: system group records — MUST

Apply S2.2-1 and S2.2-2 to the system group identity and name-to-identifier mapping. Removing an entry prevents selecting that identity by its group name for system ownership operations. This is not an assertion that removing a name removes the kernel's numeric group identifier or existing numeric permissions. Nor is it an inference that groups are accounts under S2.2-15. The content exemption does not apply: group selection and ownership operations change, beyond displaying the missing record. The record is used across system programs, not solely inside one program.

Source: `../in/raw/fedora/raw/002-groups.out`, produced by `getent group`. All 83 rows are individual group entries, not grouped directories. Ten rows checked by hand, including empty member lists and explicit supplementary members:

- fedora-bf3968c3ee4b6b46b56352b9 — identifier zero, empty supplementary list.
- fedora-81d3ebc1e32cdaadadd06ebf — identifier ten, one supplementary member.
- fedora-051419ac00bd6f4530b91c71 — identifier 36, one supplementary member.
- fedora-cdc6dd1af931be3d7c954426 — identifier 65534, empty supplementary list.
- fedora-9a53f3c878d66d483b4c3c14 — identifier 59, one supplementary member.
- fedora-f81a1c43861924b6db17a1b5 — identifier 114, empty supplementary list.
- fedora-da1cbce314ddc16627c4051b — identifier 32, empty supplementary list.
- fedora-5b3f6d68da37b1125492dbd8 — identifier 107, empty supplementary list.
- fedora-7f2950438c77270ef864f43a — identifier 42, empty supplementary list.
- fedora-989875f16bc5f7faddfd22ba — identifier 1000, empty supplementary list.

## Homogeneous rule P: registered authorization operations — MUST

Apply S2.2-1 and S2.2-2: action declaration is a prerequisite for mechanisms to perform authorization checks through polkit. The object here is the registered operation, not a human-readable description or an authorization granted to a particular user. These definitions mediate requests between processes, so S2.2-7's single-program setting exemption does not fit. The inventory does not establish the current defaults, and the classification does not invent them. Different operation names do not change the registration function relevant to this rule.

Source: `../in/raw/fedora/raw/087-polkit-actions.out`. Ten rows checked by hand against their identifiers:

- fedora-cb8d2c789a374112fc825a6c — parental-control account-information operation.
- fedora-74a693502cb6731e91793cb6 — directory mount operation.
- fedora-9ad8631bcbff806d7276bdf4 — application parental-control override operation.
- fedora-d826f7637004e4bc0e8d0eb1 — device enrollment operation.
- fedora-a2d1da167acc835765138467 — managed account update operation.
- fedora-500c90df04a2b06279496d3e — suspension with multiple sessions operation.
- fedora-40edc7f41ea98e563bfa54a3 — portable-image management operation.
- fedora-261374587fd389b936a73351 — disk health-information update operation.
- fedora-5dc5ad60a0a5245e5d175f7e — date/time configuration operation.
- fedora-4b9ea5ee69fc1e890eca03ec — low-level USB access operation.

These labels describe the identifier only; the MUST decision relies on documented action-registration semantics, not guessed implementation of the underlying operation.

## Homogeneous rule F: kernel firewall instructions — MUST

S2.2-15 explicitly requires firewall rules. Apply it to all 136 actual `rule` objects in the JSON ruleset, including jumps into empty chains. Their rule status is established by the raw schema, not by earlier inventory classification language. No assumption that each rule changes the final verdict of some currently observed packet is needed for this explicit sentence.

Source: `../in/raw/fedora/raw/080-firewall-nft.out`. Ten rows checked by hand:

- fedora-6041e2be782bf4485a8b070c — unconditional prerouting dispatch jump.
- fedora-95bd3160686c20c63d707bd6 — output-interface conditional jump.
- fedora-5fbb0b0d3a5c12dbb7d88205 — IPv6 destination rejection.
- fedora-fb4cee357f60168281580b05 — output-interface filtering dispatch.
- fedora-6f2076a680a8c3afadbdeac6 — acceptance verdict.
- fedora-395cef7f9d7998d5595b0a6b — jump to empty deny chain.
- fedora-2708de9da8345c5cc45c7865 — jump to empty NAT allow chain.
- fedora-c54c41773dd81473ea8d8e84 — jump to empty output NAT deny chain.
- fedora-7c92415ccc9b4b3f8d491b20 — jump to postrouting tail chain.
- fedora-f15d1f9101d6a5c11fe71a1c — jump to IPv6 policy pre-chain.

## Homogeneous rule C: prerequisites for existing firewall instructions — MUST

Apply S2.2-1 and S2.2-2 to chains that either connect existing rules to a network hook or provide a target used by existing jump/goto instructions. Every regular chain has incoming references in the supplied ruleset; every base chain has contained rules. The script verifies both facts from JSON. Removing a referenced target makes the corresponding existing instructions impossible. This reasoning does not equate an empty chain with an independent filtering rule, and does not claim it changes the final packet verdict. Removing other instructions as well would be a different removal counterfactual. A chain unused by any existing instruction is outside this rule and was not present.

Ten rows checked by hand, including empty targets:

- fedora-5f230e12f63dbb3f1c4fb369 — prerouting hook with a dispatch rule.
- fedora-f3aa6c9931855919cccaf245 — referenced dispatch chain with three rules.
- fedora-e6f248386082280bc6db2d52 — filtering prerouting hook with two rules.
- fedora-eba07334e63c2ed58ef85450 — input hook with six rules.
- fedora-a09e1d191830beff24acacbd — referenced input chain with six rules.
- fedora-7aeffc68321609723be3052a — empty input pre-chain, targeted by handle 166.
- fedora-879cbb5c45893deffca93378 — empty NAT pre-chain, targeted by handle 177.
- fedora-757c1020231e367eaf7e0173 — empty output deny chain, targeted by handle 214.
- fedora-26324e275f3515bbc13660cc — referenced IPv6 allow chain with eight rules.
- fedora-b60d46ad8f22cd89decf21b8 — empty mangling post-chain, targeted by handle 299.

## Individual decisions

- fedora-4e11dec134c34000bcde519b: MUST, S2.2-1 and S2.2-2. The table holds the supplied active chains, 136 instructions, and helper. Removing the container removes that operational firewall configuration.
- fedora-645f6cb16a52b5849f7bbe16: MUST, S2.2-1 and S2.2-2. The NetBIOS UDP helper is selected by rule handle 200 for UDP destination port 137. Removing this definition prevents that helper assignment. It is a protocol-processing object, not merely a historical connection record.

## Verification

`part-fedora.policy.py` checks all firewall member objects against the raw JSON, validates every regular-chain reference and base-chain population, writes append-only rows with immediate flushes, and verifies assigned IDs equal output IDs exactly once. It verifies the decision vocabulary and length bounds. Result: 847 MUST, zero NOT, HOLE, UNKNOWN, or MIXED.
