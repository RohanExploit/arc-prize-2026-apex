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

# L1 - L5
for a in [3, 3, 3, 1, 1, 1, 1, 4, 4, 4, 1, 1, 1]: env.step(moves[a])
for a in [1, 4, 1, 1, 1, 1, 1, 4, 4, 2, 4, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 1, 4, 1, 2, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 2, 3, 2, 2, 2, 2, 2]: env.step(moves[a])
for a in [1, 1, 1, 1, 1, 1, 1, 1, 3, 2, 2, 4, 2, 2, 2, 3, 2, 2, 2, 1, 1, 1, 3, 3, 1, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 3, 1, 2, 1, 4, 2]: env.step(moves[a])
for a in [3, 3, 3, 2, 2, 2, 3, 2, 2, 3, 3, 1, 2, 1, 2, 1, 2, 1, 1, 3, 3, 1, 2, 3, 3, 1, 1, 1, 2, 2, 4, 1, 1, 1, 1, 4, 1, 4, 1, 1, 3, 3, 3]: env.step(moves[a])
l5_acts = [1, 3, 1, 1, 3, 3, 3, 4, 3, 4, 3, 4, 4, 4, 3, 2, 2, 3, 3, 3, 1, 3, 1, 2, 2, 2, 2, 2, 2, 4, 4, 3, 2, 2, 4, 2, 4, 4, 4, 4, 4, 4, 4, 1]
for a in l5_acts: obs = env.step(moves[a])

print('=== READY FOR LEVEL 6 ===')
print('Current level index:', g._current_level_index)

lvl = g.current_level
start_x, start_y = g.gudziatsk.x, g.gudziatsk.y
fuel_max = 42
start_fuel = g._step_counter_ui.osgviligwp or 42
step_dec = g._step_counter_ui.efipnixsvl or 1

target_shapes = g.ldxlnycps
target_cols = g.yjdexjsoa
target_rots = g.ehwheiwsk

wall_sprites = lvl.get_sprites_by_tag('ihdgageizm')
battery_sprites = lvl.get_sprites_by_tag('npxgalaybz')
goal_sprites = list(g.plrpelhym)
shape_switches = lvl.get_sprites_by_tag('ttfwljgohq')
col_switches = lvl.get_sprites_by_tag('soyhouuebz')
rot_switches = lvl.get_sprites_by_tag('rhsxkxzdjz')
pistons = list(g.hasivfwip)

print(f'Start pos: ({start_x}, {start_y}), fuel: {start_fuel}, dec: {step_dec}')
print(f'Walls: {len(wall_sprites)}, Batteries: {len(battery_sprites)}, Goals: {len(goal_sprites)}')
print(f'Switches: shape={len(shape_switches)}, col={len(col_switches)}, rot={len(rot_switches)}, pistons={len(pistons)}')

def is_wall(px, py):
    if not (0 <= px < 64 and 0 <= py < 64): return True
    for w in wall_sprites:
        if px <= w.x < px + 5 and py <= w.y < py + 5: return True
    return False

def aabb_overlap(x1, y1, w1, h1, x2, y2, w2, h2):
    return x1 < x2 + w2 and x2 < x1 + w1 and y1 < y2 + h2 and y2 < y1 + h1

initial_state = (start_x, start_y, g.fwckfzsyc, g.hiaauhahz, g.cklxociuu, start_fuel, tuple(range(len(battery_sprites))), tuple(range(len(goal_sprites))))

q = deque([(initial_state, [])])
best_fuel = {}
found = None
visited_count = 0

while q:
    (x, y, s, c, r, fuel, batts, rem_goals), acts = q.popleft()
    visited_count += 1
    if visited_count % 20000 == 0:
        print(f'Visited {visited_count} states, queue len {len(q)}, rem_goals {len(rem_goals)}')

    if len(rem_goals) == 0:
        found = acts
        break

    for act in [1, 2, 3, 4]:
        dx, dy = action_deltas[act]
        nx, ny = x + dx, y + dy
        if is_wall(nx, ny):
            continue
        nfuel = fuel - step_dec
        if nfuel < 0:
            continue

        # Check pistons
        for p in pistons:
            if aabb_overlap(nx, ny, 5, 5, p.sprite.x, p.sprite.y, p.sprite.width, p.sprite.height):
                p_steps = p.ullzqnksoj(g.gudziatsk)
                nx = nx + p.dx * 5 * p_steps
                ny = ny + p.dy * 5 * p_steps
                break

        if is_wall(nx, ny):
            continue

        nbatts = list(batts)
        for bi in batts:
            b = battery_sprites[bi]
            if aabb_overlap(nx, ny, 5, 5, b.x, b.y, b.width, b.height):
                nfuel = fuel_max
                nbatts.remove(bi)
                break
        nbatts = tuple(nbatts)

        ns, nc, nr = s, c, r
        for sw in shape_switches:
            if aabb_overlap(nx, ny, 5, 5, sw.x, sw.y, sw.width, sw.height):
                ns = (ns + 1) % 6
                break
        for sw in col_switches:
            if aabb_overlap(nx, ny, 5, 5, sw.x, sw.y, sw.width, sw.height):
                nc = (nc + 1) % 5
                break
        for sw in rot_switches:
            if aabb_overlap(nx, ny, 5, 5, sw.x, sw.y, sw.width, sw.height):
                nr = (nr + 1) % 4
                break

        # Check collision with uncollected goals
        blocked = False
        matched_goal = None
        for gi in rem_goals:
            goal = goal_sprites[gi]
            if aabb_overlap(nx, ny, 5, 5, goal.x, goal.y, goal.width, goal.height):
                req_s = target_shapes[gi]
                req_c = target_cols[gi]
                req_r = target_rots[gi]
                if ns == req_s and nc == req_c and nr == req_r:
                    if nx == goal.x and ny == goal.y:
                        matched_goal = gi
                else:
                    blocked = True
                    break
        if blocked:
            continue

        n_goals = rem_goals
        if matched_goal is not None:
            n_goals = tuple(gi for gi in rem_goals if gi != matched_goal)

        state_key = (nx, ny, ns, nc, nr, nbatts, n_goals)
        if state_key in best_fuel and best_fuel[state_key] >= nfuel:
            continue
        best_fuel[state_key] = nfuel
        q.append(((nx, ny, ns, nc, nr, nfuel, nbatts, n_goals), acts + [act]))

if found:
    print(f'Level 6 SOLVED in {len(found)} actions after exploring {visited_count} states! Sequence: {found}')
    for i, a in enumerate(found):
        obs = env.step(moves[a])
        if obs.levels_completed > 5:
            print(f'[SUCCESS] Level 6 cleared at step {i+1}!')
            break
    print('Levels completed after executing Level 6 solution:', obs.levels_completed)
else:
    print(f'No solution found after exploring {visited_count} states.')
