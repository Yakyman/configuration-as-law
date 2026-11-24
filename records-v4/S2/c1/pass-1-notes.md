# Pass 1: scope and evidence

The 105 entries were considered before the meaning answers. The numbered entries in the preparation table specify individual decisions; no inferred classifier was run over the dossier. `pass-1.tsv` preserves the six text-decision columns. `pass-1.sha256` fixes those bytes before pass 2. The final table must preserve those columns exactly.

Evidence references of the form (not published: record outside selected evidence) use the physical line number, including the header. The original table has one physical line per fact. No referenced underlying inventory, earlier classification, other party's folder, or adjudication was opened. Public documentation below supplies program behavior, never historical instance facts.

The requirement to record an object is distinct from whether the inventory already contains a designated declaration. Lack of a historical designation alone was not used to make every observed object unknown. Likewise, a missing person's identity or exact timestamp is not automatically decisive. Unknown delivery integrity, human selection, executable contents, or input closure is decisive where its possible values change the ordered decision. A known template or generator is not proof of an unknown historical transaction.

S8.2-3: "The rule applies to objects that are on the computer." The channel objects in families 13–15 have explicitly unknown observed presence. A described operation or object type was not promoted to a historical object instance. Their pass-1 rows therefore remain UNKNOWN even where conditional classification of the described type would be straightforward. Additional missing facts are named where useful.

S8.2-6: "What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order."

S8.2-7: "Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?"

The two installed add-ons are whole installation/removal units, not merely unidentified parts of a different unit. The unchanged-content condition attaches to the second branch of S8.2-7. Unknown extension permissions do not defeat the first branch or let S8.2-21 move ahead of question one. This does not infer any missing manifest, installed version, or full-file digest.

S8.2-15: "Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines."

For the six project-history groups, both program recording and personal bringing through a requested clone fit the stated facts. The text does not say that personal bringing must be direct or that program recording must be autonomous. Both alternatives require no declaration line. The four Homebrew-history groups encounter the earlier question about installed-package provenance and unknown unchangedness; their rows do not assume that question away.

For the four Docker images, the unresolved reading concerns whether pulling and removing an application image is installation/removal of a program under S8.1-4 and S8.1-6, or management of stored templates whose contents are separately executed. Calling an image a package in Docker's documentation does not itself choose the hypothesis's meaning of installer. For the persisted container ID, the competing units are the managed installation and the saved service configuration. The dossier distinguishes its persistent representation from the workload process. No confinement capability was inferred from the image or container ID.

For the Git sample hook, complete-byte equality and the copying mechanism are established. The unresolved issue is whether "obtained as part" follows the unchanged bytes into the later copy, or whether the new copy proceeds to question two and the derivation clause. The row does not treat equality alone as proof of copying; the separate producer fact supplies that evidence.

S8.2-23: "A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code."

For the family-12 groups, the known command-bearing member supplies the gap: instructions or embedded command text can be treated as code, or the containing file can be treated as parsed values selecting a later command. The boundary between file and extracted command is not specified. A gap in one member prevents a definite group decision; it does not assert that all other immediate members have the same kind. For the cron group, both readings require its own line. For the two larger project groups, `undetermined` does not mean nothing needs recording.

Directory groups retain their listed immediate-child scope. An unresolved member does not become a definite second category merely to produce MIXED. The two unexpanded engine-store directories were not substituted with guessed descendant inventories.

## Public program documentation

Consulted on 2026-11-23 UTC. Quotations below are short evidence excerpts; conclusions about the hypothesis remain those of c1.

- Firefox add-on installation/removal: <https://firefox-source-docs.mozilla.org/python/marionette_driver.html>. "Install a Firefox addon, which can be used right away." "Uninstall a Firefox addon." The API takes the XPI path and returns an add-on ID; removal takes that ID. Applies to family 5.
- Git clone: <https://git-scm.com/docs/git-clone>. "Clones a repository into a newly created directory". The description also documents creation of remote-tracking references. Applies to family 7.
- Homebrew installation: <https://docs.brew.sh/Installation>. "The script installs Homebrew to its default prefix". Its Git-remote section documents repository fetching during installation. Applies to the four Homebrew-history groups; it supplies no historical digest comparison.
- Docker image acquisition: <https://docs.docker.com/reference/cli/docker/image/pull/>. "Download an image from a registry". Applies to family 8.
- Docker image removal: <https://docs.docker.com/reference/cli/docker/image/rm/>. "Removes (and un-tags) one or more images from the host node." Applies to family 8.
- Docker image/container distinction: <https://docs.docker.com/learn/content/what-is-a-container/>. "An image is a package of everything a container needs to start". Its explanation distinguishes stored image layers, the container process, and a writable layer. Applies to family 8.
- Git templates: <https://git-scm.com/docs/git-init>. "The sample hooks are all disabled by default." Its template section documents copying template files into the new repository. Applies to `developer-3bcbeded8b7cf5aedc1382fb`; dossier facts establish the actual complete-byte match.
- Dockerfile CMD: <https://docs.docker.com/reference/dockerfile/#cmd>. "The CMD instruction sets the command to be executed when running a container from an image." The reference distinguishes a build-time RUN from the saved CMD. Applies to `developer-d916e8927ebf41371ab8dd1d`.
- Lefthook run: <https://lefthook.dev/configuration/run/>. "specifies the actual command to be run using the sh shell." Applies to `developer-e56b4f802a20335d455ecb3a`.
- Cron file format: <https://manpages.debian.org/trixie/cron/crontab.5.en.html>. "A crontab file contains instructions". Its description explains scheduled commands and the shell used for them. Applies to `server-c354536d6d9a738329571706`.
