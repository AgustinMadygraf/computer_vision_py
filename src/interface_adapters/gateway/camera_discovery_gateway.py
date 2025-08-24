# pylint: disable=no-member
"""
Path: src/interface_adapters/gateway/camera_discovery_gateway.py
Gateway para relevamiento dinámico de hardware de cámaras (USB y WiFi).
"""

import cv2

class CameraDiscoveryGateway:
    "Gateway para descubrir cámaras USB y listar cámaras WiFi configuradas."
    def __init__(self, max_usb=5):
        self.max_usb = max_usb

    def discover_usb_cameras(self):
        "Detecta cámaras USB conectadas y retorna una lista de índices disponibles."
        usb_cameras = []
        for idx in range(self.max_usb):
            # Aquí iría la lógica real de detección, por ejemplo usando OpenCV
            cap = cv2.VideoCapture(idx)
            if cap.isOpened():
                usb_cameras.append(idx)
            cap.release()
        return usb_cameras


    def get_all_cameras(self):
        """Retorna un diccionario con cámaras USB y WiFi detectadas/configuradas."""
        return {
            "usb": self.discover_usb_cameras(),
            # "wifi": self.get_wifi_cameras()
        }
