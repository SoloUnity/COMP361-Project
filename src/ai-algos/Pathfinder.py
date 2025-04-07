from Location import Location
from Rover import Rover
from MapHandler import MapHandler
from Node import Node

class PathFinder:

    def goTo(self, fromLoc: Location, toLoc: Location, rover: Rover, mapHandler: MapHandler) -> list[Location]:
        raise NotImplementedError("Subclasses must implement the goTo method.")

    def visitAll(self, fromLoc: Location, toVisit: list[Location], rover: Rover, mapHandler: MapHandler) -> list[Location]:
        path = [fromLoc]
        if not toVisit:
            return path

        leftToVisitCoords = set((loc.x, loc.y) for loc in toVisit)
        currentLoc = fromLoc

        while leftToVisitCoords:
            closestTargetCoord = None
            shortestSubPath = None
            minPathLen = float('inf')

            for targetCoord in leftToVisitCoords:
                targetLoc = self.coordToLocation(targetCoord, mapHandler)
                tempPath = self.goTo(currentLoc, targetLoc, rover, mapHandler)

                if tempPath:
                    currentPathLen = len(tempPath) - 1
                    if currentPathLen < minPathLen:
                        minPathLen = currentPathLen
                        closestTargetCoord = targetCoord
                        shortestSubPath = tempPath

            if closestTargetCoord and shortestSubPath:
                path.extend(shortestSubPath[1:])
                currentLoc = shortestSubPath[-1]
                leftToVisitCoords.remove(closestTargetCoord)
            else:
                break

        return path

    def coordToLocation(self, coord: tuple[int, int], mapHandler: MapHandler) -> Location:
        x, y = coord
        return mapHandler.getLocationAt(x, y)

    def getPath(self, endNode: Node, mapHandler: MapHandler) -> list[Location]:
        path_coords = []
        current = endNode
        while current is not None and current.parent is not None:
            path_coords.append(current.coord)
            current = current.parent

        path_coords.reverse()
        return [self.coordToLocation(coord, mapHandler) for coord in path_coords]
