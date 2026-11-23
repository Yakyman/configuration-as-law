# Evidence layout

`rebuild-final.log` and `peer/rebuild-final.log` are the two complete final clean recipe runs. `final-build-provenance.json` records both standalone image hashes, formats/sizes, the 56 regular recipe-source hashes and successful build service results. Generated `__pycache__` directories are not recipe inputs and are removed during final cleanup. `recipe.sha256` names the published source files.

`build-factory-comparison.json` records equal complete factory and initramfs hashes from those two recipe executions. Bootstrap fixes the pinned source date for reproducible initramfs generation. `rebuild-attempt-1/` retains the preceding complete validation's failed independent comparison, differing initramfs hashes, controller exit 1, build logs and exact old recipe. `rebuild-attempt-2/` retains the later checksum-observation transport error, both cleaned failed builds and their exact recipe. Neither failed attempt is rewritten as a pass.

Numbered integration/development logs retain the implementation failures and corrected observations described in ITERATIONS. Empty early logs belong to a mistaken host invocation and are not passing tests. `peer/ordinary-dev-01.log` and `peer/ordinary-dev-02.log` preserve the failed compiler/editor cases; `focused-dev-01.log` proves only the corrected development paths, not final-image acceptance.

`rebuilt/` is the fresh final-image four-channel suite and complete preceding regression chain. `combined/` applies one exact exported declaration to fresh guests of both independent builds, verifies it after reboot and compares every actual value. The final assessment aggregates saved results; independent review supplies the closure judgment.

Published command logs replace a host home prefix with `stand/` and the transport alias with `the-host` when present. Guest `/home/stand` paths are synthetic test inputs and remain literal. No laboratory private key is exported. Declaration payloads and hashes are exported without rewriting.

`factory-info.json` checks the exported 553-row factory and all 24 installed recipe-source files against the published sources. `publish-evidence.py` packages completed evidence only after all required controller summaries are zero, preserves exact declaration payloads, and records every normalized host identifier and exported file checksum.
