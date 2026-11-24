### gentoo

No inventory was obtained: `D1/in/raw/gentoo/NOT-RUN.md` records the fresh-machine startup failure and references its retained command output and exit statuses. No package-reason, packaged-file-integrity, group-membership or filesystem-persistence fact files exist for this machine because the collector was not run. `D1/in/part-gentoo.tsv` has only the required header and no object IDs.

Host lifecycle records (`D1/in/control/gentoo/host-lifecycle.txt`) report process exit 1, without a slot-shortage diagnostic. The specific startup cause remains unknown. The committed runner discards its worker stdout and stderr (`check-inputs-v4/lab.sh`, `start`).
