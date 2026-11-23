# Author question — scope of S2.5-1

Recorded 2026-11-22 UTC. No wording change or answer is proposed.

Does excluding **how to treat** program state from the definition also exclude the state objects themselves from the recording decisions in Section 2.2?

- Reading A: S2.5-1 leaves state-handling design open; S3-1 still directs coverage decisions to Section 2.2. On the established functions, the udev record has positive coverage and executable history, executable caches and operative history retain their Section 2.2 conflicts.
- Reading B: S2.5-1 excludes state objects themselves from coverage. This would also affect the cache/history cards, not just the udev record and four sampled bookkeeping rows. The sentence does not explicitly state that such objects need not be recorded.

The corrected audit withdraws S2.5-only NOT/OUTSIDE decisions rather than treating Reading B as an added exemption. Its coverage support counts and confirmed collisions report the literal Section 2.2 rules named by S3-1; they do not claim to settle this proposed broader reading for the author. No priority between contradictory Section 2.2 sentences has been supplied. A design choice about preserving, regenerating or transferring state is not itself counted as a hole.

- S2.5-1: “How to treat data and program state, the remains of removed programs, user authority, generations and rollback, the transfer of accumulated state to another computer, when an edit of the declaration takes effect, and how to protect the declaration itself and secrets are questions of the design of a system built on the hypothesis, not conditions of declarativeness.”
- S3-1: “Whether an object must be recorded. The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.”
