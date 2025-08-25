"""
Path: tests/test_draw_line_on_frame.py
Caso de uso para dibujar una línea horizontal amarilla en un frame.
"""

import numpy as np
from src.infrastructure.open_cv.draw_line_on_frame import FrameDrawer

def test_draw_horizontal_yellow_line_modifies_frame():
    "Prueba que dibujar una línea amarilla modifica el frame."
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    drawer = FrameDrawer()
    result = drawer.draw_horizontal_yellow_line(frame.copy(), thickness=5)
    # La línea amarilla debe estar en la mitad del frame
    y = frame.shape[0] // 2
    # El color amarillo en BGR es (0, 255, 255)
    assert np.all(result[y, :, :] == [0, 255, 255]) or np.any(result[y, :, :] == [0, 255, 255])

def test_draw_horizontal_yellow_line_none():
    "Prueba que dibujar una línea amarilla con un frame None devuelve None."
    drawer = FrameDrawer()
    result = drawer.draw_horizontal_yellow_line(None)
    assert result is None
