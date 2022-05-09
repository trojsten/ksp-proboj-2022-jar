def t12(tc: TronClient):
    limit0 = 200
    limit1 = 30
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
            old = set()
            t = 0
            while new and len(old) < limit1:
                t += 1
                newer = set()
                for j in new:
                    dist[j[0]][j[1]] = max(dist[j[0]][j[1]], 1 / t)
                    for k in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        if (j[0] + k[0], j[1] + k[1]) not in old.union(new.union(newer)) and not (tc.map.contents[j[0] + k[0]][j[1] + k[1]] if 0 <= j[0] + k[0] < tc.map.width and 0 <= j[1] + k[1] < tc.map.height else True):
                            newer.add((j[0] + k[0], j[1] + k[1]))
                old = old.union(new)
                new = newer
    area = []
    for i in poss[-1]:
        area.append(0)
        new = {(newx[-1][i], newy[-1][i])}
        old = set()
        t = 1
        while new and len(old) < limit0:
            t += 1
            newer = set()
            for j in new:
                area[-1] += 1 / (dist[j[0]][j[1]] + 1) if dist[j[0]][j[1]] > 1 / t else 1
                for k in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    if (j[0] + k[0], j[1] + k[1]) not in old.union(new.union(newer)) and not (tc.map.contents[j[0] + k[0]][j[1] + k[1]] if 0 <= j[0] + k[0] < tc.map.width and 0 <= j[1] + k[1] < tc.map.height else True):
                        newer.add((j[0] + k[0], j[1] + k[1]))
            old = old.union(new)
            new = newer
        area[-1] = min(area[-1], limit0)
    if poss[-1]:
        di = poss[-1][area.index(max(area))]
        gpup = PowerUp(newx[-1][di], newy[-1][di]) in tc.map.powerups or PowerUp(susnewx[-1][di], susnewy[-1][di]) in tc.map.powerups
    return Command(dirs[di] if poss[-1] else None, tc.myself.powerup == 5 and gpup or max(area) <= 1 and tc.myself.powerup in [2, 3])
def t11(tc: TronClient):
    limit0 = 100
    limit1 = 0
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
            old = set()
            t = 0
            while new and len(old) < limit1:
                t += 1
                newer = set()
                for j in new:
                    dist[j[0]][j[1]] += 1 / t
                    for k in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        if (j[0] + k[0], j[1] + k[1]) not in old.union(new.union(newer)) and not (tc.map.contents[j[0] + k[0]][j[1] + k[1]] if 0 <= j[0] + k[0] < tc.map.width and 0 <= j[1] + k[1] < tc.map.height else True):
                            newer.add((j[0] + k[0], j[1] + k[1]))
                old = old.union(new)
                new = newer
    area = []
    for i in poss[-1]:
        area.append(0)
        new = {(newx[-1][i], newy[-1][i])}
        old = set()
        while new and len(old) < limit0:
            newer = set()
            for j in new:
                area[-1] += 1 / (dist[j[0]][j[1]] + 1)
                for k in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    if (j[0] + k[0], j[1] + k[1]) not in old.union(new.union(newer)) and not (tc.map.contents[j[0] + k[0]][j[1] + k[1]] if 0 <= j[0] + k[0] < tc.map.width and 0 <= j[1] + k[1] < tc.map.height else True):
                        newer.add((j[0] + k[0], j[1] + k[1]))
            old = old.union(new)
            new = newer
        area[-1] = min(area[-1], limit0)
    if poss[-1]:
        di = poss[-1][area.index(max(area))]
        gpup = PowerUp(newx[-1][di], newy[-1][di]) in tc.map.powerups or PowerUp(susnewx[-1][di], susnewy[-1][di]) in tc.map.powerups
    return Command(dirs[di] if poss[-1] else None, tc.myself.powerup == 5 and gpup or max(area) <= 1 and tc.myself.powerup in [2, 3])

def t8(tc: TronClient):
    dirs = [Direction.LEFT, Direction.NONE, Direction.RIGHT]
    poss = []
    newx = [tc.myself.x + tc.myself.speed * tc.myself.dy, tc.myself.x + tc.myself.speed * tc.myself.dx, tc.myself.x - tc.myself.speed * tc.myself.dy]
    newy = [tc.myself.y - tc.myself.speed * tc.myself.dx, tc.myself.y + tc.myself.speed * tc.myself.dy, tc.myself.y + tc.myself.speed * tc.myself.dx]
    susnewx = [tc.myself.x + tc.myself.dy, tc.myself.x + tc.myself.dx, tc.myself.x - tc.myself.dy]
    susnewy = [tc.myself.y - tc.myself.dx, tc.myself.y + tc.myself.dy, tc.myself.y + tc.myself.dx]
    for i in range(3):
        if not (tc.map.contents[newx[i]][newy[i]] or tc.map.contents[susnewx[i]][susnewy[i]] if (0 <= newx[i] < tc.map.width and 0 <= newy[i] < tc.map.height) else True):
            poss.append(i)
    area = []
    for i in poss:
        new = {(newx[i], newy[i])}
        old = set()
        while new and len(old) < 200:
            newer = set()
            for j in new:
                for k in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    if (j[0] + k[0], j[1] + k[1]) not in old.union(new.union(newer)) and not (tc.map.contents[j[0] + k[0]][j[1] + k[1]] if 0 <= j[0] + k[0] < tc.map.width and 0 <= j[1] + k[1] < tc.map.height else True):
                        newer.add((j[0] + k[0], j[1] + k[1]))
            old = old.union(new)
            new = newer
        area.append(min(len(old), 200))
    if poss:
        di = poss[area.index(max(area))]
        gpup = PowerUp(newx[di], newy[di]) in tc.map.powerups or PowerUp(susnewx[di], susnewy[di]) in tc.map.powerups
    return Command(dirs[di] if poss else None, tc.myself.powerup == 5 and gpup or max(area) <= 1 and tc.myself.powerup in [2, 3])


    limit0 = 100
    limit1 = 0
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
    area = []
    for i in poss[-1]:
        area.append(0)
        new = {(newx[-1][i], newy[-1][i])}
        old = set()
        while new and len(old) < limit0:
            newer = set()
            for j in new:
                area[-1] += 1
                for k in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    if (j[0] + k[0], j[1] + k[1]) not in old.union(new.union(newer)) and not (tc.map.contents[j[0] + k[0]][j[1] + k[1]] if 0 <= j[0] + k[0] < tc.map.width and 0 <= j[1] + k[1] < tc.map.height else True):
                        newer.add((j[0] + k[0], j[1] + k[1]))
            old = old.union(new)
            new = newer
        area[-1] = min(area[-1], limit0)
    if poss[-1]:
        di = poss[-1][area.index(max(area))]
        gpup = PowerUp(newx[-1][di], newy[-1][di]) in tc.map.powerups or PowerUp(susnewx[-1][di], susnewy[-1][di]) in tc.map.powerups
    return Command(dirs[di] if poss[-1] else None, tc.myself.powerup == 5 and gpup or max(area) <= 1 and tc.myself.powerup in [2, 3])

def t10_(tc: TronClient):
    limit0 = 100
    limit1 = 0
    dirs = [Direction.LEFT, Direction.NONE, Direction.RIGHT]
    poss = []
    newx = [tc.myself.x + tc.myself.speed * tc.myself.dy, tc.myself.x + tc.myself.speed * tc.myself.dx, tc.myself.x - tc.myself.speed * tc.myself.dy]
    newy = [tc.myself.y - tc.myself.speed * tc.myself.dx, tc.myself.y + tc.myself.speed * tc.myself.dy, tc.myself.y + tc.myself.speed * tc.myself.dx]
    susnewx = [tc.myself.x + tc.myself.dy, tc.myself.x + tc.myself.dx, tc.myself.x - tc.myself.dy]
    susnewy = [tc.myself.y - tc.myself.dx, tc.myself.y + tc.myself.dy, tc.myself.y + tc.myself.dx]
    for i in range(3):
        if not (tc.map.contents[newx[i]][newy[i]] or tc.map.contents[susnewx[i]][susnewy[i]] if (0 <= newx[i] < tc.map.width and 0 <= newy[i] < tc.map.height) else True):
            poss.append(i)
    area = []
    for i in poss:
        area.append(0)
        new = {(newx[i], newy[i])}
        old = set()
        while new and len(old) < limit0:
            newer = set()
            for j in new:
                area[-1] += 1
                for k in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    if (j[0] + k[0], j[1] + k[1]) not in old.union(new.union(newer)) and not (tc.map.contents[j[0] + k[0]][j[1] + k[1]] if 0 <= j[0] + k[0] < tc.map.width and 0 <= j[1] + k[1] < tc.map.height else True):
                        newer.add((j[0] + k[0], j[1] + k[1]))
            old = old.union(new)
            new = newer
        area[-1] = min(area[-1], limit0)
    if poss:
        di = poss[area.index(max(area))]
        gpup = PowerUp(newx[di], newy[di]) in tc.map.powerups or PowerUp(susnewx[di], susnewy[di]) in tc.map.powerups
    return Command(dirs[di] if poss else None, tc.myself.powerup == 5 and gpup or max(area) <= 1 and tc.myself.powerup in [2, 3])

def t13(tc: TronClient):
    limit0 = 200
    limit1 = 30
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
            old = set()
            t = 0
            while new and len(old) < limit1:
                t += 1
                newer = set()
                for j in new:
                    dist[j[0]][j[1]] = max(dist[j[0]][j[1]], 1 / t)
                    for k in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        if (j[0] + k[0], j[1] + k[1]) not in old.union(new.union(newer)) and not (tc.map.contents[j[0] + k[0]][j[1] + k[1]] if 0 <= j[0] + k[0] < tc.map.width and 0 <= j[1] + k[1] < tc.map.height else True):
                            newer.add((j[0] + k[0], j[1] + k[1]))
                old = old.union(new)
                new = newer
    area = []
    for i in poss[-1]:
        area.append(0)
        new = {(newx[-1][i], newy[-1][i], 1)}
        old = set()
        val = [tc.map.height * [0] for _ in range(tc.map.width)]
        t = 1
        while new and len(old) < limit0:
            t += 1
            newer = set()
            for j in new:
                area[-1] += val[j[0]][j[1]]
                for k in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    l = (j[0] + k[0], j[1] + k[1])
                    if l not in old.union(new) and not (tc.map.contents[l[0]][l[1]] if 0 <= l[0] < tc.map.width and 0 <= l[1] < tc.map.height else True):
                        if l not in newer:
                            newer.add(l)
                        val[l[0]][l[1]] = max(val[l[0]][l[1]], val[j[0]][j[1]] * (1 / (5 * dist[j[0]][j[1]] + 1) if dist[j[0]][j[1]] > 1 / t else 1))
            old = old.union(new)
            new = newer
        area[-1] = min(area[-1], limit0)
    if poss[-1]:
        di = poss[-1][area.index(max(area))]
        gpup = PowerUp(newx[-1][di], newy[-1][di]) in tc.map.powerups or PowerUp(susnewx[-1][di], susnewy[-1][di]) in tc.map.powerups
    return Command(dirs[di] if poss[-1] else None, tc.myself.powerup == 5 and gpup or max(area) <= 1 and tc.myself.powerup in [2, 3])

def t14(tc: TronClient):
    limit0 = 200
    limit1 = 30
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
            old = set()
            t = 0
            while new and len(old) < limit1:
                t += 1
                newer = set()
                for j in new:
                    dist[j[0]][j[1]] = max(dist[j[0]][j[1]], 1 / t)
                    for k in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        if (j[0] + k[0], j[1] + k[1]) not in old.union(new.union(newer)) and not (tc.map.contents[j[0] + k[0]][j[1] + k[1]] if 0 <= j[0] + k[0] < tc.map.width and 0 <= j[1] + k[1] < tc.map.height else True):
                            newer.add((j[0] + k[0], j[1] + k[1]))
                old = old.union(new)
                new = newer
    area = []
    for i in poss[-1]:
        area.append(0)
        new = {(newx[-1][i], newy[-1][i], 1)}
        old = set()
        val = [tc.map.height * [0] for _ in range(tc.map.width)]
        val[newx[-1][i]][newy[-1][i]] = 1
        t = 0
        while new and len(old) < limit0:
            t += 1
            newer = set()
            for j in new:
                area[-1] += val[j[0]][j[1]]
                for k in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    l = (j[0] + k[0], j[1] + k[1])
                    if l not in old.union(new) and not (tc.map.contents[l[0]][l[1]] if 0 <= l[0] < tc.map.width and 0 <= l[1] < tc.map.height else True):
                        if l not in newer:
                            newer.add(l)
                        val[l[0]][l[1]] = max(val[l[0]][l[1]], val[j[0]][j[1]] * (1 / (5 * dist[j[0]][j[1]] + 1) if dist[j[0]][j[1]] > 1 / t else 1))
            old = old.union(new)
            new = newer
        area[-1] = min(area[-1], limit0)
    if poss[-1]:
        di = poss[-1][area.index(max(area))]
        gpup = PowerUp(newx[-1][di], newy[-1][di]) in tc.map.powerups or PowerUp(susnewx[-1][di], susnewy[-1][di]) in tc.map.powerups
    return Command(dirs[di] if poss[-1] else None, tc.myself.powerup == 5 and gpup or max(area) <= 1 and tc.myself.powerup in [2, 3])

def t15(tc: TronClient):
    limit0 = 150
    limit1 = limit0 // (len(tc.players) + 1)
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
            old = set()
            t = 0
            while new and len(old) < limit1:
                t += 1
                newer = set()
                for j in new:
                    dist[j[0]][j[1]] = max(dist[j[0]][j[1]], 1 / t)
                    for k in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        if (j[0] + k[0], j[1] + k[1]) not in old.union(new.union(newer)) and not (tc.map.contents[j[0] + k[0]][j[1] + k[1]] if 0 <= j[0] + k[0] < tc.map.width and 0 <= j[1] + k[1] < tc.map.height else True):
                            newer.add((j[0] + k[0], j[1] + k[1]))
                old = old.union(new)
                new = newer
    area = []
    for i in poss[-1]:
        area.append(0)
        new = {(newx[-1][i], newy[-1][i], 1)}
        old = set()
        val = [tc.map.height * [0] for _ in range(tc.map.width)]
        val[newx[-1][i]][newy[-1][i]] = 1
        t = 0
        while new and len(old) < limit0:
            t += 1
            newer = set()
            for j in new:
                area[-1] += val[j[0]][j[1]]
                for k in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    l = (j[0] + k[0], j[1] + k[1])
                    if l not in old.union(new) and not (tc.map.contents[l[0]][l[1]] if 0 <= l[0] < tc.map.width and 0 <= l[1] < tc.map.height else True):
                        if l not in newer:
                            newer.add(l)
                        val[l[0]][l[1]] = max(val[l[0]][l[1]], val[j[0]][j[1]] * (1 / (5 * dist[j[0]][j[1]] + 1) if dist[j[0]][j[1]] > 1 / t else 1))
            old = old.union(new)
            new = newer
        area[-1] = min(area[-1], limit0)
    if poss[-1]:
        di = poss[-1][area.index(max(area))]
        gpup = PowerUp(newx[-1][di], newy[-1][di]) in tc.map.powerups or PowerUp(susnewx[-1][di], susnewy[-1][di]) in tc.map.powerups
    return Command(dirs[di] if poss[-1] else None, tc.myself.powerup == 5 and gpup or max(area) <= 1 and tc.myself.powerup in [2, 3])
