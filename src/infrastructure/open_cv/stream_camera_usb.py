# pylint: disable=no-member
"""
Path: infrastructure/opencv_stream_camera_usb.py
Implementación de stream de cámara USB usando OpenCV.
"""

import os
from datetime import datetime
import cv2

from src.use_cases.get_filter_state_usecase import GetFilterStateUseCase
from src.entities.camera_stream import BaseCameraStream
from src.shared.logger import get_logger
class OpenCVCameraStreamUSB(BaseCameraStream):
    "Implementación de stream de cámara USB usando OpenCV."
    logger = get_logger("OpenCVCameraStreamUSB")
    def __init__(self, camera_index=0, frame_processor=None):
        super().__init__(frame_processor)
        self.camera_index = int(camera_index) if camera_index is not None else 0
        self.frame_processor = frame_processor
        self.cap = None
        self.filter_enabled = False  # Nuevo atributo
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if self.cap.isOpened():
                self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            else:
                self.width = None
                self.height = None
        except (cv2.error, OSError) as e:  # pylint: disable=catching-non-exception
            self.logger.error("Error inicializando cámara USB: %s", e)

    def get_resolution(self):
        "Obtiene la resolución del stream de video."
        if self.cap and self.cap.isOpened():
            return super().get_resolution()
        return None

    def read_frame(self, max_retries=3):
        "Lee un frame del stream de video. Reintenta si falla."
        for _ in range(max_retries):
            if self.cap and self.cap.isOpened():
                ok, frame = self.cap.read()
                if ok:
                    return frame
            self._reconnect()
        self.logger.error("No se pudo leer frame de la cámara USB.")
        return None

    def _reconnect(self):
        "Intenta reabrir la cámara si se perdió la conexión."
        try:
            if self.cap:
                self.cap.release()
            self.cap = cv2.VideoCapture(self.camera_index) # pylint: disable=catching-non-exception
        except (cv2.error, OSError) as e: # pylint: disable=catching-non-exception
            self.logger.error("Reconexion USB: %s", e)

    def set_filter_enabled(self, enabled: bool):
        "Habilita o deshabilita el filtro."
        self.filter_enabled = enabled

    def mjpeg_generator(self, quality=80, ws=None):
        "Generador de stream MJPEG con control de filtro por atributo interno."
        encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        while True:
            frame = self.read_frame()
            if frame is None:
                continue
            if self.filter_enabled:
                frame = self.process_frame_callback(frame)
                _frame_tipo = "con línea"
            else:
                _frame_tipo = "sin línea"
            ret, jpeg = cv2.imencode('.jpg', frame, encode_params)
            if not ret:
                continue
            boundary = b"--frame"
            header = b"Content-Type: image/jpeg\r\n\r\n"
            yield boundary + b"\r\n" + header + jpeg.tobytes() + b"\r\n"

    def save_snapshot(self, path=None):
        "Guarda un snapshot del stream de video. Retorna la ruta si fue exitoso, None si falla."
        frame = self.read_frame()
        if frame is None:
            self.logger.error("No se pudo capturar snapshot USB.")
            return None
        frame = self.process_frame_callback(frame)
        if path is None:
            snapshots_dir = os.path.join("static", "snapshots")
            os.makedirs(snapshots_dir, exist_ok=True)
            filename = f"usb_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            path = os.path.join(snapshots_dir, filename)
        try:
            ok = cv2.imwrite(path, frame) # pylint: disable=catching-non-exception
            if ok:
                return path
            else:
                self.logger.error("Guardando snapshot USB: cv2.imwrite falló")
                return None
        except (cv2.error, OSError) as e: # pylint: disable=catching-non-exception
            self.logger.error("Guardando snapshot USB: %s", e)
            return None

    def release(self):
        "Libera los recursos de la cámara."
        try:
            if self.cap:
                self.cap.release()
        except (cv2.error, OSError) as e: # pylint: disable=catching-non-exception
            self.logger.error("Liberando cámara USB: %s", e)
        super().release()
