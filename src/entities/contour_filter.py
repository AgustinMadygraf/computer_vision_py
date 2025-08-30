# pylint: disable=no-member
"""
Path: src/entities/contour_filter.py
"""

import cv2
from src.entities.i_frame_processor import IFrameProcessor

class ContourFilter(IFrameProcessor):
    "Filtro de contornos."
    def process(self, frame):
        " "
        print(f"[DEBBUG] Frame recibido: shape={frame.shape}")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        print("[DEBBUG] Frame convertido a gris")
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        print("[DEBBUG] Frame desenfocado")
        edges = cv2.Canny(blurred, 50, 150)
        print("[DEBBUG] Bordes detectados")
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print(f"[DEBBUG] Contornos encontrados: {len(contours)}")
        contoured_frame = frame.copy()
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            center_x = x + w // 2
            print(f"[DEBBUG] Dibujando línea amarilla en x={center_x}, y={y} a y={y+h}")
            cv2.line(contoured_frame, (center_x, y), (center_x, y + h), (0, 255, 255), 3)
        else:
            print("[DEBBUG] No se encontraron contornos")
        return contoured_frame
