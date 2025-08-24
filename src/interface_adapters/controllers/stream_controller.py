"""
Path: src/interface_adapters/controllers/stream_controller.py
Controlador para operaciones de stream, desacoplado de FastAPI.
"""

from src.application.draw_line_service import DrawLineService
from src.use_cases.draw_line_on_frame_usecase import DrawLineOnFrameUseCase
from src.infrastructure.open_cv.draw_line_on_frame import FrameDrawer
from src.entities.frame_drawer import IFrameDrawer

class StreamController:
    "Controlador para coordinar operaciones de stream y dibujo."
    def __init__(self):
        frame_drawer: IFrameDrawer = FrameDrawer()
        draw_line_usecase = DrawLineOnFrameUseCase(frame_drawer)
        self.draw_line_service = DrawLineService(draw_line_usecase)

    def draw_line_on_frame(self, frame, thickness=3):
        "Dibuja una línea horizontal amarilla en el frame."
        return self.draw_line_service.draw_horizontal_yellow_line(frame, thickness)

    # Agregar aquí otros métodos para coordinar lógica de negocio de streams
