#!/usr/bin/env python

import random
import sys
from common import *
sys.setrecursionlimit(10**6)

class OurClient(TronClient):
    d = 96
    pouzitPowerup = False
    predoslaMapa = -1
    zablokovane = []
    polickoLavo = [0,0]
    polickoPravo = [0,0]
    polickoPredu = [0,0]
    def get_display_name(self) -> str:
        return "MVB_nikdy_nezomiera"

    def get_color(self) -> str:
        return "#00ffff"
    
    def powerupy(self):
        if self.myself.powerup == PowerUpType.SPEED_OTHERS or self.myself.powerup == PowerUpType.STOP_ME or self.myself.powerup == PowerUpType.CLEAN:
            self.pouzitPowerup = True
        else:
            self.pouzitPowerup = False

    def susedia(self,policko):
        susedia = []
        r = 1#self.myself.speed
        if 0 <= policko[0]+r < self.map.width:
            susedia.append([policko[0]+r,policko[1]])
        if 0 <= policko[0]-r < self.map.width:
            susedia.append([policko[0]-r,policko[1]])
        if 0 <= policko[1]+r < self.map.height:
            susedia.append([policko[0],policko[1]+r])
        if 0 <= policko[1]-r < self.map.height:
            susedia.append([policko[0],policko[1]-r])
        return susedia

    def dfs(self,zaciatok):
        if self.jeStena(zaciatok[0], zaciatok[1]):
            return -1
        self.navstivene = []
        for i in range(self.map.width):
            self.navstivene.append([False]*self.map.height)
        self.pocet = 0
        def rekurzia(policko):
            # self.log(policko,self.pocet)
            self.pocet += 1
            self.navstivene[policko[0]][policko[1]] = True
            for sused in self.susedia(policko):
                if self.map.contents[sused[0]][sused[1]] == False and sused not in self.zablokovane:
                    if self.navstivene[sused[0]][sused[1]] == False:
                        rekurzia(sused)
            return

        rekurzia(zaciatok)
        return self.pocet

    def jeStena(self,x,y,predosla=False):
        if predosla == True:
            mapa = self.predoslaMapa.copy()
        else:
            mapa = self.map.contents.copy()
        if 0 <= x < self.map.width and 0 <= y < self.map.height:
            if mapa[x][y]:
                return True
            else:
                return False
        else:
            return True
    
    def vlavoDFS(self):
        x,y = 0,0
        if self.myself.dx == 1:
            y = -1
        if self.myself.dx == -1:
            y = 1
        if self.myself.dy == 1:
            x = 1
        if self.myself.dy == -1:
            x = -1
        x0,y0 = x,y
        for i in range(1,self.myself.speed+1):
            x,y = x0*i,y0*i
            if self.jeStena(self.myself.x+x, self.myself.y+y):
                return -1
        # self.log("x,y,vlavo",x,y)
        self.polickoLavo = [self.myself.x+x,self.myself.y+y]
        return self.dfs([self.myself.x+x,self.myself.y+y])

    def vpravoDFS(self):
        x,y = 0,0
        if self.myself.dx == 1:
            y = 1
        if self.myself.dx == -1:
            y = -1
        if self.myself.dy == 1:
            x = -1
        if self.myself.dy == -1:
            x = 1
            # self.log("x,y,vpravo",x,y)
        x0,y0 = x,y
        for i in range(1,self.myself.speed+1):
            x,y = x0*i,y0*i
            if self.jeStena(self.myself.x+x, self.myself.y+y):
                return -1
        self.polickoPravo = [self.myself.x+x,self.myself.y+y]
        return self.dfs([self.myself.x+x,self.myself.y+y])

    def vpreduDFS(self):
        x0,y0 = self.myself.dx,self.myself.dy
        x,y=x0,y0
        for i in range(1,self.myself.speed+1):
            x,y = x0*i,y0*i
            if self.jeStena(self.myself.x+x, self.myself.y+y):
                return -1
        self.polickoPredu = [self.myself.x+x,self.myself.y+y]
        return self.dfs([self.myself.x+x,self.myself.y+y])
        # for i in range(1,self.myself.speed):
        #     x,y = x0*i,y0*i
        #     self.zablokovane.append([x,y])

    def vpreduStena(self,x,y,kolko):
        return self.jeStena(x+kolko*self.myself.dx,y+kolko*self.myself.dy)

    def stena(self):
        lavo = self.vlavoDFS()
        pravo = self.vpravoDFS()
        # self.log("lavo, pravo:",lavo,pravo)
        if lavo > pravo:
            self.d = Direction.LEFT
        else:
            self.d = Direction.RIGHT
        # self.d = Direction.LEFT
        # if self.vlavoJeStena():
        #     self.d = Direction.RIGHT
        # elif self.vpravoJeStena():
        #     self.d = Direction.LEFT
        
    def jeHlava(self,x,y):
        if self.predoslaMapa == -1:
            return False
        if self.jeStena(x,y) == True and self.jeStena(x,y,predosla=True) == False:
            return True
        return False

    def nezomrietNavzajom(self):
        if self.myself.speed != 1:
            return
        if self.jeHlava(self.myself.x+2*self.myself.dx, self.myself.y+2*self.myself.dy):
            self.stena()
            return
        x,y = 0,0
        if self.myself.dx == 1:
            y = 1
        if self.myself.dx == -1:
            y = -1
        if self.myself.dy == 1:
            x = -1
        if self.myself.dy == -1:
            x = 1
        if self.jeHlava(self.myself.x+x+self.myself.dx,self.myself.y+y+self.myself.dy):
            self.stena()
            return
        x,y = 0,0
        if self.myself.dx == 1:
            y = -1
        if self.myself.dx == -1:
            y = 1
        if self.myself.dy == 1:
            x = 1
        if self.myself.dy == -1:
            x = -1
        if self.jeHlava(self.myself.x+x+self.myself.dx,self.myself.y+y+self.myself.dy):
            self.stena()
            return

    def radsejKuStene(self,lavo,pravo,vpredu):
        vysledok = []
        for sused in self.susedia([self.myself.x,self.myself.y]):
            if self.map.contents[sused[0]][sused[1]] == False:
                for s in self.susedia(sused):
                    if self.map.contents[s[0]][s[1]] == True:
                        if s[0] != self.myself.x or s[1] != self.myself.y:    
                            self.log('niekde je stena',self.myself.x,self.myself.y,"policka lavo a pravo",self.polickoLavo,self.polickoPravo,"s",s)
                            if sused[0] == self.polickoLavo[0] and sused[1] == self.polickoLavo[1]:
                                vysledok.append(Direction.LEFT)
                            if sused[0] == self.polickoPravo[0] and sused[1] == self.polickoPravo[1]:
                                vysledok.append(Direction.RIGHT)
                            if sused[0] == self.polickoPredu[0] and sused[1] == self.polickoPredu[1]:
                                vysledok.append(Direction.NONE)
        # if Direction.LEFT in vysledok:
        #     return Direction.LEFT
        # if Direction.RIGHT in vysledok:
        #     return Direction.RIGHT
        # if Direction.NONE in vysledok:
        #     return Direction.NONE
        return vysledok
        # return False


    def turn(self) -> Command:
        px, mx, py, my = 0, 0, 0, 0
        prx = self.myself.x
        pry = self.myself.y
        pdx = self.myself.dx
        pdy = self.myself.dy

        if pdx != -1:
            self.myself.x, self.myself.y = prx+1, pry
            self.myself.dx, self.myself.dy = 1, 0
            px = max(self.dfs([self.myself.x+1,self.myself.y]), self.dfs([self.myself.x-1,self.myself.y]), self.dfs([self.myself.x,self.myself.y+1]), self.dfs([self.myself.x,self.myself.y-1]))
            if self.jeStena(self.myself.x, self.myself.y) == True:
                px = -1
        if pdx != 1:
            self.myself.x, self.myself.y = prx-1, pry
            self.myself.dx, self.myself.dy = -1, 0
            mx = max(self.dfs([self.myself.x+1,self.myself.y]), self.dfs([self.myself.x-1,self.myself.y]), self.dfs([self.myself.x,self.myself.y+1]), self.dfs([self.myself.x,self.myself.y-1]))
            if self.jeStena(self.myself.x, self.myself.y) == True:
                mx = -1
        if pdy != -1:
            self.myself.x, self.myself.y = prx, pry+1
            self.myself.dx, self.myself.dy = 0, 1
            py = max(self.dfs([self.myself.x+1,self.myself.y]), self.dfs([self.myself.x-1,self.myself.y]), self.dfs([self.myself.x,self.myself.y+1]), self.dfs([self.myself.x,self.myself.y-1]))
            if self.jeStena(self.myself.x, self.myself.y) == True:
                py = -1
        if pdy != 1:
            self.myself.x, self.myself.y = prx, pry-1
            self.myself.dx, self.myself.dy = 0, -1
            my = max(self.dfs([self.myself.x+1,self.myself.y]), self.dfs([self.myself.x-1,self.myself.y]), self.dfs([self.myself.x,self.myself.y+1]), self.dfs([self.myself.x,self.myself.y-1]))
            if self.jeStena(self.myself.x, self.myself.y) == True:
                my = -1

        if pdx == -1:
            lavo = py
            pravo = my
            vpredu = mx
        elif pdx == 1:
            lavo = my
            pravo = py
            vpredu = px
        elif pdy == -1:
            lavo = mx
            pravo = px
            vpredu = my
        elif pdy == 1:
            lavo = px
            pravo = mx
            vpredu = py

        self.myself.x, self.myself.y = prx, pry-1
        kam = self.radsejKuStene(lavo, pravo, vpredu)
    
        self.myself.x, self.myself.y = prx, pry
        self.myself.dx, self.myself.dy = pdx, pdy
        self.log("lavo, pravo, vpredu:",lavo,pravo,vpredu)
        najvecsie=[]
        if lavo >= vpredu and lavo >= pravo:
            najvecsie.append(lavo)
        if pravo >= vpredu and pravo >= lavo:
            najvecsie.append(pravo)
        if vpredu >= lavo and vpredu >= pravo:
            najvecsie.append(vpredu)

        if lavo == vpredu:
            if vpredu in najvecsie:
                self.d = Direction.NONE
            if lavo in najvecsie:
                self.d = Direction.LEFT
            else:
                self.d = Direction.RIGHT
        if lavo == pravo:
            if pravo in najvecsie:
                self.d = Direction.RIGHT
            if lavo in najvecsie:
                self.d = Direction.LEFT
            else:
                self.d = Direction.NONE
        elif pravo == vpredu:
            if vpredu in najvecsie:
                self.d = Direction.NONE
            if pravo in najvecsie:
                self.d = Direction.RIGHT
            else:
                self.d = Direction.LEFT
        else:
            if lavo > pravo and lavo > vpredu:
                self.d = Direction.LEFT
            elif pravo > lavo and pravo > vpredu:
                self.d = Direction.RIGHT
            elif vpredu > lavo and vpredu > pravo:
                self.d = Direction.NONE

        self.predoslaMapa = self.map.contents.copy()
        self.log(px, mx, py, my, self.myself.dx, self.myself.dy, self.d)
        self.powerupy()
        return Command(self.d, self.pouzitPowerup)


if __name__ == '__main__':
    c = OurClient()
    c.run()
