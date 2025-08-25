"""
Path: src/entities/camera_config.py
Entidad CameraConfig: representa la configuración de una cámara (USB, WiFi, Imagen).
"""
from typing import Optional

class CameraConfig:
    """Entidad pura para la configuración de una cámara."""
    def __init__(self, camera_type: str, index: Optional[int] = None, ip: Optional[str] = None, user: Optional[str] = None, password: Optional[str] = None):
        self.camera_type = camera_type  # 'usb', 'wifi', 'image'
        self.index = index
        self.ip = ip
        self.user = user
        self.password = password

    def get_type(self) -> str:
        "Devuelve el tipo de cámara."
        return self.camera_type

    def get_index(self) -> Optional[int]:
        "Devuelve el índice de la cámara."
        return self.index

    def get_ip(self) -> Optional[str]:
        "Devuelve la dirección IP de la cámara."
        return self.ip

    def get_user(self) -> Optional[str]:
        "Devuelve el usuario de la cámara."
        return self.user

    def get_password(self) -> Optional[str]:
        "Devuelve la contraseña de la cámara."
        return self.password
