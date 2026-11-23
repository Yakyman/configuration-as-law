# Guix transport rehearsal

2026-11-23 UTC. Round 1 failed boot/login after 241.576 seconds. Its precise
cause is unknown because all serial output was discarded. Graceful destruction
also failed; kill and final destroy returned zero. No property query ran.

Source review shows that passive login sends no initial character. If a login
prompt was emitted before the console reader attached, no subsequent input
causes it to reappear. This is a possible transport failure, not an observed
guest diagnosis. The next runner permits one carriage return after ten seconds
without received data, still without sending an interrupt. It changes no guest
configuration. The agetty manual recognizes carriage return/line feed as end
of line and documents waiting for these characters before printing a prompt:
https://man7.org/linux/man-pages/man8/agetty.8.html .

Expected before round 2: a new clone boots, all twenty consecutive empty commands
return zero within their sixty-second bounds, and destroy or the documented
kill/destroy fallback removes the clone. Existing serial credentials remain
unchanged. No system contents are retained or read.

Round 2 also failed boot/login (242.767 s); the single carriage return did not
establish a repair. Before round 3, fixed numeric row counts were added for
serial login/password/shell prompt recognition, completed command frames and
fixed transport failure categories. No prompt text, command output, credentials
or console tail is retained. These counters distinguish an authentication-stage
failure from a framing-stage failure without exposing guest content. Round 3
still requires a new disposable clone and the original twenty-call criterion;
no outcome is presumed from the earlier preparation smoke test.
