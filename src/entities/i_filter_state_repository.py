
"""
Path: src/entities/i_filter_state_repository.py
Interfaz para el repositorio de estado de filtro.
"""
from abc import ABC, abstractmethod

class IFilterStateRepository(ABC):
    "Interfaz para el repositorio de estado de filtro."
    @abstractmethod
    def get_filter_settings(self, user_id: str):
        """Devuelve la configuración del filtro para el usuario."""
        pass # pylint: disable=unnecessary-pass
