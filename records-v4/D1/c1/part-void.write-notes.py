import csv,json,re,pathlib
csv.field_size_limit(10000000)
rows={r['id']:r for r in csv.DictReader(open('D1/in/part-void.tsv'),delimiter='\t')}
rules=json.load(open('D1/c1/part-void.main-rules.json'))
descriptions={
'package-explicit':'An actually installed package with explicit selection answers question 1. In the absence of containing-package or derivation evidence, S8.2-16 requires its own line: INSTALLED-OWN.',
'package-dependency':'An actually installed dependency answers question 1 and is covered by the requesting package line under S8.2-16: INSTALLED-DERIVED. This is the required recording relation, not an assertion that this machine already has a declaration.',
'python-dependencies':'The browser action log expressly names the dependency chain and successful installation of each distribution under marionette_driver. This independently resolves the inventory reason=unknown for these 16 rows: INSTALLED-DERIVED. The distro row has an erroneous collected display name; its distribution location and version identify the installed distro wheel, not a separate operating system.',
'package-unknown':'The package is installed, but neither a reason nor complete containing-package provenance is established. UNKNOWN records the missing fact controlling S8.2-16. Native ownership of metadata alone does not prove native ownership of the complete language package.',
'unchanged-files':'Exact path joins establish package ownership and integrity=unchanged. S8.2-6 gives question 1 priority even for executable policy code and configuration defaults: INSTALLED-PACKAGE. This includes the supplied wpa_supplicant default file and ten GRUB files.',
'polkit-packaged':'Each registered action identifier was matched to XML content in the retained policy files, which have unchanged integrity. These definitions are parts of those packages, giving INSTALLED-PACKAGE before the setting question. An action identifier is not a performed human action.',
'sysfs-runtime':'The actual collection commands enumerate sysfs module and driver registrations, not stored module binaries. These are kernel-created runtime objects, hence RUNTIME under S8.2-5. The running kernel image and its installation integrity are not identified: parent decision UNKNOWN.',
'process-runtime':'Each row is an observed process from procfs. S8.2-5 gives RUNTIME for every executable identity. The reason names its executable and INSTALLED-PACKAGE where exact current-file integrity is unchanged, otherwise UNKNOWN. Deleted executables are not equated to replacement package bytes. The supplied inventory probe is independently bootstrapped code.',
'dump-record':'Comment lines and serialization delimiters emitted by iptables-save are query output, not live access rules or person-typed commands. S8.2-15 gives RECORD.',
'firewall-runtime':'Rows representing kernel-resident chains, counters, and rules have runtime lifetime. No saved rule file is represented by this query. S8.2-5 gives RUNTIME; Docker-marked bridge rules name the daemon, other kernel tables name netfilter. Their creator recording decision is UNKNOWN rather than guessed from an unverified executable.',
'identity-origin':'Existing passwd/group records establish local identities and rights under S8.2-13. The particular identity origin is not established, so SETTING-OWN versus SETTING-DEFAULT cannot be selected. Installation-created identities proved by action output are handled individually instead.',
'service-origin':'The symlinks select enabled runit services under S8.1-11 and S8.2-13. Their original creation as installation defaults versus separately chosen values is unrecorded, giving UNKNOWN under S8.2-17. A successful run status alone does not establish link creation provenance.',
'code-origin':'The shebang/startup/interpreter evidence identifies code, and persistence is known. The retained file manifest lacks ownership/integrity for each exact path. Earlier question 1 and S8.2-16 can therefore change the category or line; UNKNOWN names those missing facts. Executable permission by itself was not used: times.json was individually excluded.'}
f=pathlib.Path('D1/c1/part-void.notes.md').open('w')
f.write('# Void c1 classification notes\n\nOnly COMMON.md, TEXT.md, SENTENCES.md, the assigned input, its fact index, permitted retained void evidence, and public documentation were consulted. No other classification or earlier night was read. The two stored-group portions were independent parallel parts of this classification.\n\n')
f.write('## Fixed sentences\n\n')
for line in open('SENTENCES.md'):
 if any(('**'+s+'**') in line for s in ['S8.1-6','S8.1-11','S8.2-2','S8.2-5','S8.2-6','S8.2-7','S8.2-8','S8.2-9','S8.2-10','S8.2-11','S8.2-13','S8.2-15','S8.2-16','S8.2-17','S8.2-23']):f.write(line+'\n')
f.write('## Scripted rules and manual checks\n\nThe scripts append and flush each finished row and skip existing IDs. The following ten evenly spaced cases per rule were displayed and manually examined against the relevant metadata, content, and joins. A sample ID is an object reference; generic account home paths are omitted here.\n\n')
for key,desc in descriptions.items():
 ids=rules[key]; picks=[ids[int(i*(len(ids)-1)/9)] for i in range(10)]
 f.write('### '+key+'\n\n'+desc+'\n\nManually checked: '+', '.join(picks)+'.\n\n')
f.write('''## Individual decisions and evidence limits

- Installation output expressly creates _tss, polkitd, _flatpak, dbus, and docker identities during package installation. Their account/group values are SETTING-DEFAULT. The relevant application_package, network_connection, and container_run logs are under `D1/in/control/void/actions-logs/actions-logs/`.
- The network log expressly adds cal-secondary and cal-test after package installation. Their logical profiles and persistent files are SETTING-OWN. Other connection rows do not distinguish saved versus generated transient profiles.
- The sudo output headings are RECORD. secure_path, visudo environment preservation, and root authorization were checked against the retained unchanged sudoers content. Supplemental wheel and lab rules lack origin evidence and remain UNKNOWN.
- Open sockets remain RUNTIME despite the socket query omitting process ownership. The missing parent decision is expressly UNKNOWN; a conventional port number was not used to guess its process.
- Firefox times.json is timestamp data despite its executable mode. Public profile-creation documentation and the observed fresh profile establish RECORD. It is not code merely because the collector put it among executable candidates.
- The boot action stderr explicitly records generation of the 6.12.118 and 6.18.64 initramfs images. GAP-TWO states the two readings: PROGRAM-DERIVED if an archive of executable payload is itself code, RECORD if only the archive container is classified as generated storage. S8.2-9 does not define the archive boundary; S8.2-16 supplies coverage only after the object category is known. This is distinct from a known non-executed HTTP cache wrapper.
- The old initramfs and installed GRUB boot copies lack current receipt/generation facts, giving UNKNOWN. The ten unchanged GRUB package-source files answer question 1 and never reach this issue.
- The BusyBox image is an opaque filesystem image rather than a running container process. GAP-NONE names the absent treatment of such an image as a package, code itself, or filesystem material. S8.2-22 explicitly addresses the running program, not the stored image. The stopped container separately lacks a member inventory of its writable layer: UNKNOWN.
- Opaque persistent application/container stores were not called runtime. Their contents were not expanded, so their member decisions cannot be established.

## Public sources and supporting passages

- https://www.kernel.org/doc/html/latest/filesystems/sysfs.html — “sysfs is a RAM-based filesystem initially based on ramfs.” This establishes the lifetime and kernel-export function of the enumerated registrations.
- https://docs.voidlinux.org/config/services/index.html — “Void uses the runit(8) supervision suite to run system services and daemons.” The service-directory links select enabled services; documentation does not establish each observed link's origin.
- https://www.freedesktop.org/software/polkit/docs/master/pkaction.1.html — “pkaction is used to obtain information about registered polkit actions.” The query lists definitions rather than performed human actions.
- https://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html — “Actions are defined by applications.” The action definitions are matched to retained XML policy content and its installation integrity.
- https://docs.docker.com/engine/network/firewall-iptables — “Docker creates iptables rules in the host's network namespace for bridge networks.” This identifies the bridge firewall producer, not persistent configuration provenance.
- https://www.gnu.org/software/bash/manual/html_node/Interactive-Shell-Behavior.html — “Bash reads and executes startup files as described in Bash Startup Files.” Thus shell startup files reach the code question if not unchanged package objects.
- https://docs.telemetry.mozilla.org/concepts/profile/profile_creation — “a times.json containing a timestamp of the current time is stored inside that profile directory”. This identifies the profile timestamp record.
- https://www.gnu.org/software/grub/manual/grub/html_node/Invoking-grub_002dinstall.html — “The program grub-install generates a GRUB core image using grub-mkimage and installs it on your system.” Actual provenance of the observed boot copies is still not retained.
- https://www.kernel.org/pub/linux/utils/boot/dracut/dracut.html — “dracut - low-level tool for generating an initramfs/initrd image”. Generation of two observed images is independently recorded in the action stderr.
- https://docs.docker.com/engine/storage — “By default all files created inside a container are stored on a writable container layer”. The exited container's reported changes are not an inventory of those files.

## Stored groups

The rules, exact sentence quotations, ten manual checks per rule, and individual group decisions are retained in [part a notes](part-void.a.notes.md) and [part b notes](part-void.b.notes.md). These form part of this notes file by reference. Complete MIXED assignments are in the respective `part-void.a.members.tsv` and `part-void.b.members.tsv` sidecars. They describe every immediate member, not inferred recursive contents. The final output's basis points to the actual retained member table.

Section 8.5's implementation and storage-policy exclusions were not counted as gaps. No hypothesis outcome or gap weight is assigned by this classification. Mechanical output validation is not independent acceptance of the classification.
''')
f.close()
