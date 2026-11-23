# Correction of S2.5-1 coverage decisions

Date: 2026-11-22 UTC. This note supersedes the five affected dispositions in `../review/sample_audit.tsv`, not the frozen classifications or adjudication. No system probe was run.

## Literal coverage and the open scope question

- S3-1: “Whether an object must be recorded. The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.”
- S2.5-1: “How to treat data and program state, the remains of removed programs, user authority, generations and rollback, the transfer of accumulated state to another computer, when an edit of the declaration takes effect, and how to protect the declaration itself and secrets are questions of the design of a system built on the hypothesis, not conditions of declarativeness.”
- S3-2: “If what the object does remains unknown, the case yields ?.”

S2.5-1 alone is not a quoted NOT decision: it excludes design questions and never says state objects need not be recorded. That evidential correction applies consistently to all five sample rows and all cards. The proposed broader state-wide exemption is recorded as an author question in `QUESTIONS.md`, without choosing it or treating design questions as additional holes. Unknown functions yield ?; an established function with conflicting rules remains a hole.

## The five rows

| Sample / ID | Corrected disposition | Evidence and attempted refutation |
|---|---|---|
| resolved 9 / `852fec2bc63d3ac71655249a` | ? under S3-2 | `/run/systemd/journal/streams`: frozen c1 identifies stream metadata but explicitly lacks its fields; c2 asserts breakage generically. The 34 regular files in `raw/scope-inventory.tsv` do not establish the saved metadata values or the exact operations depending on these copies. A program-state label supplies neither a positive decision nor an exemption. |
| resolved 24 / `lived-tec6e90176f` | ? under S3-2 for the represented subtree | `/var/lib/containers/storage/overlay-containers`: the inventory includes runtime `config.json`, indexes, lock, secret directories and control endpoints. The frozen c1 and adjudication name these roles but give no contents or sufficient per-member effects. Neither separately inventoried container programs nor possible regeneration of configuration establishes a whole-row NOT decision; no new contradiction with an exemption is demonstrated. |
| resolved 29 / `4223394cc494d974882ce847` | ? under S3-2 | `/run/systemd/propagate/.os-release-stage`: the one staged regular file is present. The adjudication says the source remains and names propagation into services; it does not establish the actual consumer, contents or removal effect of this copy. A remaining source is not enough to prove the specific cache or content exemption. |
| resolved 40 / `e6c7b500df6175d8c883f1e4` | CONFIRMED, new card 9 | `/var/lib/systemd/deb-systemd-helper-enabled/multi-user.target.wants`: exact installed-version source identifies the markers as records of earlier enablement and checks their presence before service-link creation. See below. This is a known-function conflict, not S3-2. |
| agreed 7 / `e2107a3dd8d91a0eef56dac4` | Original MUST supported by cited S2.2-1/2 | The frozen c1 records device-node priority arbitration and the change in which device may own a shared symlink, citing `https://raw.githubusercontent.com/systemd/systemd/main/src/udev/udev-node.c`. This affects device naming. There is no cited Section 2.2 exemption; the former OUTSIDE judgment was solely the unsupported S2.5-1 inference. This restores support on the recorded function rather than claiming a new removal experiment. |

All five complete original row records are in (not published: outside selected checks and direct evidence); the four disputed adjudications are in `../adjudication/rows.tsv`. The new `sample_audit.tsv` supplies exact sentences for each corrected disposition. For the three unknowns, the uncertainty concerns instance-specific functions/removal effects; it is not a substitution of ? for the author question.

Documentation review for the unknowns: upstream journald source describes saved priority/forwarding fields and restoration (`https://raw.githubusercontent.com/systemd/systemd/main/src/journal/journald-stream.c`, `stdout_stream_load`); namespace source describes a staged os-release bind (`https://raw.githubusercontent.com/systemd/systemd/main/src/core/namespace.c`, `host_os_release_stage`). Neither supplies the missing contents/consumers of these inventoried instances. The installed systemd version is `257.13-1~deb13u1`, frozen package list line 1358; exact-tag retrieval attempts are recorded in `raw/documentation-status.txt`. No current upstream implementation is assumed to prove the installed instance's removal behaviour. No additional probe was needed to correct the unsupported NOT rationales.

Quoted source anchors from that documentation review: `stdout_stream_load` reads `"PRIORITY", &priority` and `"FORWARD_TO_SYSLOG", &forward_to_syslog`; the namespace mount entry says `/* Live copy, don't hard-fail if it goes missing */`. These describe generic mechanisms and do not fill the instance-specific gaps above.

## New card 9 — Past enablement records govern future service links

The helper records that an enable action occurred in the past. Its later link-creation logic reads the same markers, so the history exemption and behavioural-dependence requirement both apply.

- S2.2-6: “records of the past—logs, history;”
- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

Evidence: `A3R/in/raw/lived/raw/003-packages-root-dpkg-query.out:227` identifies `init-system-helpers 1.69~deb13u1`. The matching [Debian source](https://sources.debian.org/data/main/i/init-system-helpers/1.69~deb13u1/script/deb-systemd-helper) is preserved as numbered excerpts in `raw/helper-source.txt`. Source lines 354–360 translate the active-link path to a helper marker and skip the operation when the marker exists. Lines 362–375 create a link when allowed and then record the earlier enable action. This establishes a decision dependency for this exact marker family, independently of any specific future package-upgrade scenario. The actual markers are regular files in the frozen filesystem inventory; their existence is the tested input in the source branch, so marker file contents are not a missing premise.

Refutation attempts:

- REFUTED: S2.2-1 supplies MUST and S2.2-6 supplies the exemption. Neither states that the other ceases to apply to history consulted for later actions. Giving operative history priority over history, or vice versa, would add a rule.
- FACT-WRONG: the original claim that the **next upgrade necessarily re-enables disabled units** is not needed and is not endorsed. The narrower presence-dependent link-creation branch and historical purpose are explicit in the exact-version source. This correction does not erase the demonstrated collision.
- OUTSIDE: the question is the marker's recording obligation, not how an implementation preserves or regenerates it. S3-1 points to Section 2.2. S2.5-1 supplies no literal recording exemption; the proposed broader reading remains the separate author question.
- Content/cache/settings: a marker that changes a service-link decision is not merely missing content or a speed change; the effect is on service activation links outside the helper. The record of a past action has the explicit S2.2-6 exemption regardless of these other unsuccessful candidates.

Full-table extent: `recount.py` examines all 5,212 rows without filtering by classification or adjudication. It matches each row's represented members/subtree to the 56 regular-file markers under the inventoried helper-enabled directory (49 in `*.wants` directories and 7 root-level alias markers). This yields 19 marker-directory groups plus two represented parent groups (`/var/lib/systemd/deb-systemd-helper-enabled` and `/var/lib/systemd`), **21 rows**. `helper-search.tsv` lists all matches, including every kind/name match for `deb-systemd-helper`; `helper-witnesses.tsv` lists the raw witness paths. The 7 alias markers use the same source branch and are represented by the existing parent groups. Other inventoried helper-enabled regular files are `.dsh-also` aggregates already represented by those parent rows; they add no distinct row. No unexamined broad ancestor is counted just from its name.

This is an audit of a row already in the fixed 40-row sample, followed by the full-table extent search required by the original task. It adds no machine, sample draw or experiment.
