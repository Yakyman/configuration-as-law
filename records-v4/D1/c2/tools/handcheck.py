import sys
from classify import *
for i in sys.argv[1:]:
    o = [x for x in objs if x["id"] == i.replace("microos-", "")][0]
    paths = [m["path"] for m in members(o)] if o["kind"] == "stored-outside-packages" else [o["name"]]
    print("==", i, o["name"])
    for p in paths[:6]:
        d = fs[p]; L = p[len(SNAP):] if p.startswith(SNAP + "/") else p
        e = rpm.get(L, [("-", "", "", "", "")])[0]
        lv = fs.get(L, {})
        print("  ", L, d["type"], d["mode"], d.get("size"), "| rpm:", e[0].split("@")[0], e[1], e[2][:12], oct(int(e[3]) & 0o7777) if e[3] else "", "| sig:", h(d.get("signature",""))[:12], "full" if d.get("signature_bytes") == d.get("size") else "prefix",
              "| live same inode/ctime:", lv.get("inode") == d.get("inode") and lv.get("ctime") == d.get("ctime"), integ.get(L), "->", mdec(p)[0])
