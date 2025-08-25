"""
Path: tests/test_get_filter_state_usecase.py
Caso de uso para obtener el estado del filtro de un usuario/conexión.
"""

import pytest
from src.use_cases.get_filter_state_usecase import GetFilterStateUseCase
from src.infrastructure.repository.filter_state_repository import FilterStateRepository
from src.entities.filter_settings import FilterSettings

@pytest.fixture
def repo():
    "Repositorio de estado de filtros."
    return FilterStateRepository()

@pytest.fixture
def usecase(repo):
    "Caso de uso para obtener el estado del filtro."
    return GetFilterStateUseCase(filter_repository=repo)

def test_get_filter_state_default_active(usecase):
    "Prueba que el estado del filtro por defecto es activo."
    user_id = "user3"
    assert usecase.execute(user_id) is True

def test_get_filter_state_after_set(usecase, repo):
    "Prueba que el estado del filtro se puede obtener después de establecerlo."
    user_id = "user4"
    repo.set_filter_settings(user_id, FilterSettings(active=False))
    assert usecase.execute(user_id) is False
