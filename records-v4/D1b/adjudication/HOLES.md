# D1b adjudication: gap cards

2026-11-23 UTC. Two gaps out of 30,024 adjudicated rows (37 GAP rows). The row verdicts are in `rows.tsv`; the `hole` column holds the card number.

## Card 1. Container images: is the image engine an installer?

**The gap.** The object is a container image held by a container engine (Docker on Gentoo, containerd on Talos). The engine downloads the image whole, runs it as containers and removes it whole. Sentence S8.1-4 defines an installer by its documented purpose of "installing and removing programs", and names the system package manager and the package managers of languages and application packages. It does not say whether pulling and removing images is such a purpose. So the text does not decide whether the image is a package (question 1) or code that runs as its own process in a container (question 2).

**Sentences involved.**
- S8.1-4 «Installer—a program of the system whose purpose, according to its documentation, includes installing and removing programs: the system package manager, package managers of programming languages and of application packages.»
- S8.1-6 «Package—what an installer installs and removes as a whole»
- S8.2-7 «Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?»
- S8.2-22 «A program that runs as its own process on the computer, including in a container, is a program.»

**The two decisions.**
- **INSTALLED-OWN (question 1):** the image is a package. Its line records it as a package, and its layers and files are covered by that line for as long as they remain as received.
- **PROGRAM-OWN (question 2):** the image is a program. It needs a line of its own as code, and no package line covers its contents.

**Examples.**

| id | name | what it is |
|---|---|---|
| d1b-gentoo-f23478e06580c65ea0aab234 | sha256:a7dbc319b143… | busybox image pulled with Docker for the container action |
| d1b-talos-a17c1f63854bee1c87899ea5 | registry.k8s.io/kube-apiserver:v1.37.1 | control-plane image held by containerd |
| d1b-talos-a50f0524d2017d10970b75e0 | registry.k8s.io/kube-controller-manager:v1.37.1 | control-plane image held by containerd |
| d1b-talos-e634add8a1918968c654058e | registry.k8s.io/kube-scheduler:v1.37.1 | control-plane image held by containerd |
| d1b-talos-1de301bc31af36a197dad392 | registry.k8s.io/pause:3.10.2 | sandbox image held by containerd |
| d1b-talos-765c2ea628f6919041741da8 | sha256:336e72df967a… | image by digest held by containerd |

**Rows in the gap:** 13 (Gentoo 1, Talos 12).

## Card 2. A stored archive of code that nothing executes as it is

**The gap.** The object is an archive whose members are code that can run on this computer: a cached or downloaded wheel or source archive, a downloaded browser-extension archive, a download cache of source and binary archives, or a container image layer blob. No program executes the archive as it is; programs only keep it or unpack it. Question 2 asks whether the object is code the computer "executes or can execute", and question 4 names caches and downloaded files. The text does not say whether an archive that holds code is itself code. So the order of the questions does not settle the case: if the archive counts as code, question 2 answers yes first; if not, question 4 applies.

**Sentences involved.**
- S8.2-9 «Is the object code that the computer executes or can execute: on its own, at a person's command, or through another program with that program's rights?»
- S8.2-15 «Otherwise: if a program recorded the object as it ran, it is a program record—a log, cache, history, working state; if a person created or brought the object, it is material—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.»
- S8.2-23 «A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.»

**The two decisions.**
- **PROGRAM (question 2):** the archive is a program and belongs to what is installed. The declaration must carry a line for it (its own line, or a line from which the system obtained it).
- **RECORD or MATERIAL (question 4):** the archive is a program record (a cache) or material (a downloaded file). It need not be recorded, and the declaration may leave it out.

**Examples.**

| id | name | what it is |
|---|---|---|
| d1b-gentoo-ad430b0e40c6598dfabc0c7a | /home/user/.cache/pip/http-v2/3/0/9/6/6 | pip HTTP cache entry holding the published distro-1.9.0 wheel |
| d1b-gentoo-5ac0eff595ce87e7dfe6758e | /home/user/.cache/pip/http-v2/6/f/5/8/3 | pip HTTP cache entry holding the published setuptools-84.2.1 wheel |
| d1b-gentoo-44cbfcf5493841c61b3d2c5f | /home/user/.cache/pip/http-v2/b/7/7/0/d | pip HTTP cache entry holding the mozprofile-3.0.0 source archive |
| d1b-gentoo-2546496f6d830f0509d2db6c | /home/user/.cache/pip/wheels/40/8f/0b/… | wheel that pip built locally from the mozprofile source |
| d1b-gentoo-d366c590629c496123b00a73 | /home/user/Downloads | downloaded browser-extension archive (clearurls.xpi) |
| d1b-gentoo-b92d06df7c2cb763db610d04 | /var/cache/distfiles | Portage download cache: Go bootstrap and Rust binary archives, Python source archives |
| d1b-gentoo-c303bfa08eaf41759cb7b68b | /var/lib/containerd | container store with the busybox layer blob (tar+gzip) |
| d1b-void-0c614b583829bd40eb38d058 | /var/lib/docker | container store with the busybox layer blob (tar+gzip) |

**Rows in the gap:** 24 (Gentoo 23, Void 1).
