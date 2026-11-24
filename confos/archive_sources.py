"""Original component data fixes the archives available for each snapshot choice."""
import json
from pathlib import Path


def sources(snapshot):
    entries = json.loads(Path(__file__).with_name('archive-sources.json').read_text())
    if snapshot not in entries:
        raise ValueError('unsupported archive snapshot: '+snapshot)
    return ''.join('deb [check-valid-until=no] http://snapshot.debian.org/archive/'
                   +archive+'/'+stamp+'/ '+suite+' main\n'
                   for archive, stamp, suite in entries[snapshot])
