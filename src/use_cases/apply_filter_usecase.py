"""
Path: src/use_cases/apply_filter_usecase.py
Caso de uso: Aplicar filtro (línea amarilla) a un frame si el filtro está activo.
"""
from src.entities.frame import Frame
from src.entities.filter_settings import FilterSettings

class ApplyFilterUseCase:
    """Aplica el filtro de línea amarilla si está activo."""
    def __init__(self, frame_drawer):
        self.frame_drawer = frame_drawer

    def execute(self, frame: Frame, filter_settings: FilterSettings) -> Frame:
        "Aplica el filtro de línea amarilla si está activo."
        if filter_settings.is_active():
            return self.frame_drawer.draw_yellow_line(frame)
        return frame
