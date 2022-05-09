from common import *
from map_functions import *


def getbit(num, i):
    return (num >> i) & 1


MAX_NODES = 24


def longest_path(x, y, map) -> Tuple[int, int]:  # None if too many nodes
    bfs = create_bfs_grid_from_point(map, x, y, None)
    reachable = set()
    for i in range(len(bfs)):
        for j in range(len(bfs[i])):
            if bfs[i][j] is not None:
                reachable.add((i, j))
    n = len(reachable)
    if n > MAX_NODES:
        return None
    p = 1 << n

    mp = {}  # coord to id
    m2 = {}  # id to coord
    ctr = 0
    for i in reachable:
        mp[i] = ctr
        m2[ctr] = i
        ctr += 1

    dp = [[(-1)] * n] * p
    res = 0

    for i in range(p):
        for j in range(n):
            if dp[i][j] == -1:
                continue
            else:
                res = dp[i][j]
            pos = m2[j]
            if getbit(i, j) == 1:
                ci = i ^ (1 << j)

                for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    if (pos[0] + d[0], pos[1] + d[1]) in reachable:
                        id = mp[(pos[0] + d[0], pos[1] + d[1])]
                        if dp[ci][id] != -1:
                            dp[i][j] = dp[ci][id]
    return m2[res]
