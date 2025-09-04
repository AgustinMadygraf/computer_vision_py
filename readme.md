# Computer Vision Camera Service

Este proyecto proporciona una interfaz web para acceder a cámaras IP, permitiendo visualizar el stream MJPEG y tomar snapshots. Soporta los frameworks **Flask** y **FastAPI**, y puede ejecutarse en modo producción o desarrollo. Utiliza una arquitectura limpia para separar las preocupaciones y facilitar el mantenimiento y las pruebas.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-brightgreen.svg)

## 📋 Requisitos

- Python 3.8+
- OpenCV 4.x
- FastAPI 0.100+
- Uvicorn
- Acceso a una cámara IP compatible con RTSP

## 🚀 Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/agustinmadygraf/computer_vision.git
   cd computer_vision
   ```

2. Crear un entorno virtual e instalar dependencias:
   ```bash
   python -m venv venv
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

## ⚙️ Configuración

1. Crear un archivo .env en la raíz del proyecto:
   ```
   IP=your_camera_ip
   USER=admin
   PASSWORD=yourpassword
   FRAMEWORK=flask
   MODE="img" # or "usb" or "wifi"
   IMAGE_PATH="static/public/solapa.jpeg"
   ```

2. Ajustar los parámetros según las especificaciones de tu cámara IP.

## 🏃‍♂️ Ejecución


Para iniciar el servidor con la configuración por defecto (según tu archivo `.env`):
```bash
python run.py
```


El servicio estará disponible en `http://localhost:5001`.

## 🏗️ Estructura del proyecto

```
computer_vision/
├── .env                        # Variables de entorno (no incluido en el repositorio)
├── run.py                      # Punto de entrada de la aplicación (backend)
├── requirements.txt            # Dependencias del backend
├── static/
│   └── src/
│       ├── entities/                   # Entidades del dominio (frontend)
│       │   └── stream_entity.js
│       ├── use_cases/                  # Casos de uso (frontend)
│       │   └── stream_status_use_case.js
│       ├── interface_adapters/
│       │   ├── controllers/            # Controladores (frontend)
│       │   │   └── stream_controller.js
│       │   ├── gateway/                # Adaptadores de comunicación (frontend)
│       │   │   └── stream_web_socket.js
│       │   └── presenter/              # Presenters (frontend)
│       │       └── stream_ui_status_presenter.js
│       ├── infrastructure/             # Adaptadores concretos (frontend)
│       │   ├── dom_adapter.js
│       │   ├── http_adapter.js
│       │   ├── websocket_adapter.js
│       │   └── config.js
│       └── adapters/                   # Utilidades/adaptadores secundarios
│           └── header_loader.js
└── docs/                       # Documentación adicional
   └── API_DOCUMENTATION.md


## 🧩 Arquitectura

Este proyecto implementa Clean Architecture tanto en backend (Python) como en frontend (JavaScript):

### Backend (Python)
1. **Domain**: Interfaces y reglas de negocio.
2. **Application**: Casos de uso.
3. **Infrastructure**: Implementaciones concretas.
4. **Adapters**: Conectores entre capas.
5. **Presentation**: Controladores HTTP.

### Frontend (JavaScript)
1. **Entities**: Modelos y entidades del dominio.
2. **Use Cases**: Casos de uso y lógica de aplicación.
3. **Interface Adapters**: Presenters, gateways y controladores.
4. **Infrastructure**: Adaptadores concretos (DOM, HTTP, WebSocket).
5. **Adapters**: Utilidades y adaptadores secundarios.

## ⚙️ Configuración (Frontend)

La configuración de IP, puerto y rutas del servidor de streaming está centralizada en `static/src/infrastructure/config.js`.  
Asegúrate de que los valores coincidan con los definidos en tu archivo `.env` del backend.

## 🚀 Endpoints y UI

La interfaz web se encuentra en `static/index.html` y consume los endpoints definidos en el backend.  
La comunicación con el backend se realiza mediante WebSocket y MJPEG stream, configurados en el frontend.

## 📚 Documentación adicional

Consulta la carpeta `docs/` para documentación técnica y de API.
```

## 🧩 Arquitectura

Este proyecto implementa una arquitectura limpia (Clean Architecture) con las siguientes capas:

1. **Domain**: Define las interfaces y reglas de negocio.
2. **Application**: Implementa los casos de uso que orquestan el flujo de la aplicación.
3. **Infrastructure**: Contiene implementaciones concretas de las interfaces del dominio.
4. **Adapters**: Conecta la lógica de negocio con las interfaces externas.
5. **Presentation**: Maneja la forma en que se exponen las funcionalidades.

## 🌐 API

El servicio expone los siguientes endpoints:

- `GET /` - Página principal con stream embebido
- `GET /stream.mjpg` - Stream MJPEG de la cámara
- `GET /resolution` - Información sobre la resolución del video
- `GET /snapshot.jpg` - Toma un snapshot del stream actual

Para más detalles, consulta API_DOCUMENTATION.md.

## 🔧 Tecnologías utilizadas

- **OpenCV**: Procesamiento del stream de video
- **Flask**: Framework web para la API REST
- **Python-dotenv**: Gestión de variables de entorno

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor, crea un issue o pull request con tus sugerencias.