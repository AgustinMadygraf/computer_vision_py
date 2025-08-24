# pylint: disable=no-member

"""
Path: src/infrastructure/opencv_camera_stream_wifi.py
"""

import os
from time import sleep
from datetime import datetime
import cv2
from src.entities.camera_stream import BaseCameraStream

class OpenCVCameraStreamWiFi(BaseCameraStream):
    "Stream de video RTSP sobre WiFi utilizando OpenCV."
    def __init__(self, ip, user, password, draw_line_fn):
        super().__init__(draw_line_fn)
        try:
            print(f"[INFO] Inicializando OpenCVCameraStreamWiFi con IP={ip}, USER={user}")
            os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp|stimeout;5001000"
            self.rtsp_url = (
                f"rtsp://{ip}:554/"
                f"user={user}&"
                f"password={password}&"
                f"channel=1&"
                f"stream=0.sdp"
            )
            print(f"[INFO] RTSP URL: {self.rtsp_url}")
            self.cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
            if not self.cap.isOpened():
                print("[ERROR] No se pudo abrir el stream RTSP con OpenCV.")
                raise RuntimeError("No se pudo abrir el stream RTSP con OpenCV.")
            ok = False
            for i in range(20):
                try:
                    ok, _frame = self.cap.read()
                except cv2.error as e: # pylint: disable=catching-non-exception
                    print(f"[ERROR] Error al leer frame inicial: {e}")
                    ok = False
                if ok:
                    print(f"[INFO] Frame inicial leído correctamente en intento {i+1}.")
                    break
                else:
                    print(f"[WARN] Intento {i+1} fallido al leer frame inicial.")
                sleep(0.1)
            if not ok:
                print("[ERROR] No se pudo obtener el primer frame del RTSP.")
                raise RuntimeError("No se pudo obtener el primer frame del RTSP.")
            self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print(f"[INFO] Resolución de cámara WiFi: {self.width}x{self.height}")
        except (cv2.error, OSError) as e: # pylint: disable=catching-non-exception
            print(f"[CRITICAL] Error crítico al inicializar el stream de cámara: {e}")
            raise

    def get_resolution(self):
        "Obtiene la resolución del stream de video."
        try:
            if self.cap and self.cap.isOpened():
                print(f"[INFO] Resolución actual: {self.width}x{self.height}")
                return super().get_resolution()
            print("[WARN] get_resolution: Cámara no abierta.")
            return None
        except (cv2.error, OSError) as e: # pylint: disable=catching-non-exception
            print(f"[ERROR] get_resolution: {e}")
            return None

    def read_frame(self, max_retries=3):
        "Lee un frame del stream de video. Reintenta si falla y reconecta si es necesario."
        for i in range(max_retries):
            if self.cap and self.cap.isOpened():
                try:
                    _ok, _frame = self.cap.read()
                except cv2.error as e: # pylint: disable=catching-non-exception
                    print(f"[ERROR] Error al leer frame: {e}")
                    _ok, _frame = False, None
                if _ok and _frame is not None:
                    return _frame
                else:
                    print(f"[WARN] Frame no leído en intento {i+1}.")
            else:
                print(f"[WARN] Cámara no abierta en intento {i+1}.")
            self._reconnect()
            sleep(0.1)
        print("[ERROR] No se pudo leer frame de la cámara WiFi tras varios intentos.")
        return None

    def _reconnect(self):
        "Intenta reabrir el stream RTSP si se perdió la conexión."
        try:
            print("[INFO] Intentando reconectar el stream RTSP...")
            self.cap.release()
        except cv2.error as e: # pylint: disable=catching-non-exception
            print(f"[ERROR] Error al liberar recursos de la cámara: {e}")
        try:
            self.cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
            for i in range(20):
                try:
                    ok, _frame = self.cap.read()
                except cv2.error as e: # pylint: disable=catching-non-exception
                    print(f"[ERROR] Error al leer frame tras reconexión: {e}")
                    ok = False
                if ok:
                    self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    print(
                        f"[INFO] Reconexión exitosa en intento {i+1}. "
                        f"Resolución: {self.width}x{self.height}"
                    )
                    break
                else:
                    print(f"[WARN] Intento {i+1} fallido al leer frame tras reconexión.")
                sleep(0.1)
        except OSError as e:
            print(f"[CRITICAL] Error crítico al reconectar el stream de cámara: {e}")

    def mjpeg_generator(self, quality=80):
        "Generador de stream MJPEG."
        encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        while True:
            try:
                frame = self.read_frame()
                if frame is None:
                    print("[WARN] mjpeg_generator: frame es None.")
                    sleep(0.05)
                    continue
                frame = self.process_frame_callback(frame)
                frame = cv2.flip(frame, 0)  # Voltea la imagen verticalmente
                ok, jpg = cv2.imencode(".jpg", frame, encode_params)
                if not ok:
                    print("[WARN] mjpeg_generator: cv2.imencode falló.")
                    continue
                yield (b"--frame\r\n"
                       b"Content-Type: image/jpeg\r\n\r\n" +
                       jpg.tobytes() +
                       b"\r\n")
            except cv2.error as e: # pylint: disable=catching-non-exception
                print(f"[ERROR] Error en mjpeg_generator: {e}")
                sleep(0.1)
            except RuntimeError as e:
                print(f"[ERROR] Error inesperado en mjpeg_generator: {e}")
                sleep(0.1)

    def save_snapshot(self, path=None):
        "Guarda un snapshot del stream de video. Retorna la ruta si fue exitoso, None si falla."
        try:
            frame = self.read_frame()
            if frame is None:
                print("[ERROR] No se pudo capturar snapshot WiFi.")
                return None
            frame = self.process_frame_callback(frame)
            frame = cv2.flip(frame, 0)  # Voltea la imagen verticalmente
            if path is None:
                snapshots_dir = os.path.join("static", "snapshots")
                os.makedirs(snapshots_dir, exist_ok=True)
                filename = f"wifi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                path = os.path.join(snapshots_dir, filename)
            ok = cv2.imwrite(path, frame)
            if ok:
                print(f"[INFO] Snapshot guardado en {path}")
                return path
            else:
                print("[ERROR] Guardando snapshot WiFi: cv2.imwrite falló")
                return None
        except (cv2.error, OSError) as e: # pylint: disable=catching-non-exception
            print(f"[ERROR] Guardando snapshot WiFi: {e}")
            return None

    def release(self):
        "Libera los recursos de la cámara."
        try:
            print("[INFO] Liberando recursos de la cámara WiFi...")
            self.cap.release()
        except cv2.error as e: # pylint: disable=catching-non-exception
            print(f"[ERROR] Error al liberar recursos de la cámara: {e}")
        super().release()
