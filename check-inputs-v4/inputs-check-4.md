# Check 4 concrete inputs

Prepared 2026-11-23 UTC. These files are concrete pre-observation inputs. No classification or property assessment has been made. They must be committed before the first observation; this preparation does not assert that a repository commit exists. Readiness is an instrument result, not a hypothesis outcome.

| System | Release | Image checksum |
|---|---|---|
| nixos | 26.05 / 26.05.14979.94c3211b0ee8 | SHA256 `54034d71971b8937c8e5d85c252053be1a4e010d613d197ba3587dca7548618e` |
| guix | 1.5.0 | SHA256 `107e0a8082f03a10b15c1fb9383d2d752c1cdeda41b8db575a15550e1c2d8b4a` |

Release selection and checksum references are fixed in `releases.tsv`. Installation recipes are published as credential-free `.in` templates under `install/recipes/`. `install/materialize.py LAB_ROOT PUBLIC_KEY_FILE --previous-lab-root PREVIOUS_LAB_ROOT` reconstructs their relative paths, materializes explicit laboratory roots, and inserts the separately generated laboratory public key. The key material is excluded from publication; its digests are disclosed separately. Talos creates fresh credentials with its pinned release client; generated client/machine configurations are excluded. Historical failed recipes are retained and labelled by their README and CHOICES; they are not substitutes for active successful recipes.

NixOS uses the preserved declaration plus the successful instrument-access addition. Guix uses its unchanged original declaration and original serial access; failed SSH reconfigurations are historical inputs, not applied to its active base. `READY.md` records the twenty-call transport rehearsals and the Guix shutdown fallback. No collector or property probe runs on these two systems during rehearsal.

## Installation recipes

| File | SHA256 |
|---|---|
| `install/recipes/guix/KIT2.md.in` | `b9d8ce016b5a7d439488522e64dd26f10be3916b0e760f5efe46d74b64eca16a` |
| `install/recipes/guix/README.md.in` | `af05c92e99b94f947d56c4cef5a6a0117297c7fe88f9a05d0d2946e8e235647a` |
| `install/recipes/guix/access-ci.sh.in` | `84c34e6c882c6bb89b3663038fb2bbabbb2ec7a58aad9ab6a04cb29757d2521f` |
| `install/recipes/guix/access.sh.in` | `18a8ce1f540dd3f22bd8bd0eb9564228b936e2e335880315a67027abdd679df6` |
| `install/recipes/guix/bootstrap-attempt2.sh.in` | `5e72e0bed34f93b8bf74ab814eaa3acb4694c68b7f499d936733b96a12ad903e` |
| `install/recipes/guix/bootstrap-attempt3.sh.in` | `bc5696b841f5bab4309bae0a4061f20d55914719766f5a5e670c4458dc08641b` |
| `install/recipes/guix/bootstrap.sh.in` | `028cd6511a6f710aba377a7cbc50f3223f58241adac6afba79687187a1dfda85` |
| `install/recipes/guix/chroot-access-attempt1.sh.in` | `369c7cb45f540731279e54be3fa920f5c22608a79ece09f6b1b1d96b2439d73e` |
| `install/recipes/guix/chroot-access-attempt2.sh.in` | `4079ea0319744469278f85f2ec66bec7fe33ae30b507da483f3a190b9af4f404` |
| `install/recipes/guix/chroot-access-attempt3.sh.in` | `85ce6cde3c9221beb2b1fda34eba9fe636f2eba91639986e1668fe6f2ed02603` |
| `install/recipes/guix/chroot-access-attempt4.sh.in` | `a87e3bfb28025afe7da9cbc744c5847b8c1bc7de178817d3c0a9c2b317426e6c` |
| `install/recipes/guix/chroot-access-certs.sh.in` | `816133123f00199849e9e69a01fb6910c7a1feeb419e72ceb05d336466133409` |
| `install/recipes/guix/chroot-access.sh.in` | `a87e3bfb28025afe7da9cbc744c5847b8c1bc7de178817d3c0a9c2b317426e6c` |
| `install/recipes/guix/config.scm.in` | `7cb59a8f38ced54570419d4d02c0e1bb5443cf6c0621bf78b50b8bbf68efae9b` |
| `install/recipes/guix/kit2-base.json.in` | `01a8224860f7738643ce55f2c3fb67020ae414e2b076e71f943b40a0e87fc658` |
| `install/recipes/guix/kit2-passive.patch.in` | `630dd696c103ca1e544e21fd39d06bd7ce979f5ca5748718a9717c3460b7e300` |
| `install/recipes/guix/kit2-reuse.sh.in` | `b0dc737a20de79e888b9b240ca6241359b9febbb64849dc69f82d41426749059` |
| `install/recipes/guix/kit2-smoke.sh.in` | `09bf190149d91c225593f531cb06b97577d975ee0659b3f167dbb276116078b2` |
| `install/recipes/guix/original-config.scm.in` | `442f088ab713e68721c4156793f2316a04b785b1c8d8e6dffb11efe31726b886` |
| `install/recipes/guix/original-install.sh.in` | `cad0e6b9348a40db325e9025977e704a04463a3b6e30fe53ae92d824b51880a3` |
| `install/recipes/guix/recovery-activated.sh.in` | `67ca519ec82ab56d42fac6967bff58a4da780f5c1f8da3d5d0de3327e56b9343` |
| `install/recipes/guix/recovery-certs.sh.in` | `1a964be7c951017e23605e2f52d7162c21274c667f9f08c3fbc567ffaa082135` |
| `install/recipes/guix/recovery-final.sh.in` | `6b3d699bba59c1bb6510e5720b861dfe6225b45df50b1d75171c7a73b5754e0e` |
| `install/recipes/guix/recovery-first.sh.in` | `bd4fd37853fbdb4358f3a7976cf60a116dee575df8c6d9f281716eff1b678ed3` |
| `install/recipes/guix/recovery-worker.sh.in` | `29a2a8348750f02b3fc68168b931e29e9a36e5a965ec24b4a3a31ddfb6b49c9a` |
| `install/recipes/guix/recovery.sh.in` | `134087f017197b3ced19c84ae162675b59ac0acc506ee02629b88f2380a72c95` |
| `install/recipes/guix/ssh-login.sh.in` | `86f0fdcb97ba5f6319cd41f06f7a7bc1ee54d32df99b9a79fec7f34c0a4cf9d7` |
| `install/recipes/nixos/README.md.in` | `8547a432a586b908b0ad1b5de087f841e24e2f121ea62a191bcdd8f92fe5d5fa` |
| `install/recipes/nixos/access.sh.in` | `04d8b0a78b083dbec44eb8be1f8c006edb4206519ff96c4028d54d8f9298960b` |
| `install/recipes/nixos/configuration.nix.in` | `cc32fb3a4458b3f410c9fbcf49c06337f50025cf760983fafc3c973ad8daf0d5` |
| `install/recipes/nixos/original-configuration.nix.in` | `45f4f0c5de2b4bb4e49b6870915e7a66053f4feac30102d695778bc8737c9901` |
| `install/recipes/nixos/ssh-status.py.in` | `16b6f8b4b1c83f71671bc412da5a51d4293fc9c27078c60c85b2439ca6963c5c` |
| `install/materialize.py` | `d144d13a84dabfaadc7d97c897c7f3b92a2c49c9c59f8eecf9ed80adedbb3262` |
| `lab.sh` | `3402697b02c88449fd6ba41e7137c404185c43a2bcd45fa211623d0d7e349733` |

## Facts for the three properties

Appendix A.4.5 names exactly these facts, applied to the three properties of Section 8.3:

- P1: whether objects that must be recorded can be in force without being recorded.
- P2: whether recorded lines are in force after application.
- P4: whether a built-in tool can change, past the declaration, what must be recorded.

The cases are NixOS/P1, NixOS/P2, NixOS/P4, Guix/P1, Guix/P2 and Guix/P4. Each is assessed twice independently from documentation and a clean installation, with a source or experimental record. A finding that a system lacks a property is a successful assessment, not check failure. The sufficiency rule, adjudication and outcomes are exactly Appendix A.4.5; no property has been assessed here.
