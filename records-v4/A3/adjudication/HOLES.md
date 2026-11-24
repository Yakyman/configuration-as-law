# A3 adjudication: gap cards

Seven gaps. Every GAP row of `rows.tsv` names one card in its `hole` column. Row counts come from `rows.tsv`. Example ids are rows of (not published: over 20 MB). Sentence quotes are exact text from `TEXT.md` (checked with (not published: orchestration or scratch)). Documentation and file evidence is listed under each card.

## Card 1. Self-managing clients: files that a program installs, and deletes, for itself

**The gap.** A client program that is itself an installer (Steam installs and removes games; juliaup installs and removes Julia versions) also downloads, installs and replaces its own files. Steam can also delete those files, but only in a reset that reinstalls them; juliaup can uninstall itself. The text does not say whether the program's own files are then "what an installer installs and removes as a whole". It also does not say whether self-installation is the part of the program's functionality that counts as an installer.

**Sentences.**
- S8.1-4 «Installer—a program of the system whose purpose, according to its documentation, includes installing and removing programs: the system package manager, package managers of programming languages and of application packages.»
- S8.1-5 «A general-purpose program with a built-in installer counts as an installer in that part of its functionality.»
- S8.1-6 «Package—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.»
- S8.2-7 «Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?»

**Facts.**
- The Steam action log (`A3/in/operator/gaming/actions-logs/actions-logs/gaming_store_runtime.log`) shows the client's own updater at work: "Downloading update (504,927 of 504,927 KB)", "Extracting package...", "Installing update...". Kernel ctimes of the files fall in that window.
- The Debian `steam/purge` note in (not published: record outside selected evidence) (copy in (not published: record outside selected evidence)) says: "Purging is not entirely complete. Steam's working files are still located in your home directories at ~/.steam. If you intended to remove the entire application, you will need to remove those directories manually."
- Valve's (not published: downloaded distribution package metadata or sources) from the official bootstrap ((not published: record outside selected evidence), checksums in `SHA256SUMS`) defines `reset_steam`, which is run by `--reset`. It moves aside `bootstrap.tar.xz ssfn* SteamApps steamapps userdata package`, runs `rm -rf "$STEAMROOT/"*`, and then reinstalls the bootstrap ("Reset complete!").
- juliaup has `self update` and `self uninstall` commands. Sources: the juliaup README at https://docs.rs/crate/juliaup/1.19.8/source/README.md and the source file `command_selfuninstall.rs` at https://docs.rs/crate/juliaup/1.20.1/source/src/command_selfuninstall.rs.

**Two decisions.**
- **INSTALLED-PACKAGE.** The client is a package of its own installer. Its unchanged files are covered by the client's line, and a removed line removes them.
- **Not a package.** Code becomes PROGRAM-OWN, with a line of its own for each program. Data and directories become RECORD (written by the updater as it ran), which need not be recorded at all.

The declarations differ in whether ~14,800 Steam runtime and client files need any line, and in which line covers the code.

**Examples.**

| id | name | what it is |
|---|---|---|
| gaming-cfd36e0732b4def2d5ecaf69 | /home/user/.steam/debian-installation/controller_base/images/api/knockout/shared_mouse_4.svg | Steam client image resource |
| gaming-820d8fed19aa17b72181a2d7 | …/steamrt64/pv-runtime/…/files/share/i18n/locales/uz_UZ@cyrillic | locale file of the Steam runtime |
| gaming-495169019fec2fb328ec9636 | /home/user/.steam/debian-installation/bin/hardwareupdater | Steam client helper group |
| gaming-1fd35bf6b4019193bad37621 | /home/user/.steam/debian-installation/ubuntu12_32/steam-runtime.old | previous Steam runtime kept by the updater |
| gaming-4cf3d1cb3da5181824cbdf16 | /home/user/.steam/debian-installation | Steam root directory |
| gaming-5e400a5875aa136f688db7de | /home/user/.steam/debian-installation/steamui/sounds | Steam UI sounds |
| developer-cbe2f19f976b603f5bb42193 | /home/user/.juliaup/bin/juliaup | juliaup binary (self-updating, self-uninstalling) |

**Rows: 14856** (gaming 14851, developer 5).

## Card 2. Repository history fetched by git at a person's command

**The gap.** `git clone` and the Homebrew install script fetch repository objects and references into `.git` at a person's command. The fourth question gives two descriptions that both fit these objects: something a program recorded as it ran ("history"), and something a person brought ("projects, downloaded files"). It does not say which one prevails.

**Sentences.**
- S8.2-15 «Otherwise: if a program recorded the object as it ran, it is a program record—a log, cache, history, working state» … «if a person created or brought the object, it is material—documents, photographs, projects, downloaded files»

**Two decisions.** RECORD (c1) or MATERIAL (c2). Neither needs a line, so the declarations do not differ. What differs is which group the object falls into under Section 8.5, which leaves the handling of records and material to the system.

**Examples.**

| id | name | what it is |
|---|---|---|
| developer-216b547047e9bd323ef8a31b | /home/linuxbrew/.linuxbrew/Homebrew/.git/objects/3d | git object directory of the Homebrew checkout |
| developer-6bf67733481480cdeaa37d0c | /home/linuxbrew/.linuxbrew/Homebrew/.git/refs/tags | tag references of the Homebrew checkout |
| developer-4fbf65b1725f19d2f17c9c20 | /home/linuxbrew/.linuxbrew/Homebrew/.git/objects/info | object-store metadata |
| developer-05617e28292b94b182cc73aa | /home/linuxbrew/.linuxbrew/Homebrew/.git/objects/45 | git object directory |

The scc clone's `.git/objects` and `.git/refs` rows fall in the same case.

**Rows: 84** (developer).

## Card 3. Container images and containers: is a container engine an installer?

**The gap.** Docker pulls images or builds them, and removes them as a whole. Containers run the programs those images hold. The text does not say whether a container engine is an installer whose images are packages: its documentation describes building, shipping and running containers, not "installing programs". So it cannot be told whether question 1 or question 2 decides.

**Sentences.**
- S8.1-4 «Installer—a program of the system whose purpose, according to its documentation, includes installing and removing programs: the system package manager, package managers of programming languages and of application packages.»
- S8.1-6 «Package—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.»
- S8.2-22 «A program that runs as its own process on the computer, including in a container, is a program.»

**Two decisions.** INSTALLED-OWN or INSTALLED-DERIVED (the image is a package; a compose file or Dockerfile would be the line it comes from), or PROGRAM-OWN or PROGRAM-DERIVED (the image is code run through Docker). The declarations differ in whether the image is recorded as a package of an installer or as a program with its own line.

**Examples.**

| id | name | what it is |
|---|---|---|
| server-fc8e0ac75ce9ed64a08ff655 | sha256:003a9780… | caddy:2-alpine image pulled for a compose project |
| server-46f5ba6815bb94894157236c | sha256:f9cf3e1f… | postgres:17-alpine image pulled for compose |
| server-bce2d2fe9dfb24c822a93809 | sha256:20068979… | traefik/whoami image pulled for compose |
| developer-78e8326714450972e0134fb6 | sha256:92f46737… | locally built image cal-development-web:local |
| developer-59a4ddfe60a8a1b18f6627c9 | 09c141f3… | container running busybox httpd, restart unless-stopped |
| developer-ffcb51cbd136cf2f6e7408cf | /var/lib/containerd | containerd content store holding image layers |
| developer-fd23729ab637faddccc1bc3e | /var/lib/docker | Docker engine data: containers, networks, build state |

**Rows: 7** (developer 4, server 3).

## Card 4. Package contents held in an installer's cache

**The gap.** Language installers download whole packages into a cache and keep them there: `go mod download` extracts modules into the module cache, bun keeps package contents in its global cache, uv keeps unpacked wheels, RubyGems keeps the gem archive. Each package is installed into the cache as a whole, but it is removed only together with the entire cache (`go clean -modcache`, clearing the bun or uv cache). The text does not say whether such a cached package is "what an installer installs and removes as a whole", or a cache the program recorded as it ran.

**Sentences.**
- S8.1-6 «Package—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.»
- S8.2-7 «Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?»
- S8.2-15 «Otherwise: if a program recorded the object as it ran, it is a program record—a log, cache, history, working state»

**Two decisions.**
- **A package.** The cached files are INSTALLED, recorded by an own or derived line.
- **A cache.** Code becomes PROGRAM-OWN or PROGRAM-DERIVED (c2 for Go module source and bun code), and the rest RECORD.

The declarations differ in whether some 1,300 cached module and package trees must appear in the declaration and under which line.

**Examples.**

| id | name | what it is |
|---|---|---|
| developer-28b0928f32a3bd540164f5c2 | …/scc/.cal-modcache/github.com/cloudflare/circl@v1.6.3/ot/simot | Go module source in the module cache |
| developer-4bc7e8a9213ac909292c2e0a | …/scc/.cal-modcache/github.com/go-git/go-billy/v5@v5.9.0 | extracted Go module root |
| developer-9e6d06f152c07e5c13f841e0 | …/scc/.cal-modcache/github.com/go-git/go-git | module path directory in the cache |
| developer-880c223d69d1d6670ff0f5f3 | /home/user/.bun/install/cache/hookified | bun cache entry for a package |
| developer-b8d0d1ff228a2993234f695a | /home/user/.bun/install/cache/yocto-queue@0.1.0@@@1 | bun cached package contents |

The uv `archive-v0` entries and the lefthook gem archive in the RubyGems cache fall in the same case.

**Rows: 1336** (developer).

## Card 5. Code that an installed program copies or generates as it runs

**The gap.** Some code is copied or generated by an installed program, rather than by a built-in tool or by a package's maintainer scripts: wineboot fills a Wine prefix with Windows code copied from the wine packages; git clone copies the sample hooks from git's templates; RubyGems writes a wrapper script and gemspec; juliaup writes shell completion code; k3s extracts tools from its own binary. The third line form covers what "the system itself built or obtained", but the text does not say whether an installed program running at a person's command is "the system itself".

**Sentences.**
- S8.2-16 «What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.»
- S8.1-7 «Built-in tool—a program of the system whose purpose, according to its documentation, includes changing what is installed and settings: an installer, account and rights management, the service manager, network and access rule configuration.»

**Two decisions.** PROGRAM-DERIVED (covered by the line of the source package or tool) or PROGRAM-OWN (each copy needs a line of its own). The declarations differ in whether hundreds of prefix DLLs, hook samples and extracted tools need their own lines.

**Examples.**

| id | name | what it is |
|---|---|---|
| gaming-85b507e7ce1d3c2a16693bb3 | /home/user/Games/wine-tools/drive_c/windows/rundll.exe | Wine module created in the prefix by wineboot |
| gaming-542ab2b7a1cac1d1e2d23e7f | …/drive_c/windows/system32/wbem | Wine prefix code copies |
| gaming-fe91919b6bab6568dfdea112 | …/drive_c/windows/syswow64 | 813 prefix members, code copies and records |
| developer-3bcbeded8b7cf5aedc1382fb | /home/user/Projects/scc/.git/hooks/applypatch-msg.sample | executable sample hook copied by git clone |
| developer-bc1494f6f41c4c0f3175eb8c | /home/user/bin/lefthook | Ruby wrapper generated by RubyGems |
| developer-35549cad55c96268fcaf4f24 | /home/user/.julia/juliaup/completions | bash completion code generated by juliaup |
| server-be5afc83ca654a448cd1fb60 | /var/lib/rancher/k3s/data/cni | tools k3s extracted from its own binary |

**Rows: 285** (gaming 263, developer 19, server 3).

## Card 6. Values the computer obeys that a program generated rather than a person chose

**The gap.** Some values that the computer obeys were written by a running program, not chosen by a person and not created during package installation. Examples: the firewall zone and policy dockerd writes at first start; resource drop-ins systemd writes for user slices; the certificates, tokens, kubeconfig, manifests and containerd/kubelet configuration k3s generates; the sound server's authentication cookie. They are of the kinds the text lists as settings (access rules, rights, services and their parameters, values that grant access). But the third question asks for "a value chosen by a person", and the text does not say which condition prevails.

**Sentences.**
- S8.2-11 «Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?»
- S8.2-12 «Then it is a setting, however it was entered and whatever file stores it.»
- S8.2-13 «Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.»
- S8.2-14 «A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.»

**Two decisions.** A SETTING (SETTING-OWN or SETTING-DEFAULT; recorded) or RECORD (written by a program as it ran; need not be recorded). The declarations differ in whether generated access rules, credentials and cluster manifests must be recorded.

**Examples.**

| id | name | what it is |
|---|---|---|
| developer-70be1c323890746c1a78c6f5 | /etc/firewalld/policies | firewall policy written by dockerd at first start |
| developer-342e1a9fd229e3473b8c35b3 | /etc/systemd/system.control/user-1000.slice.d | resource drop-ins written by systemd |
| server-c6809ad0393bc02f2943127a | /var/lib/rancher/k3s/server/cred | credentials generated by k3s |
| server-ddd20eb86c2fac35aad9742a | /etc/rancher/node | node password generated by k3s |
| server-0a575e792deb53a2ae502487 | /var/lib/rancher/k3s/server/manifests/metrics-server | manifests k3s writes and applies |
| server-7bf44e4e4a03c100b6ad395a | /var/lib/rancher/k3s/agent | generated agent configuration and certificates |
| server-034bd74a045c24aa6dd19160 | /var/lib/rancher/k3s/server/db | cluster datastore: person's workload plus k3s state |

Also in this case: gaming-1ba8cee6c38131f0b6c75952, `/home/user/.config/pulse`, the sound server authentication cookie.

**Rows: 27** (server 20, developer 6, gaming 1).

## Card 7. Value files whose entries include commands that are run

**The gap.** Some files are read by a program as values, but contain command lines that the program hands to a shell or executes: a `cron.d` entry, the `run:` command of `lefthook.yml`, the instructions of a Dockerfile. The text separates files "executed as code" from files "only read as values", but does not say which side a file falls on when only some of its entries are executed.

**Sentences.**
- S8.2-23 «A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.»
- S8.2-9 «Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?»

**Two decisions.** PROGRAM-OWN (code) or SETTING-OWN (values that launch something). Both are recorded by an own line. The declarations differ in whether the file is recorded as a program or as a setting.

**Examples.**

| id | name | what it is |
|---|---|---|
| server-c354536d6d9a738329571706 | /etc/cron.d | person's cron.d file whose command field cron runs through /bin/sh |
| developer-e56b4f802a20335d455ecb3a | /home/user/Projects/scc | project directory holding lefthook.yml with a run: command |
| developer-d916e8927ebf41371ab8dd1d | /home/user/Projects/development-web | directory holding the person's Dockerfile |

**Rows: 3** (developer 2, server 1).
