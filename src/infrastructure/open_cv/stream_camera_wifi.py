# pylint: disable=no-member
"""
Path: src/infrastructure/opencv_camera_stream_wifi.py
"""

import os
from time import sleep
from datetime import datetime
import cv2

from src.shared.logger import get_logger

from src.entities.camera_stream import BaseCameraStream
from src.infrastructure.open_cv.color_quantization import cuantizar_color_bgr
from src.entities.filter_factory import FilterFactory

class OpenCVCameraStreamWiFi(BaseCameraStream):
    "Stream de video RTSP sobre WiFi utilizando OpenCV."
    logger = get_logger("OpenCVCameraStreamWiFi")
    def __init__(self, ip, user, password, filter_type=None):
        frame_processor = FilterFactory.get_filter(filter_type) if filter_type else None
        super().__init__(frame_processor)
        self.ip = ip
        self.user = user
        self.password = password
        self.frame_processor = frame_processor
        try:
            self.logger.info("Inicializando OpenCVCameraStreamWiFi con IP=%s, USER=%s", ip, user)
            os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp|stimeout;5001000"
            self.rtsp_url = (
                f"rtsp://{ip}:554/"
                f"user={user}&"
                f"password={password}&"
                f"channel=1&"
                f"stream=0.sdp"
            )
            self.logger.info("RTSP URL: %s", self.rtsp_url)
            self.cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
            if not self.cap.isOpened():
                self.logger.error("No se pudo abrir el stream RTSP con OpenCV.")
                raise RuntimeError("No se pudo abrir el stream RTSP con OpenCV.")
            ok = False
            for i in range(20):
                try:
                    ok, _frame = self.cap.read()
                except cv2.error as e: # pylint: disable=catching-non-exception
                    self.logger.error("Error al leer frame inicial: %s", e)
                    ok = False
                if ok:
                    self.logger.info("Frame inicial leído correctamente en intento %d.", i+1)
                    break
                else:
                    self.logger.warning("Intento %d fallido al leer frame inicial.", i+1)
                sleep(0.1)
            if not ok:
                self.logger.error("No se pudo obtener el primer frame del RTSP.")
                raise RuntimeError("No se pudo obtener el primer frame del RTSP.")
            self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.logger.info("Resolución de cámara WiFi: %dx%d", self.width, self.height)
        except (cv2.error, OSError) as e: # pylint: disable=catching-non-exception
            self.logger.critical("Error crítico al inicializar el stream de cámara: %s", e)
            raise

    def get_resolution(self):
        "Obtiene la resolución del stream de video."
        try:
            if self.cap and self.cap.isOpened():
                self.logger.info("Resolución actual: %dx%d", self.width, self.height)
                return super().get_resolution()
            self.logger.warning("get_resolution: Cámara no abierta.")
            return None
        except (cv2.error, OSError) as e: # pylint: disable=catching-non-exception
            self.logger.error("get_resolution: %s", e)
            return None

    def read_frame(self, max_retries=3):
        "Lee un frame del stream de video. Reintenta si falla y reconecta si es necesario."
        for i in range(max_retries):
            if self.cap and self.cap.isOpened():
                try:
                    _ok, _frame = self.cap.read()
                except cv2.error as e: # pylint: disable=catching-non-exception
                    self.logger.error("Error al leer frame: %s", e)
                    _ok, _frame = False, None
                if _ok and _frame is not None:
                    return _frame
                else:
                    self.logger.warning("Frame no leído en intento %d.", i+1)
            else:
                self.logger.warning("Cámara no abierta en intento %d.", i+1)
            self._reconnect()
            sleep(0.1)
        self.logger.error("No se pudo leer frame de la cámara WiFi tras varios intentos.")
        return None

    def _reconnect(self):
        "Intenta reabrir el stream RTSP si se perdió la conexión."
        try:
            self.logger.info("Intentando reconectar el stream RTSP...")
            self.cap.release()
        except cv2.error as e: # pylint: disable=catching-non-exception
            self.logger.error("Error al liberar recursos de la cámara: %s", e)
        try:
            self.cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
            for i in range(20):
                try:
                    ok, _frame = self.cap.read()
                except cv2.error as e: # pylint: disable=catching-non-exception
                    self.logger.error("Error al leer frame tras reconexión: %s", e)
                    ok = False
                if ok:
                    self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    self.logger.info("Reconexión exitosa en intento %d. Resolución: %dx%d", i+1, self.width, self.height)
                    break
                else:
                    self.logger.warning("Intento %d fallido al leer frame tras reconexión.", i+1)
                sleep(0.1)
        except OSError as e:
            self.logger.critical("Error crítico al reconectar el stream de cámara: %s", e)

    def mjpeg_generator(self, quality=80):
        "Generador de stream MJPEG con control de filtro y cuantización de color."
        encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        while True:
            try:
                frame = self.read_frame()
                if frame is None:
                    self.logger.warning("mjpeg_generator: frame es None.")
                    sleep(0.05)
                    continue
                if self.filter_enabled and self.frame_processor:
                    frame = self.frame_processor.process(frame)
                    # Aplica cuantización de color
                    frame = cuantizar_color_bgr(frame, levels_per_channel=6, mode='posterize')
                frame = cv2.flip(frame, 0)  # Voltea la imagen verticalmente
                ok, jpg = cv2.imencode(".jpg", frame, encode_params)
                if not ok:
                    self.logger.warning("mjpeg_generator: cv2.imencode falló.")
                    continue
                yield (b"--frame\r\n"
                       b"Content-Type: image/jpeg\r\n\r\n" +
                       jpg.tobytes() +
                       b"\r\n")
            except cv2.error as e: # pylint: disable=catching-non-exception
                self.logger.error("Error en mjpeg_generator: %s", e)
                sleep(0.1)
            except RuntimeError as e:
                self.logger.error("Error inesperado en mjpeg_generator: %s", e)
                sleep(0.1)

    def save_snapshot(self, path=None):
        "Guarda un snapshot del stream de video. Retorna la ruta si fue exitoso, None si falla."
        try:
            frame = self.read_frame()
            if frame is None:
                self.logger.error("No se pudo capturar snapshot WiFi.")
                return None
            if self.frame_processor:
                frame = self.frame_processor.process(frame)
            frame = cv2.flip(frame, 0)  # Voltea la imagen verticalmente
            if path is None:
                snapshots_dir = os.path.join("static", "snapshots")
                os.makedirs(snapshots_dir, exist_ok=True)
                filename = f"wifi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                path = os.path.join(snapshots_dir, filename)
            ok = cv2.imwrite(path, frame)
            if ok:
                self.logger.info("Snapshot guardado en %s", path)
                return path
            else:
                self.logger.error("Guardando snapshot WiFi: cv2.imwrite falló")
                return None
        except (cv2.error, OSError) as e: # pylint: disable=catching-non-exception
            self.logger.error("Guardando snapshot WiFi: %s", e)
            return None

    def release(self):
        "Libera los recursos de la cámara."
        try:
            self.logger.info("Liberando recursos de la cámara WiFi...")
            self.cap.release()
        except cv2.error as e: # pylint: disable=catching-non-exception
            self.logger.error("Error al liberar recursos de la cámara: %s", e)
        super().release()
