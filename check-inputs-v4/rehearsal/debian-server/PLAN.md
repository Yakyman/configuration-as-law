# Lived-in Debian server repair rehearsals

2026-11-23 UTC. This machine is outside the four checks under PROTOCOL.md
Section 5. The same thirteen activities in `actions/lived-server.sh` remain
selected. No action replacement or base choice is introduced.

Source review before the first new rehearsal: `actions/lived-server.md` gives
the exact primary references and passages for each activity. The entry script
uses Docker's documented Debian repository, Compose, K3s's stable installer,
Caddy validate/reload, PostgreSQL ON_ERROR_STOP, the pinned Node Exporter
release and checksum, and documented Debian/systemd administration tools.
The previous numerical record shows thirteen successful actions and collector
status zero; package integrity counts included directories. The shared repaired
collector now retains directory ownership outside the packaged-file integrity
denominator and verifies recorded symlink targets where available.

Expected before FX1: the thirteen original actions and twenty transport calls
return zero on a fresh throwaway clone. The collector returns zero, has L2
rows, and retains exact counts for package reason and packaged-file integrity.
The existing reason fraction was already above 90%; corrected file accounting
is expected to improve the integrity fraction. Readiness still requires both
fractions strictly above 90%, diagnosed/documented query limitations, and the
whole run below thirty minutes. Inventory, raw query stdout and member lists
remain unread and are deleted; only permitted diagnostics may inform repairs.

No VM is launched until the coordinating task authorizes the lived-in phase
after completing the check-4 transport phase. At most four new FX rounds are
allowed, stopping early only if readiness is established. Each clone is removed
when its round completes.
