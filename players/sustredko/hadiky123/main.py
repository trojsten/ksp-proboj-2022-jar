#!/usr/bin/env python

import random

from common import *
from hunter import *
import sys


class OurClient(TronClient):
    def get_display_name(self) -> str:
        return "masívny had"

    def get_color(self) -> str:
        return "#eeeeee"

    def turn(self) -> Command:
        d = hunter(self)

        return d


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    c = OurClient()
    c.run()
