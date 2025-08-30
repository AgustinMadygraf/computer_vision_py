# pylint: disable=no-member
"""
Path: src/infrastructure/opencv_imagen_stream.py
Clase para simular el stream de cámara usando una imagen fija en modo desarrollo.
"""

import cv2

from src.shared.logger import get_logger

from src.entities.camera_stream import BaseCameraStream
from src.infrastructure.open_cv.color_quantization import cuantizar_color_bgr

class ImageStream(BaseCameraStream):
    "Clase para simular el stream de cámara usando una imagen fija en modo desarrollo."
    logger = get_logger("ImageStream")
    def __init__(self, image_path=None, frame_processor=None):
        super().__init__(frame_processor)
        self.image_path = str(image_path) if image_path else None
        self.frame_processor = frame_processor

    def get_resolution(self):
        "Devuelve la resolución de la imagen cargada."
        try:
            image = cv2.imread(self.image_path)
            if image is None:
                raise FileNotFoundError(f"No se pudo cargar la imagen: {self.image_path}")
            height, width = image.shape[:2]
            self.width = width
            self.height = height
            return super().get_resolution()
        except FileNotFoundError as e:
            self.logger.error("get_resolution: %s", e)
            return None, None
        except cv2.error as e:  # pylint: disable=catching-non-exception
            self.logger.error("get_resolution (cv2): %s", e)
            return None, None

    def mjpeg_generator(self, quality=80):
        "Generador MJPEG simulado para la imagen fija en formato MJPEG estándar."
        try:
            image = cv2.imread(self.image_path)
            if image is None:
                raise FileNotFoundError(f"No se pudo cargar la imagen: {self.image_path}")
            # Aplica el callback de procesamiento de frame si está definido
            if self.process_frame_callback:
                image = self.process_frame_callback(image)
            # Aplica cuantización de color
            image = cuantizar_color_bgr(image, levels_per_channel=8, mode='posterize')
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
            ret, jpeg = cv2.imencode('.jpg', image, encode_param)
            if not ret:
                raise RuntimeError("No se pudo codificar la imagen como JPEG")
            _frame = jpeg.tobytes()
            boundary = b"--frame"
            header = b"Content-Type: image/jpeg\r\n\r\n"
            yield boundary + b"\r\n" + header + _frame + b"\r\n"
        except FileNotFoundError as e:
            self.logger.error("mjpeg_generator: %s", e)
            boundary = b"--frame"
            header = b"Content-Type: text/plain\r\n\r\n"
            error_msg = f"Error: {e}".encode()
            while True:
                yield boundary + b"\r\n" + header + error_msg + b"\r\n"
        except cv2.error as e:  # pylint: disable=catching-non-exception
            self.logger.error("mjpeg_generator (cv2): %s", e)
            boundary = b"--frame"
            header = b"Content-Type: text/plain\r\n\r\n"
            error_msg = f"Error: {e}".encode()
            while True:
                yield boundary + b"\r\n" + header + error_msg + b"\r\n"
        except RuntimeError as e:
            self.logger.error("mjpeg_generator (Runtime): %s", e)
            boundary = b"--frame"
            header = b"Content-Type: text/plain\r\n\r\n"
            error_msg = f"Error: {e}".encode()
            while True:
                yield boundary + b"\r\n" + header + error_msg + b"\r\n"

    def save_snapshot(self, path=None):
        "Guarda la imagen fija en el path indicado."
        try:
            image = cv2.imread(self.image_path)
            if image is None:
                raise FileNotFoundError(f"No se pudo cargar la imagen: {self.image_path}")
            # Aplica el callback para dibujar la línea
            image = self.process_frame_callback(image)
            save_path = path or "snapshot.jpg"
            cv2.imwrite(save_path, image)
            return save_path
        except FileNotFoundError as e:
            self.logger.error("save_snapshot (FileNotFoundError): %s", e)
            return None
        except cv2.error as e:  # pylint: disable=catching-non-exception
            self.logger.error("save_snapshot (cv2): %s", e)
            return None

    def release(self):
        "No hay recursos que liberar en el modo imagen, pero se mantiene la interfaz."
        pass # pylint: disable=unnecessary-pass
