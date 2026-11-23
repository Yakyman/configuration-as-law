#!/bin/sh
# Run on the server in <server task dir>: download every package of names.txt (bookworm main) and
# extract all into debs/all, recording path -> package in owners.tsv
cd <server task dir>/debs || exit 1
: > ../owners.tsv
for p in $(cut -d: -f1 ../names.txt); do
  f=$(awk -v p="$p" '/^Package: /{c=($2==p)} c&&/^Filename: /{print $2; exit}' ../Packages)
  [ -z "$f" ] && { echo "NOFILE $p"; continue; }
  b=$(basename "$f")
  [ -f "$b" ] || curl -sS --retry 3 -O "https://deb.debian.org/debian/$f" || { echo "FAIL $p"; continue; }
  mkdir -p "ctl/$p"
  (cd "ctl/$p" && ar p "../../$b" $(ar t "../../$b" | grep control.tar) | tar x -J 2>/dev/null || (cd "ctl/$p" && ar p "../../$b" $(ar t "../../$b" | grep control.tar) | zstd -dc | tar x 2>/dev/null))
  d=$(ar t "$b" | grep data.tar)
  case "$d" in
    *.xz) ar p "$b" "$d" | tar xJ -C all ; ar p "$b" "$d" | tar tJ | sed "s|^\./||; s|^|$p\t|" >> ../owners.tsv ;;
    *.zst) ar p "$b" "$d" | zstd -dc | tar x -C all ; ar p "$b" "$d" | zstd -dc | tar t | sed "s|^\./||; s|^|$p\t|" >> ../owners.tsv ;;
    *.gz) ar p "$b" "$d" | tar xz -C all ; ar p "$b" "$d" | tar tz | sed "s|^\./||; s|^|$p\t|" >> ../owners.tsv ;;
  esac
done
wc -l ../owners.tsv
