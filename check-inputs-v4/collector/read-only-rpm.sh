#!/bin/sh
set -eu
cd "$1"
export LAB_ROOT="$PWD" TMPDIR="$PWD"
podman --root "$PWD/podman-root" --runroot "$PWD/podman-run" --storage-driver vfs run -d --name c1-col-rocky-ro --hostname col-rpm-ro --read-only --tmpfs /tmp:rw,exec,size=64m --tmpfs /run:rw,exec,size=64m --memory 2g --cpus 2 docker.io/library/rockylinux:9 sleep 3600
printf '%s\n' '{"throwaway":true,"family":"rpm","check_system":false,"distribution":"rocky"}' > containers/c1-col-rocky-ro.json
python3 -B collector/main.py --instrument-test col-rpm-ro rpm-readonly --container c1-col-rocky-ro --family rpm
python3 -B collector/validate-output.py rpm-readonly
