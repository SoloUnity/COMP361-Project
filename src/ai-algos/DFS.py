from collections import deque
from Pathfinder import PathFinder
from Location import Location

class DFS(PathFinder):

    def goTo(self, fromLoc, toLoc, rover, mapHandler):
        stack = []
        visited = []

        # Start from fromLoc
        stack.append(Node((fromLoc.x, fromLoc.y), None))

        while len(stack) > 0:
            current = stack.pop()
            visited.append(current.coord)

            # If we've reached the destination
            if current.coord == (toLoc.x, toLoc.y):
                return [fromLoc] + self.getPath(current, mapHandler)

            # Otherwise, explore neighbors
            cx, cy = current.coord
            currentLoc = mapHandler.getLocationAt(cx, cy)
            for n in mapHandler.getNeighbors(cx, cy):
                nLoc = mapHandler.getLocationAt(n[0], n[1])
                if rover.canTraverse(currentLoc, nLoc) and n not in visited:
                    stack.append(Node(n, current))

        # If no path is found
        return []

    def visitAll(self, fromLoc, toVisit, rover, mapHandler):
        path = [fromLoc]
        if len(toVisit) == 0:
            return path

        # Convert the list of Locations to a set of (x,y) for easy membership checks
        leftToVisit = set((loc.x, loc.y) for loc in toVisit)

        stack = []
        visited = []

        # Start from fromLoc
        stack.append(Node((fromLoc.x, fromLoc.y), None))

        while len(stack) > 0:
            current = stack.pop()
            visited.append(current.coord)

            # If we've reached one of the targets
            if current.coord in leftToVisit:
                leftToVisit.remove(current.coord)
                # Add this partial path to the final path
                path += self.getPath(current, mapHandler)

                # If we've visited all required locations, return
                if len(leftToVisit) == 0:
                    return path

                # Otherwise, restart the DFS from the current node
                stack.clear()
                visited.clear()
                stack.append(Node(current.coord, None))

            else:
                # Continue DFS normally
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

class Node:
    def __init__(self, coord: (int, int), parent):
        self.coord = coord
        self.parent = parent
