#!/usr/bin/env python

from lib2to3.pgen2 import driver
import random

from common import *

def inside(map:Map,x, y):
    return map.height > y >= 0 and map.width > x >= 0

def issafe(map:Map,x, y, players:List[Player]):
    if not inside(map,x,y):
        return False
    for e in players:
        if x == e.x+e.dx and y == e.y+e.dy:
            return False
    return not map.contents[x][y]

def whatis(walls:Map,x,y,map:Map, log):
    if not inside(map,x,y):
        log(x, y, 2)
        return 2
    if walls.contents[x][y]:
        log(x, y, 1)
        return 1
    if map.contents[x][y]:
        log(x, y, 3)
        return 3
    log(x, y, 0)
    return 0


def strmap(map:Map):
    riadky = [""]*map.height
    for s in map.contents:
        for i in range(len(s)):
            riadky[i] += "#" if s[i] else "."
    return "\n".join(riadky)

susx = [1, 0,-1, 0]
susy = [0, 1, 0,-1]

def bfs(map:Map, x, y, players:List[Player]):
    if not issafe(map, x, y, players):
        return -1, 0

    pcount = 0
    
    vis = [[False for s in range(map.height)] for r in range(map.width)]
    q = []
    q.append(((x, y), 0))

    count = 0

    while len(q) != 0:
        cur, depth = q[0]
        if not vis[cur[0]][cur[1]]:
            count += 1
            vis[cur[0]][cur[1]] = True
            for i in range(4):
                sx = cur[0]+susx[i]
                sy = cur[1]+susy[i]
                for p in players:
                    if sx == p.x and sy == p.y:
                        pcount += 1
                        break
                if issafe(map, sx, sy, players):
                    q.append(((sx, sy), depth+1))

        q.pop(0)

    return count,pcount



right = {
    (-1, 0): (0, -1),
    (1, 0): (0, 1),
    (0, -1): (1, 0),
    (0, 1): (-1, 0)
}
left = {
    (-1, 0): (0, 1),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
    (0, 1): (1, 0)
}

def right_pos(player:Player, speed=1):
        dxr, dyr = right[(player.dx, player.dy)]
        return player.x+dxr*speed, player.y+dyr*speed

def left_pos(player:Player, speed=1):
        dxl, dyl =  left[(player.dx, player.dy)]
        return player.x+dxl*speed, player.y+dyl*speed 

def front_pos(player:Player, speed=1):
        dx, dy = player.dx, player.dy
        return player.x+dx*speed, player.y+dy*speed

class OurClient(TronClient):

    def __init__(self):
        super().__init__()
        self.color = "#FFA500" #%02x%02x%02x"%(random.randint(0, 255),random.randint(0, 255), random.randint(0, 255))
        self.log(self.color)
        self.walls = None
        self.dir = Direction.RIGHT

    def get_display_name(self) -> str:
        return "Trubka"

    def get_color(self) -> str:
        return self.color

    def turn(self) -> Command:
        if self.walls is None:
            self.log("Loading walls")
            self.walls = self.map.clone()
            for p in self.players:
                self.walls.contents[p.x][p.y] = False
            self.walls.contents[self.myself.x][self.myself.y] = False
        
        use = False
        if self.myself.powerup == PowerUpType.SPEED_OTHERS:
            use = True
        players = list(filter(lambda p: p.alive, self.players))
        playercoords = [(players[i].x, players[i].y) for i in range(len(players))]

        left = left_pos(self.myself)
        front = front_pos(self.myself)
        right = right_pos(self.myself)
        left_size, left_players = bfs(self.map, left[0], left[1], players)
        front_size, right_players = bfs(self.map, front[0], front[1], players)
        right_size, front_players = bfs(self.map, right[0], right[1], players)

        if self.myself.speed == 0:
            return Command(Direction.NONE, use)

        if max(left_size, front_size, right_size) == -1:
            right_obj = whatis(self.walls, right[0], right[1], self.map, self.log)
            front_obj = whatis(self.walls, front[0], front[1], self.map, self.log)
            left_obj = whatis(self.walls, left[0], left[1], self.map, self.log)
            for i in range(4):
                if self.dir == Direction.RIGHT:
                    if right_obj == i:
                        self.dir = Direction.RIGHT
                        return Command(Direction.RIGHT, use)
                else:
                    if left_obj == i:
                        self.dir = Direction.LEFT
                        return Command(Direction.LEFT,  use)

                if front_obj == i:
                    return Command(Direction.NONE, use)

                if self.dir == Direction.RIGHT:
                    if left_obj == i:
                        self.dir = Direction.LEFT
                        return Command(Direction.LEFT,  use)
                else:
                    if right_obj == i:
                        self.dir = Direction.RIGHT
                        return Command(Direction.RIGHT, use)
            return Command(Direction.NONE, use)
        
        def rightF():
            nonlocal self,use,left,left_players,left_size,front,front_players,front_size,right,right_players,right_size
            if self.myself.powerup == PowerUpType.CLEAN and (right_size < 5 or
                                    PowerUp(right[0], right[1]) in self.map.powerups):
                use = True
            if right_players == 0:
                if self.myself.powerup == PowerUpType.STOP_ME:
                    use = True
            else:
                if self.myself.powerup == PowerUpType.STOP_OTHERS:
                    use = True
            self.dir = Direction.RIGHT
            return Command(Direction.RIGHT, use)
        
        def frontF():
            nonlocal self,use,left,left_players,left_size,front,front_players,front_size,right,right_players,right_size
            if self.myself.powerup == PowerUpType.CLEAN and (front_size < 5 or
                                        PowerUp(front[0], front[1]) in self.map.powerups):
                use = True
            if front_players == 0:
                if self.myself.powerup == PowerUpType.STOP_ME:
                    use = True
            else:
                if self.myself.powerup == PowerUpType.STOP_OTHERS:
                    use = True
            return Command(Direction.NONE, use)

        def leftF():
            nonlocal self,use,left,left_players,left_size,front,front_players,front_size,right,right_players,right_size
            if self.myself.powerup == PowerUpType.CLEAN and (left_size < 5 or
                                        PowerUp(left[0], left[1]) in self.map.powerups):
                use = True
            if left_players == 0:
                if self.myself.powerup == PowerUpType.STOP_ME:
                    use = True
            else:
                if self.myself.powerup == PowerUpType.STOP_OTHERS:
                    use = True
            self.dir = Direction.LEFT
            return Command(Direction.LEFT, use)

        if self.myself.speed == 1:
            if self.dir == Direction.RIGHT:
                if (right_size == max(left_size, front_size, right_size)):
                    return rightF()
                if (front_size == max(left_size, front_size, right_size)):
                    return frontF()
                if (left_size == max(left_size, front_size, right_size)):
                    return leftF()
            else:
                if (left_size == max(left_size, front_size, right_size)):
                    return leftF()
                if (front_size == max(left_size, front_size, right_size)):
                    return frontF()
                if (right_size == max(left_size, front_size, right_size)):
                    return rightF()
        else:
            if not issafe(self.map, left_pos(self.myself, self.myself.speed)[0],
                    left_pos(self.myself, 2)[1], players):
                left_size = -1
            if not issafe(self.map, front_pos(self.myself, self.myself.speed)[0],
                    front_pos(self.myself, 2)[1], players):
                front_size = -1
            if not issafe(self.map, right_pos(self.myself, self.myself.speed)[0],
                    right_pos(self.myself, 2)[1], players):
                right_size = -1

            if self.dir == Direction.RIGHT:
                if (right_size == max(left_size, front_size, right_size)):
                    self.dir = Direction.RIGHT
                    return Command(Direction.RIGHT, use)
                if (front_size == max(left_size, front_size, right_size)):
                    return Command(Direction.NONE, use)
                if (left_size == max(left_size, front_size, right_size)):
                    self.dir = Direction.LEFT
                    return Command(Direction.LEFT, use)
            else:
                if (left_size == max(left_size, front_size, right_size)):
                    self.dir = Direction.LEFT
                    return Command(Direction.LEFT, use)
                if (front_size == max(left_size, front_size, right_size)):
                    return Command(Direction.NONE, use)
                if (right_size == max(left_size, front_size, right_size)):
                    self.dir = Direction.RIGHT
                    return Command(Direction.RIGHT, use)

        self.log("code dumb")
        self.dir = Direction.RIGHT
        return Command(Direction.RIGHT, use)



if __name__ == '__main__':
    c = OurClient()
    c.run()
