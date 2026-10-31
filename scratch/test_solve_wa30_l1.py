import os
os.chdir(r"E:\projects\arc-agi-3")
import arc_agi
from collections import deque
from arcengine import GameAction

arcade = arc_agi.Arcade(operation_mode=arc_agi.OperationMode.OFFLINE, environments_dir=r"E:\projects\arc-agi-3\environment_files")
env = arcade.make('wa30')
obs = env.reset()
g = env._game

moves = {1: GameAction.ACTION1, 2: GameAction.ACTION2, 3: GameAction.ACTION3, 4: GameAction.ACTION4, 5: GameAction.ACTION5}

# 1. Place Box 2 on goal
init_seq = [1, 1, 5, 1, 1, 5]
for a in init_seq: env.step(moves[a])

print('After Box 2 placed:')
p = g.current_level.get_sprites_by_tag('wbmdvjhthc')[0]
boxes = g.current_level.get_sprites_by_tag('geezpjgiyd')
print('Player:', (p.x, p.y))
for i, b in enumerate(boxes):
    print(f'Box {i}: ({b.x}, {b.y}), on_goal: {g.shbxbhnhjc((b.x, b.y))}')

# Now from (32, 32), let's move to Box 0 at (44, 24):
# Player (32, 32)
# Move Right: (36, 32), (40, 32), (44, 32) -> [4, 4, 4]
# Move Up: (44, 28) -> [1] (adjacent to Box 0 at 44, 24!)
# Attach: [5]
# Move Up: (44, 24), Box 0 at (44, 20) -> [1]
# Move Left: (40, 24), Box 0 at (40, 20) -> [3]
# Move Left: (36, 24), Box 0 at (36, 20) -> [3]
# Move Down: (36, 28), Box 0 at (36, 24) -> [2]
# Move Down: (36, 32), Box 0 at (36, 28)! -> [2]
# Detach: [5]

seq_b0 = [4, 4, 4, 1, 5, 1, 3, 3, 2, 2, 5]
for a in seq_b0: env.step(moves[a])

print('\nAfter Box 0 placed:')
p = g.current_level.get_sprites_by_tag('wbmdvjhthc')[0]
boxes = g.current_level.get_sprites_by_tag('geezpjgiyd')
print('Player:', (p.x, p.y))
for i, b in enumerate(boxes):
    print(f'Box {i}: ({b.x}, {b.y}), on_goal: {g.shbxbhnhjc((b.x, b.y))}')

# Now from (36, 32), let's move to Box 1 at (16, 28):
# Move Down: (36, 36) -> [2]
# Move Left: (32, 36), (28, 36), (24, 36), (20, 36), (16, 36) -> [3, 3, 3, 3, 3]
# Move Up: (16, 32) -> [1] (adjacent to Box 1 at 16, 28!)
# Attach: [5]
# Move Right: (20, 32), Box 1 at (20, 28) -> [4]
# Move Right: (24, 32), Box 1 at (24, 28) -> [4]
# Move Right: (28, 32), Box 1 at (28, 28)! -> [4]
# Detach: [5]

seq_b1 = [2, 3, 3, 3, 3, 3, 1, 5, 4, 4, 4, 5]
for a in seq_b1: obs = env.step(moves[a])

print('\nAfter Box 1 placed:')
p = g.current_level.get_sprites_by_tag('wbmdvjhthc')[0]
boxes = g.current_level.get_sprites_by_tag('geezpjgiyd')
print('Player:', (p.x, p.y))
for i, b in enumerate(boxes):
    print(f'Box {i}: ({b.x}, {b.y}), on_goal: {g.shbxbhnhjc((b.x, b.y))}')

print('\nLevels completed:', obs.levels_completed)
print('Total actions taken:', len(init_seq) + len(seq_b0) + len(seq_b1))
