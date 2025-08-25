"""
Path: src/application/stream_event_notifier.py
Clase para centralizar la notificación de eventos de stream (pérdida/recuperación de imagen).
"""

from src.shared.logger import get_logger

from src.domain.event_bus import EventBus
from src.domain.events import FilterStateChanged

class StreamEventNotifier:
    "Gestor de eventos de stream para notificar a la infraestructura (WebSocket, etc)."
    logger = get_logger("StreamEventNotifier")
    def __init__(self, event_bus=None):
        self._listeners = []
        self.event_bus = event_bus or EventBus()
        # Registrar como listener del bus de eventos
        self.event_bus.register(self._handle_domain_event)

    def register_listener(self, callback):
        "Registra un callback que será llamado con (event_name, payload)."
        self.logger.info("Listener registrado en StreamEventNotifier.")
        self._listeners.append(callback)

    def notify(self, event_name, payload=None):
        "Notifica a todos los listeners registrados (legacy)."
        self.logger.info("Notificando evento '%s' a %d listeners.", event_name, len(self._listeners))
        for cb in self._listeners:
            cb(event_name, payload or {})

    def _handle_domain_event(self, event):
        "Callback para eventos de dominio."
        if isinstance(event, FilterStateChanged):
            self.logger.info("Evento FilterStateChanged recibido: %s", event.payload)
            for cb in self._listeners:
                cb(event.name, event.payload)
