# Primary source excerpts

Checked 2026-11-23 UTC. These excerpts support the directly linked documentation in CHANNELS-V4.tsv. Classification and coverage are deductions from the fixed text, not assertions made by the tool manuals. No virtual machines, builds, installations, or runtime probes were used.

Paths containing $HOME, <profile>, <prefix>, <path>, or similar parameters are documented path templates, not paths of the host. Optional artifacts are identified conditionally. The table does not assert that every possible cache, history entry, or script-created output appears in every invocation.

The original first-column names and the explicit custom-dispatch premise come from the authorized previous CHANNELS.md. Its version-3 verdicts are not evidence for the present decisions. The parent directory preserves the original drafting evidence and classification. This directory contains the FX-B1-1 revision; ../RESULT.md is the current summary. E100-E105 below supply the newly checked primary excerpts.

S8 sentence IDs refer to SENTENCES.md. B1-9.3-command, B1-9.3-channel, B1-9.3-stream, and B1-A.4.3-removal are local labels for the exact imported passages in TEXT.md; they are not new numbered hypothesis sentences. Quoting P4 follows the published label of the property called C4 in the task.

## E001 — R01 — Python command line

[R01 — Python command line](https://docs.python.org/3/using/cmdline.html)

> When called with a file name argument or with a file as standard input, it reads and executes a script from that file.

Execution modes: script, -c, standard input and interactive input. No installation purpose is documented for these modes.

## E002 — R02 — Python exec

[R02 — Python exec](https://docs.python.org/3/library/functions.html)

> This function supports dynamic execution of Python code.

exec/eval consume source strings or code objects; a read file can become code.

## E003 — R03 — Bash reference manual, maintainer copy

[R03 — Bash reference manual, maintainer copy](https://tiswww.case.edu/php/chet/bash/bashref.html)

> Process substitution allows a process’s input or output to be referred to using a filename.

Sections 3.5.6, 3.6, 4.1 and 9.1 document pipes/descriptors, redirections, dot/source, and history. These are shell execution functions, not installation.

## E004 — R04 — Python modules

[R04 — Python modules](https://docs.python.org/3/tutorial/modules.html)

> Python caches the compiled version of each module in the __pycache__ directory under the name module.version.pyc

A module is source code; a compiled-only module can be loaded without its source. Directly run main scripts are not saved as bytecode by this mechanism.

## E005 — R05 — Python interactive history

[R05 — Python interactive history](https://docs.python.org/3/tutorial/interactive.html)

> The default configuration also saves your history into a file named .python_history in your user directory.

The history is reused by subsequent interactive sessions. FX-B1-1 applies S8.2-23 to this documented values-reading role and records its tension with the execution-capability reading of S8.2-9; syntax is not used to decide that textual dispute.

## E006 — R06 — zipimport

[R06 — zipimport](https://docs.python.org/3/library/zipimport.html)

> This module adds the ability to import Python modules (*.py, *.pyc) and packages from ZIP-format archives.

Code members in an archive can execute without extracting the archive into a conventional install location.

## E007 — R07 — Git hooks

[R07 — Git hooks](https://git-scm.com/docs/githooks)

> Hooks are programs you can place in a hooks directory to trigger actions at certain points in git’s execution.

Default directory is $GIT_DIR/hooks; core.hooksPath can select another location. Executable hook files are invoked by Git.

## E008 — R08 — Dynamic loader

[R08 — Dynamic loader](https://man7.org/linux/man-pages/man8/ld.so.8.html)

> ld.so, ld-linux.so - dynamic linker/loader

Documents direct /lib/ld-linux.so.* invocation, LD_PRELOAD, LD_AUDIT, LD_LIBRARY_PATH and /etc/ld.so.preload. These load executable libraries; they do not install them.

## E009 — R09 — memfd_create

[R09 — memfd_create](https://man7.org/linux/man-pages/man2/memfd_create.2.html)

> However, unlike a regular file, it lives in RAM and has a volatile backing storage.

The anonymous file persists until all references are dropped; /proc/self/fd/N exposes its descriptor, not a durable file.

## E010 — R10 — mmap

[R10 — mmap](https://man7.org/linux/man-pages/man2/mmap.2.html)

> mmap() creates a new mapping in the virtual address space of the calling process.

MAP_ANONYMOUS and executable protection flags describe memory execution; a file-backed mapping and its backing file are different objects.

## E011 — R11 — Debugger memory assignments

[R11 — Debugger memory assignments](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Assignment.html)

> To store values into arbitrary places in memory, use the

Assignments can change the debugged process at a supplied address. They do not by themselves rewrite the executable on disk.

## E012 — R12 — Kernel binary format handlers

[R12 — Kernel binary format handlers](https://docs.kernel.org/admin-guide/binfmt-misc.html)

> Binfmt_misc can also recognise a filename extension aka .com or .exe.

The registration string is written to /proc/sys/fs/binfmt_misc/register; a named entry appears in that directory and selects an interpreter.

## E013 — R13 — Browser sandbox

[R13 — Browser sandbox](https://chromium.googlesource.com/chromium/src/+/main/docs/design/sandbox.md)

> Sandbox leverages the OS-provided security to allow code execution that cannot make persistent changes to the computer

This documents inability to make persistent changes. FX-B1-1 applies the express web-page example in S8.2-21 to the confined web code already specified by C7.19. It does not require a new capability fact for that example; separate renderer/helper executables still require recording.

## E014 — R14 — Wasmtime command line

[R14 — Wasmtime command line](https://docs.wasmtime.dev/cli-options.html)

> The run command will execute a WebAssembly module.

The documented wasmtime --dir . foo.wasm invocation grants a host directory; compilation and instantiation occur in the runtime.

## E015 — R15 — Wasmtime filesystem security

[R15 — Wasmtime filesystem security](https://docs.wasmtime.dev/security.html)

> applications can only access files and directories they’ve been given access to.

A preopen is a capability boundary, not evidence of its particular read/write permissions or the contents of that directory. The CLI implementation cited separately fixes its WASI permission to ReadWrite; effective host permissions and reachable content remain unspecified.

## E016 — R16 — WASI context preopens

[R16 — WASI context preopens](https://docs.wasmtime.dev/api/wasmtime_wasi/struct.WasiCtxBuilder.html)

> Configures a “preopened directory” to be available to WebAssembly.

The documented API accepts FsPerms::ReadWrite or FsPerms::ReadOnly. These have different consequences for ability to change installed executable files.

## E017 — R17 — Socket interface

[R17 — Socket interface](https://docs.python.org/3/library/socket.html)

> Bind the socket to address. The socket must not already be bound.

bind/listen create a runtime listener; getsockname reports its selected port. No persistent service registration is implied.

## E018 — R18 — Pickle

[R18 — Pickle](https://docs.python.org/3/library/pickle.html)

> It is possible to construct malicious pickle data which will execute arbitrary code during unpickling.

The code-bearing serialized input in the variant is distinct from an ordinary non-executing data serialization.

## E019 — R19 — Persistent binary format rules

[R19 — Persistent binary format rules](https://www.freedesktop.org/software/systemd/man/latest/binfmt.d.html)

> binfmt.d — Configure additional binary formats for executables at boot

/etc/binfmt.d/*.conf is local policy; /usr/lib/binfmt.d/*.conf is the packaged counterpart. systemd-binfmt registers rules at boot.

## E020 — R20 — dlopen

[R20 — dlopen](https://man7.org/linux/man-pages/man3/dlopen.3.html)

> The function dlopen() loads the dynamic shared object

The path names a shared library; dependencies can also be loaded. It returns a process-local handle.

## E021 — R21 — execve

[R21 — execve](https://man7.org/linux/man-pages/man2/execve.2.html)

> execve() executes the program referred to by path.

The path may be an executable binary or a shebang script. The operation replaces the process image, not the named source file.

## E022 — R22 — OSTree deployments

[R22 — OSTree deployments](https://ostreedev.github.io/ostree/deployment/)

> A deployment is physically located at a path of the form /ostree/deploy/$stateroot/deploy/$checksum.

The deployment layer installs operating systems. Staged deployments, the repository /ostree/repo and boot entries are concrete examples of artifacts, not proof that any M row chose this backend.

## E023 — R23 — fsync

[R23 — fsync](https://man7.org/linux/man-pages/man2/fsync.2.html)

> fsync, fdatasync - synchronize a file's in-core state with storage device

File and directory persistence are separate calls; this primitive names no application-success report or declaration.

## E024 — R24 — unlink

[R24 — unlink](https://man7.org/linux/man-pages/man2/unlink.2.html)

> If the name was the last link to a file but any processes still have the file open

Open references can retain the inode after pathname removal. unlink does not terminate the processes using it.

## E025 — R25 — Service manager control

[R25 — Service manager control](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html)

> systemctl — Control the systemd system and service manager

enable/disable manipulate links; start/stop affect runtime state. This is configuration functionality, including when invoked by a shell.

## E026 — R26 — Service units

[R26 — Service units](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html)

> A unit configuration file whose name ends in ".service" encodes information about a process controlled and supervised by systemd.

Restart policies and activation dependencies can recreate processes. They do not show which configuration a generic M row changes.

## E027 — R27 — Embedded interpreter

[R27 — Embedded interpreter](https://docs.python.org/3/extending/embedding.html)

> you can pass a string containing Python statements to PyRun_SimpleString()

The embedding interface also accepts a file through PyRun_SimpleFile; embedded execution does not itself install or remove programs.

## E028 — R28 — Descriptor execution

[R28 — Descriptor execution](https://man7.org/linux/man-pages/man2/execveat.2.html)

> If path is an empty string and the AT_EMPTY_PATH flag is specified

A descriptor can name the executable instead of a pathname. This interface also supports the implementation of fexecve.

## E029 — unit

[unit](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html)

> A unit file is a plain text ini-style file

## E030 — run

[run](https://www.freedesktop.org/software/systemd/man/latest/systemd-run.html)

> Sets a property on the scope or service unit that is created.

## E031 — gen

[gen](https://www.freedesktop.org/software/systemd/man/latest/systemd.generator.html)

> Their main purpose is to convert configuration and execution context parameters

## E032 — envgen

[envgen](https://www.freedesktop.org/software/systemd/man/latest/systemd.environment-generator.html)

> Environment generators can override the environment that the manager exports to services and other processes.

## E033 — cron

[cron](https://raw.githubusercontent.com/cronie-crond/cronie/master/man/crontab.5)

> a directory for storing crontabs defined by users.

## E034 — crontool

[crontool](https://raw.githubusercontent.com/cronie-crond/cronie/master/man/crontab.1)

> maintains crontab files for individual users

## E035 — kill

[kill](https://www.freedesktop.org/software/systemd/man/latest/systemd.kill.html)

> If set to `process`, only the main process itself is killed

## E036 — login

[login](https://www.freedesktop.org/software/systemd/man/latest/loginctl.html)

> Control the systemd login manager

## E037 — bash

[bash](https://www.gnu.org/software/bash/manual/bash.html)

> Functions may be exported so that child shell processes

## E038 — bashstart

[bashstart](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files)

> uses the expanded value as the name of a file to read and execute.

## E039 — emacspkg

[emacspkg](https://raw.githubusercontent.com/emacs-mirror/emacs/master/doc/emacs/package.texi)

> If the package under point is already installed, this command will delete it.

## E040 — emacsinit

[emacsinit](https://raw.githubusercontent.com/emacs-mirror/emacs/master/doc/emacs/custom.texi)

> ;; eval: (eldoc-mode)

## E041 — git

[git](https://git-scm.com/docs/git-config)

> If the alias expansion is prefixed with an exclamation point, it will be treated as a shell command.

## E042 — addon

[addon](https://support.mozilla.org/en-US/kb/find-and-install-add-ons-add-features-to-firefox)

> Extensions add new features to Firefox or modify existing ones.

## E043 — profile

[profile](https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data?mobile=0)

> All of the changes you make in Firefox

## E044 — pref

[pref](https://support.mozilla.org/en-US/kb/firefox-support-troubleshooting-guide?mobile=0)

> This file stores all user preferences

## E045 — podman

[podman](https://docs.podman.io/en/latest/markdown/podman.1.html)

> Most Podman commands can be run as a regular user, without requiring additional privileges.

## E046 — podrun

[podrun](https://docs.podman.io/en/latest/markdown/podman-run.1.html)

> Run a process in a new container.

## E047 — pull

[pull](https://docs.podman.io/en/latest/markdown/podman-pull.1.html)

> podman pull copies an image from a registry onto the local machine.

## E048 — build

[build](https://docs.podman.io/en/latest/markdown/podman-build.1.html)

> podman build Builds an image using instructions from one or more Containerfiles or Dockerfiles and a specified build context directory.

## E049 — commit

[commit](https://docs.podman.io/en/latest/markdown/podman-commit.1.html)

> podman commit creates an image based on a changed container.

## E050 — load

[load](https://docs.podman.io/en/latest/markdown/podman-load.1.html)

> podman load loads a saved image(s) into local container storage

## E051 — restart

[restart](https://docs.podman.io/en/latest/markdown/podman-restart.1.html)

> The restart command allows containers to be restarted using their ID or name.

## E052 — dpkg

[dpkg](https://manpages.debian.org/trixie/dpkg/dpkg.1.en.html)

> dpkg is a medium-level tool to install, build, remove and manage Debian packages.

## E053 — user

[user](https://man7.org/linux/man-pages/man8/useradd.8.html)

> create a new user or update default new user information

## E054 — nm

[nm](https://networkmanager.dev/docs/api/latest/nmcli.html)

> nmcli is a command-line tool for controlling NetworkManager and reporting network status.

## E055 — key

[key](https://networkmanager.dev/docs/api/latest/nm-settings-keyfile.html)

> NetworkManager is based on the concept of connection profiles that contain network configuration

## E056 — nft

[nft](https://netfilter.org/projects/nftables/manpage.html)

> Administration tool of the nftables framework for packet filtering and classification

## E057 — rpm

[rpm](https://rpm.org/docs/6.0.x/manual/spec.html)

> Spec files describe how software is build and packaged.

## E058 — runc

[runc](https://github.com/opencontainers/runc/blob/main/man/runc.8.md)

> runc - Open Container Initiative runtime

## E059 — exec

[exec](https://docs.podman.io/en/latest/markdown/podman-exec.1.html)

> podman exec executes a command in a running container.

## E060 — rm

[rm](https://docs.podman.io/en/latest/markdown/podman-rm.1.html)

> This does not remove images.

## E061 — execpolicy

[execpolicy](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html)

> Execution environment configuration

## E062 — pacman

[pacman](https://man.archlinux.org/man/pacman.8.en)

> Remove package(s) from the system.

## E063 — pacconf

[pacconf](https://man.archlinux.org/man/pacman.conf.5.en)

> The default is /var/cache/pacman/pkg/.

## E064 — hooks

[hooks](https://man.archlinux.org/man/alpm-hooks.5.en)

> Hooks may be disabled

## E065 — pip

[pip](https://pip.pypa.io/en/stable/cli/pip_install/)

> Install packages into <dir>.

## E066 — pipmeta

[pipmeta](https://packaging.python.org/en/latest/specifications/recording-installed-packages/)

> This directory is named as `{name}-{version}.dist-info`

## E067 — pipcache

[pipcache](https://pip.pypa.io/en/stable/topics/caching/)

> Pip provides an on-by-default caching, designed to reduce the amount of time spent on duplicate downloads and builds.

## E068 — editable

[editable](https://pip.pypa.io/en/stable/topics/local-project-installs/)

> Editable installs allow you to install your project without copying any files.

## E069 — build

[build](https://pip.pypa.io/en/stable/reference/build-system/)

> Generate a wheel for the package.

## E070 — npm

[npm](https://docs.npmjs.com/cli/v11/configuring-npm/folders/)

> so that they may be found by npm scripts when necessary.

## E071 — npmuninstall

[npmuninstall](https://docs.npmjs.com/cli/v11/commands/npm-uninstall/)

> This uninstalls a package, completely removing everything npm installed on its behalf.

## E072 — npmlink

[npmlink](https://docs.npmjs.com/cli/v11/commands/npm-link/)

> Package linking is a two-step process.

## E073 — npmscripts

[npmscripts](https://docs.npmjs.com/cli/v11/using-npm/scripts/)

> Does NOT run in global mode

## E074 — site

[site](https://docs.python.org/3/library/site.html)

> Both files can exist in one of the four directories mentioned above.

## E075 — flatpak

[flatpak](https://docs.flatpak.org/en/latest/flatpak-command-reference.html)

> The application overrides are saved in text files residing in $XDG_DATA_HOME/flatpak/overrides in user mode.

## E076 — flatinside

[flatinside](https://docs.flatpak.org/en/latest/under-the-hood.html)

> With Flatpak, each application, runtime and extension is a branch in a repository.

## E077 — appimage

[appimage](https://docs.appimage.org/user-guide/run-appimages.html)

> The AppImage is unmounted when the application called in the example is interrupted

## E078 — appupdate

[appupdate](https://docs.appimage.org/packaging-guide/optional/updates.html)

> Via an updater tool built into the AppImage itself

## E079 — curl

[curl](https://curl.se/docs/manpage.html)

> Write output to the given file instead of stdout.

## E080 — chmod

[chmod](https://man.archlinux.org/man/chmod.1.en)

> chmod - change file mode bits

## E081 — bash

[bash](https://man.archlinux.org/man/bash.1.en)

> Bash is a command language interpreter that executes commands read from the standard input, from a string, or from a file.

## E082 — tar

[tar](https://man.archlinux.org/man/tar.1.en)

> tar - an archiving utility

## E083 — gcc

[gcc](https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html)

> linking combines all the object files

## E084 — plugin

[plugin](https://gcc.gnu.org/onlinedocs/gccint/Plugins.html)

> GCC plugins are loadable modules that provide extra features to the compiler.

## E085 — cmake

[cmake](https://cmake.org/cmake/help/latest/command/install.html)

> This command generates installation rules for a project.

## E086 — cmakerun

[cmakerun](https://cmake.org/cmake/help/latest/command/try_run.html)

> Try compiling and then running some code.

## E087 — Homepage behavior

[Homepage behavior](https://support.mozilla.org/en-US/kb/how-to-set-the-home-page)

> The Firefox homepage is the first page you see when you open Firefox

The same page documents opening the selected page with the Home button and in a new window. This establishes navigation, not a definition of the hypothesis's phrase launching something.

## E088 — CLI directory permissions

[CLI directory permissions](https://raw.githubusercontent.com/bytecodealliance/wasmtime/main/src/common.rs)

> builder.preopened_dir(host, guest, wasmtime_wasi::FsPerms::ReadWrite)?;

The documented CLI --dir option is configured with read/write WASI permissions. The API's separate read-only option is not evidence that this CLI invocation chooses read-only. Effective host filesystem permissions, accessible contents and module behavior are separate facts.

## E089 — Embedded debugger execution

[Embedded debugger execution](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Python-Commands.html)

> The python command can be used to evaluate Python code.

The source command can read a .py script; imported modules may create .pyc files depending on configuration.

## E090 — Database function code

[Database function code](https://www.postgresql.org/docs/current/plpython-funcs.html)

> The body of a function is simply a Python script.

The documentation shows CREATE FUNCTION with a retained function body, rather than only a transient command argument.

## E091 — AWK execution

[AWK execution](https://man.archlinux.org/man/gawk.1.en)

> Read the AWK program source from the file program-file

The -f and -e interfaces select saved source and command-argument source respectively; they are not package installation interfaces.

## E092 — pip removal purpose

[pip removal purpose](https://pip.pypa.io/en/stable/cli/pip_uninstall/)

> pip is able to uninstall most installed packages.

Together with pip install, this establishes the installing-and-removing purpose required by S8.1-4.

## E093 — Compiler purpose

[Compiler purpose](https://gcc.gnu.org/onlinedocs/gcc/G_002b_002b-and-GCC.html)

> GCC is an integrated distribution of compilers for several major programming languages.

The output-options manual documents compilation and executable output. Applying S8.1-7 through the Q2 output definition is one reading, not an adopted resolution. The alternative is general-purpose build work under S8.1-8; see GAPS.md. No installer/removal purpose is inferred.

## E094 — Build and installation purpose

[Build and installation purpose](https://cmake.org/cmake/help/latest/manual/cmake.1.html)

> CMake provides a command-line signature to install an already-generated project binary tree:

The Description identifies a build-system generator and Install a Project documents cmake --install. This supports the built-in reading, especially for C5.3. The competing reading treats output copying/linking as the functionality expressly excluded by S8.1-8, whose exception requires an installer. No removal purpose is established. Both readings are retained in GAPS.md.

## E095 — Direct imports from some wheels

[Direct imports from some wheels](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)

> a subset of wheel files do support being placed directly on `sys.path`.

The direct-import FAQ and zipimport documentation distinguish executable archive members from non-loadable archives. A cache label alone does not establish Q4. The actual retained wheel contents are unspecified in C2.1, C2.3 and C2.5.

## E096 — Serialized executable-code cache

[Serialized executable-code cache](https://v8.dev/blog/improved-code-caching)

> Chrome stores the serialized generated code onto the disk cache and keys it with the URL of the script resource.

Background explains later deserialization and reuse instead of recompilation, subject to compatibility checks. Cache presence depends on policy and eligibility; a single channel invocation does not guarantee a new entry.

## E097 — Browser code-cache root

[Browser code-cache root](https://chromium.googlesource.com/chromium/src/+/main/content/browser/storage_partition_impl.cc)

> code_cache_path = settings.path().AppendASCII("Code Cache");

The branch uses this path only for an enabled, non-memory cache. Partition settings supply the cache root.

## E098 — Browser code-cache subdirectories

[Browser code-cache subdirectories](https://chromium.googlesource.com/chromium/src/+/main/content/browser/code_cache/generated_code_cache_context.cc)

> base::FilePath generated_js_code_cache_path = path.AppendASCII("js");

The same initialization code names pc for the newer persistent collection backend; it can remove the older js cache. These are alternative layouts, not two entries asserted for every run.

## E099 — Extension registration database

[Extension registration database](https://raw.githubusercontent.com/mozilla-firefox/firefox/main/toolkit/mozapps/extensions/internal/XPIDatabase.sys.mjs)

> const FILE_JSON_DB = "extensions.json";

PROP_JSON_FIELDS includes userDisabled; toJSON serializes these fields, setUserDisabled updates activation state, and database property updates save the JSON database in the profile. Generated state is distinguished from the installed extension bundle.

## FX-B1-1 evidence additions

Checked 2026-11-23 UTC. These are documentation checks, not runtime observations. Existing quoted excerpts above are preserved; the interpretation notes for E005, E013, E093 and E094 are corrected. The original notes remain in ../SOURCES.md.

## E100 — User transient-unit location

[systemd.unit, Unit File Load Path, user-mode table](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html#Unit%20File%20Load%20Path)

> $XDG_RUNTIME_DIR/systemd/transient

> Dynamic configuration for transient units

These are the path and description in the same user-mode table row. They directly support C6.3 object a, rather than relying on the generic unit-file description in E029.

## E101 — Container privilege, namespace and device options

[podman-run option reference](https://docs.podman.io/en/latest/markdown/podman-run.1.html)

The option headings and their relevant descriptions are:

> --privileged
>
> Give extended privileges to this container.

> --pid=mode
>
> host: use the host’s PID namespace for the container.

> --device=host-device[:container-device][:permissions]
>
> Add a host device to the container.

C9.5 object a names these selected values. Their existence and semantics are documented; no claim is made that running the command itself creates a new hook JSON file.

## E102 — Hook JSON and conditional directory default

[podman, --hooks-dir](https://docs.podman.io/en/latest/markdown/podman.1.html#hooks-dir-path)

> Each `*.json` file in the path configures a hook for Podman containers.

Relevant condition and directory fragments:

> If `--hooks-dir` is unset for root callers

> `/usr/share/containers/oci/hooks.d` and `/etc/containers/oci/hooks.d`

The documentation calls these defaults deprecated and recommends explicitly selecting the directory. C9.5 now states the root-caller/unset-option condition, with <hooks-dir>/*.json as the general template. This evidence establishes the configuration location, not the identity, provenance or effects of an unspecified hook executable; FACT_UNKNOWN therefore remains.

## E103 — System mount utility and filesystem configuration

[mount(8), Name, bind options, Availability](https://man7.org/linux/man-pages/man8/mount.8.html)

> mount - mount a filesystem

> The mount command is part of the util-linux package

> Since util-linux 2.27 mount permits changing the mount options

This documents the named utility's system-utility provenance and filesystem-configuration purpose for C3.5. S8.2-13 explicitly includes filesystems among settings; S8.1-7 applies to this functionality. It supplies no evidence about the AppImage updater's identity or status as a program of the system. E078 remains only a generic update-mode description, so the updater route is FACT_UNKNOWN in C3.5 and C4.3.

## E104 — Download purpose

[curl, Description](https://curl.se/docs/manpage.html#DESCRIPTION)

> curl is a tool for transferring data from or to a server using URLs.

Together with E079's output-file option, this establishes a transfer function. It does not establish the installation/configuration purpose in S8.1-7. C4.3 no longer claims S8.1-8 explicitly lists downloading. Copying is still one of that sentence's explicit examples.

## E105 — Shell history is read into a history list

[Bash reference manual, History Builtins, history -r](https://tiswww.case.edu/php/chet/bash/bashref.html#Bash-History-Builtins)

> Read the history file and append its contents to the history list.

The Bash Variables and Bash History Facilities sections identify HISTFILE and saving/reloading entries. This supports the values-reading role in C7.17. The same manual separately documents execution of command text. E005 supplies the corresponding saved-history fact for C7.06. GAPS.md records both textual readings rather than using missing syntax to choose between them.
