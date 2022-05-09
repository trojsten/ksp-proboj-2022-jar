#!/usr/bin/env python
from sys import stderr
from common import *

smerX = [0, 1, 0, -1]
smerY = [1, 0, -1, 0]
true = True
false = False


class OurClient(TronClient):
    def get_display_name(self) -> str:
        self.last_direction = None
        return "see_5"

    def get_color(self) -> str:
        return "#ffc0cb"

    def get_next_tile(self, dir: Direction):
        speed = self.myself.speed
        if dir == Direction.LEFT:
            return (self.myself.x + self.myself.dy * speed, self.myself.y - self.myself.dx * speed)
        elif dir == Direction.RIGHT:
            return (self.myself.x - self.myself.dy * speed, self.myself.y + self.myself.dx * speed)
        elif dir == Direction.NONE:
            return (self.myself.x + self.myself.dx * speed, self.myself.y + self.myself.dy * speed)

    def get_next_dir(self, dir: Direction):
        self.log("dx: {dx}, dy: {dy}, speed: {speed}".format(
            dx=self.myself.dx, dy=self.myself.dy, speed=self.myself.speed))
        if dir == Direction.LEFT:
            return (self.myself.dy, -self.myself.dx)
        elif dir == Direction.RIGHT:
            return (-self.myself.dy, self.myself.dx)
        elif dir == Direction.NONE:
            return (self.myself.dx, self.myself.dy)

    def get_tile(self, pos) -> bool:
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= self.map.width or pos[1] >= self.map.height:
            return False
        return not self.map.contents[pos[0]][pos[1]]

    @property
    def pos(self):
        return (self.myself.x, self.myself.y)

    def to_dir(self, pos) -> Direction:
        if self.pos[0] + self.myself.dx == pos[0] and self.pos[1] + self.myself.dy == pos[1]:
            return Direction.NONE
        elif self.pos[0] - self.myself.dy == pos[0] and self.pos[1] + self.myself.dx == pos[1]:
            return Direction.RIGHT
        else:
            return Direction.LEFT

    def to_powerup(self) -> Direction:
        navstivene = [[-1 for _ in range(self.map.height)]
                      for _ in range(self.map.width)]

        MAXDIST = 3
        q = [(self.pos, 0)]
        while len(q) > 0:
            teraz = q[0]
            q.pop(0)
            if teraz[1] >= MAXDIST or navstivene[teraz[0][0]][teraz[0][1]] >= 0:
                continue
            navstivene[teraz[0][0]][teraz[0][1]] = teraz[1]

            for powerup in self.map.powerups:
                if powerup.x == teraz[0][0] and powerup.y == teraz[0][1]:
                    a = teraz
                    while navstivene[a[0][0]][a[0][1]] != 1:
                        for j in range(4):
                            next = (a[0][0] + smerX[j], a[0][1] + smerY[j])
                            if self.get_tile(next) and navstivene[next[0]][next[1]] == a[1] - 1:
                                a = (next, a[1]-1)
                    return self.to_dir(a[0])

            for i in range(4):
                next = (teraz[0][0] + smerX[i], teraz[0][1] + smerY[i])
                if self.get_tile(next) and navstivene[next[0]][next[1]] == -1:
                    q.append((next, teraz[1]+1))
        return None

    def get_available_tiles(self, dir: Direction) -> int:
        navstivene = [[False for _ in range(self.map.height)]
                      for _ in range(self.map.width)]

        currdir = self.get_next_dir(dir)
        for i in range(self.myself.speed):
            navstivene[self.myself.x + currdir[0] *
                       i][self.myself.y + currdir[1] * i] = True
        q = [(self.myself.x + currdir[0] * self.myself.speed,
              self.myself.y + currdir[1] * self.myself.speed)]
        policka = 0
        hraci = set()
        pocet_hracov = 1
        for player in self.players:
            if player != self.myself:
                hraci.add((player.x, player.y))
        while len(q) > 0:
            terajsie = q[0]
            q.pop(0)
            if navstivene[terajsie[0]][terajsie[1]]:
                continue
            navstivene[terajsie[0]][terajsie[1]] = True
            policka += 1
            if terajsie in hraci:
                pocet_hracov += 1
            for i in range(4):
                dalsie = (terajsie[0] + smerX[i], terajsie[1] + smerY[i])
                if self.get_tile(dalsie) and not navstivene[dalsie[0]][dalsie[1]]:
                    q.append(dalsie)
        return policka / pocet_hracov

    def get_player_occupied_spaces(self):
        out = set()
        for player in self.players:
            if player == self.myself:
                continue
            out.add((player.x + player.dx, player.y + player.dy))
            out.add((player.x + player.dy, player.y - player.dx))
            out.add((player.x - player.dy, player.y + player.dy))
        return out

    def use_powerup(self, dir) -> bool:
        CLEAN_THRESHOLD = 5
        if self.myself.powerup == PowerUpType.CLEAN:
            return self.get_available_tiles(dir) < CLEAN_THRESHOLD
        elif self.myself.powerup == PowerUpType.SPEED_ME:
            return False
        elif self.myself.powerup == PowerUpType.SPEED_OTHERS:
            return True
        elif self.myself.powerup == PowerUpType.STOP_ME:
            return self.myself.speed > 1 or self.get_available_tiles(dir) < 3
        elif self.myself.powerup == PowerUpType.STOP_OTHERS:
            return True
        else:
            return False

    def collect_powerups(self) -> bool:
        if self.myself.powerup == PowerUpType.CLEAN:
            return False
        elif self.myself.powerup == PowerUpType.SPEED_ME:
            return True
        elif self.myself.powerup == PowerUpType.SPEED_OTHERS:
            return True
        elif self.myself.powerup == PowerUpType.STOP_ME:
            return True
        elif self.myself.powerup == PowerUpType.STOP_OTHERS:
            return True
        else:
            return True

    def can_move(self, dir) -> bool:
        if self.myself.speed == 0:
            pos = (self.pos[0] + dir[0], self.pos[1] + dir[1])
            return self.get_tile(pos)
        for i in range(1, self.myself.speed + 1):
            pos = (self.pos[0] + dir[0] * i, self.pos[1] + dir[1] * i)
            if not self.get_tile(pos):
                return False
        return True

    def turn(self) -> Command:
        directions = [Direction.LEFT, Direction.RIGHT, Direction.NONE]
        a = Command(None, False)
        if self.collect_powerups():
            a.direction = self.to_powerup()
        if a.direction == None:
            # a.direction = Direction.NONE
            best = 0
            bestUpdated = 0
            playerOccupied = self.get_player_occupied_spaces()
            availableDirections = []
            for dir in directions:
                next = self.get_next_dir(dir)
                isPlayerOccupied = False
                for i in range(1, self.myself.speed+1):
                    if (self.pos[0] + i * next[0], self.myself.y + i * next[1]) in playerOccupied:
                        isPlayerOccupied = True
                        break
                if isPlayerOccupied:
                    self.log("Player Occupied space")
                    continue
                if self.can_move(next):
                    self.log(str(dir) + " is valid move")
                    availableDirections.append(dir)
            DIRECTION_PRIORITIES = {
                Direction.LEFT: 1,
                Direction.RIGHT: 2,
                Direction.NONE: 3
            }
            availableDirections.sort(
                key=lambda a: self.get_available_tiles(a) + DIRECTION_PRIORITIES[a], reverse=True)
            if len(availableDirections) > 0:
                a.direction = availableDirections[0]

        else:
            self.log("Going to power-up")
        if a.direction == None:
            a.direction = Direction.NONE
        a.use_powerup = self.use_powerup(a.direction)
        self.last_direction = a.direction
        return a

    def log(self, msg):
        print(msg, file=stderr)


if __name__ == '__main__':
    c = OurClient()
    c.run()
