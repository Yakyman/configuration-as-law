import re, sys, pathlib
# usage: quote.py FILE PATTERN [N_SENTENCES] ; prints the sentence(s) containing PATTERN, verbatim, whitespace collapsed
t = re.sub(r"\s+", " ", pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
n = int(sys.argv[3]) if len(sys.argv) > 3 else 1
for m in re.finditer(sys.argv[2], t):
    s = t.rfind(". ", 0, m.start()) + 2
    e = m.end()
    for _ in range(n):
        k = t.find(". ", e)
        e = len(t) if k < 0 else k + 1
    print("«" + t[s:e].strip() + "»")
