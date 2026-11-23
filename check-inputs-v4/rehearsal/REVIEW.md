# Rehearsal source review

Review date: 2026-11-23 UTC

Result: rejected pending correction.

Scope: static review of `run.py`, `sanitize-status.py`, and `../collector/main.py`, plus the available sanitized `status.tsv` and `counts.tsv`. No virtual machine was started. No raw inventory, transient unread directory, guest content, or unrelated task directory was read.

## Blocking findings

1. `run.py` destroys the rehearsal name unconditionally in `finally`, including when clone creation fails. A failed creation caused by an existing name can therefore destroy a clone that this invocation did not create. Record successful creation in a boolean and call `destroy` only when that boolean is true.

2. The action-status reducer accepts any guest-provided first field when the other two fields are decimal and retains that field in the operation label. The assertion that labels come from fixed scripts is not enforced, and `sanitize-status.py` has no rule for action labels. Match labels against a host-side exact allowlist of expected action identifiers, or retain a fixed host-defined identifier instead of the guest field.

3. The collector exit status is recorded but ignored by the reduction logic. If partial transient files exist after a nonzero collector exit, `run.py` emits plausible package, integrity, object, level, and metadata counts from those partial files. Reduce only after a zero collector exit and required artifact/schema validation, or retain an explicit numeric validity indicator for every partial reduction.

4. Rehearsal authorization in `collector/main.py` verifies only that the machine identifier begins with `reh-`. It does not verify from metadata that the target is a disposable clone. If the laboratory layer does not make the name prefix an unforgeable clone-provenance invariant, require and validate a disposable/throwaway metadata field before transport starts.

## Non-blocking checks

- All three reviewed source files parse as Python syntax.
- The available sanitized tables have the expected headers. Measurement fields are numeric, and retained labels use fixed category syntax.
- Transient collector output is removed in the outer `finally`, and guest action logs/status are explicitly removed after successful staging and reduction. Failed destruction remains visible as a numeric `destroy` status, but the clone can remain allocated and requires operational follow-up.
- `C1_INPUTS_COMMIT` is required before observation mode, as specified. Its value is checked only for non-emptiness; it is not validated against a commit identifier in this source.

Acceptance requires correcting findings 1–3. Finding 4 requires either a code guard or a documented, enforced laboratory invariant.
