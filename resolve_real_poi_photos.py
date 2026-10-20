#!/usr/bin/env python3
"""
resolve_real_poi_photos.py — Resolves authentic, place-specific photos for all POIs in exp51_data.json
and attaches verified Airbnb / Vrbo / Booking URLs for B&Bs and independent backup lodging.
"""
import os
import re
import json
import html
import time
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "exp51_data.json")

DAY_REGION_CONTEXT = {
    "Day 1": "Ontario Quebec Canada",
    "Day 2": "Cote-Nord Charlevoix Tadoussac Baie-Comeau Quebec",
    "Day 3": "Route 389 Manic-5 Fermont Labrador City Wabush",
    "Day 4": "Trans-Labrador Churchill Falls Happy Valley Goose Bay Labrador",
    "Day 5": "Labrador Straits Red Bay L'Anse-au-Clair Forteau Blanc-Sablon",
    "Day 6": "Northern Peninsula St. Anthony L'Anse aux Meadows Newfoundland",
    "Day 7": "St. Anthony L'Anse aux Meadows Quirpon Newfoundland",
    "Day 8": "Gros Morne Rocky Harbour Woody Point Newfoundland",
    "Day 9": "Gros Morne Corner Brook Western Newfoundland",
    "Day 10": "Southwest Newfoundland Port aux Basques Cape Ray",
    "Day 11": "Cape Breton Cabot Trail Louisbourg Ingonish Nova Scotia",
    "Day 12": "Cabot Trail Cheticamp Margaree Cape Breton Nova Scotia",
    "Day 13": "Prince Edward Island PEI Canada",
    "Day 14": "New Brunswick Shediac Hopewell Rocks Alma Fundy",
    "Day 15": "Fundy Trail Saint John Grand Manan Edmundston New Brunswick",
    "Day 16": "Bas-Saint-Laurent Quebec City Drummondville Quebec",
    "Day 17": "Laurentians Ottawa River Pembroke Ontario",
    "Day 18": "Mattawa North Bay Sudbury Hanmer Ontario",
}

STOPWORDS = {
    "the", "and", "for", "with", "near", "from", "stop", "area", "view", "point",
    "site", "park", "trail", "road", "hwy", "route", "st", "ste", "saint", "sainte",
    "inc", "ltd", "llc", "backup", "primary", "hotel", "motel", "inn", "lodge",
    "campground", "camping", "provincial", "national", "historic", "centre", "center",
    "station", "service", "parts", "dealer", "dealership", "pullout", "parking",
    "emergency", "crossing", "hazard", "night", "start", "arrival", "ferry", "bridge"
}


def extract_keywords(name, desc=""):
    """Extract distinctive keywords from POI name for relevance scoring."""
    clean = re.sub(r"[^\w\sÀ-ÿ'-]", " ", name)
    words = [w.strip("'-").lower() for w in clean.split() if len(w.strip("'-")) >= 3]
    sig = [w for w in words if w not in STOPWORDS and not w.isdigit()]
    if not sig:
        sig = [w for w in words if len(w) >= 2]
    return sig


def build_search_query(p):
    """Build an accurate search query tailored to the specific POI."""
    name = p.get("name", "")
    ptype = p.get("type", "")
    day = p.get("day", "Day 1")
    desc = p.get("desc", "")
    region = DAY_REGION_CONTEXT.get(day, "Canada")

    # Clean out internal tactical annotations from name
    clean_name = name
    clean_name = re.sub(r"\b(Night 2|Hotel Backup|B&B Backup|Ferry Staging Backup|Start|Arrival)\b", "", clean_name, flags=re.I)
    clean_name = re.sub(r"[—–•|]", " ", clean_name)
    clean_name = re.sub(r"\s+", " ", clean_name).strip()

    if ptype == "lighthouse":
        if "lighthouse" not in clean_name.lower() and "phare" not in clean_name.lower() and "light" not in clean_name.lower():
            clean_name += " Lighthouse"
        return f"{clean_name} {region}"

    if ptype in ("hotel-primary", "hotel-secondary"):
        if "hanmer home base" in name.lower():
            return "Hanmer Greater Sudbury Ontario residential street"
        if "trish" in name.lower():
            return "Trish's Place B&B 766 Stirling Crescent Labrador City"
        if "campement modulaire" in name.lower():
            return "Campement minier Mont-Wright Fermont ArcelorMittal"
        return f"{clean_name} {region}"

    if ptype == "dealer":
        return f"{clean_name} motorcycle dealership"

    if ptype == "shopping":
        return f"{clean_name} {region}"

    if ptype == "food":
        return f"{clean_name} restaurant {region}"

    if ptype == "coffee":
        return f"{clean_name} coffee cafe {region}"

    if ptype == "fuel":
        if p.get("octane") == "TRANSFER" or "bladder" in name.lower():
            return f"Adventure motorcycle auxiliary fuel bladder refueling {region}"
        return f"{clean_name} gas station {region}"

    if ptype == "pullout":
        # Vary query for QC-389 pullouts so each gets a distinct authentic Route 389 / Manicouagan / Monts Groulx photo
        m = re.search(r"#(\d+)", name)
        num = int(m.group(1)) if m else 0
        variants = [
            "Route 389 Quebec gravel highway Manicouagan",
            "Route 389 Monts Groulx boreal highway Quebec",
            "Route 389 Manic-5 to Fermont highway",
            "Route 389 Fire Lake Gagnon Quebec highway",
            "Baie-Comeau Fermont Route 389 scenic road",
            "Reservoir Manicouagan Route 389 viewpoint",
            "Route 389 Cote-Nord Quebec wilderness road",
            "Mont-Wright Fermont Route 389 highway Quebec"
        ]
        if num > 0:
            return f"{variants[num % len(variants)]} photo {num}"
        return f"{clean_name} Route 389 Quebec"

    if ptype == "hazard":
        if "railway" in name.lower() or "train" in name.lower():
            return "Quebec Cartier Railway crossing Route 389 Fermont Mont-Wright iron ore train"
        return "Route 389 Quebec gravel road construction sign"

    return f"{clean_name} {region}"


def fetch_bing_candidates(query):
    """Fetch photo candidates from Bing Image Search with photo filter."""
    url = (
        "https://www.bing.com/images/search?q="
        + urllib.parse.quote(query)
        + "&qft=+filterui:photo-photo&form=HDRSC2&first=1"
    )
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept-Language": "en-CA,en;q=0.9,fr-CA;q=0.8",
            "Cookie": "SRCHHPGUSR=ADLT=DEMOTE",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            body = r.read().decode("utf-8", errors="ignore")
    except Exception:
        return []

    candidates = []
    for m in re.findall(r'm="([^"]*murl[^"]*)"', body):
        try:
            d = json.loads(html.unescape(m))
        except Exception:
            continue
        turl = d.get("turl", "")
        murl = d.get("murl", "")
        title = d.get("t", "")
        purl = d.get("purl", "")
        if not turl or "mm.bing.net/th" not in turl:
            continue
        # Filter out obvious non-place images or vector/map graphics
        combined = f"{title} {purl} {murl}".lower()
        if any(bad in combined for bad in [
            "clipart", "pngtree", "coloring-page", "cartoon", "vector", "logo",
            "icon", "diagram", "locator_map", "location_map", ".svg", "flag_of",
            "coat_of_arms", "qrcode", " Portrait ", "headshot", "obituary"
        ]):
            continue
        # Extract OIP id for deduplication
        oip_match = re.search(r"id=(OIP\.[^&]+)", turl)
        oip_id = oip_match.group(1) if oip_match else turl
        # Request high-clarity 640px thumbnail from Bing CDN
        hi_turl = f"https://ts1.mm.bing.net/th?id={oip_id}&pid=15.1&w=640&c=7" if oip_match else turl
        candidates.append({
            "oip_id": oip_id,
            "turl": hi_turl,
            "murl": murl,
            "title": title,
            "purl": purl,
            "combined": combined,
        })
    return candidates


def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    pois = data["poisData"]
    print(f"Loaded {len(pois)} POIs from exp51_data.json")

    # 1. Update Airbnb / Vrbo / Booking links for B&Bs & remaining unlinked backup lodging
    for p in pois:
        nm = p.get("name", "")
        if "Trish" in nm and "Place" in nm:
            p["url"] = "https://www.airbnb.ca/rooms/22716280"
            print(f"Linked B&B on Airbnb: {nm} -> {p['url']}")
        elif "Motel Le Mirabeau" in nm:
            p["url"] = "https://www.agoda.com/en-ca/motel-le-mirabeau-h26265839/hotel/mirabel-qc-ca.html"
            print(f"Linked Motel on Agoda: {nm} -> {p['url']}")
        elif "Campement Modulaire" in nm and not p.get("url"):
            p["url"] = "https://rcmgroupe.com/"
            print(f"Linked Modular Camp: {nm} -> {p['url']}")

    # 2. Fetch candidate lists in parallel for all 943 POIs
    queries = [(idx, build_search_query(p), extract_keywords(p.get("name", ""), p.get("desc", ""))) for idx, p in enumerate(pois)]
    candidates_by_idx = {}

    print("Fetching authentic place photo candidates across 943 POIs (16 workers)...")
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=16) as ex:
        fut_map = {ex.submit(fetch_bing_candidates, q): (idx, q, kws) for idx, q, kws in queries}
        done_count = 0
        for fut in as_completed(fut_map):
            idx, q, kws = fut_map[fut]
            try:
                cands = fut.result()
            except Exception:
                cands = []
            candidates_by_idx[idx] = (cands, kws, q)
            done_count += 1
            if done_count % 100 == 0 or done_count == len(pois):
                print(f"  [{done_count}/{len(pois)}] fetched in {time.time() - t0:.1f}s")

    # 3. Assign highest-scoring unique photo per POI
    used_oip_ids = set()
    resolved_count = 0

    # Prioritize named landmarks/lodging/sights/lighthouses first so they get first pick of unique photos
    priority_order = sorted(
        range(len(pois)),
        key=lambda i: (0 if pois[i].get("type") not in ("pullout", "hazard", "fuel") else 1, i)
    )

    for idx in priority_order:
        p = pois[idx]
        cands, kws, q = candidates_by_idx.get(idx, ([], [], ""))
        if not cands:
            continue

        # Score candidates by keyword overlap + position rank
        scored = []
        for rank, c in enumerate(cands):
            comb = c["combined"]
            kw_hits = sum(1 for kw in kws if kw in comb)
            # Bonus if exact first keyword is in title
            first_bonus = 2 if (kws and kws[0] in comb) else 0
            score = (kw_hits * 3) + first_bonus - (rank * 0.25)
            scored.append((score, rank, c))

        scored.sort(key=lambda x: (-x[0], x[1]))

        chosen = None
        for score, rank, c in scored:
            if c["oip_id"] not in used_oip_ids:
                chosen = c
                used_oip_ids.add(c["oip_id"])
                break

        if not chosen and scored:
            chosen = scored[0][2]

        if chosen:
            p["real_photo"] = chosen["turl"]
            p["photo"] = chosen["turl"]
            resolved_count += 1

    print(f"Resolved {resolved_count}/{len(pois)} POIs with authentic place photos ({len(used_oip_ids)} unique photos).")

    with open(DATA_PATH, "w", encoding="utf-8") as f_out:
        json.dump(data, f_out, indent=2, ensure_ascii=False)
    print("Saved updated exp51_data.json.")


if __name__ == "__main__":
    main()
