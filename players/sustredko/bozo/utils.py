from enum import Enum
from typing import Tuple
from common import *


class Dir(Enum):
    Up = 0, -1,
    Right = 1, 0,
    Down = 0, 1,
    Left = -1, 0,
# deltas = {Dir.Up: (0, -1), Dir.Right: (1, 0), Dir.Down: (0, 1), Dir.Left: (-1, 0)}


def right(x, y, dx, dy, speed) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    moves = {Dir.Right: Dir.Down, Dir.Down: Dir.Left, Dir.Left: Dir.Up, Dir.Up: Dir.Right}
    dx, dy = normalize(dx, dy)
    move = moves[Dir((dx, dy))]
    new_dx, new_dy = move.value
    return (x + new_dx*speed, y + new_dy*speed), (new_dx, new_dy)


def left(x, y, dx, dy, speed) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    moves = {Dir.Right: Dir.Up, Dir.Up: Dir.Left, Dir.Left: Dir.Down, Dir.Down: Dir.Right}
    dx, dy = normalize(dx, dy)
    move = moves[Dir((dx, dy))]
    new_dx, new_dy = move.value
    return (x + new_dx*speed, y + new_dy*speed), (new_dx, new_dy)


def free(x, y, client: TronClient):
    client.log(f"w: {client.map.width}  h: {client.map.height} [{x, y}]")
    if not (0 <= x < client.map.width and
            0 <= y < client.map.height):
        return False
    return not client.map.contents[x][y]


def has_powerup(x, y, client: TronClient) -> bool:
    for p in client.map.powerups:
        if p.x == x and p.y == y:
            # client.log(f"[POWER]: cukrik na {x,y}")
            return True
    return False


def get_direction(x, y, client: TronClient) -> Direction:
    bozo = client.myself
    current_delta = (bozo.dx, bozo.dy)  # smer teraz
    next_delta = (x - bozo.x, y - bozo.y)  # delta do bodu
    next_delta = normalize(*next_delta)

    if next_delta == current_delta:
        return Direction.NONE

    if current_delta == (1, 0):  # Right
        if next_delta == (0, 1): return Direction.RIGHT
        if next_delta == (0, -1): return Direction.LEFT
    if current_delta == (0, 1):  # Down
        if next_delta == (-1, 0): return Direction.RIGHT
        if next_delta == (1, 0): return Direction.LEFT
    if current_delta == (-1, 0):  # Left
        if next_delta == (0, -1): return Direction.RIGHT
        if next_delta == (0, 1): return Direction.LEFT
    if current_delta == (0, -1):  # Up
        if next_delta == (1, 0): return Direction.RIGHT
        if next_delta == (-1, 0): return Direction.LEFT

    client.log(f"current {current_delta}  next {next_delta}  chceme{x,y}  sme {bozo.x},{bozo.y}")
    client.log(f"NAPICU VSETKO")  # !shout dog


def print_powerup(client: TronClient):
    client.log(f"[POWER]: mam {client.myself.powerup}")


def normalize(x, y):
    x, y = min(x, 1), min(y, 1)
    x, y = max(x, -1), max(y, -1)
    return x, y
