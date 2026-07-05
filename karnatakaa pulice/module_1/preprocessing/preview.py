from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


def save_mask_preview(path: Path, image: np.ndarray, mask: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rgb = image_to_rgb(image)
    overlay = rgb.copy()

    cloud = mask == 1
    shadow = mask == 2
    nodata = mask == 255
    overlay[cloud] = blend(overlay[cloud], np.array([255, 255, 255], dtype=np.uint8), 0.55)
    overlay[shadow] = blend(overlay[shadow], np.array([64, 110, 255], dtype=np.uint8), 0.55)
    overlay[nodata] = np.array([0, 0, 0], dtype=np.uint8)

    preview = np.concatenate([rgb, overlay], axis=1)
    Image.fromarray(preview).save(path)


def image_to_rgb(image: np.ndarray) -> np.ndarray:
    if image.shape[0] >= 3:
        bands = image[:3]
    else:
        bands = np.repeat(image[:1], 3, axis=0)

    rgb = []
    for band in bands:
        band = band.astype(np.float32)
        finite = np.isfinite(band)
        if finite.any():
            lo, hi = np.percentile(band[finite], [2, 98])
        else:
            lo, hi = 0, 1
        scaled = np.clip((band - lo) / (hi - lo + 1e-6), 0, 1)
        rgb.append((scaled * 255).astype(np.uint8))
    return np.moveaxis(np.stack(rgb, axis=0), 0, -1)


def blend(base: np.ndarray, color: np.ndarray, alpha: float) -> np.ndarray:
    return ((1 - alpha) * base + alpha * color).astype(np.uint8)
