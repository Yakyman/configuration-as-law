import urllib.request,lzma,re,csv,pathlib
installed={l.split('\t')[0].split(':')[0] for l in open('D1/in/raw/mint/raw/003-packages-root-dpkg-query.out')}
u='https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz'
s=lzma.decompress(urllib.request.urlopen(u,timeout=30).read()).decode()
targets=['libexttextcat','liblangtag','liblouisutdml','libespeak-ng','liblouis','libopenal']
out=['Source: '+u]
for block in s.split('\n\n'):
 m=re.search(r'^Package: (.+)$',block,re.M)
 if not m or m.group(1) not in installed:continue
 deps=' '.join(re.findall(r'^(?:Depends|Recommends): (.+)$',block,re.M))
 if any(t in deps for t in targets):out.append(m.group(1)+': '+deps)
pathlib.Path('D1/review/cards14-raw/mint-reader-deps.txt').write_text('\n'.join(out)+'\n')
print('\n'.join(out))
