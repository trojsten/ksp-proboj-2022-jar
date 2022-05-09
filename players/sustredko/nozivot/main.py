#!/usr/bin/env python3
from typing import List

import random
import threading
import queue
import time
from collections import deque
import logging
from common import *
from utils import *

TIME_OF_ROUND = 1.0
THRESHOLD = 0.25

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
round_event = threading.Event()
coms = queue.Queue()
coms_back = queue.Queue()

class OurClient(TronClient):
    round = 0
    natural = None
    tilemap: List[List[Tile]] = None
    clear = False # false - clear plane, true - filled plane
    potential = [0, 0, 0, 0]
    decision = [0, 0, 0, 0]
    snapshot: LepsiaMapa = None
    kompaktny = False
    vek = -1

    def get_display_name(self) -> str:
        name = "rektor"
        shuffle = False

        if not shuffle: return name
        name = list(name)
        random.shuffle(name)
        return "".join(name)

    def get_color(self) -> str:
        return "#ffff00"
        return f"#{random.randrange(0, 256**3):06x}"

    def turn(self) -> Command:
        global round_event
        # Signal round start to thread
        round_event.set()
        timer = time.time()

        OurClient.vek -= 1
        assert OurClient.vek

        x, y, dx, dy = self.myself.x, self.myself.y, self.myself.dx*self.myself.speed, self.myself.dy*self.myself.speed
        ddx, ddy = (dx>0)-(dx<0), (dy>0)-(dy<0)
        map = LepsiaMapa(self.map)
        if OurClient.natural is None:
            OurClient.natural = map.copy().bezhracov(self.myself, self.players)
        if OurClient.tilemap is None:
            OurClient.tilemap = [[Tile((_x, _y)) for _x in range(map.map.width)] for _y in range(map.map.height)]
        map.hraci(self.myself, self.players)

        def spravnysmer(x,y,ddx,ddy):
            dirs = [None, None, None]
            dist = 0
            while None in dirs:
                dist += 1
                if dirs[0] is None and map[x+ddx*dist, y+ddy*dist]: dirs[0] = dist-1
                if dirs[1] is None and map[x+ddy*dist, y-ddx*dist]: dirs[1] = dist-1
                if dirs[2] is None and map[x-ddy*dist, y+ddx*dist]: dirs[2] = dist-1
            return dirs

        dirs = spravnysmer(x,y,ddx,ddy)

        volnevolne = [-1, -1, -1]

        volne = max(dirs)
        d = (Direction.NONE, Direction.LEFT, Direction.RIGHT)[dirs.index(volne)]

        stuck = volne < 2*max(abs(dx), abs(dy))
        p = False

        if stuck and (self.myself.powerup in (PowerUpType.CLEAN, PowerUpType.STOP_ME)):
            p = True
            map = OurClient.natural.copy().hraci(self.myself, self.players)
            dirs = spravnysmer(x, y, ddx, ddy)
            d = [Direction.NONE, Direction.LEFT, Direction.RIGHT][dirs.index(max(dirs))]
        elif self.myself.powerup == PowerUpType.SPEED_OTHERS:
            p = True
        elif OurClient.kompaktny and self.myself.powerup == PowerUpType.STOP_ME:
            p = True

        self.log(dirs, d, volnevolne)
        self.log(map)

        # Send data to thread
        coms.put((self.round, map, self))
        self.round += 1

        while True:
            try:
                rec = coms_back.get(False)
                if (rec == "done"):
                    if dx == dy == 0:
                        return Command(Direction.NONE, p)
                    dirs = spravnysmer(x, y, ddx, ddy)
                    i = Vector.normals.index(Vector((dx/abs(dx) if dx!=0 else 0, dy/abs(dy) if dy!=0 else 0)))
                    potential = [
                        OurClient.potential[i][0],
                        OurClient.potential[i-1][0],
                        OurClient.potential[(i+1)%4][0]
                    ]
                    najlepsi = (-1, -1, -1)
                    for i in (1, 0, -1):
                        if dirs[i] >= self.myself.speed:
                            tiebreaker = i if OurClient.kompaktny else dirs[i]
                            najlepsi = max(najlepsi, (potential[i], tiebreaker, i))
                    d = (Direction.NONE, Direction.LEFT, Direction.RIGHT)[najlepsi[-1]]
                    OurClient.kompaktny = not OurClient.potential[najlepsi[-1]][1]
                    return Command(d, p)
            except queue.Empty: pass
            if (time.time() - timer > TIME_OF_ROUND-THRESHOLD): return Command(d, p)

bfs_visited = set()
bfs_queue = deque()
def execute_bfs(index, map, round, coords, client):
    val = 0
    players = set()
    tile = Vector(coords)
    bfs_queue.append((tile, client.myself.speed_reset_time))
    bfs_visited.add(tile)

    while bfs_queue:
        target, timer = bfs_queue.popleft()
        if map[target[0], target[1]] not in ("!", False):
            continue
        for novy in Vector.normals:
            try:
                failed = False
                speed = client.myself.speed if timer > 0 else 1
                if speed == 0: speed = 1
                for i in range(1, 1+speed):
                    b = target+novy*i
                    if map[b[0],b[1]] not in ("!", False):
                        if type(map[b[0], b[1]]) == int: players.add(map[b[0], b[1]])
                        failed = True
                        break
                if failed: continue
                for i in range(1, 1+speed):
                    b = target+novy*i
                    if (b not in bfs_visited):
                        if map[b[0], b[1]] in ("!", False):
                            # Add to visited and tie
                            bfs_queue.append((b, timer-1))
                            bfs_visited.add(b)
                            val+=1
                            OurClient.tilemap[b[0]][b[1]].linkers[index].parents.add(OurClient.tilemap[(b-novy)[0]][(b-novy)[1]])
                            OurClient.tilemap[(b-novy)[0]][(b-novy)[1]].linkers[index].successors.add(OurClient.tilemap[b[0]][b[1]])
                            OurClient.tilemap[b[0]][b[1]].lastEdit = round
                        else:
                            break
                    else:
                        OurClient.tilemap[b[0]][b[1]].linkers[index].parents.add(OurClient.tilemap[(b-novy)[0]][(b-novy)[1]])
                        break


            except IndexError: pass

    print(f"Finished bfs {index}", file=sys.stderr)
    print(val, file=sys.stderr)
    bfs_visited.clear()
    return (val, len(players))

def timeout_safe(rEvent):
    logging.info("Thread: starting")
    while True:
        while not rEvent.is_set():
            pass
        if (rEvent.wait()):
            logging.info("New round registered - attempting to get game data")

            OurClient.potential = [(0,0), (0,0), (0, 0), (0, 0)]
            # if (OurClient.snapshot is None):
            #     OurClient.snapshot = OurClient.natural

            # diff: list(Vector)

            round, map, client = coms.get()
            # if not OurClient.clear:
            # Create snapshot for comparison
            # OurClient.snapshot = map.copy()
            # Start search algorithm
            player = Vector((client.myself.x, client.myself.y))
            for a in range(len(Vector.normals)):
                dir = Vector.normals[a]
                failed = False
                speed = client.myself.speed
                if speed == 0: speed = 1
                for i in range(1, 1+speed):
                    b = player+dir*i
                    if map[b[0],b[1]] is not False:
                        failed = True
                        break
                if failed: continue
                for l in range(1, 1+speed):
                # Add to visited and tie
                    bfs_visited.add(b)
                try:
                    OurClient.tilemap[b[0]][b[1]].linkers[a].parents.add(OurClient.tilemap[(b-dir)[0]][(b-dir)[1]])
                    OurClient.tilemap[(b-dir)[0]][(b-dir)[1]].linkers[a].successors.add(OurClient.tilemap[b[0]][b[1]])
                    OurClient.tilemap[dir[0]][dir[1]].root = True
                    OurClient.tilemap[dir[0]][dir[1]].lastEdit = round
                except IndexError: pass
                OurClient.potential[a] = execute_bfs(a, map, round, player+dir*speed, client)
                #print_bfs_data(a, OurClient.tilemap)
            client.log(OurClient.potential)

            #execute_bfs(-1, map, round, player, client)


        # else:
            #     # TODO: Handle difference computation

            #     # Search for new path / try to rescue lost nodes
            #     client.

            #     # Destroy unaccesible routes
            #     for i in diff:
            #         OurClient.tilemap[i[0]][i[1]].destroy()

            #     logging.info("Applied corrections")
            #     print_bfs_data(a, OurClient.tilemap)
            #     # Create snapshot for comparison
            #     OurClient.snapshot = map.copy()
            #     pass
        coms_back.put("done")
        rEvent.clear()


if __name__ == '__main__':
    #kompaktny = random.randrange(0, 4)
    #OurClient.kompaktny = not bool(kompaktny)
    c = OurClient()

    # Setup Threading
    x = threading.Thread(target=timeout_safe, args=[round_event])
    x.start()

    c.run()
