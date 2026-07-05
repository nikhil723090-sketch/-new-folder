"""Generate crime pattern reports."""

from __future__ import annotations

from pathlib import Path

from .data_loader import load_from_csv
from .pattern_detector import CrimePatternDetector
from .visualization import save_district_plotly, save_hotspot_map, save_peak_hours_chart


def generate_pattern_report(csv_path: str | Path, output_dir: str | Path) -> dict[str, str]:
    """Create CSV summaries and charts from a crime records CSV."""

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    records = load_from_csv(csv_path)
    detector = CrimePatternDetector(records)
    summary = detector.summary()

    files = {
        "peak_crime_hours_csv": output / "peak_crime_hours.csv",
        "crime_by_season_csv": output / "crime_by_season.csv",
        "crime_by_district_csv": output / "crime_by_district.csv",
        "repeat_offenders_csv": output / "repeat_offenders.csv",
        "repeat_locations_csv": output / "repeat_locations.csv",
        "peak_hours_chart": output / "peak_crime_hours.png",
        "district_chart": output / "crime_by_district.html",
        "hotspot_map": output / "crime_hotspot_map.html",
    }

    summary.peak_crime_hours.to_csv(files["peak_crime_hours_csv"], index=False)
    summary.crime_by_season.to_csv(files["crime_by_season_csv"], index=False)
    summary.crime_by_district.to_csv(files["crime_by_district_csv"], index=False)
    summary.repeat_offenders.to_csv(files["repeat_offenders_csv"], index=False)
    summary.repeat_locations.to_csv(files["repeat_locations_csv"], index=False)

    save_peak_hours_chart(summary.peak_crime_hours, files["peak_hours_chart"])
    save_district_plotly(summary.crime_by_district, files["district_chart"])
    save_hotspot_map(records, files["hotspot_map"])

    return {name: str(path) for name, path in files.items()}
