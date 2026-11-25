#!/usr/bin/python3
"""Locate the one function that executes Basic code in the office suite's merged core library.

The source of the suite (basic/source/classes/sbxmod.cxx, class RunInitGuard) constructs the
Basic runtime in one place and runs it by one loop, `while (m_xRt->Step()) {}`; that loop
serves both SbModule::Run and SbModule::RunInit. SbiRuntime::Step() executes one instruction
of compiled Basic and returns whether to go on. The function is not exported, so its address
is taken from the debug package of the same build (matched by build ID).

Usage: locate-basic-step.py INPUT_DIR
INPUT_DIR is the output of fetch-basic-library.py. For every release this downloads the debug
package named in basic-guard-inputs.json (URL and checksum), finds the symbol, converts its
address to a file offset, counts the call instructions that target it, and writes
INPUT_DIR/located.json. Runs on the build host; needs binutils and network access.
"""
import hashlib
import json
import re
import struct
import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SYMBOL = '_ZN10SbiRuntime4StepEv'
REPLACEMENT = bytes.fromhex('31c0c3')  # xor %eax,%eax; ret: "do not go on", nothing executed
ENDBR64 = bytes.fromhex('f30f1efa')
inputs = Path(sys.argv[1]).resolve()
pinned = json.loads((HERE/'basic-guard-inputs.json').read_text())
releases = json.loads((inputs/'releases.json').read_text())
located = {}
for release, pin in sorted(pinned['releases'].items()):
    folder = inputs/re.sub(r'[^A-Za-z0-9.+~-]', '_', release)
    library = folder/'libmergedlo.so'
    data = library.read_bytes()
    assert releases[release]['archive_sha256'] == pin['archive_sha256'], release
    assert hashlib.sha256(data).hexdigest() == pin['original_sha256'], release
    notes = subprocess.check_output(['readelf', '-n', str(library)], text=True)
    build_id = re.search(r'Build ID: ([0-9a-f]{40})', notes).group(1)
    debug = folder/'libmergedlo.debug'
    if not debug.exists():
        archive = folder/'debug.deb'
        if not archive.exists():
            urllib.request.urlretrieve(pin['debug_url'], archive)
        assert hashlib.sha256(archive.read_bytes()).hexdigest() == pin['debug_archive_sha256'], release
        member = f'./usr/lib/debug/.build-id/{build_id[:2]}/{build_id[2:]}.debug'
        process = subprocess.Popen(['dpkg-deb', '--fsys-tarfile', str(archive)], stdout=subprocess.PIPE)
        with tarfile.open(fileobj=process.stdout, mode='r|') as stream:
            for entry in stream:
                if entry.name == member:
                    debug.write_bytes(stream.extractfile(entry).read())
        process.wait()
        archive.unlink()
    symbols = subprocess.check_output(['nm', '--defined-only', str(debug)], text=True)
    matches = [line.split() for line in symbols.splitlines() if line.endswith(' '+SYMBOL)]
    assert len(matches) == 1 and matches[0][1] in 'tT', (release, matches)
    address = int(matches[0][0], 16)
    # Program headers of the shipped library: the loadable segment that holds the address.
    assert data[:6] == b'\x7fELF\x02\x01'
    phoff, = struct.unpack_from('<Q', data, 32)
    phentsize, phnum = struct.unpack_from('<HH', data, 54)
    offset = None
    for index in range(phnum):
        p_type, p_flags, p_offset, p_vaddr, _, p_filesz = struct.unpack_from('<IIQQQQ', data, phoff+index*phentsize)
        if p_type == 1 and p_flags & 1 and p_vaddr <= address < p_vaddr+p_filesz:
            offset = address-p_vaddr+p_offset
            text = (p_vaddr, p_offset, p_filesz)
    assert offset is not None, release
    entry = data[offset:offset+16]
    skip = 4 if entry.startswith(ENDBR64) else 0
    original = data[offset+skip:offset+skip+len(REPLACEMENT)]
    # Direct calls and jumps (rel32) into the function from the executable segment.
    vaddr, start, size = text
    calls = 0
    for match in re.finditer(rb'[\xe8\xe9]', data[start:start+size]):
        position = match.start()
        if position+5 > size:
            continue
        displacement, = struct.unpack_from('<i', data, start+position+1)
        if vaddr+position+5+displacement == address:
            calls += 1
    patched = bytearray(data)
    patched[offset+skip:offset+skip+len(REPLACEMENT)] = REPLACEMENT
    located[release] = {
        'archive_sha256': pin['archive_sha256'], 'original_sha256': pin['original_sha256'],
        'debug_archive_sha256': pin['debug_archive_sha256'], 'build_id': build_id, 'symbol': SYMBOL,
        'address': hex(address), 'offset': offset+skip, 'entry': entry.hex(), 'original': original.hex(),
        'replacement': REPLACEMENT.hex(), 'call_sites': calls, 'sha256': hashlib.sha256(patched).hexdigest()}
    print(release, json.dumps(located[release]), flush=True)
(inputs/'located.json').write_text(json.dumps(located, indent=1, sort_keys=True)+'\n')
