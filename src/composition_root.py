"""
Path: src/composition_root.py
"""

from src.shared.config import get_env
from src.shared.logger import get_logger

from src.infrastructure.fastapi.stream_adapter import FastAPICameraHTTPAdapter
from src.infrastructure.fastapi.static_server import app as fastapi_app
from src.infrastructure.fastapi import stream_adapter
from src.interface_adapters.gateway.camera_discovery_gateway import CameraDiscoveryGateway
from src.interface_adapters.gateway.wifi_credentials_gateway import WifiCredentialsGateway
from src.use_cases.discover_cameras_usecase import DiscoverCamerasUseCase
from src.use_cases.select_camera_stream_usecase import SelectCameraStreamUseCase
from src.entities.camera_stream import CameraStreamInterface

logger = get_logger("CompositionRoot")

def create_camera_stream() -> CameraStreamInterface:
    "Crea un stream de cámara según la configuración dinámica de hardware."
    try:
        logger.info("Instanciando gateways y servicios para DiscoverCamerasUseCase")
        usb_gateway = CameraDiscoveryGateway()
        wifi_gateway = WifiCredentialsGateway()
        cameras_usecase = DiscoverCamerasUseCase(usb_gateway, wifi_gateway)
        cameras = cameras_usecase.execute()
        logger.info("Cámaras detectadas: %s", cameras)
        image_path = get_env("IMAGE_PATH")
        logger.info("IMAGE_PATH: %s", image_path)
        # Pasar el tipo de filtro como string, no la instancia
        filter_type = 'contour'
        select_stream_usecase = SelectCameraStreamUseCase(cameras, image_path, filter_type)
        return select_stream_usecase.execute()
    except Exception as e:
        logger.error("[ERROR] No se pudo crear el stream de cámara: %s", e)
        raise

def get_app():
    "Obtiene la aplicación según el marco configurado."
    # Inyecta la dependencia como interfaz y la expone globalmente para el router
    try:
        logger.info("Inicializando aplicación FastAPI y adaptador de stream")
        camera_stream = create_camera_stream()
        stream_adapter.adapter = FastAPICameraHTTPAdapter(camera_stream)
        logger.info("Aplicación FastAPI lista")
        return fastapi_app
    except Exception as e:
        logger.error("[ERROR] No se pudo inicializar la aplicación: %s", e)
        raise
