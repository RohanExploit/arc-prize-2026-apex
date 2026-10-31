import os
os.chdir(r"E:\projects\arc-agi-3")
import arc_agi
import numpy as np
from collections import deque
from arcengine import GameAction

class ActiveClickSpecialist:
    def __init__(self):
        self.dead_signatures = set()
        self.state_history = []
        
    def _get_background_color(self, grid: np.ndarray) -> int:
        """Determines the background color via edge-weighted frequency analysis."""
        counts = np.bincount(grid.flatten(), minlength=16)
        borders = np.concatenate([grid[0, :], grid[-1, :], grid[:, 0], grid[:, -1]])
        border_counts = np.bincount(borders, minlength=16)
        return int(np.argmax(counts + border_counts * 5))

    def extract_candidate_targets(self, grid: np.ndarray, last_clicked_coord=None) -> list[tuple[int, int]]:
        """Segments foreground objects and returns ranked centroids."""
        bg_color = self._get_background_color(grid)
        visited = np.zeros_like(grid, dtype=bool)
        visited[grid == bg_color] = True
        
        objects = []
        rows, cols = grid.shape
        
        for r in range(rows):
            for c in range(cols):
                if not visited[r, c]:
                    obj_coords = []
                    q = deque([(r, c)])
                    visited[r, c] = True
                    
                    while q:
                        cr, cc = q.popleft()
                        obj_coords.append((cr, cc))
                        
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nr, nc = cr + dr, cc + dc
                            if 0 <= nr < rows and 0 <= nc < cols:
                                if not visited[nr, nc] and grid[nr, nc] != bg_color:
                                    visited[nr, nc] = True
                                    q.append((nr, nc))
                                    
                    objects.append(obj_coords)
                    
        candidates = []
        for obj in objects:
            coords = np.array(obj)
            cy, cx = int(np.median(coords[:, 0])), int(np.median(coords[:, 1]))
            
            if grid[cy, cx] == bg_color:
                dists = (coords[:, 0] - cy)**2 + (coords[:, 1] - cx)**2
                closest_idx = np.argmin(dists)
                cy, cx = coords[closest_idx]
                
            if (cx, cy) not in self.dead_signatures:
                size = len(obj)
                priority = size 
                candidates.append((priority, (cx, cy)))
                
        candidates.sort(key=lambda x: x[0])
        return [coord for _, coord in candidates]

    def update_causal_feedback(self, obs_before: np.ndarray, obs_after: np.ndarray, clicked_coord: tuple[int, int]):
        delta = np.abs(obs_after - obs_before)
        diff_sum = np.sum(delta)
        cx, cy = clicked_coord
        
        if diff_sum == 0:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    self.dead_signatures.add((cx + dx, cy + dy))
        else:
            self.state_history.append({
                'coord': clicked_coord,
                'pixels_changed': int(np.count_nonzero(delta)),
                'magnitude': int(diff_sum)
            })

arcade = arc_agi.Arcade(operation_mode=arc_agi.OperationMode.OFFLINE, environments_dir=r"E:\projects\arc-agi-3\environment_files")
env = arcade.make('vc33')
obs = env.reset()

agent = ActiveClickSpecialist()

print('Initial level:', obs.levels_completed)
print('Available actions:', obs.available_actions)

for step in range(40):
    grid = np.array(obs.frame)
    if grid.ndim == 3:
        grid = grid[0]
    
    candidates = agent.extract_candidate_targets(grid)
    if not candidates:
        print(f'Step {step}: No candidates remaining! Dead signatures count: {len(agent.dead_signatures)}')
        break
        
    target_coord = candidates[0]
    cx, cy = target_coord
    
    obs_before = grid.copy()
    obs = env.step(GameAction.ACTION6, data={'x': cx, 'y': cy})
    
    grid_after = np.array(obs.frame)
    if grid_after.ndim == 3:
        grid_after = grid_after[0]
        
    agent.update_causal_feedback(obs_before, grid_after, target_coord)
    
    delta = np.abs(grid_after - obs_before)
    changed = int(np.count_nonzero(delta))
    print(f'Step {step+1}: Clicked ({cx}, {cy}) -> {changed} px changed. Dead zones: {len(agent.dead_signatures)}. Levels completed: {obs.levels_completed}')
    
    if obs.levels_completed > 0:
        print(f'LEVEL COMPLETED AT STEP {step+1}!')
        break
