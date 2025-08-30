"""
Path: src/infrastructure/open_cv/color_quantization.py
Cuantización uniforme de color a 8×8×8 niveles por canal (512 colores) para imágenes BGR OpenCV.
Opciones: modo 'posterize' (bit-shift), 'rescale' (lineal), dither opcional.
API: cuantizar_color_bgr(frame, levels_per_channel=8, mode='posterize', dither=False)
Entrada/salida: np.ndarray BGR, uint8, shape (H, W, 3)
"""
import numpy as np

# Feature flag global (puede ser gestionado por config externa)
CUANTIZACION_COLOR_ACTIVA = True


def cuantizar_color_bgr(frame: np.ndarray, levels_per_channel: int = 8, mode: str = 'posterize', dither: bool = False) -> np.ndarray:
    """
    Aplica cuantización uniforme de color a una imagen BGR (uint8).
    Args:
        frame: np.ndarray, imagen BGR, uint8, shape (H, W, 3)
        levels_per_channel: int, niveles por canal (default 8)
        mode: 'posterize' (bit-shift) o 'rescale' (lineal)
        dither: bool, aplica dither si True (no implementado)
    Returns:
        np.ndarray, imagen BGR cuantizada
    """
    if not CUANTIZACION_COLOR_ACTIVA:
        return frame
    if mode == 'posterize':
        # Posterización por bit-shift
        bits = int(np.log2(levels_per_channel))
        shift = 8 - bits
        quantized = (frame >> shift) << shift
    elif mode == 'rescale':
        # Reescalado uniforme
        step = 256 // levels_per_channel
        quantized = (frame // step) * step
    else:
        raise ValueError(f"Modo de cuantización desconocido: {mode}")
    # Dither opcional (placeholder)
    if dither:
        pass  # Implementar si se requiere
    return quantized
