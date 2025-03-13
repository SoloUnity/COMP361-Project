from Pathfinder import PathFinder
from Location import Location
import heapq
import math

class AStar(PathFinder):

    def goTo(self, fromLoc, toLoc, rover, mapHandler):
        openSet = []
        gScore = {}
        fScore = {}
        cameFrom = {}
        
        startNode = (fromLoc.x, fromLoc.y)
        goalNode = (toLoc.x, toLoc.y)
        
        heapq.heappush(openSet, (self.heuristic(startNode, goalNode), startNode))
        gScore[startNode] = 0
        fScore[startNode] = self.heuristic(startNode, goalNode)
        
        closedSet = set()
        
        while openSet:
            _, current = heapq.heappop(openSet)
            
            if current == goalNode:
                return self.reconstructPath(cameFrom, current, mapHandler)
            
            closedSet.add(current)
            cx, cy = current
            currentLoc = Location(cx, cy,
                                  mapHandler.map[cx][cy][0],
                                  mapHandler.map[cx][cy][1],
                                  mapHandler.map[cx][cy][2])
            
            for neighbor in mapHandler.getNeighbors(cx, cy):
                if neighbor in closedSet:
                    continue
                
                nx, ny = neighbor
                neighborLoc = Location(nx, ny,
                                       mapHandler.map[nx][ny][0],
                                       mapHandler.map[nx][ny][1],
                                       mapHandler.map[nx][ny][2])
                
                if not rover.canTraverse(currentLoc, neighborLoc):
                    continue
                
                tentativeGScore = gScore[current] + 1
                
                if neighbor not in gScore or tentativeGScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentativeGScore
                    fScore[neighbor] = tentativeGScore + self.heuristic(neighbor, goalNode)
                    
                    if not any(neighbor == node for _, node in openSet):
                        heapq.heappush(openSet, (fScore[neighbor], neighbor))
        
        return []

    def reconstructPath(self, cameFrom, current, mapHandler):
        totalPath = [current]
        while current in cameFrom:
            current = cameFrom[current]
            totalPath.append(current)
        totalPath.reverse()
        # Convert each coordinate to a Location object using the map data.
        return [Location(x, y,
                         mapHandler.map[x][y][0],
                         mapHandler.map[x][y][1],
                         mapHandler.map[x][y][2])
                for (x, y) in totalPath]

    def visitAll(self, fromLoc, toVisit, rover, mapHandler):
        path = [fromLoc]
        if len(toVisit) == 0:
            return path
        
        leftToVisit = set(map(lambda loc: (loc.x, loc.y), toVisit))
        currentLoc = fromLoc
        
        while leftToVisit:
            closestLoc = None
            closestPath = None
            minDistance = float('inf')
            
            for locCoord in leftToVisit:
                toLoc = self.coordToLocation(locCoord, mapHandler)
                tempPath = self.goTo(currentLoc, toLoc, rover, mapHandler)
                
                if tempPath and (len(tempPath) - 1) < minDistance:
                    minDistance = len(tempPath) - 1
                    closestLoc = locCoord
                    closestPath = tempPath
            
            if closestLoc:
                # Exclude the starting location of closestPath since it's already included.
                path.extend(closestPath[1:])
                leftToVisit.remove(closestLoc)
                currentLoc = self.coordToLocation(closestLoc, mapHandler)
            else:
                break
        
        return path

    def heuristic(self, a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def coordToLocation(self, coord, mapHandler):
        x, y = coord
        return Location(x, y,
                        mapHandler.map[x][y][0],
                        mapHandler.map[x][y][1],
                        mapHandler.map[x][y][2])
