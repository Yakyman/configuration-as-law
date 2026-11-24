# Independent dynamic-download summarizer review

Review time: 2026-11-23T12:21:40Z

Scope: bounded re-review of the `DOWNLOAD` transport correction in `summarize-round1.py` against the frozen ordinary-suite and adapter sources, the pinned baseline, and the completed carried ordinary log. The carried log was read over a read-only connection into an automatically removed local temporary directory. No guest, probe, metrics file, or remote file was started or changed.

## Source contract

The correction pins `round4-selftest.py` to SHA-256 `e72ef3e2d88a29f42127bf9979774a9067543365509843bec76e513ce74be9b7`. That source creates a loopback HTTP server with port zero and directly invokes `stand-session` to run `/usr/bin/curl` against `/development` on the kernel-selected port. The baseline `DOWNLOAD` expectation deliberately has no `command` field, which is why the earlier generic expected-row derivation missed this marker.

The new rule requires exactly one `DOWNLOAD` expectation and a Bash-entry marker immediately after it. It fixes every argument, the adapter wrapper, loopback address, URL path, tab-separated sealed command, and canonical shell quoting. Only a decimal port from 1 through 65535 may vary. The extracted port is then substituted into the exact source template and passed through the same pinned adapter transformation as every other planned marker. The complete marker sequence is still compared for payload, placement, order, and count, so the dynamic binding cannot excuse an extra marker or changes elsewhere.

Metrics retain the selected port, the ordinary-suite source SHA-256, a description of the bounded binding, all 46 marker records, and the ordered marker SHA-256. This is an honest target-derived binding for a single source-declared runtime value, rather than target-derived expected behavior.

## Read-only validation

The current summarizer and its ordinary-suite and adapter source pins match the current files. Running `adapted_rows()` and the baseline contract comparison against the completed carried `ordinary.jsonl` succeeded with:

- 120 non-marker records matching the pinned baseline contract;
- 46 Bash-entry markers;
- one dynamic `DOWNLOAD` binding, port 42957;
- ordered normalized marker SHA-256 `c832bb45931288509ab9b75b109bc8d5c2de438b10cf51bad85be5edf4b95c26`.

The temporary local copy was removed automatically after the check.

## Verdict

The correction resolves the 45-versus-46 marker defect without weakening the remaining transport checks. No material defect was found in this bounded change. The carried ordinary routing contract is acceptable for final host-side validation.

This review accepts only the corrected summarizer path. It does not accept the still-running combined replay, final metrics, publication, or any variant closure. The overall outcome remains `?`.
