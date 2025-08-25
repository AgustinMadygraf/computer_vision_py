"""
Path: tests/test_set_filter_state_usecase.py
Caso de uso para establecer el estado del filtro de un usuario/conexión.
"""

import pytest
from src.use_cases.set_filter_state_usecase import SetFilterStateUseCase
from src.infrastructure.repository.filter_state_repository import FilterStateRepository


@pytest.fixture
def repo():
    "Repositorio de estado de filtros."
    return FilterStateRepository()

@pytest.fixture
def usecase(repo):
    "Caso de uso para establecer el estado del filtro."
    return SetFilterStateUseCase(filter_repository=repo)

def test_set_filter_state_active(usecase, repo):
    "Prueba establecer el estado del filtro como activo."
    user_id = "user1"
    usecase.execute(user_id, True)
    settings = repo.get_filter_settings(user_id)
    assert settings.active is True

def test_set_filter_state_inactive(usecase, repo):
    "Prueba establecer el estado del filtro como inactivo."
    user_id = "user2"
    usecase.execute(user_id, False)
    settings = repo.get_filter_settings(user_id)
    assert settings.active is False
