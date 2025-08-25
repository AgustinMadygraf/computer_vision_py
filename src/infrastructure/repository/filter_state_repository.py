"""
Path: src/infrastructure/repository/filter_state_repository.py
Repositorio de estado de filtros independiente de WebSockets.
Implementa la interfaz IFilterRepository.
"""
from src.entities.i_filter_repository import IFilterRepository
from src.entities.filter_settings import FilterSettings

class FilterStateRepository(IFilterRepository):
    "Repositorio de estado de filtros."
    def __init__(self):
        self._filter_settings_by_user = {}

    def get_filter_settings(self, user_id: str) -> FilterSettings:
        # Devuelve el estado actual, por defecto activo
        if user_id not in self._filter_settings_by_user:
            self._filter_settings_by_user[user_id] = FilterSettings(active=True)
        return self._filter_settings_by_user[user_id]

    def set_filter_settings(self, user_id: str, filter_settings: FilterSettings):
        self._filter_settings_by_user[user_id] = filter_settings
