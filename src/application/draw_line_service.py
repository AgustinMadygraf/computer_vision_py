"""
Path: src/application/draw_line_service.py
Servicio de aplicación para coordinar operaciones de dibujo sobre frames.
"""

import numpy as np
from src.use_cases.draw_line_on_frame_usecase import DrawLineOnFrameUseCase

class DrawLineService:
    """Servicio de aplicación para coordinar el caso de uso de dibujo de línea."""
    def __init__(self, draw_line_usecase: DrawLineOnFrameUseCase):
        self.draw_line_usecase = draw_line_usecase

    def draw_horizontal_yellow_line(self, frame: np.ndarray, thickness: int = 3) -> np.ndarray:
        """Coordina la operación de dibujo sobre el frame."""
        return self.draw_line_usecase.execute(frame, thickness)
