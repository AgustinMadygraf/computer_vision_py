"""
Path: src/interface_adapters/controllers/stream_controller.py
Controlador para operaciones de stream, desacoplado de FastAPI.
"""

from src.shared.logger import get_logger

from src.use_cases.get_filter_state_usecase import GetFilterStateUseCase
from src.infrastructure.open_cv.draw_line_on_frame import FrameDrawer
from src.domain.events import FilterStateChanged
from src.use_cases.set_filter_state_usecase import SetFilterStateUseCase
from src.infrastructure.repository.filter_state_repository import FilterStateRepository

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
    def set_filtro_activo(self, ws, activo: bool, event_bus=None, user_id=None):
        "Setea el estado del filtro para una conexión WebSocket usando caso de uso puro."
        user_id = user_id or getattr(ws, 'user_id', str(ws))
        set_filter_state = SetFilterStateUseCase()
        self.logger.info("set_filtro_activo: ws=%s, user_id=%s, activo=%s", ws, user_id, activo)
        set_filter_state.execute(user_id, activo)
        # Emitir evento de dominio si se provee event_bus y user_id
        if event_bus and user_id is not None:
            event_bus.emit(FilterStateChanged(user_id, activo))

    def get_filtro_activo(self, ws, user_id=None):
        "Obtiene el estado del filtro para una conexión WebSocket usando caso de uso puro. Por defecto, activo."
        user_id = user_id or getattr(ws, 'user_id', str(ws))
        get_filter_state = GetFilterStateUseCase()
        return get_filter_state.execute(user_id)

    def remove_ws(self, ws, user_id=None):
        "Elimina el estado asociado a una conexión WebSocket en el repositorio."
        user_id = user_id or getattr(ws, 'user_id', str(ws))
        repo = FilterStateRepository()
        repo.remove(user_id)
    def handle_websocket_message(self, user_id, message):
        "Delegar el procesamiento de mensajes WebSocket al adaptador."
        if self.websocket_adapter:
            self.websocket_adapter.on_message(user_id, message)

    def stream_frames(self, user_id, camera_config):
        "Delegar el streaming de frames al adaptador."
        if self.websocket_adapter:
            self.websocket_adapter.stream_frames(user_id, camera_config)
