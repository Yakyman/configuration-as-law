# Fact locations

No inventory was taken because pre-observation input verification failed. No package, packaged-file, group-member, or persistence facts were collected. A header-only object table does not assert absence of objects.

| Machine | Exact retained file | Package reason / packaged-file integrity / group members / persistence | Object-ID mapping |
|---|---|---|---|
| alma | (not published: record outside selected evidence) | Unavailable; no collector output, fact files or columns exist | `D1/in/part-alma.tsv` is header-only; no object IDs |
| void | (not published: record outside selected evidence) | Unavailable; no collector output, fact files or columns exist | `D1/in/part-void.tsv` is header-only; no object IDs |
| gentoo | `D1/in/raw/gentoo/NOT-RUN.md` | Unavailable; no collector output, fact files or columns exist | `D1/in/part-gentoo.tsv` is header-only; no object IDs |
| microos | (not published: record outside selected evidence) | Unavailable; no collector output, fact files or columns exist | `D1/in/part-microos.tsv` is header-only; no object IDs |
| talos | (not published: record outside selected evidence) | Unavailable; no collector output, fact files or columns exist | `D1/in/part-talos.tsv` is header-only; no object IDs |

The retained Markdown files document the stop only; they are not collector output. The exact part-table header is `id	part	machine	kind	name	members	evidence`. Input-check columns in `D1/in/control/input-verification.tsv` are `path`, `expected_sha256`, `actual_sha256`, and `status`; the failing row is `PUBLISH.list`.
