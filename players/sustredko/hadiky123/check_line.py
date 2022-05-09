from common import *
from map_functions import *
from typing import Tuple
from copy import deepcopy


def is_legit_coord(x: int, y: int, map: Map) -> bool:
    return 0 <= x and x < map.width and 0 <= y and y < map.height


def check_rectangle(
    old_map: Map, our_pos: Tuple[int, int], target_pos: Tuple[int, int]
) -> bool:

    head = False
    x1, x2 = min(our_pos[0], target_pos[0]), max(our_pos[0], target_pos[0])
    y1, y2 = min(our_pos[1], target_pos[1]), max(our_pos[1], target_pos[1])
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if not is_legit_coord(x, y, old_map):
                continue
            if x == our_pos[0] and y == our_pos[1]:
                continue
            elif old_map.contents[x][y] == WALL:
                return False
            elif old_map.contents[x][y] == 2:
                head = True
    if head:
        return 2
    return True


def block_rectangle(map: Map, our_pos: Tuple[int, int], target_pos: Tuple[int, int]):
    res = deepcopy(map)
    x1, x2 = min(our_pos[0], target_pos[0]), max(our_pos[0], target_pos[0])
    y1, y2 = min(our_pos[1], target_pos[1]), max(our_pos[1], target_pos[1])
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if not is_legit_coord(x, y, map):
                continue
            if res.contents[x][y] == FREE:
                res.contents[x][y] = WALL
    return res
