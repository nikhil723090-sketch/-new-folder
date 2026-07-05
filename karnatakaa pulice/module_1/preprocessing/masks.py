from __future__ import annotations

import numpy as np
from skimage import exposure, morphology


CLEAR = np.uint8(0)
CLOUD = np.uint8(1)
SHADOW = np.uint8(2)
NODATA = np.uint8(255)


def robust_rescale(band: np.ndarray, nodata_mask: np.ndarray) -> np.ndarray:
    valid = band[~nodata_mask]
    if valid.size == 0:
        return np.zeros_like(band, dtype=np.float32)
    p2, p98 = np.percentile(valid, [2, 98])
    if p98 <= p2:
        p2, p98 = float(valid.min()), float(valid.max() + 1)
    return exposure.rescale_intensity(band.astype(np.float32), in_range=(p2, p98), out_range=(0, 1))


def create_cloud_shadow_mask(
    image: np.ndarray,
    nodata_value: float | int | None = None,
    min_cloud_size: int = 96,
    min_shadow_size: int = 96,
    cloud_dilation: int = 4,
) -> np.ndarray:
    """
    Create a practical LISS-IV cloud/shadow mask from multispectral imagery.

    Assumption for LISS-IV MX style data:
    - first visible bands are green/red-like bands
    - last band is near infrared when 3 or 4 bands are present
    """
    if image.ndim != 3:
        raise ValueError("Expected image shape as (bands, height, width).")

    nodata_mask = np.zeros(image.shape[1:], dtype=bool)
    if nodata_value is not None:
        nodata_mask = np.all(image == nodata_value, axis=0)
    nodata_mask |= ~np.all(np.isfinite(image), axis=0)

    scaled = np.stack([robust_rescale(b, nodata_mask) for b in image], axis=0)
    visible = scaled[: min(3, scaled.shape[0])]
    brightness = visible.mean(axis=0)
    whiteness = visible.std(axis=0)
    nir = scaled[-1]
    red = scaled[min(1, scaled.shape[0] - 1)]
    ndvi = (nir - red) / (nir + red + 1e-6)

    cloud = (
        (brightness > 0.68)
        & (whiteness < 0.18)
        & (ndvi < 0.45)
        & ~nodata_mask
    )
    cloud |= (brightness > 0.86) & ~nodata_mask
    cloud = morphology.remove_small_objects(cloud, min_size=min_cloud_size)
    cloud = morphology.binary_closing(cloud, morphology.disk(2))
    cloud = morphology.binary_dilation(cloud, morphology.disk(cloud_dilation))

    dark = (brightness < 0.22) & (nir < 0.28) & ~nodata_mask
    cloud_buffer = morphology.binary_dilation(cloud, morphology.disk(20))
    shadow = dark & cloud_buffer & ~cloud
    shadow = morphology.remove_small_objects(shadow, min_size=min_shadow_size)
    shadow = morphology.binary_closing(shadow, morphology.disk(2))

    mask = np.full(image.shape[1:], CLEAR, dtype=np.uint8)
    mask[cloud] = CLOUD
    mask[shadow] = SHADOW
    mask[nodata_mask] = NODATA
    return mask
