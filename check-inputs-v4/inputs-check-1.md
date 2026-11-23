# Check 1 concrete inputs

Prepared 2026-11-23 UTC. These files are concrete pre-observation inputs. No classification or property assessment has been made. They must be committed before the first observation; this preparation does not assert that a repository commit exists. Readiness is an instrument result, not a hypothesis outcome.

| System | Release | Image checksum |
|---|---|---|
| alma | 10.3 | SHA256 `f74ae9c4a8e7e3e70147534856ea276f71649d16c70b7d3ec80d0905a7b93982` |
| void | 20250202 (rolling-release installation image) | SHA256 `0f7439f500740f62dd18972cae448cec7d8a85032c7eb8f1bf946100d9a92161` |
| gentoo | stage3-amd64-openrc-20261122T164601Z | SHA512 `df8c3d560dd0bcfd6fea5b8c1bf5f4e60ef081219f7421d791d26a36004dd9aaa7ef885ec9aeb9024c56a12296f7792ff7c445e538f67891d68abf14a0477bd5` |
| microos | Snapshot20261121 plain x86_64 KVM/XEN image | SHA256 `fd2d22de41741d042a1b9c6a993fc9fa296ec1312083f14ea8dc0d4e58ce5826` |
| talos | 1.14.6 | SHA256 `c2264437db0ea7949771ce941940a95e049ce4e84f7b1860be067834137b8f23` |

Release URLs, published checksum references, cutoff and verification provenance are fixed in `releases.tsv`. The cutoff is 2026-11-23T01:19:00Z. The existing installer-choice record is fixed in `CHOICES.md`; review finding 8 identifies missing image-variant rationales, disclosed in `FIX-C1-REH-1.md` without changing that record. No new workload choice is inferred from guest contents.

Availability and rehearsal acceptance are reported in `READY.md`. All five systems remain the prescribed case list. A system that is not ready has not been silently removed from the check. Late-system preparation uses the final KIT2 inputs when available; readiness is stated explicitly in the accompanying table.

Installation recipes are published as credential-free `.in` templates under `install/recipes/`. `install/materialize.py LAB_ROOT PUBLIC_KEY_FILE --previous-lab-root PREVIOUS_LAB_ROOT` reconstructs their relative paths, materializes explicit laboratory roots, and inserts the separately generated laboratory public key. The key material is excluded from publication; its digests are disclosed separately. Talos creates fresh credentials with its pinned release client; generated client/machine configurations are excluded. Historical failed recipes are retained and labelled by their README and CHOICES; they are not substitutes for active successful recipes.

## Installation recipes

| File | SHA256 |
|---|---|
| `install/recipes/alma/README.md.in` | `58d518c00e8d2fdf9393e87c1ea9c8e9756dead9572527cc9c0326c0e9a2b4bf` |
| `install/recipes/alma/download.sh.in` | `31e0d1693ca215e38c21e81c34e4e9a43266cfc556216d49825fd2620a051a2a` |
| `install/recipes/alma/finish.sh.in` | `4ac8860bb697c111eb7ea6bf8525ae4eb8f8719943de30ea1894d4771d448e38` |
| `install/recipes/alma/install.sh.in` | `93ebc306f4543782ce939e073c1a95a2b6bb7e04bc24d5ef95dd196af8fa54d8` |
| `install/recipes/alma/ks.cfg.in` | `808b4ebb6749760e5f64eaf7d230d2a7a76374127d16ffe1166cf64ce9b3ca57` |
| `install/recipes/alma/queue-install.sh.in` | `2d4e138bc225cee7361f7ed6db53e399d498441808ecc5b4928720f6925bd398` |
| `install/recipes/gentoo/README.md.in` | `094bded7390cd606b430db373074b114f07f424d9a7e885bac1e067da9c0522e` |
| `install/recipes/gentoo/align-bios-mbr.sh.in` | `55d1b46b7986213ba4b9bb90d833114fb7574751f5111130d0d60cf6ca54ddf7` |
| `install/recipes/gentoo/attempt1-20261123.sh.in` | `e6a4b233b88068bf1419c2ebc7abbd059cab97f0cdcac9c4660dde07179413f1` |
| `install/recipes/gentoo/attempt2-20261123.sh.in` | `90368a53243071a208023a719879f13c4130811fee53bb0d7973db208ce811df` |
| `install/recipes/gentoo/extend-host-deadline.py.in` | `91fdffcb924ef79aa027056ff25d7bef98812f1d8575a39194c1f39417943894` |
| `install/recipes/gentoo/finalize-first-20261123.sh.in` | `6c81f98b64f27e67cde18aa9b50a1ecb928d6a4519ff4272843ab7dad2ca28e0` |
| `install/recipes/gentoo/finalize-second-20261123.sh.in` | `1728bb2f20e6bff6192870054f3b474072dced933d70b2b059030cd371e78a84` |
| `install/recipes/gentoo/finalize.sh.in` | `f1dd6ce6daf1fc5b0408207ff970dfb258aa0805548d7441bb1417da788c3e9a` |
| `install/recipes/gentoo/install.sh.in` | `a6b8f57b5f3f7daa25e8e30d951dd287e6bd9ecc112768c45138b6d8c1c76e27` |
| `install/recipes/gentoo/pin-repository.sh.in` | `596f484b3e3952873b06d436dbc104b389ff5b93df0ded25c7c2001a8898a9aa` |
| `install/recipes/gentoo/remount.sh.in` | `2c7d6bcdb79087c15794d5dd51cf255f8f7581c1537239af5f8935d81e341637` |
| `install/recipes/gentoo/resume-first-20261123.sh.in` | `9f4a2703dcbcfa0137ccbcc74752f19c287e6754a1f774e6864d448658921e11` |
| `install/recipes/gentoo/resume-interrupted-build.sh.in` | `83a56e4f78c55b65d448e2297ce9d46fbd1c559dd1ce48ae5c9662faa71570fb` |
| `install/recipes/gentoo/resume.sh.in` | `881a8bf1032cef9d7c0c84970b2cfd4be365e7b64a81eb083710f0ba3d59b7f9` |
| `install/recipes/gentoo/start-bootstrap.sh.in` | `b45848effa9c73150fd62991d43cee1e299d4097bdab99bd61fbbf587b4a97e6` |
| `install/recipes/gentoo/verify-image.sh.in` | `aa994ad77c26678bbac9b6dc7fc2a1743def4fe7a0351164fab3a30445977684` |
| `install/recipes/gentoo/verify-snapshot.sh.in` | `83accb75aa8b59b550567a2de877f6f0336efdd0d465bbc007d3dfd25acb5b75` |
| `install/recipes/microos/README.md.in` | `b6b431613a1accd49bc332def1ab749716dde92daec2d163dfdf57e77327dbfc` |
| `install/recipes/microos/attempt-1/autoinst.xml.in` | `290eacdcee437f89cc087e2272c96bd9b8a88accc6acef69df4fbf0466922f05` |
| `install/recipes/microos/attempt-1/combustion.template.in` | `14b65ae6075eb9fef205657b3a5563128415a96066deb069ef14309480bc5fca` |
| `install/recipes/microos/attempt-1/install.sh.in` | `2ee080727c58edc747f9d9494016fd7445003377d68aff7edffa5cb293a3b65a` |
| `install/recipes/microos/attempt-2/autoinst.xml.in` | `b6e7152b85ec90d88fd454008d893c5bb9dd1757cbcb632f74e7d72b05fa0b53` |
| `install/recipes/microos/attempt-2/combustion.template.in` | `a34e8423d46ce7c6ca5b8571d4d78947f4b42dfba17006ec2ac396456d0a5226` |
| `install/recipes/microos/attempt-2/install.sh.in` | `c06ff470420f1786c6cc49d6741ffc0ce832fb548ff4c0394e4ce8daaae4cace` |
| `install/recipes/microos/attempt-3/autoinst.xml.in` | `ab8ed16781aebbce7d897d3fc4b3a74fcc00cc9a53ce936d6dfb8c270697bc56` |
| `install/recipes/microos/attempt-3/combustion.template.in` | `a34e8423d46ce7c6ca5b8571d4d78947f4b42dfba17006ec2ac396456d0a5226` |
| `install/recipes/microos/attempt-3/install.sh.in` | `bfde85c96410bf58527bfa6d0d86ecb8083f027662b7819e6f9da7a049d781c1` |
| `install/recipes/microos/attempt-4/autoinst.xml.in` | `79e5dc49abdd22c3adad2c1d13a250f2f464bec78e1ccb2c2d534ff54b33483d` |
| `install/recipes/microos/attempt-4/combustion.template.in` | `858418bc3e2d57cbef516729a5be522c05b2608fb1a243d51fa9827c783b62c9` |
| `install/recipes/microos/attempt-4/install.sh.in` | `7fef4455740d244f67deaa9785ff79fd0c4c8865162743fd327213b48748a5f9` |
| `install/recipes/microos/attempt-5/autoinst.xml.in` | `907feb4ec55e12caedbc80b79a1cd6d4b6bfa990b6c1d787fe99332575d43b6e` |
| `install/recipes/microos/attempt-5/combustion.template.in` | `9034fa1ade19e4589ccd341c44d3c532868009658ac81c4fabf44208f116ad97` |
| `install/recipes/microos/attempt-5/install.sh.in` | `7fef4455740d244f67deaa9785ff79fd0c4c8865162743fd327213b48748a5f9` |
| `install/recipes/microos/autoinst.xml.in` | `9b8c35ae845a082b6ae69fce8b286a665e4ddaf4362a5925e5346630677f3208` |
| `install/recipes/microos/combustion.in` | `267133f566f1f16838fbe324c777485e464076a500bae24ed8b0e4e18c285954` |
| `install/recipes/microos/combustion.template.in` | `9034fa1ade19e4589ccd341c44d3c532868009658ac81c4fabf44208f116ad97` |
| `install/recipes/microos/download.sh.in` | `a5dd87ce807970915d0c89617a02ef5e62dcec1128fc3cf0930e6279236aa4b5` |
| `install/recipes/microos/install.sh.in` | `7fef4455740d244f67deaa9785ff79fd0c4c8865162743fd327213b48748a5f9` |
| `install/recipes/microos/kit2/README.md.in` | `8f41c376800e33697f63bbd9131cfea15fe71b17cd48194b5da5dc31ca457e3e` |
| `install/recipes/microos/kit2/acquire.sh.in` | `d8fb767bc1366186f907ce802bddda4e9f03a84292f35c9f15056b4d4f69a54d` |
| `install/recipes/microos/kit2/attempt-1/boot.sh.in` | `dc7d5739835359f63bec1a113d8b1ced144416464849625e634fe2f128bfb963` |
| `install/recipes/microos/kit2/attempt-1/combustion.in` | `17effc757f60de66855e42436cf84348df46e9ce69bfda9a337d80b6398de841` |
| `install/recipes/microos/kit2/attempt-1/combustion.template.in` | `f0850aa508086b22a823da25a6a86cdddb08294283123dbfe21cd79efa98dfc9` |
| `install/recipes/microos/kit2/attempt-2/boot.sh.in` | `aee0a7876c4f038ae341c6222425f3b2f7728e69d331f985e2698f2859fadf62` |
| `install/recipes/microos/kit2/attempt-2/combustion.in` | `7c2788f3588fd918643667013d5588c48063bd32c46660f87c68570350bdd54f` |
| `install/recipes/microos/kit2/attempt-2/combustion.template.in` | `36fc193eaca9de3d5f6a6b82916683f871bc713fe95437e973deed37e548632e` |
| `install/recipes/microos/kit2/attempt-2/prepare.sh.in` | `47ae2d0477f12f4168754bff66160267424db0ba0716ecbc0a3dc00aac223305` |
| `install/recipes/microos/kit2/attempt-3/boot.sh.in` | `c07f381685a1f094e500b5821472af180b2d53fa080771b9a1c46bcffc2f8f73` |
| `install/recipes/microos/kit2/attempt-3/combustion.in` | `6fb7802b08108f2a26d2b809d7f54d96732c12d53ca9c6ef5bbc9bb6ed56aa6e` |
| `install/recipes/microos/kit2/attempt-3/combustion.template.in` | `52945018337620ec736e02237b5e8b6fff595bddc3a261654059f4280abe0897` |
| `install/recipes/microos/kit2/attempt-3/prepare.sh.in` | `8aece750c13f85c725d2e8ccef5a518c9c54a9cf6cef530f3210404411d7ca92` |
| `install/recipes/microos/kit2/attempt-4/boot.sh.in` | `1751d6002a2bf9787d6bc7ca2fc343006ae9540da1122bf33e2cfa46e221017c` |
| `install/recipes/microos/kit2/attempt-4/combustion.in` | `0b773f8a0d820e974736610cae40feb61bb9663db9dedc1e9ffc5f4ab1976ed0` |
| `install/recipes/microos/kit2/attempt-4/combustion.template.in` | `0bc1f5cedbc4fc8a8e872e68ad03c7288a4e2c3bd2374d44d019150cc874696a` |
| `install/recipes/microos/kit2/attempt-4/prepare.sh.in` | `d79178f1de37496be20574099280b31b4616c02486f5ba3a3a1830e61e85fc99` |
| `install/recipes/microos/kit2/attempt-5/boot.sh.in` | `ccde6aa2d6043c9d4439cbbca0b0cea5ab6315bd2e9c2fc6cbaf8dbc81be4d49` |
| `install/recipes/microos/kit2/attempt-5/combustion.in` | `ce0cacb7c8f6a7784a5e208ecf587b72c576a131a680c8643cbd0818a86e8b7c` |
| `install/recipes/microos/kit2/attempt-5/combustion.template.in` | `834b1e49edac47fc105da66ffc6936818be9c8313f71c2b0d4a282fb1db89740` |
| `install/recipes/microos/kit2/attempt-5/prepare.sh.in` | `ae3477ba02f420dadf77fc8fc22a0903bae8d6e7fbfb17ee42affe57b36eea6d` |
| `install/recipes/microos/kit2/attempt-5/register.sh.in` | `c4303853db0a188c763d11f2f414fb816639fa11eaf479c2b686a9744f70da55` |
| `install/recipes/microos/kit2/attempt-5/validate.sh.in` | `dca078a571e6060b676bcf2a1fad69a884ec1fe0eace4d74feb94b4020f40c9f` |
| `install/recipes/microos/kit2/attempt-6/base.json.in` | `6e485063e6f3ffdd62dbc6de2c077a8a9550f58899f412c9a1bddfa7585ee7b2` |
| `install/recipes/microos/kit2/attempt-6/boot.sh.in` | `f910ef645f9afb9c29408bb8946aede5613491c40d25b7138e4942e6b7fe0c4f` |
| `install/recipes/microos/kit2/attempt-6/combustion.in` | `ce0cacb7c8f6a7784a5e208ecf587b72c576a131a680c8643cbd0818a86e8b7c` |
| `install/recipes/microos/kit2/attempt-6/combustion.template.in` | `834b1e49edac47fc105da66ffc6936818be9c8313f71c2b0d4a282fb1db89740` |
| `install/recipes/microos/kit2/attempt-6/prepare.sh.in` | `5f3914269d9ed80bc983a74fc202111f967eac9d241e8e102466f1012982aa64` |
| `install/recipes/microos/kit2/attempt-6/register.sh.in` | `f53433c2ed2098bb6d95b35f10eb64bf97c10335289b4fac59ebab40f3703e06` |
| `install/recipes/microos/kit2/attempt-6/validate.sh.in` | `efe02389b6b068318e1cb0da8cde45e3cb4fcea611d5c79c9fb2955128ae2968` |
| `install/recipes/microos/kit2/boot.sh.in` | `aee0a7876c4f038ae341c6222425f3b2f7728e69d331f985e2698f2859fadf62` |
| `install/recipes/microos/kit2/combustion.in` | `7c2788f3588fd918643667013d5588c48063bd32c46660f87c68570350bdd54f` |
| `install/recipes/microos/kit2/combustion.template.in` | `36fc193eaca9de3d5f6a6b82916683f871bc713fe95437e973deed37e548632e` |
| `install/recipes/microos/kit2/prepare.sh.in` | `47ae2d0477f12f4168754bff66160267424db0ba0716ecbc0a3dc00aac223305` |
| `install/recipes/microos/kit2/register.sh.in` | `c4303853db0a188c763d11f2f414fb816639fa11eaf479c2b686a9744f70da55` |
| `install/recipes/microos/kit2/validate.sh.in` | `dca078a571e6060b676bcf2a1fad69a884ec1fe0eace4d74feb94b4020f40c9f` |
| `install/recipes/microos/prepare.sh.in` | `7af2ee1fce5933be5f16f861e6397983ba6a88177a833815060eb10419939c7c` |
| `install/recipes/microos/verify.sh.in` | `56bb0914c47a1b3fcefef0a02513c66048b59a9381cd504374ca324a516a85ec` |
| `install/recipes/talos/README.md.in` | `c5c70ffb91df797c661fc388ddc8b5630691cdf84f2f953b54415ab0cd680280` |
| `install/recipes/talos/attempt1/install.py.in` | `9332fbc0ebf4aa49691965572113520d0eb119b25036ae06f0ea781f1c6b925c` |
| `install/recipes/talos/attempt1-install.py.in` | `9332fbc0ebf4aa49691965572113520d0eb119b25036ae06f0ea781f1c6b925c` |
| `install/recipes/talos/install.py.in` | `9db7efd823d84ac2e4c1a2f4ce542872da2f246bae8905fd34b62e91934a4224` |
| `install/recipes/talos/interpreter-smoke.py.in` | `879ba8fff91c91a89c2519eb45238c9722b5c72655c4ab50f7eff6fdb6601158` |
| `install/recipes/talos/smoke.py.in` | `fc9ce4302914097ab53fbb2fd6d00a1885e035e6c5d0915305b316b2734f4ffa` |
| `install/recipes/talos/verify.sh.in` | `77bdcda3f76a2d11db9aa58cccd6bd098b44598f09092f54875f5ee6b8d41510` |
| `install/recipes/void/README.md.in` | `5ebc41e5a69961c9dcf037237ca0a040a09f807916941318c9224ab400278dd3` |
| `install/recipes/void/access-correction.sh.in` | `7141c0accb34e0a40730ad59b2ed603deeab8676f696039d0593077d26cb0239` |
| `install/recipes/void/console-bootstrap.py.in` | `9f24425673d1043f95ecfe25f6bb52b3bc500f8f1c1cc1ef6d4ab265cb30cee2` |
| `install/recipes/void/dialog.in` | `39f5fbbd2f3a9e34f9dc6aca4f3adc3eb1cd7a9186adc11a3bb56f90b5e23d2c` |
| `install/recipes/void/download.sh.in` | `c2e5b87c5f294dbe6e2d830afefcdaa4ebb6122932ab47dfb714cc39c4ff59db` |
| `install/recipes/void/install-original.sh.in` | `794ca446dc739c59a1a7e46d54e9ec09faf551b894878bf3481dbfb6bf281e34` |
| `install/recipes/void/install.sh.in` | `6d022a482939e3dab8005c9f5003a1f742d59b1a91701156f191bc014a72a41f` |
| `install/recipes/void/start-installer.sh.in` | `41a7f03d053827e1bb6265dec72d27c3aff48e80957774bd9b4e6b20eda90f4f` |
| `install/materialize.py` | `d144d13a84dabfaadc7d97c897c7f3b92a2c49c9c59f8eecf9ed80adedbb3262` |

## Ordinary actions and exact commands

Only AlmaLinux, Void and Gentoo receive ordinary actions. Their nine activities remain the exact Section 9.2 categories. The system entry scripts below specify the selected programs and commands, including disclosed same-category replacements needed for unattended execution. `DISCLOSURES.md` records each repair and replacement. Instrument synchronization changes retain the same activity; every change is disclosed.

Stage the action directory in a fresh clone and invoke as the ordinary account `user`: `bash alma.sh`, `bash void.sh`, or `bash gentoo.sh`. The launcher in `rehearsal/fx-run.py` supplies a detached session so network changes cannot terminate the batch. These are the exact script sources and hashes, including shared helpers:

| File | SHA256 |
|---|---|
| `actions/alma.sh` | `788a1f4df09bbdb9b1e2b97ff110a78028223584201e29dd578730acf34f5058` |
| `actions/void.sh` | `cfc2cb80b337d50884b3eb122902337c8c871fdb3e2094595b8560ad6bbf6937` |
| `actions/gentoo.sh` | `3032aada829426a29c8d929e7be3e8321ac63202bb5cb82976d652c59eb82476` |
| `actions/ordinary.sh` | `4b56b87b80a0242733051287e43821d8971630be2537b2044dd3c45d866c0180` |
| `actions/lib.sh` | `e28b8797039ef632af2f43c4c661007dd04a5ffa2ff5ece1cfc61312420771a4` |
| `actions/firefox-addon.py` | `c1bf38d199226ab4560973936566b6c90305f9274cc9ef555eb29c817bb5fe92` |
| `actions/gentoo-firefox-addon.py` | `566d82cd4e0b17b4bedcabe65387a7ce09287c3389de79cbb1c2b56853b19d84` |
| `actions/ordinary.md` | `c1018333468a319db1b5ad1734adca8e2e58860feb284147dde938facf6eed94` |
| `actions/README.md` | `4210b4e4954bd48d07675e34856a652e71335d77af365129bbee71b0a2013dc8` |

### actions/alma.sh

```bash
#!/usr/bin/env bash
ACTIONS_DIR=$(dirname "$(readlink -f "$0")")
source "$ACTIONS_DIR/lib.sh"
source "$ACTIONS_DIR/ordinary.sh"
PACKAGE_LIMIT=1800
BROWSER_LIMIT=1800

native_install() {
    # https://dnf.readthedocs.io/en/latest/command_ref.html
    case "$1" in
        tree) root dnf -y install tree ;;
        flatpak) root dnf -y install flatpak ;;
        node) root dnf -y install nodejs npm ;;
        browser) root dnf -y install firefox python3 python3-pip ;;
        git) root dnf -y install git ;;
        network) root dnf -y install NetworkManager ;;
        ssh) root dnf -y install openssh-clients ;;
        container) root dnf -y install podman ;;
        *) return 64 ;;
    esac
}
user_service() {
    # https://man.openbsd.org/ssh-agent
    # https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html
    # https://www.freedesktop.org/software/systemd/man/latest/systemctl.html
    native_install ssh
    mkdir -p "$HOME/.config/systemd/user"
    cat > "$HOME/.config/systemd/user/cal-user.service" <<'UNIT'
[Unit]
Description=User authentication agent
[Service]
ExecStart=/usr/bin/ssh-agent -D -a %t/cal-agent.sock
Restart=on-failure
[Install]
WantedBy=default.target
UNIT
    systemctl --user daemon-reload
    systemctl --user enable --now cal-user.service
    systemctl --user is-active --quiet cal-user.service
}
start_network_manager() {
    root systemctl enable --now NetworkManager.service
}
container_run() {
    # https://docs.podman.io/en/latest/markdown/podman-run.1.html
    native_install container
    root podman run --name cal-container docker.io/library/busybox:1.37.0 /bin/echo ordinary-container
}
actions_main "$@"
```

### actions/void.sh

```bash
#!/usr/bin/env bash
ACTIONS_DIR=$(dirname "$(readlink -f "$0")")
source "$ACTIONS_DIR/lib.sh"
source "$ACTIONS_DIR/ordinary.sh"
PACKAGE_LIMIT=2400
BROWSER_LIMIT=2400

native_install() {
    # https://docs.voidlinux.org/xbps/index.html
    # https://man.voidlinux.org/xbps-install.1
    case "$1" in
        tree)
            # XBPS requires its own update transaction before newer repositories.
            # https://github.com/void-linux/xbps/blob/master/bin/xbps-install/transaction.c
            root xbps-install -Suy xbps
            root xbps-install -Suy
            root xbps-install -Sy tree ;;
        flatpak) root xbps-install -Sy flatpak ;;
        # Update installed C++ and SQLite runtimes explicitly: current Node
        # needs a newer C++ ABI and SQLite session support.
        # xbps-install(1): named installed packages are updated from repositories.
        node) root xbps-install -Sy nodejs 'libstdc++' sqlite ;;
        browser) root xbps-install -Sy firefox python3 python3-pip ;;
        git) root xbps-install -Sy git ;;
        network) root xbps-install -Sy NetworkManager dbus ;;
        ssh) root xbps-install -Sy openssh ;;
        container) root xbps-install -Sy docker ;;
        *) return 64 ;;
    esac
}
language_step() {
    local label=$1 start finish rc
    shift
    start=$(date +%s)
    set +e
    "$@"
    rc=$?
    set -e
    finish=$(date +%s)
    printf '%s\t%d\t%d\n' "$label" "$rc" "$((finish-start))" >> "$HOME/actions-status.tsv"
    return "$rc"
}
language_program() {
    language_step language_install_node native_install node
    # A project lock retains npm's direct/dependency installation records.
    language_step language_npm_install npm install --prefix "$HOME/.local" cowsay
    language_step language_cowsay "$HOME/.local/node_modules/.bin/cowsay" cal-test
}
wait_supervisor() {
    # runsvdir scans for new services at least every five seconds.
    # https://man.voidlinux.org/runsvdir.8
    # sv fails immediately if no supervisor owns the service yet.
    # https://man.voidlinux.org/sv.8
    local attempt
    for attempt in {1..30}; do
        root test -p "$1/supervise/ok" && return 0
        sleep 1
    done
    return 124
}
user_service() {
    # https://man.openbsd.org/ssh-agent
    # https://docs.voidlinux.org/config/services/user-services.html
    # https://docs.voidlinux.org/config/services/index.html
    native_install ssh
    mkdir -p "$HOME/service/cal-user" "$HOME/.ssh"
    chmod 700 "$HOME/.ssh"
    cat > "$HOME/service/cal-user/run" <<'RUN'
#!/bin/sh
exec ssh-agent -D -a "$HOME/.ssh/cal-agent.sock"
RUN
    chmod 755 "$HOME/service/cal-user/run"
    local config
    config=$(mktemp)
    cat > "$config" <<'RUN'
#!/bin/sh
export USER=user
export HOME=$(getent passwd "$USER" | cut -d: -f6)
groups=$(id -Gn "$USER" | tr ' ' ':')
exec chpst -u "$USER:$groups" runsvdir "$HOME/service"
RUN
    install_root_file "$config" /etc/sv/runsvdir-user/run 755
    rm "$config"
    root ln -s /etc/sv/runsvdir-user /var/service/runsvdir-user
    wait_supervisor /var/service/runsvdir-user
    root sv -w 30 up /var/service/runsvdir-user
    wait_supervisor "$HOME/service/cal-user"
    sv -w 30 up "$HOME/service/cal-user"
}
start_network_manager() {
    # Void explicitly requires disabling competing network services first.
    # https://docs.voidlinux.org/config/network/networkmanager.html
    # The clean guest primary NIC uses DHCP; NetworkManager adopts it.
    local service
    for service in dhcpcd wpa_supplicant wicd; do
        if [[ -L /var/service/$service ]]; then
            root sv -w 30 down "/var/service/$service"
            root rm "/var/service/$service"
        fi
    done
    for service in dbus NetworkManager; do
        if [[ ! -e /var/service/$service ]]; then
            root ln -s "/etc/sv/$service" "/var/service/$service"
        fi
        wait_supervisor "/var/service/$service"
        root sv -w 30 up "/var/service/$service"
    done
}
container_run() {
    # https://raw.githubusercontent.com/void-linux/void-packages/master/srcpkgs/docker-cli/template
    # https://docs.docker.com/reference/cli/docker/container/run/
    # https://docs.voidlinux.org/config/services/index.html
    native_install container
    if [[ ! -e /var/service/docker ]]; then root ln -s /etc/sv/docker /var/service/docker; fi
    wait_supervisor /var/service/docker
    root sv -w 60 up /var/service/docker
    # The daemon process can start before its API is ready.
    # https://docs.docker.com/reference/cli/docker/info/
    local attempt ready=0
    for attempt in {1..60}; do
        if root docker info >/dev/null 2>&1; then ready=1; break; fi
        sleep 1
    done
    (( ready == 1 ))
    root docker run --name cal-container docker.io/library/busybox:1.37.0 /bin/echo ordinary-container
}
actions_main "$@"
```

### actions/gentoo.sh

```bash
#!/usr/bin/env bash
ACTIONS_DIR=$(dirname "$(readlink -f "$0")")
source "$ACTIONS_DIR/lib.sh"
source "$ACTIONS_DIR/ordinary.sh"
PACKAGE_LIMIT=600
BROWSER_LIMIT=420

native_install() {
    # Source builds, using the prepared clean guest's Portage profile and USE flags.
    # https://wiki.gentoo.org/wiki/Handbook:AMD64/Working/Portage
    case "$1" in
        tree) root emerge --ask=n --noreplace app-text/tree ;;
        flatpak) root emerge --ask=n --noreplace sys-apps/flatpak ;;
        node) root emerge --ask=n --noreplace net-libs/nodejs ;;
        browser) root emerge --ask=n --noreplace www-client/firefox dev-python/pip ;;
        git) root emerge --ask=n --noreplace dev-vcs/git ;;
        network) root emerge --ask=n --noreplace net-misc/networkmanager ;;
        ssh) root emerge --ask=n --noreplace net-misc/openssh ;;
        container) root emerge --ask=n --noreplace app-containers/docker app-containers/docker-cli ;;
        *) return 64 ;;
    esac
}
user_service() {
    # https://man.openbsd.org/ssh-agent
    # Requires current OpenRC with user mode; missing user runtime state is created below.
    # https://github.com/OpenRC/openrc/blob/master/user-guide.md
    # https://github.com/OpenRC/openrc/blob/master/service-script-guide.md
    native_install ssh
    # Headless SSH may lack a PAM-created runtime directory. Create the user
    # runtime directory for native OpenRC user state; no service emulation.
    export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
    root install -d -m 700 -o "$(id -u)" -g "$(id -g)" "$XDG_RUNTIME_DIR"
    mkdir -p "$HOME/.config/rc/init.d" "$HOME/.config/rc/runlevels/default"
    cat > "$HOME/.config/rc/init.d/cal-user" <<'RC'
#!/sbin/openrc-run
description="User authentication agent"
command=/usr/bin/ssh-agent
command_args="-D -a ${XDG_RUNTIME_DIR}/cal-agent.sock"
command_background=true
pidfile="${XDG_RUNTIME_DIR}/cal-user.pid"
RC
    chmod 755 "$HOME/.config/rc/init.d/cal-user"
    rc-update --user add cal-user default
    openrc --user default
    rc-service --user cal-user status
}
start_network_manager() {
    # https://wiki.gentoo.org/wiki/NetworkManager
    # https://wiki.gentoo.org/wiki/Handbook:AMD64/Working/Initscripts
    # Migrate the DHCP primary NIC from netifrc/dhcpcd if present.
    local service
    for service in /etc/init.d/net.* /etc/init.d/dhcpcd; do
        [[ -e $service ]] || continue
        service=${service##*/}
        [[ $service != net.lo ]] || continue
        if root rc-service "$service" status >/dev/null 2>&1; then root rc-service "$service" stop; fi
        if [[ -L /etc/runlevels/default/$service ]]; then root rc-update del "$service" default; fi
        if [[ -L /etc/runlevels/boot/$service ]]; then root rc-update del "$service" boot; fi
    done
    root rc-update add dbus default
    root rc-service dbus start
    root rc-update add NetworkManager default
    root rc-service NetworkManager start
}
container_run() {
    # https://docs.docker.com/reference/cli/docker/container/run/
    # https://wiki.gentoo.org/wiki/Handbook:AMD64/Working/Initscripts
    native_install container
    root rc-update add docker default
    root rc-service docker start
    root docker run --name cal-container docker.io/library/busybox:1.37.0 /bin/echo ordinary-container
}
# Same-category alternatives evaluated after the bounded source-build rehearsal.
application_package() {
    # https://github.com/pkgforge-dev/Firefox-AppImage: self-contained AppImage.
    # A user application package does not enable a binary Portage package host.
    mkdir -p "$HOME/.local/opt" "$HOME/.local/bin"
    python3 - <<'FETCH_FIREFOX'
from pathlib import Path
import urllib.request
url = 'https://github.com/pkgforge-dev/Firefox-AppImage/releases/download/160.0.1%402026-11-20_1795187897/Firefox-160.0.1-anylinux-x86_64.AppImage'
with urllib.request.urlopen(url, timeout=180) as response:
    with (Path.home() / '.local/opt/firefox.AppImage').open('wb') as target:
        while block := response.read(1024 * 1024):
            target.write(block)
FETCH_FIREFOX
    printf '%s  %s\n' '5fa35b88256946ac33e7f92c93eaa6ce21a68b4365ce216c3a526856aefd7c24' \
        "$HOME/.local/opt/firefox.AppImage" | sha256sum --check
    chmod 755 "$HOME/.local/opt/firefox.AppImage"
    cat > "$HOME/.local/bin/firefox" <<'FIREFOX'
#!/bin/sh
export APPIMAGE_EXTRACT_AND_RUN=1 DISABLE_AUTO_UPDATES=1
exec "$HOME/.local/opt/firefox.AppImage" "$@"
FIREFOX
    chmod 755 "$HOME/.local/bin/firefox"
    "$HOME/.local/bin/firefox" --version
}
language_program() {
    # https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-t
    root emerge --ask=n --noreplace dev-python/pip
    python3 -m pip install --no-input --target "$HOME/.local/lib/cal-cowsay" cowsay
    PYTHONPATH="$HOME/.local/lib/cal-cowsay" python3 -m cowsay -t cal-test
}
browser_extension() {
    root emerge --ask=n --noreplace dev-python/pip
    python3 -m pip install --no-input --target "$HOME/.local/lib/cal-marionette" marionette_driver
    export PATH="$HOME/.local/bin:$PATH"
    mkdir -p "$HOME/.mozilla/firefox/cal-check" "$HOME/Downloads"
    firefox --headless -CreateProfile "cal-check $HOME/.mozilla/firefox/cal-check"
    PYTHONPATH="$HOME/.local/lib/cal-marionette" python3 "$ACTIONS_DIR/gentoo-firefox-addon.py"
}
network_connection() {
    # Same Section 9.2 network connection via the installed DHCP client.
    # https://man.archlinux.org/man/dhcpcd.8.en
    local device interface=''
    for device in /sys/class/net/*; do
        if [[ $(cat "$device/address") == 52:54:00:ca:10:02 ]]; then
            interface=${device##*/}
            break
        fi
    done
    [[ -n $interface ]] || return 79
    mkdir -p "$HOME/.config"
    cat > "$HOME/.config/cal-secondary-dhcpcd.conf" <<CONF
interface $interface
nogateway
noipv4ll
nohook resolv.conf,hostname
CONF
    root ip link set "$interface" up
    root dhcpcd --config "$HOME/.config/cal-secondary-dhcpcd.conf" \
        --ipv4only --waitip=4 --timeout 90 "$interface"
    ip -4 -o address show dev "$interface" scope global | grep -q ' inet '
}


actions_main "$@"
```

### actions/ordinary.sh

```bash
#!/usr/bin/env bash
# Exact shared implementations of check 1 actions; not an entry point.

package_program() {
    # Fixed without inspecting any guest: tree, even if already present.
    native_install tree
}

application_package() {
    # Installing Flatpak is part of this action on every system lacking it.
    # https://docs.flatpak.org/en/latest/using-flatpak.html
    # https://docs.flatpak.org/en/latest/flatpak-command-reference.html
    native_install flatpak
    flatpak --user remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
    flatpak --user install --noninteractive -y flathub org.gnome.Calculator
}

language_program() {
    # https://docs.npmjs.com/cli/v11/commands/npm-install/
    native_install node
    npm install --global --prefix "$HOME/.local" cowsay
    "$HOME/.local/bin/cowsay" cal-test
}

browser_extension() {
    # The distribution Firefox and Python/pip are installed here if absent.
    # https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-t
    # https://firefox-source-docs.mozilla.org/python/marionette_driver.html
    # https://wiki.mozilla.org/Firefox/CommandLineOptions
    native_install browser
    python3 -m pip install --no-input --target "$HOME/.local/lib/cal-marionette" marionette_driver
    mkdir -p "$HOME/.mozilla/firefox/cal-check" "$HOME/Downloads"
    firefox --headless -CreateProfile "cal-check $HOME/.mozilla/firefox/cal-check"
    PYTHONPATH="$HOME/.local/lib/cal-marionette" python3 "$ACTIONS_DIR/firefox-addon.py"
}

personal_setting() {
    # Git's own command, not direct editing of its configuration.
    # https://git-scm.com/docs/git-config
    native_install git
    git config --global color.ui false
}

network_connection() {
    # https://networkmanager.dev/docs/api/latest/nmcli.html
    # https://networkmanager.dev/docs/api/latest/nm-settings-nmcli.html
    native_install network
    start_network_manager
    root nmcli connection add type ethernet con-name cal-secondary ifname '*' \
        802-3-ethernet.mac-address 52:54:00:ca:10:02 \
        ipv4.method auto ipv4.never-default yes ipv6.method disabled
    root nmcli --wait 90 connection up cal-secondary
    root nmcli connection add type wifi con-name cal-test ifname '*' ssid cal-test \
        connection.autoconnect no ipv4.method auto ipv6.method disabled \
        wifi-sec.key-mgmt wpa-psk wifi-sec.psk cal-test-passphrase
    # The Wi-Fi profile is saved, never activated: there is no radio.
}

home_script() {
    mkdir -p "$HOME/.local/bin"
    cat > "$HOME/.local/bin/cal-user-script" <<'SCRIPT'
#!/bin/sh
printf '%s\n' 'ordinary-action' >> "$HOME/cal-user-script.log"
SCRIPT
    chmod 755 "$HOME/.local/bin/cal-user-script"
    "$HOME/.local/bin/cal-user-script"
}

actions() {
    # Gentoo compiles distribution packages; all limits are wall-clock seconds.
    printf '%s\n' \
        "package_program $PACKAGE_LIMIT" \
        "application_package $PACKAGE_LIMIT" \
        "language_program $PACKAGE_LIMIT" \
        "browser_extension $BROWSER_LIMIT" \
        "personal_setting $PACKAGE_LIMIT" \
        "user_service $PACKAGE_LIMIT" \
        "network_connection $PACKAGE_LIMIT" \
        'home_script 30' \
        "container_run $PACKAGE_LIMIT"
}
```

### actions/lib.sh

```bash
#!/usr/bin/env bash
# Shared runner; source from the six entry scripts. No action runs on sourcing.
# https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin
# https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html
# https://www.sudo.ws/docs/man/sudo.man/
set -euo pipefail
export LC_ALL=C TZ=UTC

root() {
    if [[ -n ${CAL_SUDO_PASSWORD:-} ]]; then
        # A here-string is authentication input, not the command's data input.
        command sudo -S -p '' -- "$@" <<< "$CAL_SUDO_PASSWORD"
    else
        command sudo -n -- "$@"
    fi
}

install_root_file() {
    root install -D -m "$3" -- "$1" "$2"
}

actions_main() {
    local name limit start finish rc failed=0 script
    script=$(readlink -f "$0")
    if [[ ${1:-} == --list ]]; then actions; return; fi
    [[ $(id -un) == user && $(id -u) != 0 ]] || {
        printf '%s\n' 'Run inside the disposable guest as user.' >&2; return 64;
    }
    if [[ ${1:-} == --action ]]; then
        [[ $# == 2 && ${CAL_ACTION_DISPATCH:-} == 1 ]] || return 64
        while read -r name limit; do
            if [[ $name == "$2" ]]; then
                # Called as a simple command: errexit is not disabled by an if test.
                "$name"
                return
            fi
        done < <(actions)
        return 64
    fi
    [[ $# == 0 ]] || return 64
    command -v timeout >/dev/null
    # Refuse a second attempt on the same guest; retain earlier evidence.
    (set -o noclobber; : > "$HOME/actions-status.tsv") || return 73
    mkdir -p "$HOME/actions-logs"
    while read -r name limit; do
        start=$(date +%s)
        set +e
        CAL_ACTION_DISPATCH=1 timeout --signal=TERM --kill-after=30s "${limit}s" \
            bash "$script" --action "$name" \
            > "$HOME/actions-logs/$name.log" 2> "$HOME/actions-logs/$name.stderr" < /dev/null
        rc=$?
        set -e
        finish=$(date +%s)
        printf '%s\t%d\t%d\n' "$name" "$rc" "$((finish-start))" >> "$HOME/actions-status.tsv"
        if (( rc != 0 )); then failed=1; fi
    done < <(actions)
    return "$failed"
}
```

### actions/firefox-addon.py

```python
#!/usr/bin/env python3
"""Called only by browser_extension inside the disposable guest."""
# https://firefox-source-docs.mozilla.org/python/marionette_driver.html
# https://addons-server.readthedocs.io/en/latest/topics/api/addons.html
# https://raw.githubusercontent.com/ClearURLs/Addon/master/manifest.json
# https://firefox-source-docs.mozilla.org/mozbase/mozprofile.html
# https://raw.githubusercontent.com/mozilla-firefox/firefox/main/testing/marionette/client/marionette_driver/geckoinstance.py
import hashlib
import json
from pathlib import Path
import shutil
import urllib.request
from mozprofile import Profile
from marionette_driver.marionette import Marionette
from marionette_driver.addons import Addons

home = Path.home()
addon_id = "{74145f27-f039-47ce-a470-a662b129930a}"
with urllib.request.urlopen("https://addons.mozilla.org/api/v5/addons/addon/clearurls/", timeout=60) as response:
    metadata = json.load(response)
assert metadata["guid"] == addon_id
release = metadata["current_version"]["file"]
with urllib.request.urlopen(release["url"], timeout=120) as response:
    payload = response.read()
algorithm, expected = release["hash"].split(":", 1)
assert hashlib.new(algorithm, payload).hexdigest() == expected
xpi = home / "Downloads/clearurls.xpi"
xpi.write_bytes(payload)
(home / "Downloads/clearurls-source.json").write_text(json.dumps({
    "id": addon_id, "version": metadata["current_version"]["version"],
    "url": release["url"], "hash": release["hash"]}, indent=2) + "\n")
# Passing a Profile object prevents GeckoInstance from cloning a path string.
# restore=False preserves the installed extension and the generated browser state.
profile = Profile(profile=str(home / ".mozilla/firefox/cal-check"), restore=False)
client = Marionette(bin=shutil.which("firefox"), app="fxdesktop", profile=profile,
                    headless=True, app_args=["--no-remote"], socket_timeout=90,
                    startup_timeout=90)
try:
    client.start_session()
    installed = Addons(client).install(str(xpi), temp=False)
    assert installed == addon_id, installed
    client.quit(in_app=True)
finally:
    client.cleanup()
```

## Collector and recorded facts

The observation command is `LAB_ROOT=LAB_ROOT C1_INPUTS_COMMIT=COMMIT C1/collect.sh --observe MACHINE OUTPUT`. Replace the two uppercase path/commit values and the synthetic machine/output names with the committed check invocation. Rehearsals use the same queries and normalization through `--rehearsal`, with a fresh `reh-` overlay and automatic numerical reduction/deletion. They differ in query-label anonymization and retention, not query selection.

| File | SHA256 |
|---|---|
| `install/materialize.py` | `d144d13a84dabfaadc7d97c897c7f3b92a2c49c9c59f8eecf9ed80adedbb3262` |
| `lab.sh` | `3402697b02c88449fd6ba41e7137c404185c43a2bcd45fa211623d0d7e349733` |
| `collect.sh` | `a8399afc2c84da00f238a3543ecb3ea0ef31d48b3edb32d104e9b990bf971fd7` |
| `collector/main.py` | `86343abd34355b02064ae1074e2deda69760d292a6c1b62821da308c9888e2dc` |
| `collector/packages.py` | `961a5386f5d834472d08f02503121ef09a39109e997c9ba996124262fdf42a34` |
| `collector/portage-reasons.py` | `5f72a480e0ffcdeef91a7dc5088c82533c792694d38967c148acff46df5199d4` |
| `collector/rpm-selected-groups.py` | `ff346b8448b1a1b9fff839a28225b0f7cdb5f18b9b6b480384ff858f2d9f01c0` |
| `collector/talos.py` | `ac4c8b083c109f019a4e6aef91cfb57353638700118bc7d89a67bf716bfb7edf` |
| `collector/probe.go` | `60039578142dbc150b6b2ce60b4ca1468306dcd1c04c60f2853caa1c35b654d0` |
| `collector/btrfs_linux.go` | `f05551b71a7c524ff401f33ffbb0d36ad28709c19cd5df0a95252e92bf724dee` |
| `collector/build_probe.py` | `c80eb0299487ffa7cabac000924169e62a2608ae359a2a4de6b18f13d7f12f05` |
| `collector/probe-linux-amd64.gz.part-000` | `27486535b5446f1bf0c8a9372344549835a523fd2ab19763f36d700dd7913df1` |
| `collector/probe-linux-amd64.gz.part-001` | `73523ffc619dc4e560b49356734d4e7e3479e19debb029d98f398ce7f4b9a687` |
| `collector/probe-linux-amd64.gz.part-002` | `953269f9b530e3169124c3e0003e186c07219406a0d480dd394cc43b5d06daa3` |
| `collector/probe-linux-amd64.gz.part-003` | `1f1d11618d8f3cd134f9cba91e5bfdb5e4d1b76691ca84824f9e386b5db1af86` |
| `collector/probe-linux-amd64.gz.part-004` | `d19f92c0ebc83f0504377d2c565bdbb01ccb1fab7739663f65f473d475229cfa` |

`COLLECT.md`, `collector/PACKAGES.md` and `TALOS-COLLECT.md` define exact query sources, limits and unavailable facts. Level 1 records packages, services and timers, processes/executables, accounts/groups, access rules, module/driver names, sockets/firewall state, network records and container/image identities. Level 2 records stored objects with unresolved or absent ownership and a separate executable-code list. Group members retain type, mode, owner, size, UTC mtime, executable bit, bounded signature and persistence. Package facts include explicit/dependency/unknown reason and file integrity against native installation digests. Configuration-origin timestamps do not prove creation time; unresolved provenance remains unknown. Missing tools or inaccessible APIs are not evidence of absence.

## Classification and adjudication: five lines from Section 9.2

```text
Each object is decided twice, independently: an installed object, a program, a setting, a program record,
material or what exists only while the computer runs; whether the object must be recorded and by which line.
On any machine, an object is found for which the text of Sections 8.1 and 8.2 does not allow deciding
what it is and whether it must be recorded, or allows deciding both ways; or the two classifications decided
differently and the adjudication finds no sentence of the text that resolves the dispute.
```

The last three lines are the failure condition. Section 9.1 incorporates Appendix A.4.1: classifications are separate and cannot see each other; adjudication is made by neither classification and quotes the resolving sentence. No agreement threshold or additional decision rule is added.

Section 9.2 says: “A machine on which the second-level inventory has not been obtained cannot yield 1: its outcome is 0 if an object meeting the failure condition below is found on it, and ? otherwise.” The sentence is quoted without addition. Whether a second level obtained only in part — rows present, the traversal bounded or partly unavailable — counts as obtained is not decided in these inputs: the question, with both readings, is recorded for the author in `QUESTIONS.md`. For Talos Linux, `TALOS-COLLECT.md` names what the documented interface cannot list.

The preparation used stricter internal thresholds for calling a system ready (a known reason for more than nine packages in ten, a known integrity for more than nine packaged files in ten); `READY.md` reports which systems met them. These thresholds are not part of Section 9.2. All five systems remain the list of the check. Where a package manager stores no individual reason for a package — a package installed as a member of a group or of a system set — the inventory records the manager's own value; a decision that depends on a fact the inventory does not establish gives that object no decision, as the classification rules say.
