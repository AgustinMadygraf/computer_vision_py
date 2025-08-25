"""
Path: src/application/stream_event_notifier.py
Clase para centralizar la notificación de eventos de stream (pérdida/recuperación de imagen).
"""

from src.shared.logger import get_logger

class StreamEventNotifier:
    "Gestor de eventos de stream para notificar a la infraestructura (WebSocket, etc)."
    logger = get_logger("StreamEventNotifier")
    def __init__(self):
        self._listeners = []

    def register_listener(self, callback):
        "Registra un callback que será llamado con (event_name, payload)."
        self.logger.info("Listener registrado en StreamEventNotifier.")
        self._listeners.append(callback)

    def notify(self, event_name, payload=None):
        "Notifica a todos los listeners registrados."
        self.logger.info("Notificando evento '%s' a %d listeners.", event_name, len(self._listeners))
        for cb in self._listeners:
            cb(event_name, payload or {})
