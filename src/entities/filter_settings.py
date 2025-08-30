"""
Path: src/entities/filter_settings.py
Entidad FilterSettings: representa la configuración y estado del filtro de línea violeta.
"""
class FilterSettings:
    """Entidad pura para el estado/configuración del filtro."""
    def __init__(self, active: bool = True, filter_type: str = "yellow_line"):
        self.active = active
        self.filter_type = filter_type

    def is_active(self) -> bool:
        "Retorna si el filtro está activo."
        return self.active

    def set_active(self, value: bool):
        "Setea el estado activo del filtro."
        self.active = value

    def get_filter_type(self) -> str:
        "Retorna el tipo de filtro."
        return self.filter_type
