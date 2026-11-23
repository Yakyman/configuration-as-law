#!/bin/sh
set -eu
cd "$1"
export TMPDIR="$PWD"
podman --root "$PWD/podman-root" --runroot "$PWD/podman-run" --storage-driver vfs run -d --name c1-col-rocky --hostname col-rpm --memory 2g --cpus 2 docker.io/library/rockylinux:9 sleep 7200
printf '%s\n' '{"throwaway":true,"family":"rpm","check_system":false,"distribution":"rocky"}' > containers/c1-col-rocky.json
