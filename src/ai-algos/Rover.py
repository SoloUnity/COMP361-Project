from Location import Location
from heuristics import euclidean_distance

class Rover:
    def __init__(self, maxSlope = 30.0):
        self.maxSlope = maxSlope
        import math
        self._tanMaxSlope = math.tan(math.radians(maxSlope))
    
    def canTraverse(self, fromLoc, toLoc):
        distance = euclidean_distance(fromLoc, toLoc)
        if distance == 0:
            return True
        slope = abs(fromLoc.altitude - toLoc.altitude) / distance
        return slope <= self._tanMaxSlope