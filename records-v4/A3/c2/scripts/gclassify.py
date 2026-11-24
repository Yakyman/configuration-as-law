#!/usr/bin/env python3
"""Member-level rules for part-gaming (classification c2). The rules are stated in A3/c2/part-gaming.notes.md.

classify(m) -> (decision, sentences, what, basis, reason, label)
m: dict with keys path, type, exec, ctime, pkg, integrity, target, size, persistence."""
import os, re

H = '/home/user'
END_DPKG = '2026-11-23T11:16:12'      # last dpkg run ended (dpkg/info ctimes end 11:16:07; Steam launch 11:16:12)
STEAMCMD_TAR = '2026-11-23T11:18:20'  # steamcmd tarball extracted 11:18:13; self-update writes from 11:18:2x
LOG = 'raw:A3/in/operator/gaming/actions-logs/actions-logs/'

DOC_STEAM_UNINSTALL = 'doc:https://help.steampowered.com/en/faqs/view/1A06-BC6C-B2EA-1FD2'
DOC_STEAMCMD = 'doc:https://web.archive.org/web/20261120003630/https://developer.valvesoftware.com/wiki/SteamCMD'
DOC_LUTRIS = 'doc:https://manpages.debian.org/testing/lutris/lutris.1'
DOC_WINE = "doc:https://gitlab.winehq.org/wine/wine/-/wikis/Wine-User's-Guide"
DOC_UPDALT = 'doc:https://manpages.debian.org/trixie/dpkg/update-alternatives.1.en.html'
DOC_CA = 'doc:https://manpages.debian.org/trixie/ca-certificates/update-ca-certificates.8.en.html'
DOC_PAM = 'doc:https://manpages.debian.org/trixie/libpam-runtime/pam-auth-update.8.en.html'
DOC_MESA = 'doc:https://docs.mesa3d.org/envvars.html'
DOC_GEN = 'doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.generator.html'
DOC_FLATPAK = 'doc:https://docs.flatpak.org/en/latest/flatpak-command-reference.html'

LINUX_CODE_EXT = {'.sh', '.py', '.pl', '.so', '.bash', '.js', '.mjs', '.cjs', '.lua'}
WIN_CODE_EXT = {'.dll', '.exe', '.drv', '.sys', '.ocx', '.cpl', '.acm', '.ax', '.ds', '.com', '.vxd', '.mod',
                '.dll16', '.exe16', '.drv16'}


def ext(p):
    b = os.path.basename(p)
    return ('.' + b.rsplit('.', 1)[1].lower()) if '.' in b.lstrip('.') else ''


def is_code(p, typ, exe, shebang='False'):
    """Code: a code extension (ELF library, script, Windows PE), a '#!' first line, or an executable
    file without extension. Data extensions (png, svg, xml, txt...) are data even when mode bits say executable."""
    if typ != 'file':
        return False
    b = os.path.basename(p)
    e = ext(p)
    if re.search(r'\.so(\.|$)', b) or e in LINUX_CODE_EXT or e in WIN_CODE_EXT:
        return True
    if shebang == 'True':
        return True
    return e == '' and exe == 'True'


def R(dec, sent, what, basis, reason, label=None):
    return (dec, sent, what, basis, reason, label or what)


# ------------------------------------------------------------------ system side
def runtime_creator(p):
    table = [
        ('/run/systemd/generator', 'systemd generators (package systemd)'),
        ('/run/systemd', 'systemd service manager (package systemd)'),
        ('/run/udev', 'systemd-udevd (package udev)'),
        ('/run/NetworkManager', 'NetworkManager (package network-manager)'),
        ('/run/user/1000/systemd', 'user service manager systemd (package systemd)'),
        ('/run/user/113/systemd', 'user service manager systemd (package systemd)'),
        ('/run/user/1000/pulse', 'pipewire-pulse (package pipewire-pulse)'),
        ('/run/user/113/pulse', 'pipewire-pulse (package pipewire-pulse)'),
        ('/run/user', 'systemd-logind and session daemons (packages systemd, gnupg, gnome-keyring, dbus)'),
        ('/run/avahi-daemon', 'avahi-daemon (package avahi-daemon)'),
        ('/run/cups', 'cupsd (package cups-daemon)'),
        ('/run/dbus', 'dbus-daemon (package dbus-daemon)'),
        ('/run/lightdm', 'lightdm (package lightdm)'),
        ('/run/speech-dispatcher', 'speech-dispatcher (package speech-dispatcher)'),
        ('/run/irqbalance', 'irqbalance (package irqbalance)'),
    ]
    for pre, who in table:
        if p == pre or p.startswith(pre + '/'):
            return who
    return 'the daemon or boot step named in its path (systemd, udev, util-linux and others; packages installed)'


ETC = {
    '/etc/.pwd.lock': ('RECORD', 'S8.2-15', 'lock file of the shadow tools', 'evidence', 'Written by account tools as they ran: working state.'),
    '/etc/.resolv.conf.systemd-resolved.bak': ('RECORD', 'S8.2-15', 'backup of resolver config made by a maintainer script', 'raw:configuration-origin.tsv', 'Backup written by systemd-resolved maintainer script as it ran: program record.'),
    '/etc/.updated': ('RECORD', 'S8.2-15', 'stamp written by systemd-update-done', 'evidence', 'Timestamp written by a program as it ran.'),
    '/etc/adjtime': ('SETTING-OWN', 'S8.2-11,S8.2-12,S8.2-13,S8.2-17', 'hardware clock mode (time setting)', 'evidence', 'Time setting the whole computer obeys, written at OS installation (04:40:51) with the person\'s timezone choice; not a package default.'),
    '/etc/brlapi.key': ('SETTING-DEFAULT', 'S8.2-11,S8.2-14,S8.2-17', 'BrlAPI authentication key', 'raw:configuration-origin.tsv', 'Grants access to the braille API; created by brltty maintainer script during package installation: default covered by package line.'),
    '/etc/ca-certificates.conf': ('SETTING-DEFAULT', 'S8.2-11,S8.2-17', 'list of trusted CA certificates', DOC_CA, 'Trust selection the whole computer obeys; rewritten by ca-certificates postinst from debconf during installation (11:15:48): default.'),
    '/etc/ca-certificates.conf.dpkg-old': ('RECORD', 'S8.2-15', 'old copy kept by maintainer script', 'raw:configuration-origin.tsv', 'Backup written by the ca-certificates postinst as it ran.'),
    '/etc/fstab': ('SETTING-OWN', 'S8.2-11,S8.2-13,S8.2-17', 'filesystem table', 'evidence', 'Filesystems are settings; written for this computer at OS installation, not by a package.'),
    '/etc/group': ('SETTING-OWN', 'S8.2-11,S8.2-13,S8.2-17', 'group accounts', 'evidence', 'Accounts are settings; holds groups of the person\'s account chosen at installation besides package defaults.'),
    '/etc/gshadow': ('SETTING-OWN', 'S8.2-11,S8.2-13,S8.2-17', 'group passwords and members', 'evidence', 'Accounts and rights; holds the person\'s group memberships chosen at installation.'),
    '/etc/passwd': ('SETTING-OWN', 'S8.2-11,S8.2-13,S8.2-17', 'user accounts', 'raw:raw/0002-metadata-read-0.out', 'Accounts are settings; holds the person\'s account (uid 1000) besides package-created system accounts.'),
    '/etc/shadow': ('SETTING-OWN', 'S8.2-11,S8.2-13,S8.2-17', 'account passwords', 'evidence', 'Means of login to this computer; holds the person\'s password.'),
    '/etc/hostname': ('SETTING-OWN', 'S8.2-11,S8.2-13', 'host name', 'evidence', 'Network setting chosen at OS installation, not by a package.'),
    '/etc/hosts': ('SETTING-OWN', 'S8.2-11,S8.2-13', 'static host table with the host name', 'evidence', 'Network setting written at installation with the chosen host name (same second as hostname).'),
    '/etc/hosts.allow': ('SETTING-DEFAULT', 'S8.2-11,S8.2-13,S8.2-17', 'TCP wrappers allow rules', 'raw:configuration-origin.tsv', 'Access rules; created by libwrap0 maintainer script during installation: package default.'),
    '/etc/hosts.deny': ('SETTING-DEFAULT', 'S8.2-11,S8.2-13,S8.2-17', 'TCP wrappers deny rules', 'raw:configuration-origin.tsv', 'Access rules; created by libwrap0 maintainer script during installation: package default.'),
    '/etc/inputrc': ('RECORD', 'S8.2-14,S8.2-23', 'readline key bindings, copy of readline-common file', 'raw:raw/0004-filesystem.out', 'Read as values by readline in programs a person runs; launches nothing, grants nothing: a record by S8.2-14.'),
    '/etc/ld.so.cache': ('RECORD', 'S8.2-15', 'dynamic linker cache', 'evidence', 'Cache generated by ldconfig as it ran.'),
    '/etc/locale.conf': ('SETTING-OWN', 'S8.2-11,S8.2-13', 'system language', 'evidence', 'Language setting written at OS installation from the installing person\'s choice.'),
    '/etc/locale.gen': ('SETTING-OWN', 'S8.2-11,S8.2-13', 'locales to generate', 'evidence', 'Language setting edited at OS installation (04:41:47) for the chosen locale.'),
    '/etc/localtime': ('SETTING-OWN', 'S8.2-11,S8.2-13', 'time zone link', 'evidence', 'Time setting chosen at OS installation.'),
    '/etc/timezone': ('SETTING-OWN', 'S8.2-11,S8.2-13', 'time zone name', 'evidence', 'Time setting chosen at OS installation.'),
    '/etc/machine-id': ('RECORD', 'S8.2-15', 'machine identifier generated by systemd', 'raw:configuration-origin.tsv', 'Generated by systemd as it ran; nobody chose the value.'),
    '/etc/mailcap': ('RECORD', 'S8.2-14,S8.2-15', 'MIME handler list generated by update-mime', 'raw:configuration-origin.tsv', 'Generated list written by update-mime as it ran; no person chose it.'),
    '/etc/motd': ('RECORD', 'S8.2-15', 'empty message-of-the-day file from the system image', 'evidence', 'Text written during image build; not code, not a setting chosen by a person.'),
    '/etc/mtab': ('RECORD', 'S8.2-15', 'link to the kernel mount table', 'evidence', 'Compatibility link created by a program; points to runtime mount data.'),
    '/etc/networks': ('SETTING-DEFAULT', 'S8.2-11,S8.2-13,S8.2-17', 'network names, copy of base-files file', 'raw:configuration-origin.tsv', 'Network setting created by base-files/netbase maintainer script during installation: default.'),
    '/etc/nsswitch.conf': ('SETTING-DEFAULT', 'S8.2-11,S8.2-13,S8.2-17', 'name service switch', 'raw:configuration-origin.tsv', 'Account/host lookup the whole computer obeys; written by libc-bin and NSS module maintainer scripts during installation.'),
    '/etc/papersize': ('SETTING-DEFAULT', 'S8.2-11,S8.2-17', 'default paper size', 'raw:configuration-origin.tsv', 'System-wide value created by libpaper1 maintainer script during installation: package default.'),
    '/etc/pnm2ppa.conf': ('SETTING-DEFAULT', 'S8.2-11,S8.2-13,S8.2-17', 'printer driver configuration', 'raw:configuration-origin.tsv', 'Device setting created by printer-driver-pnm2ppa maintainer script during installation.'),
    '/etc/printcap': ('RECORD', 'S8.2-15', 'link to printer list kept by cupsd', 'raw:raw/0454-metadata-read-256.out', 'Link created by cups-daemon postinst to a file cupsd writes as it runs.'),
    '/etc/profile': ('PROGRAM-DERIVED', 'S8.2-9,S8.2-16,S8.2-23', 'login shell startup script, copy of base-files profile', 'raw:raw/0004-filesystem.out', 'Executed by shells as code; identical signature to package file copied by base-files postinst: built by system from recorded package.'),
    '/etc/resolv.conf': ('UNKNOWN', 'S8.2-11,S8.2-17', 'DNS resolver link to systemd-resolved stub', 'evidence', 'Network setting; whether a package script or the installing person created it is not recorded (no script mention): DEFAULT or OWN.'),
    '/etc/shells': ('SETTING-DEFAULT', 'S8.2-11,S8.2-13,S8.2-17', 'permitted login shells', 'raw:configuration-origin.tsv', 'What is permitted as a means of login; maintained by debianutils add-shell during installation.'),
    '/etc/subgid': ('SETTING-OWN', 'S8.2-11,S8.2-13', 'subordinate group id ranges', 'evidence', 'Rights of the person\'s account, written when the account was created at installation.'),
    '/etc/subuid': ('SETTING-OWN', 'S8.2-11,S8.2-13', 'subordinate user id ranges', 'evidence', 'Rights of the person\'s account, written when the account was created at installation.'),
    '/etc/vconsole.conf': ('UNKNOWN', 'S8.2-11,S8.2-17', 'console keyboard link to default keyboard file', 'evidence', 'Device setting link; creator (package script or installing person) not recorded: SETTING-DEFAULT or SETTING-OWN.'),
    '/etc/cups/cupsd.conf': ('SETTING-DEFAULT', 'S8.2-11,S8.2-13,S8.2-17', 'print service configuration', 'raw:raw/0454-metadata-read-256.out', 'Service parameters; cups-daemon postinst copies the default when absent: created during installation.'),
    '/etc/cups/raw.convs': ('SETTING-DEFAULT', 'S8.2-11,S8.2-17', 'CUPS raw conversion rules', 'raw:configuration-origin.tsv', 'Service parameter created by cups postinst during installation.'),
    '/etc/cups/raw.types': ('SETTING-DEFAULT', 'S8.2-11,S8.2-17', 'CUPS raw type rules', 'raw:configuration-origin.tsv', 'Service parameter created by cups postinst during installation.'),
    '/etc/cups/subscriptions.conf': ('RECORD', 'S8.2-15', 'event subscriptions written by cupsd', 'evidence', 'Written by cupsd as it ran.'),
    '/etc/cups/subscriptions.conf.O': ('RECORD', 'S8.2-15', 'previous copy written by cupsd', 'evidence', 'Backup written by cupsd as it ran.'),
    '/etc/apparmor.d/tunables/home.d/ubuntu': ('SETTING-DEFAULT', 'S8.2-11,S8.2-13,S8.2-17', 'AppArmor home directory tunable', 'raw:configuration-origin.tsv', 'Access rule input written by apparmor postinst during installation (11:15:42).'),
}


def system(m):
    p, typ, ct, tgt = m['path'], m['type'], m['ctime'][:19], m['target']
    # merged-/usr package ownership
    if m['pkg']:
        integ = m['integrity']
        pk = m['pkg'].split(';')[0].replace('dpkg:', '')
        if typ == 'directory':
            return R('INSTALLED-PACKAGE', 'S8.2-7,S8.2-8,S8.2-16', 'directory of package ' + pk, 'raw:package-files.tsv',
                     'Directory listed in the package manifest (path through /usr alias): obtained as part of the package.', 'package directory')
        if integ == 'unchanged':
            return R('INSTALLED-PACKAGE', 'S8.2-7,S8.2-8,S8.2-16', 'file of package ' + pk, 'raw:package-files.tsv',
                     'Package file (path through /usr alias), digest unchanged since installation: installed object covered by its package line.', 'package file, unchanged')
        if integ == 'unknown' and ct and ct <= END_DPKG:
            return R('INSTALLED-PACKAGE', 'S8.2-7,S8.2-8,S8.2-16', 'link shipped in package ' + pk, 'raw:package-files.tsv',
                     'Link in the package manifest; dpkg keeps no digest, but ctime predates the end of the last dpkg run: not changed since received.', 'package link, ctime before end of dpkg run')
        return R('UNKNOWN', 'S8.2-7', 'file of package ' + pk, 'raw:package-files.tsv',
                 'Whether the package file remains as received is not recorded (integrity %s).' % integ, 'package file of unknown integrity')
    if m['persistence'] == 'runtime':
        who = runtime_creator(p)
        return R('RUNTIME', 'S8.2-5', 'runtime file on tmpfs', 'evidence',
                 'Exists only while running (tmpfs). Belongs to %s; that program\'s files are INSTALLED-PACKAGE.' % who, 'runtime file on tmpfs')
    if p in ETC:
        d, s, w, b, r = ETC[p]
        return R(d, s, w, b, r)
    if re.match(r'/etc/(group|gshadow|passwd|shadow|subuid|subgid)-$', p):
        return R('RECORD', 'S8.2-15', 'backup copy written by account tools', 'evidence', 'Previous copy written by shadow tools as they ran.')
    if p in ('/etc/opt', '/etc/pcmcia', '/etc/python3', '/var/mail', '/var/opt', '/usr/lib/python3/dist-packages/uaclient',
             '/usr/share/sounds/sf3'):
        return R('RECORD', 'S8.2-15', 'directory created by a maintainer script or image build', 'evidence',
                 'Directory created by a program as it ran; not a package file, not code, not a setting.', 'directory created by a program')
    if p.startswith('/etc/alternatives/') or tgt.startswith('/etc/alternatives/'):
        return R('SETTING-DEFAULT', 'S8.2-11,S8.2-17', 'alternatives link choosing a system-wide implementation', DOC_UPDALT,
                 'System-wide choice of implementation made by update-alternatives in maintainer scripts during installation: package default.', 'alternatives link')
    if p == '/usr/bin/evince':
        return R('UNKNOWN', 'S8.2-11,S8.2-17', 'link evince to xreader', 'evidence',
                 'Unowned link from the system image; no maintainer script mentions it: who created it (package default or person) is not recorded.')
    if p.startswith('/etc/pam.d/common-'):
        return R('SETTING-DEFAULT', 'S8.2-11,S8.2-13,S8.2-17', 'PAM common stack', DOC_PAM,
                 'Means of login; managed by pam-auth-update from package profiles in libpam-runtime postinst during installation (11:15:47).', 'PAM common stack')
    if p.startswith('/etc/systemd/user/'):
        return R('SETTING-DEFAULT', 'S8.2-11,S8.2-13,S8.2-17', 'user unit enablement link or wants directory', 'raw:raw/0004-filesystem.out',
                 'Service enablement created by deb-systemd-user-helper in maintainer scripts during package installation: default covered by package line.', 'user unit enablement (package default)')
    if p.startswith('/etc/ssl/certs/'):
        return R('SETTING-DEFAULT', 'S8.2-11,S8.2-17', 'trusted CA certificate link or bundle', DOC_CA,
                 'Trust store the whole computer obeys, generated by update-ca-certificates from ca-certificates.conf during package installation.', 'trusted CA link (default)')
    if p.startswith('/var/lib/dpkg/info/'):
        b = os.path.basename(p)
        if b.endswith('.list') or b == 'format':
            return R('RECORD', 'S8.2-15', 'dpkg list of installed paths', 'evidence', 'Written by dpkg as it ran: its database.', 'dpkg file list')
        if ct and ct <= END_DPKG:
            return R('INSTALLED-PACKAGE', 'S8.2-7,S8.2-8,S8.2-16', 'package control file kept by dpkg', 'evidence',
                     'Control file obtained as part of the package; ctime predates end of last dpkg run, so not changed since received.', 'dpkg control file, unchanged since installation')
        return R('UNKNOWN', 'S8.2-7', 'package control file', 'evidence', 'Changed after the last dpkg run or ctime missing: whether as received is unknown.')
    if p.startswith('/var/lib/dpkg/'):
        if p == '/var/lib/dpkg/arch':
            return R('SETTING-OWN', 'S8.2-11', 'foreign architectures enabled for dpkg', LOG + 'gaming_prerequisites.stderr',
                     'Value chosen by a person (i386 added, log "adding i386 architecture", ctime 11:13:33) that the system package manager obeys.')
        if p in ('/var/lib/dpkg/statoverride', '/var/lib/dpkg/diversions'):
            return R('SETTING-DEFAULT', 'S8.2-11,S8.2-17', 'dpkg ownership overrides or diversions', 'evidence',
                     'Values the system package manager obeys, created by maintainer scripts during package installation: defaults.')
        return R('RECORD', 'S8.2-15', 'dpkg database, lock or trigger state', 'evidence', 'Written by dpkg as it ran: working state.', 'dpkg working state')
    if p.startswith('/var/lib/alsa/'):
        return R('UNKNOWN', 'S8.2-11,S8.2-14,S8.2-15', 'ALSA mixer state restored at boot', 'evidence',
                 'Written 11:19:42 right after the volume action; whether it holds a level chosen by a person (setting) or only program state (record) is not recorded.')
    if p.startswith('/var/lib/systemd/deb-systemd'):
        return R('RECORD', 'S8.2-15', 'deb-systemd-helper state of past enablement', 'evidence',
                 'A record that a service was enabled, written by a program as it ran (Section 8.6 row).', 'enablement state record')
    if p.startswith('/var/') or p.startswith('/root/.cache') or p.startswith('/tmp/'):
        return R('RECORD', 'S8.2-15', 'log, cache, database or working state', 'evidence',
                 'Written by a program as it ran (logs, caches, package lists, state); no person chose it.', 'program record under /var, /tmp or cache')
    if p == '/boot/grub/grub.cfg':
        return R('PROGRAM-DERIVED', 'S8.2-9,S8.2-16,S8.2-23', 'GRUB script generated by update-grub', 'evidence',
                 'GRUB executes it as code; generated by update-grub from recorded packages and settings: built by the system.')
    if p.startswith('/boot/grub/'):
        return R('RECORD', 'S8.2-15', 'GRUB environment, copied font or module directory', 'evidence',
                 'Written by grub-install or GRUB as it ran; not code itself, not a setting chosen by a person.', 'GRUB work file')
    if p.startswith('/usr/lib/cups/backend/'):
        return R('INSTALLED-PACKAGE', 'S8.2-7,S8.2-16', 'CUPS backend, hard link of package file', 'raw:raw/0004-filesystem.out',
                 'Same inode as unchanged backend-available file of cups (cups postinst ln): the package file as received.', 'CUPS backend hard link')
    if re.match(r'/usr/lib/.*/wine/.*-windows/zlib1\.dll$', p):
        return R('PROGRAM-DERIVED', 'S8.2-9,S8.2-16', 'Wine builtin zlib DLL', 'raw:raw/0465-metadata-read-960.out',
                 'Windows code run through Wine; built by libwine postinst from recorded libz-mingw-w64 file: built by the system.')
    if '__pycache__' in p:
        if typ == 'directory':
            return R('RECORD', 'S8.2-15', 'bytecode cache directory', 'evidence', 'Directory created by py3compile as it ran.', 'pycache directory')
        return R('PROGRAM-DERIVED', 'S8.2-9,S8.2-16', 'compiled Python bytecode', 'evidence',
                 'Executed by Python; compiled copy built by py3compile in maintainer scripts from recorded packages.', 'compiled bytecode')
    if p in ('/usr/share/applications/mimeapps.list', '/usr/share/applications/mint-meta-codecs.desktop'):
        return R('UNKNOWN', 'S8.2-14,S8.2-17', 'default application/launcher entry from the system image', 'evidence',
                 'Launches programs (setting by S8.2-14); unowned, no script mention: whether a package installation or a person created it is not recorded.')
    if p.startswith('/usr/'):
        return R('RECORD', 'S8.2-15', 'cache generated by a trigger', 'evidence',
                 'Cache (module, icon, schema, hwdb, MIME) generated by a program as it ran.', 'generated cache')
    return None


# ------------------------------------------------------------------ home side
STEAM = H + '/.steam/debian-installation'
STEAM_RECORD_DIRS = ('package', 'logs', 'appcache', 'config', 'userdata', 'steamapps', 'deb-installer')
STEAM_RECORD_FILES = ('libraryfolder.vdf', 'bootstrap.tar.xz', 'steamdeps.txt')


def steam_code(p, typ, m):
    """In the Steam tree the zip archives give data files executable mode bits, so an extensionless executable
    counts as code only in a program directory (bin, sbin, libexec, ubuntu12_32/64, linux32/64, steamrt*)."""
    if typ != 'file':
        return False
    e = ext(p)
    if re.search(r'\.so(\.|$)', os.path.basename(p)) or e in LINUX_CODE_EXT or e in WIN_CODE_EXT or m.get('shebang') == 'True':
        return True
    if e == '' and m['exec'] == 'True':
        d = os.path.dirname(p)
        return bool(re.search(r'/(bin|sbin|libexec)(/|$)', d) or re.search(r'/debian-installation/(ubuntu12_32|ubuntu12_64|linux32|linux64|steamrt32|steamrt64)$', d))
    return False


def steam(m):
    p, typ = m['path'], m['type']
    rel = p[len(STEAM) + 1:]
    top = rel.split('/')[0]
    if p == STEAM:
        return R('RECORD', 'S8.2-15', 'Steam installation directory', 'evidence', 'Directory created by the steam launcher as it ran.')
    if top in STEAM_RECORD_DIRS or rel in STEAM_RECORD_FILES:
        return R('RECORD', 'S8.2-15', 'Steam download cache, manifest, log, config or launcher files', 'evidence',
                 'Downloaded archives, manifests, logs and state written by Steam or its launcher as they ran.', 'Steam record')
    s = 'S8.1-4,S8.1-6,S8.2-7,S8.2-9,S8.2-15'
    if typ == 'directory':
        return R('GAP-TWO', s, 'directory of the Steam client', DOC_STEAM_UNINSTALL,
                 'INSTALLED-PACKAGE if the client that Steam (a documented installer) installs and --reset removes whole is a package; else RECORD.', 'Steam client directory')
    if steam_code(p, typ, m) or (typ == 'symlink' and re.search(r'\.so(\.\d+)*$|/bin/', p)):
        return R('GAP-TWO', s, 'code of the Steam client or its runtime', DOC_STEAM_UNINSTALL,
                 'INSTALLED-PACKAGE if a client Steam installs and removes whole counts as a package; else PROGRAM-OWN (code obtained from Valve, not built from a line).', 'Steam client code')
    return R('GAP-TWO', s, 'data file of the Steam client or its runtime', DOC_STEAM_UNINSTALL,
             'INSTALLED-PACKAGE if the client Steam installs and removes whole is a package; else RECORD (written by Steam\'s updater as it ran).', 'Steam client data')


def steamcmd(m):
    p, typ, ct = m['path'], m['type'], m['ctime'][:19]
    rel = p[len(H + '/.local/share/steamcmd'):]
    by_person = bool(ct) and ct < STEAMCMD_TAR
    if rel.startswith('/package') or rel.startswith('/logs'):
        return R('RECORD', 'S8.2-15', 'SteamCMD download cache and manifests', 'evidence', 'Written by SteamCMD self-update as it ran.', 'SteamCMD record')
    if typ == 'file' and ext(p) in ('.js', '.mjs', '.cjs'):
        return R('GAP-TWO', 'S8.2-9,S8.2-21,S8.2-15', 'JavaScript of the SteamCMD web server UI', DOC_STEAMCMD,
                 'Code a browser executes (S8.2-9: PROGRAM-OWN), but web-page code inside a browser need not be recorded (S8.2-21: RECORD, written by self-update); no sentence decides.', 'SteamCMD web UI script')
    if is_code(p, typ, m['exec'], m.get('shebang', 'False')):
        return R('PROGRAM-OWN', 'S8.1-4,S8.2-9,S8.2-10', 'SteamCMD code', DOC_STEAMCMD,
                 'Executable code; SteamCMD docs state install/update only, so it is no installer and its files no package; brought by a person or SteamCMD download.', 'SteamCMD code')
    if by_person:
        return R('MATERIAL', 'S8.1-4,S8.2-15', 'file or directory from the SteamCMD tarball', DOC_STEAMCMD,
                 'Not code; extracted from the tarball a person downloaded (ctime 11:18:13): material.', 'SteamCMD tarball data')
    return R('RECORD', 'S8.1-4,S8.2-15', 'SteamCMD data written by its self-update', DOC_STEAMCMD,
             'Not code; written by SteamCMD self-update as it ran (no documented installer, so no package): record.', 'SteamCMD update data')


WINE = H + '/Games/wine-tools'


_WCOPY = None


def wine_copies():
    global _WCOPY
    if _WCOPY is None:
        import csv
        _WCOPY = {}
        for x in csv.DictReader(open('<HOME>/Projects/ideas/cal-paper/night-1123/A3/c2/raw/gaming-wine-copies.tsv'), delimiter='\t'):
            _WCOPY[x['path']] = x['match']
    return _WCOPY


def wine(m):
    p, typ = m['path'], m['type']
    if p.startswith(WINE + '/drive_c/') and typ == 'file' and ext(p) in WIN_CODE_EXT:
        if wine_copies().get(p):
            return R('PROGRAM-DERIVED', 'S8.2-9,S8.2-16', 'Windows code copied into the prefix by wineboot', 'raw:A3/c2/raw/gaming-wine-copies.tsv',
                     'Code run through Wine; same name, size and signature as a libwine package file: copy built by wine from a recorded package.', 'Wine prefix code copy')
        return R('PROGRAM-DERIVED', 'S8.2-9,S8.2-16', 'Wine fake/16-bit module created in the prefix by wineboot', DOC_WINE,
                 'Code run through Wine; created by wineboot from Wine\'s package modules (setupapi fakedll): built from a recorded package.', 'Wine prefix generated module')
    return R('RECORD', 'S8.2-15', 'Wine prefix registry, drive link, data or directory', DOC_WINE,
             'Created by wine/wineboot as it ran (registry, dosdevices, data copies, directories); not code, not chosen by a person.', 'Wine prefix record')


GAME7 = H + '/Games/cal-7zip-tool'


def lutris_game(m):
    p, typ = m['path'], m['type']
    if is_code(p, typ, m['exec'], m.get('shebang', 'False')):
        return R('PROGRAM-OWN', 'S8.1-4,S8.1-6,S8.2-9,S8.2-10', '7-Zip console binary extracted by Lutris', DOC_LUTRIS,
                 'Executable code; Lutris documentation states install only, so the game is no package; obtained from a downloaded archive, not built from a line.', 'Lutris game code')
    return R('MATERIAL', 'S8.1-4,S8.2-15', '7-Zip documentation or game directory', DOC_LUTRIS,
             'Not code; extracted at a person\'s command from an archive named in the person\'s installer script: downloaded file.', 'Lutris game data')


HOME_FIXED = {
    H: ('RECORD', 'S8.2-15', 'home directory', 'evidence', 'Created by account creation as it ran.'),
    H + '/.bash_history': ('RECORD', 'S8.2-15', 'shell history', 'evidence', 'History written by bash.'),
    H + '/.bash_logout': ('PROGRAM-DERIVED', 'S8.2-9,S8.2-16,S8.2-23', 'shell logout script copied from skeleton', 'raw:raw/0004-filesystem.out', 'Executed by bash; identical to /etc/skel copy made at account creation: built by the system.'),
    H + '/.bashrc': ('PROGRAM-DERIVED', 'S8.2-9,S8.2-16,S8.2-23', 'shell startup script copied from skeleton', 'raw:raw/0004-filesystem.out', 'Executed by bash; identical to /etc/skel copy made at account creation: built by the system.'),
    H + '/.profile': ('PROGRAM-DERIVED', 'S8.2-9,S8.2-16,S8.2-23', 'login shell script copied from skeleton', 'raw:raw/0004-filesystem.out', 'Executed by shells; identical to /etc/skel copy made at account creation: built by the system.'),
    H + '/.gtkrc-2.0': ('RECORD', 'S8.2-14', 'GTK theme values', 'evidence', 'Values obeyed by programs a person runs; launch nothing, grant nothing: record.'),
    H + '/.gtkrc-xfce': ('RECORD', 'S8.2-14', 'GTK theme values', 'evidence', 'Values obeyed by programs a person runs; launch nothing, grant nothing: record.'),
    H + '/.steampath': ('RECORD', 'S8.2-15', 'link written by Steam', 'evidence', 'Written by Steam as it ran.'),
    H + '/.steampid': ('RECORD', 'S8.2-15', 'link written by Steam', 'evidence', 'Written by Steam as it ran.'),
    H + '/.sudo_as_admin_successful': ('RECORD', 'S8.2-15', 'sudo marker', 'evidence', 'Written by sudo as it ran.'),
    H + '/.cache': ('RECORD', 'S8.2-15', 'cache directory', 'evidence', 'Created by programs as they ran.'),
    H + '/.config': ('RECORD', 'S8.2-15', 'configuration directory', 'evidence', 'Created by programs as they ran.'),
    H + '/.local': ('RECORD', 'S8.2-15', 'data directory', 'evidence', 'Created by programs as they ran.'),
    H + '/.steam': ('RECORD', 'S8.2-15', 'Steam directory', 'evidence', 'Created by the steam launcher.'),
    H + '/.ssh': ('MATERIAL', 'S8.2-15', 'SSH directory of the person', 'evidence', 'Brought by the person or operator; contents not part of this row.'),
    H + '/Games': ('UNKNOWN', 'S8.2-15', 'games directory', 'evidence', 'Created either at the person\'s command (MATERIAL) or by Lutris default game path (RECORD); creator not recorded.'),
    H + '/actions-logs': ('RECORD', 'S8.2-15', 'action log directory', 'evidence', 'Written by the action runner as it ran.'),
    H + '/actions-status.tsv': ('RECORD', 'S8.2-15', 'action status table', 'evidence', 'Written by the action runner.'),
    H + '/.cal-rehearsal-actions': ('RECORD', 'S8.2-15', 'helper state directory', 'evidence', 'Backups written by the HTTPS sources helper as it ran.'),
    H + '/.config/MangoHud': ('MATERIAL', 'S8.2-15', 'MangoHud config directory', LOG + 'gaming_overlay.log', 'Created with the person\'s overlay configuration.'),
    H + '/.config/MangoHud/MangoHud.conf': ('UNKNOWN', 'S8.2-14', 'MangoHud overlay configuration', 'doc:https://github.com/flightlessmango/MangoHud', 'Read by MangoHud in games a person runs; setting only if it launches something (exec option) or grants access; contents not read.'),
    H + '/.config/autostart': ('MATERIAL', 'S8.2-15', 'autostart directory', LOG + 'gaming_autostart.log', 'Created at the person\'s autostart action (11:19:41).'),
    H + '/.config/autostart/lutris.desktop': ('SETTING-OWN', 'S8.2-11,S8.2-14,S8.2-23', 'autostart entry launching Lutris at login', 'evidence', 'Read as values; launches a program at login: setting by S8.2-14, created by the person\'s autostart action.'),
    H + '/.config/dconf': ('RECORD', 'S8.2-15', 'dconf directory', 'evidence', 'Created by dconf as it ran.'),
    H + '/.config/dconf/user': ('UNKNOWN', 'S8.2-14', 'per-user dconf settings database', LOG + 'gaming_user_settings.log', 'Holds keys set by the person (gsettings) and programs; setting only if a key launches something or grants access; contents not read.'),
    H + '/.config/ibus': ('RECORD', 'S8.2-15', 'ibus directory', 'evidence', 'Created by ibus.'),
    H + '/.config/ibus/bus': ('RECORD', 'S8.2-15', 'ibus bus address directory', 'evidence', 'Created by ibus as it ran.'),
    H + '/.config/caja': ('RECORD', 'S8.2-15', 'file manager directory', 'evidence', 'Created by a program as it ran.'),
    H + '/.config/pulse': ('RECORD', 'S8.2-15', 'pulse directory', 'evidence', 'Created by the sound server.'),
    H + '/.config/pulse/cookie': ('RECORD', 'S8.2-11,S8.2-15', 'sound server authentication cookie', 'evidence', 'Random value generated by the sound server, not chosen by a person: record.'),
    H + '/.config/lutris': ('RECORD', 'S8.2-15', 'Lutris configuration directory', 'evidence', 'Created by Lutris.'),
    H + '/.config/lutris/lutris.conf': ('RECORD', 'S8.2-14,S8.2-15', 'Lutris general options', LOG + 'gaming_launcher_tool.log', 'Written by Lutris on its run; the action set no Lutris option, so no value chosen by a person.'),
    H + '/.config/lutris/games': ('RECORD', 'S8.2-15', 'Lutris games config directory', 'evidence', 'Created by Lutris.'),
    H + '/.config/lutris/runners': ('RECORD', 'S8.2-15', 'Lutris runners directory', 'evidence', 'Created by Lutris.'),
    H + '/.local/share': ('RECORD', 'S8.2-15', 'data directory', 'evidence', 'Created by programs.'),
    H + '/.local/state': ('RECORD', 'S8.2-15', 'state directory', 'evidence', 'Created by programs.'),
    H + '/.local/share/applications': ('RECORD', 'S8.2-15', 'menu entry directory', 'evidence', 'Created by programs.'),
    H + '/.local/share/applications/steam.desktop': ('RECORD', 'S8.2-14,S8.2-15', 'menu entry link created by Steam launcher', 'evidence', 'Created by the Steam launcher as it ran, not chosen by a person.'),
    H + '/.local/share/applications/webapp-OnlineChat4519.desktop': ('UNKNOWN', 'S8.2-14,S8.2-17', 'web-app menu launcher from account skeleton', 'evidence', 'Launches a program (S8.2-14); created at account creation, origin (package default or person) not recorded.'),
    H + '/.local/share/cal-gaming': ('MATERIAL', 'S8.2-15', 'directory of downloaded tools', 'evidence', 'Created at the person\'s command.'),
    H + '/.local/share/cal-gaming/7zr.exe': ('PROGRAM-OWN', 'S8.2-9,S8.2-10', 'downloaded 7-Zip Windows console program', LOG + 'gaming_windows_program.log', 'Windows code run through Wine at a person\'s command; downloaded, not built from a line.'),
    H + '/.local/share/cal-gaming/7zip.yml': ('GAP-TWO', 'S8.2-9,S8.2-14,S8.2-23', 'Lutris installer script', 'doc:https://github.com/lutris/lutris/blob/master/docs/installers.rst', 'Lutris performs its directives: PROGRAM-OWN if that is executing code (S8.2-23); else SETTING-OWN, values that launch an install (S8.2-14).'),
    H + '/.local/share/icons': ('RECORD', 'S8.2-15', 'icon directory', 'evidence', 'Created by the Steam launcher as it ran.'),
    H + '/.local/share/ice':('RECORD', 'S8.2-15', 'web-app manager directory', 'evidence', 'Created by a program.'),
    H + '/.local/share/flatpak': ('RECORD', 'S8.2-15', 'Flatpak user installation directory', DOC_FLATPAK, 'Directory created by flatpak; its contents are a separate row.'),
    H + '/.local/share/lutris': ('RECORD', 'S8.2-15', 'Lutris data directory', 'evidence', 'Created by Lutris.'),
    H + '/.local/share/steamcmd': ('MATERIAL', 'S8.2-15', 'SteamCMD directory', DOC_STEAMCMD, 'Created when the person extracted the SteamCMD tarball.'),
    H + '/.local/state/wireplumber': ('RECORD', 'S8.2-15', 'WirePlumber state directory', 'evidence', 'Created by WirePlumber.'),
    H + '/.local/state/wireplumber/restore-stream': ('RECORD', 'S8.2-14', 'saved stream volumes', 'evidence', 'Volumes obeyed only by the user\'s sound server; launch nothing, grant nothing: record by S8.2-14.'),
    H + '/Games/U3DS': ('RECORD', 'S8.2-15', 'SteamCMD install directory', LOG + 'gaming_anonymous_download.log', 'Created by SteamCMD for the failed app install.'),
    H + '/Games/U3DS/steamapps': ('RECORD', 'S8.2-15', 'SteamCMD app state directory', LOG + 'gaming_anonymous_download.log', 'Written by SteamCMD as it ran.'),
    GAME7: ('MATERIAL', 'S8.1-4,S8.2-15', 'Lutris game directory', DOC_LUTRIS, 'Directory of files extracted at the person\'s command; Lutris game is no documented package.'),
    WINE: ('RECORD', 'S8.2-15', 'Wine prefix directory', DOC_WINE, 'Created by wine as it ran (configuration directory).'),
}


def home(m):
    p, typ = m['path'], m['type']
    if p in HOME_FIXED:
        d, s, w, b, r = HOME_FIXED[p]
        return R(d, s, w, b, r)
    if p.startswith(STEAM + '/') or p == STEAM:
        return steam(m)
    if p.startswith(H + '/.steam/'):
        return R('RECORD', 'S8.2-15', 'Steam link, pid, pipe, token or registry', 'evidence', 'Written by Steam as it ran.', 'Steam root record')
    if p.startswith(H + '/.local/share/steamcmd/'):
        return steamcmd(m)
    if p.startswith(WINE + '/'):
        return wine(m)
    if p.startswith(GAME7 + '/'):
        return lutris_game(m)
    if p.startswith(H + '/.cache/') or p.startswith(H + '/actions-logs/') or p.startswith(H + '/.cal-rehearsal-actions/'):
        return R('RECORD', 'S8.2-15', 'cache, log or helper state', 'evidence', 'Written by a program as it ran (cache, action log, helper backup).', 'home cache or log')
    if p.startswith(H + '/.config/lutris/games/') and p.endswith('.yml'):
        return R('SETTING-OWN', 'S8.2-11,S8.2-14', 'Lutris game configuration (executable to launch)', 'doc:https://github.com/lutris/lutris/blob/master/README.rst',
                 'Values obeyed by Lutris that launch the game; from the person\'s installer script; game is no package, so no package default.')
    if p.startswith(H + '/.local/share/icons/') or p.startswith(H + '/.local/share/lutris/'):
        return R('RECORD', 'S8.2-15', 'icon links, icon cache or Lutris database', 'evidence', 'Written by Steam launcher, icon cache tool or Lutris as they ran.', 'home record')
    return None


def classify(m):
    p = m['path']
    if p.startswith('/home/'):
        return home(m)
    return system(m)
