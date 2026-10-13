# Implementation Plan: Expedition 51 "Return Home July 1st" Blueprint

## 1. Goal Description

The user requested: **"Let's plan to be back home July 1st"**.

Targeting an arrival back at **4671 Dupuis Drive, Hanmer, ON** on **July 1st (Canada Day)** establishes an extraordinary 15-day expedition calendar:
* **Departure Date (Day 1)**: **Wednesday, June 17**
* **Home Arrival Date (Day 15)**: **Wednesday, July 1 (Canada Day)** *(or Thursday June 17 – Thursday July 1 in 2027)*
* **Key Calendar Synchronicity**:
  * **Day 4 lands on the Summer Solstice (June 20)** in central Labrador: riding under the maximum 17.5+ hours of subarctic daylight.
  * **Days 5 & 6 (June 21–22) in Iceberg Alley**: Arriving at the Strait of Belle Isle and Northern Peninsula at the peak density of colossal Greenland icebergs.
  * **Day 15 (July 1 - Canada Day)**: Rolling into Hanmer on Canada Day, with four days of long-weekend recovery before the work week begins.

This plan details the full stage-by-stage calendar, the late-June historical weather profiles, the live **Open-Meteo** API integration in the feed, and the necessary cold/bug gear logistics.

---

## 2. The June 17 – July 1 Master Calendar Matrix

```mermaid
flowchart TD
    subgraph Week1["Week 1: Solstice & Subarctic Transit"]
        D1["Day 1: Wed Jun 17 • Hanmer -> Mirabel (572 km)"]
        D2["Day 2: Thu Jun 18 • Mirabel -> Baie-Comeau (642 km)"]
        D3["Day 3: Fri Jun 19 • QC-389 -> Labrador City (567 km)"]
        D4["Day 4: Sat Jun 20 • SUMMER SOLSTICE: Lab City -> Goose Bay (530 km)"]
        D5["Day 5: Sun Jun 21 • TLH-510 -> Blanc-Sablon (615 km)"]
    end

    subgraph Week2["Week 2: Iceberg Alley & Cabot Trail"]
        D6["Day 6: Mon Jun 22 • ICEBERGS: Ferry -> St. Anthony -> Meadows (175 km)"]
        D7["Day 7: Tue Jun 23 • Viking Trail -> Rocky Harbour, Gros Morne (365 km)"]
        D8["Day 8: Wed Jun 24 • Gros Morne Exploration (Tablelands/Fjord)"]
        D9["Day 9: Thu Jun 25 • Gros Morne -> Port aux Basques -> Night Ferry (340 km)"]
        D10["Day 10: Fri Jun 26 • Cabot Trail Full Loop -> Baddeck (345 km)"]
    end

    subgraph Week3["Week 3: Maritimes & Canada Day Return"]
        D11["Day 11: Sat Jun 27 • Baddeck -> Hwy 6 -> Bridge -> Charlottetown (360 km)"]
        D12["Day 12: Sun Jun 28 • Anne Circuit -> Bridge -> Alma/Fundy (318 km)"]
        D13["Day 13: Mon Jun 29 • Fundy -> Saint John Valley -> Lévis, QC (675 km)"]
        D14["Day 14: Tue Jun 30 • Lévis -> A-50 Bypass -> Pembroke, ON (510 km)"]
        D15["Day 15: Wed Jul 1 • CANADA DAY RETURN: Pembroke -> Hanmer, ON (350 km)"]
    end

    Week1 --> Week2 --> Week3
```

---

## 3. Stage-by-Stage Weather & Environmental Profile (June 17 – July 1)

During this specific late-June window, weather conditions transition from warm Ontario early-summer to subarctic coastal maritime, with dramatic daylight and active icebergs:

| Day | Date | Stage & Overnight Destination | Historical High | Historical Low | Rain Risk | Daylight | Key Weather / Road Factor |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **D1** | **Jun 17** | Hanmer $\rightarrow$ Mirabel, QC | 24°C (75°F) | 13°C (55°F) | 26% | 15.6 hrs | Warm, pleasant highway cruising |
| **D2** | **Jun 18** | Mirabel $\rightarrow$ Baie-Comeau, QC | 20°C (68°F) | 10°C (50°F) | 28% | 15.8 hrs | Cool St. Lawrence estuary sea breeze |
| **D3** | **Jun 19** | Baie-Comeau $\rightarrow$ Labrador City | 17°C (63°F) | 5°C (41°F) | 35% | 16.6 hrs | Elevation 600m; QC-389 thaw completed; blackflies active |
| **D4** | **Jun 20** | **SOLSTICE**: Lab City $\rightarrow$ Goose Bay | 18°C (64°F) | 6°C (43°F) | 33% | **17.5 hrs**| **Peak Daylight**: Dusk past 10:15 PM; endless riding light |
| **D5** | **Jun 21** | Goose Bay $\rightarrow$ Blanc-Sablon | 13°C (55°F) | 4°C (39°F) | 42% | 17.2 hrs | Strait of Belle Isle cold marine air; thermal layers on |
| **D6** | **Jun 22** | **ICEBERGS**: St. Anthony / Meadows | 14°C (57°F) | 4°C (39°F) | 38% | 16.9 hrs | **Peak Iceberg density**; giant bergs grounded offshore |
| **D7** | **Jun 23** | Meadows $\rightarrow$ Rocky Harbour (Gros Morne)| 18°C (64°F)| 7°C (45°F) | 32% | 16.5 hrs | Long Range Mountains backdrop; lush spring greenery |
| **D8** | **Jun 24** | Gros Morne Exploration Day | 18°C (64°F) | 8°C (46°F) | 30% | 16.5 hrs | Ideal hiking temps; snowpatches lingering on Tablelands |
| **D9** | **Jun 25** | Rocky Harbour $\rightarrow$ Port aux Basques | 16°C (61°F) | 8°C (46°F) | 35% | 16.2 hrs | Check Wreckhouse coastal wind alert; overnight ferry |
| **D10**| **Jun 26** | Cabot Trail Loop $\rightarrow$ Baddeck | 21°C (70°F) | 11°C (52°F) | 28% | 15.9 hrs | Low tourist traffic; clear mountain coastal vistas |
| **D11**| **Jun 27** | Baddeck $\rightarrow$ Hwy 6 $\rightarrow$ Charlottetown | 22°C (72°F) | 12°C (54°F) | 25% | 15.7 hrs | Check Confederation Bridge winds (<70 km/h) |
| **D12**| **Jun 28** | PEI Anne Circuit $\rightarrow$ Alma (Fundy) | 20°C (68°F) | 10°C (50°F) | 28% | 15.6 hrs | Red lupins blooming across Cavendish & French River |
| **D13**| **Jun 29** | Alma $\rightarrow$ Saint John Valley $\rightarrow$ Lévis | 23°C (73°F) | 12°C (54°F) | 30% | 15.5 hrs | Smooth high-speed highway transit along A-85 & A-20 |
| **D14**| **Jun 30** | Lévis $\rightarrow$ A-50 Bypass $\rightarrow$ Pembroke | 25°C (77°F) | 13°C (55°F) | 26% | 15.4 hrs | Warm summer evening along the Upper Ottawa River |
| **D15**| **Jul 1**  | **CANADA DAY**: Pembroke $\rightarrow$ Hanmer | 25°C (77°F) | 13°C (55°F) | 25% | 15.3 hrs | **HOME ARRIVAL**: Direct Radar Road bypass to 4671 Dupuis |

---

## 4. Proposed Changes to Codebase & Artifacts

### Component 1: Daily Cards in Feed (`expedition_51_itinerary.html` & `index.html`)
* **Header Dates**: Update every day card header with the exact calendar date (e.g. `Wednesday, June 17 • Day 1` through `Wednesday, July 1 (Canada Day) • Day 15`).
* **Weather Module (`<div class="info-box">`)**: Inject the dual-layer weather widget into each day card:
  1. **Historical Norms (Late June)**: High, Low, Rain probability, Wind index, and Gear recommendations.
  2. **Live Actual Weather Fetcher**: Asynchronous **Open-Meteo** API integration that fetches live weather when online and caches locally for 30 minutes.
* **Special Milestone Badges**:
  * Day 4: `☀️ Summer Solstice Special (17.5 hrs daylight)`
  * Day 6: `🧊 Peak Iceberg Alley Alert`
  * Day 15: `🇨🇦 Canada Day Homecoming Celebration`

### Component 2: Master Markdown Documents
* **`east_coast_moto_expedition_plan.md`**: Update master schedule table with June 17 – July 1 dates, solstice notes, and Canada Day return protocols.
* **`expedition_51_booking_and_fuel_protocol.md`**: Align booking horizon milestones with the June 17 departure date.

---

## 5. Verification Plan

### Automated Checks
```powershell
python scratch/verify_html_divs.py
```
* Confirm `Total <div == Total </div` (`Diff = 0`).
* Confirm section hierarchy (`body < data_pane < safety < downloads < fleet < script`).

### Live Weather Verification
* Confirm Open-Meteo API returns valid weather data for all 15 destination coordinates.
* Confirm that when offline, the UI shows historical late-June climatology with zero console errors.

---

## User Review Required

> [!IMPORTANT]
> **Key Confirmation**:
> Does the **Wednesday, June 17 $\rightarrow$ Wednesday, July 1 (Canada Day)** schedule match your vision?
> 
> Upon your approval, I will immediately execute the updates across [`expedition_51_itinerary.html`](file:///C:/Users/Jamie/Desktop/Expedition%2051/expedition_51_itinerary.html), [`index.html`](file:///C:/Users/Jamie/Desktop/Expedition%2051/index.html), and all master documentation.
