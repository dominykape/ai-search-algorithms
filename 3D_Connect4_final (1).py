# -*- coding: utf-8 -*-
"""
Dominyka Petraskaite
3D Connect4 for 4x4x4 board agent.

Board coordinates: [z][y][x]
0 = empty, 1 = player 1, 2 = player 2

Main function the referee should call:
    ai_make_move(B, playerTurn) -> [z, y, x]
"""

import time

SIZE = 4
WIN_LEN = 4

# Directions we need for 3D lines
COO = [
    (1, 0, 0), (0, 1, 0), (0, 0, 1),
    (1, 1, 0), (1, -1, 0),
    (1, 0, 1), (1, 0, -1),
    (0, 1, 1), (0, 1, -1),
    (1, 1, 1), (1, 1, -1),
    (1, -1, 1), (1, -1, -1),
]

# Generated all 4-in-a-row lines once so evaluation is faster later.
ALL_LINES = []


def inside(z, y, x):
    return 0 <= z < SIZE and 0 <= y < SIZE and 0 <= x < SIZE


def build_lines():
    lines = []
    seen = set()

    for z in range(SIZE):
        for y in range(SIZE):
            for x in range(SIZE):
                for dz, dy, dx in COO:

                    # Only start a line if we are at the “first” cell in that direction.
                    if inside(z - dz, y - dy, x - dx):
                        continue

                    coords = []
                    ok = True
                    for k in range(WIN_LEN):
                        zz = z + dz * k
                        yy = y + dy * k
                        xx = x + dx * k
                        if not inside(zz, yy, xx):
                            ok = False
                            break
                        coords.append((zz, yy, xx))

                    if ok:
                        key = tuple(coords)
                        if key not in seen:
                            seen.add(key)
                            lines.append(key)

    return lines


ALL_LINES = build_lines()


def other_player(p):
    return 2 if p == 1 else 1


def list_moves(B):
    moves = []
    for z in range(SIZE):
        for y in range(SIZE):
            for x in range(SIZE):
                if B[z][y][x] == 0:
                    moves.append((z, y, x))
    return moves


def place(B, move, p):
    z, y, x = move
    B[z][y][x] = p


def unplace(B, move):
    z, y, x = move
    B[z][y][x] = 0


def check_winner(B):
    for line in ALL_LINES:
        (a, b, c, d) = line
        v = B[a[0]][a[1]][a[2]]
        if v != 0 and v == B[b[0]][b[1]][b[2]] == B[c[0]][c[1]][c[2]] == B[d[0]][d[1]][d[2]]:
            return v
    return 0


def centering_score(z, y, x):
    # small center bonus to increase the winning chance
    dist = abs(z - 1.5) + abs(y - 1.5) + abs(x - 1.5)
    return int(round(6 - dist))


WEIGHTS = {0: 0, 1: 1, 2: 10, 3: 60, 4: 10000}


def eval_board(B, me):
    them = other_player(me)

    w = check_winner(B)
    if w == me:
        return 200000
    if w == them:
        return -200000

    score = 0

    # Score open lines only because blocked lines don’t matter
    for line in ALL_LINES:
        me_count = 0
        them_count = 0

        for (z, y, x) in line:
            if B[z][y][x] == me:
                me_count += 1
            elif B[z][y][x] == them:
                them_count += 1

        if me_count and them_count:
            continue  # blocked

        if me_count:
            score += WEIGHTS[me_count]
        elif them_count:
            score -= WEIGHTS[them_count]

    # Center bonus 
    for z in range(SIZE):
        for y in range(SIZE):
            for x in range(SIZE):
                if B[z][y][x] == me:
                    score += centering_score(z, y, x)
                elif B[z][y][x] == them:
                    score -= centering_score(z, y, x)

    return score


def order_moves(B, moves, p):
    # Simple ordering: immediate win > immediate block > centering
    them = other_player(p)
    ranked = []

    for m in moves:
        z, y, x = m

        # winning
        B[z][y][x] = p
        if check_winner(B) == p:
            B[z][y][x] = 0
            ranked.append((10_000_000, m))
            continue
        B[z][y][x] = 0

        # blocking
        B[z][y][x] = them
        if check_winner(B) == them:
            B[z][y][x] = 0
            ranked.append((9_000_000, m))
            continue
        B[z][y][x] = 0

        ranked.append((centering_score(z, y, x), m))

    ranked.sort(reverse=True, key=lambda t: t[0])
    return [m for _, m in ranked]


def minimax_ab(B, depth, maximizing, me, alpha, beta, t0, time_limit):
    # extra credit part: time cutoff meaning: return heuristic if we’re about to go over
    if time.perf_counter() - t0 > time_limit:
        return eval_board(B, me), None

    if depth == 0 or check_winner(B) != 0:
        return eval_board(B, me), None

    moves = list_moves(B)
    if not moves:
        return 0, None

    current = me if maximizing else other_player(me)
    moves = order_moves(B, moves, current)

    best_move = None

    if maximizing:
        best_val = -10**9
        for m in moves:
            place(B, m, current)
            val, _ = minimax_ab(B, depth - 1, False, me, alpha, beta, t0, time_limit)
            unplace(B, m)

            if val > best_val:
                best_val = val
                best_move = m

            alpha = max(alpha, best_val)
            if beta <= alpha:
                break

            if time.perf_counter() - t0 > time_limit:
                break

        return best_val, best_move

    else:
        best_val = 10**9
        for m in moves:
            place(B, m, current)
            val, _ = minimax_ab(B, depth - 1, True, me, alpha, beta, t0, time_limit)
            unplace(B, m)

            if val < best_val:
                best_val = val
                best_move = m

            beta = min(beta, best_val)
            if beta <= alpha:
                break

            if time.perf_counter() - t0 > time_limit:
                break

        return best_val, best_move


def ai_make_move(B, playerTurn):
    t0 = time.perf_counter()
    time_limit = 0.95  # little buffer

    moves = list_moves(B)
    if not moves:
        return [0, 0, 0]

    # quick tactics first
    for m in order_moves(B, moves, playerTurn):
        place(B, m, playerTurn)
        if check_winner(B) == playerTurn:
            unplace(B, m)
            return [m[0], m[1], m[2]]
        unplace(B, m)

    them = other_player(playerTurn)
    for m in moves:
        place(B, m, them)
        if check_winner(B) == them:
            unplace(B, m)
            return [m[0], m[1], m[2]]
        unplace(B, m)

    # minimax depth 4 plies
    best_val, best_move = minimax_ab(B, 4, True, playerTurn, -10**9, 10**9, t0, time_limit)

    if best_move is None:
        best_move = order_moves(B, moves, playerTurn)[0]

    return [best_move[0], best_move[1], best_move[2]]


if __name__ == "__main__":
    empty = [[[0 for _ in range(SIZE)] for _ in range(SIZE)] for _ in range(SIZE)]
    print("Move for P1:", ai_make_move(empty, 1))
