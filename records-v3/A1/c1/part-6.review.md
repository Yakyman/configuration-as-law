# Review of the current c1 part 6 draft

Scope: the current `part-6.tsv`, `part-6.3.tsv`, their notes, and the corresponding rows of `../in/part-6.tsv`, under Sections 2 and 3 of the fixed text. The unavailable raw directories were not searched elsewhere.

## Concrete findings

### R1 — four executed shell scripts (resolved during review)

IDs: `debian-desktop-fb87e8bdd4`, `debian-desktop-09fa2e5ce3`, `debian-desktop-2438267eef`, `debian-desktop-d54b59c426`.

The earlier UNKNOWN decisions overlooked evidence elsewhere in the same input part. User-unit rows `debian-desktop-53d095e912`, `debian-desktop-fdb6cb41a8`, `debian-desktop-ba3d3e02a2`, and `debian-desktop-7218a536a4` explicitly show `bash` executing the respective stored paths. The application-specific purpose and file contents are unnecessary once unrestricted interpreter execution is established. The current draft has corrected all four to MUST with basis `evidence` under S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”

### R2 — `debian-desktop-5deb3892cc` (resolved during review)

Earlier: MUST. Corrected: UNKNOWN, S3-2.

The input establishes only that `/etc/environment` exists. Documentation establishes what effective assignments in that file can do, but neither the input nor the cited evidence supplies its contents. An empty, comment-only, or otherwise ineffective file would not have the claimed removal consequence, so “Sets environment variables inherited by login sessions” is not established for this object. S3-2: “If what the object does remains unknown, the case yields ?.”

### R3 — `debian-desktop-4cce813fe8` (resolved during review)

Earlier: MUST. Corrected: UNKNOWN, S3-2.

The input supplies only the `/etc/fstab` path. The cited format documentation does not establish that this particular file contains an effective filesystem entry. Empty, comment-only, or default-equivalent contents remain possible, so the claimed loss of specified mounting behavior is unsupported by the saved evidence.

### R4 — `debian-desktop-868a743843` (resolved during review)

Earlier: MUST. Corrected: UNKNOWN, S3-2.

The input supplies only the `/etc/papersize` path and no selected value. The documentation establishes the format and possible shared effect, not this object's effective value or whether removal changes the selected default. The removal consequence required by S2.2-2 is therefore unestablished.

### R5 — `freebsd-4cce813fe8` (resolved during review)

Earlier: MUST. Corrected: UNKNOWN, S3-2.

As with R3, the input supplies only the `/etc/fstab` path. The cited format documentation establishes possible entries and their effects, but no effective entry in this particular file. The earlier claim that removing “these definitions” changes system capabilities presupposed definitions that the evidence does not show.

## Checked interpretations without a concrete correction

- The `*.device`, `*.mount`, `*.scope`, and `*.slice` group decisions depend on how the inventoried runtime unit objects are treated. Type documentation establishes their general roles, but not every member-specific dependency or setting. The current MUST readings are arguable from the active unit roles, so this review does not count them as concrete errors.
- `debian-desktop-809cb439ce` remains defensibly UNKNOWN: sampled manual-page links are NOT, but the sampled alternatives-directory executable link alone does not establish its generic-name consumer or a lost capability after removal.
- `freebsd-72a7d6a331` is correctly MUST: the supplied `set number` command is executed as an editor command, so S2.2-13 gives code precedence over the one-program setting exemption.
- `freebsd-83dfca210b` is correctly NOT: the supplied `minfree` value is read as a setting used only by `savecore`, rather than executed as code.
