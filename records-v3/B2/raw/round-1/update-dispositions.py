from pathlib import Path
p=Path('B2/STAND.md')
changes={
'C1.1':('NOT CLOSED','R02/R11: original repository backend mutations refuse; pinned declaration program install/update/remove works. Repository/base-system update through the declaration is still unimplemented; that implementation gap prevents full closure.'),
'C1.2':('CLOSED','R01–R03: root-only original package executables, helper/module/library trees, protected system databases and declaration-only sudo. Direct backend, copy, Python apt, native apt library and sudo bypasses refuse.'),
'C1.3':('NOT CLOSED','R02/R13: original --root/--admindir/extraction refuse, caches are private and retained native copies fail direct/loader execution. Arbitrary extraction followed by interpreter reads or another executable-memory route is not controlled by this mechanism.'),
'C1.4':('CLOSED','R02/R09: original installers cannot run caller hooks; arbitrary declared service hooks/root execution refuse admission. Valid local package postinst and apt hook/config attempts fail with no marker.'),
'C1.5':('CLOSED','R02/R03: mandatory backend DAC and fixed broker environment survive configuration and environment overrides; isolated Python ignores caller module/bus variables, sudo refuses environment preservation/assignment.'),
'C1.6':('NOT CLOSED','R13: caches/generations are root-only; copied native worker refuses direct/loader start after removal. Bytes copied while declared can still be passed to an interpreter; no general revocation of those bytes is built.'),
'C6.1':('CLOSED','R05/R06: supplied user manager is root-only and user@.service masked. Written units, drop-ins, templates and aliases are not honoured; private/user-manager and enable/start bypasses refuse. Declared jobs use protected system units with User=stand.'),
'C6.2':('CLOSED','R05: original CLI unavailable, system-manager D-Bus calls denied by sender policy/polkit; start, enable, reload, link and set-property tested both directly and through granted sudo.'),
'C6.3':('CLOSED','R05/R06: original systemd-run, user transient timer and StartTransientUnit API refuse. Declared timer/service lines retain a scheduling route.'),
'C6.4':('CLOSED','R07/R11: cron/at clients/daemons absent or private, services masked and spools root-only; crontab/@reboot/at/spool attempts fail. Declared timers are the supported scheduling route.'),
'C6.5':('NOT CLOSED','R06/R09: user unit/environment generators are not honoured and arbitrary unit hooks refuse. An admitted executable may itself interpret mutable command/configuration inputs; declaring ExecStart alone does not close that input route.'),
'C6.6':('NOT CLOSED','R11/R13 and repeated D06/D07: declared timer/service removal stops the finite fixture and rejects recreation via user/direct manager paths. Complete activation-edge and surviving-child/code revocation is not established.'),
'C10.1':('CLOSED','R01/R04/R05/R08: ordinary authority is restricted to declaration tools; direct account/package/service/network/Bluetooth/firewall clients, daemon APIs and native nft library mutation refuse. Host-held external operator root is outside this grant, as specified by BC1.'),
'C10.2':('CLOSED','R01/R09: no generic sudo shell, environment launcher or mount tool is granted; guard-changing backends are private and authority-bearing declaration injections refuse. The external operator can still deliberately break mechanisms.'),
'C10.3':('NOT CLOSED','R09/R12: arbitrary privileged hooks are refused and one live service mismatch restores the prior declaration. General multi-resource side-effect restoration, especially across daemon/device state, is not established.'),
'M1.01':('CLOSED','R09/R11: validation and root-only frozen preparation do not emit SUCCESS. A success report follows activation and every-line readback; invalid candidates leave the previous declaration selected. Live atomicity is separately M1.02.'),
'M1.02':('NOT CLOSED','R10–R12: all supplied tools now share nonblocking exclusion, and a live readback mismatch emits failure, never SUCCESS. Finite file/service/account/rule/profile readers do not establish complete live cross-resource/device semantics.'),
}
lines=[]
for line in p.read_text().splitlines():
 if line.startswith('| ') and ' — ' in line:
  ident=line.split()[1]
  if ident in changes:
   cols=line.split('|');status,why=changes[ident]
   line='|'+cols[1]+'|'+cols[2]+'| **'+status+'** — '+why+' [Round-1 evidence](SELFTEST.md). |'
 lines.append(line)
s='\n'.join(lines)+'\n'
s=s.replace('Attempt/evidence keys:', 'Round 1 closes 10 variants; 10 of 88 are CLOSED. R01–R14 refer to the round-1 SELFTEST table and its raw command IDs. Rows outside the 17-variant BC1 scope retain their earlier disposition.\n\nHistorical attempt/evidence keys:')
p.write_text(s)
