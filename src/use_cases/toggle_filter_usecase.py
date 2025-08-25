"""
Path: src/use_cases/toggle_filter_usecase.py
Caso de uso: Activar/desactivar el filtro por usuario/conexión.
"""

from src.entities.filter_settings import FilterSettings

class ToggleFilterUseCase:
    "Activa o desactiva el filtro según comando recibido."
    def execute(self, filter_settings: FilterSettings, command: str):
        "Ejecuta el caso de uso."
        if command == "filtro:on":
            filter_settings.set_active(True)
        elif command == "filtro:off":
            filter_settings.set_active(False)
