# C1 evidence register — 2026-11-19

The table in ATTACK.md links to these IDs. Each entry identifies primary documentation and a saved local copy/excerpt. Source facts are paraphrased in the report; the attack conclusions are our deductions. Retrieval was read-only. Failed full-page retrievals are identified explicitly.

| ID | Primary source | Saved evidence and useful locator |
|---|---|---|
| <a id="e01"></a>E01 | [GNU Emacs manual](https://www.gnu.org/software/emacs/manual/pdf/emacs.pdf), [GNU Emacs Lisp introduction](https://www.gnu.org/software/emacs/manual/pdf/eintr.pdf) | Official manual search evidence, initialization sections; full HTML fetch failed. PAPER O2 independently states the executable-settings case. |
| <a id="e02"></a>E02 | [Mozilla profile contents](https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data) | Mozilla excerpts, places.sqlite/bookmarks/history; further excerpts. Direct fetch was bot content, not relied upon. |
| <a id="e03"></a>E03 | [VS Code extension host](https://code.visualstudio.com/api/advanced-topics/extension-host) | Copy, local Node.js / web / remote extension hosts. Paper §6 supplies Firefox extension classification. |
| <a id="e04"></a>E04 | [PostgreSQL database layout](https://www.postgresql.org/docs/current/storage-file-layout.html) | Copy, base, global, pg_wal, transaction state. |
| <a id="e05"></a>E05 | [PostgreSQL pg_upgrade](https://www.postgresql.org/docs/current/pgupgrade.html) | Copy, major-version catalog changes and migration. |
| <a id="e06"></a>E06 | [Docker images and containers](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/) | Copy, isolated process and image components. |
| <a id="e07"></a>E07 | [libvirt domain XML](https://libvirt.org/formatdomain.html) | Copy, disk, TPM emulator, persistent_state. |
| <a id="e08"></a>E08 | [npm exec](https://docs.npmjs.com/cli/v11/commands/npm-exec) | Copy, absent packages installed in cache and executed via PATH. |
| <a id="e09"></a>E09 | [pip cache](https://pip.pypa.io/en/stable/topics/caching/) | Copy, HTTP and wheel caches, purge. |
| <a id="e10"></a>E10 | [Chrome native messaging](https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging) | Copy, separate native-host process. |
| <a id="e11"></a>E11 | [OneDrive Files On-Demand](https://support.microsoft.com/en-us/office/save-disk-space-with-onedrive-files-on-demand-for-windows-0e6860d3-d9f3-4971-b321-7092438fb38e) | Copy, online-only and locally available content. |
| <a id="e12"></a>E12 | [Windows activation/slmgr](https://learn.microsoft.com/en-us/windows-server/get-started/activation-slmgr-vbs-options) | Copy, KMS activation and renewal intervals. |
| <a id="e13"></a>E13 | [systemd machine-id](https://www.freedesktop.org/software/systemd/man/latest/machine-id.html) | Snapshot, machine-id section, physical file lines 16–37 (embedded page labels L13–34): generation and persistence; first-boot use at file lines 38–45. This section starts at file line 1. |
| <a id="e14"></a>E14 | [NetworkManager keyfiles](https://networkmanager.dev/docs/api/latest/nm-settings-keyfile.html) | Snapshot, nm-settings-keyfile section, physical file lines 902–915 (embedded page labels L7–20): profiles and secrets; manual creation/editing at file line 911. This section starts at file line 893. |
| <a id="e15"></a>E15 | [BlueZ storage specification](https://raw.githubusercontent.com/bluez/bluez/master/doc/settings-storage.txt) | Saved specification, Purpose, directory layout, LinkKey/LongTermKey groups. |
| <a id="e16"></a>E16 | [OpenSSH ssh-keygen](https://man.openbsd.org/ssh-keygen.1), [sshd_config](https://man.openbsd.org/sshd_config.5) | Search evidence, -A; snapshot, sshd_config HostKey L193–200. |
| <a id="e17"></a>E17 | [Certbot user guide](https://eff-certbot.readthedocs.io/en/stable/using.html) | Snapshot, Where are my certificates L556 onward; overview, obtaining versus installing. |
| <a id="e18"></a>E18 | [DKMS README](https://github.com/dkms-project/dkms) | Snapshot, modules built/installed, signing keys L245–281. |
| <a id="e19"></a>E19 | [Cronie crontab source](https://raw.githubusercontent.com/cronie-crond/cronie/master/man/crontab.5), [systemd.timer](https://www.freedesktop.org/software/systemd/man/255/systemd.timer.html) | Cronie, L23–35; timer, Persistent L98–101. |
| <a id="e20"></a>E20 | [systemd-coredump](https://www.freedesktop.org/software/systemd/man/262/systemd-coredump.html), [journald.conf](https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html) | Core snapshot, L26–31; journal copy, retention. |
| <a id="e21"></a>E21 | [Linux capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html) | Snapshot, L17–30: permission checks attach to processes/threads, not human intent. |
| <a id="e22"></a>E22 | [Apple Secure Enclave](https://support.apple.com/en-ca/guide/security/sec59b0b31ff/1/web/1) | Primary-domain search excerpt, manufacturing UID generation/fusing; failed full open, HTTP 429. |
| <a id="e23"></a>E23 | [ESP-IDF eFuses](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/efuse.html), [Linux NVMEM](https://www.kernel.org/doc/html/latest/driver-api/nvmem.html) | eFuse snapshot, one-way fields and factory MAC; NVMEM excerpt; calibration ESP32-H2 reference excerpt. |
| <a id="e24"></a>E24 | [ESP32-C5 bootloader anti-rollback](https://docs.espressif.com/projects/esp-idf/en/v5.5.6/esp32c5/api-guides/bootloader.html#anti-rollback-feature) | Snapshot, Anti-Rollback Feature, physical file lines 77–96 (embedded page labels L158–177): ROM enforcement at file line 79, irreversible increase at 82. The duplicate at file lines 146–165 is not the locator used here. The paper’s Generation definition is PAPER.html line 135. |
| <a id="e25"></a>E25 | [UEFI 2.10 boot manager](https://uefi.org/specs/UEFI/2.10/03_Boot_Manager.html) | Snapshot, BootOrder, BootNext consumption, firmware maintenance of variables. |
| <a id="e26"></a>E26 | [Android Keystore version binding](https://source.android.com/docs/security/features/keystore/version-binding), [Keymaster implementer reference](https://android.googlesource.com/platform/docs/source.android.com/+/04426e67ca3ee557a0083f9b3c6ba789021bd7a0/en/security/keystore/implementer-ref.html) | Binding snapshot, keyblob upgrade; reference, rollback-resistant deletion. |
| <a id="e27"></a>E27 | [TPM NV increment](https://tpm2-tools.readthedocs.io/en/stable/man/tpm2_nvincrement.1/), [NV undefine](https://tpm2-tools.readthedocs.io/en/stable/man/tpm2_nvundefine.1/) | Counter snapshot; deletion snapshot. |
| <a id="e28"></a>E28 | [Microsoft PCR banks and sealing](https://learn.microsoft.com/en-us/windows/security/hardware-security/tpm/switch-pcr-banks-on-tpm-2-0-devices) | Snapshot, measured state and failure to unseal. |
| <a id="e29"></a>E29 | [Linux microcode loader](https://www.kernel.org/doc/html/v6.1/x86/microcode.html), [Android hardware security](https://source.android.com/docs/security/best-practices/hardware?authuser=111) | Microcode; KeyMint/StrongBox. |
| <a id="e30"></a>E30 | [Android 14 compatibility definition](https://source.android.com/docs/compatibility/14/android-14-cdd?authuser=5) | Excerpt, bootloader lock, confirmation and erasure. |

The paper's exact wording and fixed check criteria are saved in paper-sections.txt, with source line numbers, and its SHA-256. The report does not claim that documentation establishes an actual census result for a person's machine.
