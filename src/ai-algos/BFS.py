from collections import deque
from Pathfinder import PathFinder
from Location import Location

class BFS(PathFinder):

    def goTo(self, fromLoc, toLoc, rover, mapHandler):
        q = deque()
        visited = []

        q.append(Node((fromLoc.x, fromLoc.y), None))
        while(len(q) > 0) :
            current = q.popleft()
            visited.append(current.coord)
            if (current.coord == (toLoc.x, toLoc.y)) :
                return self.getPath(current, mapHandler)
            
            cx, cy = current.coord
            for n in mapHandler.getNeighbors(cx, cy):
                currentLoc = Location(cx, cy, mapHandler.map[cx][cy][0], mapHandler.map[cx][cy][1], mapHandler.map[cx][cy][2])
                nLoc = Location(n[0], n[1], mapHandler.map[n[0]][n[1]][0], mapHandler.map[n[0]][n[1]][1], mapHandler.map[n[0]][n[1]][2])
                if n not in visited : # and rover.canTraverse(currentLoc, nLoc)
                    q.append(Node(n, current))
        
        return []

    def visitAll(self, fromLoc, toVisit, rover, mapHandler):
        if (len(toVisit) == 0) : return [fromLoc]

        leftToVisit = set(map(lambda loc : (loc.x, loc.y), toVisit))
        q = deque()
        visited = []
        path = []

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
                    if n not in visited : # and rover.canTraverse(currentLoc, nLoc)
                        q.append(Node(n, current))

        return path

    def getPath(self, toLoc, mapHandler) :
        path = []
        current = toLoc
        while current != None :
            cx, cy = current.coord
            path.append(Location(cx, cy, mapHandler.map[cx][cy][0], mapHandler.map[cx][cy][1], mapHandler.map[cx][cy][2]))
            current = current.parent
        path.reverse()
        return path

class Node :
    def __init__(self, coord : (int, int), parent) :
        self.coord = coord
        self.parent = parent
