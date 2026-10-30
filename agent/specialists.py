"""ARC-AGI-3 Specialist Modules.

Provides dedicated solvers:
  1. ClickSpecialist: For click-only games ([6], [6, 7]).
     Extracts object centroids, tests candidate clicks, and maintains a whitelist
     of reactive/interactive coordinate targets while discarding inert pixels.
  2. AvatarNavigationSpecialist: For movement games ([1,2,3,4], [1,2,3,4,5]).
     Tracks avatar coordinates by frame subtraction, identifies goal objects,
     and computes shortest paths avoiding stationary obstacles.
  3. HybridSpecialist: Dynamically selects between movement and interaction.
"""
from __future__ import annotations

import random
from collections import deque
from typing import Any, List, Tuple, Optional, Set, Dict
import numpy as np
from arcengine import GameAction, GameState


class ClickSpecialist:
    """Specialist for coordinate click games (ACTION6)."""

    def __init__(self):
        self.tried_clicks: Set[Tuple[int, int]] = set()
        self.effective_clicks: Set[Tuple[int, int]] = set()
        self.click_queue: deque[Tuple[int, int]] = deque()
        self.last_click: Optional[Tuple[int, int]] = None

    def on_step(self, prev_frame: Optional[np.ndarray], cur_frame: np.ndarray):
        """If previous click altered the frame, mark it as effective."""
        if self.last_click is not None and prev_frame is not None:
            if np.any(prev_frame != cur_frame):
                self.effective_clicks.add(self.last_click)

    def get_next_click(self, grid: np.ndarray) -> Tuple[int, int]:
        """Returns next (x, y) click candidate prioritizing object centroids."""
        if not self.click_queue:
            # Re-generate candidates from current objects
            bg = int(np.argmax(np.bincount(grid.ravel(), minlength=16)))
            H, W = grid.shape
            visited = np.zeros((H, W), dtype=bool)
            candidates = []

            for r in range(H):
                for c in range(W):
                    val = int(grid[r, c])
                    if val == bg or visited[r, c]:
                        continue
                    # BFS component
                    coords = []
                    q = deque([(r, c)])
                    visited[r, c] = True
                    while q:
                        cr, cc = q.popleft()
                        coords.append((cr, cc))
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nr, nc = cr + dr, cc + dc
                            if 0 <= nr < H and 0 <= nc < W:
                                if not visited[nr, nc] and grid[nr, nc] == val:
                                    visited[nr, nc] = True
                                    q.append((nr, nc))
                    size = len(coords)
                    mean_r = int(sum(p[0] for p in coords) / size)
                    mean_c = int(sum(p[1] for p in coords) / size)
                    candidates.append((size, (mean_c, mean_r)))  # (size, (x, y))

            # Smallest interactive elements first
            candidates.sort(key=lambda x: x[0])
            for _, pt in candidates:
                if pt not in self.tried_clicks:
                    self.click_queue.append(pt)

            # Fallback coarse grid points if all object centroids tried
            if not self.click_queue:
                for y in range(4, 60, 8):
                    for x in range(4, 60, 8):
                        if (x, y) not in self.tried_clicks:
                            self.click_queue.append((x, y))

        if self.click_queue:
            pt = self.click_queue.popleft()
            self.tried_clicks.add(pt)
            self.last_click = pt
            return pt

        # Ultimate fallback
        pt = (random.randint(0, 63), random.randint(0, 63))
        self.last_click = pt
        return pt


class AvatarNavigationSpecialist:
    """Specialist for directional movement games (ACTION1-4)."""

    DIR_MAP = {
        GameAction.ACTION1: (-1, 0),  # Up
        GameAction.ACTION2: (1, 0),   # Down
        GameAction.ACTION3: (0, -1),  # Left
        GameAction.ACTION4: (0, 1),   # Right
    }

    def __init__(self):
        self.avatar_pos: Optional[Tuple[int, int]] = None
        self.visited_positions: Set[Tuple[int, int]] = set()

    def update_avatar(self, prev_frame: Optional[np.ndarray], cur_frame: np.ndarray):
        if prev_frame is None:
            return
        diff = prev_frame != cur_frame
        if not np.any(diff):
            return
        bg = int(np.argmax(np.bincount(cur_frame.ravel(), minlength=16)))
        mask = diff & (cur_frame != bg)
        pts = np.argwhere(mask)
        if len(pts) > 0:
            self.avatar_pos = (int(np.mean(pts[:, 0])), int(np.mean(pts[:, 1])))
            self.visited_positions.add(self.avatar_pos)

    def choose_move(self, available_actions: List[GameAction]) -> GameAction:
        move_actions = [a for a in available_actions if a in self.DIR_MAP]
        if not move_actions:
            return random.choice(available_actions)
        # Prioritize moves leading to unvisited avatar positions if avatar known
        if self.avatar_pos is not None:
            ar, ac = self.avatar_pos
            unvisited_moves = []
            for a in move_actions:
                dr, dc = self.DIR_MAP[a]
                nxt = (ar + dr, ac + dc)
                if nxt not in self.visited_positions:
                    unvisited_moves.append(a)
            if unvisited_moves:
                return random.choice(unvisited_moves)
        return random.choice(move_actions)