# pylint: disable=no-member
"""
Path: src/shared/config.py
Configura y expone las variables de entorno necesarias para la aplicación.
"""

import os
import cv2
from dotenv import load_dotenv
from src.shared.logger import get_logger


logger = get_logger("Config")
load_dotenv()

def get_env(var_name, default=None):
    "Obtiene una variable de entorno"
    return os.environ.get(var_name, default)

def get_config():
    "Devuelve las variables de entorno actuales."
    config = {
        "IP": get_env("IP"),
        "USER": get_env("USER"),
        "PASSWORD": get_env("PASSWORD"),
        "MODE": get_env("MODE"),
        "IMAGE_PATH": get_env("IMAGE_PATH"),
    }
    # Validar variables críticas
    if config["MODE"] is None:
        logger.error("La variable de entorno MODE no está definida. Verifica tu archivo .env.")
        exit(1)

    # Detectar cámaras USB conectadas
    usb_cameras = []
    max_tested = 5  # Número máximo de índices a probar
    for idx in range(max_tested):
        try:
            cap = cv2.VideoCapture(idx)
            if cap is not None and cap.isOpened():
                usb_cameras.append(idx)
            if cap:
                cap.release()
        except (cv2.error, OSError):  # pylint: disable=catching-non-exception
            pass

    # Listar cámaras WiFi (por ahora solo una, pero se puede extender)
    wifi_cameras = []
    if config["IP"]:
        wifi_cameras.append({
            "ip": config["IP"],
            "user": config["USER"],
            "password": config["PASSWORD"]
        })

    config["USB_CAMERAS"] = usb_cameras
    config["WIFI_CAMERAS"] = wifi_cameras
    return config

def get_static_path():
    "Obtiene la ruta base de archivos estáticos"
    return get_env("STATIC_PATH", "static")
