from collections import deque
from Pathfinder import PathFinder
from Location import Location

class DFS(PathFinder):

    def goTo(self, fromLoc, toLoc, rover, mapHandler):

        stack = []
        visited = []

        stack.append(Node((fromLoc.x, fromLoc.y), None))
        while(len(stack) > 0):
            current = stack.pop()
            
            if current.coord not in visited:
                visited.append(current.coord)
                
                if (current.coord == (toLoc.x, toLoc.y)):
                    return [fromLoc] + self.getPath(current, mapHandler)
                
                cx, cy = current.coord
                for n in mapHandler.getNeighbors(cx, cy):
                    currentLoc = Location(cx, cy, mapHandler.map[cx][cy][0], mapHandler.map[cx][cy][1], mapHandler.map[cx][cy][2])
                    nLoc = Location(n[0], n[1], mapHandler.map[n[0]][n[1]][0], mapHandler.map[n[0]][n[1]][1], mapHandler.map[n[0]][n[1]][2])
                    if n not in visited and rover.canTraverse(currentLoc, nLoc):
                        stack.append(Node(n, current))
        
        return []

    def visitAll(self, fromLoc, toVisit, rover, mapHandler):
        
        path = [fromLoc]
        if (len(toVisit) == 0): return path

        leftToVisit = set(map(lambda loc: (loc.x, loc.y), toVisit))
        stack = []
        visited = []

        stack.append(Node((fromLoc.x, fromLoc.y), None))
        while(len(stack) > 0):
            current = stack.pop()  # Pop from the end LIFO
            
            if current.coord not in visited:
                visited.append(current.coord)
                
                if current.coord in leftToVisit:
                    leftToVisit.remove(current.coord)
                    path += self.getPath(current, mapHandler)
                    if (len(leftToVisit) == 0): return path

                    stack.clear()
                    visited.clear()
                    stack.append(Node(current.coord, None))
                else:
                    cx, cy = current.coord
                    for n in mapHandler.getNeighbors(cx, cy):
                        currentLoc = Location(cx, cy, mapHandler.map[cx][cy][0], mapHandler.map[cx][cy][1], mapHandler.map[cx][cy][2])
                        nLoc = Location(n[0], n[1], mapHandler.map[n[0]][n[1]][0], mapHandler.map[n[0]][n[1]][1], mapHandler.map[n[0]][n[1]][2])
                        if n not in visited and rover.canTraverse(currentLoc, nLoc):
                            stack.append(Node(n, current))

        return path

    def getPath(self, toLoc, mapHandler):
        path = []
        current = toLoc
        while current.parent != None:
            cx, cy = current.coord
            path.append(Location(cx, cy, mapHandler.map[cx][cy][0], mapHandler.map[cx][cy][1], mapHandler.map[cx][cy][2]))
            current = current.parent
        path.reverse()
        return path

class Node:
    def __init__(self, coord: (int, int), parent):
        self.coord = coord
        self.parent = parent