# pylint: disable=no-member
"""
Path: src/entities/contour_filter.py
"""

import cv2
from src.entities.i_frame_processor import IFrameProcessor

class ContourFilter(IFrameProcessor):
    "Filtro de contornos."
    def process(self, frame):
        "Aplica el filtro de identificación de contornos al frame."
        # Convertir a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Aplicar desenfoque para reducir ruido
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        # Detectar bordes con Canny
        edges = cv2.Canny(blurred, 50, 150)
        # Encontrar contornos
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Dibujar contornos sobre el frame original
        contoured_frame = frame.copy()
        cv2.drawContours(contoured_frame, contours, -1, (0, 255, 0), 2)
        return
