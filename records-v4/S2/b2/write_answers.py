import csv

csv.field_size_limit(10**9)
rows = list(csv.DictReader(open('S2/sample/flagged.tsv'), delimiter='\t'))
cups_g = ("yes: covered by the line of package cups", "yes",
          "Hard links to packaged, unchanged files in backend-available (same inodes), made by cups-daemon postinst from a default debconf selection: default content created during installation (raw/cups-daemon-postinst-backends.txt).")
cups_s = ("yes: covered by the line of package cups", "yes",
          "Same inode as packaged unchanged backend-available/snmp; link created by cups-daemon postinst during installation from default debconf selection (raw/cups-daemon-postinst-backends.txt).")
steam = ("no", "yes",
         "Compressed Steam client update archive (.zip.vz) the self-updating client downloaded; no ELF or shebang, never executed itself; the unpacked client is what is installed.")


def k3s(n):
    return ("yes: covered by the line of k3s (/usr/local/bin/k3s)", "yes",
            f"{n} extracted by the k3s binary at first start (ctime seconds after install); executable code of k3s, recording k3s covers it; forbids nothing.")


ans = {
    'gaming-0b9c75abae9461b0be7b041d': cups_g,
    'gaming-7b8b804e906bab4f5a36ccf2': cups_s,
    'gaming-4538cc406b1a701b2b46aa9a': steam,
    'gaming-92303a3b6a6e1ad452236f8b': steam,
    'gaming-b9490dffe916c5dcc4575874': steam,
    'server-0343cc0e3743fdc6279f4a3e': k3s('Multicall coreutils'),
    'server-9c59629a43e8b28a746de9d5': k3s('CNI plugin multicall binary'),
    'server-a1bf573f2de859142047fce6': k3s('Running k3s binary (process executable)'),
}
with open('S2/b2/answers.tsv', 'w', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n')
    w.writerow(['source', 'id', 'by_meaning', 'without_forbidding', 'reason'])
    for r in rows:
        a = ans[r['id']]
        assert len(a[2].split()) <= 30, (r['id'], len(a[2].split()))
        w.writerow([r['source'], r['id'], *a])
with open('S2/b2/DONE', 'w') as f:
    f.write(f"rows: {len(rows)}\n")
print(len(rows))
