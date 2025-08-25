"""
Path: src/composition_root.py
"""

from src.shared.config import get_env
from src.shared.logger import get_logger

from src.use_cases.discover_cameras_usecase import DiscoverCamerasUseCase
from src.use_cases.select_camera_stream_usecase import SelectCameraStreamUseCase
from src.infrastructure.fastapi.static_server import app as fastapi_app
from src.infrastructure.fastapi import stream_adapter
from src.entities.camera_stream import CameraStreamInterface
from src.infrastructure.fastapi.stream_adapter import FastAPICameraHTTPAdapter

logger = get_logger("CompositionRoot")

def create_camera_stream() -> CameraStreamInterface:
    "Crea un stream de cámara según la configuración dinámica de hardware, inyectando dependencias explícitamente."
    logger.info("Instanciando gateways y servicios para DiscoverCamerasUseCase")
    usb_gateway = __import__('src.interface_adapters.gateway.camera_discovery_gateway', fromlist=['CameraDiscoveryGateway']).CameraDiscoveryGateway()
    wifi_gateway = __import__('src.interface_adapters.gateway.wifi_credentials_gateway', fromlist=['WifiCredentialsGateway']).WifiCredentialsGateway()
    cameras_usecase = DiscoverCamerasUseCase(usb_gateway, wifi_gateway)
    cameras = cameras_usecase.execute()
    logger.info("Cámaras detectadas: %s", cameras)
    image_path = get_env("IMAGE_PATH")
    logger.info("IMAGE_PATH: %s", image_path)
    # Instanciar FrameDrawer y pasarlo a los streams
    frame_drawer = __import__('src.infrastructure.open_cv.draw_line_on_frame', fromlist=['FrameDrawer']).FrameDrawer()
    # Instanciar SelectCameraStreamUseCase con dependencias explícitas
    select_stream_usecase = SelectCameraStreamUseCase(cameras, image_path, frame_drawer)
    return select_stream_usecase.execute()

def get_app():
    "Obtiene la aplicación según el marco configurado."
    # Inyecta la dependencia como interfaz y la expone globalmente para el router
    logger.info("Inicializando aplicación FastAPI y adaptador de stream")
    camera_stream = create_camera_stream()
    stream_adapter.adapter = FastAPICameraHTTPAdapter(camera_stream)
    logger.info("Aplicación FastAPI lista")
    return fastapi_app
