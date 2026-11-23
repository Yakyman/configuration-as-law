# FX-B1-2 evidence audit

Recorded 2026-11-22 UTC. Role: operator. Documentation and report analysis only; no VM, probe or testbed.

## E2-1: conditional Landlock control versus mandatory launch coverage

Primary source revisited: [Linux 6.12 Landlock documentation](https://docs.kernel.org/6.12/userspace-api/landlock.html), “Defining and enforcing a security policy” and “Inheritance”. Exact excerpt: “The current thread is now ready to sandbox itself with the ruleset.” The example calls `landlock_restrict_self(ruleset_fd, 0)`; descendants inherit the resulting domain. This documents self-restriction/inheritance, not a system component placing every interpreter launch there. Existing source ledger: `../raw/c7-sources.md` E12. Existing descriptor limitation: `../fix-b1-1/control-audit.md`, D section.

Inference: the proposed restriction can deny a new file open after domain entry, but that does not establish coverage of every launch. A shell outside the domain can start an interpreter outside it; inheriting the restriction throughout a session also denies unrecorded document-file reads to descendant editors. D does not mediate instruction bytes supplied through argv/environment, inherited stdin/descriptors or arbitrary socket/IPC input. These are limits of the claimed file-open control, not a statement that no mandatory integration could ever exist.

The finding is accepted for C2.6, C4.4, C7.01/07/08/09/24 and C8.01/02. C7.23 also cited D for foreign-binary file reads and receives the same correction. All are UNKNOWN. C7.02/12 retain N as the primitive for direct execve of the script/hook; interpreter-argument execution is separately C7.01. Their overall verdict still becomes UNKNOWN under full R below. C7.05 adds E12 explicitly; the already inherited descriptor remains a different route.

## E2-2: one verdict for the whole stated requirement

Evidence: `before/B1/CHANNELS.md`, R paragraph and C7.25; `../fix-b1-1/evidence-addendum.md`, final runtime-network paragraph; (not published: orchestration and working notes), Method item 4. The prior report included P2, Removal and S2.2-15 in every C row while treating a native/file control as sufficient for CLOSABLE. That was inconsistent.

This revision chooses the review's second remedy: retain R exactly and let the verdict follow it. Every previously CLOSABLE C row becomes UNKNOWN because complete application/recovery obligations are unestablished (M1.02/M2.02/M3.02); runtime ports additionally retain C7.25's UNKNOWN wherever applicable. The same standard applies even to a route whose particular content is exempt, such as C8.08: its values-only classification is settled, but the row explicitly inherited full R. This does not turn exempt values into required objects, assert that every program listens on a port, or alter a failure condition.

The remaining eight CLOSABLE rows are M1.01, M2.01, M3.01, M4.01–04 and M5.01. Each retains its individually bounded stated requirement and existing evidence; none has R in its requirement cell. Their full composition is unestablished. No additional empirical question follows from this bookkeeping correction.

## E2-3: custom-dispatch input routes and Q1

Evidence: `before/B1/CHANNELS.md`, Q1's explicit own-rights-code premise and D limitations; `../fix-b1-1/text-audit.md`, finding 5; `../../SENTENCES.md` S2.2-10/13, S2.3-4/6. The conditional argument never required the interpreter itself to open the file. Conventional eval/import checks need not observe a dispatcher implemented by admitted code.

C7.24 stays one variant with two explicitly distinguished routes: a new file open, and instruction input through stdin, argv/environment, inherited descriptors or socket/IPC. Both are UNKNOWN. A reader outside D sending the command file's bytes through `cat F | M`, or M consuming a socket instruction stream, preserves the stipulated own-rights-code premise. These are logical counterroutes to the proposed control, not newly observed failures. If the input is merely values, the premise does not hold; no new code/value rule is introduced.

Q1 now makes mandatory domain entry conditional and keeps non-file ingress unresolved even after entry. Q3 distinguishes lost direct file-read workflows from still-possible receipt of arbitrary bytes through other inputs. No safe general programming or dependency workflow is inferred from D alone. Q3 editing and C8.01/02 explicitly state the wider document-read loss under whole-session inheritance.

## Rerun decision

The task is a correction of conclusions and their evidence links. The cited documentation and frozen report establish the relevant gaps. No new probe is eligible: another primitive test cannot establish an unbuilt mandatory launcher, declaration broker or complete lifecycle. P01 and all previous raw evidence remain frozen. Only the changed table parsing, counts, design list, link/quote checks and preservation checks are regenerated in this directory. This is not a repeated Check 2 case.
