"""Every case of CASES.md as data, in its order. `run --list` prints the IDs (diffed against CASES.md).

Step vocabulary (interpreted by `run`):
  ('L+', SPEC) ('L~', SPEC) ('L-', SPEC)      the person adds / changes / removes a line (adapter.py renders it)
  ('APPLY',)                                  the documented application; followed by INV + CMP (row P2-1:<case>:<n>)
  ('U', CMD[, CHECK]) ('R', CMD[, CHECK])      a step of the action; it must hold CHECK (default: exit 0)
  ('ATTEMPT', 'U'|'R', CMD)                   a P4 attempt: its exit does not decide anything
  ('LOGIN', CMD)                              a new SSH login of the ordinary account (login shell), CMD on its stdin
  ('PROBE', 'U'|'R', CMD, AGAINST)            observation; AGAINST says when it counts against the part
  ('OBSERVE', 'U'|'R', CMD)                   recorded only
  ('LOGIN-WITH-GUEST-KEY', PATH)              H: ssh as the ordinary account with a private key read from the guest;
                                              a successful login counts against
  ('RESTART',) ('WAIT', SECONDS) ('INV', TAG) ('INV0', TAG): an inventory without rows of its own, the state before a
  P4 attempt, against which the attempt's effect is measured
CHECK / AGAINST: 'exit0' | 'nonzero' | 'eq:N' | 're:REGEX' | '!re:REGEX' (on stdout+stderr) |
  'renz:REGEX' (counts against when REGEX matches or the observation itself exits nonzero)
Command templates: @HTTP@ = http://10.0.2.2:PORT of the case's payload server, @DEV@ = the guest's network device.
"""

JQ_URL = 'https://github.com/jqlang/jq/releases/download/jq-1.7.1/jq-linux-amd64'
NVIM_095_URL = 'https://github.com/neovim/neovim/releases/download/v0.9.5/nvim.appimage'
RG_URL = ('https://github.com/BurntSushi/ripgrep/releases/download/14.1.1/'
          'ripgrep-14.1.1-x86_64-unknown-linux-musl.tar.gz')
GNU_HELLO_URL = 'https://ftp.gnu.org/gnu/hello/hello-2.12.1.tar.gz'
HELLO_C_URL = ('https://raw.githubusercontent.com/docker-library/hello-world/'
               '522bcd2faf422c60b9d20e64d7cd6d56600aec97/hello.c')
HELLO_C_SHA = 'cb95a0ed950c272471e7eb2a6b4261d857174bc3750874f538ac60e20af16d34'
HELLO_OUT = {'original': '8d9adee79e1c69c44f1713b1eeaf875a8dc33e738b1983a36c55be54899f871f',
             1: '59230970d23884e1ba5ed4c7dc17db7b95532d4ba57a58501edd022037b8ff2e',
             2: '61565a664cffb6f957778f4c1d0c70644b5c5c5d8d0a3b7e6afee277a76485bc',
             3: '49f7d4506fb2e5cbd506b37e6fb1e071e38a343e18d470982dd17df5320cd3ce'}
LGSM_URL = ('https://raw.githubusercontent.com/GameServerManagers/LinuxGSM/'
            '50dc4e551b661b9d1fa39c291068a16a66056aff/linuxgsm.sh')
LGSM_SHA = '3063de7f3bf025976dcd11693af84bbe78b43564c3174129d524c7b3c16f5707'
GAME_PREREQS = ('bc bsdmainutils bzip2 distro-info jq lib32gcc-s1 lib32stdc++6 libc6-i386 libevent-core-2.1-7t64 '
                'libjq1 libonig5 ncal pigz tmux unzip').split()

# Inputs fixed when the inputs are committed (QUESTIONS.md Q1). None = not fixed yet: the case is `unobserved`.
ARCHIVE_STATES = {'T0': '20260801T000000Z', 'T1': '20261001T000000Z', 'T2': '20261123T000000Z'}  # PROGRAMS.md, tools/update-diff.out
CHG1_PACKAGE = ('ed', None)          # (package, the other available version); None = not fixed yet

PS = "ps -eo args="                  # process list; patterns below are matched whole-line, never by pgrep -f
# The effective ruleset: the documented read of ConfOS (build/INTERFACE.md rev. 3, `sudo confos rules`, the native
# nftables output unchanged), else the native query itself (stock image).
RULES = 'confos rules 2>/dev/null || nft list ruleset'

# ---------------------------------------------------------------- payload of the download-and-execute cases

PAYLOAD_SH = r'''#!/bin/sh
sleep 86406 >/dev/null 2>&1 &
mkdir -p ~/.config/systemd/user
printf '[Service]\nExecStart=/bin/sleep 86407\n[Install]\nWantedBy=default.target\n' > ~/.config/systemd/user/cases-pipe.service
systemctl --user daemon-reload; systemctl --user enable --now cases-pipe.service
printf '* * * * * /bin/true cases-pipe\n' | crontab -
echo 'sleep 86408 >/dev/null 2>&1 & # cases-pipe' >> ~/.bashrc
curl -fsSo ~/jq @HTTP@/jq && chmod +x ~/jq
echo payload-done
'''

PAYLOAD_PY = r'''import os, subprocess, urllib.request
home = os.path.expanduser('~')
subprocess.Popen(['sleep', '86406'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
d = os.path.join(home, '.config/systemd/user'); os.makedirs(d, exist_ok=True)
open(os.path.join(d, 'cases-pipe.service'), 'w').write('[Service]\nExecStart=/bin/sleep 86407\n[Install]\nWantedBy=default.target\n')
subprocess.call(['systemctl', '--user', 'daemon-reload']); subprocess.call(['systemctl', '--user', 'enable', '--now', 'cases-pipe.service'])
subprocess.run(['crontab', '-'], input=b'* * * * * /bin/true cases-pipe\n')
open(os.path.join(home, '.bashrc'), 'a').write('sleep 86408 >/dev/null 2>&1 & # cases-pipe\n')
open(os.path.join(home, 'jq'), 'wb').write(urllib.request.urlopen('@HTTP@/jq').read()); os.chmod(os.path.join(home, 'jq'), 0o755)
print('payload-done')
'''

PIPE_SERVE = {'payload.sh': PAYLOAD_SH, 'payload.py': PAYLOAD_PY, 'jq': ('url', JQ_URL)}

PIPE_PROBES = [
    ('PROBE', 'U', f"{PS} | grep -xE 'sleep 8640[678]( .*)?|/bin/sleep 8640[678]'", 'exit0'),
    ('PROBE', 'U', 'systemctl --user is-enabled cases-pipe.service', 're:^enabled'),
    ('PROBE', 'U', 'systemctl --user is-active cases-pipe.service', 're:^active'),
    ('PROBE', 'U', 'crontab -l', 're:cases-pipe'),
    ('PROBE', 'U', 'grep -n cases-pipe ~/.bashrc', 'exit0'),
    ('PROBE', 'U', '~/jq --version', 'exit0'),
]


def _observe_only(steps):
    """The probes before the restart are recorded; only the state after the restart decides (plus P1 rows)."""
    return [('OBSERVE',) + s[1:4] if s[0] == 'PROBE' else s for s in steps]


def pipe_case(cid, attempt):
    return dict(id=cid, part='P4', family='steps', policy='probe', serve=PIPE_SERVE,
                source='Paper 4, Section 9.3: “a command downloads and executes code without saving it; after a '
                       'reboot, nothing that was executed must be in force”',
                steps=[('INV0', cid + '-pre'), ('ATTEMPT', 'U', attempt)] + _observe_only(PIPE_PROBES) +
                      [('INV', cid + '-before'), ('RESTART',)] + PIPE_PROBES + [('INV', cid)])


def p4(cid, steps, note=None, serve=None):
    d = dict(id=cid, part='P4', family='steps', policy='probe', steps=[('INV0', cid + '-pre')] + list(steps) +
             [('INV', cid)],
             source='Table 9, P4: “Through every channel of [3], Section 4.3, an attempt is made to install, launch '
                    'or change what is not recorded; the built-in tools, including the system’s own package '
                    'installer, are also tried directly with superuser privileges.”')
    if note:
        d['note'] = note
    if serve:
        d['serve'] = serve
    return d


def ran(who, cmd):
    """The attempted object ran: exit 0 counts against."""
    return ('PROBE', who, cmd, 'exit0')


# A P4 probe is taken before the attempt too and counts only if it changed ([n2-5]); a probe that would
# itself perform the attempt (it downloads and installs what it runs) is not taken before, with this reason.
NOPRE_SELF = {'nopre': 'the probe itself downloads and installs what it runs, so taking it before the attempt would '
                       'perform the attempt'}


def proc(pattern):
    return ('PROBE', 'U', f"{PS} | grep -xE '{pattern}'", 'exit0')


HELLO_PROBES = [ran('U', 'hello --version'),
                ('PROBE', 'U', "dpkg-query -W -f '${db:Status-Abbrev}' hello", 're:^ii')]
ED_STAYS = [('PROBE', 'U', 'ed --version', 'nonzero'), ('OBSERVE', 'U', 'dpkg-query -W ed')]

CASES = []

# ---------------------------------------------------------------- ordinary work

OW_SRC = 'plan Section 9.3: “It counts against the hypothesis when an ordinary action cannot be performed through ' \
         'the declaration and its built-in tools.”'
CASES += [
    dict(id='OW-1', part='OW', family='steps', policy='ow', source=OW_SRC + ' — “installing a program”',
         steps=[('L+', 'package tree'), ('APPLY',), ('U', 'tree --version', 're:v2\\.2\\.1'), ('U', 'tree -L 1 ~'),
                ('U', "dpkg-query -W -f '${Version}' tree", 're:^2\\.2\\.1-1$'), ('INV', 'OW-1')]),
    dict(id='OW-2', part='OW', family='ow-updates', source=OW_SRC + ' — “two updates with a restart after each”'),
    dict(id='OW-3', part='OW', family='with', with_case='OW-2', source=OW_SRC + ' — the second update'),
    dict(id='OW-4', part='OW', family='steps', policy='ow', source=OW_SRC + ' — “working in a browser”',
         serve={'page.html': '<html><body><h1>cases page</h1></body></html>\n'},
         steps=[('L+', 'package firefox-esr'), ('APPLY',),
                ('U', 'firefox-esr --headless --screenshot ~/shot.png @HTTP@/page.html'),
                ('U', 'firefox-esr --headless --screenshot ~/local.png file:///usr/share/doc/firefox-esr/copyright'),
                ('U', 'test -s ~/shot.png && test -s ~/local.png && head -c 8 ~/shot.png | od -An -c', 're:P +N +G'),
                ('INV', 'OW-4')]),
    dict(id='OW-5', part='OW', family='steps', policy='ow', source=OW_SRC + ' — “editing documents”',
         steps=[('L+', 'package libreoffice-writer'), ('APPLY',),
                ('U', "printf 'First line\\n' > ~/doc.txt"),
                ('U', 'soffice --headless --convert-to odt --outdir ~ ~/doc.txt'),
                ('U', "printf 'First line\\nSecond line\\n' > ~/doc.txt"),
                ('U', 'soffice --headless --convert-to odt --outdir ~ ~/doc.txt'),
                ('U', 'soffice --headless --cat ~/doc.odt', 're:(?s)First line.*Second line'), ('INV', 'OW-5')]),
    dict(id='OW-6', part='OW', family='steps', policy='ow',
         source=OW_SRC + ' — “running ordinary commands and one’s own recorded script” [4, 9.3]',
         steps=[('U', "ls -la ~ && cp /etc/hostname ~/h && grep -c . ~/h && sort /etc/shells && "
                      "printf '1p\\nq\\n' | ed -s ~/h"),
                ('U', '~/bin/cases-report.sh', 're:cases-report ok'), ('INV', 'OW-6')]),
    dict(id='OW-7', part='OW', family='ow-build',
         source=OW_SRC + ' — “fetching, building, changing and rebuilding a small program”'),
    dict(id='OW-8', part='OW', family='ow-game',
         source=OW_SRC + ' — “installing and starting a game through a launcher that downloads it”'),
    dict(id='OW-9', part='OW', family='netloss',
         source=OW_SRC + ' — “an installation during which the network is lost and then restored”'),
    dict(id='OW-10', part='OW', family='hardware', source=OW_SRC + ' — “connecting to a Wi-Fi network … on real '
         'hardware”'),
    dict(id='OW-11', part='OW', family='hardware', source=OW_SRC + ' — “pairing a Bluetooth device on real '
         'hardware”'),
]

# ---------------------------------------------------------------- P1, P2

CASES += [
    dict(id='P1-0', part='P1', family='steps', policy='inv-only',
         source='Table 9, P1: “an inventory of the whole machine … every object is decided”',
         steps=[('INV', 'P1-0')]),
]
P2_SRC = ('Table 9, P2: “A power cut right after the report of success, three times for each kind of application: '
          'adding, changing and removing a line”')
for k, spec in ((1, 'package tree'), (2, 'package sl'),
                (3, "user-unit person cases-cut.service '[Service]\\nExecStart=/bin/sleep 86400\\n' enabled")):
    CASES.append(dict(id=f'P2-ADD-{k}', part='P2', family='p2-cut', source=P2_SRC, op=('L+', spec), probes=[]))
CASES += [
    dict(id='P2-CHG-1', part='P2', family='p2-cut', source=P2_SRC, op=('L~', 'setting hostname cases-chg'),
         probes=[('PROBE', 'U', 'cat /proc/sys/kernel/hostname', '!re:^cases-chg$')]),
    dict(id='P2-CHG-2', part='P2', family='p2-cut', source=P2_SRC,
         op=('L~', "firewall cases-8081 'add rule inet confos input tcp dport 8082 accept'"),
         probes=[('PROBE', 'R', RULES, '!re:dport 8082')]),
    dict(id='P2-CHG-3', part='P2', family='p2-cut', source=P2_SRC,
         op=('L~', 'account person uid=1000 gid=1000 groups=wheel shell=/bin/sh home=/home/person'),
         probes=[('PROBE', 'U', "grep '^person:' /etc/passwd", '!re::/bin/sh$')]),
    dict(id='P2-REM-1', part='P2', family='p2-cut', source=P2_SRC, op=('L-', 'package ed'),
         probes=[('PROBE', 'U', 'command -v ed', 'exit0')]),
    dict(id='P2-REM-2', part='P2', family='p2-cut', source=P2_SRC, op=('L-', "firewall cases-8081 x"),
         probes=[('PROBE', 'R', RULES, 'renz:dport 8081')]),
    dict(id='P2-REM-3', part='P2', family='p2-cut', source=P2_SRC,
         op=('L-', "user-unit person cases-tick.timer x"),
         probes=[('PROBE', 'U', 'systemctl --user is-enabled cases-tick.timer', 're:^enabled')]),
    dict(id='P2-NET-1', part='P2', family='netloss',
         source='Table 9, P2: “An installation interrupted by a loss of network”'),
]

# ---------------------------------------------------------------- P4

C6 = [('P4-C6-1', '~'), ('P4-C6-2', '/tmp'), ('P4-C6-3', '/dev/shm'), ('P4-C6-4', '/var/tmp')]
CASES += [
    p4('P4-C1-1', [('ATTEMPT', 'U', 'apt-get download hello; apt-get install -y hello')] + HELLO_PROBES),
    p4('P4-C1-2', [('ATTEMPT', 'R', 'apt-get update; apt-get install -y hello')] + HELLO_PROBES),
    p4('P4-C1-3', [('ATTEMPT', 'R', 'cd /root && apt-get download hello && dpkg -i hello_*.deb')]
       + HELLO_PROBES),
    p4('P4-C1-4', [('ATTEMPT', 'R', 'apt-get remove -y ed')] + ED_STAYS),
    p4('P4-C1-5', [('ATTEMPT', 'R', 'dpkg --purge --force-depends ed')] + ED_STAYS),
    p4('P4-C1-6', [('ATTEMPT', 'U', 'cd ~ && apt-get download hello && dpkg-deb -x hello_*.deb ~/x'),
                   ran('U', '~/x/usr/bin/hello')]),
    p4('P4-C2-1', [('ATTEMPT', 'U', 'pip install --user --break-system-packages pyjokes==0.8.3'),
                   ran('U', '~/.local/bin/pyjoke'),
                   ('PROBE', 'U', 'python3 -m pip list --user', 're:pyjokes')]),
    p4('P4-C2-2', [('ATTEMPT', 'U', 'python3 -m venv ~/venv && ~/venv/bin/pip install pyjokes==0.8.3'),
                   ran('U', '~/venv/bin/pyjoke')]),
    p4('P4-C2-3', [('ATTEMPT', 'R', 'pip install --break-system-packages pyjokes==0.8.3'),
                   ran('R', 'pyjoke'), ('PROBE', 'R', 'pip list', 're:pyjokes')]),
    p4('P4-C2-4', [('ATTEMPT', 'U', 'pip download pyjokes==0.8.3 -d ~/w && '
                                    'pip install --user --break-system-packages --no-index ~/w/*.whl'),
                   ran('U', '~/.local/bin/pyjoke')]),
    p4('P4-C3-1', [('ATTEMPT', 'U', 'npm install -g --prefix ~/.npm-global semver@7.6.3'),
                   ran('U', '~/.npm-global/bin/semver 1.2.3')]),
    p4('P4-C3-2', [('ATTEMPT', 'U', 'mkdir -p ~/p && cd ~/p && npm install semver@7.6.3'),
                   ran('U', '~/p/node_modules/.bin/semver 1.2.3')]),
    p4('P4-C3-3', [('PROBE', 'U', 'npx --yes semver@7.6.3 1.2.3', 'exit0', NOPRE_SELF), ('OBSERVE', 'U', 'ls ~/.npm/_npx')]),
    p4('P4-C3-4', [('ATTEMPT', 'R', 'npm install -g semver@7.6.3'), ran('R', 'semver 1.2.3')]),
    p4('P4-C4-1', [('ATTEMPT', 'U', 'flatpak remote-add --user --if-not-exists flathub '
                                    'https://dl.flathub.org/repo/flathub.flatpakrepo && '
                                    'flatpak install --user -y flathub net.sourceforge.ExtremeTuxRacer'),
                   ('PROBE', 'U', 'flatpak list --user', 're:ExtremeTuxRacer'),
                   ran('U', 'flatpak run --command=true net.sourceforge.ExtremeTuxRacer')]),
    p4('P4-C4-2', [('ATTEMPT', 'R', 'flatpak remote-add --system --if-not-exists flathub '
                                    'https://dl.flathub.org/repo/flathub.flatpakrepo; '
                                    'flatpak install --system -y flathub net.sourceforge.ExtremeTuxRacer'),
                   ('PROBE', 'R', 'flatpak list --system', 're:ExtremeTuxRacer'),
                   ran('U', 'flatpak run --command=true net.sourceforge.ExtremeTuxRacer')]),
    p4('P4-C4-3', [('ATTEMPT', 'U', 'flatpak remote-add --user cases-extra '
                                    'https://dl.flathub.org/beta-repo/flathub-beta.flatpakrepo'),
                   ('PROBE', 'U', 'flatpak remotes --user', 're:cases-extra')]),
    p4('P4-C5-1', [('ATTEMPT', 'U', f'curl -fsSLo ~/nvim.appimage {NVIM_095_URL} && chmod +x ~/nvim.appimage'),
                   ran('U', '~/nvim.appimage --version')]),
    p4('P4-C5-2', [('ATTEMPT', 'U', f'curl -fsSLo ~/nvim.appimage {NVIM_095_URL} && chmod +x ~/nvim.appimage'),
                   ran('U', '~/nvim.appimage --appimage-extract-and-run --version'),
                   ('ATTEMPT', 'U', 'cd ~ && ~/nvim.appimage --appimage-extract'),
                   ran('U', '~/squashfs-root/AppRun --version')]),
] + [
    p4(cid, [('ATTEMPT', 'U', f'curl -fsSLo {d}/jq {JQ_URL} && chmod +x {d}/jq'), ran('U', f'{d}/jq --version')])
    for cid, d in C6
] + [
    p4('P4-C6-5', [('ATTEMPT', 'R', f'curl -fsSLo /usr/local/bin/jq {JQ_URL} && chmod +x /usr/local/bin/jq'),
                   ran('R', '/usr/local/bin/jq --version')],
       note='breaking-candidate (QUESTIONS.md Q6): a direct write by root with curl -o into /usr/local/bin'),
    p4('P4-C6-6', [('ATTEMPT', 'U', f'curl -fsSLo ~/rg.tgz {RG_URL} && tar xf ~/rg.tgz -C ~'),
                   ran('U', '~/ripgrep-14.1.1-x86_64-unknown-linux-musl/rg --version')]),
    p4('P4-C7-1', [('ATTEMPT', 'U', f'curl -fsSLo ~/h.tgz {GNU_HELLO_URL} && tar xf ~/h.tgz -C ~ && '
                                    'cd ~/hello-2.12.1 && ./configure --prefix=$HOME/.local && make && make install'),
                   ran('U', '~/.local/bin/hello')]),
    p4('P4-C7-2', [('ATTEMPT', 'U', "printf 'int main(){return 42;}' > ~/t.c && gcc -o ~/t ~/t.c"),
                   ('PROBE', 'U', '~/t', 'eq:42')]),
    p4('P4-C7-3', [('ATTEMPT', 'U', "printf 'int main(){return 42;}' > /tmp/t.c && gcc -o /tmp/t /tmp/t.c && "
                                    "gcc -o /dev/shm/t /tmp/t.c"),
                   ('PROBE', 'U', '/tmp/t', 'eq:42'), ('PROBE', 'U', '/dev/shm/t', 'eq:42')]),
    p4('P4-C8-1', [('ATTEMPT', 'U', "mkdir -p ~/.config/systemd/user && printf '[Service]\\nExecStart=/bin/sleep "
                                    "86400\\n[Install]\\nWantedBy=default.target\\n' > ~/.config/systemd/user/p4.service"
                                    " && systemctl --user daemon-reload && systemctl --user enable --now p4.service"),
                   ('PROBE', 'U', 'systemctl --user is-enabled p4', 're:^enabled'),
                   ('PROBE', 'U', 'systemctl --user is-active p4', 're:^active'),
                   ('RESTART',),
                   ('PROBE', 'U', 'systemctl --user is-enabled p4', 're:^enabled'),
                   ('PROBE', 'U', 'systemctl --user is-active p4', 're:^active'),
                   proc('(/bin/)?sleep 86400')]),
    p4('P4-C8-2', [('ATTEMPT', 'U', 'systemd-run --user --unit=p4t /bin/sleep 86400'),
                   ('PROBE', 'U', 'systemctl --user is-active p4t', 're:^active'), proc('(/bin/)?sleep 86400')]),
    p4('P4-C8-3', [('ATTEMPT', 'U', "systemd-run --user --on-calendar='*:*:00' --unit=p4c /bin/true"),
                   ('PROBE', 'U', 'systemctl --user list-timers --all', 're:p4c')]),
    p4('P4-C8-4', [('ATTEMPT', 'U', "printf '* * * * * /bin/touch /tmp/p4cron\\n' > ~/ct && crontab ~/ct"),
                   ('WAIT', 70), ('PROBE', 'U', 'crontab -l', 're:p4cron'),
                   ('PROBE', 'U', 'test -e /tmp/p4cron', 'exit0')]),
    p4('P4-C8-5', [('ATTEMPT', 'R', "printf '* * * * * /bin/touch /tmp/p4cronr\\n' > /root/ct && crontab /root/ct"),
                   ('WAIT', 70), ('PROBE', 'R', 'crontab -l', 're:p4cronr'),
                   ('PROBE', 'R', 'test -e /tmp/p4cronr', 'exit0')]),
    p4('P4-C8-6', [('ATTEMPT', 'R', "printf '[Service]\\nExecStart=/bin/sleep 86409\\n[Install]\\n"
                                    "WantedBy=multi-user.target\\n' > /root/p4root.service && "
                                    "systemctl link /root/p4root.service && systemctl enable --now p4root.service"),
                   ('PROBE', 'R', 'systemctl is-enabled p4root.service', 're:^(enabled|linked)'),
                   ('PROBE', 'R', 'systemctl is-active p4root.service', 're:^active'),
                   proc('(/bin/)?sleep 86409')]),
    p4('P4-C8-7', [('ATTEMPT', 'R', 'systemctl disable --now cases-svc.service; systemctl mask cases-svc.service'),
                   ('PROBE', 'U', f"{PS} | grep -xE '(/usr/bin/)?sleep infinity'", 'nonzero'),
                   ('OBSERVE', 'R', 'systemctl is-enabled cases-svc.service; systemctl is-active cases-svc.service'),
                   ('PROBE', 'R', 'systemctl is-enabled cases-svc.service', 're:^masked')]),
    p4('P4-C8-8', [('ATTEMPT', 'R', 'loginctl enable-linger person'),
                   ('PROBE', 'R', 'loginctl show-user person -p Linger', 're:Linger=yes')]),
    p4('P4-C8-9', [('ATTEMPT', 'U', 'command -v at && echo /bin/true | at now + 1 minute'),
                   ('PROBE', 'U', 'atq', 'out:\\S')], note='if `at` is not present the attempt cannot run'),
    p4('P4-C9-1', [('ATTEMPT', 'U', "for d in ~ /tmp /dev/shm; do printf 'sleep 86410 &\\n' > $d/f.sh; "
                                    "bash $d/f.sh; done"),
                   proc('sleep 86410')]),
    p4('P4-C9-2', [('ATTEMPT', 'U', "for d in ~ /tmp /dev/shm; do printf 'import subprocess\\n"
                                    "subprocess.Popen([\"sleep\", \"86411\"], start_new_session=True)\\n' > $d/f.py; "
                                    "python3 $d/f.py; done"),
                   proc('sleep 86411')]),
    p4('P4-C9-3', [('ATTEMPT', 'U', "for d in ~ /tmp /dev/shm; do printf 'system(\"sleep 86412 &\");\\n' > $d/f.pl; "
                                    "perl $d/f.pl; done"),
                   proc('sleep 86412')]),
    p4('P4-C9-4', [('ATTEMPT', 'U', "printf '#!/bin/sh\\necho ran\\n' > ~/s.sh && chmod +x ~/s.sh"),
                   ('PROBE', 'U', '~/s.sh', 're:^ran')]),
    p4('P4-C9-5', [('ATTEMPT', 'U', 'cp /usr/bin/true ~/tru && chmod -x ~/tru'),
                   ('PROBE', 'U', '/lib64/ld-linux-x86-64.so.2 ~/tru', 'exit0')]),
    p4('P4-C10-1', [('ATTEMPT', 'U', "echo 'sleep 86401 &' >> ~/.bashrc"), ('ATTEMPT', 'U', 'bash -lic true'),
                    proc('sleep 86401')]),
    p4('P4-C10-2', [('ATTEMPT', 'U', "echo 'sleep 86402 &' >> ~/.profile"), ('LOGIN', 'true'),
                    proc('sleep 86402')]),
    p4('P4-C10-3', [('ATTEMPT', 'U', "git config --global alias.p4 '!sleep 86403 &' && git p4"),
                    proc('sleep 86403')]),
    p4('P4-C10-4', [('ATTEMPT', 'U', "git init ~/r && git -C ~/r config core.hooksPath ~/hooks && mkdir -p ~/hooks "
                                     "&& printf '#!/bin/sh\\ntouch /tmp/p4hook\\n' > ~/hooks/pre-commit && "
                                     "chmod +x ~/hooks/pre-commit && git -C ~/r -c user.name=p -c user.email=p@p "
                                     "commit --allow-empty -m x"),
                    ('PROBE', 'U', 'test -e /tmp/p4hook', 'exit0')]),
    p4('P4-C10-5', [('ATTEMPT', 'U', "mkdir -p ~/.config/autostart && printf '[Desktop Entry]\\nType=Application\\n"
                                     "Exec=/bin/sleep 86404\\n' > ~/.config/autostart/p4.desktop")],
       note='the file is a setting that launches something (S8.2-14); decided by CMP'),
    p4('P4-C10-6', [('ATTEMPT', 'U', "printf 'sleep 86405 &\\n' > ~/.ssh/rc"), ('LOGIN', 'true'),
                    proc('sleep 86405')]),
    p4('P4-C10-7', [('ATTEMPT', 'U', "ssh-keygen -q -t ed25519 -N '' -f ~/k && cat ~/k.pub >> ~/.ssh/authorized_keys"),
                    ('LOGIN-WITH-GUEST-KEY', '~/k')]),
    p4('P4-C11-1', [('ATTEMPT', 'U', 'podman pull docker.io/library/busybox:1.36.1'),
                    ('PROBE', 'U', 'podman run --rm docker.io/library/busybox:1.36.1 true', 'exit0', NOPRE_SELF),
                    ('PROBE', 'U', 'podman images', 're:busybox')]),
    p4('P4-C11-2', [('ATTEMPT', 'U', 'podman run -d --name p4c docker.io/library/busybox:1.36.1 sleep 86400'),
                    ('PROBE', 'U', 'podman ps', 're:p4c'), proc('(/bin/)?sleep 86400')]),
    p4('P4-C11-3', [('ATTEMPT', 'U', "printf 'FROM docker.io/library/alpine:3.20.3\\nRUN true\\n' > ~/Containerfile "
                                     "&& podman build -t p4b ~"),
                    ('PROBE', 'U', 'podman images', 're:p4b')]),
    p4('P4-C11-4', [('ATTEMPT', 'U', "mkdir -p ~/.config/containers/systemd && printf '[Container]\\nImage=docker.io/"
                                     "library/busybox:1.36.1\\nExec=sleep 86400\\n[Install]\\nWantedBy=default.target"
                                     "\\n' > ~/.config/containers/systemd/p4q.container && systemctl --user "
                                     "daemon-reload && systemctl --user start p4q"),
                    ('PROBE', 'U', 'systemctl --user is-active p4q', 're:^active')]),
    p4('P4-BT-1', [('ATTEMPT', 'R', 'useradd -m p4user'), ('PROBE', 'R', "grep '^p4user:' /etc/passwd", 'exit0')]),
    p4('P4-BT-2', [('ATTEMPT', 'R', 'usermod -aG sudo person'), ('PROBE', 'R', 'id person', 're:\\(sudo\\)')]),
    p4('P4-BT-3', [('SNAP', 'R', "grep '^person:' /etc/shadow | sha256sum"),
                   ('ATTEMPT', 'R', "echo 'person:Other-pass-1' | chpasswd"),
                   ('PROBE-CHANGED', 'R', "grep '^person:' /etc/shadow | sha256sum")]),
    p4('P4-BT-4', [('ATTEMPT', 'R', 'groupadd p4group'), ('PROBE', 'R', "grep '^p4group:' /etc/group", 'exit0')]),
    p4('P4-BT-5', [('ATTEMPT', 'R', "printf 'person ALL=(ALL) NOPASSWD: ALL\\n' > /tmp/s && visudo -cf /tmp/s && "
                                    "install -m 0440 /tmp/s /etc/sudoers.d/p4"),
                   ('PROBE', 'R', 'sudo -l -U person', 're:\\(ALL\\) NOPASSWD: ALL'),
                   ('ATTEMPT', 'R', "printf 'person ALL=(ALL) NOPASSWD: /usr/bin/id\\n' | EDITOR='tee -a' visudo"),
                   ('PROBE', 'R', 'sudo -l -U person', 're:/usr/bin/id')],
       note='breaking-candidate (QUESTIONS.md Q6): `install` into /etc/sudoers.d is file copying (S8.1-8)'),
    p4('P4-BT-6', [('ATTEMPT', 'R', "nft add table inet p4; nft add chain inet p4 c '{ type filter hook input "
                                    "priority 0; }'; nft add rule inet p4 c tcp dport 9999 accept"),
                   ('PROBE', 'R', RULES, 'renz:dport 9999')]),
    p4('P4-BT-7', [('ATTEMPT', 'R', 'ip addr add 192.0.2.7/24 dev @DEV@'),
                   ('PROBE', 'R', 'ip -j addr', 're:192\\.0\\.2\\.7')]),
    p4('P4-BT-8', [('ATTEMPT', 'R', 'command -v nmcli && nmcli connection add type dummy ifname p4d con-name p4d'),
                   ('PROBE', 'R', 'nmcli -t c show', 're:p4d')],
       note='without NetworkManager the attempt cannot run; the outcome is then decided by the probe and CMP'),
    p4('P4-BT-9', [('ATTEMPT', 'R', 'hostnamectl set-hostname p4host'),
                   ('PROBE', 'U', 'hostname', 're:p4host'),
                   ('PROBE', 'U', 'hostnamectl --static', 're:p4host')]),
    p4('P4-BT-10', [('ATTEMPT', 'R', 'timedatectl set-timezone Asia/Tokyo'),
                    ('PROBE', 'U', 'timedatectl show -p Timezone', 're:Asia/Tokyo'),
                    ('PROBE', 'U', 'date +%Z', 're:JST')]),
    p4('P4-BT-11', [('ATTEMPT', 'R', 'localectl set-locale LANG=C.UTF-8'),
                    ('PROBE', 'U', 'localectl status', 're:LANG=C\\.UTF-8')]),
    p4('P4-BT-12', [('ATTEMPT', 'R', 'modprobe dummy'), ('PROBE', 'U', 'cat /proc/modules', 're:^dummy ')]),
    p4('P4-BT-13', [('ATTEMPT', 'R', 'sysctl -w net.ipv4.ip_forward=1'),
                    ('PROBE', 'U', 'cat /proc/sys/net/ipv4/ip_forward', 're:^1')]),
    p4('P4-BT-14', [('ATTEMPT', 'R', 'mount -t tmpfs p4 /mnt'), ('PROBE', 'U', 'grep " /mnt " /proc/mounts',
                                                                 'exit0')]),
    p4('P4-BT-15', [('ATTEMPT', 'R', 'systemctl set-property cases-svc.service CPUQuota=10%'),
                    ('PROBE', 'R', 'systemctl show -p CPUQuotaPerSecUSec cases-svc.service', 're:=100ms')]),
    dict(id='P4-SHELL', part='P4', family='steps', policy='ow', source='“The command shell is present”',
         steps=[('U', "echo $0; bash -c 'echo shell-ok'", 're:shell-ok')]),
    pipe_case('P4-PIPE-1', 'curl -fsS @HTTP@/payload.sh | bash'),
    pipe_case('P4-PIPE-2', 'bash <(curl -fsS @HTTP@/payload.sh)'),
    pipe_case('P4-PIPE-3', 'python3 -c "$(curl -fsS @HTTP@/payload.py)"'),
]

# ---------------------------------------------------------------- the successes of the search ([f6] of CORRECTIONS.md)
#
# Plan, Section 9.5: “Each success becomes a new case, committed before the next complete run … Cases are only added
# in this way, never removed or weakened.” casedefs_search.py is written by tools/make-search-cases.py from the
# tables and scripts of the search and the builder's finding; nothing of it is typed here. The attempt is the
# route's own script, sent as the search sent it; the probe is the condition of its `RESULT RAN` line; the outcome
# rule is that of every saved-code case of P4 (p4 above). `made`: what the route's typed commands create.
from casedefs_search import SEARCH_CASES  # noqa: E402

SEARCH_SRC = ('plan, Section 9.5: “Each success becomes a new case, committed before the next complete run”; and '
              'Table 9, P4: “Through every channel of [3], Section 4.3, an attempt is made to install, launch or '
              'change what is not recorded”')
for _s in SEARCH_CASES:
    _steps = [tuple(x) for x in _s['steps']]
    _first = _steps[:2] if _s.get('line_first') else []      # the line of the program the route needs, applied
    _c = p4(_s['id'], _steps[len(_first):],
            note=f"a success of the search: {_s['table']}, row {_s['row']} ({_s['program']}); attempt from "
                 f"{_s['script']}")
    _c['steps'] = _first + _c['steps']
    _c['source'] = SEARCH_SRC
    _c['made'] = [tuple(x) for x in _s['made']]
    if _s.get('tool'):
        _c['tool'] = _s['tool']
    CASES.append(_c)

# ---------------------------------------------------------------- Removal

REM_SRC = ('Table 9, Removal: “The lines of a program, a service and a rule are removed and the declaration applied; '
           'a shared object with two owners, whose lines are removed one after the other”')
CASES += [
    dict(id='REM-1', part='REM', family='steps', policy='probe', source=REM_SRC,
         steps=[('L+', 'package tmux'), ('APPLY',), ('U', 'tmux new -d -s rem sleep 86400'),
                ('CONTRIB', 'package tmux'), ('L-', 'package tmux'), ('APPLY',),
                ('PROBE', 'U', f"{PS} | grep -E '^tmux'", 'exit0'), ran('U', 'tmux -V'),
                ('OBSERVE', 'U', 'dpkg-query -W tmux'), ('INV', 'REM-1'), ('LEFTOVER', 'package tmux')]),
    dict(id='REM-2', part='REM', family='steps', policy='probe', source=REM_SRC,
         note='the service is named cases-rem because D-test already records cases-svc',
         steps=[('L+', 'service cases-rem enabled /usr/bin/sleep 86413'), ('APPLY',),
                ('U', f"{PS} | grep -xE '(/usr/bin/)?sleep 86413'"),
                ('CONTRIB', 'service cases-rem x'), ('L-', 'service cases-rem x'), ('APPLY',),
                ('PROBE', 'R', 'systemctl is-enabled cases-rem', 're:^enabled'),
                ('PROBE', 'R', 'systemctl is-active cases-rem', 're:^active'),
                proc('(/usr/bin/)?sleep 86413'), ('INV', 'REM-2'), ('LEFTOVER', 'service cases-rem x')]),
    dict(id='REM-3a', part='REM', family='steps', policy='probe', source=REM_SRC,
         note='port 8083 because D-test already records the rule of port 8081',
         steps=[('L+', "firewall cases-8083 'add rule inet confos input tcp dport 8083 accept'"), ('APPLY',),
                ('R', RULES, 're:dport 8083'),
                ('CONTRIB', 'firewall cases-8083 x'), ('L-', 'firewall cases-8083 x'), ('APPLY',),
                ('PROBE', 'R', RULES, 'renz:dport 8083'), ('INV', 'REM-3a'),
                ('LEFTOVER', 'firewall cases-8083 x')]),
    dict(id='REM-3b', part='REM', family='steps', policy='probe', source=REM_SRC,
         steps=[('L+', "sudo 'person ALL=(root) NOPASSWD: /usr/bin/true'"), ('APPLY',),
                ('R', 'sudo -l -U person', 're:/usr/bin/true'),
                ('CONTRIB', "sudo 'person ALL=(root) NOPASSWD: /usr/bin/true'"),
                ('L-', "sudo 'person ALL=(root) NOPASSWD: /usr/bin/true'"), ('APPLY',),
                ('PROBE', 'R', 'sudo -l -U person', 're:/usr/bin/true'),
                ('PROBE', 'R', 'ls /etc/sudoers.d/', 're:cases-'), ('INV', 'REM-3b'),
                ('LEFTOVER', "sudo 'person ALL=(root) NOPASSWD: /usr/bin/true'")]),
    dict(id='REM-4', part='REM', family='steps', policy='probe', source=REM_SRC,
         steps=[('L+', 'package jq'), ('L+', 'package python3-jq'), ('APPLY',),
                ('U', 'jq --version && python3 -c "import jq"'),
                ('CONTRIB', 'package jq'), ('L-', 'package jq'), ('APPLY',),
                ran('U', 'jq --version'), ('PROBE', 'U', 'python3 -c "import jq"', 'nonzero'),
                ('INV', 'REM-4a'), ('LEFTOVER', 'package jq'),
                ('CONTRIB', 'package python3-jq'), ('L-', 'package python3-jq'), ('APPLY',),
                ran('U', 'python3 -c "import jq"'),
                ('PROBE', 'U', 'ls /usr/lib/x86_64-linux-gnu/ | grep -E "^libjq\\.so"', 'exit0'),
                ('OBSERVE', 'U', 'dpkg-query -W libjq1 jq python3-jq'),
                ('INV', 'REM-4b'), ('LEFTOVER', 'package python3-jq')]),
]

# ---------------------------------------------------------------- Reproducibility, Understanding

REPRO_SRC = ('Table 9, Reproducibility: “The same declaration, all of whose lines are unambiguous, is applied to two '
             'independent clean installations; the same with two packages installed in opposite orders”')
CASES += [
    dict(id='REPRO-1', part='REPRO', family='repro1', vms=2, source=REPRO_SRC),
    dict(id='REPRO-2a', part='REPRO', family='repro2', vms=2, source=REPRO_SRC, with_ids=True),
    dict(id='REPRO-2b', part='REPRO', family='repro2', vms=2, source=REPRO_SRC, with_ids=False),
    dict(id='UND-0', part='UND', family='und0', vms=0,
         source='Table 9, Understanding: “From the declaration alone, without access to the machine, a published '
                'program derives what must be installed and the value of every setting”'),
]

# ---------------------------------------------------------------- what the person's own commands made
#
# [n2-3]. S8.2-15: “if a person created or brought the object, it is material—documents, photographs,
# projects, downloaded files, private keys and passwords for logging in to other machines”; S8.2-4: “A command that
# a person typed himself or herself is that person’s action, not an object.” For each case: the objects that the
# person's own typed commands create or bring — `mkdir`, a shell redirection, `curl -o`, `cp`, `tar x`, `git init`,
# `ssh-keygen`, a compiler run at the person's command — never the products of a channel's installer (pip, npm,
# Flatpak, apt, podman, `make install`), which are decided as before. Each entry: (TYPE, PATH GLOB), `~/` the home
# of the account `person`, `~root/` that of root. TYPE `data`: material unless a direct route executes it (item 4,
# R1); `obeyed`: a startup file, unit file, hook or alias, material unless something obeys it (a probe of the case
# shows it in force since the last restart) or a direct route executes it. compare applies them (FORMATS.md,
# "Additions of 2026-11-24, 11:45–13:50 UTC"); they are taken through the four questions there, in their order.
D = 'data'
O = 'obeyed'
MADE = {
    'OW-4': [(D, '~/shot.png'), (D, '~/local.png')],
    'OW-5': [(D, '~/doc.txt'), (D, '~/doc.odt')],
    'OW-6': [(D, '~/h')],
    'OW-7': [(D, '~/src'), (D, '~/src/hello.c')],
    'OW-8': [(D, '~/game'), (D, '~/game/linuxgsm.sh')],
    'P4-C1-1': [(D, '~/hello_*.deb')],
    'P4-C1-3': [(D, '~root/hello_*.deb')],
    'P4-C1-6': [(D, '~/hello_*.deb'), (D, '~/x'), (D, '~/x/**')],
    'P4-C2-4': [(D, '~/w'), (D, '~/w/*.whl')],
    'P4-C3-2': [(D, '~/p')],
    'P4-C5-1': [(D, '~/nvim.appimage')],
    'P4-C5-2': [(D, '~/nvim.appimage')],
    'P4-C6-1': [(D, '~/jq')], 'P4-C6-2': [(D, '/tmp/jq')], 'P4-C6-3': [(D, '/dev/shm/jq')],
    'P4-C6-4': [(D, '/var/tmp/jq')], 'P4-C6-5': [(D, '/usr/local/bin/jq')],
    'P4-C6-6': [(D, '~/rg.tgz'), (D, '~/ripgrep-14.1.1-x86_64-unknown-linux-musl'),
                (D, '~/ripgrep-14.1.1-x86_64-unknown-linux-musl/**')],
    'P4-C7-1': [(D, '~/h.tgz'), (D, '~/hello-2.12.1'), (D, '~/hello-2.12.1/**')],
    'P4-C7-2': [(D, '~/t.c'), (D, '~/t')],
    'P4-C7-3': [(D, '/tmp/t.c'), (D, '/tmp/t'), (D, '/dev/shm/t')],
    'P4-C8-1': [(D, '~/.config'), (D, '~/.config/systemd'), (D, '~/.config/systemd/user'),
                (O, '~/.config/systemd/user/p4.service')],
    'P4-C8-4': [(D, '~/ct')],
    'P4-C8-5': [(D, '~root/ct')],
    'P4-C8-6': [(O, '~root/p4root.service')],
    'P4-C9-1': [(D, '~/f.sh'), (D, '/tmp/f.sh'), (D, '/dev/shm/f.sh')],
    'P4-C9-2': [(D, '~/f.py'), (D, '/tmp/f.py'), (D, '/dev/shm/f.py')],
    'P4-C9-3': [(D, '~/f.pl'), (D, '/tmp/f.pl'), (D, '/dev/shm/f.pl')],
    'P4-C9-4': [(D, '~/s.sh')],
    'P4-C9-5': [(D, '~/tru')],
    'P4-C10-1': [(O, '~/.bashrc')],
    'P4-C10-2': [(O, '~/.profile')],
    'P4-C10-3': [(O, '~/.gitconfig')],
    'P4-C10-4': [(D, '~/r'), (D, '~/r/**'), (D, '~/hooks'), (O, '~/hooks/pre-commit')],
    'P4-C10-5': [(D, '~/.config'), (D, '~/.config/autostart'), (O, '~/.config/autostart/p4.desktop')],
    'P4-C10-6': [(O, '~/.ssh/rc')],
    'P4-C10-7': [(D, '~/k'), (D, '~/k.pub'), (O, '~/.ssh/authorized_keys')],
    'P4-C11-3': [(D, '~/Containerfile')],
    'P4-C11-4': [(D, '~/.config'), (D, '~/.config/containers'), (D, '~/.config/containers/systemd'),
                 (O, '~/.config/containers/systemd/p4q.container')],
    'P4-BT-5': [(D, '/tmp/s')],
}
for _p in ('P4-PIPE-1', 'P4-PIPE-2', 'P4-PIPE-3'):
    # the payload is code that the person had executed; what it saved is decided like what the person saves
    MADE[_p] = [(D, '~/jq'), (D, '~/.config'), (D, '~/.config/systemd'), (D, '~/.config/systemd/user'),
                (O, '~/.config/systemd/user/cases-pipe.service'), (O, '~/.bashrc')]
for _c in CASES:
    if _c['id'] in MADE:
        _c['made'] = MADE[_c['id']]

# ---------------------------------------------------------------- rows evaluated under both readings (item 6)
#
# S8.3-7, “Its tools for installation and configuration record changes in the declaration even when they run with
# superuser privileges: an installer does not install a program past the declaration but adds it to the
# declaration”, is not decided by the review (REVIEW.md; build/QUESTIONS.md 1): reading A, the built-in tool's
# refusal suffices; reading B, the tool must add the line. A P4 case whose attempt is made with a built-in tool
# (S8.1-7: an installer, account and rights management, the service manager, network and access rule
# configuration, and the system's tools for its other settings) and that is met only because the tool refused is
# met under A and not under B: `undecided` (S8.3-7). The tool of each such case:
TOOL = {}
for _cid, _tool in [
        ('P4-C1-1', 'apt-get'), ('P4-C1-2', 'apt-get'), ('P4-C1-3', 'dpkg'), ('P4-C1-4', 'apt-get'),
        ('P4-C1-5', 'dpkg'), ('P4-C1-6', 'dpkg-deb'), ('P4-C2-1', 'pip'), ('P4-C2-2', 'venv, pip'),
        ('P4-C2-3', 'pip'), ('P4-C2-4', 'pip'), ('P4-C3-1', 'npm'), ('P4-C3-2', 'npm'), ('P4-C3-3', 'npx'),
        ('P4-C3-4', 'npm'), ('P4-C4-1', 'flatpak'), ('P4-C4-2', 'flatpak'), ('P4-C4-3', 'flatpak'),
        ('P4-C8-1', 'systemctl --user'), ('P4-C8-2', 'systemd-run --user'), ('P4-C8-3', 'systemd-run --user'),
        ('P4-C8-4', 'crontab'), ('P4-C8-5', 'crontab'), ('P4-C8-6', 'systemctl'), ('P4-C8-7', 'systemctl'),
        ('P4-C8-8', 'loginctl'), ('P4-C8-9', 'at'), ('P4-C11-1', 'podman'), ('P4-C11-2', 'podman'),
        ('P4-C11-3', 'podman'), ('P4-C11-4', 'systemctl --user (quadlet)'), ('P4-BT-1', 'useradd'),
        ('P4-BT-2', 'usermod'), ('P4-BT-3', 'chpasswd'), ('P4-BT-4', 'groupadd'), ('P4-BT-5', 'visudo'),
        ('P4-BT-6', 'nft'), ('P4-BT-7', 'ip'), ('P4-BT-8', 'nmcli'), ('P4-BT-9', 'hostnamectl'),
        ('P4-BT-10', 'timedatectl'), ('P4-BT-11', 'localectl'), ('P4-BT-12', 'modprobe'), ('P4-BT-13', 'sysctl'),
        ('P4-BT-14', 'mount'), ('P4-BT-15', 'systemctl set-property'), ('P4-PIPE-1', 'systemctl --user, crontab'),
        ('P4-PIPE-2', 'systemctl --user, crontab'), ('P4-PIPE-3', 'systemctl --user, crontab')]:
    TOOL[_cid] = _tool
# Q6: a direct write by root with a general-purpose program (a breaking candidate under S8.1-15). Reading A, it is
# breaking and does not count; reading B, it counts. A row that fails only on what that write did is `undecided`
# (Q6). P4-C6-5: the whole attempt; P4-BT-5: the first attempt (its probe and the file it writes).
Q6_ALL = {'P4-C6-5'}
Q6_PROBES = {'P4-BT-5': ['re:\\(ALL\\) NOPASSWD: ALL']}
Q6_PATHS = {'P4-BT-5': ['/etc/sudoers.d/p4']}
for _c in CASES:
    if _c['id'] in TOOL:
        _c['tool'] = TOOL[_c['id']]

# Rows generated by the runner (not cases of their own): one per application and one per inventory.
GENERATED = ['P2-1:*', 'UND:<TAG>', 'P1:<TAG>']

IDS = [c['id'] for c in CASES]
assert len(IDS) == len(set(IDS)), 'duplicate case IDs'
BY_ID = {c['id']: c for c in CASES}

# Test-only cases: not in CASES.md, never part of a run unless named with --only. They are the experiment that the
# P4 measure of the effect of an attempt (run: attempt_effect) works on the implementation itself: an attempt that
# plants an unrecorded file in the home directory and a running process, with no probe, must give `fail` with both in
# attempt-effect.tsv; an attempt that does nothing must give `pass` (two inventories of one machine add no noise).
TEST_CASES = [
    p4('P4-T-PLANT', [('ATTEMPT', 'U', 'echo planted > ~/planted-by-test && '
                                       '(setsid sleep 86499 </dev/null >/dev/null 2>&1 &)')]),
    p4('P4-T-NOOP', [('ATTEMPT', 'U', 'true')]),
]
# [n2-7], the specificity test: on a clean installation with the test declaration, an application of
# the unchanged declaration (a P2 row), then what a person ordinarily leaves — a directory made with mkdir, a saved
# text document, an archive of sources downloaded into the home directory — and the two refused attempts of P4-BT-5.
# No row of P1, P2 or P4 may be `fail` (selftest/specificity/test.sh).
_SPEC = p4('P4-T-SPEC', [
    ('ATTEMPT', 'U', 'mkdir -p ~/p'),
    ('ATTEMPT', 'U', "printf 'A text document, saved by the person.\\nSecond line.\\n' > ~/doc.txt"),
    ('ATTEMPT', 'U', f'curl -fsSLo ~/hello-2.12.1.tar.gz {GNU_HELLO_URL}'),
] + [s for s in BY_ID['P4-BT-5']['steps'] if s[0] in ('ATTEMPT', 'PROBE')])
_SPEC['steps'] = [('APPLY',)] + _SPEC['steps']
_SPEC['made'] = [(D, '~/p'), (D, '~/doc.txt'), (D, '~/hello-2.12.1.tar.gz'), (D, '/tmp/s')]
_SPEC['tool'] = TOOL['P4-BT-5']
Q6_PROBES['P4-T-SPEC'] = Q6_PROBES['P4-BT-5']
Q6_PATHS['P4-T-SPEC'] = Q6_PATHS['P4-BT-5']
# A code test of item 4: a saved shell script, a saved JavaScript file and a copied program in the home directory are
# code if a direct route of their form executes them (R1); the row must be `fail` exactly when one does, with the route
# in routes.tsv. (The script is refused by the code readers of ConfOS 0.27+; Node is confined only from 0.30.)
_CODE = p4('P4-T-CODE', [('ATTEMPT', 'U', "printf 'echo cases-code-ran\\n' > ~/code.sh && "
                                        "printf 'console.log(\"cases-code-ran\");\\n' > ~/code.js && "
                                        "cp /usr/bin/true ~/tru2")])
_CODE['made'] = [(D, '~/code.sh'), (D, '~/code.js'), (D, '~/tru2')]
TEST_CASES += [_SPEC, _CODE]
# [n3-A]: the four questions must not lose sensitivity. Each planted object below must make its row
# `fail` through its question (attempt-effect.tsv names it), and the last must not (selftest/specificity/check.py).
# P4-T-PLANT plants a Python module into the person's package store of pip (question 1: whatever a system does with
# code, an object of a package store counts once it is there) and a running process of a recorded program.
TEST_CASES[0]['steps'][1] = ('ATTEMPT', 'U', "mkdir -p ~/.local/lib/python3.13/site-packages && echo 'PLANTED = 1' > "
                                             "~/.local/lib/python3.13/site-packages/planted-by-test.py && "
                                             "(setsid sleep 86499 </dev/null >/dev/null 2>&1 &)")
# Question 1: a Python package unpacked by hand into the person's package store of pip (as a wheel is installed),
# past the declaration; no probe, so only the comparison can make the row fail.
_Q1 = p4('P4-T-Q1', [('ATTEMPT', 'U', "d=~/.local/lib/python3.13/site-packages && mkdir -p $d/cases_planted "
                                      "$d/cases_planted-1.0.dist-info && printf 'VALUE = 1\\n' > "
                                      "$d/cases_planted/__init__.py && printf 'Metadata-Version: 2.1\\nName: "
                                      "cases-planted\\nVersion: 1.0\\n' > $d/cases_planted-1.0.dist-info/METADATA && "
                                      "printf 'pip\\n' > $d/cases_planted-1.0.dist-info/INSTALLER && : > "
                                      "$d/cases_planted-1.0.dist-info/RECORD")])
# Question 3: a user unit put in force by every way open to the person (its file in the configuration and runtime
# folders of the account's service manager, enabled by a symlink, the manager told to reload by systemctl, by D-Bus and
# by a signal to the person's own manager process, then started). No probe: only the comparison can make the row fail.
_Q3_UNIT = "[Unit]\\nDescription=cases-q3\\n[Service]\\nExecStart=/usr/bin/sleep 86497\\n[Install]\\nWantedBy=default.target\\n"
_Q3 = p4('P4-T-Q3', [
    ('ATTEMPT', 'U', f"mkdir -p ~/.config/systemd/user/default.target.wants && printf '{_Q3_UNIT}' > "
                     "~/.config/systemd/user/cases-q3.service && ln -sf ../cases-q3.service "
                     "~/.config/systemd/user/default.target.wants/cases-q3.service"),
    ('ATTEMPT', 'U', f"mkdir -p /run/user/$(id -u)/systemd/user && printf '{_Q3_UNIT}' > "
                     "/run/user/$(id -u)/systemd/user/cases-q3r.service"),
    ('ATTEMPT', 'U', 'export XDG_RUNTIME_DIR=/run/user/$(id -u) DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus; '
                     'systemctl --user daemon-reload; busctl --user call org.freedesktop.systemd1 '
                     '/org/freedesktop/systemd1 org.freedesktop.systemd1.Manager Reload; '
                     'pkill -HUP -u "$(id -u)" -x systemd; sleep 3; '
                     'systemctl --user start cases-q3.service cases-q3r.service; busctl --user call '
                     'org.freedesktop.systemd1 /org/freedesktop/systemd1 org.freedesktop.systemd1.Manager StartUnit ss '
                     'cases-q3.service replace; sleep 2; systemctl --user list-units --all "cases-q3*" --no-pager'),
])
# Not counted: a file that a recorded program (gpg, package `gpg`) writes into its own working folder under the home
# directory (S8.2-15, program record). The row must not be `fail`.
_WORK = p4('P4-T-WORK', [('ATTEMPT', 'U', 'gpg --batch --list-keys; ls -la ~/.gnupg')])
TEST_CASES += [_Q1, _Q3, _WORK]
for _c in TEST_CASES:
    _c['test_only'] = True
    BY_ID[_c['id']] = _c
