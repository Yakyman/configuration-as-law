# FX-B1-1 evidence addendum: findings 2 and 8

Recorded 2026-11-22 UTC. Role: research. Documentation/source review only; no experiment. This is not acceptance review. Original evidence remains unchanged.

## Finding 2: privileged extension implementation

**Recommendation: fixed by changing C8.07 to required, UNKNOWN.**

S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”

S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”

E-FX2 — [API Implementation Basics](https://firefox-source-docs.mozilla.org/toolkit/components/extensions/webextensions/basics.html), “The API Schema” and “Built-in versus Experimental APIs”: “implementation of a WebExtensions API runs with full chrome privileges”; “a special type of extension called a privileged extension”. The page identifies the implementation as JavaScript code and describes packaging an experimental API inside a privileged extension. Its sandboxed extension caller is a different object.

Inference: the card's privileged implementation is executable code even if it holds settings, and its own-rights execution requires recording. The previous effects-based answer does not defeat the explicit code classification. Remove the T2 TEXT-OPEN card rather than introduce a new priority rule. This does not classify every browser extension as own-rights code. The source describes installation/development and privileges, not complete declaration-bound admission, revocation, or closure of every privileged loading path. No such closure was established in the original evidence or this focused review: UNKNOWN, not NOT-CLOSABLE. Ordinary confined webpage browsing is not thereby lost.

## Finding 8: runtime network-port change

**Recommendation: add S2.2-15 to the shared requirement R, explicitly including C2, C3, C5, C7 and C9.2. Treat code admission and authority to open an unrecorded listening port as separate obligations within these existing channels.**

S2.2-15: “accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;”

A recorded script's unrecorded listener is not excused by recording the script. S2.3-4 and S2.3-6 apply to the port independently; no superuser action is needed for an ordinary unprivileged TCP port. This is the change route in the existing channels, not a new channel.

E-FX8a — [Linux 6.12 Landlock documentation](https://docs.kernel.org/6.12/userspace-api/landlock.html), network rules and `landlock_net_port_attr`: “Network rules (since ABI v4)”; “requesting to bind on port 0 is allowed”. A ruleset can handle TCP binding and grant only specified port numbers; ungranted handled actions are denied. Apply it before launching the confined process and its descendants; require the ABI instead of silently dropping this obligation on older/disabled kernels. Granting port zero authorizes automatic selection from the ephemeral range, so it must not be included in a fixed-port allowlist merely as a convenience. The 6.12 API covers TCP, not UDP. This establishes closure of explicit bind requests to denied TCP port numbers, not every listener route or full P2/Removal.

E-FX8b — [Linux v7.3 Landlock network source](https://raw.githubusercontent.com/torvalds/linux/v7.3/security/landlock/net.c), `landlock_hooks`:

```c
LSM_HOOK_INIT(socket_bind, hook_socket_bind),
LSM_HOOK_INIT(socket_connect, hook_socket_connect),
LSM_HOOK_INIT(socket_sendmsg, hook_socket_sendmsg),
```

These are its network hooks; there is no socket-listen hook. Source inspection also finds separate UDP bind/send rights and UDP automatic-binding checks in this newer source. Do not extrapolate the older TCP-only limit to this version, or assert that BIND_TCP covers UDP. This upstream tag is source evidence, not verification of the configured backport binary.

E-FX8c — [listen(2)](https://man7.org/linux/man-pages/man2/listen.2.html), EADDRINUSE: “had not previously been bound to an address” and “attempting to bind it to an ephemeral port”. Thus listen can itself allocate a local port when no explicit bind preceded it. Combined with E-FX8b, this is a documented alternative path that BIND_TCP alone does not establish as closed. Already-bound or already-listening inherited/transferred sockets likewise do not require a new explicit bind; a bind filter is not a revocation mechanism. This is a source-based inference about the claimed control's coverage, not a measured testbed result.

**Bounded verdict:** explicit runtime `bind` to a denied TCP port is CLOSABLE with Landlock's handled BIND_TCP right and no port-zero grant, at the cost of forbidding undeclared local server ports. **Whole runtime-listener route: UNKNOWN in this evidence set.** It additionally requires control of implicit listen binding, inherited/transferred sockets, relevant protocols, launch coverage and removal of old listeners. A deny-listen syscall policy is a candidate for non-server domains but was not established here as an integrated policy retaining declared server operation. No universal impossibility follows. Do not label an entire affected row CLOSABLE solely because code admission or explicit bind filtering is evidenced. If the inventory's rows include this runtime-change obligation, their full verdict must retain this UNKNOWN until complementary closure is evidenced.

No rerun was necessary: primary documentation and source resolve the narrow behavior questions. No failure condition or published sentence was changed.
