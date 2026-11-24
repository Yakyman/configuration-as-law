# Documentation and source corrections, round 2

Accessed 2026-11-23 UTC. Public primary sources only; no documented command was executed. These are documentation facts, not received-content or historical-provenance measurements.

## Go: download storage and installation are explicitly distinct

[Go module reference, module-aware commands](https://go.dev/ref/mod#mod-commands) separately describes “downloaded dependencies (in `GOPATH/pkg/mod`” and “installed commands (in `GOPATH/bin`, unless `GOBIN` is set)”. [The installation subsection](https://go.dev/ref/mod#go-install) also states: “Non-executable packages are built and cached but not installed.” The same reference's module-cache section explains the `GOMODCACHE` override. These excerpts were read on the live reference page; formatting around identifiers is retained here.

Application: `check-inputs-v4/actions/lived-developer.sh` lines 72–76 set `GOMODCACHE` to the project's `.cal-modcache`, download modules there, then build a separate `scc` executable. The source comment on line 70 calls the dependencies installed in the cache; that comment is not the tool's documentation and cannot override the documented distinction. The original card's assertion that the cached module tree is itself the installed package is FACT-WRONG on this evidence. This does not establish each source member's executable capability, or make every Go cache an unconditionally resolved RECORD.

## Docker: purpose is documented; the remaining issue is a reading

[Docker overview](https://docs.docker.com/get-started/docker-overview) states: “Docker is an open platform for developing, shipping, and running applications.” Its containers subsection states: “A container is a runnable instance of an image.” The primary [documentation repository page](https://github.com/docker/docs/blob/main/content/get-started/docker-overview.md) was also returned by the documentation search with the same passages and the surrounding explanation of image building, pulling, deployment and container lifecycle. Direct opens of the overview and raw source returned 404; the excerpts here are from the search service's indexed primary-source text, not a claimed downloaded snapshot. The direct repository contents API also returned 404.

[Docker Engine overview](https://docs.docker.com/engine/) states: “Docker Engine is an open source containerization technology for building and containerizing your applications.” Its description assigns image/container lifecycle management to the daemon. [Image pull](https://docs.docker.com/reference/cli/docker/image/pull/) describes “Download an image from a registry”; [image removal](https://docs.docker.com/reference/cli/docker/image/rm/) describes “Removes (and un-tags) one or more images from the host node.” The latter two excerpts are retained from round 1.

These sources establish the purpose and operations. They do not explicitly separate an image download from a later program-installation destination as the Go and Bun documentation does. Whether those known Docker operations constitute installation/removal of programs under S8.1-4/6 is the unresolved reading; it is not a request for a missing inventory fact. The result retains both readings as card 3. This is not a claim that an exact keyword is required in documentation, or that every download is installation.

## Homebrew: immutable source reference replaces moving HEAD and incorrect lines

The current source was fetched read-only, with commit fixed before fetching its bytes:

- Commit: `c9c975046f78e6e6d662deb801bd461ebd6a54ed`.
- [Immutable uninstall source](https://github.com/Homebrew/install/blob/c9c975046f78e6e6d662deb801bd461ebd6a54ed/uninstall.sh#L340), relevant lines 340–342.
- Whole source SHA-256: `7e5576d1200bdf4fbd1fe38513f129139473ec39f04890ff5c7f1d05480af78a`.
- Saved exact excerpt with original line numbers, URL and checksum: [homebrew-source.json](homebrew-source.json).

Line 340 is `elif [[ "${HOMEBREW_REPOSITORY}" == "${HOMEBREW_PREFIX}/Homebrew" ]]`; line 342 is `sudo_removal_paths+=("${HOMEBREW_REPOSITORY}")`. Round 1's reference to lines 322–324 was wrong. Its historical record remains unmodified. The fixed source confirms the removal target; it does not prove that this revision ran during the inventory or that the inventoried metadata remains as received.

## Unchanged tool-specific evidence

Bun's explicit cache-to-installation distinction and uv's per-package cache removal remain in [round 1 documentation](../../fix-a3-h-1/raw/documentation.md). Bun's disposition is relabeled FACT-WRONG because its rejection addresses a factual installation premise. The Docker firewalld documentation in that file remains the basis for inferring generation of the two observed access-rule files. Both files also have `created=unknown` in the frozen origin table. Round 2 does not convert that inference into a measured origin or extend it to the 23 unresolved C6 candidates; the extent is now explicitly a lower bound.
