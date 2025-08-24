"""
Path: infrastructure/fastapi/static_server.py
Corrección para manejo adecuado de archivos estáticos
"""

import os
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

from src.shared.config import get_static_path

from src.infrastructure.fastapi.stream_adapter import router as stream_router
from src.interface_adapters.controllers.static_controller import get_favicon


app = FastAPI(title="Computer Vision", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_path = get_static_path()

src_dir = os.path.join(static_path, "src")


app.mount("/src", StaticFiles(directory=src_dir), name="src")

# Incluir el router de la API
app.include_router(stream_router, prefix="/api/computer_vision", tags=["stream"])

# Ruta para el favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    "Ruta para el favicon"
    result = get_favicon()
    return HTMLResponse(
        content=result["content"],
        media_type=result["mime_type"],
        status_code=result["status_code"]
    )

# Ruta principal y /index.html que sirven el HTML
@app.get("/", response_class=HTMLResponse)
@app.post("/", response_class=HTMLResponse)
@app.get("/index.html", response_class=HTMLResponse)
@app.post("/index.html", response_class=HTMLResponse)
async def read_root():
    "Ruta para el index.html"
    index_path = os.path.join(static_path, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        return HTMLResponse(content=html_content)

# Ruta para manejar otras páginas de la SPA (Single Page Application)
@app.get("/{path:path}", response_class=HTMLResponse)
async def serve_spa(path: str):
    "Ruta para manejar otras páginas de la SPA (Single Page Application)"
    # Evitar capturar rutas de la API
    if path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    public_file = os.path.join(static_path, "public", path)
    src_file = os.path.join(static_path, "src", path)
    if os.path.exists(public_file):
        return FileResponse(public_file)
    elif os.path.exists(src_file):
        return FileResponse(src_file)
    else:
        if path.endswith('.js'):
            raise HTTPException(status_code=404, detail="Archivo JS no encontrado")
        # Si no existe el archivo, servir el index.html
        with open(os.path.join(static_path, "index.html"), "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
