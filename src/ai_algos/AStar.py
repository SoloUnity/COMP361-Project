import heapq
from Location import Location
from Pathfinder import PathFinder
from Node import Node
from heuristics import manhattan_distance


class AStar(PathFinder):
    def __init__(self, heuristic_funcs=None):
        if heuristic_funcs is None:
            self.heuristic_funcs = [(1, manhattan_distance)]
        else:
            self.heuristic_funcs = heuristic_funcs
            for tuple in self.heuristic_funcs:
                if not callable(tuple[1]):
                    raise TypeError(f"{tuple[1]} must be a callable function")
    
    def goTo(self, fromLoc, toLoc, rover, mapHandler):
        priorityQueue = []
        gScore = {}
        visited_coords = set()
        
        startCoord = (fromLoc.x, fromLoc.y)
        goalCoord = (toLoc.x, toLoc.y)
        
        startNode = Node(startCoord, None)
        
        # Calculate initial heuristic value using all heuristic functions
        start_h = 0
        for tuple in self.heuristic_funcs:
            if tuple[1].__name__.endswith('_h'):
                start_h += tuple[0] * tuple[1]([], fromLoc, toLoc, rover, mapHandler)
            else:
                start_h += tuple[0] * tuple[1](fromLoc, toLoc)
        
        gScore[startCoord] = 0
        heapq.heappush(priorityQueue, (start_h, startNode))
        
        while priorityQueue:
            current_f, currentNode = heapq.heappop(priorityQueue)
            currentCoord = currentNode.coord
            
            if currentCoord == goalCoord:
                path = self.getPath(currentNode, mapHandler)
                return [fromLoc] + path
            
            if currentCoord in visited_coords:
                continue
                
            visited_coords.add(currentCoord)
            currentLocation = self.coordToLocation(currentCoord, mapHandler)
            current_g = gScore[currentCoord]
            
            path_so_far = self.getPath(currentNode, mapHandler)
            
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
                    
                    neighborNode = Node(neighborCoord, currentNode)
                    
                    # Calculate combined heuristic value for neighbor
                    neighbor_h = 0
                    for tuple in self.heuristic_funcs:
                        if tuple[1].__name__.endswith('_h'):
                            # Path-based heuristic
                            neighbor_h += tuple[0] * tuple[1](path_so_far, neighborLocation, toLoc, rover, mapHandler)
                        else:
                            # Simple distance heuristic
                            neighbor_h += tuple[0] * tuple[1](neighborLocation, toLoc)
                    
                    fScore = tentative_gScore + neighbor_h
                    heapq.heappush(priorityQueue, (fScore, neighborNode))
        
        return []
    
    def cost(self, currentLoc, neighborLoc, rover):
        altitudeDiff = neighborLoc.altitude - currentLoc.altitude
        base_distance = 1
        return base_distance + max(0, altitudeDiff)