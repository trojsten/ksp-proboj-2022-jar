#!/usr/bin/env python

from copy import deepcopy
import random
from sys import stderr

from common import *


class OurClient(TronClient):

    pole: List[List[bool]] = None
    DX = [0, 1, 0, -1]
    DY = [-1, 0, 1, 0]
    DS = [1, 0, -1]

    dir = {
        -1 : Direction.LEFT,
        0 : Direction.NONE,
        1 : Direction.RIGHT
    }

    def get_display_name(self) -> str:
        sys.setrecursionlimit(100000)
        return "veduci.py"

    def get_color(self) -> str:
        return f"#{random.randint(0, 255**3):06x}"

    def seg(self, x, y):
        return x >=0 and x < self.map.width and y >= 0 and y < self.map.height

    def hlupyOk(self, x, y):
        return self.seg(x, y) and self.map.contents[x][y] == False

    def ok(self, x, y):
        return self.seg(x, y) and self.pole[x][y] == False

    def getSmer(self, player):
        if player.dx == 0:
            if player.dy == 1:
                return 2
            else:
                return 0
        elif player.dx == 1:
            return 1
        else:
            return 3

    def hlupyTurn(self, usePowerUp) -> Command:
        if(self.myself.speed == 0):
            return Command(Direction.NONE, usePowerUp)

        S = self.getSmer(self.myself)


        for ds in self.DS:
            OK = True
            for i in range(1, self.myself.speed+1):

                x = self.myself.x + i*self.DX[(S+ds)%4]
                y = self.myself.y + i*self.DY[(S+ds)%4]

                if self.hlupyOk(x, y) == False:
                    OK = False

            if OK:
                # self.log(self.dir[ds])
                return Command(self.dir[ds], usePowerUp)
    
        print('penisss12313')   
    
    def najdiEnemy(self, vis, x, y):
        vis[x][y] = True

        for player in self.players:
            if player.alive:
                if player.x == x and player.y == y:
                    # self.log('enemy')
                    return 1
 
        res = 0
        for s in range(4):
            dx = self.DX[s]
            dy = self.DY[s]
            if self.seg(x+dx, y+dy) and vis[x+dx][y+dy] == False:
                res += self.najdiEnemy(vis, x+dx, y+dy)

        return res

    def value(self, x, y):
        return 1 + int((x, y) in self.map.powerups)

    def dfs(self, vis, x, y, speed=1):
        vis[x][y] = True
        res = self.value(x, y)

        for s in range(4):
            ok = True
            for i in range(1, speed):      
                dx = i*self.DX[s]
                dy = i*self.DY[s]
                if not(self.ok(x+dx, y+dy) and vis[x+dx][y+dy] == False):
                    ok = False
                    break
            dx = speed*self.DX[s]
            dy = speed*self.DY[s]
            if ok and self.ok(x+dx, y+dy) and vis[x+dx][y+dy] == False:
                res += self.dfs(vis, x+dx, y+dy, speed)

            
        return res

    
    def turn(self) -> Command:

        usePowerUp = False

        if self.myself.powerup == 2:
            usePowerUp = True
        
        if(self.myself.speed == 0):
            return Command(Direction.NONE, usePowerUp)
        
        self.pole = [x[:] for x in self.map.contents]


        for player in self.players:
            if player.alive:  
                S = self.getSmer(player)

                for ds in self.DS:
                    for i in range(1, player.speed+1):
                        x = player.x + i*self.DX[(S+ds)%4]
                        y = player.y + i*self.DY[(S+ds)%4]
                        if self.seg(x, y):
                            self.pole[x][y] = True
                        if(not self.hlupyOk(x, y)):
                            break
        
        # self.log(self.pole)

        S = self.getSmer(self.myself)
        enemaci = []
        plocha = []

        for ds in self.DS:
            vis = [x[:] for x in self.map.contents]
            for player in self.players:
                if player.alive:
                    vis[player.x][player.y] = False

            x = self.myself.x + self.DX[(S+ds)%4]
            y = self.myself.y + self.DY[(S+ds)%4]
            if self.hlupyOk(x, y):
                enemaci.append(self.najdiEnemy(vis, x, y))
            else:
                enemaci.append(0)
            # self.log(enemaci)
            # self.log(vis)


        
        for ds in self.DS: 
            vis = [x[:] for x in self.pole]
            for i in range(1, self.myself.speed):
                x = self.myself.x + i*self.DX[(S+ds)%4]
                y = self.myself.y + i*self.DY[(S+ds)%4]
                if self.seg(x, y):
                    vis[x][y] = True
            
            x = self.myself.x + self.myself.speed*self.DX[(S+ds)%4]
            y = self.myself.y + self.myself.speed*self.DY[(S+ds)%4]
            if self.ok(x, y) and vis[x][y] == False:
                plocha.append(self.dfs(vis, x, y))
            else:
                plocha.append(0)

        # self.log(plocha)

        ######
        #sprav dfs este s vacsimi rychlostami ak su enemaci
        if(sum(enemaci) != 0):
            if self.myself.powerup == 4:
                usePowerUp = True

            
            speed = self.myself.speed
            value = 2
            
            for i in range(3):
                for s in range(3):
                    ds = self.DS[s]
                    vis = [x[:] for x in self.pole]
                    for i in range(1, speed):
                        x = self.myself.x + i*self.DX[(S+ds)%4]
                        y = self.myself.y + i*self.DY[(S+ds)%4]
                        if self.seg(x, y):
                            vis[x][y] = True
                
                    x = self.myself.x + speed*self.DX[(S+ds)%4]
                    y = self.myself.y + speed*self.DY[(S+ds)%4]
                    if self.ok(x, y) and vis[x][y] == False:
                        plocha[s] += self.dfs(vis, x, y, speed)*value

                speed *= 2
                value /= 2

        ### nie su enemy
        else:
            if self.myself.powerup == 3:
                usePowerUp = True  
    
        ######

        if max(plocha) < 3*self.myself.speed and self.myself.powerup == 5:
            usePowerUp = True



        # self.log(plocha)

        for j in range(len(plocha)):
            ds = self.DS[j]
            for i in range(1, self.myself.speed+1):
                x = self.myself.x + i*self.DX[(S+ds)%4]
                y = self.myself.y + i*self.DY[(S+ds)%4]
                if not self.ok(x, y):
                    plocha[j] = 0
        

        # self.log(plocha)

        if(max(plocha) == 0):
            return self.hlupyTurn(usePowerUp)
        

        for i in range(3):
            plocha[i] /= (enemaci[i]+1)


        for i in range(len(plocha)):
            if plocha[i] == max(plocha):
                # self.log(self.dir[self.DS[i]])
                return Command(self.dir[self.DS[i]], usePowerUp)


        


if __name__ == '__main__':
    c = OurClient()
    c.run()
