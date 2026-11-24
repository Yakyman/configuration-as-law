# Round 0 provenance notes

Recorded 2026-11-23 UTC.

- `carried-recipe-sha256.json` hashes the 56 original laptop recipe files before copying/relocation.
- `prior-server-recipe-sha256.json` hashes the 56 original server recipe files in the previous night's final build root, read before copying inputs. This is a **pre-relocation** source inventory, not tonight's deployed recipe. It equals `carried-recipe-sha256.json`. Its initial ambiguous filename `server-source-recipe-sha256.json` was renamed after document review; bytes did not change.
- `recipe-provenance.json` contains both original and relocated recipe hashes. Only `lab.py` changes: `VMs/cal-1122/slots` becomes `VMs/cal-1123/slots`. No installed mechanism, self-test assertion, fixture, or expected result changes.
- `build-identities.json` identifies two independent full recipe executions. Image hashes can differ; the full declaration/actual-state comparison is a separate test, not inferred from image digests.
- The source links in (not published: orchestration or scratch) were corrected after the baseline started from (not published: record outside this collection) to `../../`. The expectations, commands and scope were unchanged.

Both build logs report a 552-row factory and 31,247 base files. They emit the same factory SHA-256 `03838ed7782e26b95583066eeaff28608e2e1fdfdf5cfbd8d29bedd7d84a2c72`, base-manifest SHA-256 `389ef31925caf6029db0629fcc5073d5a2b45520113c45820a14480a1e9da1fc`, and initramfs SHA-256 `668563d9966420710c09b8826e1ccbcc9112ccbcc449782994cdb0b5321c4aac` (`primary-build.log`, `peer-build.log`, their final hash-output block).

The allowed previous final review reports 553 factory rows and factory SHA-256 `0cccc17c3d5ef98f37b90ecff4665711b4a99e2cd79571dd3688f124a4395b27`; its base-manifest and initramfs hashes equal tonight's. The factory row-count/hash difference is retained as an observation, not attributed to a version 4 mechanism. `FACT_UNKNOWN`: the changed historical row/value cannot be identified from the named historical reports alone. The old complete declaration/raw exports are outside this task's named read set; no additional historical data or probe was used to choose a cause. Later work must use tonight's exported factory as its actual baseline, not assume the previous factory digest.
