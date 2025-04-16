from .Location import Location
import math
from .heuristics import euclidean_distance

class Rover:

    def __init__(self, maxSlope = 30.0, lowSlopeEnergy = 0.0, midSlopeEnergy = 0.0, highSlopeEnergy = 0.0):
        self.maxSlope = maxSlope
        self.lowSlopeEnergy = lowSlopeEnergy
        self.midSlopeEnergy = midSlopeEnergy
        self.highSlopeEnergy = highSlopeEnergy

        self._tanMaxSlope = math.tan(math.radians(maxSlope))
        self.tanHighSlope = math.tan(2 * maxSlope/3)
        self.tanMidSlope = math.tan(maxSlope/3)
    
    def canTraverse(self, fromLoc, toLoc):
        distance = euclidean_distance(fromLoc, toLoc)
        if distance == 0:
            return True
        slope = abs(fromLoc.altitude - toLoc.altitude) / distance
        return slope <= self._tanMaxSlope