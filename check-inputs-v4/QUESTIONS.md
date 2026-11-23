# Questions for the author, recorded before the first observation

## 1. Is a second level obtained only in part “obtained”?

Section 9.2: “A machine on which the second-level inventory has not been obtained cannot yield 1: its outcome is 0 if
an object meeting the failure condition below is found on it, and ? otherwise.”

On Talos Linux the documented interface lists only part of the stored objects (see `TALOS-COLLECT.md`); on the other
systems the traversal is bounded where the collector documentation says so (`COLLECT.md`).

- Reading A: “obtained” means that second-level rows exist for the machine. A machine with a partial second level
  can then yield 1.
- Reading B: “obtained” means the whole second level. A machine with a partial second level then cannot yield 1.

The text does not say which. The inputs do not choose: the records of the check report, for every machine, what part
of the second level was obtained, and the outcome of such a machine is stated under both readings.
