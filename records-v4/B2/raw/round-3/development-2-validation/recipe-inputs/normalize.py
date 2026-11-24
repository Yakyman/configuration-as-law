#!/usr/bin/python3 -I
"""Deterministic non-secret defaults and explicit lab-key recipe inputs."""
import pathlib,shutil,os
P=pathlib.Path
# Host identity is an explicit retained laboratory input shared across recipe
# executions, not fresh entropy mistakenly required by the same declaration.
for p in P('/etc/ssh').glob('ssh_host_*'):p.unlink()
for suffix,mode in (('',0o600),('.pub',0o644)):
    p=P('/etc/ssh/ssh_host_ed25519_key'+suffix)
    shutil.copyfile('/tmp/host_ed25519'+suffix,p);p.chmod(mode)
    P('/tmp/host_ed25519'+suffix).unlink()
# This prototype has no TLS service; package-generated example credentials
# contribute no live service and are not part of the factory content closure.
for name in ('/etc/ssl/private/ssl-cert-snakeoil.key','/etc/ssl/certs/ssl-cert-snakeoil.pem'):
    P(name).unlink(missing_ok=True)
print('Explicit host-key input and stable factory defaults installed')
