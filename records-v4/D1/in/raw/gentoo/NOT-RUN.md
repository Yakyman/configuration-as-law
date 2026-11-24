Inventory not obtained.

The single prescribed `lab.sh new d1-gentoo gentoo` attempt returned 1. Its exact diagnostic is `lab: VM failed to start` in `D1/in/control/gentoo/new.err`; stdout in `new.out` is empty. The runner does not supply a more specific cause in that output. No ordinary action or collector was run. `lab.sh destroy d1-gentoo` returned 0. Statuses: `D1/in/control/gentoo/status.json`. No retry or replacement was made.
