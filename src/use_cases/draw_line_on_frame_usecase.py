"""
Path: src/use_cases/draw_line_on_frame_usecase.py
Caso de uso para operaciones de dibujo sobre frames.
"""

import numpy as np
from src.entities.frame_drawer import IFrameDrawer

class DrawLineOnFrameUseCase:
    """Caso de uso para dibujar una línea horizontal violeta en la mitad de la imagen."""
    def __init__(self, frame_drawer: IFrameDrawer):
        self.frame_drawer = frame_drawer

    def execute(self, frame: np.ndarray, thickness: int = 3) -> np.ndarray:
        """Ejecuta la operación de dibujo usando el frame_drawer proporcionado."""
        return self.frame_drawer.draw_horizontal_violet_line(frame, thickness)
