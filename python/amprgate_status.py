#!/usr/bin/env python3
"""
amprgate_status.py — AMPRNet Gateway Status Service
Runs on the dedicated 44Net gateway Pi (192.168.50.2)
Serves status API on port 9000 and the dashboard UI

Endpoints:
  GET  /           — Status dashboard HTML
  GET  /api/status — JSON status of tunnel, routes, system
  POST /api/tunnel/up      — Bring tunnel up (wg-quick up ampr0)
  POST /api/tunnel/down    — Bring tunnel down (wg-quick down ampr0)
  POST /api/tunnel/restart — Restart tunnel
"""

import json
import os
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

PORT = 9000
TEMPLATES = Path("/opt/amprgate/templates")
WG_INTERFACE = "ampr0"


def utcnow():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(cmd, timeout=5):
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        return r.stdout.strip(), r.returncode
    except Exception as e:
        return str(e), -1


def get_cpu_temp():
    """Read CPU temperature in Celsius."""
    for tz in Path("/sys/class/thermal").glob("thermal_zone*/temp"):
        try:
            v = int(tz.read_text().strip())
            if 10000 < v < 100000:
                return round(v / 1000, 1)
        except Exception:
            pass
    out, _ = run(["vcgencmd", "measure_temp"])
    if "temp=" in out:
        try:
            return float(out.split("=")[1].replace("'C", "").strip())
        except Exception:
            pass
    return None


def get_mem():
    """Return (used_mb, total_mb)."""
    try:
        lines = Path("/proc/meminfo").read_text().splitlines()
        info = {}
        for line in lines:
            parts = line.split()
            if len(parts) >= 2:
                info[parts[0].rstrip(":")] = int(parts[1])
        total = info.get("MemTotal", 0) // 1024
        avail = info.get("MemAvailable", 0) // 1024
        return total - avail, total
    except Exception:
        return None, None


def get_uptime():
    """Return human-readable uptime string."""
    try:
        secs = float(Path("/proc/uptime").read_text().split()[0])
        h = int(secs // 3600)
        m = int((secs % 3600) // 60)
        return f"{h}h {m}m"
    except Exception:
        return None


def get_ip_forward():
    """Check if IP forwarding is enabled."""
    try:
        val = Path("/proc/sys/net/ipv4/ip_forward").read_text().strip()
        return val == "1"
    except Exception:
        return False


def get_wg_status():
    """
    Parse `wg show ampr0 dump` output.
    Returns dict with tunnel state and peer info.
    """
    out, rc = run(["sudo", "wg", "show", WG_INTERFACE, "dump"])
    if rc != 0 or not out.strip():
        return {"tunnel": "down", "ampr_address": None,
                "last_handshake": None, "rx_bytes": 0, "tx_bytes": 0}

    lines = [l.split("\t") for l in out.strip().splitlines()]
    if not lines:
        return {"tunnel": "down", "ampr_address": None,
                "last_handshake": None, "rx_bytes": 0, "tx_bytes": 0}

    # First line is the interface itself: private_key, public_key, listen_port, fwmark
    # Subsequent lines are peers: public_key, preshared_key, endpoint,
    #                              allowed_ips, last_handshake, rx, tx, persistent_keepalive

    # Get our assigned 44.x address from the interface
    addr_out, _ = run(["ip", "addr", "show", WG_INTERFACE])
    ampr_addr = None
    for line in addr_out.splitlines():
        m = re.search(r"inet\s+(44\.\d+\.\d+\.\d+/\d+)", line)
        if m:
            ampr_addr = m.group(1)
            break

    # Parse peer line(s)
    rx_total = 0
    tx_total = 0
    last_hs = None

    for line in lines[1:]:  # skip interface line
        if len(line) >= 7:
            try:
                hs_epoch = int(line[4])
                rx_total += int(line[5])
                tx_total += int(line[6])
                if hs_epoch > 0:
                    hs_dt = datetime.fromtimestamp(hs_epoch, tz=timezone.utc)
                    age_s = int(time.time()) - hs_epoch
                    if age_s < 60:
                        last_hs = f"{age_s}s ago"
                    elif age_s < 3600:
                        last_hs = f"{age_s // 60}m ago"
                    else:
                        last_hs = hs_dt.strftime("%H:%M UTC")
            except (ValueError, IndexError):
                pass

    # Tunnel is "up" if we have an ampr address and a recent handshake
    hs_epoch_val = 0
    if len(lines) > 1 and len(lines[1]) >= 5:
        try:
            hs_epoch_val = int(lines[1][4])
        except ValueError:
            pass

    tunnel_up = ampr_addr is not None and (
        hs_epoch_val > 0 and (int(time.time()) - hs_epoch_val) < 300
    )

    return {
        "tunnel": "up" if tunnel_up else "down",
        "ampr_address": ampr_addr,
        "last_handshake": last_hs or "Never",
        "rx_bytes": rx_total,
        "tx_bytes": tx_total,
    }


def get_routes():
    """Return list of relevant routing table entries."""
    out, _ = run(["ip", "route", "show"])
    routes = []
    for line in out.splitlines():
        if "44.0.0.0" in line or "ampr0" in line:
            parts = line.split()
            net = parts[0] if parts else "?"
            via = "ampr0"
            for i, p in enumerate(parts):
                if p == "via" and i + 1 < len(parts):
                    via = parts[i + 1]
                    break
                if p == "dev" and i + 1 < len(parts):
                    via = parts[i + 1]
                    break
            routes.append({"net": net, "via": via, "ok": True})

    if not routes:
        routes.append({"net": "44.0.0.0/8", "via": "—", "ok": False})
    return routes


def build_status():
    """Build the full status JSON response."""
    wg = get_wg_status()
    cpu_temp = get_cpu_temp()
    mem_used, mem_total = get_mem()
    uptime = get_uptime()
    ip_fwd = get_ip_forward()
    routes = get_routes()

    return {
        "timestamp": utcnow(),
        "gateway_ip": "192.168.50.2",
        **wg,
        "cpu_temp": cpu_temp,
        "mem_used_mb": mem_used,
        "mem_total_mb": mem_total,
        "uptime": uptime,
        "ip_forward": ip_fwd,
        "routes": routes,
    }


def tunnel_action(action):
    """Bring the WireGuard tunnel up, down, or restart it."""
    if action == "up":
        out, rc = run(["sudo", "wg-quick", "up", WG_INTERFACE], timeout=15)
        return {"ok": rc == 0, "message": out or "Tunnel brought up" if rc == 0 else f"Error: {out}"}
    elif action == "down":
        out, rc = run(["sudo", "wg-quick", "down", WG_INTERFACE], timeout=15)
        return {"ok": rc == 0, "message": out or "Tunnel brought down" if rc == 0 else f"Error: {out}"}
    elif action == "restart":
        run(["sudo", "wg-quick", "down", WG_INTERFACE], timeout=10)
        time.sleep(1)
        out, rc = run(["sudo", "wg-quick", "up", WG_INTERFACE], timeout=15)
        return {"ok": rc == 0, "message": "Tunnel restarted" if rc == 0 else f"Error: {out}"}
    return {"ok": False, "message": "Unknown action"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # Suppress default access log noise

    def send_json(self, data, code=200):
        body = json.dumps(data, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, body, code=200):
        b = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(b))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        path = urlparse(self.path).path.rstrip("/")

        if path == "" or path == "/":
            tmpl = TEMPLATES / "index.html"
            if tmpl.exists():
                self.send_html(tmpl.read_bytes())
            else:
                self.send_html("<h1>Status page template not found</h1>", 500)

        elif path == "/api/status":
            self.send_json(build_status())

        elif path == "/health":
            self.send_json({"status": "ok", "service": "amprgate-status"})

        else:
            self.send_json({"error": "Not found"}, 404)

    def do_POST(self):
        path = urlparse(self.path).path

        if path.startswith("/api/tunnel/"):
            action = path.split("/")[-1]
            if action in ("up", "down", "restart"):
                result = tunnel_action(action)
                self.send_json(result)
            else:
                self.send_json({"error": "Unknown action"}, 400)
        else:
            self.send_json({"error": "Not found"}, 404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()


if __name__ == "__main__":
    print(f"[amprgate-status] Starting on port {PORT}")
    print(f"[amprgate-status] Status page: http://0.0.0.0:{PORT}")
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("[amprgate-status] Stopped")
