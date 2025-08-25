"""
Path: src/shared/logger.py
Logger centralizado para la aplicación.
"""
import logging
import os

class FastAPIStyleFormatter(logging.Formatter):
    "Formatter para logs al estilo de FastAPI."
    COLORS = {
        'INFO': '\033[32m',      # Verde
        'WARNING': '\033[33m',   # Amarillo
        'ERROR': '\033[31m',     # Rojo
        'CRITICAL': '\033[31m',  # Rojo
        'DEBUG': '\033[36m',     # Cyan
        'RESET': '\033[0m',
    }

    def format(self, record):
        level = record.levelname
        color = self.COLORS.get(level, '')
        reset = self.COLORS['RESET']
        # Ejemplo: INFO:    mensaje
        # Espaciado para alinear los mensajes
        level_str = f"{color}{level}:{reset}"
        # 7 espacios después del levelname para alineación visual
        pad = ' ' * (7 - len(level)) if len(level) < 7 else ' '
        msg = f"{level_str}{pad}{record.getMessage()}"
        return msg

def get_logger(name: str = "computer_vision"):
    "Obtiene un logger configurado para la aplicación."
    level = os.environ.get("CV_DEBUG", "INFO").upper()
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = FastAPIStyleFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
