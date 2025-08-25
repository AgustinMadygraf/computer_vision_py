"""
Path: src/interface_adapters/adapters/websocket_stream_adapter.py
Adaptador WebSocket para desacoplar la infraestructura de la lógica de negocio.
"""
from src.use_cases.apply_filter_usecase import ApplyFilterUseCase
from src.use_cases.toggle_filter_usecase import ToggleFilterUseCase
from src.use_cases.get_video_stream_usecase import GetVideoStreamUseCase
from src.entities.i_filter_repository import IFilterRepository
from src.entities.i_frame_processor import IFrameProcessor
from src.entities.i_stream_source import IStreamSource

class WebSocketStreamAdapter:
    "Adaptador WebSocket para desacoplar la infraestructura de la lógica de negocio."
    def __init__(self, filter_repository: IFilterRepository, frame_processor: IFrameProcessor, stream_source: IStreamSource):
        self.filter_repository = filter_repository
        self.frame_processor = frame_processor
        self.stream_source = stream_source
        self.apply_filter_usecase = ApplyFilterUseCase(frame_processor)
        self.toggle_filter_usecase = ToggleFilterUseCase()
        self.get_video_stream_usecase = GetVideoStreamUseCase(stream_source)

    def on_message(self, user_id: str, message: str):
        """Procesa comandos recibidos por WebSocket."""
        if message in ("filtro:on", "filtro:off"):
            filter_settings = self.filter_repository.get_filter_settings(user_id)
            self.toggle_filter_usecase.execute(filter_settings, message)
            self.filter_repository.set_filter_settings(user_id, filter_settings)

    def stream_frames(self, user_id: str, camera_config):
        """Envía frames procesados según el estado del filtro."""
        filter_settings = self.filter_repository.get_filter_settings(user_id)
        for frame in self.get_video_stream_usecase.execute(camera_config):
            processed_frame = self.apply_filter_usecase.execute(frame, filter_settings)
            self.send_frame(user_id, processed_frame)

    def send_frame(self, user_id: str, frame):
        """Envía el frame al frontend por WebSocket (implementación concreta)."""
        raise NotImplementedError()
