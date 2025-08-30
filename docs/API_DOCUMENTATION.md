# Documentación de la API Backend

## Descripción General

Este backend permite exponer el stream de una cámara IP, obtener snapshots, consultar la resolución y recibir notificaciones en tiempo real sobre el estado del stream. Soporta los frameworks Flask y FastAPI, y está diseñado siguiendo principios de arquitectura limpia.

**Por defecto, el backend se ejecuta en el puerto 5001.**

---


## Endpoints HTTP

### 1. Página principal
- **URL:** `/`
- **Método:** GET
- **Descripción:** Devuelve la página principal con el stream MJPEG embebido.
- **Respuesta:** HTML

### 1b. Streams disponibles
- **URL:** `/streams`
- **Método:** GET
- **Descripción:** Devuelve la lista de streams disponibles (USB, WiFi, imágenes) y sus índices/metadatos para que el frontend pueda mostrar solo las opciones válidas.
- **Respuesta:** JSON
  ```json
  {
    "usb": [ { "index": 0, "type": "usb", "name": "USB Camera 0" }, ... ],
    "wifi": [ { "index": 0, "type": "wifi", "name": "WiFi Camera 0", "ip": "192.168.1.10" }, ... ],
    "img": [ { "index": 0, "type": "img", "name": "Imagen 0", "path": "static/img0.jpg" }, ... ]
  }
  ```



### 2.a. Stream MJPEG (Básico)
- **URL:** `/usb/{index}/stream.mjpg`, `/wifi/{index}/stream.mjpg`, `/img/{index}/stream.mjpg`
- **Método:** GET
- **Descripción:** Devuelve el stream de video en formato MJPEG para la fuente y el índice especificados, sin aplicar filtros.
- **Respuesta:** `multipart/x-mixed-replace; boundary=frame`
- **Uso en frontend:**  
  `<img src="/api/computer_vision/usb/0/stream.mjpg" alt="USB 0" />`
  `<img src="/api/computer_vision/wifi/1/stream.mjpg" alt="WiFi 1" />`
  `<img src="/api/computer_vision/img/2/stream.mjpg" alt="Imagen 2" />`

### 2.b. Stream MJPEG con variantes de filtro
- **URL:** `/usb/{index}/stream_original.mjpg`, `/usb/{index}/stream_filtro.mjpg`, `/wifi/{index}/stream_original.mjpg`, `/wifi/{index}/stream_filtro.mjpg`
- **Método:** GET
- **Descripción:**
  - `stream_original.mjpg`: Devuelve el stream MJPEG sin filtros.
  - `stream_filtro.mjpg`: Devuelve el stream MJPEG aplicando un filtro visual (por ejemplo, filtro amarillo).
- **Respuesta:** `multipart/x-mixed-replace; boundary=frame`
- **Uso en frontend:**  
  `<img src="/api/computer_vision/usb/0/stream_original.mjpg" alt="USB Original" />`
  `<img src="/api/computer_vision/usb/0/stream_filtro.mjpg" alt="USB Filtro" />`
  `<img src="/api/computer_vision/wifi/1/stream_original.mjpg" alt="WiFi Original" />`
  `<img src="/api/computer_vision/wifi/1/stream_filtro.mjpg" alt="WiFi Filtro" />`


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

### 5. Flujo de integración recomendado

1. El frontend solicita `/streams` para obtener la lista de streams disponibles y sus índices.
2. Solicita `/usb/{index}/resolution`, `/wifi/{index}/resolution` o `/img/{index}/resolution` para conocer el tamaño del video de cada fuente.
3. Muestra el stream embebiendo `/usb/{index}/stream.mjpg`, `/wifi/{index}/stream.mjpg` o `/img/{index}/stream.mjpg` en un `<img>`.
4. Permite al usuario tomar snapshots solicitando `/usb/{index}/snapshot.jpg`, `/wifi/{index}/snapshot.jpg` o `/img/{index}/snapshot.jpg`.

---

### 6. Manejo de errores

- Si la cámara no está disponible, los endpoints pueden devolver errores HTTP (503 en `/snapshot.jpg`).
- El frontend debe manejar estos errores y mostrar mensajes adecuados al usuario.
- El WebSocket permite notificar automáticamente al frontend sobre eventos críticos.

---

## 7. CORS

- El backend implementa CORS para permitir el acceso desde otros dominios.
- Si el frontend se sirve desde un dominio diferente, asegúrate de que CORS esté habilitado.

---

### 8. Reglas de negocio

- El stream y los snapshots requieren que la cámara esté conectada y configurada.
- No hay autenticación implementada actualmente.
- El backend ahora soporta múltiples fuentes de video (USB, WiFi, imágenes) por instancia, accesibles por tipo e índice.

---

## Notas técnicas

- Backend desarrollado en Python con Flask y FastAPI.
- Arquitectura desacoplada y extensible.
- Los snapshots se generan en tiempo real y no se almacenan en disco.
- El adaptador HTTP y los controladores están desacoplados de la lógica de negocio.
