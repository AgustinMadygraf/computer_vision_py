# pylint: disable=no-member
"""
Path: src/infrastructure/draw_line_on_frame.py
Implementación concreta de IFrameDrawer usando OpenCV.
"""

import numpy as np
import cv2
from src.entities.frame_drawer import IFrameDrawer

class FrameDrawer(IFrameDrawer):
    "Implementación concreta que depende solo de la interfaz IFrameDrawer."
    def draw_horizontal_yellow_line(self, frame: np.ndarray, thickness: int = 3) -> np.ndarray:
        if frame is None:
            # print("[DEBUG] draw_horizontal_yellow_line: frame is None")
            return None
        height, width = frame.shape[:2]
        y = height // 2
        # print(f"[DEBUG] draw_horizontal_yellow_line: frame shape={frame.shape},
        # thickness={thickness}, y={y}")
        cv2.line(frame, (0, y), (width, y), (0, 255, 255), thickness)  # Amarillo en BGR
        return frame
