# Evidence used for the independent opinion

Recorded 2026-11-23 UTC. Only the task's named local source files were read. No machines or runtime probes were started. The opinion is a document and logic review, not an additional inventory, a weighting decision, or an acceptance of another task. 

Local source identities, captured at 12:35 UTC, after reading the files:

| File | SHA-256 |
|---|---|
| (not published: orchestration or scratch) | `f400df36392dabc01622032f1ba0a2ccd33604f3665fd141854d7baa5e121775` |
| `TEXT.md` | `9870346d010b9dc5f68a3a2015d58e0d780a6769fd2db6d88b904373098ec38b` |
| `SENTENCES.md` | `2308d41811e98e98272e778cddd820cc3e2b19ca9022cd162a72f0ad81e9119b` |
| `PROTOCOL.md` | `6f8e958edd1a32fb7a021aa32d2f9aad6113c10ba917a2aed7f72926ed34adc3` |
| `A2/CARDS.md` | `3655132e7e5049b08adce5fe8682637e725e882221558b65f8d778bfb333a78e` |
| `A2/VERIFY.md` | `e377a2e1245f9c2cb5f4f0650fcaf04d17beb9ef598028d7cf422ef037286385` |
| `B1/RESULT.md` | `0426e479dcb5d37276440572b1e3bd072d813551e419676c32875ba584a9cfd3` |
| `B1/fix-b1-1/GAPS.md` | `f6033b705946747cccf03a2105ac791ba8542ce82d6d025edb57603640859348` |
| `D4/RESULT.md` | `187c5e2f6de20fc1d87f8e0ab9b5005c059749764ffbee7e2b1490ae4dbcabe0` |
| `D1/in/READY.md` | `c7d384b576442e60393b5ad0d1a5b60430279f15adf4f4ec72c4394b1ee8b909` |
| `D1/compare/STATS.md` | `6bb70a6e7bc41d32ff4fa05a43cdb45795a6972e6c775a861a80bbecbae9424c` |
| `A3/in/READY.md` | `7f96b0306314fdded9650c1e8ed7f293fe613ccd49b144b36992d05002dd9053` |
| `A3/compare/STATS.md` | `02bc0c758762409e87980697a771001a383fefbeb9a22e7ea8d4b8652f02443c` |
| `B2/STAND.md` | `00859fdfe59f5371755b8e3c1e82631344b34dfed5cb34dfaf2c94dc448830ed` |
| `B2/ROUNDS.md` | `aba217497172503a02432a28d4adab53beb30ce17e4e4b442122324d0140e67d` |
| `W0/RESULT.md` | `c5a42fe895ee296876df96a9bf94365146492e3ae58a0b29e7a9ab5879bebc0b` |

The linked raw records of those tasks were not independently re-audited. References in the opinion to their observations mean the observations reported in these named result files. Adjudication results arriving later are outside this evidence snapshot.

Three primary documentation sources were consulted to establish that the proposed situations are ordinary supported behavior. They do not establish that any existing system satisfies P1, P2 and P4.

1. **Automatic account identifiers.** [systemd 258 sysusers.d manual, ID](https://www.freedesktop.org/software/systemd/man/258/sysusers.d.html#ID), accessed 2026-11-23 UTC. Exact excerpt: “Specify \"-\" for automatic UID/GID allocation for the user or group”. The Description and Type sections place account creation at package installation or boot and create named accounts only if absent. These facts support a history-sensitive allocation example; the opinion does not claim to have measured a particular pair of installations.
2. **Offline directory state.** [SSSD troubleshooting, identity information](https://sssd.io/troubleshooting/basics.html#troubleshooting-identity-information), accessed 2026-11-23 UTC. Exact excerpt: “Do not remove the cache files if your system is offline and it relies on SSSD authentication!” The same page's illustrated failed provider request returns cached identity data. The inference in the opinion is that current remote state and usable cached local state can differ; no particular revocation latency is asserted.
3. **Hardware-dependent application builds.** [GCC x86 options, native](https://gcc.gnu.org/onlinedocs/gcc/x86-Options.html), accessed 2026-11-23 UTC. Exact excerpt: “Using -march=native enables all instruction subsets supported by the local machine”. This supports a possible hardware-caused difference in an ordinary application binary, beyond drivers, firmware and device files. Different checksums for any particular program were not measured.
