part-mint: memberless groups (69, UNKNOWN) could be settled only by a removal probe on a disposable copy (S3-1) or a filesystem inventory of name references; not part of this task.
- (part flatcar) S2.2-7 scope for settings of one program that decide what can be done on the computer through it (sshd forwarding, GRUB autoload lists, /etc/skel): NOT or MUST? Recorded as HOLE.
- (part flatcar) Server host keys are not "keys used to log in to an account" (S2.2-15); recorded as HOLE.
- (part flatcar) machine-id: does regeneration with a different value on removal mean the computer "stops doing something" (S2.2-2)? Recorded as HOLE.
fedora (c2): inventory does not record the boot mode (BIOS/UEFI) of the machine; 14 UEFI boot rows stay UNKNOWN.
fedora (c2): rpm file ownership query (113-ownership-rpm.out) returned nothing; rpm contents taken from public Fedora 45 repository metadata.
fedora (c2): reading used: S2.2-2 decides both ways (failing the test = need not); S2.2-3..7 are exceptions to the test. Author may want to confirm.
