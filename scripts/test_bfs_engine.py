import sys
from pathlib import Path
from collections import deque
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "vendor" / "ARC-AGI-3-Agents"))

import arc_agi
from arcengine import GameAction, GameState

def hash_frame(frame):
    if hasattr(frame, "frame") and frame.frame:
        f0 = frame.frame[0]
        if hasattr(f0, "tobytes"):
            return f0.tobytes()
        return bytes([int(x) for row in f0 for x in row])
    return b""

def solve_env(game_id="ls20", max_actions=100):
    arc = arc_agi.Arcade(operation_mode=arc_agi.OperationMode.OFFLINE)
    env = arc.make(game_id)
    f0 = env.reset()
    
    # Graph: state_hash -> {action_id: next_state_hash}
    graph = {}
    untried = {} # state_hash -> list of action_ids
    fatal = set() # (state_hash, action_id)
    noop = set() # (state_hash, action_id)
    parent = {} # next_state_hash -> (from_state_hash, action_id)
    
    start_hash = hash_frame(f0)
    avail = [a for a in f0.available_actions if a != GameAction.RESET]
    untried[start_hash] = list(avail)
    
    cur_hash = start_hash
    cur_state_obj = f0
    step_count = 0
    playback_queue = deque()
    
    print(f"Starting BFS on {game_id}, initial available actions: {avail}")
    
    while step_count < max_actions:
        step_count += 1
        
        # Check if won
        if cur_state_obj.levels_completed > 0:
            print(f"[SUCCESS] Won level in {step_count} actions! levels_completed={cur_state_obj.levels_completed}")
            return True, step_count
            
        if cur_state_obj.state == GameState.GAME_OVER:
            print(f"[DEATH] at step {step_count}, resetting...")
            f_reset = env.step(GameAction.RESET)
            cur_hash = hash_frame(f_reset)
            cur_state_obj = f_reset
            playback_queue.clear()
            continue

        # If we have a planned playback path to frontier, follow it
        if playback_queue:
            act_id = playback_queue.popleft()
            act = GameAction.from_id(act_id) if isinstance(act_id, int) else GameAction.from_name(act_id)
            nxt = env.step(act)
            nxt_hash = hash_frame(nxt)
            cur_hash = nxt_hash
            cur_state_obj = nxt
            continue
            
        # If current state has untried actions, try one
        actions_left = untried.get(cur_hash, [])
        if actions_left:
            act_id = actions_left.pop(0)
            act = GameAction.from_id(act_id) if isinstance(act_id, int) else GameAction.from_name(act_id)
            nxt = env.step(act)
            nxt_hash = hash_frame(nxt)
            
            # Record transition
            graph.setdefault(cur_hash, {})[act_id] = nxt_hash
            
            if nxt.state == GameState.GAME_OVER:
                fatal.add((cur_hash, act_id))
                cur_hash = nxt_hash
                cur_state_obj = nxt
                continue
                
            if nxt_hash == cur_hash:
                # No-op (hit wall)
                noop.add((cur_hash, act_id))
            else:
                if nxt_hash not in untried and nxt.state != GameState.GAME_OVER:
                    avail_nxt = [a for a in nxt.available_actions if a != GameAction.RESET]
                    untried[nxt_hash] = list(avail_nxt)
                    parent[nxt_hash] = (cur_hash, act_id)
                    
            cur_hash = nxt_hash
            cur_state_obj = nxt
            continue
            
        # No untried actions in current state. Find shortest path to ANY state with untried actions!
        target_path = None
        # BFS from cur_hash
        q = deque([(cur_hash, [])])
        vis = {cur_hash}
        while q:
            s, path = q.popleft()
            if untried.get(s, []):
                target_path = path
                break
            for a_id, nxt_s in graph.get(s, {}).items():
                if (s, a_id) not in fatal and (s, a_id) not in noop and nxt_s not in vis:
                    vis.add(nxt_s)
                    q.append((nxt_s, path + [a_id]))
                    
        if target_path:
            playback_queue.extend(target_path)
            continue
            
        # If no reachable state from cur_hash, RESET and route from start_hash!
        print(f"[RESET TO START] No frontier reachable from current state at step {step_count}")
        f_reset = env.step(GameAction.RESET)
        cur_hash = hash_frame(f_reset)
        cur_state_obj = f_reset
        
        # BFS from start_hash to any untried
        q = deque([(cur_hash, [])])
        vis = {cur_hash}
        found_path = None
        while q:
            s, path = q.popleft()
            if untried.get(s, []):
                found_path = path
                break
            for a_id, nxt_s in graph.get(s, {}).items():
                if (s, a_id) not in fatal and (s, a_id) not in noop and nxt_s not in vis:
                    vis.add(nxt_s)
                    q.append((nxt_s, path + [a_id]))
                    
        if found_path:
            playback_queue.extend(found_path)
        else:
            print(f"[EXHAUSTED] Entire graph searched, no remaining frontiers.")
            break
            
    print(f"Finished run: state={cur_state_obj.state}, levels={cur_state_obj.levels_completed}, steps={step_count}")
    return cur_state_obj.levels_completed > 0, step_count

if __name__ == "__main__":
    solve_env("ls20", max_actions=100)
