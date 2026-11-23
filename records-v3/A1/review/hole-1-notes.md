# Hole 1: revised literal review and whole-table extent

The initial refutation in `cards.md` chose an effect-only meaning of the phrase in force only inside one program. The definition does not choose between the location of applying a setting and the scope of its consequences, so that refutation is withdrawn. The setting files covered here are parsed by one program but determine other processes, system resources, or shared operating behaviour. S2.2-13 identifies them as settings without resolving the scope of S2.2-7, and S2.2-2 supplies the competing must-record result. This is a missing boundary, expressed as the collision of the exemption and the removal rule, not a proposed textual amendment.

S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”

## Enumeration and object boundaries

`build-hole-1-extent.py` traverses every row of `../compare/joined.tsv`. `hole-1-scan.tsv` records the kind/name and scope disposition of all 5200 rows; `hole-1-extent.tsv` gives individual qualifications and evidence for candidate/excluded rows. The original 97 anchors were examined rather than used as the search boundary. Kind/name searches covered configuration paths, native unit definitions, store configuration outputs, and configuration-only package components; descriptive function searches covered settings without a conventional .conf suffix, including CA selectors, locale lists, PAM entries and filesystem specifications.

Stored native unit files are configuration objects. Their ExecStart value identifies a separate executable with arguments; the unit file itself is parsed as key/value settings. Conversely separately inventoried unit-script outputs, Scheme service definitions and sourced shell files are executing code. The official [service documentation](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html) describes the service file as configuration of another process; [timer](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html), [target](https://www.freedesktop.org/software/systemd/man/latest/systemd.target.html) and [mount](https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html) documentation establish activation, dependency and mount-value roles. The file-backed system-unit/user-unit rows themselves identify a fragment path and classify removal of that definition, so they are included as definition objects. An inactive unit is not automatically incapable of being started. Known false assertions and absence of required programs are separately excluded on the adjudication facts.

Actual port/firewall/login/right objects are decided by S2.2-15, but a manager unit starting a related service is a different settings object. A socket unit name alone does not distinguish a network port from a Unix, FIFO or device endpoint; those 72 candidates remain factual unknown rather than being excluded by name. Unit inventory groups without per-member fragment provenance remain factual unknowns; synthesized device/scope state does not establish a setting-file example. Program packages containing executable programs are not silently recounted as configuration-only components. Mixed directory/tree rows are labelled CONFIRMED-CONSTITUENT: the count identifies rows containing a hole instance, not a claim that every member or whole-directory deletion is ambiguous.

## Counts and limits

Confirmed row coverage: 721 (683 standalone definitions, 38 constituent-containing groups). Factual unknown candidates: 158; multiple-reader exclusions: 5; known-fact exclusions: 15; runtime-state exclusions: 15.

The confirmed rows are exact listed memberships, but not an assertion that the remaining factual unknown candidates are outside the hole. The inventory does not establish their active values, single reader, exact removal effect, or whether a grouped unit has a persistent fragment. Consequently the total possible extent is bounded by the saved evidence; reporting the confirmed count as a fully settled universal extent would overstate it.

Original anchors were also audited for the single-reader premise: nix.conf CLI/daemon use, two preset outputs, three skeleton groups and the kernel-image file remain unknown; the three NixOS sysctl.d store outputs have both systemd-sysctl and procps sysctl readers and are excluded. Individual qualifications remain in the TSV. No classification sample was changed, no new machine/object was introduced, and no experiment was performed.

The final boundary pass also includes native file-backed system-unit and user-unit rows (not only store outputs), ssh_config client settings and known manager enablement/linger selectors. For client settings the external effect is connection choice; no clause explicitly records those client options. For enablement selectors the effect is activation of another process. Mixed SSH groups still have an overall MUST constituent for server login/port rules; inclusion here records the unresolved client constituent.

The installed procps evidence is in `../in/raw/nixos/system-closure.txt` and `../in/raw/coreos/packages.tsv`. The upstream [sysctl manual](https://man7.org/linux/man-pages/man8/sysctl.8.html) documents --system reading sysctl.d files; thus their one-reader premise fails where both tools are installed. The Guix sysctl file is not excluded on this basis: the Guix system uses procps directly rather than a second systemd-sysctl reader. No fact about additional reader installation on another system is inferred merely by analogy.

The agreed-sample candidate coreos-160df5d64d (nftables-services) is retained as factual unknown: filenames alone do not establish the firewall-rule contents or exact manager-setting constituents. After the final state/reader corrections, confirmed coverage is 721 rows.

Final accuracy correction: nine exact generated/transient /run fragment rows listed in `final-boundaries.md` are excluded as state under S2.5-1; the /run/current-system persistent-profile path is not included in that exclusion. Ubuntu sysctl.d row ubuntu-7ab5b73f41 is factual unknown because an additional reader is unproved, rather than proved absent. No additional cases were introduced.
