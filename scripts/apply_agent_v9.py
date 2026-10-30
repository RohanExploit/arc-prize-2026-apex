import re
from pathlib import Path

agent_file = Path("agent/my_agent.py")
content = agent_file.read_text(encoding="utf-8")

# 1. Update ClickSpecialist.get_next_click
old_click_spec = """        if not self.click_queue:
            bg = _get_bg_color(grid)
            H, W = grid.shape
            visited = np.zeros((H, W), dtype=bool)
            candidates = []

            for r in range(H):
                for c in range(W):
                    val = int(grid[r, c])
                    if val == bg or visited[r, c]:
                        continue
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
                    candidates.append((size, (mean_c, mean_r)))

            candidates.sort(key=lambda x: x[0])
            for _, pt in candidates:
                if pt not in self.tried_clicks:
                    self.click_queue.append(pt)

            if not self.click_queue:
                for y in range(4, 60, 8):
                    for x in range(4, 60, 8):
                        if (x, y) not in self.tried_clicks:
                            self.click_queue.append((x, y))"""

new_click_spec = """        if not self.click_queue:
            bg = _get_bg_color(grid)
            H, W = grid.shape
            visited = np.zeros((H, W), dtype=bool)
            solid_pieces = []
            cavities = []
            hollow_borders = []

            for r in range(H):
                for c in range(W):
                    val = int(grid[r, c])
                    if val == bg or visited[r, c]:
                        continue
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
                    min_r = min(p[0] for p in coords)
                    max_r = max(p[0] for p in coords)
                    min_c = min(p[1] for p in coords)
                    max_c = max(p[1] for p in coords)
                    bbox_h = max_r - min_r + 1
                    bbox_w = max_c - min_c + 1
                    bbox_area = bbox_h * bbox_w
                    solidity = size / bbox_area if bbox_area > 0 else 1.0

                    mean_r = int(sum(p[0] for p in coords) / size)
                    mean_c = int(sum(p[1] for p in coords) / size)
                    box_r = (min_r + max_r) // 2
                    box_c = (min_c + max_c) // 2

                    if solidity >= 0.7:
                        solid_pieces.append((size, (mean_c, mean_r)))
                    else:
                        if bbox_h >= 4 and bbox_w >= 4:
                            cavities.append((bbox_area, (box_c, box_r)))
                        hollow_borders.append((size, (mean_c, mean_r)))

            solid_pieces.sort(key=lambda x: x[0])
            cavities.sort(key=lambda x: x[0])
            hollow_borders.sort(key=lambda x: x[0])

            for _, pt in solid_pieces + cavities + hollow_borders:
                if pt not in self.tried_clicks:
                    self.click_queue.append(pt)

            if not self.click_queue:
                for y in range(4, 60, 8):
                    for x in range(4, 60, 8):
                        if (x, y) not in self.tried_clicks:
                            self.click_queue.append((x, y))"""

# Normalize CRLF
content_norm = content.replace("\r\n", "\n")
old_click_spec_norm = old_click_spec.replace("\r\n", "\n")
new_click_spec_norm = new_click_spec.replace("\r\n", "\n")

assert old_click_spec_norm in content_norm, "old_click_spec not found in content"
content_norm = content_norm.replace(old_click_spec_norm, new_click_spec_norm)

# 2. Update _get_candidate_actions
old_cand = """        if complex_avail and grid is not None:
            base = complex_avail[0]
            bg = _get_bg_color(grid)
            H, W = grid.shape
            visited = np.zeros((H, W), dtype=bool)
            candidates = []

            for r in range(H):
                for c in range(W):
                    val = int(grid[r, c])
                    if val == bg or visited[r, c]:
                        continue
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
                    candidates.append((size, mean_c, mean_r))

            candidates.sort(key=lambda x: x[0])
            for _, mc, mr in candidates:
                keys.append(f"{base.name}:{mc},{mr}")

            # Fallback grid clicks if few objects detected
            if len(keys) < 8:
                for y in range(8, 56, 12):
                    for x in range(8, 56, 12):
                        k = f"{base.name}:{x},{y}"
                        if k not in keys:
                            keys.append(k)"""

new_cand = """        if complex_avail and grid is not None:
            base = complex_avail[0]
            bg = _get_bg_color(grid)
            H, W = grid.shape
            visited = np.zeros((H, W), dtype=bool)
            solid_pieces = []
            cavities = []
            hollow_borders = []

            for r in range(H):
                for c in range(W):
                    val = int(grid[r, c])
                    if val == bg or visited[r, c]:
                        continue
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
                    min_r = min(p[0] for p in coords)
                    max_r = max(p[0] for p in coords)
                    min_c = min(p[1] for p in coords)
                    max_c = max(p[1] for p in coords)
                    bbox_h = max_r - min_r + 1
                    bbox_w = max_c - min_c + 1
                    bbox_area = bbox_h * bbox_w
                    solidity = size / bbox_area if bbox_area > 0 else 1.0

                    mean_r = int(sum(p[0] for p in coords) / size)
                    mean_c = int(sum(p[1] for p in coords) / size)
                    box_r = (min_r + max_r) // 2
                    box_c = (min_c + max_c) // 2

                    if solidity >= 0.7:
                        solid_pieces.append((size, mean_c, mean_r))
                    else:
                        if bbox_h >= 4 and bbox_w >= 4:
                            cavities.append((bbox_area, box_c, box_r))
                        hollow_borders.append((size, mean_c, mean_r))

            solid_pieces.sort(key=lambda x: x[0])
            cavities.sort(key=lambda x: x[0])
            hollow_borders.sort(key=lambda x: x[0])

            # Prioritize solid manipulable tokens, then receptacle cavities, then borders
            for _, mc, mr in solid_pieces:
                k = f"{base.name}:{mc},{mr}"
                if k not in keys:
                    keys.append(k)

            for _, bc, br in cavities:
                k = f"{base.name}:{bc},{br}"
                if k not in keys:
                    keys.append(k)

            for _, mc, mr in hollow_borders:
                k = f"{base.name}:{mc},{mr}"
                if k not in keys:
                    keys.append(k)

            # Fallback grid clicks if few objects detected
            if len(keys) < 8:
                for y in range(8, 56, 12):
                    for x in range(8, 56, 12):
                        k = f"{base.name}:{x},{y}"
                        if k not in keys:
                            keys.append(k)"""

old_cand_norm = old_cand.replace("\r\n", "\n")
new_cand_norm = new_cand.replace("\r\n", "\n")

assert old_cand_norm in content_norm, "old_cand not found in content"
content_norm = content_norm.replace(old_cand_norm, new_cand_norm)

# Update docstring to v9
content_norm = content_norm.replace(
    '"""ARC-AGI-3 Agent — Multi-Specialist Object BFS Explorer (Self-Contained).',
    '"""ARC-AGI-3 Agent v9 — Cavity-Aware Receptacle & Dynamic Multi-Specialist BFS Explorer.'
)

agent_file.write_text(content_norm, encoding="utf-8")
print("Successfully upgraded agent/my_agent.py to v9 (Cavity-Aware Receptacle BFS Explorer)!")
