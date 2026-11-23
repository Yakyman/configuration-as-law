# Exact-hash metadata evidence attempt

Seven unresolved compiled-module rows were looked up at both official substitute servers using bounded narinfo-only requests. No archive, build, or runtime probe was requested.

| Row | Metadata URL | Result |
|---|---|---|
| guix-4693999f1c | https://bordeaux.guix.gnu.org/7l0k1845l029ml5wqwvv7d395cqz4yb2.narinfo | HTTP Error 404: Not Found |
| guix-4693999f1c | https://ci.guix.gnu.org/7l0k1845l029ml5wqwvv7d395cqz4yb2.narinfo | 200 |
| guix-a36c632a1b | https://bordeaux.guix.gnu.org/8274vsd16hj4f9s16nrrra8037i5bx23.narinfo | HTTP Error 404: Not Found |
| guix-a36c632a1b | https://ci.guix.gnu.org/8274vsd16hj4f9s16nrrra8037i5bx23.narinfo | 200 |
| guix-9b6df1084f | https://bordeaux.guix.gnu.org/8dyvh1f7hzfyz8c80vyb7qqis8qd578w.narinfo | HTTP Error 404: Not Found |
| guix-9b6df1084f | https://ci.guix.gnu.org/8dyvh1f7hzfyz8c80vyb7qqis8qd578w.narinfo | 200 |
| guix-2b6eee2e59 | https://bordeaux.guix.gnu.org/agiylfh65q5vxzmxb0351xl8ln2bdrvd.narinfo | HTTP Error 404: Not Found |
| guix-2b6eee2e59 | https://ci.guix.gnu.org/agiylfh65q5vxzmxb0351xl8ln2bdrvd.narinfo | 200 |
| guix-1823ef372b | https://bordeaux.guix.gnu.org/g8yfyalaa2498vk0h77811hlwmq42w0a.narinfo | HTTP Error 404: Not Found |
| guix-1823ef372b | https://ci.guix.gnu.org/g8yfyalaa2498vk0h77811hlwmq42w0a.narinfo | 200 |
| guix-b54e286053 | https://bordeaux.guix.gnu.org/n6q9aywm8asqq6zaj9sfrcyxzmdzhs6m.narinfo | HTTP Error 404: Not Found |
| guix-b54e286053 | https://ci.guix.gnu.org/n6q9aywm8asqq6zaj9sfrcyxzmdzhs6m.narinfo | 200 |
| guix-060983918a | https://bordeaux.guix.gnu.org/x97clbjs37ar4ywqjykmgfqa5w03kizy.narinfo | HTTP Error 404: Not Found |
| guix-060983918a | https://ci.guix.gnu.org/x97clbjs37ar4ywqjykmgfqa5w03kizy.narinfo | 200 |

A substitute reference list alone would not prove that the actual executing loader retains the matching source on its fallback search path. Without an exact loader/source mapping these rows remain factual unknowns, not additional confirmed instances.

All seven successful responses have an empty `References:` field, and identify only a derivation name, sizes/hashes, signature and download locations. Responses are saved under `A1/review/raw/narinfo/`. Empty references establish neither absence of source elsewhere nor availability of source on a runtime load path. No source-loader mapping can be extracted from these metadata.

A whole-file search for the seven exact hashes in `A1/in/raw/guix/` and `(not published: adjudication scratch)` found matches only in `../in/raw/guix/group-members.json`, `store-top-level.txt`, and `system-closure.txt`. These enumerate paths; they contain no corresponding derivation or loader records.

For guix-2b6eee2e59 (`agiylfh65q5vxzmxb0351xl8ln2bdrvd`), `NarSize: 96` is also a reason not to infer executable compiled content from the store name alone. This metadata does not enumerate any module. The unresolved exact extent is a limitation of the saved object evidence, not a reason to assign all seven rows to the hole.

## Exact empty output verified

The sole additional artifact retrieval was the 69-byte zstd stream at `https://ci.guix.gnu.org/nar/zstd/agiylfh65q5vxzmxb0351xl8ln2bdrvd-module-import-compiled`, bounded to 1024 bytes. It expands to 96 bytes, matching NarSize. SHA-256 in the advertised base32 encoding is `0sjjj9z1dhilhpc8pq4154czrb79z9cm044jvn75kxcjv6v5l2m5`, matching the saved narinfo.

Decoded NAR strings: `nix-archive-1`, `(`, `type`, `directory`, `)`. There are no directory entries and no code files. Exact bytes are saved as `A1/review/raw/narinfo/agiylfh65q5vxzmxb0351xl8ln2bdrvd.nar`. Therefore guix-2b6eee2e59 is FACT-WRONG as a compiled-code/cache instance and is excluded; six other exact module-import-compiled rows remain factually unknown. This was static artifact inspection, not execution or a behavioural probe.
