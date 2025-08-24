"""
Path: src/composition_root.py
"""

from src.shared.config import get_env

from src.interface_adapters.gateway.camera_discovery_gateway import CameraDiscoveryGateway
from src.infrastructure.fastapi.static_server import app as fastapi_app
from src.infrastructure.fastapi import stream_adapter
from src.infrastructure.open_cv.stream_camera_wifi import OpenCVCameraStreamWiFi
from src.infrastructure.open_cv.stream_camera_usb import OpenCVCameraStreamUSB
from src.infrastructure.open_cv.stream_imagen import ImageStream
from src.infrastructure.open_cv.draw_line_on_frame import FrameDrawer
from src.entities.camera_stream import CameraStreamInterface
from src.infrastructure.fastapi.stream_adapter import FastAPICameraHTTPAdapter

def create_camera_stream() -> CameraStreamInterface:
    "Crea un stream de cámara según la configuración dinámica de hardware."
    gateway = CameraDiscoveryGateway()
    config = gateway.get_all_cameras()
    # Aquí podrías decidir el modo por variable de entorno o por lógica de preferencia
    # Ejemplo: priorizar USB si hay, luego WiFi, luego imagen
    if config["usb"]:
        camera_index = config["usb"][0]
        return OpenCVCameraStreamUSB(FrameDrawer(), camera_index)
    elif config["wifi"]:
        wifi = config["wifi"][0]
        return OpenCVCameraStreamWiFi(wifi["ip"], wifi["user"], wifi["password"], FrameDrawer())
    image_path = get_env("IMAGE_PATH")
    if image_path:
        return ImageStream(FrameDrawer(), image_path)
    raise RuntimeError("No se pudo inicializar el stream de cámara.")

def get_app():
    "Obtiene la aplicación según el marco configurado."
    # Inyecta la dependencia como interfaz y la expone globalmente para el router
    camera_stream = create_camera_stream()
    stream_adapter.adapter = FastAPICameraHTTPAdapter(camera_stream)
    return fastapi_app
