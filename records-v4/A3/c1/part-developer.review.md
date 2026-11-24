# Review of the developer classification

The current partial output has two bounded issues. This follow-up supersedes the earlier review text.

## 1. Go build-cache groups containing regular `-d` entries need UNKNOWN

`developer-96805d38cf622a0b45a638f4` is representative. Its complete member table contains several regular `-d` files but records only modes, sizes and prefix hashes. The Go cache implementation identifies executable cache outputs by making the `-d` output path a directory, so these observed regular files are not those executable entries. Even so, the supplied evidence does not identify their exact payloads or exclude every form of execution through another program. S8.2-9 includes execution through another program, and S8.2-20 requires the fact that code cannot execute on this computer. The conservative result for groups containing regular `-d` files is therefore UNKNOWN pending content/type evidence.

This does not invalidate every Go cache RECORD. `developer-8e4741c8990fe035b816f7bf`, `developer-0e5ee95188114b28bd055b8d`, and `developer-5bd472ce02d9a509e8a327b3` contain only `-a` metadata entries and may remain RECORD; the cache-root group may also remain RECORD. Group decisions must follow their actual member composition.

## 2. The libvirt runtime creator mapping is overbroad

`developer-df39a529b53c474304339913` attributes the whole runtime group to `libvirtd`. Its complete member table instead contains separately named sockets for `virtinterfaced`, `virtlockd`, `virtlogd`, `virtnetworkd`, `virtnodedevd`, `virtnwfilterd`, `virtqemud`, `virtsecretd`, and `virtstoraged`, as well as generic libvirt sockets. The inventory also records the legacy `libvirtd.service` as inactive. A single `libvirtd` creator and creator decision are therefore not supported for this mixed group; creators must be assigned per member or retained as UNKNOWN. The final object decision can remain RUNTIME under S8.2-5.

`developer-bc2eff9fbcd1c8ce543692ad` is specifically the QEMU runtime subtree but is also mapped to `libvirtd`; its members include `driver.pid` and `autostarted`, while the inventory separately identifies `virtqemud` and its installed executable. The recorded creator should be `virtqemud` if that relation is established, otherwise UNKNOWN.

The prior objections to `developer-130507d632cdd51fdf840931`, `developer-6c65e1a3bddb9b836b534f27`, and runtime rows with an UNKNOWN creator are withdrawn. S8.2-5 permits the immediate creating program, and when every possible creator decision leaves the child runtime-only, RUNTIME remains the final decision.

## 3. The three project-summary SETTING-OWN results lack provenance

`developer-5eb44d0def12c43daae1fbb3`, `developer-525ed7742d9bd835216a4b96`, and `developer-da97ea3d424d9e95f97e9301` are settings because they enable or define launched work, but the evidence does not establish own-line coverage. `configuration-origin.tsv` records `created=unknown` for both unit files, with no maintainer-script or installation-log evidence. Their containing groups `developer-8eec9396036ab3dbdc3aa47b`, `developer-8bb75545e63903670ff45fac`, and `developer-59ca32b77b0915ebed0e500f` are already UNKNOWN for installation-default versus later-configuration provenance, and the launched script is independently UNKNOWN. A custom name and user configuration location do not prove that a package or installer did not create the default. Under S8.2-17, package-default coverage versus a line of its own is FACT_UNKNOWN, so all three level-one rows should be UNKNOWN.

## 4. The cached `ruff` distribution is not merely a RECORD row

`developer-d1fbc4bd76f69c08a8b6ecf7` is an input package row for a Python distribution with `reason=unknown`. Its package-file evidence includes adjacent `ruff` Python modules, a distribution script with unknown integrity, and distribution metadata; the stored groups for the adjacent payload are also UNKNOWN. The current result reinterprets the whole distribution row as only cached metadata based on its location. That skips the ordered package question and ignores the adjacent executable payload represented by the same package identifier. Cache location alone does not establish that the distribution is only a program record rather than an installer-managed package or package source. The correct result is UNKNOWN under S8.2-6, S8.2-7, S8.2-9 and S8.2-16.
