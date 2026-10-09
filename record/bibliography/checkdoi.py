"""Resolve DOIs: Crossref for title/year, doi.org redirect as fallback (DataCite, arXiv).
Usage: python3 -I checkdoi.py < file_with 'key doi' lines"""
import sys, json, urllib.request, urllib.parse
def crossref(doi):
    try:
        with urllib.request.urlopen("https://api.crossref.org/works/" + urllib.parse.quote(doi), timeout=30) as r:
            m = json.load(r)["message"]
            return (m.get("title") or ["?"])[0], (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
    except Exception:
        return None
def doiorg(doi):
    req = urllib.request.Request("https://doi.org/api/handles/" + doi)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
            return d.get("responseCode") == 1
    except Exception:
        return False
for line in sys.stdin:
    parts = line.split()
    if len(parts) < 2: continue
    key, doi = parts[0], parts[1]
    c = crossref(doi)
    if c: print(f"OK  {key:28} {doi:45} {c[1]} | {c[0][:70]}")
    elif doiorg(doi): print(f"OK? {key:28} {doi:45} (registered at doi.org, not Crossref)")
    else: print(f"BAD {key:28} {doi}")
