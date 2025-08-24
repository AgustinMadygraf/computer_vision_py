# Documentación de la API Backend

## Descripción General

Este backend permite exponer el stream de una cámara IP, obtener snapshots, consultar la resolución y recibir notificaciones en tiempo real sobre el estado del stream. Soporta los frameworks Flask y FastAPI, y está diseñado siguiendo principios de arquitectura limpia.

---

## Endpoints HTTP

### 1. Página principal
- **URL:** `/`
- **Método:** GET
- **Descripción:** Devuelve la página principal con el stream MJPEG embebido.
- **Respuesta:** HTML


### 2. Stream MJPEG (Múltiples fuentes)
- **URL:** `/usb/{index}/stream.mjpg`, `/wifi/{index}/stream.mjpg`, `/img/{index}/stream.mjpg`
- **Método:** GET
- **Descripción:** Devuelve el stream de video en formato MJPEG para la fuente y el índice especificados.
- **Respuesta:** `multipart/x-mixed-replace; boundary=frame`
- **Uso en frontend:**  
  `<img src="/api/computer_vision/usb/0/stream.mjpg" alt="USB 0" />`
  `<img src="/api/computer_vision/wifi/1/stream.mjpg" alt="WiFi 1" />`
  `<img src="/api/computer_vision/img/2/stream.mjpg" alt="Imagen 2" />`


### 3. Resolución del stream (Múltiples fuentes)
- **URL:** `/usb/{index}/resolution`, `/wifi/{index}/resolution`, `/img/{index}/resolution`
- **Método:** GET
- **Descripción:** Devuelve la resolución actual del stream de video para la fuente y el índice especificados.
- **Respuesta:** JSON  
  `{ "width": 1280, "height": 720 }`


### 4. Snapshot (Múltiples fuentes)
- **URL:** `/usb/{index}/snapshot.jpg`, `/wifi/{index}/snapshot.jpg`, `/img/{index}/snapshot.jpg`
- **Método:** GET
- **Descripción:** Toma un snapshot del stream especificado y lo devuelve como imagen JPEG.
- **Respuesta exitosa:** `image/jpeg`
- **Respuesta de error:**  
  - Código 503, texto plano: `No se pudo capturar frame`
- **Ejemplo de uso en frontend:**
  ```js
  fetch('/api/computer_vision/usb/0/snapshot.jpg')
    .then(res => res.blob())
    .then(blob => {
      const url = URL.createObjectURL(blob);
      document.getElementById('snapshot').src = url;
    });
  ```

---


## Endpoint WebSocket

### 5. Notificaciones en tiempo real
- **URL:** `/ws`
- **Protocolo:** WebSocket
- **Descripción:** Permite recibir notificaciones automáticas sobre el estado de los streams (por ejemplo, pérdida o recuperación de imagen). Actualmente el WebSocket es global, pero puede adaptarse para identificar el stream si es necesario.
- **Eventos enviados:**
  - `status`: Conexión exitosa.
  - `imagen_perdida`: El stream se ha caído.
  - `imagen_recuperada`: El stream se ha restablecido.
- **Ejemplo de conexión en frontend (JavaScript):**
  ```js
  const ws = new WebSocket('ws://localhost:5001/ws');
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.event === 'imagen_perdida') {
      // Mostrar alerta o intentar reconectar
    }
    if (data.event === 'imagen_recuperada') {
      // Refrescar stream
    }
  };
  ```

#### Cierre ordenado de la conexión WebSocket

Para cerrar la conexión WebSocket de forma ordenada, el cliente debe enviar el mensaje `"close"`. El backend responderá con una confirmación y cerrará la conexión:

```js
ws.send("close"); // Solicita cierre ordenado
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.message === "Cerrando conexión WebSocket") {
    // El servidor está cerrando la conexión
  }
};
ws.onclose = () => {
  // La conexión se ha cerrado
};
```

Esto permite liberar recursos en el servidor y evitar conexiones abiertas innecesarias.

---


## Flujo de integración recomendado

1. El frontend solicita `/usb/{index}/resolution`, `/wifi/{index}/resolution` o `/img/{index}/resolution` para conocer el tamaño del video de cada fuente.
2. Muestra el stream embebiendo `/usb/{index}/stream.mjpg`, `/wifi/{index}/stream.mjpg` o `/img/{index}/stream.mjpg` en un `<img>`.
3. Permite al usuario tomar snapshots solicitando `/usb/{index}/snapshot.jpg`, `/wifi/{index}/snapshot.jpg` o `/img/{index}/snapshot.jpg`.
4. Se conecta al WebSocket `/ws` para recibir notificaciones en tiempo real sobre el estado de los streams.

---

## Manejo de errores

- Si la cámara no está disponible, los endpoints pueden devolver errores HTTP (503 en `/snapshot.jpg`).
- El frontend debe manejar estos errores y mostrar mensajes adecuados al usuario.
- El WebSocket permite notificar automáticamente al frontend sobre eventos críticos.

---

## CORS

- El backend implementa CORS para permitir el acceso desde otros dominios.
- Si el frontend se sirve desde un dominio diferente, asegúrate de que CORS esté habilitado.

---

## Reglas de negocio

- El stream y los snapshots requieren que la cámara esté conectada y configurada.
- No hay autenticación implementada actualmente.
- El backend ahora soporta múltiples fuentes de video (USB, WiFi, imágenes) por instancia, accesibles por tipo e índice.

---

## Notas técnicas

- Backend desarrollado en Python con Flask y FastAPI.
- Arquitectura desacoplada y extensible.
- Los snapshots se generan en tiempo real y no se almacenan en disco.
- El adaptador HTTP y los controladores están desacoplados de la lógica de negocio.
- Soporte para notificaciones en tiempo real vía WebSocket.
