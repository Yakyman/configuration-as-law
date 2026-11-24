#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
test "$(cat VERSION)" = 0.40
grep -qx 'CANDIDATE40 RADIO AND REGRESSIONS PASS' logs/prepare-radio-0.40.log
grep -qx 'CANONICAL40 RADIO GATES PASS' logs/radio-0.40.log
grep -qx 'CANONICAL40 FLATPAK RADIO CONTROLS PASS' logs/radio-flatpak-0.40.log
grep -qx 'SMOKE PASS' logs/smoke-0.40.log
python3 check-runtime-source-package.py 0.40 >logs/runtime-source-package-0.40.log
python3 check-radio-component-inheritance.py >logs/reader-inheritance-0.40.log
cp radio-040-fixture/normal.conf records/radio-040-normal-fixture.conf
cp radio-040-fixture/systemd.conf records/radio-040-systemd-fixture.conf
cp radio-040-flatpak-fixture/declaration.conf records/radio-040-flatpak-fixture.conf
sha256sum releases/confos-0.39-source.tar.gz releases/inherited-0.39.sha256 \
    logs/flatpak-readers-0.39.log logs/configuration-recording-0.38.log \
    logs/radio-0.40.log >releases/inherited-0.40.sha256
bash archive-source.sh
sha256sum assemble.py confos runtime-init early-init recording.py configuration_recording.py \
    configuration-command systemctl-query user_units.py flatpak_readers.py flatpak_profile.py \
    flatpak-profile.apparmor installers.py package-base.py package-initramfs.py build.sh boot.sh \
    radio_declaration.py radio_runtime.py radio_integration.py radio_systemd.py radio_inspect.py \
    radio-control-denials.apparmor radio-trusted-profile.apparmor archive-source.sh \
    archive-radio-040.sh check-radio-component-inheritance.py >releases/source-0.40.sha256
sha256sum images/confos-0.40-clean.work/root.sqfs images/confos-0.40-clean.work/initramfs \
    images/confos-0.40-clean.work/efi/EFI/BOOT/BOOTX64.EFI >releases/payload-0.40.sha256
CONFOS_FORBID_HOST_GRUB=1 CONFOS_FORBID_HOST_INITRAMFS=1 \
    bash verify-payload-inventory.sh 0.40 ../cases/inventory/inventory
