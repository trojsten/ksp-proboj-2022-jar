from common import *
from random import randint
from utils import *


class Pointselector:

    def get(self, client: TronClient) -> Command:

        mapenka = client.map.contents
        rand_x, rand_y = randint(0, len(mapenka)), randint(0, len(mapenka))
        x, y = client.myself.x, client.myself.y

        while mapenka[rand_x][rand_y]:
            rand_x, rand_y = randint(0, len(mapenka)), randint(0, len(mapenka))
            if (abs(x - rand_x) < 10 or abs(y - rand_y) < 10) or \
                    (abs(x - rand_x) > 40 or abs(y - rand_y) > 40): continue

        # go there by bfs if possible (else get beck to get())

        return tuple(rand_x, rand_y)


class Powerups:
    # insta use
    def use_powerup(self, client:TronClient):
        powerup = client.myself.powerup.value if client.myself.powerup is not None else 0
        if powerup in (2, 3, 5):
            return True

        """ elif powerup == 5:
            x, y, dx, dy, speed, speed_reset_time = client.myself.x, client.myself.y, client.myself.dx, client.myself.dy, client.myself.speed, client.myself.speed_reset_time
            board = client.map.contents

        # ak pojdeme doprava:

            (x1, y1), (dx1, dy1) = right(x, y, dx, dy, speed)
            movesr = 0
            if board[x1][y1] == 0:
                speed = 1 if speed_reset_time - 1 == 0 else speed

                (xr, yr), (dxr, dyr) = right(x1, y1, dx1, dy1, speed)
                (xu, yu) = (x1 + dx1*speed, y1 + dy1*speed)
                (xl, yl), (dxl, dyl) = left(x1, y1, dx1, dy1, speed)

                movesr += (board[xr][yr] == 0) + (board[xu][yu] == 0) + (board[xl][yl] == 0)


        # ak pojdeme dolava:
        
            (x1, y1), (dx1, dy1) = left(x, y, dx, dy, speed)
            movesl = 0
            if board[x1][y1] == 0:
                speed = 1 if speed_reset_time - 1 == 0 else speed

                (xr, yr), (dxr, dyr) = right(x1, y1, dx1, dy1, speed)
                (xu, yu) = (x1 + dx1*speed, y1 + dy1*speed)
                (xl, yl), (dxl, dyl) = left(x1, y1, dx1, dy1, speed)

                movesl += (board[xr][yr] == 0) + (board[xu][yu] == 0) + (board[xl][yl] == 0)

        # ak pojdeme rovno:
    
            (x1, y1), (dx1, dy1) = free(x, y, dx, dy, speed)
            movesu = 0
            if board[x1][y1] == 0:
                speed = 1 if speed_reset_time - 1 == 0 else speed

                (xr, yr), (dxr, dyr) = right(x1, y1, dx1, dy1, speed)
                (xu, yu) = (x1 + dx1*speed, y1 + dy1*speed)
                (xl, yl), (dxl, dyl) = left(x1, y1, dx1, dy1, speed)

                movesu += (board[xr][yr] == 0) + (board[xu][yu] == 0) + (board[xl][yl] == 0)

            if movesr + movesu + movesl == 0:
                return True
            else:
                return False """

        return False
