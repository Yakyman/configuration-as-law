set -eu
cp /tmp/codeboundary.py /tmp/guard.py /tmp/capture.py /usr/local/lib/stand/
python3 -I /tmp/install-code-boundary.py
systemctl restart ssh
# Refresh implementation baseline only on this disposable development VM.
python3 -B /usr/local/lib/stand/capture.py
/usr/local/bin/stand-apply /etc/stand/factory
/usr/local/bin/stand-verify
