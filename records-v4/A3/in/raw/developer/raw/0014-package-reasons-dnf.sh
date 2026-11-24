dnf -C repoquery --installed --qf '%{name}@%{version}-%{release}.%{arch}	%{reason}\n'
