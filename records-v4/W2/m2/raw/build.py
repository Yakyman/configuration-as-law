#!/usr/bin/env python3
"""Builds W2/m2/objects.tsv from the decisions below; checks every quote against SENTENCES.md."""
import csv, pathlib, re, sys

root = pathlib.Path(sys.argv[1])
sent = {}
for line in (root / "SENTENCES.md").read_text().splitlines():
    m = re.match(r"- \*\*(S8\.\d-\d+)\*\* (.*)$", line)
    if m:
        sent[m.group(1)] = m.group(2)

Q15a = "if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state"
Q15b = "if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files"
Q2 = "The rest need not be recorded."
Q14 = "A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program."
Q23 = "A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code."
Q9 = "Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?"
Q11 = "Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?"
Q4i = "a program of the system whose purpose, according to its documentation, includes installing and removing programs"
Q6 = "in a system that is installed and updated as an image, the image is a package."
Q22 = "A program that runs as its own process on the computer, including in a container, is a program."
Q16 = "What is installed is recorded by one of three lines: a line of its own"
Q17 = "A setting is recorded by a line of its own"
Q8_2_6 = "the first affirmative answer decides"

quotes_by_id = {"S8.2-15": [Q15a, Q15b], "S8.2-2": [Q2], "S8.2-14": [Q14], "S8.2-23": [Q23],
                "S8.2-9": [Q9], "S8.2-11": [Q11], "S8.1-4": [Q4i], "S8.1-6": [Q6], "S8.2-22": [Q22],
                "S8.2-16": [Q16], "S8.2-17": [Q17], "S8.2-6": [Q8_2_6]}
for sid, qs in quotes_by_id.items():
    for q in qs:
        assert q in sent[sid], (sid, q)

G1_DEC = ("what it is: two ways. Q1 no (git is not an installer by S8.1-4); Q2 no (packed history and git bookkeeping "
          "are read by git as data, S8.2-23); Q3 no (not a value the computer as a whole obeys). Q4 fits both branches: "
          "git recorded it as it ran (program record: history, working state) and the person brought it by cloning "
          "(material: projects, downloaded files); S8.2-15 gives no precedence. Whether recorded: not required on "
          "either branch (S8.2-2)")
G1_MEAN = "no: fetched history and git's own bookkeeping of a person's project are neither installed nor a setting of the computer"
G1_ACH = "yes: nothing has to be recorded, so no action of Section 9.2 is restricted"
G1_REF_NOTE = (" Refs hold values obeyed only by git, which the person runs for himself; S8.2-14 would call them 'a record "
               "of that program', but S8.2-11 (chosen by a person) is not met and they were fetched, so Q4 is still reached "
               "with both branches; the recording answer (no) is the same.")
EV = "A3/in/raw/developer/members/{}.tsv; action developer_public_project (C1/actions/lived-developer.sh: git clone --depth 1)."

rows = []
def g1(oid, extra=""):
    rows.append(["G1", oid, "two-ways", "S8.2-15; S8.2-2",
                 Q15a + " | " + Q15b + " | " + Q2, G1_DEC, G1_MEAN, G1_ACH,
                 EV.format(oid.split("-", 1)[1]) + extra])

g1("developer-53425eb85c9fbc80fd72ef81")  # .git/objects
g1("developer-6939a0c70bd7e159e638d411", " Members: pack-*.pack, .idx, .rev (mode 0444, not executable).")
g1("developer-b33a49ff4891eb30d52c7e46", G1_REF_NOTE)
rows.append(["G1", "developer-79f8aad1cf16d03db17b4621", "two-ways", "S8.2-15; S8.2-2; S8.2-14",
             Q15a + " | " + Q15b + " | " + Q14,
             G1_DEC + ". Member config: values obeyed only by git; S8.2-14 makes it a setting only if it launches "
             "something or grants access (content not in inventory, 268 bytes; FACT_UNKNOWN whether it sets a hook path)",
             "no for the history and bookkeeping; the executable hook under hooks/ (written by lefthook install) is a "
             "separate code object and is not answered here",
             G1_ACH,
             EV.format("79f8aad1cf16d03db17b4621") + " 11 members: HEAD, config, description, hooks/, index, info/, "
             "logs/, objects/, packed-refs, refs/, shallow. Hooks are listed as separate code objects in "
             "A3/in/raw/developer/objects.tsv; https://git-scm.com/docs/githooks: 'Hooks are programs you can place in "
             "a hooks directory to trigger actions at certain points in git’s execution.'"])
g1("developer-2cd27841286438a33a7be083", " Member refs/heads/master (41 bytes)." + G1_REF_NOTE)
g1("developer-e6a1511f1247825437884782", G1_REF_NOTE)
g1("developer-3f398d23eb0fcf553dff5b42", " Member refs/remotes/origin/HEAD (32 bytes)." + G1_REF_NOTE)

G2_DEC_DOCKER = ("docker.xml / docker-forwarding.xml: Q1 no (not in the firewalld package file list; created at docker "
                 "service start, not during installation, so S8.2-17's package-default clause does not apply); Q2 no "
                 "(XML read as values, S8.2-23); Q3 no: the value was chosen by the docker daemon, not by a person; Q4: a "
                 "program recorded it as it ran -> program record, need not be recorded (S8.2-2). S8.2-13 lists access "
                 "rules among settings, but it is the consequence of an affirmative Q3, and S8.2-6 makes the order decide")
G2_MEAN_DOCKER = ("yes, covered by another line: the line of the docker package with its enabled service, which "
                  "creates this zone/policy whenever it starts with firewalld")
G2_ACH = "yes: the system regenerates them from the recorded docker line; installing, enabling and running containers stay allowed"
DOCKER_DOC = ("https://docs.docker.com/engine/network/packet-filtering-firewalls/: 'Docker creates a `firewalld` zone "
              "called `docker`, with target `ACCEPT`.' and 'Docker also creates a forwarding policy called "
              "`docker-forwarding`'. mtime 2026-11-23T11:15:00Z coincides with 'systemctl enable --now docker' in "
              "developer_container; A3/in/raw/developer/raw/0017-package-files-rpm.out lists only the directories "
              "under firewalld@2.5.2-1.fc45.")
rows.append(["G2", "developer-70be1c323890746c1a78c6f5", "yes", "S8.2-11; S8.2-15; S8.2-6",
             Q11 + " | " + Q15a + " | " + Q8_2_6, G2_DEC_DOCKER, G2_MEAN_DOCKER, G2_ACH,
             "Member: docker-forwarding.xml (A3/in/raw/developer/members/70be1c323890746c1a78c6f5.tsv). " + DOCKER_DOC])
rows.append(["G2", "developer-24c8232c52212725d6ea3882", "yes", "S8.2-11; S8.2-15; S8.2-6",
             Q11 + " | " + Q15a + " | " + Q8_2_6,
             G2_DEC_DOCKER + ". FedoraWorkstation.xml and .xml.old date from the base installation "
             "(2026-11-22T04:40Z, identical in developer-base); who wrote them is not in the inventory "
             "(configuration-origin.tsv: created=unknown): FACT_UNKNOWN (person's choice -> setting, own line; package "
             "installation script -> package line; program as it ran -> program record)",
             G2_MEAN_DOCKER + "; the FedoraWorkstation zone copy is an access rule in force: yes, by its own line or by "
             "the line of whatever installed it (creator not in inventory)",
             G2_ACH,
             "Members: FedoraWorkstation.xml, FedoraWorkstation.xml.old, docker.xml "
             "(A3/in/raw/developer/members/24c8232c52212725d6ea3882.tsv; base: "
             "A3/in/raw/developer-base/members/48e6b9cdd90db629c057a32c.tsv). " + DOCKER_DOC])

rows.append(["G3", "server-c354536d6d9a738329571706", "two-ways", "S8.2-9; S8.2-23; S8.2-11; S8.2-17; S8.2-16",
             Q9 + " | " + Q23 + " | " + Q11 + " | " + Q17 + " | " + Q16,
             "what it is: two ways. cron reads the file's schedule and user fields as values and hands the command "
             "field to /bin/sh, which executes it with root rights: the file is neither one 'a program executes as code' "
             "nor one a program 'only reads as values', so S8.2-23 decides nothing and Q2 has no single answer; if code "
             "-> program (Q2), else a value chosen by a person that the system scheduler obeys -> setting (Q3). Whether "
             "and by which line: the same on both branches, a line of its own (program not built from anything recorded, "
             "S8.2-16; setting, S8.2-17)",
             "yes, by a line of its own: a system-wide scheduled job chosen by a person",
             "yes: the job is written from its declaration line; adding a system cron job is not an ordinary action of Section 9.2",
             "Member /etc/cron.d/cal-maintenance (A3/in/raw/server/members/c354536d6d9a738329571706.tsv), written by "
             "server_scheduled_jobs (C1/actions/lived-server.sh): '17 * * * * root /usr/bin/date -u >> "
             "/var/log/cal-maintenance.log'."])

rows.append(["G3", "developer-e56b4f802a20335d455ecb3a", "two-ways", "S8.2-23; S8.2-9; S8.2-14; S8.2-15",
             Q23 + " | " + Q9 + " | " + Q14 + " | " + Q15b,
             "mixed group. Decided by the text: test-all.sh and the built scc binary are code the computer can execute "
             "-> programs, line of their own (S8.2-9/S8.2-16); plain sources and documents -> material. Not decided: the "
             "value files whose entries are commands (lefthook.yml 'run: git diff --cached --check', Dockerfile, "
             ".goreleaser.yml): the tools read them as values and pass entries to a shell, so neither branch of "
             "S8.2-23 fits; program (Q2) or, if not code, a value of a self-run program that launches something -> "
             "setting (S8.2-14), or, for files no program here obeys, material (S8.2-15, projects, downloaded files): "
             "what it is and whether it is recorded both have more than one answer",
             "no as a whole: a fetched project with its own build, hook and CI files and its build output is the person's "
             "material; the hook installed into .git/hooks is a separate object",
             "yes: nothing in the project tree has to be recorded, so no action of Section 9.2 is restricted",
             "42 members (A3/in/raw/developer/members/e56b4f802a20335d455ecb3a.tsv) incl. .cal-modcache, .git, "
             ".github, .devcontainer, vendor, lefthook.yml, Dockerfile, .goreleaser.yml, scc (executable), test-all.sh "
             "(executable); actions developer_public_project and developer_git_hooks (C1/actions/lived-developer.sh)."])

rows.append(["G3", "developer-d916e8927ebf41371ab8dd1d", "two-ways", "S8.2-23; S8.2-9; S8.2-14; S8.2-15",
             Q23 + " | " + Q9 + " | " + Q14 + " | " + Q15b,
             "index.html: created by the person, not executed here -> material (S8.2-15). Dockerfile: docker build "
             "carries out its instructions (FROM, COPY) and stores CMD, which later starts httpd in the container; it is "
             "neither a file 'a program executes as code' nor one 'only read as values', so S8.2-23 decides nothing: "
             "program (Q2, own line), setting of a self-run program that launches something (S8.2-14, own line) or "
             "project material (S8.2-15, not recorded): what it is and whether it is recorded have more than one answer",
             "no: the project files are the person's material; what they produced (the image and the running container) "
             "is what the declaration must describe",
             "yes: nothing has to be recorded for these files, so no action of Section 9.2 is restricted",
             "Members Dockerfile, index.html (A3/in/raw/developer/members/d916e8927ebf41371ab8dd1d.tsv), written by "
             "developer_container (C1/actions/lived-developer.sh)."])

G4_DEC = ("what it is: two ways. Q1 holds only if docker is an installer, i.e. if its documentation states a purpose "
          "of installing and removing programs (S8.1-4); the documentation calls an image 'a package of everything a "
          "container needs to start' but does not describe docker as installing programs, and S8.1-6's image clause "
          "concerns a system installed as an image, not a container image: Q1 has no single answer. If Q1 yes -> "
          "installed object; if no -> Q2: code the computer executes in a container -> program (S8.2-9, S8.2-22). "
          "Whether and by which line: the same on both branches, a line of its own (S8.2-16), since no declaration line "
          "built or obtained it")
G4_MEAN = "yes, covered by another line: the line declaring the container (on the server, the compose stack) that names this image"
G4_ACH = ("yes: running a container stays allowed if the container tool adds the container and its image to the "
          "declaration, as P4 already requires of installation tools")
G4_DOC = (" https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/: 'An image is a package of "
          "everything a container needs to start'; https://docs.docker.com/compose/: 'Docker Compose is a tool for "
          "defining and running multi-container applications.'")
QG4 = Q4i + " | " + Q6 + " | " + Q9 + " | " + Q22 + " | " + Q16
rows.append(["G4", "developer-78e8326714450972e0134fb6", "two-ways", "S8.1-4; S8.1-6; S8.2-9; S8.2-22; S8.2-16", QG4,
             G4_DEC + ". This image was built locally by 'docker build' from the person's Dockerfile, not obtained by any line",
             "yes, covered by another line: the line declaring the container cal-development-web, which names the image "
             "and its build recipe",
             G4_ACH,
             "cal-development-web:local, Containers=1 (A3/in/raw/developer/raw/0296-docker-image.out); developer_container "
             "runs it with --restart unless-stopped." + G4_DOC])
for oid, nm in [("server-fc8e0ac75ce9ed64a08ff655", "caddy:2-alpine"), ("server-46f5ba6815bb94894157236c", "postgres:17-alpine"),
                ("server-bce2d2fe9dfb24c822a93809", "traefik/whoami:v1.11.0")]:
    rows.append(["G4", oid, "two-ways", "S8.1-4; S8.1-6; S8.2-9; S8.2-22; S8.2-16", QG4,
                 G4_DEC + ". Pulled by docker compose for the cal-server stack",
                 G4_MEAN, G4_ACH,
                 nm + ", Containers=1 (A3/in/raw/server/raw/0085-docker-image.out); server_compose "
                 "(C1/actions/lived-server.sh) compose.yaml." + G4_DOC])

header = ["gap", "id", "decided", "sentence", "quote", "decision", "meaning_answer", "achievable", "note"]
for r in rows:
    assert len(r) == len(header)
    for c in r:
        assert "\t" not in c and "\n" not in c
out = root / "W2/m2/objects.tsv"
with out.open("w", newline="") as f:
    w = csv.writer(f, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar=None, lineterminator="\n")
    w.writerow(header)
    w.writerows(rows)
# every object of OBJECTS.tsv covered exactly once
with (root / "W2/OBJECTS.tsv").open() as f:
    ids = [r["id"] for r in csv.DictReader(f, delimiter="\t")]
assert sorted(ids) == sorted(r[1] for r in rows), "object set mismatch"
(root / "W2/m2/DONE").write_text(f"{len(rows)}\n")
print(len(rows), sum(r[2] == "yes" for r in rows))
