from Location import Location

class Rover:
    def __init__(self, maxSlope = 30.0):
        self.maxSlope = maxSlope
        import math
        self._tanMaxSlope = math.tan(math.radians(maxSlope))
    
    def canTraverse(self, fromLoc, toLoc):
        distance = ((fromLoc.x - toLoc.x)**2 + (fromLoc.y - toLoc.y)**2)**0.5
        if distance == 0:
            return True
        slope = abs(fromLoc.altitude - toLoc.altitude) / distance
        return slope <= self._tanMaxSlope