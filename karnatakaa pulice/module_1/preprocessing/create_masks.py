from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import rasterio
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from preprocessing.io import list_rasters, read_raster, write_raster
from preprocessing.masks import create_cloud_shadow_mask
from preprocessing.preview import save_mask_preview


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create LISS-IV cloud/shadow masks.")
    parser.add_argument("--input-dir", required=True, type=Path, help="Cloudy LISS-IV image file or folder.")
    parser.add_argument("--output-dir", required=True, type=Path, help="Folder for mask GeoTIFFs.")
    parser.add_argument("--preview-dir", type=Path, help="Optional folder for side-by-side PNG previews.")
    parser.add_argument("--nodata", type=float, default=None, help="Override nodata value.")
    parser.add_argument("--min-cloud-size", type=int, default=96)
    parser.add_argument("--min-shadow-size", type=int, default=96)
    parser.add_argument("--cloud-dilation", type=int, default=4)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    rasters = list_rasters(args.input_dir)
    if not rasters:
        raise SystemExit(f"No rasters found in {args.input_dir}")

    for image_path in tqdm(rasters, desc="Creating masks"):
        image, profile = read_raster(image_path, masked=True)
        nodata = args.nodata if args.nodata is not None else profile.get("nodata")
        mask = create_cloud_shadow_mask(
            image,
            nodata_value=nodata,
            min_cloud_size=args.min_cloud_size,
            min_shadow_size=args.min_shadow_size,
            cloud_dilation=args.cloud_dilation,
        )

        mask_profile = profile.copy()
        mask_profile.update(count=1, dtype=rasterio.uint8, nodata=255)
        out_path = args.output_dir / f"{image_path.stem}_mask.tif"
        write_raster(out_path, mask, mask_profile, dtype="uint8")

        if args.preview_dir:
            save_mask_preview(args.preview_dir / f"{image_path.stem}_mask_preview.png", image, mask)

    logging.info("Saved %d masks to %s", len(rasters), args.output_dir)


if __name__ == "__main__":
    main()
