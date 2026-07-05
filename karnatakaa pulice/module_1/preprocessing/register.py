from __future__ import annotations

from pathlib import Path

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject


def align_to_reference(
    source_path: Path,
    reference_path: Path,
    output_path: Path,
    resampling: Resampling = Resampling.bilinear,
    dst_dtype: str | None = None,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with rasterio.open(reference_path) as ref, rasterio.open(source_path) as src:
        profile = src.profile.copy()
        profile.update(
            crs=ref.crs,
            transform=ref.transform,
            width=ref.width,
            height=ref.height,
            compress="deflate",
            tiled=True,
            BIGTIFF="IF_SAFER",
        )
        if dst_dtype:
            profile.update(dtype=dst_dtype)

        destination = np.zeros(
            (src.count, ref.height, ref.width),
            dtype=np.dtype(profile["dtype"]),
        )

        for band_index in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, band_index),
                destination=destination[band_index - 1],
                src_transform=src.transform,
                src_crs=src.crs,
                src_nodata=src.nodata,
                dst_transform=ref.transform,
                dst_crs=ref.crs,
                dst_nodata=src.nodata,
                resampling=resampling,
            )

        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(destination)
