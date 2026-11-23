# RPM repair details for collector documentation

The RPM file query now also reads FILEMODES and FILELINKTOS. Directory records
remain ownership evidence but are not packaged-file integrity denominators.
The installed symlink target is compared with RPM's recorded target; an observed
replacement by another file type is changed. Unobserved paths are not declared
missing merely because the filesystem walk did not contain them.

The digest parser accepts only an algorithm-appropriate hexadecimal digest.
An absent or zero FILEDIGESTALGO uses RPM's documented legacy MD5 default;
unsupported algorithms and missing digest records remain unknown.

Primary source: https://rpm.org/docs/latest/manual/tags.html — FILEMODES is
“Unix file mode”; FILELINKTOS is “Symlink target for symlink files”. The same
page documents the missing FILEDIGESTALGO default as MD5.

DNF's own reason records are retained. Group and external reasons remain
unknown rather than being recoded as explicitly selected or dependency:
https://dnf.readthedocs.io/en/latest/command_ref.html .

A proposed DNF `--userinstalled` fallback was investigated, not applied.
The command reference says its history equivalent includes packages selected
through groups/module profiles and outside DNF. Current upstream source,
`dnf/db/history.py::user_installed`, instead accepts USER or UNKNOWN and
explicitly calls the latter a likelihood judgment about installation via RPM.
`dnf/cli/commands/repoquery.py` uses that predicate. Therefore the query does
not provide a source-supported way to turn all stored GROUP reasons into
known explicit installation facts. Sources are recorded in `PLAN.md`.

The following failures have diagnosed limitations rather than presumed absence:
user Flatpak scopes that cannot access their configured repository; a queried
user manager without session bus/runtime environment; missing OpenRC and
Docker interfaces on the machine. Each affected query retains its nonzero
status and stderr; these scopes are reported as not collected.

The filesystem error was diagnosed on the next fresh round as an inaccessible
runtime document-portal mount (`diagnostics/fx2/filesystem-live.stderr`).
Primary documentation describes the portal as a virtual FUSE filesystem:
https://flatpak.github.io/xdg-desktop-portal/docs/documents-and-fuse.html .
The documented mount is the user runtime `doc` directory; original host paths
are available through its documented xattr, not inferred from its children:
https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.Documents.html .
Any opaque handling must identify the virtual alias limitation and retain the
underlying stored namespace; permission denial is not an empty directory.

## Positive selected-group linkage repair

The new `collector/rpm-selected-groups.py` reads persisted DNF4 group/environment
transaction records through libdnf. It accepts only a current, successful,
nonremoved group selected with native reason USER, or a current environment
selected with USER whose saved installed-group list contains the group. It
then reads only group members with installed=true. The complete selection
linkage is retained as additional provenance, while native GROUP remains
reason=unknown. A selected group does not establish individual historical
package selection. Group/external/absent reasons remain unknown. The adapter
does not infer individual selection from
the current repository's group definitions or from an absence in a list.

Sources (read before implementation):
- https://raw.githubusercontent.com/rpm-software-management/libdnf/master/libdnf/transaction/CompsGroupItem.cpp — resolves latest successful group transaction, rejects removed groups, loads installed package membership.
- https://raw.githubusercontent.com/rpm-software-management/libdnf/master/libdnf/transaction/CompsEnvironmentItem.cpp — corresponding persisted environment and installed-group records.
- https://raw.githubusercontent.com/rpm-software-management/libdnf/master/libdnf/transaction/CompsEnvironmentItem.hpp — getGroups, getInstalled, getGroupId.
- https://raw.githubusercontent.com/rpm-software-management/libdnf/master/libdnf/transaction/TransactionItem.hpp — getReason on each transaction item.
- https://raw.githubusercontent.com/rpm-software-management/dnf/master/dnf/db/group.py — native access to history group records.

DNF4 requires its own installed Python/libdnf bindings. A missing history
interface or interpreter remains a query failure; no package is installed by
the collector. DNF5 and zypp do not receive a guessed DNF4 history conversion.
