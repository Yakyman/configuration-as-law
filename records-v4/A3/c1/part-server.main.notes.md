# Server classification: package and runtime subset

Only (not published: orchestration), TEXT.md, SENTENCES.md, A3/in/FACTS.md, the server input and server raw inventory were used. No other classification was consulted. These are classification decisions, not acceptance of a hypothesis or independent review.

## Interpretation and facts

The four questions are applied in order. S8.2-5 identifies runtime instances before a persistent object's four questions are needed. A running process is distinct from its stored executable; a kernel table is distinct from a saved firewall configuration. Installed-package coverage is asserted for a stored executable only when package-files.tsv reports unchanged. Package rows themselves are installed objects regardless of individual file integrity.

The runtime class is invariant when the creator's identity or own recording line is unknown. The task explicitly requires the invariant decision when every possible missing fact gives it. Therefore the process/socket remains RUNTIME, and its reason openly states that the creator or creator decision is UNKNOWN. Socket output contains no PID or executable ownership: standard port numbers cannot establish actual ownership. No undocumented name is supplied to fill that absence. Container process executable paths do not establish unchanged image contents.

Kernel-module names describe modules exposed by the running kernel, not new copies of their persistent files. All 41 names were matched to unique kernel package files and unchanged integrity. The runtime module instance follows that file's INSTALLED-PACKAGE decision. Both nft and nf_tables persistent binaries also have unchanged package integrity.

Firewall rows are kernel state reported by nft/iptables queries. KUBE/FLANNEL objects are attributed to the documented K3s networking controllers; Docker chains/interfaces to dockerd. Other base tables/chains belong to the nf_tables kernel subsystem. The cal_filter objects are loaded by nft. The dockerd executable has unknown integrity; this uncertainty is retained in its parent decision. A running extracted K3s executable is distinguished from its installation launcher. These attributions use recorded controller processes, concrete chain/interface identities, and documentation; they do not classify by inventory kind wording alone.

## Documentary support

- https://www.netfilter.org/projects/nftables/manpage.html: “rules in the Linux kernel, in the nftables framework.” This establishes that the query observes kernel firewall state.
- https://docs.docker.com/engine/network/firewall-iptables/: “Docker creates the following custom `iptables` chains in the `filter` table”. This supports the Docker chain attribution.
- https://docs.k3s.io/networking/networking-services: “K3s includes an embedded network policy controller.” This supports K3s network-policy attribution.
- https://docs.k3s.io/networking/basic-network-options: “The default backend for Flannel is `vxlan`.” The page describes Flannel as K3s network functionality.
- https://docs.k3s.io/blog/2025/03/25/K3s-initialization: “At this point, K3s will extract the binaries.” It documents the data directory containing extracted bundled executables.
- https://man7.org/linux/man-pages/man5/sysfs.5.html: “The sysfs filesystem is a pseudo-filesystem which provides an interface to kernel data structures.” This supports treating exposed module instances as runtime state.
- https://man7.org/linux/man-pages/man8/iptables-save.8.html: “iptables-save — dump iptables rules”. Generated comments and COMMIT separators are dump framing, not typed actions or independent firewall policies.

## Homogeneous rules

P — Installed dpkg package rows. Question one answers yes. Use the recorded explicit/dependency reason: explicit packages need their own line; dependencies are covered by their requesting package's line. Deciding sentences: S8.1-6, S8.2-6 through S8.2-8, S8.2-16. Integrity affects package members, not the fact that the package is installed.

X — Process instances. S8.2-5 gives RUNTIME. For the reason, independently join the executable path to package integrity, or use documented K3s extraction, or retain UNKNOWN for unestablished provenance. A separately supplied standalone executable has its own program line. Deciding sentences: S8.2-5, S8.2-7, S8.2-9, S8.2-10, S8.2-16.

M — Kernel module instances. S8.2-5 gives RUNTIME; each unique unchanged backing module is INSTALLED-PACKAGE under S8.2-7, S8.2-8, S8.2-16. The script asserts the unique unchanged join for every row.

L — Open sockets. S8.2-5 explicitly gives RUNTIME. All source rows omit socket ownership. Missing owner identity never changes this class; the reason states the unresolved creator decision.

F — Actual kernel firewall tables, chains and rules. S8.2-5 gives RUNTIME. Parent attribution is resolved separately as explained above. Dump framing is excluded before this rule. No assumption about persistent saved configuration is inferred from the live rules.

D — Generated dump comments and COMMIT framing. These are output recorded by the dump program; S8.2-15 gives RECORD after the earlier questions fail. COMMIT is not an action typed by a person and does not itself hold a firewall policy.

The following samples were displayed and checked manually against their full row metadata, resulting reason and relevant raw-file joins. Each list has ten IDs. P checks include explicit and dependency reasons; X includes unavailable executable identities; M checks module integrity; L checks TCP/UDP and missing ownership; F checks NFT/iptables objects and distinct parent branches; D checks both comments and terminators.

P: server-4830b005c5e95a80b9f05ea4, server-894f5d9c38cd1e3d38bd400a, server-7f79272f1d28c42f51277b05, server-e0a3fcedc0d8fc7f2c62819b, server-dd035f97841eb9c1044b6a0a, server-c5ad3ba1bcf58c05751986c3, server-a9a4344573c7ba68fe031a19, server-26b2cc84e0f18c65684980ac, server-ac29b0440441e8288cfb4d98, server-bb9e72f382f8bf301bbe6862.

X: server-cabd2fe206a1d620b3e41bad, server-eb5512b7d87a9d73d71980ba, server-4ee952c534b1127162151e32, server-6e2f004cb8fc03dbacfbb622, server-1421586b181f55637bdde0b8, server-5328ae6ea261addd2d5c2cb5, server-7fe924d095e53dae4a99f8e9, server-78e6bce75d501759ddc81955, server-82a020220e4fab69bebe0b17, server-bd383f6adda5449ee17f182b.

M: server-cafbb167cd3c3263e11c45af, server-72df891f8e9fbb3c82e182aa, server-ef17b770682f7c6d48df36ef, server-81c82a1e10a33a9ec991ba8d, server-7d5779b77057f6d8e522bbce, server-820b6ffacd170a3a74f3a610, server-eb412d6403b0bc1457e35413, server-443f97e416cabdd6b6d30460, server-ab26cfb98955a4597f6db852, server-9a13b95e77fca3a626a8d8ec.

L: server-2f5b482b083f366816d44e3f, server-c4d2aebc308b9235ab3cc3ea, server-9d7da68dc1067a79c753fb67, server-3cb5278e4dd09604d4b38f53, server-553a7bd762f9b89e286a67c4, server-256a6ae7114b5f2532bc9947, server-937210adca00b36db1edaad2, server-c9db236bc5e64bca80f177b6, server-0bda2359e78aad923356bfa7, server-9fd3e42a94561c2dbbfd8dba.

F: server-df39c40167f8ea0d545dc239, server-1be3fa2818d993c93cb99cfd, server-6f871340730b47a44335c957, server-5309ce530ffcc7acb81a8b50, server-4b83b7f6ba1008e10b9097d0, server-4e9b27c65dac31ea55eb5033, server-3ac8a7fed8fd8316ee5ec3cc, server-705809e00425cf00cf227a0d, server-c0780fcf72408c3372315333, server-b16b05c3819a49da8de0c367.

D: server-5502da6830c10a1165a74676, server-1ba2be3776f025f8783a28b1, server-e1388a90f4459e733417839b, server-8a3aeac968de2b8a45e679fe, server-9b75fa3ea1a9710aad2bf1e4, server-0c12b9253ef30ef4a3fde492, server-c810ba3b3d9d8b295861e0b0, server-6fb8e469e318c6fad6796d83, server-bb36907dcf8ea69d8b8eceba, server-ff146b3df6f16f6dfa28e559.

## Exact deciding sentences

- **S8.1-6** **Package**—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.

- **S8.2-5** What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.

- **S8.2-6** What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.

- **S8.2-7** Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?

- **S8.2-8** Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.

- **S8.2-9** Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?

- **S8.2-10** Then it is a **program**, whoever wrote it and wherever it came from; a program belongs to what is installed.

- **S8.2-15** Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.

- **S8.2-16** What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.

