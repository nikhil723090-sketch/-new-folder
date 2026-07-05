"""Command-line pattern detection demo."""

from __future__ import annotations

import argparse

from .report import generate_pattern_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate crime pattern detection report.")
    parser.add_argument("csv_path", help="Crime records CSV path")
    parser.add_argument("--output-dir", default="pattern_report", help="Output report folder")
    args = parser.parse_args()

    files = generate_pattern_report(args.csv_path, args.output_dir)
    for name, path in files.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
