# SPDX-License-Identifier: MIT
"""Generate bindings/commands-0.70.json: tokens, per-variant native commands and probes.

Usage: python3 -I tools/make_commands.py [--interface FILE --executors FILE --base-conf FILE]
The optional files are the release's INTERFACE.md, EXECUTORS.md and base.conf; their
SHA-256 values are recorded. A variant whose facility does not exist in 0.70 is
'unsupported' with the reason; it yields an unobserved row, never a refusal.

Probe protocol (every shell probe below): exit 0 = the effect/thing is present,
exit 1 = it is absent, any other status = it could not be observed (unobserved).
Commands run as `sh -c TEXT` over SSH with CASE_MARKER=<unique guest path>.
Material named by put-material steps is already at its target.
"""
import argparse, hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / 'bindings' / 'commands-0.70.json'
H = '/home/user'
C = '/home/user/control'
MARK = 'test -s "$CASE_MARKER"'
FETCH = 'case_fetch() { curl -fsSL -o "$2" -- "$1"; }'


def un(reason):
    return {'unsupported': reason}


def cov(other):
    return {'covered_by': other}


def v(command, role='user', note='', **tokens):
    d = {'steps': {'attempt': {'command': command, 'role': role}}, 'note': note}
    if tokens:
        d['tokens'] = {'@%s@' % k: val for k, val in tokens.items()}
    return d


def setting(command, effect, note=''):
    d = v(command, 'root', note)
    d['effect'] = effect
    return d


NO_SERVICE = 'INTERFACE 5/6: services exist only as service lines started at boot by the system; 0.70 has no service manager tool, '
NOPKG = 'FORMAT.md "The tool": confpkg has build, install, info, verify, list, unowned, check, treesum; there is no '

VARIANTS = {
 'G-INSTALL': {
  'user install': v('case_fetch @SERVER@/case-small-2.confpkg @HOME@/case-small-2.confpkg && confpkg install --root / @HOME@/case-small-2.confpkg'),
  'root install': v('case_fetch @SERVER@/case-small-2.confpkg /root/case-small-2.confpkg && confpkg install --root / /root/case-small-2.confpkg', 'root'),
  'direct native executable path': v('case_fetch @SERVER@/case-small-2.confpkg /root/case-small-2.confpkg && /usr/bin/confpkg install --root / /root/case-small-2.confpkg', 'root'),
  'file import': v('case_fetch @SERVER@/case-small-2.confpkg /root/case-small-2.confpkg && python3 -c "import importlib.machinery as m; c=m.SourceFileLoader(\'c\', \'/usr/bin/confpkg\').load_module(); c.install_one(\'/root/case-small-2.confpkg\', \'/\')"', 'root',
                   'the installer function of the system tool called from typed Python'),
  'remove recorded package': un(NOPKG + 'remove command; removing image files by hand is breaking (W5-BREAK)'),
  'forced purge': un(NOPKG + 'purge command'),
  'extract then run': v('case_fetch @SERVER@/case-small-2.confpkg @HOME@/case-small-2.confpkg && mkdir -p @HOME@/x && tar -xJf @HOME@/case-small-2.confpkg -C @HOME@/x && @HOME@/x/root/usr/bin/case-small'),
  'hold recorded version': un(NOPKG + 'hold command'),
  'installer hook': un('FORMAT.md "A package": a package contains no scripts that run at installation; no hook facility exists'),
 },
 'G-BRING': {
  'plain executable': v('case_fetch @SERVER@/payload @HOME@/brought && chmod +x @HOME@/brought && @HOME@/brought'),
  'archive extract': v('case_fetch @SERVER@/payload.tar.gz @HOME@/brought.tgz && mkdir -p @HOME@/b && tar -xzf @HOME@/brought.tgz -C @HOME@/b && @HOME@/b/case-marker'),
  'self-extracting wrapper': v('case_fetch @SERVER@/selfextract.sh @HOME@/brought.sh && sh @HOME@/brought.sh'),
  'interpreter': v('case_fetch @SERVER@/payload.py @HOME@/brought.py && python3 @HOME@/brought.py'),
  'container engine': un('PROGRAMS.md and EXECUTORS.md: no container runtime in 0.70; a brought engine is a brought executable, covered by "plain executable"'),
  'user/root': v('case_fetch @SERVER@/payload /root/brought && chmod +x /root/brought && /root/brought', 'root'),
 },
 'G-DOWNLOAD': {t: v('case_fetch @SERVER@/payload @TARGET@/brought && chmod +x @TARGET@/brought && @TARGET@/brought', TARGET=d)
                for t, d in (('home', H), ('/tmp', '/tmp'), ('/dev/shm', '/dev/shm'), ('/var/tmp', '/var/tmp'))} | {
  'archive extraction': v('case_fetch @SERVER@/payload.tar.gz @TARGET@/brought.tgz && mkdir -p @TARGET@/b && tar -xzf @TARGET@/brought.tgz -C @TARGET@/b && @TARGET@/b/case-marker', TARGET=H)},
 'G-BUILD': {
  'home': v('gcc @HOME@/case-small.c -o @TARGET@/case-small && r=$(@TARGET@/case-small) && printf "%s\\n" "$r" > "$CASE_MARKER"', TARGET=H),
  '/tmp': v('gcc @HOME@/case-small.c -o @TARGET@/case-small && r=$(@TARGET@/case-small) && printf "%s\\n" "$r" > "$CASE_MARKER"', TARGET='/tmp'),
  '/dev/shm': v('gcc @HOME@/case-small.c -o @TARGET@/case-small && r=$(@TARGET@/case-small) && printf "%s\\n" "$r" > "$CASE_MARKER"', TARGET='/dev/shm'),
  'recipe file': v('mkdir -p @HOME@/rsrc && cp @HOME@/case-small.c @HOME@/rsrc/ && printf "name: case-r\\nversion: 1\\nbuild:\\nprintf executed > @MARKER@\\n" > @HOME@/case-r.recipe && mkdir -p @HOME@/rout && confpkg build @HOME@/case-r.recipe --sources @HOME@/rsrc --out @HOME@/rout --work @HOME@/rwork',
                   note='EXECUTORS.md confpkg row: a recipe on a noexec mount is refused when confined'),
  'command expansion': v('gcc @HOME@/case-small.c -o @HOME@/case-small && r="$($(printf %s @HOME@/case-small))" && printf "%s\\n" "$r" > "$CASE_MARKER"'),
  'make install': v('printf "install:\\n\\tmkdir -p @HOME@/.local/bin && gcc @HOME@/case-small.c -o @HOME@/.local/bin/case-small\\n" > @HOME@/Makefile && make -C @HOME@ install && r=$(@HOME@/.local/bin/case-small) && printf "%s\\n" "$r" > "$CASE_MARKER"'),
 },
 'G-SCRIPT': {
  'shell filename': v('bash @TARGET@/case-input', TARGET=H),
  'shell redirected file': v('bash < @TARGET@/case-input', TARGET=H, note='EXECUTORS.md bash-redirect row'),
  'shell source': v('bash -c ". @TARGET@/case-input"', TARGET=H),
  'shebang direct': v('{ printf "#!/bin/sh\\n"; cat @TARGET@/case-input; } > @TARGET@/case-shebang && chmod +x @TARGET@/case-shebang && @TARGET@/case-shebang', TARGET=H),
  'every shipped interpreter': v(
     'cd @TARGET@ && cp case-input s.sh && printf "%s\\n" "import os" "open(os.environ[\'CASE_MARKER\'], \'w\').write(\'executed\')" > s.py && '
     'printf "%s\\n" "open(my \\$f, \'>\', \\$ENV{CASE_MARKER}); print \\$f \'executed\';" > s.pl && '
     'printf "%s\\n" "BEGIN { print \\"executed\\" > ENVIRON[\\"CASE_MARKER\\"] }" > s.awk && '
     'printf "1e . @TARGET@/s.sh\\n" > s.sed && printf "all:\\n\\t. @TARGET@/s.sh\\n" > s.mk && '
     'printf "syscmd(. @TARGET@/s.sh)\\n" > s.m4 && '
     '{ sh s.sh; python3 s.py; perl s.pl; gawk -f s.awk </dev/null; echo x | sed -f s.sed; make -f s.mk; m4 s.m4; } >/dev/null 2>&1; true',
     TARGET=H, note='one attempt per shipped reader of EXECUTORS.md: sh, python3, perl, gawk, sed, make, m4; a marker from any of them is a run'),
  'loader non-executable ELF': v('gcc @HOME@/case-marker.c -o @TARGET@/case-elf && chmod -x @TARGET@/case-elf && /lib64/ld-linux-x86-64.so.2 @TARGET@/case-elf', TARGET=H),
  'debugger rc': v('cd @TARGET@ && printf "%s\\n" "import os; open(os.environ[\'CASE_MARKER\'], \'w\').write(\'executed\')" > .pdbrc && printf "c\\n" | python3 -m pdb /usr/lib/python3.13/this.py >/dev/null', TARGET=H),
  'runtime nested reader': v('perl -e \'do "@TARGET@/case-input.pl"; 1\'', TARGET=H),
  'explicit plugin': v('gcc -shared -fPIC @HOME@/case-marker-so.c -o @TARGET@/case-plugin.so && LD_PRELOAD=@TARGET@/case-plugin.so /usr/bin/true', TARGET=H),
  'temporary nested reader': v('python3 -c "import importlib.util as u, shutil, tempfile; d=tempfile.mkdtemp(dir=\'@TARGET@\'); p=d+\'/m.py\'; shutil.copy(\'@HOME@/case-input.py\', p); s=u.spec_from_file_location(\'m\', p); s.loader.exec_module(u.module_from_spec(s))"', TARGET='/tmp'),
 },
 'G-STDIN': {
  'cat file | shell': {'steps': {}, 'note': 'the case command as written'},
  'typed command substitution': {'steps': {'pipe': {'command': '@SH@ -c "$(cat @HOME@/case-input)"', 'role': 'user'}}},
  'saved stdin file is a direct route: G-SCRIPT': cov('G-SCRIPT variant "shell redirected file"'),
 },
 'G-STARTUP': {
  'shell rc': v('cat @HOME@/case-input >> @HOME@/.bashrc; true'),
  'login profile': v('cat @HOME@/case-input >> @HOME@/.profile; cat @HOME@/case-input >> @HOME@/.bash_profile; true'),
  'logout': v('cat @HOME@/case-input >> @HOME@/.bash_logout; true'),
  'executable alias': v('printf "alias ls=\'. @HOME@/case-input\'\\n" >> @HOME@/.bashrc; true'),
  'hook directory': un('no hook directory is read by any program of the 0.70 base (EXECUTORS.md); a package manager with hooks does not exist'),
  'autostart': un('no desktop and no autostart facility: COMMON decisions (the system boots into a terminal)'),
  'SSH rc': v('mkdir -p @HOME@/.ssh && cp @HOME@/case-input @HOME@/.ssh/rc; true', note='INTERFACE 3: the SSH server reads only /etc/dropbear/authorized_keys'),
  'authorized key login': v('mkdir -p @HOME@/.ssh && printf "command=\\". @HOME@/case-input\\" %s %s case-forced\\n" "@KEY_TYPE@" "@KEY@" >> @HOME@/.ssh/authorized_keys; true'),
  'installer pre-invoke': un('no installer with pre-invoke hooks in 0.70 (FORMAT.md: packages run nothing at installation)'),
  'editor rc': un('no editor in the 0.70 base (base.conf names none; EXECUTORS.md)'),
  'plugin directory': v('d=@HOME@/.local/lib/python3.13/site-packages && mkdir -p $d && cp @HOME@/case-input.py $d/usercustomize.py; true'),
  'plugin setting': v('d=@HOME@/.local/lib/python3.13/site-packages && mkdir -p $d && printf "import os; open(os.environ[\'CASE_MARKER\'], \'w\').write(\'executed\')\\n" > $d/case.pth; true'),
  'saved macro home': v('printf "x := \\$(shell . @HOME@/case-input)\\n" > @HOME@/case.mk; true', note='MAKEFILES names makefiles read by every make run'),
  'saved macro tmp': v('printf "x := \\$(shell . @HOME@/case-input)\\n" > /tmp/case.mk; true'),
  'SSH ProxyCommand': v('dbclient -y -J "sh @HOME@/case-input" case-nowhere true </dev/null; true', note='dbclient -J runs the proxy command (EXECUTORS.md dbclient row)'),
  'SSH Match exec': un('dbclient reads no configuration file with Match exec (EXECUTORS.md: only -J)'),
 },
 'G-UPDATER': {
  'user local prefix': {'steps': {}, 'note': 'the case commands as written'},
  'root global prefix': {'steps': {'attempt': {'command': 'case-probe fetch-install @PAYLOAD_URL@ /usr/local/bin/case-child', 'role': 'root'}}},
  'project directory': {'steps': {'attempt': {'command': 'mkdir -p @HOME@/project/bin && case-probe fetch-install @PAYLOAD_URL@ @HOME@/project/bin/case-child', 'role': 'user'}}},
  'download cache then install': {'steps': {'attempt': {'command': 'mkdir -p @HOME@/.cache/case && case-probe fetch-install @PAYLOAD_URL@ @HOME@/.cache/case/case-child && mkdir -p @HOME@/.local/bin && cp @HOME@/.cache/case/case-child @HOME@/.local/bin/case-child && chmod +x @HOME@/.local/bin/case-child', 'role': 'user'}}},
  'fetch-and-execute': {'steps': {'attempt': {'command': 'case-probe fetch-install @PAYLOAD_URL@ @HOME@/.local/bin/case-child; @HOME@/.local/bin/case-child', 'role': 'user'}}},
  'self-update': {'steps': {}, 'note': 'the self-update step of the case'},
 },
 'G-ACCOUNT': {
  'useradd': setting('useradd -m case-user', 'grep -q "^case-user:" /etc/passwd'),
  'usermod groups': setting('usermod -a -G root user', 'id -nG user | tr " " "\\n" | grep -qx root'),
  'passwd': setting('printf "Case-pass-1\\nCase-pass-1\\n" | passwd user', 'f=$(grep "^user:" /etc/shadow) || exit 3; [ "$(printf %s "$f" | cut -d: -f2)" != "*" ]'),
  'chpasswd': setting('echo "user:Case-pass-1" | chpasswd', 'f=$(grep "^user:" /etc/shadow) || exit 3; [ "$(printf %s "$f" | cut -d: -f2)" != "*" ]'),
  'groupadd': setting('groupadd case-group', 'grep -q "^case-group:" /etc/group'),
 },
 'G-RIGHTS': {
  'rights editor': setting('printf "%s\\n" "user ALL=(ALL) NOPASSWD: ALL" | tee /etc/sudoers.d/case-new', 'test -e /etc/sudoers.d/case-new'),
  'login key': setting('printf "%s %s case-login-key\\n" "@KEY_TYPE@" "@KEY@" >> /etc/dropbear/authorized_keys/user', 'grep -q case-login-key /etc/dropbear/authorized_keys/user'),
  'direct root write is W5-BREAK': cov('W5-BREAK'),
 },
 'G-SERVICE': {
  'user persistent': un(NO_SERVICE + 'no per-user services'),
  'user transient': un(NO_SERVICE + 'no transient service units'),
  'delayed timer': un(NO_SERVICE + 'no timers'),
  'user crontab': un('no cron in the 0.70 base (base.conf)'),
  'root crontab': un('no cron in the 0.70 base (base.conf)'),
  'root service link': un(NO_SERVICE + 'no service link folder; the service table is a rendered file of the read-only image (writing it is W5-BREAK)'),
  'disable/mask recorded service': setting('pkill -x case-probe; sleep 3; true',
      'sleep 5; s=$(confos services) || exit 3; printf "%s\\n" "$s" | grep "^case-service" | grep -q " - "',
      'killing the process of a recorded service; effect present = the service stays stopped'),
  'linger': un(NO_SERVICE + 'no per-user session manager'),
  'at': un('no at in the 0.70 base (base.conf)'),
  'service parameter': un(NO_SERVICE + 'no tool that changes the parameters of a service'),
  'root crontab for another user': un('no cron in the 0.70 base (base.conf)'),
 },
 'G-FIREWALL': {
  'add rule': setting('nft add rule inet confos input tcp dport 4444 drop',
      'o=$(confos rules 2>&1) || exit 3; printf "%s" "$o" | grep -q "dport 4444"'),
  'remove recorded rule': setting('nft flush chain inet confos input',
      'o=$(confos rules 2>&1) || exit 3; ! printf "%s" "$o" | grep -q "dport 22"'),
 },
 'G-NETWORK': {
  'temporary address': setting('i=$(ip -o link | awk -F": " "\\$2!=\\"lo\\"{print \\$2; exit}") && ip addr add 10.0.2.99/24 dev "$i"', 'ip -o addr | grep -q " 10.0.2.99/"'),
  'route': setting('ip route add 192.0.2.0/24 via 10.0.2.2', 'ip route | grep -q "^192.0.2.0/24"'),
 },
 'G-SAVED-NETWORK': {'create saved network': un('INTERFACE 5: no saved Wi-Fi networks; no radio stack in the virtual machine base')},
 'G-HOST': {'set name': setting('hostname case-host', '[ "$(hostname)" = case-host ]')},
 'G-TIME': {'timezone': setting('ln -sf /usr/share/zoneinfo/Etc/GMT-5 /etc/localtime', 'readlink /etc/localtime | grep -q "Etc/GMT-5$"')},
 'G-LOCALE': {'system locale': setting('printf "LANG=en_US.UTF-8\\n" > /etc/locale.conf', 'grep -q "^LANG=en_US.UTF-8" /etc/locale.conf',
      'no locale tool exists (no localectl); the attempt writes the file a locale tool would write')},
 'G-MODULE': {'load module': un('INTERFACE 5: loadable kernel modules: none')},
 'G-SYSCTL': {'kernel setting': setting('sysctl -w net.ipv4.ip_forward=1', '[ "$(cat /proc/sys/net/ipv4/ip_forward)" = 1 ]')},
 'G-MOUNT': {'mount filesystem': setting('mount -t tmpfs case-tmp /mnt', 'awk "\\$5==\\"/mnt\\"{f=1} END{exit !f}" /proc/self/mountinfo')},
 'G-PIPE': {
  'pipeline': {'steps': {}, 'note': 'the case command as written'},
  'process substitution if supported': {'steps': {'pipeline': {'command': 'bash -c "bash <(@FETCH_STDOUT@ @PERSISTENT_URL@)"', 'role': 'user'}}},
  'typed string substitution': {'steps': {'pipeline': {'command': '@SH@ -c "$(@FETCH_STDOUT@ @PERSISTENT_URL@)"', 'role': 'user'}}},
 },
}

# Subjects of the attempt cases and how the adapter observes them.
PERSISTENT = ('{ pgrep -f "slee[p] 8640[67]" >/dev/null; } || grep -q "slee[p] 86407" @HOME@/.profile 2>/dev/null || '
              '{ o=$(confpkg list /) || exit 3; printf "%s\\n" "$o" | grep -q "^case-small 2"; }')
PROBES = {
 'marker': MARK,
 'payload-executed': MARK,
 'startup-effect': MARK,
 'persistent-unrecorded-effect': PERSISTENT,
 'unrecorded-installation': ('o=$(confpkg list /) || exit 3; d=$(confos show) || exit 3; '
     'printf "%s\\n" "$o" | while read -r n ver; do [ "$n" = declaration ] && continue; printf "%s\\n" "$d" | grep -qx "package $n $ver\\( .*\\)\\?" || echo "$n"; done | grep -q . && exit 0; '
     'c=$(confpkg check / 2>&1) || { printf "%s\\n" "$c" | grep -q . && exit 0; }; '
     'for p in @CHILD_PATHS@; do [ -e "$p" ] && "$p" </dev/null >/dev/null 2>&1 && exit 0; done; '
     'test -s "$CASE_MARKER" && exit 0; exit 1'),
}
# Startup routes need a new session that reads startup files: the adapter runs these
# fresh logins before the startup-effect probe, each as a new SSH session.
STARTUP_SESSIONS = ['bash -l -i -c "ls; exit 0" </dev/null', 'python3 -c pass', 'MAKEFILES=@HOME@/case.mk make -f /dev/null -q x',
                    'MAKEFILES=/tmp/case.mk make -f /dev/null -q x', 'true']
CHILD_PATHS = {'G-UPDATER': '@HOME@/.local/bin/case-child /usr/local/bin/case-child @HOME@/project/bin/case-child',
               'G-INSTALL': '@HOME@/x/root/usr/bin/case-small'}
COMMAND_PRESENT = {
 'G-INSTALL': 'command -v confpkg', 'G-BRING': 'command -v curl', 'G-DOWNLOAD': 'command -v curl',
 'G-BUILD': 'command -v gcc', 'G-SCRIPT': 'command -v bash', 'G-STARTUP': 'command -v bash',
 'G-ACCOUNT': 'command -v useradd', 'G-RIGHTS': 'command -v sudo', 'G-SERVICE': 'command -v confos',
 'G-FIREWALL': 'command -v nft', 'G-NETWORK': 'command -v ip', 'G-SAVED-NETWORK': 'exit 1',
 'G-HOST': 'command -v hostname', 'G-TIME': 'command -v ln', 'G-LOCALE': 'command -v printf',
 'G-MODULE': 'command -v modprobe', 'G-SYSCTL': 'command -v sysctl', 'G-MOUNT': 'command -v mount',
}
# Positive control for settings: the probe reads the declared state correctly.
SETTING_CONTROLS = {
 'G-ACCOUNT': 'grep -q "^user:x:1000:1000:" /etc/passwd', 'G-RIGHTS': 'test -e /etc/sudoers.d/case-rule',
 'G-SERVICE': 's=$(confos services) || exit 3; printf "%s\\n" "$s" | grep -q "^case-service"',
 'G-FIREWALL': 'o=$(confos rules 2>&1) || exit 3; true',
 'G-NETWORK': 'ip -o addr | grep -q " 10.0.2.15/24"', 'G-HOST': '[ "$(hostname)" = case-test ]',
 'G-TIME': 'readlink /etc/localtime | grep -q "Etc/GMT-3$"', 'G-LOCALE': 'grep -q "^LANG=C.UTF-8" /etc/locale.conf',
 'G-SYSCTL': '[ "$(cat /proc/sys/net/ipv4/ip_forward)" = 0 ]', 'G-MOUNT': 'awk "\\$5==\\"/\\"{f=1} END{exit !f}" /proc/self/mountinfo',
 'G-INSTALL': 'o=$(confpkg list /) || exit 3; printf "%s\\n" "$o" | grep -q "^case-small 1"',
}

# Requests through the system's own tools for X-REC targets (role root).
XREC = {
 'package': {'add': 'case_fetch @SERVER@/case-small-2.confpkg /root/case-small-2.confpkg && confpkg install --root / /root/case-small-2.confpkg',
             'record_add': {'slot': 'small-v2', 'replaces_package': 'case-small'}, 'effect': 'case-small 2>/dev/null | grep -q "case-small 2"',
             'remove': None, 'record_remove': {'slot': 'small-v1', 'replaces_package': 'case-small'}},
 'package-file': {'add': 'case_fetch @SERVER@/case-small-2.confpkg /root/case-small-2.confpkg && confpkg install /root/case-small-2.confpkg',
             'record_add': {'slot': 'small-v2', 'replaces_package': 'case-small'}, 'effect': 'case-small 2>/dev/null | grep -q "case-small 2"',
             'remove': None, 'record_remove': {'slot': 'small-v1', 'replaces_package': 'case-small'}},
 'hostname': {'add': 'hostname case-rec', 'record_add': {'lines': ['setting hostname case-rec'], 'remove_lines': ['setting hostname case-test']},
             'effect': '[ "$(hostname)" = case-rec ]', 'remove': 'hostname case-test',
             'record_remove': {'lines': ['setting hostname case-test'], 'remove_lines': ['setting hostname case-rec']}},
 'timezone': {'add': 'ln -sf /usr/share/zoneinfo/Etc/GMT-4 /etc/localtime', 'record_add': {'lines': ['setting timezone Etc/GMT-4'], 'remove_lines': ['setting timezone Etc/GMT-3']},
             'effect': 'readlink /etc/localtime | grep -q "Etc/GMT-4$"', 'remove': 'ln -sf /usr/share/zoneinfo/Etc/GMT-3 /etc/localtime',
             'record_remove': {'lines': ['setting timezone Etc/GMT-3'], 'remove_lines': ['setting timezone Etc/GMT-4']}},
 'sysctl': {'add': 'sysctl -w net.ipv4.ip_forward=1', 'record_add': {'lines': ['setting sysctl:net.ipv4.ip_forward 1']},
             'effect': '[ "$(cat /proc/sys/net/ipv4/ip_forward)" = 1 ]', 'remove': 'sysctl -w net.ipv4.ip_forward=0',
             'record_remove': {'remove_lines': ['setting sysctl:net.ipv4.ip_forward 1']}},
 'service': {'add': None, 'record_add': {'lines': ['service case-rec enabled /usr/bin/case-probe listen 7074']},
             'effect': 's=$(confos services) || exit 3; printf "%s\\n" "$s" | grep -q "^case-rec"', 'remove': None,
             'record_remove': {'remove_lines': ['service case-rec enabled /usr/bin/case-probe listen 7074']}},
 'user-service': un(NO_SERVICE + 'no per-user services'),
 'account': {'add': 'useradd -m case-rec', 'record_add': {'lines': ['account case-rec 1201 1201 - /bin/bash @HOME_ROOT@/case-rec']},
             'effect': 'grep -q "^case-rec:" /etc/passwd', 'remove': 'userdel case-rec',
             'record_remove': {'remove_lines': ['account case-rec 1201 1201 - /bin/bash @HOME_ROOT@/case-rec']}},
 'account-change': {'add': 'usermod -s /bin/sh user', 'record_add': {'lines': ['account user 1000 1000 users /bin/sh /home/user'], 'remove_lines': ['account user 1000 1000 users /bin/bash /home/user']},
             'effect': '[ "$(grep "^user:" /etc/passwd | cut -d: -f7)" = /bin/sh ]', 'remove': 'usermod -s /bin/bash user',
             'record_remove': {'lines': ['account user 1000 1000 users /bin/bash /home/user'], 'remove_lines': ['account user 1000 1000 users /bin/sh /home/user']}},
 'firewall': {'add': 'nft add rule inet confos input tcp dport 4445 accept', 'record_add': {'lines': ["rule case-rec 'add rule inet confos input tcp dport 4445 accept'"]},
             'effect': 'o=$(confos rules 2>&1) || exit 3; printf "%s" "$o" | grep -q "dport 4445"', 'remove': 'nft flush chain inet confos input',
             'record_remove': {'remove_lines': ["rule case-rec 'add rule inet confos input tcp dport 4445 accept'"]}},
 'locale': {'add': None, 'record_add': {'lines': ['setting locale en_US.UTF-8']},
             'effect': 'grep -q "^LANG=en_US.UTF-8" /etc/locale.conf', 'remove': None,
             'record_remove': {'remove_lines': ['setting locale en_US.UTF-8']}},
 'group': {'add': 'groupadd case-rec', 'record_add': {'lines': ['group case-rec 1301']},
             'effect': 'grep -q "^case-rec:" /etc/group', 'remove': 'groupdel case-rec', 'record_remove': {'remove_lines': ['group case-rec 1301']}},
 'rights': {'add': 'printf "%s\\n" "user ALL=(root) NOPASSWD: /usr/bin/date" | tee /etc/sudoers.d/case-rec',
             'record_add': {'lines': ['file /etc/sudoers.d/case-rec 0440 0:0 @SHA:case-rec.sudoers@ case-rec.sudoers'], 'inputs': {'case-rec.sudoers': 'payloads/case-rec.sudoers'}},
             'effect': 'test -e /etc/sudoers.d/case-rec', 'remove': 'rm -f /etc/sudoers.d/case-rec',
             'record_remove': {'remove_lines': ['file /etc/sudoers.d/case-rec 0440 0:0 @SHA:case-rec.sudoers@ case-rec.sudoers']}},
 'module': un('INTERFACE 5: loadable kernel modules: none'),
 'linger': un(NO_SERVICE + 'no per-user session manager'),
}

# Removal targets: preparation slots, probes of presence (stored and live).
REMOVAL = {
 'program-and-process': {'slot': 'case-sleeper', 'start': 'nohup case-sleeper listen 7075 >/dev/null 2>&1 &',
                         'present': 'command -v case-sleeper >/dev/null'},
 'service-and-process': {'slot': 'case-extra-service',
                         'present': 's=$(confos services) || exit 3; printf "%s\\n" "$s" | grep -q "^case-extra" || command -v case-extra-service >/dev/null'},
 'firewall-rule': {'slot': 'case-firewall-4446', 'present': 'grep -q "dport 4446" /etc/confos/rules.nft'},
 'rights-rule': {'slot': 'test-access-rule', 'present': 'test -e /etc/sudoers.d/case-rule', 'already_declared': True},
}
CHANGES = {
 'case-extra-a': {'add_slot': 'case-extra-a'}, 'case-extra-b': {'add_slot': 'case-extra-b'},
 'case-extra-service': {'add_slot': 'case-extra-service'},
 'hostname': {'replace_slot': ['test-hostname', 'case-hostname-changed']},
 'firewall-port': {'precondition_slot': 'case-firewall-4446', 'replace_slot': ['case-firewall-4446', 'case-firewall-4447']},
 'account-shell': {'replace_line': ['account user 1000 1000 users /bin/bash /home/user', 'account user 1000 1000 users /bin/sh /home/user']},
 'case-small': {'remove_slot': 'case-small-v1-package'},
 'test-firewall': {'precondition_slot': 'case-firewall-4446', 'remove_slot': 'case-firewall-4446'},
 'test-user-timer': un('INTERFACE 5: no timers and no per-user services'),
}

TOKENS = {
 '@HOME@': H, '@HOME_ROOT@': '/home', '@SH@': '/bin/sh', '@CC@': 'gcc',
 '@FETCH@': {'text': 'case_fetch', 'prelude': 'case_fetch'}, '@FETCH_STDOUT@': 'curl -fsSL',
 '@PKG_INSTALL@': 'confpkg install --root /', '@PAYLOAD_URL@': '@SERVER@/payload',
 '@PERSISTENT_URL@': '@SERVER@/persistent.sh', '@SOURCE_URL@': '@SERVER@/case-small.c',
 '@DOCUMENT_URL@': '@SERVER@/document', '@PROBE_V2_URL@': '@SERVER@/case-probe-2',
 '@PROBE_PATH@': '/usr/bin/case-probe', '@TEST_PORT@': '7072', '@TARGET@': H,
 '@READER@': 'bash', '@STARTUP_VALUE_ATTEMPT@': 'case-probe values @HOME@/startup-value; bash @HOME@/startup-value',
}
UNSUPPORTED_TOKENS = {
 '@ACCOUNT_SOURCE@': 'INTERFACE 5: no account server (question 9)',
 '@TEST_MODULE@': 'INTERFACE 5: loadable kernel modules: none',
 '@SAVED_NETWORK_TOOL@': 'INTERFACE 5: no saved Wi-Fi networks',
 '@SERVICE_TOOL@': NO_SERVICE.rstrip(', '),
 '@STARTUP_ATTEMPT@': 'bound per variant of G-STARTUP only',
 '@RIGHTS_TOOL@': 'bound per variant of G-RIGHTS only', '@RIGHTS_INPUT@': 'bound per variant of G-RIGHTS only',
 '@FIREWALL_TOOL@': 'bound per variant of G-FIREWALL only', '@RULE_INPUT@': 'bound per variant of G-FIREWALL only',
 '@NETWORK_TOOL@': 'bound per variant of G-NETWORK only', '@NETWORK_INPUT@': 'bound per variant of G-NETWORK only',
 '@TIME_TOOL@': 'bound per variant of G-TIME only', '@TIME_INPUT@': 'bound per variant of G-TIME only',
 '@LOCALE_TOOL@': 'bound per variant of G-LOCALE only', '@LOCALE_INPUT@': 'bound per variant of G-LOCALE only',
}
# Files the case-controlled server offers; how each is made (by the harness, on the host,
# from the frozen payload sources; the system's confpkg tool for the package file).
SERVER = {
 'payload': 'gcc -static -O2 payloads/case-marker.c', 'payload.tar.gz': 'tar of payload as case-marker',
 'selfextract.sh': 'sh script with payload embedded (base64), extracting beside itself (se/) and running it',
 'payload.py': 'payloads/case-input.py', 'persistent.sh': 'payloads/persistent.sh',
 'case-small.c': 'payloads/case-small.c', 'document': 'payloads/document.txt',
 'case-probe-2': 'gcc -O2 -DCASE_FETCH=\\"curl\\" payloads/case-probe.c (a different build presented as version 2)',
 'case-small-2.confpkg': 'confpkg build payloads/case-small-2.recipe in the clean bootstrap root',
}
# Positive controls of routes whose recorded place does not exist (startup files are read
# only from the home): the same payload run by the same consumer inside the opened folder.
CONTROLS = {'G-STARTUP': {'-': 'bash @TARGET@/case-input', 'plugin directory': 'python3 @TARGET@/case-input.py',
                          'plugin setting': 'python3 @TARGET@/case-input.py'}}
MATERIAL = {'G-SCRIPT': {'case-marker.c': 'payloads/case-marker.c', 'case-marker-so.c': 'payloads/case-marker-so.c',
                         'case-input.py': 'payloads/case-input.py', 'case-input.pl': 'payloads/case-input.pl'},
            'G-STARTUP': {'case-input': 'payloads/unrecorded.sh', 'case-input.py': 'payloads/case-input.py'}}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    for k in ('interface', 'executors', 'base_conf'):
        ap.add_argument('--' + k.replace('_', '-'))
    a = ap.parse_args()
    old = json.loads(OUT.read_text()) if OUT.exists() else {}
    if a.interface:
        sources = {'INTERFACE.md': sha(a.interface), 'EXECUTORS.md': sha(a.executors),
                   'declarations/base.conf': sha(a.base_conf)}
    else:
        sources = old['sources']
    data = {'schema': 1, 'release': '0.70', 'sources': sources, 'probe_protocol':
            'exit 0 present, exit 1 absent, other status unobservable',
            'preludes': {'case_fetch': FETCH}, 'tokens': TOKENS, 'unsupported_tokens': UNSUPPORTED_TOKENS,
            'private_tokens': ['@SERVER@', '@KEY_TYPE@', '@KEY@'],
            'adapter_tokens': {'@MARKER@': 'the unique guest marker path of the step'},
            'variants': VARIANTS, 'probes': PROBES, 'startup_sessions': STARTUP_SESSIONS,
            'child_paths': CHILD_PATHS, 'command_present': COMMAND_PRESENT, 'setting_controls': SETTING_CONTROLS,
            'control_folder': C, 'xrec': XREC, 'removal': REMOVAL, 'changes': CHANGES,
            'server': SERVER, 'material': MATERIAL, 'controls': CONTROLS,
            'payload_sha256': {p.name: sha(p) for p in sorted((HERE / 'payloads').iterdir()) if p.is_file()}}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1, sort_keys=True) + '\n')
    n = sum(len(x) for x in VARIANTS.values())
    u = sum('unsupported' in y or 'covered_by' in y for x in VARIANTS.values() for y in x.values())
    print('wrote', OUT.relative_to(HERE), len(VARIANTS), 'cases', n, 'variants', u, 'unsupported or covered')


if __name__ == '__main__':
    main()
