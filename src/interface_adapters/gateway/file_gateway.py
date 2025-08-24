"""
Path: interface_adapters/gateway/file_gateway.py
"""

import os

def get_file(path: str) -> bytes | None:
    "Obtiene el contenido de un archivo"
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()
    return None
