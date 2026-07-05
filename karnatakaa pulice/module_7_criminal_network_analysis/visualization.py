"""Export graph data for frontend node-edge visualization."""

from __future__ import annotations

import json
from pathlib import Path


def save_graph_json(nodes: list[dict], edges: list[dict], output_path: str | Path) -> Path:
    """Save graph nodes and edges for React, Cytoscape, D3, or vis-network."""

    output = Path(output_path)
    output.write_text(json.dumps({"nodes": nodes, "edges": edges}, indent=2), encoding="utf-8")
    return output
