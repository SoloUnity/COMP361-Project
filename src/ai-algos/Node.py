class Node:
    def __init__(self, coord: (int, int), parent):
        self.coord = coord
        self.parent = parent

    def __lt__(self, other):
        return self.coord < other.coord
