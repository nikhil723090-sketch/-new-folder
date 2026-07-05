"""Hotspot detection using DBSCAN, KMeans, and KDE."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class HotspotResult:
    """Hotspot detection output."""

    records: pd.DataFrame
    algorithm: str
    summary: pd.DataFrame


class HotspotDetector:
    """Detect geographic crime clusters from latitude/longitude data."""

    def __init__(self, records: pd.DataFrame) -> None:
        required = {"latitude", "longitude", "crime_type"}
        missing = required.difference(records.columns)
        if missing:
            raise ValueError(f"Missing hotspot columns: {sorted(missing)}")
        self.records = records.dropna(subset=["latitude", "longitude"]).copy()

    def dbscan(self, eps_km: float = 1.0, min_samples: int = 5) -> HotspotResult:
        """Cluster nearby crimes using DBSCAN."""

        from sklearn.cluster import DBSCAN

        clustered = self.records.copy()
        coords = np.radians(clustered[["latitude", "longitude"]].astype(float).to_numpy())
        earth_radius_km = 6371.0088
        model = DBSCAN(eps=eps_km / earth_radius_km, min_samples=min_samples, metric="haversine")
        clustered["hotspot_id"] = model.fit_predict(coords)
        return HotspotResult(clustered, "DBSCAN", _cluster_summary(clustered))

    def kmeans(self, clusters: int = 5) -> HotspotResult:
        """Cluster crimes into a fixed number of hotspot zones."""

        from sklearn.cluster import KMeans

        clustered = self.records.copy()
        coords = clustered[["latitude", "longitude"]].astype(float).to_numpy()
        model = KMeans(n_clusters=min(clusters, len(clustered)), random_state=42, n_init="auto")
        clustered["hotspot_id"] = model.fit_predict(coords)
        return HotspotResult(clustered, "KMeans", _cluster_summary(clustered))

    def kde(self, bandwidth: float = 0.02) -> HotspotResult:
        """Estimate hotspot intensity with Kernel Density Estimation."""

        from sklearn.neighbors import KernelDensity

        scored = self.records.copy()
        coords = scored[["latitude", "longitude"]].astype(float).to_numpy()
        model = KernelDensity(kernel="gaussian", bandwidth=bandwidth)
        model.fit(coords)
        scored["hotspot_score"] = np.exp(model.score_samples(coords))
        scored["hotspot_id"] = pd.qcut(scored["hotspot_score"], q=4, labels=False, duplicates="drop")
        return HotspotResult(scored, "KDE", _cluster_summary(scored))


def _cluster_summary(records: pd.DataFrame) -> pd.DataFrame:
    filtered = records[records["hotspot_id"] >= 0] if "hotspot_id" in records else records
    if filtered.empty:
        return pd.DataFrame(columns=["hotspot_id", "case_count", "center_latitude", "center_longitude"])
    return (
        filtered.groupby("hotspot_id")
        .agg(
            case_count=("crime_type", "count"),
            center_latitude=("latitude", "mean"),
            center_longitude=("longitude", "mean"),
            top_crime_type=("crime_type", lambda values: values.value_counts().index[0]),
        )
        .reset_index()
        .sort_values("case_count", ascending=False)
    )
