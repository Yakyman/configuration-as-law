"""Rules of classification c2, part 4 (Guix machine).

Closure store objects (kind system-closure-store-object), kernel modules, system services,
processes and accounts are decided by the rules below; every other row is decided row by row
in ROWS. Usage: python3 -I rules_part4.py <input.tsv> <output.tsv>
"""
import csv, re, sys

DRV = 'doc:https://guix.gnu.org/manual/en/html_node/Derivations.html'
GC = 'doc:https://guix.gnu.org/manual/en/html_node/Invoking-guix-gc.html'
CONF = 'raw:configuration/etc/config.scm'

def r(dec, sent, what, basis, reason):
    return (dec, sent, what, basis, reason)

# ---------------------------------------------------------------- closure rules
PKG = r('MUST', 'S2.2-1,S2.2-2,S2.2-9,S2.2-10',
        'Package output: programs or libraries the current system uses at run time',
        DRV, 'Run-time dependency of the system: removing it stops programs that use it or makes '
        'its programs impossible to start, which the removal test makes MUST.')
CODE = r('MUST', 'S2.2-10,S2.2-13',
         'Guile code run by the activation script or by shepherd as root',
         'raw:system-closure.txt', 'Code executed by a system program with that program\'s own '
         '(superuser) rights; S2.2-10 and S2.2-13 make such code MUST.')
SHEP = r('MUST', 'S2.2-10,S2.2-13',
         'Service definition (Scheme source or compiled) loaded by shepherd, PID 1',
         'raw:herd-status.txt', 'Shepherd executes this file as code with its own superuser '
         'rights; S2.2-10 and S2.2-13 make it MUST.')
SCRIPT = r('MUST', 'S2.2-10,S2.2-13', 'Script or wrapper executed by a system program or session',
           'raw:system-closure.txt', 'An executable script runs with the rights of the program '
           'that starts it; S2.2-10 makes such code MUST.')
GUIXMOD = r('MUST', 'S2.2-2,S2.2-9,S2.2-10',
            'Part of the guix command or daemon: Guile modules, launcher, module union',
            DRV, 'The guix tool loads these modules as code with its own rights; without them '
            'guix commands become impossible (S2.2-2, S2.2-10).')
GUIXSRC = r('UNKNOWN', 'S3-1,S3-2', 'Scheme source tree of Guix modules beside compiled modules',
            'none', 'Whether guix reads these sources at run time or only their compiled copies '
            'could not be established from the evidence or documentation reached.')
PAM = r('MUST', 'S2.2-15,S2.2-2',
        'PAM service file in pam.d naming how a program authenticates users',
        'doc:https://cgit.git.savannah.gnu.org/cgit/guix.git/plain/gnu/system/pam.scm', 'PAM rules decide password login and becoming superuser (su, sudo); '
        'S2.2-15 requires the rule that password login is allowed.')
SYSCONF = r('MUST', 'S2.2-1,S2.2-2,S2.2-13',
            'Configuration read as values by many programs of the system',
            'raw:system-closure.txt', 'A setting read by many programs, not inside one program '
            '(so S2.2-7 does not exempt it); removing it changes what the computer does.')
ONECONF = r('HOLE', 'S2.2-7,S2.2-2',
            'Configuration file read only by one daemon; its effect reaches the whole computer',
            'raw:system-closure.txt', 'S2.2-7 exempts settings in force only inside one program; '
            'S2.2-2 requires what removal changes. Text lacks whether a daemon\'s own '
            'configuration is "inside one program".')
THEME = r('HOLE', 'S2.2-4,S2.2-7,S2.2-2',
          'Fonts, icons, theme or sounds used by many programs for presentation',
          'raw:system-closure.txt', 'Neither content (S2.2-4) nor a setting of one program '
          '(S2.2-7); text lacks whether a changed appearance after removal counts as the computer '
          'stopping doing something (S2.2-2).')
ONETHEME = r('NOT', 'S2.2-7', 'Theme or artwork used inside one program only',
             'raw:system-closure.txt', 'A theme in force only inside one program; S2.2-7 lists '
             'theme as a setting that need not be recorded.')
DOC = r('NOT', 'S2.2-4', 'Documentation or document index (manual, info directory)',
        'raw:system-closure.txt', 'Documents: after removal the computer does the same, only '
        'the documents are unavailable; S2.2-4 says content need not be recorded.')
CACHE = r('NOT', 'S2.2-5', 'Cache built to speed up a lookup; regenerable',
          'raw:system-closure.txt', 'A cache: after removal the computer does the same, only '
          'more slowly; S2.2-5 says cache need not be recorded.')
RECORD = r('NOT', 'S2.2-6', 'Record of how this system generation was built (provenance, copy)',
           'raw:system-generations.txt', 'A record of the past build; S2.2-6 says records of '
           'the past need not be recorded.')
CONTENT = r('NOT', 'S2.2-4', 'Images or message text shown to the user', 'raw:system-closure.txt',
            'Content: after removal the computer does the same and only the content itself is '
            'unavailable (S2.2-4).')
DATA = r('MUST', 'S2.2-1,S2.2-2,S2.2-13',
         'Data read as values by many programs to work (locale, zones, certificates, schemas)',
         'raw:system-closure.txt', 'A setting read as values by many programs; removing it '
         'makes functions impossible (e.g. TLS, locale, file types), so S2.2-2 gives MUST.')
PULSE = r('MUST', 'S2.2-10,S2.2-13', 'PulseAudio /etc/pulse: default.pa and system.pa scripts, daemon.conf, client.conf',
          'doc:https://cgit.git.savannah.gnu.org/cgit/guix.git/plain/gnu/services/sound.scm',
          'default.pa is a command script pulseaudio executes at start (loads modules): a file executed as code (S2.2-13, S2.2-10).')
UNKNOWN_READER = r('UNKNOWN', 'S3-1,S3-2', 'Compatibility file; no program shown to read it here',
                   'raw:files.tsv', 'Which program on this machine reads it, and what stops '
                   'without it, could not be established; S3-2 gives ?.')

def U(what, reason, basis='none', sent='S3-1,S3-2'):
    return r('UNKNOWN', sent, what, basis, reason)

CLOSURE_SPECIAL = [
    # exact base names first
    (r'shepherd-.*\.(scm|go)|shepherd\.conf', SHEP),
    (r'activate(-service)?\.scm|boot|module-import(-compiled)?|raw-initrd', CODE),
    (r'parameters|system|etc|profile', r('MUST', 'S2.2-1,S2.2-2,S2.2-9',
        'System generation tree: system dir, /etc union, package profiles, boot parameters',
        'raw:system-closure.txt', 'The running system reaches its programs and configuration through '
        'these directories; removing one makes them unreachable (S2.2-2).')),
    (r'vulkan-headers-.*|xorgproto-.*|util-macros-.*|wayland-protocols-.*', r('MUST', 'S2.2-2',
        'Header files and build macros for compiling against X, Vulkan, Wayland',
        'raw:system-closure.txt', 'With gcc and pkg-config in the system, removal makes compiling '
        'programs that include these headers impossible on the computer (S2.2-2).')),
    (r'guix-icons-.*', THEME),
    (r'(pam\.d|polkit-1|su|sudo|login|passwd|chfn|other|groupadd|groupdel|groupmod|useradd|userdel|usermod|sshd|slim|xlock|slock|xfce4-screensaver)', PAM),
    (r'guix-(system|cli|cli-core|extra|packages-base|system-tests|d58da8a56)-source|guix-cli-core-source', GUIXSRC),
    (r'guix-(system|cli|cli-core|extra|packages-base|system-tests|d58da8a56)(-modules)?|guix-command|guix-module-union|guix-daemon|guix-d58da8a56|guix-cli-core-modules', GUIXMOD),
    (r'guix-locale-guix(-packages)?', r('NOT', 'S2.2-7,S2.2-2', 'Message translations of the guix command',
        'raw:system-closure.txt', 'Language of messages inside one program; locale is en_US, so '
        'removal changes nothing; S2.2-7 exempts settings inside one program.')),
    (r'guile-launcher\.c', U('C source text of the guix launcher kept in the run-time closure',
        'No program is shown to read or run this source file at run time; what removal would stop is not established.')),
    (r'guix-manual|info-dir', DOC),
    (r'manual-database|guix-package-cache|gtk-icon-themes|xdg-desktop-database', CACHE),
    (r'provenance|channels\.scm|configuration\.scm', RECORD),
    (r'motd|issue|guix-backgrounds-.*|gnome-backgrounds-.*', CONTENT),
    (r'guix-artwork-.*|xfwm4-themes-.*', ONETHEME),
    (r'emacs-subdirs', r('NOT', 'S2.2-1,S2.2-2,S2.2-10', 'Emacs Lisp load-path file; no Emacs on this system',
        'raw:system-closure.txt', 'S2.2-10 requires code only if a program runs it; no Emacs is in '
        'the closure, so removal stops nothing.')),
    (r'(hicolor|adwaita|elementary-xfce)-icon-theme-.*|greybird-gtk-theme-.*|sound-theme-freedesktop-.*|font-(dejavu|bitstream-vera|adobe75dpi|ghostscript)-.*|iso-codes-.*', THEME),
    (r'font-(misc-misc|alias)-.*', U('X core bitmap fonts and font aliases on the default X font path',
        'Whether the X server here fails without them (default font "fixed") could not be confirmed from documentation reached.',
        'doc:https://cgit.git.savannah.gnu.org/cgit/guix.git/plain/gnu/services/xorg.scm')),
    (r'font-gnu-unifont-.*-psf', THEME[:2] + ('Default console font loaded by the console-font services',
        'doc:https://cgit.git.savannah.gnu.org/cgit/guix.git/plain/gnu/services/base.scm', THEME[4])),
    (r'firmware', U('Firmware directory given to the kernel; config sets firmware to empty list',
        'Contents of the directory not inventoried; whether any device loads firmware from it is not established.', CONF)),
    (r'os-release|hostname|timezone', UNKNOWN_READER),
    (r'tzdata-.*|nss-certs-.*|ca-certificate-bundle|glibc-utf8-locales-.*|locale-.*|locale-multiple-versions|xkeyboard-config-.*|wireless-regdb-.*|shared-mime-info-.*|gsettings-desktop-schemas-.*|poppler-data-.*|usb-modeswitch-data-.*|alsa-ucm-conf-.*|alsa-topology-conf-.*|xdg-mime-database|glib-schemas|gdk-pixbuf-loaders-cache-file|gtk-im-modules|fonts-dir|linux-module-database|hwdb\.bin|net-base-.*', DATA),
    (r'nsswitch\.conf|hosts|environment|login\.defs|sysctl\.conf|asound\.conf|shells|fstab|nscd\.conf|udev(\.conf)?|udev-rules\.d|90-kvm\.rules|usb_modeswitch\.rules|skel', SYSCONF),
    (r'sudoers|sshd_config|openssh-authorized-keys', r('MUST', 'S2.2-15',
        'Superuser rights (sudoers), SSH server rules, or keys for logging in',
        CONF, 'S2.2-15 requires the right to become superuser, keys used to log in, open ports '
        'and the password-login rule; this object states them.')),
    (r'polkit-wheel|wheel\.rules|etc-polkit-1', r('MUST', 'S2.2-10,S2.2-13,S2.2-15',
        'Polkit rules (JavaScript run by polkitd) granting the wheel group administration',
        'raw:system-closure.txt', 'Rules files are code executed by polkitd and decide rights to '
        'act as administrator; S2.2-13 and S2.2-15 give MUST.')),
    (r'avahi-daemon\.conf', r('MUST', 'S2.2-15', 'Avahi daemon configuration: mDNS service on UDP port 5353',
        'raw:herd-status.txt', 'It governs a port open for connection (mDNS); S2.2-15 says ports open '
        'for connection must be recorded.')),
    (r'client\.conf', r('NOT', 'S2.2-1,S2.2-2', 'PulseAudio client.conf built from the empty default client-conf list',
        'doc:https://cgit.git.savannah.gnu.org/cgit/guix.git/plain/gnu/services/sound.scm',
        'The default client-conf is the empty list, so the file sets nothing; removal changes nothing.')),
    (r'pulse', PULSE),
    (r'acl', ONECONF),
    (r'dhcpcd\.conf|ntpd\.conf|daemon\.conf|dbus-configuration|dbus-system-services|etc-elogind|logind\.conf|sleep\.conf|UPower\.conf|geoclue\.conf|xserver\.conf|xorg\.conf\.d|slim\.cfg', ONECONF),
    (r'xinitrc|startx|X-wrapper|guile-wrapper|geoclue-wrapper|geoclue-program-wrapper|upower-wrapper|upower-program-wrapper|elogind-dbus-service-wrapper|elogind-dbus-shepherd-sync|run-with-writable-store|set-up-network|tear-down-network|delete-old-logs|validate-guix-ownership|usb_modeswitch-sh|aliases\.sh|bashrc|bashrc\.d|modprobe', SCRIPT),
]

def base_name(storepath):
    return re.sub(r'^/gnu/store/[a-z0-9]{32}-', '', storepath)

VERSIONED = re.compile(r'-[0-9][0-9A-Za-z.+_~-]*$')

def closure_rule(name):
    b = base_name(name)
    for pat, dec in CLOSURE_SPECIAL:
        if re.fullmatch(pat, b):
            return dec, pat
    if VERSIONED.search(b):
        return PKG, 'PKG'
    raise KeyError(b)

KMOD = r('MUST', 'S2.2-10,S2.2-2', 'Loaded Linux kernel module (driver or subsystem code)',
         'raw:modules.txt', 'Code the kernel runs with its own rights (S2.2-10); unloading or '
         'removing it stops the driver or function it provides (S2.2-2).')
SERVICE = r('MUST', 'S2.1-3,S2.2-1,S2.2-2', 'Shepherd system service, running or started at boot',
            'raw:herd-status.txt', 'An enabled service is in force (S2.1-3); removing it stops '
            'what it starts or sets up, so S2.2-2 gives MUST.')
PROC = r('MUST', 'S2.2-9', 'Running program (process of a system or session program)',
         'raw:processes.txt', 'S2.2-9: a program that runs on the computer must be recorded '
         'regardless of how it was installed.')
ACCT = r('MUST', 'S2.2-15', 'User account in the account database', 'raw:accounts.txt',
         'S2.2-15: accounts must be recorded.')

# ---------------------------------------------------------------- row-by-row
NOT_LOG = r('NOT', 'S2.2-6', 'Log file of a daemon or of logins', 'evidence',
            'A log is a record of the past; S2.2-6 says it need not be recorded.')
STATE = lambda what, reason: r('NOT', 'S2.5-1,S2.5-2', what, 'evidence', reason)
SHELLRC = r('MUST', 'S2.2-10', 'Shell startup file executed by bash at login', 'evidence',
            'S2.2-10 names shell startup files as code that must be recorded.')
ROWS = {
 'guix-258ca137f0': r('MUST', 'S2.2-15', 'Ten build accounts guix-daemon uses to run builds',
     'raw:guix-builder-accounts.txt', 'S2.2-15: accounts must be recorded.'),
 'guix-89ce5c5668': r('MUST', 'S2.2-9', 'Threads of the running Linux kernel', 'raw:processes.txt',
     'They are the kernel, a program running on the computer; S2.2-9 makes running programs MUST.'),
 'guix-d8ee8908a9': r('MUST', 'S2.2-9', 'ps from procps, run by the inventory at collection time',
     'raw:processes.txt', 'A program that ran on the computer; S2.2-9 makes it MUST regardless of who started it.'),
 'guix-da5f01a3ef': r('MIXED', 'S2.2-5,S2.5-1,S2.2-1,S2.2-2',
     'Store items not in the current system: derivations, builders, sources, old generation',
     'raw:store-outside-system-closure.txt', 'NOT: .drv/builders/sources/patches (removal changes nothing, '
     'rebuilt; S2.2-1,S2.2-2,S2.2-5); NOT: generation-1 closure (rollback, S2.5-1). Profile/home items: other rows.'),
 'guix-25ad6943ae': r('MIXED', 'S2.2-10,S2.2-4,S2.2-6',
     'Guix Home generation: activation scripts, shell profile, fonts.conf, note file, records',
     'raw:home-closure-outside-system-and-user.txt', 'MUST: home, activate, on-first-login, '
     'setup-environment, update-symlinks, shell-profile, module-import*, profile, fonts.conf, guix (code/settings, '
     'S2.2-10). NOT: w1-declared-note (S2.2-4), configuration.scm, provenance (S2.2-6).'),
 'guix-451d25b3c7': r('NOT', 'S2.2-1,S2.2-2,S2.2-4',
     'emacs-subdirs and info-dir of the user profile', 'raw:user-profile-support-outside-system.txt',
     'info-dir indexes documents (S2.2-4); emacs-subdirs is run only by Emacs, absent here, so removal stops nothing.'),
 'guix-6633666c2c': r('MUST', 'S2.2-2,S2.2-9', 'User profile generation that puts hello on the user\'s PATH',
     'raw:day/user-day.log', 'Removing it makes the installed hello impossible to start; S2.2-9 covers '
     'programs however installed.'),
 'guix-0fbdac78d4': r('MUST', 'S2.2-9', 'hello program installed and run by the ordinary user',
     'raw:day/user-day.log', 'S2.2-9: a program that runs must be recorded regardless of how it was installed.'),
 'guix-64f62c6553': r('MIXED', 'S2.2-4,S2.2-5,S2.5-1,S3-2',
     'Thirty-four empty directories: parents, state, cache, user and run directories',
     'raw:directory-only-groups.json', 'NOT: cache, state and run dirs (S2.2-5,S2.5-1), empty user '
     'dirs (S2.2-4). UNKNOWN: /var/empty, /var/log, parents (/etc, /home/guest...) - what stops unestablished.'),
 # stored rows
 'guix-76634f69cd': r('MIXED', 'S2.2-16,S2.2-10,S2.2-7',
     'Installed GRUB: grub.cfg, grubenv, i386-pc modules, fonts, locale', 'evidence',
     'MUST: grub.cfg, grubenv, i386-pc modules (boot entries and order S2.2-16; code GRUB runs S2.2-10). '
     'NOT: fonts and locale (look and language inside GRUB, S2.2-7).'),
 'guix-84d10d5518': SYSCONF[:2] + ('ALSA configuration for all ALSA programs (link to store)', 'evidence', SYSCONF[4]),
 'guix-69b4850472': SHELLRC,
 'guix-5076d5b4dd': r('MUST', 'S2.2-10', 'Directory of shell snippets sourced by /etc/bashrc',
     'evidence', 'S2.2-10 names shell startup files as code that must be recorded.'),
 'guix-1ed80370a6': r('HOLE', 'S2.1-1,S2.2-1,S2.2-2',
     'The system configuration file used by guix system reconfigure', 'raw:configuration/etc/config.scm',
     'Text lacks whether the files of the declaration itself are objects that must be recorded in it; '
     'removal makes reconfiguring from it impossible (S2.2-2).'),
 'guix-df290cde86': ONECONF[:2] + ('D-Bus daemon configuration (bus policy, service directories)', 'evidence', ONECONF[4]),
 'guix-bff4e92c8d': ONECONF[:2] + ('elogind configuration (logind.conf, sleep.conf)', 'evidence', ONECONF[4]),
 'guix-5deb3892cc': SYSCONF[:2] + ('Environment variables set for every login session', 'evidence', SYSCONF[4]),
 'guix-4cce813fe8': SYSCONF[:2] + ('File system table read by mount and other tools', 'evidence', SYSCONF[4]),
 'guix-a763d184b3': ACCT[:2] + ('Group database (groups and their members)', 'evidence', 'S2.2-15: accounts and the right to become superuser (wheel membership) must be recorded; this file states them.'),
 'guix-493d4cfdb1': ACCT[:2] + ('Account database', 'evidence', 'S2.2-15: accounts must be recorded; this file holds them.'),
 'guix-cfe66bc678': r('MUST', 'S2.2-15,S2.2-2', 'Shadow database: password hashes and per-account password-login state',
     'evidence', 'Passwords are exempt (S2.2-15), but this file also states whether password login is allowed, '
     'and removing it makes login impossible (S2.2-2).'),
 'guix-c7553146ab': r('MIXED', 'S2.2-14,S2.2-2,S2.2-7',
     'guix-daemon signing key pair and authorized-keys acl link', 'evidence',
     'HOLE for all: keys - change leaves behaviour same (password-like, S2.2-14) yet removal stops signing (S2.2-2); '
     'acl - daemon-only setting (S2.2-7 vs S2.2-2).'),
 'guix-ea2b617ba5': UNKNOWN_READER[:4] + ('Which program reads /etc/hostname here (host-name service sets the name) is not established.',),
 'guix-5cad41b508': SYSCONF[:2] + ('Static host-name table read by the resolver in every program', 'evidence', SYSCONF[4]),
 'guix-132a96a8d6': CONTENT[:2] + ('Text shown before the login prompt', 'evidence', CONTENT[4]),
 'guix-966442e2a8': DATA[:2] + ('System time zone used by every program (link into tzdata)', 'evidence', DATA[4]),
 'guix-cafee5136d': SYSCONF[:2] + ('Shadow suite settings read by login, useradd, passwd and others', 'evidence', SYSCONF[4]),
 'guix-1809ee6527': STATE('Machine identifier generated by the system for D-Bus and elogind',
     'A generated identifier is program state; S2.5-1 leaves treating state to system design, so the definition does not require it.'),
 'guix-6b4026dd02': UNKNOWN_READER[:4] + ('Which program on this machine still reads /etc/mtab instead of /proc is not established.',),
 'guix-5f65179c45': SYSCONF[:2] + ('Name service switch used by glibc in every program', 'evidence', SYSCONF[4]),
 'guix-6a38277ef0': UNKNOWN_READER[:4] + ('Which program on this machine reads os-release is not established.',),
 'guix-4d882498fa': PAM[:2] + ('PAM configuration directory for all authenticating programs', 'evidence', PAM[4]),
 'guix-d80ad67f85': r('MUST', 'S2.2-10,S2.2-13,S2.2-15', 'Polkit configuration and rules directory',
     'evidence', 'Rules are code executed by polkitd and decide administrative rights; S2.2-13 and S2.2-15 give MUST.'),
 'guix-3543b3a205': SHELLRC[:2] + ('System login shell profile sourced by bash', 'evidence', SHELLRC[4]),
 'guix-6c0aa5e2c0': DATA[:2] + ('Protocol number table read by glibc in every program', 'evidence', DATA[4]),
 'guix-5c951bf035': PULSE,
 'guix-cee61291d2': STATE('DNS resolver list written at run time by dhcpcd/openresolv',
     'Written by a program from the DHCP lease, i.e. program state; S2.5-1 leaves state to system design.'),
 'guix-9b10886117': DATA[:2] + ('RPC program number table read by glibc', 'evidence', DATA[4]),
 'guix-0f267cfacf': DATA[:2] + ('Service name to port table read by glibc in every program', 'evidence', DATA[4]),
 'guix-5b5a9c277e': SYSCONF[:2] + ('List of valid login shells read by chsh and PAM', 'evidence', SYSCONF[4]),
 'guix-9a671be062': SYSCONF[:2] + ('Skeleton files copied into the home of each new account', 'evidence', SYSCONF[4]),
 'guix-0075a76d48': r('MIXED', 'S2.2-15,S2.2-14,S2.2-2',
     'SSH host key pairs and the authorized_keys.d directory', 'evidence',
     'MUST: authorized_keys.d (login keys, S2.2-15). HOLE: host keys - take part in SSH login but are not '
     'keys to an account; password-like (S2.2-14) vs removal (S2.2-2).'),
 'guix-0306bdd9a9': DATA[:2] + ('TLS certificate directory (link into the system profile)', 'evidence', DATA[4]),
 'guix-09d9e916a6': r('MUST', 'S2.2-15', 'sudo rules: root and wheel may become superuser',
     CONF, 'S2.2-15: the right to become superuser must be recorded.'),
 'guix-8c833da179': UNKNOWN_READER[:4] + ('Which program on this machine reads /etc/timezone (localtime is separate) is not established.',),
 'guix-561d6a5935': SYSCONF[:2] + ('udev rules and hardware database directory', 'evidence', SYSCONF[4]),
 'guix-be124b1a83': STATE('ICE authentication cookies created by the X session',
     'Created at run time by the session, i.e. program state; S2.5-1 leaves state to system design.'),
 'guix-9d9653678b': STATE('X authorization cookie created at login by slim',
     'Created at run time by the session, i.e. program state; S2.5-1 leaves state to system design.'),
 'guix-9052456462': r('NOT', 'S2.2-7', 'X resources (terminal settings) from the skeleton', 'evidence',
     'Values read by X clients for their own look; settings in force inside one program need not be recorded (S2.2-7).'),
 'guix-d68b8b54b5': SHELLRC,
 'guix-9dbbe46297': CACHE[:2] + ('fontconfig font cache of the user', 'evidence', CACHE[4]),
 'guix-084d6fb332': CACHE[:2] + ('Guile auto-compilation cache (compiled home.scm)', 'evidence', CACHE[4]),
 'guix-364f7352cb': r('NOT', 'S2.2-6', 'Notification history database of xfce4-notifyd', 'evidence',
     'A history of past notifications; S2.2-6 says history need not be recorded.'),
 'guix-bd5c3d6b7a': r('HOLE', 'S2.2-7,S2.2-13', 'Thunar custom actions file (commands Thunar runs on request)',
     'evidence', 'S2.2-7 exempts settings inside one program; S2.2-13 makes a file executed as code code. '
     'Text lacks whether a command line Thunar runs is code.'),
 'guix-694c8b6762': SYSCONF[:2] + ('User fontconfig configuration from Guix Home, read by all font users', 'evidence', SYSCONF[4]),
 'guix-a9e486a84b': r('NOT', 'S2.2-1,S2.2-2,S2.2-10', 'gdb init file; gdb is not on this system',
     'raw:system-closure.txt', 'S2.2-10 requires code only if a program runs it; gdb is absent, so removal stops nothing.'),
 'guix-7f3f786b88': U('GSettings keyfile with settings of GLib programs',
     'Which programs\' keys it holds is not in the evidence; whether they are one-program settings is not established.', 'evidence'),
 'guix-6e81e82021': r('NOT', 'S2.2-7', 'nano editor settings file', 'evidence',
     'Settings in force only inside nano; S2.2-7 says they need not be recorded.'),
 'guix-f3795bdd86': r('NOT', 'S2.2-4', 'Plain-text note placed by the Home declaration', 'raw:configuration/home/guest/home.scm',
     'A text document: after removal the computer does the same (S2.2-4).'),
 'guix-7bc12ec287': r('MIXED', 'S2.2-7,S2.2-13,S2.2-2',
     'Xfce settings: xfconf channels, panel launchers, desktop icons, accels', 'evidence',
     'NOT: desktop accels/icons, thunar.xml, xfwm4, notifyd, panel, xsettings, displays (one-program, S2.2-7). HOLE: '
     'launcher .desktop files, keyboard-shortcuts (commands run: code? S2.2-13).'),
 'guix-b0a815366f': STATE('Session bus address file written by dbus-launch',
     'Written at run time, i.e. program state; S2.5-1 leaves state to system design.'),
 'guix-570c2a56ed': r('MUST', 'S2.2-10', 'Guile REPL init file executed by guile at start', 'evidence',
     'Code that guile runs with its own rights, like a shell startup file; S2.2-10 gives MUST.'),
 'guix-1fc1506027': r('MUST', 'S2.2-2', 'Link to the current Guix Home generation', 'evidence',
     'Removal leaves the home profile, shell profile and activation unreachable, so things stop (S2.2-2).'),
 'guix-4e7a5a4664': r('MUST', 'S2.2-2,S2.2-9', 'Link to the user profile holding hello', 'evidence',
     'Removal makes the user-installed program impossible to start from PATH (S2.2-2, S2.2-9).'),
 'guix-cd878659f0': NOT_LOG[:2] + ('Rotated log of x-resize', 'evidence', NOT_LOG[4]),
 'guix-f2103c80af': SHELLRC[:2] + ('Shell profile from Guix Home sourced at login', 'evidence', SHELLRC[4]),
 'guix-a5b845fd5c': r('NOT', 'S2.2-1,S2.2-2,S2.2-10', 'vim settings file; vim is not on this system',
     'raw:system-closure.txt', 'No vim in the closure (nvi reads .nexrc/.exrc), so removal stops nothing; S2.2-10 needs a program that runs it.'),
 'guix-dea3c6354f': r('NOT', 'S2.2-1,S2.2-2,S2.2-10', 'zsh login file; zsh is not on this system',
     'raw:system-closure.txt', 'No zsh in the closure, so nothing runs it and removal stops nothing.'),
 'guix-8c2f616ee7': r('NOT', 'S2.2-4', 'User documents (a day note)', 'evidence',
     'Documents are content; S2.2-4 says content need not be recorded.'),
 'guix-8bcc29aa90': r('NOT', 'S2.2-1,S2.2-2', 'Sample Home configuration copied from the skeleton, not applied',
     'raw:configuration/etc/skel/guix-home-config.scm', 'Nothing runs or reads it; the applied home is home.scm, so removal stops nothing.'),
 'guix-9690fd0a05': r('HOLE', 'S2.1-1,S2.2-1,S2.2-2', 'Guix Home configuration applied for the user',
     'raw:configuration/home/guest/home.scm', 'Text lacks whether the files of a declaration itself are objects '
     'that must be recorded in it; removal makes reapplying impossible (S2.2-2).'),
 'guix-a008390f8b': r('NOT', 'S2.2-7', 'X resources of root (terminal settings)', 'evidence',
     'Values read by X clients for their own look; S2.2-7 exempts settings inside one program.'),
 'guix-0253fce5e2': SHELLRC,
 'guix-033f2e4eef': CACHE[:2] + ('Guile auto-compilation cache of root (compiled config.scm)', 'evidence', CACHE[4]),
 'guix-56d65ad800': CACHE[:2] + ('Channel checkout cache of guix pull/reconfigure', 'evidence', CACHE[4]),
 'guix-b1ffaedde8': CACHE[:2] + ('Mesa shader cache', 'evidence', CACHE[4]),
 'guix-9969ba0797': r('NOT', 'S2.2-1,S2.2-2,S2.2-10', 'gdb init file of root; gdb is not on this system',
     'raw:system-closure.txt', 'S2.2-10 requires code only if a program runs it; gdb is absent, so removal stops nothing.'),
 'guix-3bc83b10e8': r('NOT', 'S2.2-7', 'nano settings file of root', 'evidence',
     'Settings in force only inside nano; S2.2-7 says they need not be recorded.'),
 'guix-d62cf2da81': r('MUST', 'S2.2-10', 'Guile REPL init file of root', 'evidence',
     'Code guile runs with its own (root) rights; S2.2-10 gives MUST.'),
 'guix-351644c1fd': r('MUST', 'S2.2-15', 'Authorized SSH keys for logging in as root', 'evidence',
     'S2.2-15: the keys used to log in to an account must be recorded.'),
 'guix-14d33b9392': r('NOT', 'S2.2-1,S2.2-2,S2.2-10', 'zsh login file of root; zsh is not on this system',
     'raw:system-closure.txt', 'No zsh in the closure, so nothing runs it and removal stops nothing.'),
 'guix-88a33ee425': r('NOT', 'S2.2-1,S2.2-2', 'Sample Home configuration for root, not applied',
     'raw:root-profile.txt', 'Root has no Home generation or profile; nothing reads it, so removal stops nothing.'),
 'guix-006de2c726': STATE('dhcpcd DUID, lease and secret',
     'State written by dhcpcd; S2.5-1 leaves program state to system design.'),
 'guix-6336b9bd7f': CACHE[:2] + ('nscd persistent caches of hosts and services', 'evidence', CACHE[4]),
 'guix-ab6f354e5f': STATE('guix-daemon listening socket', 'Created by the running daemon, i.e. program state; S2.5-1.'),
 'guix-db686654db': STATE('Store database of guix-daemon (valid items, references)',
     'Data and program state of guix-daemon; S2.5-1 leaves its treatment to system design.'),
 'guix-a1b981c4d1': STATE('Garbage-collector lock file', 'Lock created by guix-daemon, program state; S2.5-1.'),
 'guix-b88e111ba5': STATE('Garbage-collector roots (links to boot config, systems, profiles)',
     'Roots only protect store items from collection; generations and state are left to system design (S2.5-1).'),
 'guix-76e4372b50': r('NOT', 'S2.5-1,S2.5-2', 'System generation links (generation 1 and current 2)', 'evidence',
     'Generations and rollback are questions of system design (S2.5-1), not conditions of the definition.'),
 'guix-d1c1f98b6f': r('MUST', 'S2.2-2', 'Current Guix Home generation link of the user', 'evidence',
     '~/.guix-home resolves through it; removal makes the home environment unreachable (S2.2-2).'),
 'guix-e495746cb2': r('MUST', 'S2.2-2,S2.2-9', 'Current user profile link (resolves ~/.guix-profile)', 'evidence',
     'Removal makes the user-installed hello impossible to start (S2.2-2, S2.2-9).'),
 'guix-bbce7dc4de': CACHE[:2] + ('Substitute lookup cache of guix', 'evidence', CACHE[4]),
 'guix-9d9876779f': STATE('Build user pool lock files of guix-daemon', 'Locks created by the daemon, program state; S2.5-1.'),
 'guix-31edaf98e6': STATE('Saved random seed', 'Saved state of the random number pool; S2.5-1 leaves state to design.'),
 'guix-985ad63959': NOT_LOG[:2] + ('Build logs of guix-daemon', 'evidence', NOT_LOG[4]),
 'guix-c2cf70a5ff': STATE('slim auth and lock files, utmpx', 'Run-time state of slim and login records; S2.5-1, S2.2-6.'),
 'guix-77aeb7b4fa': STATE('Compatibility link to the D-Bus run directory', 'Created at activation for run-time sockets, program state; S2.5-1.'),
 'guix-a2b4d23600': STATE('dhcpcd run-time files (pid, sockets, hook state)', 'Run-time state of dhcpcd; S2.5-1.'),
 'guix-d084f3423e': STATE('nscd pid and socket', 'Run-time state of nscd; S2.5-1.'),
 'guix-d0ad40aadd': STATE('Shepherd control socket', 'Run-time state of shepherd; S2.5-1.'),
}
for lid in ['guix-a4963ec3b5', 'guix-2cd84ac792', 'guix-b6a2c8e4dd', 'guix-5ba0b35443', 'guix-43c963f378',
            'guix-698c23461f', 'guix-91a21a61f1', 'guix-e684d315eb', 'guix-4ac29aa55a', 'guix-e7eb2f0db9',
            'guix-d6ce9987c3']:
    ROWS[lid] = NOT_LOG

def decide(row):
    if row['id'] in ROWS:
        return ROWS[row['id']], 'row'
    k = row['kind']
    if k == 'system-closure-store-object':
        return closure_rule(row['name'])
    if k == 'kernel-module':
        return KMOD, 'KMOD'
    if k == 'system-service':
        return SERVICE, 'SERVICE'
    if k == 'process':
        return PROC, 'PROC'
    if k == 'account':
        return ACCT, 'ACCT'
    raise KeyError(row['id'])

if __name__ == '__main__':
    inp, out = sys.argv[1], sys.argv[2]
    rows = list(csv.DictReader(open(inp, encoding='utf-8'), delimiter='\t'))
    import os
    have = set()
    if os.path.exists(out) and os.path.getsize(out) > 0:
        have = {l.split('\t', 1)[0] for l in open(out, encoding='utf-8')}
    with open(out, 'a', encoding='utf-8', newline='') as f:
        if not have:
            f.write('id\tdecision\tsentences\twhat_it_does\tbasis\treason\n')
        for row in rows:
            (dec, sent, what, basis, reason), rule = decide(row)
            for x in (what, reason):
                assert '\t' not in x and '\n' not in x
            if row['id'] not in have:
                f.write('\t'.join([row['id'], dec, sent, what, basis, reason]) + '\n')
                f.flush()
            if len(sys.argv) > 3:
                print(row['id'], rule, base_name(row['name']), dec, sep='\t', file=sys.stderr)
