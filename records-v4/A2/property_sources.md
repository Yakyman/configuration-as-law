# Primary evidence for the property sweep

This is a beyond-plan textual examination, not an inventory, implementation experiment, weighting or published-check outcome. Source passages are quoted once here and referenced by identifier from PROPERTIES.tsv. All software objects below are documented real objects; declarations discussed alongside them are alternative readings of the hypothesis, not claims about existing implementations satisfying all its properties.

## PS1 — installation-created SSH host identity

URL: https://sources.debian.org/src/openssh/1:9.2p1-2%2Bdeb12u7/debian/openssh-server.postinst/

Passages: `ssh-keygen -q -f "$file" -N '' "$@"`; `"$hostkeys" /etc/ssh/ssh_host_ed25519_key -t ed25519`; `if [ "$action" = configure ]; then`; `create_keys`.

The create_key function runs only if the requested host-key file does not exist. The configure branch invokes create_keys. Thus installation, without manual modification, produces the real service's default Ed25519 host key.

## PS2 — the host key is used by the service

URL: https://man.openbsd.org/sshd_config.5#HostKey

Passage: “Specifies a file containing a private host key used by SSH.”

The directive's listed defaults include /etc/ssh/ssh_host_ed25519_key. The case concerns the service's identity parameter, not a private client key for logging in to another machine.

## PS3 — generation uses randomness

URL: https://raw.githubusercontent.com/openssh/openssh-portable/V_9_2_P1/ed25519.c

Passages: `randombytes(sk,32);`; `crypto_hash_sha512(az,sk,32);`

These adjacent statements occur in crypto_sign_ed25519_keypair. The secret seed bytes are filled at generation time; the installed package's source and version do not encode those bytes. The source is pinned to the upstream release corresponding to PS1.

## PS4 — enablement and execution differ

URL: https://www.freedesktop.org/software/systemd/man/latest/systemctl.html

Passage: “Note that this does not have the effect of also starting any of the units being enabled.”

The passage concerns enable. The disable explanation separately states that disabling does not implicitly stop the service. The same primary page documents user, runtime and system scopes and identifies systemctl as control of the service manager. It establishes real reachable enabled-but-stopped and disabled-but-running service states, without asserting that they defeat any conforming implementation.

## PS5 — persistent records survive an ordinary configuration change

URL: https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html

Passage: “Note that when this option is changed to "volatile", existing persistent data is not removed.”

This concerns Storage=. Persistent journal data is a real program record. Whether removal of those records should be implemented is expressly excluded by Section 8.5.

## PS6 — generated database configuration

URL: https://www.postgresql.org/docs/18/app-initdb.html

Passage: “The libc locale provider takes the locale settings from the environment, and determines the encoding from the locale settings.”

The page documents creation of an actual database cluster and default authentication rules. Locale defaults illustrate environmental input but do not establish a separate conflict: a fully specified declaration may already describe its environment, and service-parameter classification must be kept distinct from private database material.

## PS7 — suspension

URL: https://docs.kernel.org/admin-guide/pm/sleep-states.html

Passage: “Sleep states are global low-power states of the entire system in which user space code cannot be executed”

This is the opening clause of the kernel documentation's first sentence. It documents a normal system state, not privileged editing past the declaration. It supplies a boundary for 'can be started' and 'at any moment'; it does not establish that the intended meaning excludes resuming first.
