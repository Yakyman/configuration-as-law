#!/bin/sh
# Disposable guest only; tests installation records and membership completeness.
set -eu
mkdir -p /tmp/c1-fixture-pkg/DEBIAN /tmp/c1-fixture-pkg/usr/share/c1-fixture /tmp/c1-fixture-pkg/etc
cat > /tmp/c1-fixture-pkg/DEBIAN/control <<'CONTROL'
Package: c1-fixture
Version: 1.0
Architecture: all
Maintainer: Test <test@example.invalid>
Description: Collector validation fixture
CONTROL
for f in unchanged changed missing; do printf 'installed\n' > /tmp/c1-fixture-pkg/usr/share/c1-fixture/$f; done
printf 'installed-config\n' > /tmp/c1-fixture-pkg/etc/c1-fixture.conf
printf '/etc/c1-fixture.conf\n' > /tmp/c1-fixture-pkg/DEBIAN/conffiles
cat > /tmp/c1-fixture-pkg/DEBIAN/postinst <<'SCRIPT'
#!/bin/sh
printf 'generated at install\n' > /etc/c1-fixture-generated.conf
SCRIPT
chmod 755 /tmp/c1-fixture-pkg/DEBIAN/postinst
(cd /tmp/c1-fixture-pkg; md5sum usr/share/c1-fixture/* etc/c1-fixture.conf > DEBIAN/md5sums)
dpkg-deb --build /tmp/c1-fixture-pkg /tmp/c1-fixture.deb
dpkg -i /tmp/c1-fixture.deb
apt-mark manual c1-fixture
printf 'changed after install\n' > /usr/share/c1-fixture/changed
rm /usr/share/c1-fixture/missing
printf 'changed config\n' > /etc/c1-fixture.conf
mkdir -p /home/user/.config/c1-fixture /home/user/.local/bin
printf '#!/bin/sh\ntrue\n' > /home/user/.local/bin/c1-shebang
python3 -I -S - <<'PY'
from pathlib import Path
p=Path('/home/user/.config/c1-fixture')
for i in range(1200):(p/('member-%04d'%i)).write_text('member %d\n'%i)
(p/'tab\tnewline\nmember').write_text('special name\n')
PY
rm -rf /tmp/c1-fixture-pkg
printf 'fixture installed; explicit package; unchanged/changed/missing files; 1201 group members\n'
