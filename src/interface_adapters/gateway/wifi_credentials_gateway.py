"""
Path: src/interface_adapters/gateway/wifi_credentials_gateway.py
Gateway dedicado a la obtención y parseo de credenciales WiFi desde configuración/env.
"""

from src.shared.config import get_env

class WifiCredentialsGateway:
    "Gateway para obtener credenciales WiFi configuradas."
    def get_wifi_cameras(self):
        "Obtiene la lista de cámaras WiFi configuradas en .env."
        wifi_cameras = []
        raw = get_env("WIFI_CAMERAS")
        if raw:
            for entry in raw.split(";"):
                parts = entry.split(",")
                if len(parts) == 3:
                    wifi_cameras.append({
                        "ip": parts[0].strip(),
                        "user": parts[1].strip(),
                        "password": parts[2].strip()
                    })
        else:
            ip = get_env("IP")
            user = get_env("USER")
            password = get_env("PASSWORD")
            if ip:
                wifi_cameras.append({
                    "ip": ip,
                    "user": user,
                    "password": password
                })
        return wifi_cameras
