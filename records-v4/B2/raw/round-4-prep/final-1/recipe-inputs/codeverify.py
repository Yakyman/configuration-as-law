"""Compare generated AppArmor policy with the binary loaded by the kernel."""

import os
import pathlib
import subprocess


P = pathlib.Path
PARSER = "/usr/sbin/apparmor_parser"
POLICY = P("/sys/kernel/security/apparmor/policy")

def revision_value(path):
    # This event-style file blocks a second read until the next policy revision.
    fd=os.open(path,os.O_RDONLY|os.O_NONBLOCK)
    try:return os.read(fd,128).strip()
    finally:os.close(fd)


def verify_kernel_policy(source, wanted_profile_names):
    """Return mismatches between one policy source and its loaded transaction.

    ``apparmor_parser -S`` emits the same binary format accepted by the kernel.
    AppArmor exposes that original load binary through each profile's
    ``policy/profiles/.../raw_data`` symlink.  The exported transactions must contain exactly the requested profiles, and
    their serialized objects must byte-for-byte cover a fresh compilation.

    References:
    https://manpages.debian.org/unstable/apparmor/apparmor_parser.8.en.html
    https://gitlab.com/apparmor/apparmor/-/wikis/AppArmorInterfaces
    """
    bad = []
    supplied = tuple(wanted_profile_names)
    wanted = set(supplied)
    if not wanted or len(wanted) != len(supplied):
        return ["invalid expected kernel policy profile set"]
    if any(not isinstance(name, str) or not name for name in wanted):
        return ["invalid expected kernel policy profile name"]

    try:
        compiled = subprocess.run(
            [PARSER, "-S", "-T", os.fspath(source)],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as error:
        return ["kernel policy compile unavailable: " + str(error)]
    if compiled.returncode:
        detail = compiled.stderr.decode(errors="replace").strip()
        return ["kernel policy compile failed" + (": " + detail if detail else "")]

    profiles = POLICY / "profiles"
    revision = POLICY / "revision"
    try:
        before = revision_value(revision)
        name_files = sorted(profiles.rglob("name"), key=lambda path: str(path))
    except OSError as error:
        return ["kernel policy export unavailable: " + str(error)]

    records = []
    for name_file in name_files:
        directory = name_file.parent
        try:
            name = name_file.read_text().strip()
            raw = directory / "raw_data"
            raw_stat = raw.stat()
            target = (raw_stat.st_dev, raw_stat.st_ino)
            mode = (directory / "mode").read_text().strip()
        except OSError as error:
            bad.append("kernel policy profile export unreadable: " + str(error))
            continue
        records.append((name, mode, target, raw))

    by_name = {}
    for record in records:
        by_name.setdefault(record[0], []).append(record)
    for name in sorted(wanted):
        matches = by_name.get(name, [])
        if len(matches) != 1:
            bad.append("kernel policy profile count differs: " + name)
        elif matches[0][1] != "enforce":
            bad.append("kernel policy profile is not enforcing: " + name)

    selected = [record for record in records if record[0] in wanted]
    targets = {record[2] for record in selected}
    blobs=[]
    for target in targets:
        linked = {record[0] for record in records if record[2] == target}
        if not linked.issubset(wanted):bad.append("kernel policy transaction contains unexpected profiles")
        try:
            loaded = next(record[3] for record in selected if record[2] == target).read_bytes()
            if not loaded:bad.append("empty kernel policy transaction")
            blobs.append(loaded)
        except (OSError, StopIteration) as error:
            bad.append("kernel policy transaction unreadable: " + str(error))
    # The parser may load one transaction per profile. Its -S output is the
    # concatenation of those same serialized policy objects; require exact byte
    # coverage with every exported object used once, without accepting a prefix.
    remaining=compiled.stdout
    while blobs and remaining:
        matches=[i for i,blob in enumerate(blobs) if remaining.startswith(blob)]
        if len(matches)!=1:break
        blob=blobs.pop(matches[0]);remaining=remaining[len(blob):]
    if blobs or remaining:bad.append("kernel policy transaction binaries differ")

    try:
        after = revision_value(revision)
        if after != before:
            bad.append("kernel policy changed during verification")
    except OSError as error:
        bad.append("kernel policy revision unreadable: " + str(error))
    return bad
