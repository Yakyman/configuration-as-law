# Installation-channel documentation

Primary documentation checked online; quotes are short source anchors, with path and behaviour details in the linked sections. Placeholders name tool-selected paths, not additional variants. Generated administrative metadata is distinguished from package payload. No runtime experiments.

- **pacman** [https://man.archlinux.org/man/pacman.8.en](https://man.archlinux.org/man/pacman.8.en): “Remove package(s) from the system.”
- **pacconf** [https://man.archlinux.org/man/pacman.conf.5.en](https://man.archlinux.org/man/pacman.conf.5.en): “The default is /var/cache/pacman/pkg/.”
- **hooks** [https://man.archlinux.org/man/alpm-hooks.5.en](https://man.archlinux.org/man/alpm-hooks.5.en): “Hooks may be disabled”
- **pip** [https://pip.pypa.io/en/stable/cli/pip_install/](https://pip.pypa.io/en/stable/cli/pip_install/): “Install packages into <dir>.”
- **pipmeta** [https://packaging.python.org/en/latest/specifications/recording-installed-packages/](https://packaging.python.org/en/latest/specifications/recording-installed-packages/): “This directory is named as `{name}-{version}.dist-info`”
- **pipcache** [https://pip.pypa.io/en/stable/topics/caching/](https://pip.pypa.io/en/stable/topics/caching/): “Pip provides an on-by-default caching, designed to reduce the amount of time spent on duplicate downloads and builds.”
- **editable** [https://pip.pypa.io/en/stable/topics/local-project-installs/](https://pip.pypa.io/en/stable/topics/local-project-installs/): “Editable installs allow you to install your project without copying any files.”
- **build** [https://pip.pypa.io/en/stable/reference/build-system/](https://pip.pypa.io/en/stable/reference/build-system/): “Generate a wheel for the package.”
- **npm** [https://docs.npmjs.com/cli/v11/configuring-npm/folders/](https://docs.npmjs.com/cli/v11/configuring-npm/folders/): “so that they may be found by npm scripts when necessary.”
- **npmuninstall** [https://docs.npmjs.com/cli/v11/commands/npm-uninstall/](https://docs.npmjs.com/cli/v11/commands/npm-uninstall/): “This uninstalls a package, completely removing everything npm installed on its behalf.”
- **npmlink** [https://docs.npmjs.com/cli/v11/commands/npm-link/](https://docs.npmjs.com/cli/v11/commands/npm-link/): “Package linking is a two-step process.”
- **npmscripts** [https://docs.npmjs.com/cli/v11/using-npm/scripts/](https://docs.npmjs.com/cli/v11/using-npm/scripts/): “Does NOT run in global mode”
- **site** [https://docs.python.org/3/library/site.html](https://docs.python.org/3/library/site.html): “Both files can exist in one of the four directories mentioned above.”
- **flatpak** [https://docs.flatpak.org/en/latest/flatpak-command-reference.html](https://docs.flatpak.org/en/latest/flatpak-command-reference.html): “The application overrides are saved in text files residing in $XDG_DATA_HOME/flatpak/overrides in user mode.”
- **flatinside** [https://docs.flatpak.org/en/latest/under-the-hood.html](https://docs.flatpak.org/en/latest/under-the-hood.html): “With Flatpak, each application, runtime and extension is a branch in a repository.”
- **appimage** [https://docs.appimage.org/user-guide/run-appimages.html](https://docs.appimage.org/user-guide/run-appimages.html): “The AppImage is unmounted when the application called in the example is interrupted”
- **appupdate** [https://docs.appimage.org/packaging-guide/optional/updates.html](https://docs.appimage.org/packaging-guide/optional/updates.html): “Via an updater tool built into the AppImage itself”
- **curl** [https://curl.se/docs/manpage.html](https://curl.se/docs/manpage.html): “Write output to the given file instead of stdout.”
- **chmod** [https://man.archlinux.org/man/chmod.1.en](https://man.archlinux.org/man/chmod.1.en): “chmod - change file mode bits”
- **bash** [https://man.archlinux.org/man/bash.1.en](https://man.archlinux.org/man/bash.1.en): “Bash is a command language interpreter that executes commands read from the standard input, from a string, or from a file.”
- **tar** [https://man.archlinux.org/man/tar.1.en](https://man.archlinux.org/man/tar.1.en): “tar - an archiving utility”
- **gcc** [https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html](https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html): “linking combines all the object files”
- **plugin** [https://gcc.gnu.org/onlinedocs/gccint/Plugins.html](https://gcc.gnu.org/onlinedocs/gccint/Plugins.html): “GCC plugins are loadable modules that provide extra features to the compiler.”
- **cmake** [https://cmake.org/cmake/help/latest/command/install.html](https://cmake.org/cmake/help/latest/command/install.html): “This command generates installation rules for a project.”
- **cmakerun** [https://cmake.org/cmake/help/latest/command/try_run.html](https://cmake.org/cmake/help/latest/command/try_run.html): “Try compiling and then running some code.”
- **systemctl** [https://www.freedesktop.org/software/systemd/man/latest/systemctl.html](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html): “systemctl — Control the systemd system and service manager”

## Local Section 9.3 labels

- **B1-9.3-command**: “A command typed by a person is not considered a channel for bypassing the declaration.”
- **B1-9.3-channel**: “A channel is anything that such a command tries to leave behind: saving and running a file, registering a service, a timer or an autostart, changing a setting.”
- **B1-9.3-stream**: “A separate case: a command downloads and executes code without saving it; after a reboot, nothing that was executed must be in force.”
