import heapq
import math

from Location import Location
from Pathfinder import PathFinder

class AStar(PathFinder):

    def goTo(self, fromLoc, toLoc, rover, mapHandler):
        openSet = []
        gScore = {}
        fScore = {}
        cameFrom = {}

        startNode = (fromLoc.x, fromLoc.y)
        goalNode  = (toLoc.x, toLoc.y)

        # Push the start node into the priority queue.
        heapq.heappush(openSet, (self.heuristic(startNode, goalNode), startNode))
        gScore[startNode] = 0
        fScore[startNode] = self.heuristic(startNode, goalNode)

        closedSet = set()

        while openSet:
            _, current = heapq.heappop(openSet)
            if current == goalNode:
                # Goal reached – reconstruct the path!
                return self.reconstructPath(cameFrom, current, mapHandler)

            closedSet.add(current)
            cx, cy = current
            currentLoc = self.coordToLocation(current, mapHandler)

            # Check all valid neighbors
            for neighbor in mapHandler.getNeighbors(cx, cy):
                if neighbor in closedSet:
                    continue

                neighborLoc = self.coordToLocation(neighbor, mapHandler)
                
                # If the rover can't traverse from current to neighbor, skip.
                if not rover.canTraverse(currentLoc, neighborLoc):
                    continue

                # Compute G-score if we take this step
                tentativeGScore = gScore[current] + self.cost(currentLoc, neighborLoc, rover)
                if (neighbor not in gScore) or (tentativeGScore < gScore[neighbor]):
                    cameFrom[neighbor] = current
                    gScore[neighbor]   = tentativeGScore
                    fScore[neighbor]   = tentativeGScore + self.heuristic(neighbor, goalNode)

                    # Only push onto openSet if not already there
                    # (or you could just push duplicates and let the fScore check weed them out)
                    if not any(neighbor == node for _, node in openSet):
                        heapq.heappush(openSet, (fScore[neighbor], neighbor))

        # If we exhaust the open set, no route was found.
        return []

    def cost(self, currentLoc, neighborLoc, rover):
        """
        Basic movement cost:
          - 1 "step" cost
          - plus any positive altitude climb
        """
        altitudeDiff = neighborLoc.altitude - currentLoc.altitude
        return 1 + max(0, altitudeDiff)

    def reconstructPath(self, cameFrom, current, mapHandler):
        path = [current]
        while current in cameFrom:
            current = cameFrom[current]
            path.append(current)
        path.reverse()

        # Convert (x, y) back to Location objects
        return [
            self.coordToLocation(coord, mapHandler)
            for coord in path
        ]

    def visitAll(self, fromLoc, toVisit, rover, mapHandler):
        """
        Example routine that tries to 'visitAll' locations in some minimal path order.
        (Not used by the given tests but included for completeness.)
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

            for locCoord in leftToVisit:
                toLoc = self.coordToLocation(locCoord, mapHandler)
                tempPath = self.goTo(currentLoc, toLoc, rover, mapHandler)
                # If we found a path and it's shorter than all known so far
                if tempPath and (len(tempPath) - 1) < minDistance:
                    minDistance = len(tempPath) - 1
                    closestLoc = locCoord
                    closestPath = tempPath

            if closestLoc:
                # Extend the overall path (skipping the duplicated start of new path)
                path.extend(closestPath[1:])
                leftToVisit.remove(closestLoc)
                currentLoc = self.coordToLocation(closestLoc, mapHandler)
            else:
                # If we can't reach any remaining location, break out (partial or no coverage).
                break

        return path

    def heuristic(self, a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def coordToLocation(self, coord, mapHandler):
        x, y = coord
        cell = mapHandler.map[x][y]  # e.g. [ originalX, originalY, altitude ]
        return Location(x, y, cell[0], cell[1], cell[2])

    # def canTraverseAltitudeOnly(self, currentLoc, neighborLoc, maxClimb):
    #     if (neighborLoc.altitude - currentLoc.altitude) > maxClimb:
    #         return False
    #     return True
