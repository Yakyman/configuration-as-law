# Documentation excerpts for fix round 1

Accessed 2026-11-23 UTC. Public documentation only; no command from a documentation page was executed. Short verbatim excerpts follow. These document functionality, not the historical integrity of any inventoried file.

| Source | Exact excerpt | Use and limit |
|---|---|---|
| [Homebrew FAQ](https://docs.brew.sh/FAQ#how-do-i-uninstall-homebrew) | “To uninstall Homebrew, run the uninstall script from the Homebrew/install repository.” | Self-removal is documented. |
| [Homebrew manual, update](https://docs.brew.sh/Manpage#update-up-options) | “Fetch the newest version of Homebrew and all formulae from GitHub using git(1) and perform any necessary migrations.” | Repository updates are documented; this is not a received-content comparison. |
| [Homebrew uninstall source](https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh), lines 322–324 | `elif [[ "${HOMEBREW_REPOSITORY}" == "${HOMEBREW_PREFIX}/Homebrew" ]]` … `sudo_removal_paths+=("${HOMEBREW_REPOSITORY}")` | The repository is a removal target in the layout observed. The source was read, never executed. |
| [Docker pull](https://docs.docker.com/reference/cli/docker/image/pull/) | “Download an image from a registry” | Establishes image download, not a definitive S8.1-4 installer classification. |
| [Docker image rm](https://docs.docker.com/reference/cli/docker/image/rm/) | “Removes (and un-tags) one or more images from the host node.” | Establishes removal; tags and image contents are distinct. Q1 remains FACT_UNKNOWN on this evidence. |
| [Go module reference](https://go.dev/ref/mod#go-mod-download) | “The go mod download command downloads the named modules into the module cache.” | The observed module-cache action is a download; the cache location alone does not establish Q1 installation. |
| [Bun global cache](https://bun.sh/docs/pm/global-cache) | “Once a package is downloaded into the cache, Bun still needs to copy those files into node_modules.” | Documentation distinguishes the download from installing into node_modules. |
| [uv caching](https://docs.astral.sh/uv/concepts/cache/) | “To clear the cache for a specific package, run uv cache clean <package-name>.” | Directly refutes whole-cache-only removal for uv, not for other tools. |
| [Docker firewalld integration](https://docs.docker.com/engine/network/packet-filtering-firewalls/#integration-with-firewalld) | “Docker creates a firewalld zone called docker, with target ACCEPT.”; “Docker also creates a forwarding policy called docker-forwarding” | These excerpts identify the automatically generated zone and policy observed in the saved inventory. |
| [Juliaup documentation](https://github.com/JuliaLang/juliaup#using-juliaup) | “juliaup self uninstall uninstalls Juliaup.” | Corroborates the saved installation log's self-uninstall instruction. The docs.rs URL could not be opened through the documentation tool; this is the upstream fallback. |

Markup around command names is omitted in the displayed excerpts; words are unchanged. The repository source is current documentation, not a claim that this exact revision ran during the recorded installation.
