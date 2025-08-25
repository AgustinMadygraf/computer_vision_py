"""
Interfaz para procesadores de frames (aplicación de filtros, dibujo de líneas, etc).
"""
from src.entities.frame import Frame

class IFrameProcessor:
    "Interfaz para procesadores de frames."
    def draw_yellow_line(self, frame: Frame) -> Frame:
        """Dibuja una línea amarilla en el frame."""
        raise NotImplementedError()

    def apply_filter(self, frame: Frame, filter_type: str) -> Frame:
        """Aplica un filtro al frame según el tipo."""
        raise NotImplementedError()
