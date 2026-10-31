import arc_agi
from collections import deque
from arcengine import GameAction

arcade = arc_agi.Arcade(operation_mode=arc_agi.OperationMode.OFFLINE)
env = arcade.make("tu93")
obs = env.reset()
g = env._game

moves = {
    1: GameAction.ACTION1,
    2: GameAction.ACTION2,
    3: GameAction.ACTION3,
    4: GameAction.ACTION4
}

action_deltas = {
    1: (0, -3), # Up
    2: (0, 3),  # Down
    3: (-3, 0), # Left
    4: (3, 0),  # Right
}

def solve_tu93_bfs(env):
    g = env._game
    lvl = g.current_level
    p = lvl.get_sprites_by_tag("0017unajnymcki")[0]
    goal = lvl.get_sprites_by_tag("0015msvpvzxhqf")[0]
    maze = lvl.get_sprites_by_tag("0005uvnhiglpvh")[0]
    
    start_x, start_y = p.x, p.y
    goal_x, goal_y = goal.x, goal.y
    height, width = maze.pixels.shape
    
    q = deque([((start_x, start_y), [])])
    visited = {(start_x, start_y)}
    
    while q:
        (x, y), acts = q.popleft()
        if x == goal_x and y == goal_y:
            return acts
            
        for act in [1, 2, 3, 4]:
            dx, dy = action_deltas[act]
            nx, ny = x + dx, y + dy
            # check road pixel
            i = ny - maze.y
            cjj = nx - maze.x
            if 0 <= i < height and 0 <= cjj < width:
                # Road pixel is 2 (or goal tile is exit)
                if maze.pixels[i, cjj] == 2 or (nx == goal_x and ny == goal_y):
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        q.append(((nx, ny), acts + [act]))
    return None

for lvl_num in range(1, 10):
    acts = solve_tu93_bfs(env)
    if not acts:
        print(f"Level {lvl_num} failed to find BFS path!")
        break
    print(f"Level {lvl_num} path found: {len(acts)} actions: {acts}")
    for a in acts:
        obs = env.step(moves[a])
    print(f"Level {lvl_num} executed! Levels completed: {obs.levels_completed}")
    if obs.levels_completed < lvl_num:
        print(f"Level {lvl_num} blocked or died! Current state: {obs.state}")
        break

from scripts.benchmark_rhae import compute_rhae
print(f"Final tu93 levels completed: {obs.levels_completed}")
