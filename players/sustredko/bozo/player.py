#!/usr/bin/env python
from common import *
from random import choice
from basic_turn_handler import handle
from samo import Powerups


class BozoClient(TronClient):
    def __init__(self):
        super().__init__()
        self.powerups = Powerups()

    def get_display_name(self) -> str:
        words = ['angriest', 'worst', 'biggest', 'bitterest', 'blackest', 'blandest', 'bloodiest', 'bluest', 'boldest', 'bossiest', 'bravest', 'briefest', 'brightest', 'broadest', 'busiest', 'calmest', 'cheapest', 'chewiest', 'chubbiest', 'classiest', 'cleanest', 'clearest', 'cleverest', 'closest', 'cloudiest', 'clumsiest', 'busiest', 'calmest', 'coarsest', 'coldest', 'coolest', 'craziest', 'creamiest', 'creepiest', 'crispiest', 'cruellest', 'crunchiest', 'curliest', 'curviest', 'cutest', 'dampest', 'darkest', 'deadliest', 'deepest', 'densest', 'dirtiest', 'driest', 'dullest', 'dumbest', 'dustiest', 'earliest', 'easiest', 'faintest', 'fairest', 'fanciest', 'fattest', 'fewest', 'fiercest', 'filthiest', 'finest', 'firmest', 'fittest', 'flakiest', 'flattest', 'freshest', 'friendliest', 'fullest', 'funniest', 'gentlest', 'best', 'grandest', 'gravest', 'greasiest', 'greatest', 'greediest', 'grossest', 'guiltiest', 'hairiest', 'handiest', 'happiest', 'hardest', 'harshest', 'healthiest', 'hippest', 'hottest', 'humblest', 'hungriest', 'iciest', 'itchiest', 'juiciest', 'kindest', 'largest', 'latest', 'laziest', 'lightest', 'likeliest', 'littlest', 'longest', 'loudest', 'loveliest', 'lowest', 'maddest', 'meanest', 'messiest', 'mildest', 'moistest', 'narrowest', 'nastiest', 'naughtiest', 'nearest', 'neatest', 'nicest', 'noisiest', 'oddest', 'oiliest', 'oldest/eldest', 'plainest', 'politest', 'poorest', 'prettiest', 'proudest', 'purest', 'quickest', 'quietest', 'rarest', 'ripest', 'riskiest', 'roomiest', 'roughest', 'rudest', 'rustiest', 'saddest', 'safest', 'saltiest', 'sanest', 'scariest', 'shallowest', 'sharpest', 'shiniest', 'sincerest', 'skinniest', 'sleepiest', 'slimmest', 'slimiest', 'slowest', 'smallest', 'smartest', 'smelliest', 'smokiest', 'smoothest', 'softest', 'soonest', 'sorest', 'sweatiest', 'sweetest', 'tallest', 'tannest', 'tastiest', 'thickest', 'thinnest', 'thirstiest', 'tiniest', 'toughest', 'truest', 'ugliest', 'warmest', 'weakest']
        return f"{choice(words)}-bozo"

    def get_color(self) -> str:
        return "#c0ffee"

    def turn(self) -> Command:
        return handle(self, self.powerups)


if __name__ == '__main__':
    c = BozoClient()
    c.run()
