#!/bin/bash
set -euxo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends auditd expect polkitd pkexec
mkdir -p /usr/local/lib/e2 /var/lib/e2/probes /var/lib/e2/markers
id e2op || useradd -m -u 1102 -s /bin/bash -G sudo e2op
printf 'e2op:<REDACTED-12>\nroot:<REDACTED-13>\n' | chpasswd
install -d -m 0700 -o e2op -g e2op /home/e2op/.ssh
install -m 0600 -o e2op -g e2op /root/.ssh/authorized_keys /home/e2op/.ssh/authorized_keys
printf 'Defaults:e2op timestamp_type=tty,timestamp_timeout=5\ne2op ALL=(root) PASSWD: ALL\n' >/etc/sudoers.d/e2
chmod 0440 /etc/sudoers.d/e2
visudo -c
systemctl unmask cron.service
systemctl start cron.service auditd.service polkit.service
# Existing stand instrumentation is retained; this new account has an ordinary
# Bash shell so cal-alice/cal-bob profiles do not decide the O4 measurements.
auditctl -b 16384
auditctl -r 0
auditctl -a always,exit -F arch=b64 -S execve -k e2exec
auditctl -w /var/lib/e2/markers -p wa -k e2marker
{ date -Is; uname -a; dpkg-query -W auditd expect polkitd pkexec sudo systemd cron openssh-server; id e2op; cat /proc/self/attr/current; cat /etc/sudoers.d/e2; cat /etc/pam.d/sshd /etc/pam.d/cron /etc/pam.d/sudo; auditctl -s; auditctl -l; systemctl is-active cron auditd polkit; sshd -T; } >/var/lib/e2/setup-state.txt
