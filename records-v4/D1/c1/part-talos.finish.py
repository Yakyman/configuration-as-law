import csv,collections,json,os,re
from pathlib import Path
base=Path('D1/c1'); inp=list(csv.DictReader(open('D1/in/part-talos.tsv'),delimiter='\t'))
fields=['id','decision','sentences','what_it_does','basis','reason']
p=base/'part-talos.tsv'
existing=list(csv.DictReader(p.open(),delimiter='\t')); seen={r['id'] for r in existing}
with p.open('a') as f:
 w=csv.DictWriter(f,fields,delimiter='\t',lineterminator='\n')
 for k in (1,2):
  for r in csv.DictReader((base/f'part-talos.{k}.tsv').open(),delimiter='\t'):
   if r['id'] in seen:continue
   w.writerow(r);f.flush();os.fsync(f.fileno());seen.add(r['id'])
notes='''# Talos classification c1 notes

COMMON.md was read first. The decision standard is TEXT.md Sections 8.1–8.3, with Section 8.5 exclusions; SENTENCES.md supplies the cited identifiers. Only the assigned Talos input and its indexed raw evidence were used. The other classification, comparison, adjudication and earlier nights were not consulted.

The three parallel parts partitioned input indices 0–91, 92–212 and 213–277. Their decisions are consolidated without removing image aliases or repeated paths: input row identity is preserved.

## Container image rule

Rows 213–224 are containerd image observations. The first question, together with the installer/package definitions, takes precedence over describing their executable payload as a program. S8.2-16 requires selecting a recording line. The observations establish image presence and CRI management, but not whether an image was obtained explicitly or from another recorded object. Both acquisition routes are possible; this is a missing instance fact, not a conflict in the text. All twelve decisions are UNKNOWN.

Ten rows were checked manually against the complete image metadata, matching image reference, digest, timestamp, size and management labels. The first eight are tag/digest pairs for the API server, controller manager, scheduler and pause image; the next two are image-ID aliases of controller manager and scheduler. None contains acquisition-reason or source-line evidence:

'''
notes+='\n'.join('- '+inp[i]['id'] for i in range(213,223))+'\n'
notes+='''
The remaining two image-ID aliases were also checked individually against the pause and API server digests. Management and pinned labels do not identify the acquisition source.

Primary documentation:

- https://github.com/containerd/containerd/blob/main/docs/cri/crictl.md : “The pull command tells the container runtime to download a container image from a container registry.” The same guide documents image loading from an archive. Neither establishes how these particular images arrived.
- https://github.com/containerd/containerd/blob/main/cmd/ctr/commands/images/pull.go : “Fetch and prepare an image for use in containerd.” This identifies image acquisition functionality rather than a conventional native package manager.

## Stored objects: individual assessments

Every row from 225 through 277 was assessed individually. All 35 complete immediate member tables were read, including every listed member of the large udev data, links and watch groups. The other rows are eleven opaque directories and seven executable-permission candidates. Each output explanation identifies the missing instance fact; no classification rule based on the collector's kind label was used.

FACTS.md explicitly states that all member persistence fields are unknown, signatures were not collected, and the mount observations are not a certified object-to-covering-mount persistence map. The 287 captured package-file candidates also have unknown integrity. No unchanged package ownership is inferred for paths outside that bounded candidate list.

Mount relationships and stored directory entries are distinct input objects. An active mount is runtime, but its path alone does not establish the origin of the underlying stored directory or the backing of every nested member. The container rootfs mounts below /run are a concrete reason not to extrapolate the enclosing tmpfs to opaque descendants. General documentation cannot certify an unobserved bind mount, file content, integrity, or creator on this instance.

The listing's executable flag for /run/mdadm/autorebuild.pid was not treated as code. Upstream source identifies the file as a process identifier written with mode 0700. The unresolved decision is its actual storage lifetime, rather than whether an execute bit automatically makes a program.

Primary documentation and scope of use:

- https://kernel.googlesource.com/pub/scm/linux/kernel/git/hare/mdadm/+/f7a6246bab1541d7208a5f0f9f0c6cac114e38da/Monitor.c : `open(path, O_WRONLY | O_CREAT | O_TRUNC, 0700)` and `fprintf(fp, "%d\\n", pid)` identify PID-file creation and explain the misleading execute bit.
- https://www.cni.dev/plugins/current/ : “These are general-purpose CNI network plugins maintained by the containernetworking team.” Individual entries identify bridge creation, local address allocation, firewall rules and port mapping. This establishes the named programs' roles, not the signatures or provenance of the inventoried files.
- https://docs.kernel.org/filesystems/sysfs.html : “sysfs is a RAM-based filesystem initially based on ramfs.” This identifies sysfs semantics; the opaque /sys directory observation does not itself certify its mount identity or expanded contents.
- https://docs.kernel.org/filesystems/proc.html : “The proc file system acts as an interface to internal data structures in the kernel.” This identifies procfs semantics without supplying the missing instance mount observation.
- https://cdn.kernel.org/doc/html/latest/filesystems/tmpfs.html : “Tmpfs is a file system which keeps all of its files in virtual memory.” This explains why object-specific backing matters: a transient object and a persistent working record can have different decisions.

No group is marked MIXED merely because filenames suggest heterogeneous purposes: differing decisions must be established. For these stored groups, the missing facts prevent definitive member decisions. This is UNKNOWN rather than a defect of the text. Section 8.5 implementation questions were not counted as gaps.

## Deciding sentences

'''
sents=Path('SENTENCES.md').read_text().splitlines()
for line in sents:
 if any('**'+sid+'**' in line for sid in ['S8.1-4','S8.1-6','S8.2-5','S8.2-6','S8.2-7','S8.2-9','S8.2-11','S8.2-15','S8.2-16','S8.2-17','S8.2-23']):notes+=line+'\n\n'
notes+='## Part 1 notes\n\n'+(base/'part-talos.1.notes.md').read_text()+'\n## Part 2 notes\n\n'+(base/'part-talos.2.notes.md').read_text()
(base/'part-talos.notes.md').write_text(notes)
allowed='INSTALLED-OWN INSTALLED-PACKAGE INSTALLED-DERIVED PROGRAM-OWN PROGRAM-DERIVED SETTING-OWN SETTING-DEFAULT RECORD MATERIAL RUNTIME ACTION GAP-NONE GAP-TWO UNKNOWN MIXED'.split()
with p.open() as f:
 reader=csv.DictReader(f,delimiter='\t'); assert reader.fieldnames==fields; output=list(reader)
a=collections.Counter(r['id'] for r in inp);b=collections.Counter(r['id'] for r in output)
assert a==b and all(n==1 for n in b.values()) and len(inp)==len(output)
valid_sids=set(re.findall(r'\*\*(S8\.[123]-\d+)\*\*',Path('SENTENCES.md').read_text()))
for r in output:
 assert set(r)==set(fields) and all(isinstance(x,str) for x in r.values()),r
 assert r['decision'] in allowed,r
 assert len(r['what_it_does'].split())<=15,r
 assert len(r['reason'].split())<=30,r
 assert set(r['sentences'].split(','))<=valid_sids,r
 assert all('\t' not in v and '\n' not in v and '\r' not in v for v in r.values()),r
 if r['basis'].startswith('raw:'):
  q=r['basis'][4:]
  assert Path(q).exists() or Path('D1/in/raw/talos',q).exists(),q
counts=collections.Counter(r['decision'] for r in output)
(base/'part-talos.done').write_text(''.join(f'{d}\t{counts[d]}\n' for d in allowed))
with (base/'part-talos.notes.md').open('a') as f:
 f.write('\n## Final mechanical verification\n\nVerified 278 input IDs and 278 output IDs: identical sets and counts, each once. All decisions belong to the fifteen allowed words; all sentence identifiers, field limits, field delimiters and raw evidence paths passed validation.\n')
print('\n'.join(f'{d}\t{counts[d]}' for d in allowed))
