"""File USGS Landsat Collection 2 band files into landsat/<date UTC>/<product ID>/ unchanged, with a manifest.
Usage: python3 scripts/ingest.py FILE [FILE ...]
Browser-added suffixes (e.g. _B4_1.TIF) are removed so names match the product's MTL file; the received name is recorded."""
import sys, os, re, json, hashlib, shutil
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
for src in sys.argv[1:]:
    name = os.path.basename(src)
    m = re.search(r"(L[COTEM]0\d_L[12][A-Z]{2}_\d{6}_(\d{8})_\d{8}_\d{2}_[A-Z0-9]{2})_(.+?)(?:_\d+)?(\.TIF|\.txt|\.xml)$", name, re.I)
    if not m: print("skip", name); continue
    pid, date, part, ext = m.groups(); canon = f"{pid}_{part}{ext}"
    dest = os.path.join(REPO, "landsat", f"{date[:4]}-{date[4:6]}-{date[6:]}", pid); os.makedirs(dest, exist_ok=True)
    shutil.copyfile(src, os.path.join(dest, canon))
    mp = os.path.join(dest, "manifest.json")
    man = json.load(open(mp)) if os.path.exists(mp) else {"product_id": pid, "source": "USGS EarthExplorer, Landsat Collection 2", "licence": "Landsat data courtesy of the U.S. Geological Survey (public domain)", "files": {}}
    man["files"][canon] = {"bytes": os.path.getsize(src), "sha256": sha(src), "received_as": name}
    json.dump(man, open(mp, "w"), indent=1); print(canon, man["files"][canon]["bytes"])
