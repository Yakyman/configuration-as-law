# Primary documentation for the interpreter and mechanics rows

Source quotations are short excerpts; object classifications are applications of the fixed text, not claims made by the tool manuals. Generic parameter paths describe documented locations, not an inventory of a particular host.

## R01 — Python command line

[Python command line](https://docs.python.org/3/using/cmdline.html)

Documentation excerpt: «When called with a file name argument or with a file as standard input, it reads and executes a script from that file.»

Execution modes: script, -c, standard input and interactive input. No installation purpose is documented for these modes.

## R02 — Python exec

[Python exec](https://docs.python.org/3/library/functions.html)

Documentation excerpt: «This function supports dynamic execution of Python code.»

exec/eval consume source strings or code objects; a read file can become code.

## R03 — Bash reference manual, maintainer copy

[Bash reference manual, maintainer copy](https://tiswww.case.edu/php/chet/bash/bashref.html)

Documentation excerpt: «Process substitution allows a process’s input or output to be referred to using a filename.»

Sections 3.5.6, 3.6, 4.1 and 9.1 document pipes/descriptors, redirections, dot/source, and history. These are shell execution functions, not installation.

## R04 — Python modules

[Python modules](https://docs.python.org/3/tutorial/modules.html)

Documentation excerpt: «Python caches the compiled version of each module in the __pycache__ directory under the name module.version.pyc»

A module is source code; a compiled-only module can be loaded without its source. Directly run main scripts are not saved as bytecode by this mechanism.

## R05 — Python interactive history

[Python interactive history](https://docs.python.org/3/tutorial/interactive.html)

Documentation excerpt: «The default configuration also saves your history into a file named .python_history in your user directory.»

The history is reused by subsequent interactive sessions; this does not establish that every history file is a valid executable script.

## R06 — zipimport

[zipimport](https://docs.python.org/3/library/zipimport.html)

Documentation excerpt: «This module adds the ability to import Python modules (*.py, *.pyc) and packages from ZIP-format archives.»

Code members in an archive can execute without extracting the archive into a conventional install location.

## R07 — Git hooks

[Git hooks](https://git-scm.com/docs/githooks)

Documentation excerpt: «Hooks are programs you can place in a hooks directory to trigger actions at certain points in git’s execution.»

Default directory is $GIT_DIR/hooks; core.hooksPath can select another location. Executable hook files are invoked by Git.

## R08 — Dynamic loader

[Dynamic loader](https://man7.org/linux/man-pages/man8/ld.so.8.html)

Documentation excerpt: «ld.so, ld-linux.so - dynamic linker/loader»

Documents direct /lib/ld-linux.so.* invocation, LD_PRELOAD, LD_AUDIT, LD_LIBRARY_PATH and /etc/ld.so.preload. These load executable libraries; they do not install them.

## R09 — memfd_create

[memfd_create](https://man7.org/linux/man-pages/man2/memfd_create.2.html)

Documentation excerpt: «However, unlike a regular file, it lives in RAM and has a volatile backing storage.»

The anonymous file persists until all references are dropped; /proc/self/fd/N exposes its descriptor, not a durable file.

## R10 — mmap

[mmap](https://man7.org/linux/man-pages/man2/mmap.2.html)

Documentation excerpt: «mmap() creates a new mapping in the virtual address space of the calling process.»

MAP_ANONYMOUS and executable protection flags describe memory execution; a file-backed mapping and its backing file are different objects.

## R11 — Debugger memory assignments

[Debugger memory assignments](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Assignment.html)

Documentation excerpt: «To store values into arbitrary places in memory, use the»

Assignments can change the debugged process at a supplied address. They do not by themselves rewrite the executable on disk.

## R12 — Kernel binary format handlers

[Kernel binary format handlers](https://docs.kernel.org/admin-guide/binfmt-misc.html)

Documentation excerpt: «Binfmt_misc can also recognise a filename extension aka .com or .exe.»

The registration string is written to /proc/sys/fs/binfmt_misc/register; a named entry appears in that directory and selects an interpreter.

## R13 — Browser sandbox

[Browser sandbox](https://chromium.googlesource.com/chromium/src/+/main/docs/design/sandbox.md)

Documentation excerpt: «Sandbox leverages the OS-provided security to allow code execution that cannot make persistent changes to the computer»

This documents confinement intent. The variant expressly assumes confinement; helpers are separate processes and are not exempt merely because they render pages.

## R14 — Wasmtime command line

[Wasmtime command line](https://docs.wasmtime.dev/cli-options.html)

Documentation excerpt: «The run command will execute a WebAssembly module.»

The documented wasmtime --dir . foo.wasm invocation grants a host directory; compilation and instantiation occur in the runtime.

## R15 — Wasmtime filesystem security

[Wasmtime filesystem security](https://docs.wasmtime.dev/security.html)

Documentation excerpt: «applications can only access files and directories they’ve been given access to.»

A preopen is a capability boundary, not evidence of its particular read/write permissions or the contents of that directory.

## R16 — WASI context preopens

[WASI context preopens](https://docs.wasmtime.dev/api/wasmtime_wasi/struct.WasiCtxBuilder.html)

Documentation excerpt: «Configures a “preopened directory” to be available to WebAssembly.»

The documented API accepts FsPerms::ReadWrite or FsPerms::ReadOnly. These have different consequences for ability to change installed executable files.

## R17 — Socket interface

[Socket interface](https://docs.python.org/3/library/socket.html)

Documentation excerpt: «Bind the socket to address. The socket must not already be bound.»

bind/listen create a runtime listener; getsockname reports its selected port. No persistent service registration is implied.

## R18 — Pickle

[Pickle](https://docs.python.org/3/library/pickle.html)

Documentation excerpt: «It is possible to construct malicious pickle data which will execute arbitrary code during unpickling.»

The code-bearing serialized input in the variant is distinct from an ordinary non-executing data serialization.

## R19 — Persistent binary format rules

[Persistent binary format rules](https://www.freedesktop.org/software/systemd/man/latest/binfmt.d.html)

Documentation excerpt: «binfmt.d — Configure additional binary formats for executables at boot»

/etc/binfmt.d/*.conf is local policy; /usr/lib/binfmt.d/*.conf is the packaged counterpart. systemd-binfmt registers rules at boot.

## R20 — dlopen

[dlopen](https://man7.org/linux/man-pages/man3/dlopen.3.html)

Documentation excerpt: «The function dlopen() loads the dynamic shared object»

The path names a shared library; dependencies can also be loaded. It returns a process-local handle.

## R21 — execve

[execve](https://man7.org/linux/man-pages/man2/execve.2.html)

Documentation excerpt: «execve() executes the program referred to by path.»

The path may be an executable binary or a shebang script. The operation replaces the process image, not the named source file.

## R22 — OSTree deployments

[OSTree deployments](https://ostreedev.github.io/ostree/deployment/)

Documentation excerpt: «A deployment is physically located at a path of the form /ostree/deploy/$stateroot/deploy/$checksum.»

The deployment layer installs operating systems. Staged deployments, the repository /ostree/repo and boot entries are concrete examples of artifacts, not proof that any M row chose this backend.

## R23 — fsync

[fsync](https://man7.org/linux/man-pages/man2/fsync.2.html)

Documentation excerpt: «fsync, fdatasync - synchronize a file's in-core state with storage device»

File and directory persistence are separate calls; this primitive names no application-success report or declaration.

## R24 — unlink

[unlink](https://man7.org/linux/man-pages/man2/unlink.2.html)

Documentation excerpt: «If the name was the last link to a file but any processes still have the file open»

Open references can retain the inode after pathname removal. unlink does not terminate the processes using it.

## R25 — Service manager control

[Service manager control](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html)

Documentation excerpt: «systemctl — Control the systemd system and service manager»

enable/disable manipulate links; start/stop affect runtime state. This is configuration functionality, including when invoked by a shell.

## R26 — Service units

[Service units](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html)

Documentation excerpt: «A unit configuration file whose name ends in ".service" encodes information about a process controlled and supervised by systemd.»

Restart policies and activation dependencies can recreate processes. They do not show which configuration a generic M row changes.

## R27 — Embedded interpreter

[Embedded interpreter](https://docs.python.org/3/extending/embedding.html)

Documentation excerpt: «you can pass a string containing Python statements to PyRun_SimpleString()»

The embedding interface also accepts a file through PyRun_SimpleFile; embedded execution does not itself install or remove programs.

## R28 — Descriptor execution

[Descriptor execution](https://man7.org/linux/man-pages/man2/execveat.2.html)

Documentation excerpt: «If path is an empty string and the AT_EMPTY_PATH flag is specified»

A descriptor can name the executable instead of a pathname. This interface also supports the implementation of fexecve.
