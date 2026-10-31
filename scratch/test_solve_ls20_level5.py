import os
os.chdir(r"E:\projects\arc-agi-3")
import arc_agi
from collections import deque
from arcengine import GameAction

arcade = arc_agi.Arcade(operation_mode=arc_agi.OperationMode.OFFLINE, environments_dir=r"E:\projects\arc-agi-3\environment_files")
env = arcade.make('ls20')
obs = env.reset()
g = env._game

moves = {1: GameAction.ACTION1, 2: GameAction.ACTION2, 3: GameAction.ACTION3, 4: GameAction.ACTION4}
action_deltas = {1: (0, -5), 2: (0, 5), 3: (-5, 0), 4: (5, 0)}

# Run L1 - L4
for a in [3, 3, 3, 1, 1, 1, 1, 4, 4, 4, 1, 1, 1]: env.step(moves[a])
for a in [1, 4, 1, 1, 1, 1, 1, 4, 4, 2, 4, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 1, 4, 1, 2, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 2, 3, 2, 2, 2, 2, 2]: env.step(moves[a])
for a in [1, 1, 1, 1, 1, 1, 1, 1, 3, 2, 2, 4, 2, 2, 2, 3, 2, 2, 2, 1, 1, 1, 3, 3, 1, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 3, 1, 2, 1, 4, 2]: env.step(moves[a])
for a in [3, 3, 3, 2, 2, 2, 3, 2, 2, 3, 3, 1, 2, 1, 2, 1, 2, 1, 1, 3, 3, 1, 2, 3, 3, 1, 1, 1, 2, 2, 4, 1, 1, 1, 1, 4, 1, 4, 1, 1, 3, 3, 3]: env.step(moves[a])

print('=== READY FOR LEVEL 5 ===')
print('Current level index:', g._current_level_index)

lvl = g.current_level
start_x, start_y = g.gudziatsk.x, g.gudziatsk.y
fuel_max = 42
start_fuel = g._step_counter_ui.osgviligwp or 42
step_dec = g._step_counter_ui.efipnixsvl or 2

target_shapes = g.ldxlnycps
target_cols = g.yjdexjsoa
target_rots = g.ehwheiwsk

wall_sprites = lvl.get_sprites_by_tag('ihdgageizm')
battery_sprites = lvl.get_sprites_by_tag('npxgalaybz')
goal_sprites = lvl.get_sprites_by_tag('rjlbuycveu')
shape_switches = lvl.get_sprites_by_tag('ttfwljgohq')
col_switches = lvl.get_sprites_by_tag('soyhouuebz')
pistons = list(g.hasivfwip)

def is_wall(px, py):
    if not (0 <= px < 64 and 0 <= py < 64): return True
    for w in wall_sprites:
        if px <= w.x < px + 5 and py <= w.y < py + 5: return True
    return False

def aabb_overlap(x1, y1, w1, h1, x2, y2, w2, h2):
    return x1 < x2 + w2 and x2 < x1 + w1 and y1 < y2 + h2 and y2 < y1 + h1

def get_patrol_pos(t):
    cycle = [14, 19, 24, 19]
    return (cycle[t % 4], 35)

initial_batts = tuple(range(len(battery_sprites)))
initial_goals = tuple(range(len(goal_sprites)))

# State: (x, y, s, c, r, fuel, batts, rem_goals, step_count)
start_state = (start_x, start_y, g.fwckfzsyc, g.hiaauhahz, g.cklxociuu, start_fuel, initial_batts, initial_goals, 0)
q = deque([(start_state, [])])
best_fuel = {(start_x, start_y, g.fwckfzsyc, g.hiaauhahz, g.cklxociuu, initial_batts, initial_goals, 0): start_fuel}

found = None
visited_count = 0
while q:
    (x, y, s, c, r, fuel, batts, rem_goals, t), acts = q.popleft()
    visited_count += 1
    
    if len(rem_goals) == 0:
        found = acts
        break
        
    if fuel < step_dec:
        continue
        
    nt = t + 1
    sw_x, sw_y = get_patrol_pos(nt)
    
    for act in [1, 2, 3, 4]:
        dx, dy = action_deltas[act]
        nx, ny = x + dx, y + dy
        if is_wall(nx, ny):
            continue
            
        blocked_goal = False
        matched_goal = None
        for g_idx in rem_goals:
            gs = goal_sprites[g_idx]
            if nx <= gs.x < nx + 5 and ny <= gs.y < ny + 5:
                if s == target_shapes[g_idx] and c == target_cols[g_idx] and r == target_rots[g_idx]:
                    matched_goal = g_idx
                else:
                    blocked_goal = True
                break
        if blocked_goal:
            continue
            
        for p in pistons:
            if aabb_overlap(nx, ny, 5, 5, p.sprite.x, p.sprite.y, p.sprite.width, p.sprite.height):
                p_steps = p.ullzqnksoj(g.gudziatsk)
                nx = nx + p.dx * 5 * p_steps
                ny = ny + p.dy * 5 * p_steps
                break
                
        ns, nc, nr = s, c, r
        for sw in shape_switches:
            if nx <= sw.x < nx + 5 and ny <= sw.y < ny + 5: ns = (ns + 1) % len(g.ijessuuig)
        for sw in col_switches:
            if nx <= sw.x < nx + 5 and ny <= sw.y < ny + 5: nc = (nc + 1) % len(g.tnkekoeuk)
            
        # Check moving rotation switch at time nt!
        if nx <= sw_x < nx + 5 and ny <= sw_y < ny + 5:
            nr = (nr + 1) % 4
            
        nfuel = fuel - step_dec
        nbatts = list(batts)
        for b_idx in batts:
            bs = battery_sprites[b_idx]
            if nx <= bs.x < nx + 5 and ny <= bs.y < ny + 5:
                nfuel = fuel_max
                nbatts.remove(b_idx)
                break
        nbatts = tuple(nbatts)
        
        n_goals = rem_goals
        if matched_goal is not None:
            n_goals = tuple(gi for gi in rem_goals if gi != matched_goal)
            
        t_phase = nt % 4
        state_key = (nx, ny, ns, nc, nr, nbatts, n_goals, t_phase)
        if state_key in best_fuel and best_fuel[state_key] >= nfuel:
            continue
        best_fuel[state_key] = nfuel
        q.append(((nx, ny, ns, nc, nr, nfuel, nbatts, n_goals, nt), acts + [act]))

if found:
    print(f'Level 5 SOLVED in {len(found)} actions after exploring {visited_count} states! Sequence: {found}')
    for i, a in enumerate(found):
        obs = env.step(moves[a])
        if obs.levels_completed > 4:
            print(f'[SUCCESS] Level 5 cleared at step {i+1}!')
            break
    print('Levels completed after executing Level 5 solution:', obs.levels_completed)
else:
    print(f'Failed to solve Level 5 after exploring {visited_count} states.')
