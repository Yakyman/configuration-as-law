import sys
sys.path.insert(0,'c2/work')
from emit import emit
def h7(prog):
    return f'Values read only by {prog} (S2.2-13) with effects beyond it: S2.2-2 gives MUST, S2.2-7 read literally gives NOT; nothing says which prevails.'
H7S='S2.2-2,S2.2-7,S2.2-13'
MAN='doc:https://man7.org/linux/man-pages/'
FD='doc:https://www.freedesktop.org/software/systemd/man/latest/'
OWN='raw:raw/coreos/files.tsv'
STO='raw:raw/coreos/unowned-groups.json'
DIST='raw:c2/raw/dist/'
def run(rows):
    print(emit([list(r) for r in rows]))
