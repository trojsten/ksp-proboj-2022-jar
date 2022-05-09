from enum import Enum
from queue import Queue
from typing import List, Generator, Any, Iterable, Union, Sequence


class Distance(Enum):
    MANHATTAN = 4,
    CHESSBOARD = 8

    def __str__(self):
        return self.name.title()


class Tile:

    def __init__(self, x: int, y: int, parent: "Grid", data=None):
        self.data = data
        self.x, self.y = x, y
        self.parent = parent

    def __repr__(self):
        return f"<Tile: {repr(self.data)} at [{self.x}, {self.y}]>"

    def __str__(self):
        return str(self.data)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other: Union["Tile", int, float]):
        if isinstance(other, Tile):
            return self.copy(data=self.data + other.data)
        return self.copy(data=self.data + other)

    def __sub__(self, other: Union["Tile", int, float]):
        if isinstance(other, Tile):
            return self.copy(data=self.data - other.data)
        return self.copy(data=self.data - other)

    def copy(self, **kwargs):
        for attribute in self.__dict__:
            if attribute not in kwargs:
                kwargs[attribute] = self.__dict__[attribute]
        return Tile(**kwargs)

    def neighbours(self, distance=1) -> Generator["Tile", None, None]:
        return self.parent.neighbours(self.x, self.y, distance)

    def swap(self, other: "Tile"):
        self.parent.swap(self, other)


class GridView:
    ...


class Grid:

    def __init__(self, width: int = 100, height: int = 100, distance=Distance.MANHATTAN, fill=None):
        self.width = width
        self.height = height
        self.distance_type = distance
        self._array = [[Tile(x, y, self, fill) for x in range(width)] for y in range(height)]

    @classmethod
    def from_sequence(cls, sequence: Sequence[Sequence[Any]], distance=Distance.MANHATTAN) -> "Grid":
        """Create new grid from a two dimensional sequence."""
        new_grid = Grid(len(sequence), len(sequence[0]), distance)
        new_grid.fill((item for row in sequence for item in row))
        return new_grid

    def __repr__(self):
        return f"<Grid: {self.height}x{self.width}, {self.distance_type}>"

    def __str__(self):
        # Todo: justify the table, multidimensional support
        return "\n".join(" ".join(f"[{str(tile)}]" for tile in row) for row in self._array)

    def __len__(self) -> int:
        """Returns the size (number of tiles) of the grid."""
        return self.width * self.height

    def __getitem__(self, item) -> List[Tile]:
        return self._array[item]

    def __iter__(self) -> Generator[Tile, None, None]:
        return (tile for row in self._array for tile in row)

    def __reversed__(self) -> Generator[Tile, None, None]:
        return (tile for row in reversed(self._array) for tile in reversed(row))

    def __add__(self, other):
        new_grid = Grid(width=self.width, height=self.height, distance=self.distance_type)
        new_grid.fill((tile1 + tile2).data for tile1, tile2 in zip(self, other))
        return new_grid

    def __sub__(self, other):
        new_grid = Grid(width=self.width, height=self.height, distance=self.distance_type)
        new_grid.fill((tile1 - tile2).data for tile1, tile2 in zip(self, other))
        return new_grid

    def get_tile(self, x: int, y: int) -> Tile:
        return self._array[y][x]

    def get_data(self, x: int, y: int) -> Any:
        return self.get_tile(x, y).data

    def set_tile(self, x: int, y: int, tile: Tile):
        self._array[y][x] = tile
        tile.x, tile.y = x, y

    def set_data(self, x: int, y: int, data):
        self.get_tile(x, y).data = data

    def swap(self, tile1: Tile, tile2: Tile):
        self.set_tile(tile1.x, tile1.y, tile2)
        self.set_tile(tile2.x, tile2.y, tile1)

    def fill(self, iterable: Iterable):
        """Fill the grid with values provided by iterable."""
        if not isinstance(iterable, Iterable):
            raise TypeError(f"{type(iterable)} is not iterable")

        for tile, value in zip(self, iterable):
            tile.data = value

    def fill_int(self):
        self.fill(range(len(self)))

    def neighbours(self, x, y, distance=1) -> Generator[Tile, None, None]:
        """Iterate through the neighbours of the tile at [x, y] within the given distance.

        Coordinates start at 0.
        x - horizontal, y - vertical"""

        for next_y in range(y - distance, y + distance + 2):
            for next_x in range(x - distance, x + distance + 2):

                # Inside the grid
                in_bounds = next_x in range(self.width) and next_y in range(self.height)

                # The distance is within the desired range - depends on distance type
                correct_distance = True
                if self.distance_type == Distance.MANHATTAN:
                    correct_distance = distance >= abs(x - next_x) + abs(y - next_y) > 0

                if in_bounds and correct_distance:
                    yield self._array[next_y][next_x]

    def reverse(self):
        for front, back in zip((val for i, val in enumerate(self) if i < len(self // 2)), reversed(self)):
            self.swap(front, back)
            print(f"swapping {repr(front)} with {repr(back)}")

    def transpose(self):
        ...

    def rotate_right(self):
        for row in self._array:
            for tile in self._array:
                ...

    # def path(self, source: Tile, dest: Tile) -> List[Tile]:
    #     q = Queue()
    #     seen = set()
    #     shortest_to = []
    #     grid = Grid.from_sequence(client.map.contents)
    #     for tile in grid:
    #         tile.dist = float("inf")
    #         tile.pred = None
    #
    #     target = Tile(x, y, grid)
    #     bozo = client.myself
    #     client.log(repr(grid))
    #     client.log(str(grid))
    #
    #     tile = Tile(bozo.x, bozo.y, grid)  # my tile
    #     tile.dist, tile.pred = 0, None
    #     q.put(tile)
    #     seen.add(tile)
    #
    #     while not q.empty():
    #         tile = q.get()
    #         if tile == target:
    #             client.log(f"[PATH] Found the target tile {repr(target)}")
    #             break
    #
    #         for neighbour in tile.neighbours():
    #             if tile.dist + 1 < neighbour.dist:
    #                 neighbour.dist = tile.dist + 1
    #                 neighbour.pred = tile
    #             if neighbour not in seen:
    #                 seen.add(neighbour)
    #                 q.put(neighbour)
    #
    #     return [(0, 0)]
