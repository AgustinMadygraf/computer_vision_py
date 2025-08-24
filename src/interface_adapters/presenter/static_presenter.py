"""
Path: interface_adapters/presenter/static_presenter.py
"""

def present_static_file(content: bytes, mime_type: str, status_code: int = 200):
    "Presenta un archivo estático"
    return {
        "content": content,
        "mime_type": mime_type,
        "status_code": status_code
    }

def present_not_found():
    "Presenta un error 404"
    return {
        "content": b"Archivo no encontrado",
        "mime_type": "text/html",
        "status_code": 404
    }
