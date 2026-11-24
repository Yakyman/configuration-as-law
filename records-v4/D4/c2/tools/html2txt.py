import html, re, sys, pathlib
for p in sys.argv[1:]:
    s = pathlib.Path(p).read_text(encoding="utf-8")
    t = html.unescape(re.sub(r"<[^>]+>", "", s))
    t = re.sub(r"[ \t]+", " ", t)
    pathlib.Path(p[:-5] + ".txt").write_text(t, encoding="utf-8")
