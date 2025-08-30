# Mapeo de dependencias entre casos de uso y adaptadores

## Casos de uso y sus dependencias

- [`src/use_cases/discover_cameras_usecase.py`](src/use_cases/discover_cameras_usecase.py)
  - Depende de: [`src/interface_adapters/gateway/camera_discovery_gateway.py`](src/interface_adapters/gateway/camera_discovery_gateway.py) (USB)
  - Depende de: [`src/interface_adapters/gateway/wifi_credentials_gateway.py`](src/interface_adapters/gateway/wifi_credentials_gateway.py) (WiFi)

- [`src/use_cases/select_camera_stream_usecase.py`](src/use_cases/select_camera_stream_usecase.py)
  - Depende de: [`src/infrastructure/open_cv/stream_camera_usb.py`](src/infrastructure/open_cv/stream_camera_usb.py)
  - Depende de: [`src/infrastructure/open_cv/stream_camera_wifi.py`](src/infrastructure/open_cv/stream_camera_wifi.py)
  - Depende de: [`src/infrastructure/open_cv/stream_imagen.py`](src/infrastructure/open_cv/stream_imagen.py)

- [`src/use_cases/set_filter_state_usecase.py`](src/use_cases/set_filter_state_usecase.py)
  - Depende de: [`src/infrastructure/repository/filter_state_repository.py`](src/infrastructure/repository/filter_state_repository.py)

- [`src/use_cases/get_filter_state_usecase.py`](src/use_cases/get_filter_state_usecase.py)
  - Depende de: [`src/infrastructure/repository/filter_state_repository.py`](src/infrastructure/repository/filter_state_repository.py)

- [`src/use_cases/draw_line_on_frame_usecase.py`](src/use_cases/draw_line_on_frame_usecase.py)
  - Depende de: [`src/entities/frame_drawer.py`](src/entities/frame_drawer.py) (interfaz)
  - Depende de: [`src/infrastructure/open_cv/draw_line_on_frame.py`](src/infrastructure/open_cv/draw_line_on_frame.py) (implementación)

- [`src/use_cases/apply_filter_usecase.py`](src/use_cases/apply_filter_usecase.py)
  - Depende de: [`src/entities/frame_drawer.py`](src/entities/frame_drawer.py) (interfaz)

## Adaptadores y sus dependencias

- [`src/infrastructure/open_cv/stream_camera_usb.py`](src/infrastructure/open_cv/stream_camera_usb.py)
  - Depende de: [`src/entities/camera_stream.py`](src/entities/camera_stream.py) (interfaz/base)
  - Depende de: OpenCV (cv2)

- [`src/infrastructure/open_cv/stream_camera_wifi.py`](src/infrastructure/open_cv/stream_camera_wifi.py)
  - Depende de: [`src/entities/camera_stream.py`](src/entities/camera_stream.py) (interfaz/base)
  - Depende de: OpenCV (cv2)

- [`src/infrastructure/open_cv/stream_imagen.py`](src/infrastructure/open_cv/stream_imagen.py)
  - Depende de: [`src/entities/camera_stream.py`](src/entities/camera_stream.py) (interfaz/base)
  - Depende de: OpenCV (cv2)

- [`src/infrastructure/repository/filter_state_repository.py`](src/infrastructure/repository/filter_state_repository.py)
  - Implementa: [`src/entities/i_filter_repository.py`](src/entities/i_filter_repository.py)

- [`src/infrastructure/open_cv/draw_line_on_frame.py`](src/infrastructure/open_cv/draw_line_on_frame.py)
  - Implementa: [`src/entities/frame_drawer.py`](src/entities/frame_drawer.py)
  - Depende de: OpenCV (cv2)

## Composición raíz

- [`src/composition_root.py`](src/composition_root.py)
  - Inyecta dependencias explícitamente entre casos de uso y