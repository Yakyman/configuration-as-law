"""Read-only Talos API adapter with supplemental bounded content facts.

The caller supplies a bounded query transport. This module never invokes a
shell, discovers credentials, or opens a connection by itself.
"""
import json
import posixpath
import re
import shlex
from collections import deque

MAX_DEPTH = 4
MAX_DIRECTORIES = 64
MAX_MEMBERS = 4096
MAX_ROWS = 20000

# These objects are represented, never expanded. Symlinks are never followed.
OPAQUE = {"proc", "sys", "dev",
          "system", ".snapshots", "snapshots", "docker", "containers",
          "containerd", "kubelet", "overlay", "overlay2", "lost+found"}
STARTUP = {".profile", ".bashrc", ".bash_profile", ".bash_login", ".zshrc",
           ".zprofile", ".zshenv", ".kshrc", "profile", "bash.bashrc"}


def table(data):
    """Decode aligned CLI columns, preserving spaces inside the last column."""
    lines = data.decode("utf-8", "strict").splitlines()
    if not lines:
        return []
    headers = re.split(r"\s{2,}|\t+", lines[0].strip())
    if not headers or headers[0] != "NODE":
        raise ValueError("unrecognized CLI table header")
    starts = []
    cursor = 0
    for header in headers:
        start = lines[0].index(header, cursor)
        starts.append(start)
        cursor = start + len(header)
    result = []
    for line in lines[1:]:
        if not line.strip():
            continue
        if len(line) < starts[-1]:
            raise ValueError("short CLI row or embedded newline")
        row = {key: line[start:starts[i + 1] if i + 1 < len(starts) else None].strip()
               for i, (key, start) in enumerate(zip(headers, starts))}
        result.append(row)
    return result


def resources(data):
    """talosctl JSON is a stream, not necessarily a JSON array."""
    text = data.decode("utf-8", "strict")
    decoder = json.JSONDecoder()
    result = []
    while text.strip():
        text = text.lstrip()
        value, end = decoder.raw_decode(text)
        text = text[end:]
        values = value if isinstance(value, list) else [value]
        for item in values:
            if not isinstance(item, dict) or not isinstance(item.get("metadata"), dict):
                raise ValueError("unrecognized resource envelope")
            result.append(item)
    return result


def file_rows(data, directory):
    result = []
    for item in table(data):
        if not {"NAME", "MODE", "UID", "GID", "SIZE(B)", "LASTMOD"} <= item.keys():
            raise ValueError("unrecognized list columns")
        mode = item["MODE"]
        # Go FileMode.String uses L for symlinks. The target is not a member.
        name = item["NAME"].split(" -> ", 1)[0] if mode.startswith("L") else item["NAME"]
        path = posixpath.normpath(posixpath.join(directory, name))
        if path == directory:
            continue
        if posixpath.dirname(path) != directory or any(ord(c) < 32 for c in path):
            raise ValueError("listing escaped immediate parent or contains control characters")
        typ = "directory" if mode.startswith("d") else "symlink" if mode.startswith("L") else "file" if mode.startswith("-") else "special"
        result.append({"path": path, "type": typ, "mode": mode,
                       "owner": item["UID"] + ":" + item["GID"], "size": item["SIZE(B)"],
                       "link_target": item["NAME"].split(" -> ",1)[1] if typ == "symlink" and " -> " in item["NAME"] else "",
                       "mtime": "unknown", "mtime_api_display": item["LASTMOD"],
                       "executable": "yes" if typ == "file" and "x" in mode else "no",
                       "signature": "unknown:no-bounded-content-API-used",
                       "persistence": "unknown", "ownership": "unknown",
                       "integrity": "unknown", "configuration_origin": "unknown"})
    if len({row["path"] for row in result}) != len(result):
        raise ValueError("duplicate paths or multiple nodes in list response")
    return result


def readonly_image_roots(mount_rows, block_mounts, disks):
    """Join actual root mount source to kernel-reported read-only block device.

    No readonly inference from a product name, version, file mode or disk name.
    Mounted overlays are not proven by readonly backing disks alone.
    """
    readonly_devices = {d.get("spec", {}).get("dev_path") for d in disks
                        if d.get("spec", {}).get("readonly") is True}
    roots = {m.get("spec", {}).get("target") for m in block_mounts
             if m.get("spec", {}).get("target") == "/"
             and m.get("spec", {}).get("readOnly") is True}
    for mount in mount_rows:
        if mount.get("MOUNTED ON") == "/" and mount.get("FILESYSTEM") in readonly_devices:
            roots.add("/")
    return sorted(roots)


def file_on_image(path, image_roots, mount_targets, complete_mapping=False):
    # Available APIs do not establish an exhaustive covering-mount map.
    if not complete_mapping:
        return False
    # Restrict ownership claims to the installed /usr namespace; mutable /etc,
    # /var, /run and home contents are not image membership from a pathname.
    if not path.startswith("/usr/"):
        return False
    return bool(image_roots) and not any(target != "/" and
        (path == target or path.startswith(target.rstrip("/") + "/"))
        for target in mount_targets if target.startswith("/"))


def collect(ctx):
    """Use ctx.query(argv, timeout, max_lines), add and write_members only."""
    succeeded = {}

    def query(label, args, cap=MAX_ROWS):
        data, status, evidence = ctx.query("talos-" + label, ["talosctl"] + args,
                                           timeout=15, max_lines=cap + 1)
        succeeded[label] = status == 0
        if status:
            ctx.gaps.append("talos-" + label + ": not collected; exit=" + str(status))
            return None, evidence
        return data, evidence

    def records(label, args, kind, key, json_output=False):
        data, evidence = query(label, args)
        if data is None:
            return []
        try:
            rows = resources(data) if json_output else table(data)
            if len(rows) > MAX_ROWS:
                raise ValueError("row count bound reached")
            for row in rows:
                name = row.get("metadata", {}).get("id") if json_output else row.get(key)
                if not name:
                    raise ValueError("missing object identity")
            for row in rows:
                name = row["metadata"]["id"] if json_output else row[key]
                if kind == "process":
                    name = str(row.get("PID", "unknown")) + ":" + name
                detail = dict(row)
                detail.pop("NODE", None)
                detail.pop("node", None)
                if kind == "extension":
                    detail["reason"] = "unknown"
                ctx.add(1, kind, name, json.dumps(detail, sort_keys=True), evidence)
            return rows
        except (ValueError, UnicodeError, KeyError) as exc:
            succeeded[label] = False
            ctx.gaps.append("talos-" + label + ": not collected; parser=" + str(exc))
            return []

    # MachineConfig.spec is YAML text. Redact on the host before raw retention:
    # only installation-image references leave this command, never credentials.
    image_script = r"""import json,re,subprocess,sys
p=subprocess.run(['talosctl','get','machineconfig','v1alpha1','-o','json'],capture_output=True,timeout=12)
if p.returncode:
 sys.stderr.buffer.write(p.stderr);sys.exit(p.returncode)
try:
 spec=json.loads(p.stdout)['spec']
 if not isinstance(spec,str): raise ValueError('machine config spec is not YAML text')
 images=[]
 for doc in re.split(r'^---\s*$',spec,flags=re.M):
  wanted=['installer','image'] if re.search(r'^kind: UnattendedInstallConfig\s*$',doc,re.M) else ['machine','install','image']
  stack=[]
  for line in doc.splitlines():
   m=re.match(r'^( *)([A-Za-z][A-Za-z0-9]*):(?: (.*))?$',line)
   if not m: continue
   n=len(m.group(1))
   while stack and stack[-1][0]>=n: stack.pop()
   keys=[v for _,v in stack]+[m.group(2)]
   if keys==wanted and m.group(3): images.append(m.group(3).strip().strip('\"\''))
   stack.append((n,m.group(2)))
 images=[i for i in images if re.fullmatch(r'[A-Za-z0-9._/@:+-]+',i)]
 print(json.dumps({'images':images}))
except (ValueError,KeyError,TypeError):
 print('active machine configuration image could not be decoded',file=sys.stderr);sys.exit(65)
"""
    image_data, image_rc, image_ev = ctx.query("talos-install-image", ["python3", "-c", image_script], timeout=15, max_lines=2)
    configured_images = []
    if image_rc == 0:
        try:
            configured_images = json.loads(image_data)["images"]
        except (ValueError, KeyError):
            ctx.gaps.append("talos-install-image: malformed redacted image result")
    version, version_ev = query("version", ["version"])
    mounts = records("block-mount-resources", ["get", "MountStatuses.block.talos.dev", "-o", "json"], "mount-resource", "", True)
    mount_rows = records("mounts", ["mounts"], "mount", "MOUNTED ON")
    disks = records("readonly-disks", ["get", "Disks.block.talos.dev", "-o", "json"], "block-device", "", True)
    legacy_mounts = records("mount-resources", ["get", "mounts", "-o", "json"], "mount-resource", "", True)
    mapping_queries_ok = all(succeeded.get(label, False) for label in
                             ("mounts", "block-mount-resources", "mount-resources", "readonly-disks"))
    image_mounts = readonly_image_roots(mount_rows, mounts, disks) if mapping_queries_ok else []
    mount_targets = [r.get("MOUNTED ON", "") for r in mount_rows] + [r.get("spec", {}).get("target", "") for r in mounts + legacy_mounts]
    import sys
    print("talos instrument: configured-image-count=" + str(len(configured_images)) + "; proven-readonly-image-mount-count=" + str(len(image_mounts)), file=sys.stderr)
    image_id = None
    if version is not None:
        image_id = ctx.add(1, "package", "talos-installed-image",
                {"reason": "explicit" if configured_images else "unknown",
                 "reason_evidence": image_ev, "configured_images": configured_images,
                 "integrity": "unknown",
                 "integrity_rule": "Read-only root evidence is retained separately; complete image and covering-mount verification is unavailable.",
                 "image_mounts": image_mounts, "members_not_expanded": True}, version_ev)
    records("services", ["service"], "service", "SERVICE")
    records("processes", ["processes"], "process", "COMMAND")
    records("modules", ["get", "loadedkernelmodules", "-o", "json"], "kernel-module", "", True)
    records("extensions", ["get", "extensions", "-o", "json"], "extension", "", True)
    for resource in ("LinkSpec", "AddressSpec", "RouteSpec", "ResolverSpec", "TimeServerSpec"):
        records("network-" + resource.lower(), ["get", resource, "-o", "json"], "network-configuration", "", True)
    for resource in ("links", "addresses", "routes"):
        records("network-" + resource, ["get", resource, "-o", "json"], "network-state", "", True)
    records("ports", ["netstat", "--all"], "socket", "Local Address")
    records("containers", ["containers"], "container", "ID")
    records("images", ["image", "list"], "container-image", "IMAGE")

    queue = deque([("/", 0)])
    directories = 0
    members = 0
    while queue and directories < MAX_DIRECTORIES and members < MAX_MEMBERS:
        directory, depth = queue.popleft()
        directories += 1
        data, evidence = query("list-" + str(directories),
                               ["list", "--depth", "1", "--long", directory], MAX_MEMBERS - members)
        if data is None:
            continue
        try:
            rows = file_rows(data, directory)
            if len(rows) > MAX_MEMBERS - members:
                raise ValueError("member count bound reached; no partial group emitted")
        except (ValueError, UnicodeError) as exc:
            ctx.gaps.append("talos-list " + directory + ": not collected; " + str(exc))
            continue
        members += len(rows)
        if rows and not directory.startswith("/usr"):
            # Complete immediate-child membership only; package ownership unavailable.
            group = ctx.add(2, "stored-ownership-unknown", directory,
                            "complete_immediate_listing=true;ownership=unknown", evidence)
            ctx.write_members(group, rows)
        for row in rows:
            path = row["path"]
            packaged = path.startswith("/usr/")
            if image_id and row["type"] in ("file", "symlink") and packaged:
                known = row["type"] == "file" and file_on_image(path, image_mounts, mount_targets)
                ctx.package_files.append({"package": image_id, "path": path,
                    "integrity": "unchanged" if known else "unknown", "evidence": evidence,
                    "rule": "installed /usr namespace; actual readonly root backing and no listed submount" if known else "installed /usr namespace; readonly mapping not demonstrated"})
            name = posixpath.basename(path)
            if not packaged and row["type"] == "file" and (row["executable"] == "yes" or name in STARTUP):
                ctx.add(2, "code-ownership-unknown", path,
                        "ownership=unknown;signature=unknown;shebang=unknown", evidence)
            if row["type"] != "directory":
                continue
            if name in OPAQUE:
                ctx.add(2, "opaque-directory", path, "contents_not_expanded=true", evidence)
            elif depth + 1 < MAX_DEPTH:
                queue.append((path, depth + 1))
            else:
                ctx.gaps.append("talos-list " + path + ": not collected; depth bound")
    if queue:
        ctx.gaps.append("talos-list: not collected remaining directories; count bound")
    import extra_talos
    extra_talos.collect(ctx)
    ctx.gaps.extend([
        "talos: package ownership and complete non-package level 2 inventory not collected; exposed listing only",
        "talos: image/file integrity known only for API-proven read-only image filesystems; other files unknown",
        "talos: image reason comes from configured installation image; extension reasons unknown",
        "talos: file signatures, shebang-only code and configuration creation facts not collected; no content reads",
        "talos: exact UTC file modification times and persistence unknown; list timestamps omit year or seconds",
        "talos: process executable links, system/user timers, accounts/groups, sudo/doas/polkit and firewall not collected",
        "talos: desired network specs are not proof of saved/manual network origin; origin unknown",
        "talos: workload-internal inventories not collected; containers and images are opaque",
        "talos: container/image listing covers default runtime namespace only; other namespaces not collected",
        "talos: names with embedded newlines and unknown snapshot/container locations cannot be fully decoded or detected",
    ])


def fixture_check():
    """Pure mocked validation, to be run only on an authorized disposable guest."""
    headers = ["NODE", "MODE", "UID", "GID", "SIZE(B)", "LASTMOD", "LABEL", "NAME"]
    widths = [10, 14, 6, 6, 10, 24, 10, 0]

    def listing(entries):
        def line(values):
            return "".join(str(value).ljust(width) for value, width in zip(values, widths))
        return (line(headers) + "\n" + "\n".join(line(["node", mode, 0, 0, 10,
                "Nov 22 01:00:00", "", name]) for mode, name in entries) + "\n").encode()

    payload = listing([("drwxr-xr-x", "proc"), ("drwxr-xr-x", "etc"),
                       ("drwxr-xr-x", "sys"), ("drwxr-xr-x", "dev"),
                       ("drwxr-xr-x", "usr"), ("drwxr-xr-x", ".snapshots"),
                       ("Lrwxrwxrwx", "alias -> /proc")])
    decoded = file_rows(payload, "/")
    assert len(decoded) == 7
    assert decoded[-1]["path"] == "/alias" and decoded[-1]["type"] == "symlink"
    try:
        file_rows(listing([("-rw-r--r--", "../escape")]), "/etc")
    except ValueError:
        pass
    else:
        raise AssertionError("path escape accepted")
    assert len(resources(b'{"metadata":{"id":"a"}}\n{"metadata":{"id":"b"}}')) == 2

    class Mock:
        def __init__(self):
            self.gaps, self.calls, self.objects, self.members = [], [], [], {}
            self.package_files = []

        def query(self, label, argv, timeout, max_lines):
            if argv[0] == "python3":
                return b'{"images":["factory.example/image:version"]}', 0, label
            assert argv[0] == "talosctl" and timeout == 15 and max_lines > 0
            assert not ({"read", "copy", "--recurse"} & set(argv))
            self.calls.append(argv)
            if argv[1] == "list":
                assert argv[-1] in ("/", "/etc", "/usr")
                return (payload if argv[-1] == "/" else listing([("-rwxr-xr-x", "local tool")])), 0, label
            if argv[1] == "version":
                return b"Server: v1\n", 0, label
            return b"", 1, label

        def add(self, level, kind, name, members, evidence):
            self.objects.append((level, kind, name, members, evidence))
            return str(len(self.objects))

        def write_members(self, identity, rows):
            self.members[identity] = rows

    ctx = Mock()
    collect(ctx)
    assert [call[-1] for call in ctx.calls if call[1] == "list"] == ["/", "/etc", "/usr"]
    assert sum(len(rows) for rows in ctx.members.values()) == 8
    assert any(row[1] == "code-ownership-unknown" and row[2] == "/etc/local tool" for row in ctx.objects)
    assert any("talos-services: not collected" in gap for gap in ctx.gaps)
    assert len(ctx.package_files) == 1 and ctx.package_files[0]["integrity"] == "unknown"
    disk = [{"spec": {"dev_path": "/dev/loop0", "readonly": True}}]
    root = [{"FILESYSTEM": "/dev/loop0", "MOUNTED ON": "/"}]
    assert readonly_image_roots(root, [], disk) == ["/"]
    assert readonly_image_roots([{ "FILESYSTEM": "overlay", "MOUNTED ON": "/"}], [], disk) == []
    assert not file_on_image("/usr/bin/tool", ["/"], ["/", "/etc"])
    assert not file_on_image("/usr/bin/tool", ["/"], ["/", "/usr/bin"])
    assert not file_on_image("/etc/config", ["/"], ["/"])
    return {"passed": True, "checks": ["list metadata", "symlink exclusion", "pseudo/image/snapshot exclusions",
            "complete immediate members", "spaces in names", "path escape rejected", "JSON streams",
            "failure continuation", "no content requests", "query time/count bounds", "readonly backing join", "overlay not inferred", "nested mount masking", "installed namespace package files"]}
