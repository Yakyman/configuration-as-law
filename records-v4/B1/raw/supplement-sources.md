# Additional primary evidence

## Homepage behavior

[Home page behavior](https://support.mozilla.org/en-US/kb/how-to-set-the-home-page)

> The Firefox homepage is the first page you see when you open Firefox

The same page documents opening the selected page with the Home button and in a new window. This establishes navigation, not a definition of the hypothesis's phrase launching something.

## CLI directory permissions

[Wasmtime CLI implementation](https://raw.githubusercontent.com/bytecodealliance/wasmtime/main/src/common.rs)

> builder.preopened_dir(host, guest, wasmtime_wasi::FsPerms::ReadWrite)?;

The documented CLI --dir option is configured with read/write WASI permissions. The API's separate read-only option is not evidence that this CLI invocation chooses read-only. Effective host filesystem permissions, accessible contents and module behavior are separate facts.

## Embedded debugger execution

[Debugger Python commands](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Python-Commands.html)

> The python command can be used to evaluate Python code.

The source command can read a .py script; imported modules may create .pyc files depending on configuration.

## Database function code

[PL/Python function bodies](https://www.postgresql.org/docs/current/plpython-funcs.html)

> The body of a function is simply a Python script.

The documentation shows CREATE FUNCTION with a retained function body, rather than only a transient command argument.

## AWK execution

[AWK upstream manual distributed by the package](https://man.archlinux.org/man/gawk.1.en)

> Read the AWK program source from the file program-file

The -f and -e interfaces select saved source and command-argument source respectively; they are not package installation interfaces.
