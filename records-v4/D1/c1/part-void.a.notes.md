# Part a classification notes

Scope: first 1,015 stored-group rows in source order. No other classification was consulted. All complete immediate member tables were read; each count was checked against its source row. Classification is of the listed immediate objects, not recursively of their descendants. A directory's execute bit is not evidence of executable code. Persistent FIFOs and state files were not called runtime merely because a service uses them.

The script is `part-void.a.build.py`. Detailed member assignments, including every MIXED row, are in `part-void.a.members.tsv`. Raw member paths are relative to the inventoried machine; its generic account home is abbreviated `~` in the sidecar. Every source member was joined by exact path against `D1/in/raw/void/package-files.tsv`: none has a matching retained manifest record. This absence does not establish that a member was not packaged. `metadata.json` explicitly records incomplete ownership. `configuration-origin.tsv` reports unknown creation and warns that mtimes and script mentions do not prove installation-time creation. Public documentation cannot recover installation integrity or the creator of these particular files.

## Rules and literal deciding sentences

S8.2-6: “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”

S8.2-7: “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”

S8.2-15: “Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.”

S8.2-5: “What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.”

S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”

1. **Unresolved provenance rule.** Persistent members with neither retained installation integrity nor independent evidence establishing a later question remain UNKNOWN. In particular, kernel module filenames and installed JavaScript/Python directory names do not prove unchanged receipt. The unknown fact changes the decision between INSTALLED-PACKAGE and the later questions or changes the recording line. A missing fact is not a textual gap. The script applies this only after the independently supported generated-record and runtime cases below are removed. Manual checks include native directories, Python support, JavaScript source, and kernel modules; all lack manifest matches. Prefix hashes establish current bytes only.
2. **Pip cache rule.** The pip-created HTTP cache, wheel cache, cache metadata, and containing cache directories are RECORD under S8.2-15. They are cached downloads/build outputs, not installed packages. The action log confirms pip downloaded the corresponding dependencies and saved its built wheel. A wheel cached before installation is not a package installed on the computer; its archive is not executed in this representation.
3. **Npm cache rule.** The content-addressed `_cacache`, indexes, cache bookkeeping, directories, and diagnostic log are RECORD under S8.2-15. These objects store request data and operational bookkeeping; installed `node_modules` content was kept outside this rule.
4. **Runtime rule.** Members explicitly marked runtime in the retained filesystem facts are RUNTIME under S8.2-5. Parent program and its decision are retained per member. For a heterogeneous collection of runtime producers, the main row points to the exact member mapping. Program integrity was checked in the package-file table. When the creator program or its integrity is unavailable, the parent's decision remains UNKNOWN; that does not change the child's established runtime status. A top-level runtime filesystem directory belongs to its filesystem setting, whose origin/default status is UNKNOWN.
5. **Browser operational storage rule.** Profile grouping databases, telemetry records, and browser database storage are RECORD under S8.2-15. Their filesystem persistence is known. Extension packages, preferences files, and script/startup caches are excluded: their execution/access behavior or provenance may affect earlier questions. Cache-like names alone are not a universal exemption.

## Individually examined cases

- `void-d261da4b189f658f590c655e`: both named network profiles are newly added by the network action, as recorded at the end of `D1/in/control/void/actions-logs/actions-logs/network_connection.log`; S8.2-11–13 and S8.2-17 give SETTING-OWN. The initial configuration-origin uncertainty is resolved for these exact additions by the independent action output.
- `void-d65c2d748a2f1ba5116779ae` and `void-53cafa8dbfe1164feacdbb6e`: the `run` file has a shebang, but its installation origin is unavailable. `supervise` is runsv-created state storage, giving MIXED UNKNOWN/RECORD.
- `void-d58f3b966b9109316ccd7cf2` and `void-9cb770a06c308eb3a6e23f52`: all six members are persistent runsv status/control objects, hence RECORD, including persistent FIFO names.
- Root group: only `run` and `tmp` have runtime persistence; every other listed member has unresolved persistent provenance, hence MIXED.
- The generic home script has a shebang, but the retained `home_script.log` contains no command text. A success status does not establish its source. It remains UNKNOWN rather than assuming unpackaged origin.
- Kernel modules from the older kernel and its directories have no retained package integrity records. A filename indicating a version does not establish whether a corresponding installed package owns the current bytes.
- Browser startup script caches and downloaded extension archives are not assigned RECORD from the word “cache” or MATERIAL from their location alone.

## Public documentation used

- https://pip.pypa.io/en/stable/topics/caching/ — “This cache functions like a web browser cache.” The page describes request-response caching and locally built wheel caching.
- https://docs.npmjs.com/cli/v11/commands/npm-cache/ — “npm stores cache data in an opaque directory within the configured `cache`, named `_cacache`.” It identifies this as content-addressed HTTP/package request storage.
- https://smarden.org/runit/runsv.8 — “runsv maintains status information in a binary format” and “The named pipes service/supervise/control”. These distinguish state/control storage from executable `run` scripts.
- https://www.freedesktop.org/software/systemd/man/latest/udev.html — “All device information udev processes is stored in the udev database”. The observed udev data and link indexes have runtime persistence; the eudev binary is unchanged in its package.
- https://firefox-source-docs.mozilla.org/toolkit/components/telemetry/data/common-ping.html — “This defines the top-level structure of a Telemetry ping.” It describes profile identifiers and recorded measurement payloads.
- https://firefox-source-docs.mozilla.org/networking/cache2/doc.html — “Provides access to a cached entry data and meta data for reading or writing or in some cases both”. This documents storage semantics without proving arbitrary cache payloads cannot execute.
- https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html — “This file is automatically maintained by fontconfig.” This identifies font caches, but the mixed symlink/tag members retain unresolved provenance rather than extrapolating a uniform decision.

Section 8.5's storage/removal policies, authority, declaration format, and enforcement mechanism were not treated as classification gaps.

## Manual rule checks

The following complete member lists were examined by hand, alongside their type/persistence and package joins.

Unresolved provenance: void-8d280df3af0a49f9d0604694, void-5f368f02dd6cd06d3f5ffaca, void-d14cab53b503072e3e41a163, void-c914dd2221e357409a570bfb, void-a99e2797d84ce334a9a54ae0, void-9e81bdf0f8994a6654991825, void-d27ebd7b8ebda674ca25d5df, void-ae68189b03d85e13c1870e35, void-3a8fe7255eeb87df56bbbb14, void-2117150e804586582c619aca.

Pip cache: void-bd1f76eddac5dde5a00e9325, void-056fb0c3034a3e56f1b0980e, void-7cdd21cd61a18aad050ba6b5, void-d9d57ebd050950d8355e6776, void-74154aad0825f21dfd6c99e2, void-c3274f07f17199b3b9a3c9a4, void-9fd039663ae7be1646dd6a5e, void-86a3f41b36b65a78c1517b32, void-20218371bb598bc7e27e9ae2, void-bf8067d56569d78a7803c1fc.

Npm cache: void-bc13ff3324748093e99236b5, void-b277449d35d56b94b5eb4278, void-fa03afc88f745c8be8cce5a2, void-940335dcaa0097585a3d192a, void-a43dd6b78828a56a2956a000, void-7a894cc04341a5be8e8c9752, void-c8a63205fa13f422bc6d9e44, void-3615361f7907da704d3b0eaa, void-35459a2dee9fe3ee971b6bd3, void-6609f741e8ac4caef770c58d.

Runtime: void-0da88c4d8aba9a240255361e, void-4b55bcc9e08c6f275b3b966b, void-4e6d569fe712286fd7ee683d, void-bcbb885908a9755acc09d6a4, void-028d211554c326f462917c13, void-abfa0f41a6863adfe72fa1dc, void-8161dc9f02d85252b5046bb5, void-8960bee536f0573a29fb6374, void-8e80dca3afccf8c2a8e3caf8, void-49775aef4613432a2da26395.

Browser operational storage: void-a04c9e7c7c7a15fae5d245e4, void-5bf923f1c068f4c3d8b2dc8c, void-7a9c50985072d69592cf194c, void-2fcfcf64177d428c0781d7fe, void-bfcbb5dd620628099370a778, void-31a378de5659c65b31ffeb42, void-a81041576d472abaf664847d, void-61cbdc75372f732e8d045a01, void-858606b8d2ba7d5e6004fcae, void-62bd1360300577cbf830c920.

