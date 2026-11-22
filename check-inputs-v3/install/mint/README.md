# Mint clean installation recipe

Use Linux Mint 22.3 Cinnamon 64-bit standard ISO, verified by SHA256 and its detached signature. No HWE variant is selected: the official edition page recommends the standard ISO and offers HWE as a fallback for hardware that cannot boot it.

On the host, extract only `/casper/vmlinuz` and `/casper/initrd.lz` from the installation ISO using `xorriso -osirrox on -indev ... -extract ...`. This is installer preparation, not inspection of an installed check machine. Put exact `preseed.cfg` at archive root and append a compressed newc cpio archive to the original initrd:

```sh
mkdir seed
cp preseed.cfg seed/preseed.cfg
(cd seed; printf 'preseed.cfg\n' | cpio -o -H newc) | gzip > seed.gz
cat initrd.lz seed.gz > initrd-seeded.lz
rm -rf seed seed.gz
```

Create a blank 32 GiB qcow2 disk and execute `boot.sh` under a persistent user unit. That script holds slot 10 and boots the installer using `file=/preseed.cfg automatic-ubiquity`. The first attempted HTTP-preseed approach did not load the seed; it is recorded under raw and was discarded before this clean attempt.

The seed chooses installer defaults: Cinnamon edition, entire blank disk, ordinary account `user`, no encryption, no optional multimedia codecs and no install-time package updates. Language en_US.UTF-8, keyboard US and UTC timezone are fixed for reproducibility. Account password is the isolated lab credential `cal-test`, not a personal credential. Default sudo policy is unchanged. No SSH server or guest agent is added. The success command only enables serial login and its boot console, which are necessary command instruments. No additional packages are selected.

After unattended shutdown, mark `C1/base/mint.qcow2` read-only. Metadata: serial transport, user `user`, password `cal-test`. Then boot one disposable clone for login/command smoke and the exact `C1/actions/mint.sh`; destroy the clone afterward. Do not collect an inventory.

Sources for installer keys: https://github.com/linuxmint/ubiquity/blob/master/d-i/source/user-setup/debian/user-setup-udeb.templates ; https://github.com/linuxmint/ubiquity/blob/master/d-i/source/partman-auto/debian/partman-auto.templates ; https://github.com/linuxmint/ubiquity/blob/master/ubiquity/plugins/ubi-prepare.py .

The Ubiquity success hook did not produce a working serial login in the first boot smoke. The selected recipe therefore includes the explicit final installation step `enable-serial.sh`, delivered by `console-input.py` through virtual-console login (user/test password). It only sets the boot console and enables the existing serial-getty unit. No installed files are read. Shut down this still-clean clone and flatten its overlay to the selected read-only backing before testing ordinary actions on a new clone.
