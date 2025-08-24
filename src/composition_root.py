"""
Path: src/composition_root.py
"""

from src.shared.config import get_config

from src.infrastructure.fastapi.static_server import app as fastapi_app
from src.infrastructure.fastapi import stream_adapter
from src.infrastructure.open_cv.stream_camera_wifi import OpenCVCameraStreamWiFi
from src.infrastructure.open_cv.stream_camera_usb import OpenCVCameraStreamUSB
from src.infrastructure.open_cv.stream_imagen import ImageStream
from src.infrastructure.open_cv.draw_line_on_frame import FrameDrawer
from src.entities.camera_stream import CameraStreamInterface
from src.infrastructure.fastapi.stream_adapter import FastAPICameraHTTPAdapter

def create_camera_stream() -> CameraStreamInterface:
    "Crea un stream de cámara según la configuración."
    config = get_config()
    mode = config["MODE"].lower()
    frame_drawer = FrameDrawer()
    if mode == "wifi":
        return OpenCVCameraStreamWiFi(
            ip=config["IP"],
            user=config["USER"],
            password=config["PASSWORD"],
            draw_line_fn=frame_drawer.draw_horizontal_yellow_line
        )
    elif mode == "usb":
        return OpenCVCameraStreamUSB(
            draw_line_fn=frame_drawer.draw_horizontal_yellow_line
        )
    elif mode == "img":
        return ImageStream(
            process_frame_callback=frame_drawer.draw_horizontal_yellow_line,
            image_path=config["IMAGE_PATH"]
        )
    else:
        raise RuntimeError(f"Modo de cámara desconocido: {mode}")

def get_app():
    "Obtiene la aplicación según el marco configurado."
    # Inyecta la dependencia como interfaz y la expone globalmente para el router
    camera_stream = create_camera_stream()
    stream_adapter.adapter = FastAPICameraHTTPAdapter(camera_stream)
    return fastapi_app
