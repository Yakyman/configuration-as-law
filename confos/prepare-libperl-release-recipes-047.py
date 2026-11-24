#!/usr/bin/python3
"""Prepare the next release recipes without changing VERSION or components."""
from pathlib import Path
def remap(text):
 text=text.replace('0.46','@NEXT@').replace('0.45','@PREV@').replace('0.44','@DROP@')
 text=text.replace('@NEXT@','0.47').replace('@PREV@','0.46').replace('@DROP@','0.45')
 return text.replace('046','047').replace('LIBPYTHON','LIBPERL').replace('libpython','libperl').replace('embedded-python','embedded-perl').replace('libperl3.13','libperl5.40').replace('3.13.5-2+deb13u5','5.40.1-6+deb13u1').replace('libperl5.40.so.1.0','libperl.so.5.40.1').replace('e21f94b1ccdaed10a83120d9150a4efd162e847d484383f57e79ff777e29328b','9055c106dbe1ab867bb2832956a558c3e1d51f2918581c6e192f978a806df3c8').replace('NATIVE46','NATIVE47').replace('CANONICAL46','CANONICAL47').replace('CANDIDATE46','CANDIDATE47').replace('native46','native47').replace('Compose46','Compose47').replace('sealed45','sealed46').replace('22461','22464')
for old,new in [('prepare-libpython-046.py','prepare-libperl-047.py'),('prepare-libpython-release-046.sh','prepare-libperl-release-047.sh'),('archive-libpython-046.sh','archive-libperl-047.sh'),('fetch-libpython-046.sh','fetch-libperl-047.sh'),('cleanup-libpython-046.sh','cleanup-libperl-047.sh')]:
 Path(new).write_text(remap(Path(old).read_text()))
text=remap(Path('build-libpython-fixture-046.py').read_text())
start=text.index('code=b');end=text.index("(inputs/'recorded.py')")
perl=Path('embedded-perl-private-build.py').read_text();a=perl.index('code=b');b=perl.index("(inputs/'recorded.pl')")
text=text[:start]+perl[a:b]+text[end:]
text=text.replace('recorded.py','recorded.pl')
a=text.index("for name in ('recorded-filename-reader.py'");b=text.index("(inputs/'declaration.conf')",a)
text=text[:a]+text[b:]
Path('build-libperl-fixture-047.py').write_text(text)
text=remap(Path('probe-libpython-046.sh').read_text())
text=text.replace(" guest 'python3 /usr/local/share/probe-recorded-filename-reader.py'\n",'')
text=text.replace("'/usr/local/bin/embedded-perl file /usr/local/share/embedded-recorded.py'","'/usr/local/bin/embedded-perl /usr/local/share/embedded-recorded.pl'")
Path('probe-libperl-047.sh').write_text(text)
print('47 RECIPES PREPARED; NO RELEASE PROMOTION')
