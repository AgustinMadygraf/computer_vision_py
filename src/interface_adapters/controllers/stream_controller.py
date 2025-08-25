"""
Path: src/interface_adapters/controllers/stream_controller.py
Controlador para operaciones de stream, desacoplado de FastAPI.
"""

from src.infrastructure.open_cv.draw_line_on_frame import FrameDrawer
from src.shared.logger import get_logger
from src.domain.events import FilterStateChanged
class StreamController:
    "Controlador para coordinar operaciones de stream y dibujo."
    logger = get_logger("StreamController")
    def __init__(self, websocket_adapter=None):
        self.websocket_adapter = websocket_adapter
        self.frame_drawer = FrameDrawer()

    def draw_line_on_frame(self, frame, thickness=3):
        "Dibuja una línea horizontal amarilla en el frame."
        frame_modificado = self.frame_drawer.draw_horizontal_yellow_line(frame, thickness)
        return frame_modificado

    # Estado del filtro por conexión (WebSocket)
    _filtro_por_ws = {}

    def set_filtro_activo(self, ws, activo: bool, event_bus=None, user_id=None):
        "Setea el estado del filtro para una conexión WebSocket y emite evento de dominio si corresponde."
        self.logger.info("set_filtro_activo: ws=%s, activo=%s", ws, activo)
        self._filtro_por_ws[ws] = activo
        # Emitir evento de dominio si se provee event_bus y user_id
        if event_bus and user_id is not None:
            event_bus.emit(FilterStateChanged(user_id, activo))

    def get_filtro_activo(self, ws):
        "Obtiene el estado del filtro para una conexión WebSocket. Por defecto, activo."
        if ws is None:
            return True

        estado = self._filtro_por_ws.get(ws, True)
        return estado

    def remove_ws(self, ws):
        "Elimina el estado asociado a una conexión WebSocket."
        self.logger.info("remove_ws: ws=%s", ws)
        if ws in self._filtro_por_ws:
            del self._filtro_por_ws[ws]
    def handle_websocket_message(self, user_id, message):
        "Delegar el procesamiento de mensajes WebSocket al adaptador."
        if self.websocket_adapter:
            self.websocket_adapter.on_message(user_id, message)

    def stream_frames(self, user_id, camera_config):
        "Delegar el streaming de frames al adaptador."
        if self.websocket_adapter:
            self.websocket_adapter.stream_frames(user_id, camera_config)
