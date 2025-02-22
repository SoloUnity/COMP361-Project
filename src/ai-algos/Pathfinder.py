from Location import Location
from Rover import Rover
from MapHandler import MapHandler

class PathFinder:
    def goTo(self, fromLoc, toLoc, rover, mapHandler):
        raise NotImplementedError()
    
    def visitAll(self, fromLoc, toVisit, rover, mapHandler):
        raise NotImplementedError()