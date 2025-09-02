"""
Path: src/entities/violet_line_filter.py
"""

from src.entities.i_frame_processor import IFrameProcessor
from src.infrastructure.open_cv.draw_line_on_frame import FrameDrawer

class VioletLineFilter(IFrameProcessor):
    "Filtro de línea violeta."
    def __init__(self):
        self.drawer = FrameDrawer()

    def process(self, frame):
        "Dibuja una línea horizontal violeta en el frame."
        return self.drawer.draw_horizontal_violet_line(frame, thickness=3)
