from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import rasterio
from rasterio.windows import Window
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from preprocessing.io import list_rasters, match_by_stem


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract aligned cloudy/target/mask patches.")
    parser.add_argument("--cloudy-dir", required=True, type=Path)
    parser.add_argument("--target-dir", required=True, type=Path)
    parser.add_argument("--mask-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--patch-size", type=int, default=256)
    parser.add_argument("--stride", type=int, default=128)
    parser.add_argument("--max-cloud-fraction", type=float, default=0.95)
    parser.add_argument("--min-cloud-fraction", type=float, default=0.02)
    parser.add_argument("--keep-clear-patches", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    cloudy_files = list_rasters(args.cloudy_dir)
    target_pairs = match_by_stem(cloudy_files, args.target_dir)
    mask_pairs = match_by_stem(cloudy_files, args.mask_dir)
    manifest = []
    patch_id = 0

    for cloudy_path in tqdm(cloudy_files, desc="Extracting patches"):
        if cloudy_path not in target_pairs or cloudy_path not in mask_pairs:
            continue
        target_path = target_pairs[cloudy_path]
        mask_path = mask_pairs[cloudy_path]

        with rasterio.open(cloudy_path) as cloudy, rasterio.open(target_path) as target, rasterio.open(mask_path) as mask_src:
            assert_same_grid(cloudy, target, target_path)
            assert_same_grid(cloudy, mask_src, mask_path)

            for row in range(0, cloudy.height - args.patch_size + 1, args.stride):
                for col in range(0, cloudy.width - args.patch_size + 1, args.stride):
                    window = Window(col, row, args.patch_size, args.patch_size)
                    mask = mask_src.read(1, window=window)
                    valid = mask != 255
                    if valid.mean() < 0.90:
                        continue
                    cloud_fraction = np.isin(mask, [1, 2]).mean()
                    if not args.keep_clear_patches and cloud_fraction < args.min_cloud_fraction:
                        continue
                    if cloud_fraction > args.max_cloud_fraction:
                        continue

                    cloudy_patch = cloudy.read(window=window)
                    target_patch = target.read(window=window)
                    transform = cloudy.window_transform(window)
                    out_name = f"patch_{patch_id:06d}.npz"
                    out_path = args.output_dir / out_name
                    np.savez_compressed(
                        out_path,
                        cloudy=cloudy_patch.astype(np.float32),
                        target=target_patch.astype(np.float32),
                        mask=mask.astype(np.uint8),
                        transform=np.array(transform.to_gdal(), dtype=np.float64),
                        crs=str(cloudy.crs),
                        source=cloudy_path.name,
                    )
                    manifest.append(
                        {
                            "file": out_name,
                            "source": cloudy_path.name,
                            "target": target_path.name,
                            "mask": mask_path.name,
                            "row": row,
                            "col": col,
                            "cloud_fraction": float(cloud_fraction),
                        }
                    )
                    patch_id += 1

    with (args.output_dir / "manifest.json").open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Saved {patch_id} patches to {args.output_dir}")


def assert_same_grid(a: rasterio.DatasetReader, b: rasterio.DatasetReader, b_path: Path) -> None:
    if a.crs != b.crs or a.transform != b.transform or a.width != b.width or a.height != b.height:
        raise ValueError(f"{b_path} is not aligned. Run scripts/register_images.py first.")


if __name__ == "__main__":
    main()
