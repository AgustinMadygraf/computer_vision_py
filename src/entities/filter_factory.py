"""
Path: src/entities/filter_factory.py
"""

from src.entities.contour_filter import ContourFilter
from src.entities.yellow_line_filter import YellowLineFilter

class FilterFactory:
    "Fábrica de filtros."
    @staticmethod
    def get_filter(filter_type: str):
        "Obtiene un filtro según el tipo especificado."
        if filter_type == 'contour':
            return ContourFilter()
        elif filter_type == 'yellow_line':
            return YellowLineFilter()
        else:
            raise ValueError(f"Filtro desconocido: {filter_type}")
