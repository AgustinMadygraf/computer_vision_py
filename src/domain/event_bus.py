"""
Path: src/domain/event_bus.py
Bus de eventos de dominio para registrar listeners y emitir eventos.
"""

class EventBus:
    "Bus de eventos simple para desacoplar emisores y listeners."
    def __init__(self):
        self._listeners = []

    def register(self, callback):
        "Registra un listener que recibirá eventos."
        self._listeners.append(callback)

    def emit(self, event):
        "Emite un evento a todos los listeners registrados."
        for cb in self._listeners:
            cb(event)
