#!/bin/sh
# SPDX-License-Identifier: MIT
# Run only inside a staged package build, never with an empty DESTDIR.
set -eu
: "${DESTDIR:?staged output directory required}"
: "${CC:=cc}"
: "${CASE_VERSION:=1}"
: "${CASE_FETCH:=curl}"
: "${CASE_SHELL:=/bin/sh}"
: "${CASE_FETCH_STYLE:=curl}"
case "$CASE_FETCH$CASE_SHELL" in *[!a-zA-Z0-9_./-]*) exit 2;; esac
mkdir -p "$DESTDIR/usr/bin"
"$CC" -O2 -DCASE_VERSION="$CASE_VERSION" case-small.c -o "$DESTDIR/usr/bin/case-small"
case "$CASE_FETCH_STYLE" in
  curl) set --;;
  wget) set -- -DCASE_FETCH_WGET;;
  *) exit 2;;
esac
"$CC" -O2 "-DCASE_FETCH=\"$CASE_FETCH\"" "-DCASE_SHELL=\"$CASE_SHELL\"" "$@" case-probe.c -o "$DESTDIR/usr/bin/case-probe"
