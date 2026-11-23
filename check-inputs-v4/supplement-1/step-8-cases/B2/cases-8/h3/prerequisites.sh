#!/usr/bin/bash
# Run once with the laboratory root credential before ordinary history.sh.
set -e
trap 'printf "ACTION_FAILED h3-prerequisites line=%s\n" "$LINENO"' ERR
printf "ACTION_BEGIN h3-prerequisites-fetch\n"
mkdir -p /tmp/s8-h3-prerequisites
cd /tmp/s8-h3-prerequisites
/usr/bin/curl --fail --location --output bc_1.07.1-4_amd64.deb https://deb.debian.org/debian/pool/main/b/bc/bc_1.07.1-4_amd64.deb
printf '%s\n' 'd055a11f0f9c5f8fe78b31d502c01dfe46ddf9c24f753aaddadaaff95fcc75ad  bc_1.07.1-4_amd64.deb' | /usr/bin/sha256sum --check -
/usr/bin/curl --fail --location --output bsdmainutils_12.1.8_all.deb https://deb.debian.org/debian/pool/main/b/bsdmainutils/bsdmainutils_12.1.8_all.deb
printf '%s\n' '02e817ed3ac20296862ed240942d5697a86bc043312bd402991fad8501e054b0  bsdmainutils_12.1.8_all.deb' | /usr/bin/sha256sum --check -
/usr/bin/curl --fail --location --output bzip2_1.0.8-6_amd64.deb https://deb.debian.org/debian/pool/main/b/bzip2/bzip2_1.0.8-6_amd64.deb
printf '%s\n' '6b5fbe71f0fc41e85919bc4b3c514e6c47577c5005dbf1f5af6e4a49cc221aab  bzip2_1.0.8-6_amd64.deb' | /usr/bin/sha256sum --check -
/usr/bin/curl --fail --location --output distro-info_1.13_amd64.deb https://deb.debian.org/debian/pool/main/d/distro-info/distro-info_1.13_amd64.deb
printf '%s\n' 'ae95925233da814e0b9f5998757115e82c619bc94a044fcf311eb84effdc2aba  distro-info_1.13_amd64.deb' | /usr/bin/sha256sum --check -
/usr/bin/curl --fail --location --output jq_1.7.1-6+deb13u4_amd64.deb https://deb.debian.org/debian/pool/main/j/jq/jq_1.7.1-6+deb13u4_amd64.deb
printf '%s\n' '7350392f700e20e46b7ae174a57f54e4ea106dd559753646d629b4e618bf2bff  jq_1.7.1-6+deb13u4_amd64.deb' | /usr/bin/sha256sum --check -
/usr/bin/curl --fail --location --output lib32gcc-s1_14.2.0-19_amd64.deb https://deb.debian.org/debian/pool/main/g/gcc-14/lib32gcc-s1_14.2.0-19_amd64.deb
printf '%s\n' 'aa7674a786d58a1efaacb3ce377c06a2d3153c1fa7360b08375c7dd67c90c3fe  lib32gcc-s1_14.2.0-19_amd64.deb' | /usr/bin/sha256sum --check -
/usr/bin/curl --fail --location --output lib32stdc++6_14.2.0-19_amd64.deb https://deb.debian.org/debian/pool/main/g/gcc-14/lib32stdc++6_14.2.0-19_amd64.deb
printf '%s\n' '326011247094e9a5e5b7dd431b67ccf6dddfd9c4ee5078a8d1a15661883791c2  lib32stdc++6_14.2.0-19_amd64.deb' | /usr/bin/sha256sum --check -
/usr/bin/curl --fail --location --output libc6-i386_2.41-12+deb13u5_amd64.deb https://deb.debian.org/debian/pool/main/g/glibc/libc6-i386_2.41-12+deb13u5_amd64.deb
printf '%s\n' '1e59f89ce33149849ffffc53c38ca54ffa7a15e48cd0394eb3f4ba02fe553ca4  libc6-i386_2.41-12+deb13u5_amd64.deb' | /usr/bin/sha256sum --check -
/usr/bin/curl --fail --location --output 'libevent-core-2.1-7t64_2.1.13-stable-1~deb13u1_amd64.deb' 'https://deb.debian.org/debian/pool/main/libe/libevent/libevent-core-2.1-7t64_2.1.13-stable-1~deb13u1_amd64.deb'
printf '%s\n' 'faa7d20cc8fa05ac3b0497065fa60bc920eacd3711ff039649d43a7aa34421ce  libevent-core-2.1-7t64_2.1.13-stable-1~deb13u1_amd64.deb' | /usr/bin/sha256sum --check -
/usr/bin/curl --fail --location --output libjq1_1.7.1-6+deb13u4_amd64.deb https://deb.debian.org/debian/pool/main/j/jq/libjq1_1.7.1-6+deb13u4_amd64.deb
printf '%s\n' '70bb2cbd66d5ada4349067ae9f61d0560b3b359d4203f2c051ca5773153ae0ba  libjq1_1.7.1-6+deb13u4_amd64.deb' | /usr/bin/sha256sum --check -
/usr/bin/curl --fail --location --output libonig5_6.9.9-1+b1_amd64.deb https://deb.debian.org/debian/pool/main/libo/libonig/libonig5_6.9.9-1+b1_amd64.deb
printf '%s\n' '3abee130696244050500bcc7870e3b4cb82ddd87149ece3fd55010c3d4e1d18c  libonig5_6.9.9-1+b1_amd64.deb' | /usr/bin/sha256sum --check -
/usr/bin/curl --fail --location --output ncal_12.1.8_amd64.deb https://deb.debian.org/debian/pool/main/b/bsdmainutils/ncal_12.1.8_amd64.deb
printf '%s\n' 'd2de213d7e86ae56d1d44318dc8307e1efe5ea6ede0dbef6ae3c7ed68e4be618  ncal_12.1.8_amd64.deb' | /usr/bin/sha256sum --check -
/usr/bin/curl --fail --location --output pigz_2.8-1_amd64.deb https://deb.debian.org/debian/pool/main/p/pigz/pigz_2.8-1_amd64.deb
printf '%s\n' '876b4612815c310d91cced1e6193a14e397d03ebb5ae85fec72fc6e0246ccdd9  pigz_2.8-1_amd64.deb' | /usr/bin/sha256sum --check -
/usr/bin/curl --fail --location --output tmux_3.5a-3_amd64.deb https://deb.debian.org/debian/pool/main/t/tmux/tmux_3.5a-3_amd64.deb
printf '%s\n' 'e6b6aa51780044e2c4a0e618c33f832b70ec80caa30303e6c254a0c851b5af78  tmux_3.5a-3_amd64.deb' | /usr/bin/sha256sum --check -
/usr/bin/curl --fail --location --output unzip_6.0-29+deb13u1_amd64.deb https://deb.debian.org/debian/pool/main/u/unzip/unzip_6.0-29+deb13u1_amd64.deb
printf '%s\n' 'fc11f8736bdec6fc46a6864f75bce0c8206a790df37dbcab5ddb25b1bf0f58f0  unzip_6.0-29+deb13u1_amd64.deb' | /usr/bin/sha256sum --check -
printf "ACTION_DONE h3-prerequisites-fetch\n"
printf "ACTION_BEGIN h3-prerequisites-install\n"
/usr/bin/dpkg --install bc_1.07.1-4_amd64.deb bsdmainutils_12.1.8_all.deb bzip2_1.0.8-6_amd64.deb distro-info_1.13_amd64.deb jq_1.7.1-6+deb13u4_amd64.deb lib32gcc-s1_14.2.0-19_amd64.deb lib32stdc++6_14.2.0-19_amd64.deb libc6-i386_2.41-12+deb13u5_amd64.deb 'libevent-core-2.1-7t64_2.1.13-stable-1~deb13u1_amd64.deb' libjq1_1.7.1-6+deb13u4_amd64.deb libonig5_6.9.9-1+b1_amd64.deb ncal_12.1.8_amd64.deb pigz_2.8-1_amd64.deb tmux_3.5a-3_amd64.deb unzip_6.0-29+deb13u1_amd64.deb
printf "ACTION_DONE h3-prerequisites-install\n"
printf "ACTION_BEGIN h3-prerequisites-readback\n"
/usr/bin/dpkg-query -W '-f=${Package}\t${Version}\t${db:Status-Status}\n' bc bsdmainutils bzip2 distro-info jq lib32gcc-s1 lib32stdc++6 libc6-i386 libevent-core-2.1-7t64 libjq1 libonig5 ncal pigz tmux unzip
printf "ACTION_DONE h3-prerequisites-readback\n"
