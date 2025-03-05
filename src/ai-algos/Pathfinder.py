from Location import Location
from Rover import Rover
from MapHandler import MapHandler

class PathFinder:
    def goTo(self, fromLoc: Location, toLoc: Location, rover, mapHandler):
        raise NotImplementedError()
    
    def visitAll(self, fromLoc: Location, toVisit, rover, mapHandler):
        raise NotImplementedError()