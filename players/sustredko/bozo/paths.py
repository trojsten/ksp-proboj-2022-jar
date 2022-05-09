from common import *
from typing import Tuple
from utils import Dir, has_powerup, right, left, free


def unable(x1, y1, x2, y2, client: TronClient) -> bool:
    board = client.map.contents
    dx = x2-x1
    dy = y2-y1
    for i in range(1, max(abs(x2-x1), abs(y2-y1))+1):
        if not free(x1 + dx*i, y1 + dy*i, client):
            return True
    return False
    

def get_path(x, y, client: TronClient, powerup = False) -> List[Tuple[int, int]]:
    grid = client.map.contents
    bozo = client.myself
    origin = (bozo.x, bozo.y)
    target = (x, y)
    found, found_powerup = False, False

    q, seen = [], {origin}
    pred = {origin: origin}
    dist = {origin: 0}
    q.append(origin)

    while q:
        # client.log(f"[BFS]: Q({len(q)} {q})")
        tile = q.pop(0)
        # client.log(f"[BFS]: zerem {tile}")

        if powerup and has_powerup(*tile, client):
            target = tile

        if tile == target:
            found = True
            break

        last = pred[tile]
        if tile == origin:
            delta = (bozo.dx, bozo.dy)
        else:
            delta = (tile[0] - last[0], tile[1] - last[1])  # abs vector rotacie
        neighbours = [(tile[0] + delta[0], tile[1] + delta[1]),
                      right(*tile, *delta, bozo.speed)[0],
                      left(*tile, *delta, bozo.speed)[0]]

        for n in neighbours:  # for each neighbour
            # client.log(f"mam sus {neighbours}   n je {n}")
            # dx, dy = vect.value
            # n = (tile[0] + dx, tile[1] + dy)

            if unable(*tile, *n, client):
                continue
            x, y = n

            # Invalid tile (wall or out)
            if not (0 <= x < client.map.width and 0 <= y < client.map.height):
                continue
            if grid[x][y]:
                continue

            # client.log(f"[BFS]: vidim {tile}")

            # Found shorter path
            if n not in dist or dist[n] > dist[tile] + 1:
                # client.log(f"[BFS]: kratsia {n}: {n not in dist}")
                dist[n] = dist[tile] + 1
                pred[n] = tile

            # client.log(f"[BFS]: videl som {seen}")
            if n not in seen:
                seen.add(n)
                q.append(n)
                # client.log(f"[BFS]: nove {n}")

    if not found:
        # client.log(f"Path not found")
        return []

    # client.log(f"[BFS: stavam")
    path = []
    tile = target
    while tile != origin:
        path.append(tile)
        tile = pred[tile]

    path.reverse()
    # client.log(f"[BFS]: mam {'k cukriku' if found_powerup else 'k bodu'} {path}")
    # client.log(f"[BFS]: mam {path[0]}...{path[-1]}")
    return path
