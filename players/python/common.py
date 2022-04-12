import enum
import sys
from dataclasses import dataclass
from typing import List


@dataclass
class Player:
    x: int
    y: int
    dx: int = 0
    dy: int = 0
    speed: int = 0
    speed_reset_time: int = 0
    alive: bool = False

    @classmethod
    def from_input(cls, data: str) -> "Player":
        alive, x, y, dx, dy, s, sr = map(int, data.split())
        alive = bool(alive)
        return Player(x, y, dx, dy, s, sr, alive)


@dataclass
class PowerUp:
    x: int
    y: int


@dataclass
class Map:
    width: int
    height: int
    contents: List[List[bool]] = None
    powerups: List[PowerUp] = None


class Command(enum.Enum):
    LEFT = "L"
    RIGHT = "R"
    NONE = "x"


class TronClient:
    def __init__(self):
        self.map = Map(0, 0)
        self.myself = Player(0, 0)
        self.players: List[Player] = []

    def read_state(self):
        self.map.width, self.map.height = map(int, input().split())
        self.map.contents = []
        for y in range(self.map.height):
            self.map.contents.append(list(map(bool, input().split())))

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
            print(cmd.value)
            print(".", flush=True)
        print("Bye")

    def turn(self) -> Command:
        raise NotImplementedError()

    def get_display_name(self) -> str:
        raise NotImplementedError()

    def get_color(self) -> str:
        raise NotImplementedError()