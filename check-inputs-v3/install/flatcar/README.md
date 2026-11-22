# Flatcar clean installation recipe

Release: 4757.2.3 stable, amd64, official QEMU qcow2 image compressed with bzip2. The published image is installed by decompressing it to `C1/base/flatcar.qcow2`, then booting once with the exact `ignition.json` through QEMU `-fw_cfg name=opt/org.flatcar-linux/config,file=...` as in `boot.sh`.

The only selected configuration creates ordinary account `user`, adds it to the documented `sudo` group, and sets its public SSH login key. No additional packages are introduced. The associated private lab key stays on the host, confined to this lab and not included in published records. User execution uses `user`; root execution uses the distribution sudo-group policy. The key is an instrument credential, not personal data.

Verification: `C1/raw/flatcar-verification.txt`. The primary signing key has historic expired subkeys; the signature verifies with the current signing subkey identified by VALIDSIG. SHA512 compares against the published DIGESTS file. The digest/signature/key were downloaded before boot.

Installation smoke: SSH executes only `printf boot-login-ok; sudo -n poweroff`. After QEMU exits, `chmod 444 C1/base/flatcar.qcow2`. No package/service/file/account/process inventory was run. Lab smoke is separately recorded. Baseline metadata uses transport `ssh`, user `user`, key `C1/install/flatcar/key`. The machine has two fixed virtual NICs as specified by the lab.

Sources: https://www.flatcar.org/docs/latest/deploy/virt-options/qemu/ and https://www.flatcar.org/docs/latest/updates-releases/releases/verify-images/ .

The first attempted baseline used native `core`; it was discarded and rebuilt to meet the requested account name. Its configuration remains `ignition-attempt1-core.json`; earlier smoke records refer to that attempt. Selected-baseline smoke is `raw/flatcar-user-smoke.txt`. User creation source: https://www.flatcar.org/docs/latest/os-config/host-config/adding-users/ .
