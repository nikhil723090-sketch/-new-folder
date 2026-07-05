from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from tqdm import tqdm


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize extracted LISS-IV training patches.")
    parser.add_argument("--patch-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--stats-json", required=True, type=Path)
    parser.add_argument("--method", choices=["zscore", "minmax"], default="zscore")
    parser.add_argument("--reuse-stats", action="store_true", help="Use existing stats-json instead of recomputing.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    patches = sorted(args.patch_dir.glob("*.npz"))
    if not patches:
        raise SystemExit(f"No .npz patches found in {args.patch_dir}")

    if args.reuse_stats:
        stats = json.loads(args.stats_json.read_text(encoding="utf-8"))
    else:
        stats = compute_stats(patches, args.method)
        args.stats_json.parent.mkdir(parents=True, exist_ok=True)
        args.stats_json.write_text(json.dumps(stats, indent=2), encoding="utf-8")

    for patch_path in tqdm(patches, desc="Normalizing patches"):
        with np.load(patch_path, allow_pickle=False) as patch:
            cloudy = normalize_array(patch["cloudy"], stats["cloudy"], args.method)
            target = normalize_array(patch["target"], stats["target"], args.method)
            payload = {key: patch[key] for key in patch.files if key not in {"cloudy", "target"}}
            payload["cloudy"] = cloudy.astype(np.float32)
            payload["target"] = target.astype(np.float32)
            np.savez_compressed(args.output_dir / patch_path.name, **payload)

    print(f"Saved normalized patches to {args.output_dir}")
    print(f"Statistics: {args.stats_json}")


def compute_stats(paths: list[Path], method: str) -> dict:
    arrays = {"cloudy": [], "target": []}
    for path in tqdm(paths, desc="Computing normalization statistics"):
        with np.load(path, allow_pickle=False) as patch:
            arrays["cloudy"].append(patch["cloudy"])
            arrays["target"].append(patch["target"])

    stats = {"method": method}
    for name, chunks in arrays.items():
        data = np.concatenate([x.reshape(x.shape[0], -1) for x in chunks], axis=1)
        if method == "zscore":
            stats[name] = {
                "mean": data.mean(axis=1).tolist(),
                "std": np.maximum(data.std(axis=1), 1e-6).tolist(),
            }
        else:
            stats[name] = {
                "min": np.percentile(data, 2, axis=1).tolist(),
                "max": np.percentile(data, 98, axis=1).tolist(),
            }
    return stats


def normalize_array(array: np.ndarray, stats: dict, method: str) -> np.ndarray:
    if method == "zscore":
        mean = np.array(stats["mean"], dtype=np.float32)[:, None, None]
        std = np.array(stats["std"], dtype=np.float32)[:, None, None]
        return (array - mean) / std

    lo = np.array(stats["min"], dtype=np.float32)[:, None, None]
    hi = np.array(stats["max"], dtype=np.float32)[:, None, None]
    return np.clip((array - lo) / (hi - lo + 1e-6), 0, 1)


if __name__ == "__main__":
    main()
