# pylint: disable=no-member
"""
Path: src/infrastructure/draw_line_on_frame.py
Implementación concreta de IFrameDrawer usando OpenCV.
"""

import numpy as np
import cv2
from src.entities.frame_drawer import IFrameDrawer
from src.shared.logger import get_logger

class FrameDrawer(IFrameDrawer):
    "Implementación concreta que depende solo de la interfaz IFrameDrawer."
    logger = get_logger("FrameDrawer")
    "Implementación concreta que depende solo de la interfaz IFrameDrawer."
    def draw_horizontal_yellow_line(self, frame: np.ndarray, thickness: int = 3) -> np.ndarray:
        if frame is None:
            self.logger.warning("draw_horizontal_yellow_line: frame is None")
            return None
        height, width = frame.shape[:2]
        y = height // 2
#        self.logger.debug("Procesando frame: shape=%s, thickness=%d, y=%d",
#                          frame.shape, thickness, y)
#        self.logger.debug("Aplicando línea amarilla al frame")
        cv2.line(frame, (0, y), (width, y), (0, 255, 255), thickness)
#        self.logger.debug("Frame procesado con línea amarilla")
        return frame
