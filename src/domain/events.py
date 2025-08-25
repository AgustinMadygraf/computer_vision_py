"""
Path: src/domain/events.py
Eventos de dominio para notificar cambios relevantes en el sistema.
"""

class DomainEvent:
    "Evento base de dominio."
    def __init__(self, name, payload=None):
        self.name = name
        self.payload = payload or {}

class FilterStateChanged(DomainEvent):
    "Evento emitido cuando el estado del filtro cambia."
    def __init__(self, user_id, new_state):
        super().__init__("FilterStateChanged", {"user_id": user_id, "new_state": new_state})
