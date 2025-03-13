from collections import deque
from Pathfinder import PathFinder
from Location import Location

class DFS(PathFinder):

    def goTo(self, fromLoc, toLoc, rover, mapHandler):
        stack = []
        visited = []

        # starting coordinates fromLoc
        stack.append(Node((fromLoc.x, fromLoc.y), None))

        while len(stack) > 0:
            current = stack.pop()
            visited.append(current.coord)

            # if destitantion coordinate reached
            if current.coord == (toLoc.x, toLoc.y):
                return [fromLoc] + self.getPath(current, mapHandler)

            # explore neighbours
            cx, cy = current.coord
            currentLoc = mapHandler.getLocationAt(cx, cy)
            for n in mapHandler.getNeighbors(cx, cy):
                nLoc = mapHandler.getLocationAt(n[0], n[1])
                if rover.canTraverse(currentLoc, nLoc) and n not in visited:
                    stack.append(Node(n, current))

        # no path found
        return []

    def visitAll(self, fromLoc, toVisit, rover, mapHandler):
        # toVisit is a list of Locations

        path = [fromLoc]
        if len(toVisit) == 0:
            return path

        # Convert the list of Locations to a set of (x,y) for easy membership checks
        leftToVisit = set((loc.x, loc.y) for loc in toVisit)

        stack = []
        visited = []

        # starting coordinates fromLoc
        stack.append(Node((fromLoc.x, fromLoc.y), None))

        while len(stack) > 0:
            current = stack.pop()
            visited.append(current.coord)

            # one coordinate reached
            if current.coord in leftToVisit:
                leftToVisit.remove(current.coord)
                # add partial path to the final path
                path += self.getPath(current, mapHandler)

                if len(leftToVisit) == 0:
                    return path

                # restart DFS from current node
                stack.clear()
                visited.clear()
                stack.append(Node(current.coord, None))

            else:
                # continue DFS
                cx, cy = current.coord
                currentLoc = mapHandler.getLocationAt(cx, cy)
                for n in mapHandler.getNeighbors(cx, cy):
                    nLoc = mapHandler.getLocationAt(n[0], n[1])
                    if rover.canTraverse(currentLoc, nLoc) and n not in visited:
                        stack.append(Node(n, current))

        # If we can't reach all targets, return what we have so far
        return path

    def getPath(self, toLoc, mapHandler):
        path = []
        current = toLoc
        while current.parent is not None:
            cx, cy = current.coord
            path.append(mapHandler.getLocationAt(cx, cy))
            current = current.parent
        path.reverse()
        return path

# TODO make a common node class after merging everything together
class Node:
    def __init__(self, coord: (int, int), parent):
        self.coord = coord
        self.parent = parent
