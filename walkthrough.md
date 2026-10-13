# Walkthrough: 18-Day West Coast Viking, Split Cabot Trail & PEI Grand Loop Expedition
### Tour Dates: Wednesday, June 16 – Saturday, July 3, 2027 • Saturday Homecoming Edition

The entire expedition package has been updated, audited, and synchronized for the **18-Day Master Itinerary**, incorporating:
1. **Outbound via Pembroke, Portage-du-Fort, Route 148 & Motel au P'tit Sapin (Mirabel)**: Rolls east along Highway 17 from Hanmer past North Bay to Pembroke, crossing the Ottawa River into Quebec at Portage-du-Fort via the Chenaux Generating Station dam, and staying on Route 148 East through Shawville, Quyon, Aylmer, Gatineau (Boulevard des Allumettières), Montebello, and Lachute to **Motel au P'tit Sapin** in **Mirabel, QC** for Night 1. Day 2 continues east via Route 158 to Joliette and historic Chemin du Roy (Route 138) through Trois-Rivières to Quebec City, Charlevoix, Tadoussac, and Baie-Comeau along the St. Lawrence North Shore.
2. **Category & Button Consolidation ("Attractions")**: Merged "Anne of Green Gables" (7 POIs) and "Historic Curiosities" (16 POIs) into a single consolidated category: **"Attractions" (23 POIs)**. The standalone Anne of Green Gables button has been removed from the map toolbar and replaced with `🏛️ Attractions (23)`, preserving the full curated gems total at **61 POIs** (28 Lighthouses • 23 Attractions • 10 Short Hikes).
3. **Master 18-Day Expedition Timeline & Saddle Gantt Chart**: Added a responsive, styled Gantt chart at the bottom of the feed (beneath Day 18) based on the *Daily Saddle Time, Fuel Logistics & Pacing Protocols* document. Visualizes minute-exact daily schedules across all 18 days (06:00 AM to 24:00 window), including 07:00 AM standard rollouts, 06:00 AM early ferry wakeups (Days 6 & 11), 30-minute breakfasts and lunches, 1-hour suppers, in-the-saddle riding stints, dual-octane fuel stops, and ferry crossings with rich interactive hover tooltips and day-focus clicks.
4. **Direct TLH 510 Mainline**: Follows the direct Route 510 mainline south to Blanc-Sablon.
5. **Continuous, Zero-Gap GPX Tracks**: Audited all 18 tracks in `east_coast_adv_loop.gpx`. Guaranteed strictly 0.000000 m boundary continuity between every consecutive day (1 to 18) and full loop closure back to Hanmer.
6. **Night 10 Overnight Marine Atlantic Ferry Stateroom**: Ride the scenic Codroy Valley to Cape Anguille and Cape Ray Lighthouses, board the 23:45 overnight ferry in Port aux Basques, and sleep in a private 2-berth en-suite stateroom cabin aboard the MV Highlanders.
7. **Day 11 Morning 07:00 AM Disembarkation Jump**: Roll off the ferry at 07:00 AM sharp into North Sydney, proceed over Seal Island Bridge to St. Ann's, begin the Cabot Trail along St. Ann's Bay, climb Cape Smokey to Neil's Harbour Lighthouse, and camp at **Broad Cove Campground** in Ingonish Beach.
8. **PEI Grand Island Loop & Cavendish Beach Oceanfront Camp**: Enter PEI toll-free across Confederation Bridge on Day 13, ride Victoria-by-the-Sea, French River look-off, Cape Tryon Lighthouse, and PEI National Park. Camp at **Cavendish Campground**. Depart Day 14 via Seacow Head Lighthouse, Cape Enrage, and Hopewell Rocks to Fundy National Park.
9. **Comprehensive 28 Coastal Lighthouses & 72 Gas Stations**: Full database of 203 POIs including 28 historic coastal lighthouses, 72 fuel stations (primary + backup with 91 AKI availability), 23 attractions, 10 short hikes, 19 primary lodgings, 18 fallback hotels, 14 parks, 7 ferries/bridges, and 12 scenic sights.
10. **Three-Day Return Leg (~431 km Daily Average)**: Returning from Edmundston in three manageable days: Day 16 to Drummondville (437 km), Day 17 to Pembroke (502 km), and Day 18 to Hanmer Home Base (355 km).
11. **Saturday, July 3, 2027 Homecoming**: Allowing Sunday, July 4, 2027 as a full recovery day at home before returning to regular weekday schedules.

---

## 1. 🌟 Master Feature Architecture

1. **Category & Toolbar Consolidation**:
   - "Anne of Green Gables" has been unified with "Historic Curiosities" into **"Attractions" (23 POIs total)**.
   - The toolbar button `🏛️ Attractions (23)` toggles all 23 sites seamlessly.
   - ⭐ **All Curated Gems (61)** aggregates 28 Lighthouses + 23 Attractions + 10 Short Hikes.
   - Clean 100% pass on automated DOM toggle click tests (`test_filter_clicks.js`).

2. **Master 18-Day Gantt Chart Component in Feed**:
   - Situated at the bottom of the feed in `#data-pane` immediately following Day 18.
   - Proportional time blocks with distinct color coding:
     - 🟦 **In-the-Saddle Riding**: Exact duration in hours/minutes and leg kilometers.
     - 🟧 **Meals**: 30m breakfast (07:00–07:30 AM standard; 06:15–06:45 AM ferry days), 30m lunch (12:00–01:15 PM window), 1h evening supper (06:00–07:30 PM).
     - 🟥 **Fuel Stops**: 15–25m primary gas stops + bike stretch intervals.
     - 🟪 **Attractions & Sights**: Coastal stops, cultural centres, and hikes.
     - 🔷 **Ferries**: MV Qajaq W crossing (Belle Isle) and Marine Atlantic overnight sailing (Cabot Strait).
     - 🟩 **Lodging / Camp**: Arrival, check-in, tent pitching, and evening motorcycle checks.
   - Interactive hover tooltips provide departure/arrival times, saddle minutes, fuel stop details, and octane notes.
   - Clicking any day row automatically zooms the map to that day and scrolls directly to its day card.

3. **Saturday, July 3 Homecoming**:
   - Concluding on **Saturday afternoon** provides **Sunday, July 4, 2027** as a dedicated rest and maintenance day at home before the workweek begins.

4. **Night 10 Overnight Ferry Stateroom & Cabot Trail Jump**:
   - Ride the Codroy Valley to Cape Anguille and Cape Ray Lighthouses, board the 23:45 overnight ferry in Port aux Basques, and rest in a private 2-berth en-suite stateroom cabin.
   - Roll off at 07:00 AM Saturday morning refreshed and ready to ride, traversing Cape Smokey and Neil's Harbour before afternoon traffic, camping at Broad Cove on Saturday night and Chéticamp on Sunday night.

5. **Dual-Rider Budget Summary**:
   - **~$5,450 CAD total** for two riders combined (~$2,450 CAD savings relative to an all-hotel itinerary).

---

## 2. 🗺️ Day-by-Day Google Maps Turn-by-Turn Links

| Day | Date | From (Start Point) | To (End Point) | Direct Google Maps Driving Link |
| :---: | :--- | :--- | :--- | :---: |
| **1** | Wed Jun 16 | 4671 Dupuis Dr, Hanmer, ON | Motel au P'tit Sapin, Mirabel, QC | [Open Day 1 Route ↗](https://www.google.com/maps/dir/4671+Dupuis+Drive,+Hanmer,+ON+P3P+0B3,+Canada/Pembroke,+Ontario/Portage-du-Fort,+Quebec/45.484148,-75.6479648/Masson-Angers,+Gatineau,+QC/45.6434004,-74.8182866/45.6258796,-74.434645/Motel+au+P'tit+Sapin,+16033+Du,+Bd+Cur%C3%A9-Labelle,+Mirabel,+QC+J7J+2G6/@45.5217157,-75.867381,9.75z/data=!4m44!4m43!1m5!1m1!1s0x4d2f09cab13f135d:0x51f92cbedd860d29!2m2!1d-80.8829995!2d46.6562318!1m5!1m1!1s0x4cd14d1b8e6d6243:0xc898283285e5b85c!2m2!1d-77.1108826!2d45.8266513!1m5!1m1!1s0x4cd17744624d0c11:0x667f02175389f72!2m2!1d-76.660131!2d45.593286!1m5!3m4!1m2!1d-75.1046879!2d45.6068802!3s0x4cce5c980c9e572b:0x84b028c21b4a6cfa!1m0!1m10!3m4!1m2!1d-74.334428!2d45.656916!3s0x4ccedbdb0d266d33:0x222bebeb3d6ecb4!3m4!1m2!1d-74.0830366!2d45.7039439!3s0x4cced58729d2e32b:0x4df0ef7491932e53!1m5!1m1!1s0x4cc8d4e4e799b587:0xa5d1ba26bd8815d7!2m2!1d-73.9663472!2d45.7347599!3e0?entry=ttu&g_ep=EgoyMDI2MTAwNy4wIKXMDSoASAFQAw%3D%3D) |
| **2** | Thu Jun 17 | Motel au P'tit Sapin, Mirabel, QC | Travelodge Baie-Comeau, QC | [Open Day 2 Route ↗](https://www.google.com/maps/dir/?api=1&origin=Motel+au+P%27tit+Sapin%2C+16033+Bd+Cur%C3%A9-Labelle%2C+Mirabel%2C+QC&destination=Travelodge+by+Wyndham+Baie-Comeau%2C+Baie-Comeau%2C+QC&waypoints=Joliette%2C+QC%7CBerthierville%2C+QC%7CTrois-Rivi%C3%A8res%2C+QC%7CRoute+138%2C+Sainte-Anne-de-Beaupr%C3%A9%2C+QC%7CBaie-Saint-Paul%2C+QC%7CTadoussac%2C+QC&travelmode=driving) |
| **3** | Fri Jun 18 | Travelodge Baie-Comeau, QC | Hotel Wabush, Lab City, NL | [Open Day 3 Route ↗](https://www.google.com/maps/dir/?api=1&origin=Travelodge+by+Wyndham+Baie-Comeau%2C+Baie-Comeau%2C+QC&destination=Hotel+Wabush%2C+Wabush%2C+NL&travelmode=driving&waypoints=Manic-5%2C+QC%7CRelais+Gabriel%2C+QC) |
| **4** | Sat Jun 19 | Hotel Wabush, Lab City, NL | Royal Inn & Suites, Goose Bay, NL | [Open Day 4 Route ↗](https://www.google.com/maps/dir/?api=1&origin=Hotel+Wabush%2C+Wabush%2C+NL&destination=Royal+Inn+%26+Suites%2C+Happy+Valley-Goose+Bay%2C+NL&travelmode=driving&waypoints=Churchill+Falls%2C+NL) |
| **5** | Sun Jun 20 | Royal Inn & Suites, Goose Bay | Northern Light Inn, L'Anse-au-Clair | [Open Day 5 Route ↗](https://www.google.com/maps/dir/?api=1&origin=Royal+Inn+%26+Suites%2C+Happy+Valley-Goose+Bay%2C+NL&destination=Northern+Light+Inn%2C+L%27Anse-au-Clair%2C+NL&travelmode=driving&waypoints=Port+Hope+Simpson%2C+NL%7CRed+Bay%2C+NL) |
| **6** | Mon Jun 21 | Northern Light Inn, L'Anse-au-Clair | St. Anthony & Snorri Cabins (Hay Cove) | [Open Day 6 Route ↗](https://www.google.com/maps/dir/?api=1&origin=Northern+Light+Inn%2C+L%27Anse-au-Clair%2C+NL&destination=Snorri+Cabins%2C+Hay+Cove%2C+NL&travelmode=driving&waypoints=Blanc-Sablon+Ferry+Terminal%2C+QC%7CSt.+Barbe+Ferry+Terminal%2C+NL%7CGrenfell+Historic+Properties%2C+St.+Anthony%2C+NL%7CFishing+Point+Lighthouse%2C+St.+Anthony%2C+NL) |
| **7** | Tue Jun 22 | Snorri Cabins (Viking Day Loop) | Snorri Cabins (Meadows & Cape Onion) | [Open Day 7 Route ↗](https://www.google.com/maps/dir/?api=1&origin=Snorri+Cabins%2C+Hay+Cove%2C+NL&destination=Snorri+Cabins%2C+Hay+Cove%2C+NL&travelmode=driving&waypoints=L%27Anse+aux+Meadows+National+Historic+Site%2C+NL%7CNorstead%2C+Hay+Cove%2C+NL%7CCape+Onion%2C+NL) |
| **8** | Wed Jun 23 | Snorri Cabins, Hay Cove, NL | Gros Morne / Norris Point KOA | [Open Day 8 Route ↗](https://www.google.com/maps/dir/?api=1&origin=Snorri+Cabins%2C+Hay+Cove%2C+NL&destination=Gros+Morne+%2F+Norris+Point+KOA+Holiday%2C+Norris+Point%2C+NL&travelmode=driving&waypoints=Point+Riche+Lighthouse%2C+Port+au+Choix%2C+NL) |
| **9** | Thu Jun 24 | Gros Morne KOA Holiday | Green Point Campground, Gros Morne | [Open Day 9 Route ↗](https://www.google.com/maps/dir/?api=1&origin=Gros+Morne+%2F+Norris+Point+KOA+Holiday%2C+Norris+Point%2C+NL&destination=Green+Point+Campground%2C+Rocky+Harbour%2C+NL&travelmode=driving&waypoints=Tablelands+Trailhead%2C+Woody+Point%2C+NL%7CTrout+River%2C+NL) |
| **10** | Fri Jun 25 | Green Point Campground, NL | Port aux Basques (Overnight Ferry Cabin) | [Open Day 10 Route ↗](https://www.google.com/maps/dir/?api=1&origin=Green+Point+Campground%2C+Rocky+Harbour%2C+NL&destination=Marine+Atlantic+Ferry+Terminal%2C+Port+aux+Basques%2C+NL&travelmode=driving&waypoints=Cape+Anguille+Lighthouse%2C+NL%7CCape+Ray+Lighthouse%2C+NL) |
| **11** | Sat Jun 26 | North Sydney Ferry Dock (7 AM Jump) | Broad Cove Camp, Highlands NP | [Open Day 11 Route ↗](https://www.google.com/maps/dir/?api=1&origin=Marine+Atlantic+Ferry+Terminal%2C+North+Sydney%2C+NS&destination=Broad+Cove+Campground%2C+Ingonish+Beach%2C+NS&travelmode=driving&waypoints=St.+Ann%27s%2C+NS%7CCape+Smokey+Provincial+Park%2C+NS%7CNeils+Harbour+Lighthouse%2C+NS) |
| **12** | Sun Jun 27 | Broad Cove Camp, Ingonish Beach | Chéticamp Camp, Highlands NP | [Open Day 12 Route ↗](https://www.google.com/maps/dir/?api=1&origin=Broad+Cove+Campground%2C+Ingonish+Beach%2C+NS&destination=Ch%C3%A9ticamp+Campground%2C+Ch%C3%A9ticamp%2C+NS&travelmode=driving&waypoints=Meat+Cove+Welcome+Center%2C+Meat+Cove%2C+NS%7CSkyline+Trail%2C+Cabot+Trail%2C+NS) |
| **13** | Mon Jun 28 | Chéticamp Camp, Highlands NP | Cavendish Campground (PEI National Park) | [Open Day 13 Route ↗](https://www.google.com/maps/dir/?api=1&origin=Ch%C3%A9ticamp+Campground%2C+Ch%C3%A9ticamp%2C+NS&destination=Cavendish+Campground%2C+Prince+Edward+Island+National+Park%2C+PE&travelmode=driving&waypoints=Canso+Causeway%2C+Port+Hastings%2C+NS%7CCape+Jourimain%2C+Bayfield%2C+NB%7CVictoria-by-the-Sea%2C+PE%7CFrench+River%2C+PE%7CCape+Tryon+Lighthouse%2C+PE%7CAnne+of+Green+Gables+Heritage+Place%2C+Cavendish%2C+PE%7CNorth+Rustico+Harbour%2C+PE) |
| **14** | Tue Jun 29 | Cavendish Campground, PEI | Fundy National Park Headquarters | [Open Day 14 Route ↗](https://www.google.com/maps/dir/?api=1&origin=Cavendish+Campground%2C+Prince+Edward+Island+National+Park%2C+PE&destination=Fundy+National+Park+Headquarters+Campground%2C+Alma%2C+NB&travelmode=driving&waypoints=Seacow+Head+Lighthouse%2C+Borden-Carleton%2C+PE%7CCape+Jourimain%2C+Bayfield%2C+NB%7CCape+Enrage+Lighthouse%2C+NB%7CThe+Hopewell+Rocks%2C+Hopewell+Cape%2C+NB) |
| **15** | Wed Jun 30 | Fundy National Park Headquarters | de la République PP, Edmundston, NB | [Open Day 15 Route ↗](https://www.google.com/maps/dir/45.5968321,-64.9521371/45.5154872,-65.2968873/45.4310118,-65.3693319/45.4262806,-65.392869/45.4257948,-65.4093835/45.4120034,-65.4225108/45.4015382,-65.4601292/45.2733153,-66.063308/46.2970,-67.5280/47.4353,-68.3904) |
| **16** | Thu Jul 01 | de la République PP, Edmundston | Camping des Voltigeurs, Drummondville | [Open Day 16 Route ↗](https://www.google.com/maps/dir/?api=1&origin=Parc+provincial+de+la+R%C3%A9publique%2C+Edmundston%2C+NB&destination=Camping+des+Voltigeurs%2C+Drummondville%2C+QC&waypoints=Rivi%C3%A8re-du-Loup%2C+QC&travelmode=driving) |
| **17** | Fri Jul 02 | Camping des Voltigeurs, Drummondville | Best Western Pembroke Inn, ON | [Open Day 17 Route ↗](https://www.google.com/maps/dir/?api=1&origin=Camping+des+Voltigeurs%2C+Drummondville%2C+QC&destination=Best+Western+Pembroke+Inn+%26+Conference+Centre%2C+Pembroke%2C+ON&waypoints=Autoroute+30%2C+Boucherville%2C+QC%7CAutoroute+30%2C+Beauharnois%2C+QC%7CCasselman%2C+ON%7CManotick%2C+Ottawa%2C+ON%7CCarleton+Place%2C+ON&travelmode=driving) |
| **18** | Sat Jul 03 | Best Western Pembroke Inn, ON | 4671 Dupuis Dr, Hanmer, ON | [Open Day 18 Route ↗](https://www.google.com/maps/dir/?api=1&origin=Best+Western+Pembroke+Inn+%26+Conference+Centre%2C+Pembroke%2C+ON&destination=4671+Dupuis+Dr%2C+Hanmer%2C+ON&waypoints=North+Bay%2C+ON&travelmode=driving) |

---

## 3. 📅 Earliest Moments to Book (2026 / 2027 Master Schedule)

| Category / Destination | Venues Covered | Earliest Moment to Book | Booking Agency / Portal | Operational Strategy & Tips |
| :--- | :--- | :---: | :--- | :--- |
| 🏕️ **KOA Campground** | Gros Morne KOA (Day 8) | **June 2026** (Rolling 12 Mos) | [koa.com](https://koa.com/) | 12-month rolling window. Book tent site with power near laundry & heated pool. |
| 🏞️ **Parks Canada (NL)** | Green Point Campground, Gros Morne NP (Day 9) | **Jan 15, 2027 @ 8:00 AM NST (6:30 AM EST)** | [reservation.pc.gc.ca](https://reservation.pc.gc.ca/) | Staggered NL provincial release. Log in 15 min early for oceanfront clifftop sites. |
| 🏨 **Mirabel Motel (QC)** | Motel au P'tit Sapin, Mirabel (Day 1) | **Fall 2026 (3–6 Mos Ahead)** | [Direct Booking](https://www.motelauptitsapin.com/) | Route 117 drive-up room motel. Exterior bike parking, fast jump to R-158. |
| 🏞️ **Parks Canada (NS)** | Broad Cove (Day 11) & Chéticamp (Day 12), Cape Breton Highlands NP | **Jan 18, 2027 @ 8:00 AM AST (7:00 AM EST)** | [reservation.pc.gc.ca](https://reservation.pc.gc.ca/) | Staggered NS provincial release. Oceanfront beach sites at Broad Cove sell out fast. |
| 🏞️ **Parks Canada (PEI & NB)** | Cavendish Campground, PEI NP (Day 13) & Fundy NP Headquarters (Day 14) | **Jan 19, 2027 @ 8:00 AM AST (7:00 AM EST)** | [reservation.pc.gc.ca](https://reservation.pc.gc.ca/) | Staggered PEI/NB provincial release. Red sand dune sites at Cavendish & cliff sites at Fundy. |
| 🍁 **NB Provincial Parks** | de la République Provincial Park, Edmundston (Day 15) | **Feb 1, 2027 @ 9:00 AM AST (8:00 AM EST)** | [parcsnbparks.info](https://www.parcsnbparks.info/) | Annual Parcs NB summer reservation launch. Wooded riverside sites. |
| 🏕️ **Sépaq (QC)** | Camping des Voltigeurs, Drummondville (Day 16) | **November 2026** (4–6 Mos Ahead) | [sepaq.com/pq/vol](https://www.sepaq.com/pq/vol/) | Annual Sépaq summer launch. Tranquil riverside sites. |
| ⛴️ **Marine Atlantic Ferry** | Port aux Basques, NL ➔ North Sydney, NS (Day 10) | **Late Fall 2026 (Oct/Nov 2026 - 7–8 Mos Ahead)** | [marineatlantic.ca](https://www.marineatlantic.ca/) | Summer schedule opens before year-end. **Book 2 motorcycles + private 2-berth en-suite stateroom cabin immediately!** |
| ⛴️ **Labrador Marine Ferry** | MV Qajaq W: Blanc-Sablon ➔ St. Barbe (Day 6) | **March 1, 2027** | [mylmi.labradormarine.com](https://mylmi.labradormarine.com/) | Summer schedule opens March 1. Motorcyclists board first. |
| 🌉 **Confederation Bridge** | Cape Jourimain, NB ➔ Borden-Carleton, PEI (Days 13 & 14) | **No Reservation Needed** | [confederationbridge.com](https://www.confederationbridge.com/) | **Inbound Day 13 is 100% Toll-Free!** Exit toll collected only upon leaving PEI on Day 14 (~$20.25/bike). |
| ⚔️ **Viking Ocean Cabins** | Snorri Cabins / Valhalla Lodge, L'Anse aux Meadows (Days 6–7) | **Summer/Fall 2026 (8–10 Mos Ahead)** | [valhalla-lodge.com](https://valhalla-lodge.com/) | Only 4 rustic cabins exist in Hay Cove! Critical bottleneck; book immediately. |
| 🏨 **Remote Outposts & Hotels**| Baie-Comeau (Day 2), Lab City (Day 3), Goose Bay (Day 4), L'Anse-au-Clair (Day 5), Pembroke (Day 17) | **Fall 2026 (6–8 Mos Ahead)** | Direct Hotel Portals | Remote mining and highway hubs book up fast; secure flexible rates early. |

---

## 4. 🌐 24/7 Global GitHub Pages Deployment (Account: Rindelk)

The entire expedition package has been initialized as a clean Git repository on branch `main` and linked to `https://github.com/Rindelk/expedition-51.git`.

### Repository & Live Links
* **GitHub Repository**: [https://github.com/Rindelk/expedition-51](https://github.com/Rindelk/expedition-51)
* **Live 24/7 Web App**: [https://rindelk.github.io/expedition-51/](https://rindelk.github.io/expedition-51/)
* **Direct GPX Navigation Download**: [https://rindelk.github.io/expedition-51/east_coast_adv_loop.gpx](https://rindelk.github.io/expedition-51/east_coast_adv_loop.gpx)

### Initial Push Execution
1. Double-click [`Deploy_To_GitHub.bat`](file:///C:/Users/Jamie/Desktop/Expedition%2051/Deploy_To_GitHub.bat) in your `Desktop\Expedition 51` folder.
2. Sign in via the one-time GitHub Credential Manager web popup on your desktop.
3. Enable GitHub Pages in your repo settings: [https://github.com/Rindelk/expedition-51/settings/pages](https://github.com/Rindelk/expedition-51/settings/pages) (Source: `Deploy from a branch` ➔ Branch: `main` / `/(root)` ➔ `Save`).

### Routine 1-Click Updates
Whenever you update routes, schedules, or notes:
1. Double-click [`Update_GitHub.bat`](file:///C:/Users/Jamie/Desktop/Expedition%2051/Update_GitHub.bat).
2. It automatically synchronizes `index.html`, stages modified files, commits with a timestamp, and pushes to GitHub.
3. Within 30 to 45 seconds, GitHub Pages automatically deploys the updated live site worldwide.

---

## 5. 🎛️ Interactive Drag-to-Resize Divider Gutter (`#resizer-gutter`)

In accordance with the Moto ADV Expedition Master skill standard:
- Replaced the previous split toggle buttons (`◫ 50/50`, `🗺️ Map`, `📋 Feed`) in the navigation bar with an intuitive, drag-to-resize divider gutter located directly between the map and feed panes.
- **Drag Interaction**: Click and drag the vertical gutter left or right to seamlessly adjust the map-to-feed width ratio with live map resizing.
- **Double-Click Reset**: Double-clicking the gutter resets the view to a perfect 50/50 split.
- **State Persistence**: The user's preferred layout width is safely preserved in browser storage.
- **Desktop Exclusive**: Active on screens `> 850px` for seamless side-by-side trip planning and analysis.
- **Mobile Mode**: On screens `<= 850px`, the gutter gracefully hides in favor of the dedicated full-screen mobile app layout.

---

## 6. 📱 Native Mobile App Architecture (`<= 850px`)

To eliminate vertical split-screen cramping on smartphones, the dashboard transforms into a native-feeling mobile web application on mobile viewports:

1. **Dedicated Full-Height Views via Fixed Bottom Nav**:
   - Replaced cramped vertical stacking with four dedicated, full-screen views controlled by a persistent thumb-friendly bottom navigation bar:
     - 🗺️ **Map**: Edge-to-edge interactive Leaflet map taking 92%+ of screen height.
     - 📋 **Itinerary**: Complete feed of all 18 day cards, turn-by-turn links, and logistics tables.
     - ⏱️ **Timeline**: Direct access to the master 18-day interactive Gantt chart.
     - 📥 **Files**: 1-tap downloads for GPX tracks, KML files, CSV POI tables, and guidebooks.
2. **Horizontal Swipeable Filter Chips**:
   - The map category filter bar condenses into a clean single-row, horizontally scrollable tray of touch chips (~38px height).
   - Keeps map controls readily accessible without occluding route lines or satellite imagery.
3. **Sticky Quick-Day Jumper**:
   - A sticky horizontal pill bar (`Day 1` through `Day 18`) docks to the top of the Itinerary view for instant jumping to any leg of the journey.
4. **1-Tap Cross-View Route Focus**:
   - Tapping any route card's **"Focus on Map"** button on mobile automatically switches active tabs to the **Map**, smoothly flies to that leg's bounding box, highlights the route track, and displays a temporary floating notification badge (`🗺️ Focused on Day X`).
5. **Mobile PWA & Viewport Standards**:
   - Includes `viewport-fit=cover`, Apple mobile web app capability (`apple-mobile-web-app-capable`), status bar customization, and theme-color meta headers for seamless "Add to Home Screen" smartphone usage.
6. **Dual-View Mobile Timeline & Freeze-Pane Gantt Chart**:
   - **📱 Daily Schedule (Mobile Default)**: High-contrast vertical chronological agenda for each day with swipeable day selector chips (`[Day 1]` through `[Day 18]`). Displays minute-exact riding stints, gas stops (with 91 AKI availability), meals, and accommodations with 1-tap **"Focus Day on Map"** and **"View Itinerary Details"** buttons.
   - **📊 Full 18-Day Grid with Freeze-Pane**: The left `Day & Date` column stays pinned (`position: sticky; left: 0`) while panning horizontally across the 06:00 to 24:00 time scale, preventing row disorientation. Tapping any colored block opens an instant touch inspector popover.




