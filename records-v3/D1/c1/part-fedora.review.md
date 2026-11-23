# Review of the current Fedora c1 artifacts

Status: current tables pass this internal review. This is not acceptance of a check outcome.

## Corrected findings

1. The earlier Locale inconsistency is corrected. `fedora-762dfd196143c74a63b73bbc` is narrowly documented as calculator interface translations and remains `NOT`. `fedora-6a3fc7cac41c026ead69015c` is now `MUST`; its source chain establishes library locale definitions, and the notes document their effects on sorting, character handling, parsing, and formatting. RPM language packages were also revised from the actual payload evidence.

2. The earlier 414 blanket RPM `HOLE` decisions were reviewed against package payloads. The current correction map changes 426 rows: genuine dependency-only packages and content packages are `NOT`; packages containing code, account rules, operational links, or locale rules are `MUST`; and rows lacking occupancy, macro-content, deployment, or code-confinement facts are `UNKNOWN`. All 426 corrections match the RPM shard and merged output exactly.

3. The 25 missing-service `NOT` rationales now discuss the represented absent service: no definition or running service exists and therefore no service capability is in force. They no longer apply removal to an inventory line.

## Remaining HOLE and UNKNOWN review

The 80 RPM `HOLE` rows reduce to 40 root/user pairs. Their reasons state the competing fixed-text readings: operational reference-table content versus lost behavior, or a setting read by one program versus a setting whose effects extend beyond it. The 44 RPM `UNKNOWN` rows reduce to 22 root/user pairs and identify concrete missing facts: directory occupancy and dependence, macro contents, firmware deployment context, or stylesheet/script execution and confinement. No remaining row clearly substitutes an unknown factual function with `HOLE`.

## Checks that passed

- The completed main, unit, and policy sets have the required six-column schema, no blank fields, unique IDs, permitted decision vocabulary, and exact ID coverage for their assigned kinds. The merged table is their 1,933-row union.
- The completed RPM shard has 3,954 unique IDs and exactly matches those rows in the merged output. Its correction map and correction audit each contain the same 426 unique IDs.
- RPM notes record 13 homogeneous rules and exactly ten distinct sample IDs for each rule: 130 distinct IDs total. Every sample exists in the RPM output, has the decision stated by its rule, and has the stated `what_it_does` text. All 129 represented package names are present in the saved documentation extraction; one package appears in both inventory contexts.
- Ten-row manual checks are recorded for every completed homogeneous main and unit rule. The policy notes record ten checks for each bulk group, polkit-action, firewall-rule, and firewall-chain rule. The individually handled main categories contain fewer than ten rows each and are explicitly reported as individually examined.
- The process rationales correctly refuse to attach the final executable on a malformed physical line to its first PID. Driver rationales classify the evidenced binding/driver function rather than the symlink text. Group rationales classify the group identity and mapping, and polkit rationales classify registered actions rather than authorization grants.
