import heapq
import math

from Location import Location
from Pathfinder import PathFinder

class AStar(PathFinder):

    def goTo(self, fromLoc, toLoc, rover, mapHandler):
        """
        Finds a path from fromLoc to toLoc using the A* algorithm.
        Accounts for the new map data layout by using mapHandler.getLocationAt(...)
        to construct Location objects.
        """
        openSet = []
        gScore = {}
        fScore = {}
        cameFrom = {}

        startNode = (fromLoc.x, fromLoc.y)
        goalNode  = (toLoc.x, toLoc.y)

        # Initialize the start node
        heapq.heappush(openSet, (self.heuristic(startNode, goalNode), startNode))
        gScore[startNode] = 0
        fScore[startNode] = self.heuristic(startNode, goalNode)

        closedSet = set()

        while openSet:
            _, current = heapq.heappop(openSet)
            if current == goalNode:
                # Goal reached – reconstruct the path
                return self.reconstructPath(cameFrom, current, mapHandler)

            closedSet.add(current)
            cx, cy = current
            currentLoc = self.coordToLocation(current, mapHandler)

            # Check all neighbors
            for neighbor in mapHandler.getNeighbors(cx, cy):
                if neighbor in closedSet:
                    continue

                neighborLoc = self.coordToLocation(neighbor, mapHandler)

                # Check if the rover can traverse from currentLoc to neighborLoc
                if not rover.canTraverse(currentLoc, neighborLoc):
                    continue

                # Compute the cost so far + cost of stepping to neighbor
                tentativeGScore = gScore[current] + self.cost(currentLoc, neighborLoc, rover)
                if (neighbor not in gScore) or (tentativeGScore < gScore[neighbor]):
                    cameFrom[neighbor] = current
                    gScore[neighbor]   = tentativeGScore
                    fScore[neighbor]   = tentativeGScore + self.heuristic(neighbor, goalNode)

                    # Push onto openSet if not already in it
                    if not any(neighbor == node for _, node in openSet):
                        heapq.heappush(openSet, (fScore[neighbor], neighbor))

        # If no route is found
        return []

    def visitAll(self, fromLoc, toVisit, rover, mapHandler):
        """
        Finds a path from 'fromLoc' that visits each location in 'toVisit' 
        in some order, using repeated A* searches for each next closest target.
        (Sample implementation - you can adjust how you pick the next target.)
        """
        path = [fromLoc]
        if not toVisit:
            return path

        leftToVisit = set((loc.x, loc.y) for loc in toVisit)
        currentLoc = fromLoc

        while leftToVisit:
            closestLoc = None
            closestPath = None
            minDistance = float('inf')

            # Find the next reachable location with the shortest path
            for locCoord in leftToVisit:
                toLoc = self.coordToLocation(locCoord, mapHandler)
                tempPath = self.goTo(currentLoc, toLoc, rover, mapHandler)
                # If found a path and it's shorter than our current best
                if tempPath and (len(tempPath) - 1) < minDistance:
                    minDistance = len(tempPath) - 1
                    closestLoc = locCoord
                    closestPath = tempPath

            if closestLoc:
                # Append the new path (minus the duplicate start) to our total path
                path.extend(closestPath[1:])
                leftToVisit.remove(closestLoc)
                currentLoc = self.coordToLocation(closestLoc, mapHandler)
            else:
                # Can't reach any of the remaining targets
                break

        return path

    def cost(self, currentLoc, neighborLoc, rover):
        """
        Basic movement cost:
          - 1 "step" cost
          - plus additional cost if climbing up (positive altitude difference).
        """
        altitudeDiff = neighborLoc.altitude - currentLoc.altitude
        return 1 + max(0, altitudeDiff)

    def reconstructPath(self, cameFrom, current, mapHandler):
        """
        Reconstructs the path by walking backward from the 'goal' node 
        to the start node using 'cameFrom' dict, then reversing it.
        """
        path = [current]
        while current in cameFrom:
            current = cameFrom[current]
            path.append(current)
        path.reverse()

        # Convert (x, y) -> Location objects
        return [self.coordToLocation(coord, mapHandler) for coord in path]

    def heuristic(self, a, b):
        """
        A simple Manhattan distance heuristic. 
        Alternatively, you might consider diagonal moves or slope.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def coordToLocation(self, coord, mapHandler):
        """
        Convert a (x, y) tuple into a Location object via mapHandler.getLocationAt(...).
        This ensures we handle the new 3-element list [ (lat,lon), (elev,slope), obstacle ].
        """
        x, y = coord
        return mapHandler.getLocationAt(x, y)
