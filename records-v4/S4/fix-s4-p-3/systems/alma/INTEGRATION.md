# Key-event adapter integration

Publish byte-identical copies of `assembled-main.py` and `key_events.py` in `S4/fix-s4-p-3/`; the wrapper resolves its core as `R.parent/'collector'`. `check-inputs-v4/supplement-1/step-4-instruments/S4/collector` remains unchanged. The fourth fresh rehearsal uses exactly this layout under a task root: `addition/assembled-main.py`, `addition/key_events.py`, `check-inputs-v4/supplement-1/step-4-instruments/S4/collector`. The harness's root wrapper path is a symlink to `addition/assembled-main.py`; resolving `__file__` therefore selects the intended layout. Hashes are in `raw/final-adapter.sha256.tsv`.

For Alma only, the new collect entry point should execute this wrapper with the original CLI arguments and LAB_ROOT. The wrapper calls the unchanged `extended.collect(ctx)` and then `key_events.collect(ctx)`. Other systems use the original entry point. No modification to any earlier-round source is required.

`alma-key-events.tsv` columns:

`object_id`, `key_id`, `fingerprint`, `key_source`, `import_timestamp`, `success_timestamp`, `preceding_command`, `source_file`, `log_segment`, `command_line`, `event_line`, `success_line`, `status`, `evidence`.

The object join is to package names beginning `rpm:gpg-pubkey@<key_id>-`; multiple candidates explicitly receive `unknown:multiple-package-key-matches`. `fingerprint` is the full logged fingerprint and must end in the key ID for complete fields. `key_source` is an allowlisted local RPM key path. `preceding_command` is the safe DNF install invocation logged before the event in the same initialization segment; it is a measured textual relationship, never a classification or a complete causal trace. Command resets and new log segments prevent crossing a boundary for the success message. Unsupported commands and absent fields retain explicit unknown markers. No key user ID or arbitrary command argument is saved.

`alma-key-event-coverage.tsv` columns: `source`, `status`, `lines`, `bytes`, `query_exit_status`, `evidence`. Every current/rotated DNF log is covered; a 32 MiB per-file cap or read failure remains explicit. The `evidence` reference points to the retained query output in an authorized observation. The query retains event fields, not an explicit/dependent label.

The aggregate diagnostic `adapters.alma_key_events` records query exit status, joined rows and complete field rows. The seven synthetic parser checks are in `raw/key-parser-tests.json`; they test field retention, missing success, a command boundary, unsupported arguments, and general safe package names. No synthetic check is an object decision.

The byte cap is applied before UTF-8 decoding. Coverage always includes a query-level status; nonzero query exits preserve available fields with `unknown:query-failed`, never `fields-recorded`. Synthetic checks include a multibyte byte-cap case and partial stdout with nonzero transport exit.
