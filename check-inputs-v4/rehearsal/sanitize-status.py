#!/usr/bin/env python3
import pathlib,re,sys
for name in sys.argv[1:]:
 p=pathlib.Path(name)
 if not p.exists():continue
 text=p.read_text()
 text=re.sub(r'query-packages-flatpak-user-[0-9]+-','query-packages-flatpak-user-',text)
 text=re.sub(r'(\tquery-(?:package-reason-xbps|package-files-xbps))-([^\t\n]*)',r'\1',text)
 text=re.sub(r'\tquery-user-[^\t\n]*-(service|timer|unit-file)\t',r'\tquery-user-\1\t',text)
 text=re.sub(r'(\tquery-(?:sudo|user-containers|user-images|package-manager-discovery-user))-[^\t\n]*',r'\1',text)
 p.write_text(text)
