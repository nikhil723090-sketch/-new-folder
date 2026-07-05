"""Folium/Leaflet map outputs for hotspot detection."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def save_heatmap(records: pd.DataFrame, output_path: str | Path) -> Path:
    """Save a Folium heatmap for crime locations."""

    import folium
    from folium.plugins import HeatMap

    output = Path(output_path)
    center = [records["latitude"].astype(float).mean(), records["longitude"].astype(float).mean()]
    fmap = folium.Map(location=center, zoom_start=7, tiles="OpenStreetMap")
    heat_data = records[["latitude", "longitude"]].astype(float).values.tolist()
    HeatMap(heat_data, radius=16, blur=22).add_to(fmap)
    fmap.save(output)
    return output


def save_cluster_map(records: pd.DataFrame, output_path: str | Path) -> Path:
    """Save a Folium map with hotspot cluster markers."""

    import folium

    output = Path(output_path)
    center = [records["latitude"].astype(float).mean(), records["longitude"].astype(float).mean()]
    fmap = folium.Map(location=center, zoom_start=7, tiles="OpenStreetMap")
    for _, row in records.iterrows():
        folium.CircleMarker(
            location=[float(row["latitude"]), float(row["longitude"])],
            radius=5,
            popup=f"{row.get('crime_type', 'Crime')} | Hotspot {row.get('hotspot_id', '-')}",
            color="#b11226",
            fill=True,
        ).add_to(fmap)
    fmap.save(output)
    return output
