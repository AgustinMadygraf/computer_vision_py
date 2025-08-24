"""
Path: src/infrastructure/fastapi/websocket_server.py
Servidor WebSocket para notificaciones en tiempo real usando FastAPI.
"""

import asyncio
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from src.application.stream_event_notifier import StreamEventNotifier

connected_websockets = set()
notifier = StreamEventNotifier()

# Listener para emitir eventos a todos los clientes conectados
def emit_event(event_name, payload):
    "Emite un evento a todos los clientes conectados."
    print(f"[INFO] Emitiendo evento '{event_name}' a {len(connected_websockets)} clientes WebSocket.")
    for ws in list(connected_websockets):
        try:
            asyncio.create_task(ws.send_json({"event": event_name, **(payload or {})}))
        except RuntimeError:
            connected_websockets.discard(ws)

notifier.register_listener(emit_event)

async def websocket_endpoint(websocket: WebSocket):
    "Maneja la conexión WebSocket."
    await websocket.accept()
    connected_websockets.add(websocket)
    print(f"[INFO] Cliente WebSocket conectado. Total: {len(connected_websockets)}")
    try:
        await websocket.send_json({"message": "Conectado al WebSocket"})
        while True:
            data = await websocket.receive_text()
            if data.strip().lower() == "close":
                await websocket.send_json({"message": "Cerrando conexión WebSocket"})
                await websocket.close()
                break
    except (WebSocketDisconnect, RuntimeError):
        print("[INFO] WebSocket desconectado por el cliente.")
    except asyncio.CancelledError as e:
        print(f"[INFO] WebSocket task cancelada: {e}")
    finally:
        connected_websockets.discard(websocket)
        print(f"[INFO] Cliente WebSocket eliminado. Total: {len(connected_websockets)}")
