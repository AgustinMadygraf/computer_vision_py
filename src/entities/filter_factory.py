"""
Path: src/entities/filter_factory.py
"""

from src.entities.contour_filter import ContourFilter
from src.entities.violet_line_filter import VioletLineFilter

class FilterFactory:
    "Fábrica y registro dinámico de filtros."
    _registry = {
        'contour': ContourFilter,
        'violet_line': VioletLineFilter,
    }

    @classmethod
    def register_filter(cls, filter_type: str, filter_cls):
        """Registra un nuevo filtro en el registro."""
        cls._registry[filter_type] = filter_cls

    @classmethod
    def get_filter(cls, filter_type: str):
        """Obtiene una instancia de filtro según el tipo especificado."""
        filter_cls = cls._registry.get(filter_type)
        if not filter_cls:
            raise ValueError(f"Filtro desconocido: {filter_type}")
        return filter_cls()
