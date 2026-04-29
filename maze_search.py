# Project 1 - Maze Search Agents (using 10x10)
from collections import deque
import math
maze = [
    ["¯ ", "¯ ", "¯ ", "¯ ", "¯ ", "¯ ", "¯ ", "¯ ", "¯ ", "¯|"],
    [" |", "¯ ", "¯ ", "¯ ", "¯ ", "¯ ", "¯ ", "¯ ", "¯ ", " |"],
    [" |", " ", "¯ ", "¯ ", "¯ ", "¯|", "¯ ", "¯ ", "¯ ", " |"],
    [" |", "¯ ", "¯ ", "¯ ", " |", "¯ ", "¯ ", "¯ ", "¯ ", "¯|"],
    [" |", " ", " ", " ", " |", " ", "¯|", "¯ ", "¯|", " |"],
    [" |", " ", " ", " ", " ", "¯ ", "¯ ", "¯ ", "¯ ", " |"],
    [" |", "¯ ", "¯ ", "¯ ", "¯ ", "¯ ", "¯ ", "¯ ", "¯ ", " |"],
    [" |", " |", "¯ ", "¯|", "¯ ", "¯|", "¯|", "¯|", "¯ ", " |"],
    [" |", " |", " |", " |", " |", " |", " ", " |", " ", "¯|"],
    [" |", " ", " |", " ", " |", " ", "¯ ", " ", "¯ ", " |"],
]
ROWS, COLS = 10, 10
START = (0, 0)
GOAL = (9, 9)
# Normalizing maze cells
maze = [[(s + " ") if len(s) == 1 else s for s in row] for row in maze]
# Movement rules
def move_up(r, c):
    return r > 0 and maze[r][c][0] == " "
def move_right(r, c):
    return c < COLS - 1 and maze[r][c][1] == " "
def move_left(r, c):
    return c > 0 and maze[r][c - 1][1] == " "
def move_down(r, c):
    return r < ROWS - 1 and maze[r + 1][c][0] == " "
MOVES = [
    ("U", (-1, 0), move_up),
    ("R", (0, 1), move_right),
    ("D", (1, 0), move_down),
    ("L", (0, -1), move_left),
]
# Getting adjacent neighbors from a node
def adjacent(node):
    r, c = node
    for mv, (dr, dc), ok in MOVES:
        if ok(r, c):
            yield mv, (r + dr, c + dc)
# Making the path when goal found
def reconstruct(parent, end):
    nodes, moves = [], []
    current = end
    # While we have a recorded parent,we  keep stepping backward
    while current in parent:
        prev, mv = parent[current]
        nodes.append(current)
        moves.append(mv)
        current = prev
    nodes.append(current)
    # Reversing to get forward order
    nodes.reverse()
    moves.reverse()
    return nodes, moves
def bfs(start=START, goal=GOAL):
    FIFO = deque([start])     # Queue of nodes to expand next
    parent = {}               # To reconstruct the  path
    visited = {start}         # Nodes we've discovered already
    expanded = 0              # Count of expanded nodes
    while FIFO:
        current = FIFO.popleft()
        expanded += 1
        # If we reach the goal, we reconstruct and return solution
        if current == goal:
            nodes, moves = reconstruct(parent, current)
            return nodes, moves, expanded
        # Otherwise, expanding neighbors
        for mv, nxt in adjacent(current):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = (current, mv)
                FIFO.append(nxt)
    # If no goal found
    return None, None, expanded
def dfs(start=START, goal=GOAL, order=("R", "D", "L", "U")):
    order_map = {m: i for i, m in enumerate(order)}
    def ordered_adjacent(node):
        nbs = list(adjacent(node))
        nbs.sort(key=lambda x: order_map.get(x[0], 999))
        return nbs
    best_moves, best_nodes, best_len = None, None, math.inf
    expanded = 0
    path_set = {start}    # To avoid cycles in the current path
    path_nodes = [start]
    path_moves = []
    def rec(current):
        nonlocal best_moves, best_nodes, best_len, expanded
        expanded += 1
        # If current path already worse or equal to best, prune it
        if len(path_moves) >= best_len:
            return
        if current == goal:
            best_len = len(path_moves)
            best_moves = list(path_moves)
            best_nodes = list(path_nodes)
            return
        for mv, nxt in ordered_adjacent(current):
            if nxt in path_set:
                continue  # prevents infinite loops
            path_set.add(nxt)
            path_nodes.append(nxt)
            path_moves.append(mv)
            rec(nxt)
            # backtrack (undo move)
            path_moves.pop()
            path_nodes.pop()
            path_set.remove(nxt)
    rec(start)
    return best_nodes, best_moves, expanded
def dls(start, goal, limit, order=("R", "D", "L", "U")):
    order_map = {m: i for i, m in enumerate(order)}
    def ordered_adjacent(node):
        nbs = list(adjacent(node))
        nbs.sort(key=lambda x: order_map.get(x[0], 999))
        return nbs
    expanded = 0
    parent = {}
    stack = [(start, 0)]
    # if seen a node at a smaller depth, no need to revisit it deeper.
    best_depth = {start: 0}
    while stack:
        current, depth = stack.pop()
        expanded += 1
        if current == goal:
            nodes, moves = reconstruct(parent, current)
            return nodes, moves, expanded, True
        if depth == limit:
            continue
        children = ordered_adjacent(current)
        for mv, nxt in reversed(children):
            nd = depth + 1
            if nxt not in best_depth or nd < best_depth[nxt]:
                best_depth[nxt] = nd
                parent[nxt] = (current, mv)
                stack.append((nxt, nd))
    return None, None, expanded, False
def ids(start=START, goal=GOAL, max_depth=300, order=("R", "D", "L", "U")):
    total_expanded = 0
    for limit in range(max_depth + 1):
        nodes, moves, expanded, found = dls(start, goal, limit, order=order)
        total_expanded += expanded
        if found:
            return nodes, moves, total_expanded, limit
    return None, None, total_expanded, None
# output
if __name__ == "__main__":
    # Running the three agents
    bfs_nodes, bfs_moves, bfs_expanded = bfs()
    dfs_nodes, dfs_moves, dfs_expanded = dfs()
    ids_nodes, ids_moves, ids_total_expanded, ids_depth = ids(max_depth=150)
    print("Maze Search Results (10x10):")
    print("BFS:")
    print(f"- Nodes expanded: {bfs_expanded}")
    print(f"- Optimal path length: {len(bfs_moves)} moves")
    print(f"- Moves: {''.join(bfs_moves)}\n")
    print("DFS")
    print(f"- Nodes expanded: {dfs_expanded}")
    print(f"- Optimal path length: {len(dfs_moves)} moves")
    print(f"- Moves: {''.join(dfs_moves)}\n")
    print("Iterative Deepening Search")
    print(f"- Nodes expanded total (all depth limits): {ids_total_expanded}")
    print(f"- Depth limit where solution found: {ids_depth}")
    print(f"- Optimal path length: {len(ids_moves)} moves")
    print(f"- Moves: {''.join(ids_moves)}\n")
    print("Numbered optimal steps:")
    for i, mv in enumerate(bfs_moves, start=1):
        print(f"{i:02d}. {mv}")