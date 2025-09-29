''' R=起点
G=普通可走
蝴蝶1生成可走=a
蝴蝶2生成可走=b
第一个蝴蝶块=1
第二个蝴蝶块=2
.=不可走'''
grid_lines = [
    "...aGa.",
    "...G.G.",
    ".GG.Ga",
    "GGGGb..",
    "GG1Rb..",
    "..GGG2G",
    "....GG."
]
from collections import deque
import sys
sys.setrecursionlimit(10000)
grid = [list(row) for row in grid_lines]
R = len(grid)
C = len(grid[0])
blue_chars = {'a':0, 'b':1}
yellow_to_bit = {'1':0, '2':1}
start = None
walkable_coords = set()
for i in range(R):
    for j in range(C):
        ch = grid[i][j]
        if ch == 'R':
            start = (i,j)
            walkable_coords.add((i,j))
        elif ch != '.':
            walkable_coords.add((i,j))
if start is None:
    raise ValueError("R起点未找到")
total_to_visit = len(walkable_coords)
dirs = [(1,0),(-1,0),(0,1),(0,-1)]
def enterable(i,j, unlocked_mask):
    if i<0 or i>=R or j<0 or j>=C: return False
    ch = grid[i][j]
    if ch == '.': return False
    if ch in blue_chars:
        bit = blue_chars[ch]
        return ((unlocked_mask >> bit) & 1) == 1
    return True
visited_global_counter = 0
found_path = None
def dfs(i,j, visited, unlocked_mask, path):
    global visited_global_counter, found_path
    visited_global_counter += 1
    if found_path is not None:
        return True
    ch = grid[i][j]
    if ch in yellow_to_bit:
        unlocked_mask |= (1 << yellow_to_bit[ch])
    visited.add((i,j))
    path.append((i,j))
    if len(visited) == total_to_visit:
        found_path = list(path)
        return True
    neighs = []
    for di,dj in dirs:
        ni,nj = i+di, j+dj
        if (ni,nj) in visited: continue
        if not enterable(ni,nj, unlocked_mask): continue
        neighs.append((ni,nj))
    def degree(cell):
        ci,cj = cell
        cnt = 0
        for di,dj in dirs:
            xi,xj = ci+di, cj+dj
            if (xi,xj) in visited: continue
            if enterable(xi,xj, unlocked_mask):
                cnt += 1
        return cnt
    neighs.sort(key=degree)
    for ni,nj in neighs:
        if dfs(ni,nj, visited, unlocked_mask, path):
            return True
    visited.remove((i,j))
    path.pop()
    return False
visited=set()
found_path=None
dfs(start[0], start[1], visited, 0, [])

if found_path:
    print("步骤数：", len(found_path))
    print(found_path)
else:
    print("未找到满足条件的完整路径（可能无解或需要更长时间?..")
print("搜索节点数：", visited_global_counter)