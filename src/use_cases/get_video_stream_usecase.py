"""
Caso de uso: Obtener el stream de video de una cámara según configuración.
"""

from typing import Iterator
from src.entities.camera_config import CameraConfig
from src.entities.frame import Frame

class GetVideoStreamUseCase:
    "Obtiene el stream de video de una cámara."
    def __init__(self, stream_factory):
        self.stream_factory = stream_factory

    def execute(self, camera_config: CameraConfig) -> Iterator[Frame]:
        "Ejecuta el caso de uso."
        stream = self.stream_factory.create_stream(camera_config)
        for frame in stream:
            yield frame
