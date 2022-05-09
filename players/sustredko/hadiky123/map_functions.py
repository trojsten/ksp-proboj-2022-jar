from typing import Any, List, Tuple
import heapq as hq
from check_line import check_rectangle
from common import *
from queue import deque


def is_legit_coord(x: int, y: int, map: Map) -> bool:
    return 0 <= x and x < map.width and 0 <= y and y < map.height


def generate_new_board(w: int, h: int, empty_value: Any) -> List[List[Any]]:
    return list(list(empty_value for y in range(h)) for x in range(w))


def compute_goodness(
    old_map: Map, pos_x: int, pos_y: int, coord0: Optional[Tuple[int, int]] = None
) -> int:
    no_int = -1
    board = generate_new_board(old_map.width, old_map.height, no_int)
    ans = 0

    if coord0 is not None:
        x0, y0 = coord0
    else:
        x0, y0 = pos_x, pos_y

    queue = deque([(pos_x, pos_y, 0)])

    while len(queue) > 0:
        x, y, v = queue.popleft()
        if board[x][y] != no_int:
            continue
        if (y == y0 and (x0 <= x < pos_x or x0 >= x > pos_x)) or (
            (y0 <= y < pos_y or y0 >= y > pos_y) and x == x0
        ):
            continue
        board[x][y] = v
        ans += 1
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if is_legit_coord(nx, ny, old_map):
                if old_map.contents[nx][ny] == FREE:
                    queue.append((nx, ny, v + 1))

    return ans


def create_bfs_grid_from_point(
    old_map: Map, pos_x: int, pos_y: int, empty_number: int
) -> List[List[Any]]:
    no_int = -1 if empty_number == None else empty_number
    board = generate_new_board(old_map.width, old_map.height, no_int)

    queue = deque([(pos_x, pos_y, 0)])
    board[pos_x][pos_y] = 0

    while len(queue) > 0:
        x, y, v = queue.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if is_legit_coord(nx, ny, old_map):
                if old_map.contents[nx][ny] == FREE:
                    if board[nx][ny] == no_int:
                        queue.append((nx, ny, v + 1))
                        board[nx][ny] = v + 1

    return board


"""
def create_dfs_paths(old_map: Map, pos_x: int, pos_y: int,
        max_number: int):
    best = -1
    for i in range(max_number):
        board = generate_new_board(old_map.width, old_map.height, -1)
        stack = [(pos_x, pos_y)]

        while len(stack) > 0:
"""
