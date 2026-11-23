# A3R adjudication: hole cards

Each card groups the adjudicated rows (`rows.tsv`, column `hole`) that fall into the same gap of
Sections 2–3 of `../../TEXT.md`. A group row counts in a card when at least one of its members falls into the gap. A row
that falls into several gaps is counted in one card only (the card in its `hole` column) and named in the others.

Totals: 2010 rows adjudicated, 621 HOLE rows, 8 cards.

## 1. Code caches

**Gap.** Some regenerable caches hold code that a program runs with its own rights: byte-compiled Emacs Lisp (.elc,
.eln), Python `__pycache__` files, Lua and JavaScript bytecode caches, zsh compiled dumps, and runnable scripts or
binaries inside download and module caches. The cache exemption says they need not be recorded and the code rule says
they must be, and no sentence says which prevails.

**Sentences.**
- S2.2-5: “cache: after it is removed, the computer does the same, only more slowly”
- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings”

**Examples.**
- `dd743d5660f8360b1a7dd17e` /home/user/.emacs.d/elpa/embark-consult-20260503.118 — Lisp sources with their .elc byte-compiled copies that Emacs loads.
- `lived-tcf3018d0d8` /home/user/.emacs.d/eln-cache/30.1-c7a97098 — native-compiled .eln trampolines that Emacs regenerates and loads as code.
- `8116f43e8ff91b41a1de6d2b` /home/user/.cache/nvim/luac — 310 Lua bytecode files of the editor configuration and plugins, run by the editor.
- `c7bc1fe807df7769d0fbb42e` /home/user/go/pkg/mod/golang.org/x/net@v0.48.0/internal/quic/cmd/interop/run_endpoint.sh — shell script inside the Go module download cache.
- `lived-te8aa6135e5` /home/user/.cargo/registry/src — Rust registry download cache that includes a runnable ELF test fixture.
- `00be4be3f78767b555ebdc00` (nvim state) — lazy.nvim's regenerable spec cache `pkg-cache.lua`, loaded as Lua.
- `29f17ad3cf7575804118ec06` /var/lib/flatpak/repo — repository objects hard-linked to deployed runtime files, including `__pycache__` files.

**Rows: 132.**

## 2. Compiler and build input

**Gap.** Source files of compiled languages (Java, Go, C#, Rust, C), type declarations (.d.ts, .pyi) and templates are
read and translated by a compiler or generator; they are neither executed as code nor only read as values. The text
classifies files only as executed code, values or content, and for these files the content exemption's property (only
the content itself becomes unavailable) and the removal test (building the program becomes impossible) give opposite
answers.

**Sentences.**
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting”
- S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

**Examples.**
- `7ab53c3d01fc5b25f6f43afb` /home/user/Projects/express/node_modules/hasha/node_modules/type-fest — npm package of TypeScript declarations, used only for type checking.
- `lived-t9bcd444add` /home/user/.vscode/extensions/ms-python.vscode-pylance-2026.4.1 — .pyi type stubs read by the Pylance type checker.
- `lived-t4a8c2cf574` /home/user/Projects/awesome-compose/sparkjava-mysql — Java application source compiled during the image build.
- `lived-t3a5e8c36ee` /home/user/Projects/awesome-compose/nginx-golang-postgres — Go backend source compiled into the service binary.
- `lived-tf9e8ae870c` /home/user/Projects/awesome-compose/aspnet-mssql — C# and Razor sources of a web application.
- `lived-tb1657f171f` /home/user/Projects/awesome-compose/spring-postgres — Java sources and a FreeMarker template.
- `lived-t88b40d452e` /home/user/.local/share/nvim — Rust sources of a plugin's native matcher, built on demand.

**Rows: 36.**

## 3. “In force only inside one program”

**Gap.** Many settings are read and applied by a single program, yet they decide what other programs or persons can do
on the computer: sshd options that S2.2-15 does not name, sshd host keys, a compose file that only compose reads but
that starts containers, PulseAudio defaults that govern the sound of every program, CUPS queues, mail aliases. Read as
“applied by one program”, the exemption gives NOT; read as “effect confined to one program”, the general rule gives
MUST, and the text does not say which reading holds.

**Sentences.**
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser”
- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-15: “accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be”

**Examples.**
- `5f8fcf77e7c5041de9f3e517` ssh-access:usepam — sshd option that enables PAM account and session checks for remote logins.
- `83bfbe2fd66f60bcc74b2389` ssh-access:allowtcpforwarding — sshd option that lets remote users open TCP tunnels.
- `73b70232c07e15bee2c93628` ssh-access:maxauthtries — sshd option limiting authentication attempts per connection.
- `ab310cbf841cfc3d22cb157b` /etc/ssh — host keys and sshd settings beyond those S2.2-15 names, read only by sshd.
- `lived-t5593bedbb3` /home/user/Projects/awesome-compose/apache-php — compose.yaml read only by compose, from which containers start.
- `041bcd50f0176118f1200688` /home/user/.config/pulse — default sink/source and volume databases of the sound server, applied to all programs.
- `a236c198c6522e6154ee71e9` /etc/cups — cupsd.conf and printers.conf, read only by cupsd, defining the print queues all programs use.
- `f291cc06cd1e8855bc44b998` /boot/efi/EFI/debian — BOOTX64.CSV, read only by the fallback loader, which creates firmware boot entries from it.
- `lived-t51cc65dbda` /home/user/.config/xfce4/xfconf — window-manager and notification daemon settings that govern all windows and notifications.

**Rows: 148** (85 of them are sshd options of kind `access-rule`).

## 4. Command strings in value files

**Gap.** Manifests such as `package.json` are read by a tool as values, but the tool passes some of those values (the
`scripts` field, a `postCreateCommand`, a launcher's `Exec` line, an ssh `ProxyCommand`) to a shell that executes them.
S2.2-13 sorts files into those a program executes as code and those it only reads as values, and such a file fits
neither clause; when only one program reads it, the code reading gives MUST and the setting reading gives NOT.

**Sentences.**
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting”
- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do”
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser”

**Examples.**
- `5f0c9a232213a85ce17b1a62` /home/user/.nvm/versions/node/v26.13.1/lib/node_modules/npm/node_modules/npm-bundled/package.json — manifest of one of npm's own bundled dependencies, with a `scripts` field.
- `f2384a93340393c000d0f294` /home/user/.nvm/versions/node/v26.13.1/lib/node_modules/npm/node_modules/debug/package.json — same kind, npm-internal dependency.
- `ab373871de57456ba9bdc8d5` /usr/share/code/resources/app/extensions/git/package.json — manifest of a built-in editor extension, with `scripts` and `main`.
- `87ad719c2a0813ce175c2a89` /usr/share/code/resources/app/extensions/prompt-basics/package.json — built-in extension manifest with a `scripts` field.
- `c04501ebe561207b22284ddb` /home/user/.nvm/versions/node/v26.13.1/lib/node_modules/npm/node_modules/spdx-exceptions — data package read only by npm whose manifest carries `scripts`.
- `54c86841fb0c34fd62a14f37` /home/user/.config/Thunar — custom actions, each a command line that only the file manager reads and launches.
- `56e2e00352bb36231b2da3cd` /home/user/.config/xfce4 — panel launchers whose `Exec` lines only the panel reads and runs.
- `e39ae1be47374abe25b3a90a` /home/user/.ssh — ssh client config whose `ProxyCommand` value ssh passes to the user's shell.

**Rows: 249** (240 of them are `package.json` files of kind `package-environment-evidence`).

## 5. Named cache or database that is not dispensable

**Gap.** Generated indexes that their documentation calls a cache or a database (the shared MIME-info database, the
udev hardware and device databases, gdk-pixbuf `loaders.cache`, GTK `immodules.cache`, `mimeinfo.cache`, the man-db
index, X11 font indexes) disable a function when removed, until they are regenerated. S2.2-4 and S2.2-5 exempt
caches and the contents of databases and state that their removal changes nothing, which is false for these objects,
while the removal test requires them; the text does not say whether the class name or the stated property decides.

**Sentences.**
- S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable”
- S2.2-5: “cache: after it is removed, the computer does the same, only more slowly”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

**Examples.**
- `1690bef9f5dd9343f83fb23d` /usr/lib/udev — compiled hardware database `hwdb.bin`; lookups for keymaps and quirks return nothing without it.
- `c6b3dd48abb80159fee9f231` /usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0 — `loaders.cache`; without it the image loaders are not found.
- `d58e9992edcefd52310ad71a` /usr/lib/x86_64-linux-gnu/gtk-3.0/3.0.0 — `immodules.cache`; without it GTK 3 sees no module input methods.
- `1ce57ed0757b9e9232133b56` /usr/share/applications — `mimeinfo.cache`; without it no MIME handlers are found.
- `a4de6292d1e78167decc7081` /usr/share/mime — the shared MIME-info database used for file-type detection.
- `4510afc64020ce965c69c93a` /var/cache/man — man-db index database caches; without `index.db`, apropos and whatis fail.
- `3c4a5ca44a8a5ebbd1c4566e` /run — `udev/data`, the udev device database; removal strips device properties and tags.
- `lived-t50ddcd97a8` /usr/share/fonts/X11 — generated X11 font indexes and alias maps.

**Rows: 49.**

## 6. Redundant copies

**Gap.** A locally added root certificate duplicates one that the trust store already holds. Removed alone it changes
nothing, so the removal test gives no MUST; yet the computer's behaviour (trusting that authority) depends on it as
much as on the other copy, and the text does not say how an object whose function another object duplicates is
decided.

**Sentences.**
- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

**Examples.**
- `f1dd4152b042e843dfb15c5c` /usr/local/share/ca-certificates — `isrg-root-x1-local.crt`, the same authority as the trusted ISRG Root X1.
- `4ea154d98eaad2618e7296f8` /etc/ssl/certs — `isrg-root-x1-local.pem`, for which no second hash link was made.
- `df8029550d37b2b3e98149c3` /usr/local — holds the same duplicate certificate.
- `df85b130531509e4f79cd4b1` /usr/local/share — holds the same duplicate certificate.
- `2f41a4b31ef3629ad27efa7b` /usr — holds the same duplicate certificate.

**Rows: 5** (all are the same certificate seen at different directory levels).

## 7. History stored as code

**Gap.** Some programs keep their history as code that they execute at start: Emacs writes `recentf` and `savehist`
as Lisp and loads them. Records of the past are exempt, code the program runs with its rights must be recorded, and
no sentence says which prevails.

**Sentences.**
- S2.2-6: “records of the past—logs, history”
- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do”

**Examples.**
- `99b8709d5a3af244262c5442` /home/user/.emacs.d/savefile — `recentf` and `savehist`, history files written as Lisp and executed by Emacs with `load`.
- Also present, but counted in card 1: `00be4be3f78767b555ebdc00` and `lived-tbba8c81784` — nvim session files, editor state that the editor executes with `:source`.

**Rows: 1** (plus the session files inside the two rows of card 1).

## 8. Documents that carry macros

**Gap.** An office document can embed a macro that the office suite runs with its own rights. Documents are content
and need not be recorded, code the program runs with its rights must be recorded, and no sentence says which
prevails.

**Sentences.**
- S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable”
- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do”

**Examples.**
- `fd76e7d51f3623288353a7c8` /home/user/Documents — `AndrewFontMacro.odt`, a document with an embedded Basic macro that builds a font sample.

**Rows: 1.**
