"""
Path: src/shared/config.py
Configura y expone las variables de entorno necesarias para la aplicación.
"""

import os
from dotenv import load_dotenv

load_dotenv()

def get_env(var_name, default=None):
    "Obtiene una variable de entorno"
    return os.environ.get(var_name, default)

def get_config():
    "Devuelve las variables de entorno actuales."
    config = {
        "IP": get_env("IP"),
        "USER": get_env("USER"),
        "PASSWORD": get_env("PASSWORD"),
        "MODE": get_env("MODE"),
        "IMAGE_PATH": get_env("IMAGE_PATH"),
    }
    # Validar variables críticas
    if config["MODE"] is None:
        print("[ERROR] La variable de entorno MODE no está definida. Verifica tu archivo .env.")
        exit(1)
    return config

def get_static_path():
    "Obtiene la ruta base de archivos estáticos"
    return get_env("STATIC_PATH", "static")
