# D-test: the test declaration of the case party, as semantic line specs (CASES.md, "Notation").
# adapter.py renders it into the builder's syntax (build/DECLARATION.md). One spec per line.
# Paper 3, Section 4.3: "The test declaration names everything it permits: the base system and,
# for each channel below, one program installed through that channel."
#
# Base system and archive state (T2, plan Section 9.5: latest stable release on the day of the commit)
base
archive-state 20261123T000000Z
# The ordinary account, its means of login and superuser privileges by the documented group
account person uid=1000 gid=1000 groups=wheel shell=/bin/bash home=/home/person
authorized-key person @PERSON_KEY@
# Tools the cases use for observation and ordinary commands
package procps
package iproute2
package nftables
package coreutils
package findutils
package grep
package sed
package openssh-client
# C1 system package manager: recorded program
package ed
# C2 pip
package python3-pip
package python3-venv
pip cowsay==6.1
# C3 npm
package nodejs
package npm
npm cowsay@1.6.0
# C4 Flatpak
package flatpak
# required beside flatpak by build/DECLARATION.md revision 9+ (also by containers and user units)
package util-linux
package gpg
package gpg-agent
flatpak io.mpv.Mpv flathub
# C5 AppImage
package libfuse2t64
appimage /home/person/bin/nvim.appimage https://github.com/neovim/neovim/releases/download/v0.10.4/nvim-linux-x86_64.appimage @SHA256@
# C6 direct download of programs and archives
package curl
download /home/person/bin/rg https://github.com/BurntSushi/ripgrep/releases/download/14.1.1/ripgrep-14.1.1-x86_64-unknown-linux-musl.tar.gz @SHA256@ unpack=ripgrep-14.1.1-x86_64-unknown-linux-musl/rg
# C7 building from source in the home directory
package gcc
package make
package libc6-dev
built /home/person/bin/hello-world /home/person/src/hello.c 'gcc -O2 -o /home/person/bin/hello-world /home/person/src/hello.c'
# C8 user services and schedulers
package cron
# required for user units by build/DECLARATION.md revision 12
package systemd
user-unit person cases-tick.timer '[Timer]\nOnCalendar=hourly\n[Install]\nWantedBy=timers.target\n' enabled
user-unit person cases-tick.service '[Service]\nType=oneshot\nExecStart=/bin/true\n'
# C9 interpreters executing scripts: the person's own recorded script (ordinary work, Paper 4 Section 9.3)
package python3
script /home/person/bin/cases-report.sh 2fb12358ed0c2cf3ef02685dc629f046b5b40f32e1ff52ba03cdd854ea58c1d4
# C10 shell startup files and executable program settings
package git
shell-startup person .bashrc 'PATH="$HOME/bin:$PATH"'
git-config person alias.st status
# C11 containers
package podman
package uidmap
package slirp4netns
container-image docker.io/library/alpine:3.20.3@@DIGEST@
# A recorded system service and a recorded rule (P4-C8-7, P2-CHG-2, P2-REM-2, P4-BT-15)
service cases-svc enabled /usr/bin/sleep infinity
firewall cases-8081 'add rule inet confos input tcp dport 8081 accept'
setting hostname confos-test
setting timezone Etc/UTC
