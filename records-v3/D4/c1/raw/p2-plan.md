# P2 experiment: declared account group after application

Written 2026-11-22 UTC before either P2 run.
Sources examined: official NixOS 26.05 User Management section; Guix 1.5.0
User Accounts and Invoking guix system; upstream and installed usermod(8).
They document account modification and configuration application, but do not
record a successful application and its subsequent account state on these exact
clean installations. This is the outstanding combined temporal fact.

Expected in each system: application of its unchanged selected declaration
returns status 0; the account `user` initially has primary group `users` (100);
`usermod -g wheel user` succeeds and changes it to `wheel` (1), with declaration
hashes unchanged and without any intervening application. NixOS's evaluated
configuration confirms `users` and mutableUsers=true; Guix explicitly says
(group "users"). This would violate P2 after the last successful application.
One experiment per system; no retry after an observation. The command restores
the primary group at the end solely for cleanup. It writes no declaration and
uses no direct superuser file modification. Existing supplementary wheel access
is retained. A failed application would not establish the proposed P2 witness.
Commands and full output: p2-nixos.sh/.txt and p2-guix.sh/.txt.

Guix transport note, before the P2 attempt: `new` timed out and the read-only
inspection's shell wrapper failed with a syntax error before receiving the
script. No inspection or account mutation ran. The planned root P2 invocation
will still be attempted once through the unchanged runner; its first reads
will identify the selected version, declaration and account tools. It will not
proceed to account modification unless application itself reports status 0.
