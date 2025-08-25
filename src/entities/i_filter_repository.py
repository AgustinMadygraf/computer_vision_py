"""
Interfaz para repositorio de estado/configuración de filtros.
"""
from src.entities.filter_settings import FilterSettings

class IFilterRepository:
    "Interfaz para repositorio de estado/configuración de filtros."
    def get_filter_settings(self, user_id: str) -> FilterSettings:
        """Obtiene la configuración de filtro para un usuario/conexión."""
        raise NotImplementedError()

    def set_filter_settings(self, user_id: str, filter_settings: FilterSettings):
        """Actualiza la configuración de filtro para un usuario/conexión."""
        raise NotImplementedError()
