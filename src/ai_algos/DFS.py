from .Pathfinder import PathFinder
from .Location import Location
from .Node import Node

class DFS(PathFinder):

    def goTo(self, fromLoc, toLoc, rover, mapHandler):
        stack = []
        visited_coords = set()

        startCoord = (fromLoc.x, fromLoc.y)
        goalCoord = (toLoc.x, toLoc.y)

        startNode = Node(startCoord, None)
        stack.append(startNode)

        while stack:
            currentNode = stack.pop()
            currentCoord = currentNode.coord

            if currentCoord in visited_coords:
                 continue
            visited_coords.add(currentCoord)

            if currentCoord == goalCoord:
                return [fromLoc] + self.getPath(currentNode, mapHandler)

            currentLocation = self.coordToLocation(currentCoord, mapHandler)

            for neighborCoord in mapHandler.getNeighbors(currentCoord[0], currentCoord[1]):
                if neighborCoord not in visited_coords:
                    neighborLocation = self.coordToLocation(neighborCoord, mapHandler)

                    if rover.canTraverse(currentLocation, neighborLocation):
                        neighborNode = Node(neighborCoord, currentNode)
                        stack.append(neighborNode)

        return []