"""
Path: src/entities/camera_stream_interface.py
Define la interfaz común para todos los streams de cámara.
"""
from abc import ABC, abstractmethod

class CameraStreamInterface(ABC):
    @abstractmethod
    def start_stream(self):
        "Inicia el stream de video."
        pass

    @abstractmethod
    def get_frame(self):
        "Obtiene el frame actual del stream."
        pass

    @abstractmethod
    def release(self):
        "Libera los recursos asociados al stream."
        pass

    @abstractmethod
    def set_frame_processor(self, processor):
        "Establece la función procesadora de frames."
        pass

    @abstractmethod
    def set_filter_enabled(self, enabled: bool):
        """
        Activa o desactiva el filtro en el stream de cámara.
        """
        pass
