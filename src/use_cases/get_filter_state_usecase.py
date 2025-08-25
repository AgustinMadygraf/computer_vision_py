"""
Path: src/use_cases/get_filter_state_usecase.py
Caso de uso para consultar el estado del filtro de un usuario/conexión.
"""
from src.infrastructure.repository.filter_state_repository import FilterStateRepository

class GetFilterStateUseCase:
    "Consulta el estado del filtro para un usuario específico."
    def __init__(self, filter_repository=None):
        self.filter_repository = filter_repository or FilterStateRepository()

    def execute(self, user_id: str) -> bool:
        "Ejecuta el caso de uso."
        settings = self.filter_repository.get_filter_settings(user_id)
        return settings.active
