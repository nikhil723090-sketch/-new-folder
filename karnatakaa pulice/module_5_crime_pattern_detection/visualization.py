"""Matplotlib and Plotly visualizations for crime patterns."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def save_peak_hours_chart(peak_hours: pd.DataFrame, output_path: str | Path) -> Path:
    """Save a Matplotlib bar chart for peak crime hours."""

    import matplotlib.pyplot as plt

    output = Path(output_path)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(peak_hours["crime_hour"].astype(str), peak_hours["case_count"], color="#2f6fbb")
    ax.set_title("Peak Crime Hours")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Case Count")
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)
    return output


def save_district_plotly(crime_by_district: pd.DataFrame, output_path: str | Path) -> Path:
    """Save an interactive Plotly chart for district crime patterns."""

    import plotly.express as px

    output = Path(output_path)
    fig = px.bar(
        crime_by_district,
        x="district",
        y="case_count",
        color="crime_type",
        title="Crime by District",
        labels={"district": "District", "case_count": "Case Count", "crime_type": "Crime Type"},
    )
    fig.write_html(output)
    return output


def save_hotspot_map(records: pd.DataFrame, output_path: str | Path) -> Path:
    """Save an interactive Plotly map using latitude and longitude."""

    import plotly.express as px

    output = Path(output_path)
    fig = px.scatter_mapbox(
        records,
        lat="latitude",
        lon="longitude",
        color="crime_type",
        hover_name="crime_id",
        hover_data=["district", "police_station", "status"],
        zoom=5,
        height=650,
        title="Crime Location Hotspots",
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.write_html(output)
    return output
