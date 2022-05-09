from typing import List

import sys
class Vector(tuple):
    def __add__(self, other):
        return Vector((self[i] + other[i] for i in range(len(self))))

    def __sub__(self, other):
        return Vector((self[i] - other[i] for i in range(len(self))))

    def __neg__(self):
        return Vector((-self[i] for i in range(len(self))))

    def __mul__(self, scalar):
        return Vector((self[i] * scalar for i in range(len(self))))

    def susedia(self, kolko=1):
        return (self + kolko*smer for smer in Vector.normals)

Vector.normals = (Vector((1, 0)), Vector((0, 1)), Vector((-1, 0)), Vector((0, -1)))

class LepsiaMapa:
    def __init__(self, map):
        self.map = map

    def __getitem__(self, xy):
        x, y = xy
        if 0 <= x < self.map.width and 0 <= y < self.map.height:
            return self.map.contents[x][y]
        return True

    def __setitem__(self, xy, val):
        x, y = xy
        if 0 <= x < self.map.width and 0 <= y < self.map.height:
            self.map.contents[x][y] = val

    def __repr__(self):
        result = []
        for y in range(-1, self.map.height + 1):
            for x in range(-1, self.map.width + 1):
                result.append("#" if self[x, y] == True else " " if self[x, y] == False else str(self[x, y]))
            result.append("\n")
        result.pop()
        return "".join(result)

    def hraci(self, myself, players):
        x, y, dx, dy = myself.x, myself.y, myself.dx, myself.dy
        self[x, y] = "@"

        for i in range(len(players)):
            hrac = players[i]
            if not hrac.alive:
                continue
            x, y, d = hrac.x, hrac.y, max(abs(hrac.dx), abs(hrac.dy))
            self[x, y] = (i+1)%9+1
            for kolko in range(1, 1+d):
                for smer in ((kolko, 0), (0, kolko), (-kolko, 0), (0, -kolko)):
                    if not self[x+smer[0], y+smer[1]]: self[x+smer[0], y+smer[1]] = "!"

        return self

    def bezhracov(self, myself, players):
        x, y, dx, dy = myself.x, myself.y, myself.dx, myself.dy
        self[x, y] = False

        for i in range(len(players)):
            hrac = players[i]
            if not hrac.alive:
                continue
            x, y, dx, dy = hrac.x, hrac.y, hrac.dx, hrac.dy
            self[x, y] = False

        return self

    def copy(self):
        nova = LepsiaMapa(self.map)
        nova.map.contents = nova.map.contents.copy()
        for i in range(len(nova.map.contents)):
            nova.map.contents[i] = nova.map.contents[i].copy()
        nova.map.powerups = nova.map.powerups.copy()

        return nova

    def compare(self, other):
        volne = ("!", False)

        added = []
        for x in range(self.map.width):
            for y in range(self.map.height):
                if other[x, y] in volne and self[x, y] not in volne:
                    return True
                elif other[x, y] not in volne and self[x, y]:
                    added.append((x, y))
        return added

class Linker:
    parents = set()
    successors = set()

class Tile:
    root = False
    coords = None
    linkers: List[Linker] = [Linker(), Linker(), Linker(), Linker()]
    lastEdit = 0

    def __init__(self, coords, parent = None, root = False) -> None:
        self.coords = Vector(coords)
        self.parent = parent
        self.root = root

    def destroy(self):
        for l in range(len(self.linkers)):
            for i in self.linkers[l].parents:
                i.linkers[l].successors.discard(self)
            for i in self.linkers[l].successors:
                i.destroy()



    def __hash__(self):
        return hash(self.coords)
    def _is_valid_operand(self, other):
        return hasattr(other, "coords")
    def __eq__(self, other):
        return self.coords == other.coords

def print_bfs_data(index, tilemap: List[List[Tile]]):
    strfield = [["" for x in range(len(tilemap))] for y in range(len(tilemap[0]))]
    for i in range(len(tilemap)):
        for j in range(len(tilemap[0])):
            resVector = Vector((0, 0))
            for l in tilemap[i][j].linkers[index].parents:
                aVect = tilemap[i][j].coords - l.coords
                if resVector is None:
                    resVector = aVect
                else:
                    resVector += aVect
            resVector = tuple([(x/abs(x) if x!=0 else 0) for x in resVector])
            arrs = {(-1, 0): "<", (1, 0):">", (0,- 1):"^", (0, 1):"v", (-1, -1):"F", (1, -1):"T", (1, 1):"J", (-1, 1):"L", (0, 0):"•"}
            strfield[i][j] =  arrs[resVector]
    print(f"Running for INDEX {index}", file=sys.stderr)
    for i in range(len(strfield)):
        for j in range(len(strfield[0])):
            print(strfield[i][j], end="", file=sys.stderr)
        print("",file=sys.stderr)
