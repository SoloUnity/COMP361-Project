from Location import Location
import math
from heuristics import euclidean_distance

class Rover:

    def __init__(self, maxSlope = 30.0):
        self.maxSlope = maxSlope
        self._tanMaxSlope = math.tan(math.radians(maxSlope))
    
    # Angle based approach to determine if the rover can traverse from one location to another
    def canTraverse(self, fromLoc, toLoc):
        distance = euclidean_distance(fromLoc, toLoc)
        if distance == 0:
            return True
        slope = 100 * abs(fromLoc.altitude - toLoc.altitude) / distance
        return slope <= self._tanMaxSlope