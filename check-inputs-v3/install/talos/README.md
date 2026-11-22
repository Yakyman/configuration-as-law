# Talos clean installation recipe

Use the version-pinned 1.14.6 metal-amd64 ISO and talosctl; verify SHA256 and Sigstore bundles before either is used. `C1/raw/talos-verification.txt` records success. Bundle verification is constrained to certificate issuer `https://token.actions.githubusercontent.com` and exact identity `https://github.com/siderolabs/talos/.github/workflows/ci.yaml@refs/tags/v1.14.6`.

Generate a control-plane configuration with the matching talosctl:

```sh
talosctl gen config cal-test https://10.0.2.15:6443 \
  --install-disk /dev/vda \
  --install-image factory.talos.dev/metal-installer/376567988ad370138ad8b2698212367b8edcb69b5fd68c80be1f2ec7d603b4ba:v1.14.6 \
  --output-dir C1/install/talos --with-docs=false --with-examples=false
```

Add `127.0.0.1` to machine certSANs for the loopback-forwarded authenticated API connection. `controlplane.yaml` is the exact installation input, including generated laboratory PKI; it is not a template. It is for isolated disposable machines only. The original failed legacy-installer configuration is preserved as `controlplane-attempt1.yaml`, not the selected input.

Create a blank 24 GiB qcow2 disk, boot with `boot.sh` under a persistent user unit holding slot 11, and submit:

```sh
talosctl apply-config --insecure --nodes 127.0.0.1:50111 --file C1/install/talos/controlplane.yaml
```

The first maintenance API submission is the documented initial installation operation. After disk installation and reboot, authenticate and request only `version --short`. This is the shell-less equivalent of login smoke. Do not bootstrap a Kubernetes cluster or request services, packages, files, accounts, or processes. Request `shutdown --force --wait=false`, wait for the host VM process to exit, and make `C1/base/talos.qcow2` read-only.

Copy the generated `talosconfig` to `C1/base/talosconfig` on the host. The lab's `run` runs stdin on the host, with talosctl receiving the clone's configured API endpoint and nodes; it does not provide an in-machine shell. `--root` has no different shell meaning on Talos. The lab command smoke is a version request and a host `printf`, without inventory.

Sources: https://docs.siderolabs.com/talos/v1.14/reference/cli ; https://pkg.go.dev/github.com/siderolabs/terraform-provider-talos@v0.12.0/pkg/talos#GenerateInstallerImage .
