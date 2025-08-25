"""
Path: src/entities/frame.py
Entidad Frame: representa un frame de imagen/video en el dominio core.
"""
from typing import Any

class Frame:
    """Entidad pura para encapsular datos de imagen/video."""
    def __init__(self, data: Any, timestamp: float = None):
        self.data = data
        self.timestamp = timestamp

    def get_data(self) -> Any:
        "Retorna los datos del frame."
        return self.data

    def get_timestamp(self) -> float:
        "Retorna la marca de tiempo del frame."
        return self.timestamp
