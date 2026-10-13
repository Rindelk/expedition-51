import os
import sys
import time
import socket
import re
import shutil
import threading
import subprocess
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

# Reconfigure stdout for UTF-8 and emoji support
sys.stdout.reconfigure(encoding='utf-8')

EXPEDITION_DIR = r"C:\Users\Jamie\Desktop\Expedition 51"
DEFAULT_PORT = 8080

def get_lan_ip():
    """Detect local network IP for home Wi-Fi access."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Does not actually send data; used to query routing table
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def find_open_port(start_port=DEFAULT_PORT):
    """Find an available port starting from start_port."""
    port = start_port
    while port < start_port + 50:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
        port += 1
    return start_port

def copy_to_clipboard(text):
    """Copy text to Windows clipboard via clip.exe."""
    try:
        p = subprocess.Popen(['clip'], stdin=subprocess.PIPE, close_fds=True)
        p.communicate(input=text.strip().encode('utf-16'))
        return True
    except Exception:
        return False

def print_qr(url):
    """Print ASCII QR code to console if qrcode is available."""
    try:
        import qrcode
        qr = qrcode.QRCode(border=1)
        qr.add_data(url)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
    except Exception:
        pass

def main():
    os.chdir(EXPEDITION_DIR)
    
    # 1. Sync index.html with expedition_51_itinerary.html
    src_html = os.path.join(EXPEDITION_DIR, "expedition_51_itinerary.html")
    dst_html = os.path.join(EXPEDITION_DIR, "index.html")
    if os.path.exists(src_html):
        shutil.copy2(src_html, dst_html)

    # 2. Pick port and LAN IP
    port = find_open_port(DEFAULT_PORT)
    lan_ip = get_lan_ip()

    # 3. Start local HTTP server in background thread
    class CustomHandler(SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.send_header('Access-Control-Allow-Origin', '*')
            super().end_headers()

        def log_message(self, format, *args):
            # Suppress normal asset log spam, show only key page hits
            msg = format % args
            if "GET / " in msg or "GET /index.html" in msg or "GET /east_coast_adv_loop.gpx" in msg:
                print(f"[{time.strftime('%H:%M:%S')}] 📥 Visitor: {msg}")

    httpd = ThreadingHTTPServer(('0.0.0.0', port), CustomHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    print("=" * 72)
    print("🏍️  EXPEDITION 51: STARTING LOCAL & PUBLIC ONLINE SERVER")
    print("=" * 72)
    print(f"[*] Local HTTP Server listening on port {port}...")
    print(f"[*] Connecting to Cloudflare global network for free public HTTPS tunnel...")

    # 4. Launch cloudflared tunnel
    cloudflared_cmd = ["cloudflared", "tunnel", "--url", f"http://localhost:{port}"]
    tunnel_proc = subprocess.Popen(
        cloudflared_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    public_url = None
    start_time = time.time()

    # Read tunnel output to extract the trycloudflare.com URL
    while time.time() - start_time < 20:
        line = tunnel_proc.stdout.readline()
        if not line:
            break
        m = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
        if m:
            public_url = m.group(0)
            break

    # 5. Display banner and share links
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 72)
    print("🏍️  EXPEDITION 51 INTERACTIVE DASHBOARD IS LIVE ONLINE!")
    print("=" * 72)
    print("")

    if public_url:
        copied = copy_to_clipboard(public_url)
        print("🌐 PUBLIC INTERNET LINK (Share with anyone in the world):")
        print(f"   👉 {public_url}")
        if copied:
            print("   ✅ (URL COPIED TO CLIPBOARD! Press Ctrl+V in email or messages)")
        print("")
        print("📱 SCAN WITH SMARTPHONE CAMERA TO OPEN IMMEDIATELY:")
        print_qr(public_url)
        print("")
    else:
        print("⚠️ Could not establish Cloudflare public tunnel. Local Wi-Fi is active.")

    print("-" * 72)
    print(f"📶 LOCAL HOME WI-FI LINK (For devices on your Wi-Fi):")
    print(f"   👉 http://{lan_ip}:{port}")
    print(f"💻 LOCAL COMPUTER LINK:")
    print(f"   👉 http://localhost:{port}")
    print("=" * 72)
    print("")
    print("  [!] KEEP THIS WINDOW OPEN to keep the server and link active.")
    print("  [!] Press Ctrl+C in this window anytime to stop the server.")
    print("=" * 72)

    # 6. Open browser locally
    webbrowser.open(f"http://localhost:{port}")

    # 7. Keep running until interrupted
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Shutting down Expedition 51 server and closing tunnel...")
    finally:
        tunnel_proc.terminate()
        try:
            tunnel_proc.wait(timeout=3)
        except Exception:
            tunnel_proc.kill()
        httpd.shutdown()
        print("[✓] Server stopped cleanly. Have a great ride!")

if __name__ == "__main__":
    main()
