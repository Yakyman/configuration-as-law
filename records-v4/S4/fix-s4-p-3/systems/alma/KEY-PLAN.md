# Structured key-event route

Written 2026-11-23 UTC before the third fresh rehearsal. Candidate verification found an exact target-key import message in the DNF log. No conclusion about a reason follows from the absence of a same-line English reason keyword.

Primary source checked before the next query:

- https://raw.githubusercontent.com/rpm-software-management/dnf/master/dnf/crypto.py, `log_key_import`: the message contains “Importing GPG key”, “Fingerprint:” and “From”.
- https://raw.githubusercontent.com/rpm-software-management/dnf/master/dnf/base.py, key import: “Key imported successfully” is logged only after `pgpImportPubkey` returns zero.
- https://raw.githubusercontent.com/rpm-software-management/dnf/master/dnf/cli/cli.py: “Base command:” and “Extra commands:” are log fields; `_log_essentials` records the command invocation.

These sources explain log fields, but do not answer whether this concrete log contains enough fields to link the target key to its import invocation. A new structured parser will record the key message block, fingerprint/source, following import-success message, and preceding command within the same log initialization segment. It never labels an import explicit or dependent; those are not measurement fields. The command field is an allowlisted DNF invocation only; arbitrary command strings and key user IDs are excluded. Any absent fields remain unknown. Expectation: the exact key may have a complete logged invocation and success sequence, but causal attribution is not inferred merely from proximity. The parser's diagnostic reducer reports completeness and ambiguity; raw event rows are never displayed or retained in rehearsal. A third fresh copy receives unchanged ordinary actions. If useful, the same module will be available for the frozen collector.
