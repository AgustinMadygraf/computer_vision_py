"""
Path: src/composition_root.py
"""

from src.shared.config import get_env
from src.shared.logger import get_logger
logger = get_logger("CompositionRoot")

from src.use_cases.discover_cameras_usecase import DiscoverCamerasUseCase
from src.use_cases.select_camera_stream_usecase import SelectCameraStreamUseCase
from src.infrastructure.fastapi.static_server import app as fastapi_app
from src.infrastructure.fastapi import stream_adapter
from src.entities.camera_stream import CameraStreamInterface
from src.infrastructure.fastapi.stream_adapter import FastAPICameraHTTPAdapter

def create_camera_stream() -> CameraStreamInterface:
    "Crea un stream de cámara según la configuración dinámica de hardware."
    # Instanciar dependencias core
    # Si se requiere frame_drawer para wiring, instanciar aquí y pasar explícitamente
    logger.info("Creando instancia de DiscoverCamerasUseCase")
    cameras_usecase = DiscoverCamerasUseCase()
    cameras = cameras_usecase.execute()
    logger.info("Cámaras detectadas: %s", cameras)
    image_path = get_env("IMAGE_PATH")
    logger.info("IMAGE_PATH: %s", image_path)
    select_stream_usecase = SelectCameraStreamUseCase(cameras, image_path)
    # Si select_stream_usecase requiere draw_line_usecase, pásalo aquí
    # (ajustar constructor si es necesario)
    # Ejemplo:
    # select_stream_usecase = SelectCameraStreamUseCase(cameras, image_path, _frame_drawer)
    return select_stream_usecase.execute()

def get_app():
    "Obtiene la aplicación según el marco configurado."
    # Inyecta la dependencia como interfaz y la expone globalmente para el router
    logger.info("Inicializando aplicación FastAPI y adaptador de stream")
    camera_stream = create_camera_stream()
    stream_adapter.adapter = FastAPICameraHTTPAdapter(camera_stream)
    logger.info("Aplicación FastAPI lista")
    return fastapi_app
