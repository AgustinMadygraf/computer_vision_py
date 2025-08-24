# pylint: disable=no-member
"""
Path: infrastructure/opencv_stream_camera_usb.py
Implementación de stream de cámara USB usando OpenCV.
"""

import os
from datetime import datetime
import cv2

from src.entities.camera_stream import BaseCameraStream
from src.entities.frame_drawer import IFrameDrawer

class OpenCVCameraStreamUSB(BaseCameraStream):
    "Stream de video USB utilizando OpenCV."
    def __init__(self, frame_drawer: IFrameDrawer, camera_index=0):
        super().__init__(frame_drawer)
        self.camera_index = camera_index
        try:
            self.cap = cv2.VideoCapture(self.camera_index) # pylint: disable=catching-non-exception
            if not self.cap.isOpened():
                print(f"[ERROR] No se pudo abrir la cámara USB en el índice {self.camera_index}")
                self.cap = None
            else:
                self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # pylint: disable=catching-non-exception
                self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # pylint: disable=catching-non-exception
        except (cv2.error, OSError) as e: # pylint: disable=catching-non-exception
            print(f"[CRITICAL] Error al inicializar la cámara USB: {e}")
            self.cap = None

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
        print("[ERROR] No se pudo leer frame de la cámara USB.")
        return None

    def _reconnect(self):
        "Intenta reabrir la cámara si se perdió la conexión."
        try:
            if self.cap:
                self.cap.release()
            self.cap = cv2.VideoCapture(self.camera_index) # pylint: disable=catching-non-exception
        except (cv2.error, OSError) as e: # pylint: disable=catching-non-exception
            print(f"[ERROR] Reconexion USB: {e}")

    def mjpeg_generator(self, quality=80):
        "Generador de stream MJPEG."
        encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), quality] # pylint: disable=catching-non-exception
        while True:
            frame = self.read_frame()
            if frame is None:
                continue
            frame = self.process_frame_callback(frame)
            ret, jpeg = cv2.imencode('.jpg', frame, encode_params) # pylint: disable=catching-non-exception
            if not ret:
                continue
            boundary = b"--frame"
            header = b"Content-Type: image/jpeg\r\n\r\n"
            yield boundary + b"\r\n" + header + jpeg.tobytes() + b"\r\n"

    def save_snapshot(self, path=None):
        "Guarda un snapshot del stream de video. Retorna la ruta si fue exitoso, None si falla."
        frame = self.read_frame()
        if frame is None:
            print("[ERROR] No se pudo capturar snapshot USB.")
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
                print("[ERROR] Guardando snapshot USB: cv2.imwrite falló")
                return None
        except (cv2.error, OSError) as e: # pylint: disable=catching-non-exception
            print(f"[ERROR] Guardando snapshot USB: {e}")
            return None

    def release(self):
        "Libera los recursos de la cámara."
        try:
            if self.cap:
                self.cap.release()
        except (cv2.error, OSError) as e: # pylint: disable=catching-non-exception
            print(f"[ERROR] Liberando cámara USB: {e}")
        super().release()
