from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from rasterio.enums import Resampling
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from preprocessing.io import list_rasters, match_by_stem
from preprocessing.register import align_to_reference


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Register/reproject LISS-IV images to a reference grid.")
    parser.add_argument("--reference", required=True, type=Path, help="Reference cloud-free scene/grid.")
    parser.add_argument("--input-dir", required=True, type=Path, help="Cloudy image file or folder.")
    parser.add_argument("--output-dir", required=True, type=Path, help="Output folder.")
    parser.add_argument("--mask-dir", type=Path, help="Optional mask folder to register with nearest-neighbor.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    image_out = args.output_dir / "images"
    mask_out = args.output_dir / "masks"
    images = list_rasters(args.input_dir)
    if not images:
        raise SystemExit(f"No rasters found in {args.input_dir}")

    for image_path in tqdm(images, desc="Registering images"):
        align_to_reference(
            image_path,
            args.reference,
            image_out / f"{image_path.stem}_registered.tif",
            resampling=Resampling.bilinear,
        )

    if args.mask_dir:
        pairs = match_by_stem(images, args.mask_dir)
        for image_path, mask_path in tqdm(pairs.items(), desc="Registering masks"):
            align_to_reference(
                mask_path,
                args.reference,
                mask_out / f"{image_path.stem}_mask_registered.tif",
                resampling=Resampling.nearest,
                dst_dtype="uint8",
            )
        logging.info("Matched and registered %d masks.", len(pairs))

    logging.info("Registered %d images to %s", len(images), args.reference)


if __name__ == "__main__":
    main()
