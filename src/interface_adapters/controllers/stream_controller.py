"""
Path: src/interface_adapters/controllers/stream_controller.py
Controlador para operaciones de stream, desacoplado de FastAPI.
"""

from src.shared.logger import get_logger

from src.infrastructure.open_cv.draw_line_on_frame import FrameDrawer

class StreamController:
    "Controlador para coordinar operaciones de stream y dibujo."
    logger = get_logger("StreamController")
    def __init__(self):
        self.frame_drawer = FrameDrawer()

    def draw_line_on_frame(self, frame, thickness=3):
        "Dibuja una línea horizontal violeta en el frame."
        frame_modificado = self.frame_drawer.draw_horizontal_violet_line(frame, thickness)
        return frame_modificado
