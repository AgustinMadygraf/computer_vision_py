"""
Path: src/use_cases/get_filter_state_usecase.py
Caso de uso para consultar el estado del filtro de un usuario/conexión.
"""
from src.entities.i_filter_state_repository import IFilterStateRepository


class GetFilterStateUseCase:
    "Consulta el estado del filtro para un usuario específico."
    def __init__(self, filter_repository: IFilterStateRepository):
        self.filter_repository = filter_repository

    def execute(self, user_id: str) -> bool:
        "Ejecuta el caso de uso."
        settings = self.filter_repository.get_filter_settings(user_id)
        return settings.active
