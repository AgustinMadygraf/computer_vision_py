"""
Path: src/entities/camera_stream.py

"""

from abc import ABC, abstractmethod
# pylint: disable=unnecessary-pass

class CameraStreamInterface(ABC):
    "Interfaz para el stream de cámara IP."
    @abstractmethod
    def get_resolution(self):
        "Obtiene la resolución del stream de video."
        pass

    @abstractmethod
    def mjpeg_generator(self, quality=80):
        "Generador de stream MJPEG."
        pass

    @abstractmethod
    def save_snapshot(self, path=None):
        "Guarda un snapshot del stream de video."
        pass

    @abstractmethod
    def release(self):
        "Libera los recursos de la cámara."
        pass


class BaseCameraStream(CameraStreamInterface):
    "Clase base abstracta para streams de cámara, con lógica y atributos comunes."
    def __init__(self, process_frame_callback=None):
        self.process_frame_callback = process_frame_callback
        self.width = None
        self.height = None

    def get_resolution(self):
        "Devuelve la resolución del stream si está disponible."
        return self.width, self.height

    def release(self):
        "Libera recursos si es necesario. Por defecto, no hace nada."
        pass

    # Los siguientes métodos siguen siendo abstractos, para que las subclases los implementen
    @abstractmethod
    def mjpeg_generator(self, quality=80):
        pass

    @abstractmethod
    def save_snapshot(self, path=None):
        pass
