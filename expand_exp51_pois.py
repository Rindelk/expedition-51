#!/usr/bin/env python3
"""
expand_exp51_pois.py
Integrates all user-curated Camping Backups, QC-389 Emergency Pullouts,
Food & Brewpub Stops, Coffee Stops (Twiggs, Tim Hortons, Starbucks),
42 Verified Sights/Drone/Border POIs, and QC-389 Road/Rail Hazard Markers
into exp51_data.json, and regenerates GPX, KML, and CSV navigation files.
"""
import os
import json
import math
import csv
from xml.sax.saxutils import escape

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "exp51_data.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    exp_data = json.load(f)

existing_pois = exp_data["poisData"]

# Keep base POIs that weren't created by this script (so running idempotently never duplicates)
base_pois = [p for p in existing_pois if not p.get("custom_added")]

def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2)**2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

new_pois = []

def add_poi(name, lat, lon, ptype, day, desc, cost="Free", octane="", url=""):
    # Check if an identical or near-identical POI of same type & similar name already exists in base_pois
    for bp in base_pois:
        if bp.get("type") == ptype and haversine_m(lat, lon, bp["lat"], bp["lon"]) < 120:
            if name.lower()[:10] in bp["name"].lower() or bp["name"].lower()[:10] in name.lower():
                return
    new_pois.append({
        "name": name,
        "lat": round(float(lat), 6),
        "lon": round(float(lon), 6),
        "type": ptype,
        "day": f"Day {day}" if isinstance(day, int) else day,
        "desc": desc,
        "cost": cost,
        "octane": octane,
        "url": url,
        "custom_added": True
    })

# ==============================================================================
# 1. HOTEL, CHALET & B&B LODGING BACKUPS (Day 3 — QC-389 & Labrador City / Wabush)
# ==============================================================================
camping_backups = [
    ("Pourvoirie Relais Gabriel — Inn & Chalets (Hotel Backup)", 51.329536, -68.133731, "hotel-secondary", 3,
     "Indoor hotel rooms, heated wooden chalets, and full dining room at Relais Gabriel (km 318 of Route 389) right after the Manic-5 to Relais Gabriel gravel stretch.", "$145 CAD/night", "", "https://www.pourvoirierelaisgabriel.com/fr"),
    ("Station Uapishka — Monts Groulx (Hotel Backup)", 51.471759, -68.236055, "hotel-secondary", 3,
     "UNESCO Manicouagan-Uapishka Biosphere Reserve eco-lodge, inn, and outfitter backup at the base of the Monts Groulx (km 336 of QC-389).", "$195 CAD/night", "", "https://www.stationuapishka.com/"),
    ("Campement Modulaire (Mont-Wright / QC-389)", 52.774307, -67.324279, "hotel-secondary", 3,
     "Indoor modular hotel room facility near Mont-Wright and the southern approach to Fermont on Route 389.", "$140 CAD/night", "", "https://rcmgroupe.com/"),
    ("Pourvoirie Lac Justone Fermont | Rivière Caniapiscau", 52.811832, -67.219923, "hotel-secondary", 3,
     "Heated outfitter cabins and indoor lodge backup on Lac Justone just west of Fermont on Route 389.", "$150 CAD/night", "", "https://lacjustone.com/"),
    ("Trish’s Place (Wabush / Labrador City B&B Backup)", 52.937108, -66.919275, "hotel-secondary", 3,
     "Welcoming local guesthouse and B&B lodging backup in Wabush / Labrador City.", "$145 CAD/night", "", "https://www.airbnb.ca/rooms/22716280"),
    ("Gateway Labrador — Visitor Information Centre & Museum", 52.950460, -66.919026, "sight", 3,
     "Official Labrador West visitor information centre and regional heritage museum right on Route 500 in Labrador City.", "Free", "", "https://www.destinationlabrador.com/guide/"),
]
for item in camping_backups:
    add_poi(*item)

# ==============================================================================
# 2. EMERGENCY QC-LB HIGHWAY PARKING / ROADSIDE STOPPING AREAS (Day 3)
# ==============================================================================
named_pullouts = [
    ("Stationnement Harfang-Nord (Monts Groulx Trailhead Parking)", 51.608152, -68.230754,
     "Official Monts Groulx Harfang-Nord trailhead parking & emergency highway stopping area on QC-389."),
    ("Stationnement Départ Monts Groulx Nord/Sud", 51.682533, -68.111869,
     "Official Monts Groulx North/South trailhead parking lot & safe roadside pullout on QC-389."),
    ("Large Area for Parking Stop (QC-389 Pullout)", 52.553079, -67.428593,
     "Extra-large graded gravel roadside staging & emergency parking area along Route 389."),
]
for nm, lat, lon, desc in named_pullouts:
    add_poi(nm, lat, lon, "pullout", 3, desc)

raw_parking_coords = [
    (51.376414, -68.187355),
    (51.422301, -68.214818),
    (51.440324, -68.212486),
    (51.468964, -68.211148),
    (51.505175, -68.239348),
    (51.580861, -68.227583),
    (51.618408, -68.232390),
    (51.652669, -68.198432),
    (51.744676, -68.040927),
    (51.801462, -68.108573),
    (51.813975, -68.111343),
    (51.837451, -68.111073),
    (51.885932, -68.163653),
    (51.906198, -68.160475),
    (51.919596, -68.153208),
    (52.058942, -68.089425),
    (52.081798, -68.071490),
    (52.122799, -67.987068),
    (52.185172, -67.911495),
    (52.196199, -67.900831),
    (52.197067, -67.898953),
    (52.200763, -67.873233),
    (52.206596, -67.796580),
    (52.227555, -67.765065),
    (52.248730, -67.725269),
    (52.253362, -67.695979),
    (52.264500, -67.653115),
    (52.267330, -67.648690),
    (52.346907, -67.413391),
    (52.349333, -67.406944), # 52°20'57.6"N 67°24'25.0"W
    (52.381287, -67.367783),
    (52.397037, -67.386167),
    (52.427762, -67.402412),
    (52.430227, -67.403857),
    (52.432893, -67.401928),
    (52.444057, -67.407866),
    (52.456633, -67.416858),
    (52.488594, -67.430605),
    (52.488572, -67.430608), # duplicate within 3m
    (52.505479, -67.432436),
    (52.525976, -67.431687),
    (52.540158, -67.429293),
    (52.571029, -67.429168),
    (52.582357, -67.434086),
    (52.621692, -67.420061),
    (52.648573, -67.430297),
    (52.655882, -67.425581),
    (52.659684, -67.420892),
    (52.681497, -67.394614),
    (52.690018, -67.392578),
    (52.707084, -67.386452),
    (52.679765, -67.396375),
    (52.655887, -67.425560), # duplicate within 2m
    (52.659703, -67.420853), # duplicate within 3m
    (52.720618, -67.398121),
    (52.728100, -67.414505),
    (52.731309, -67.412062),
    (52.750799, -67.422589),
    (52.755194, -67.423381),
    (52.775476, -67.415534),
    (52.788079, -67.404205),
    (52.781424, -67.290759),
    (52.783230, -67.286905),
    (52.788244, -67.263661),
    (52.808286, -67.163052),
    (52.887814, -67.062622),
    (52.916322, -67.024088),
]

dedup_parking = []
for lat, lon in raw_parking_coords:
    if not any(haversine_m(lat, lon, p[0], p[1]) < 15.0 for p in dedup_parking):
        dedup_parking.append((lat, lon))

for idx, (lat, lon) in enumerate(dedup_parking, 1):
    add_poi(
        f"QC-389 Emergency Pullout / Parking Stop #{idx}",
        lat, lon, "pullout", 3,
        f"Verified emergency roadside pullout and rest/bladder-transfer stopping bay #{idx} along Route 389 ({lat:.5f}, {lon:.5f})."
    )

# ==============================================================================
# 3. ROAD & RAILWAY CROSSING HAZARD MARKERS (Day 3 — QC-389 & NL-500)
# ==============================================================================
road_hazards = [
    ("Dirt Road Section Starts (Fire Lake Unpaved QC-389)", 52.344335, -67.378378,
     "⚠️ Paved highway ends and unpaved gravel road section begins near Fire Lake Mine. Reduce speed to 70–80 km/h and stand on pegs over washboard."),
    ("Dirt Road Stops Here — Pavement Begins (Mont-Wright)", 52.771881, -67.322654,
     "✅ Northern end of the Fire Lake–Mont-Wright gravel stretch! Smooth asphalt pavement resumes into Fermont and the Labrador border."),
    ("🛑 Stop Sign — Before Single-Lane Bridge (QC-389)", 52.729326, -67.413572,
     "⚠️ Mandatory stop sign approaching narrow single-lane wilderness bridge on Route 389. Yield to oncoming heavy iron-ore haul trucks."),
    ("⚠️ Double Train Crossing (Cartier Railway QC-389)", 52.584388, -67.431434,
     "⚠️ Double industrial iron-ore railway crossing on Route 389. Cross tracks at a 90° angle and watch for wet steel rails."),
]
for nm, lat, lon, desc in road_hazards:
    add_poi(nm, lat, lon, "hazard", 3, desc)

raw_train_crossings = [
    (52.342896, -67.390412),
    (52.362970, -67.385776),
    (52.388552, -67.374288),
    (52.408457, -67.392103),
    (52.447889, -67.411056), # 52°26'52.4"N 67°24'39.8"W
    (52.595417, -67.429306), # 52°35'43.5"N 67°25'45.5"W
    (52.648917, -67.429250), # 52°38'56.1"N 67°25'45.3"W
    (52.679106, -67.396727),
    (52.690373, -67.392390),
    (52.584406, -67.431405), # near double crossing
    (52.679107, -67.396731), # duplicate
    (52.679099, -67.396763), # duplicate
    (52.690439, -67.392397), # duplicate
    (52.739139, -67.412889), # 52°44'20.9"N 67°24'46.4"W
    (52.913255, -67.025522), # Labrador City crossing
]
dedup_train = []
for lat, lon in raw_train_crossings:
    if haversine_m(lat, lon, 52.584388, -67.431434) < 30.0:
        continue
    if not any(haversine_m(lat, lon, t[0], t[1]) < 25.0 for t in dedup_train):
        dedup_train.append((lat, lon))

for idx, (lat, lon) in enumerate(dedup_train, 1):
    add_poi(
        f"⚠️ Train Crossing #{idx} (QC-389 / Iron Ore Railway)",
        lat, lon, "hazard", 3,
        f"Active Cartier / QNS&L iron-ore railway grade crossing #{idx} across Route 389 ({lat:.5f}, {lon:.5f}). Slow down and cross rails squarely."
    )

# ==============================================================================
# 4. FOOD STOPS & BREWPUBS (61 Curated Stops Across All 18 Stages)
# ==============================================================================
food_stops = [
    # Day 1
    ("The Nook Creperie (Pembroke)", 45.8268, -77.1125, "food", 1,
     "Charming downtown Pembroke creperie serving sweet & savory buckwheat crepes, paninis, and espresso — ideal Day 1 lunch stop along Hwy 17.", "$$"),
    # Day 2
    ("Microbrasserie Le Temps d'une Pinte (Trois-Rivières)", 46.3432, -72.5421, "food", 2,
     "Award-winning Trois-Rivières craft microbrewery and kitchen bistrot serving artisanal Quebec cuisine and house-roasted coffee.", "$$"),
    ("St-Pancrace — Microbrasserie / Le Pub (Baie-Comeau)", 49.2165, -68.1481, "food", 2,
     "55 Pl. la Salle, Baie-Comeau. Celebrated Côte-Nord craft brewpub featuring boreal-inspired ales and hearty pub fare before launching up QC-389.", "$$"),
    ("Pêcherie Manicouagan Inc (Baie-Comeau)", 49.2219, -68.1456, "food", 2,
     "334 Bd la Salle, Baie-Comeau. Fresh St. Lawrence snow crab, Nordic shrimp, smoked salmon, and coastal seafood market.", "$$"),
    # Day 3
    ("Pourvoirie Relais Gabriel Restaurant (Hwy 389)", 51.3292, -68.1341, "food", 3,
     "Iconic wilderness outfitter dining room at km 318 of Route 389 serving hot rider meals, soup, and coffee in the heart of the Côte-Nord.", "$$"),
    ("Iron Rock Brewing Co. (Labrador City)", 52.9463, -66.9152, "food", 3,
     "Labrador's premier craft brewery in Labrador City (118 Humphrey Rd) — great post-QC-389 celebration taproom and food stop.", "$$"),
    ("Baba Q's Smoke & Grill (Labrador City)", 52.9448, -66.9129, "food", 3,
     "Authentic slow-smoked brisket, ribs, pulled pork, and hearty platters in Labrador City.", "$$"),
    # Day 4
    ("Mamattuk Restaurant (Happy Valley-Goose Bay)", 53.3038, -60.3256, "food", 4,
     "2C Tenth St, Happy Valley-Goose Bay. Upscale Labrador dining featuring local wild game, Arctic char, and regional specialties.", "$$$"),
    ("Hotel North Restaurant (Happy Valley-Goose Bay)", 53.3061, -60.3212, "food", 4,
     "Full-service restaurant inside Hotel North on Hamilton River Rd serving steaks, seafood, and hearty Labrador breakfasts.", "$$"),
    # Day 5
    ("Northern Light Inn Dining Room (L'Anse-au-Clair)", 51.4208, -57.0628, "food", 5,
     "Welcoming Strait of Belle Isle dining room right at the Labrador/Newfoundland gateway serving cod tongues, seafood chowder, and roast turkey dinners.", "$$"),
    # Day 6 & Day 7
    ("Rudder's Restaurant & Pub (St. Anthony)", 51.3688, -55.5924, "food", 6,
     "Waterfront harbour pub in St. Anthony overlooking Iceberg Alley, famous for pan-fried cod, moose burgers, and partridgeberry desserts.", "$$"),
    ("Lightkeepers Café (Fishing Point, St. Anthony)", 51.3609, -55.5568, "food", 6,
     "Perched at Fishing Point Park beneath Fox Point Lighthouse — spectacular whale & iceberg viewing deck with fresh seafood chowder and fishcakes.", "$$"),
    ("The Great Viking Feast Dinner Theatre (St. Anthony)", 51.3694, -55.5951, "food", 6,
     "Interactive 11th-century Norse sod-house dinner theatre in St. Anthony featuring Viking comedy, mead, and traditional Newfoundland dishes.", "$$$"),
    ("The Norseman Restaurant (L'Anse aux Meadows)", 51.5928, -55.5312, "food", 7,
     "Harbourside fine dining steps from L'Anse aux Meadows UNESCO Viking site — renowned for bakeapple cheesecake, halibut, and iceberg beer.", "$$$"),
    ("The Daily Catch (St. Lunaire-Griquet)", 51.5098, -55.4662, "food", 7,
     "214 Main St, St. Lunaire-Griquet. Beloved Great Northern Peninsula seafood restaurant serving fresh-off-the-boat Atlantic cod, snow crab, and lobster.", "$$"),
    ("Café Nymphe — The Dark Tickle Company (St. Lunaire-Griquet)", 51.5042, -55.4695, "food", 7,
     "75 Main St, St. Lunaire-Griquet. Economuseum and wild-berry café specializing in bakeapple (cloudberry), partridgeberry, and crowberry treats & espresso.", "$"),
    ("Burnt Cape Café (Raleigh, NL-430)", 51.5561, -55.7364, "food", 7,
     "Home-cooked Newfoundland meals, toutons, cod au gratin, and fresh-baked bread in the coastal fishing village of Raleigh.", "$$"),
    ("Northern Delight Restaurant (Gunners Cove)", 51.5472, -55.5245, "food", 7,
     "Main Street, Gunners Cove. Cozy Viking Trail stop for breakfast, fish & chips, moose soup, and homemade berry pies.", "$$"),
    # Day 8 & Day 9
    ("Java Jack's Restaurant & Gallery (Rocky Harbour)", 49.5914, -57.9168, "food", 8,
     "Acclaimed culinary gem in the heart of Gros Morne National Park (Rocky Harbour) — creative Newfoundland seafood, espresso, and local art.", "$$$"),
    ("Ocean View Bistro & Dining (Rocky Harbour)", 49.5902, -57.9189, "food", 8,
     "Harbourfront dining room overlooking Bonne Bay in Rocky Harbour serving fresh Atlantic lobster, cod, and Newfoundland entertainment.", "$$"),
    ("Deer Lake Irving Big Stop Restaurant (Deer Lake)", 49.1804, -57.4192, "food", 9,
     "62 Trans-Canada Hwy, Deer Lake. Classic rider pit stop with huge country breakfasts, hot turkey sandwiches, and fish & chips right at the Route 430 junction.", "$$"),
    ("Off The Hook Fish & Chips (Deer Lake)", 49.1765, -57.4318, "food", 9,
     "37 Old Bonne Bay Rd, Deer Lake. Crispy golden beer-battered Newfoundland cod & hand-cut fries.", "$$"),
    ("Shipyard Eatery / Boomstick Brewing (Corner Brook)", 48.9518, -57.9482, "food", 9,
     "55 West St, Corner Brook (inside Hew & Draw Hotel). Craft brewery and scratch kitchen serving elevated gastropub fare.", "$$"),
    ("Jennifer's Restaurant (Corner Brook)", 48.9502, -57.9465, "food", 9,
     "48 Broadway, Corner Brook. Long-standing local favourite for prime rib, stuffed cod, and classic Newfoundland hospitality.", "$$$"),
    # Day 10
    ("Alma's Family Restaurant (Channel-Port aux Basques)", 47.5762, -59.1468, "food", 10,
     "27 Grand Bay Rd, Channel-Port aux Basques. Homestyle pre-ferry dinner or breakfast spot minutes from the Marine Atlantic terminal.", "$$"),
    # Day 11 & Day 12
    ("The Chanterelle Country Inn & Restaurant (Cabot Trail)", 46.3085, -60.5318, "food", 11,
     "Scenic farm-to-table dining along the Cabot Trail between Baddeck and Ingonish overlooking St. Ann's Bay.", "$$$"),
    ("Coastal Restaurant & Pub (Ingonish)", 46.6852, -60.3765, "food", 11,
     "36404 Cabot Trail, Ingonish. Famous home of the 'aranac' burger, Digby scallops, and Cape Breton craft beer.", "$$"),
    ("Le Gabriel Restaurant & Lounge (Chéticamp)", 46.6312, -61.0108, "food", 12,
     "15424 Cabot Trail, Chéticamp. Landmark Acadian seafood restaurant featuring snow crab, lobster dinners, Acadian chicken fricot, and live fiddle music.", "$$"),
    ("L'Abri Café, Restaurant et Bar (Chéticamp)", 46.6378, -61.0072, "food", 12,
     "15549 Cabot Trail, Chéticamp. Vibrant coastal bistro overlooking the Gulf of St. Lawrence — lobster rolls, fish tacos, craft cocktails, and espresso.", "$$"),
    ("Harbour Restaurant & Bar (Chéticamp)", 46.6265, -61.0138, "food", 12,
     "15289 Cabot Trail, Chéticamp. Dockside patio right on the Chéticamp boardwalk with fresh lobster, haddock, and harbour views.", "$$"),
    ("Mr. Chicken / Last Chance Sandwich Stop (Chéticamp)", 46.6295, -61.0121, "food", 12,
     "Quick Cabot Trail sandwich, wrap, and picnic lunch stop in Chéticamp before riding the western coastal cliffs.", "$"),
    ("Restaurant Évangéline (Chéticamp)", 46.6242, -61.0152, "food", 12,
     "15212 Cabot Trail, Chéticamp. Traditional Acadian home cooking, meat pies, fish & chips, and homemade coconut cream pie.", "$$"),
    ("Seafood Stop (Chéticamp)", 46.6345, -61.0091, "food", 12,
     "Fresh local Cape Breton lobster, crab, chowder, and takeaway seafood along the Chéticamp harbour strip.", "$$"),
    ("The Doryman Pub & Grill (Chéticamp)", 46.6278, -61.0131, "food", 12,
     "15328 Cabot Trail, Chéticamp. Legendary Cape Breton live-music tavern and grill — world-famous Saturday afternoon & evening ceilidh fiddle sessions.", "$$"),
    # Day 13 & Day 14 (New Glasgow NS & PEI)
    ("The Old Triangle Irish Alehouse (Sydney / Charlottetown)", 46.2348, -63.1262, "food", 13,
     "75 University Ave, Charlottetown (and Charlotte St, Sydney). Authentic Irish pub fare, boxties, Guinness, and live East Coast music.", "$$"),
    ("Point Prim Chowder House (Point Prim, PEI)", 46.0518, -62.9982, "food", 13,
     "2150 Point Prim Rd, Belfast, PEI. Waterfront gem right at Point Prim Lighthouse off the Wood Islands ferry — world-class seafood chowder and lobster rolls.", "$$"),
    ("PEI Preserve Company Restaurant (New Glasgow, PEI)", 46.4108, -63.3492, "food", 14,
     "2841 New Glasgow Rd, New Glasgow, PEI. Riverside country kitchen overlooking the River Clyde — famous raspberry cream cheese pie, potato bacon soup, and artisanal preserves.", "$$"),
    ("New Glasgow Lobster Suppers / Lobster Pub (New Glasgow, PEI)", 46.4095, -63.3504, "food", 14,
     "604 Route 258, New Glasgow, PEI. Iconic Prince Edward Island traditional lobster supper with unlimited PEI steamed mussels and homemade mile-high lemon meringue pie.", "$$$"),
    ("Blue Mussel Café (North Rustico Harbour, PEI)", 46.4582, -63.3018, "food", 14,
     "312 Harbourview Dr, North Rustico, PEI. Spectacular waterside seafood shack renowned for steamed PEI blue mussels, halibut, and seafood bake.", "$$$"),
    ("Chez Yvonne's / Baywatch Restaurant (Cavendish, PEI)", 46.4892, -63.3845, "food", 14,
     "Route 6, Cavendish, PEI. Classic Cavendish family dining serving Maritime seafood platters, chowder, and lobster rolls.", "$$"),
    ("La Rose Bistro (Cavendish / New Glasgow, PEI)", 46.4712, -63.3685, "food", 14,
     "Intimate PEI bistro near Cavendish serving seasonal island produce, fresh catch, and espresso.", "$$"),
    ("Cavendish Fish and Chips (Cavendish, PEI)", 46.4915, -63.3812, "food", 14,
     "Freshly battered Atlantic haddock, PEI Russet hand-cut fries, and fried clams in the heart of Cavendish.", "$$"),
    ("Dave's Lobster (Cavendish Boardwalk / Charlottetown)", 46.4904, -63.3862, "food", 14,
     "Famous PEI lobster roll shack serving warm buttered and chilled mayo lobster rolls on griddled brioche buns.", "$$"),
    ("Razzy's Roadhouse / Beach House (Cavendish, PEI)", 46.4908, -63.3885, "food", 14,
     "8885 Cavendish Rd, Cavendish, PEI. Casual roadhouse grill serving burgers, ribs, lobster rolls, and cold draft beer.", "$$"),
    ("The Lost Anchor (Cavendish, PEI)", 46.4898, -63.3935, "food", 14,
     "9099 Cavendish Rd, Cavendish, PEI. Maritime pub & seafood eatery minutes from Cavendish Campground.", "$$"),
    ("The Ship's Company Pub & Galley (Cavendish, PEI)", 46.4912, -63.3828, "food", 14,
     "Nautical-themed Cavendish pub & galley serving PEI mussels, seafood chowder, and fish & chips.", "$$"),
    ("Sims Corner Steakhouse & Oyster Bar (Charlottetown, PEI)", 46.2339, -63.1275, "food", 14,
     "86 Queen St, Charlottetown, PEI. Premier PEI steakhouse and raw oyster bar featuring aged Maritime beef and freshly shucked Malpeque & Raspberry Point oysters.", "$$$"),
    ("Claddagh Oyster House (Charlottetown, PEI)", 46.2335, -63.1288, "food", 14,
     "131 Sydney St, Charlottetown, PEI. Award-winning seafood & oyster house in historic Old Charlottetown.", "$$$"),
    # Day 15 & Day 16 (Moncton, Fundy / Alma, Saint John & Edmundston NB)
    ("Skipper Jack's Maritime Restaurant (Moncton, NB)", 46.1152, -64.8325, "food", 15,
     "211 Mapleton Rd, Moncton, NB. Lively boat-themed Maritime seafood restaurant famous for lobster rolls, fried clams, and Atlantic haddock.", "$$"),
    ("Pump House Brewpub & Restaurant (Moncton, NB)", 46.0882, -64.7745, "food", 15,
     "5 Orange Ln, Moncton, NB. Iconic Canadian craft brewery (home of Blueberry Ale) with wood-fired pizzas and pub fare.", "$$"),
    ("Octopus' Garden Café & Bakery (Alma / Fundy NP, NB)", 45.6012, -64.9482, "food", 15,
     "8598 Main St, Alma, NB. Beloved coastal café right outside Fundy National Park — famous sticky buns, espresso, paninis, and craft beer garden.", "$$"),
    ("The Baratie — Reversing Falls Restaurant (Saint John, NB)", 45.2592, -66.0868, "food", 16,
     "200 Bridge Rd, Saint John, NB. Rooftop & dining room perched directly above the Reversing Falls rapids at Stonehammer UNESCO Global Geopark.", "$$"),
    ("Lemongrass Thai Fare (Saint John, NB)", 45.2718, -66.0612, "food", 16,
     "42 Princess St, Uptown Saint John, NB. Vibrant Thai restaurant and patio in the historic Trinity Royal district.", "$$"),
    ("Steamers Lobster Co. (Saint John, NB)", 45.2698, -66.0635, "food", 16,
     "110 Water St, Saint John, NB. Harbourside lobster boil house right on the Bay of Fundy waterfront.", "$$"),
    ("Britt's Pub & Eatery (Saint John, NB)", 45.2722, -66.0608, "food", 16,
     "42 Princess St, Saint John, NB. Classic Uptown Saint John gastro-pub with extensive local tap list and comfort food.", "$$"),
    ("Picaroons General Store & Brewtique (Saint John, NB)", 45.2729, -66.0598, "food", 16,
     "32 Canterbury St, Saint John, NB. New Brunswick craft beer taproom and historic general store in Uptown Saint John.", "$$"),
    ("Cask & Kettle Irish Gastropub (Saint John, NB)", 45.2738, -66.0585, "food", 16,
     "112 Prince William St, Saint John, NB. Scratch-made Irish gastropub fare, local craft ciders, and Maritime hospitality.", "$$"),
    ("Splash Thai Cuisine (Saint John, NB)", 45.2745, -66.0572, "food", 16,
     "Uptown Saint John favourite for fresh curries, pad thai, and quick rider lunches.", "$$"),
    ("Le Café / Café Lotus Bleu (Edmundston, NB)", 47.3652, -68.3278, "food", 16,
     "Downtown Edmundston artisanal café & bistro serving Brayon specialties, espresso, and homemade soups.", "$$"),
    ("Frank's Bar & Grill (Edmundston, NB)", 47.3688, -68.3312, "food", 16,
     "135 Rue Victoria, Edmundston, NB. Landmark Edmundston steakhouse, ribs, and roadhouse grill since 1968.", "$$"),
    ("Moonshin'hers Café Bistro (Edmundston, NB)", 47.3642, -68.3265, "food", 16,
     "Cozy Edmundston café bistro for gourmet sandwiches, salads, and specialty coffees.", "$$"),
    ("Le Deck Resto-Bar (Edmundston / Lac Baker, NB)", 47.3598, -68.3295, "food", 16,
     "Lively patio resto-bar in the Edmundston region serving burgers, poutine, and local brews.", "$$"),
]
for item in food_stops:
    add_poi(*item)

# ==============================================================================
# 5. COFFEE STOPS (Twiggs Coffee Roasters, Tim Hortons & Starbucks along Route)
# ==============================================================================
coffee_stops = [
    ("Twiggs Coffee Roasters (North Bay — Hwy 17)", 46.3125, -79.4428, "coffee", 1,
     "473 Fraser St / McKeown Ave, North Bay, ON. Famous Northern Ontario micro-roaster — fresh espresso, baked scones, and rider breakfast stop on Day 1 & Day 18.", "$"),
    ("Tim Hortons (Sturgeon Falls — Hwy 17)", 46.3658, -79.9272, "coffee", 1,
     "Front St / Trans-Canada Hwy 17, Sturgeon Falls, ON. First morning coffee stop east of Hanmer.", "$"),
    ("Tim Hortons (Mattawa — Hwy 17)", 46.3142, -78.7058, "coffee", 1,
     "Main St / Hwy 17, Mattawa, ON. Convenient coffee & restroom stop at the confluence of the Mattawa and Ottawa rivers.", "$"),
    ("Tim Hortons (Pembroke — Hwy 17)", 45.8152, -77.1145, "coffee", 1,
     "Pembroke St W, Pembroke, ON. Quick coffee & snack stop along the Ottawa Valley corridor.", "$"),
    ("Starbucks (Pembroke — Pembroke Mall)", 45.8214, -77.0812, "coffee", 1,
     "1100 Pembroke St E, Pembroke, ON. Espresso & cold brew stop right along the Ottawa River corridor.", "$"),
    ("Tim Hortons (Mirabel — Route 117)", 45.6912, -74.0885, "coffee", 1,
     "13425 Bd Curé-Labelle, Mirabel, QC. Right beside Day 1 lodging for Day 2 07:00 AM rollout coffee.", "$"),
    ("Starbucks (Trois-Rivières — Hwy 40)", 46.3512, -72.5785, "coffee", 2,
     "4520 Bd des Forges, Trois-Rivières, QC. Quick espresso stop off Autoroute 40.", "$"),
    ("Tim Hortons (Beaupré / Sainte-Anne-de-Beaupré — Route 138)", 47.0385, -70.8962, "coffee", 2,
     "10620 Bd Sainte-Anne, Beaupré, QC. Right on Route 138 before climbing into the Charlevoix highlands.", "$"),
    ("Tim Hortons (La Malbaie — Route 138)", 47.6542, -70.1518, "coffee", 2,
     "375 Bd de Comporté, La Malbaie, QC. Coffee & warm-up stop along the St. Lawrence north shore.", "$"),
    ("Tim Hortons (Baie-Comeau — Bd Laflèche)", 49.2015, -68.1842, "coffee", 3,
     "855 Bd Laflèche, Baie-Comeau, QC. Essential final Tim Hortons coffee & breakfast stop before turning north onto Route 389 toward Manic-5!", "$"),
    ("Tim Hortons (Labrador City — Route 500)", 52.9458, -66.9168, "coffee", 4,
     "200 Route 500 (Carol Automart / Mall), Labrador City, NL. Hot coffee & breakfast sandwiches before launching across the Trans-Labrador Highway.", "$"),
    ("Tim Hortons (Happy Valley-Goose Bay)", 53.3072, -60.3285, "coffee", 5,
     "356 Hamilton River Rd, Happy Valley-Goose Bay, NL. Early morning coffee stop before the 608 km ride south to the Strait of Belle Isle.", "$"),
    ("Tim Hortons (St. Anthony)", 51.3712, -55.5968, "coffee", 6,
     "West St, St. Anthony, NL. Northernmost Tim Hortons in Newfoundland — great warm-up stop after visiting L'Anse aux Meadows & Iceberg Alley.", "$"),
    ("Tim Hortons (Deer Lake — Trans-Canada Hwy 1)", 49.1792, -57.4215, "coffee", 9,
     "Trans-Canada Hwy & Route 430 Junction, Deer Lake, NL. Rider hub right at the Viking Trail exit.", "$"),
    ("Starbucks (Corner Brook — Murphy Square)", 48.9435, -57.9312, "coffee", 9,
     "44 Maple Valley Rd, Corner Brook, NL. Espresso and pastry stop in Corner Brook.", "$"),
    ("Tim Hortons (Channel-Port aux Basques)", 47.5785, -59.1482, "coffee", 10,
     "Grand Bay Rd, Channel-Port aux Basques, NL. Right next to the Marine Atlantic Ferry staging terminal.", "$"),
    ("Tim Hortons (North Sydney — Ferry Terminal Approach)", 46.2085, -60.2542, "coffee", 11,
     "119 King St, North Sydney, NS. First coffee stop off the morning ferry arrival from Newfoundland before riding the Cabot Trail.", "$"),
    ("Tim Hortons (Baddeck — Cabot Trail Gateway)", 46.1012, -60.7548, "coffee", 11,
     "9025 Trans-Canada Hwy 105, Baddeck, NS. Gateway coffee stop at the start/finish of the Cabot Trail loop.", "$"),
    ("Tim Hortons (Port Hawkesbury — Canso Causeway)", 45.6185, -61.3512, "coffee", 13,
     "632 Reeves St, Port Hawkesbury, NS. Coffee stop right after crossing the Canso Causeway onto mainland Nova Scotia.", "$"),
    ("Starbucks (New Glasgow, NS — Highland Square)", 45.5742, -62.6468, "coffee", 13,
     "699 Westville Rd, New Glasgow, NS. Espresso stop en route to the Caribou–Wood Islands PEI ferry.", "$"),
    ("Tim Hortons (Cavendish, PEI — Route 6)", 46.4895, -63.3818, "coffee", 14,
     "Cavendish Boardwalk / Route 6, Cavendish, PEI. Morning coffee steps from Cavendish Campground and Green Gables.", "$"),
    ("Starbucks (Charlottetown, PEI — Historic Downtown)", 46.2342, -63.1268, "coffee", 14,
     "154 Queen St, Charlottetown, PEI. Downtown Charlottetown coffee stop near Victoria Row and St. Dunstan's Basilica.", "$"),
    ("Tim Hortons (Borden-Carleton — Confederation Bridge Gateway)", 46.2545, -63.6942, "coffee", 15,
     "24419 Trans-Canada Hwy, Borden-Carleton, PEI. Right at the base of the 12.9 km Confederation Bridge.", "$"),
    ("Starbucks (Moncton, NB — Mapleton Rd)", 46.1145, -64.8312, "coffee", 15,
     "30 Wyse St / Mapleton Rd, Moncton, NB. Coffee stop en route to Hopewell Rocks and Fundy National Park.", "$"),
    ("Starbucks (Saint John, NB — King's Square / Uptown)", 45.2735, -66.0582, "coffee", 16,
     "49 King St, Saint John, NB. Uptown Saint John espresso stop near the City Market and Reversing Falls.", "$"),
    ("Tim Hortons (Grand Falls, NB — Trans-Canada Hwy 2)", 47.0462, -67.7418, "coffee", 16,
     "235 Madawaska Rd, Grand Falls, NB. Coffee stop overlooking the Grand Falls Gorge.", "$"),
    ("Tim Hortons (Edmundston, NB)", 47.3672, -68.3292, "coffee", 17,
     "180 Bd Hébert, Edmundston, NB. Morning coffee before riding along Lake Temiscouata toward Rivière-du-Loup.", "$"),
    ("Starbucks (Rivière-du-Loup, QC)", 47.8385, -69.5368, "coffee", 17,
     "298 Bd Armand-Thériault, Rivière-du-Loup, QC. Espresso stop along the St. Lawrence south shore.", "$"),
]
# Fix Port aux Basques Tim Hortons type to coffee
coffee_stops = [(nm, lat, lon, "coffee", d, desc, c) for (nm, lat, lon, _, d, desc, c) in coffee_stops]
for item in coffee_stops:
    add_poi(*item)

# ==============================================================================
# 6. POINTS OF INTEREST TO VERIFY & ADD (42 Sights, Drone Spots, Trails & Signs)
# ==============================================================================
verified_pois = [
    # QC-389 & Labrador City / Wabush (Day 3)
    ("Belvédère Réservoir Manicouagan (QC-389 Viewpoint)", 50.6525, -68.7385, "sight", 3,
     "Panoramic highway overlook beside the Manicouagan Reservoir ('Eye of Québec' annular impact crater lake) north of Manic-5 Dam.", "Free"),
    ("Gagnon Airport (Former Mining Town Runway — QC-389)", 51.950649, -68.139965, "sight", 3,
     "Abandoned airstrip and hauntingly flat highway corridor of the former iron-mining town of Gagnon (closed and dismantled in 1985) along Route 389.", "Free"),
    ("QC-389 Off-Road Side-of-Road Viewpoint", 52.268160, -67.647522, "sight", 3,
     "Elevated side-of-road gravel pull-off viewpoint overlooking the subarctic Côte-Nord valleys and lakes.", "Free"),
    ("QC-389 Emergency Highway Telephone Booth", 52.320796, -67.582709, "sight", 3,
     "Remote emergency satellite/landline highway telephone booth on Route 389 south of Fire Lake.", "Free"),
    ("🚁 Drone Launch Spot: Fire Lake Iron Mine", 52.344339, -67.377745, "sight", 3,
     "Designated roadside pullout to launch the drone for dramatic aerial footage of the ArcelorMittal Fire Lake open-pit iron mine and QC-389.", "Free"),
    ("🚁 Drone Launch Spot: Mont-Wright Mega-Mine", 52.776427, -67.300992, "sight", 3,
     "Prime roadside vantage point to fly the drone overlooking the colossal Mont-Wright open-pit iron ore mining complex near Fermont.", "Free"),
    ("📸 Fermont Welcome Sign", 52.818357, -67.115868, "sight", 3,
     "Photo-op stop at the town entrance sign for Fermont, QC (home of the famous 1.3 km wind-screening 'Le Mur-Écran' building).", "Free"),
    ("📸 Québec Provincial Border Sign (QC-389 / NL-500)", 52.863850, -67.112159, "sight", 3,
     "Iconic 'Bonjour Québec' border sign at the 53rd parallel dividing Québec (Route 389) and Labrador (Route 500).", "Free"),
    ("📸 Welcome to Labrador Border Sign (South)", 52.864452, -67.111656, "sight", 3,
     "Mandatory rider photo stop at the 'Welcome to Labrador / Bienvenue au Labrador' border monument entering Newfoundland & Labrador!", "Free"),
    ("📸 Labrador Border Sign (North Pullout)", 52.865238, -67.111567, "sight", 3,
     "Northern pullout side of the Québec–Labrador border crossing on Route 500.", "Free"),
    ("Crystal Falls Hiking Trail (Labrador City)", 52.945010, -66.973953, "hike", 3,
     "Scenic short hike overlooking cascading Crystal Falls between the Labrador border and Labrador City.", "Free"),
    ("Harrie Lake Trail (Labrador West)", 52.933453, -66.935664, "hike", 3,
     "Peaceful boreal lakeside walking trail near Labrador City and Wabush.", "Free"),
    ("The Truck — Giant Terex Mining Dump Truck Display", 52.950790, -66.900059, "attraction", 3,
     "Colossal retired open-pit iron ore haul truck on display in Labrador City — classic motorcycle scale photo-op!", "Free"),
    ("Smokey Mountain Ski & Recreational Area", 52.953960, -66.917920, "park", 3,
     "Labrador City's alpine ski hill and scenic high-point overlook just northwest of town.", "Free"),
    ("Jean Lake Walking Trail (Wabush)", 52.898039, -66.881416, "hike", 3,
     "5.5 km groomed boardwalk and gravel walking trail looping around Jean Lake between Wabush and Labrador City.", "Free"),

    # Newfoundland (Days 6–9)
    ("Grenfell Historic Properties (St. Anthony)", 51.3642, -55.5845, "attraction", 6,
     "Museum, historic home, and interpretive centre honoring medical missionary Sir Wilfred Grenfell in St. Anthony.", "$12 CAD"),
    ("Fox Point Lighthouse (Fishing Point, St. Anthony)", 51.3605, -55.5558, "lighthouse", 6,
     "Iconic red-and-white hexagonal lighthouse perched on the dramatic cliffs of Fishing Point at the entrance to St. Anthony Harbour.", "Free"),
    ("Corner Brook Stream Trail", 48.9488, -57.9432, "hike", 9,
     "Lush gorge boardwalk, waterfalls, and salmon stream trail winding right through the heart of Corner Brook.", "Free"),

    # Prince Edward Island (Days 13–14)
    ("St. Dunstan's Basilica (Charlottetown, PEI)", 46.2332, -63.1258, "attraction", 14,
     "Magnificent French Gothic twin-spired stone basilica and National Historic Site in downtown Charlottetown.", "Free"),
    ("Cavendish Cliffs (PEI National Park)", 46.4985, -63.3912, "sight", 14,
     "Striking rust-red sandstone sea cliffs sculpted by the Gulf of St. Lawrence waves along the Cavendish coast.", "Included in Park Pass"),
    ("Victoria Row (Charlottetown, PEI)", 46.2345, -63.1272, "attraction", 14,
     "Pedestrian-only cobblestone Victorian street lined with red-brick cafés, patios, boutiques, and live music next to Confederation Centre.", "Free"),
    ("Brackley Beach (PEI National Park)", 46.4315, -63.2085, "park", 14,
     "Kilometers of sweeping golden sand dunes and warm Gulf shore waters along the PEI Central Coastal Drive.", "Included in Park Pass"),
    ("Anne of Green Gables Museum (Park Corner / Silver Bush)", 46.5192, -63.5512, "attraction", 14,
     "Historic 1872 Campbell homestead at Park Corner overlooking the 'Lake of Shining Waters' where L.M. Montgomery was married.", "$10 CAD"),
    ("Avonlea Village (Cavendish, PEI)", 46.4898, -63.3835, "attraction", 14,
     "Turn-of-the-century heritage village in Cavendish featuring historic schoolhouse, church, and local PEI artisan food stalls.", "Free"),
    ("The Bottle Houses (Cap-Egmont, PEI)", 46.4012, -64.1285, "attraction", 14,
     "Whimsical folk-art village of three shimmering buildings and gardens constructed from over 25,000 recycled glass bottles.", "$12 CAD"),
    ("Prince Edward Island National Park", 46.4625, -63.3145, "park", 14,
     "Coastal national park stretching along PEI's North Shore with red cliffs, shifting parabolic dunes, and scenic Gulf Shore Parkway.", "$9.00 CAD"),
    ("Canadian Potato Museum (O'Leary, PEI)", 46.7058, -64.2285, "attraction", 14,
     "Home of the world's largest potato sculpture, heritage farm machinery hall, and PEI Potato Country Kitchen.", "$12 CAD"),
    ("Thunder Cove Beach & Teacup Rock (Darnley, PEI)", 46.5295, -63.6482, "sight", 14,
     "Spectacular hidden PEI beach featuring towering crimson sandstone caves, sea stacks, and the famous Teacup Rock formation.", "Free"),
    ("West Point Lighthouse (West Point, PEI)", 46.6192, -64.3828, "lighthouse", 14,
     "Tallest lighthouse on Prince Edward Island (1875), striped in bold black-and-white bands overlooking the Northumberland Strait.", "Free"),
    ("Point Prim Lighthouse (Point Prim, PEI)", 46.0504, -62.9992, "lighthouse", 13,
     "Built in 1845 — PEI's oldest lighthouse and one of only two round brick lighthouses in Canada, minutes from the Wood Islands ferry.", "Free"),
    ("Acadian Museum of PEI (Miscouche, PEI)", 46.4312, -63.8615, "attraction", 14,
     "Chronicles over 300 years of Island Acadian history and culture in Miscouche near Summerside.", "$6 CAD"),
    ("Prince Edward Island Regiment Museum (Charlottetown, PEI)", 46.2385, -63.1212, "attraction", 14,
     "Military museum housed at Queen Charlotte Armoury showcasing PEI's regimental history from 1875 to present.", "Free"),
    ("Victoria Seaport Lighthouse (Victoria-by-the-Sea, PEI)", 46.2125, -63.4892, "lighthouse", 15,
     "Charming 1879 square-tapered wooden range light on the wharf in the picturesque artisan village of Victoria-by-the-Sea.", "Free"),
    ("Cape Bear Lighthouse & Marconi Station (Murray Harbour, PEI)", 46.0068, -62.4592, "lighthouse", 13,
     "1881 cliffside lighthouse on southeastern PEI where Canadian wireless operators first received the distress call from the sinking RMS Titanic in 1912.", "$6 CAD"),
    ("Village musical acadien (Abram-Village, PEI)", 46.4518, -64.0725, "attraction", 14,
     "Lively Acadian cultural and musical centre in the Évangéline region featuring fiddle music, step-dancing, bakery, and crêperie.", "$10 CAD"),

    # Saint John, New Brunswick (Day 16)
    ("Saint John Firefighters' Museum (Saint John, NB)", 45.2742, -66.0568, "attraction", 16,
     "Historic No. 2 Engine House museum in Uptown Saint John displaying antique steam pumpers and Great Fire of 1877 artifacts.", "Free"),
    ("Little River Reservoir Park (Saint John, NB)", 45.2892, -65.9985, "park", 16,
     "Tranquil lakeside urban park and walking trail network on the east side of Saint John.", "Free"),
    ("Saints Rest Beach (Saint John, NB)", 45.2395, -66.1248, "sight", 16,
     "Sweeping Bay of Fundy sand and pebble beach adjacent to Irving Nature Park with views of Partridge Island.", "Free"),
    ("Reversing Falls Observation Deck (Saint John, NB)", 45.2595, -66.0865, "sight", 16,
     "Dramatic lookout deck at Fallsview Park watching the monstrous Bay of Fundy tides force the Saint John River to flow backward through a narrow gorge.", "Free"),
    ("Carleton Martello Tower National Historic Site (Saint John, NB)", 45.2528, -66.0762, "attraction", 16,
     "1812 circular stone coastal fortification with WWII fire-control superstructure offering 360-degree views over Saint John Harbour and the Bay of Fundy.", "Free"),
    ("AREA 506 Waterfront Container Village (Saint John, NB)", 45.2682, -66.0628, "attraction", 16,
     "Vibrant colourful shipping-container village on the Saint John waterfront featuring local vendors, murals, food trucks, and waterfront stage.", "Free"),
]
for item in verified_pois:
    add_poi(*item)

# Combine base_pois + new_pois and sort by Day
def day_sort_key(p):
    d = p.get("day", "Day 1").replace("Day ", "").strip()
    try:
        return int(d)
    except ValueError:
        return 99

all_pois = base_pois + new_pois
all_pois.sort(key=day_sort_key)

exp_data["poisData"] = all_pois

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(exp_data, f, indent=2, ensure_ascii=False)

# Print summary by type
counts = {}
for p in all_pois:
    t = p.get("type", "unknown")
    counts[t] = counts.get(t, 0) + 1

print(f"Total POIs in exp51_data.json: {len(all_pois)} (Base: {len(base_pois)}, Newly Added: {len(new_pois)})")
for k, v in sorted(counts.items()):
    print(f"  - {k}: {v}")

# ==============================================================================
# Regenerate CSV, GPX, and KML Navigation Files (all 423 POIs)
# ==============================================================================
for csv_name in ["expedition_51_waypoints.csv", "east_coast_adv_pois.csv"]:
    csv_path = os.path.join(BASE_DIR, csv_name)
    with open(csv_path, "w", newline="", encoding="utf-8") as cf:
        writer = csv.writer(cf)
        writer.writerow(["Day", "Type", "Name", "Latitude", "Longitude", "Cost_Or_Octane", "Description"])
        for p in all_pois:
            co = p.get("octane") if p.get("type") == "fuel" else p.get("cost", "")
            writer.writerow([p.get("day",""), p.get("type",""), p.get("name",""), p.get("lat",""), p.get("lon",""), co, p.get("desc","")])
    print(f"Wrote {csv_path}")

for gpx_name in ["expedition_51_master.gpx", "east_coast_adv_loop.gpx"]:
    gpx_path = os.path.join(BASE_DIR, gpx_name)
    with open(gpx_path, "w", encoding="utf-8") as gf:
        gf.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        gf.write('<gpx version="1.1" creator="Expedition 51 Master Planner" xmlns="http://www.topografix.com/GPX/1/1">\n')
        gf.write('  <metadata><name>2027 East Coast &amp; Labrador Moto Expedition (Expedition 51)</name></metadata>\n')
        for p in all_pois:
            nm = escape(str(p.get("name", "")))
            ds = escape(f"[{p.get('day','')}] ({p.get('type','')}) {p.get('desc','')}")
            tp = escape(str(p.get("type", "")))
            gf.write(f'  <wpt lat="{p["lat"]}" lon="{p["lon"]}"><name>{nm}</name><desc>{ds}</desc><type>{tp}</type></wpt>\n')
        for trk in exp_data["tracksData"]:
            tnm = escape(f"Day {trk['day']}: {trk['name']}")
            gf.write(f'  <trk><name>{tnm}</name><trkseg>\n')
            for pt in trk["coords"]:
                gf.write(f'    <trkpt lat="{pt[0]}" lon="{pt[1]}"></trkpt>\n')
            gf.write('  </trkseg></trk>\n')
        gf.write('</gpx>\n')
    print(f"Wrote {gpx_path}")

kml_path = os.path.join(BASE_DIR, "east_coast_colored_pois.kml")
with open(kml_path, "w", encoding="utf-8") as kf:
    kf.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    kf.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    kf.write('  <Document>\n')
    kf.write('    <name>Expedition 51 — 423 Categorized &amp; Color-Coded POIs</name>\n')
    by_type = {}
    for p in all_pois:
        by_type.setdefault(p.get("type", "sight"), []).append(p)
    for ptype, plist in sorted(by_type.items()):
        kf.write(f'    <Folder><name>{escape(ptype.upper())} ({len(plist)})</name>\n')
        for p in plist:
            nm = escape(str(p.get("name", "")))
            ds = escape(f"[{p.get('day','')}] {p.get('desc','')}")
            kf.write(f'      <Placemark><name>{nm}</name><description>{ds}</description><Point><coordinates>{p["lon"]},{p["lat"]},0</coordinates></Point></Placemark>\n')
        kf.write('    </Folder>\n')
    kf.write('  </Document>\n')
    kf.write('</kml>\n')
print(f"Wrote {kml_path}")

