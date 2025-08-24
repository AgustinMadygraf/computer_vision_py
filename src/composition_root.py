"""
Path: src/composition_root.py
"""

from src.shared.config import get_env

from src.use_cases.discover_cameras_usecase import DiscoverCamerasUseCase
from src.use_cases.select_camera_stream_usecase import SelectCameraStreamUseCase
from src.infrastructure.fastapi.static_server import app as fastapi_app
from src.infrastructure.fastapi import stream_adapter
from src.entities.camera_stream import CameraStreamInterface
from src.infrastructure.fastapi.stream_adapter import FastAPICameraHTTPAdapter

def create_camera_stream() -> CameraStreamInterface:
    "Crea un stream de cámara según la configuración dinámica de hardware."
    cameras_usecase = DiscoverCamerasUseCase()
    cameras = cameras_usecase.execute()
    image_path = get_env("IMAGE_PATH")
    select_stream_usecase = SelectCameraStreamUseCase(cameras, image_path)
    return select_stream_usecase.execute()

def get_app():
    "Obtiene la aplicación según el marco configurado."
    # Inyecta la dependencia como interfaz y la expone globalmente para el router
    camera_stream = create_camera_stream()
    stream_adapter.adapter = FastAPICameraHTTPAdapter(camera_stream)
    return fastapi_app
