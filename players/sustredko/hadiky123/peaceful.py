from typing import Any, List, Tuple
import heapq as hq
from longest_path_dp import longest_path
from common import *
from map_functions import *
import random
from main import *
import time
from areas import area_fill_move


def is_legit_coord(x: int, y: int, map: Map) -> bool:
    return 0 <= x and x < map.width and 0 <= y and y < map.height


def dx_dy_to_dir(dx: int, dy: int) -> int:
    # up, right, down, left :: 0, 1, 2, 3
    if dy < 0:
        dir = 0
    elif dx > 0:
        dir = 1
    elif dy > 0:
        dir = 2
    elif dx < 0:
        dir = 3
    return dir


def dir_to_dx_dy(dir: int) -> Tuple[int, int]:
    return [(0, -1), (1, 0), (0, 1), (-1, 0)][dir]


def rotation_from_direction(player: Player, target: Tuple[int, int]) -> Direction:
    us = player
    dx, dy = target[0] - us.x, target[1] - us.y
    our_dir = dx_dy_to_dir(us.dx, us.dy)
    target_dir = dx_dy_to_dir(dx, dy)
    rotate = [Direction.LEFT, Direction.NONE, Direction.RIGHT, Direction.NONE][
        ((target_dir - our_dir) % 4 + 1) % 4
    ]
    return rotate


vis = set()

TL = 0.5


def peaceful_move(old_map: Map, us: Player, client: TronClient) -> Command:
    x, y = us.x, us.y
    speed = us.speed
    """
    for nx, ny, new_dir in ((x + speed, y, 1), (x - speed, y, 3),
            (x, y + speed, 2), (x, y - speed, 0)):
    """
    to_return = Command(Direction.NONE)
    to_return.direction = Direction.NONE

    rs = longest_path(x, y, old_map)
    if rs is not None:
        nx, ny = rs
        to_return.direction = rotation_from_direction(us, (nx, ny))
        return to_return

    max_length = 0
    start_time = time.time()
    while time.time() - start_time < TL:
        vis.clear()
        best = dfs(us.x, us.y, old_map, client)
        if best[1] is None:
            continue
        if best[0] > max_length:
            max_length = best[0]
            to_return.direction = rotation_from_direction(us, best[1])
    to_return.use_powerup = us.powerup in (
        PowerUpType.SPEED_OTHERS,
        PowerUpType.STOP_ME,
    )

    return to_return


DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def dfs(x: int, y: int, map: Map, client, depth: float = 1, fp=None) -> None:
    if (x, y) in vis:
        return (depth, (fp))
    vis.add((x, y))
    best = (depth, fp)

    dirs = DIRS[:]
    random.shuffle(dirs)
    nc = 0

    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if is_legit_coord(nx, ny, map):
            if map.contents[nx][ny] == WALL or (nx, ny) in vis:
                nc += 1
            if map.contents[nx][ny] == FREE:
                score, fr = dfs(
                    nx,
                    ny,
                    map,
                    client,
                    depth + 1,
                    (nx, ny) if fp is None else fp,
                )
                if score > best[0]:
                    best = (score, fr)
        else:
            nc += 1
    bonus = [0, -5888.8, -300, -4500, -1e5][nc] / (depth ** 1.5)
    return best[0] + bonus, best[1]
