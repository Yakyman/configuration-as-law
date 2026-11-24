import os as _os; NIGHT_DIR = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../..")) + "/"  # night folder
"""c2 classification of A3/in/part-server.tsv.

Appends to A3/c2/part-server.tsv every input row whose id is not yet in the output (keeps earlier rows).
Writes A3/c2/part-server.members.tsv (per-member decisions of group rows) when groups are decided.
Rules are stated in A3/c2/part-server.notes.md.
"""
import csv
import json
import os
import re
import sys

csv.field_size_limit(10**9)
NIGHT = NIGHT_DIR + ""
IN = NIGHT + "A3/in/part-server.tsv"
RAWROOT = NIGHT + "A3/in/raw/server/"
OUT = NIGHT + "A3/c2/part-server.tsv"
MEMOUT = NIGHT + "A3/c2/part-server.members.tsv"
HEADER = ["id", "decision", "sentences", "what_it_does", "basis", "reason"]

rows = list(csv.DictReader(open(IN), delimiter="\t"))

# ---------------------------------------------------------------- sentence sets
S_INST = "S8.2-6,S8.2-7,S8.2-8,S8.2-16"
S_PROG = "S8.2-6,S8.2-9,S8.2-10,S8.2-16"
S_SET = "S8.2-11,S8.2-12,S8.2-13,S8.2-17"
S_DEF = "S8.2-11,S8.2-13,S8.2-17"
S_REC = "S8.2-6,S8.2-15,S8.2-2"
S_MAT = "S8.2-6,S8.2-15,S8.2-2"
S_RUN = "S8.2-5"
S_ACT = "S8.2-3,S8.2-4"

DOC_K3S_INIT = "doc:https://docs.k3s.io/blog/2025/03/25/K3s-initialization"
DOC_K3S_PKG = "doc:https://docs.k3s.io/installation/packaged-components"
DOC_K3S_REQ = "doc:https://docs.k3s.io/installation/requirements"
DOC_DOCKER_IMG = "doc:https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/"
DOC_DOCKER_FW = "doc:https://docs.docker.com/engine/network/packet-filtering-firewalls/"
DOC_NFT = "doc:https://wiki.nftables.org/wiki-nftables/index.php/Scripting"
DOC_CRONTAB = "doc:https://manpages.debian.org/trixie/cron/crontab.5.en.html"
DOC_DEBPOL = "doc:https://www.debian.org/doc/debian-policy/ch-maintainerscripts.html"
DOC_PRIVTMP = "doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html"
DOC_RESOLVED = "doc:https://www.freedesktop.org/software/systemd/man/latest/systemd-resolved.service.html"

# creators named in RUNTIME reasons, with that object's decision
DOCKERD = "dockerd (docker-ce file; change not recorded: INSTALLED-PACKAGE if unchanged, else PROGRAM-OWN)"
DOCKERD_S = "dockerd (docker-ce; INSTALLED-PACKAGE if unchanged)"
K3S = "k3s process (bundled binary extracted by k3s: PROGRAM-DERIVED; /usr/local/bin/k3s PROGRAM-OWN)"
K3S_S = "k3s (PROGRAM-DERIVED from PROGRAM-OWN k3s)"
CONTAINERD = "containerd (containerd.io file; change not recorded)"
CALFW = "cal-firewall.service (SETTING-OWN)"


def row(id_, dec, sents, what, basis, reason):
    return {"id": id_, "decision": dec, "sentences": sents, "what_it_does": what, "basis": basis, "reason": reason}


# ================================================================ small kinds, by hand
def members_json(r):
    try:
        return json.loads(r["members"])
    except Exception:
        return {}


def decide_small(r):
    k, n, m = r["kind"], r["name"], members_json(r)
    rec = m.get("record", "")
    i = r["id"]
    if k == "1:account":
        if n == "Debian-exim":
            return row(i, "SETTING-DEFAULT", S_DEF + ",S8.1-11", "system account for the exim4 mail server",
                       "raw:raw/0113-metadata-read-320.out",
                       "An account is a setting; exim4-base.postinst runs adduser --system for it during package installation: a default created at installation, covered by the package line.")
        if n == "calops":
            return row(i, "SETTING-OWN", S_SET + ",S8.1-11", "login account calops created by the operator",
                       "evidence", "Accounts are settings (S8.2-13); calops was created by a person's action, not at a package installation, so it needs a line of its own.")
    if k == "1:group":
        if n == "users":
            return row(i, "SETTING-OWN", S_SET, "users group now listing calops as member",
                       "evidence", "Group membership is an account/rights setting; the member calops was added by creating that person's account, not by a package installation.")
        if n == "crontab":
            return row(i, "SETTING-DEFAULT", S_DEF, "system group owning crontab files",
                       "raw:raw/0111-metadata-read-192.out",
                       "A group is an account setting; cron-daemon-common.postinst runs addgroup --system crontab during installation: default covered by the package line.")
        if n == "Debian-exim":
            return row(i, "SETTING-DEFAULT", S_DEF, "system group of the exim4 mail server",
                       "raw:raw/0113-metadata-read-320.out",
                       "Group created by exim4-base.postinst (adduser --system --group) during package installation: a default covered by the package line.")
        if n == "docker":
            return row(i, "SETTING-DEFAULT", S_DEF, "group granting access to the docker socket",
                       "raw:raw/0113-metadata-read-320.out",
                       "A rights/account setting created by docker-ce.postinst (groupadd --system docker) during installation: default covered by the package line.")
        if n == "calops":
            return row(i, "SETTING-OWN", S_SET, "primary group of account calops",
                       "evidence", "Group created together with the person-created account calops; an account setting chosen by a person, needs its own line.")
    if k == "1:package":
        reason = m.get("reason")
        if reason == "explicit":
            return row(i, "INSTALLED-OWN", S_INST, f"Debian package {n.split(':',1)[1]} installed explicitly",
                       "raw:raw/0022-package-reasons-apt-manual.out",
                       "A package installed on the computer is an installed object (Q1); installed explicitly, not as a dependency, so no other line covers it: line of its own.")
        if reason == "dependency":
            return row(i, "INSTALLED-DERIVED", S_INST, f"Debian package {n.split(':',1)[1]} installed as a dependency",
                       "raw:raw/0023-package-reasons-apt-auto.out",
                       "Installed object (Q1); apt installed it as a dependency, which S8.2-16 names as a line from which the system obtained it.")
    if k == "1:service":
        return decide_service(i, n, rec)
    if k == "1:timer":
        return decide_timer(i, rec)
    if k == "1:unit-file":
        return decide_unitfile(i, n, rec)
    if k == "1:user-unit-file":
        return row(i, "INSTALLED-PACKAGE", S_INST, "user unit file of the D-Bus session bus",
                   "raw:package-files.tsv", "File /usr/lib/systemd/user/dbus.service obtained with dbus-user-session and recorded unchanged: installed object covered by the package line.")
    if k == "1:user-service":
        if "dbus.service" in n:
            return row(i, "INSTALLED-PACKAGE", S_INST, "static per-user D-Bus session bus service",
                       "raw:package-files.tsv", "Static user unit from dbus-user-session, unchanged; no enablement value exists, so the service is the package's object.")
        if "ssh-agent" in n:
            return row(i, "INSTALLED-PACKAGE", S_INST, "per-user OpenSSH agent service, not running",
                       "raw:package-files.tsv", "User unit /usr/lib/systemd/user/ssh-agent.service from openssh-client, unchanged; loaded, not enabled by a person: installed object.")
        return row(i, "RUNTIME", S_RUN, "dangling reference to absent unit in user manager",
                   "evidence", "systemd-remount-fs.service not-found exists only as a dependency reference inside the running user manager; belongs to the referring user unit (package file, INSTALLED-PACKAGE).")
    if k == "1:sudo-access":
        if n == "Matching":
            return row(i, "INSTALLED-PACKAGE", S_INST, "heading of Defaults entries from /etc/sudoers applying to calops",
                       "raw:package-files.tsv", "The Defaults entries come from /etc/sudoers, obtained with sudo and unchanged: default setting values listed under question 1.")
        if n == "User":
            return row(i, "SETTING-OWN", S_SET, "heading of sudo rights granted to calops",
                       "raw:raw/0104-sudo-calops.out", "Rights are settings (S8.2-13); calops's rights come from /etc/sudoers.d/calops, written by a person: line of its own.")
        return row(i, "SETTING-OWN", S_SET, "lets calops restart cal-node-exporter as root",
                   "raw:raw/0104-sudo-calops.out", "A right chosen by a person, granted by /etc/sudoers.d/calops; rights are settings needing a line of their own.")
    if k == "1:access-rule":
        if n == "/etc/sudoers.d/calops":
            return row(i, "SETTING-OWN", S_SET, "sudoers rule for calops restarting cal-node-exporter",
                       "raw:raw/0107-metadata-read-0.out", "Rights and access rules are settings; file written by a person's action, not by a package: line of its own.")
        if n == "/etc/sudoers.d/90-cloud-init-users":
            return row(i, "SETTING-OWN", S_SET + ",S8.2-18", "passwordless sudo for user, written by cloud-init",
                       "raw:raw/0107-metadata-read-0.out", "A right obeyed by sudo system-wide; written at first boot by cloud-init from instance configuration, not at package installation; setting however entered: own line.")
        if n == "/etc/pam.d/cron":
            return row(i, "INSTALLED-PACKAGE", S_INST, "PAM rules for the cron daemon",
                       "raw:package-files.tsv", "Conffile obtained with cron and recorded unchanged: a default setting value, which question 1 makes an installed object of the package.")
    if k == "1:docker-container":
        return row(i, "PROGRAM-DERIVED", S_PROG + ",S8.2-22", f"compose container {m.get('Names','')} running image {m.get('Image','').split('/')[-1]}",
                   "raw:raw/0084-docker-container.out",
                   "Runs as its own process: a program (S8.2-22); docker compose created it from /home/user/server-stack/compose.yaml, the line from which the system built it.")
    if k == "1:docker-image":
        return row(i, "GAP-TWO", "S8.1-4,S8.1-6,S8.2-7,S8.2-9,S8.2-16", f"container image {m.get('Repository')}:{m.get('Tag')} pulled for compose",
                   DOC_DOCKER_IMG,
                   "INSTALLED-DERIVED if Docker counts as installer (docs call an image a package of binaries; pulled/removed whole) or PROGRAM-DERIVED; S8.1-4 needs documented 'installing programs', docs never say so.")
    if k == "1:firewall-table":
        return decide_nft(r)
    if k == "2:image-container-store":
        return decide_store(r, m)
    return None


def decide_service(i, n, rec):
    name = rec.split()[1] if rec.startswith("*") else n
    if "not-found" in rec:
        ref = {"firewalld.service": "docker.service (docker-ce unit lists it in After=)"}.get(name, "a loaded unit (referrer not recorded)")
        return row(i, "RUNTIME", S_RUN, f"{name}: absent unit known only as dependency reference",
                   "raw:raw/0070-service.out",
                   f"No such unit on disk; systemd holds it only as a relationship between services while running; belongs to {ref}, an INSTALLED-PACKAGE unit file.")
    own = {"cal-firewall.service": "oneshot loading the operator's nftables input firewall",
           "cal-maintenance.service": "writes daily maintenance timestamp, started by cal-maintenance.timer",
           "cal-node-exporter.service": "runs node_exporter metrics exporter as a system service",
           "k3s.service": "runs the k3s Kubernetes server"}
    if n in own:
        return row(i, "SETTING-OWN", S_SET + ",S8.1-11", own[n], "evidence",
                   "A service and its parameters are a setting; unit written and enabled by a person's actions (or the k3s script they ran), not by a package: own line.")
    dflt = {"containerd.service": ("containerd runtime used by Docker", "containerd.io.postinst"),
            "cron.service": ("cron daemon running scheduled jobs", "cron.postinst"),
            "docker.service": ("Docker Engine daemon", "docker-ce.postinst"),
            "exim4.service": ("exim4 mail transport agent daemon", "exim4-daemon-light.postinst")}
    if n in dflt:
        what, script = dflt[n]
        return row(i, "SETTING-DEFAULT", S_DEF + ",S8.1-11", what, "raw:raw/0113-metadata-read-320.out",
                   f"A service is a setting, in force when enabled; {script} enabled it via deb-systemd-helper during installation (state recorded): default covered by the package line.")
    static = {"exim4-base.service": "exim4 housekeeping, started by exim4-base.timer",
              "ldconfig.service": "rebuilds dynamic linker cache at boot when needed",
              "logrotate.service": "rotates log files, started by logrotate.timer",
              "systemd-journal-catalog-update.service": "rebuilds journal message catalog when needed",
              "systemd-machine-id-commit.service": "saves transient machine-id to disk when needed",
              "systemd-sysusers.service": "creates system users declared in sysusers.d",
              "systemd-update-done.service": "marks /etc and /var as updated after package changes"}
    if n in static:
        return row(i, "INSTALLED-PACKAGE", S_INST, static[n], "raw:package-files.tsv",
                   "Static unit with no enablement value; defined and wired entirely by its unchanged package unit file: installed object covered by the package line.")
    return None


def decide_timer(i, rec):
    t = rec.split()[-2]
    if t == "cal-maintenance.timer":
        return row(i, "SETTING-OWN", S_SET + ",S8.2-14", "daily timer starting cal-maintenance.service",
                   "evidence", "A timer launching a service is a service parameter, a setting; written and enabled by a person's action: line of its own.")
    if t == "systemd-tmpfiles-clean.timer":
        return row(i, "INSTALLED-PACKAGE", S_INST, "daily cleanup of temporary directories",
                   "raw:package-files.tsv", "Static timer wired by systemd package files, unchanged; no enablement value: installed object covered by the package line.")
    pk = {"apt-listchanges.timer": "apt-listchanges", "dpkg-db-backup.timer": "dpkg", "exim4-base.timer": "exim4-base",
          "logrotate.timer": "logrotate", "apt-daily.timer": "apt", "apt-daily-upgrade.timer": "apt",
          "man-db.timer": "man-db", "e2scrub_all.timer": "e2fsprogs", "fstrim.timer": "util-linux"}[t]
    what = {"apt-listchanges.timer": "periodic apt-listchanges run", "dpkg-db-backup.timer": "daily backup of dpkg database",
            "exim4-base.timer": "daily exim4 housekeeping", "logrotate.timer": "daily log rotation",
            "apt-daily.timer": "daily apt package list update", "apt-daily-upgrade.timer": "daily unattended upgrade run",
            "man-db.timer": "daily manual page index update", "e2scrub_all.timer": "weekly ext4 metadata check",
            "fstrim.timer": "weekly discard of unused blocks"}[t]
    return row(i, "SETTING-DEFAULT", S_DEF, what, "evidence",
               f"Timer enablement is a service setting; deb-systemd-helper enabled {t} during {pk} installation (state in deb-systemd-helper-enabled): default covered by package line.")


def decide_unitfile(i, n, rec):
    own = {"cal-firewall.service", "cal-maintenance.service", "cal-node-exporter.service", "k3s.service", "cal-maintenance.timer"}
    if n in own:
        return row(i, "SETTING-OWN", S_SET + ",S8.2-23", f"unit file {n} in /etc/systemd/system",
                   "evidence", "Unit file read by systemd as values, not executed (S8.2-23): service parameters chosen by a person (or the k3s script they ran): own line.")
    return row(i, "INSTALLED-PACKAGE", S_INST, f"packaged unit file {n} with its enablement state",
               "raw:package-files.tsv", "The unit file was obtained with its package and is recorded unchanged: installed object covered by the package line (enablement decided on the service row).")


# ================================================================ firewall
def fw_creator(text, table):
    t = text
    if "cal_filter" in t:
        return CALFW, "table and rules of the operator's nftables input firewall"
    if re.search(r"KUBE|FLANNEL|flannel|kube|cni0|10\.42\.|10\.43\.|flannel\.1", t):
        return K3S, "Kubernetes service, pod and network-policy packet filtering from k3s"
    if re.search(r"DOCKER|docker0|br-91deedb1c880|172\.1[78]\.|18081", t):
        return DOCKERD + "; networks/ports per compose.yaml (SETTING-OWN)", "Docker container networking and port publishing rules"
    if table == "raw":
        return DOCKERD, "built-in raw table chain used by Docker"
    if table == "mangle":
        return K3S, "built-in mangle chain used by kubelet hint chains"
    return "dockerd (docker-ce) or k3s, whichever first created it (not recorded); RUNTIME either way", "built-in table or base chain shared by Docker and k3s"


def decide_nft(r):
    m = members_json(r)
    i, n = r["id"], r["name"]
    table = m.get("table") or m.get("name", "")
    text = n + " " + json.dumps(m)
    creator, what = fw_creator(text, table)
    return row(i, "RUNTIME", S_RUN + ",S8.2-13", what[:90], "raw:raw/0077-firewall-nft.out",
               f"Kernel netfilter object, exists only while the computer runs; belongs to {creator}.")


_ipt_table = {"1:firewall-ipv4": None, "1:firewall-ipv6": None}


def decide_ipt(r):
    m = members_json(r)
    rec = m.get("record", "")
    k = r["kind"]
    src = "raw:raw/0078-firewall-ipv4.out" if k.endswith("ipv4") else "raw:raw/0079-firewall-ipv6.out"
    if rec.startswith("*"):
        _ipt_table[k] = rec[1:]
    i = r["id"]
    if rec.startswith("#") or rec == "COMMIT":
        return row(i, "ACTION", S_ACT, "line printed by the inventory's iptables-save run",
                   src, "Not an object on the computer: header/terminator text produced by the collector's own command at collection time, part of that action.")
    table = _ipt_table[k] or ""
    creator, what = fw_creator(rec, table)
    if rec.startswith("*"):
        what = f"iptables {rec[1:]} table (nf_tables backend)"
    return row(i, "RUNTIME", S_RUN + ",S8.2-13", what[:90], src,
               f"Kernel netfilter object, exists only while the computer runs; belongs to {creator}.")


# ================================================================ processes, ports, modules
def pkg_index():
    pf = list(csv.DictReader(open(RAWROOT + "package-files.tsv"), delimiter="\t"))
    objs = {o["id"]: o for o in csv.DictReader(open(RAWROOT + "objects.tsv"), delimiter="\t")}
    idx = {}
    for p in pf:
        o = objs.get(p["package"])
        idx[p["path"]] = (o["name"].split(":", 1)[1] if o else p["package"], p["integrity"])
    return idx


PKG = pkg_index()


def prog_decision(path):
    if path in PKG:
        pkg, integ = PKG[path]
        if integ == "unchanged":
            return f"{path} ({pkg} file, unchanged: INSTALLED-PACKAGE)"
        return f"{path} ({pkg} file, change not recorded: INSTALLED-PACKAGE if unchanged, else PROGRAM-OWN)"
    return None


CONTAINER_PROGS = {
    "/usr/bin/caddy": "caddy:2-alpine image of the compose proxy container (GAP-TWO: INSTALLED-/PROGRAM-DERIVED)",
    "/usr/local/bin/postgres": "postgres:17-alpine image of the compose db container (GAP-TWO: INSTALLED-/PROGRAM-DERIVED)",
    "/whoami": "traefik/whoami image of compose web container or cal-web pod (GAP-TWO: INSTALLED-/PROGRAM-DERIVED)",
    "/pause": "k3s pod sandbox pause image pulled by k3s (GAP-TWO: INSTALLED-/PROGRAM-DERIVED)",
    "/coredns": "coredns image from k3s packaged manifest (GAP-TWO: INSTALLED-/PROGRAM-DERIVED)",
    "/metrics-server": "metrics-server image from k3s packaged manifest (GAP-TWO: INSTALLED-/PROGRAM-DERIVED)",
    "/usr/bin/local-path-provisioner": "local-path-provisioner image from k3s manifest (GAP-TWO: INSTALLED-/PROGRAM-DERIVED)",
}


def decide_process(r):
    rec = members_json(r).get("record", "")
    pid, exe = rec.split("\t", 1)
    i = r["id"]
    if exe == "unknown":
        return row(i, "RUNTIME", S_RUN, f"process {pid}; executable path not recorded by the inventory",
                   "raw:raw/0086-process-executables.out",
                   "A process exists only while the computer runs; whatever program started it, the decision is RUNTIME; the creating program is not recorded.")
    if "/var/lib/rancher/k3s/data/" in exe:
        b = os.path.basename(exe)
        return row(i, "RUNTIME", S_RUN + ",S8.2-22", f"process {pid} of k3s bundled {b}", "raw:raw/0086-process-executables.out",
                   f"Process; belongs to {b} extracted by k3s into its data dir (PROGRAM-DERIVED from /usr/local/bin/k3s, PROGRAM-OWN).")
    if exe in CONTAINER_PROGS:
        return row(i, "RUNTIME", S_RUN + ",S8.2-22", f"container process {pid} running {exe}", "raw:raw/0086-process-executables.out",
                   f"Process exists only while running; belongs to {exe} from the {CONTAINER_PROGS[exe]}.")
    if exe == "/usr/local/bin/node_exporter":
        return row(i, "RUNTIME", S_RUN, f"process {pid} of node_exporter metrics exporter", "raw:raw/0086-process-executables.out",
                   "Process; belongs to /usr/local/bin/node_exporter, a downloaded program placed by a person (PROGRAM-OWN), started by cal-node-exporter.service (SETTING-OWN).")
    if exe == "/tmp/c1-collector/probe":
        return row(i, "RUNTIME", S_RUN, f"process {pid} of the inventory collector probe", "raw:raw/0086-process-executables.out",
                   "Process; belongs to the collector program the operator copied to /tmp for this inventory (code outside packages: PROGRAM-OWN).")
    d = prog_decision(exe)
    if d:
        return row(i, "RUNTIME", S_RUN, f"process {pid} running {exe}", "raw:raw/0086-process-executables.out",
                   f"A process exists only while the computer runs; it belongs to {d}.")
    return None


PORTS = {
    "8472": ("flannel VXLAN endpoint of k3s", K3S_S, DOC_K3S_REQ),
    "5355": ("LLMNR responder of systemd-resolved", "systemd-resolved (package file unchanged: INSTALLED-PACKAGE)", DOC_RESOLVED),
    "53": ("local DNS stub of systemd-resolved", "systemd-resolved (package file unchanged: INSTALLED-PACKAGE)", DOC_RESOLVED),
    "68": ("DHCP client socket on ens3", "systemd-networkd (systemd file unchanged: INSTALLED-PACKAGE) per netplan setting", "evidence"),
    "10248": ("kubelet health endpoint inside k3s", K3S_S, DOC_K3S_REQ),
    "10249": ("kube-proxy metrics endpoint inside k3s", K3S_S, DOC_K3S_REQ),
    "10258": ("cloud-controller-manager endpoint inside k3s", K3S_S, DOC_K3S_REQ),
    "10259": ("kube-scheduler endpoint inside k3s", K3S_S, DOC_K3S_REQ),
    "10256": ("kube-proxy health endpoint inside k3s", K3S_S, DOC_K3S_REQ),
    "10257": ("kube-controller-manager endpoint inside k3s", K3S_S, DOC_K3S_REQ),
    "6444": ("internal API endpoint of k3s supervisor", K3S_S, DOC_K3S_REQ),
    "22": ("SSH server listening socket", "sshd (openssh-server file unchanged: INSTALLED-PACKAGE)", "evidence"),
    "9100": ("node_exporter metrics endpoint", "node_exporter (PROGRAM-OWN) via cal-node-exporter.service (SETTING-OWN)", "evidence"),
    "25": ("local SMTP listener of exim4", "exim4 (exim4-daemon-light file unchanged: INSTALLED-PACKAGE)", "evidence"),
    "18081": ("published compose proxy port 127.0.0.1:18081", "docker-proxy (docker-ce, unchanged: INSTALLED-PACKAGE) per compose.yaml (SETTING-OWN)", "raw:raw/0084-docker-container.out"),
    "10010": ("containerd CRI streaming endpoint of k3s", K3S_S, DOC_K3S_REQ),
    "10250": ("kubelet API of k3s", K3S_S, DOC_K3S_REQ),
    "6443": ("Kubernetes API server of k3s", K3S_S, DOC_K3S_REQ),
}


def decide_port(r):
    rec = members_json(r).get("record", "")
    local = rec.split()[4]
    port = local.rsplit(":", 1)[1]
    what, creator, basis = PORTS[port]
    return row(r["id"], "RUNTIME", S_RUN, f"{r['name']} {local}: {what}", basis,
               f"Open port: exists only while running (S8.2-5); listener not recorded; documented user of this port: {creator}.")


def decide_module(r):
    n = r["name"]
    return row(r["id"], "RUNTIME", S_RUN, f"loaded kernel module {n}", "raw:raw/0087-module-names.out",
               "A loaded module exists only while running; loader not recorded (k3s, dockerd, nft rules or kernel autoload); RUNTIME for any of them; module file belongs to the kernel package.")


# ================================================================ executable code outside packages
def decide_exec(r):
    p = r["name"]
    i = r["id"]
    if re.match(r"^/home/[^/]+/\.(bashrc|profile|bash_logout)$", p):
        return row(i, "PROGRAM-DERIVED", S_PROG + ",S8.2-23", f"shell startup file {os.path.basename(p)} copied from /etc/skel", "evidence",
                   "Shell executes it as code: a program; account creation (useradd/cloud-init) copied it from /etc/skel, so the system built it from the account line.")
    if p == "/usr/local/bin/k3s":
        return row(i, "PROGRAM-OWN", S_PROG + ",S8.1-4", "k3s Kubernetes distribution binary", "raw:../../operator/server/actions-logs/server_orchestrator.log",
                   "Code outside packages, put by the downloaded get.k3s.io script, which is no installer of the system (S8.1-4): a program needing a line of its own.")
    if p in ("/usr/local/bin/k3s-killall.sh", "/usr/local/bin/k3s-uninstall.sh"):
        return row(i, "PROGRAM-OWN", S_PROG, f"{os.path.basename(p)} shell script written by k3s install script", "raw:../../operator/server/actions-logs/server_orchestrator.log",
                   "Executable shell script outside packages, created by the person-run k3s install script, not built by the system from a line: line of its own.")
    if p == "/usr/local/bin/node_exporter":
        return row(i, "PROGRAM-OWN", S_PROG, "Prometheus node_exporter metrics binary", "raw:../../operator/server/actions-logs/server_binary_service.log",
                   "Downloaded tarball binary placed by a person; code outside any package: a program needing a line of its own.")
    if p == "/var/lib/cni/networks/cbr0/lock":
        return row(i, "RECORD", S_REC + ",S8.2-20", "empty lock file of CNI host-local IP allocator", "evidence",
                   "Zero bytes: contains no code despite the execute bit, so not a program; written by the CNI plugin as it ran: program record.")
    if p.startswith("/var/lib/dpkg/info/"):
        return row(i, "UNKNOWN", S_INST + ",S8.2-9", f"dpkg maintainer script {os.path.basename(p)}", DOC_DEBPOL,
                   "Obtained in the package's control area; fact missing: unchanged since installation (not in package-files). Unchanged gives INSTALLED-PACKAGE, changed gives PROGRAM-OWN.")
    if "/var/lib/rancher/k3s/data/" in p:
        return row(i, "PROGRAM-DERIVED", S_PROG, f"k3s bundled userspace tool {os.path.basename(p)}", DOC_K3S_INIT,
                   "Executable code k3s extracts from its own binary into data/<hash>: built by the system from the k3s line (k3s itself PROGRAM-OWN).")
    return None


# ================================================================ stored-object stores (not expanded)
def decide_store(r, m):
    p = r["name"]
    i = r["id"]
    if m.get("metadata", {}).get("persistence") == "runtime":
        return row(i, "RUNTIME", S_RUN, "k3s containerd runtime state directory on tmpfs", "evidence",
                   "On tmpfs: exists only while running; belongs to the containerd embedded in k3s (PROGRAM-DERIVED from PROGRAM-OWN k3s).")
    what = {"/var/lib/containerd": "containerd content/snapshot store used by Docker",
            "/var/lib/docker": "Docker Engine data: containers, volumes, networks, image metadata",
            "/var/lib/kubelet/pods": "kubelet per-pod volumes and state",
            "/var/lib/rancher/k3s/agent/containerd": "k3s containerd image content and snapshot store"}[p]
    return row(i, "UNKNOWN", S_INST + ",S8.2-9,S8.2-15", what, "evidence",
               "Not expanded by the inventory (expanded=false); holds images, container layers, volumes, state of different kinds. Missing fact: its member list; decision per member unknown.")


# ================================================================ group members
def mrule(path, typ, pers):
    """Return (decision, sentences, short reason) for one immediate member of a stored group."""
    b = os.path.basename(path)
    # --- runtime
    if path.startswith("/run/docker/netns/"):
        return ("RUNTIME", S_RUN, "network-namespace mount point (nsfs) of a container; dockerd")
    if pers == "runtime":
        return ("RUNTIME", S_RUN, "on tmpfs; created while running by " + run_creator(path))
    if typ == "socket":
        return ("RUNTIME", S_RUN, "socket of a listening program: " + ("k3s/kubelet" if "kube" in path or "rancher" in path else "running daemon"))
    if re.match(r"^/var/tmp/systemd-private-", path):
        return ("RUNTIME", S_RUN + ",S8.2-13", "PrivateTmp directory systemd removes when the unit stops; belongs to the packaged unit's PrivateTmp setting")
    # --- root, boot
    if path == "/swap-cal":
        return ("SETTING-OWN", S_SET, "swap area created by a person and listed in fstab: devices/filesystems setting")
    if path in ("/lost+found", "/media", "/mnt", "/srv", "/opt", "/etc/opt", "/usr/local/etc", "/usr/local/games",
                "/usr/local/include", "/usr/local/lib", "/usr/local/libexec", "/usr/local/sbin", "/usr/local/share",
                "/usr/local/src", "/usr/local/bin", "/usr/local/man", "/etc/python3"):
        return ("RECORD", S_REC, "empty/structural directory or link made by installation programs; no code, no chosen value")
    if path.startswith("/boot/grub/"):
        if b == "grubenv":
            return ("RECORD", S_REC, "GRUB environment block rewritten at boot")
        if b == "grub.cfg":
            return ("PROGRAM-DERIVED", S_PROG + ",S8.2-23", "GRUB script executed by GRUB, generated by update-grub from recorded packages/settings")
        return ("PROGRAM-DERIVED", S_PROG, "GRUB modules/fonts/locales copied by grub-install from grub packages")
    # --- /etc single files
    E = {
        "/etc/.pwd.lock": ("RECORD", S_REC, "lock file of shadow tools"),
        "/etc/.resolv.conf.systemd-resolved.bak": ("RECORD", S_REC, "backup written by systemd-resolved postinst"),
        "/etc/.updated": ("RECORD", S_REC, "stamp written by systemd-update-done"),
        "/etc/aliases": ("SETTING-DEFAULT", S_DEF, "mail aliases created by exim4-config.postinst at installation (11:14:28)"),
        "/etc/ca-certificates.conf": ("UNKNOWN", S_DEF, "trusted-CA selection; image-build file: created by ca-certificates.postinst (DEFAULT) or changed by image builder (OWN) not recorded"),
        "/etc/ca-certificates.conf.dpkg-old": ("RECORD", S_REC, "backup kept by the maintainer script"),
        "/etc/cal-firewall.nft": ("UNKNOWN", "S8.2-9,S8.2-11,S8.2-23", "content and loader not recorded: nft -f script gives PROGRAM-OWN, values only gives SETTING-OWN"),
        "/etc/cloud-release": ("RECORD", S_REC, "image release identification written by image build"),
        "/etc/fstab": ("SETTING-OWN", S_SET, "filesystems and swap chosen by people"),
        "/etc/group": ("SETTING-OWN", S_SET, "groups incl. person-created ones"),
        "/etc/gshadow": ("SETTING-OWN", S_SET, "group passwords/admins"),
        "/etc/passwd": ("SETTING-OWN", S_SET, "accounts incl. calops"),
        "/etc/shadow": ("SETTING-OWN", S_SET, "account password data"),
        "/etc/subgid": ("SETTING-OWN", S_SET, "subordinate gid ranges of accounts"),
        "/etc/subuid": ("SETTING-OWN", S_SET, "subordinate uid ranges of accounts"),
        "/etc/hostname": ("SETTING-OWN", S_SET + ",S8.2-18", "host name set by cloud-init from instance data"),
        "/etc/hosts": ("UNKNOWN", S_DEF, "name resolution table; image-build: netbase script default or image builder value not recorded"),
        "/etc/hosts.allow": ("UNKNOWN", S_DEF, "access rules; image-build: libwrap0 script default or builder value not recorded"),
        "/etc/hosts.deny": ("UNKNOWN", S_DEF, "access rules; image-build: libwrap0 script default or builder value not recorded"),
        "/etc/inputrc": ("RECORD", S_REC + ",S8.2-14", "readline keys for programs a person runs; launches nothing, grants nothing: record (S8.2-14)"),
        "/etc/kernel-img.conf": ("SETTING-OWN", S_SET, "kernel install hook settings written by image build, no package script"),
        "/etc/ld.so.cache": ("RECORD", S_REC, "cache generated by ldconfig"),
        "/etc/locale.conf": ("UNKNOWN", S_DEF, "language setting; package-script default or image-builder value not recorded"),
        "/etc/locale.gen": ("UNKNOWN", S_DEF, "language setting; package-script default or image-builder value not recorded"),
        "/etc/localtime": ("UNKNOWN", S_DEF, "time zone link; tzdata default or image-builder value not recorded"),
        "/etc/machine-id": ("RECORD", S_REC, "identifier generated by systemd at first boot"),
        "/etc/mailname": ("SETTING-DEFAULT", S_DEF, "mail name created by exim4-config.postinst at installation"),
        "/etc/motd": ("SETTING-DEFAULT", S_DEF, "login message copied by base-files.postinst, package mtime kept"),
        "/etc/mtab": ("RECORD", S_REC, "compatibility link to kernel mount list made by installer"),
        "/etc/networks": ("UNKNOWN", S_DEF, "network names; netbase default or builder value not recorded"),
        "/etc/nsswitch.conf": ("UNKNOWN", S_DEF, "name-service order; package-script default or builder value not recorded"),
        "/etc/profile": ("PROGRAM-DERIVED", S_PROG + ",S8.2-23", "shell code copied from base-files by its postinst"),
        "/etc/resolv.conf": ("UNKNOWN", S_DEF, "resolver link; systemd-resolved default or builder value not recorded"),
        "/etc/shells": ("UNKNOWN", S_DEF, "valid login shells; package add-shell default or builder value not recorded"),
        "/etc/vconsole.conf": ("UNKNOWN", S_DEF, "console keyboard link; package default or builder value not recorded"),
        "/etc/rancher": ("RECORD", S_REC, "directory created by k3s"),
        "/etc/rancher/k3s": ("RECORD", S_REC, "directory created by k3s"),
        "/etc/rancher/node": ("RECORD", S_REC, "directory created by k3s"),
        "/etc/rancher/k3s/k3s.yaml": ("RECORD", S_REC, "admin kubeconfig generated by k3s as it ran"),
        "/etc/rancher/node/password": ("RECORD", S_REC, "node password generated by k3s"),
        "/etc/apt/apt.conf.d/20auto-upgrades": ("SETTING-OWN", S_SET, "automatic update periods set by a person's action (11:15:13)"),
        "/etc/apt/apt.conf.d/50unattended-upgrades": ("SETTING-DEFAULT", S_DEF, "unattended-upgrades config installed by its postinst, package mtime kept"),
        "/etc/apt/keyrings/docker.asc": ("SETTING-OWN", S_SET, "repository signing key apt trusts, added by a person"),
        "/etc/apt/mirrors/debian-security.list": ("SETTING-OWN", S_SET + ",S8.2-18", "package mirror written by cloud-init from instance configuration"),
        "/etc/apt/mirrors/debian.list": ("SETTING-OWN", S_SET + ",S8.2-18", "package mirror written by cloud-init from instance configuration"),
        "/etc/apt/sources.list.d/debian.sources": ("SETTING-OWN", S_SET, "package sources written by image build, no package script"),
        "/etc/apt/sources.list.d/docker.sources": ("SETTING-OWN", S_SET, "Docker repository added by a person"),
        "/etc/cron.d/cal-maintenance": ("GAP-TWO", "S8.2-9,S8.2-11,S8.2-14,S8.2-23", "cron reads it as schedule values but runs its command field via /bin/sh: PROGRAM-OWN or SETTING-OWN"),
        "/etc/default/exim4": ("SETTING-DEFAULT", S_DEF, "exim4 daemon defaults created by exim4-config.postinst at installation"),
        "/etc/default/locale": ("UNKNOWN", S_DEF, "locale link; package default or builder value not recorded"),
        "/etc/exim4/update-exim4.conf.conf": ("SETTING-DEFAULT", S_DEF, "exim4 debconf settings written by exim4-config.postinst at installation"),
        "/etc/logrotate.d/cal-maintenance": ("UNKNOWN", "S8.2-9,S8.2-11,S8.2-23", "content not recorded: pre/postrotate script would make it code (GAP like cron), values only SETTING-OWN"),
        "/etc/netplan/50-cloud-init.yaml": ("SETTING-OWN", S_SET + ",S8.2-18", "network setting written by cloud-init from instance data"),
        "/etc/ssh/sshd_config": ("UNKNOWN", S_DEF, "SSH login policy; openssh-server ucf default or builder change not recorded"),
        "/etc/ssh/sshd_config.d/50-cloud-init.conf": ("SETTING-OWN", S_SET + ",S8.2-18", "login policy written by cloud-init from configuration"),
        "/etc/sudoers.d/90-cloud-init-users": ("SETTING-OWN", S_SET, "rights written by cloud-init for user"),
        "/etc/sudoers.d/calops": ("SETTING-OWN", S_SET, "rights written by a person"),
        "/etc/sysctl.d/90-cal-server.conf": ("SETTING-OWN", S_SET, "kernel parameters chosen by a person"),
        "/etc/systemd/system/cal-firewall.service": ("SETTING-OWN", S_SET, "person's unit file"),
        "/etc/systemd/system/cal-maintenance.service": ("SETTING-OWN", S_SET, "person's unit file"),
        "/etc/systemd/system/cal-maintenance.timer": ("SETTING-OWN", S_SET, "person's timer unit"),
        "/etc/systemd/system/cal-node-exporter.service": ("SETTING-OWN", S_SET, "person's unit file"),
        "/etc/systemd/system/k3s.service": ("SETTING-OWN", S_SET, "unit written by the k3s script a person ran"),
        "/etc/systemd/system/k3s.service.env": ("SETTING-OWN", S_SET, "empty environment file of k3s.service, written by the script a person ran"),
        "/etc/systemd/system/sshd.service": ("SETTING-DEFAULT", S_DEF, "alias link created by openssh-server postinst (deb-systemd-helper state)"),
        "/etc/systemd/system/dbus-org.freedesktop.resolve1.service": ("SETTING-DEFAULT", S_DEF, "alias from enabling systemd-resolved in its postinst (dsh state)"),
        "/etc/systemd/system/dbus-org.freedesktop.timesync1.service": ("SETTING-DEFAULT", S_DEF, "alias from enabling systemd-timesyncd in its postinst (dsh state)"),
        "/etc/systemd/system/dbus-org.freedesktop.network1.service": ("SETTING-OWN", S_SET, "alias from enabling systemd-networkd by image build; no package-script state"),
        "/usr/lib/systemd/system/containerd.service": ("INSTALLED-PACKAGE", S_INST, "unit file of containerd.io (dpkg lists it as /lib/...; unchanged)"),
        "/usr/lib/systemd/system/screen-cleanup.service": ("SETTING-DEFAULT", S_DEF, "mask link made by screen.postinst at installation"),
        "/home/calops": ("RECORD", S_REC, "home directory made by account creation tool"),
        "/home/user": ("RECORD", S_REC, "home directory made by cloud-init account creation"),
        "/home/calops/.ssh": ("MATERIAL", S_MAT, "directory created by a person's action"),
        "/home/calops/.ssh/authorized_keys": ("SETTING-OWN", S_SET, "permitted login key for calops: means of login"),
        "/home/user/.ssh": ("RECORD", S_REC, "directory made by cloud-init"),
        "/home/user/.ssh/authorized_keys": ("SETTING-OWN", S_SET + ",S8.2-18", "permitted login key written by cloud-init from instance data"),
        "/home/user/.ssh/calops": ("MATERIAL", S_MAT, "private key for logging in to another account"),
        "/home/user/.ssh/calops.pub": ("MATERIAL", S_MAT, "public half of that key, created by a person"),
        "/home/user/.local": ("MATERIAL", S_MAT, "directory created by a person's script"),
        "/home/user/.local/state": ("MATERIAL", S_MAT, "directory created by a person's script"),
        "/home/user/.local/state/cal-server": ("MATERIAL", S_MAT, "directory created by a person's script"),
        "/home/user/.local/state/cal-server/node-exporter.sha256": ("MATERIAL", S_MAT, "checksum line downloaded/kept by a person"),
        "/home/user/.sudo_as_admin_successful": ("RECORD", S_REC, "marker written by sudo"),
        "/home/user/actions-logs": ("MATERIAL", S_MAT, "directory created by the operator's harness"),
        "/home/user/actions-status.tsv": ("RECORD", S_REC, "status table written by the action harness"),
        "/home/user/server-stack": ("MATERIAL", S_MAT, "project directory created by a person"),
        "/home/user/server-stack/compose.yaml": ("SETTING-OWN", S_SET + ",S8.2-14", "compose project launching containers"),
        "/home/user/server-stack/Caddyfile": ("SETTING-OWN", S_SET, "parameters of the caddy proxy service (bind-mounted)"),
        "/home/user/server-stack/workload.yaml": ("SETTING-OWN", S_SET + ",S8.2-14", "Kubernetes deployment/service applied to k3s"),
        "/root/.kube": ("RECORD", S_REC, "kubectl cache directory"),
        "/root/.ssh": ("RECORD", S_REC, "directory made by cloud-init"),
        "/root/.ssh/authorized_keys": ("SETTING-OWN", S_SET, "empty root login key list written by cloud-init: means of login"),
        "/var/lib/rancher/k3s/server/db/state.db": ("GAP-TWO", "S8.2-12,S8.2-15", "stores the person's applied workload (setting, whatever file stores it) and k3s working state: SETTING-OWN or RECORD"),
        "/var/lib/rancher/k3s/server/db/state.db-wal": ("GAP-TWO", "S8.2-12,S8.2-15", "write-ahead log of the same store: SETTING-OWN or RECORD"),
        "/var/lib/dpkg/statoverride": ("UNKNOWN", S_DEF, "permission overrides; cron entry made by cron.postinst, origin of earlier entries not recorded (DEFAULT or OWN)"),
    }
    if path in E:
        return E[path]
    if path.startswith("/opt/containerd"):
        return ("RECORD", S_REC, "empty plugin directory created by containerd as it ran")
    if path in ("/usr/local/bin/k3s", "/usr/local/bin/k3s-killall.sh", "/usr/local/bin/k3s-uninstall.sh", "/usr/local/bin/node_exporter"):
        return ("PROGRAM-OWN", S_PROG, "code outside packages placed by a person or the person-run k3s script")
    if path in ("/usr/local/bin/kubectl", "/usr/local/bin/crictl"):
        return ("PROGRAM-OWN", S_PROG, "command name linking to k3s, made by the person-run k3s script; running it runs k3s code")
    if re.match(r"^/home/[^/]+/\.(bashrc|profile|bash_logout)$", path) or path in ("/root/.bashrc", "/root/.profile"):
        return ("PROGRAM-DERIVED", S_PROG + ",S8.2-23", "shell startup code copied by the system (skel/base-files)")
    if re.match(r"^/etc/(group|gshadow|passwd|shadow|subuid|subgid)-$", path):
        return ("RECORD", S_REC, "backup copy kept by shadow tools")
    if path.startswith("/home/user/actions-logs/"):
        return ("RECORD", S_REC, "output log of an action run")
    if re.match(r"^/etc/ssh/ssh_host_", path):
        return ("RECORD", S_REC, "host key generated at first boot; not chosen, not a login permission")
    # systemd enablement links
    if re.match(r"^/etc/systemd/system/[^/]+\.wants/", path) or re.match(r"^/etc/rc[0-6S]\.d/", path):
        unit = re.sub(r"^[SK][0-9]+", "", b)
        if unit in ("cal-firewall.service", "cal-node-exporter.service", "k3s.service", "cal-maintenance.timer"):
            return ("SETTING-OWN", S_SET, "enablement link created by a person's action")
        if unit in ("systemd-networkd.service", "systemd-networkd.socket"):
            return ("SETTING-OWN", S_SET, "enablement made at image build, no deb-systemd-helper state")
        if unit == "remote-fs.target":
            return ("SETTING-DEFAULT", S_DEF, "enabled by systemd.postinst on new installs")
        if path.startswith("/etc/rc"):
            return ("SETTING-DEFAULT", S_DEF, "SysV link made by update-rc.d in package maintainer scripts")
        return ("SETTING-DEFAULT", S_DEF, "enablement link made by deb-systemd-helper during package installation (state recorded)")
    if re.match(r"^/etc/systemd/system/[^/]+\.wants$", path):
        return ("RECORD", S_REC, "directory holding enablement links, made by systemctl/deb-systemd-helper")
    # alternatives
    if path.startswith("/etc/alternatives/") or path.startswith("/usr/bin/") or path.startswith("/usr/share/man/man1/"):
        if path.startswith("/etc/alternatives/"):
            if re.match(r"^(Mail|mail|mailx)(\.1\.gz)?$", b):
                return ("SETTING-DEFAULT", S_DEF, "alternative set in auto mode by bsd-mailx installation (action log)")
            return ("UNKNOWN", S_DEF, "alternative choice; auto (DEFAULT) or manual (OWN) mode not recorded")
        return ("SETTING-DEFAULT", S_DEF, "generic name link created by update-alternatives --install in a postinst")
    # dpkg database
    if path.startswith("/var/lib/dpkg/info/"):
        if b.endswith(".list") or b == "format":
            return ("RECORD", S_REC, "file list/format written by dpkg as it ran")
        return ("UNKNOWN", S_INST, "control-area file obtained with the package; unchanged-since-installation not recorded")
    if path.startswith("/var/lib/dpkg/alternatives/"):
        return ("RECORD", S_REC, "update-alternatives state database")
    if path.startswith("/var/lib/dpkg/"):
        return ("RECORD", S_REC, "dpkg database/lock/trigger state")
    if path.startswith("/var/lib/systemd/deb-systemd-helper"):
        return ("RECORD", S_REC, "record of past enablement by deb-systemd-helper (8.6)")
    # k3s
    if path.startswith("/var/lib/rancher/k3s/data/"):
        if path in ("/var/lib/rancher/k3s/data/.lock", "/var/lib/rancher/k3s/data/current"):
            return ("RECORD", S_REC, "k3s extraction lock/pointer")
        if re.match(r"^/var/lib/rancher/k3s/data/[0-9a-f]{64}$", path):
            return ("RECORD", S_REC, "directory of extracted k3s runtime")
        if typ == "directory":
            return ("RECORD", S_REC, "directory made by k3s extraction")
        return ("PROGRAM-DERIVED", S_PROG, "userspace tool or link extracted by k3s from its binary")
    if path.startswith("/var/lib/rancher/") or path.startswith("/etc/rancher/"):
        return ("RECORD", S_REC, "certificate, key, kubeconfig, manifest or config written by k3s as it ran")
    if path.startswith("/usr/libexec/kubernetes"):
        return ("RECORD", S_REC, "plugin directory created by kubelet in k3s")
    if path.startswith("/usr/share/netplan/"):
        if path.endswith(".pyc"):
            return ("PROGRAM-DERIVED", S_PROG, "Python bytecode compiled from the netplan package: compiled copy (8.6)")
        return ("RECORD", S_REC, "__pycache__ directory created by Python")
    if path.startswith("/root/.kube/"):
        return ("RECORD", S_REC, "kubectl discovery/http cache")
    if path.startswith("/var/cache/"):
        return ("RECORD", S_REC, "cache written by apt/debconf/ldconfig/man-db/apparmor_parser")
    if path.startswith("/var/log/"):
        return ("RECORD", S_REC, "log written by a program")
    if path.startswith("/var/lib/") or path.startswith("/var/spool/") or path.startswith("/var/tmp/"):
        return ("RECORD", S_REC, "working state written by a program (cloud-init, kubelet, CNI, apt, systemd, exim4, logrotate)")
    return None


RUNC = [
    ("/run/udev", "systemd-udevd (udev; INSTALLED-PACKAGE if unchanged)"),
    ("/run/systemd/generator", "systemd generators from fstab, netplan, cloud-init, ssh settings"),
    ("/run/systemd/network", "netplan generate from /etc/netplan/50-cloud-init.yaml (SETTING-OWN)"),
    ("/run/systemd/netif", "systemd-networkd (INSTALLED-PACKAGE)"),
    ("/run/systemd/resolve", "systemd-resolved (INSTALLED-PACKAGE)"),
    ("/run/systemd/journal", "systemd-journald (INSTALLED-PACKAGE)"),
    ("/run/log", "systemd-journald (INSTALLED-PACKAGE)"),
    ("/run/systemd/sessions", "systemd-logind (INSTALLED-PACKAGE)"),
    ("/run/systemd/seats", "systemd-logind (INSTALLED-PACKAGE)"),
    ("/run/systemd/users", "systemd-logind (INSTALLED-PACKAGE)"),
    ("/run/systemd/inhibit", "systemd-logind (INSTALLED-PACKAGE)"),
    ("/run/systemd/transient/docker", "systemd scopes requested for compose containers by dockerd/runc"),
    ("/run/systemd", "systemd (INSTALLED-PACKAGE)"),
    ("/run/user", "systemd user manager/logind for uid 1000 (INSTALLED-PACKAGE)"),
    ("/run/containerd", "containerd (containerd.io; change not recorded)"),
    ("/run/docker", "dockerd (docker-ce; change not recorded)"),
    ("/run/k3s", "containerd inside k3s (PROGRAM-DERIVED)"),
    ("/run/cloud-init", "cloud-init (INSTALLED-PACKAGE)"),
    ("/run/blkid", "blkid (util-linux, INSTALLED-PACKAGE)"),
    ("/run/credentials", "systemd (INSTALLED-PACKAGE)"),
    ("/run/dbus", "dbus-daemon (INSTALLED-PACKAGE)"),
    ("/run/exim4", "exim4 (INSTALLED-PACKAGE)"),
    ("/run/fsck", "systemd-fsck (INSTALLED-PACKAGE)"),
    ("/run/mount", "libmount/systemd (INSTALLED-PACKAGE)"),
    ("/run/nri", "containerd NRI"),
    ("/run/ssh-unix-local", "systemd ssh generator socket (INSTALLED-PACKAGE)"),
    ("/run/tmpfiles.d", "systemd-tmpfiles (INSTALLED-PACKAGE)"),
    ("/run/uuidd", "uuidd (INSTALLED-PACKAGE)"),
    ("/run/lock", "systemd-tmpfiles (INSTALLED-PACKAGE)"),
    ("/tmp/systemd-private", "systemd PrivateTmp of exim4/logind units (package unit settings)"),
    ("/tmp", "systemd-tmpfiles (INSTALLED-PACKAGE)"),
    ("/run", "systemd, cron, sshd, dockerd and other daemons"),
]


def run_creator(path):
    for pre, c in RUNC:
        if path == pre or path.startswith(pre + "/") or path.startswith(pre):
            return c
    return "a running program"


NORULE = []


def group_files(r):
    m = members_json(r)
    t = list(csv.DictReader(open(RAWROOT + m["file"]), delimiter="\t"))
    return m, t


def decide_group(r, memw):
    m, t = group_files(r)
    i, name = r["id"], r["name"]
    decs = []
    for x in t:
        d = mrule(x["path"], x["type"], x["persistence"])
        if d is None:
            NORULE.append(x["path"])
            return None
        decs.append((x["path"], d))
        memw.writerow([i, x["path"], d[0], d[1], d[2]])
    kinds = {}
    for p, d in decs:
        kinds.setdefault(d[0], []).append(p)
    basis = f"raw:{m['file']}"
    if len(kinds) == 1:
        dec = next(iter(kinds))
        d0 = decs[0][1]
        sents = d0[1]
        reasons = sorted({d[2] for _, d in decs})
        if dec == "RUNTIME":
            creators = sorted({run_creator(p) for p, _ in decs if not p.startswith("/run/docker/netns")})
            rs = "Every member is on tmpfs or otherwise exists only while running; creators per member in part-server.members.tsv: " + "; ".join(sorted({c.split(" (")[0] for c in creators}))
            if any(p.startswith("/run/docker/netns") for p, _ in decs):
                rs = "All members are nsfs namespace mount points of compose containers, made by dockerd (docker-ce; change not recorded)"
            if name.startswith("/var/tmp/systemd-private") or name.startswith("/tmp/systemd-private"):
                rs = "PrivateTmp tree systemd removes when the unit stops; belongs to the unit's PrivateTmp setting (packaged exim4/logind units, INSTALLED-PACKAGE)"
            if all(x["type"] == "socket" for x in t) and not name.startswith("/run"):
                rs = "Members are sockets of a running daemon; exist only while it runs; belong to the kubelet in k3s (PROGRAM-DERIVED)"
            reason = rs if len(rs.split()) <= 30 else "Every member is on tmpfs: exists only while running; created by systemd, its generators and running daemons; creator of each member in part-server.members.tsv."
        else:
            reason = f"All {len(decs)} members: " + "; ".join(reasons)
            if len(reason.split()) > 30:
                reason = f"All {len(decs)} members {dec}, e.g. {min(reasons, key=len)}; each member's reason in part-server.members.tsv."
        what = f"directory {name}: {len(decs)} members not owned by packages"
        return row(i, dec, sents, what[:120], basis, clip(reason))
    parts = [f"{k} {len(v)}" for k, v in sorted(kinds.items(), key=lambda kv: -len(kv[1]))]
    examples = []
    for k, v in sorted(kinds.items(), key=lambda kv: -len(kv[1])):
        examples.append(f"{k}: {os.path.basename(v[0])}" + ("…" if len(v) > 1 else ""))
    reason = "Members differ: " + ", ".join(parts) + ". Which member gets which: part-server.members.tsv, rows with this group_id."
    sents = ",".join(sorted({s for _, d in decs for s in d[1].split(",")}, key=lambda s: (s[:4], int(s.split('-')[1]))))
    return row(i, "MIXED", sents, f"directory {name}: {len(decs)} members of different kinds", basis, clip(reason))


def clip(s, n=30):
    w = s.split()
    return s


# ================================================================ main
def decide(r, memw):
    k = r["kind"]
    if k in ("1:firewall-chain", "1:firewall-rule"):
        return decide_nft(r)
    if k in ("1:firewall-ipv4", "1:firewall-ipv6"):
        return decide_ipt(r)
    if k == "1:process":
        return decide_process(r)
    if k == "1:port":
        return decide_port(r)
    if k == "1:module-name":
        return decide_module(r)
    if k == "2:executable-code-outside-packages":
        return decide_exec(r)
    if k == "2:stored-outside-packages":
        return decide_group(r, memw)
    return decide_small(r)


def main():
    done = set()
    exists = os.path.exists(OUT) and os.path.getsize(OUT) > 0
    if exists:
        for x in csv.DictReader(open(OUT), delimiter="\t"):
            done.add(x["id"])
    out = open(OUT, "a", newline="")
    w = None
    if not exists:
        out.write("\t".join(HEADER) + "\n")
    memf = open(MEMOUT, "w", newline="")
    memw = csv.writer(memf, delimiter="\t", lineterminator="\n")
    memw.writerow(["group_id", "path", "decision", "sentences", "reason"])
    missing = []
    for r in rows:
        d = decide(r, memw)  # always evaluated so ipt table tracking and member file stay complete
        if r["id"] in done:
            continue
        if d is None:
            missing.append(r["id"] + " " + r["kind"] + " " + r["name"])
            continue
        for f in HEADER:
            assert "\t" not in d[f] and "\n" not in d[f], d
        out.write("\t".join(d[f] for f in HEADER) + "\n")
        out.flush()
    print("members without rule:", len(NORULE))
    for x in NORULE[:60]:
        print("  M", x)
    print("undecided:", len(missing))
    for x in missing[:40]:
        print(" ", x)


if __name__ == "__main__":
    main()
