# Finding 5: source provenance

Recorded 2026-11-22 UTC. No experiment was run and no frozen file was changed. The new records contain source retrieval metadata, hashes, and a source comparison.

| Saved source | Verified upstream version and URL | Full-file SHA-256 |
|---|---|---|
| `(not published: adjudication scratch)` | Guile **3.0.10**, [`libguile/load.c` at v3.0.10](https://cgit.git.savannah.gnu.org/cgit/guile.git/plain/libguile/load.c?h=v3.0.10); independently identical to that member of the [official 3.0.10 release archive](https://ftp.gnu.org/gnu/guile/guile-3.0.10.tar.xz) | `2eb1c9b82634f99276f848a3220360ef2ef6af74088e4b660dbfc03ade6657ae` |
| `(not published: adjudication scratch)` | Guix [`guix/self.scm` at commit **82df357bb2b40f4053534e8fb5697daae47f3b60**](https://codeberg.org/guix/guix/raw/commit/82df357bb2b40f4053534e8fb5697daae47f3b60/guix/self.scm) | `4cf00c3a27039f0604e232e4bfcb33cd79b95d631a25d21142ab7f824badd044` |

Both pinned upstream responses are byte-for-byte identical to the corresponding saved files: `raw/provenance/guile-cgit-lookup.json`, `raw/provenance/guile-release-lookup.json`, and `raw/provenance/guix-pinned-lookup.json`. The Guile source has 42,569 bytes; the Guix source has 61,135 bytes. `raw/provenance/guix-api-history.json` identifies the matching Guix file revision as the commit with subject “self: Link with libgc.”, dated 2026-02-24 00:17:45 UTC. A commit identifier is used instead of inventing a release label for that development revision.

The original download URL and original checkout commit cannot be recovered from the saved fetch script or its `dl/*.list` files: neither source is listed. `(not published: adjudication scratch):58` already labels the Guile source v3.0.10. These checks establish content identity with pinned upstream versions, not the historical route of the original download or uniqueness of a matching commit. The unpinned Savannah URL `https://cgit.git.savannah.gnu.org/cgit/guix.git/plain/guix/self.scm` also returned identical content (`raw/provenance/guix-savannah-lookup.json`); that moving URL is not used as the version identifier. Failed lookup attempts remain in the same raw directory.

## Relation to the inventoried system

`A1/in/raw/guix/guix-system-description.txt:7-12` and `A1/in/raw/guix/home-description.txt:4-8` identify the system/home channel commit as **d58da8a56b75af73a7b5466f7ef8a81679713aa3**. The system description labels its system GNU Guix 1.5.0. This does **not** make the saved `guix-self.scm` a source file from that release/revision.

The [file at the inventoried channel revision](https://codeberg.org/guix/guix/raw/commit/d58da8a56b75af73a7b5466f7ef8a81679713aa3/guix/self.scm) has 60,812 bytes and SHA-256 `5e4852dbc153f94d16669fd8c373c355e49e50a3bcebc04f18b627e3dd17fbfc` (`raw/provenance/guix-codeberg-lookup.json`). The complete comparison is `raw/provenance/guix-system-revision.diff`: the saved file adds a libgc package lookup, its definition, and linker arguments for the Guile launcher. The node source/compiled pairing, bundle links, built-modules union with `#:copy? #t`, and runtime module paths cited for hole 2 are unchanged. Saved-file line numbers after those additions are eight lines higher than their system-revision equivalents (for example saved line 1104 is system-revision line 1096).

Disposition: **fixed** for the requested upstream and version attribution, with the historical-download limitation explicitly retained. No source version is silently equated to the installed system; no new definition rule or failure condition is introduced.
