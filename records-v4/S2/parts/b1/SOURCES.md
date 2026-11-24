# Primary documentation checked 2026-11-23 UTC

Documentation behavior is not a claim that a machine was observed. The pages describe their published versions; no tool version is assigned to a B1 template.

## gcc

[gcc](https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html)

> linking combines all the object files

Compilation and assembly produce object files; linking produces an executable. -o selects the output name; the default executable name is a.out. An object file is linker input, not the linked executable.

## gcc-purpose

[gcc-purpose](https://gcc.gnu.org/onlinedocs/gcc/G_002b_002b-and-GCC.html)

> GCC is an integrated distribution of compilers for several major programming languages.

The documented purpose is compilation; back ends generate machine code.

## plugin

[plugin](https://gcc.gnu.org/onlinedocs/gccint/Plugins.html)

> GCC plugins are loadable modules that provide extra features to the compiler.

Plugins extend the compiler using its API, including transformations and analysis.

## plugin-load

[plugin-load](https://gcc.gnu.org/onlinedocs/gccint/Plugins-loading.html)

> They are loaded by the compiler using `dlopen` or equivalent

The plugin option names a shared-library file loaded into GCC. This documents an in-process extension rather than a separate plugin process.

## cmake

[cmake](https://cmake.org/cmake/help/latest/manual/cmake.1.html)

> cross-platform buildsystem generator CMake

CMake reads a project starting at CMakeLists.txt, generates a build tree, and writes CMakeCache.txt with persistent build information. It provides --build, --install and -P script interfaces.

## install

[install](https://cmake.org/cmake/help/latest/command/install.html)

> This command generates installation rules for a project.

Install rules select destinations relative to a prefix and copy outputs. CMake generates cmake_install.cmake in the build directory; the install target, CPack, or cmake -P can execute it.

## run

[run](https://cmake.org/cmake/help/latest/command/try_run.html)

> Try compiling and then running some code.

try_run builds an executable and, on success, runs it. Compile and run results are cached unless NO_CACHE; a configure-log event is written unless NO_LOG. COPY_FILE requests a retained copy. Cross compilation may require an emulator.

## log

[log](https://cmake.org/cmake/help/latest/manual/cmake-configure-log.7.html)

> The log file is a YAML document stream

CMake writes selected configure events for build debugging. The documented location is <build>/CMakeFiles/CMakeConfigureLog.yaml; the path can change between versions.

## child

[child](https://cmake.org/cmake/help/latest/command/execute_process.html)

> Execute one or more child processes.

CMake scripts have a documented facility for starting child processes; this does not establish which commands an unspecified project actually invokes.

## theme

[theme](https://support.mozilla.org/en-US/kb/use-themes-change-look-of-firefox)

> A browser theme changes the appearance of Firefox

The selected theme controls browser appearance; this value is distinct from an installed theme bundle.

## pref

[pref](https://support.mozilla.org/en-US/kb/firefox-support-troubleshooting-guide?mobile=0)

> This file stores all user preferences

The prefs.js entry explicitly includes the home page and activated theme. These two selected values, rather than the entire preference file, are the objects here.

## home

[home](https://support.mozilla.org/en-US/kb/how-to-set-the-home-page)

> The Firefox homepage is the first page you see when you open Firefox

The selected page opens on browser opening, Home button, or a new window; session restore can instead restore previous tabs. The documented UI lets the user choose the URL.

## python

[python](https://docs.python.org/3/tutorial/interactive.html)

> The history will be available again during the next interactive interpreter session.

The default interactive configuration saves history in ~/.python_history. Input editing and history substitution allow recall; this does not assert that an arbitrary whole history file is a valid script.

## readline

[readline](https://docs.python.org/3/library/readline.html)

> reading/writing of history files

The interpreter has history reading/writing functions. The module is optional, and different back ends may use different file formats.

## bash

[bash](https://tiswww.case.edu/php/chet/bash/bashref.html)

> Read the history file and append its contents to the history list.

HISTFILE selects a saved file (default ~/.bash_history). Startup reads entries into history; exit saves entries if enabled and writable. history -r reads without replay; fc and history substitution can re-execute entries. Bash executes startup files and uses PATH for command search.

## symlink

[symlink](https://man7.org/linux/man-pages/man7/symlink.7.html)

> A symbolic link is a special type of file

A symbolic link contains a pathname used to resolve access to another file.

## exec

[exec](https://man7.org/linux/man-pages/man2/execve.2.html)

> execve() executes the program referred to by path.

Execution replaces the calling process image. Effective IDs can change for set-ID executables and capabilities; exact rights require instance evidence, not just an output filename.
