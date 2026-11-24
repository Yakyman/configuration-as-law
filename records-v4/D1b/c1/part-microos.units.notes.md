# Unit-file classification rule

Scope: 260 system and user unit-file inventory rows. No other classification was read.

Rule U1: Resolve the inventory unit through s4-microos-unit-selected.tsv. The selected fragment, and every selected drop-in/source file, must have an exact package-files.tsv comparison of unchanged and an installed supplying package in objects.tsv. Then S8.2-6, S8.2-7 and S8.2-8 answer question 1 affirmatively; S8.2-16 covers this installed file with its supplying package line. All 260 meet this predicate. Package installation reason does not change coverage of files obtained with that package; the package object's own recording is a separate question. Disabled/static/template files remain installed files. No inference about human choice from enablement or preset equality is made.

The objects are the listed unit definitions, not the enabled-state value or the running process. Current selected fragment resolution avoids inferring the selected source from a basename. Multiple identical property records for aliases are checked for the same fragment; drop-ins are checked separately.

Documentation: https://www.freedesktop.org/software/systemd/man/latest/systemctl.html describes list-unit-files as listing installed unit files and distinguishes it from list-units. Exact excerpt: “Use list-unit-files (see below) for listing installed unit template files.”

https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html describes unit files as INI-style configuration and alias resolution through symbolic links. Exact excerpt: “Units can be aliased (have an alternative name), by creating a symlink”.

Facts: D1b/handoff/microos/s4-microos-unit-selected.tsv, package-files.tsv, objects.tsv and s4-microos-sources.tsv. Saved query evidence is retained in those tables. Current source inspection confirms configuration definitions and purposes. Selected definitions and drop-ins are supplied installed package files; none is a transient /run fragment.

## Manual checks of U1

Ten spread rows were manually inspected: current source bytes decoded from s4-microos-sources.tsv, selected-fragment join and unchanged package comparison.

- d1b-microos-f06da3a3f0ee84b03de126f4: `/usr/lib/systemd/system/audit-rules.service`; Load Audit Rules; exact package comparison unchanged.
- d1b-microos-bbe5442b300f188f6536bdbf: `/usr/lib/systemd/system/getty@.service`; Getty on %I; exact package comparison unchanged.
- d1b-microos-01ced4baf08a723b7b2cf763: `/usr/lib/systemd/system/dbus-broker.service`; D-Bus System Message Bus; exact package comparison unchanged.
- d1b-microos-c4de4b827444bfd8498705d1: `/usr/lib/systemd/system/kmod-static-nodes.service`; Create List of Static Device Nodes; exact package comparison unchanged.
- d1b-microos-c1c3fd6d4026c63cd01265b8: `/usr/lib/systemd/system/rebootmgr.service`; Reboot Manager; exact package comparison unchanged.
- d1b-microos-a48c334856edc21e74e0390b: `/usr/lib/systemd/system/systemd-cryptenroll-firstboot.service`; Interactive Disk Encryption Setup; exact package comparison unchanged.
- d1b-microos-51ba25f6baed0c3ea96f3560: `/usr/lib/systemd/system/systemd-nspawn@.service`; Container %i; exact package comparison unchanged.
- d1b-microos-4a8f2301293beff583e02304: `/usr/lib/systemd/system/systemd-timedated.service`; Time & Date Service; exact package comparison unchanged.
- d1b-microos-0cc14b5799a7a76099c6e6b6: `/usr/lib/systemd/system/fstrim.timer`; Discard unused filesystem blocks once a week; exact package comparison unchanged.
- d1b-microos-265cccefa2e7dd3d604bb488: `/usr/lib/systemd/user/systemd-tmpfiles-clean.timer`; Daily Cleanup of User's Temporary Directories; exact package comparison unchanged.

All selected additional drop-ins are also unchanged package files, including user@.service, dbus-broker, logind, ignition-delete-config, remount-fs, sysctl and udevd. No gap rows. Output IDs and field word limits were verified by the accompanying script.
