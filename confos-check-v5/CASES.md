# Cases for the source-built terminal system

2026-11-26 UTC. Specification: paper 6 §5 (version 5) and §7, paper 5 §9
Table 9, and the stand review R1–R10 where §5 does not supersede them.
PROGRAMS.md chooses the minimum programs; PORT.md preserves every old case ID.
There has been no operating-system run. These are portable case definitions.

## Execution and evidence

`python3 -B run --list`, `run --validate`, and `run --case ID --plan` inspect
these definitions. `casedefs.py` is authoritative; `plans.json` contains its
fully expanded primitive steps and assertions. Release-specific operations are
translated only by adapter.py and must be bound before a real run. Unknown
capabilities and missing evidence are unobserved, never refusals or passes.
Every variant listed below is a separate execution from a clean installation,
with its own commands, probes and inventories. A generic variant name is an
adapter binding requirement; it is not evidence of an executed command.

Each installation starts from the same designated D-test and the named release,
with recorded positive controls. Before a negative probe, its marker/effect is
absent and its actual consumer exists. The attempt's exit code does not decide
refusal: independent probes and the whole inventory decide. An absent executable,
unsupported syntax or failed setup cannot establish refusal. Positive ordinary
work must actually succeed. All effects use disposable guest state.

At each checkpoint, externally read the committed declaration and independently
inventory stored and effective objects. P1 checks for unrecorded installed things
or settings, P2 for missing/different requirements, UND for the complete strict
derivation. Missing observations stay explicit. Refused saved code can be personal
material only with origin and actual direct-route evidence (R1/R4/R5). Paths or
hashes copied from the implementation's ownership ledger are not observations.
For processes and ports use actual executable bytes through process roots (R9).
Observe modules, kernel parameters, saved networks and Bluetooth pairs explicitly;
the stand's extra-run omissions must not recur.

After candidate edits, use the last successful committed law. Do not advance it
on a progress message, reconnect or candidate-file write. A reported-success
power cut must record the exact success observation, cut ordering and subsequent
boot identity. Each add/change/remove cut occurs three times. Network loss is
triggered only after captured progress, with old-law evidence before retry.

OW-2 and OW-3 are one sequence on the same installation: T0 → T1, restart,
T1 → T2, restart. `fresh` on OW-3 means the existing sequence installation and
must not silently rebuild T1; an independent T1 setup is useful only as a
supplement. The adapter must preserve and report sequence identity. A changed
test greeting does not count as a system update. REPRO uses independent builds,
not clones; compare the named source/recipe and every named setting, retaining
byte comparisons as diagnostics rather than a byte-reproducibility requirement.

No operating-system event is called breaking by the case party alone. W5-BREAK
runs only in an owned disposable guest and needs independent review; an installer
under root is not breaking. Q4/R10 permits behavior of a recorded personal reader,
but its installation/configuration effects remain subject to the law.

Outcomes: pass (all required observations hold); fail (a requirement is violated
under both readings); undecided (named question, only one reading met); unobserved
(missing capability, failed capture, unavailable hardware or unresolved binding,
with exact command/error). A failing setup blocks dependent checks and emits their
unobserved rows. Each case also gets a summary row. Every fail/unobserved row is
included by `request_entries` in the builder-request evidence. Fixture reports are
labelled FIXTURE ONLY and are never RUN-n.md. Logical rule checks are separate
from machine observations and cannot establish an operating-system property.

## All cases

The steps column names primitive captures/actions; their exact requests, shell
texts, reference comparisons and assertions are printed by `run --case ID --plan`
and frozen in plans.json. Tokens and semantic line kinds are defined in
ASSUMPTIONS.md and FORMATS.md; undocumented native commands are not invented here.

| ID | Version-5 labels | Purpose | Steps |
|---|---|---|---|
| P1-0 | C0, D, K1, K2, W2a, W2b, W3e | Inventory the complete clean machine, including base and all stored generations. | fresh:fresh → read-law:clean-law → inventory:clean |
| UND-0 | K2, W3a, W3b, W3c | Derive without a disk or guest transport; only declared source/package inputs. | derive-inputs:derive |
| G-SHELL | Q4 | Typed ordinary shell command works. | fresh:fresh → command:shell → read-law:final-law → inventory:final |
| G-INSTALL | K1, K4, W2a, Q2 | User/root tool installation, direct package import, extraction, removal, purge, hold and hooks. | fresh:fresh → query:control → query:tool-present → query:before → command:attempt → query:after → read-law:final-law → inventory:final |
| G-BRING | K1, W2a, W4b, Q2, Q3 | Bring an absent installer/runtime as data, then try direct and extracted launch. | fresh:fresh → query:control → query:tool-present → query:before → command:attempt → query:after → read-law:final-law → inventory:final |
| G-DOWNLOAD | K1, W2c, Q3 | Downloaded executable is data until an allowed line; test each storage route. | fresh:fresh → query:control → query:tool-present → query:before → command:attempt → query:after → read-law:final-law → inventory:final |
| G-BUILD | K1, W2c, W3b, Q3 | Compilation may create material; direct execution outside an opening is refused. | fresh:fresh → put-material:source → query:control → query:tool-present → query:before → command:attempt → query:after → read-law:final-law → inventory:final |
| G-SCRIPT | K1, W4b, Q3 | Every shipped interpreter and loader refuses an unrecorded file. | fresh:fresh → put-material:script → query:control → query:tool-present → query:before → command:attempt → query:after → read-law:final-law → inventory:final |
| G-STDIN | W2c, Q4 | Typed pipeline reads material; no unrecorded persistent installation or setting may result. | fresh:fresh → put-material:script → command:pipe → restart:restart → read-law:final-law → inventory:final |
| G-STARTUP | K1, W2b, W4b, Q3, Q7 | Saved startup, hook, alias, automatic macro and login access do not take effect past the law. | fresh:fresh → query:control → query:tool-present → query:before → command:attempt → query:after → read-law:final-law → inventory:final |
| G-READER | K1, W2c, Q3, Q4 | Recorded personal file reader versus unrecorded reader; input execution follows Q4/R10, installation/configuration still forbidden. | fresh:fresh → edit:record → read-law:record-apply-candidate → apply:record-apply → read-law:record-apply-law → put-material:script → command:reader → put-material:persistent-script → command:reader-persistent → restart:restart → query:persistence → read-law:final-law → inventory:final |
| G-UPDATER | K1, K4, W1c, W2a, Q2 | Recorded downloader/installer fetches and attempts a child and a self-update; then explicit lines allow the intended child. | fresh:fresh → edit:record → read-law:record-apply-candidate → apply:record-apply → read-law:record-apply-law → command:attempt → query:unrecorded → command:self-update → query:old-version → read-law:before-child-law → inventory:before-child → edit:child → read-law:child-apply-candidate → apply:child-apply → read-law:child-apply-law → command:child-run → read-law:final-law → inventory:final |
| G-ACCOUNT | K1, W2b, W5a, Q2 | Built-in account mutation through actual tool, including root and absolute tool paths. | fresh:fresh → query:control → query:tool-present → query:before → command:attempt → query:after → read-law:final-law → inventory:final |
| G-RIGHTS | K1, W2b, W5a, Q2 | Built-in rights mutation through actual tool, including root and absolute tool paths. | fresh:fresh → query:control → query:tool-present → query:before → command:attempt → query:after → read-law:final-law → inventory:final |
| G-SERVICE | K1, W2b, W5a, Q2 | Built-in service mutation through actual tool, including root and absolute tool paths. | fresh:fresh → query:control → query:tool-present → query:before → command:attempt → query:after → read-law:final-law → inventory:final |
| G-FIREWALL | K1, W2b, W5a, Q2 | Built-in firewall mutation through actual tool, including root and absolute tool paths. | fresh:fresh → query:control → query:tool-present → query:before → command:attempt → query:after → read-law:final-law → inventory:final |
| G-NETWORK | K1, W2b, W5a, Q2 | Built-in network mutation through actual tool, including root and absolute tool paths. | fresh:fresh → query:control → query:tool-present → query:before → command:attempt → query:after → read-law:final-law → inventory:final |
| G-SAVED-NETWORK | K1, W2b, W5a, Q2 | Built-in saved-network mutation through actual tool, including root and absolute tool paths. | fresh:fresh → query:control → query:tool-present → query:before → command:attempt → query:after → read-law:final-law → inventory:final |
| G-HOST | K1, W2b, W5a, Q2 | Built-in host mutation through actual tool, including root and absolute tool paths. | fresh:fresh → query:control → query:tool-present → query:before → command:attempt → query:after → read-law:final-law → inventory:final |
| G-TIME | K1, W2b, W5a, Q2 | Built-in time mutation through actual tool, including root and absolute tool paths. | fresh:fresh → query:control → query:tool-present → query:before → command:attempt → query:after → read-law:final-law → inventory:final |
| G-LOCALE | K1, W2b, W5a, Q2 | Built-in locale mutation through actual tool, including root and absolute tool paths. | fresh:fresh → query:control → query:tool-present → query:before → command:attempt → query:after → read-law:final-law → inventory:final |
| G-MODULE | K1, W2b, W5a, Q2 | Built-in module mutation through actual tool, including root and absolute tool paths. | fresh:fresh → query:control → query:tool-present → query:before → command:attempt → query:after → read-law:final-law → inventory:final |
| G-SYSCTL | K1, W2b, W5a, Q2 | Built-in sysctl mutation through actual tool, including root and absolute tool paths. | fresh:fresh → query:control → query:tool-present → query:before → command:attempt → query:after → read-law:final-law → inventory:final |
| G-MOUNT | K1, W2b, W5a, Q2 | Built-in mount mutation through actual tool, including root and absolute tool paths. | fresh:fresh → query:control → query:tool-present → query:before → command:attempt → query:after → read-law:final-law → inventory:final |
| G-PIPE | K1, W2b, Q4 | Download/execute typed input; preserve before-reboot evidence and judge persistence after reboot. | fresh:fresh → command:pipeline → inventory:before-reboot → restart:restart → query:persistent → read-law:final-law → inventory:final |
| G-CONTAINER | K1, W2a, Q5 | An actual namespace/container child is inventoried as a host process; unrecorded image/child refuses, recorded child works. | fresh:fresh → query:runtime → container:attempt → query:absent → edit:record → read-law:record-apply-candidate → apply:record-apply → read-law:record-apply-law → container:launch → query:host-process → read-law:final-law → inventory:final |
| OPEN-IN | K1, W4a, Q1, Q3 | Own saved script runs inside the opened folder. | fresh:fresh → edit:open → read-law:open-apply-candidate → apply:open-apply → read-law:open-apply-law → put-material:script → query:positive-script → query:before-script → command:script-attempt → query:marker → read-law:final-law → inventory:final |
| OPEN-OUT | K1, W4a, Q1, Q3 | Same script is refused outside the opened folder. | fresh:fresh → edit:open → read-law:open-apply-candidate → apply:open-apply → read-law:open-apply-law → put-material:script → query:positive-script → query:before-script → command:script-attempt → query:marker → read-law:final-law → inventory:final |
| OPEN-VISIBLE | K2, W1c, W4a, Q1 | Candidate opening is not law until apply; committed externally read declaration visibly names exactly the folder. | fresh:fresh → read-law:old → edit:open → read-law:still-old → read-law:open-apply-candidate → apply:open-apply → read-law:open-apply-law → query:visible → read-law:final-law → inventory:final |
| OPEN-BOUNDARY | K1, K4, W4a, Q1 | No prefix-sibling or symlink-out escape; removal closes the opening after application. | fresh:fresh → edit:open → read-law:open-apply-candidate → apply:open-apply → read-law:open-apply-law → put-material:links → command:symlink-out → query:out → command:prefix → query:prefix-refused → edit:close → read-law:close-apply-candidate → apply:close-apply → read-law:close-apply-law → command:closed → query:closed-refused → read-law:final-law → inventory:final |
| N-VERDICT | N | No percentage/degree substitutes for verdict 1/0/?; test report aggregation with controlled evidence. | fixture verdict matrix (logic only) |
| W4c-DEFAULT | W4c, W4b | A permissive default is a failure even if a later prohibition closes it; preserve both observations. | fresh:fresh → put-material:script → command:default-attempt → query:default → edit:prohibition → apply:prohibit → command:again → query:closed → read-law:final-law → inventory:final |
| W1d-MULTI | W1d, W1c | Split designated description across two files; change included file; compare joined law and unapplied candidate. | fresh:fresh → split-declaration:split → read-law:split-apply-candidate → apply:split-apply → read-law:split-apply-law → query:equivalence → edit:included-edit → query:not-yet → read-law:include-apply-candidate → apply:include-apply → read-law:include-apply-law → read-law:final-law → inventory:final |
| W3d-OPEN | K3, W3d, W3e | Omitted UID/GID may differ; every explicitly named account field must match across order-reversed installations. | two-clean-builds:builds → query:explicit → query:source |
| W3d-LATEST | W3d, W3e | Mutable selector resolves two source versions; compare only named constraints, record both resolutions. | two-clean-builds:builds → query:named → query:resolutions |
| W5-BREAK | W5a, W5b, Q2 | Separate disposable-guest raw root mutation from built-in installer use; retain event for independent review. | fresh:fresh → clone-disposable:clone → raw-root-write:breaking-candidate → query:event → review-event:review |
| Q9-SOURCE | Q9, W3c, W3e | Actual accounts follow a named external server; change server list, reproduce, and remove source line. | fresh:fresh → external-server:server → edit:source → read-law:source-apply-candidate → apply:source-apply → read-law:source-apply-law → query:lookup-a → external-server:change → query:lookup-b → fresh-from-law:reproduce → query:again → edit:remove → read-law:remove-apply-candidate → apply:remove-apply → read-law:remove-apply-law → query:gone → read-law:final-law → inventory:final |
| Q6-GUEST | Q6 | Recorded VM program contains an unrecorded guest system without changing host installation/settings; outer test VM is not this case. | fresh:fresh → query:vm → guest-system:guest → query:contained → query:host-change → read-law:final-law → inventory:final |
| Q7-VALUES | W2c, Q3, Q7 | Ordinary theme/user-agent value is program data; executable/access value is a computer setting. | fresh:fresh → put-material:values → command:read-values → put-material:exec-value → command:execute-value → query:marker → read-law:final-law → inventory:final |
| Q8-PORT | Q8 | Process and listener attributable to recorded executable bytes, with no separate process/port lines. | fresh:fresh → command:listen → query:port → query:identity → read-law:final-law → inventory:final |
| OW-1 | K1, W1b, W2a | Install a source-built program by adding its line. | fresh:fresh → edit:install → read-law:install-apply-candidate → apply:install-apply → read-law:install-apply-law → command:program → read-law:final-law → inventory:final |
| OW-2 | K2, W1b, W1c, W2a, W3b | System update 1 followed by a restart. | fresh:fresh → select-update-start:start → read-boot:old → edit:update → read-law:update-apply-candidate → apply:update-apply → read-law:update-apply-law → restart:restart → query:sources → query:changed → read-law:final-law → inventory:final |
| OW-3 | K2, W1b, W1c, W2a, W3b | System update 2 followed by a restart. | resume-sequence:resume → read-boot:old → edit:update → read-law:update-apply-candidate → apply:update-apply → read-law:update-apply-law → restart:restart → query:sources → query:changed → read-law:final-law → inventory:final |
| OW-4 | W2c | Fetch a plain document with the terminal source-fetch tool. | fresh:fresh → command:fetch → command:read → read-law:final-law → inventory:final |
| OW-5 | W2c | Create, edit and read a plain text file. | fresh:fresh → command:edit → command:read → read-law:final-law → inventory:final |
| OW-6 | W2c, Q4 | Ordinary commands and the recorded own script. | fresh:fresh → command:commands → command:script → read-law:final-law → inventory:final |
| OW-7 | W2c, W3b, Q1, Q4 | Fetch, build, change and rebuild in the opened folder; run all three changed versions. | fresh:fresh → edit:open → read-law:open-apply-candidate → apply:open-apply → read-law:open-apply-law → command:fetch → command:build-1 → command:run-1 → command:edit-1 → command:build-2 → command:run-2 → command:edit-2 → command:build-3 → command:run-3 → command:edit-3 → read-law:final-law → inventory:final |
| OW-8 | K1, K4, W3b, Q2 | Recorded updater and child replace launcher/game; apply install/update/remove through lines. | fresh:fresh → edit:child → read-law:install-candidate → apply:install → read-law:install-law → command:run → edit:update-line → read-law:update-candidate → apply:update → read-law:update-law → command:updated → read-law:final-law → inventory:final |
| OW-9 | K2, W1c | Interrupt an installation after observed transfer starts; old law survives failure; restore and retry. | fresh:fresh → read-law:old → edit:install → start-apply:begin → query:progress → network:down → finish-apply:failed → read-law:unchanged → read-law:failed-state-law → inventory:failed-state → network:up → read-law:retry-candidate → apply:retry → read-law:retry-law → command:program → read-law:final-law → inventory:final |
| P2-NET-1 | K2, W1c | Interrupt an installation after observed transfer starts; old law survives failure; restore and retry. | fresh:fresh → read-law:old → edit:install → start-apply:begin → query:progress → network:down → finish-apply:failed → read-law:unchanged → read-law:failed-state-law → inventory:failed-state → network:up → read-law:retry-candidate → apply:retry → read-law:retry-law → command:program → read-law:final-law → inventory:final |
| OW-10 | K3, K4, W2b | Connect/pair, independently inspect stored/effective state, reproduce and remove; physical laptop. | fresh:fresh → query:hardware → radio-request:request → record-radio-if-needed:line → read-law:connect-apply-candidate → apply:connect-apply → read-law:connect-apply-law → query:connected → query:stored → read-law:connected-state-law → inventory:connected-state → fresh-from-law:reproduce → query:reproduced → edit:remove → read-law:remove-apply-candidate → apply:remove-apply → read-law:remove-apply-law → query:gone-live → query:gone-stored → read-law:removed-law → inventory:removed |
| OW-11 | K3, K4, W2b | Connect/pair, independently inspect stored/effective state, reproduce and remove; physical laptop. | fresh:fresh → query:hardware → radio-request:request → record-radio-if-needed:line → read-law:connect-apply-candidate → apply:connect-apply → read-law:connect-apply-law → query:connected → query:stored → read-law:connected-state-law → inventory:connected-state → fresh-from-law:reproduce → query:reproduced → edit:remove → read-law:remove-apply-candidate → apply:remove-apply → read-law:remove-apply-law → query:gone-live → query:gone-stored → read-law:removed-law → inventory:removed |
| X-WIFI | K3, K4, W2b | Connect/pair, independently inspect stored/effective state, reproduce and remove; simulated radio only. | fresh:fresh → query:hardware → radio-request:request → record-radio-if-needed:line → read-law:connect-apply-candidate → apply:connect-apply → read-law:connect-apply-law → query:connected → query:stored → read-law:connected-state-law → inventory:connected-state → fresh-from-law:reproduce → query:reproduced → edit:remove → read-law:remove-apply-candidate → apply:remove-apply → read-law:remove-apply-law → query:gone-live → query:gone-stored → read-law:removed-law → inventory:removed |
| X-BT | K3, K4, W2b | Connect/pair, independently inspect stored/effective state, reproduce and remove; simulated radio only. | fresh:fresh → query:hardware → radio-request:request → record-radio-if-needed:line → read-law:connect-apply-candidate → apply:connect-apply → read-law:connect-apply-law → query:connected → query:stored → read-law:connected-state-law → inventory:connected-state → fresh-from-law:reproduce → query:reproduced → edit:remove → read-law:remove-apply-candidate → apply:remove-apply → read-law:remove-apply-law → query:gone-live → query:gone-stored → read-law:removed-law → inventory:removed |
| P2-ADD-1 | K2, W1a, W1b, W1c, W1e, W3a | Power cut immediately after reported success: add, repetition 1. | fresh:fresh → prepare-change:prepare → read-law:candidate → apply-cut:cut → boot:boot → read-law:durable → read-law:final-law → inventory:final |
| P2-ADD-2 | K2, W1a, W1b, W1c, W1e, W3a | Power cut immediately after reported success: add, repetition 2. | fresh:fresh → prepare-change:prepare → read-law:candidate → apply-cut:cut → boot:boot → read-law:durable → read-law:final-law → inventory:final |
| P2-ADD-3 | K2, W1a, W1b, W1c, W1e, W3a | Power cut immediately after reported success: add, repetition 3. | fresh:fresh → prepare-change:prepare → read-law:candidate → apply-cut:cut → boot:boot → read-law:durable → read-law:final-law → inventory:final |
| P2-CHG-1 | K2, W1a, W1b, W1c, W1e, W3a | Power cut immediately after reported success: chg, repetition 1. | fresh:fresh → prepare-change:prepare → read-law:candidate → apply-cut:cut → boot:boot → read-law:durable → read-law:final-law → inventory:final |
| P2-CHG-2 | K2, W1a, W1b, W1c, W1e, W3a | Power cut immediately after reported success: chg, repetition 2. | fresh:fresh → prepare-change:prepare → read-law:candidate → apply-cut:cut → boot:boot → read-law:durable → read-law:final-law → inventory:final |
| P2-CHG-3 | K2, W1a, W1b, W1c, W1e, W3a | Power cut immediately after reported success: chg, repetition 3. | fresh:fresh → prepare-change:prepare → read-law:candidate → apply-cut:cut → boot:boot → read-law:durable → read-law:final-law → inventory:final |
| P2-REM-1 | K2, W1a, W1b, W1c, W1e, W3a | Power cut immediately after reported success: rem, repetition 1. | fresh:fresh → prepare-change:prepare → read-law:candidate → apply-cut:cut → boot:boot → read-law:durable → read-law:final-law → inventory:final |
| P2-REM-2 | K2, W1a, W1b, W1c, W1e, W3a | Power cut immediately after reported success: rem, repetition 2. | fresh:fresh → prepare-change:prepare → read-law:candidate → apply-cut:cut → boot:boot → read-law:durable → read-law:final-law → inventory:final |
| P2-REM-3 | K2, W1a, W1b, W1c, W1e, W3a | Power cut immediately after reported success: rem, repetition 3. | fresh:fresh → prepare-change:prepare → read-law:candidate → apply-cut:cut → boot:boot → read-law:durable → read-law:final-law → inventory:final |
| REM-1 | K4, W3b, W3e | Remove program-and-process and every contribution not supplied by another line. | fresh:fresh → prepare-removal:prepare → query:present → inventory:before → edit:remove → read-law:remove-apply-candidate → apply:remove-apply → read-law:remove-apply-law → query:absent → query:contributions → read-law:final-law → inventory:final |
| REM-2 | K4, W3b, W3e | Remove service-and-process and every contribution not supplied by another line. | fresh:fresh → prepare-removal:prepare → query:present → inventory:before → edit:remove → read-law:remove-apply-candidate → apply:remove-apply → read-law:remove-apply-law → query:absent → query:contributions → read-law:final-law → inventory:final |
| REM-3a | K4, W3b, W3e | Remove firewall-rule and every contribution not supplied by another line. | fresh:fresh → prepare-removal:prepare → query:present → inventory:before → edit:remove → read-law:remove-apply-candidate → apply:remove-apply → read-law:remove-apply-law → query:absent → query:contributions → read-law:final-law → inventory:final |
| REM-3b | K4, W3b, W3e | Remove rights-rule and every contribution not supplied by another line. | fresh:fresh → prepare-removal:prepare → query:present → inventory:before → edit:remove → read-law:remove-apply-candidate → apply:remove-apply → read-law:remove-apply-law → query:absent → query:contributions → read-law:final-law → inventory:final |
| REM-4 | K4, W3b, W3e | Shared dependency remains with one owner; disappears after removing last owner. | fresh:fresh → prepare-shared:owners → edit:remove-a → read-law:remove-a-apply-candidate → apply:remove-a-apply → read-law:remove-a-apply-law → query:shared-stays → read-law:one-owner-law → inventory:one-owner → edit:remove-b → read-law:remove-b-apply-candidate → apply:remove-b-apply → read-law:remove-b-apply-law → query:shared-gone → read-law:final-law → inventory:final |
| REPRO-1 | K3, W3c, W3d | Two independent clean builds; compare named source/recipe and setting values, not compiled byte identity. | two-clean-builds:builds → query:independent → query:equal |
| REPRO-2a | K3, W3c, W3d | Two independent clean builds; compare named source/recipe and setting values, not compiled byte identity. | two-clean-builds:builds → query:independent → query:equal |
| REPRO-2b | K3, W3c, W3d | Two independent clean builds; compare named source/recipe and setting values, not compiled byte identity. | two-clean-builds:builds → query:independent → query:equal |
| X-REC-APT | K1, K4, W1a, W1b, W1c, W2a, W2b, Q2 | Request package; refusal or exact record is allowed; manual line supplies positive install/apply/remove cycle. | fresh:fresh → read-law:old → tool-request:request → read-law:still-old → query:candidate-delta → query:no-effect → record-if-refused:record → read-law:requested-apply-candidate → apply:requested-apply → read-law:requested-apply-law → query:effect → read-law:applied-law → inventory:applied → tool-request:remove-request → query:still-effect → record-removal-if-refused:remove → read-law:removed-apply-candidate → apply:removed-apply → read-law:removed-apply-law → query:gone → read-law:final-law → inventory:final |
| X-REC-APT2 | K1, K4, W1a, W1b, W1c, W2a, W2b, Q2 | Request package-file; refusal or exact record is allowed; manual line supplies positive install/apply/remove cycle. | fresh:fresh → read-law:old → tool-request:request → read-law:still-old → query:candidate-delta → query:no-effect → record-if-refused:record → read-law:requested-apply-candidate → apply:requested-apply → read-law:requested-apply-law → query:effect → read-law:applied-law → inventory:applied → tool-request:remove-request → query:still-effect → record-removal-if-refused:remove → read-law:removed-apply-candidate → apply:removed-apply → read-law:removed-apply-law → query:gone → read-law:final-law → inventory:final |
| X-REC-HOST | K1, K4, W1a, W1b, W1c, W2a, W2b, Q2 | Request hostname; refusal or exact record is allowed; manual line supplies positive install/apply/remove cycle. | fresh:fresh → read-law:old → tool-request:request → read-law:still-old → query:candidate-delta → query:no-effect → record-if-refused:record → read-law:requested-apply-candidate → apply:requested-apply → read-law:requested-apply-law → query:effect → read-law:applied-law → inventory:applied → tool-request:remove-request → query:still-effect → record-removal-if-refused:remove → read-law:removed-apply-candidate → apply:removed-apply → read-law:removed-apply-law → query:gone → read-law:final-law → inventory:final |
| X-REC-TIME | K1, K4, W1a, W1b, W1c, W2a, W2b, Q2 | Request timezone; refusal or exact record is allowed; manual line supplies positive install/apply/remove cycle. | fresh:fresh → read-law:old → tool-request:request → read-law:still-old → query:candidate-delta → query:no-effect → record-if-refused:record → read-law:requested-apply-candidate → apply:requested-apply → read-law:requested-apply-law → query:effect → read-law:applied-law → inventory:applied → tool-request:remove-request → query:still-effect → record-removal-if-refused:remove → read-law:removed-apply-candidate → apply:removed-apply → read-law:removed-apply-law → query:gone → read-law:final-law → inventory:final |
| X-REC-SYSCTL | K1, K4, W1a, W1b, W1c, W2a, W2b, Q2 | Request sysctl; refusal or exact record is allowed; manual line supplies positive install/apply/remove cycle. | fresh:fresh → read-law:old → tool-request:request → read-law:still-old → query:candidate-delta → query:no-effect → record-if-refused:record → read-law:requested-apply-candidate → apply:requested-apply → read-law:requested-apply-law → query:effect → read-law:applied-law → inventory:applied → tool-request:remove-request → query:still-effect → record-removal-if-refused:remove → read-law:removed-apply-candidate → apply:removed-apply → read-law:removed-apply-law → query:gone → read-law:final-law → inventory:final |
| X-REC-ENABLE | K1, K4, W1a, W1b, W1c, W2a, W2b, Q2 | Request service; refusal or exact record is allowed; manual line supplies positive install/apply/remove cycle. | fresh:fresh → read-law:old → tool-request:request → read-law:still-old → query:candidate-delta → query:no-effect → record-if-refused:record → read-law:requested-apply-candidate → apply:requested-apply → read-law:requested-apply-law → query:effect → read-law:applied-law → inventory:applied → tool-request:remove-request → query:still-effect → record-removal-if-refused:remove → read-law:removed-apply-candidate → apply:removed-apply → read-law:removed-apply-law → query:gone → read-law:final-law → inventory:final |
| X-REC-UENABLE | K1, K4, W1a, W1b, W1c, W2a, W2b, Q2 | Request user-service; refusal or exact record is allowed; manual line supplies positive install/apply/remove cycle. | fresh:fresh → read-law:old → tool-request:request → read-law:still-old → query:candidate-delta → query:no-effect → record-if-refused:record → read-law:requested-apply-candidate → apply:requested-apply → read-law:requested-apply-law → query:effect → read-law:applied-law → inventory:applied → tool-request:remove-request → query:still-effect → record-removal-if-refused:remove → read-law:removed-apply-candidate → apply:removed-apply → read-law:removed-apply-law → query:gone → read-law:final-law → inventory:final |
| X-REC-USER | K1, K4, W1a, W1b, W1c, W2a, W2b, Q2 | Request account; refusal or exact record is allowed; manual line supplies positive install/apply/remove cycle. | fresh:fresh → read-law:old → tool-request:request → read-law:still-old → query:candidate-delta → query:no-effect → record-if-refused:record → read-law:requested-apply-candidate → apply:requested-apply → read-law:requested-apply-law → query:effect → read-law:applied-law → inventory:applied → tool-request:remove-request → query:still-effect → record-removal-if-refused:remove → read-law:removed-apply-candidate → apply:removed-apply → read-law:removed-apply-law → query:gone → read-law:final-law → inventory:final |
| X-REC-USERMOD | K1, K4, W1a, W1b, W1c, W2a, W2b, Q2 | Request account-change; refusal or exact record is allowed; manual line supplies positive install/apply/remove cycle. | fresh:fresh → read-law:old → tool-request:request → read-law:still-old → query:candidate-delta → query:no-effect → record-if-refused:record → read-law:requested-apply-candidate → apply:requested-apply → read-law:requested-apply-law → query:effect → read-law:applied-law → inventory:applied → tool-request:remove-request → query:still-effect → record-removal-if-refused:remove → read-law:removed-apply-candidate → apply:removed-apply → read-law:removed-apply-law → query:gone → read-law:final-law → inventory:final |
| X-REC-NFT | K1, K4, W1a, W1b, W1c, W2a, W2b, Q2 | Request firewall; refusal or exact record is allowed; manual line supplies positive install/apply/remove cycle. | fresh:fresh → read-law:old → tool-request:request → read-law:still-old → query:candidate-delta → query:no-effect → record-if-refused:record → read-law:requested-apply-candidate → apply:requested-apply → read-law:requested-apply-law → query:effect → read-law:applied-law → inventory:applied → tool-request:remove-request → query:still-effect → record-removal-if-refused:remove → read-law:removed-apply-candidate → apply:removed-apply → read-law:removed-apply-law → query:gone → read-law:final-law → inventory:final |
| X-REC-LOCALE | K1, K4, W1a, W1b, W1c, W2a, W2b, Q2 | Request locale; refusal or exact record is allowed; manual line supplies positive install/apply/remove cycle. | fresh:fresh → read-law:old → tool-request:request → read-law:still-old → query:candidate-delta → query:no-effect → record-if-refused:record → read-law:requested-apply-candidate → apply:requested-apply → read-law:requested-apply-law → query:effect → read-law:applied-law → inventory:applied → tool-request:remove-request → query:still-effect → record-removal-if-refused:remove → read-law:removed-apply-candidate → apply:removed-apply → read-law:removed-apply-law → query:gone → read-law:final-law → inventory:final |
| X-REC-GROUP | K1, K4, W1a, W1b, W1c, W2a, W2b, Q2 | Request group; refusal or exact record is allowed; manual line supplies positive install/apply/remove cycle. | fresh:fresh → read-law:old → tool-request:request → read-law:still-old → query:candidate-delta → query:no-effect → record-if-refused:record → read-law:requested-apply-candidate → apply:requested-apply → read-law:requested-apply-law → query:effect → read-law:applied-law → inventory:applied → tool-request:remove-request → query:still-effect → record-removal-if-refused:remove → read-law:removed-apply-candidate → apply:removed-apply → read-law:removed-apply-law → query:gone → read-law:final-law → inventory:final |
| X-REC-SUDO | K1, K4, W1a, W1b, W1c, W2a, W2b, Q2 | Request rights; refusal or exact record is allowed; manual line supplies positive install/apply/remove cycle. | fresh:fresh → read-law:old → tool-request:request → read-law:still-old → query:candidate-delta → query:no-effect → record-if-refused:record → read-law:requested-apply-candidate → apply:requested-apply → read-law:requested-apply-law → query:effect → read-law:applied-law → inventory:applied → tool-request:remove-request → query:still-effect → record-removal-if-refused:remove → read-law:removed-apply-candidate → apply:removed-apply → read-law:removed-apply-law → query:gone → read-law:final-law → inventory:final |
| X-REC-MODULE | K1, K4, W1a, W1b, W1c, W2a, W2b, Q2 | Request module; refusal or exact record is allowed; manual line supplies positive install/apply/remove cycle. | fresh:fresh → read-law:old → tool-request:request → read-law:still-old → query:candidate-delta → query:no-effect → record-if-refused:record → read-law:requested-apply-candidate → apply:requested-apply → read-law:requested-apply-law → query:effect → read-law:applied-law → inventory:applied → tool-request:remove-request → query:still-effect → record-removal-if-refused:remove → read-law:removed-apply-candidate → apply:removed-apply → read-law:removed-apply-law → query:gone → read-law:final-law → inventory:final |
| X-REC-LINGER | K1, K4, W1a, W1b, W1c, W2a, W2b, Q2 | Request linger; refusal or exact record is allowed; manual line supplies positive install/apply/remove cycle. | fresh:fresh → read-law:old → tool-request:request → read-law:still-old → query:candidate-delta → query:no-effect → record-if-refused:record → read-law:requested-apply-candidate → apply:requested-apply → read-law:requested-apply-law → query:effect → read-law:applied-law → inventory:applied → tool-request:remove-request → query:still-effect → record-removal-if-refused:remove → read-law:removed-apply-candidate → apply:removed-apply → read-law:removed-apply-law → query:gone → read-law:final-law → inventory:final |

## Required variant executions

- **G-INSTALL**: user install; root install; direct native executable path; file import; remove recorded package; forced purge; extract then run; hold recorded version; installer hook.
- **G-BRING**: plain executable; archive extract; self-extracting wrapper; interpreter; container engine; user/root.
- **G-DOWNLOAD**: home; /tmp; /dev/shm; /var/tmp; archive extraction.
- **G-BUILD**: home; /tmp; /dev/shm; recipe file; command expansion; make install.
- **G-SCRIPT**: shell filename; shell redirected file; shell source; shebang direct; every shipped interpreter; loader non-executable ELF; debugger rc; runtime nested reader; explicit plugin; temporary nested reader.
- **G-STDIN**: cat file | shell; typed command substitution; saved stdin file is a direct route: G-SCRIPT.
- **G-STARTUP**: shell rc; login profile; logout; executable alias; hook directory; autostart; SSH rc; authorized key login; installer pre-invoke; editor rc; plugin directory; plugin setting; saved macro home; saved macro tmp; SSH ProxyCommand; SSH Match exec.
- **G-UPDATER**: user local prefix; root global prefix; project directory; download cache then install; fetch-and-execute; self-update.
- **G-ACCOUNT**: useradd; usermod groups; passwd; chpasswd; groupadd.
- **G-RIGHTS**: rights editor; login key; direct root write is W5-BREAK.
- **G-SERVICE**: user persistent; user transient; delayed timer; user crontab; root crontab; root service link; disable/mask recorded service; linger; at; service parameter; root crontab for another user.
- **G-FIREWALL**: add rule; remove recorded rule.
- **G-NETWORK**: temporary address; route.
- **G-SAVED-NETWORK**: create saved network.
- **G-HOST**: set name.
- **G-TIME**: timezone.
- **G-LOCALE**: system locale.
- **G-MODULE**: load module.
- **G-SYSCTL**: kernel setting.
- **G-MOUNT**: mount filesystem.
- **G-PIPE**: pipeline; process substitution if supported; typed string substitution.

## Previously untested and partial statements

| TABLE.md gap | Case | Limit retained |
|---|---|---|
| N | N-VERDICT | Logical reporting test only, not an empirical definition test. |
| W1d | W1d-MULTI | Requires actual multi-file designated description, not merely input payload files. |
| W3d | W3d-OPEN, W3d-LATEST, REPRO-2b | Unsupported omission/selector remains unobserved. |
| W4a, Q1 | OPEN-IN, OPEN-OUT, OPEN-VISIBLE, OPEN-BOUNDARY | One kind of real folder-opening line; no fixture substitutes for native execution. |
| W4c | W4c-DEFAULT | Default result retained even if a later prohibition succeeds; logical aggregation also fixture-tested. |
| W5b | W5-BREAK | Successful raw event and independent classification required; lack of full root is unobserved. |
| Q9 | Q9-SOURCE | Actual account lookups from named server, not a mock list disconnected from login/account mechanisms. |
| Q2 updaters | G-UPDATER | Small recorded downloader/installer, user and root variants; does not claim every updater tested. |
| Q4 recorded reader | G-READER | Same saved input through ordinary interpreter vs personally recorded file reader; persistent effects checked. |
| Q6 guest system | Q6-GUEST | In-system VM program required; outer VM not a substitute. |
| Q7 harmless values | Q7-VALUES | Plain theme/user-agent data contrasted with executable/access configuration. |
| Q8 port attribution | Q8-PORT | Listening port and process attributed by executable bytes, no extra line. |

## Freeze and runs

READY.md lists the publication set and the native-binding addendum required before
run 1. Part 1 does not start a VM, install an OS, or issue a system verdict. The set is
published before the first complete run; these tools do not publish. Every complete run later names one
release, source hash and declaration/binding hash and attempts every variant,
including hardware cases as unobserved when hardware is unavailable. No clean
VM result substitutes for the required real-hardware result. At most eight
complete runs; search results are added before the next complete run.
