"""
Path: src/entities/frame_drawer.py
Interfaz para operaciones de dibujo sobre frames.
"""

from abc import ABC, abstractmethod
from typing import Any
# pylint: disable=unnecessary-pass

class IFrameDrawer(ABC):
    """Interfaz para dibujar sobre frames de imagen."""

    @abstractmethod
    def draw_horizontal_yellow_line(self, frame: Any, thickness: int = 3) -> Any:
        """Dibuja una línea horizontal violeta en la mitad de la imagen."""
        pass
