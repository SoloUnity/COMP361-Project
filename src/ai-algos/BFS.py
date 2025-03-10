from collections import deque
from Pathfinder import PathFinder
from Location import Location

class BFS(PathFinder):
    """
    Breadth-first search algorithm
    """

    def goTo(self, fromLoc, toLoc, rover, mapHandler):
        """
        Finds a path from fromLoc to toLoc in the provided submap and for the provided rover
            using BFS
        Returns a list of locations corresponding to the path

        fromLoc : Location
            the starting location
        toLoc : Location
            the destination
        rover : Rover
            the rover for which the method searches a path
        mapHandler : MapHandler
            handler for the map subsection the methods searches in
        """

        q = deque()
        visited = []

        q.append(Node((fromLoc.x, fromLoc.y), None))
        while(len(q) > 0) :
            current = q.popleft()
            visited.append(current.coord)
            if (current.coord == (toLoc.x, toLoc.y)) :
                return [fromLoc] + self.getPath(current, mapHandler)
            
            cx, cy = current.coord
            for n in mapHandler.getNeighbors(cx, cy):
                currentLoc = Location(cx, cy, mapHandler.map[cx][cy][0], mapHandler.map[cx][cy][1], mapHandler.map[cx][cy][2])
                nLoc = Location(n[0], n[1], mapHandler.map[n[0]][n[1]][0], mapHandler.map[n[0]][n[1]][1], mapHandler.map[n[0]][n[1]][2])
                if rover.canTraverse(currentLoc, nLoc) and n not in visited :
                    q.append(Node(n, current))
        
        return []

    def visitAll(self, fromLoc, toVisit, rover, mapHandler):
        """
        Finds a path from fromLoc that visits the locations in toVisit in the provided submap and for the provided rover
            using BFS
        Returns a list of locations corresponding to the path

        fromLoc : Location
            the starting location
        toVisit : List[Location]
            the destination
        rover : Rover
            the rover for which the method searches a path
        mapHandler : MapHandler
            handler for the map subsection the methods searches in
        """
        
        path = [fromLoc]
        if (len(toVisit) == 0) : return path

        leftToVisit = set(map(lambda loc : (loc.x, loc.y), toVisit))
        q = deque()
        visited = []

        q.append(Node((fromLoc.x, fromLoc.y), None))
        while(len(q) > 0) :
            current = q.popleft()
            visited.append(current.coord)
            if current.coord in leftToVisit :
                leftToVisit.remove(current.coord)
                path += self.getPath(current, mapHandler)
                if (len(leftToVisit) == 0) : return path

                # restart with current as the new fromLoc
                q.clear()
                visited.clear()
                q.append(Node(current.coord, None))

            else :
                cx, cy = current.coord
                for n in mapHandler.getNeighbors(cx, cy):
                    currentLoc = Location(cx, cy, mapHandler.map[cx][cy][0], mapHandler.map[cx][cy][1], mapHandler.map[cx][cy][2])
                    nLoc = Location(n[0], n[1], mapHandler.map[n[0]][n[1]][0], mapHandler.map[n[0]][n[1]][1], mapHandler.map[n[0]][n[1]][2])
                    if rover.canTraverse(currentLoc, nLoc) and n not in visited :
                        q.append(Node(n, current))

        return path

    def getPath(self, toLoc, mapHandler) :
        """
        Computes the path starting at toLoc following the parent of each Node (fromLoc is excluded)
        Returns a list of Locations

        toLoc : Node
        mapHandler : MapHandler
        """
        path = []
        current = toLoc
        while current.parent != None :
            cx, cy = current.coord
            path.append(Location(cx, cy, mapHandler.map[cx][cy][0], mapHandler.map[cx][cy][1], mapHandler.map[cx][cy][2]))
            current = current.parent
        path.reverse()
        return path

class Node :
    def __init__(self, coord : (int, int), parent) :
        self.coord = coord
        self.parent = parent
