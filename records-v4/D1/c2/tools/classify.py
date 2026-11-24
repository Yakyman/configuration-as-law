"""c2 classification of D1/in/part-microos.tsv. Rules are stated in ../part-microos.notes.md."""
import re, sys, json, csv, collections
from facts import *

SNAP = "/.snapshots/1/snapshot"
IP, ID, IO = "INSTALLED-PACKAGE", "INSTALLED-DERIVED", "INSTALLED-OWN"
PD, SD, SO = "PROGRAM-DERIVED", "SETTING-DEFAULT", "SETTING-OWN"
REC, RT, G2, UNK, MIX = "RECORD", "RUNTIME", "GAP-TWO", "UNKNOWN", "MIXED"

# ---------------------------------------------------------------- member level
# returns (decision, label) ; label is a short class used in reasons
CODE_PAT = re.compile(r"(\.mod|\.img|\.image|\.exec|/efiemu(32|64)\.o|\.efi|/grub\.cfg|/load\.cfg|/modinfo\.sh|/activate-theme|/grub-snapshot\.cfg|/initrd[^/]*|/vmlinuz|/30ignition/ignition)$")

def received(path, L, snap):
    """Q1 test for a path whose relative path L is in an rpm file list. Returns 'yes', 'no', 'ghost', 'unverified'."""
    d = fs.get(path)
    ent = rpm[L]
    if d is None:
        return "unverified"
    t = d.get("type")
    if t == "directory":
        return "yes" if int(d["mode"], 8) in {int(e[3]) & 0o7777 for e in ent if e[3]} else "no"
    if t == "symlink":
        return "yes" if d.get("target") in {e[4] for e in ent} else "no"
    digs = {e[2] for e in ent} - {""}
    if not digs:
        return "ghost"
    if d.get("signature_bytes") == d.get("size") and d.get("size") is not None:
        if h(d.get("signature")) in digs:
            return "yes" if int(d["mode"], 8) in {int(e[3]) & 0o7777 for e in ent} else "no"
        return "no"
    if snap:
        lv = fs.get(L)
        if lv and lv.get("inode") == d.get("inode") and lv.get("ctime") == d.get("ctime") and live_unchanged(L):
            return "yes"
    else:
        if live_unchanged(L): return "yes"
    return "unverified"

def nonreceived(path, L, snap, how):
    """Decision for an object that is not (or not verifiably) as received from a package."""
    d = fs.get(path, {})
    t = d.get("type", "")
    inact = " (copy in inactive root generation)" if snap else ""
    if L.startswith("/usr/share/mime/"):
        return (G2, "mime-genlist") if t == "file" else (REC, "dir-by-program")
    if re.match(r"/usr/lib/modules/[^/]+/modules\.", L):
        return G2, "modules-genlist"
    if L == "/etc/ld.so.cache":
        return G2, "ldcache-genlist"
    if L in ("/etc/selinux/targeted/active/commit_num", "/etc/selinux/targeted/active/modules_checksum", "/usr/lib/udev/compat-symlink-generation") or L.startswith("/etc/crypto-policies/state/"):
        return REC, "state-record"
    if L.startswith("/etc/selinux/targeted/") and t == "file":
        return G2, "selinux-genlist"
    if L == "/etc/audit/audit.rules":
        return G2, "audit-genlist"
    if snap and L in ("/etc/selinux/config", "/etc/default/grub", "/etc/locale.conf", "/etc/vconsole.conf", "/etc/crypto-policies/config", "/etc/audit/rules.d/audit.rules") or (snap and L.startswith("/etc/pam.d/")):
        return G2, "setting-copy-inactive"
    if snap and re.match(r"/etc/systemd/(system|user)/", L) and t == "symlink":
        return G2, "enable-link-copy-inactive"
    if not snap and d.get("persistence") == "runtime":
        return RT, "runtime:" + runtime_creator(L)
    if not snap and L.startswith("/var/tmp/systemd-private-"):
        return RT, "runtime:privatetmp"
    if snap and (L in ("/etc/passwd", "/etc/group", "/etc/shadow", "/etc/fstab", "/etc/dracut.conf.d/50-microos-growfs.conf", "/etc/snapper/configs/root", "/etc/products.d/baseproduct")
                 or L.startswith("/etc/sysconfig/") or L.startswith("/etc/zypp/repos.d/")):
        return G2, "setting-copy-inactive"
    if L in ("/var/lib/ca-certificates/ca-bundle.pem", "/var/lib/ca-certificates/java-cacerts", "/etc/ssl/ca-bundle.pem", "/var/lib/systemd/catalog/database") \
            or L.startswith("/var/lib/ca-certificates/openssl/") or L.startswith("/var/lib/ca-certificates/pem/"):
        return G2, "cert-or-catalog-genlist"
    if L == "/home/user/.ssh/authorized_keys":
        return SO, "login-key"
    if L in ("/home/user/.bashrc", "/home/user/.profile"):
        return PD, "skel-copy-code"
    if L.startswith("/var/") or L in ("/etc/.combustion-result.json", "/etc/group-", "/etc/passwd-", "/etc/shadow-", "/etc/.ignition-result.json", "/etc/.pwd.lock", "/etc/audit/audit.rules.prev", "/etc/default/grub.old", "/etc/selinux/.autorelabel", "/etc/selinux/.relabelled", "/etc/selinux/selinux_modules_migrated-targeted", "/boot/mbrid", "/config.partids", "/.snapshots/1/info.xml", "/.snapshots/2/info.xml") \
            or L.startswith("/etc/crypto-policies/back-ends/"):
        return REC, "record-file"
    if t == "symlink" and (L.startswith("/boot/") or L == "/etc/ssl/certs"):
        return REC, "link-by-program"
    if L == "/boot/grub2/grubenv":
        return UNK, "grubenv"
    if CODE_PAT.search(L) and t == "file" or (t == "file" and d.get("shebang")):
        return PD, "code-copied-or-built"
    if L.startswith("/boot/grub2/") and t == "file":
        return REC, "grub-data-copy"
    if L.startswith("/usr/lib/sysimage/rpm/"):
        return REC, "rpmdb"
    if t == "directory":
        return REC, "dir-by-program"
    if L.startswith("/dev/") or L == "/dev":
        return REC, "dev-skeleton"
    return None, "UNRULED"

def mdec(path):
    snap = path.startswith(SNAP + "/")
    L = path[len(SNAP):] if snap else path
    if path == SNAP:
        return REC, "generation-root-dir"
    if L in rpm:
        r = received(path, L, snap)
        if r == "yes":
            return IP, "pkg-as-received"
        if r == "unverified":
            return UNK, "copy-unverified"
        return nonreceived(path, L, snap, r)
    return nonreceived(path, L, snap, "unpackaged")

RUNTIME_CREATORS = [
    ("/run/udev", "systemd-udevd (udev package)"),
    ("/run/systemd/generator", "systemd generators from fstab and unit settings (systemd package)"),
    ("/run/systemd/journal", "systemd-journald (systemd package)"),
    ("/run/systemd", "systemd and its daemons (systemd package)"),
    ("/run/user/1000", "the user's systemd manager and systemd-logind (systemd package)"),
    ("/run/user", "systemd-logind (systemd package)"),
    ("/run/NetworkManager", "NetworkManager (NetworkManager package)"),
    ("/run/chrony", "chronyd (chrony package)"),
    ("/run/dbus", "dbus-broker (dbus-broker package)"),
    ("/run/lvm", "lvm2 tools (lvm2 package)"), ("/run/lock", "lvm2 tools (lvm2 package)"),
    ("/run/blkid", "libblkid (util-linux)"), ("/run/fsck", "systemd-fsck (systemd package)"),
    ("/run/initramfs", "the initrd built by dracut (dracut and systemd packages)"),
    ("/run/mount", "libmount (util-linux)"), ("/run/polkit", "polkit (polkit package)"),
    ("/run/rebootmgr", "rebootmgrd (rebootmgr package)"), ("/run/sysextmgr", "sysextmgrd (sysextmgr)"),
    ("/run/log", "systemd-journald (systemd package)"), ("/run/credentials", "systemd (systemd package)"),
    ("/run/tmpfiles.d", "kmod static-nodes run by systemd (kmod, systemd)"), ("/run/varlink", "systemd (systemd package)"),
    ("/run/wtmpdb", "wtmpdbd (wtmpdb package)"),
    ("/tmp/systemd-private-", "systemd PrivateTmp= of the service unit (systemd package)"),
    ("/tmp/", "systemd-tmpfiles from packaged tmpfiles.d (systemd package)"),
    ("/run/", "daemons started by systemd (their packages)"),
]
def runtime_creator(L):
    for p, c in RUNTIME_CREATORS:
        if L.startswith(p): return c
    return "unidentified program"

# ---------------------------------------------------------------- helpers
def members(o):
    m = json.loads(o["members"])
    return list(csv.DictReader(open(base + "/" + m["file"]), delimiter="\t"))

LBL = {
    "pkg-as-received": "packaged files/dirs as received",
    "copy-unverified": "packaged copies whose full content is not verified",
    "mime-genlist": "MIME database files generated by update-mime-database",
    "modules-genlist": "module lists generated by depmod",
    "ldcache-genlist": "ldconfig cache",
    "selinux-genlist": "SELinux store files generated by semodule",
    "audit-genlist": "audit rules generated by augenrules",
    "state-record": "state/counter files",
    "setting-copy-inactive": "changed setting files in the inactive generation",
    "enable-link-copy-inactive": "unit enablement links in the inactive generation",
    "grubenv": "grub environment block",
    "code-copied-or-built": "code copied or built by the system",
    "grub-data-copy": "grub data copied from packages",
    "rpmdb": "rpm database",
    "dir-by-program": "directories created by programs",
    "dev-skeleton": "device skeleton entries",
    "generation-root-dir": "generation root directory",
}

def group_decision(decs, names):
    """decs: list of (decision,label) per member."""
    s = {d for d, _ in decs}
    if len(s) == 1:
        return s.pop(), None
    if UNK in s and len(s - {UNK}) == 1:
        return UNK, None
    return MIX, None

def describe_mix(decs, names):
    by = collections.OrderedDict()
    for (d, l), n in zip(decs, names):
        by.setdefault((d, l), []).append(n.rsplit("/", 1)[-1])
    parts = []
    for (d, l), ns in by.items():
        ex = ",".join(ns[:2]) + ("…" if len(ns) > 2 else "")
        parts.append(f"{d}: {len(ns)} {LBL.get(l, l)} ({ex})")
    return "; ".join(parts)
