
"""
Path: infrastructure/fastapi/streamer_adapter.py
"""

from fastapi import APIRouter, WebSocket, HTTPException, Query
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse

from src.infrastructure.fastapi.websocket_server import websocket_endpoint
from src.infrastructure.open_cv.stream_camera_usb import OpenCVCameraStreamUSB
from src.infrastructure.open_cv.stream_camera_wifi import OpenCVCameraStreamWiFi
from src.infrastructure.open_cv.stream_imagen import ImageStream
from src.shared.config import get_config
from src.use_cases.discover_cameras_usecase import DiscoverCamerasUseCase
from src.interface_adapters.controllers.stream_controller import StreamController

router = APIRouter(tags=["stream"])

@router.get("/cameras/refresh", tags=["stream"])
def refresh_cameras():
    "Endpoint para recargar y devolver la lista actual de cámaras USB y WiFi."
    usecase = DiscoverCamerasUseCase()
    cameras = usecase.execute()
    return {"cameras": cameras}

streams = {}

def get_stream_instance(stream_type: str, index: int):
    "Obtiene o crea la instancia de stream correspondiente."
    key = (stream_type, index)
    if key in streams:
        return streams[key]
    config = get_config()
    stream_controller = StreamController()
    if stream_type == "usb":
        instance = OpenCVCameraStreamUSB(index, stream_controller.draw_line_on_frame)
    elif stream_type == "wifi":
        wifi_list = config.get("WIFI_CAMERAS", [])
        if index >= len(wifi_list):
            raise HTTPException(status_code=404, detail="Cámara WiFi no encontrada")
        cam_conf = wifi_list[index]
        instance = OpenCVCameraStreamWiFi(
            cam_conf["ip"],
            cam_conf.get("user", ""),
            cam_conf.get("password", ""),
            stream_controller.draw_line_on_frame
        )
    elif stream_type == "img":
        image_path = config.get("IMAGE_PATH")
        instance = ImageStream(image_path=image_path, frame_processor=stream_controller.draw_line_on_frame)
    else:
        raise HTTPException(status_code=400, detail="Tipo de stream no soportado")
    streams[key] = instance
    return instance

@router.get("/usb/{index}/snapshot.jpg")
def snapshot_usb_endpoint(index: int):
    "Toma un snapshot del stream MJPEG para la cámara USB en el índice dado"
    try:
        instance = get_stream_instance("usb", index)
        adapter = FastAPICameraHTTPAdapter(instance)
        return adapter.snapshot()
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail})

@router.get("/wifi/{index}/snapshot.jpg")
def snapshot_wifi_endpoint(index: int):
    "Toma un snapshot del stream MJPEG para la cámara WiFi en el índice dado"
    try:
        instance = get_stream_instance("wifi", index)
        adapter = FastAPICameraHTTPAdapter(instance)
        return adapter.snapshot()
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail})

@router.get("/img/{index}/snapshot.jpg")
def snapshot_img_endpoint(index: int):
    "Toma un snapshot del stream MJPEG para la imagen en el índice dado"
    try:
        instance = get_stream_instance("img", index)
        adapter = FastAPICameraHTTPAdapter(instance)
        return adapter.snapshot()
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail})

@router.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    "WebSocket para eventos o streaming en tiempo real"
    await websocket_endpoint(websocket)
class FastAPICameraHTTPAdapter:
    "Adaptador HTTP para exponer los casos de uso de la cámara IP con FastAPI."
    def __init__(self, camera_usecase):
        self.camera_usecase = camera_usecase
        self.width, self.height = self.camera_usecase.get_resolution()

    def stream_mjpeg(self):
        "Stream MJPEG."
        return StreamingResponse(
            self.camera_usecase.mjpeg_generator(quality=80),
            media_type="multipart/x-mixed-replace; boundary=frame"
        )

    def resolution(self):
        "Obtiene la resolución del stream de video."
        return JSONResponse(content={"width": self.width, "height": self.height})

    def snapshot(self):
        "Toma un snapshot del stream de video."
        fname = self.camera_usecase.save_snapshot()
        if fname is None:
            raise HTTPException(status_code=503, detail="No se pudo capturar frame")
        return FileResponse(fname, media_type="image/jpeg")

    def cleanup(self):
        "Libera los recursos de la cámara."
        self.camera_usecase.release()

@router.get("/streams")
def available_streams():
    "Devuelve la lista de streams disponibles para el frontend."
    config = get_config()
    result = {"usb": [], "wifi": [], "img": []}
    # USB: se asume que los índices válidos son 0..N-1 (puede ajustarse según hardware)
    usb_count = config.get("USB_COUNT", 1)
    for i in range(usb_count):
        result["usb"].append({"index": i, "type": "usb", "name": f"USB Camera {i}"})
    # WiFi: lista de cámaras en config
    wifi_list = config.get("WIFI_CAMERAS", [])
    for i, cam in enumerate(wifi_list):
        result["wifi"].append({
            "index": i,
            "type": "wifi",
            "name": cam.get("NAME", f"WiFi Camera {i}"),
            "ip": cam.get("IP")
        })
    # Imagen: lista de rutas en config
    img_list = config.get("IMAGE_PATHS", [])
    for i, path in enumerate(img_list):
        result["img"].append({
            "index": i,
            "type": "img",
            "name": f"Imagen {i}",
            "path": path
        })
    return JSONResponse(content=result)

@router.get("/usb/{index}/stream.mjpg")
def stream_usb_endpoint(index: int, user_id: str = Query(None)):
    "Streaming MJPEG para cámara USB en el índice dado"
    config = get_config()
    usb_cameras = config.get("USB_CAMERAS", [])
    if index not in usb_cameras:
        return JSONResponse(status_code=404,
                            content={"error": f"No se encontró cámara USB en el índice {index}"})
    class DummyWS:
        "Clase dummy para simular el WebSocket"
        def __init__(self, user_id):
            self.user_id = user_id

    ws = DummyWS(user_id if user_id is not None else str(index))
    try:
        instance = get_stream_instance("usb", index)
        _adapter = FastAPICameraHTTPAdapter(instance)
        return StreamingResponse(
            instance.mjpeg_generator(quality=80, ws=ws),
            media_type="multipart/x-mixed-replace; boundary=frame"
        )
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail})
