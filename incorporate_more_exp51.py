#!/usr/bin/env python3
"""
incorporate_more_exp51.py — Parses and incorporates all feedback from
C:\\Users\\Jamie\\Downloads\\MORE Exp 51.md into exp51_data.json,
and resolves authentic photos for the new POIs.
"""
import os
import re
import json
import math
import html
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "exp51_data.json")
MD_PATH = r"C:\Users\Jamie\Downloads\MORE Exp 51.md"


def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2)**2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def fetch_bing_candidates(query):
    url = (
        "https://www.bing.com/images/search?q="
        + urllib.parse.quote(query)
        + "&qft=+filterui:photo-photo&form=HDRSC2&first=1"
    )
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept-Language": "en-CA,en;q=0.9",
            "Cookie": "SRCHHPGUSR=ADLT=DEMOTE",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            body = r.read().decode("utf-8", errors="ignore")
    except Exception:
        return []

    out = []
    for m in re.findall(r'm="([^"]*murl[^"]*)"', body):
        try:
            d = json.loads(html.unescape(m))
        except Exception:
            continue
        turl = d.get("turl", "")
        title = d.get("t", "")
        purl = d.get("purl", "")
        murl = d.get("murl", "")
        if not turl or "mm.bing.net/th" not in turl:
            continue
        comb = f"{title} {purl} {murl}".lower()
        if any(bad in comb for bad in ["clipart", "pngtree", "cartoon", "vector", "logo", "locator_map", ".svg"]):
            continue
        oip_m = re.search(r"id=(OIP\.[^&]+)", turl)
        oip_id = oip_m.group(1) if oip_m else turl
        hi_turl = f"https://ts1.mm.bing.net/th?id={oip_id}&pid=15.1&w=640&c=7" if oip_m else turl
        out.append({"oip_id": oip_id, "turl": hi_turl, "comb": comb})
    return out


def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    pois = data["poisData"]
    # Remove any previous run of more_exp51_added so script is 100% idempotent
    pois = [p for p in pois if not p.get("more_exp51_added")]
    print(f"Base POIs before MORE Exp 51.md ingestion: {len(pois)}")

    used_oip_ids = set()
    for p in pois:
        rp = p.get("real_photo", "")
        m = re.search(r"id=(OIP\.[^&]+)", rp)
        if m:
            used_oip_ids.add(m.group(1))

    added_pois = []

    def add_item(name, lat, lon, ptype, day_num, desc, cost="Free", hours="24 Hours (Open Access)", admission="Free", url=""):
        # Check duplicate within 40m of same type
        for ep in pois + added_pois:
            if ep.get("type") == ptype and haversine_m(lat, lon, ep["lat"], ep["lon"]) < 40:
                return
        item = {
            "name": name,
            "lat": round(float(lat), 6),
            "lon": round(float(lon), 6),
            "type": ptype,
            "day": f"Day {day_num}" if isinstance(day_num, int) else day_num,
            "desc": desc,
            "cost": cost,
            "hours": hours,
            "admission": admission,
            "url": url,
            "more_exp51_added": True,
        }
        added_pois.append(item)

    # ==========================================================================
    # 1. WELCOME TO (CITY / TOWN / PROVINCE) SIGNAGE POIs
    # ==========================================================================
    welcome_signs = [
        ("📸 Welcome to Mattawa Sign (Voyageur Country)", 46.3138, -78.7125, 1, "Town of Mattawa highway welcome sign at the confluence of the Mattawa and Ottawa Rivers."),
        ("📸 Welcome to Pembroke Sign (Heart of the Ottawa Valley)", 45.8165, -77.1350, 1, "City of Pembroke welcome sign along Highway 17 in the Upper Ottawa Valley."),
        ("📸 Bienvenue au Québec Sign (Portage-du-Fort / Route 148)", 45.5902, -76.6635, 1, "Historic Ottawa River interprovincial bridge welcome signage entering Pontiac County, Québec."),
        ("📸 Bienvenue à Trois-Rivières Sign", 46.3320, -72.5650, 2, "City of Trois-Rivières highway welcome sign on the Chemin du Roy (Route 138)."),
        ("📸 Bienvenue à Tadoussac Sign", 48.1465, -69.7185, 2, "Historic village of Tadoussac welcome sign on the north shore of the Saguenay Fjord."),
        ("📸 Bienvenue à Baie-Comeau Sign (Gateway to Route 389)", 49.2165, -68.1650, 2, "Baie-Comeau city welcome sign at the southern terminus of Route 389."),
        ("📸 Welcome to Labrador City / Wabush Sign", 52.9260, -66.9150, 3, "Town of Labrador City & Wabush welcome sign welcoming riders into Labrador West on Route 500."),
        ("📸 Welcome to Churchill Falls Sign", 53.5515, -64.0285, 4, "Town of Churchill Falls welcome sign along the Trans-Labrador Highway (Route 500)."),
        ("📸 Welcome to Happy Valley-Goose Bay Sign", 53.2960, -60.4350, 4, "Town of Happy Valley-Goose Bay welcome sign at the western gateway on Route 500."),
        ("📸 Timezone Border Sign (Atlantic / Newfoundland Time — Route 510)", 52.860333, -57.083066, 5, "Official Trans-Labrador Highway Route 510 Timezone Border Sign marking the transition between Atlantic and Newfoundland Time."),
        ("📸 Welcome to Port Hope Simpson Sign", 52.5495, -56.3090, 5, "Town of Port Hope Simpson welcome sign on the Alexis River along Route 510."),
        ("📸 Welcome to Mary's Harbour Sign", 52.3155, -55.8395, 5, "Town of Mary's Harbour coastal welcome sign on the Labrador Straits."),
        ("📸 Welcome to Red Bay Sign (UNESCO Basque Whaling Port)", 51.7365, -56.4320, 5, "Town of Red Bay welcome sign entering the historic Basque whaling harbor on Route 510."),
        ("📸 Town of Pinware Welcome Sign", 51.631127, -56.709958, 5, "Official Town of Pinware roadside welcome sign along Route 510 on the Labrador Straits."),
        ("📸 Welcome to Forteau Sign", 51.4820, -56.9580, 5, "Town of Forteau welcome sign overlooking Forteau Bay on Route 510."),
        ("📸 Welcome to L'Anse-au-Clair Sign", 51.4255, -57.0585, 5, "Town of L'Anse-au-Clair welcome sign near the southern terminus of Route 510."),
        ("📸 Labrador Gateway Trail Sign (NL / QC Border)", 51.420616, -57.099853, 5, "Iconic Labrador Coastal Drive / Gateway to Labrador highway sign at the southern Labrador border."),
        ("📸 Bienvenue au Québec Border Sign (Blanc-Sablon / Route 138)", 51.420052, -57.105274, 5, "Official Québec provincial border welcome sign entering Blanc-Sablon from L'Anse-au-Clair."),
        ("📸 Welcome to St. Anthony Sign", 51.3750, -55.6050, 6, "Town of St. Anthony welcome sign near the northern tip of Newfoundland's Great Northern Peninsula."),
        ("📸 Welcome to Rocky Harbour Sign (Gros Morne Heart)", 49.5890, -57.9120, 8, "Town of Rocky Harbour welcome sign overlooking Bonne Bay in Gros Morne National Park."),
        ("📸 Welcome to Corner Brook Sign", 48.9550, -57.9320, 9, "City of Corner Brook welcome sign in the Humber Valley along TCH-1."),
        ("📸 Welcome to Port aux Basques Sign (Gateway to Newfoundland)", 47.5785, -59.1460, 10, "Town of Channel-Port aux Basques welcome sign overlooking the Marine Atlantic ferry harbor."),
        ("📸 Welcome to Cape Breton Island Sign", 45.6470, -61.4120, 11, "Iconic Welcome to Cape Breton Island sign at the Canso Causeway gateway."),
        ("📸 Welcome to Baddeck Sign (Cabot Trail Start / Finish)", 46.0985, -60.7550, 11, "Village of Baddeck welcome sign on the Bras d'Or Lake shoreline."),
        ("📸 Welcome to Chéticamp Sign (Acadian Coastal Hub)", 46.6580, -60.9850, 12, "Acadian village of Chéticamp welcome sign at the western gateway to Cape Breton Highlands National Park."),
        ("📸 Welcome to New Brunswick / Bienvenue au Nouveau-Brunswick Sign", 46.1350, -63.8420, 14, "Official New Brunswick provincial welcome sign at the Cape Jourimain approach from Confederation Bridge."),
        ("📸 Welcome to Shediac Sign (Lobster Capital of the World)", 46.2195, -64.5480, 14, "Town of Shediac welcome sign near the World's Largest Lobster monument."),
        ("📸 Welcome to Alma Sign (Fundy Gateway)", 45.6020, -64.9480, 14, "Village of Alma coastal welcome sign at the eastern entrance to Fundy National Park."),
        ("📸 Welcome to Saint John Sign (Bay of Fundy Port City)", 45.2850, -66.0520, 15, "City of Saint John welcome sign along the Bay of Fundy corridor."),
        ("📸 Welcome to Edmundston Sign (Madawaska Republic)", 47.3650, -68.3220, 15, "City of Edmundston welcome sign in northwestern New Brunswick."),
        ("📸 Bienvenue à Drummondville Sign", 45.8880, -72.4820, 16, "City of Drummondville welcome sign on the Saint-François River."),
        ("📸 Welcome to North Bay Sign (Gateway of the North)", 46.3050, -79.4420, 18, "City of North Bay welcome sign on the shore of Lake Nipissing (Hwy 17)."),
        ("📸 Welcome to Greater Sudbury / Hanmer Sign", 46.6450, -80.9850, 18, "City of Greater Sudbury / Valley East welcome sign returning to Hanmer Home Base."),
    ]
    for nm, lat, lon, dnum, desc in welcome_signs:
        add_item(nm, lat, lon, "sight", dnum, desc)

    # ==========================================================================
    # 2. SPECIAL EMERGENCY PHONES & SATELLITE PHONE STATIONS (QC-389 & TLH)
    # ==========================================================================
    emergency_phones = [
        # QC-389 Roadside Emergency Telephones (Téléphones d'urgence & Starlink SOS booths)
        ("📞 QC-389 Emergency Telephone Booth — Km 52", 49.5650, -68.2580, 3, "MTMD roadside emergency telephone booth at Km 52 of Route 389 north of Baie-Comeau."),
        ("📞 QC-389 Emergency Telephone Booth — Km 95 (Manic-3 Corridor)", 49.8920, -68.4250, 3, "MTMD / Hydro-Québec roadside emergency telephone at Km 95 of Route 389."),
        ("📞 QC-389 Emergency Telephone Booth — Km 165", 50.3410, -68.6180, 3, "MTMD roadside emergency telephone booth at Km 165 of Route 389 approaching Manic-5."),
        ("📞 QC-389 Emergency Telephone — Km 214 (Motel de l'Énergie / Manic-5)", 50.6428, -68.7240, 3, "Emergency telephone and landline access at Km 214 (Motel de l'Énergie / Daniel-Johnson Dam)."),
        ("📞 QC-389 Emergency Telephone Booth — Km 272", 51.0280, -68.3840, 3, "MTMD wilderness emergency telephone booth at Km 272 along the Manicouagan Reservoir gravel stretch."),
        ("📞 QC-389 Emergency Telephone — Km 318 (Relais-Gabriel MTMD Garage)", 51.3298, -68.1332, 3, "Emergency public telephone at Relais-Gabriel / Garage du Ministère (Km 318 of Route 389)."),
        ("📞 QC-389 Starlink Emergency Telephone Booth — Km 364 (Monts Groulx)", 51.6380, -68.1950, 3, "High-speed Starlink-equipped MTMD emergency SOS telephone booth at Km 364 in the Monts Groulx highlands."),
        ("📞 QC-389 Emergency Telephone Booth — Km 418 (Rivière-Mouchalagane)", 51.9840, -68.1120, 3, "MTMD wilderness emergency telephone booth at Km 418 near Rivière-Mouchalagane."),
        ("📞 QC-389 Starlink Emergency Telephone Booth — Km 464", 52.4350, -67.4820, 3, "Starlink-upgraded MTMD emergency SOS satellite telephone booth at Km 464 of Route 389."),
        ("📞 QC-389 Emergency Telephone Booth — Km 495 (Fire Lake)", 52.6180, -67.3920, 3, "MTMD emergency roadside telephone at Km 495 near the Fire Lake iron mine transition."),
        ("📞 QC-389 Emergency Telephone Booth — Km 511 (Mont-Wright Approach)", 52.7150, -67.3810, 3, "MTMD emergency roadside telephone at Km 511 approaching Mont-Wright and Fermont."),
        # Trans-Labrador Highway (NL-500 & NL-510) Satellite Phone Loan Stations & Starlink Highway Depots
        ("📡 TLH Emergency Satellite Phone Hub — Wabush Hotel (Labrador West)", 52.9275, -66.8665, 3, "Official Gov of NL Free Emergency Satellite Phone Loan Program pickup/drop-off hub at Wabush Hotel (709-282-3221). Pre-programmed to dial RNC/RCMP."),
        ("📡 TLH Highway Depot Emergency Comms — Ranger Lake Depot (Route 500)", 53.4050, -65.0430, 4, "NL Dept of Transportation Ranger Lake Highway Maintenance Depot with emergency satellite communications on Route 500."),
        ("📡 TLH Emergency Satellite Phone Hub — Midway Travel Inn (Churchill Falls)", 53.5478, -63.9930, 4, "Official Gov of NL Free Emergency Satellite Phone Loan Program hub in Churchill Falls (709-925-3211)."),
        ("📡 TLH Highway Depot Public Starlink Wi-Fi & Emergency Comms — Cache River Depot", 53.2962, -62.6265, 4, "NL Transportation Cache River Highway Depot (~120 km west of Goose Bay on Route 500) equipped with free public Starlink Wi-Fi for emergency Wi-Fi calling."),
        ("📡 TLH Emergency Satellite Phone Hub — Hotel North Two / Royal Inn (Goose Bay)", 53.3020, -60.3815, 4, "Official Gov of NL Free Emergency Satellite Phone Loan Program hub in Happy Valley-Goose Bay (709-896-3398 / 709-896-2456)."),
        ("📡 TLH Highway Depot Public Starlink Wi-Fi & Emergency Comms — Crook's Lake Depot", 52.6862, -58.5034, 5, "NL Transportation Crook's Lake Highway Depot (~150 km south of Goose Bay on Route 510) equipped with free public Starlink Wi-Fi for emergency calling."),
        ("📡 TLH Highway Depot Free Emergency Wi-Fi — Cartwright Junction Depot", 53.058157, -57.488761, 5, "Cartwright Junction Highway Depot on Route 510 offering 24/7 free public emergency Wi-Fi hotspot and staging."),
        ("📡 TLH Emergency Satellite Phone Hub — Alexis Hotel (Port Hope Simpson)", 52.5488, -56.3072, 5, "Official Gov of NL Free Emergency Satellite Phone Loan Program hub at Alexis Hotel in Port Hope Simpson (709-960-0228)."),
        ("📡 TLH Emergency Satellite Phone Hub — Riverlodge Hotel (Mary's Harbour)", 52.3130, -55.8380, 5, "Official Gov of NL Free Emergency Satellite Phone Loan Program hub at Riverlodge Hotel in Mary's Harbour."),
        ("📡 TLH Highway Depot Emergency Comms — Chateau Pond Maintenance Depot", 51.9795, -56.3050, 5, "NL Transportation Chateau Pond Highway Maintenance Depot between Mary's Harbour and Red Bay on Route 510."),
        ("📡 TLH Emergency Satellite Phone Hub — BNL Enterprises (Red Bay)", 51.7308, -56.4282, 5, "Official Gov of NL Free Emergency Satellite Phone Loan Program hub at BNL Enterprises in Red Bay."),
        ("📡 TLH Emergency Satellite Phone Hub — Northern Light Inn (L'Anse-au-Clair)", 51.4210, -57.0598, 5, "Official Gov of NL Free Emergency Satellite Phone Loan Program southern drop-off/pickup hub at Northern Light Inn (709-931-2332)."),
    ]
    for nm, lat, lon, dnum, desc in emergency_phones:
        add_item(nm, lat, lon, "sight", dnum, desc)

    # ==========================================================================
    # 3. PARSE ALL 349 EMERGENCY PULLOUTS / PARKING STOPS FROM MORE Exp 51.md
    # ==========================================================================
    with open(MD_PATH, "r", encoding="utf-8") as f_md:
        md_lines = [ln.strip() for ln in f_md.readlines()]

    # Pullouts section runs from line index 9 to "Lake  \\  Ocean viewpoint"
    pullout_idx = 0
    for ln in md_lines[9:716]:
        if not ln:
            continue
        # Check DMS coordinate: 53°11'52.6"N 60°27'39.2"W
        if "53°11'52.6" in ln:
            lat = 53 + 11 / 60.0 + 52.6 / 3600.0
            lon = -(60 + 27 / 60.0 + 39.2 / 3600.0)
            note = ""
        else:
            clean_ln = ln.replace("*", "").strip()
            m = re.match(r"^([+-]?\d+\.\d+)\s*,\s*([+-]?\d+\.\d+)\s*(.*)$", clean_ln)
            if not m:
                continue
            lat = float(m.group(1))
            lon = float(m.group(2))
            note = m.group(3).strip(" ()")

        pullout_idx += 1
        # Determine Day 4 (Route 500: Wabush -> Goose Bay) vs Day 5 (Route 510: Goose Bay -> L'Anse-au-Clair)
        # In the list, pullouts #1..#249 are on Route 500 (lon <= -60.50), and #250+ are on Route 510 heading south from Goose Bay
        day_num = 4 if pullout_idx <= 249 else 5
        hwy_lbl = "NL-500" if day_num == 4 else "NL-510"
        note_str = f" ({note.title()})" if note else ""
        surf_desc = f" • Surface/Size: {note.title()}" if note else ""
        add_item(
            f"{hwy_lbl} Emergency Pullout / Parking Stop #{pullout_idx}{note_str}",
            lat,
            lon,
            "pullout",
            day_num,
            f"Verified {hwy_lbl} Trans-Labrador Highway emergency roadside pullout and safe motorcycle stopping area{surf_desc}.",
        )

    print(f"Parsed {pullout_idx} TLH emergency pullout stops from MORE Exp 51.md")

    # ==========================================================================
    # 4. 5 LAKE / OCEAN VIEWPOINTS (Lines 717-728)
    # ==========================================================================
    lake_ocean_viewpoints = [
        ("🌄 Route 500 Boreal Lake Viewpoint #1 (Labrador West)", 53.025416, -66.673850, 4, "Scenic lakeside highway overlook along Route 500 east of Wabush / Labrador City."),
        ("🌄 Route 500 Subarctic Lake Viewpoint #2", 53.045142, -66.534351, 4, "Panoramic subarctic lake viewpoint along Trans-Labrador Highway Route 500."),
        ("🌄 Smallwood Reservoir / Ashuanipi Lake Viewpoint (Route 500)", 53.446157, -64.939720, 4, "Expansive water overlook along Route 500 approaching the Smallwood Reservoir watershed."),
        ("🌊 Strait of Belle Isle Ocean Viewpoint (West St. Modeste)", 51.564304, -56.751986, 5, "Coastal ocean lookout on Route 510 overlooking icebergs, whales, and the Strait of Belle Isle."),
        ("🌊 Forteau Bay / Strait of Belle Isle Ocean Viewpoint", 51.464682, -56.958206, 5, "Sweeping ocean viewpoint above Forteau Bay along the Labrador Coastal Drive (Route 510)."),
    ]
    for nm, lat, lon, dnum, desc in lake_ocean_viewpoints:
        add_item(nm, lat, lon, "sight", dnum, desc)

    # ==========================================================================
    # 5. OTHER POIs FROM MORE Exp 51.md (Lines 733-788)
    # ==========================================================================
    other_pois = [
        ("Churchill Falls Trail Parking", 53.600879, -64.315620, "hike", 4, "Trailhead parking for the historic Churchill Falls & Bowdoin Canyon nature trails off Route 500."),
        ("Belvédère de Bowdoin Canyon Nature Trail Viewpoint", 53.593959, -64.307078, "sight", 4, "Spectacular canyon overlook above the Churchill River gorge and Bowdoin Canyon."),
        ("Churchill Falls Tourist Information", 53.547571, -63.993447, "sight", 4, "Official Churchill Falls town visitor centre and hydroelectric heritage information stop."),
        ("Churchill Falls Tourist Viewing Area", 53.544821, -63.993423, "sight", 4, "Scenic overlook and visitor viewing area in Churchill Falls."),
        ("Churchill Falls Airport (ZUM)", 53.561900, -64.106400, "sight", 4, "Regional airfield serving Churchill Falls and the Upper Churchill hydroelectric complex."),
        ("Veterans Memorial Bridge (Churchill River Crossing)", 53.249800, -60.785200, "ferry", 4, "Major steel bridge crossing the Churchill River at the junction of Route 500 and Route 510."),
        ("Labrador Military Museum / Labrador Interpretation Centre", 53.301489, -60.411885, "attraction", 4, "Comprehensive museum chronicling Labrador's Indigenous, aviation, and military history at CFB Goose Bay."),
        ("Minipi Outfitters (Happy Valley-Goose Bay)", 53.330171, -60.412205, "shopping", 4, "Renowned Labrador wilderness outfitter and fly-fishing / adventure headquarters in Goose Bay."),
        ("Valard Camp Parking Lot (Route 510 Staging)", 52.551961, -59.322946, "pullout", 5, "Large graded staging and parking lot at the former Valard Lower Churchill transmission camp on Route 510."),
        (" Salmon River (Big Bumpy) Bridge", 52.415758, -56.091204, "sight", 5, "Landmark bridge crossing the Salmon River ('Big Bumpy') along Route 510 in southern Labrador."),
        ("Big Hill Hiking Trail (Red Bay)", 51.753314, -56.442286, "hike", 5, "Elevated coastal hiking trail overlooking Red Bay harbor and the Strait of Belle Isle."),
        ("Boney Shore Walking Trail (Red Bay)", 51.735093, -56.441093, "hike", 5, "Scenic shoreline walking trail in Red Bay where historic whale bones wash ashore."),
        ("Red Bay National Historic Site Visitor Centre", 51.728500, -56.429500, "attraction", 5, "Parks Canada Visitor Orientation Centre for the 16th-century Basque whaling station."),
        ("Whaler's Restaurant & Cabins (Red Bay)", 51.731200, -56.427800, "food", 5, "Iconic coastal Labrador seafood restaurant and cabins right in Red Bay harbor."),
        ("Red Bay National Historic Site & UNESCO World Heritage Site", 51.726700, -56.431700, "attraction", 5, "UNESCO World Heritage Basque whaling archaeological site and Saddle Island boat dock."),
        ("Saddle Island (Red Bay) Lighthouse", 51.722500, -56.428500, 5, "lighthouse", "Historic island lighthouse guarding the entrance to Red Bay harbor in the Strait of Belle Isle."),
        ("Model of Basque Fishermen Monument (Red Bay)", 51.730200, -56.429000, "sight", 5, "Sculptural monument honoring the 16th-century Basque whalers and fishermen of Red Bay."),
        ("St. Modeste Island Lighthouse", 51.595080, -56.700992, "lighthouse", 5, "Historic coastal navigational light on St. Modeste Island along the Labrador Straits (Route 510)."),
        ("L'Anse Amour National Historic Site (Burial Mound)", 51.474400, -56.871100, "attraction", 5, "Oldest known funerary monument in the Americas (7,500+ years old Maritime Archaic burial mound)."),
        ("Point Amour Provincial Historic Site", 51.460300, -56.857000, "attraction", 5, "Provincial historic site grounds surrounding the 1857 Point Amour Lighthouse and HMS Raleigh wreck trail."),
        ("Gateway to Labrador Visitor Centre (L'Anse-au-Clair)", 51.422200, -57.065800, "sight", 5, "Regional visitor information centre and heritage exhibits housed in a historic church in L'Anse-au-Clair."),
        ("Bradore Falls (Chutes de Brador)", 51.461500, -57.239500, "sight", 5, "Picturesque coastal waterfall near Blanc-Sablon / Brador just west of the Labrador border."),
    ]
    for item in other_pois:
        if len(item) == 6 and isinstance(item[3], int):
            # Handle (nm, lat, lon, dnum, ptype, desc)
            nm, lat, lon, dnum, ptype, desc = item
        else:
            nm, lat, lon, ptype, dnum, desc = item
        add_item(nm.strip(), lat, lon, ptype, dnum, desc)

    # ==========================================================================
    # 6. STORES / OUTPOSTS (Lines 791-804)
    # ==========================================================================
    stores = [
        ("Churchill Falls Hobby Shop (2 Beaver St)", 53.527600, -64.013800, "shopping", 4, "Local hobby, craft, and community retail shop at 2 Beaver St in the Churchill Falls town centre."),
        ("Red Roof Quickstop (Port Hope Simpson)", 52.548520, -56.307561, "shopping", 5, "Convenient roadside general store, snacks, and traveler supplies on Route 510 in Port Hope Simpson."),
        ("Penney's Pitstop (Port Hope Simpson)", 52.545887, -56.307519, "shopping", 5, "Local pitstop, convenience store, and road trip supplies in Port Hope Simpson on Route 510."),
        ("Earle's Groceries Ltd (Forteau)", 51.522125, -56.837093, "shopping", 5, "Established Labrador Straits grocery store and provisioning stop in L'Anse-au-Loup / Forteau corridor."),
        ("Pharmasave Big Land Forteau", 51.477500, -56.955800, "shopping", 5, "Full-service pharmacy, medical supplies, and convenience store on Route 510 in Forteau."),
        ("Forteau Sales & Services Ltd (Hardware & Parts)", 51.476200, -56.957500, "dealer", 5, "Automotive/powersports hardware, lubricants, and emergency mechanical service supplies in Forteau."),
    ]
    for nm, lat, lon, ptype, dnum, desc in stores:
        add_item(nm, lat, lon, ptype, dnum, desc)

    # ==========================================================================
    # 7. FOOD STOPS (Lines 807-812)
    # ==========================================================================
    food_stops = [
        ("Circuit Restobar (Churchill Falls)", 53.532519, -64.011190, "food", 4, "Welcoming local restobar and grill in the Churchill Falls town centre along Route 500.", "$$"),
        ("Skipper Joe's Fish & Chips (445 Hamilton River Rd, Goose Bay)", 53.308800, -60.395500, "food", 4, "Beloved Happy Valley-Goose Bay seafood & fish-and-chips diner at 445 Hamilton River Rd.", "$$"),
    ]
    for nm, lat, lon, ptype, dnum, desc, cost in food_stops:
        add_item(nm, lat, lon, ptype, dnum, desc, cost=cost)

    # ==========================================================================
    # 8. TRAIN CROSSINGS ON ROUTE 500 (Lines 817-825)
    # ==========================================================================
    train_crossings = [
        ("⚠️ Railway Crossing — TLH Route 500 #1 (East of Wabush)", 52.936730, -66.844975, 4, "Active iron-ore railway level crossing on Route 500 just east of Wabush. Slow down and cross rails at 90 degrees."),
        ("⚠️ Railway Crossing — TLH Route 500 #2", 52.951437, -66.778433, 4, "Active railway level crossing on Route 500 in Labrador West. Watch for heavy ore trains and wet steel flangeways."),
        ("⚠️ Railway Crossing — TLH Route 500 #3 (Duley / Walsh River)", 53.022237, -66.672124, 4, "Active railway level crossing on Route 500 near Walsh River."),
        ("⚠️ Railway Crossing — TLH Route 500 #4 (QNS&L Mainline)", 53.065594, -66.203476, 4, "Active QNS&L iron-ore railway level crossing on Trans-Labrador Highway Route 500."),
    ]
    for nm, lat, lon, dnum, desc in train_crossings:
        add_item(nm, lat, lon, "hazard", dnum, desc)

    print(f"Total new POIs to add from MORE Exp 51.md: {len(added_pois)}")

    # ==========================================================================
    # 9. RESOLVE AUTHENTIC PHOTOS FOR NEW POIs
    # ==========================================================================
    # Fetch a pool of 25 authentic Trans-Labrador Highway Route 500 / 510 pullout photos for the 349 pullout pins
    tlh_pullout_queries = [
        "Trans-Labrador Highway Route 500 paved road pullout Labrador",
        "Trans-Labrador Highway Route 510 scenic road Labrador",
        "Route 500 Labrador City to Churchill Falls highway",
        "Route 510 Happy Valley Goose Bay to Red Bay highway",
        "Trans-Labrador Highway boreal forest road Newfoundland Labrador",
        "Labrador Coastal Drive Route 510 highway viewpoint",
    ]
    tlh_photo_pool = []
    for q in tlh_pullout_queries:
        for c in fetch_bing_candidates(q):
            if c["turl"] not in tlh_photo_pool:
                tlh_photo_pool.append(c["turl"])

    # Resolve unique photos for all non-pullout new POIs in parallel
    named_new = [(i, p) for i, p in enumerate(added_pois) if p["type"] != "pullout"]
    print(f"Resolving authentic place photos for {len(named_new)} new named POIs...")

    with ThreadPoolExecutor(max_workers=16) as ex:
        fut_map = {}
        for i, p in named_new:
            clean_nm = re.sub(r"[📸📞📡🌄🌊⚠️]", "", p["name"]).strip()
            q = f"{clean_nm} Labrador Canada" if p["day"] in ("Day 3", "Day 4", "Day 5") else f"{clean_nm} Canada"
            fut_map[ex.submit(fetch_bing_candidates, q)] = i

        for fut in as_completed(fut_map):
            i = fut_map[fut]
            p = added_pois[i]
            try:
                cands = fut.result()
            except Exception:
                cands = []
            chosen = None
            for c in cands:
                if c["oip_id"] not in used_oip_ids:
                    chosen = c
                    used_oip_ids.add(c["oip_id"])
                    break
            if not chosen and cands:
                chosen = cands[0]
            if chosen:
                p["real_photo"] = chosen["turl"]
                p["photo"] = chosen["turl"]

    # Assign varied authentic TLH highway photos across the new pullouts
    if tlh_photo_pool:
        p_counter = 0
        for p in added_pois:
            if p["type"] == "pullout":
                img = tlh_photo_pool[p_counter % len(tlh_photo_pool)]
                p["real_photo"] = img
                p["photo"] = img
                p_counter += 1

    pois.extend(added_pois)
    data["poisData"] = pois

    with open(DATA_PATH, "w", encoding="utf-8") as f_out:
        json.dump(data, f_out, indent=2, ensure_ascii=False)

    print(f"Saved exp51_data.json with {len(pois)} total POIs.")


if __name__ == "__main__":
    main()
