class Location:
    def __init__(self, x: int, y: int, lon: float, lat: float, altitude: float):
        self.x = x
        self.y = y
        self.lon = lon
        self.lat = lat
        self.altitude = altitude

    def printLoc(self) :
        print("({0}, {1}, {2}) at ({3}, {4}) in the map"\
                .format(self.lon, self.lat, self.altitude, self.x, self.y))
