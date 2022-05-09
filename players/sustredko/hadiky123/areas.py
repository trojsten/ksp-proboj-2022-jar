from typing import Any, List, Tuple
from common import *
from map_functions import *
import random
from main import *
import time
from peaceful import *

AREA_SIDE = 20
AREA_DENSITY = 0.3


def area_fill_move(usc: TronClient) -> Direction:
    us = usc.myself
    x, y = us.x, us.y
    speed = us.speed
    if speed == 0:
        return Direction.NONE
    old_map = usc.map
    walls = 0

    x1, x2 = 0, us.dx * AREA_SIDE
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = 0, us.dy * AREA_SIDE
    y1, y2 = min(y1, y2), max(y1, y2)
    if x2 == 0:
        x1, x2 = -AREA_SIDE, AREA_SIDE
    elif y2 == 0:
        y1, y2 = -AREA_SIDE, AREA_SIDE
    for nx in range(x1, x2):
        for ny in range(y1, y2):
            if not is_legit_coord(x + nx, y + ny, old_map):
                continue
            if old_map.contents[nx][ny] == WALL:
                walls += 1

    if walls < AREA_SIDE * AREA_SIDE * AREA_DENSITY:
        return random.choice((Direction.LEFT, Direction.RIGHT))
    else:
        return Direction.NONE
