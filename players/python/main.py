#!/usr/bin/env python

import random

from common import *


class OurClient(TronClient):
    def get_display_name(self) -> str:
        return "BestBot"

    def get_color(self) -> str:
        return "#ff0000"

    def turn(self) -> Command:
        return random.choice([Command.LEFT, Command.RIGHT, Command.NONE])


if __name__ == '__main__':
    c = OurClient()
    c.run()
