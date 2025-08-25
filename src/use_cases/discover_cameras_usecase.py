"""
Path: src/use_cases/discover_cameras_usecase.py
Caso de uso para relevamiento dinámico de cámaras USB y WiFi.
"""

class DiscoverCamerasUseCase:
    "Caso de uso para obtener la lista de cámaras disponibles (USB y WiFi)."
    def __init__(self, usb_gateway, wifi_gateway):
        self.usb_gateway = usb_gateway
        self.wifi_gateway = wifi_gateway

    def execute(self):
        "Retorna un diccionario con listas de cámaras USB y WiFi."
        usb_cameras = self.usb_gateway.discover_usb_cameras()
        wifi_cameras = self.wifi_gateway.get_wifi_cameras()
        return {
            "usb": usb_cameras,
            "wifi": wifi_cameras
        }
