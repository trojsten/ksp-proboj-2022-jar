import enum
import sys
from dataclasses import dataclass
from typing import List, Optional


class PowerUpType(enum.IntEnum):
    SPEED_ME = 1
    SPEED_OTHERS = 2
    STOP_ME = 3
    STOP_OTHERS = 4
    CLEAN = 5


@dataclass
class Player:
    x: int
    y: int
    dx: int = 0
    dy: int = 0
    speed: int = 0
    speed_reset_time: int = 0
    alive: bool = False
    powerup: Optional[PowerUpType] = 0

    @classmethod
    def from_input(cls, data: str) -> "Player":
        alive, x, y, dx, dy, s, sr, powerup = map(int, data.split())
        alive = bool(alive)
        if powerup == 0:
            powerup = None
        else:
            powerup = PowerUpType(powerup)
        return Player(x, y, dx, dy, s, sr, alive, powerup)


@dataclass
class PowerUp:
    x: int
    y: int


FREE = False
WALL = True


@dataclass
class Map:
    width: int
    height: int
    contents: List[List[bool]] = None
    powerups: List[PowerUp] = None


class Direction(enum.Enum):
    LEFT = "L"
    RIGHT = "R"
    NONE = "x"


@dataclass
class Command:
    direction: Direction
    use_powerup: bool = False

    def to_string(self):
        if self.use_powerup:
            return f"{self.direction.value}+"
        return f"{self.direction.value}"

    def __hash__(self):
        return hash(self.direction) + self.use_powerup * 21163


class TronClient:
    def __init__(self):
        self.map = Map(0, 0)
        self.myself = Player(0, 0)
        self.players: List[Player] = []

    def read_state(self):
        self.map.width, self.map.height = map(int, input().split())
        if self.map.contents is None:
            self.map.contents = [
                [False for y in range(self.map.height)] for x in range(self.map.width)
            ]

        for y in range(self.map.height):
            row = list(map(lambda x: x == "1", input().split()))
            for x in range(self.map.width):
                self.map.contents[x][y] = row[x]

        self.myself = Player.from_input(input())

        players = int(input())
        self.players = []
        for _ in range(players):
            self.players.append(Player.from_input(input()))

        powerups = int(input())
        self.map.powerups = []
        for _ in range(powerups):
            x, y = map(int, input().split())
            self.map.powerups.append(PowerUp(x, y))

        assert input() == "."

    def greet_server(self):
        assert input() == "HELLO"
        assert input() == "."
        name = self.get_display_name().replace(" ", "_")
        color = self.get_color()
        print(f"{name} {color}")
        print(".", flush=True)

    def log(self, *data):
        print(*data, file=sys.stderr)

    def run(self):
        self.greet_server()
        self.myself.alive = True
        while self.myself.alive:
            self.read_state()
            cmd = self.turn()
            print(cmd.to_string())
            print(".", flush=True)
        print("Bye")

    def turn(self) -> Command:
        raise NotImplementedError()

    def get_display_name(self) -> str:
        raise NotImplementedError()

    def get_color(self) -> str:
        raise NotImplementedError()
