"""The cases of CASES-EXTRA.md as data, for `run-extra`. Not read by `run` or by a complete run.

Second form (2026-11-24, for release 0.43): the requests are the command forms that the implementation documents as
recording (build/CHOICES.md, table “S8.3-7 recording choice”; build/INTERFACE.md revisions 34–43;
build/CONFIGURATION-RECORDING-DRAFT.md), and the radio cases use the implementation's own simulated radios and its
rows `radio-fixture`, `network`, `bluetooth-pair` (build/DECLARATION.md revision 40, the release's
`radio-public-fixture/`). The first form (written before the implementation recorded anything) is kept in
scraps/f5/casedefs_extra.py.before.

X-REC case keys:
  add / remove     the request to the tool and the removal request, as root (`sudo -n`, the documented means)
  expect_added     regexes: every line the request adds to the declaration text must match one, and each regex must
                   match exactly one added line (the line the tool must write, and nothing else)
  expect_removed   the same for the lines the request takes out (a changed line is one removed and one added)
  restore_ok       regexes of lines that may differ from the text before the request once the removal request is
                   recorded (a value the declaration did not record before, now recorded at its former value)
  probes           (who, command, test): must not hold before the application, must hold after it, and must not hold
                   after the removal is applied (test as in casedefs: exit0, re:REGEX, ...)
  setup            (op, spec) added or removed and applied before step 1; op L+ or L-
  put              (source, guest path): a file the person has on the machine before the request (source
                   `input:NAME` = the pinned inputs of tools/make-inputs.sh)
  late             {@NAME@: command}: read on the machine as root after the application, substituted in `remove`
  builder_names    True when build/CHOICES.md names the tool and the request form as recording

The spec kind `builder-line 'LINE' REL=SOURCE ...` (run-extra only) is a line in the builder's own syntax, with its
content files: SOURCE `release:PATH` (a file of the published source of the release under test) or `input:NAME`.
"""
import re

PS = 'ps -eo args='
SRC_REC = ('S8.3-7: “Its tools for installation and configuration record changes in the declaration even when they '
           'run with superuser privileges: an installer does not install a program past the declaration but adds it '
           'to the declaration.”')
H64 = '[0-9a-f]{64}'


def xrec(cid, tool, add, probes, remove, expect_added, expect_removed=(), restore_ok=(), setup=(), put=(), late=None,
         builder_names=True, run=True):
    return dict(id=cid, part='X-REC', family='xrec', tool=tool, add=add, probes=probes, remove=remove,
                expect_added=list(expect_added), expect_removed=list(expect_removed), restore_ok=list(restore_ok),
                setup=list(setup), put=list(put), late=late or {}, builder_names=builder_names, source=SRC_REC,
                run=run)


# The runtime and application bundles that release 0.43 accepts for this commit: the builder's own exports
# (build/STATE.md, “flatpak-inputs/”; flatpak_readers.py refuses any other bundle of the same commit, DEV-14.md)
RUNTIME = ('flatpak runtime/org.freedesktop.Platform/x86_64/26.08 '
           'df26daaf9d07610b4a72cc4585566194051275ac68396597b06474396f66427c '
           '072d80f7f24a5c5ff75e2c244fdd5aea032216fcb6e6138af175e18ee76054e3 files/runtime.flatpak')
MPV_BUNDLE = '66d65390ff1b7a526b25a448f12d137f72df5859460c1d05e17508ed6a88bed9'

CASES = [
    # ------------------------------------------------------------------ installers (CHOICES.md, from 0.34–0.37)
    xrec('X-REC-APT', 'apt-get', 'apt-get install -y hello',
         [('U', 'hello --version', 'exit0'), ('U', "dpkg-query -W -f '${db:Status-Abbrev}' hello", 're:^ii')],
         'apt-get remove -y hello', [r'^package hello \S+$']),
    xrec('X-REC-APT2', 'apt', 'apt install -y hello',
         [('U', 'hello --version', 'exit0'), ('U', "dpkg-query -W -f '${db:Status-Abbrev}' hello", 're:^ii')],
         'apt purge -y hello', [r'^package hello \S+$']),
    xrec('X-REC-PIP', 'pip', 'pip install --break-system-packages pyjokes==0.8.3',
         [('U', 'pyjoke', 'exit0'), ('U', 'python3 -m pip show pyjokes', 're:Version: 0\\.8\\.3')],
         'pip uninstall -y pyjokes', [rf'^pip pyjokes 0\.8\.3 {H64} \S+$']),
    xrec('X-REC-NPM', 'npm', 'npm install -g semver@7.6.3',
         # where the implementation installs a recorded global npm package (the inventory of dev-14-extra, X-REC-NPM)
         [('U', "grep -h '\"version\"' /opt/confos/npm/semver/node_modules/semver/package.json", 're:7\\.6\\.3'),
          ('U', "node -e 'process.exit(require(\"/opt/confos/npm/semver/node_modules/semver\").valid(\"1.2.3\") ? 0 : 1)'",
           'exit0')],
         'npm uninstall -g semver', [rf'^npm semver 7\.6\.3 {H64} \S+$']),
    xrec('X-REC-FLATPAK', 'flatpak', 'flatpak install -y --bundle /home/person/mpv.flatpak',
         [('U', 'flatpak list --app --columns=application', 're:io\\.mpv\\.Mpv'),
          ('U', 'flatpak info io.mpv.Mpv', 'exit0')],
         'flatpak uninstall -y io.mpv.Mpv',
         [rf'^flatpak app/io\.mpv\.Mpv/x86_64/stable {H64} {MPV_BUNDLE} \S+$'],
         # the declaration of the run has no flatpak line (D-test-noflatpak.spec); the runtime is recorded first (“An
         # application requires its runtime already recorded”, INTERFACE.md revision 36)
         setup=[('L+', f"builder-line '{RUNTIME}' files/runtime.flatpak=build:flatpak-inputs/runtime.flatpak")],
         put=[('build:flatpak-inputs/mpv.flatpak', '/home/person/mpv.flatpak')]),
    xrec('X-REC-PODMAN', 'podman', 'podman pull docker.io/library/busybox:1.36.1',
         [('U', 'podman images', 're:busybox'),
          ('U', 'podman run --rm docker.io/library/busybox:1.36.1 true', 'exit0')],
         'podman rmi docker.io/library/busybox:1.36.1',
         [rf'^container person docker\.io/library/busybox:1\.36\.1 {H64} {H64} \S+$']),
    # ------------------------------------------------------------------ configuration tools (from 0.38, nft 0.43)
    xrec('X-REC-HOST', 'hostnamectl', 'hostnamectl set-hostname xrechost',
         [('U', 'hostnamectl --static', 're:^xrechost'), ('U', 'hostname', 're:^xrechost')],
         'hostnamectl set-hostname @HOST0@', [r'^setting hostname xrechost$'], [r'^setting hostname \S+$']),
    xrec('X-REC-TIME', 'timedatectl', 'timedatectl set-timezone UTC',
         [('U', 'cat /etc/timezone', 're:^UTC$')],
         'timedatectl set-timezone @TZ0@', [r'^setting timezone UTC$'], [r'^setting timezone \S+$']),
    xrec('X-REC-SYSCTL', 'sysctl', 'sysctl -w net.ipv4.ip_forward=1',
         [('U', 'sysctl -n net.ipv4.ip_forward', 're:^1')],
         'sysctl -w net.ipv4.ip_forward=@FWD0@', [r'^setting sysctl:net\.ipv4\.ip_forward 1$'],
         restore_ok=[r'^setting sysctl:net\.ipv4\.ip_forward @FWD0@$']),
    xrec('X-REC-ENABLE', 'systemctl enable', 'systemctl enable cases-xrec',
         [('U', f"{PS} | grep -xE '(/usr/bin/)?sleep 86412'", 'exit0')],
         'systemctl disable cases-xrec', [r'^service cases-xrec enabled /usr/bin/sleep 86412$'],
         [r'^service cases-xrec disabled /usr/bin/sleep 86412$'],
         setup=[('L+', 'service cases-xrec disabled /usr/bin/sleep 86412')]),
    xrec('X-REC-UENABLE', 'systemctl --user disable', 'systemctl --user disable cases-tick.timer',
         [('U', 'systemctl --user is-enabled cases-tick.timer', 're:^disabled')],
         'systemctl --user enable cases-tick.timer', [rf'^user-unit person cases-tick\.timer disabled {H64} \S+$'],
         [rf'^user-unit person cases-tick\.timer enabled {H64} \S+$']),
    xrec('X-REC-USER', 'useradd, userdel', 'useradd -m xrecuser',
         [('U', 'getent passwd xrecuser', 'exit0')],
         'userdel xrecuser', [r'^account xrecuser 1001 1001 - /bin/bash /home/(xrecuser)$']),
    xrec('X-REC-USERMOD', 'usermod', 'usermod -s /bin/sh xrecmod',
         [('U', 'getent passwd xrecmod', 're::/bin/sh$')],
         'usermod -s /bin/bash xrecmod', [r'^account xrecmod 1500 1500 - /bin/sh /home/(xrecmod)$'],
         [r'^account xrecmod 1500 1500 - /bin/bash /home/(xrecmod)$'],
         setup=[('L+', 'account xrecmod uid=1500 gid=1500 groups=- shell=/bin/bash')]),
    xrec('X-REC-NFT', 'nft', 'nft add rule inet confos input tcp dport 9998 accept',
         [('R', 'nft list ruleset', 're:tcp dport 9998 accept')],
         'nft delete rule inet confos input handle @HANDLE@', [r'^rule \S+ .*tcp dport 9998 accept'],
         late={'@HANDLE@': "nft -a list ruleset | sed -n 's/.*tcp dport 9998 accept.*# handle \\([0-9]*\\).*/\\1/p' "
                           "| head -1"}),
    # ------------------------------------------------------------------ tools that build/CHOICES.md names as refusing
    # (rows “configuration tools … refuses; S8.3-7 incomplete”, “groupadd; … localectl, modprobe …”, visudo from 0.44):
    # defined, not performed on 0.43 (the order of the development run names the recording tools)
    xrec('X-REC-LOCALE', 'localectl', 'localectl set-locale LANG=C.UTF-8',
         [('U', 'localectl status', 're:LANG=C\\.UTF-8')], 'localectl set-locale @LANG0@', [r'(?i)locale|LANG='],
         builder_names=False, run=False),
    xrec('X-REC-GROUP', 'groupadd', 'groupadd xrecgroup', [('U', 'getent group xrecgroup', 'exit0')],
         # groupadd records from 0.50 (build/CHOICES.md of 0.52: “groupadd [-g GID] NAME; groupdel NAME | `group NAME
         # GID` … | records from 0.50”)
         'groupdel xrecgroup', [r'xrecgroup'], builder_names=True, run=True),
    # visudo records from 0.44 (build/CHOICES.md of 0.49: “visudo | [-f /etc/sudoers.d/NAME]; --remove … | records
    # from44”; VISUDO-RECORDING-DRAFT.md: `EDITOR='tee -a' visudo` edits the snippet /etc/sudoers.d/confos-local)
    xrec('X-REC-SUDO', 'visudo', "printf 'person ALL=(root) NOPASSWD: /usr/bin/true\\n' | EDITOR='tee -a' visudo",
         [('R', 'sudo -l -U person', 're:NOPASSWD: /usr/bin/true')], 'visudo --remove', [r'^file /etc/sudoers\.d/'],
         builder_names=True, run=True),
    xrec('X-REC-MODULE', 'modprobe', 'modprobe dummy', [('U', 'grep -w ^dummy /proc/modules', 'exit0')],
         # modprobe records from 0.50 (build/CHOICES.md of 0.52: “modprobe NAME; modprobe -r NAME | `setting
         # module:NAME loaded` … | records from 0.50; the module is loaded at every start after the application”)
         'modprobe -r dummy', [r'\bdummy\b'], builder_names=True, run=True),
    xrec('X-REC-LINGER', 'loginctl', 'loginctl enable-linger person',
         [('U', 'loginctl show-user person -p Linger', 're:Linger=yes')], 'loginctl disable-linger person',
         [r'(?i)linger'], builder_names=False, run=False),
]

# The values that the removal requests of the configuration tools restore: read from the machine before step 1
# (the value DECL0 gives), substituted for @NAME@ in `remove` and `restore_ok`.
RESTORE = {
    '@HOST0@': 'hostnamectl --static',
    '@TZ0@': 'cat /etc/timezone',
    '@LANG0@': "localectl status | sed -n 's/^ *System Locale: *//p' | head -1",
    '@FWD0@': 'sysctl -n net.ipv4.ip_forward',
}

SRC_WIFI = ('plan Section 9.3, ordinary work, “connecting to a Wi-Fi network”; S8.2-13: “Settings are services and '
            'their parameters, the network, including saved networks, …”')
SRC_BT = 'plan Section 9.3, ordinary work, “pairing a Bluetooth device”; S8.2-13: “… devices …”'

# build/DECLARATION.md revision 40: the packages of radio-public-fixture/packages.conf that D-test does not already
# record, at their versions, and the fixture row with its input file from the published source of the release
RADIO_PACKAGES = ['bluez=5.82-1.1', 'bluez-test-tools=5.82-1.1', 'hostapd=2:2.10-24', 'wpasupplicant=2:2.10-24',
                  'iw=6.9-1', 'wireless-regdb=2026.09.03-1~deb13u1', 'dbus=1.16.2-2', 'python3-dbus=1.4.0-1',
                  'python3-gi=3.50.0-4+b1', 'iputils-ping=3:20240905-3']
FIX = 'release:radio-public-fixture/'
RADIO_FIXTURE = ([f'package {p}' for p in RADIO_PACKAGES] +
                 [f"builder-line 'radio-fixture lab 8c0d7645b676e60da88d8ced9f3742f3603ffbf23d2b711e324df4bc47babc67 "
                  f"fixture.json' fixture.json={FIX}fixture.json"])
INSPECT_WIFI = 'confos radio-inspect wifi'
INSPECT_BT = 'confos radio-inspect bluetooth'

CASES += [
    dict(id='X-WIFI', part='X-WIFI', family='xradio', source=SRC_WIFI, run=True,
         fixture=RADIO_FIXTURE,
         fixture_check=('R', INSPECT_WIFI, 're:type AP'),
         # the person connects with the built-in tool. From release 0.45 the implementation records this request of
         # nmcli (build/CHOICES.md of 0.49, “Revision45 Wi-Fi request choices”: the add syntax with every property
         # required); the values are those of the published fixture (radio-public-fixture/client.json: ssid_hex
         # 436f6e664f532d726164696f2d66697874757265, psk, address 192.0.2.2/24). The removal is the tool's own
         # request (`nmcli connection delete id NAME`). `lines` is the row written by hand only if the tool writes
         # none (release 0.43, DECLARATION.md rev. 40).
         connect=('R', 'command -v nmcli; nmcli connection add type wifi ifname wlan1 autoconnect yes '
                       'con-name casesnet ssid ConfOS-radio-fixture wifi-sec.key-mgmt wpa-psk wifi-sec.proto rsn '
                       'wifi-sec.pairwise ccmp wifi-sec.group ccmp '
                       'wifi-sec.psk 043558ba09d4c96be30002e16c8125fe10633c75dea9f1e436844b34bc35460f '
                       'ipv4.method manual ipv4.addresses 192.0.2.2/24'),
         disconnect=('R', 'nmcli connection delete id casesnet'),
         lines=["builder-line 'network saved ed8415df4da909cd7a4889bc1bfacda86237c01fdb7f3fa605ceacbae59a493e "
                f"client.json' client.json={FIX}client.json"],
         connected=('R', INSPECT_WIFI, 're:Connected to 02:00:00:00:00:00 \\(on wlan1\\)'),
         stored=('R', 'test -f /usr/lib/confos/radio/wpa.conf', 'exit0'),
         wait=180),
    dict(id='X-BT', part='X-BT', family='xradio', source=SRC_BT, run=True,
         fixture=RADIO_FIXTURE,
         fixture_check=('R', INSPECT_BT, 're:00:AA:01:01:00:01'),
         connect=('R', "printf 'select 00:AA:01:00:00:00\\npair 00:AA:01:01:00:01\\n' | timeout 30 bluetoothctl"),
         lines=["builder-line 'bluetooth-pair 00:AA:01:00:00:00 00:AA:01:01:00:01 "
                "d64093eaddc1a6d392b4f9707b7bbaaa64af072df3a96cdba305fc472931108b 00AA01000000.info' "
                f"00AA01000000.info={FIX}00AA01000000.info",
                "builder-line 'bluetooth-pair 00:AA:01:01:00:01 00:AA:01:00:00:00 "
                "0dd10ad01633603b9c537ae709020274d9eb0ba3b4d137f48992730e6f1e83d4 00AA01010001.info' "
                f"00AA01010001.info={FIX}00AA01010001.info"],
         connected=('R', INSPECT_BT, 're:"Paired": 1'),
         stored=('R', 'test -f /usr/lib/confos/radio/bluez/00:AA:01:00:00:00/00:AA:01:01:00:01/info', 'exit0'),
         wait=180),
]

IDS = [c['id'] for c in CASES]
BY_ID = {c['id']: c for c in CASES}
RUN_IDS = [c['id'] for c in CASES if c.get('run', True)]
assert all(re.compile(p) for c in CASES if c['family'] == 'xrec' for p in c['expect_added'])
