#!/usr/bin/env python3
"""Offline saved-evidence audit; never runs a guest or changes old evidence.

Exit 0: complete, structurally validated evidence (failures remain reported).
Exit 1: invalid/inconsistent evidence. Exit 2: required evidence is missing.
Neither audit validity nor zero controller exits imply closed variants.
"""
import argparse,ast,collections,hashlib,importlib.util,json,pathlib,re,sys
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parents[2]
RAW=ROOT/'raw/round-2'
OLD=ROOT/'raw/round-1/final-2'
HELPER_SHA='df131f96cae4dc61cf4c10b6ddf196472051fdedd51cc10478fd353efbdcc9a4'
PINNED_BASELINES={'carried-suite/applications-examples/channel-examples/appimage.jsonl': '267015970615c4441192e182c5819a954288ca1afc823d8e7dc7193e6b01cf35', 'carried-suite/applications-examples/channel-examples/flatpak.jsonl': 'a8963146b30ca9986bd901eef99cb0250387b01d68198127a011de377ac19180', 'carried-suite/applications-examples/channel-examples/oci.jsonl': '265513caa60b10db51da08127e003f47ae8102c9b3a9c096f2c4a5e2253b6131', 'carried-suite/applications-examples-export.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/applications-helper-availability.jsonl': '5bd7bd0497d2e866f0e3b99e1ba95fe474c8c600f0790c98bb61fdd7ffcb135f', 'carried-suite/applications-new.log': '4dc0574d067777deafdeb13dce3d0503585c61a6a1404ee98b0dad8b1224235f', 'carried-suite/applications-verify.jsonl': '310e45e22d3485a91b16154be45f77eec237b61c50ad78454593822a89d808cc', 'carried-suite/applications.jsonl': '595402284de3a9354bcb275086f79c216ab4b31b451e97d35f6dd05c51a8e9c2', 'carried-suite/bc4-final-2-applications-destroy.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/bc4-final-2-language-destroy.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/bc4-final-2-ordinary-destroy.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/bc4-final-2-system-destroy.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/events.jsonl': 'd3f9c1764db0343387771e11980986a7c261cefaabe8e7e811d8d44fbfc4d6ae', 'carried-suite/factory-export/factory/base-files.json': 'b0e4fa2073555f08726a3c319e8aaefb85422cb37cde8cb95c21c1715d00ed47', 'carried-suite/factory-export/factory/machine.jsonl': 'c45b095cb0db71285b7de413549cde93c0c4c2e45b5a9bfa2526d0e31798cd53', 'carried-suite/factory-export.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/language-examples/channel-examples/npm.jsonl': 'd62f4bba468945773f7e5900aac6b60f9662dd3a4dbd6860bf664638db4227fd', 'carried-suite/language-examples/channel-examples/pip-native.jsonl': '82b3fa27cdfbad46fb8c4abcebeb326874317fb635c6713dd5ff914c0a5fd798', 'carried-suite/language-examples/channel-examples/pip.jsonl': 'e0beb8c4a51321b59582c815348d6d1eb8c4271dea668c2a6bd1cfd1524a94cf', 'carried-suite/language-examples-export.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/language-new.log': '050b386d0e8df9b7479f9bffe3790a08edb32e2095d688cc485fa571a4eea7c4', 'carried-suite/language-verify.jsonl': '5d3c814cd5a48ac1a33ac2a08ea22ddb54c0d9d6c7187b7a6ef342f4d203661c', 'carried-suite/language.jsonl': '74829eeddbc6dd7e5e654a296d8f2ade9798752bcded7127b1604894c60da34f', 'carried-suite/ordinary-examples/channel-examples/ordinary.jsonl': '15e497df4e13b3e8dae4b4f2f11d2a1ae63d0ca7490fa8ff96c9877231ef514c', 'carried-suite/ordinary-examples-export.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/ordinary-new.log': '6fe9bed244311f0740f9e9e387135aff9506066eaf1d76ec668e0fb9d601ef20', 'carried-suite/ordinary-verify.jsonl': '310e45e22d3485a91b16154be45f77eec237b61c50ad78454593822a89d808cc', 'carried-suite/ordinary.jsonl': '0d70128ad813df5bf487fbd864569fc46519d9fa56fdaa5b745b54bf713d4a7d', 'carried-suite/recipe-sha256.json': 'e0cdfdc59b927d97b4dd1f7e050585f5a93cb232cd67bf96f985137626c6cea8', 'carried-suite/regressions/bc3-bc4-final-2-copy-round3-selftest.py.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/bc3-bc4-final-2-destroy.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/bc3-bc4-final-2-new.log': '8ba7b576158efc8611214b7e65855d2923a36cc6135165694c40178fb7721dd8', 'carried-suite/regressions/bc3-inventory-bc4-final-2-copy-round3-inventory-test.py.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/bc3-inventory-bc4-final-2-destroy.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/bc3-inventory-bc4-final-2-new.log': 'c761ef29a7082ccf995194c031c21564598f76608c1ed8741f0e8c613b435b51', 'carried-suite/regressions/bc3-peer-a-destroy.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/bc3-peer-a-new.log': 'a2c5c6d6aa9c36ec839f1aa15c4ab868f98f5c1c4be6d2a9b0c08c633679eac5', 'carried-suite/regressions/bc3-peer-b-destroy.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/bc3-peer-b-new.log': '3c3b2dc8b6c38767699fbe2cef1c787b81477868fa0879789866f6fec4142329', 'carried-suite/regressions/bc3-regression1-bc4-final-2-copy-round1-selftest.py.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/bc3-regression1-bc4-final-2-destroy.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/bc3-regression1-bc4-final-2-new.log': 'b1839f2b40bd6b3bd3fa09c51d9b0d717b3d8cda71dad120efcf7fadb25b8255', 'carried-suite/regressions/bc3-regression2-bc4-final-2-copy-round2-probe.c.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/bc3-regression2-bc4-final-2-copy-round2-selftest.py.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/bc3-regression2-bc4-final-2-destroy.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/bc3-regression2-bc4-final-2-new.log': 'c5c6fc76f7e4428f4fef339343e7067705a4e4284cf3b036b80f47a79b4af820', 'carried-suite/regressions/boot-attempts.json': '87112e9659193a5cf718a96422d1f4e930170e6c2421af246e7c3aeeb5c5d906', 'carried-suite/regressions/boot-delay-cleanup.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/boot-delay-setup.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/boot-gate-stop.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/boot-order.jsonl': '9667fe34ef03be44867592c3ad6ed46078720ecde77eeef97b173035c62901e8', 'carried-suite/regressions/boot-start.log': '8975f3960cc1558a658672d6f3d1026e6afcb76b289e30384ca48874a978f330', 'carried-suite/regressions/independent-compare.json': '66e0becc367c0bc2b4e9f62042cfb652ec25e0c1777a92881defe82e3ecb2ac9', 'carried-suite/regressions/independent-stand-compare.jsonl': 'c1aed05ad4b3c1719081d1df1bd4c48b67970d8a41fe85029561bf759a8ab122', 'carried-suite/regressions/inventory.jsonl': '9396d409b6f7516e5f939344351eedcedd440c9e97ea69c8900fb391ad177760', 'carried-suite/regressions/original/D01.log': 'df1ba2c6b3fd7266297679a32d661283f36ee7813f020b9b68303d1aaec68fce', 'carried-suite/regressions/original/D02.log': '0e9f10bdd09e8babed9ed61b0334b6e85f896230ef6068c1acdea344c6332e0c', 'carried-suite/regressions/original/D03.log': '6e86e68d86a3eee96b5220524a6b3e1b3ad23f6a0a456c65ca5c6c4f88a37c61', 'carried-suite/regressions/original/D04.log': 'eca9d99ff743166662beabbd45c13664581d8a407f8e5da6ec4ea76ab887f901', 'carried-suite/regressions/original/D05.log': '0af335343dd4be44916a617cd9e380cbbab34c5af2ca495801b6582af18bf200', 'carried-suite/regressions/original/D06.log': '8a0d67998b1daa9869a341fe719b0a37d536c6b1fd8ab3ea2880ad796dc197a3', 'carried-suite/regressions/original/D07.log': 'f012b03f8275fa62a991120000e41fcdc2ad2ad0c3e90661d37d3bed8dbf799e', 'carried-suite/regressions/original/D08.log': '17874ee4317eceb0604a268c6963ed9bd95993463317aa9a9917d6509463a44a', 'carried-suite/regressions/original/D09.log': 'cfbc98377d49b3be452cc66593985d064ed36e9da8c6ba6bc4204d8c0a38db67', 'carried-suite/regressions/original/D10-compare.jsonl': 'c1aed05ad4b3c1719081d1df1bd4c48b67970d8a41fe85029561bf759a8ab122', 'carried-suite/regressions/original/D10-peer-a.log': '9e0504c45719b4db20f795be861736af1f32c6f88b94b971ff8a6cb30d108c96', 'carried-suite/regressions/original/D10-peer-b.log': 'f953ae5a6a314fa19a1857266d9d6fdbb80cb4e9b063f7ead1988ed8c0e66e42', 'carried-suite/regressions/original/D10-summary.log': 'b0161ec76a10f64468c281b0673ee28a8dfbeb12db21b2566cf04ed478a3baba', 'carried-suite/regressions/original/cleanup-cut.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/original/create-cut.log': '54e9d7e5bf1de25725b700234e46360c7180207969f60b4e3f05dd37b1c074e8', 'carried-suite/regressions/original/create-dev.log': '35593282dd7eac457558af620cd2c499858fabd81befae082085de2f1b3c1da0', 'carried-suite/regressions/original/create-peer-a.log': 'a49e7f6048f7955a66cfe0c3fca74b5987ecd333187b10d1383c14783bd2f427', 'carried-suite/regressions/original/create-peer-b.log': '6e095c0ced8421da97391154ccd761bf60f51472890217964d03e0a6cda3758b', 'carried-suite/regressions/original/cut/last-success.json': 'abfb82eb3a25f6ac39ed277c044d877a0022f9903c3464554b5c86e6c3abdb09', 'carried-suite/regressions/original/destroy-dev.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/original/destroy-peer-a.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/original/destroy-peer-b.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/original/dev/evidence/added.json': 'c6025202e927e55435c755676156143c2fe86aeef04c0fb3d29a710062f593c4', 'carried-suite/regressions/original/dev/evidence/factory.json': '87be16ceb1e968c59047a2260308cdb478c0b3d0d626d735f372b9b75ff6a280', 'carried-suite/regressions/original/dev/evidence/packages.tsv': 'f3710e2cd0a8214eb6aa1ccf51cda776f3f74ec5c8169af5eff394f63207d4e7', 'carried-suite/regressions/original/example/factory/base-files.json': 'b0e4fa2073555f08726a3c319e8aaefb85422cb37cde8cb95c21c1715d00ed47', 'carried-suite/regressions/original/example/factory/machine.jsonl': 'c45b095cb0db71285b7de413549cde93c0c4c2e45b5a9bfa2526d0e31798cd53', 'carried-suite/regressions/original/export-cut.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/original/export-declaration-peer-a.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/original/export-declaration-peer-b.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/original/export-dev.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/original/export-example.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/original/export-peer-a.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/original/export-peer-b.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/original/peer-a/added.json': 'c6025202e927e55435c755676156143c2fe86aeef04c0fb3d29a710062f593c4', 'carried-suite/regressions/original/peer-a/dev-add/base-files.json': 'b0e4fa2073555f08726a3c319e8aaefb85422cb37cde8cb95c21c1715d00ed47', 'carried-suite/regressions/original/peer-a/dev-add/machine.jsonl': '242dad801cafcd09883d14de7338cf8bc96fb87656a7202eb4cbbe3d3f037525', 'carried-suite/regressions/original/peer-b/added.json': 'c6025202e927e55435c755676156143c2fe86aeef04c0fb3d29a710062f593c4', 'carried-suite/regressions/original/peer-b/dev-add/base-files.json': 'b0e4fa2073555f08726a3c319e8aaefb85422cb37cde8cb95c21c1715d00ed47', 'carried-suite/regressions/original/peer-b/dev-add/machine.jsonl': '242dad801cafcd09883d14de7338cf8bc96fb87656a7202eb4cbbe3d3f037525', 'carried-suite/regressions/original-console.log': 'fdc71e24ebf5c588172f3af5f5e7a37e19453dd3bd6d95184b7142173853a2a9', 'carried-suite/regressions/peer-a/added.json': 'c6025202e927e55435c755676156143c2fe86aeef04c0fb3d29a710062f593c4', 'carried-suite/regressions/peer-a/dev-add/base-files.json': 'b0e4fa2073555f08726a3c319e8aaefb85422cb37cde8cb95c21c1715d00ed47', 'carried-suite/regressions/peer-a/dev-add/machine.jsonl': '242dad801cafcd09883d14de7338cf8bc96fb87656a7202eb4cbbe3d3f037525', 'carried-suite/regressions/peer-a-apply.log': 'b4aca8e0896c3c00e0a9082a5721ce2f5f56ad6cb0468adb8d6cd90d24326c1d', 'carried-suite/regressions/peer-a-declaration-export.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/peer-a-snapshot-export.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/peer-b/added.json': 'c6025202e927e55435c755676156143c2fe86aeef04c0fb3d29a710062f593c4', 'carried-suite/regressions/peer-b/dev-add/base-files.json': 'b0e4fa2073555f08726a3c319e8aaefb85422cb37cde8cb95c21c1715d00ed47', 'carried-suite/regressions/peer-b/dev-add/machine.jsonl': '242dad801cafcd09883d14de7338cf8bc96fb87656a7202eb4cbbe3d3f037525', 'carried-suite/regressions/peer-b-apply.log': '6e386758b4c720a25ac402b902d744cab5dcb5855a7eed42afed86de728598f2', 'carried-suite/regressions/peer-b-declaration-export.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/peer-b-snapshot-export.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/regressions/powercuts.jsonl': '920169261bd84d0491673febc2597d76d24406218452e3d46f63541ec154cae5', 'carried-suite/regressions/round1.jsonl': '5c7aa42b9e1de82c9dc1f8ebb870c902a42888d5a653f1c2e80db7bb664160a1', 'carried-suite/regressions/round2.jsonl': '41b6f2b0feea6f669831c058187768bdef737298bbc333e944755e4751f900ed', 'carried-suite/regressions/round3.jsonl': '4e790a04d77b559341cc9c11416a1ff8afa2a4ebdd4e6dceadecda39e1e9aed4', 'carried-suite/regressions/summary.json': 'f1b637d748e037238e781aab50ae19dd22557020a8509519dc218fe6f9e8976e', 'carried-suite/regressions-console.jsonl': '84af18a4eddb9d03144a3537305fff608849f2053333c0dd2c1a436e7c413b8f', 'carried-suite/summary.json': 'c295d10e7289df292c267a53bf10e31c4805190a4748dea4165512d8d35db8d7', 'carried-suite/system-examples/channel-examples/repository.jsonl': '6d42f55fca92e84a85f3b673e1e2ea9b327cf7fcd1647494ab98f4e5dbba2362', 'carried-suite/system-examples/channel-examples/system-update.jsonl': 'f173fe5ef4ae205cfb79aabc84576d7343b8937ddd9aa4c78e6b85088da50fd5', 'carried-suite/system-examples-export.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/system-new.log': 'bf5f941fd1dcd3b41440f4ffe17154fdec3d456340e344ec968eaa271d4c738a', 'carried-suite/system-state/channel-system-state/machine.jsonl': '9c33afdd3a771387f17c5e004af7cb55bccb8736a7d0b150c8a9050e3c39af9d', 'carried-suite/system-state-export.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'carried-suite/system-verify.jsonl': '310e45e22d3485a91b16154be45f77eec237b61c50ad78454593822a89d808cc', 'carried-suite/system.jsonl': '3ff7e0261a7a9929721d919213fce76f466ae8c0ffbcc7bf149593fd5d0eeac0', 'combined/a-apply.log': 'fb1e59d9a3a73a6b11a3112cfafe56c108c0645cb3f303af612a74d3dcb605fd', 'combined/a-deliver.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'combined/a-destroy.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'combined/a-exact.jsonl': '5125a909b427f6b5fd3d32af951e8d024cc7e45454576313305387b31f17b656', 'combined/a-launch-appimage.log': 'e8c24a97cf8400aabb87ef415a9724112ede1028d5014ab71b4cbb9d28df0fbd', 'combined/a-launch-download.log': '2d730e95f1029428692279f5bc6c89816a690dac6705ec811ad07176ba34fee6', 'combined/a-launch-flatpak.log': 'e8c24a97cf8400aabb87ef415a9724112ede1028d5014ab71b4cbb9d28df0fbd', 'combined/a-launch-native-wheel.log': '06579f034131c1d653e559a3146fac64fc8b89f163da631bf60515bcc2ea889d', 'combined/a-launch-npm.log': 'e017f486d358766733585c1154d60f73af1f5617190c2fce3ff1b83a3aac7764', 'combined/a-launch-oci.log': 'a729110b5ad6683250c52f215e66c3249507961ad3a62e3f13ec1efb29bc49c2', 'combined/a-launch-pip.log': 'db7c566e7c9fff5ebeb86fa76b67fa0d40039b3e5867e19f07d367c39ee392bd', 'combined/a-launch-repository.log': 'd9014c4624844aa5bac314773d6b689ad467fa4e1d1a50a1b8a99d5a95f72ff5', 'combined/a-launch-source-build.log': 'f97449337e7cef44fcd40a66f8a3769fe5800c944b1f5c168e67bda3e7f57691', 'combined/a-launch-updated-base.log': 'c75299ff58b3ba03084174049d180edb487e4cde20d2c51453effc2288eac888', 'combined/a-launch-user-service-program.log': '2d730e95f1029428692279f5bc6c89816a690dac6705ec811ad07176ba34fee6', 'combined/a-new.log': '0a1124e6b9cb10424acfebb74daa1a8f3c70ce302a42d789fbcb463a4633363d', 'combined/a-reboot-exact.jsonl': '5125a909b427f6b5fd3d32af951e8d024cc7e45454576313305387b31f17b656', 'combined/a-reboot-verify.jsonl': '880fd3b0ffdcef9be197b28163d60936d69e954eaa82abd6257b414bf2337bcf', 'combined/a-schedule.jsonl': '56e8ba3a74a0186d5d0b190ca694d0be936a8f7ac6b024431320b0a4e1682062', 'combined/a-snapshot.json': 'f04c8318b15942a3b96df98971c02f355d962a244d450f51b5afc5940847aefe', 'combined/a-start.log': '991c4bf9a39bb04b7d8f94cde11f51914a67d475ae259d85676598305fdae690', 'combined/a-stop.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'combined/a-verify.jsonl': '880fd3b0ffdcef9be197b28163d60936d69e954eaa82abd6257b414bf2337bcf', 'combined/b-apply.log': 'fb1e59d9a3a73a6b11a3112cfafe56c108c0645cb3f303af612a74d3dcb605fd', 'combined/b-deliver.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'combined/b-destroy.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'combined/b-exact.jsonl': '5125a909b427f6b5fd3d32af951e8d024cc7e45454576313305387b31f17b656', 'combined/b-launch-appimage.log': 'e8c24a97cf8400aabb87ef415a9724112ede1028d5014ab71b4cbb9d28df0fbd', 'combined/b-launch-download.log': '2d730e95f1029428692279f5bc6c89816a690dac6705ec811ad07176ba34fee6', 'combined/b-launch-flatpak.log': 'e8c24a97cf8400aabb87ef415a9724112ede1028d5014ab71b4cbb9d28df0fbd', 'combined/b-launch-native-wheel.log': '06579f034131c1d653e559a3146fac64fc8b89f163da631bf60515bcc2ea889d', 'combined/b-launch-npm.log': 'e017f486d358766733585c1154d60f73af1f5617190c2fce3ff1b83a3aac7764', 'combined/b-launch-oci.log': 'a729110b5ad6683250c52f215e66c3249507961ad3a62e3f13ec1efb29bc49c2', 'combined/b-launch-pip.log': 'db7c566e7c9fff5ebeb86fa76b67fa0d40039b3e5867e19f07d367c39ee392bd', 'combined/b-launch-repository.log': 'd9014c4624844aa5bac314773d6b689ad467fa4e1d1a50a1b8a99d5a95f72ff5', 'combined/b-launch-source-build.log': 'f97449337e7cef44fcd40a66f8a3769fe5800c944b1f5c168e67bda3e7f57691', 'combined/b-launch-updated-base.log': 'c75299ff58b3ba03084174049d180edb487e4cde20d2c51453effc2288eac888', 'combined/b-launch-user-service-program.log': '2d730e95f1029428692279f5bc6c89816a690dac6705ec811ad07176ba34fee6', 'combined/b-new.log': '18ff8f188b7e30a7d654a887c210276c5a1be9b601f113c5cbbcba25b81bf6a8', 'combined/b-reboot-exact.jsonl': '5125a909b427f6b5fd3d32af951e8d024cc7e45454576313305387b31f17b656', 'combined/b-reboot-verify.jsonl': '880fd3b0ffdcef9be197b28163d60936d69e954eaa82abd6257b414bf2337bcf', 'combined/b-schedule.jsonl': '56e8ba3a74a0186d5d0b190ca694d0be936a8f7ac6b024431320b0a4e1682062', 'combined/b-snapshot.json': 'f04c8318b15942a3b96df98971c02f355d962a244d450f51b5afc5940847aefe', 'combined/b-start.log': '769c895b9b9e87cf2b3064bf5c4c0f2a42f3b848440ef681557a4578dd4d5392', 'combined/b-stop.log': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'combined/b-verify.jsonl': '880fd3b0ffdcef9be197b28163d60936d69e954eaa82abd6257b414bf2337bcf', 'combined/events.jsonl': '9887dfb934d9484856520e159e85da0c4608296900c4c0a9eca138d3e9d31185', 'combined/provenance.json': '067a5ddcc79a757ee8917e16095dd31a58dd0e8d6f3d8e96a8b98c1507d39d77', 'combined/stand-compare.jsonl': 'b009661c2480d8340e0a85228838e9fddc8e1ea0fafbc70a6f9bba40122a89d8', 'combined/summary.json': '0c6638ccf2e2fcdefaaf9688819e0be1e1d15cf9eab664130c3af2ce95c6e936', 'gate.jsonl': '40afd8d6714ef82893474f0b1c78f844af909d6794b83785b128c411fc64ec16', 'shell-reboot.jsonl': 'b92fa2fd0cc233596ffe560ecbf78ec050b75da805491edee96ffa5eb1d0ce4a', 'shell.jsonl': 'd6eb43d2d285c64140e1421aad165bb16f4477b7635e35a9fa42e4c21f603053', 'supplement/direct.jsonl': 'ebe8c79eea62f0cb25cbac56b80785d84b0768ecbf856a7cf1ef4e1e3b2b6c2d', 'supplement/extra.jsonl': '9cf246374f4a3902c9dd3052214462fc86a5039c8f353d9acfd62fe2f8559db6', 'tools.jsonl': '3b8ce48f1fe2ad5ec7c54f63a9d853845be2c2c3470029644ef4b861147c5e2d'}
FROZEN_MANIFEST_SHA='0c8b93b8cf824ed0eecf029046c840c81a9747e7d5f1e28cc360470cb8aa4a6d'
PRIOR_COMBINED_SHA='7a5c9116f501dc280e1681970d1489c97b009509cc14e0c4048a82123d3b7284'
OBJECT_IDS=[
 'ORDERED-RULES','NATIVE-PACKAGE-CENSUS',
 'ADD-v4:objects','ADD-v4:meta','ADD-v4:noncode','ADD-v4:printk','ADD-dev-worker','ADD-v4:unit-source','ADD-v4:generated-unit',
 'PACKAGE-package:stand:v4-objects','PACKAGE-package:stand:v4-meta','PACKAGE-package:stand:v4-noncode','PACKAGE-package:stand:v4-dependency',
 'FILE-default.conf','FILE-source.py','FILE-copy.py','FILE-source.pyc','CHOSEN-SYSTEM-SETTING','installed-verify','GENERATED-UNIT',
 'UNDECLARED-GENERATOR','BYTECODE-RUN','LOOSE-NONCODE-COPY','DEFAULT-WRITE','SYSTEM-VALUE-WRITE','FALSE-DERIVATION','BREAKING-READBACK',
 'MISSING-OWNER-package:stand:v4-meta','MISSING-OWNER-package:stand:v4-dependency','MISSING-OWNER-/opt/stand/pkgs/v4-noncode/lookup.txt',
 'PERSONAL-VALUES','UNRECORDED-BYTECODE','EXTRACTED-CODE','ALT-FIXTURE','ALTERNATE-DATABASE','RUNTIME-NO-SEPARATE-LINE',
 'UNKNOWN-DOES-NOT-COVER','UNSUPPORTED-ALGORITHM','ADD-v4:printk',
 'REMOVE-v4:generated-unit','REMOVE-v4:unit-source','REMOVE-dev-worker','REMOVE-v4:printk','REMOVE-v4:noncode','REMOVE-v4:meta','REMOVE-v4:objects',
 'REMOVAL-package:stand:v4-meta','REMOVAL-package:stand:v4-dependency','REMOVAL-/opt/stand/pkgs/v4-noncode/lookup.txt',
 'REMOVAL-/opt/stand/pkgs/v4-objects/source.pyc','LOOSE-COPY-NO-PACKAGE-MEMBERSHIP','final-verify']
EXTRA_IDS={'v4:objects','v4:meta','v4:noncode','v4:printk','v4:unit-source','v4:generated-unit'}
CENSUSES=('initial','installed','unapplied-without-owners','with-attempts','removed')
errors=[];missing=[];checks=[];failures=[];untested=[];counts={}

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def insist(condition,message):
    if not condition:raise ValueError(message)
def present(path):
    if not path.is_file():raise FileNotFoundError(str(path.relative_to(ROOT)))
    return path

def load_helper():
    path=ROOT/'tools/summarize-round1.py'
    insist(sha(path)==HELPER_SHA,'unchanged audit helper digest differs')
    spec=importlib.util.spec_from_file_location('round1_evidence_helpers',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.RAW=RAW
    return module
H=load_helper()
def doc(path):return H.document(present(path))
def records(path):return H.records(present(path))
def group(name,fn):
    try:
        fn();checks.append({'check':name,'status':'validated'})
    except FileNotFoundError as exc:
        missing.append({'check':name,'reason':str(exc).replace(str(ROOT),'[stand-root]')});checks.append({'check':name,'status':'incomplete'})
    except (ValueError,OSError,KeyError,TypeError,IndexError) as exc:
        message=str(exc).replace(str(ROOT),'[stand-root]')
        errors.append({'check':name,'reason':message});checks.append({'check':name,'status':'invalid'})

def observe(rows,path):
    for number,row in enumerate(rows):
        if row.get('phase')=='summary' or row.get('kind','').endswith('summary'):continue
        false=[k for k in ('passed','pass_','ok','equal') if row.get(k) is False]
        if 'log' in row and 'rc' in row and row['rc']!=0:false.append('rc_nonzero')
        if false:failures.append({'file':str(path.relative_to(ROOT)),'index':number,'id':row.get('id',row.get('name')),
            'false_fields':false,'required':row.get('required',row.get('requirement')),'classification':row.get('classification')})
        if row.get('status')=='UNTESTED' or row.get('phase')=='unavailable' or ('passed' in row and row['passed'] is None):
            untested.append({'file':str(path.relative_to(ROOT)),'index':number,'id':row.get('id'),'status':row.get('status','unavailable')})

def baseline(name):
    path=OLD/name
    insist(name in PINNED_BASELINES and sha(present(path))==PINNED_BASELINES[name],'prior evidence changed: '+name)
    return path

def signatures(rows):return [H.signature(row) for row in rows]
def suite_contract(path,expected):
    rows=records(path)
    insist(signatures(rows)==signatures(expected),'fixed phase/ID/schema inventory differs: '+path.name)
    observe(rows,path)
    tests=[r for r in rows if r.get('id') and type(r.get('passed',r.get('ok'))) is bool and r.get('phase')!='summary']
    counts[str(path.relative_to(ROOT))]={'boolean_results':len(tests),'passed':sum(r.get('passed',r.get('ok')) for r in tests),'failed':sum(not r.get('passed',r.get('ok')) for r in tests)}

def verify(path,expected):
    present(path)
    # Preserve failed lines while still insisting on the entire exact ID/type set.
    values={}
    for line in H.lines(path):
        parts=line.split('\t');insist(len(parts)==4,'invalid verify row')
        ident,kind,state,digest=parts
        insist(ident not in values and state in ('OK','FAIL') and re.fullmatch('[0-9a-f]{64}',digest),'invalid/duplicate verify row')
        values[ident]=kind
        if state=='FAIL':failures.append({'file':str(path.relative_to(ROOT)),'id':ident,'false_fields':['readback'],'required':True})
    insist(values==expected,'verify ID/type inventory differs: '+path.name)

def inventory_files(directory,names):
    absent=[name for name in names if not (directory/name).is_file()]
    if absent:raise FileNotFoundError(str(directory.relative_to(ROOT))+': missing files '+', '.join(absent))
    H.require_files(directory,names)

def frozen_inputs(final):
    insist(sha(present(RAW/'final-1-source-sha256.json'))==FROZEN_MANIFEST_SHA,'frozen source manifest digest differs')
    expected=doc(RAW/'final-1-source-sha256.json')
    actual=doc(final/'input-sha256.json')
    insist(expected==actual,'frozen manifest and run input manifest differ')
    for key,digest in expected.items():
        insist(sha(present(ROOT/key))==digest,'current source differs: '+key)
        folder,filename=key.split('/',1)
        snapshot=final/('recipe-inputs' if folder=='build' else 'controller-inputs')/filename
        insist(sha(present(snapshot))==digest,'snapshot differs: '+key)
    for folder,destination in [('build','recipe-inputs'),('tools','controller-inputs')]:
        inventory_files(final/destination,[key.split('/',1)[1] for key in expected if key.startswith(folder+'/')])

def object_suite(final):
    insist(len(OBJECT_IDS)==52,'audit object contract must contain 52 results')
    path=final/'objects.jsonl';rows=records(path)
    results=[r for r in rows if r.get('phase')=='result']
    insist([r.get('id') for r in results]==OBJECT_IDS,'52-object ordered ID inventory differs, including printk restoration')
    insist(all(type(r.get('passed')) is bool and type(r.get('required')) is bool for r in results),'object verdict missing')
    observe(results,path)
    summary=[r for r in rows if r.get('phase')=='summary']
    insist(len(summary)==1 and summary[0].get('assertions')==52,'object summary inventory differs')
    for key,required in [('implementation_failures',True),('boundary_failures',False)]:
        insist(summary[0].get(key)==[r['id'] for r in results if not r['passed'] and r['required']==required],'object failure summary inconsistent: '+key)
    evidence=final/'objects-evidence/round2-evidence'
    saved=H.json_value(present(evidence/'results.json'),list)
    insist([{k:v for k,v in r.items() if k not in ('phase','utc')} for r in results]==saved,'object saved results differ from log')
    source=ast.parse((final/'recipe-inputs/v4-rules-selftest.py').read_text())
    names=[];pure_expected={}
    for node in source.body:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('CLASS_CASES','COVER_CASES') for t in node.targets):
            family=node.targets[0].id
            for case in node.value.elts:
                name=ast.literal_eval(case.elts[0]);names.append(name)
                if family=='CLASS_CASES':
                    pure_expected[name]=dict(zip(('category','required','question'),[ast.literal_eval(item) for item in case.elts[-3:]]))
                else:pure_expected[name]={'status':ast.literal_eval(case.elts[-2]),'lines':ast.literal_eval(case.elts[-1])}
    pure=[r for r in rows if 'pass_' in r]
    insist(len(names)==37 and [r.get('name') for r in pure]==names,'37 pure fixed cases incomplete')
    insist(all(type(r.get('pass_')) is bool for r in pure),'pure verdict missing')
    for r in pure:
        insist(r['expected']==pure_expected[r['name']],'pure expected verdict differs from frozen source')
        consistent=all(r['observed'].get(k)==v for k,v in r['expected'].items())
        insist(r['pass_']==consistent,'pure test verdict inconsistent')
    insist(pure==H.json_value(present(evidence/'rule-cases.json'),list),'pure exported cases differ')
    observe(pure,path)
    after=records(final/'objects-reboot.jsonl')
    insist([r.get('id') for r in after]==['OBJECTS-AFTER-REBOOT','after-reboot-verify'],'two reboot cases missing')
    insist(all(type(r.get('passed')) is bool for r in after),'reboot verdict missing');observe(after,final/'objects-reboot.jsonl')
    capability=[r for r in rows if r.get('id')=='INTERNAL-CODE-CAPABILITIES']
    insist(len(capability)==1 and capability[0].get('status')=='UNTESTED','unsupported capabilities must remain explicit UNTESTED');observe(capability,path)
    byid={r['id']:r for r in results}
    consumer=byid['BYTECODE-RUN']['command']
    insist(consumer['exit']==0 and consumer['stdout'].splitlines()==['RECORDED-BYTECODE','DEFAULT-LANGUAGE:en'],'default value not consumed by actual recorded program')
    insist(byid['FALSE-DERIVATION']['command']['exit']!=0 and byid['FALSE-DERIVATION']['passed'],'false derivation not refused')
    alt=byid['ALTERNATE-DATABASE']
    bypass=alt['command']['exit']==0 and alt['package_readback']=='install ok installed 1' and not alt['file_readback'].get('missing') and alt['report_unchanged'] is True
    insist(alt['passed']==(not bypass) and alt['boundary_result']==('failed' if bypass else 'not-established'),'alternate-installer outcome inconsistent')
    if not bypass:untested.append({'file':str(path.relative_to(ROOT)),'id':'ALTERNATE-DATABASE','status':'NOT_ESTABLISHED'})
    counts['objects']={'boolean_results':52,'passed':sum(r['passed'] for r in results),'failed':sum(not r['passed'] for r in results),'pure_cases':37,'after_reboot':2}

def censuses(final):
    directory=final/'objects-evidence/round2-evidence'
    for name in CENSUSES:
        path=directory/(name+'.jsonl');rows=records(path)
        insist(rows[-1].get('kind')=='summary','census summary missing')
        items=rows[:-1];found=collections.Counter(r['status'] for r in items)
        insist(dict(found)==rows[-1]['counts'],'census counts differ')
        for row in items:
            classification=row['classification']
            if row['status']=='FACT_UNKNOWN' or classification['category']=='FACT_UNKNOWN':
                insist(row['status']=='FACT_UNKNOWN' and not row['lines'] and not row['coverage'],'unknown counted as coverage')
            if row['status']=='covered':
                insist(bool(row['coverage']) and bool(row['lines']),'coverage without exact claim')
                insist(all(edge['required']==row['observed'] and edge['line'] in row['lines'] for edge in row['coverage']),'coverage not exact')
            if classification['category']=='runtime':insist(row['status']=='diagnostic' and classification['required'] is False,'runtime separate mandatory object')
        counts['census:'+name]=dict(found)

def carried_and_new(final):
    for oldname,spec in H.NEW.items():
        name=oldname.replace('supplement/','supplement-')
        expected=H.records(baseline(oldname))
        insist([H.signature(r) for r in expected]==spec['record_contract'],'prior new-suite contract changed')
        insist(sha(ROOT/spec['source'])==spec['source_sha256'],'carried new-suite source changed')
        suite_contract(final/name,expected)
    carried=final/'carried-suite'
    rename=lambda name:name.replace('bc3-bc4-final-2','bc3-bc2-final-1-regressions').replace('bc3-inventory-bc4-final-2','bc3-inventory-bc2-final-1-regressions').replace('bc3-regression1-bc4-final-2','bc3-regression1-bc2-final-1-regressions').replace('bc3-regression2-bc4-final-2','bc3-regression2-bc2-final-1-regressions').replace('bc4-final-2','bc4-bc2-final-1')
    inventory_files(carried,[rename(n) for n in H.REQUIRED_CARRIED if n!='regressions-console.jsonl'])
    inventory_files(final/'combined',H.REQUIRED_COMBINED)
    expected_events=H.records(baseline('carried-suite/events.jsonl'))
    adjusted=[]
    for row in expected_events:
        if row.get('log')=='regressions-console.jsonl':continue
        if row.get('id')=='PRIOR-SUITES':
            adjusted.append({'phase':'not-tested','id':'PRIOR-SUITES','reason':'--regressions not requested','utc':''});continue
        row=dict(row)
        for key in ('id','log'):
            if isinstance(row.get(key),str):row[key]=row[key].replace('bc4-final-2','bc4-bc2-final-1')
        adjusted.append(row)
    suite_contract(carried/'events.jsonl',adjusted)
    expected_console=H.records(baseline('carried-suite/regressions-console.jsonl'))
    adjusted=[]
    for row in expected_console:
        row=dict(row)
        if isinstance(row.get('log'),str):row['log']=rename(row['log'])
        adjusted.append(row)
    suite_contract(final/'regressions-console.jsonl',adjusted)
    factory=H.declaration(present(carried/'factory-export/factory/machine.jsonl'))
    insist(factory==H.declaration(baseline('carried-suite/factory-export/factory/machine.jsonl')),'factory identity/type inventory changed')
    for name in H.CARRIED:
        if name=='events.jsonl':continue
        path=carried/name;base=baseline('carried-suite/'+name)
        if name.endswith('powercuts.jsonl'):
            expected=H.powercut_records(base,factory);actual=H.powercut_records(path,factory)
            insist(signatures(actual)==signatures(expected),'powercut fixed contract differs');observe(actual,path)
        else:suite_contract(path,H.records(base))
    for name in ('objects','shell','gate','tools','supplement'):
        verify(final/(name+'-verify.log'),factory)
    for name in ('objects','shell','supplement'):verify(final/(name+'-before-verify.log'),factory)
    for name in ('applications','ordinary','system','language'):
        expected=dict(factory)
        if name=='language':
            for variant in ('pip','npm'):expected.update(H.declaration(carried/f'language-examples/channel-examples/{variant}.jsonl'))
        verify(carried/(name+'-verify.jsonl'),expected)
    for relative,decl in [('regressions/independent-stand-compare.jsonl','regressions/peer-a/dev-add/machine.jsonl'),('regressions/original/D10-compare.jsonl','regressions/original/peer-a/dev-add/machine.jsonl')]:
        path=carried/relative;observe(H.comparisons(path,H.declaration(carried/decl)),path)
    return factory

def object_exports(final):
    directory=final/'objects-evidence/round2-evidence'
    expected=[name+'.jsonl' for name in CENSUSES]+['rule-cases.json','fixture-rows.json','generated-unit-rows.json',
        'installed-verify.json','final-verify.json','after-reboot-verify.json','residual-setting.json','before-reboot.json','results.json',
        'without-owners/machine.jsonl','without-owners/base-files.json']
    inventory_files(directory,expected)
    factory_dir=final/'factory-export/factory'
    inventory_files(factory_dir,['machine.jsonl','base-files.json'])
    for name in ('machine.jsonl','base-files.json'):
        insist((factory_dir/name).read_bytes()==(final/'carried-suite/factory-export/factory'/name).read_bytes(),'independent component factory export differs: '+name)
    factory=H.declaration(factory_dir/'machine.jsonl')
    fixture=H.json_value(directory/'fixture-rows.json',list)
    generated=H.json_value(directory/'generated-unit-rows.json',list)
    insist([r['id'] for r in fixture]==['v4:objects','v4:meta','v4:noncode','v4:printk'],'fixed object fixture rows differ')
    insist([r['id'] for r in generated]==['v4:unit-source','v4:generated-unit'],'fixed generated fixture rows differ')
    installed={**factory,**{r['id']:r['type'] for r in fixture+generated},'dev-worker':'program'}
    for name,expected_ids in [('installed-verify.json',installed),('final-verify.json',factory),('after-reboot-verify.json',factory)]:
        values=H.json_value(directory/name,list)
        insist(len(values)==len(expected_ids) and {r['id']:r['type'] for r in values}==expected_ids,'exported full readback inventory differs: '+name)
        insist(all(type(r.get('ok')) is bool for r in values),'exported readback verdict missing');observe(values,directory/name)

def combined(final,declaration):
    declared=H.declaration(present(declaration))
    old_path=ROOT/'example/round-1/combined/machine.jsonl'
    insist(sha(present(old_path))==PRIOR_COMBINED_SHA,'prior complete declaration changed')
    old=H.declaration(old_path)
    insist(len(declared)==578 and set(declared)-set(old)==EXTRA_IDS and not set(old)-set(declared),'combined exact 578-row/new-six-ID inventory differs')
    metadata=doc(final/'complete-example.json')
    insist(metadata['rows']==578 and set(metadata['added_rows'])==EXTRA_IDS and metadata['machine_sha256']==sha(declaration),'combined metadata differs')
    directory=final/'combined'
    summary=doc(directory/'summary.json')
    insist(summary['declaration_rows']==578 and summary['snapshot_sides']==['a','b'] and set(summary['results'])=={'a','b'},'combined complete sides missing')
    for side in ('a','b'):
        for suffix in ('verify.jsonl','reboot-verify.jsonl'):verify(directory/(side+'-'+suffix),declared)
        for suffix in ('exact.jsonl','reboot-exact.jsonl','schedule.jsonl'):
            path=directory/(side+'-'+suffix);suite_contract(path,H.records(baseline('combined/'+side+'-'+suffix)))
            rows=records(path)
            if suffix!='schedule.jsonl':insist(rows[0]['files_sha256']=={'machine.jsonl':sha(declaration)},'combined exact bytes mismatch')
        snapshot=H.json_value(present(directory/(side+'-snapshot.json')),list)
        insist(len(snapshot)==578 and {r['id']:r['type'] for r in snapshot}==declared,'combined snapshot ID/type differs')
        insist(all(type(r.get('ok')) is bool for r in snapshot),'combined snapshot verdict missing')
        observe(snapshot,directory/(side+'-snapshot.json'))
    path=directory/'stand-compare.jsonl';observe(H.comparisons(path,declared),path)
    suite_contract(directory/'events.jsonl',H.records(baseline('combined/events.jsonl')))
    insist(summary['suite_exit']==0 and summary['owned_vms_remaining']==[],'combined controller failed/unclean')


def original_and_ancillary(final):
    carried=final/'carried-suite'
    # These unchanged native-controller outputs mix command transport and exact
    # readback. Normalize only documented volatile timestamps, hashes and PIDs;
    # EXIT numbers, refusal/success markers and every readback ID stay exact.
    def normalize(line):
        line=re.sub(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ','<UTC>',line)
        line=re.sub(r'\b[0-9a-f]{64}\b','<SHA256>',line)
        line=re.sub(r'(MainPID=)\d+',r'\1<PID>',line)
        line=re.sub(r'(invocation ID: )[0-9a-f]{32}',r'\1<ID>',line)
        line=re.sub(r'(stand-)[0-9a-f]{16,32}(?:-\d+)?(\.service)',r'\1<ID>\2',line)
        line=re.sub(r'(delay_from_marker_ms=)[0-9]+(?:\.[0-9]+)?',r'\1<MEASURED_MS>',line)
        return line
    for name in ('D01','D02','D03','D04','D05','D06','D07','D08','D09','D10-peer-a','D10-peer-b','D10-summary'):
        relative='carried-suite/regressions/original/'+name+'.log'
        target=final/relative;expected=H.lines(baseline(relative));actual=H.lines(present(target))
        insist([normalize(x) for x in actual]==[normalize(x) for x in expected],name+': native result/readback inventory differs; review required')
        for line in actual:
            fields=line.split('\t')
            if len(fields)==4 and fields[2]=='FAIL':failures.append({'file':str(target.relative_to(ROOT)),'id':fields[0],'false_fields':['readback'],'required':True})
        if name=='D09':untested.append({'file':str(target.relative_to(ROOT)),'id':'real-radio-hardware','status':'UNTESTED'})
    for name in ('applications-helper-availability.jsonl',):
        suite_contract(carried/name,H.records(baseline('carried-suite/'+name)))
    name='regressions/boot-order.jsonl';target=carried/name
    actual=H.lines(present(target));expected=H.lines(baseline('carried-suite/'+name))
    ar=H.decode(actual[0],name);er=H.decode(expected[0],name)
    insist(H.signature(ar)==H.signature(er),'boot gate assertion missing');observe([ar],target)
    def dependencies(lines):
        units=('getty@tty1.service','serial-getty@ttyS0.service','systemd-logind.service','systemd-user-sessions.service')
        insist(len(lines)==12,'boot ordering transport has missing/extra lines')
        result=[]
        for index,unit in enumerate(units):
            first,second,blank=lines[index*3:index*3+3]
            insist(first.startswith(unit+' Requires=') and second.startswith('After=') and blank=='',
                   'boot ordering transport unit/property framing differs')
            properties=[]
            for line,prefix in ((first,unit+' Requires='),(second,'After=')):
                tokens=line[len(prefix):].split()
                insist(tokens and 'stand-replay.service' in tokens,'boot replay dependency missing')
                # systemctl lists dependency relations, not an execution order.
                # Keep exact token spelling and multiplicity; normalize only
                # enumeration order within each of the eight named properties.
                properties.append(sorted(tokens))
            result.append(properties)
        return result
    insist(dependencies(actual[1:])==dependencies(expected[1:]),'boot dependency token inventory differs')
    name='regressions/inventory.jsonl';target=carried/name
    actual=H.lines(present(target));expected=H.lines(baseline('carried-suite/'+name))
    insist(actual[0]==expected[0] and actual[-1]==expected[-1],'legacy inventory test markers missing')
    rows=[H.decode(line,name) for line in actual[1:-1]]
    insist(rows[-1].get('kind')=='summary' and dict(collections.Counter(r['status'] for r in rows[:-1]))==rows[-1]['counts'],'legacy census summary inconsistent')
    # Native source signatures and identities are checked against frozen inputs;
    # completed prior evidence provides the expected fixed result inventory.
    compare=doc(carried/'regressions/independent-compare.json')
    expected_ids=H.declaration(carried/'regressions/peer-a/dev-add/machine.jsonl')
    for side in ('left','right'):
        values=compare[side]
        insist(len(values)==len(expected_ids) and {r['id']:r['type'] for r in values}==expected_ids,'independent peer readback incomplete')
        observe(values,carried/'regressions/independent-compare.json')
    insist(compare['values_equal']==(compare['left']==compare['right']),'independent comparison verdict inconsistent')
    a=carried/'regressions/peer-a/dev-add/machine.jsonl';b=carried/'regressions/peer-b/dev-add/machine.jsonl'
    insist(compare['declaration_bytes_equal']==(a.read_bytes()==b.read_bytes()),'independent declaration verdict inconsistent')
    insist(compare['values_equal'] and compare['declaration_bytes_equal'],'independent peers differ')

def controller(final):
    summary=doc(final/'summary.json');steps=H.json_value(present(final/'steps.json'),list)
    insist(summary['steps']==steps,'controller steps differ from saved ledger')
    expected=['build.log','peer-build.log','carried-console.jsonl','regressions-console.jsonl','assemble.log','combined-console.jsonl']
    for suite in ('objects','shell','gate','tools','supplement'):
        expected += [suite+'-new.log',suite+'-verify.log','bc2-final-1-'+suite+'-destroy.log']
        expected += ['supplement-direct.jsonl','supplement-extra.jsonl'] if suite=='supplement' else [suite+'.jsonl']
        if suite in ('objects','shell','supplement'):expected += [suite+'-before-verify.log',suite+'-stop.log',suite+'-start.log']
        if suite in ('objects','shell'):expected += [suite+'-reboot.jsonl']
        if suite=='objects':expected += ['objects-export.log','factory-export.log']
    insist(collections.Counter(s['log'] for s in steps)==collections.Counter(expected),'controller exact step inventory differs')
    for step in steps:
        present(final/step['log']);insist(type(step['exit']) is int,'step exit absent')
        if step['exit']:failures.append({'file':'final-1/steps.json','id':step['log'],'false_fields':['exit'],'required':True})
    ledger=doc(final/'whole-suite-ledger.json')
    insist(set(ledger['lanes'])=={'components','round4','round3'} and ledger['lanes']==summary['lanes'],'whole-suite lane inventory differs')
    insist(all(lane['exit']==0 for lane in ledger['lanes'].values()) and all(s['exit']==0 for s in steps),'controller/lane nonzero exit')
    insist(summary['controller_exit']==0 and summary['remaining_vms']==[] and summary['peer_remaining'] is False,'controller unfinished or unclean')
    carried=doc(final/'carried-suite/summary.json');reg=doc(final/'carried-suite/regressions/summary.json')
    insist(carried['suite_exit']==0 and carried['owned_vms_remaining']==[] and carried['regressions_requested'] is False,'four-suite controller incomplete')
    insist(set(carried['suites'])=={'language','applications','system','ordinary'},'four-suite result inventory differs')
    for name,value in carried['suites'].items():
        insist(value['tested'] is True and all(value[k]==0 for k in ('suite_exit','verify_exit','example_export_exit','metadata_exit')),'carried suite failed: '+name)
    insist(reg['suite_exit']==0 and reg['regressions_run'] is True and reg['independent_peer_supplied'] is True,'regression chain incomplete')
    # Child global VM listings can contain other concurrently running lanes.
    # Final parent cleanup above is authoritative and does not rewrite them.

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--final',type=pathlib.Path,default=RAW/'final-1')
    parser.add_argument('--combined-declaration',type=pathlib.Path,default=ROOT/'example/round-2/combined/machine.jsonl')
    parser.add_argument('--output',type=pathlib.Path)
    args=parser.parse_args();final=args.final.resolve()
    args.combined_declaration=args.combined_declaration.resolve()
    group('frozen-inputs',lambda:frozen_inputs(final))
    group('object-suite',lambda:object_suite(final))
    group('independent-censuses',lambda:censuses(final))
    group('whole-suite-fixed-inventories',lambda:carried_and_new(final))
    group('object-export-inventories',lambda:object_exports(final))
    group('native-regression-and-ancillary',lambda:original_and_ancillary(final))
    group('combined-every-line',lambda:combined(final,args.combined_declaration))
    group('controller-lanes-cleanup',lambda:controller(final))
    result={'audit_complete':not errors and not missing,'errors':errors,'missing':missing,'checks':checks,'counts':counts,
        'false_observations':failures,'untested_observations':untested,
        'record_counts':{'false_observations':len(failures),'untested_observations':len(untested),'invalid_sections':len(errors),'missing_sections':len(missing)},
        'controller_success_is_not_boundary_success':True,'hypothesis_outcome':'?',
        'limitations':['Finite saved-evidence audit, not independent reproduction or variant acceptance.',
                      'Missing or malformed evidence never counts as a passed test; preserved false and untested rows remain separate.']}
    data=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        insist(args.output.resolve().is_relative_to(RAW.resolve()),'audit output must remain in this round raw directory')
        args.output.write_text(data)
    print(data,end='')
    return 1 if errors else 2 if missing else 0
if __name__=='__main__':raise SystemExit(main())
