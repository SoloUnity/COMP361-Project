import heapq
import math

from Location import Location
from Pathfinder import PathFinder
from Node import Node

class AStar(PathFinder):

    def __init__(self, heuristic_func=None):
        if heuristic_func is None:
            # use heuristis manhattan_distance(loc1, loc2)
            self.heuristic_func = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])
        else:
            if not callable(heuristic_func):
                raise TypeError("heuristic_func must be a callable function")
            self.heuristic_func = heuristic_func

    def goTo(self, fromLoc, toLoc, rover, mapHandler):
        priorityQueue = []
        gScore = {}
        visited_coords = set()

        startCoord = (fromLoc.x, fromLoc.y)
        goalCoord = (toLoc.x, toLoc.y)

        startNode = Node(startCoord, None)
        start_h = self.heuristic_func(startCoord, goalCoord)
        gScore[startCoord] = 0
        heapq.heappush(priorityQueue, (start_h, startNode))

        while priorityQueue:
            current_f, currentNode = heapq.heappop(priorityQueue)
            currentCoord = currentNode.coord

            if currentCoord == goalCoord:
                return [fromLoc] + self.getPath(currentNode, mapHandler)

            if currentCoord in visited_coords:
                continue
            visited_coords.add(currentCoord)

            currentLocation = self.coordToLocation(currentCoord, mapHandler)
            current_g = gScore[currentCoord]

            for neighborCoord in mapHandler.getNeighbors(currentCoord[0], currentCoord[1]):
                if neighborCoord in visited_coords:
                    continue

                neighborLocation = self.coordToLocation(neighborCoord, mapHandler)

                if not rover.canTraverse(currentLocation, neighborLocation):
                    continue

                move_cost = self.cost(currentLocation, neighborLocation, rover)
                tentative_gScore = current_g + move_cost

                if neighborCoord not in gScore or tentative_gScore < gScore[neighborCoord]:
                    gScore[neighborCoord] = tentative_gScore
                    neighbor_h = self.heuristic_func(neighborCoord, goalCoord)
                    fScore = tentative_gScore + neighbor_h

                    neighborNode = Node(neighborCoord, currentNode)
                    heapq.heappush(priorityQueue, (fScore, neighborNode))

        return []

    def cost(self, currentLoc, neighborLoc, rover):
        altitudeDiff = neighborLoc.altitude - currentLoc.altitude
        base_distance = 1
        return base_distance + max(0, altitudeDiff)