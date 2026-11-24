# Review notes: A3 sample rows 1–150

The output is `S2/a1/raw/a3-first.tsv`. The complete row-to-inventory map is `S2/a1/raw/a3-first-evidence.md`. The script encodes the reviewed rules, not the original classifications' reasons. Every original row was joined by ID, and every referenced member table was read. Sample path escaping was normalized only for the equality check; original inventory metadata decides facts.

## Literal decision rules

S8.2-5: “What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.” This decides live firewall observations, processes, loaded module instances, timer activation observations, open ports, and groups whose entire immediate membership is on volatile filesystems. This is not a decision about the persistent settings that recreate them. Unknown process executable identity does not change the label RUNTIME: every possible executable identity leaves a process a process.

S8.2-7 and S8.2-8 decide installed packages first. S8.2-16 says: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.” Explicit versus dependency reasons are directly present in the original package JSON. This review tests the appropriate recording route, not whether these ordinary machines already possess a declaration.

S8.2-15 decides locally generated logs, cache metadata and cache directory structures. S8.2-23 distinguishes values from code. Group membership is exactly the complete immediate-child list established by `A3/in/FACTS.md`, not recursive descent. In particular, cache directories do not make their nested package or code files RECORD. No descendant claims were made for either the cache-root or uv-cache-root group.

## Specific evidence

- All ordinary volatile groups have every member marked `runtime`. Two exceptions required inspecting original filesystem magic rather than accepting the collector's `persistent` fallback: RPC pipefs has `0x67596969`; the network namespace handle has `0x6e736673`. See (not published: over 20 MB). The kernel [RPC implementation](https://raw.githubusercontent.com/torvalds/linux/v6.12/net/sunrpc/rpc_pipe.c) defines `RPCAUTH_GSSMAGIC 0x67596969` and assigns it to the superblock; the [magic definitions](https://raw.githubusercontent.com/torvalds/linux/v6.12/include/uapi/linux/magic.h) define `NSFS_MAGIC 0x6e736673`. The [RPC filesystem implementation](https://raw.githubusercontent.com/torvalds/linux/master/net/sunrpc/rpc_pipe.c) describes itself as “Userland/kernel interface for rpcauth_gss.” The [namespace filesystem implementation](https://raw.githubusercontent.com/torvalds/linux/master/fs/nsfs.c) implements live namespace references using a pseudo filesystem. These are runtime communication objects, not saved disk contents.
- CUPS backend group and individual SNMP backend: all five backend-available originals are `unchanged` in (not published: over 20 MB). (not published: over 20 MB) establishes identical device/inode for each corresponding backend name, including the additional `mdns` name sharing the `dnssd` inode. Consequently the same file object was obtained with the installed package and remains unchanged. This is stronger than the prefix hashes; no equality was inferred solely from hashes or names.
- Two Lutris bytecode groups: every member has a corresponding source module owned unchanged by package ID `be8e5cf13c046a178fc7e8e7` in (not published: over 20 MB). The saved post-install script in `A3/in/raw/gaming/raw/0455-metadata-read-320.out`, decoded from its metadata entry, contains `py3compile -p lutris`. `A3/in/operator/gaming/actions-logs/actions-logs/gaming_prerequisites.log` records the successful package setup. The [Python documentation](https://docs.python.org/3/tutorial/modules.html#compiled-python-files) describes the corresponding compiled-module cache layout. S8.2-9/10 decides executable bytecode; S8.2-16 expressly covers the compiled copy from the package source.
- Nine Bun hashed `.npm` cache files: the [installer documentation](https://bun.sh/docs/pm/cli/install#npm-registry-metadata) says “Bun uses a binary format for caching npm registry responses.” The documented filename pattern is `${hash(packageName)}.npm`. These are registry metadata, despite the generic collector's shebang flag. The installation is corroborated by `A3/in/operator/developer/actions-logs/actions-logs/developer_global_tools.log`, which records the package-manager operation and 78 packages installed. No executable permission or code inference was made from the cache label.
- Go cache group: all five immediate members have `-a` suffix, size 175 bytes and no executable bit. The [Go cache implementation](https://go.dev/src/cmd/go/internal/cache/cache.go) defines an action index with output hash, size and timestamp; it distinguishes these from the `-d` output objects. The exact format is “v1 <hex id> <hex out> <decimal size space-padded to 20 bytes> <unixnano space-padded to 20 bytes>”. The action-index metadata is a program record; compiled output is not among these members.
- Both Git groups contain local reflogs, not downloaded object databases. [Git's documentation](https://git-scm.com/docs/git-reflog.html) says: “Reference logs, or "reflogs", record when the tips of branches and other references were updated in the local repository.” The one immediate member in each group is a local reference log.
- Cache structures: direct member tables identify directories, cache markers, lock files and manual-page indexes. [uv cache documentation](https://docs.astral.sh/uv/concepts/cache/) says “The uv cache is composed of a number of buckets” and “The directory and its lock file remain”. The [DNF5 configuration reference](https://dnf5.readthedocs.io/en/stable/dnf5.conf.5.html) describes cache storage as “including repositories metadata and downloaded packages.” Only directory structures are in the relevant DNF and PackageKit groups. [RubyGems source](https://github.com/ruby/rubygems/blob/master/lib/rubygems/source.rb) explicitly uses `FileUtils.mkdir_p cache_dir` while storing fetched specifications. The recorded RubyGems installation is in `A3/in/operator/developer/actions-logs/actions-logs/developer_global_tools.log`. The manual-page cache groups contain CACHEDIR.TAG, empty cat directories and index.db. None is a program or selected system value.
- The eighteen execution-log members correspond to the saved files in `A3/in/operator/gaming/actions-logs/actions-logs/`; all are captured log/error streams, rather than source scripts.
- One unresolved archive: `gaming-4538cc406b1a701b2b46aa9a`. The saved `A3/in/operator/gaming/actions-logs/actions-logs/gaming_store_runtime.log` explicitly records the updater downloading the named archive; the original object records executable permission but no shebang and a bounded prefix hash. Neither names nor permissions establish its contents, their execution, or whether the retained archive is installed package content rather than download working state. Therefore FACT-UNKNOWN, not a wording gap, and not automatically RECORD because it lives under an updater directory.

## Hand review

The following IDs were checked against original metadata and member tables for each scripted rule (all IDs where fewer than ten). All remaining rows were also matched to their original row and tested for the same predicate. The full per-row mapping is in the evidence index.

- live-firewall: `developer-0483d8313c7e79d98d978327`, `developer-0ca58f7e144d80e549c1f46e`, `developer-0ea638401e177c48cf413749`, `developer-1253d5a130cdaa34b5ca3536`, `developer-19a9801153a5a6aef2a4e4d6`, `developer-1a62b0867f27f523a8f95c35`, `developer-1e54809c7b95c6761dde8378`, `developer-1ef34b7917960d6a10b7fc78`, `developer-247454c44e1032f70f9fb187`, `developer-36157cc7f63180eafae0c7d1`.

- go-action-index: `developer-0e5ee95188114b28bd055b8d`.

- process: `developer-11ca06226251bb7f5eafa399`, `developer-ae0bce02c33762c6a56b10c2`, `developer-bd8228d5f97c8dee0503baa1`, `developer-c13e5b8a817caf485e06106f`, `developer-c21f181244c1042808b8b05a`, `developer-d9c2ff76e2ac3a590a6f37f7`, `gaming-0cb7818fab83e10338da62ab`, `gaming-0fc0effde8d7359f4fb826cc`, `gaming-29a0acc377b5db84054125f4`, `gaming-30f4c6b5d2db838496f3a00c`.

- loaded-module: `developer-14811ef3546842155799f6bf`, `developer-31c0f4039115f618fdff36d0`.

- volatile-group: `developer-149c70c5219b510072977722`, `developer-18ea5f4e221aa5f32280a00d`, `developer-193a71d04bb20ef1040b66b7`, `developer-213ce21036163379433b098b`, `developer-29e0e54310bc54f4bd737781`, `developer-836d0c42ef91dd70f6160bab`, `developer-846d4817df9ca86fc96c7f28`, `developer-85ad304e49b4adfb4947637d`, `developer-ad049be7fc84b4e2033c8217`, `developer-baa5c69d2f2f6fc6ad116568`.

- cache-structure: `developer-16415e37959f984fee21b60d`, `developer-46ca9bfe0e791e875df69c89`, `developer-539bb507dcc1804377569b44`, `developer-85370bd02a407aa5cd74a307`, `developer-a419b07b4143f33a89f73f20`, `developer-acdd0ff1bb96c8e4a4b12542`, `developer-d87e3f837a1ae9be300f8799`.

- reflog: `developer-226987a15b8a43af2eb8b4b9`, `developer-43a827e9fcd360a7f3a1998f`.

- rpc-pseudo: `developer-2fb915987929c6ab62914533`.

- live-timer: `developer-57de0524b6f8df2ca477e95a`, `gaming-05fa1da6777a4976051c47cd`.

- manifest-cache: `developer-5e8ac643acc6bacfdb91a5e2`, `developer-690f7a5c7cebae87fa1c36d2`, `developer-704817ab60b35f13c0e2005e`, `developer-75d811e4f3378831941acdba`, `developer-9ce9f539b5e490a54d1171a5`, `developer-a34d17b13459a78e47f7c118`, `developer-a4bc197697ae12a0c9a23f71`, `developer-a9ac2007a0541ca9027c2500`, `developer-b8d64740265cecd46cded211`.

- explicit-package: `developer-763fc6a0cbe95f3edf0f2342`, `developer-7a079508519a5bf9d2a34ff7`, `gaming-022e83da0853292b7b3b7dd4`, `gaming-0789731045c7fe02517c4efa`, `gaming-15f05a5d329a26af5ff02497`, `gaming-1a9ec40c717400c4f4a0a9ed`, `gaming-1ae2d58d2e725607780d97ca`, `gaming-1d2ee5bbf38be981ff3f32c6`, `gaming-2a851a15c4804d3e762f7086`, `gaming-34865e1874a15cbb0cf9f9fa`.

- dependency-package: `developer-8b01ef18afde74c7a799390e`, `gaming-2f1d6d4ca9d1b8351b2d4a03`.

- namespace: `developer-b18fbe731b7c03811a1b2eea`.

- open-port: `developer-c740f517bcde161990c1c168`.

- cups-hardlink: `gaming-0b9c75abae9461b0be7b041d`, `gaming-7b8b804e906bab4f5a36ccf2`.

- archive-unresolved: `gaming-4538cc406b1a701b2b46aa9a`.

- compiled-python: `gaming-55eab001092535e3e4aa0ea9`, `gaming-564fb794cbad0f9742f7ccd6`.

- execution-log: `gaming-63e2acee9dd1c09ce676ad5f`.
