"""
Path: src/application/stream_event_notifier.py
Clase para centralizar la notificación de eventos de stream (pérdida/recuperación de imagen).
"""

class StreamEventNotifier:
    "Gestor de eventos de stream para notificar a la infraestructura (WebSocket, etc)."
    def __init__(self):
        self._listeners = []

    def register_listener(self, callback):
        "Registra un callback que será llamado con (event_name, payload)."
        print("[INFO] Listener registrado en StreamEventNotifier.")
        self._listeners.append(callback)

    def notify(self, event_name, payload=None):
        "Notifica a todos los listeners registrados."
        print(f"[INFO] Notificando evento '{event_name}' a {len(self._listeners)} listeners.")
        for cb in self._listeners:
            cb(event_name, payload or {})
