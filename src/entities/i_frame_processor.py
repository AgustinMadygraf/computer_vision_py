"""
Interfaz para procesadores de frames (aplicación de filtros, dibujo de líneas, etc).
"""

from abc import ABC, abstractmethod

class IFrameProcessor(ABC):
    "Interfaz para procesadores de frames."
    @abstractmethod
    def process(self, frame):
        """Procesa el frame y retorna el resultado filtrado."""
        pass # pylint: disable=unnecessary-pass
