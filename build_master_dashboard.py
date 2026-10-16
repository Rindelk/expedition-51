#!/usr/bin/env python3
"""
build_master_dashboard.py — Expedition 51 Master Dashboard Generator
Adopts the exact color palette, dual-theme system (:root Daylight & [data-theme="dark"] Campfire),
and layout architecture from Rockies and Mount Robson Expedition, tailored to Expedition 51
(18 Days • 8,243.4 km Pure Canadian Metric • 203 Curated POIs with 100% in-context local photos).
"""
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "exp51_data.json"), "r", encoding="utf-8") as f:
    exp_data = json.load(f)

with open(os.path.join(BASE_DIR, "luggage_checklist.json"), "r", encoding="utf-8") as f_chk:
    checklist_data = json.load(f_chk)

tracks_data = exp_data["tracksData"]
gravel_data = exp_data["gravelData"]
pois_data = exp_data["poisData"]
gantt_days_data = exp_data["ganttDaysData"]
days_meta = exp_data["daysMeta"]


def assign_contextual_photo(p):
    """Assigns a 100% in-context local photo path based strictly on POI type first, then name."""
    ptype = p.get("type", "")
    name = p.get("name", "")
    desc = p.get("desc", "")
    nm = name.lower()
    nl = (name + " " + desc).lower()

    # 1. FUEL STATIONS (strictly gas stations or bladder transfer stops)
    if ptype == "fuel":
        if p.get("octane") == "TRANSFER" or "bladder" in nm or "transfer" in nm:
            return "images/pois/fuel_bladder_transfer.jpg"
        if "shell" in nl:
            return "images/pois/fuel_shell.jpg"
        if "petro" in nl:
            return "images/pois/fuel_petro_canada.jpg"
        if "irving" in nl:
            return "images/pois/fuel_irving.jpg"
        if "esso" in nl or "mobil" in nl:
            return "images/pois/fuel_esso.jpg"
        if "ultramar" in nl or "harnois" in nl or "sonic" in nl:
            return "images/pois/fuel_ultramar.jpg"
        return "images/pois/fuel_outpost.jpg"

    # 2. FERRIES & MAJOR BRIDGES
    if ptype == "ferry":
        if "tadoussac" in nl or "baie-sainte-catherine" in nl or "saguenay" in nl:
            return "images/pois/ferry_tadoussac.jpg"
        if "qajaq" in nl or "blanc-sablon" in nl or "st. barbe" in nl or "sainte-barbe" in nl or "labrador" in nl:
            return "images/pois/ferry_qajaq.jpg"
        if "marine atlantic" in nl or "port aux basques" in nl or "north sydney" in nl:
            return "images/pois/ferry_marine_atlantic.jpg"
        if "canso" in nl:
            return "images/pois/bridge_canso_causeway.jpg"
        if "confederation" in nl:
            return "images/pois/bridge_confederation.jpg"
        if "serge-marcil" in nl or "pont" in nl:
            return "images/pois/bridge_serge_marcil.jpg"
        return "images/pois/ferry_marine_atlantic.jpg"

    # 3. LIGHTHOUSES (strictly authentic Atlantic lighthouses)
    if ptype == "lighthouse":
        if "point amour" in nm or "l'anse-amour" in nm:
            return "images/pois/lh_point_amour.jpg"
        if any(k in nm for k in ["pointe-des-monts", "franquelin", "baie-comeau", "cap-de-la-table", "pointe-au-père", "moulin", "bon-désir"]):
            return "images/pois/lh_pointe_des_monts.jpg"
        if any(k in nm for k in ["cape norman", "fox point", "fishing point", "st. anthony", "flower's cove", "quirpon", "cape bauld"]):
            return "images/pois/lh_cape_norman_st_anthony.jpg"
        if any(k in nm for k in ["pointe riche", "port au choix", "cow head", "keppel"]):
            return "images/pois/lh_pointe_riche.jpg"
        if "lobster cove" in nm or "rocky harbour" in nm:
            return "images/pois/lh_lobster_cove.jpg"
        if "woody point" in nm or "bonne bay" in nm:
            return "images/pois/lh_woody_point.jpg"
        if any(k in nm for k in ["cape ray", "cape anguille", "rose blanche", "channel head", "port aux basques"]):
            return "images/pois/lh_cape_ray.jpg"
        if any(k in nm for k in ["neil's harbour", "white point", "ingonish", "low point", "louisbourg", "st. paul", "dingwall"]):
            return "images/pois/lh_neils_harbour.jpg"
        if any(k in nm for k in ["chéticamp", "cheticamp", "enragée", "margaree", "port hood", "henry island"]):
            return "images/pois/lh_cape_breton.jpg"
        if any(k in nm for k in ["covehead", "north rustico", "cape tryon", "new london", "souris", "east point", "wood islands"]):
            return "images/pois/lh_covehead_pei.jpg"
        if any(k in nm for k in ["point prim", "seacow", "blockhouse", "panmure", "cape bear", "victoria"]):
            return "images/pois/lh_point_prim_seacow.jpg"
        if any(k in nm for k in ["west point", "north cape", "big tignish", "summerside"]):
            return "images/pois/lh_west_point_pei.jpg"
        if any(k in nm for k in ["jourimain", "shediac", "caissie", "buctouche", "tormentine"]):
            return "images/pois/lh_cape_jourimain.jpg"
        if any(k in nm for k in ["cape enrage", "quaco", "st. martins", "anderson hollow", "swallowtail", "head harbour", "reversing falls", "fundy"]):
            return "images/pois/lh_cape_enrage_fundy.jpg"
        return "images/pois/lh_lobster_cove.jpg"

    # 4. HOTELS, MOTELS, CABINS & CAMPGROUNDS (Primary & Secondary)
    if ptype in ("hotel-primary", "hotel-secondary"):
        if "hanmer" in nm or "home base" in nm:
            return "images/pois/home_hanmer.jpg"
        if "marine atlantic" in nm or "overnight ferry" in nm:
            return "images/pois/ferry_marine_atlantic.jpg"
        if "snorri" in nm or "viking" in nm or "norstead" in nm:
            return "images/pois/hotel_viking_cabin.jpg"
        if "keltic lodge" in nm:
            return "images/pois/hotel_keltic_lodge.jpg"
        if any(k in nm for k in ["koa", "campground", "camping", "provincial park", "national park", "driftwood", "finlay", "berry hill", "shallow bay", "broad cove", "mactaquac", "cavendish", "chéticamp", "green point", "fundy", "voltigeurs", "république", "duley", "relais de gabriel", "gateway labrador", "justone", "pourvoirie"]):
            return "images/pois/camp_ocean_national_park.jpg"
        if "best western" in nm or "sheraton" in nm or "dauphin" in nm or "manoir" in nm or "travelodge" in nm or "wabush" in nm or "hotel north" in nm or "port aux basques" in nm:
            return "images/pois/hotel_best_western.jpg"
        if any(k in nm for k in ["motel", "super 8", "motor inn", "laurie", "ptit sapin", "p'tit sapin", "mirabeau", "campement", "modulaire"]):
            return "images/pois/hotel_super8_motel.jpg"
        if any(k in nm for k in ["inn", "cottage", "kindred", "ocean view", "parkland", "haven", "northern light", "uapishka", "trish"]):
            return "images/pois/hotel_coastal_inn.jpg"
        return "images/pois/hotel_best_western.jpg"

    # 5. FOOD & BREWPUB STOPS (62 curated Maritime seafood shacks, microbreweries & restaurants)
    if ptype == "food":
        if any(k in nl for k in ["lobster", "seafood", "fish", "chowder", "oyster", "mussel", "clam", "catch", "pêcherie", "harbour", "ocean", "coastal", "skipper", "steamers", "rudder", "daily catch", "shipyard", "lost anchor", "ship's company", "baywatch", "razzy", "chanterelle", "doryman"]):
            return "images/pois/food_seafood_maritime.jpg"
        return "images/pois/food_brewpub_grill.jpg"

    # 6. COFFEE STOPS (28 curated Tim Hortons, Starbucks & Twiggs Coffee Roasters)
    if ptype == "coffee":
        if "tim hortons" in nm or "tims" in nm:
            return "images/pois/coffee_tim_hortons.jpg"
        return "images/pois/coffee_roaster_starbucks.jpg"

    # 7. QC-389 ROAD & RAILWAY CROSSING HAZARD MARKERS
    if ptype == "hazard":
        if "dirt road" in nm or "pavement" in nm:
            return "images/pois/pullout_qc389_highway.jpg"
        return "images/pois/hazard_train_crossing.jpg"

    # 8. QC-389 EMERGENCY HIGHWAY PULLOUTS & PARKING STOPS
    if ptype == "pullout":
        return "images/pois/pullout_qc389_highway.jpg"

    # 9. ATTRACTIONS, HIKES, SIGHTS & PARKS
    if any(k in nm for k in ["manic-5", "manic 5", "daniel-johnson", "manic-2", "manic 2"]):
        return "images/pois/attr_manic5_dam.jpg"
    if any(k in nm for k in ["fermont", "gagnon", "fire lake", "manicouagan", "389", "mont-wright", "telephone", "quebec", "québec", "labrador", "the truck"]):
        return "images/pois/attr_fermont_wall.jpg"
    if any(k in nm for k in ["churchill falls", "muskrat", "smallwood", "goose bay", "trans-labrador", "crystal falls", "harrie lake", "jean lake", "smokey mountain"]):
        return "images/pois/attr_churchill_falls.jpg"
    if any(k in nm for k in ["red bay", "pinware", "battle harbour", "l'anse amour", "l'anse-au-clair", "tracey hill", "forteau"]):
        return "images/pois/attr_red_bay.jpg"
    if "norstead" in nm:
        return "images/pois/attr_norstead_viking.jpg"
    if any(k in nm for k in ["l'anse aux meadows", "viking", "epaves"]):
        return "images/pois/attr_lanse_aux_meadows.jpg"
    if any(k in nm for k in ["grenfell", "st. anthony", "hms raleigh", "raleigh", "burnt cape", "pistolet"]):
        return "images/pois/attr_st_anthony_grenfell.jpg"
    if any(k in nm for k in ["green gables", "montgomery", "shining waters", "silver bush", "st. dunstan", "victoria row", "avonlea", "bottle houses", "potato", "acadian", "regiment", "musical"]):
        return "images/pois/attr_green_gables.jpg"
    if any(k in nm for k in ["french river", "malpeque", "thunder cove", "darnley"]):
        return "images/pois/sight_french_river_pei.jpg"
    if any(k in nm for k in ["cavendish", "prince edward island", "pei", "greenwich", "brackley"]):
        return "images/pois/park_cavendish_pei.jpg"
    if any(k in nm for k in ["tablelands", "trout river", "woody point", "discovery centre"]):
        return "images/pois/sight_tablelands.jpg"
    if "green point" in nm:
        return "images/pois/hike_green_point_gros_morne.jpg"
    if any(k in nm for k in ["gros morne", "western brook", "broom point", "shallow bay", "arches", "port au choix", "sir richard squires", "berry hill", "corner brook"]):
        return "images/pois/park_gros_morne.jpg"
    if "skyline trail" in nm:
        return "images/pois/hike_skyline_trail.jpg"
    if any(k in nm for k in ["meat cove", "white point", "aspy", "beulach"]):
        return "images/pois/sight_meat_cove.jpg"
    if any(k in nm for k in ["cabot trail", "cape breton", "smokey", "french mountain", "mackenzie", "black brook", "aucoin", "gaelic", "wreckhouse", "ingonish", "chéticamp", "broad cove"]):
        return "images/pois/sight_cabot_trail.jpg"
    if any(k in nm for k in ["hopewell", "enrage", "shediac", "magnetic"]):
        return "images/pois/sight_hopewell_rocks.jpg"
    if any(k in nm for k in ["dickson", "fundy", "alma", "st. martins", "little river", "saints rest"]):
        return "images/pois/park_fundy_dickson_falls.jpg"
    if any(k in nm for k in ["hartland", "covered bridge", "grand falls", "edmundston", "mactaquac", "république"]):
        return "images/pois/attr_hartland_bridge.jpg"
    if any(k in nm for k in ["saint john", "reversing falls", "city market", "martello", "area 506", "firefighters"]):
        return "images/pois/attr_saint_john_market.jpg"
    if any(k in nm for k in ["charlevoix", "saguenay", "port-au-persil", "route 138", "hautes-gorges", "tadoussac", "baie-comeau"]):
        return "images/pois/park_saguenay_charlevoix.jpg"
    if any(k in nm for k in ["portage-du-fort", "route 148", "ottawa", "eau claire", "carillon", "mattawa", "pembroke", "algonquin", "samuel de champlain", "driftwood", "finlay"]):
        return "images/pois/sight_ottawa_river.jpg"
    if any(k in nm for k in ["champlain", "cap diamant", "quebec", "québec", "montmorency", "orléans", "drummondville", "voltigeurs", "mirabel"]):
        return "images/pois/sight_quebec_champlain.jpg"

    return "images/pois/sight_cabot_trail.jpg"


for p in pois_data:
    p["photo"] = assign_contextual_photo(p)

# Persist updated photo paths back to exp51_data.json
with open(os.path.join(BASE_DIR, "exp51_data.json"), "w", encoding="utf-8") as f_out:
    json.dump(exp_data, f_out, indent=2, ensure_ascii=False)

# Build lookup of secondary hotels per day for the 10-element Rockies Day Card layout
sec_hotels_by_day = {}
extra_sec_hotels_by_day = {}
for p in pois_data:
    if p.get("type") == "hotel-secondary":
        d_str = p.get("day", "")
        if d_str.startswith("Day "):
            dnum = int(d_str.replace("Day ", "").strip())
            if dnum not in sec_hotels_by_day:
                sec_hotels_by_day[dnum] = p
            else:
                extra_sec_hotels_by_day.setdefault(dnum, []).append(p)

# Build Gantt Chart HTML using the exact Rockies / generate_gantt_chart.py CSS-variable architecture
DEFAULT_TYPE_STYLES = {
    "ride": {"bg": "#2563eb", "border": "#3b82f6", "icon": "🏍️", "label": "In Saddle", "pill_bg": "rgba(37,99,235,0.2)"},
    "meal": {"bg": "#d97706", "border": "#f59e0b", "icon": "🍽️", "label": "Meal", "pill_bg": "rgba(217,119,6,0.2)"},
    "fuel": {"bg": "#dc2626", "border": "#ef4444", "icon": "⛽", "label": "Fuel & Rest", "pill_bg": "rgba(220,38,38,0.2)"},
    "sight": {"bg": "#7c3aed", "border": "#8b5cf6", "icon": "🏛️", "label": "Attraction / Hike", "pill_bg": "rgba(124,58,237,0.2)"},
    "ferry": {"bg": "#0891b2", "border": "#06b6d4", "icon": "⛴️", "label": "Ferry Crossing", "pill_bg": "rgba(8,145,178,0.2)"},
    "lodging": {"bg": "#059669", "border": "#10b981", "icon": "🏕️", "label": "Lodging / Camp", "pill_bg": "rgba(5,150,105,0.2)"},
    "wake": {"bg": "#475569", "border": "#64748b", "icon": "⏰", "label": "Wake & Prep", "pill_bg": "rgba(71,85,105,0.2)"}
}


def build_gantt_section_html(days_list):
    base_hour = 6
    end_hour = 24
    base_m = base_hour * 60.0
    total_span = (end_hour - base_hour) * 60.0
    hours = [(h * 60, f"{h:02d}:00") for h in range(base_hour, end_hour + 1, 2)]

    out = []
    out.append("""<div class="gantt-section" id="sec-gantt" style="margin-top: 32px; margin-bottom: 24px;">
    <div class="gantt-wrapper" style="background: var(--gantt-bg, #ffffff); border: 1px solid var(--gantt-border, #e2e8f0); border-radius: 12px; padding: 24px; box-shadow: var(--gantt-shadow, 0 4px 15px rgba(0, 0, 0, 0.08)); position: relative;">
        <!-- Header -->
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 14px; border-bottom: 1px solid var(--gantt-border, #e2e8f0); padding-bottom: 12px;">
            <h2 style="margin: 0; font-size: 1.25rem; color: var(--text-main, #0f172a); display: flex; align-items: center; gap: 8px;">
                <span>⏱️</span> Daily Schedule
            </h2>
        </div>

        <!-- View Mode Switcher -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 10px;">
            <div class="gantt-view-toggle" style="display: inline-flex; background: var(--gantt-subtle-bg, #f8fafc); border: 1px solid var(--gantt-border, #e2e8f0); border-radius: 8px; padding: 3px; gap: 4px;">
                <button type="button" id="btn-gantt-view-day" onclick="switchGanttView('day')" style="background: var(--accent-blue, #0284c7); color: #ffffff; border: none; padding: 6px 14px; border-radius: 6px; font-size: 0.82rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 6px; transition: all 0.15s ease;">
                    <span>📱</span> Daily Schedule
                </button>
                <button type="button" id="btn-gantt-view-grid" onclick="switchGanttView('grid')" style="background: transparent; color: var(--text-muted, #64748b); border: none; padding: 6px 14px; border-radius: 6px; font-size: 0.82rem; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 6px; transition: all 0.15s ease;">
                    <span>📊</span> Full 18-Day Grid
                </button>
            </div>
            <div id="gantt-swipe-hint" style="display: none; font-size: 0.75rem; color: var(--accent-blue, #0284c7); background: rgba(2, 132, 199, 0.1); border: 1px solid rgba(2, 132, 199, 0.25); padding: 4px 10px; border-radius: 6px;">
                👈 Swipe horizontally for 06:00 to 24:00 👉
            </div>
        </div>

        <!-- VIEW 1: DEDICATED MOBILE DAILY SCHEDULE (VERTICAL CARDS) -->
        <div id="gantt-day-view" style="display: block;">
            <div style="display: flex; gap: 6px; overflow-x: auto; -webkit-overflow-scrolling: touch; padding-bottom: 10px; margin-bottom: 14px; scrollbar-width: none;">
                <div style="font-size: 0.72rem; font-weight: 800; color: var(--text-muted, #64748b); display: flex; align-items: center; padding-right: 4px; flex-shrink: 0;">STAGE:</div>""")

    for d in days_list:
        day_num = d["day"]
        out.append(f"""                <button type="button" class="gantt-day-chip{' active' if day_num == 1 else ''}" id="gantt-day-chip-{day_num}" onclick="selectGanttDay({day_num})" style="flex-shrink: 0; background: {'var(--accent-blue, #0284c7)' if day_num == 1 else 'var(--gantt-subtle-bg, #f8fafc)'}; border: 1px solid {'var(--accent-blue, #0284c7)' if day_num == 1 else 'var(--gantt-border, #e2e8f0)'}; color: {'#ffffff' if day_num == 1 else 'var(--text-muted, #64748b)'}; padding: 6px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; cursor: pointer; white-space: nowrap; transition: all 0.15s ease;">Day {day_num}</button>""")

    out.append("""            </div>

            <div id="gantt-active-day-content" style="background: var(--gantt-subtle-bg, #f8fafc); border: 1px solid var(--gantt-border, #e2e8f0); border-radius: 10px; padding: 16px;">
                <!-- Populated via JavaScript on load & day selection -->
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px;">
                <button type="button" id="btn-gantt-prev-day" onclick="stepGanttDay(-1)" style="background: var(--gantt-bg, #ffffff); border: 1px solid var(--gantt-border, #e2e8f0); color: var(--text-main, #0f172a); padding: 6px 14px; border-radius: 6px; font-size: 0.80rem; font-weight: 600; cursor: pointer;">◀ Previous Day</button>
                <span id="gantt-day-indicator" style="font-size: 0.80rem; color: var(--text-muted, #64748b); font-weight: 600;">Day 1 of 18</span>
                <button type="button" id="btn-gantt-next-day" onclick="stepGanttDay(1)" style="background: var(--gantt-bg, #ffffff); border: 1px solid var(--gantt-border, #e2e8f0); color: var(--text-main, #0f172a); padding: 6px 14px; border-radius: 6px; font-size: 0.80rem; font-weight: 600; cursor: pointer;">Next Day ▶</button>
            </div>
        </div>

        <!-- VIEW 2: FULL HORIZONTAL GRID WITH FREEZE-PANE STICKY DAY LABELS -->
        <div id="gantt-grid-view" style="display: none;">
            <div style="display: flex; flex-wrap: wrap; gap: 10px; background: var(--gantt-subtle-bg, #f8fafc); border: 1px solid var(--gantt-border, #e2e8f0); padding: 8px 12px; border-radius: 8px; margin-bottom: 14px; font-size: 0.76rem; align-items: center;">
                <span style="color: var(--text-muted, #64748b); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; font-size: 0.70rem; margin-right: 4px;">Legend:</span>
                <div style="display: flex; align-items: center; gap: 5px;">
                    <span style="width: 12px; height: 12px; background: #0284c7; border: 1px solid #0369a1; border-radius: 3px; display: inline-block;"></span>
                    <span style="color: var(--text-main, #0f172a);">Riding</span>
                </div>
                <div style="display: flex; align-items: center; gap: 5px;">
                    <span style="width: 12px; height: 12px; background: #d97706; border: 1px solid #b45309; border-radius: 3px; display: inline-block;"></span>
                    <span style="color: var(--text-main, #0f172a);">Meals</span>
                </div>
                <div style="display: flex; align-items: center; gap: 5px;">
                    <span style="width: 12px; height: 12px; background: #dc2626; border: 1px solid #b91c1c; border-radius: 3px; display: inline-block;"></span>
                    <span style="color: var(--text-main, #0f172a);">Fuel (15-25m)</span>
                </div>
                <div style="display: flex; align-items: center; gap: 5px;">
                    <span style="width: 12px; height: 12px; background: #7c3aed; border: 1px solid #6d28d9; border-radius: 3px; display: inline-block;"></span>
                    <span style="color: var(--text-main, #0f172a);">Attractions</span>
                </div>
                <div style="display: flex; align-items: center; gap: 5px;">
                    <span style="width: 12px; height: 12px; background: #0891b2; border: 1px solid #0e7490; border-radius: 3px; display: inline-block;"></span>
                    <span style="color: var(--text-main, #0f172a);">Ferries</span>
                </div>
                <div style="display: flex; align-items: center; gap: 5px;">
                    <span style="width: 12px; height: 12px; background: #059669; border: 1px solid #047857; border-radius: 3px; display: inline-block;"></span>
                    <span style="color: var(--text-main, #0f172a);">Lodging</span>
                </div>
            </div>

            <div class="gantt-scroll-box" style="overflow-x: auto; -webkit-overflow-scrolling: touch; padding-bottom: 8px;">
                <div style="min-width: 980px; position: relative;">
                    <!-- Time Scale Header -->
                    <div style="display: flex; align-items: center; margin-bottom: 8px; font-family: monospace; font-size: 0.75rem; color: var(--text-muted, #64748b);">
                        <div style="width: 140px; flex-shrink: 0; font-weight: 700; color: var(--text-main, #0f172a); text-transform: uppercase; letter-spacing: 0.5px; position: sticky; left: 0; background: var(--gantt-stage-bg, var(--gantt-bg, #ffffff)); z-index: 15; padding: 2px 8px 2px 0;">Day &amp; Date</div>
                        <div style="flex: 1; position: relative; height: 24px; border-bottom: 1px solid var(--gantt-time-border, #cbd5e1);">""")

    for m, label in hours:
        pct = ((m - base_m) / total_span) * 100.0
        align = "transform: translateX(-50%);"
        if m == base_m:
            align = "transform: translateX(0);"
        elif m == (end_hour * 60):
            align = "transform: translateX(-100%);"
        out.append(f"""                            <span style="position: absolute; left: {pct:.2f}%; {align} top: 2px;">{label}</span>""")

    out.append("""                        </div>
                    </div>

                    <!-- Daily Rows -->""")

    for d in days_list:
        day = d["day"]
        dist_km = float(d["dist"])
        date_short = d["date"].split(",")[1].strip() if "," in d["date"] else d["date"]
        blocks = d["blocks"]

        out.append(f"""
                    <!-- Day {day} Row -->
                    <div style="display: flex; align-items: center; margin-bottom: 7px; height: 38px; cursor: pointer; transition: background 0.15s ease;"
                         onmouseover="this.style.background='rgba(2, 132, 199, 0.08)'" onmouseout="this.style.background='transparent'"
                         onclick="if(typeof focusDay==='function') focusDay({day}); const el=document.getElementById('day-card-{day}'); if(el) el.scrollIntoView({{behavior: 'smooth', block: 'center'}});">
                        
                        <!-- Sticky Freeze-Pane Day Label -->
                        <div class="gantt-col-stage" style="width: 140px; flex-shrink: 0; display: flex; flex-direction: column; justify-content: center; padding-right: 10px; position: sticky; left: 0; background: var(--gantt-stage-bg, var(--gantt-bg, #ffffff)); z-index: 10; box-shadow: 2px 0 6px rgba(0,0,0,0.08);">
                            <div style="display: flex; align-items: center; justify-content: space-between;">
                                <span style="font-weight: 700; font-size: 0.82rem; color: var(--text-main, #0f172a);">Day {day}</span>
                                <span style="font-size: 0.72rem; color: var(--accent-blue, #0284c7); font-family: monospace;">{dist_km:.1f} km</span>
                            </div>
                            <div style="font-size: 0.68rem; color: var(--text-muted, #64748b); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                                {date_short}
                            </div>
                        </div>

                        <!-- Day Track with Vertical Hour Lines -->
                        <div style="flex: 1; position: relative; height: 32px; background: var(--gantt-subtle-bg, #f8fafc); border-radius: 6px; border: 1px solid var(--gantt-border, #e2e8f0); overflow: hidden;">""")

        for m, _ in hours[1:-1]:
            pct = ((m - base_m) / total_span) * 100.0
            out.append(f"""                            <div style="position: absolute; left: {pct:.2f}%; top: 0; bottom: 0; width: 1px; background: var(--gantt-border, rgba(100, 116, 139, 0.2)); pointer-events: none; z-index: 1;"></div>""")

        for b in blocks:
            b_start = max(b["start_m"], int(base_m))
            b_end = min(b["end_m"], int(end_hour * 60))
            if b_end <= b_start:
                continue

            left_pct = ((b_start - base_m) / total_span) * 100.0
            width_pct = ((b_end - b_start) / total_span) * 100.0
            style = DEFAULT_TYPE_STYLES.get(b["type"], DEFAULT_TYPE_STYLES["ride"])
            dur_min = b["end_m"] - b["start_m"]
            dur_str = f"{dur_min // 60}h {dur_min % 60}m" if dur_min >= 60 else f"{dur_min}m"

            block_content = ""
            if width_pct >= 6.5:
                block_content = f"""<span style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding: 0 4px; pointer-events: none;">{style['icon']} {b['title']}</span>"""
            elif width_pct >= 3.0:
                block_content = f"""<span style="pointer-events: none;">{style['icon']}</span>"""

            tooltip_text = f"{b['start_str']} – {b['end_str']} ({dur_str})&#10;{b['title']}&#10;{b['details']}"
            safe_details = b["details"].replace("'", "\\'").replace('"', "&quot;")
            safe_title = b["title"].replace("'", "\\'").replace('"', "&quot;")

            out.append(f"""                            <div style="position: absolute; left: {left_pct:.2f}%; width: {width_pct:.2f}%; top: 2px; bottom: 2px; background: {style['bg']}; border: 1px solid {style['border']}; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: #ffffff; font-size: 0.70rem; font-weight: 600; cursor: pointer; z-index: 2; transition: transform 0.1s ease, filter 0.1s ease;"
                                 title="{tooltip_text}"
                                 onclick="event.stopPropagation(); inspectGanttBlock('{b['start_str']} – {b['end_str']} ({dur_str})', '{safe_title}', '{safe_details}', '{style['icon']}');"
                                 onmouseover="this.style.zIndex='10'; this.style.filter='brightness(1.15)';"
                                 onmouseout="this.style.zIndex='2'; this.style.filter='none';">
                                {block_content}
                            </div>""")

        out.append("""                        </div>
                    </div>""")

    out.append("""                </div>
            </div>

            <!-- Tap-to-Inspect Block Card -->
            <div id="gantt-block-inspect-card" style="display: none; margin-top: 12px; background: var(--gantt-subtle-bg, #f8fafc); border: 1px solid var(--accent-blue, #0284c7); border-radius: 8px; padding: 12px; position: relative;">
                <button type="button" onclick="document.getElementById('gantt-block-inspect-card').style.display='none';" style="position: absolute; top: 8px; right: 8px; background: transparent; border: none; color: var(--text-muted, #64748b); font-size: 14px; cursor: pointer;">✕</button>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                    <span id="inspect-icon" style="font-size: 1.2rem;">⏱️</span>
                    <span id="inspect-time" style="font-family: monospace; font-size: 0.82rem; font-weight: 700; color: var(--accent-blue, #0284c7);"></span>
                </div>
                <div id="inspect-title" style="font-size: 0.88rem; font-weight: 700; color: var(--text-main, #0f172a); margin-bottom: 4px;"></div>
                <div id="inspect-details" style="font-size: 0.80rem; color: var(--text-card, #334155); line-height: 1.4;"></div>
            </div>
        </div>

        <!-- Footnote Callout -->
        <div style="margin-top: 16px; padding: 12px 16px; background: var(--gantt-subtle-bg, #f8fafc); border-left: 4px solid var(--accent-blue, #0284c7); border-radius: 4px; font-size: 0.80rem; color: var(--text-muted, #64748b); line-height: 1.45;">
            <strong style="color: var(--text-main, #0f172a);">💡 Interactive Tip:</strong> Tap any day pill above or use <strong>Prev/Next</strong> to view that stage's complete minute-by-minute schedule, gas stops, and saddle intervals. Switch to <strong>Full 18-Day Grid</strong> to pan the visual cross-trip comparison with freeze-pane sticky day labels.
        </div>
    </div>
</div>""")
    return "\n".join(out)


gantt_html = build_gantt_section_html(gantt_days_data)

# Build the 18 Day Cards using the exact Rockies 10-element Day Card layout
day_cards_html = []
for idx, dm in enumerate(days_meta):
    day_num = dm["day"]
    color = dm.get("badge_bg", "#0284c7")
    title = dm["title"]
    date_str = dm["date"]
    dist_chip = dm["dist_chip"]
    time_chip = dm["time_chip"]
    surf_chip = dm["surf_chip"]
    hist_weather = dm["hist_weather"]
    desc = dm["desc"]
    hotel_title = dm["hotel_title"]
    hotel_loc = dm["hotel_loc"]
    hotel_rate = dm["hotel_rate"]
    book_url = dm.get("book_url", "")
    call_tel = dm.get("call_tel", "")
    res_window = dm.get("res_window", "Book Early")
    fuel_desc = dm.get("fuel_desc", "")
    highlights = dm.get("highlights", [])
    gmaps_url = dm.get("gmaps_url", "#")

    # Primary Hotel Action Buttons
    pri_btns = []
    if book_url:
        pri_btns.append(f'<a href="{book_url}" target="_blank" onclick="event.stopPropagation();" class="hotel-action-btn" style="background: rgba(5, 150, 105, 0.12); color: var(--accent-green); border: 1px solid rgba(5, 150, 105, 0.35);">🌐 Website / Book</a>')
    if call_tel:
        clean_phone = call_tel.replace("tel:", "")
        pri_btns.append(f'<a href="{call_tel}" onclick="event.stopPropagation();" class="hotel-action-btn" style="background: var(--bg-subtle); color: var(--text-main); border: 1px solid var(--border);">📞 {clean_phone}</a>')
    if res_window:
        pri_btns.append(f'<span class="hotel-action-btn" style="background: rgba(2, 132, 199, 0.1); color: var(--accent-blue); border: 1px solid rgba(2, 132, 199, 0.28); cursor: default;">📅 {res_window}</span>')
    pri_btns_html = "\n                        ".join(pri_btns)

    # Secondary / Fallback Hotel Row (Rockies 10-element Day Card parity)
    sec_p = sec_hotels_by_day.get(day_num)
    extra_secs = extra_sec_hotels_by_day.get(day_num, [])
    extra_sec_html = ""
    if extra_secs:
        extra_items = []
        for ep in extra_secs:
            ep_name = ep.get("name", "")
            ep_cost = ep.get("cost", "")
            ep_lat = ep.get("lat", 0)
            ep_lon = ep.get("lon", 0)
            extra_items.append(
                f'<span onclick="event.stopPropagation(); map.setView([{ep_lat}, {ep_lon}], 13);" '
                f'style="display:inline-flex; align-items:center; gap:4px; background:var(--bg-card); border:1px solid var(--border); '
                f'border-radius:5px; padding:3px 7px; font-size:0.70rem; font-weight:700; color:var(--text-main); cursor:pointer;" '
                f'title="Click to center map on {ep_name}">⛺ {ep_name} <span style="color:var(--accent-orange);">({ep_cost})</span></span>'
            )
        extra_hdr = (
            f"🏕️ Additional Route 389 &amp; Labrador West Camping / Lodging Backups ({len(extra_secs)}):"
            if day_num == 3
            else f"🏕️ Additional Stage Lodging / Camping Backups ({len(extra_secs)}):"
        )
        extra_sec_html = f"""
                    <div style="margin-top:8px; padding-top:7px; border-top:1px dashed var(--border);">
                        <div style="font-size:0.69rem; font-weight:800; text-transform:uppercase; color:var(--text-muted); margin-bottom:5px;">{extra_hdr}</div>
                        <div style="display:flex; flex-wrap:wrap; gap:5px;">
                            {"".join(extra_items)}
                        </div>
                    </div>"""
    if sec_p:
        sec_name = sec_p.get("name", "Fallback Hotel")
        sec_desc = sec_p.get("desc", "")
        sec_cost = sec_p.get("cost", "")
        sec_url = sec_p.get("url", "")
        sec_phone = sec_p.get("phone", "")
        sec_btns = []
        if sec_url:
            sec_btns.append(f'<a href="{sec_url}" target="_blank" onclick="event.stopPropagation();" class="hotel-action-btn" style="background: rgba(217, 119, 6, 0.12); color: var(--accent-orange); border: 1px solid rgba(217, 119, 6, 0.35);">🌐 Website</a>')
        if sec_phone:
            tel_href = "tel:" + sec_phone.replace(" ", "")
            sec_btns.append(f'<a href="{tel_href}" onclick="event.stopPropagation();" class="hotel-action-btn" style="background: var(--bg-subtle); color: var(--text-main); border: 1px solid var(--border);">📞 {sec_phone}</a>')
        sec_btns_html = "\n                        ".join(sec_btns)
        sec_hotel_box_html = f"""
                <div class="hotel-box" style="border-left: 3px solid var(--accent-orange); margin-top: 8px;">
                    <div class="hotel-header-row">
                        <div class="hotel-title" style="color: var(--accent-orange);">🏨 Secondary / Fallback: {sec_name}</div>
                        <span class="hotel-rate-pill" style="background: rgba(217, 119, 6, 0.12); color: var(--accent-orange); border-color: rgba(217, 119, 6, 0.3);">{sec_cost}</span>
                    </div>
                    <div class="hotel-sub">{sec_desc}</div>
                    <div class="hotel-actions">
                        {sec_btns_html}
                    </div>{extra_sec_html}
                </div>"""
    else:
        sec_hotel_box_html = """
                <div class="hotel-box" style="border-left: 3px solid var(--accent-green); margin-top: 8px;">
                    <div class="hotel-header-row">
                        <div class="hotel-title" style="color: var(--accent-green);">🏠 Expedition Completion — Return to Hanmer Home Base</div>
                        <span class="hotel-rate-pill">$0 CAD</span>
                    </div>
                    <div class="hotel-sub">4671 Dupuis Drive, Hanmer, ON — End of 8,243.4 km East Coast &amp; Labrador Expedition Loop!</div>
                </div>"""

    hl_items = "\n                        ".join([f"<li>{h}</li>" for h in highlights])

    card_html = f"""
            <div class="day-card collapsed" id="day-card-{day_num}" onclick="focusDay({day_num})">
                <div class="day-header" onclick="handleDayHeaderClick(event, {day_num})">
                    <div class="day-title-row">
                        <span class="day-badge" style="background: {color};">Day {day_num}</span>
                        <h3 class="day-title">{title}</h3>
                    </div>
                    <div style="display:flex; align-items:center; gap:6px; flex-shrink:0;">
                        <span class="day-date">{date_str}</span>
                        <button type="button" class="day-collapse-btn" id="day-chevron-{day_num}" onclick="event.stopPropagation(); toggleDayCard({day_num});" title="Collapse / Expand Day {day_num}">▸</button>
                    </div>
                </div>

                <div class="stats-row">
                    <span class="stat-chip">{dist_chip}</span>
                    <span class="stat-chip">{time_chip}</span>
                    <span class="stat-chip">{surf_chip}</span>
                </div>

                <div class="day-collapsible-body" id="day-body-{day_num}">
                    <div class="weather-bar" id="weather-day-{day_num}">
                        <span>🌤️ {hist_weather}</span>
                        <span class="live-weather-badge" id="live-weather-{day_num}">⏳ Fetching live forecast...</span>
                    </div>

                    <p class="day-desc">{desc}</p>

                    <div class="hotel-box" style="border-left: 3px solid var(--accent-green);">
                        <div class="hotel-header-row">
                            <div class="hotel-title">{hotel_title}</div>
                            <span class="hotel-rate-pill">{hotel_rate}</span>
                        </div>
                        <div class="hotel-sub">{hotel_loc}</div>
                        <div class="hotel-actions">
                            {pri_btns_html}
                        </div>
                    </div>
                    {sec_hotel_box_html}

                    <div class="fuel-box">
                        <strong>⛽ Fuel &amp; 91 Octane Strategy:</strong> {fuel_desc}
                    </div>

                    <div class="highlights-box">
                        <div class="highlights-title">✨ Stage Highlights &amp; Stops</div>
                        <ul class="highlights-list">
                            {hl_items}
                        </ul>
                    </div>

                    <div style="display:flex; gap:8px; flex-wrap:wrap; margin-top:12px;">
                        <button type="button" onclick="event.stopPropagation(); focusDay({day_num});" class="gmaps-btn" style="flex:1; background: rgba(2, 132, 199, 0.12); color: var(--accent-blue); border: 1px solid rgba(2, 132, 199, 0.35); cursor:pointer;">
                            🗺️ Focus Stage {day_num} on Map
                        </button>
                        <a href="{gmaps_url}" target="_blank" onclick="event.stopPropagation();" class="gmaps-btn" style="flex:1;">
                            🧭 Google Maps Turn-by-Turn ↗
                        </a>
                    </div>
                </div>
            </div>"""
    day_cards_html.append(card_html)

all_day_cards_str = "\n".join(day_cards_html)

# Mobile day jump pills (1 to 18)
day_jump_pills = "\n            ".join([
    f'<button type="button" class="day-jump-pill" id="jump-pill-{d["day"]}" onclick="jumpToDayCard({d["day"]})">D{d["day"]}</button>'
    for d in days_meta
])

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <title>Expedition 51</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        /* ROCKIES & MOUNT ROBSON DUAL-THEME COLOR SYSTEM (DAYLIGHT DEFAULT + CAMPFIRE DARK) */
        :root {{
            --bg-dark: #f1f5f9;
            --bg-panel: #ffffff;
            --bg-card: #ffffff;
            --bg-card-hover: #f8fafc;
            --bg-subtle: #f8fafc;
            --bg-stat: #f1f5f9;
            --text-main: #0f172a;
            --text-muted: #475569;
            --text-card: #334155;
            --accent-blue: #0284c7;
            --accent-green: #059669;
            --accent-orange: #d97706;
            --accent-red: #dc2626;
            --accent-purple: #7c3aed;
            --border: #cbd5e1;
            --header-bg: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
            --shadow-card: 0 2px 8px rgba(15, 23, 42, 0.06);
            --gantt-bg: #ffffff;
            --gantt-subtle-bg: #f8fafc;
            --gantt-border: #e2e8f0;
            --gantt-stage-bg: #ffffff;
            --gantt-time-border: #cbd5e1;
            --gantt-shadow: 0 4px 15px rgba(15, 23, 42, 0.06);
        }}

        [data-theme="dark"] {{
            --bg-dark: #0f172a;
            --bg-panel: #1e293b;
            --bg-card: #26334d;
            --bg-card-hover: #2d3d5c;
            --bg-subtle: rgba(15, 23, 42, 0.55);
            --bg-stat: rgba(15, 23, 42, 0.7);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --text-card: #cbd5e1;
            --accent-blue: #38bdf8;
            --accent-green: #10b981;
            --accent-orange: #f59e0b;
            --accent-red: #ef4444;
            --accent-purple: #a855f7;
            --border: #334155;
            --header-bg: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
            --shadow-card: 0 4px 14px rgba(0, 0, 0, 0.35);
            --gantt-bg: #1e293b;
            --gantt-subtle-bg: #0f172a;
            --gantt-border: #334155;
            --gantt-stage-bg: #1e293b;
            --gantt-time-border: #475569;
            --gantt-shadow: 0 10px 25px rgba(0, 0, 0, 0.35);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            overflow-x: hidden;
            transition: background-color 0.2s ease, color 0.2s ease;
        }}

        /* Top Header (Streamlined Rockies Layout) */
        header {{
            background: var(--header-bg);
            border-bottom: 1px solid var(--border);
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 1000;
            box-shadow: var(--shadow-card);
            gap: 12px;
            flex-wrap: wrap;
        }}

        .header-title h1 {{
            font-size: 1.18rem;
            font-weight: 800;
            letter-spacing: -0.3px;
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--text-main);
        }}

        .header-title p {{
            font-size: 0.76rem;
            color: var(--text-muted);
            margin-top: 2px;
        }}

        .header-badges {{
            display: flex;
            gap: 8px;
            align-items: center;
            flex-wrap: wrap;
        }}

        .stats-strip {{
            display: flex;
            align-items: center;
            gap: 14px;
            padding-right: 12px;
            border-right: 1px solid var(--border);
            margin-right: 2px;
        }}
        .stat-item {{
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            line-height: 1.15;
        }}
        .stat-item .val {{
            font-size: 0.84rem;
            font-weight: 800;
            color: var(--text-main);
        }}
        .stat-item .lbl {{
            font-size: 0.63rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            color: var(--text-muted);
        }}

        .badge {{
            background: var(--bg-subtle);
            border: 1px solid var(--border);
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 0.74rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
            color: var(--text-main);
        }}

        .badge-green {{ border-color: var(--accent-green); color: var(--accent-green); }}
        .badge-orange {{ border-color: var(--accent-orange); color: var(--accent-orange); }}
        .badge-blue {{ border-color: var(--accent-blue); color: var(--accent-blue); }}
        .badge-red {{ border-color: var(--accent-red); color: var(--accent-red); }}

        .theme-toggle-btn {{
            background: var(--bg-card);
            border: 1px solid var(--accent-blue);
            color: var(--accent-blue);
            padding: 6px 11px;
            border-radius: 6px;
            font-size: 0.76rem;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 5px;
            transition: all 0.15s ease;
        }}
        .theme-toggle-btn:hover {{
            background: var(--accent-blue);
            color: #ffffff;
        }}

        /* Main Split Layout (Desktop Default) */
        .main-container {{
            display: flex;
            height: 83vh;
            min-height: 640px;
            border-bottom: 2px solid var(--border);
            overflow: hidden;
            position: relative;
        }}

        /* Map Side */
        .map-wrapper {{
            flex: 1 1 auto;
            min-width: 140px;
            position: relative;
            height: 100%;
        }}

        #map {{
            width: 100%;
            height: 100%;
            background: #cbd5e1;
        }}

        /* Resizable Split Divider Gutter (Map <-> Itinerary) */
        #resizer-gutter {{
            width: 10px;
            background: var(--bg-subtle);
            border-left: 1px solid var(--border);
            border-right: 1px solid var(--border);
            cursor: col-resize;
            position: relative;
            z-index: 950;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.15s ease, border-color 0.15s ease;
            user-select: none;
            touch-action: none;
        }}
        #resizer-gutter::after {{
            content: "⋮";
            color: var(--text-muted);
            font-size: 0.95rem;
            font-weight: 900;
            line-height: 1;
            pointer-events: none;
        }}
        #resizer-gutter:hover,
        #resizer-gutter.dragging {{
            background: rgba(2, 132, 199, 0.16);
            border-color: var(--accent-blue);
        }}
        #resizer-gutter:hover::after,
        #resizer-gutter.dragging::after {{
            color: var(--accent-blue);
        }}
        body.is-resizing {{
            cursor: col-resize !important;
            user-select: none !important;
        }}

        /* Floating Map Filter Toolbar — Single-Row Horizontal Scroll (Zero Multi-Row Clutter) */
        .filter-toolbar {{
            position: absolute;
            top: 10px;
            left: 50px;
            right: 10px;
            z-index: 900;
            display: flex;
            flex-wrap: nowrap;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            scrollbar-width: none;
            gap: 4px;
            padding-bottom: 2px;
            pointer-events: auto;
        }}
        .filter-toolbar::-webkit-scrollbar {{
            display: none;
        }}

        .filter-btn {{
            flex-shrink: 0;
            pointer-events: auto;
            background: var(--bg-panel);
            backdrop-filter: blur(8px);
            border: 1px solid var(--border);
            color: var(--text-main);
            padding: 4px 9px;
            border-radius: 16px;
            font-size: 0.71rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s ease;
            display: flex;
            align-items: center;
            gap: 4px;
            box-shadow: var(--shadow-card);
            white-space: nowrap;
        }}

        .filter-btn:hover {{
            border-color: var(--accent-blue);
            transform: translateY(-1px);
        }}

        .filter-btn.active {{
            background: var(--accent-blue);
            color: #ffffff;
            border-color: var(--accent-blue);
        }}

        /* Right Sidebar (Itinerary) */
        .sidebar {{
            flex: 0 0 540px;
            width: 540px;
            min-width: 160px;
            max-width: none;
            background: var(--bg-panel);
            display: flex;
            flex-direction: column;
            height: 100%;
        }}

        .sidebar-header {{
            padding: 12px 16px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--bg-subtle);
            gap: 8px;
            flex-wrap: wrap;
        }}

        .sidebar-header h2 {{
            font-size: 0.98rem;
            font-weight: 800;
            color: var(--text-main);
        }}

        .reset-map-btn {{
            background: var(--bg-card);
            border: 1px solid var(--accent-blue);
            color: var(--accent-blue);
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 0.73rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s ease;
            white-space: nowrap;
        }}

        .reset-map-btn:hover {{
            background: var(--accent-blue);
            color: #ffffff;
        }}

        /* Sticky Mobile Day Jump Bar */
        .day-jump-bar {{
            display: flex;
            gap: 5px;
            padding: 8px 14px;
            background: var(--bg-panel);
            border-bottom: 1px solid var(--border);
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            scrollbar-width: none;
            flex-shrink: 0;
        }}
        .day-jump-bar::-webkit-scrollbar {{ display: none; }}

        .day-jump-pill {{
            flex-shrink: 0;
            background: var(--bg-subtle);
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 4px 10px;
            border-radius: 14px;
            font-size: 0.73rem;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.15s ease;
        }}
        .day-jump-pill:hover, .day-jump-pill.active {{
            background: var(--accent-blue);
            color: #ffffff;
            border-color: var(--accent-blue);
        }}

        .itinerary-list {{
            flex: 1;
            overflow-y: auto;
            overflow-x: hidden;
            padding: 14px;
            display: flex;
            flex-direction: column;
            gap: 14px;
        }}

        /* Day Cards */
        .day-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px;
            cursor: pointer;
            transition: border-color 0.15s ease, box-shadow 0.15s ease;
            position: relative;
            box-shadow: var(--shadow-card);
        }}

        .day-card:hover {{
            background: var(--bg-card-hover);
            border-color: var(--accent-blue);
        }}

        .day-card.active {{
            border-color: var(--accent-blue);
            box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.25);
        }}

        .day-card.collapsed {{
            padding: 12px 16px;
        }}
        .day-card.collapsed .day-collapsible-body {{
            display: none;
        }}
        .day-card.collapsed .stats-row {{
            margin-bottom: 0;
        }}

        .day-collapse-btn {{
            background: var(--bg-subtle);
            border: 1px solid var(--border);
            color: var(--text-muted);
            width: 24px;
            height: 24px;
            border-radius: 6px;
            font-size: 0.80rem;
            font-weight: 800;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            transition: all 0.15s ease;
            padding: 0;
            line-height: 1;
        }}
        .day-collapse-btn:hover {{
            background: var(--accent-blue);
            color: #ffffff;
            border-color: var(--accent-blue);
        }}

        .day-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            margin-bottom: 10px;
            gap: 8px;
        }}

        .day-title-row {{
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .day-badge {{
            font-size: 0.72rem;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: 4px;
            color: #fff;
            text-transform: uppercase;
        }}

        .day-title {{
            font-size: 1.02rem;
            font-weight: 800;
            color: var(--text-main);
        }}

        .day-date {{
            font-size: 0.74rem;
            color: var(--text-muted);
            font-weight: 600;
            white-space: nowrap;
        }}

        .stats-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 10px;
        }}

        .stat-chip {{
            background: var(--bg-stat);
            border: 1px solid var(--border);
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.74rem;
            color: var(--text-card);
            font-weight: 600;
        }}

        .weather-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 6px;
            background: rgba(2, 132, 199, 0.08);
            border: 1px solid rgba(2, 132, 199, 0.25);
            padding: 6px 10px;
            border-radius: 6px;
            margin-bottom: 10px;
            font-size: 0.74rem;
            color: var(--text-main);
        }}

        .live-weather-badge {{
            background: var(--bg-card);
            padding: 2px 7px;
            border-radius: 4px;
            font-weight: 700;
            color: var(--accent-blue);
            border: 1px solid var(--border);
        }}

        .day-desc {{
            font-size: 0.83rem;
            line-height: 1.48;
            color: var(--text-card);
            margin-bottom: 12px;
        }}

        .hotel-box {{
            background: var(--bg-subtle);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 10px 12px;
            margin-bottom: 8px;
        }}

        .hotel-header-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            margin-bottom: 3px;
        }}

        .hotel-title {{
            font-size: 0.83rem;
            font-weight: 800;
            color: var(--accent-green);
        }}

        .hotel-rate-pill {{
            font-size: 0.72rem;
            font-weight: 800;
            background: rgba(5, 150, 105, 0.12);
            color: var(--accent-green);
            padding: 2px 8px;
            border-radius: 12px;
            border: 1px solid rgba(5, 150, 105, 0.3);
            white-space: nowrap;
        }}

        .hotel-sub {{
            font-size: 0.76rem;
            color: var(--text-muted);
            margin-bottom: 6px;
        }}

        .hotel-actions {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}

        .hotel-action-btn {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 9px;
            border-radius: 5px;
            font-size: 0.72rem;
            font-weight: 700;
            text-decoration: none;
            transition: all 0.15s ease;
        }}

        .fuel-box {{
            background: rgba(217, 119, 6, 0.08);
            border: 1px solid rgba(217, 119, 6, 0.35);
            border-radius: 6px;
            padding: 9px 11px;
            font-size: 0.77rem;
            color: var(--text-main);
            margin-bottom: 10px;
            line-height: 1.42;
        }}

        .fuel-box strong {{
            color: var(--accent-orange);
        }}

        .highlights-box {{
            background: var(--bg-subtle);
            border-radius: 6px;
            padding: 9px 12px;
            border: 1px solid var(--border);
        }}

        .highlights-title {{
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 5px;
            letter-spacing: 0.4px;
        }}

        .highlights-list {{
            list-style: none;
            font-size: 0.77rem;
            color: var(--text-card);
        }}

        .highlights-list li {{
            margin-bottom: 3px;
            display: flex;
            align-items: flex-start;
            gap: 6px;
        }}

        .highlights-list li::before {{
            content: "▸";
            color: var(--accent-blue);
            font-weight: bold;
        }}

        .gmaps-btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            margin-top: 4px;
            padding: 8px 12px;
            background: rgba(5, 150, 105, 0.1);
            border: 1px solid var(--accent-green);
            color: var(--accent-green);
            border-radius: 6px;
            font-size: 0.78rem;
            font-weight: 700;
            text-decoration: none;
            transition: all 0.15s ease;
        }}

        .gmaps-btn:hover {{
            background: var(--accent-green);
            color: #fff;
        }}

        /* Bottom Details Section */
        .details-section {{
            padding: 28px 24px 90px 24px;
            max-width: 1600px;
            margin: 0 auto;
            width: 100%;
        }}

        .section-title {{
            font-size: 1.35rem;
            font-weight: 800;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--border);
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--text-main);
        }}

        /* Budget Cards & Matrix */
        .budget-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
            gap: 14px;
            margin-bottom: 22px;
        }}

        .budget-card {{
            background: var(--bg-panel);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 18px;
            box-shadow: var(--shadow-card);
        }}

        .budget-card .label {{
            font-size: 0.75rem;
            text-transform: uppercase;
            color: var(--text-muted);
            font-weight: 800;
            letter-spacing: 0.5px;
        }}

        .budget-card .amount {{
            font-size: 1.65rem;
            font-weight: 900;
            color: var(--accent-green);
            margin: 6px 0 4px 0;
        }}

        .budget-card .sub {{
            font-size: 0.77rem;
            color: var(--text-card);
            line-height: 1.4;
        }}

        /* Downloads & Safety Grid */
        .downloads-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 14px;
            margin-bottom: 32px;
        }}

        .download-card {{
            background: var(--bg-panel);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 18px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: var(--shadow-card);
        }}

        .download-card h4 {{
            font-size: 0.98rem;
            margin-bottom: 6px;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .download-card p {{
            font-size: 0.80rem;
            color: var(--text-muted);
            margin-bottom: 14px;
            line-height: 1.42;
        }}

        .dl-btn {{
            display: inline-block;
            text-align: center;
            background: var(--accent-blue);
            color: #ffffff;
            font-weight: 800;
            font-size: 0.80rem;
            padding: 9px 14px;
            border-radius: 6px;
            text-decoration: none;
            transition: opacity 0.15s ease;
        }}

        .dl-btn:hover {{
            opacity: 0.9;
        }}

        /* Tables */
        .table-wrapper {{
            overflow-x: auto;
            background: var(--bg-panel);
            border: 1px solid var(--border);
            border-radius: 10px;
            margin-bottom: 32px;
            box-shadow: var(--shadow-card);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.82rem;
        }}

        th, td {{
            padding: 11px 14px;
            border-bottom: 1px solid var(--border);
        }}

        th {{
            background: var(--bg-subtle);
            color: var(--text-muted);
            font-weight: 800;
            text-transform: uppercase;
            font-size: 0.72rem;
            letter-spacing: 0.5px;
        }}

        tr:hover td {{
            background: var(--bg-card-hover);
        }}

        /* Leaflet Custom Popup */
        .leaflet-popup-pane {{
            z-index: 950 !important;
        }}
        .leaflet-popup-content-wrapper {{
            background: var(--bg-card);
            color: var(--text-main);
            border: 1px solid var(--border);
            border-radius: 10px;
            box-shadow: var(--shadow-card);
        }}
        .leaflet-popup-tip {{
            background: var(--bg-card);
        }}
        .poi-popup-card {{
            min-width: 245px;
            max-width: 290px;
        }}
        .poi-popup-photo-wrap {{
            width: 100%;
            height: 138px;
            border-radius: 7px;
            overflow: hidden;
            margin-bottom: 8px;
            border: 1px solid var(--border);
            background: var(--bg-subtle);
            position: relative;
        }}
        .poi-popup-photo {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }}
        .poi-popup-title {{
            font-weight: 800;
            font-size: 0.92rem;
            margin-bottom: 3px;
            color: var(--text-main);
        }}
        .poi-popup-type {{
            font-size: 0.68rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--accent-blue);
            font-weight: 800;
            margin-bottom: 6px;
        }}
        .poi-popup-desc {{
            font-size: 0.79rem;
            color: var(--text-card);
            line-height: 1.38;
            margin-bottom: 8px;
        }}
        .poi-popup-link {{
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--accent-green);
            text-decoration: none;
        }}

        /* Family & Friends Cloud Live Tracker HUD & Pulsing Bike Marker */
        .live-dot {{
            width: 9px;
            height: 9px;
            border-radius: 50%;
            display: inline-block;
            background: var(--accent-green);
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            animation: livePulse 2s infinite;
        }}
        .live-dot.standby {{
            background: var(--accent-orange);
            animation: none;
        }}
        @keyframes livePulse {{
            0% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
            70% {{ box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
        }}

        .live-bike-marker-wrap {{
            position: relative;
            width: 38px;
            height: 38px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.25s ease;
        }}
        .live-bike-marker-wrap.co-located-atas {{
            transform: translate(-23px, 0);
        }}
        .live-bike-marker-wrap.co-located-v2s {{
            transform: translate(23px, 0);
        }}
        .live-bike-pulse {{
            position: absolute;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: rgba(220, 38, 38, 0.35);
            border: 2px solid #dc2626;
            animation: bikeRadar 1.8s ease-out infinite;
        }}
        .live-bike-pulse.v2s {{
            background: rgba(22, 163, 74, 0.38);
            border-color: #16a34a;
        }}
        .live-bike-core {{
            position: relative;
            z-index: 2;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: #ffffff;
            border: 2.5px solid #dc2626;
            box-shadow: 0 2px 8px rgba(0,0,0,0.45);
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .live-bike-core.v2s {{
            background: #16a34a;
            border: 2.5px solid #ffffff;
        }}
        .live-bike-callsign {{
            position: absolute;
            bottom: -11px;
            z-index: 3;
            background: #ffffff;
            color: #dc2626;
            font-size: 0.58rem;
            font-weight: 900;
            letter-spacing: 0.4px;
            padding: 1px 5px;
            border-radius: 4px;
            border: 1.5px solid #dc2626;
            box-shadow: 0 1px 4px rgba(0,0,0,0.4);
            white-space: nowrap;
        }}
        .live-bike-callsign.v2s {{
            background: #16a34a;
            color: #ffffff;
            border: 1.5px solid #ffffff;
        }}
        @keyframes bikeRadar {{
            0% {{ transform: scale(0.8); opacity: 1; }}
            100% {{ transform: scale(2.1); opacity: 0; }}
        }}

        .lt-rider-pill {{
            display: inline-flex;
            align-items: center;
            gap: 3px;
            padding: 1px 6px;
            border-radius: 4px;
            font-size: 0.64rem;
            font-weight: 900;
            color: #dc2626;
            letter-spacing: 0.4px;
            background: #ffffff;
            border: 1.5px solid #dc2626;
            box-shadow: 0 1px 2px rgba(220, 38, 38, 0.18);
        }}
        .lt-rider-pill.v2s {{
            background: #16a34a;
            color: #ffffff;
            border: 1.5px solid #15803d;
            box-shadow: 0 1px 2px rgba(22, 163, 74, 0.22);
        }}
        .lt-riders-grid {{
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
            gap: 7px;
        }}
        .lt-rider-card {{
            background: var(--bg-subtle);
            border: 1px solid var(--border);
            border-left: 4px solid #dc2626;
            border-radius: 8px;
            padding: 7px 9px;
            cursor: pointer;
            min-width: 0;
            transition: border-color 0.15s ease, transform 0.15s ease;
        }}
        .lt-rider-card.v2s {{
            border-left-color: #16a34a;
        }}
        .lt-rider-card:hover {{
            transform: translateY(-1px);
        }}

        .live-tracker-panel {{
            position: absolute;
            bottom: 20px;
            right: 14px;
            z-index: 920;
            width: 375px;
            max-width: calc(100vw - 28px);
            background: var(--bg-panel);
            border: 1px solid var(--border);
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
            color: var(--text-main);
            display: none;
            flex-direction: column;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }}
        .live-tracker-panel.open {{
            display: flex;
        }}
        .lt-header {{
            padding: 10px 12px;
            background: var(--bg-subtle);
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 6px;
        }}
        .lt-title {{
            font-size: 0.78rem;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 6px;
            color: var(--text-main);
            white-space: nowrap;
        }}
        .lt-body {{
            padding: 12px 14px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-height: 68vh;
            overflow-y: auto;
            overflow-x: hidden;
        }}
        .lt-status-box {{
            background: var(--bg-subtle);
            border: 1px solid var(--border);
            border-left: 4px solid var(--accent-green);
            border-radius: 8px;
            padding: 9px 11px;
        }}
        .lt-metrics-grid {{
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
            gap: 7px;
        }}
        .lt-metric-card {{
            background: var(--bg-subtle);
            border: 1px solid var(--border);
            border-radius: 7px;
            padding: 7px 9px;
            min-width: 0;
            overflow: hidden;
        }}
        .lt-metric-label {{
            font-size: 0.65rem;
            text-transform: uppercase;
            font-weight: 800;
            color: var(--text-muted);
            letter-spacing: 0.4px;
        }}
        .lt-metric-val {{
            font-size: 0.80rem;
            font-weight: 800;
            color: var(--text-main);
            margin-top: 2px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .lt-feed-list {{
            display: flex;
            flex-direction: column;
            gap: 6px;
            max-height: 135px;
            overflow-y: auto;
            padding-right: 2px;
        }}
        .lt-feed-item {{
            background: var(--bg-subtle);
            border: 1px solid var(--border);
            border-radius: 7px;
            padding: 7px 9px;
            font-size: 0.74rem;
            cursor: pointer;
            transition: border-color 0.15s ease;
        }}
        .lt-feed-item:hover {{
            border-color: var(--accent-blue);
        }}
        .lt-chip-btn {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-main);
            padding: 5px 8px;
            border-radius: 6px;
            font-size: 0.71rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s ease;
        }}
        .lt-chip-btn:hover, .lt-chip-btn.active {{
            background: var(--accent-blue);
            color: #ffffff;
            border-color: var(--accent-blue);
        }}

        /* Native Mobile Bottom Navigation Bar */
        .mobile-bottom-nav {{
            display: none;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 60px;
            background: var(--bg-panel);
            border-top: 1px solid var(--border);
            z-index: 2000;
            justify-content: space-around;
            align-items: center;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.08);
        }}

        .mob-nav-btn {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-size: 0.68rem;
            font-weight: 700;
            gap: 3px;
            cursor: pointer;
            flex: 1;
            height: 100%;
        }}

        .mob-nav-btn span.icon {{
            font-size: 1.15rem;
        }}

        .mob-nav-btn.active {{
            color: var(--accent-blue);
            border-top: 2px solid var(--accent-blue);
        }}

        /* Responsive Mobile App Layout */
        @media (max-width: 1024px) {{
            header {{
                padding: 10px 14px;
            }}
            .header-title h1 {{
                font-size: 1.05rem;
            }}
            .header-badges .badge.hide-mobile {{
                display: none;
            }}
            .main-container {{
                flex-direction: column;
                height: auto;
                min-height: 0;
            }}
            .map-wrapper {{
                height: 62vh;
                min-height: 380px;
                flex: none;
                width: 100%;
            }}
            .filter-toolbar {{
                left: 48px;
                flex-wrap: nowrap;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
                padding-bottom: 4px;
                scrollbar-width: none;
            }}
            .filter-toolbar::-webkit-scrollbar {{ display: none; }}
            #resizer-gutter {{
                display: none !important;
            }}
            .sidebar {{
                flex: none !important;
                width: 100% !important;
                min-width: 100% !important;
                max-width: 100% !important;
                height: auto;
                border-left: none;
                border-top: 2px solid var(--border);
            }}
            .itinerary-list {{
                max-height: none;
                overflow-y: visible;
            }}
            .mobile-bottom-nav {{
                display: flex;
            }}
            .live-tracker-panel {{
                bottom: 10px;
                right: 10px;
                left: 10px;
                width: auto;
            }}
            .chk-bikes-grid {{
                grid-template-columns: 1fr !important;
            }}
        }}

        /* Permanent Unpaved QC-389 Map Label Pill */
        .gravel-map-label {{
            background: rgba(120, 53, 15, 0.92);
            color: #fef3c7;
            border: 1.5px dashed #f59e0b;
            border-radius: 6px;
            padding: 2px 7px;
            font-size: 0.66rem;
            font-weight: 800;
            white-space: nowrap;
            box-shadow: 0 2px 6px rgba(0,0,0,0.35);
            pointer-events: auto;
        }}

        /* Per-Bike Luggage Volume & Packing Checklist (Git-Backed) */
        .chk-sync-bar {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-left: 4px solid var(--accent-blue);
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            box-shadow: var(--shadow-card);
        }}
        .chk-bikes-grid {{
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
            gap: 18px;
            align-items: start;
        }}
        .chk-bike-panel {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            box-shadow: var(--shadow-card);
            display: flex;
            flex-direction: column;
            gap: 14px;
        }}
        .chk-bike-panel.jamie {{
            border-top: 4px solid #dc2626;
        }}
        .chk-bike-panel.rosie {{
            border-top: 4px solid #16a34a;
        }}
        .chk-vol-bar-track {{
            width: 100%;
            height: 10px;
            background: var(--bg-subtle);
            border: 1px solid var(--border);
            border-radius: 99px;
            overflow: hidden;
            position: relative;
        }}
        .chk-vol-bar-fill {{
            height: 100%;
            border-radius: 99px;
            transition: width 0.25s ease, background-color 0.25s ease;
        }}
        .chk-comp-card {{
            background: var(--bg-subtle);
            border: 1px solid var(--border);
            border-radius: 9px;
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .chk-item-row {{
            display: flex;
            align-items: center;
            gap: 7px;
            padding: 6px 8px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 7px;
            font-size: 0.78rem;
            transition: border-color 0.15s ease, opacity 0.15s ease;
        }}
        .chk-item-row.unpacked {{
            opacity: 0.65;
            border-style: dashed;
        }}
        .chk-item-row:hover {{
            border-color: var(--accent-blue);
        }}
        .chk-inline-input {{
            background: transparent;
            color: var(--text-main);
            border: 1px solid transparent;
            border-radius: 4px;
            padding: 2px 5px;
            font-size: 0.78rem;
            font-family: inherit;
        }}
        .chk-inline-input:hover,
        .chk-inline-input:focus {{
            background: var(--bg-subtle);
            border-color: var(--accent-blue);
            outline: none;
        }}
        .chk-num-input {{
            width: 54px;
            text-align: right;
            font-family: monospace;
            font-weight: 700;
            background: var(--bg-subtle);
            color: var(--accent-blue);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 2px 4px;
            font-size: 0.75rem;
        }}
    </style>
</head>
<body>

    <header>
        <div class="header-title">
            <h1>Expedition 51</h1>
            <p>June 16 – July 3, 2027 • 18 Days • 8,243.4 km</p>
        </div>
        <div class="header-badges">
            <div class="stats-strip hide-mobile">
                <div class="stat-item"><span class="val">8,243.4 km</span><span class="lbl">Distance</span></div>
                <div class="stat-item"><span class="val">18 Days</span><span class="lbl">Stages</span></div>
                <div class="stat-item"><span class="val">{len(pois_data)} POIs</span><span class="lbl">Pins</span></div>
            </div>
            <button type="button" class="theme-toggle-btn" id="live-tracker-btn" onclick="toggleLiveTrackerPanel()" style="border-color: var(--accent-green); color: var(--accent-green);">
                <span class="live-dot" id="live-tracker-dot"></span>
                <span>📡 Live Tracker</span>
            </button>
            <button type="button" class="theme-toggle-btn" id="checklist-nav-btn" onclick="document.getElementById('sec-checklist').scrollIntoView({{behavior:'smooth'}})" style="border-color: var(--accent-orange); color: var(--accent-orange);">
                <span>🧳</span> <span>Checklist</span>
            </button>
            <button type="button" class="theme-toggle-btn" id="notes-btn" onclick="openNotesModal()">
                <span>📝</span> <span>Notes</span>
            </button>
            <button type="button" class="theme-toggle-btn" id="theme-toggle" onclick="toggleTheme()">
                <span id="theme-icon">🌙</span> <span id="theme-label">Dark Mode</span>
            </button>
        </div>
    </header>

    <div class="main-container" id="sec-top">
        <!-- Interactive Map -->
        <div class="map-wrapper" id="sec-map">
            <div class="filter-toolbar" id="poi-filter-toolbar">
                <button type="button" class="filter-btn active" data-cat="all" onclick="filterPOIs('all', this)">🌐 All</button>
                <button type="button" class="filter-btn" data-cat="lodging" onclick="filterPOIs('lodging', this)">🏕️ Lodging</button>
                <button type="button" class="filter-btn" data-cat="fuel" onclick="filterPOIs('fuel', this)">⛽ Fuel</button>
                <button type="button" class="filter-btn" data-cat="food" onclick="filterPOIs('food', this)">🍽️ Food</button>
                <button type="button" class="filter-btn" data-cat="coffee" onclick="filterPOIs('coffee', this)">☕ Coffee</button>
                <button type="button" class="filter-btn" data-cat="sights" onclick="filterPOIs('sights', this)">📸 Sights</button>
                <button type="button" class="filter-btn" data-cat="ferry" onclick="filterPOIs('ferry', this)">⛴️ Ferries</button>
                <button type="button" class="filter-btn" data-cat="qc389" onclick="filterPOIs('qc389', this)">⚠️ QC-389</button>
            </div>

            <div id="map"></div>

            <!-- Family & Friends Cloud Live Tracker Panel (Dual-Rider: Jamie White/Red & Rosie Green) -->
            <div class="live-tracker-panel" id="live-tracker-panel">
                <div class="lt-header">
                    <div class="lt-title">
                        <span class="live-dot" id="lt-panel-dot"></span>
                        <span>📡 Live Tracker</span>
                    </div>
                    <div style="display:flex; align-items:center; gap:4px; flex-shrink:0;">
                        <button type="button" onclick="centerOnLiveBike('Jamie')" class="lt-chip-btn" style="padding:2px 6px; font-size:0.65rem; background:#ffffff; border:1.5px solid #dc2626; color:#dc2626; font-weight:900; white-space:nowrap;" title="Center map on Jamie (White &amp; Red 2025 Africa Twin)">🎯 Jamie</button>
                        <button type="button" onclick="centerOnLiveBike('Rosie')" class="lt-chip-btn" style="padding:2px 6px; font-size:0.65rem; background:#16a34a; border:1.5px solid #15803d; color:#ffffff; font-weight:900; white-space:nowrap;" title="Center map on Rosie (Green Ducati V2S)">🎯 Rosie</button>
                        <button type="button" onclick="toggleLiveTrackerPanel()" style="background:transparent; border:none; color:var(--text-muted); font-size:0.95rem; cursor:pointer; padding:2px 4px;">✕</button>
                    </div>
                </div>

                <div class="lt-body">
                    <!-- Dual-Rider Live Status Cards (Jamie White/Red & Rosie Green) -->
                    <div class="lt-riders-grid">
                        <div class="lt-rider-card" id="lt-card-atas" onclick="centerOnLiveBike('Jamie')" title="Click to center on Jamie (White &amp; Red 2025 Honda Africa Twin)">
                            <div style="display:flex; justify-content:space-between; align-items:center; gap:4px; margin-bottom:3px;">
                                <span class="lt-rider-pill"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="5.5" cy="17.5" r="3.5"/><circle cx="18.5" cy="17.5" r="3.5"/><path d="M15 6h3l2 5h-5l-3-5z" fill="#dc2626"/><path d="M6 14l4-5h5l2 5"/></svg> Jamie</span>
                                <span id="lt-time-atas" style="font-size:0.62rem; color:var(--text-muted); font-family:monospace;">Ready</span>
                            </div>
                            <div id="lt-status-atas" style="font-size:0.72rem; font-weight:800; color:var(--text-main); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">🏕️ Hanmer Start</div>
                            <div id="lt-note-atas" style="font-size:0.67rem; color:var(--text-muted); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-top:1px;">2025 Africa Twin • Day 1</div>
                        </div>

                        <div class="lt-rider-card v2s" id="lt-card-v2s" onclick="centerOnLiveBike('Rosie')" title="Click to center on Rosie (Green Ducati Multistrada V2S)">
                            <div style="display:flex; justify-content:space-between; align-items:center; gap:4px; margin-bottom:3px;">
                                <span class="lt-rider-pill v2s"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="5.5" cy="17.5" r="3.5"/><circle cx="18.5" cy="17.5" r="3.5"/><path d="M15 6h3l2 5h-5l-3-5z" fill="#ffffff"/><path d="M6 14l4-5h5l2 5"/></svg> Rosie</span>
                                <span id="lt-time-v2s" style="font-size:0.62rem; color:var(--text-muted); font-family:monospace;">Ready</span>
                            </div>
                            <div id="lt-status-v2s" style="font-size:0.72rem; font-weight:800; color:var(--text-main); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">🏕️ Hanmer Start</div>
                            <div id="lt-note-v2s" style="font-size:0.67rem; color:var(--text-muted); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-top:1px;">Ducati V2S • Day 1</div>
                        </div>
                    </div>

                    <!-- Loop Progress Bar -->
                    <div>
                        <div style="display:flex; justify-content:space-between; font-size:0.71rem; font-weight:800; margin-bottom:4px;">
                            <span style="color:var(--text-muted);">PROGRESS</span>
                            <span id="lt-progress-text" style="color:var(--accent-blue);">0.0 / 8,243.4 km (0.0%)</span>
                        </div>
                        <div style="width:100%; height:7px; background:var(--bg-subtle); border:1px solid var(--border); border-radius:99px; overflow:hidden;">
                            <div id="lt-progress-fill" style="width:1%; height:100%; background:linear-gradient(90deg, var(--accent-blue), var(--accent-green)); transition:width 0.35s ease;"></div>
                        </div>
                    </div>

                    <!-- 4-Metric Telemetry Summary (Pure Metric) -->
                    <div class="lt-metrics-grid">
                        <div class="lt-metric-card">
                            <div class="lt-metric-label">📅 Stage</div>
                            <div class="lt-metric-val" id="lt-metric-stage">Day 1: Hanmer → Mirabel</div>
                        </div>
                        <div class="lt-metric-card">
                            <div class="lt-metric-label">🏕️ To Lodging</div>
                            <div class="lt-metric-val" id="lt-metric-hotel">648.7 km to Mirabel</div>
                        </div>
                        <div class="lt-metric-card">
                            <div class="lt-metric-label">⛽ Next Fuel</div>
                            <div class="lt-metric-val" id="lt-metric-fuel">Sturgeon Falls (91 AKI)</div>
                        </div>
                        <div class="lt-metric-card">
                            <div class="lt-metric-label">🤝 Riders</div>
                            <div class="lt-metric-val" id="lt-metric-speed">Together (0.0 km apart)</div>
                        </div>
                    </div>

                    <!-- Recent Check-Ins & Breadcrumb Feed -->
                    <div>
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
                            <span style="font-size:0.68rem; font-weight:800; text-transform:uppercase; color:var(--text-muted); letter-spacing:0.4px;">📍 Check-Ins</span>
                            <button type="button" onclick="pollCloudTrackerFeed(true)" style="background:transparent; border:none; color:var(--accent-blue); font-size:0.68rem; font-weight:700; cursor:pointer;">🔄 Refresh</button>
                        </div>
                        <div class="lt-feed-list" id="lt-feed-list">
                            <!-- Populated dynamically -->
                        </div>
                    </div>

                    <!-- PIN-Protected Rider Broadcast & Check-In Drawer -->
                    <div style="border-top:1px solid var(--border); padding-top:8px;">
                        <button type="button" onclick="toggleRiderBroadcastDrawer()" style="width:100%; background:var(--bg-subtle); border:1px solid var(--border); color:var(--text-muted); padding:6px 10px; border-radius:6px; font-size:0.72rem; font-weight:800; cursor:pointer; display:flex; justify-content:space-between; align-items:center;">
                            <span>🔐 Rider Check-In &amp; GPS</span>
                            <span id="lt-rider-chevron">▸</span>
                        </button>

                        <div id="lt-rider-drawer" style="display:none; margin-top:8px; background:var(--bg-subtle); border:1px solid var(--border); border-radius:8px; padding:10px;">
                            <!-- PIN Lock Screen -->
                            <div id="lt-pin-gate" style="display:flex; gap:6px; align-items:center;">
                                <input type="password" id="lt-pin-input" placeholder="Rider PIN (2027)" style="flex:1; background:var(--bg-panel); color:var(--text-main); border:1px solid var(--border); border-radius:6px; padding:6px 9px; font-size:0.76rem;" />
                                <button type="button" onclick="unlockRiderControls()" class="dl-btn" style="padding:6px 12px; font-size:0.74rem;">Unlock</button>
                            </div>

                            <!-- Unlocked Rider Broadcast Controls -->
                            <div id="lt-rider-controls" style="display:none; flex-direction:column; gap:8px;">
                                <!-- Rider Bike Callsign Selector (Jamie White/Red vs Rosie Green) -->
                                <div>
                                    <div style="font-size:0.66rem; font-weight:800; color:var(--text-muted); text-transform:uppercase; margin-bottom:4px;">1. Select Rider:</div>
                                    <div style="display:flex; gap:6px;">
                                        <button type="button" id="btn-rider-atas" class="lt-chip-btn active" onclick="selectRiderCallsign('Jamie')" style="flex:1; border:1.5px solid #dc2626;">⚪🔴 Jamie (2025 Africa Twin)</button>
                                        <button type="button" id="btn-rider-v2s" class="lt-chip-btn" onclick="selectRiderCallsign('Rosie')" style="flex:1; border:1.5px solid #16a34a;">🟢 Rosie (Ducati V2S)</button>
                                    </div>
                                </div>

                                <div style="display:flex; justify-content:space-between; align-items:center; gap:6px;">
                                    <button type="button" id="btn-auto-gps" onclick="toggleAutoGpsBroadcast()" class="lt-chip-btn" style="flex:1; border-color:var(--accent-green); color:var(--accent-green);">
                                        📡 Start Live Phone GPS
                                    </button>
                                    <span id="lt-queue-badge" onclick="flushOfflineTrackerQueue()" style="font-size:0.68rem; font-weight:700; color:var(--text-muted); cursor:pointer;" title="Tap to force sync">✓ 0 queued</span>
                                </div>

                                <div style="font-size:0.68rem; font-weight:800; color:var(--text-muted); text-transform:uppercase;">2. Status:</div>
                                <div style="display:flex; flex-wrap:wrap; gap:5px;" id="lt-status-chips">
                                    <button type="button" class="lt-chip-btn active" onclick="selectCheckInStatus('🏍️ In Saddle', 'Riding on stage — all good!', this)">🏍️ Rolling</button>
                                    <button type="button" class="lt-chip-btn" onclick="selectCheckInStatus('⛽ Fuel Stop', 'Fueled up main tank & reserve bladder.', this)">⛽ Fueled Up</button>
                                    <button type="button" class="lt-chip-btn" onclick="selectCheckInStatus('🍽️ Meal Stop', 'Stopped for a 30m meal & coffee break.', this)">🍽️ Meal Stop</button>
                                    <button type="button" class="lt-chip-btn" onclick="selectCheckInStatus('⛴️ On Ferry', 'Bike strapped down safely on ferry deck!', this)">⛴️ On Ferry</button>
                                    <button type="button" class="lt-chip-btn" onclick="selectCheckInStatus('🏕️ Checked In', 'Arrived safely at tonight\\'s lodging!', this)">🏕️ Safe at Camp/Hotel</button>
                                </div>

                                <div>
                                    <div style="font-size:0.68rem; font-weight:800; color:var(--text-muted); margin-bottom:3px;">3. LOCATION:</div>
                                    <select id="lt-location-select" style="width:100%; background:var(--bg-panel); color:var(--text-main); border:1px solid var(--border); border-radius:6px; padding:5px 8px; font-size:0.74rem;">
                                        <option value="gps">📍 Use My Phone's Live GPS Hardware</option>
                                    </select>
                                </div>

                                <div style="display:flex; gap:6px;">
                                    <input type="text" id="lt-note-input" placeholder="Optional check-in note..." style="flex:1; background:var(--bg-panel); color:var(--text-main); border:1px solid var(--border); border-radius:6px; padding:6px 9px; font-size:0.75rem;" />
                                    <button type="button" onclick="postRiderCheckIn()" class="dl-btn" style="padding:6px 11px; font-size:0.74rem; white-space:nowrap; background:var(--accent-green);">📍 Post Live</button>
                                </div>
                                <div id="lt-broadcast-feedback" style="font-size:0.70rem; color:var(--accent-green); min-height:14px;"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Draggable Resizer Gutter -->
        <div id="resizer-gutter" title="Drag left/right to resize Map &amp; Itinerary panels (Double-click to reset)"></div>

        <!-- Right Sidebar: 18-Day Itinerary -->
        <div class="sidebar" id="sec-itinerary">
            <div class="sidebar-header">
                <h2>📅 Itinerary</h2>
                <div style="display:flex; gap:6px; align-items:center;">
                    <button type="button" class="reset-map-btn" id="btn-collapse-all" onclick="toggleAllDayCards()">↕️ Expand All</button>
                    <button type="button" class="reset-map-btn" onclick="resetMapView()">🔄 Full Loop</button>
                </div>
            </div>
            <div class="day-jump-bar">
                {day_jump_pills}
            </div>
            <div class="itinerary-list" id="itinerary-list">
                {all_day_cards_str}
            </div>
        </div>
    </div>

    <!-- Bottom Sections: Schedule, Budget, Motorcycles, Checklist & Exports -->
    <div class="details-section">

        <!-- 1. Interactive Master Gantt Timeline -->
        {gantt_html}

        <!-- 2. Budget -->
        <h2 class="section-title" id="sec-budget" style="margin-top: 32px;">💰 Budget</h2>
        <div class="budget-grid">
            <div class="budget-card">
                <div class="label">🏕️ Lodging (17 Nights)</div>
                <div class="amount">$1,671 CAD</div>
                <div class="sub">7 camp nights ($306) + 9 hotel/cabin nights ($1,225) + 1 ferry stateroom share ($140).</div>
            </div>
            <div class="budget-card">
                <div class="label">⛽ Fuel &amp; Octane Booster</div>
                <div class="amount">$890 CAD</div>
                <div class="sub">~445 L per bike @ avg $1.95/L + 2× Lucas Oil MMT Octane Booster bottles ($24 CAD).</div>
            </div>
            <div class="budget-card">
                <div class="label">⛴️ Ferries, Bridges &amp; Parks</div>
                <div class="amount">$485 CAD</div>
                <div class="sub">MV Qajaq W ($55) + Marine Atlantic ($185) + Confederation Bridge ($21.50) + Parks ($223).</div>
            </div>
            <div class="budget-card">
                <div class="label">🍽️ Total Per Rider (Hybrid)</div>
                <div class="amount">$4,486 CAD</div>
                <div class="sub">Includes $1,440 meals ($80/day). <strong>Range:</strong> $3,580 (Camp) • <strong>$4,486 (Hybrid)</strong> • $5,890 (Hotel).</div>
            </div>
        </div>

        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>Category (Per Rider CAD)</th>
                        <th>🏕️ Max Camping</th>
                        <th>⚖️ Hybrid (Recommended)</th>
                        <th>🏨 Full Hotel</th>
                        <th>Notes</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Lodging (17 Nights)</strong></td>
                        <td>$980 CAD</td>
                        <td><strong>$1,671 CAD</strong></td>
                        <td>$3,075 CAD</td>
                        <td>Hotels/Cabins on Days 1–7, 17 + Parks/KOA on Days 8–9, 11–16.</td>
                    </tr>
                    <tr>
                        <td><strong>Fuel (8,243.4 km)</strong></td>
                        <td>$890 CAD</td>
                        <td><strong>$890 CAD</strong></td>
                        <td>$890 CAD</td>
                        <td>5.1 L/100km avg + auxiliary fuel bladders + Lucas Oil MMT.</td>
                    </tr>
                    <tr>
                        <td><strong>Ferries &amp; Tolls</strong></td>
                        <td>$265 CAD</td>
                        <td><strong>$265 CAD</strong></td>
                        <td>$265 CAD</td>
                        <td>Tadoussac (Free), MV Qajaq W ($55), Marine Atlantic ($185), Confederation Bridge ($21.50), A-30 ($3.50).</td>
                    </tr>
                    <tr>
                        <td><strong>Parks &amp; Admissions</strong></td>
                        <td>$220 CAD</td>
                        <td><strong>$220 CAD</strong></td>
                        <td>$220 CAD</td>
                        <td>Manic-5 Dam, Red Bay, L'Anse aux Meadows, Norstead, Gros Morne, Cape Breton, PEI, Hopewell Rocks.</td>
                    </tr>
                    <tr>
                        <td><strong>Meals &amp; Provisions</strong></td>
                        <td>$1,225 CAD</td>
                        <td><strong>$1,440 CAD</strong></td>
                        <td>$1,440 CAD</td>
                        <td>Breakfast, road lunch, and sit-down supper ($80/day).</td>
                    </tr>
                    <tr style="background: rgba(5, 150, 105, 0.08); font-weight: 800;">
                        <td><strong>TOTAL PER RIDER</strong></td>
                        <td><strong>$3,580 CAD</strong></td>
                        <td style="color: var(--accent-green); font-size: 0.95rem;"><strong>$4,486 CAD</strong></td>
                        <td><strong>$5,890 CAD</strong></td>
                        <td>All figures in CAD including tax.</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- 3. Simplified GPS & Data Exports Bar -->
        <h2 class="section-title" id="sec-downloads" style="margin-top: 28px;">📡 Exports</h2>
        <div style="display:flex; flex-wrap:wrap; gap:10px; align-items:center; background:var(--bg-card); border:1px solid var(--border); border-radius:10px; padding:12px 16px; box-shadow:var(--shadow-card); margin-bottom:28px;">
            <span style="font-size:0.80rem; font-weight:700; color:var(--text-muted); margin-right:6px;">Download 18 tracks &amp; {len(pois_data)} waypoints:</span>
            <a href="east_coast_adv_loop.gpx" download class="dl-btn" style="padding:7px 14px; font-size:0.78rem;">⬇️ GPX Route &amp; POIs (.gpx)</a>
            <a href="east_coast_route_tracks.kml" download class="dl-btn" style="padding:7px 14px; font-size:0.78rem; background:var(--bg-subtle); color:var(--text-main); border:1px solid var(--border);">⬇️ Route Tracks (.kml)</a>
            <a href="east_coast_colored_pois.kml" download class="dl-btn" style="padding:7px 14px; font-size:0.78rem; background:var(--bg-subtle); color:var(--text-main); border:1px solid var(--border);">⬇️ POIs (.kml)</a>
            <a href="east_coast_adv_pois.csv" download class="dl-btn" style="padding:7px 14px; font-size:0.78rem; background:var(--bg-subtle); color:var(--text-main); border:1px solid var(--border);">⬇️ Spreadsheet (.csv)</a>
        </div>

        <!-- 4. Motorcycles -->
        <h2 class="section-title" id="sec-fleet">🏍️ Motorcycles</h2>
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>Rider &amp; Motorcycle</th>
                        <th>Fuel Tank</th>
                        <th>Consumption</th>
                        <th>Highway Range</th>
                        <th>Aux Bladder</th>
                        <th>Fuel Grade &amp; Notes</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Jamie — 2025 Honda CRF1100L Africa Twin Adventure Sports ES (White &amp; Red)</strong></td>
                        <td>24.8 L</td>
                        <td>4.9 L/100km</td>
                        <td>~450 km</td>
                        <td>+100 km (~550 km)</td>
                        <td><strong>87 Regular</strong> — Native low-octane map handles all remote Labrador pumps.</td>
                    </tr>
                    <tr>
                        <td><strong>Rosie — 2026 Ducati Multistrada V2S (Green)</strong></td>
                        <td>19.0 L</td>
                        <td>5.2 L/100km</td>
                        <td>~315 km</td>
                        <td>+95 km (~410 km)</td>
                        <td><strong>91 Premium</strong> — Dose <strong>6 ml/L Lucas Oil MMT</strong> at remote 87-only pumps (Days 2–7).</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- 5. Packing Checklist (Git-Backed) -->
        <h2 class="section-title" id="sec-checklist" style="margin-top: 32px;">🧳 Packing Checklist</h2>
        <div class="chk-sync-bar">
            <div>
                <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                    <span style="font-size:0.84rem; font-weight:800; color:var(--text-main);">📦 Git Sync: <code style="background:var(--bg-subtle); padding:2px 6px; border-radius:4px; border:1px solid var(--border);">luggage_checklist.json</code></span>
                    <span id="chk-git-status-badge" style="font-size:0.73rem; font-weight:700; padding:3px 9px; border-radius:99px; background:rgba(5,150,105,0.14); color:var(--accent-green); border:1px solid rgba(5,150,105,0.3);">✓ Synced with Git (main)</span>
                </div>
            </div>
            <div style="display:flex; gap:7px; flex-wrap:wrap; align-items:center;">
                <div style="display:flex; gap:4px; background:var(--bg-subtle); padding:3px; border-radius:8px; border:1px solid var(--border);">
                    <button type="button" class="lt-chip-btn active" id="chk-view-both" onclick="setChecklistBikeFilter('both')">🏍️ Both Bikes</button>
                    <button type="button" class="lt-chip-btn" id="chk-view-jamie" onclick="setChecklistBikeFilter('jamie')">⚪🔴 Jamie (139L)</button>
                    <button type="button" class="lt-chip-btn" id="chk-view-rosie" onclick="setChecklistBikeFilter('rosie')">🟢 Rosie (104L)</button>
                </div>
                <button type="button" class="theme-toggle-btn" onclick="pullChecklistFromGit(true)" title="Fetch latest luggage_checklist.json from GitHub">🔄 Pull</button>
                <button type="button" class="dl-btn" id="btn-commit-git" onclick="commitChecklistToGit()" style="padding:6px 12px; font-size:0.76rem; background:var(--accent-green);">☁️ Save to Git</button>
                <button type="button" class="theme-toggle-btn" onclick="toggleGitTokenDrawer()" style="border-color:var(--text-muted); color:var(--text-muted);" title="Configure GitHub Token">🔑 Git Auth</button>
                <button type="button" class="theme-toggle-btn" onclick="downloadChecklistJson()" style="border-color:var(--text-muted); color:var(--text-muted);" title="Download luggage_checklist.json">⬇️ .json</button>
            </div>
        </div>

        <!-- Optional GitHub Token Configuration Bar -->
        <div id="chk-git-token-drawer" style="display:none; background:var(--bg-card); border:1px solid var(--border); border-left:4px solid var(--accent-purple); border-radius:10px; padding:12px 16px; margin-bottom:18px; box-shadow:var(--shadow-card);">
            <div style="font-size:0.80rem; font-weight:800; color:var(--text-main); margin-bottom:4px;">🔑 GitHub Direct Commit Token</div>
            <div style="display:flex; gap:8px; flex-wrap:wrap; align-items:center; margin-top:6px;">
                <input type="password" id="chk-github-pat-input" placeholder="github_pat_... or ghp_..." style="flex:1; min-width:240px; background:var(--bg-subtle); color:var(--text-main); border:1px solid var(--border); border-radius:6px; padding:6px 10px; font-size:0.78rem; font-family:monospace;" />
                <input type="text" id="chk-commit-author-input" placeholder="Committer" value="Jamie & Rosie" style="width:160px; background:var(--bg-subtle); color:var(--text-main); border:1px solid var(--border); border-radius:6px; padding:6px 10px; font-size:0.78rem;" />
                <button type="button" class="dl-btn" onclick="applyGitAuthConfig()" style="padding:6px 14px; font-size:0.76rem;">✓ Apply</button>
            </div>
        </div>

        <!-- Dual-Bike Interactive Luggage Volume & Checklist Grid -->
        <div class="chk-bikes-grid" id="chk-bikes-container">
            <!-- Rendered dynamically by renderLuggageChecklist() -->
        </div>

    </div>

    <!-- Native Mobile Bottom Bar -->
    <nav class="mobile-bottom-nav">
        <button type="button" class="mob-nav-btn active" onclick="mobileNav('map', this)">
            <span class="icon">🗺️</span>
            <span>Map</span>
        </button>
        <button type="button" class="mob-nav-btn" onclick="mobileNav('itinerary', this)">
            <span class="icon">📅</span>
            <span>Itinerary</span>
        </button>
        <button type="button" class="mob-nav-btn" onclick="mobileNav('gantt', this)">
            <span class="icon">⏱️</span>
            <span>Schedule</span>
        </button>
        <button type="button" class="mob-nav-btn" onclick="mobileNav('checklist', this)">
            <span class="icon">🧳</span>
            <span>Checklist</span>
        </button>
        <button type="button" class="mob-nav-btn" onclick="mobileNav('downloads', this)">
            <span class="icon">📡</span>
            <span>Budget</span>
        </button>
    </nav>

    <!-- Trip Notes Modal -->
    <div id="notes-modal-overlay" onclick="if(event.target===this) closeNotesModal()" style="display:none; position:fixed; inset:0; background:rgba(15,23,42,0.75); backdrop-filter:blur(4px); z-index:4000; align-items:center; justify-content:center; padding:16px;">
        <div style="background:var(--bg-panel); border:1px solid var(--border); border-radius:12px; width:100%; max-width:780px; max-height:88vh; display:flex; flex-direction:column; box-shadow:0 20px 50px rgba(0,0,0,0.5); overflow:hidden;">
            <div style="padding:16px 20px; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; align-items:center; background:var(--bg-subtle);">
                <div>
                    <h3 style="margin:0; font-size:1.05rem; color:var(--text-main); display:flex; align-items:center; gap:8px;">📝 Trip Notes</h3>
                    <div id="notes-sync-status" style="font-size:0.74rem; color:var(--accent-green); margin-top:2px;">✓ Saved</div>
                </div>
                <button type="button" onclick="closeNotesModal()" style="background:transparent; border:1px solid var(--border); color:var(--text-muted); width:32px; height:32px; border-radius:6px; font-size:1rem; cursor:pointer;">✕</button>
            </div>
            <div style="padding:16px 20px; flex:1; overflow-y:auto; display:flex; flex-direction:column; gap:12px;">
                <textarea id="trip-notes-textarea" oninput="handleNotesInput()" placeholder="Write your personal packing notes, ferry confirmation codes, tire pressure logs, or stage adjustments here..." style="width:100%; min-height:340px; flex:1; background:var(--bg-dark); color:var(--text-main); border:1px solid var(--border); border-radius:8px; padding:14px; font-family:monospace; font-size:0.86rem; line-height:1.5; resize:vertical;"></textarea>
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                    <div style="display:flex; gap:8px;">
                        <button type="button" onclick="exportNotesFile()" class="theme-toggle-btn">⬇️ Export .txt</button>
                        <button type="button" onclick="resetDefaultNotes()" class="theme-toggle-btn" style="border-color:var(--text-muted); color:var(--text-muted);">🔄 Load Default Notes</button>
                    </div>
                    <button type="button" onclick="closeNotesModal()" class="dl-btn" style="padding:7px 18px;">Done</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Embedded Expedition 51 Data
        const tracksData = {json.dumps(tracks_data, ensure_ascii=False)};
        const gravelData = {json.dumps(gravel_data, ensure_ascii=False)};
        const poisData = {json.dumps(pois_data, ensure_ascii=False)};
        const ganttDaysData = {json.dumps(gantt_days_data, ensure_ascii=False)};
        const defaultChecklistData = {json.dumps(checklist_data, ensure_ascii=False)};

        // Theme Management (Daylight Default + Campfire Dark)
        var currentGanttDay = 1;
        const ganttTypeStyles = {{
            "ride":    {{ bg: "#0284c7", icon: "🏍️", label: "In Saddle" }},
            "meal":    {{ bg: "#d97706", icon: "🍽️", label: "Meal Stop" }},
            "fuel":    {{ bg: "#dc2626", icon: "⛽", label: "Fuel & Rest" }},
            "sight":   {{ bg: "#7c3aed", icon: "🏛️", label: "Attraction / Hike" }},
            "ferry":   {{ bg: "#0891b2", icon: "⛴️", label: "Ferry Crossing" }},
            "lodging": {{ bg: "#059669", icon: "🏕️", label: "Lodging / Camp" }},
            "wake":    {{ bg: "#475569", icon: "⏰", label: "Wake & Prep" }}
        }};

        function applyTheme(theme) {{
            if (theme === 'dark') {{
                document.documentElement.setAttribute('data-theme', 'dark');
                document.getElementById('theme-icon').textContent = '☀️';
                document.getElementById('theme-label').textContent = 'Light Mode';
            }} else {{
                document.documentElement.removeAttribute('data-theme');
                document.getElementById('theme-icon').textContent = '🌙';
                document.getElementById('theme-label').textContent = 'Dark Mode';
            }}
            localStorage.setItem('exp51_theme', theme);
            if (typeof renderGanttActiveDayContent === 'function') {{
                renderGanttActiveDayContent(currentGanttDay);
            }}
        }}

        function toggleTheme() {{
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            applyTheme(isDark ? 'light' : 'dark');
        }}

        const savedTheme = localStorage.getItem('exp51_theme') || 'light';
        applyTheme(savedTheme);

        // Initialize Map with OpenStreetMap Standard Road Map as Default
        const map = L.map('map', {{
            center: [49.8, -64.5],
            zoom: 5,
            zoomControl: true
        }});

        const osmRoadLayer = L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            maxZoom: 19,
            attribution: '&copy; OpenStreetMap contributors'
        }});

        const topoLayer = L.tileLayer('https://{{s}}.tile.opentopomap.org/{{z}}/{{x}}/{{y}}.png', {{
            maxZoom: 17,
            attribution: 'Map data: &copy; OpenStreetMap contributors, SRTM | Map style: &copy; OpenTopoMap'
        }});

        const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
            maxZoom: 18,
            attribution: 'Tiles &copy; Esri'
        }});

        osmRoadLayer.addTo(map);

        L.control.layers({{
            "🗺️ OpenStreetMap (Default)": osmRoadLayer,
            "🏔️ Topographic Terrain": topoLayer,
            "🛰️ Satellite Imagery": satelliteLayer
        }}, null, {{ position: 'topleft' }}).addTo(map);

        // Render 18 Daily Road-Snapped Tracks (coords in exp51_data.json are [lat, lon])
        const trackLayers = {{}};
        const allTrackGroup = L.featureGroup().addTo(map);

        tracksData.forEach(trk => {{
            const poly = L.polyline(trk.coords, {{
                color: trk.color,
                weight: 4.5,
                opacity: 0.88
            }}).addTo(allTrackGroup);

            poly.bindTooltip(`<strong>Day ${{trk.day}}: ${{trk.name}}</strong><br>${{trk.dist_km}} km • ~${{trk.duration_hr}} hrs`, {{
                sticky: true
            }});

            poly.on('click', () => {{
                focusDay(trk.day);
            }});

            trackLayers[trk.day] = poly;
        }});

        // Permanently Mark Unpaved QC-389 Gravel Segments on Map (Visual Hashed Lines Only)
        const gravelGroup = L.featureGroup().addTo(map);
        gravelData.forEach((g) => {{
            // High-contrast dark amber casing so unpaved segments stand out at any zoom
            L.polyline(g.coords, {{
                color: '#78350F',
                weight: 9,
                opacity: 0.55
            }}).addTo(gravelGroup);

            const gPoly = L.polyline(g.coords, {{
                color: '#F59E0B',
                weight: 5.5,
                opacity: 1.0,
                dashArray: '8, 8'
            }}).addTo(gravelGroup);

            gPoly.bindTooltip(`<strong>⚠️ ${{g.name}}</strong><br>Unpaved Graded Gravel • Maintain 70–80 km/h • Daylight Riding Only`, {{
                sticky: true
            }});
        }});

        // Render 452 Curated POIs with Contextual Photo Cards, Hours & Admission
        const poiMarkers = [];
        const poiLayerGroup = L.layerGroup().addTo(map);

        function getCategoryStyle(p) {{
            const typeMap = {{
                'hotel-primary':   {{ color: '#10B981', radius: 8, label: '🏕️ Primary Lodging / Camp' }},
                'hotel-secondary': {{ color: '#F59E0B', radius: 7, label: '⛺ Backup Lodging / Camp' }},
                'fuel':            {{ color: '#EF4444', radius: 5.5, label: '⛽ Verified Fuel Station' }},
                'food':            {{ color: '#F97316', radius: 6, label: '🍽️ Food' }},
                'coffee':          {{ color: '#B45309', radius: 5.5, label: '☕ Coffee Stop' }},
                'lighthouse':      {{ color: '#EC4899', radius: 6.5, label: '🚨 Historic Lighthouse' }},
                'attraction':      {{ color: '#8B5CF6', radius: 7, label: '🏛️ Must-See Attraction' }},
                'park':            {{ color: '#22C55E', radius: 7, label: '🌲 National / Prov. Park' }},
                'sight':           {{ color: '#EAB308', radius: 6.5, label: '📸 Scenic Viewpoint' }},
                'hike':            {{ color: '#14B8A6', radius: 6.5, label: '🥾 Short Trail / Hike' }},
                'ferry':           {{ color: '#06B6D4', radius: 8, label: '⛴️ Ferry / Major Bridge' }},
                'hazard':          {{ color: '#E11D48', radius: 6, label: '⚠️ Road / Rail Marker' }},
                'pullout':         {{ color: '#64748B', radius: 4.5, label: '🅿️ QC-389 Emergency Pullout' }}
            }};
            return typeMap[p.type] || {{ color: p.color || '#38bdf8', radius: 6, label: p.category || 'Expedition POI' }};
        }}

        poisData.forEach(p => {{
            const st = getCategoryStyle(p);
            const marker = L.circleMarker([p.lat, p.lon], {{
                radius: st.radius,
                fillColor: st.color,
                color: '#ffffff',
                weight: 1.8,
                opacity: 1,
                fillOpacity: 0.92
            }});

            const photoHtml = p.photo
                ? `<div class="poi-popup-photo-wrap">
                       <img src="${{p.photo}}" alt="${{p.name.replace(/"/g, '&quot;')}}" class="poi-popup-photo" loading="lazy" onerror="this.parentElement.style.display='none';" />
                   </div>`
                : '';

            let octaneHtml = '';
            if (p.type === 'fuel' && p.octane) {{
                if (p.octane === 'YES') {{
                    octaneHtml = `<div style="font-size:0.74rem; font-weight:700; background:rgba(5,150,105,0.14); color:var(--accent-green); padding:4px 8px; border-radius:4px; margin-bottom:6px;">⛽ 91 Octane: Available (87 &amp; 91 AKI)</div>`;
                }} else if (p.octane === 'NO') {{
                    octaneHtml = `<div style="font-size:0.74rem; font-weight:700; background:rgba(217,119,6,0.14); color:var(--accent-orange); padding:4px 8px; border-radius:4px; margin-bottom:6px;">⚠️ 87 Regular Only — Dose Lucas Oil MMT</div>`;
                }} else if (p.octane === 'TRANSFER') {{
                    octaneHtml = `<div style="font-size:0.74rem; font-weight:700; background:rgba(2,132,199,0.14); color:var(--accent-blue); padding:4px 8px; border-radius:4px; margin-bottom:6px;">🛢️ 5L Bladder Transfer Stop (No Pump)</div>`;
                }} else {{
                    octaneHtml = `<div style="font-size:0.74rem; font-weight:700; background:rgba(5,150,105,0.14); color:var(--accent-green); padding:4px 8px; border-radius:4px; margin-bottom:6px;">⛽ Octane: ${{p.octane}}</div>`;
                }}
            }}

            const costBadge = (p.cost && p.cost !== 'Free' && p.cost !== '$')
                ? `<span style="font-size:0.70rem; font-weight:700; color:var(--accent-green); background:rgba(5,150,105,0.12); padding:2px 6px; border-radius:4px;">${{p.cost}}</span>`
                : '';

            const hoursHtml = p.hours
                ? `<div style="font-size:0.73rem; color:var(--text-main); line-height:1.35;"><strong>🕒 Hours:</strong> ${{p.hours}}</div>`
                : '';

            const hasPaidAdmission = p.admission && !/^free/i.test(p.admission.trim());
            const admissionHtml = p.admission
                ? `<div style="font-size:0.73rem; color:${{hasPaidAdmission ? 'var(--accent-orange)' : 'var(--text-muted)'}}; font-weight:${{hasPaidAdmission ? '700' : '600'}}; line-height:1.35; margin-top:2px;"><strong>🎟️ Admission:</strong> ${{p.admission}}</div>`
                : '';

            const hoursAdmissionBox = (hoursHtml || admissionHtml)
                ? `<div style="background:var(--bg-subtle); border:1px solid var(--border); border-left:3px solid ${{hasPaidAdmission ? 'var(--accent-orange)' : st.color}}; border-radius:6px; padding:5px 8px; margin-bottom:7px;">
                       ${{hoursHtml}}
                       ${{admissionHtml}}
                   </div>`
                : '';

            const gmapsSearch = `https://www.google.com/maps/search/?api=1&query=${{encodeURIComponent(p.name + ' ' + p.lat + ',' + p.lon)}}`;
            const webLink = p.url ? `<a href="${{p.url}}" target="_blank" class="poi-popup-link" style="margin-right:10px;">🌐 Official Website ↗</a>` : '';

            const popupHtml = `
                <div class="poi-popup-card">
                    ${{photoHtml}}
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:3px;">
                        <div class="poi-popup-type" style="color:${{st.color}}; margin-bottom:0;">${{st.label}} • ${{p.day}}</div>
                        ${{costBadge}}
                    </div>
                    <div class="poi-popup-title">${{p.name}}</div>
                    ${{octaneHtml}}
                    ${{hoursAdmissionBox}}
                    <div class="poi-popup-desc">${{p.desc || ''}}</div>
                    <div style="display:flex; flex-wrap:wrap; gap:6px; align-items:center;">
                        ${{webLink}}
                        <a href="${{gmapsSearch}}" target="_blank" class="poi-popup-link">📍 Open in Google Maps ↗</a>
                    </div>
                </div>
            `;

            marker.bindPopup(popupHtml, {{
                maxWidth: 300,
                autoPanPaddingTopLeft: window.innerWidth > 768 ? [265, 130] : [16, 110],
                autoPanPaddingBottomRight: [20, 30]
            }});
            marker.poiData = p;
            poiMarkers.push(marker);
        }});

        map.fitBounds(allTrackGroup.getBounds().pad(0.06));

        // Toggleable Filter POIs by Category (True On/Off Toggle for "All POIs" & Individual Categories)
        let allPoisActive = true;
        const activeCategories = new Set();
        let activeFocusedDay = null;

        function syncFilterToolbarButtons() {{
            document.querySelectorAll('#poi-filter-toolbar .filter-btn').forEach(b => {{
                const cat = b.getAttribute('data-cat');
                if (cat === 'all') {{
                    b.classList.toggle('active', allPoisActive);
                }} else {{
                    b.classList.toggle('active', !allPoisActive && activeCategories.has(cat));
                }}
            }});
        }}

        function filterPOIs(category, btnEl) {{
            if (category === 'all') {{
                // Toggle "All" ON or OFF
                allPoisActive = !allPoisActive;
                activeCategories.clear();
            }} else {{
                if (allPoisActive) {{
                    // Switching from "All" to major category toggle mode
                    allPoisActive = false;
                    activeCategories.clear();
                    activeCategories.add(category);
                }} else {{
                    // Toggle this specific major category ON or OFF
                    if (activeCategories.has(category)) {{
                        activeCategories.delete(category);
                    }} else {{
                        activeCategories.add(category);
                    }}
                }}
                if (activeCategories.has(category) && category === 'qc389' && trackLayers[3]) {{
                    map.fitBounds(trackLayers[3].getBounds().pad(0.12));
                }}
            }}
            syncFilterToolbarButtons();
            updateVisiblePOIs();
        }}

        function updateVisiblePOIs() {{
            poiLayerGroup.clearLayers();
            if (!allPoisActive && activeCategories.size === 0) {{
                // All POIs toggled OFF
                return;
            }}
            const sightsTypes = new Set(['lighthouse', 'attraction', 'sight', 'hike', 'park']);
            poiMarkers.forEach(m => {{
                const p = m.poiData;
                let catMatch = false;
                if (allPoisActive) {{
                    // Smart decluttering: hide dense QC-389 emergency pullouts & rail hazards in full-loop zoom 5 view,
                    // and reveal them automatically when Day 3 is focused!
                    if ((p.type === 'pullout' || p.type === 'hazard') && activeFocusedDay !== 3) {{
                        catMatch = false;
                    }} else {{
                        catMatch = true;
                    }}
                }} else {{
                    if (activeCategories.has(p.type)) {{
                        catMatch = true;
                    }} else if (activeCategories.has('lodging') && (p.type === 'hotel-primary' || p.type === 'hotel-secondary')) {{
                        catMatch = true;
                    }} else if (activeCategories.has('sights') && sightsTypes.has(p.type)) {{
                        catMatch = true;
                    }} else if (activeCategories.has('qc389') && (p.type === 'hazard' || p.type === 'pullout')) {{
                        catMatch = true;
                    }}
                }}

                const dayMatch = (activeFocusedDay === null) || (p.day === `Day ${{activeFocusedDay}}`);
                if (catMatch && dayMatch) {{
                    m.addTo(poiLayerGroup);
                }}
            }});
        }}

        // Populate initial visible POIs
        updateVisiblePOIs();

        // Collapsible Day Cards & Focus Stage Logic
        function updateCollapseAllButtonState() {{
            const btn = document.getElementById('btn-collapse-all');
            if (!btn) return;
            const allCards = Array.from(document.querySelectorAll('.day-card'));
            const allCollapsed = allCards.length > 0 && allCards.every(c => c.classList.contains('collapsed'));
            btn.textContent = allCollapsed ? '↕️ Expand All' : '↕️ Collapse All';
        }}

        function toggleDayCard(dayNum, forceCollapse) {{
            const card = document.getElementById(`day-card-${{dayNum}}`);
            const chev = document.getElementById(`day-chevron-${{dayNum}}`);
            if (!card) return;
            const shouldCollapse = (typeof forceCollapse === 'boolean')
                ? forceCollapse
                : !card.classList.contains('collapsed');
            card.classList.toggle('collapsed', shouldCollapse);
            if (chev) chev.textContent = shouldCollapse ? '▸' : '▾';
            updateCollapseAllButtonState();
        }}

        function toggleAllDayCards() {{
            const allCards = Array.from(document.querySelectorAll('.day-card'));
            const allCollapsed = allCards.length > 0 && allCards.every(c => c.classList.contains('collapsed'));
            const targetCollapse = !allCollapsed;
            for (let d = 1; d <= 18; d++) {{
                toggleDayCard(d, targetCollapse);
            }}
        }}

        function handleDayHeaderClick(evt, dayNum) {{
            const card = document.getElementById(`day-card-${{dayNum}}`);
            if (!card) return;
            // If clicking the header of an already active & expanded card, collapse it cleanly
            if (activeFocusedDay === dayNum && !card.classList.contains('collapsed')) {{
                evt.stopPropagation();
                toggleDayCard(dayNum, true);
            }}
        }}

        // Resizable Split Divider Gutter (Map <-> Itinerary)
        (function initResizerGutter() {{
            const gutter = document.getElementById('resizer-gutter');
            const container = document.getElementById('sec-top');
            const sidebar = document.getElementById('sec-itinerary');
            if (!gutter || !container || !sidebar) return;

            const STORAGE_KEY = 'exp51_sidebar_width_px';
            const DEFAULT_WIDTH = 540;

            function applySidebarWidth(w) {{
                if (window.innerWidth <= 1024) {{
                    sidebar.style.flex = '';
                    sidebar.style.width = '';
                    return;
                }}
                const rect = container.getBoundingClientRect();
                const maxW = Math.max(160, rect.width - 140);
                const clamped = Math.max(160, Math.min(maxW, w));
                sidebar.style.flex = `0 0 ${{clamped}}px`;
                sidebar.style.width = `${{clamped}}px`;
            }}

            const savedW = parseInt(localStorage.getItem(STORAGE_KEY), 10);
            if (!isNaN(savedW) && savedW >= 160 && window.innerWidth > 1024) {{
                applySidebarWidth(savedW);
                setTimeout(() => map.invalidateSize({{ pan: false }}), 60);
            }}

            let isDragging = false;
            let rafPending = false;

            function onMove(clientX) {{
                if (!isDragging) return;
                const rect = container.getBoundingClientRect();
                const newSidebarWidth = rect.right - clientX;
                applySidebarWidth(newSidebarWidth);
                if (!rafPending) {{
                    rafPending = true;
                    requestAnimationFrame(() => {{
                        map.invalidateSize({{ pan: false }});
                        rafPending = false;
                    }});
                }}
            }}

            function stopDrag() {{
                if (!isDragging) return;
                isDragging = false;
                gutter.classList.remove('dragging');
                document.body.classList.remove('is-resizing');
                const currentW = Math.round(sidebar.getBoundingClientRect().width);
                if (currentW >= 160 && window.innerWidth > 1024) {{
                    localStorage.setItem(STORAGE_KEY, String(currentW));
                }}
                map.invalidateSize({{ pan: false }});
            }}

            gutter.addEventListener('mousedown', (e) => {{
                if (window.innerWidth <= 1024) return;
                e.preventDefault();
                isDragging = true;
                gutter.classList.add('dragging');
                document.body.classList.add('is-resizing');
            }});

            window.addEventListener('mousemove', (e) => {{
                if (isDragging) onMove(e.clientX);
            }});

            window.addEventListener('mouseup', stopDrag);

            gutter.addEventListener('touchstart', (e) => {{
                if (window.innerWidth <= 1024 || !e.touches.length) return;
                isDragging = true;
                gutter.classList.add('dragging');
                document.body.classList.add('is-resizing');
            }}, {{ passive: true }});

            window.addEventListener('touchmove', (e) => {{
                if (isDragging && e.touches.length) onMove(e.touches[0].clientX);
            }}, {{ passive: true }});

            window.addEventListener('touchend', stopDrag);

            gutter.addEventListener('dblclick', () => {{
                if (window.innerWidth <= 1024) return;
                localStorage.removeItem(STORAGE_KEY);
                applySidebarWidth(DEFAULT_WIDTH);
                map.invalidateSize({{ pan: false }});
            }});

            window.addEventListener('resize', () => {{
                if (window.innerWidth <= 1024) {{
                    sidebar.style.flex = '';
                    sidebar.style.width = '';
                }} else {{
                    const sw = parseInt(localStorage.getItem(STORAGE_KEY), 10);
                    if (!isNaN(sw) && sw >= 160) applySidebarWidth(sw);
                }}
                map.invalidateSize({{ pan: false }});
            }});
        }})();

        // Focus Specific Day Stage
        function focusDay(dayNum) {{
            activeFocusedDay = dayNum;

            document.querySelectorAll('.day-card').forEach(c => c.classList.remove('active'));
            const activeCard = document.getElementById(`day-card-${{dayNum}}`);
            if (activeCard) {{
                activeCard.classList.add('active');
                if (activeCard.classList.contains('collapsed')) {{
                    toggleDayCard(dayNum, false);
                }}
            }}

            document.querySelectorAll('.day-jump-pill').forEach(p => p.classList.remove('active'));
            const activePill = document.getElementById(`jump-pill-${{dayNum}}`);
            if (activePill) activePill.classList.add('active');

            Object.keys(trackLayers).forEach(d => {{
                const layer = trackLayers[d];
                if (parseInt(d) === dayNum) {{
                    layer.setStyle({{ weight: 6.5, opacity: 1.0 }});
                    layer.bringToFront();
                    map.fitBounds(layer.getBounds().pad(0.18));
                }} else {{
                    layer.setStyle({{ weight: 3, opacity: 0.25 }});
                }}
            }});

            updateVisiblePOIs();
            selectGanttDay(dayNum, false);
        }}

        function jumpToDayCard(dayNum) {{
            focusDay(dayNum);
            const card = document.getElementById(`day-card-${{dayNum}}`);
            if (card) {{
                card.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}
        }}

        function resetMapView() {{
            activeFocusedDay = null;
            document.querySelectorAll('.day-card').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.day-jump-pill').forEach(p => p.classList.remove('active'));
            Object.keys(trackLayers).forEach(d => {{
                trackLayers[d].setStyle({{ weight: 4.5, opacity: 0.88 }});
            }});
            map.fitBounds(allTrackGroup.getBounds().pad(0.06));
            updateVisiblePOIs();
        }}

        // Interactive Gantt Chart Functions (Rockies Dual-View Parity)

        function switchGanttView(mode) {{
            const dayView = document.getElementById('gantt-day-view');
            const gridView = document.getElementById('gantt-grid-view');
            const btnDay = document.getElementById('btn-gantt-view-day');
            const btnGrid = document.getElementById('btn-gantt-view-grid');
            const hint = document.getElementById('gantt-swipe-hint');

            if (mode === 'grid') {{
                dayView.style.display = 'none';
                gridView.style.display = 'block';
                hint.style.display = 'inline-block';
                btnGrid.style.background = 'var(--accent-blue, #0284c7)';
                btnGrid.style.color = '#ffffff';
                btnDay.style.background = 'transparent';
                btnDay.style.color = 'var(--text-muted, #64748b)';
            }} else {{
                dayView.style.display = 'block';
                gridView.style.display = 'none';
                hint.style.display = 'none';
                btnDay.style.background = 'var(--accent-blue, #0284c7)';
                btnDay.style.color = '#ffffff';
                btnGrid.style.background = 'transparent';
                btnGrid.style.color = 'var(--text-muted, #64748b)';
            }}
        }}

        function renderGanttActiveDayContent(dayNum) {{
            const d = ganttDaysData.find(x => x.day === dayNum) || ganttDaysData[0];
            if (!d) return;
            const container = document.getElementById('gantt-active-day-content');
            if (!container) return;

            let blocksHtml = '';
            d.blocks.forEach(b => {{
                const st = ganttTypeStyles[b.type] || ganttTypeStyles['ride'];
                const durMin = b.end_m - b.start_m;
                const durStr = durMin >= 60 ? `${{Math.floor(durMin/60)}}h ${{durMin%60}}m` : `${{durMin}}m`;
                blocksHtml += `
                    <div style="display:flex; align-items:flex-start; gap:12px; padding:10px 12px; background:var(--gantt-bg, #ffffff); border:1px solid var(--gantt-border, #e2e8f0); border-left:4px solid ${{st.bg}}; border-radius:8px;">
                        <div style="min-width:115px; font-family:monospace; font-size:0.78rem; font-weight:700; color:var(--accent-blue, #0284c7);">
                            <div>${{b.start_str}} – ${{b.end_str}}</div>
                            <div style="font-size:0.70rem; color:var(--text-muted, #64748b);">${{durStr}} • ${{st.label}}</div>
                        </div>
                        <div style="flex:1;">
                            <div style="font-size:0.86rem; font-weight:800; color:var(--text-main, #0f172a); margin-bottom:2px;">${{st.icon}} ${{b.title}}</div>
                            <div style="font-size:0.78rem; color:var(--text-card, #334155); line-height:1.38;">${{b.details}}</div>
                        </div>
                    </div>
                `;
            }});

            container.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px; padding-bottom:10px; border-bottom:1px solid var(--gantt-border, #e2e8f0);">
                    <div>
                        <div style="font-size:1.02rem; font-weight:800; color:var(--text-main, #0f172a);">Day ${{d.day}}: ${{d.title}}</div>
                        <div style="font-size:0.78rem; color:var(--text-muted, #64748b);">${{d.date}} • 🏕️ ${{d.hotel}}</div>
                    </div>
                    <div style="display:flex; gap:8px; align-items:center;">
                        <span style="background:rgba(2,132,199,0.12); color:var(--accent-blue, #0284c7); border:1px solid rgba(2,132,199,0.3); padding:4px 10px; border-radius:6px; font-size:0.78rem; font-weight:800;">📏 ${{Number(d.dist).toFixed(1)}} km</span>
                        <button type="button" onclick="focusDay(${{d.day}});" style="background:var(--accent-blue, #0284c7); color:#ffffff; border:none; padding:5px 10px; border-radius:6px; font-size:0.75rem; font-weight:700; cursor:pointer;">🗺️ View on Map</button>
                    </div>
                </div>
                <div style="display:flex; flex-direction:column; gap:8px;">
                    ${{blocksHtml}}
                </div>
            `;
        }}

        function selectGanttDay(dayNum, scrollChip=true) {{
            currentGanttDay = dayNum;
            document.querySelectorAll('.gantt-day-chip').forEach(btn => {{
                btn.style.background = 'var(--gantt-subtle-bg, #f8fafc)';
                btn.style.borderColor = 'var(--gantt-border, #e2e8f0)';
                btn.style.color = 'var(--text-muted, #64748b)';
                btn.classList.remove('active');
            }});
            const activeChip = document.getElementById(`gantt-day-chip-${{dayNum}}`);
            if (activeChip) {{
                activeChip.style.background = 'var(--accent-blue, #0284c7)';
                activeChip.style.borderColor = 'var(--accent-blue, #0284c7)';
                activeChip.style.color = '#ffffff';
                activeChip.classList.add('active');
                if (scrollChip) activeChip.scrollIntoView({{ behavior: 'smooth', inline: 'center', block: 'nearest' }});
            }}
            const ind = document.getElementById('gantt-day-indicator');
            if (ind) ind.textContent = `Day ${{dayNum}} of 18`;
            renderGanttActiveDayContent(dayNum);
        }}

        function stepGanttDay(delta) {{
            let next = currentGanttDay + delta;
            if (next < 1) next = 18;
            if (next > 18) next = 1;
            selectGanttDay(next);
        }}

        function inspectGanttBlock(timeStr, titleStr, detailsStr, iconStr) {{
            const card = document.getElementById('gantt-block-inspect-card');
            if (!card) return;
            document.getElementById('inspect-icon').textContent = iconStr;
            document.getElementById('inspect-time').textContent = timeStr;
            document.getElementById('inspect-title').textContent = titleStr;
            document.getElementById('inspect-details').textContent = detailsStr;
            card.style.display = 'block';
        }}

        renderGanttActiveDayContent(1);

        // Mobile Bottom Navigation Handler
        function mobileNav(target, btnEl) {{
            document.querySelectorAll('.mob-nav-btn').forEach(b => b.classList.remove('active'));
            if (btnEl) btnEl.classList.add('active');

            const elMap = document.getElementById('sec-map');
            const elItin = document.getElementById('sec-itinerary');
            const elGantt = document.getElementById('sec-gantt');
            const elChk = document.getElementById('sec-checklist');
            const elDl = document.getElementById('sec-budget');

            if (target === 'map' && elMap) {{
                elMap.scrollIntoView({{ behavior: 'smooth' }});
                setTimeout(() => map.invalidateSize(), 250);
            }} else if (target === 'itinerary' && elItin) {{
                elItin.scrollIntoView({{ behavior: 'smooth' }});
            }} else if (target === 'gantt' && elGantt) {{
                elGantt.scrollIntoView({{ behavior: 'smooth' }});
            }} else if (target === 'checklist' && elChk) {{
                elChk.scrollIntoView({{ behavior: 'smooth' }});
            }} else if (target === 'downloads' && elDl) {{
                elDl.scrollIntoView({{ behavior: 'smooth' }});
            }}
        }}

        // Live Weather Fetcher (Open-Meteo API for each stage's primary destination)
        async function fetchLiveWeather() {{
            const primaryHotels = poisData.filter(p => p.type === 'hotel-primary');
            for (let dayNum = 1; dayNum <= 18; dayNum++) {{
                const badge = document.getElementById(`live-weather-${{dayNum}}`);
                if (!badge) continue;
                const hp = primaryHotels.find(p => p.day === `Day ${{dayNum}}`) || primaryHotels[0];
                if (!hp) continue;
                try {{
                    const url = `https://api.open-meteo.com/v1/forecast?latitude=${{hp.lat}}&longitude=${{hp.lon}}&current_weather=true`;
                    const res = await fetch(url);
                    if (!res.ok) throw new Error('Weather HTTP error');
                    const data = await res.json();
                    if (data && data.current_weather) {{
                        const temp = Math.round(data.current_weather.temperature);
                        const wind = Math.round(data.current_weather.windspeed);
                        badge.textContent = `🌡️ Live Now: ${{temp}}°C • 💨 ${{wind}} km/h`;
                    }}
                }} catch (e) {{
                    badge.textContent = `🌡️ Seasonal Metric Target`;
                }}
            }}
        }}
        fetchLiveWeather();

        // Trip Notes Modal & LocalStorage Persistence
        const NOTES_STORAGE_KEY = 'exp51_master_trip_notes_v1';
        const DEFAULT_NOTES_TEXT = `=== 2027 EAST COAST & LABRADOR MOTO EXPEDITION (EXPEDITION 51) ===
Dates: June 16 – July 3, 2027 (18 Days • 8,243.4 km Pure Metric)
Fleet: 2025 Honda Africa Twin Adv Sports ES (Jamie) + 2026 Ducati Multistrada V2S (Rosie)

[CRITICAL RESERVATION CHECKLIST]
[ ] Jan 2027: Book Marine Atlantic Overnight Ferry (Day 10: Port aux Basques -> North Sydney + 2-Berth Cabin)
[ ] Jan 2027: Book Labrador Marine MV Qajaq W Ferry (Day 6: Blanc-Sablon -> St. Barbe)
[ ] Jan 2027: Reserve Parks Canada Campgrounds (Gros Morne, Cape Breton Highlands, PEI Cavendish, Fundy NP)
[ ] Feb 2027: Confirm Snorri Cabins / Valhalla Lodge (Days 6 & 7: L'Anse aux Meadows / Hay Cove)

[REMOTE FUEL & OCTANE PROTOCOL]
- Carry 1x 5L Giant Loop Armadillo fuel bladder per motorcycle (mandatory on QC-389 & Trans-Labrador Hwy)
- Carry 1x 946ml bottle of Lucas Oil Octane Booster (MMT) for Ducati Multistrada V2S (dose 6ml/L at 87-only pumps)
- Pack 4 heavy-duty cam-buckle tie-down straps per bike for ocean ferry decks

[STAGE NOTES & LOGS]
- `;

        function openNotesModal() {{
            const overlay = document.getElementById('notes-modal-overlay');
            const ta = document.getElementById('trip-notes-textarea');
            const saved = localStorage.getItem(NOTES_STORAGE_KEY);
            ta.value = (saved !== null) ? saved : DEFAULT_NOTES_TEXT;
            overlay.style.display = 'flex';
        }}

        function closeNotesModal() {{
            document.getElementById('notes-modal-overlay').style.display = 'none';
        }}

        function handleNotesInput() {{
            const ta = document.getElementById('trip-notes-textarea');
            localStorage.setItem(NOTES_STORAGE_KEY, ta.value);
            const status = document.getElementById('notes-sync-status');
            status.textContent = '✓ Saved at ' + new Date().toLocaleTimeString();
        }}

        function resetDefaultNotes() {{
            const ta = document.getElementById('trip-notes-textarea');
            ta.value = DEFAULT_NOTES_TEXT;
            localStorage.setItem(NOTES_STORAGE_KEY, ta.value);
        }}

        function exportNotesFile() {{
            const ta = document.getElementById('trip-notes-textarea');
            const blob = new Blob([ta.value], {{ type: 'text/plain;charset=utf-8' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'expedition_51_trip_notes.txt';
            a.click();
            URL.revokeObjectURL(url);
        }}

        // =========================================================================
        // FAMILY & FRIENDS CLOUD LIVE TRACKER ENGINE (Cloud Feed + Rider Broadcast)
        // =========================================================================
        const LIVE_CLOUD_TOPIC = 'exp51_live_cloud_feed_2027_prod';
        const LIVE_HISTORY_KEY = 'exp51_live_feed_history_v1';
        const LIVE_QUEUE_KEY   = 'exp51_live_offline_queue_v1';
        const RIDER_PIN_CODE   = '2027';
        const TOTAL_EXP_KM     = 8243.4;

        function haversineKm(lat1, lon1, lat2, lon2) {{
            const R = 6371.0;
            const dLat = (lat2 - lat1) * Math.PI / 180.0;
            const dLon = (lon2 - lon1) * Math.PI / 180.0;
            const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                      Math.cos(lat1 * Math.PI / 180.0) * Math.cos(lat2 * Math.PI / 180.0) *
                      Math.sin(dLon / 2) * Math.sin(dLon / 2);
            return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        }}

        // Build Route Spine across all 18 road-snapped stages for instant km snapping
        const routeSpine = [];
        const stageCumBounds = {{}};
        (function buildRouteSpine() {{
            let cumKm = 0.0;
            tracksData.forEach(trk => {{
                const startKm = cumKm;
                const pts = trk.coords || [];
                let rawLen = 0.0;
                for (let i = 1; i < pts.length; i++) {{
                    rawLen += haversineKm(pts[i - 1][0], pts[i - 1][1], pts[i][0], pts[i][1]);
                }}
                const targetLen = Number(trk.dist_km) || rawLen || 1.0;
                const scale = rawLen > 0 ? (targetLen / rawLen) : 1.0;
                const cleanStageName = (trk.name || '').replace(/^Stage\\s+\\d+:\\s*/i, '');

                let stageCum = 0.0;
                for (let i = 0; i < pts.length; i++) {{
                    if (i > 0) {{
                        const seg = haversineKm(pts[i - 1][0], pts[i - 1][1], pts[i][0], pts[i][1]) * scale;
                        stageCum += seg;
                        cumKm += seg;
                    }}
                    routeSpine.push({{
                        lat: pts[i][0],
                        lon: pts[i][1],
                        day: trk.day,
                        stageName: cleanStageName,
                        stageDistKm: targetLen,
                        stageCumKm: stageCum,
                        cumKm: cumKm
                    }});
                }}
                stageCumBounds[trk.day] = {{ startKm, endKm: cumKm, distKm: targetLen, name: cleanStageName }};
            }});
        }})();

        // Project Fuel POIs onto the route spine for exact "Next Fuel Ahead" calculation
        const fuelSpineList = poisData.filter(p => p.type === 'fuel').map(fp => {{
            const dayNum = parseInt((fp.day || 'Day 1').replace('Day ', '')) || 1;
            let bestIdx = 0;
            let bestDist = Infinity;
            for (let i = 0; i < routeSpine.length; i++) {{
                if (routeSpine[i].day !== dayNum) continue;
                const d = haversineKm(fp.lat, fp.lon, routeSpine[i].lat, routeSpine[i].lon);
                if (d < bestDist) {{
                    bestDist = d;
                    bestIdx = i;
                }}
            }}
            return {{
                name: fp.name,
                day: dayNum,
                octane: fp.octane || 'YES',
                cumKm: routeSpine[bestIdx] ? routeSpine[bestIdx].cumKm : 0
            }};
        }}).sort((a, b) => a.cumKm - b.cumKm);

        function snapToRoute(lat, lon, preferredDay) {{
            if (!routeSpine.length) return null;
            let bestIdx = 0;
            let bestDist = Infinity;
            for (let i = 0; i < routeSpine.length; i++) {{
                if (preferredDay && routeSpine[i].day !== preferredDay) continue;
                const d = haversineKm(lat, lon, routeSpine[i].lat, routeSpine[i].lon);
                if (d < bestDist) {{
                    bestDist = d;
                    bestIdx = i;
                }}
            }}
            // Fallback across all days if preferredDay was not matched
            if (bestDist === Infinity) {{
                for (let i = 0; i < routeSpine.length; i++) {{
                    const d = haversineKm(lat, lon, routeSpine[i].lat, routeSpine[i].lon);
                    if (d < bestDist) {{
                        bestDist = d;
                        bestIdx = i;
                    }}
                }}
            }}
            const pt = routeSpine[bestIdx];
            const cumKm = Math.min(TOTAL_EXP_KM, pt.cumKm);
            const pct = Math.min(100, (cumKm / TOTAL_EXP_KM) * 100);
            const stageRemKm = Math.max(0, pt.stageDistKm - pt.stageCumKm);

            const dayHotels = poisData.filter(p => p.type === 'hotel-primary' && p.day === `Day ${{pt.day}}`);
            const priHotel = dayHotels.length ? dayHotels[dayHotels.length - 1] : null;
            const hotelShort = priHotel ? priHotel.name.split('(')[0].trim() : `Stage ${{pt.day}} Camp/Hotel`;

            const nextFuel = fuelSpineList.find(f => f.cumKm > cumKm + 2.0) || fuelSpineList[fuelSpineList.length - 1];
            const nextFuelKm = nextFuel ? Math.max(0, nextFuel.cumKm - cumKm) : 0;

            const completedCoords = [];
            for (let i = 0; i <= bestIdx; i += 2) {{
                completedCoords.push([routeSpine[i].lat, routeSpine[i].lon]);
            }}
            completedCoords.push([pt.lat, pt.lon]);

            return {{
                lat: pt.lat,
                lon: pt.lon,
                day: pt.day,
                stageName: pt.stageName,
                cumKm: cumKm,
                pct: pct,
                stageRemKm: stageRemKm,
                hotelShort: hotelShort,
                nextFuelName: nextFuel ? nextFuel.name.split('(')[0].trim() : 'Hanmer Arrival',
                nextFuelKm: nextFuelKm,
                nextFuelOctane: nextFuel ? nextFuel.octane : 'YES',
                completedCoords: completedCoords
            }};
        }}

        // Populate Rider Waypoint Selector for quick check-ins
        (function populateRiderLocationSelector() {{
            const sel = document.getElementById('lt-location-select');
            if (!sel) return;
            const keyStops = poisData.filter(p => p.type === 'hotel-primary' || p.type === 'ferry' || p.type === 'attraction');
            keyStops.forEach((p, idx) => {{
                const opt = document.createElement('option');
                opt.value = `${{p.lat}},${{p.lon}},${{(p.day || 'Day 1').replace('Day ', '')}},${{p.name.replace(/"/g, '')}}`;
                opt.textContent = `${{p.day}}: ${{p.name}}`;
                sel.appendChild(opt);
            }});
        }})();

        // Completed Trail Polyline & Dual Pulsing Live Bike Markers (Jamie White/Red & Rosie Green)
        const liveCompletedTrail = L.polyline([], {{
            color: '#0284c7',
            weight: 6.5,
            opacity: 0.95
        }}).addTo(map);

        const liveCheckInLayer = L.layerGroup().addTo(map);

        const ATAS_MOTO_SVG = `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><circle cx="5.5" cy="17.5" r="3.5" fill="#ffffff"/><circle cx="18.5" cy="17.5" r="3.5" fill="#ffffff"/><path d="M14 6h3.5l2 5.5h-5.5l-2.5-5.5z" fill="#dc2626"/><path d="M5.5 14l4.5-5h4.5l2.5 5"/></svg>`;
        const V2S_MOTO_SVG  = `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><circle cx="5.5" cy="17.5" r="3.5" fill="#15803d"/><circle cx="18.5" cy="17.5" r="3.5" fill="#15803d"/><path d="M14 6h3.5l2 5.5h-5.5l-2.5-5.5z" fill="#ffffff"/><path d="M5.5 14l4.5-5h4.5l2.5 5"/></svg>`;

        function normalizeRider(r) {{
            if (r === 'Rosie' || r === 'V2S') return 'Rosie';
            return 'Jamie';
        }}

        function createLiveBikeIcon(callsign, isCoLocated) {{
            const norm = normalizeRider(callsign);
            const isRosie = norm === 'Rosie';
            const coClass = isCoLocated ? (isRosie ? 'co-located-v2s' : 'co-located-atas') : '';
            const v2sClass = isRosie ? 'v2s' : '';
            const svgIcon = isRosie ? V2S_MOTO_SVG : ATAS_MOTO_SVG;
            return L.divIcon({{
                className: '',
                html: `<div class="live-bike-marker-wrap ${{coClass}}"><div class="live-bike-pulse ${{v2sClass}}"></div><div class="live-bike-core ${{v2sClass}}">${{svgIcon}}</div><div class="live-bike-callsign ${{v2sClass}}">${{norm}}</div></div>`,
                iconSize: [38, 44],
                iconAnchor: [19, 19],
                popupAnchor: isCoLocated ? (isRosie ? [23, -18] : [-23, -18]) : [0, -18]
            }});
        }}

        const liveMarkerATAS = L.marker([46.656232, -80.882479], {{
            icon: createLiveBikeIcon('Jamie', true),
            zIndexOffset: 2510
        }}).addTo(map);

        const liveMarkerV2S = L.marker([46.656232, -80.882479], {{
            icon: createLiveBikeIcon('Rosie', true),
            zIndexOffset: 2500
        }}).addTo(map);

        const RIDER_META = {{
            Jamie: {{
                callsign: 'Jamie',
                model: '2025 Honda CRF1100L Africa Twin Adv Sports ES (White & Red)',
                shortModel: '2025 Africa Twin',
                color: '#dc2626'
            }},
            Rosie: {{
                callsign: 'Rosie',
                model: '2026 Ducati Multistrada V2S (Green)',
                shortModel: 'Ducati V2S',
                color: '#16a34a'
            }}
        }};

        let latestATASPacket = null;
        let latestV2SPacket = null;
        let latestLeadPacket = null;
        let selectedRiderCallsign = normalizeRider(localStorage.getItem('exp51_rider_callsign') || 'Jamie');
        let selectedStatusLabel = '🏍️ In Saddle';
        let selectedDefaultNote = 'Riding on stage — all good!';
        let liveGpsWatchId = null;
        let lastAutoBroadcastMs = 0;

        function selectRiderCallsign(callsign) {{
            selectedRiderCallsign = normalizeRider(callsign);
            localStorage.setItem('exp51_rider_callsign', selectedRiderCallsign);
            const btnAtas = document.getElementById('btn-rider-atas');
            const btnV2s  = document.getElementById('btn-rider-v2s');
            if (btnAtas) {{
                const isJamie = selectedRiderCallsign === 'Jamie';
                btnAtas.classList.toggle('active', isJamie);
                btnAtas.style.background = isJamie ? '#ffffff' : 'var(--bg-card)';
                btnAtas.style.color = isJamie ? '#dc2626' : 'var(--text-main)';
                btnAtas.style.borderColor = '#dc2626';
                btnAtas.style.boxShadow = isJamie ? 'inset 0 0 0 1.5px #dc2626' : 'none';
            }}
            if (btnV2s) {{
                const isRosie = selectedRiderCallsign === 'Rosie';
                btnV2s.classList.toggle('active', isRosie);
                btnV2s.style.background = isRosie ? '#16a34a' : 'var(--bg-card)';
                btnV2s.style.color = isRosie ? '#ffffff' : 'var(--text-main)';
                btnV2s.style.borderColor = '#16a34a';
            }}
        }}

        function getStoredFeedHistory() {{
            try {{
                const raw = localStorage.getItem(LIVE_HISTORY_KEY + '_v3');
                if (raw) {{
                    const parsed = JSON.parse(raw);
                    if (Array.isArray(parsed) && parsed.length > 0) {{
                        return parsed.map(p => ({{ ...p, rider: normalizeRider(p.rider) }}));
                    }}
                }}
            }} catch (e) {{}}
            const now = Date.now();
            return [
                {{
                    id: 'init-hanmer-jamie',
                    rider: 'Jamie',
                    ts: now - 3500000,
                    lat: 46.656232,
                    lon: -80.882479,
                    day: 1,
                    speedKmh: 0,
                    altM: 295,
                    status: '🏕️ Checked In • Hanmer Start',
                    note: 'Jamie (2025 Honda Africa Twin ES) prepped at Hanmer Home Base (4671 Dupuis Dr) — 24.8L tank & panniers loaded!'
                }},
                {{
                    id: 'init-hanmer-rosie',
                    rider: 'Rosie',
                    ts: now - 3550000,
                    lat: 46.656232,
                    lon: -80.882479,
                    day: 1,
                    speedKmh: 0,
                    altM: 295,
                    status: '🏕️ Checked In • Hanmer Start',
                    note: 'Rosie (2026 Ducati Multistrada V2S) prepped at Hanmer Home Base — 5L auxiliary bladder & Lucas MMT packed!'
                }}
            ];
        }}

        function saveStoredFeedHistory(list) {{
            try {{
                localStorage.setItem(LIVE_HISTORY_KEY + '_v3', JSON.stringify(list.slice(0, 80)));
            }} catch (e) {{}}
        }}

        function getOfflineQueue() {{
            try {{
                const raw = localStorage.getItem(LIVE_QUEUE_KEY);
                return raw ? JSON.parse(raw) : [];
            }} catch (e) {{
                return [];
            }}
        }}

        function saveOfflineQueue(q) {{
            try {{
                localStorage.setItem(LIVE_QUEUE_KEY, JSON.stringify(q));
            }} catch (e) {{}}
            updateOfflineQueueBadge();
        }}

        function updateOfflineQueueBadge() {{
            const badge = document.getElementById('lt-queue-badge');
            if (!badge) return;
            const q = getOfflineQueue();
            if (q.length === 0) {{
                badge.textContent = '✓ 0 queued';
                badge.style.color = 'var(--text-muted)';
            }} else {{
                badge.textContent = `⏳ ${{q.length}} queued (Tap to sync)`;
                badge.style.color = 'var(--accent-orange)';
            }}
        }}

        function formatRelativeTime(ts) {{
            const diffSec = Math.max(0, Math.floor((Date.now() - ts) / 1000));
            if (diffSec < 45) return 'Just now';
            if (diffSec < 3600) return `${{Math.floor(diffSec / 60)}}m ago`;
            if (diffSec < 86400) return `${{Math.floor(diffSec / 3600)}}h ago`;
            return new Date(ts).toLocaleDateString('en-CA', {{ month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }});
        }}

        function buildBikePopupHtml(callsign, pkt, snap, separationKm) {{
            const norm = normalizeRider(callsign);
            const meta = RIDER_META[norm] || RIDER_META.Jamie;
            const otherRider = norm === 'Jamie' ? 'Rosie' : 'Jamie';
            const sepText = separationKm < 0.5
                ? '🤝 Riding Together with ' + otherRider
                : `📏 ${{separationKm.toFixed(1)}} km from ${{otherRider}}`;
            return `
                <div class="poi-popup-card">
                    <div class="poi-popup-type" style="color:${{meta.color}};">📡 ${{meta.callsign.toUpperCase()}} LIVE TRACKER • DAY ${{snap.day}}</div>
                    <div class="poi-popup-title"><span class="lt-rider-pill ${{norm === 'Rosie' ? 'v2s' : ''}}" style="margin-right:5px; vertical-align:middle;">${{norm}}</span>${{pkt.status}}</div>
                    <div style="font-size:0.71rem; font-weight:700; color:var(--text-muted); margin-bottom:4px;">🏍️ ${{meta.model}}</div>
                    <div class="poi-popup-desc" style="margin-top:2px;">${{pkt.note || ''}}</div>
                    <div style="font-size:0.74rem; color:var(--text-muted); background:var(--bg-subtle); padding:6px 8px; border-radius:6px; border:1px solid var(--border); margin-bottom:6px;">
                        <div><strong>📏 Loop Progress:</strong> ${{snap.cumKm.toFixed(1)}} / 8,243.4 km (${{snap.pct.toFixed(1)}}%)</div>
                        <div><strong>🏕️ To Tonight's Stop:</strong> ${{snap.stageRemKm.toFixed(1)}} km (${{snap.hotelShort}})</div>
                        <div><strong>⛽ Next Fuel:</strong> ${{snap.nextFuelName}} in ${{snap.nextFuelKm.toFixed(1)}} km</div>
                        <div><strong>🏍️ Fleet Status:</strong> ${{sepText}} • ${{Number(pkt.speedKmh) || 0}} km/h</div>
                        <div><strong>🕒 Updated:</strong> ${{formatRelativeTime(pkt.ts)}} (${{pkt.lat.toFixed(4)}}, ${{pkt.lon.toFixed(4)}})</div>
                    </div>
                    <a href="https://www.google.com/maps/search/?api=1&query=${{pkt.lat}},${{pkt.lon}}" target="_blank" class="poi-popup-link">📍 Open ${{norm}} Coordinates in Google Maps ↗</a>
                </div>
            `;
        }}

        function renderLiveTrackerState(historyList) {{
            if (!historyList || !historyList.length) return;
            const sorted = [...historyList].map(x => ({{ ...x, rider: normalizeRider(x.rider) }})).sort((a, b) => b.ts - a.ts);

            const defaultJamie = {{
                id: 'fallback-jamie', rider: 'Jamie', ts: Date.now() - 3600000,
                lat: 46.656232, lon: -80.882479, day: 1, speedKmh: 0, altM: 295,
                status: '🏕️ Hanmer Start', note: '2025 Africa Twin staged at Hanmer Home Base.'
            }};
            const defaultRosie = {{
                id: 'fallback-rosie', rider: 'Rosie', ts: Date.now() - 3600000,
                lat: 46.656232, lon: -80.882479, day: 1, speedKmh: 0, altM: 295,
                status: '🏕️ Hanmer Start', note: 'Ducati V2S staged at Hanmer Home Base.'
            }};

            latestATASPacket = sorted.find(x => x.rider === 'Jamie') || defaultJamie;
            latestV2SPacket  = sorted.find(x => x.rider === 'Rosie') || defaultRosie;
            latestLeadPacket = sorted[0];

            const snapATAS = snapToRoute(latestATASPacket.lat, latestATASPacket.lon, latestATASPacket.day) || {{
                lat: latestATASPacket.lat, lon: latestATASPacket.lon, day: latestATASPacket.day || 1,
                stageName: 'Hanmer to Mirabel', cumKm: 0, pct: 0, stageRemKm: 648.7,
                hotelShort: "Motel au P'tit Sapin", nextFuelName: 'Sturgeon Falls', nextFuelKm: 92.0,
                nextFuelOctane: 'YES', completedCoords: [[46.656232, -80.882479]]
            }};
            const snapV2S = snapToRoute(latestV2SPacket.lat, latestV2SPacket.lon, latestV2SPacket.day) || {{
                lat: latestV2SPacket.lat, lon: latestV2SPacket.lon, day: latestV2SPacket.day || 1,
                stageName: 'Hanmer to Mirabel', cumKm: 0, pct: 0, stageRemKm: 648.7,
                hotelShort: "Motel au P'tit Sapin", nextFuelName: 'Sturgeon Falls', nextFuelKm: 92.0,
                nextFuelOctane: 'YES', completedCoords: [[46.656232, -80.882479]]
            }};

            // Lead progress uses whichever rider is further along the loop
            const leadSnap = snapATAS.cumKm >= snapV2S.cumKm ? snapATAS : snapV2S;

            // Calculate live separation between Jamie and Rosie
            const separationKm = haversineKm(
                latestATASPacket.lat, latestATASPacket.lon,
                latestV2SPacket.lat, latestV2SPacket.lon
            );
            const isCoLocated = separationKm < 0.5;

            // Update both Live Bike Markers & Completed Polyline
            liveMarkerATAS.setIcon(createLiveBikeIcon('Jamie', isCoLocated));
            liveMarkerV2S.setIcon(createLiveBikeIcon('Rosie', isCoLocated));
            liveMarkerATAS.setLatLng([latestATASPacket.lat, latestATASPacket.lon]);
            liveMarkerV2S.setLatLng([latestV2SPacket.lat, latestV2SPacket.lon]);

            liveCompletedTrail.setLatLngs(leadSnap.completedCoords);
            liveCompletedTrail.bringToFront();

            liveMarkerATAS.bindPopup(buildBikePopupHtml('Jamie', latestATASPacket, snapATAS, separationKm), {{
                maxWidth: 305,
                autoPanPaddingTopLeft: window.innerWidth > 768 ? [60, 110] : [16, 110],
                autoPanPaddingBottomRight: window.innerWidth > 768 ? [405, 30] : [20, 30]
            }});
            liveMarkerV2S.bindPopup(buildBikePopupHtml('Rosie', latestV2SPacket, snapV2S, separationKm), {{
                maxWidth: 305,
                autoPanPaddingTopLeft: window.innerWidth > 768 ? [60, 110] : [16, 110],
                autoPanPaddingBottomRight: window.innerWidth > 768 ? [405, 30] : [20, 30]
            }});

            // Update Historical Check-In Pins (White & Red for Jamie, Green for Rosie)
            liveCheckInLayer.clearLayers();
            sorted.slice(0, 18).forEach(item => {{
                const rCall = normalizeRider(item.rider);
                const isRosie = rCall === 'Rosie';
                const pinFill = isRosie ? '#16a34a' : '#ffffff';
                const pinStroke = isRosie ? '#ffffff' : '#dc2626';
                const pinAccent = isRosie ? '#16a34a' : '#dc2626';
                const cm = L.circleMarker([item.lat, item.lon], {{
                    radius: 5.5,
                    fillColor: pinFill,
                    color: pinStroke,
                    weight: 2.5,
                    opacity: 1,
                    fillOpacity: 0.95
                }}).addTo(liveCheckInLayer);
                cm.bindPopup(`
                    <div class="poi-popup-card">
                        <div class="poi-popup-type" style="color:${{pinAccent}};">✓ ${{rCall.toUpperCase()}} CHECK-IN • DAY ${{item.day || 1}}</div>
                        <div class="poi-popup-title"><span class="lt-rider-pill ${{isRosie ? 'v2s' : ''}}" style="margin-right:5px;">${{rCall}}</span>${{item.status}}</div>
                        <div class="poi-popup-desc">${{item.note || ''}}</div>
                        <div style="font-size:0.72rem; color:var(--text-muted);">🕒 ${{new Date(item.ts).toLocaleString('en-CA')}}</div>
                    </div>
                `);
            }});

            // Update Jamie & Rosie Status Cards in HUD
            const elTimeAtas   = document.getElementById('lt-time-atas');
            const elStatusAtas = document.getElementById('lt-status-atas');
            const elNoteAtas   = document.getElementById('lt-note-atas');
            if (elTimeAtas)   elTimeAtas.textContent   = formatRelativeTime(latestATASPacket.ts);
            if (elStatusAtas) elStatusAtas.textContent = `${{latestATASPacket.status}}`;
            if (elNoteAtas)   elNoteAtas.textContent   = `Day ${{snapATAS.day}} • ${{latestATASPacket.note || '2025 Africa Twin'}}`;

            const elTimeV2s   = document.getElementById('lt-time-v2s');
            const elStatusV2s = document.getElementById('lt-status-v2s');
            const elNoteV2s   = document.getElementById('lt-note-v2s');
            if (elTimeV2s)   elTimeV2s.textContent   = formatRelativeTime(latestV2SPacket.ts);
            if (elStatusV2s) elStatusV2s.textContent = `${{latestV2SPacket.status}}`;
            if (elNoteV2s)   elNoteV2s.textContent   = `Day ${{snapV2S.day}} • ${{latestV2SPacket.note || 'Ducati V2S'}}`;

            // Update Loop Progress & 4-Metric Telemetry Grid
            const elProgT  = document.getElementById('lt-progress-text');
            const elProgF  = document.getElementById('lt-progress-fill');
            const elStage  = document.getElementById('lt-metric-stage');
            const elHotel  = document.getElementById('lt-metric-hotel');
            const elFuel   = document.getElementById('lt-metric-fuel');
            const elSpeed  = document.getElementById('lt-metric-speed');

            if (elProgT)  elProgT.textContent  = `${{leadSnap.cumKm.toFixed(1)}} / 8,243.4 km (${{leadSnap.pct.toFixed(1)}}%)`;
            if (elProgF)  elProgF.style.width  = `${{Math.max(1.5, leadSnap.pct)}}%`;
            if (elStage)  elStage.textContent  = `Day ${{leadSnap.day}}: ${{leadSnap.stageName}}`;
            if (elHotel)  elHotel.textContent  = `${{leadSnap.stageRemKm.toFixed(1)}} km to ${{leadSnap.hotelShort}}`;
            if (elFuel) {{
                const octLabel = leadSnap.nextFuelOctane === 'NO' ? '87 Only' : '91 AKI';
                elFuel.textContent = `+${{leadSnap.nextFuelKm.toFixed(0)}} km • ${{leadSnap.nextFuelName}} (${{octLabel}})`;
            }}
            if (elSpeed) {{
                if (separationKm < 0.5) {{
                    const maxSpd = Math.max(Number(latestATASPacket.speedKmh) || 0, Number(latestV2SPacket.speedKmh) || 0);
                    elSpeed.textContent = maxSpd > 0 ? `Together • ${{maxSpd}} km/h` : 'Together (0.0 km apart)';
                }} else {{
                    elSpeed.textContent = `${{separationKm.toFixed(1)}} km apart`;
                }}
            }}

            // Populate Check-In Feed List with Jamie / Rosie Callsign Pills
            const feedEl = document.getElementById('lt-feed-list');
            if (feedEl) {{
                feedEl.innerHTML = sorted.slice(0, 14).map((item) => {{
                    const rCall = normalizeRider(item.rider);
                    const pillClass = rCall === 'Rosie' ? 'v2s' : '';
                    return `
                    <div class="lt-feed-item" onclick="focusCheckInItem(${{item.lat}}, ${{item.lon}}, '${{rCall}}')">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:2px;">
                            <span style="font-weight:800; color:var(--text-main); display:flex; align-items:center; gap:5px;">
                                <span class="lt-rider-pill ${{pillClass}}">${{rCall}}</span>
                                <span>${{item.status}}</span>
                                <span style="color:var(--accent-blue); font-weight:700;">(Day ${{item.day || 1}})</span>
                            </span>
                            <span style="font-size:0.66rem; color:var(--text-muted); font-family:monospace;">${{formatRelativeTime(item.ts)}}</span>
                        </div>
                        <div style="color:var(--text-card); line-height:1.32;">${{item.note || ''}}</div>
                    </div>
                    `;
                }}).join('');
            }}
        }}

        function focusCheckInItem(lat, lon, callsign) {{
            const lonOffset = window.innerWidth > 768 ? 0.25 : 0;
            map.setView([lat + 0.08, lon + lonOffset], 10, {{ animate: true }});
            if (normalizeRider(callsign) === 'Rosie') {{
                liveMarkerV2S.openPopup();
            }} else {{
                liveMarkerATAS.openPopup();
            }}
        }}

        function centerOnLiveBike(callsign) {{
            const targetCall = callsign ? normalizeRider(callsign) : (latestLeadPacket ? normalizeRider(latestLeadPacket.rider) : 'Jamie');
            const pkt = targetCall === 'Rosie' ? latestV2SPacket : latestATASPacket;
            const marker = targetCall === 'Rosie' ? liveMarkerV2S : liveMarkerATAS;
            if (!pkt) return;
            const lonOffset = window.innerWidth > 768 ? 0.55 : 0;
            map.setView([pkt.lat + 0.14, pkt.lon + lonOffset], 9, {{ animate: true }});
            if (marker) marker.openPopup();
        }}

        function toggleLiveTrackerPanel() {{
            const panel = document.getElementById('live-tracker-panel');
            if (!panel) return;
            panel.classList.toggle('open');
        }}

        function toggleRiderBroadcastDrawer() {{
            const drawer = document.getElementById('lt-rider-drawer');
            const chev = document.getElementById('lt-rider-chevron');
            if (!drawer) return;
            const isHidden = drawer.style.display === 'none';
            drawer.style.display = isHidden ? 'block' : 'none';
            if (chev) chev.textContent = isHidden ? '▾' : '▸';
        }}

        function unlockRiderControls() {{
            const pinIn = document.getElementById('lt-pin-input');
            const gate = document.getElementById('lt-pin-gate');
            const ctrls = document.getElementById('lt-rider-controls');
            const fb = document.getElementById('lt-broadcast-feedback');
            if (!pinIn) return;
            if (pinIn.value.trim() === RIDER_PIN_CODE) {{
                gate.style.display = 'none';
                ctrls.style.display = 'flex';
                localStorage.setItem('exp51_rider_unlocked', 'true');
            }} else {{
                pinIn.style.borderColor = 'var(--accent-red)';
                if (fb) fb.textContent = '⚠️ Invalid Rider PIN (Default: 2027)';
            }}
        }}

        if (localStorage.getItem('exp51_rider_unlocked') === 'true') {{
            const gate = document.getElementById('lt-pin-gate');
            const ctrls = document.getElementById('lt-rider-controls');
            if (gate && ctrls) {{
                gate.style.display = 'none';
                ctrls.style.display = 'flex';
            }}
        }}
        selectRiderCallsign(selectedRiderCallsign);

        function selectCheckInStatus(statusLabel, defaultNote, btnEl) {{
            selectedStatusLabel = statusLabel;
            selectedDefaultNote = defaultNote;
            document.querySelectorAll('#lt-status-chips .lt-chip-btn').forEach(b => b.classList.remove('active'));
            if (btnEl) btnEl.classList.add('active');
        }}

        async function publishPacketToCloud(pkt) {{
            pkt.rider = normalizeRider(pkt.rider);
            // Save immediately to local history and update UI
            const hist = getStoredFeedHistory();
            if (!hist.some(x => x.id === pkt.id)) {{
                hist.unshift(pkt);
                saveStoredFeedHistory(hist);
                renderLiveTrackerState(hist);
            }}

            try {{
                const res = await fetch(`https://ntfy.sh/${{LIVE_CLOUD_TOPIC}}`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'text/plain;charset=utf-8' }},
                    body: JSON.stringify(pkt)
                }});
                if (!res.ok) throw new Error('Cloud HTTP ' + res.status);
                return true;
            }} catch (err) {{
                const q = getOfflineQueue();
                if (!q.some(x => x.id === pkt.id)) {{
                    q.push(pkt);
                    saveOfflineQueue(q);
                }}
                return false;
            }}
        }}

        async function flushOfflineTrackerQueue() {{
            const q = getOfflineQueue();
            if (!q.length) return;
            const remaining = [];
            for (const pkt of q) {{
                try {{
                    const res = await fetch(`https://ntfy.sh/${{LIVE_CLOUD_TOPIC}}`, {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'text/plain;charset=utf-8' }},
                        body: JSON.stringify(pkt)
                    }});
                    if (!res.ok) remaining.push(pkt);
                }} catch (e) {{
                    remaining.push(pkt);
                }}
            }}
            saveOfflineQueue(remaining);
        }}
        window.addEventListener('online', flushOfflineTrackerQueue);

        async function postRiderCheckIn() {{
            const locSel = document.getElementById('lt-location-select');
            const noteIn = document.getElementById('lt-note-input');
            const fb = document.getElementById('lt-broadcast-feedback');
            const customNote = noteIn && noteIn.value.trim() ? noteIn.value.trim() : selectedDefaultNote;
            const callsign = normalizeRider(selectedRiderCallsign);

            const sendWithCoords = async (lat, lon, dayHint, speedKmh, altM) => {{
                const snap = snapToRoute(lat, lon, dayHint);
                const pkt = {{
                    app: 'exp51-live',
                    sig: RIDER_PIN_CODE,
                    rider: callsign,
                    id: 'chk-' + callsign.toLowerCase() + '-' + Date.now() + '-' + Math.random().toString(36).slice(2, 6),
                    ts: Date.now(),
                    lat: Number(lat.toFixed(6)),
                    lon: Number(lon.toFixed(6)),
                    day: snap ? snap.day : (dayHint || 1),
                    speedKmh: speedKmh || 0,
                    altM: altM || 120,
                    status: selectedStatusLabel,
                    note: customNote
                }};
                if (fb) fb.textContent = `📡 Broadcasting ${{callsign}} check-in to Family Feed...`;
                const synced = await publishPacketToCloud(pkt);
                if (noteIn) noteIn.value = '';
                if (fb) {{
                    fb.style.color = synced ? 'var(--accent-green)' : 'var(--accent-orange)';
                    fb.textContent = synced
                        ? `✓ [${{callsign}}] Broadcast live to Family & Friends Cloud Feed!`
                        : `⏳ [${{callsign}}] Saved & queued offline (will auto-sync on cell signal)`;
                }}
                centerOnLiveBike(callsign);
            }};

            const fallbackPkt = (callsign === 'Rosie' ? latestV2SPacket : latestATASPacket) || {{ lat: 46.656232, lon: -80.882479, day: 1 }};

            if (locSel && locSel.value !== 'gps') {{
                const parts = locSel.value.split(',');
                const lat = parseFloat(parts[0]);
                const lon = parseFloat(parts[1]);
                const dayHint = parseInt(parts[2]) || 1;
                await sendWithCoords(lat, lon, dayHint, 0, 145);
            }} else if (navigator.geolocation) {{
                if (fb) fb.textContent = `🛰️ [${{callsign}}] Acquiring phone GPS lock...`;
                navigator.geolocation.getCurrentPosition(
                    pos => {{
                        const spd = pos.coords.speed ? Math.round(pos.coords.speed * 3.6) : 0;
                        const alt = pos.coords.altitude ? Math.round(pos.coords.altitude) : 150;
                        sendWithCoords(pos.coords.latitude, pos.coords.longitude, null, spd, alt);
                    }},
                    err => {{
                        sendWithCoords(fallbackPkt.lat, fallbackPkt.lon, fallbackPkt.day, 0, 150);
                    }},
                    {{ enableHighAccuracy: true, timeout: 6000 }}
                );
            }} else {{
                await sendWithCoords(fallbackPkt.lat, fallbackPkt.lon, fallbackPkt.day, 0, 150);
            }}
        }}

        function toggleAutoGpsBroadcast() {{
            const btn = document.getElementById('btn-auto-gps');
            const fb = document.getElementById('lt-broadcast-feedback');
            if (liveGpsWatchId !== null) {{
                navigator.geolocation.clearWatch(liveGpsWatchId);
                liveGpsWatchId = null;
                if (btn) {{
                    btn.textContent = '📡 Start Live Phone GPS';
                    btn.classList.remove('active');
                }}
                if (fb) fb.textContent = `⏹️ [${{selectedRiderCallsign}}] Live Phone GPS auto-broadcast stopped.`;
                return;
            }}
            if (!navigator.geolocation) {{
                if (fb) fb.textContent = '⚠️ Geolocation API not available on this device.';
                return;
            }}
            if (btn) {{
                btn.textContent = `🟢 [${{selectedRiderCallsign}}] GPS Broadcasting (Stop)`;
                btn.classList.add('active');
            }}
            if (fb) fb.textContent = `🛰️ Watching [${{selectedRiderCallsign}}] phone GPS & broadcasting every 5 mins...`;

            liveGpsWatchId = navigator.geolocation.watchPosition(
                pos => {{
                    const now = Date.now();
                    const callsign = normalizeRider(selectedRiderCallsign);
                    const spd = pos.coords.speed ? Math.round(pos.coords.speed * 3.6) : 0;
                    const alt = pos.coords.altitude ? Math.round(pos.coords.altitude) : 150;
                    const snap = snapToRoute(pos.coords.latitude, pos.coords.longitude, null);
                    // Broadcast immediately on first fix, then every 5 minutes
                    if (now - lastAutoBroadcastMs >= 300000 || lastAutoBroadcastMs === 0) {{
                        lastAutoBroadcastMs = now;
                        const pkt = {{
                            app: 'exp51-live',
                            sig: RIDER_PIN_CODE,
                            rider: callsign,
                            id: 'gps-' + callsign.toLowerCase() + '-' + now,
                            ts: now,
                            lat: Number(pos.coords.latitude.toFixed(6)),
                            lon: Number(pos.coords.longitude.toFixed(6)),
                            day: snap ? snap.day : 1,
                            speedKmh: spd,
                            altM: alt,
                            status: spd > 5 ? '🏍️ In Saddle (Live GPS)' : selectedStatusLabel,
                            note: `[${{callsign}}] Auto GPS telemetry beacon • ${{spd}} km/h`
                        }};
                        publishPacketToCloud(pkt);
                    }}
                }},
                err => {{
                    if (fb) fb.textContent = '⚠️ GPS signal weak — standing by for satellite lock.';
                }},
                {{ enableHighAccuracy: true, maximumAge: 15000, timeout: 15000 }}
            );
        }}

        async function pollCloudTrackerFeed(showFeedback = false) {{
            try {{
                const res = await fetch(`https://ntfy.sh/${{LIVE_CLOUD_TOPIC}}/json?poll=1&since=all`);
                if (!res.ok) throw new Error('Cloud poll HTTP ' + res.status);
                const text = await res.text();
                const lines = text.trim().split('\\n').filter(Boolean);
                const hist = getStoredFeedHistory();
                let added = false;

                lines.forEach(line => {{
                    try {{
                        const env = JSON.parse(line);
                        if (env && env.event === 'message' && env.message) {{
                            const pkt = JSON.parse(env.message);
                            if (pkt && pkt.app === 'exp51-live' && pkt.sig === RIDER_PIN_CODE && pkt.id) {{
                                pkt.rider = normalizeRider(pkt.rider);
                                if (!hist.some(x => x.id === pkt.id)) {{
                                    hist.push(pkt);
                                    added = true;
                                }}
                            }}
                        }}
                    }} catch (e) {{}}
                }});

                if (added || showFeedback) {{
                    hist.sort((a, b) => b.ts - a.ts);
                    saveStoredFeedHistory(hist);
                    renderLiveTrackerState(hist);
                }}
            }} catch (e) {{}}
        }}

        function connectCloudTrackerSSE() {{
            if (typeof EventSource === 'undefined') return;
            try {{
                const es = new EventSource(`https://ntfy.sh/${{LIVE_CLOUD_TOPIC}}/sse`);
                es.onmessage = (evt) => {{
                    try {{
                        const env = JSON.parse(evt.data);
                        if (env && env.message) {{
                            const pkt = JSON.parse(env.message);
                            if (pkt && pkt.app === 'exp51-live' && pkt.sig === RIDER_PIN_CODE && pkt.id) {{
                                pkt.rider = normalizeRider(pkt.rider);
                                const hist = getStoredFeedHistory();
                                if (!hist.some(x => x.id === pkt.id)) {{
                                    hist.unshift(pkt);
                                    saveStoredFeedHistory(hist);
                                    renderLiveTrackerState(hist);
                                }}
                            }}
                        }}
                    }} catch (e) {{}}
                }};
            }} catch (e) {{}}
        }}

        // Initialize Family & Friends Live Tracker on Load (Dual-Rider: Jamie & Rosie)
        renderLiveTrackerState(getStoredFeedHistory());
        updateOfflineQueueBadge();
        pollCloudTrackerFeed(false);
        connectCloudTrackerSSE();

        // =========================================================================
        // PER-BIKE LUGGAGE VOLUME & PACKING CHECKLIST (GIT-BACKED, ZERO LOCAL LOCK-IN)
        // =========================================================================
        const GIT_REPO_OWNER = 'Rindelk';
        const GIT_REPO_NAME  = 'expedition-51';
        const GIT_BRANCH     = 'main';
        const GIT_FILE_PATH  = 'luggage_checklist.json';
        const GIT_CHECKLIST_RELAY_TOPIC = 'exp51_git_checklist_sync_2027';

        // In-memory state loaded from Git (luggage_checklist.json) — not stored on local device storage
        let checklistState = JSON.parse(JSON.stringify(defaultChecklistData));
        let checklistGitSha = null;
        let checklistViewFilter = 'both';
        let checklistSessionToken = '';
        let checklistDirty = false;

        function setGitStatusBadge(text, tone) {{
            const badge = document.getElementById('chk-git-status-badge');
            if (!badge) return;
            badge.textContent = text;
            if (tone === 'green') {{
                badge.style.background = 'rgba(5, 150, 105, 0.14)';
                badge.style.color = 'var(--accent-green)';
                badge.style.borderColor = 'rgba(5, 150, 105, 0.35)';
            }} else if (tone === 'orange') {{
                badge.style.background = 'rgba(217, 119, 6, 0.14)';
                badge.style.color = 'var(--accent-orange)';
                badge.style.borderColor = 'rgba(217, 119, 6, 0.35)';
            }} else if (tone === 'blue') {{
                badge.style.background = 'rgba(2, 132, 199, 0.14)';
                badge.style.color = 'var(--accent-blue)';
                badge.style.borderColor = 'rgba(2, 132, 199, 0.35)';
            }} else {{
                badge.style.background = 'rgba(220, 38, 38, 0.14)';
                badge.style.color = 'var(--accent-red)';
                badge.style.borderColor = 'rgba(220, 38, 38, 0.35)';
            }}
        }}

        function markChecklistDirty() {{
            checklistDirty = true;
            checklistState.lastUpdated = new Date().toISOString();
            setGitStatusBadge('✏️ Uncommitted Edits — Click "Commit & Save to Git"', 'orange');
        }}

        function setChecklistBikeFilter(mode) {{
            checklistViewFilter = mode;
            ['both', 'jamie', 'rosie'].forEach(m => {{
                const btn = document.getElementById('chk-view-' + m);
                if (btn) btn.classList.toggle('active', m === mode);
            }});
            const grid = document.getElementById('chk-bikes-container');
            if (grid) {{
                grid.style.gridTemplateColumns = (mode === 'both') ? 'minmax(0, 1fr) minmax(0, 1fr)' : '1fr';
            }}
            renderLuggageChecklist();
        }}

        function toggleGitTokenDrawer() {{
            const drawer = document.getElementById('chk-git-token-drawer');
            if (!drawer) return;
            drawer.style.display = (drawer.style.display === 'none') ? 'block' : 'none';
        }}

        async function applyGitAuthConfig() {{
            const patIn = document.getElementById('chk-github-pat-input');
            const authIn = document.getElementById('chk-commit-author-input');
            if (patIn) checklistSessionToken = patIn.value.trim();
            if (authIn && authIn.value.trim()) checklistState.updatedBy = authIn.value.trim();
            if (!checklistSessionToken) {{
                setGitStatusBadge('⚠️ Enter a valid GitHub PAT token to push directly to GitHub', 'orange');
                return;
            }}
            setGitStatusBadge('🔄 Verifying GitHub repo access...', 'blue');
            await pullChecklistFromGit(true);
            const drawer = document.getElementById('chk-git-token-drawer');
            if (drawer) drawer.style.display = 'none';
        }}

        function escapeHtmlAttr(str) {{
            return String(str || '').replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        }}

        function renderLuggageChecklist() {{
            const container = document.getElementById('chk-bikes-container');
            if (!container || !checklistState || !checklistState.bikes) return;

            const bikeKeys = checklistViewFilter === 'both'
                ? ['jamie', 'rosie']
                : [checklistViewFilter];

            container.innerHTML = bikeKeys.map(bikeKey => {{
                const bike = checklistState.bikes[bikeKey];
                if (!bike) return '';
                const isJamie = (bikeKey === 'jamie');
                const badgeStyle = isJamie
                    ? 'background:#ffffff; color:#dc2626; border:1.5px solid #dc2626;'
                    : 'background:#16a34a; color:#ffffff; border:1.5px solid #15803d;';

                // Calculate total capacity across all compartments
                const comps = bike.compartments || [];
                const items = bike.items || [];
                const totalCapL = comps.reduce((acc, c) => acc + (Number(c.capacityL) || 0), 0);
                bike.totalCapacityL = Number(totalCapL.toFixed(1));

                const packedVolL = items.filter(i => i.packed).reduce((acc, i) => acc + (Number(i.volumeL) || 0), 0);
                const allAllocatedVolL = items.reduce((acc, i) => acc + (Number(i.volumeL) || 0), 0);
                const packedWeightKg = items.filter(i => i.packed).reduce((acc, i) => acc + (Number(i.weightKg) || 0), 0);
                const freeVolL = totalCapL - packedVolL;
                const pctFull = totalCapL > 0 ? (packedVolL / totalCapL) * 100 : 0;
                const packedCount = items.filter(i => i.packed).length;

                let barColor = isJamie ? '#dc2626' : '#16a34a';
                if (pctFull > 100) barColor = '#ef4444';
                else if (pctFull > 88) barColor = '#f59e0b';

                const overWarnHtml = freeVolL < 0
                    ? `<span style="color:var(--accent-red); font-weight:800;">⚠️ OVER CAPACITY BY ${{Math.abs(freeVolL).toFixed(1)}} L!</span>`
                    : `<span style="color:var(--accent-green); font-weight:800;">✓ ${{freeVolL.toFixed(1)}} L Free Space</span>`;

                const compartmentsHtml = comps.map(comp => {{
                    const cItems = items.filter(i => i.compartmentId === comp.id);
                    const cCapL = Number(comp.capacityL) || 1;
                    const cPackedL = cItems.filter(i => i.packed).reduce((acc, i) => acc + (Number(i.volumeL) || 0), 0);
                    const cAllocL = cItems.reduce((acc, i) => acc + (Number(i.volumeL) || 0), 0);
                    const cWeightKg = cItems.filter(i => i.packed).reduce((acc, i) => acc + (Number(i.weightKg) || 0), 0);
                    const cFreeL = cCapL - cPackedL;
                    const cPct = cCapL > 0 ? (cPackedL / cCapL) * 100 : 0;

                    let cBarColor = 'var(--accent-blue)';
                    if (cPct > 100) cBarColor = 'var(--accent-red)';
                    else if (cPct > 88) cBarColor = 'var(--accent-orange)';
                    else cBarColor = 'var(--accent-green)';

                    const cStatusText = cFreeL < 0
                        ? `<span style="color:var(--accent-red); font-weight:800;">⚠️ +${{Math.abs(cFreeL).toFixed(1)}} L Over!</span>`
                        : `<span style="color:var(--text-muted);">${{cFreeL.toFixed(1)}} L free</span>`;

                    const rowsHtml = cItems.map(item => `
                        <div class="chk-item-row ${{item.packed ? '' : 'unpacked'}}">
                            <input type="checkbox" ${{item.packed ? 'checked' : ''}} onchange="toggleChecklistItemPacked('${{bikeKey}}', '${{item.id}}', this.checked)" style="width:16px; height:16px; cursor:pointer; accent-color:${{isJamie ? '#dc2626' : '#16a34a'}};" title="Toggle Packed Status (Included in Packed Volume)" />
                            <div style="flex:1; min-width:0; display:flex; flex-direction:column;">
                                <input type="text" class="chk-inline-input" value="${{escapeHtmlAttr(item.name)}}" onchange="updateChecklistItemField('${{bikeKey}}', '${{item.id}}', 'name', this.value)" style="font-weight:700; width:100%;" title="Click to edit item name" />
                                <input type="text" class="chk-inline-input" value="${{escapeHtmlAttr(item.notes || '')}}" placeholder="Add packing note..." onchange="updateChecklistItemField('${{bikeKey}}', '${{item.id}}', 'notes', this.value)" style="font-size:0.69rem; color:var(--text-muted); width:100%;" title="Click to edit item note" />
                            </div>
                            <div style="display:flex; align-items:center; gap:4px; flex-shrink:0;" title="Item Volume in Litres (L)">
                                <input type="number" step="0.5" min="0" max="100" class="chk-num-input" value="${{Number(item.volumeL).toFixed(1)}}" onchange="updateChecklistItemField('${{bikeKey}}', '${{item.id}}', 'volumeL', parseFloat(this.value)||0)" />
                                <span style="font-size:0.70rem; font-weight:800; color:var(--text-muted);">L</span>
                            </div>
                            <div style="display:flex; align-items:center; gap:3px; flex-shrink:0;" title="Item Weight in Kilograms (kg)">
                                <input type="number" step="0.1" min="0" max="50" class="chk-num-input" style="width:46px; color:var(--text-main);" value="${{Number(item.weightKg || 0).toFixed(1)}}" onchange="updateChecklistItemField('${{bikeKey}}', '${{item.id}}', 'weightKg', parseFloat(this.value)||0)" />
                                <span style="font-size:0.68rem; color:var(--text-muted);">kg</span>
                            </div>
                            <button type="button" onclick="deleteChecklistItem('${{bikeKey}}', '${{item.id}}')" style="background:transparent; border:none; color:var(--text-muted); cursor:pointer; font-size:0.82rem; padding:2px 4px;" title="Remove item">🗑️</button>
                        </div>
                    `).join('');

                    return `
                        <div class="chk-comp-card">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:8px; flex-wrap:wrap;">
                                <div>
                                    <div style="font-size:0.84rem; font-weight:800; color:var(--text-main); display:flex; align-items:center; gap:6px;">
                                        <span>${{comp.icon || '🧳'}}</span>
                                        <span>${{comp.name}}</span>
                                    </div>
                                    <div style="font-size:0.71rem; color:var(--text-muted);">${{comp.role || ''}}</div>
                                </div>
                                <div style="display:flex; align-items:center; gap:6px; font-size:0.74rem; font-weight:800;">
                                    <span style="color:var(--accent-blue);">${{cPackedL.toFixed(1)}} L</span>
                                    <span style="color:var(--text-muted);">/</span>
                                    <input type="number" step="1" min="1" max="120" class="chk-num-input" style="width:58px;" value="${{cCapL.toFixed(1)}}" onchange="updateCompartmentCapacity('${{bikeKey}}', '${{comp.id}}', parseFloat(this.value)||1)" title="Edit Compartment Max Capacity (L)" />
                                    <span style="color:var(--text-muted);">L Cap</span>
                                </div>
                            </div>

                            <!-- Compartment Volume Bar -->
                            <div>
                                <div style="display:flex; justify-content:space-between; font-size:0.69rem; font-weight:700; margin-bottom:3px;">
                                    <span>Packed: ${{cPackedL.toFixed(1)}} L (${{cPct.toFixed(0)}}%) • Weight: ${{cWeightKg.toFixed(1)}} kg</span>
                                    ${{cStatusText}}
                                </div>
                                <div class="chk-vol-bar-track" style="height:7px;">
                                    <div class="chk-vol-bar-fill" style="width:${{Math.min(100, Math.max(2, cPct))}}%; background:${{cBarColor}};"></div>
                                </div>
                            </div>

                            <!-- Items List -->
                            <div style="display:flex; flex-direction:column; gap:5px;">
                                ${{rowsHtml}}
                            </div>

                            <!-- Add Item Row -->
                            <div style="display:flex; gap:5px; align-items:center; margin-top:2px; padding-top:6px; border-top:1px dashed var(--border); flex-wrap:wrap;">
                                <input type="text" id="add-name-${{comp.id}}" placeholder="+ Add gear to ${{comp.name.split('(')[0].trim()}}..." style="flex:1; min-width:130px; background:var(--bg-card); color:var(--text-main); border:1px solid var(--border); border-radius:6px; padding:5px 8px; font-size:0.74rem;" />
                                <input type="number" id="add-vol-${{comp.id}}" step="0.5" min="0.1" placeholder="L" value="2.0" style="width:52px; background:var(--bg-card); color:var(--accent-blue); border:1px solid var(--border); border-radius:6px; padding:5px 6px; font-size:0.74rem; font-weight:700; text-align:right;" title="Volume in Litres (L)" />
                                <span style="font-size:0.70rem; font-weight:700; color:var(--text-muted);">L</span>
                                <input type="number" id="add-wt-${{comp.id}}" step="0.1" min="0" placeholder="kg" value="0.5" style="width:48px; background:var(--bg-card); color:var(--text-main); border:1px solid var(--border); border-radius:6px; padding:5px 6px; font-size:0.74rem; text-align:right;" title="Weight in kg" />
                                <span style="font-size:0.70rem; color:var(--text-muted);">kg</span>
                                <button type="button" onclick="addChecklistItem('${{bikeKey}}', '${{comp.id}}')" class="lt-chip-btn" style="padding:5px 10px; font-weight:800;">+ Add</button>
                            </div>
                        </div>
                    `;
                }}).join('');

                return `
                    <div class="chk-bike-panel ${{bikeKey}}">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px; flex-wrap:wrap; border-bottom:1px solid var(--border); padding-bottom:12px;">
                            <div>
                                <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                                    <span style="padding:3px 9px; border-radius:6px; font-size:0.76rem; font-weight:900; ${{badgeStyle}}">${{bike.rider}}</span>
                                    <h3 style="font-size:1.02rem; font-weight:800; color:var(--text-main); margin:0;">${{bike.model}}</h3>
                                </div>
                                <div style="font-size:0.74rem; color:var(--text-muted); margin-top:4px;">
                                    🎨 Color: <strong>${{bike.color}}</strong> • 🧳 ${{comps.length}} Compartments • ✓ ${{packedCount}}/${{items.length}} Items Packed
                                </div>
                            </div>
                            <div style="text-align:right;">
                                <div style="font-size:1.05rem; font-weight:900; color:var(--text-main);">${{packedVolL.toFixed(1)}} L <span style="font-size:0.80rem; font-weight:700; color:var(--text-muted);">/ ${{totalCapL.toFixed(1)}} L</span></div>
                                <div style="font-size:0.71rem; color:var(--text-muted);">⚖️ ${{packedWeightKg.toFixed(1)}} kg Packed Load</div>
                            </div>
                        </div>

                        <!-- Total Bike Luggage Volume Utilization Bar -->
                        <div style="background:var(--bg-subtle); border:1px solid var(--border); border-radius:8px; padding:10px 12px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.75rem; font-weight:800; margin-bottom:5px; flex-wrap:wrap; gap:4px;">
                                <span>📊 TOTAL LUGGAGE VOLUME UTILIZATION (${{pctFull.toFixed(1)}}%)</span>
                                ${{overWarnHtml}}
                            </div>
                            <div class="chk-vol-bar-track">
                                <div class="chk-vol-bar-fill" style="width:${{Math.min(100, Math.max(2, pctFull))}}%; background:${{barColor}};"></div>
                            </div>
                            <div style="display:flex; justify-content:space-between; font-size:0.69rem; color:var(--text-muted); margin-top:5px; flex-wrap:wrap; gap:6px;">
                                <span>📦 Packed Volume: <strong>${{packedVolL.toFixed(1)}} L</strong></span>
                                <span>📋 Total Listed Gear: <strong>${{allAllocatedVolL.toFixed(1)}} L</strong></span>
                                <span>🧳 Max Bike Capacity: <strong>${{totalCapL.toFixed(1)}} L</strong></span>
                            </div>
                        </div>

                        <!-- Compartments Breakdown -->
                        <div style="display:flex; flex-direction:column; gap:12px;">
                            ${{compartmentsHtml}}
                        </div>
                    </div>
                `;
            }}).join('');
        }}

        function toggleChecklistItemPacked(bikeKey, itemId, isPacked) {{
            const bike = checklistState.bikes[bikeKey];
            if (!bike) return;
            const item = (bike.items || []).find(i => i.id === itemId);
            if (item) {{
                item.packed = Boolean(isPacked);
                markChecklistDirty();
                renderLuggageChecklist();
            }}
        }}

        function updateChecklistItemField(bikeKey, itemId, field, value) {{
            const bike = checklistState.bikes[bikeKey];
            if (!bike) return;
            const item = (bike.items || []).find(i => i.id === itemId);
            if (item) {{
                item[field] = value;
                markChecklistDirty();
                renderLuggageChecklist();
            }}
        }}

        function updateCompartmentCapacity(bikeKey, compId, newCapL) {{
            const bike = checklistState.bikes[bikeKey];
            if (!bike) return;
            const comp = (bike.compartments || []).find(c => c.id === compId);
            if (comp && newCapL > 0) {{
                comp.capacityL = Number(newCapL.toFixed(1));
                markChecklistDirty();
                renderLuggageChecklist();
            }}
        }}

        function addChecklistItem(bikeKey, compId) {{
            const bike = checklistState.bikes[bikeKey];
            if (!bike) return;
            const nameEl = document.getElementById('add-name-' + compId);
            const volEl  = document.getElementById('add-vol-' + compId);
            const wtEl   = document.getElementById('add-wt-' + compId);
            const name = nameEl ? nameEl.value.trim() : '';
            if (!name) return;
            const vol = volEl ? (parseFloat(volEl.value) || 1.0) : 1.0;
            const wt  = wtEl ? (parseFloat(wtEl.value) || 0.2) : 0.2;

            bike.items.push({{
                id: bikeKey[0] + '-' + Date.now().toString(36),
                compartmentId: compId,
                name: name,
                volumeL: Number(vol.toFixed(1)),
                weightKg: Number(wt.toFixed(1)),
                packed: true,
                notes: ''
            }});
            markChecklistDirty();
            renderLuggageChecklist();
        }}

        function deleteChecklistItem(bikeKey, itemId) {{
            const bike = checklistState.bikes[bikeKey];
            if (!bike) return;
            bike.items = (bike.items || []).filter(i => i.id !== itemId);
            markChecklistDirty();
            renderLuggageChecklist();
        }}

        function utf8ToBase64(str) {{
            return btoa(unescape(encodeURIComponent(str)));
        }}

        function base64ToUtf8(b64) {{
            return decodeURIComponent(escape(atob(b64.replace(/\\s/g, ''))));
        }}

        // Pull latest luggage_checklist.json from GitHub Contents API + Cloud Relay (zero local device lock-in)
        async function pullChecklistFromGit(showFeedback = false) {{
            if (showFeedback) setGitStatusBadge('🔄 Pulling luggage_checklist.json from Git...', 'blue');
            let loadedFromGitApi = false;
            try {{
                const headers = {{ 'Accept': 'application/vnd.github.v3+json' }};
                if (checklistSessionToken) {{
                    headers['Authorization'] = `Bearer ${{checklistSessionToken}}`;
                }}
                const apiRes = await fetch(`https://api.github.com/repos/${{GIT_REPO_OWNER}}/${{GIT_REPO_NAME}}/contents/${{GIT_FILE_PATH}}?ref=${{GIT_BRANCH}}&t=${{Date.now()}}`, {{
                    headers: headers,
                    cache: 'no-store'
                }});
                if (apiRes.ok) {{
                    const meta = await apiRes.json();
                    if (meta && meta.content) {{
                        checklistGitSha = meta.sha;
                        const parsed = JSON.parse(base64ToUtf8(meta.content));
                        if (parsed && parsed.bikes) {{
                            checklistState = parsed;
                            loadedFromGitApi = true;
                        }}
                    }}
                }}
            }} catch (e) {{}}

            if (!loadedFromGitApi) {{
                try {{
                    const rawRes = await fetch(`./${{GIT_FILE_PATH}}?t=${{Date.now()}}`, {{ cache: 'no-store' }});
                    if (rawRes.ok) {{
                        const parsed = await rawRes.json();
                        if (parsed && parsed.bikes) {{
                            checklistState = parsed;
                            loadedFromGitApi = true;
                        }}
                    }}
                }} catch (e) {{}}
            }}

            // Also check cloud relay for any newer commits/broadcasts across devices
            try {{
                const relayRes = await fetch(`https://ntfy.sh/${{GIT_CHECKLIST_RELAY_TOPIC}}/json?poll=1&since=all`, {{ cache: 'no-store' }});
                if (relayRes.ok) {{
                    const txt = await relayRes.text();
                    const lines = txt.trim().split('\\n').filter(Boolean);
                    for (let i = lines.length - 1; i >= 0; i--) {{
                        try {{
                            const env = JSON.parse(lines[i]);
                            if (env && env.event === 'message' && env.message) {{
                                const payload = JSON.parse(env.message);
                                if (payload && payload.bikes && payload.lastUpdated) {{
                                    const curTs = Date.parse(checklistState.lastUpdated || '') || 0;
                                    const newTs = Date.parse(payload.lastUpdated) || 0;
                                    if (newTs >= curTs) {{
                                        checklistState = payload;
                                        break;
                                    }}
                                }}
                            }}
                        }} catch (innerE) {{}}
                    }}
                }}
            }} catch (e) {{}}

            checklistDirty = false;
            renderLuggageChecklist();
            const tsStr = checklistState.lastUpdated
                ? new Date(checklistState.lastUpdated).toLocaleString('en-CA', {{ month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }})
                : 'main';
            setGitStatusBadge(`✓ Synced with Git (${{tsStr}})`, 'green');
        }}

        // Commit & Save updated luggage_checklist.json directly to GitHub REST API + Cloud Relay
        async function commitChecklistToGit() {{
            const patIn = document.getElementById('chk-github-pat-input');
            const authIn = document.getElementById('chk-commit-author-input');
            if (patIn && patIn.value.trim()) checklistSessionToken = patIn.value.trim();
            if (authIn && authIn.value.trim()) checklistState.updatedBy = authIn.value.trim();

            checklistState.lastUpdated = new Date().toISOString();
            const jsonPretty = JSON.stringify(checklistState, null, 2);
            setGitStatusBadge('☁️ Committing luggage_checklist.json to Git...', 'blue');

            let gitCommitted = false;
            if (checklistSessionToken) {{
                try {{
                    // Ensure we have the latest file SHA on main before committing
                    if (!checklistGitSha) {{
                        const shaRes = await fetch(`https://api.github.com/repos/${{GIT_REPO_OWNER}}/${{GIT_REPO_NAME}}/contents/${{GIT_FILE_PATH}}?ref=${{GIT_BRANCH}}`, {{
                            headers: {{
                                'Accept': 'application/vnd.github.v3+json',
                                'Authorization': `Bearer ${{checklistSessionToken}}`
                            }}
                        }});
                        if (shaRes.ok) {{
                            const shaData = await shaRes.json();
                            checklistGitSha = shaData.sha;
                        }}
                    }}

                    const putBody = {{
                        message: `Update per-bike luggage checklist (${{checklistState.updatedBy || 'Jamie & Rosie'}})`,
                        content: utf8ToBase64(jsonPretty),
                        branch: GIT_BRANCH
                    }};
                    if (checklistGitSha) putBody.sha = checklistGitSha;

                    const putRes = await fetch(`https://api.github.com/repos/${{GIT_REPO_OWNER}}/${{GIT_REPO_NAME}}/contents/${{GIT_FILE_PATH}}`, {{
                        method: 'PUT',
                        headers: {{
                            'Accept': 'application/vnd.github.v3+json',
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${{checklistSessionToken}}`
                        }},
                        body: JSON.stringify(putBody)
                    }});

                    if (putRes.ok) {{
                        const putData = await putRes.json();
                        if (putData && putData.content && putData.content.sha) {{
                            checklistGitSha = putData.content.sha;
                        }}
                        gitCommitted = true;
                    }}
                }} catch (e) {{}}
            }}

            // Broadcast to cloud relay so all connected devices receive the updated Git checklist state immediately
            let relaySynced = false;
            try {{
                const relayRes = await fetch(`https://ntfy.sh/${{GIT_CHECKLIST_RELAY_TOPIC}}`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'text/plain;charset=utf-8' }},
                    body: JSON.stringify(checklistState)
                }});
                relaySynced = relayRes.ok;
            }} catch (e) {{}}

            checklistDirty = false;
            if (gitCommitted) {{
                setGitStatusBadge(`✓ Committed to GitHub (Rindelk/expedition-51@main) at ${{new Date().toLocaleTimeString()}}`, 'green');
            }} else if (relaySynced) {{
                setGitStatusBadge(`✓ Synced to Cloud Relay at ${{new Date().toLocaleTimeString()}} (Add 🔑 Git Auth token for direct repo commits)`, 'green');
            }} else {{
                setGitStatusBadge('⚠️ Offline — Click 🔑 Git Auth or ⬇️ .json to commit', 'orange');
            }}
        }}

        function downloadChecklistJson() {{
            const blob = new Blob([JSON.stringify(checklistState, null, 2)], {{ type: 'application/json;charset=utf-8' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'luggage_checklist.json';
            a.click();
            URL.revokeObjectURL(url);
        }}

        // Render initial Git-backed luggage checklist and pull latest from Git
        renderLuggageChecklist();
        pullChecklistFromGit(false);
    </script>
</body>
</html>
"""

for fname in ["index.html", "expedition_51_itinerary.html"]:
    out_path = os.path.join(BASE_DIR, fname)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"Wrote {out_path} ({len(html_template):,} bytes)")
