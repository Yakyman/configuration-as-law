# Questions noted by c2 (part microos) — for the author; not decided here

- Q-1. Section 8.2: is a non-code generated list (MIME database, module index, ld.so.cache, CA bundle) a program record by Q4 (S8.2-15, order S8.2-6), or an installed object covered by a derived line (S8.2-16 “a generated list”)? Classified GAP-TWO.
- Q-2. Section 8.2/8.5: does a person-chosen value stored in an inactive root generation (snapper snapshot 1), which the computer obeys only after a rollback, count as a value “that the computer as a whole obeys” (S8.2-11)? Classified GAP-TWO (setting vs program record).
- Q-3. S8.2-7 read by provenance (“written by the installer when installing the package”): copies inside snapshot 1 are then installed objects of the package. A reading by location (only the path the installer records) would change about 4300 rows. c2 applied provenance; noted for adjudication.

- talos: is a container runtime that pulls and deletes images (containerd, by its README: "image transfer and storage") an installer under S8.1-4? c2 read it strictly as not an installer (images decided by Q2); the other reading makes images packages (Q1).

## c2 (part void)

- Directories: the text does not say whether a directory, apart from its entries, is an object, or which line covers
  it. c2 gave each directory the decision of its entries (convention in `part-void.notes.md`). An author reading is
  needed.
- Defaults that are not chosen by a person: S8.2-11 asks for "a value chosen by a person", while S8.2-17 covers
  defaults "created during its installation". The two readings recur for xbps alternatives links, npm `.bin` links
  and image-build values (GAP-TWO rows).
- Files kept from an earlier package version (xbps `preserve`, the old kernel tree): question 1 does not say whether
  they count as "obtained as part of such a package".
- Generated lists (MIME database, ld.so.cache, locale-archive, hwdb.bin, CA trust links): the void part also
  classified these GAP-TWO, the same question as Q-1 above.

Restoration note: the talos line was appended at 11:40 UTC. At 11:48 UTC the microos part rewrote the file
(`cat >`), which dropped that line. The void part then overwrote the file by mistake. All three texts above were
restored verbatim from the parts' own write commands.
