# Adapter assumptions before the source-built interface

2026-11-26 UTC. No build/INTERFACE.md existed when these were written.
The reference is confos/INTERFACE.md, revision 55, operation table and
Disk paragraphs, plus confos-check/adapter.py. None of the following
is a claim about the new system. Only adapter.py may translate these operations.

| ID | Assumption / reference | Before running on a release |
|---|---|---|
| A01 | Stand clean build: ./build.sh DECLARATION OUTPUT.qcow2 | Replace with source-only clean build command; record source and recipe hashes, no builder working tree or preconfigured disk as the clean build. |
| A02 | Stand boot: ./boot.sh DISK SSH_PORT MEMORY_MIB SERIAL_LOG QMP_SOCKET | Replace boot/transport; COMMON's FOUR slots, confos.slice, 8 GiB/4 vCPU per test machine override the stand's six locks. Never invoke the old boot helper without enforcing this. |
| A03 | Stand user SSH and sudo -n for root commands | Resolve transport, account and escalation from new interface. All guest commands run only through adapter transport; never on host as fallback. |
| A04 | Candidate /state/declaration.conf; success confos status = APPLIED SHA256; confos apply may reboot | Match exact native candidate and committed identities, independently read committed text. Candidate edits do not advance in-force state. |
| A05 | Stand GPT EFI/system/data, squashfs root, writable /state | Resolve all filesystems, live mounts and namespace views. External disk reader must inventory all stored roots, including inactive generations (classified, not ignored). Never trust a package ledger as inventory. |
| A06 | Stand package, account, service, setting, rule, file lines | Semantic JSON in declarations is the case party's input language, not invented native syntax. Renderer fails on unknown kinds; no silent line omission. |
| A07 | No opening line in stand | open-folder is a semantic line pending builder grammar. All three OPEN cases and boundary/removal cases stay blocked at rendering until documented. |
| A08 | confpkg format and dependency metadata unknown | Package read API needs validated archive hash, member content/links/modes/owners and dependencies. fixtures use a tiny tar format explicitly limited to fixtures; never identify it with confpkg. |
| A09 | Base source/recipe lock and three update states unknown | D-base/updates are binding slots, not fabricated versions. Freeze concrete release bindings and native declarations before first complete run. A changed greeting alone is not a system update. |
| A10 | Kernel/live queries needed for accounts, services, mounts, network, saved networks, modules, sysctls, locale, rights, ports, processes, radio | Capture actual query bytes and status, parse independently. Missing/failed query is an error; empty list is not a substitute. Resolve executable identity through process root and hash (review R9). |
| A11 | Actual shell, fetcher, compiler, loader and file readers unknown | Tokens @SH@, @FETCH@, @CC@, @LOADER@ and @HOME@ bind once in local.env/release bindings. Expand only whitelisted quoted values; command-fragment tokens require documented argv templates. Enumerate all shipped interpreters, startup consumers and direct executable paths. |
| A12 | No provision for multi-file law, omitted account IDs, latest source selector or account server in stand | Preserve W1d/W3d/Q9 scenarios. Unsupported format gives unobserved with exact attempted rendering, not a pass. Source-pinned base policy is not overridden to invent a latest selector. |
| A13 | Container runtime and in-guest VM absent | G-CONTAINER/Q6-GUEST require actual respective facilities. The outer test VM is not an in-system guest. No host process is used as a substitute. |
| A14 | Radio simulation and physical hardware not yet defined | X-WIFI/X-BT and OW-10/11 separate. Observe stored profile/pairing AND effective connection, reproduction and removal. Real endpoints/credentials stay unpublished. |
| A15 | Interruptible install and crash timing | Cut network only after captured transfer progress, cut power immediately after actual success identity. Evidence includes ordering, monotonic timestamps, old/new boot IDs. Failure before success preserves old law. |
| A16 | Test services, firewall, rights and scheduler controls depend on base | Semantic mutations bind to real tools. Missing tool cannot be counted as a policy refusal. Keep all user/root, transient/persistent/delayed variants. |
| A17 | Independent derivation may be incomplete for compiled outputs/default generated values | Derive only from declaration and named packages/source/recipes; emit underived objects instead of using a reference machine. Strict Table 9 outcome remains separate (QUESTIONS Q-DERIVE). |

The portable scenario engine, comparison, derivation, fixture capture and report
logic are executable now. Native rendering, package parsing, disk/transport and
lifecycle bindings are deliberately fail-closed until documented. These are
adapter work in part 2, not evidence that an operating-system case passed.

P2's prerequisite targets are fixed in plans.json: additions case-extra-a,
case-extra-b and case-extra-service; changes hostname, firewall port and account
shell; removals case-small, test firewall and test user timer. Native binding must
establish each opposite precondition first, and capture it. ADD payloads use the
same greeting source under separate package names; no new runtime is implied.
The payload recipe supports curl- and wget-shaped base fetchers and a bound shell
path. These recipe parameters are part of the frozen source/recipe identity.

A18. Every marker-based route gets a unique guest-only CASE_MARKER, passed to the
actual consumer's environment. The positive control uses the same payload and
invocation form in its recorded/allowed location and must create the marker; it
then removes that marker before the negative attempt. A script that merely fails
because CASE_MARKER is unset cannot establish refusal. OPEN-OUT carries its own
positive control inside the opening. Controls and marker cleanup are raw evidence.
A19. Q8's listener fixture lasts 30 seconds. Capture its socket owner and executable
while it is alive; the adapter must retain that coherent observation for the
checkpoint. If capture misses the lifetime, report unobserved, never infer it.

## Resolution against release 0.60 (2026-11-26 UTC)

The builder's interface of 0.60 now exists. Each assumption is resolved as follows;
BINDING.md gives the commands. Not resolved = the row stays unobserved in a run.

| ID | 0.60 |
|---|---|
| A01 | Resolved: `confos-assemble` in the clean bootstrap root (INTERFACE 1, PROCEDURE 6), from a package store the case party builds from the release source by PROCEDURE 1–5. |
| A02 | Resolved: QEMU as `scripts/boot.sh` plus a QMP socket; slot lock 1–4; ≤8 GiB/4 vCPU. |
| A03 | Resolved: SSH as `user` / as root by `authorized-key` lines (INTERFACE 3, 4); no sudo rule for `user`. |
| A04 | Resolved: candidate `/data/confos/declaration.conf` with inputs beside it; success = `confos status` `APPLIED <identity>` after the restart; committed = generation named by `boot.cfg`, read externally. |
| A05 | Resolved: GPT of INTERFACE 7; `adapter_disk.read_disk` reads both ext4 partitions (journal replayed on a copy) and every `root.sqfs`; retained generations and the store are classified with QUESTIONS 9. |
| A06 | Resolved: native lines of INTERFACE 5; `bindings/release-0.60.json`; unknown semantic kinds fail closed. |
| A07 | Resolved: `open PATH` (INTERFACE 5, rule 1). |
| A08 | Resolved: FORMAT.md; `adapter_disk.read_confpkg` checks every member against the passport itself. |
| A09 | Partly: base lock = the release's `base.conf`; update states T0–T2 do not exist in 0.60 (INTERFACE 9): OW-2/OW-3 unobserved. |
| A10 | Resolved: live capture script (BINDING 3); a failed query is an error, never an empty list. |
| A11 | Resolved: `bindings/commands-0.60.json` (tokens, preludes, per-variant commands); unknown tokens fail closed. |
| A12 | Resolved as absent: multi-file is supported (`include`); `auto` IDs supported; latest selector and account server absent (unobserved). |
| A13 | Resolved as absent: no container runtime or hypervisor in the base. |
| A14 | Resolved as absent in the virtual machine (no radio stack); the laptop cases remain for later. |
| A15 | Partly: power cut by SIGKILL after the observed `APPLIED` status; network loss cannot interrupt an installation because `confos apply` transfers nothing (OW-9, P2-NET-1 unobserved). |
| A16 | Resolved per variant; facilities without a tool are unsupported, never refusals. |
| A17 | Resolved: derivation from lines, named package stores and sources of the named base packages (BINDING 4); rendered bytes are presence-only. |
| A18 | Resolved: `/home/user/control` and `/root/control` are opened by the test account binding; same payload and command there, with the role of the attempt. |
| A19 | Resolved: the listener's owner and executable are read while it lives and retained. |

## Release 0.65 (2026-11-26 UTC)

Release 0.65 was named for run 1. Against 0.60 its interface changes: `confos rules` shows the
packet filter in force; `reboot` and `poweroff` work from a superuser session and the power
button powers off; IPv6 is off on every interface without an IPv6 `network` line; a second
package that installs a file of another is refused. The resolutions above hold for 0.65 with
the binding files `bindings/release-0.65.json` and `bindings/commands-0.65.json`; A09, A12–A15
are unchanged (INTERFACE 5 and 9 of 0.65 name the same absent facilities).

## Releases 0.66 and 0.67 (2026-11-27 UTC)

Release 0.66 updates the system through the declaration (INTERFACE 9): a `base RELEASE FOLDER
SHA256` line names a tree the person brings; its update states 0.66.1 and 0.66.2 bind OW-2 and
OW-3, which were unobserved before (Q-UPDATE). Release 0.67, named for run 1, keeps on the
system partition only what the lines of the declaration in force bring, removed when the new
generation has finished starting and before `confos status` prints `APPLIED` (INTERFACE 7);
its update states are 0.67.1 and 0.67.2. The resolutions above hold with the binding files
`bindings/release-0.67.json` and `bindings/commands-0.67.json`; A09, A12–A15 are unchanged.

## Release 0.68 (run 2) (2026-11-27 UTC)

Release 0.68, named for run 2, differs from 0.67 only by the readline init-file guard and
the version bumps of `base-files`, `confos` and `os-release` (`confpkg` and `confos-boot`
stay 0.67). All resolutions above hold unchanged with the binding files
`bindings/release-0.68.json` and `bindings/commands-0.68.json`; its update states are the
builder's tags `0.68.1` and `0.68.2`. No assumption is re-opened by the release.
