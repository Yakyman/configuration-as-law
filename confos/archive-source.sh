#!/bin/bash
# Create a source archive once; never overwrite an existing release archive.
set -euo pipefail
cd "$(dirname "$0")"
version=$(cat VERSION)
archive="releases/confos-$version-source.tar.gz"
test ! -e "$archive"
extra_paths=$(mktemp)
temporary=
trap 'rm -f "$extra_paths"; if [ -n "$temporary" ]; then rm -f "$temporary"; fi' EXIT
# Generate the whole list successfully before tar: process substitution would hide
# a validation failure and could silently archive only a prefix of required inputs.
python3 flatpak-readers-archive-paths.py >"$extra_paths"
python3 flatpak-mpv-js-archive41-paths-draft.py >>"$extra_paths"
python3 readers-archive-paths-042.py >>"$extra_paths"
python3 nft-ed-archive-paths-043.py >>"$extra_paths"
python3 tools-archive-paths-044.py >>"$extra_paths"
python3 ssh-archive-paths-044.py >>"$extra_paths"
archive_members=( \
    advance-paths-049.py prepare-readers-049.py prepare-paths-release-049.sh check-other-export-049.sh check-other-export-049.py compare-native-entries.py archive-paths-049.sh cleanup-paths-049.sh fetch-paths-049.sh sync-paths-049.sh handoff-paths-049.py push-files.sh test-durability.py test-recording-apt.py test-configuration-recording.py test-language-recording.py test-podman-recording.py test-flatpak-recording.py test-flatpak-readers-module.py resume2-solver-release-048.sh records/reader-inheritance-0.49.json packages/confos-code-readers_0.48_amd64.deb packages/confos-code-readers_0.48_amd64.deb.sha256 \
    SOLVER-PRIVATE.md records/lo-solver-private records/lo-macro-private-build-failure inspect-lo-resolution-private.py probe-lo-solver-private.py advance-solver-048.py prepare-readers-048.py prepare-solver-release-048.sh probe-solver-048.sh archive-solver-048.sh fetch-solver-048.sh cleanup-solver-048.sh document-solver-048.py sync-solver-048.sh handoff-solver-048.py records/reader-inheritance-0.48.json packages/confos-code-readers_0.47_amd64.deb packages/confos-code-readers_0.47_amd64.deb.sha256 \
    interpreter-inputs/libperl-private records/libperl-guest-private build-libperl-private.sh rebuild-libperl-private.sh libperl-private-build-deps.py continue-libperl-private.sh libperl-private-config-paths.py complete-libperl-private.sh libperl-guest-private-build.py libperl-guest-private-probe.py libperl-guest-private-run.sh libperl-guest-private-cleanup.py embedded-perl-probe.c finalize-libperl-private.py prepare-libperl-release-recipes-047.py advance-libperl-047.py prepare-libperl-047.py prepare-libperl-release-047.sh build-libperl-fixture-047.py probe-libperl-047.sh archive-libperl-047.sh fetch-libperl-047.sh cleanup-libperl-047.sh document-libperl-047.py sync-libperl-047.sh handoff-libperl-047.py records/reader-inheritance-0.47.json packages/confos-code-readers_0.46_amd64.deb packages/confos-code-readers_0.46_amd64.deb.sha256 \
    prepare-libpython-release-plumbing-046.py fetch-libpython-046.sh cleanup-libpython-046.sh handoff-libpython-046.py \
    recorded-filename-reader.py probe-recorded-filename-reader.py document-libpython-046.py sync-libpython-046.sh \
    interpreter-inputs/libpython-private records/libpython-guest-private records/libpython-guest-private-abi-failure LIBPYTHON-PRIVATE.md build-libpython-private.sh rebuild-libpython-private.sh libpython-debian-modules-private.py prepare-libpython-guest-private.py libpython-guest-private-build.py libpython-guest-private-probe.py libpython-guest-private-run.sh libpython-guest-private-cleanup.py finalize-libpython-private.py embedded-python-probe.c advance-libpython-046.py prepare-libpython-046.py prepare-libpython-release-046.sh prepare-libpython-probes-046.py build-libpython-fixture-046.py probe-libpython-046.sh archive-libpython-046.sh records/reader-inheritance-0.46.json packages/confos-code-readers_0.45_amd64.deb packages/confos-code-readers_0.45_amd64.deb.sha256 \
    document-radio-recording-045.py sync-radio-recording-045.sh fetch-radio-recording-045.sh cleanup-radio-recording-045.sh handoff-radio-recording-045.py records/reader-inheritance-0.45.json packages/confos-code-readers_0.44_amd64.deb packages/confos-code-readers_0.44_amd64.deb.sha256 \
    nmcli-command radio-recording-command-draft radio-recording-private-probe.py radio-recording-private-evidence radio-recording-private-evidence-attempt1 RADIO-RECORDING-DRAFT.md advance-radio-recording-045.py prepare-radio-recording-045.py build-radio-recording-045.py probe-radio-recording-045.sh prepare-radio-release-045.sh archive-radio-recording-045.sh prepare-readers-045.py \
    radio_declaration.py radio_runtime.py radio_integration.py radio_systemd.py radio-control-denials.apparmor radio-trusted-profile.apparmor radio-public-fixture RADIO-040-DOCUMENTATION.md advance-radio-release-040.py prepare-radio-040.sh prepare-radio-component-040.py build-radio-fixture-040.py build-radio-fault-fixture-040.py probe-radio-040.sh sync-radio-040.sh radio-mutation-probe.py test-radio-declaration.py test-radio-runtime-draft.py \
    build-radio-lifecycle-fault-040.py radio-lifecycle-private.py radio-lifecycle-private.sh test-radio-lifecycle.py RADIO-LIFECYCLE-RESULTS.md sync-radio-lifecycle-040.sh \
    archive-radio-040.sh check-radio-component-inheritance.py cleanup-radio-040.sh packages/confos-code-readers_0.39_amd64.deb packages/confos-code-readers_0.39_amd64.deb.sha256 \
    radio-lifecycle-retry.py radio-lifecycle-retry.sh \
    build-radio-flatpak-fixture-040.py radio-flatpak-control-probe.py probe-radio-flatpak-040.sh RADIO-FLATPAK-040.md \
    radio_inspect.py wire-radio-inspection-040.py probe-radio-inspection.py document-radio-040.py document-radio-underived.py resume-radio-040.sh resume-radio-probes-040.sh rebuild-radio-cleanup-040.sh \
    advance-mpv-release-041.py prepare-mpv-component-041.py prepare-mpv-041.sh sync-mpv-041.sh build-mpv-fixture-041.py mpv41-app-probe.py mpv41-original-alias-probe.py probe-mpv-041.sh archive-mpv-041.sh cleanup-mpv-041.sh document-mpv-041.py MPV-041-DOCUMENTATION.md \
    assemble.py recording.py language_recording.py flatpak_recording.py podman_recording.py configuration_recording.py configuration-command apt-command optional_readers.py appimage_readers.py flatpak_profile.py flatpak-profile.apparmor installers.py containers.py user_units.py games.py installer-chroot nft-query flatpak-command podman-command systemctl-query language-query confos runtime-init early-init components.txt components base-roots.txt lock-components.py build.sh boot.sh VERSION \
    examples INTERFACE.md DECLARATION.md CHOICES.md README.md CODE-READERS.md package-base.py check-runtime-source-package.py base-defaults.json \
    archive_sources.py archive-sources.json \
    package-boot.py boot-components.txt boot-grub.cfg \
    package-initramfs.py packages/confos-initramfs_${version}+*_amd64.deb packages/confos-initramfs_${version}+*_amd64.deb.sha256 \
    "packages/confos-boot_${version}_amd64.deb" "packages/confos-boot_${version}_amd64.deb.sha256" \
    "packages/confos-runtime_${version}_all.deb" "packages/confos-runtime_${version}_all.deb.sha256" \
    "packages/confos-code-readers_${version}_amd64.deb" "packages/confos-code-readers_${version}_amd64.deb.sha256" \
    build-native-readers.sh package-code-readers.py code-file-policy.h \
    patch-bash-code.py patch-python-code.py patch-perl-code.py interpreter-source.sha256 \
    patch-busybox-code.py busybox-source.sha256 \
    interpreter-inputs/busybox/*.dsc interpreter-inputs/busybox/*.tar.xz interpreter-inputs/busybox/*.tar.bz2 \
    interpreter-inputs/debian/*.dsc interpreter-inputs/debian/*.tar.xz interpreter-inputs/debian/*.asc \
    packages/confos-code-readers_0.28_amd64.deb packages/confos-code-readers_0.28_amd64.deb.sha256 \
    package-optional-readers.py build-optional-readers.sh build-tools-code.sh build-make-code.sh \
    patch-tools-code.py patch-make-code.py make-code-policy.h tools-source.sha256 \
    normalize-reader-times.py extract-tools-sources.sh prepare-tools-build-deps.py \
    interpreter-inputs/tools/*.dsc interpreter-inputs/tools/*.tar.* \
    packages/confos-code-readers_0.29_amd64.deb packages/confos-code-readers_0.29_amd64.deb.sha256 \
    package-node-readers.py build-node-reader-component.sh build-node-code.sh node-build-inner.sh \
    prepare-node-build-deps.py prepare-node-build-tree.py patch-node-code.py \
    patch-node-metadata.py patch-node-startup.py harden-node-bindings.py node-source.sha256 \
    interpreter-inputs/node/*.dsc interpreter-inputs/node/*.tar.xz \
    packages/confos-code-readers_0.30_amd64.deb packages/confos-code-readers_0.30_amd64.deb.sha256 \
    package-git-readers.py build-git-reader-component.sh build-git-code.sh prepare-git-build-deps.py \
    patch-git-code.py git-code-policy.h git-source.sha256 \
    interpreter-inputs/git/*.dsc interpreter-inputs/git/*.tar.xz interpreter-inputs/git/git_2.47.3-0+deb13u1_amd64.deb \
    packages/confos-code-readers_0.31_amd64.deb packages/confos-code-readers_0.31_amd64.deb.sha256 \
    package-nvim-readers.py build-nvim-reader-component.sh build-nvim-code.sh \
    patch-nvim-code.py patch-luajit-code.py nvim-source.sha256 nvim-appimage-entry \
    interpreter-inputs/nvim/neovim-v0.10.4.tar.gz appimage-inputs/nvim.appimage \
    packages/confos-code-readers_0.32_amd64.deb packages/confos-code-readers_0.32_amd64.deb.sha256 \
    patch-busybox-vi.py build-busybox-vi.sh package-busybox-vi-readers.py build-busybox-vi-component.sh \
    prepare-game-sources.py prepare-game-bundles.py game-common.cfg game-server.cfg game-packages.conf )
# Fail before writing any numbered archive if a required source input is missing.
for member in "${archive_members[@]}"; do
    test -e "$member" || test -L "$member" || { echo "Missing archive input: $member" >&2; exit 1; }
done
temporary=$(mktemp "releases/.confos-$version-source.XXXXXXXX")
tar --null -T "$extra_paths" --sort=name --mtime=@1795392000 --owner=0 --group=0 -czf "$temporary" "${archive_members[@]}"
chmod 0644 "$temporary"
# A hard link publishes the complete file without replacing an existing version.
ln "$temporary" "$archive"
rm "$temporary"
temporary=
sha256sum "images/confos-$version-clean.qcow2" "$archive" >"releases/release-$version.sha256"
