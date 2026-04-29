# AI Search Algorithms & Game AI

Implementation of classical AI search algorithms and adversarial game playing.
Built for an AI course — all algorithms implemented from scratch in Python.

## Projects

### 1. Maze Solver — BFS, DFS, and Iterative Deepening Search
Three agents solve a 10x10 grid maze using different search strategies.

**Algorithms implemented:**
- Breadth-First Search (BFS) — guaranteed optimal, explores level by level
- Depth-First Search (DFS) — with branch-and-bound pruning for optimality
- Iterative Deepening Search (IDS) — combines BFS optimality with DFS memory efficiency

**Output per agent:**
- Optimal solution path (exact steps: U/D/L/R)
- Number of nodes expanded during search

**File:** `maze_search.py`

---

### 2. 3D Connect 4 AI Agent
An AI agent that plays 3D Connect 4 on a 4x4x4 board using adversarial search.

**Features:**
- Minimax with alpha-beta pruning
- Move ordering (win detection → block detection → center heuristic)
- Custom board evaluation function with weighted line scoring
- Time-limited search with 0.95s cutoff for real-time play
- Pre-generated all 76 possible 4-in-a-row lines at startup for fast evaluation

**File:** `3D_Connect4_final.py`

## How to Run

**Requirements:** Python 3.x (no external libraries needed)

**Maze solver:**
```bash
python3 maze_search.py
```

**3D Connect 4 agent:**
```bash
python3 3D_Connect4_final.py
```
The agent will print its first move on an empty board.
To integrate with a referee, call `ai_make_move(board, playerTurn)` — returns `[z, y, x]`.

## Key Concepts
Uninformed search · BFS · DFS · Iterative deepening · Minimax · 
Alpha-beta pruning · Adversarial search · Heuristic evaluation · Move ordering

## Course
CSC6013 — Artificial Intelligence
