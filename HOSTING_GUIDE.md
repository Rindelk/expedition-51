# Expedition 51: Global Hosting & Live Deployment Guide
### Account: Rindelk • Repository: `expedition-51` • 100% Free 24/7 Global Access

Your Expedition 51 itinerary, road-snapped Leaflet map, Master Gantt Chart, and GPS assets can be accessed globally on any smartphone, tablet, or computer.

---

## 1. Primary Method: 24/7 Global GitHub Pages Hosting ⭐ *(Recommended)*

Because Expedition 51 is a client-side web application consisting of pure HTML, CSS, JavaScript, and static download assets (`.gpx`, `.kml`, `.csv`), it runs directly on GitHub's global edge network (Fastly CDN) with **zero server costs, zero router configuration, and zero PC uptime**.

### Key Repository Links
* **Your GitHub Repository**: [https://github.com/Rindelk/expedition-51](https://github.com/Rindelk/expedition-51)
* **Your Live 24/7 Web App**: [https://rindelk.github.io/expedition-51/](https://rindelk.github.io/expedition-51/)
* **Direct GPX Navigation Download**: [https://rindelk.github.io/expedition-51/east_coast_adv_loop.gpx](https://rindelk.github.io/expedition-51/east_coast_adv_loop.gpx)

---

### Initial Setup (5 Minutes)
1. **Initialize & Push Your Project**:
   * Double-click **`Deploy_To_GitHub.bat`** inside your `Desktop\Expedition 51` folder.
   * If prompted, sign in via the standard GitHub Credential Manager web popup.
   * The script automatically stages all 18 stage tracks, 203 POIs, and day cards, creating the `main` branch and pushing everything to your repo.
2. **Enable GitHub Pages**:
   * Navigate to: [https://github.com/Rindelk/expedition-51/settings/pages](https://github.com/Rindelk/expedition-51/settings/pages)
   * Under **Build and deployment ➔ Source**:
     - Choose: **Deploy from a branch**
     - Under **Branch**: Select **`main`** and folder **`/(root)`**
     - Click **Save**
3. **Live Worldwide**:
   * In ~45 seconds, your live interactive tour is active at:
     $$\mathbf{https://rindelk.github.io/expedition-51/}$$

---

### How to Update the Package (Routine Updates)
Whenever you adjust route coordinates, hotel bookings, ferry times, or saddle timing:
1. **Double-click `Update_GitHub.bat`** on your Desktop.
2. The script automatically:
   - Synchronizes `index.html` with your latest `expedition_51_itinerary.html`.
   - Stages all modified files (`git add .`).
   - Prompts for an optional commit note (or press Enter for an automatic timestamp).
   - Pushes directly to GitHub (`git push origin main`).
3. GitHub Pages automatically compiles and deploys the new version within 30 to 45 seconds worldwide.
4. *Tip for Mobile Viewers*: Simply drag down on iPhone/Android to refresh and receive the latest data.

---

## 2. Alternative Method: Local LAN & Direct Port Forwarding (Without Cloud Services)

If you wish to test locally on your home Wi-Fi or run directly from your PC without third-party cloud hosting:

### A. Local Home Wi-Fi Sharing (Zero Setup)
1. Any phone or tablet connected to your home Wi-Fi can view the map directly at your PC's local IP address:
   `http://<Your-LAN-IP>:8080` (e.g. `http://192.168.1.145:8080`)
2. Useful for reviewing routes in your garage or living room before departures.

### B. Direct Router Port Forwarding (Self-Hosting from PC)
If you wish to self-host directly from your PC over the public internet without Cloudflare:
1. **Windows Firewall**:
   - Open PowerShell as Administrator and run:
     ```powershell
     New-NetFirewallRule -DisplayName "Expedition 51 Port 8080" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow
     ```
2. **Router Port Forwarding**:
   - Log into your home router admin console (`192.168.1.1` or `10.0.0.1`).
   - Under **Port Forwarding / NAT Rules**, add:
     - **External Port**: `8080` (TCP)
     - **Internal IP**: Your computer's local IP address (`192.168.1.145`)
     - **Internal Port**: `8080` (TCP)
3. **Public Access**:
   - Visitors access via `http://<your-public-ip>:8080`.
   - *Note*: Your PC must remain powered on and awake for visitors to connect.

---

## 3. Downloads & Navigation Sharing

When anyone visits your live site via [https://rindelk.github.io/expedition-51/](https://rindelk.github.io/expedition-51/), they can:
* Click the **GPX Master Track** button to download the 18 continuous stage tracks directly to their Garmin Zumo, BMW Navigator, or phone.
* Click the **KML Color Track** button to load the entire visual loop into Google Earth, OsmAnd, or Organic Maps.
* Click the **POI Database (CSV)** button to view all 203 points of interest with octane ratings, coordinates, and phone numbers.
