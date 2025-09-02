"""
Path: src/entities/violet_line_filter.py
"""

from src.entities.i_frame_processor import IFrameProcessor

class VioletLineFilter(IFrameProcessor):
    "Filtro de línea violeta."
    def process(self, frame):
        "Aplica el filtro de línea violeta al frame. (Por ahora, passthrough)"
        return frame
