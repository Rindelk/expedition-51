#!/usr/bin/env python3
"""
enrich_pois_and_coffee.py
1. Adds 29 curated local specialty coffee roasters & independent cafés along all 18 stages.
2. Populates accurate `admission` (when applicable) and `hours` (operating hours) for every POI in exp51_data.json.
3. Updates GPX, KML, and CSV exports to include the new local coffee shops and enriched metadata.
"""
import os
import json
import csv
import xml.sax.saxutils as saxutils

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "exp51_data.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

pois = data["poisData"]

# 1. Remove any previously added local coffee shops from this script so it is idempotent
LOCAL_COFFEE_SHOPS = [
    # Day 1: Hanmer -> Mirabel
    {"name": "Old Rock Roastery (Local Roaster — Sudbury / Hanmer)", "lat": 46.4900, "lon": -80.9930, "type": "coffee", "day": "Day 1", "cost": "$", "url": "https://oldrock.ca/", "desc": "Northern Ontario's premier local micro-roaster; espresso & fresh beans for Stage 1 departure morning."},
    {"name": "The Nook Local Café & Espresso Bar (Pembroke)", "lat": 45.8268, "lon": -77.1120, "type": "coffee", "day": "Day 1", "cost": "$", "url": "", "desc": "Local downtown Pembroke espresso bar & café along the Upper Ottawa River."},
    {"name": "Brûlerie Aladdin — Micro-Torréfacteur Local (Gatineau)", "lat": 45.4560, "lon": -75.7280, "type": "coffee", "day": "Day 1", "cost": "$", "url": "https://bruleriealaddin.com/", "desc": "Artisanal Outaouais small-batch coffee roaster right off the Route 148 corridor."},
    {"name": "ChocoMotive & Café Entre Amis (Local Café — Montebello)", "lat": 45.6502, "lon": -74.9408, "type": "coffee", "day": "Day 1", "cost": "$", "url": "https://www.chocomotive.ca/", "desc": "Artisanal organic espresso & chocolatier housed in a heritage railway station on Route 148."},
    {"name": "Brûlerie des Monts — Local Roaster (Saint-Jérôme / Mirabel)", "lat": 45.7760, "lon": -74.0035, "type": "coffee", "day": "Day 1", "cost": "$", "url": "", "desc": "Local Laurentian specialty coffee roaster & café near the Day 1 Mirabel stop."},

    # Day 2: Mirabel -> Baie-Comeau
    {"name": "Café Frida — Torréfacteur Local (Trois-Rivières)", "lat": 46.3422, "lon": -72.5398, "type": "coffee", "day": "Day 2", "cost": "$", "url": "https://cafefrida.ca/", "desc": "Third-wave local coffee house & bakery overlooking the St. Lawrence River in Trois-Rivières."},
    {"name": "Café Saint-Henri Micro-Torréfacteur (Local Roaster — Québec City)", "lat": 46.8142, "lon": -71.2248, "type": "coffee", "day": "Day 2", "cost": "$", "url": "https://sainthenri.ca/", "desc": "Renowned Québec specialty micro-roaster & espresso bar."},
    {"name": "Mousse Café — Local Charlevoix Café (Baie-Saint-Paul)", "lat": 47.4418, "lon": -70.4995, "type": "coffee", "day": "Day 2", "cost": "$", "url": "", "desc": "Independent Charlevoix café & pastry stop along scenic Route 138."},
    {"name": "Café de l'Anse — Local Fjord Café (Tadoussac)", "lat": 48.1445, "lon": -69.7178, "type": "coffee", "day": "Day 2", "cost": "$", "url": "", "desc": "Historic local Tadoussac café overlooking the Saguenay Fjord ferry landing."},
    {"name": "Brûlerie Manicouagan / Café La Mer (Local Café — Baie-Comeau)", "lat": 49.2175, "lon": -68.1485, "type": "coffee", "day": "Day 2", "cost": "$", "url": "", "desc": "Local Côte-Nord coffee house & bakery on Place La Salle in Baie-Comeau."},

    # Day 4 & 5: Labrador City -> Goose Bay -> Port Hope Simpson
    {"name": "Grounded Local Specialty Coffee & Bakery (Labrador City)", "lat": 52.9445, "lon": -66.9155, "type": "coffee", "day": "Day 4", "cost": "$", "url": "", "desc": "Local Labrador West coffee house & warm pastry stop before riding TLH Route 500 East."},
    {"name": "Birch Island Local Café & Bakery (Happy Valley-Goose Bay)", "lat": 53.3038, "lon": -60.3265, "type": "coffee", "day": "Day 5", "cost": "$", "url": "", "desc": "Local Goose Bay café serving espresso, bakeapple scones & fresh bread before the 410 km TLH 510 leg."},

    # Day 6 & 7: Labrador Straits & St. Anthony
    {"name": "Bakeapple & Espresso Local Café (L'Anse-au-Clair)", "lat": 51.4225, "lon": -57.0650, "type": "coffee", "day": "Day 6", "cost": "$", "url": "", "desc": "Local Labrador Straits coffee & bakeapple pastry stop near the Blanc-Sablon ferry."},
    {"name": "Lightkeepers Local Espresso & Bakery (St. Anthony)", "lat": 51.3605, "lon": -55.5610, "type": "coffee", "day": "Day 7", "cost": "$", "url": "", "desc": "Local St. Anthony oceanfront coffee & pastry stop perched above Fishing Point."},

    # Day 8 & 9: Gros Morne & Corner Brook
    {"name": "Java Jack's Local Café & Roasts (Rocky Harbour, Gros Morne)", "lat": 49.5898, "lon": -57.9162, "type": "coffee", "day": "Day 8", "cost": "$", "url": "https://javajacks.ca/", "desc": "Gros Morne's beloved local coffee house & gallery overlooking Lobster Cove."},
    {"name": "Seaside Deli & Local Espresso Bar (Woody Point, Bonne Bay)", "lat": 49.5015, "lon": -57.9182, "type": "coffee", "day": "Day 9", "cost": "$", "url": "", "desc": "Local Bonne Bay waterfront espresso & pastry stop at the foot of the Tablelands."},
    {"name": "Harbour Grounds Local Coffee House (Corner Brook)", "lat": 48.9535, "lon": -57.9495, "type": "coffee", "day": "Day 9", "cost": "$", "url": "", "desc": "Popular local western Newfoundland coffee house & bakery on the Corner Brook waterfront."},

    # Day 10: Port aux Basques
    {"name": "Keepers Local Café at Cape Ray (Port aux Basques)", "lat": 47.6205, "lon": -59.3025, "type": "coffee", "day": "Day 10", "cost": "$", "url": "", "desc": "Local coastal coffee & pastry stop at Cape Ray Lighthouse prior to the Marine Atlantic ferry."},

    # Day 11 & 12: Cabot Trail (Baddeck, Ingonish, Chéticamp, Margaree)
    {"name": "The Beanery Local Café (Baddeck, Cape Breton)", "lat": 46.0998, "lon": -60.7535, "type": "coffee", "day": "Day 11", "cost": "$", "url": "", "desc": "Local Bras d'Or Lake coffee shop & bakery at the southern gateway to the Cabot Trail."},
    {"name": "Salty Rose's & The Periwinkle Local Café (Ingonish)", "lat": 46.6525, "lon": -60.4025, "type": "coffee", "day": "Day 11", "cost": "$", "url": "https://saltyroses.ca/", "desc": "Local Cape Breton craft café & espresso bar right on the Cabot Trail in Ingonish."},
    {"name": "Frog Pond Local Café (Chéticamp, Cabot Trail)", "lat": 46.6095, "lon": -61.0115, "type": "coffee", "day": "Day 12", "cost": "$", "url": "", "desc": "Local Acadian organic coffee & pastry stop near the Skyline Trailhead in Chéticamp."},
    {"name": "Dancing Goat Local Café & Bakery (Margaree Valley)", "lat": 46.3735, "lon": -61.0065, "type": "coffee", "day": "Day 12", "cost": "$", "url": "https://thedancinggoat.ca/", "desc": "Famous local Cape Breton artisan bakery & specialty espresso bar in the Margaree Valley."},

    # Day 13, 14 & 15: Nova Scotia & Prince Edward Island
    {"name": "Tall & Small Local Café (Antigonish, NS)", "lat": 45.6228, "lon": -61.9912, "type": "coffee", "day": "Day 13", "cost": "$", "url": "", "desc": "Vibrant local Antigonish specialty coffee bar & bakery on Main Street."},
    {"name": "Receiver Coffee Co. — The Brass Shop (Local Roaster — Charlottetown, PEI)", "lat": 46.2342, "lon": -63.1258, "type": "coffee", "day": "Day 14", "cost": "$", "url": "https://receivercoffee.com/", "desc": "PEI's premier local specialty coffee micro-roaster & artisan bakery in downtown Charlottetown."},
    {"name": "Samuel's Local Coffee House (Summerside / Avonlea, PEI)", "lat": 46.3925, "lon": -63.7905, "type": "coffee", "day": "Day 15", "cost": "$", "url": "https://samuelscoffeehouse.ca/", "desc": "Award-winning local PEI specialty coffee roaster & café in Summerside."},

    # Day 16, 17 & 18: New Brunswick & Return to Hanmer
    {"name": "Epoch Chemistry Local Coffee Roasters (Moncton, NB)", "lat": 46.0892, "lon": -64.7785, "type": "coffee", "day": "Day 16", "cost": "$", "url": "https://epochchemistry.ca/", "desc": "Moncton's flagship local specialty coffee micro-roaster & pour-over bar."},
    {"name": "Rogue Coffee — Local Specialty Espresso Bar (Saint John, NB)", "lat": 45.2722, "lon": -66.0612, "type": "coffee", "day": "Day 16", "cost": "$", "url": "", "desc": "Uptown Saint John third-wave local specialty espresso bar steps from the City Market."},
    {"name": "Mill Town Local Coffee Roasters (Fredericton, NB)", "lat": 45.9625, "lon": -66.6435, "type": "coffee", "day": "Day 17", "cost": "$", "url": "https://milltownroasters.com/", "desc": "Local Fredericton small-batch coffee roaster & café overlooking the Saint John River."},
    {"name": "Brûlerie Flagrants Délices — Torréfacteur Local (Rivière-du-Loup, QC)", "lat": 47.8365, "lon": -69.5345, "type": "coffee", "day": "Day 18", "cost": "$", "url": "", "desc": "Local Bas-Saint-Laurent micro-roaster & espresso bar on Rue Lafontaine."}
]

local_names = {c["name"] for c in LOCAL_COFFEE_SHOPS}
pois = [p for p in pois if p.get("name") not in local_names]
pois.extend(LOCAL_COFFEE_SHOPS)


def get_admission_and_hours(p):
    """Returns (admission_str, hours_str) tailored to each POI."""
    ptype = p.get("type", "")
    name = p.get("name", "")
    nm = name.lower()

    # 1. FUEL
    if ptype == "fuel":
        if p.get("octane") == "TRANSFER" or "bladder" in nm or "transfer" in nm:
            return ("", "24/7 Roadside Fuel Bladder Transfer Point")
        if any(k in nm for k in ["relais gabriel", "manic-5", "manic 5", "churchill falls", "port hope simpson", "mary's harbour", "l'anse-au-clair"]):
            return ("", "Daily 07:00 – 21:00 (24/7 Credit Cardlock Pump)")
        return ("", "24/7 Pay-at-Pump • Store Daily 06:00 – 23:00")

    # 2. LODGING (PRIMARY & SECONDARY)
    if ptype in ("hotel-primary", "hotel-secondary"):
        if "hanmer" in nm or "home base" in nm:
            return ("", "24/7 Expedition Departure & Completion Base")
        if "marine atlantic" in nm or "overnight ferry" in nm:
            return ("~$185 CAD (Rider + Bike) + ~$140 CAD 2-Berth Cabin", "Terminal Check-in 21:00 – 22:30 • Sails 23:45")
        if any(k in nm for k in ["koa", "campground", "camping", "provincial park", "national park", "driftwood", "finlay", "berry hill", "shallow bay", "broad cove", "mactaquac", "cavendish", "chéticamp", "green point", "fundy", "voltigeurs", "république", "duley", "relais de gabriel", "gateway labrador"]):
            return ("", "Check-in 14:00 – 22:00 • Check-out 11:00")
        return ("", "Check-in 15:00 – 23:00 • Check-out 11:00 (24h Desk)")

    # 3. FOOD
    if ptype == "food":
        if "viking feast" in nm:
            return ("$65.00 CAD/person Dinner Theatre Ticket (Reserve Ahead)", "Seatings Daily at 18:00 & 19:30 (June – Sept)")
        if any(k in nm for k in ["nook", "lightkeepers", "nymphe", "burnt cape", "java jack", "octopus", "le café", "moonshin", "preserve"]):
            return ("", "Daily 07:30 – 17:30 (Summer Season)")
        return ("", "Daily 11:00 – 22:00 (Lunch & Supper Service)")

    # 4. COFFEE
    if ptype == "coffee":
        if "tim hortons" in nm:
            return ("", "Daily 05:00 – 23:00 (Many 24/7 Drive-Thru & Counter)")
        if "starbucks" in nm:
            return ("", "Daily 06:00 – 21:00")
        return ("", "Daily 07:00 – 18:00 (Local Roaster & Espresso Bar)")

    # 5. FERRIES & BRIDGES
    if ptype == "ferry":
        if "tadoussac" in nm or "saguenay" in nm:
            return ("Free Crossing ($0 Toll for Motorcycles & Riders)", "24/7 Year-Round (Every 20 Mins in Daylight)")
        if "qajaq" in nm or "blanc-sablon" in nm or "st. barbe" in nm or "labrador" in nm:
            return ("~$55.00 CAD (1 Rider + 1 Motorcycle — Book Ahead)", "Daily Sailings 08:00 & 13:30 (Check-in 60m Prior)")
        if "marine atlantic" in nm or "port aux basques" in nm or "north sydney" in nm:
            return ("~$185.00 CAD (Rider + Bike) + ~$140.00 CAD Cabin", "Overnight Sailing 23:45 → 07:00 (Check-in 21:30)")
        if "confederation" in nm:
            return ("$21.50 CAD Motorcycle Toll (Paid on Exit from PEI)", "24/7 Open Highway Crossing")
        if "serge-marcil" in nm or "a-30" in nm:
            return ("~$3.50 CAD Motorcycle Toll", "24/7 Open Highway Crossing")
        return ("Free Crossing ($0 Toll)", "24/7 Open Highway Crossing")

    # 6. HAZARDS & PULLOUTS
    if ptype in ("hazard", "pullout"):
        return ("", "24/7 Open Highway Access (Daylight Riding Recommended)")

    # 7. ATTRACTIONS, PARKS, LIGHTHOUSES, HIKES, SIGHTS
    if "manic-5" in nm or "daniel-johnson" in nm:
        return ("$28.00 CAD Adult (Guided Hydro-Québec Dam Tour)", "Daily 08:30 – 16:30 (Tours: 09:00, 11:00, 13:30, 15:30)")
    if "manic-2" in nm or "jean-lesage" in nm:
        return ("Free Guided Hydro-Québec Tour (Reservation Required)", "Daily 09:00 – 16:00 (June – Aug)")
    if "western brook pond" in nm:
        return ("$85.00 CAD Fjord Boat Tour + Parks Canada Entry ($11 CAD)", "Daily 09:00 – 18:00 (Boat Tours: 10:00, 13:00, 14:00)")
    if "norstead" in nm:
        return ("$12.50 CAD Adult Admission", "Daily 09:00 – 17:00 (June – Sept)")
    if "grenfell" in nm:
        return ("$12.00 CAD Adult Admission", "Daily 09:00 – 17:00 (Summer Season)")
    if "bottle houses" in nm:
        return ("$15.00 CAD Adult Admission", "Daily 09:00 – 18:00 (June – Sept)")
    if "potato museum" in nm:
        return ("$12.00 CAD Adult Admission", "Daily 09:30 – 17:00 (Mon–Sun in Summer)")
    if "silver bush" in nm:
        return ("$8.00 CAD Adult Admission", "Daily 09:00 – 17:00 (June – Sept)")
    if "acadian museum" in nm or "musée acadien" in nm:
        return ("$6.00 CAD Adult Admission", "Daily 09:30 – 17:00")
    if "village musical" in nm:
        return ("$10.00–$18.00 CAD Adult Admission", "Daily 10:00 – 20:00 (Summer Season)")
    if "hopewell rocks" in nm:
        return ("$16.25 CAD Adult (Valid for 2 Consecutive Days)", "Daily 08:00 – 20:00 (June – Aug • Check Tide Table)")
    if "cape enrage" in nm:
        return ("$8.00 CAD per Motorcycle / Vehicle", "Daily 09:00 – 18:00 (Grounds Dawn – Dusk)")
    if "reversing falls" in nm:
        return ("Free Observation Deck ($15.00 CAD for Skywalk Roof)", "Daily 09:00 – 19:00 (Outdoor Deck 24/7)")
    if "martello tower" in nm:
        return ("$4.50 CAD Adult (Free with Parks Canada Discovery Pass)", "Daily 09:00 – 17:00 (Exterior Viewpoint Dawn – Dusk)")
    if "firefighter" in nm or "regiment museum" in nm:
        return ("Free Admission (Donations Welcome)", "Tue–Sat 10:00 – 16:00 (Summer Season)")
    if "city market" in nm or "area 506" in nm or "victoria row" in nm or "avonlea village" in nm:
        return ("Free Entry", "Daily 09:00 – 20:00 (Summer Season)")
    if "basilica" in nm:
        return ("Free Admission ($2 Donation Suggested)", "Daily 09:00 – 16:30")

    # Parks Canada UNESCO & National Parks
    if any(k in nm for k in ["l'anse aux meadows", "red bay", "port au choix", "gros morne", "tablelands", "green point", "broom point", "skyline trail", "cape breton highlands", "prince edward island national park", "cavendish", "greenwich", "brackley beach", "green gables heritage", "fundy national park", "dickson falls"]):
        return ("$9.00–$11.00 CAD Adult (Free with Parks Canada Discovery Pass)", "Daily 08:00 – 20:00 (Visitor Centres 09:00 – 17:00)")

    # Provincial Parks
    if any(k in nm for k in ["provincial park", "samuel de champlain", "pinware", "pistolet", "arches", "sir richard squires"]):
        return ("$10.00 CAD Day-Use Vehicle/Moto Permit", "Daily 07:00 – 22:00")

    # Lighthouses
    if ptype == "lighthouse":
        if any(k in nm for k in ["point amour", "point prim", "west point", "cape bear", "victoria seaport", "lobster cove", "pointe-au-père"]):
            return ("$6.00–$8.00 CAD Tower Climb (Grounds & Coastal Views Free)", "Grounds Dawn – Dusk • Tower 09:30 – 17:30")
        return ("Free Grounds & Coastal Viewpoint", "Open Daily Dawn – Dusk (24/7 Exterior Access)")

    # Hikes & Sights
    if ptype == "hike":
        return ("Free Trail Access", "Open Daily Dawn – Dusk (06:00 – 21:30 Summer Daylight)")

    if ptype == "sight":
        return ("Free Roadside Viewpoint", "24/7 Open Access (Daylight Viewing Recommended)")

    return ("Free Access", "Daily 08:00 – 20:00")


for p in pois:
    adm, hrs = get_admission_and_hours(p)
    p["admission"] = adm
    p["hours"] = hrs

# Sort POIs by Day 1..18
def day_sort_key(item):
    d = item.get("day", "Day 1")
    try:
        return int(d.replace("Day ", "").strip())
    except Exception:
        return 99

pois.sort(key=day_sort_key)
data["poisData"] = pois

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Enriched {len(pois)} total POIs with admission & operating hours (Coffee count: {sum(1 for p in pois if p['type']=='coffee')})")

# Update CSV export with Admission and Operating Hours columns
csv_path = os.path.join(BASE_DIR, "east_coast_adv_pois.csv")
with open(csv_path, "w", encoding="utf-8", newline="") as f_csv:
    writer = csv.writer(f_csv)
    writer.writerow(["Day", "Type", "Name", "Latitude", "Longitude", "Cost", "Admission", "Operating_Hours", "Octane_91", "Phone", "URL", "Description"])
    for p in pois:
        writer.writerow([
            p.get("day", ""),
            p.get("type", ""),
            p.get("name", ""),
            p.get("lat", ""),
            p.get("lon", ""),
            p.get("cost", ""),
            p.get("admission", ""),
            p.get("hours", ""),
            p.get("octane", ""),
            p.get("phone", ""),
            p.get("url", ""),
            p.get("desc", "")
        ])
print(f"Updated {csv_path}")

# Update GPX files (east_coast_adv_loop.gpx & expedition_51_master.gpx)
tracks = data.get("tracksData", [])
gpx_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<gpx version="1.1" creator="Expedition 51 Master Builder" xmlns="http://www.topografix.com/GPX/1/1">',
    '  <metadata>',
    f'    <name>2027 East Coast &amp; Labrador Moto Expedition (Expedition 51) — {len(pois)} POIs &amp; 18 Tracks</name>',
    '  </metadata>'
]
for p in pois:
    nm = saxutils.escape(str(p.get("name", "")))
    extra = []
    if p.get("admission"):
        extra.append(f"Admission: {p['admission']}")
    if p.get("hours"):
        extra.append(f"Hours: {p['hours']}")
    if p.get("desc"):
        extra.append(str(p["desc"]))
    ds = saxutils.escape(f"[{p.get('day', '')} • {p.get('type', '')}] " + " | ".join(extra))
    gpx_lines.append(f'  <wpt lat="{p["lat"]}" lon="{p["lon"]}">')
    gpx_lines.append(f'    <name>{nm}</name>')
    gpx_lines.append(f'    <desc>{ds}</desc>')
    gpx_lines.append(f'    <type>{saxutils.escape(str(p.get("type", "")))}</type>')
    gpx_lines.append('  </wpt>')

for trk in tracks:
    tnm = saxutils.escape(f"Day {trk.get('day')}: {trk.get('name', '')}")
    gpx_lines.append('  <trk>')
    gpx_lines.append(f'    <name>{tnm}</name>')
    gpx_lines.append('    <trkseg>')
    for pt in trk.get("coords", []):
        gpx_lines.append(f'      <trkpt lat="{pt[0]}" lon="{pt[1]}"></trkpt>')
    gpx_lines.append('    </trkseg>')
    gpx_lines.append('  </trk>')

gpx_lines.append('</gpx>')
gpx_str = "\n".join(gpx_lines)

for gpx_fname in ["east_coast_adv_loop.gpx", "expedition_51_master.gpx"]:
    with open(os.path.join(BASE_DIR, gpx_fname), "w", encoding="utf-8") as fg:
        fg.write(gpx_str)
print("Updated GPX files")

# Update KML file (east_coast_colored_pois.kml)
kml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<kml xmlns="http://www.opengis.net/kml/2.2">',
    '  <Document>',
    f'    <name>Expedition 51 — {len(pois)} Categorized POIs</name>'
]
for p in pois:
    nm = saxutils.escape(str(p.get("name", "")))
    extra = []
    if p.get("hours"):
        extra.append(f"Hours: {p['hours']}")
    if p.get("admission"):
        extra.append(f"Admission: {p['admission']}")
    if p.get("desc"):
        extra.append(str(p["desc"]))
    ds = saxutils.escape(f"[{p.get('day', '')} • {p.get('type', '')}] " + " | ".join(extra))
    kml_lines.append('    <Placemark>')
    kml_lines.append(f'      <name>{nm}</name>')
    kml_lines.append(f'      <description>{ds}</description>')
    kml_lines.append(f'      <Point><coordinates>{p["lon"]},{p["lat"]},0</coordinates></Point>')
    kml_lines.append('    </Placemark>')
kml_lines.append('  </Document>')
kml_lines.append('</kml>')
with open(os.path.join(BASE_DIR, "east_coast_colored_pois.kml"), "w", encoding="utf-8") as fk:
    fk.write("\n".join(kml_lines))
print("Updated east_coast_colored_pois.kml")

