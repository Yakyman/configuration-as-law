# Void operator launch notes

2026-11-23 UTC. The records-host verifier passed all 49 hashed published inputs before staging. The manifest itself is excluded from its own hash. The fixed inputs commit is `c62afbb5861fb038aa7da0aa00c0730ad140ec7c`.

A task-local laboratory root uses unchanged `check-inputs-v4/lab.sh`, the published S4 inputs, unchanged `check-inputs-v4/actions`, and links to the registered read-only base, existing keys/client/install resources and shared slot locks. The host orchestration runs in a durable user service. The initial service submission rejected the unexpanded working-directory syntax before starting any process; the subsequent submission supplied the expanded task directory. No machine creation, ordinary action or collector command was repeated.

The guest runs `bash void.sh` once in its unchanged action directory, as the ordinary account in a detached session. Monitoring reads only the completion sentinel. Each action's stdout and stderr are preserved separately by the committed helper. The entire fixed list runs before transport scaffolding is removed and collection begins. Network transport interruptions do not repeat actions.

The exact collector command and the cleanup command are recorded in `operate.py`; lifecycle/status evidence is in `status.json`. Review is external to this operator.
