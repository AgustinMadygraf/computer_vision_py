"""
Path: src/infrastructure/fastapi/websocket_server.py
Servidor WebSocket para notificaciones en tiempo real usando FastAPI.
"""

import asyncio
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect
from src.shared.logger import get_logger

from src.application.stream_event_notifier import StreamEventNotifier
from src.interface_adapters.controllers.stream_controller import StreamController


logger = get_logger("WebSocketServer")
connected_websockets = set()
notifier = StreamEventNotifier()

# Listener para emitir eventos a todos los clientes conectados
def emit_event(event_name, payload):
    "Emite un evento a todos los clientes conectados."
    logger.info("Emitiendo evento '%s' a %d clientes WebSocket.", event_name, len(connected_websockets))
    for ws in list(connected_websockets):
        try:
            asyncio.create_task(ws.send_json({"event": event_name, **(payload or {})}))
        except RuntimeError:
            connected_websockets.discard(ws)

notifier.register_listener(emit_event)

async def websocket_endpoint(websocket: WebSocket):
    "Maneja la conexión WebSocket."
    await websocket.accept()
    # Asignar un identificador único y persistente al WebSocket
    # Puede provenir de un token, parámetro, o generarse automáticamente
    if not hasattr(websocket, 'user_id'):
        # Ejemplo: usar la dirección remota como identificador (ajustar según seguridad)
        websocket.user_id = getattr(websocket, 'client', None)
        if websocket.user_id is None:
            # Fallback: usar id de objeto
            websocket.user_id = str(id(websocket))
    connected_websockets.add(websocket)
    logger.info("Cliente WebSocket conectado. user_id=%s. Total: %d", websocket.user_id, len(connected_websockets))
    # Estado del filtro por conexión coordinado con el controlador
    stream_controller = StreamController()
    try:
        await websocket.send_json({
            "message": "Conectado al WebSocket",
            "user_id": str(websocket.user_id)
        })
        while True:
            data = await websocket.receive_text()
            if data.strip().lower() == "close":
                await websocket.send_json({"message": "Cerrando conexión WebSocket"})
                await websocket.close()
                break
            # Mensaje para alternar filtro
            if data.strip().lower() == "filtro:on":
                logger.debug("WebSocket user_id=%s: comando recibido 'filtro:on'", websocket.user_id)
                stream_controller.set_filtro_activo(websocket, True)
                await websocket.send_json({"message": "Filtro activado"})
            elif data.strip().lower() == "filtro:off":
                logger.debug("WebSocket user_id=%s: comando recibido 'filtro:off'", websocket.user_id)
                stream_controller.set_filtro_activo(websocket, False)
                await websocket.send_json({"message": "Filtro desactivado"})
            # El controlador mantiene el estado por conexión
    except (WebSocketDisconnect, RuntimeError):
        logger.info("WebSocket desconectado por el cliente.")
    except asyncio.CancelledError as e:
        logger.info("WebSocket task cancelada: %s", e)
    finally:
        stream_controller.remove_ws(websocket)
        connected_websockets.discard(websocket)
        logger.info("Cliente WebSocket eliminado. Total: %d", len(connected_websockets))
