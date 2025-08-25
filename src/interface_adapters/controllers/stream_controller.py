"""
Path: src/interface_adapters/controllers/stream_controller.py
Controlador para operaciones de stream, desacoplado de FastAPI.
"""

from src.infrastructure.open_cv.draw_line_on_frame import FrameDrawer
from src.shared.logger import get_logger

class StreamController:
    "Controlador para coordinar operaciones de stream y dibujo."
    logger = get_logger("StreamController")
    def __init__(self):
        self.frame_drawer = FrameDrawer()
        # ...otros inicializadores...

    def draw_line_on_frame(self, frame, thickness=3):
        "Dibuja una línea horizontal amarilla en el frame."
        # print(f"[DEBUG] draw_line_on_frame: frame shape={getattr(frame,
        # 'shape', None)}, thickness={thickness}")
        frame_modificado = self.frame_drawer.draw_horizontal_yellow_line(frame, thickness)
        return frame_modificado

    # Estado del filtro por conexión (WebSocket)
    _filtro_por_ws = {}

    def set_filtro_activo(self, ws, activo: bool):
        "Setea el estado del filtro para una conexión WebSocket."
        self.logger.info("set_filtro_activo: ws=%s, activo=%s", ws, activo)
        self._filtro_por_ws[ws] = activo

    def get_filtro_activo(self, ws):
        "Obtiene el estado del filtro para una conexión WebSocket. Por defecto, activo."
        if ws is None:
            return True

        estado = self._filtro_por_ws.get(ws, True)
        # print(f"[DEBUG] get_filtro_activo: ws={ws}, estado={estado}")
        return estado

    def remove_ws(self, ws):
        "Elimina el estado asociado a una conexión WebSocket."
        self.logger.info("remove_ws: ws=%s", ws)
        if ws in self._filtro_por_ws:
            del self._filtro_por_ws[ws]
