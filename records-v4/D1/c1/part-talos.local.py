import csv,json,os
from pathlib import Path
rows=list(csv.DictReader(open('D1/in/part-talos.tsv'),delimiter='\t'))
out=Path('D1/c1/part-talos.tsv')
fields=['id','decision','sentences','what_it_does','basis','reason']
existing={r['id'] for r in csv.DictReader(out.open(),delimiter='\t')} if out.exists() else set()
def put(i,decision,sentences,what,reason,basis=None):
 r=rows[i]
 if r['id'] in existing:return
 assert len(what.split())<=15,(i,what)
 assert len(reason.split())<=30,(i,reason)
 with out.open('a') as f:
  w=csv.writer(f,delimiter='\t',lineterminator='\n')
  if out.stat().st_size==0:w.writerow(fields)
  w.writerow([r['id'],decision,sentences,what,basis or 'raw:D1/in/raw/talos/'+r['evidence'],reason]);f.flush();os.fsync(f.fileno())
 existing.add(r['id'])
for i in range(213,225):
 put(i,'UNKNOWN','S8.1-4,S8.1-6,S8.2-7,S8.2-8,S8.2-16','Containerd image supplying Kubernetes component executable files.','Image presence is established; whether explicitly obtained or obtained from another recorded object is unknown, preventing selection of its recording line.')
# Each entry below is an individual assessment of the complete supplied member list or opaque object.
assessments={
225:('Root directory entries and symbolic links.','Member ownership, integrity and backing are unknown; names alone do not establish which stored entries came unchanged from the image or were generated.'),
226:('Unexpanded device directory.','Contents and backing of the stored directory are unestablished; the devtmpfs mount observation does not identify every contained object or its origin.'),
227:('Unexpanded process information directory.','The inventory does not establish this directory’s mounted filesystem or contents; the conventional procfs purpose cannot certify this particular stored object.'),
228:('Unexpanded system device information directory.','The inventory does not establish this directory’s mounted filesystem or contents; the conventional sysfs purpose cannot certify this particular stored object.'),
229:('Unexpanded system service directory.','The directory is unexpanded; backing of nested contents and their package membership, integrity and function are unknown.'),
230:('EFI directory entry under the boot directory.','The EFI directory’s package membership, integrity, creator and backing are unknown; no contents or creation evidence establish its recording line.'),
231:('System configuration files, directories and symbolic links.','Every member lacks ownership and integrity facts; generated values, unchanged image defaults and chosen settings cannot be distinguished from this listing.'),
232:('Unexpanded containerd configuration directory.','Contents, package membership, integrity and provenance are unknown; the directory name does not establish whether values are defaults or chosen settings.'),
233:('CNI and containerd directories under the optional software directory.','Both directory entries lack package membership, integrity and creation evidence; the overlay mount alone does not determine their recording lines.'),
234:('Unexpanded containerd storage directory.','Contents and creation provenance are absent; executable content, image components and working records cannot be distinguished.'),
235:('Runtime service directory entries.','Member backing is unknown; nested container root mounts show that the enclosing tmpfs name cannot establish persistence for every listed object.'),
236:('Unexpanded containerd runtime directory.','Nested persistent container root mounts exist; unexpanded contents cannot be uniformly assigned RUNTIME, installed content or program records.'),
237:('Variable-data directories and a runtime symbolic link.','Membership is complete, but stored entries’ origins and backing are unknown; mount relationships do not establish directory-entry creation provenance.'),
238:('Unexpanded variable system directory.','No contents, package relationship or creator facts establish whether stored objects are installed components, settings or records.'),
239:('AppArmor parser configuration file.','Package membership, integrity, value contents and origin are unknown; unchanged package data and chosen access configuration require different decisions.'),
240:('AppArmor ABI and disabled-profile directory entries.','Both entries lack package membership, integrity and creation evidence; default directories and changed access configuration cannot be distinguished.'),
241:('CNI network configuration directory entry.','The net.d entry lacks object-specific backing and provenance; enclosing tmpfs evidence does not certify nested contents or their recording line.'),
242:('Containerd configuration file and configuration-fragment directory.','Both members lack package integrity and creation provenance; package defaults, chosen service settings and runtime-generated values cannot be distinguished.'),
243:('iSCSI initiator identity file.','The identity’s value and origin are uncollected; a chosen setting, package default and generated working identity have different decisions.'),
244:('Kubelet connection configuration, service configuration and certificate directory.','All members lack object-specific backing and origin; generated transient values, packaged values and chosen service parameters cannot be distinguished.'),
245:('LVM configuration files and profile directory.','Package ownership, integrity and chosen-versus-default origin are unknown for all three members, preventing the first and third questions from being resolved.'),
246:('NVMe host identifier and qualified-name files.','Whether these identities were chosen, packaged unchanged or generated is unestablished; their contents and object-specific persistence were not collected.'),
247:('SELinux targeted-policy directory entry.','The directory’s package membership, integrity and origin are unknown; its name does not establish unchanged installed policy.'),
248:('Certificate-store directory entry.','Package membership, integrity and creation provenance of the certs directory are unknown; a directory name cannot establish inherited recording coverage.'),
249:('CNI executable-directory entry.','The bin directory’s creation provenance and package relationship are unknown; known plugin names below it do not establish the directory’s own origin.'),
250:('D-Bus system socket filesystem entry.','A socket node is listed, but liveness and object-specific backing are unknown; a persistent stale node and a live runtime endpoint differ.'),
251:('LVM lock-directory entry.','Object-specific backing and creation provenance are unknown; the enclosing run directory does not certify this stored entry’s lifetime.'),
252:('MD RAID monitor process identifier file.','Documentation identifies a PID record despite executable permissions; object-specific persistence is unknown, leaving RECORD versus RUNTIME unresolved.'),
253:('MD RAID monitor process identifier file with executable permissions.','An execute bit does not prove code; documentation identifies a PID record, but unestablished backing leaves RECORD versus RUNTIME unresolved.'),
254:('Node Resource Interface socket filesystem entry.','A socket node is listed, but liveness and object-specific backing are unknown; a stale stored node and a runtime endpoint differ.'),
255:('Udev sockets and device-state directory entries.','Socket liveness and object-specific backing of all members are unestablished; runtime objects cannot be distinguished from stored working records solely by names.'),
256:('CNI, containerd, etcd and kubelet data-directory entries.','All four entries lack creation and package provenance; their service associations do not establish whether stored objects are defaults, chosen settings or records.'),
257:('Unexpanded containerd data directory.','Contents are opaque; installed image data, service parameters and working records cannot be individually identified or assigned recording lines.'),
258:('Unexpanded kubelet data directory.','Contents are opaque; executable workload data, service parameters and working records cannot be individually identified or assigned recording lines.'),
259:('Service log files and audit, container and pod directories.','Log naming indicates records, but contents and object-specific backing are unknown; directory members are unexpanded and transient versus persistent records remain unresolved.'),
260:('Unexpanded container log directory.','Contents and object-specific backing are unknown; a persistent log record and a transient runtime object require different decisions.'),
261:('AppArmor ABI feature-description file.','Its package membership and integrity are unknown; an unchanged packaged description and a generated or supplied replacement have different first-question answers.'),
262:('Containerd base fragment, service configuration, container specification and registry directory.','Each member lacks integrity and origin evidence; packaged defaults, chosen service settings and generated runtime values cannot be distinguished.'),
263:('Kubernetes certificate-authority certificate.','Certificate origin, package integrity and object-specific backing are unknown; package content, chosen trust settings and transient generated values cannot be distinguished.'),
264:('Eight LVM profile files.','Every profile lacks package membership and integrity; unchanged package defaults and locally supplied or changed configuration require different decisions.'),
265:('SELinux security-context directory entry.','Package membership, integrity and creation provenance are unknown; the unexpanded context directory does not establish a recording line.'),
266:('Certificate bundle and certificate-directory symbolic link.','Both members lack package integrity and creation provenance; unchanged installed content and changed trust values cannot be distinguished.'),
267:('Six executable-permission CNI network plugin files.','All six files lack signatures, package membership, integrity and derivation facts; neither executability nor the correct recording line is established.'),
268:('Bridge CNI plugin candidate.','The named plugin normally creates bridges, but this file’s signature, package integrity and acquisition provenance are unknown; the first question remains unresolved.'),
269:('Firewall CNI plugin candidate.','The named plugin normally configures filtering, but this file’s signature, package integrity and acquisition provenance are unknown; the first question remains unresolved.'),
270:('Flannel CNI plugin candidate.','This executable-permission file lacks content signature, package membership, integrity and derivation evidence; its filename cannot establish the recording line.'),
271:('Host-local CNI address-allocation plugin candidate.','The named plugin normally allocates addresses, but this file’s signature, package integrity and acquisition provenance are unknown; the first question remains unresolved.'),
272:('Loopback CNI plugin candidate.','This executable-permission file lacks content signature, package membership, integrity and derivation evidence; its filename cannot establish the recording line.'),
273:('Port-mapping CNI plugin candidate.','The named plugin normally maps ports, but this file’s signature, package integrity and acquisition provenance are unknown; the first question remains unresolved.'),
274:('Udev device-state database entries.','The listing identifies device-state records but not contents or object-specific backing; persistence determines RECORD versus RUNTIME and is unestablished.'),
275:('Udev device-link tracking directory entries.','The directories’ contents and object-specific backing are unknown; persistent working records and transient runtime state cannot be distinguished.'),
276:('Udev systemd-tag tracking directory entry.','The directory’s contents and object-specific backing are unknown; persistent working records and transient runtime state cannot be distinguished.'),
277:('Udev device-watch tracking symbolic links.','The links’ object-specific backing and targets are uncollected; persistent working records and transient runtime state cannot be distinguished.')
}
for i,(what,reason) in assessments.items():
 m=json.loads(rows[i]['members'])
 basis='raw:D1/in/raw/talos/'+m['file'] if isinstance(m,dict) and 'file' in m else None
 ss='S8.2-5,S8.2-7,S8.2-9,S8.2-11,S8.2-15,S8.2-16,S8.2-17'
 put(i,'UNKNOWN',ss,what,reason,basis)
