# Exact public radio fixture inputs

Copied from the successful renderer test in a private sealed35 derivative. These
are intentionally public simulated keys, not real network/device credentials.

Keep these inputs beside the declaration. Append `packages.conf` and
`radio-draft.conf` to the base/snapshot/account lines for the source release being
built. Those radio kinds are still proposed: production currently rejects them.
The renderer test used snapshot20261123T000000Z plus its security20261124 lock.

`SHA256SUMS` covers the original source inputs and fragments. The two `.info`
files contain native negotiated type5 bonds; no startup generation is needed.
`fixture.json` records both simulated radios/AP settings; `client.json` records
the saved client. Both opposite pairing rows are explicit. Remove a client/pair
row to remove only its contribution; keep the fixture to retain AP/controllers.

The pure `radio_declaration.derive()` reads `radio-draft.conf` here and reproduces
the native config bytes tested in `RADIO-RENDERED-RESULTS.md`.
