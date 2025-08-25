"""
Interfaz para fuentes de stream de video (USB, WiFi, imagen fija).
"""

from typing import Iterator

from src.entities.camera_config import CameraConfig
from src.entities.frame import Frame

class IStreamSource:
    "Interfaz para fuentes de stream de video."
    def create_stream(self, camera_config: CameraConfig) -> Iterator[Frame]:
        """Crea un stream de frames según la configuración de cámara."""
        raise NotImplementedError()
