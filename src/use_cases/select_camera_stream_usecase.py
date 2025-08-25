"""
Path: src/use_cases/select_camera_stream_usecase.py
Caso de uso para seleccionar el stream de cámara según preferencia (USB > WiFi > Imagen).
"""
from src.infrastructure.open_cv.stream_camera_usb import OpenCVCameraStreamUSB
from src.infrastructure.open_cv.stream_camera_wifi import OpenCVCameraStreamWiFi
from src.infrastructure.open_cv.stream_imagen import ImageStream

class SelectCameraStreamUseCase:
    "Caso de uso para seleccionar el stream de cámara adecuado."
    def __init__(self, cameras, image_path=None, frame_drawer=None):
        self.cameras = cameras
        self.image_path = image_path
        self.frame_drawer = frame_drawer

    def execute(self):
        "Devuelve la instancia de stream según la preferencia: USB > WiFi > Imagen."
        if self.cameras["usb"]:
            camera_index = self.cameras["usb"][0]
            return OpenCVCameraStreamUSB(camera_index, self.frame_drawer)
        elif self.cameras["wifi"]:
            wifi = self.cameras["wifi"][0]
            return OpenCVCameraStreamWiFi(wifi["ip"], wifi["user"], wifi["password"], self.frame_drawer)
        elif self.image_path:
            return ImageStream(self.image_path, self.frame_drawer)
        raise RuntimeError("No se pudo inicializar el stream de cámara.")
