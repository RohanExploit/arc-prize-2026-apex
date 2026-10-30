"""Object-Centric DSL for ARC-AGI-3 grid analysis.

Implements 4-way connected component analysis, background color detection,
bounding box extraction, centroid calculation, and spatial object tracking.
"""
from __future__ import annotations
import numpy as np
from collections import deque
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Any


@dataclass
class GridObject:
    color: int
    coords: List[Tuple[int, int]]  # list of (r, c)
    min_r: int
    max_r: int
    min_c: int
    max_c: int
    size: int
    centroid: Tuple[int, int]  # (r, c)


def get_background_color(grid: np.ndarray) -> int:
    """Most frequent color in the grid, typically 0."""
    counts = np.bincount(grid.ravel(), minlength=16)
    return int(np.argmax(counts))


def find_objects(grid: np.ndarray, bg_color: Optional[int] = None) -> List[GridObject]:
    """4-way connectivity object extraction.
    
    Returns list of GridObject with color, coordinates, bounding box, size, centroid.
    """
    if bg_color is None:
        bg_color = get_background_color(grid)

    H, W = grid.shape
    visited = np.zeros((H, W), dtype=bool)
    objects: List[GridObject] = []

    for r in range(H):
        for c in range(W):
            color = int(grid[r, c])
            if color == bg_color or visited[r, c]:
                continue

            coords = []
            queue = deque([(r, c)])
            visited[r, c] = True
            min_r, max_r = r, r
            min_c, max_c = c, c

            while queue:
                cr, cc = queue.popleft()
                coords.append((cr, cc))
                if cr < min_r: min_r = cr
                if cr > max_r: max_r = cr
                if cc < min_c: min_c = cc
                if cc > max_c: max_c = cc

                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < H and 0 <= nc < W:
                        if not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            queue.append((nr, nc))

            size = len(coords)
            mean_r = int(sum(p[0] for p in coords) / size)
            mean_c = int(sum(p[1] for p in coords) / size)

            objects.append(GridObject(
                color=color,
                coords=coords,
                min_r=min_r,
                max_r=max_r,
                min_c=min_c,
                max_c=max_c,
                size=size,
                centroid=(mean_r, mean_c),
            ))

    return objects


def compute_frame_delta(grid_prev: np.ndarray, grid_cur: np.ndarray) -> np.ndarray:
    """Return binary mask of changed cells between two consecutive frames."""
    return grid_prev != grid_cur


def extract_moving_object(grid_prev: np.ndarray, grid_cur: np.ndarray) -> Optional[Tuple[int, int]]:
    """Identify centroid of the primary moving object (e.g. player avatar)."""
    diff = compute_frame_delta(grid_prev, grid_cur)
    if not np.any(diff):
        return None
    bg = get_background_color(grid_cur)
    changed_mask = diff & (grid_cur != bg)
    coords = np.argwhere(changed_mask)
    if len(coords) == 0:
        coords = np.argwhere(diff)
    if len(coords) == 0:
        return None
    mean_r = int(np.mean(coords[:, 0]))
    mean_c = int(np.mean(coords[:, 1]))
    return (mean_r, mean_c)


def get_candidate_clicks(grid: np.ndarray, max_candidates: int = 16) -> List[Tuple[int, int]]:
    """Generate intelligent coordinate candidates (x, y) for ACTION6.
    
    Prioritizes centroids of non-background objects, then small interactive components.
    Note: Returns (x, y) where x=col, y=row as required by GameAction.ACTION6.
    """
    objects = find_objects(grid)
    objects_sorted = sorted(objects, key=lambda o: o.size)
    clicks = []
    for o in objects_sorted[:max_candidates]:
        r, c = o.centroid
        clicks.append((c, r))  # x=col, y=row
    return clicks
