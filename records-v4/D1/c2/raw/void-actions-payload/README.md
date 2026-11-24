# Fixed action inputs

Prepared from documentation and primary source code on 2026-11-23 UTC. This task has no machines. The six entry scripts and their shared helpers are inputs for C1-REH, not successful execution records. No hypothesis outcome is assigned here.

The binding sources are TEXT.md Section 9.2 and PROTOCOL.md Section 5. The previous input record's explicit commands and disclosures were used as the record format. The previous A3/BUILD.md was used only to avoid repeating tools when alternatives exist. Neither file was used to infer contents of these clean machines. In particular, `tree` is fixed by name before seeing any guest inventory and is not replaced if already installed.

| Entry script | Base | Actions | Description and sources |
|---|---|---:|---|
| `alma.sh` | Clean AlmaLinux | 9 | `ordinary.md` |
| `void.sh` | Clean Void Linux, glibc, runit | 9 | `ordinary.md` |
| `gentoo.sh` | Clean Gentoo, OpenRC user-service support | 9 | `ordinary.md` |
| `lived-developer.sh` | Previous clean Fedora Workstation installation | 13 | `lived-developer.md` |
| `lived-gaming.sh` | Previous clean Linux Mint Cinnamon installation | 9 | `lived-gaming.md` |
| `lived-server.sh` | Debian stable amd64 cloud image | 13 | `lived-server.md` |

No action script is supplied for MicroOS or Talos. The three lived-in machines are beyond the plan, separate from the outcome of check 1.

## Invocation contract

Copy this directory into each disposable guest. Run exactly one entry script there with Bash as the ordinary account **user**. Administrator operations go through `sudo`: use the account's existing noninteractive authorization, or provide `CAL_SUDO_PASSWORD` in the guest process environment for that disposable account. The scripts do not grant user blanket new sudo privileges or use a host secret. Never enable shell tracing around credentials.

For example, inside the disposable AlmaLinux guest: `bash alma.sh`. `bash alma.sh --list` prints only the fixed function names and limits. It performs no action and is safe for inspecting these inputs. `--action` is an internal timeout dispatcher, not the rehearsal entry point. All shell helpers must travel with the scripts; `firefox-addon.py` is required for AlmaLinux/Void, and `gentoo-firefox-addon.py` for Gentoo.

Preconditions: x86-64 guests, working time/TLS/DNS/Internet, Bash, GNU coreutils (`timeout`), sudo, and a writable home. Ordinary graphical/session software needs a login-created session bus. AlmaLinux and Fedora require a working systemd user manager; Gentoo requires current OpenRC user services; its action creates the user runtime and default runlevel directories if absent. Void's user supervisor is installed by its action. Mint requires its existing Cinnamon X11 and audio session. No private accounts or real user data are supplied.

The ordinary network action requires a second virtual Ethernet NIC with MAC **<MAC>**, attached to a DHCP network. The primary NIC also uses DHCP on clean Void/Gentoo installations. Void migrates its primary connection to NetworkManager; Gentoo uses installed dhcpcd on the secondary NIC only. On Void, conflicting runit network services are stopped and disabled as its handbook prescribes. Gentoo preserves the primary networking services and disables route/DNS/hostname hooks in its secondary configuration. This can briefly interrupt the transport. C1-REH must launch the guest job through a durable guest session/service before this action. This is part of the disclosed network action, not an undisclosed change to the clean backing image. The second profile never supplies a default route. `cal-test` Wi-Fi is saved without activation or any radio on the NetworkManager implementations; the Gentoo replacement makes the actual secondary Ethernet connection without a Wi-Fi profile.

Gentoo preserves its prepared Portage profile and default USE flags. Native prerequisites build from source with `--noreplace`; no action accepts license changes or unmasks packages. The repaired actions use a pinned self-contained application package, Python/pip cowsay, native OpenRC user services, and dhcpcd secondary networking. The reasons, sources, and thirty-minute repair window are recorded in (not published: record outside this collection). Package/service limits are 600 seconds and browser automation 420; a compiling clone holds four slots under COMMON.md.

## Status and limits

`lib.sh` dispatches each action in a new `bash` under GNU `timeout`, with `errexit`, `nounset`, and `pipefail`. It does not invoke action functions as a conditional test, which would suppress Bash's errexit. A failure aborts that function and the outer runner continues the fixed list. Timeout sends TERM and allows at most 30 further seconds before KILL. Each script defines its limits explicitly in seconds; package operations and builds are bounded together with their action.

(not published: record outside this collection) contains no header and exactly these fields: **function name, exit status, elapsed whole seconds**. Status 0 means the function completed; 124 is a timeout, and forced termination may produce 137. The overall script returns 1 if any action failed. The runner refuses to overwrite an existing status file, so a second attempt requires a fresh disposable clone, not deletion of prior evidence. A lost/rebooted machine can leave a partial file; a missing row is incomplete execution, never success. Per-action output goes to (not published: record outside this collection) for the rehearsal; the runner never prints password contents.

Long-lived guest services are launched through the guest service/container managers. Their continued presence is intended inventory material. Installer state, language caches, user files and application data inside the guest are also intended. Temporary download/extraction files are removed where appropriate. No action is run, installed or downloaded on the host by this preparation task.

The lists are fixed here. C1-REH may replace an action that cannot run unattended only with a disclosed reason; package versions, network availability and installer behavior are not asserted as observations here. Commit the complete input set before the first inventory under Appendix A.4.1. Independent acceptance and machine rehearsal are outside this preparation result; local syntax checks are not their substitute.

## Shared command sources

- [GNU Bash](https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin): `-e`, `-u`, `pipefail`, functions, traps and here-documents.
- [GNU timeout](https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html): “Start command, and kill it if still running after duration.”
- [sudo](https://www.sudo.ws/docs/man/sudo.man/): `-n` requests noninteractive operation; `-S` obtains authentication on standard input.
- [GNU install](https://www.gnu.org/software/coreutils/manual/html_node/install-invocation.html): “Copy files and set attributes.” `install_root_file` uses `install -D -m` on a temporary file, so sudo authentication cannot consume file contents.
- [curl](https://curl.se/docs/manpage.html): fail on HTTP errors, follow redirects, select output and bound transfers.
- [Python urllib](https://docs.python.org/3/library/urllib.request.html), [hashlib](https://docs.python.org/3/library/hashlib.html), and [json](https://docs.python.org/3/library/json.html) cover the small Firefox download/metadata helper. This helper calls the browser installer rather than unpacking an extension into its profile.

All ordinary shell file operations are explicit in the scripts. Each nontrivial application command has a URL next to its implementation and/or in the corresponding action table.
