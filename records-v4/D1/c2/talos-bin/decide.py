"""Decide every row of D1/in/part-talos.tsv (classification c2). Rules are stated in part-talos.notes.md."""
import csv, json, sys, os

csv.field_size_limit(10**9)
IN, OUT = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(IN), delimiter='\t'))

ARCH = 'doc:https://docs.siderolabs.com/talos/v1.14/learn-more/architecture'
SRC = 'doc:https://github.com/siderolabs/talos/tree/v1.14.6'
DOCKERFILE = 'doc:https://github.com/siderolabs/talos/blob/v1.14.6/Dockerfile'
SEQ = 'doc:https://github.com/siderolabs/talos/blob/v1.14.6/internal/app/machined/pkg/runtime/v1alpha1/v1alpha1_sequencer_tasks.go'
CONTAINERD = 'doc:https://github.com/containerd/containerd/blob/main/README.md'
CONST = 'doc:https://github.com/siderolabs/talos/blob/v1.14.6/pkg/machinery/constants/constants.go'

RT = 'S8.2-5'
PKG = 'S8.1-6,S8.2-7,S8.2-8,S8.2-16'
IMG = 'Talos image (INSTALLED-PACKAGE)'

out = {}

def put(rid, dec, sent, what, basis, reason):
    out[rid] = (dec, sent, what, basis, reason)

# ---------- R1 processes ----------
PROC = [
    ('/sbin/init', 'machined, the Talos init and service manager', 'machined'),
    ('/sbin/dashboard', 'Talos console dashboard', 'dashboard'),
    ('/apid', 'Talos API daemon in its system container', 'apid'),
    ('/trustd', 'Talos trust daemon in its system container', 'trustd'),
    ('/sbin/sandboxd', 'Talos sandbox namespace daemon', 'sandboxd'),
    ('/bin/containerd', 'containerd container runtime daemon', 'containerd'),
    ('/usr/bin/containerd-shim-runc-v2', 'containerd shim supervising one container', 'containerd-shim-runc-v2'),
    ('/sbin/systemd-udevd', 'udev device manager daemon', 'systemd-udevd'),
    ('(udev-worker)', 'udev worker handling a device event', 'systemd-udevd'),
]

def proc(r):
    cmd = r['name'].split(':', 1)[1]
    for pfx, what, prog in PROC:
        if cmd.startswith(pfx):
            return put(r['id'], 'RUNTIME', RT + ',' + PKG, 'Running process of ' + what + '.', 'raw:raw/0008-talos-processes.out',
                       f'A process exists only while running (S8.2-5); it belongs to program {prog}, shipped in the read-only installed Talos image: INSTALLED-PACKAGE.')
    if cmd.startswith('/usr/local/bin/kubelet') or cmd.startswith('/usr/local/bin/etcd'):
        prog = 'kubelet' if 'kubelet' in cmd.split()[0] else 'etcd'
        return put(r['id'], 'RUNTIME', RT + ',S8.2-9,S8.2-16,S8.2-22', f'Running {prog} process inside its system container.', 'raw:raw/0008-talos-processes.out',
                   f'Process exists only while running (S8.2-5); belongs to {prog} from a pulled container image: PROGRAM-DERIVED if Talos pulled it, PROGRAM-OWN if a person did; puller not inventoried.')
    raise SystemExit('unmapped process ' + r['name'])

# ---------- R2 sockets ----------
def sock(r):
    m = json.loads(json.loads(r['members'])) if r['members'].startswith('"') else json.loads(r['members'])
    loc, fo, st = m['Local Address'], m['Foreign Address'], m.get('State', '')
    lport = loc.rsplit(':', 1)[1]
    fport = fo.rsplit(':', 1)[1]
    owner = None
    if loc.startswith('169.254.116.108:53') or loc.startswith('127.0.0.53:53'):
        owner = ('machined host DNS cache', 'INSTALLED-PACKAGE', CONST)
    elif lport == '7445':
        owner = ('machined KubePrism load balancer', 'INSTALLED-PACKAGE', CONST)
    elif lport in ('50000',):
        owner = ('apid', 'INSTALLED-PACKAGE', CONST)
    elif lport in ('50001',) and st == 'LISTEN':
        owner = ('trustd', 'INSTALLED-PACKAGE', CONST)
    elif lport in ('2379', '2380', '2383'):
        owner = ('etcd (listen flags in its process arguments)', 'PROGRAM-DERIVED or PROGRAM-OWN, puller not inventoried', 'raw:raw/0008-talos-processes.out')
    elif lport in ('10248', '10250'):
        owner = ('kubelet (default health and API ports)', 'PROGRAM-DERIVED or PROGRAM-OWN, puller not inventoried', 'doc:https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/')
    if st == 'LISTEN' or (m['Proto'].startswith('udp') and fo.endswith(':*')):
        what = f'Listening {m["Proto"]} socket on {loc}.'
    elif st == 'TIME_WAIT':
        what = f'Closed TCP connection {loc} to {fo} held in TIME_WAIT.'
    else:
        what = f'{m["Proto"]} connection {loc} to {fo}, state {st or "connected"}.'
    if owner:
        reason = f'An open port or connection exists only while running (S8.2-5); it belongs to {owner[0]}, whose decision is {owner[1]}.'
        basis = owner[2]
    else:
        reason = ('An open port or connection exists only while running (S8.2-5); the inventory records no owning process, '
                  'and every possible owner still gives RUNTIME.')
        basis = 'raw:raw/0019-talos-ports.out'
    return put(r['id'], 'RUNTIME', RT, what[:200], basis, reason)

# ---------- R3 network ----------
def net(r):
    name, kind = r['name'], r['kind']
    if kind.endswith('network-configuration'):
        m = json.loads(json.loads(r['members']))
        layer = m['spec'].get('layer')
        what = f'In-memory Talos network spec {name}, layer {layer}.'
        if layer == 'default':
            reason = 'An in-memory resource of machined, recreated each boot (S8.2-5); it belongs to a built-in default of the Talos image: INSTALLED-PACKAGE.'
        else:
            reason = ('An in-memory resource recreated each boot (S8.2-5); it belongs to a machined network operator (Talos image, INSTALLED-PACKAGE); '
                      'operator enablement source not inventoried.')
        basis = 'raw:' + r['evidence']
        return put(r['id'], 'RUNTIME', RT, what, basis, reason)
    what = f'Live kernel network state: {name}.'
    reason = ('Kernel link, address or route state exists only while running (S8.2-5); it belongs to the kernel and machined network '
              'controllers of the Talos image: INSTALLED-PACKAGE.')
    return put(r['id'], 'RUNTIME', RT, what, 'raw:' + r['evidence'], reason)

# ---------- R4 mounts ----------
CONTAINER_ROOTFS = '/run/containerd/io.containerd.runtime.v2.task/system/'
def mnt(r):
    name = r['name']
    if name.startswith(CONTAINER_ROOTFS):
        c = name[len(CONTAINER_ROOTFS):].split('/')[0]
        return put(r['id'], 'RUNTIME', RT, f'Overlay root filesystem mount of the {c} system container.', 'raw:' + r['evidence'],
                   f'A mount point is not a separate object (S8.2-5); containerd (Talos image, INSTALLED-PACKAGE) creates it for the {c} container.')
    if r['kind'].endswith('mount-resource'):
        what = f'Talos mount status resource for volume or path {name}.'
    else:
        what = f'Mounted filesystem at {name}.'
    reason = 'A mount point is not a separate object (S8.2-5); Talos init (machined) mount and volume code of the image creates it: INSTALLED-PACKAGE.'
    return put(r['id'], 'RUNTIME', RT, what, 'raw:' + r['evidence'], reason)

# ---------- R5 kernel modules ----------
def kmod(r):
    return put(r['id'], 'RUNTIME', RT + ',' + PKG, f'Kernel module {r["name"]} loaded in the running kernel.', 'raw:' + r['evidence'],
               'Loaded-module state exists only while running (S8.2-5); it belongs to the module file of the Talos image, loaded by kernel or udev: INSTALLED-PACKAGE.')

# ---------- R6 block devices ----------
def blk(r):
    n = r['name']
    if n.startswith('loop'):
        what = 'Read-only loop device backing a Talos squashfs image.'
        reason = 'A kernel device registration exists only while running (S8.2-5); Talos init creates it to mount its squashfs image: INSTALLED-PACKAGE.'
    else:
        what = f'Kernel block device {n} for virtual hardware.'
        reason = 'A kernel device registration exists only while running (S8.2-5); kernel drivers and machined disk controller of the Talos image create it: INSTALLED-PACKAGE.'
    return put(r['id'], 'RUNTIME', RT, what, 'raw:' + r['evidence'], reason)

# ---------- R7 container images ----------
def cimg(r):
    m = json.loads(json.loads(r['members']))
    img = m['IMAGE']
    if img.startswith('sha256:'):
        what = 'Stored container image, referenced by image id.'
    elif '@sha256' in img:
        what = 'Stored container image, referenced by digest.'
    else:
        what = 'Stored container image, referenced by tag.'
    reason = ('A program (S8.2-9, S8.2-22), not a package: containerd documents image transfer, not installing (S8.1-4). '
              'Who pulled it is not inventoried: PROGRAM-DERIVED if system, PROGRAM-OWN if person.')
    return put(r['id'], 'UNKNOWN', 'S8.1-4,S8.2-9,S8.2-10,S8.2-16,S8.2-22', what, CONTAINERD, reason)

# ---------- hand-decided rows ----------
H = {}
def h(rid, dec, sent, what, basis, reason):
    H['talos-' + rid] = (dec, sent, what, basis, reason)

h('a037a062f5765e8529765ed7', 'INSTALLED-OWN', PKG, 'The installed Talos system image (factory installer image).', 'raw:raw/0001-talos-install-image.out',
  'In an image-installed system the image is a package (S8.1-6); installed, so an installed object; reason explicit, not a dependency: a line of its own.')
for rid, nm, what in [
    ('2460ff1bf90731c4d0396e53', 'apid', 'Talos API service.'),
    ('ea25f1cd0ddf09183b339dfe', 'auditd', 'Talos kernel audit log service.'),
    ('720a4c38c495d5f81d0920c8', 'containerd', 'Talos system containerd service.'),
    ('0562357a4d7bc8da0fb6544f', 'cri', 'Talos containerd CRI service for Kubernetes workloads.'),
    ('1f95e03e468aa8e91113c4a7', 'dashboard', 'Talos console dashboard service.'),
    ('ac61467428d376073f3b4466', 'kubelet', 'Talos kubelet service.'),
    ('7f23712d563026482709ffc1', 'machined', 'Talos machined service.'),
    ('9311e018d90e007503711ee3', 'sandboxd', 'Talos sandbox namespace service.'),
    ('999b2dc7cbd5907385abd795', 'syslogd', 'Talos syslog service.'),
    ('c370027d2ae46e07147805f0', 'udevd', 'Talos udev service.'),
]:
    h(rid, 'INSTALLED-PACKAGE', PKG + ',S8.1-11', what, SEQ,
      f'machined code in the image enables {nm} on every node (no machine-config value selects it): a default setting value obtained with the package, as received.')
h('b6b695f738a4b20f37d515bb', 'SETTING-OWN', 'S8.1-11,S8.2-11,S8.2-12,S8.2-13,S8.2-17', 'Talos etcd service.', SEQ,
  'Enabled only because the machine config sets a control-plane type: not as received; a service is a setting (S8.2-13), chosen by a person: a line of its own.')
h('22a0618964511c050dd76e83', 'SETTING-OWN', 'S8.1-11,S8.2-11,S8.2-12,S8.2-13,S8.2-17', 'Talos trustd service.', SEQ,
  'Enabled only because the machine config sets a control-plane type: not as received; a service is a setting (S8.2-13), chosen by a person: a line of its own.')
h('cdabbcef312a0739eb978083', 'RUNTIME', RT + ',S8.2-22', 'Running system container of apid.', 'raw:raw/0020-talos-containers.out',
  'A running container task exists only while running (S8.2-5); it belongs to the apid service of the Talos image: INSTALLED-PACKAGE.')
h('af01b7b528ad15264f3bd03a', 'RUNTIME', RT + ',S8.2-22', 'Running system container of trustd.', 'raw:raw/0020-talos-containers.out',
  'A running container task exists only while running (S8.2-5); it belongs to the trustd service: SETTING-OWN, program from the Talos image (INSTALLED-PACKAGE).')

# L2 opaque directories
for rid, what in [('b2c1d35516b9bf6ae72ee042', 'devtmpfs device node tree.'), ('21525d3e02038ac108a31d9d', 'proc pseudo filesystem of kernel state.'),
                  ('95f5f37280f94c5130e0012b', 'sysfs pseudo filesystem of kernel objects.')]:
    h(rid, 'RUNTIME', RT, what, 'raw:raw/0004-talos-mounts.out' if rid.startswith('b2c') else ARCH,
      'A kernel pseudo filesystem exists only while running (S8.2-5); every possible content belongs to the kernel of the Talos image: INSTALLED-PACKAGE.')
h('d12793014eb6f6ae75cb88db', 'RUNTIME', RT, 'Talos internal tmpfs recreated each boot.', ARCH,
  'On tmpfs, recreated on each boot (docs), so any content exists only while running (S8.2-5); created by machined of the Talos image: INSTALLED-PACKAGE.')
h('056fb8955448861e20501608', 'RUNTIME', RT, 'containerd runtime state directory on /run tmpfs.', 'raw:raw/0004-talos-mounts.out',
  'Under /run, a tmpfs mount: any content exists only while running (S8.2-5); created by containerd of the Talos image: INSTALLED-PACKAGE.')
for rid, nm, fact in [
    ('c7aab4c8a9b84956cc58bfc2', '/etc/containerd', 'image file or tmpfs-upper file written from configuration'),
    ('3b1ccfbf523a01e065827fe4', '/opt/containerd', 'image lower-layer file unchanged or written into writable persistent upper'),
    ('e474e02f772723ab6fab93a5', '/var/system', 'program record, copied package file or person-made file'),
    ('221540406974d5a8df5d5cfb', '/var/lib/containerd', 'pulled image content (and who pulled it) or runtime metadata'),
    ('81784b3738811c88acb17653', '/var/lib/kubelet', 'kubelet record, generated credential or other object'),
    ('445895923527ed83ab1d72b3', '/var/log/containers', 'log written by a program or object placed by someone else'),
]:
    h(rid, 'UNKNOWN', 'S8.2-7,S8.2-9,S8.2-15', f'Directory {nm}; contents not listed by the inventory.', 'evidence',
      f'Contents were not inventoried (contents_not_expanded); the decision depends on what each entry is: {fact}.')

h('0ef7f470fe09509cf8804594', 'RUNTIME', RT + ',S8.2-23', 'mdadm PID file on /run tmpfs.', 'raw:raw/0004-talos-mounts.out',
  'A PID file is read as a value, not executed (S8.2-23); on tmpfs it exists only while running (S8.2-5); belongs to mdadm of the Talos image: INSTALLED-PACKAGE.')
for rid, nm in [('6ba0499338de982b118add0e', 'bridge'), ('997f8af85b846cc0b08cb788', 'firewall'), ('2123143dd59cfa8a65d89c2e', 'flannel'),
                ('ef5794c4d65299a78f9d0ab3', 'host-local'), ('c3bfa964520b20475dcaec7b', 'loopback'), ('6c7e22c445534534f8821ef2', 'portmap')]:
    h(rid, 'UNKNOWN', 'S8.2-7,S8.2-9,S8.2-10,S8.2-16', f'CNI plugin executable {nm}.', DOCKERFILE,
      'Image ships it in /opt, but /opt is an overlay with a writable persistent upper; integrity unknown: unchanged gives INSTALLED-PACKAGE, rewritten gives a program decision.')

# L2 stored groups
h('d82085fcdfd8922534b0400b', 'MIXED', PKG + ',' + RT, 'Root directory listing: image directories and mount points.', ARCH,
  'Image entries /.extra /bin /boot /lib /lib64 /mnt /root /sbin /usr: INSTALLED-PACKAGE; /dev /proc /sys /run /system /tmp: RUNTIME; /etc /opt /var: MIXED, UNKNOWN, MIXED.')
h('152a1c4e080604a614e51cb3', 'INSTALLED-PACKAGE', PKG, '/boot with empty EFI directory from the image.', DOCKERFILE,
  'boot/EFI is created in the image build on the read-only squashfs root (docs): obtained as part of the package and as received.')
h('79eb0f8bca299bc0071046b6', 'MIXED', PKG + ',' + RT, '/etc overlay: image files plus Talos-generated tmpfs files.', SRC,
  'Image lower files, symlinks, apparmor apparmor.d lvm selinux ssl: INSTALLED-PACKAGE; hosts resolv.conf machine-id cni kubernetes iscsi nvme: RUNTIME; cri: MIXED; containerd: UNKNOWN.')
h('fa7b2e7ba5b47e94efde578c', 'UNKNOWN', 'S8.2-7,S8.2-9', '/opt overlay holding cni and containerd directories.', ARCH,
  'Both members are undecided: /opt/cni holds CNI binaries of unknown integrity in a writable persistent overlay; /opt/containerd contents not inventoried.')
h('830fdb15b41fbec5e25d0b71', 'RUNTIME', RT, '/run tmpfs with runtime directories of system programs.', 'raw:raw/0004-talos-mounts.out',
  'All members lie on the /run tmpfs and exist only while running (S8.2-5); created by containerd, machined, lvm, mdadm, udevd of the Talos image: INSTALLED-PACKAGE.')
h('170147a6d5dc76a88b74d35e', 'MIXED', 'S8.2-15', 'EPHEMERAL /var top level.', ARCH,
  '/var/log: RECORD; /var/mnt and /var/run symlink, created by machined as it ran: RECORD; /var/lib: MIXED; /var/system: UNKNOWN (contents not inventoried).')
h('00207c57714347b56c652e0d', 'INSTALLED-PACKAGE', PKG, 'AppArmor parser configuration from the image.', ARCH,
  'parser.conf is in the read-only image lower layer of /etc and no Talos controller writes it: obtained as part of the package, as received.')
h('46b5304a4a235508da943734', 'INSTALLED-PACKAGE', PKG, 'AppArmor profile directories from the image.', ARCH,
  'abi and disable are directories of the read-only image lower layer of /etc: obtained as part of the package, as received.')
h('52da29e78cfe7b4d0b4bff09', 'INSTALLED-PACKAGE', PKG, 'AppArmor ABI definition file from the image.', ARCH,
  'abi/3.0 lies in the read-only image lower layer of /etc and no Talos controller writes it: obtained as part of the package, as received.')
h('193f04c5940ff5bae58af1ae', 'RUNTIME', RT, '/etc/cni tmpfs holding the CNI network configuration directory.', 'raw:raw/0004-talos-mounts.out',
  '/etc/cni is a tmpfs mount, so net.d exists only while running (S8.2-5); created by machined of the Talos image: INSTALLED-PACKAGE.')
h('c5c75b80d7d84f871fdd7d89', 'MIXED', PKG + ',' + RT, 'CRI containerd configuration directory.', DOCKERFILE,
  'containerd.toml: image file, size matches source: INSTALLED-PACKAGE; conf.d: MIXED (image part file plus tmpfs files generated by machined).')
h('031345862da2c66a525d289e', 'MIXED', PKG + ',' + RT, 'CRI configuration fragments directory.', SRC,
  '00-base.part and hosts directory: image, INSTALLED-PACKAGE; cri.toml and base-spec.json: written by machined controllers into the /etc tmpfs upper: RUNTIME.')
h('31539e9beecf8e9fc80bc5bf', 'RUNTIME', RT, 'Generated iSCSI initiator name file.', 'doc:https://github.com/siderolabs/talos/blob/v1.14.6/internal/app/machined/pkg/controllers/files/iqn.go',
  'Written by the machined IQN controller into the /etc tmpfs upper each boot: exists only while running (S8.2-5); belongs to machined: INSTALLED-PACKAGE.')
h('9881fb71e57fa368da3a1aec', 'RUNTIME', RT, 'Kubelet kubeconfigs, configuration and PKI on tmpfs.', 'raw:raw/0004-talos-mounts.out',
  '/etc/kubernetes is a tmpfs mount: members exist only while running (S8.2-5); written by machined kubelet controllers and kubelet from machine-config settings.')
h('9be052858bf7d39cb4c1fff2', 'RUNTIME', RT, 'Kubernetes CA certificate for kubelet on tmpfs.', 'raw:raw/0004-talos-mounts.out',
  'Under the /etc/kubernetes tmpfs: exists only while running (S8.2-5); written by machined from the machine-config cluster CA.')
h('2dec6c01357214a7397d7a97', 'INSTALLED-PACKAGE', PKG, 'LVM configuration files from the image.', DOCKERFILE,
  'lvm.conf (size matches source), lvmlocal.conf and profile lie in the read-only image lower layer; no controller writes them: as received.')
h('18508e44a84cfadd1f104a66', 'INSTALLED-PACKAGE', PKG, 'LVM profile templates from the image.', ARCH,
  'Profiles lie in the read-only image lower layer of /etc and no Talos controller writes them: obtained as part of the package, as received.')
h('1be77f5ba1258694002947f0', 'RUNTIME', RT, 'Generated NVMe host id and host NQN files.', 'doc:https://github.com/siderolabs/talos/blob/v1.14.6/internal/app/machined/pkg/controllers/files/nqn.go',
  'Written by the machined NQN controller into the /etc tmpfs upper: exists only while running (S8.2-5); belongs to machined: INSTALLED-PACKAGE.')
h('1878dffc601dac99c389a298', 'INSTALLED-PACKAGE', PKG, 'SELinux policy directory from the image.', DOCKERFILE,
  'targeted is created in the image build on the read-only lower layer: obtained as part of the package, as received.')
h('10bed7104010761be3a33410', 'INSTALLED-PACKAGE', PKG, 'SELinux targeted policy directory from the image.', DOCKERFILE,
  'contexts is created in the image build on the read-only lower layer: obtained as part of the package, as received.')
h('1d528d7397348135ba0976e0', 'INSTALLED-PACKAGE', PKG, 'TLS directory from the image.', DOCKERFILE,
  'certs is created in the image build on the read-only lower layer: obtained as part of the package, as received.')
h('6dd18ebf778907d1984a1cfc', 'MIXED', PKG + ',' + RT, 'Trusted CA bundle and its symlink.', 'doc:https://github.com/siderolabs/talos/blob/v1.14.6/internal/app/machined/pkg/controllers/secrets/trusted_roots.go',
  'ca-certificates symlink: image, INSTALLED-PACKAGE; ca-certificates.crt: written by the machined trusted-roots controller into the /etc tmpfs upper: RUNTIME.')
h('6cf1c9fe2b87eaf863c6eb7a', 'UNKNOWN', 'S8.2-7,S8.2-9', '/opt/cni directory holding the CNI plugin directory.', DOCKERFILE,
  'Sole member /opt/cni/bin holds CNI binaries in a writable persistent overlay with unknown integrity: unchanged gives INSTALLED-PACKAGE, rewritten gives a program decision.')
h('21ec1ec89f766ac1e795911d', 'UNKNOWN', 'S8.2-7,S8.2-9,S8.2-10,S8.2-16', 'Six CNI plugin executables.', DOCKERFILE,
  'All six are image files in /opt, an overlay with a writable persistent upper; integrity unknown: unchanged gives INSTALLED-PACKAGE, rewritten gives a program decision.')
for rid, nm, owner in [('957905dcda8370c223e7f5a4', '/run/dbus', 'machined D-Bus server'), ('35473ecc6aa313b7bd659afe', '/run/lock', 'lvm'),
                       ('acbd559fae528925f36f26a1', '/run/mdadm', 'mdadm'), ('cf789723d48a6d35225eefa1', '/run/nri', 'containerd NRI'),
                       ('764a6e33a565b4a290e9062f', '/run/udev', 'systemd-udevd'), ('dafd06c97c0653fc5030a896', '/run/udev/data', 'systemd-udevd'),
                       ('3e0cc9ce8057a1d903e6c016', '/run/udev/links', 'systemd-udevd'), ('70f335c7386ea147d6c207ea', '/run/udev/tags', 'systemd-udevd'),
                       ('04248be55ad1f7ee6ee84d95', '/run/udev/watch', 'systemd-udevd')]:
    h(rid, 'RUNTIME', RT, f'Runtime state of {owner} under {nm}.', 'raw:raw/0004-talos-mounts.out',
      f'On the /run tmpfs, so every member exists only while running (S8.2-5); created by {owner} of the Talos image: INSTALLED-PACKAGE.')
h('b106dcdb914f18f62f868511', 'MIXED', 'S8.2-15,S8.2-7', 'Persistent state directories of CNI, containerd, etcd, kubelet.', 'raw:raw/0008-talos-processes.out',
  'cni (IPAM state) and etcd (data dir per its arguments), written by programs as they ran: RECORD; containerd and kubelet: UNKNOWN, contents not inventoried.')
h('bf4af619270934ca327e3b4b', 'RECORD', 'S8.2-15', 'Service log files and log directories.', 'evidence',
  'Every member is a log file of a Talos service or a log directory of kubelet/audit: recorded by programs as they ran, a program record.')

for r in rows:
    k = r['kind']
    if r['id'] in H:
        put(r['id'], *H[r['id']])
    elif k == 'L1:process': proc(r)
    elif k == 'L1:socket': sock(r)
    elif k in ('L1:network-state', 'L1:network-configuration'): net(r)
    elif k in ('L1:mount', 'L1:mount-resource'): mnt(r)
    elif k == 'L1:kernel-module': kmod(r)
    elif k == 'L1:block-device': blk(r)
    elif k == 'L1:container-image': cimg(r)
    else: raise SystemExit('undecided ' + r['id'] + ' ' + k)

bad = []
for rid, (dec, sent, what, basis, reason) in out.items():
    if len(what.split()) > 15: bad.append((rid, 'what', len(what.split()), what))
    if len(reason.split()) > 30: bad.append((rid, 'reason', len(reason.split()), reason))
    for f in (dec, sent, what, basis, reason):
        assert '\t' not in f and '\n' not in f
if bad:
    for b in bad: print(b)
    raise SystemExit('length check failed')

done = set()
if os.path.exists(OUT):
    done = {l.split('\t', 1)[0] for l in open(OUT).read().splitlines()[1:] if l}
with open(OUT, 'a') as f:
    if not done:
        f.write('id\tdecision\tsentences\twhat_it_does\tbasis\treason\n')
    for r in rows:
        if r['id'] in done: continue
        f.write('\t'.join((r['id'],) + out[r['id']]) + '\n')
print('written', len(rows) - len(done))
