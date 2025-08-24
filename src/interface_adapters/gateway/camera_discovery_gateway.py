# pylint: disable=no-member
"""
Path: src/interface_adapters/gateway/camera_discovery_gateway.py
Gateway para relevamiento dinámico de hardware de cámaras (USB y WiFi).
"""

import cv2
from src.shared.config import get_env

class CameraDiscoveryGateway:
    "Gateway para descubrir cámaras USB y listar cámaras WiFi configuradas."
    def __init__(self, max_usb=5):
        self.max_usb = max_usb

    def discover_usb_cameras(self):
        "Detecta cámaras USB conectadas y retorna una lista de índices disponibles."
        usb_cameras = []
        for idx in range(self.max_usb):
            cap = None
            try:
                cap = cv2.VideoCapture(idx)
                if cap is not None and cap.isOpened():
                    usb_cameras.append(idx)
            except cv2.error:# pylint: disable=catching-non-exception
                pass
            finally:
                if cap:
                    cap.release()
        return usb_cameras

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

    def get_all_cameras(self):
        """Retorna un diccionario con cámaras USB y WiFi detectadas/configuradas."""
        return {
            "usb": self.discover_usb_cameras(),
            "wifi": self.get_wifi_cameras()
        }
