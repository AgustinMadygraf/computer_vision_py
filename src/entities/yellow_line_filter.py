"""
Path: src/entities/yellow_line_filter.py
"""

from src.entities.i_frame_processor import IFrameProcessor

class YellowLineFilter(IFrameProcessor):
    "Filtro de línea amarilla."
    def process(self, frame):
        "Aplica el filtro de línea amarilla al frame."
        pass # pylint: disable=unnecessary-pass
