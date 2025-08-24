# pylint: disable=no-member
"""
Path: src/infrastructure/draw_line_on_frame.py
Implementación concreta de IFrameDrawer usando OpenCV.
"""

import cv2
import numpy as np
from src.entities.frame_drawer import IFrameDrawer

class FrameDrawer(IFrameDrawer):
    """Implementación de IFrameDrawer para dibujar sobre frames de imagen."""

    def draw_horizontal_yellow_line(self, frame: np.ndarray, thickness: int = 3) -> np.ndarray:
        """Dibuja una línea horizontal amarilla en la mitad de la imagen."""
        if frame is not None:
            y = frame.shape[0] // 2
            cv2.line(frame, (0, y), (frame.shape[1], y), (0, 255, 255), thickness)
        return frame
