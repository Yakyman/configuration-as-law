# Inventory frontend expectation

2026-11-22 UTC, before execution. The planting test exercises the census API as external root. A separate fresh final-image VM tests the actual ordinary-user entry: `broker<TAB>stand-inventory`. Expect structured object rows followed by `kind=summary`, `complete:false`, `p1:?`, and exit 1 or 2 (never a false clean-P1 success). This verifies the installed dispatcher, declared sudo authorization and output route, not another object-planting experiment. No private key payload is requested. The VM is destroyed after capture.
