import heapq
import math

from Location import Location
from Pathfinder import PathFinder
from Node import Node

class AStar(PathFinder):

    def goTo(self, fromLoc, toLoc, rover, mapHandler):
        priorityQueue = []
        gScore = {} # g(n), cost from start to n
        fScore = {} # f(n), g(n) + h(n)

        startNode = Node((fromLoc.x, fromLoc.y), None)  # changed to use Node
        goalNode  = (toLoc.x, toLoc.y)

        # start node
        heapq.heappush(priorityQueue, (self.heuristic(startNode.coord, goalNode), startNode))
        gScore[startNode.coord] = 0
        fScore[startNode.coord] = self.heuristic(startNode.coord, goalNode)

        visited = set()

        while priorityQueue:
            _, current = heapq.heappop(priorityQueue)

            # reached the goal coordinate, reconstruct the path from the end
            if current.coord == goalNode:
                return self.getPath(current, mapHandler)

            visited.add(current.coord)
            cx, cy = current.coord
            currentLoc = self.coordToLocation(current.coord, mapHandler)

            # check all neighbours
            for neighbour in mapHandler.getNeighbors(cx, cy):
                if neighbour in visited:
                    continue

                neighbourLoc = self.coordToLocation(neighbour, mapHandler)

                # check if the rover can traverse to the neighbour
                if not rover.canTraverse(currentLoc, neighbourLoc):
                    continue

                # computing best known cost so far + cost of going to neighbour

                tentativeGScore = gScore[current.coord] + self.cost(currentLoc, neighbourLoc, rover)
                # if new path is better
                if (neighbour not in gScore) or (tentativeGScore < gScore[neighbour]):
                    gScore[neighbour]   = tentativeGScore
                    fScore[neighbour]   = tentativeGScore + self.heuristic(neighbour, goalNode) # f(n) = g(n) + h(n)

                    # push to prioQ if not already in it
                    if not any(neighbour == node.coord for _, node in priorityQueue):
                        heapq.heappush(priorityQueue, (fScore[neighbour], Node(neighbour, current)))

        # no path found
        return []

    def visitAll(self, fromLoc, toVisit, rover, mapHandler):
        path = [fromLoc]
        if not toVisit:
            return path

        leftToVisit = set((loc.x, loc.y) for loc in toVisit)
        currentLoc = fromLoc

        while leftToVisit:
            closestLoc = None
            closestPath = None
            minDistance = float('inf')

            # find the next reachable location with the shortest path
            for locCoord in leftToVisit:
                toLoc = self.coordToLocation(locCoord, mapHandler)
                tempPath = self.goTo(currentLoc, toLoc, rover, mapHandler)
                # if found a path shorter than our current best
                if tempPath and (len(tempPath) - 1) < minDistance:
                    minDistance = len(tempPath) - 1
                    closestLoc = locCoord
                    closestPath = tempPath

            if closestLoc:
                # append the new path without the duplicate start to our total path
                path.extend(closestPath[1:])
                leftToVisit.remove(closestLoc)
                currentLoc = self.coordToLocation(closestLoc, mapHandler)
            else:
                # cant reach any more locations
                break

        return path

    def cost(self, currentLoc, neighborLoc, rover):
        altitudeDiff = neighborLoc.altitude - currentLoc.altitude
        return 1 + max(0, altitudeDiff)

    def heuristic(self, a, b):
        # current heuristic is Manhattan distance
        # TODO experiment with other heuristics
        # TODO use heuristic function from heuristics.py
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def coordToLocation(self, coord, mapHandler):
        x, y = coord
        return mapHandler.getLocationAt(x, y)

    def getPath(self, current, mapHandler):
        path = []
        while current is not None:
            path.append(current.coord)
            current = current.parent
        path.reverse()

        # convert (x, y) tuples to Location objects
        return [self.coordToLocation(coord, mapHandler) for coord in path]
