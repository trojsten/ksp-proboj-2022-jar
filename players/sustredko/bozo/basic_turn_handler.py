from common import *
from utils import left, right, free, Dir, get_direction, print_powerup
from paths import get_path
from samo import Powerups


def handle(client: TronClient, powerup: Powerups) -> Command:
    # try:
    bozo, grid, players = client.myself, client.map.contents, client.players
    client.log(f"[BOZO]: [{bozo.x, bozo.y}] v{bozo.dx, bozo.dy} S{bozo.speed} P{bozo.powerup if bozo.powerup is not None else 0}")

    # Stopnuty sme
    if bozo.speed == 0:
        client.log(f"[BOZO]: Stopped, waiting.")
        return Command(Direction.NONE, False)

    elif bozo.speed != 1:
        client.log(f"[BOZO]: I'm fast! ({bozo.speed})")

    path = get_path(1000, 1000, client, powerup=True)

    if path:
        step = path[0]
        deltas = (step[0] - bozo.x, step[1] - bozo.y)
        # assert abs(sum(deltas)) == 1
        next_dir = get_direction(*step, client)
        # client.log(f"[MOVE] Path found, going to {step} ({next_dir})")

    else:
        next_forward = bozo.x + bozo.dx, bozo.y + bozo.dy
        next_left, next_left_deltas = left(bozo.x, bozo.y, bozo.dx, bozo.dy, bozo.speed)
        next_right, next_right_deltas = right(bozo.x, bozo.y, bozo.dx, bozo.dy, bozo.speed)

        next_dir = Direction.NONE
        if not free(*next_forward, client):
            next_dir = Direction.RIGHT if free(*next_right, client) else Direction.LEFT

        # client.log(f"[MOVE] Path NOT found, going {next_dir}")

    client.log(f"{print_powerup(client)}")
    use = powerup.use_powerup(client)
    if use:
        client.log(f"[POWER] Using powerup" + "!"*20)

    return Command(next_dir, use)

    # except:
    #     client.log(f"[PRUSER]: ideme rovno")
    #     return Command(Direction.NONE, False)
