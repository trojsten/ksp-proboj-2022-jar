#!/usr/bin/env python

import random
import time

from common import *

def t15(tc: TronClient):
    if not tc.myself.speed:
        return Command(Direction.NONE, False)
    ssuo = False
    rt = time.time()
    limit0 = 150
    limit1 = limit0 // (1.75 * len(tc.players) + 1)
    dirs = [Direction.LEFT, Direction.NONE, Direction.RIGHT]
    poss, newx, newy, susnewx, susnewy = ([] for i in range(5))
    for p in tc.players + [tc.myself]:
        poss.append([])
        newx.append([p.x + p.speed * p.dy, p.x + p.speed * p.dx, p.x - p.speed * p.dy])
        newy.append([p.y - p.speed * p.dx, p.y + p.speed * p.dy, p.y + p.speed * p.dx])
        susnewx.append([p.x + p.dy, p.x + p.dx, p.x - p.dy])
        susnewy.append([p.y - p.dx, p.y + p.dy, p.y + p.dx])
        for i in range(3):
            if not (tc.map.contents[newx[-1][i]][newy[-1][i]] or tc.map.contents[susnewx[-1][i]][susnewy[-1][i]] if (
                    0 <= newx[-1][i] < tc.map.width and 0 <= newy[-1][i] < tc.map.height) else True):
                poss[-1].append(i)
    dist = [tc.map.height * [0] for i in range(tc.map.width)]
    for p in range(len(tc.players)):
        for i in poss[p]:
            new = {(newx[p][i], newy[p][i])}
            newf = {(newx[p][i], newy[p][i])}
            old = set()
            oldf = set()
            t = 0
            while new and len(old) < limit1 and time.time() - rt < 0.8:
                t += 1
                newer = set()
                if t % 2:
                    newerf = set()
                for j in new:
                    dist[j[0]][j[1]] = max(dist[j[0]][j[1]], 1 / t)
                    for k in [(0, tc.players[p].speed), (tc.players[p].speed, 0), (0, -tc.players[p].speed), (-tc.players[p].speed, 0)]:
                        if (j[0] + k[0], j[1] + k[1]) not in old.union(new.union(newer)) and not (tc.map.contents[j[0] + k[0]][j[1] + k[1]] if 0 <= j[0] + k[0] < tc.map.width and 0 <= j[1] + k[1] < tc.map.height else True):
                            newer.add((j[0] + k[0], j[1] + k[1]))
                    if j in newf:
                        for k in [(0, 2 * tc.players[p].speed), (2 * tc.players[p].speed, 0), (0, -2 * tc.players[p].speed), (-2 * tc.players[p].speed, 0)]:
                            if (j[0] + k[0], j[1] + k[1]) not in old.union(new.union(newer)) and not (tc.map.contents[j[0] + k[0]][j[1] + k[1]] if 0 <= j[0] + k[0] < tc.map.width and 0 <= j[1] + k[1] < tc.map.height else True):
                                newerf.add((j[0] + k[0], j[1] + k[1]))
                old = old.union(new)
                new = newer
                if t % 2:
                    oldf = oldf.union(newf)
                    newf = newerf
            if len(oldf) < 6:
                ssuo = True
    area = []
    for i in poss[-1]:
        area.append(0)
        new = {(newx[-1][i], newy[-1][i], 1)}
        old = set()
        val = [tc.map.height * [0] for _ in range(tc.map.width)]
        val[newx[-1][i]][newy[-1][i]] = 1
        t = 0
        while new and len(old) < limit0 and time.time() - rt < 1.8:
            t += 1
            newer = set()
            for j in new:
                area[-1] += val[j[0]][j[1]]
                for k in [(0, tc.myself.speed), (tc.myself.speed, 0), (0, -tc.myself.speed), (-tc.myself.speed, 0)]:
                    l = (j[0] + k[0], j[1] + k[1])
                    if l not in old.union(new) and not (tc.map.contents[l[0]][l[1]] if 0 <= l[0] < tc.map.width and 0 <= l[1] < tc.map.height else True):
                        if l not in newer:
                            newer.add(l)
                        val[l[0]][l[1]] = max(val[l[0]][l[1]], val[j[0]][j[1]] * (1 / (5 * dist[j[0]][j[1]] + 1) if dist[j[0]][j[1]] > 1 / t else 1))
            old = old.union(new)
            new = newer
        area[-1] = min(area[-1], limit0)
    gpupup = False
    if poss[-1]:
        di = poss[-1][area.index(max(area))]
        gpupup = PowerUp(newx[-1][di], newy[-1][di]) in tc.map.powerups or PowerUp(susnewx[-1][di], susnewy[-1][di]) in tc.map.powerups
    pup = tc.myself.powerup
    supup = pup == 2 and ssuo or pup == 3 and tc.myself.speed > 1 or pup == 5 and gpupup or max(area) <= 1 and tc.myself.powerup in [2, 3, 5]
    return Command(dirs[di] if poss[-1] else None, supup)

class OurClient(TronClient):
    def get_display_name(self) -> str:
        return "JoPaSa"

    def get_color(self) -> str:
        return "#4dff52"

    def turn(self) -> Command:
        # d = random.choice([Direction.NONE]) # Direction.LEFT
        return t15(self)


if __name__ == '__main__':
    c = OurClient()
    c.run()

