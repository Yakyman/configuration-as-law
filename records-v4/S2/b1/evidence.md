# Evidence for the two answers

These are independent answers by meaning under PROTOCOL.md Section 2, not adjudication decisions or assigned gap weights.

## cups

A3/in/raw/gaming/members/0b9c75abae9461b0be7b041d.tsv lists the six backends. (not published: over 20 MB) shows that each has the same device and inode as its corresponding backend-available file; mdns shares dnssd's inode. (not published: over 20 MB) identifies those backend-available files as unchanged contents of package 6ff4bb862fc7c9a79185e240 (cups).

A3/in/raw/gaming/raw/0456-metadata-read-384.out contains the base64-encoded /var/lib/dpkg/info/cups.postinst. Decoded lines 51–64 create these hard links, including:

```sh
ln /usr/lib/cups/backend-available/$module /usr/lib/cups/backend/$module
ln /usr/lib/cups/backend/dnssd /usr/lib/cups/backend/mdns
```

The package line can describe these installed components without requiring a separate line for each hard link. Recording the package installation imposes no prohibition on the ordinary actions in TEXT.md Section 9.2.

## steam

A3/in/operator/gaming/actions-logs/actions-logs/gaming_store_runtime.log names the exact sampled archives at lines 146, 162, and 167 and queues them for downloading. Lines 536–539 report “Extracting package...” and “Update complete, launching...”. The matching archived files remain present in (not published: over 20 MB) and in the sampled inventory rows.

By meaning, these retained compressed installation downloads are cache objects, distinct from the extracted installed resources and libraries. Their executable permission bits do not themselves make compressed archives running programs. Leaving these cache objects outside the required declaration does not prohibit any listed ordinary action; the installed client and components can still be recorded.

## k3s

A3/in/operator/server/actions-logs/server_orchestrator.log records downloading and verifying release v1.37.2+k3s1, installing /usr/local/bin/k3s, and enabling and starting its service. (not published: direct evidence at least 2 MB) records the three sampled executable files in the same versioned data directory. A3/in/raw/server/level-1.tsv also records processes executing the sampled bin/k3s path.

The official [K3s initialization description](https://docs.k3s.io/blog/2025/03/25/K3s-initialization), sections “The Embedded Powerhouse” and “The Boot Sequence, Step-by-Step”, states: “The embedded binaries are always deployed in the same directory: `/var/lib/rancher/k3s/data`.” It also states: “At this point, K3s will extract the binaries.”

Together the installation log, inventory locations, and documented extraction establish the basis for treating these as components supplied by the K3s installation. The coverage answer means a declaration line specifying that installation and its bundled executables. Recording this installation can permit extraction, service operation, and container execution. It requires no prohibition of an ordinary action in TEXT.md Section 9.2. This is an existence answer about a system meeting the requirement, not a claim that the inventoried system enforces it.
