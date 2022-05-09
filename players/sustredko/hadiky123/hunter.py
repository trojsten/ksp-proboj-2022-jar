from collections import deque

from numpy import block

from common import *
from map_functions import *
from peaceful import peaceful_move
from typing import Tuple
from copy import deepcopy
from check_line import check_rectangle, block_rectangle

dx = [-1, 0, 1, 0]
dy = [0, -1, 0, 1]

INF = 1e9

FREE = False

moves_ahead = 2


def hunter(client: TronClient) -> Command:
    return check_and_correct_move_safety(get_move_to_follow_closest(client), client)


SAVING_POWERUP_GOODNESS = 2
FOLLOW_DIST = 20


def check_and_correct_move_safety(move: Command, client: TronClient) -> Command:
    speed = client.myself.speed
    if speed == 0:
        return Command(Direction.NONE, False)
    dirs = ((-1, 0), (0, -1), (1, 0), (0, 1))
    ip = dirs.index((client.myself.dx, client.myself.dy))
    goodnesses = {}

    split_board = deepcopy(client.map)
    map = deepcopy(client.map)
    for player in client.players:
        if player == client.myself:
            continue
        split_board.contents[player.x][player.y] = WALL
        for i in range(4):
            nx = player.x + dx[i] * player.speed
            ny = player.y + dy[i] * player.speed
            if is_legit_coord(nx, ny, map):
                map.contents[nx][ny] = 2
                split_board.contents[nx][ny] = WALL

    # left
    shft = (ip + 3) % 4
    nx = dx[shft] * speed + client.myself.x
    ny = dy[shft] * speed + client.myself.y
    split1 = block_rectangle(split_board, (client.myself.x, client.myself.y), (nx, ny))
    if (
        is_legit_coord(nx, ny, map)
        and check_rectangle(map, (client.myself.x, client.myself.y), (nx, ny)) == True
    ):
        goodnesses[Direction.LEFT] = compute_goodness(split1, nx, ny)
    if (
        is_legit_coord(nx, ny, map)
        and check_rectangle(map, (client.myself.x, client.myself.y), (nx, ny)) == 2
    ):
        goodnesses[Direction.LEFT] = -100000 + compute_goodness(split1, nx, ny)

    # right
    shft = (ip + 1) % 4
    nx = dx[shft] * speed + client.myself.x
    ny = dy[shft] * speed + client.myself.y
    split2 = block_rectangle(split_board, (client.myself.x, client.myself.y), (nx, ny))
    if (
        is_legit_coord(nx, ny, map)
        and check_rectangle(map, (client.myself.x, client.myself.y), (nx, ny)) == True
    ):
        goodnesses[Direction.RIGHT] = compute_goodness(split2, nx, ny)
    if (
        is_legit_coord(nx, ny, map)
        and check_rectangle(map, (client.myself.x, client.myself.y), (nx, ny)) == 2
    ):
        goodnesses[Direction.RIGHT] = -100000 + compute_goodness(split2, nx, ny)

    # none
    shft = ip
    nx = dx[shft] * speed + client.myself.x
    ny = dy[shft] * speed + client.myself.y
    split3 = block_rectangle(split_board, (client.myself.x, client.myself.y), (nx, ny))
    if (
        is_legit_coord(nx, ny, map)
        and check_rectangle(map, (client.myself.x, client.myself.y), (nx, ny)) == True
    ):
        goodnesses[Direction.NONE] = compute_goodness(split3, nx, ny)
    if (
        is_legit_coord(nx, ny, map)
        and check_rectangle(map, (client.myself.x, client.myself.y), (nx, ny)) == 2
    ):
        goodnesses[Direction.NONE] = -100000 + compute_goodness(split3, nx, ny)

    if len(goodnesses) == 0:

        raise Exception

    if move.direction in goodnesses and goodnesses[move.direction] == max(
        goodnesses.values()
    ):
        return move

    max_goodness = max(goodnesses.values())
    return Command(
        max(goodnesses, key=lambda x: goodnesses[x]),
        max_goodness <= SAVING_POWERUP_GOODNESS
        and client.myself.powerup in (PowerUpType.STOP_ME, PowerUpType.CLEAN),
    )


def to_bounds(x: int, y: int, map: Map) -> Tuple[int, int]:
    x = max(0, x)
    x = min(map.width - 1, x)
    y = max(0, y)
    y = min(map.height - 1, y)
    return x, y


def get_move_to_follow_closest(client: TronClient) -> Command:
    speed = client.myself.speed
    pos = client.myself.x, client.myself.y

    grid = deepcopy(client.map)

    mindist = INF
    RES = INF

    for player in client.players:
        if player == client.myself:
            continue
        grid.contents[player.x][player.y] = WALL

        for i in range(4):
            nx, ny = player.x + dx[i] * player.speed, player.y + dy[i] * player.speed
            if nx < 0 or nx >= client.map.width or ny < 0 or ny >= client.map.height:
                continue
            grid.contents[nx][ny] = WALL

    dists = create_bfs_grid_from_point(grid, pos[0], pos[1], INF)
    for player in client.players:
        aheadx = player.x + player.dx * moves_ahead * player.speed
        aheady = player.y + player.dy * moves_ahead * player.speed

        if is_legit_coord(aheadx, aheady, grid) and dists[aheadx][aheady] < mindist:
            mindist = dists[aheadx][aheady]
            RES = aheadx, aheady

    if RES == INF:
        return peaceful_move(grid, client.myself, client)

    dists_from_target = create_bfs_grid_from_point(grid, RES[0], RES[1], INF)
    rRES = INF

    for i in range(4):
        nx, ny = (pos[0] + dx[i], pos[1] + dy[i])
        if nx < 0 or nx >= client.map.width or ny < 0 or ny >= client.map.height:
            continue
        if dists_from_target[nx][ny] < mindist:
            rRES = (nx, ny)

    use_powerup = client.myself.powerup in (
        PowerUpType.STOP_OTHERS,
        PowerUpType.SPEED_ME,
    )
    if rRES == INF or mindist > FOLLOW_DIST:
        return peaceful_move(client.map, client.myself, client)

    if speed == 0:
        return Command(Direction.NONE, use_powerup)
    dirs = ((-1, 0), (0, -1), (1, 0), (0, 1))
    try:
        ip = dirs.index((client.myself.dx, client.myself.dy))
    except:
        ip = 1

    if (
        rRES[0] - pos[0] == client.myself.dx
        and rRES[1] - pos[1] == client.myself.dy
    ):
        return Command(Direction.NONE, use_powerup)

    iR = dirs.index((rRES[0] - pos[0], rRES[1] - pos[1]))

    if iR - ip == 1 or iR - ip == -3:
        return Command(Direction.RIGHT, use_powerup)
    else:
        return Command(Direction.LEFT, use_powerup)


def zigzag(start, client: TronClient) -> Direction:
    pass
    """
    while pred bot nie je stena:
        if stena o dve policka vpred:

    """
