"""
Path: src/entities/contour_filter.py
"""

from src.entities.i_frame_processor import IFrameProcessor

class ContourFilter(IFrameProcessor):
    "Filtro de contornos."
    def process(self, frame):
        "Aplica el filtro de contornos al frame."
        pass # pylint: disable=unnecessary-pass
