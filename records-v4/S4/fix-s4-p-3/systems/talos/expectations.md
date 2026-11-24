# Targeted Talos rehearsals

Written 2026-11-23 UTC before boot and queries. Only T03 and T05 are in scope; no ordinary action is assigned by C1/actions/README.md. Existing complete listing/hash attempts are not repeated. All queries run on a new disposable copy. No object decisions are made.

Primary sources checked:

- https://raw.githubusercontent.com/siderolabs/talos/v1.14.6/cmd/talosctl/cmd/talos/logs.go: “Retrieve logs for a service”. Retained machined/installer logs may contain an installation reference or member writes, but retention may start at this boot.
- https://raw.githubusercontent.com/siderolabs/talos/v1.14.6/cmd/talosctl/cmd/talos/events.go: “Stream runtime events”; output includes ID, EVENT, ACTOR, SOURCE, MESSAGE. A bounded replay may expose writer events; current events need not cover installation.
- https://raw.githubusercontent.com/siderolabs/talos/v1.14.6/internal/app/auditd/auditd.go: “logs audit events”. Structured kernel PATH/SYSCALL records, if present, can identify writes; service presence does not imply retained creation records.
- https://raw.githubusercontent.com/siderolabs/talos/v1.14.6/internal/app/machined/pkg/controllers/runtime/sbom_item.go: “We are only interested in some fields.” The resource projection keeps package fields, so do not repeat that known insufficient query; read raw SPDX documents to test whether files/checksums/relationships survive there.
- https://raw.githubusercontent.com/siderolabs/talos/v1.14.6/pkg/machinery/constants/constants.go: `SPDXPath = "/usr/share/spdx"`; `StateMountPoint = "/system/state"`. Raw SPDX and retained installation-state files are distinct candidate reference routes.
- https://raw.githubusercontent.com/siderolabs/talos/v1.14.6/pkg/machinery/resources/files/etcfile_status.go: `SpecVersion string`; this resource links rendered files to specifications, but its schema alone establishes no historic writer. Resource metadata and corresponding spec controller ownership will be examined as candidate derivation evidence, without equating present ownership to past creation.
- https://raw.githubusercontent.com/siderolabs/talos/v1.14.6/cmd/talosctl/cmd/talos/get.go: “use 'talosctl get rd' to see all available resource types”. Discovery selects actual resource names before the targeted resource queries.

T03 methods: (1) raw installed SPDX document file/checksum/relationship fields; (2) retained boot/state installation references and artifact companion metadata; (3) service installation history, including every candidate event and explicit residual missing member/reference linkage. Expected: package identities or boot artifacts may exist, but no complete per-member original reference plus current comparison across all 31 groups.

T05 methods: (1) structured audit records for member creation, correlating event identifiers rather than words; (2) file-controller spec/status and resource metadata, joining actual selected resources; (3) replay of runtime events, examining all returned event types/actors/messages. Expected: some live controller associations, but no complete historic per-member creator/derivation chain for all 29 groups.

Bounds: each ordinary query 30 seconds/16 MiB, SPDX file 64 MiB, runtime events 10 seconds with last 1000 replay entries. Timeouts and caps are failed methods, not absence. Candidate names and event structures are inspected explicitly; arbitrary English keyword absence is never sufficient. Raw inventories stay transient and are deleted; retain command statuses, counts, field schemas and diagnostic excerpts only.
