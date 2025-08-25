"""
Path: src/use_cases/set_filter_state_usecase.py
Caso de uso para alternar el estado del filtro de un usuario/conexión.
"""
from src.infrastructure.repository.filter_state_repository import FilterStateRepository
from src.entities.filter_settings import FilterSettings

class SetFilterStateUseCase:
    "Alterna el estado del filtro para un usuario específico."
    def __init__(self, filter_repository=None):
        self.filter_repository = filter_repository or FilterStateRepository()

    def execute(self, user_id: str, activo: bool):
        "Ejecuta el caso de uso."
        settings = FilterSettings(active=activo)
        self.filter_repository.set_filter_settings(user_id, settings)
        return settings.active
