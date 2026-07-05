from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import rasterio


SUPPORTED_RASTER_SUFFIXES = {".tif", ".tiff", ".img"}


def list_rasters(path: Path) -> list[Path]:
    """Return rasters from a file or directory in a stable order."""
    path = Path(path)
    if path.is_file():
        return [path]
    return sorted(
        p for p in path.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_RASTER_SUFFIXES
    )


def match_by_stem(primary: Iterable[Path], secondary_dir: Path) -> dict[Path, Path]:
    """Match files by stem, allowing common suffixes like _mask or _cloudfree."""
    secondary = list_rasters(secondary_dir)
    index: dict[str, Path] = {}
    for path in secondary:
        stem = normalized_stem(path)
        index[stem] = path

    pairs: dict[Path, Path] = {}
    for path in primary:
        stem = normalized_stem(path)
        if stem in index:
            pairs[path] = index[stem]
    return pairs


def normalized_stem(path: Path) -> str:
    stem = path.stem.lower()
    for token in ("_cloudy", "_cloudfree", "_clear", "_target", "_mask", "_registered"):
        stem = stem.replace(token, "")
    return stem


def read_raster(path: Path, masked: bool = True) -> tuple[np.ndarray, dict]:
    with rasterio.open(path) as src:
        data = src.read(masked=masked)
        profile = src.profile.copy()
    if masked and np.ma.isMaskedArray(data):
        data = data.filled(profile.get("nodata", 0))
    return np.asarray(data), profile


def write_raster(path: Path, data: np.ndarray, profile: dict, dtype: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    out_profile = profile.copy()
    if data.ndim == 2:
        count = 1
    else:
        count = data.shape[0]
    out_profile.update(
        driver="GTiff",
        count=count,
        dtype=dtype or str(data.dtype),
        compress="deflate",
        tiled=True,
        BIGTIFF="IF_SAFER",
    )
    with rasterio.open(path, "w", **out_profile) as dst:
        if data.ndim == 2:
            dst.write(data, 1)
        else:
            dst.write(data)
