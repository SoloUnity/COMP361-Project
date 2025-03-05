from math import sqrt, sin, asin

def euclidean_distance(loc1, loc2) :
    """
    Computes the euclidean distance based on the coordinates of the locations in the map (their indices in the matrix)
    This method considers that the map has a point every 10 meters
    """
    return 10 * sqrt(((loc1.x - loc2.x)**2 + (loc1.y - loc2.y)**2))

def manhattan_distance(loc1, loc2) :
    """
    Computes the Manhattan distance based on the coordinates of the locations in the map (their indices in the matrix)
    This method considers that the map has a point every 10 meters
    """
    return 10 * (abs(loc1.x - loc2.x) + abs(loc1.y - loc2.y))

def physical_distance(loc1, loc2) :
    """
    Computes the distance according to spherical geometry using the Haversine formula
    """
    r = 3389000 # meters
    hav = (1-cos(loc1.lat - loc2.lat))/2 + cos(loc1.lat) * cos(loc1.lat) * (1-cos(loc1.lon - loc2.lon))/2
    return 2 * r * asin(sqrt(hav))

def altitude_difference(loc1, loc2) :
    return loc2.altitude - loc1.altitude

def distance_heuristic(fromLoc, loc, toLoc, distance) :
    return distance(fromLoc, loc) + distance(loc, toLoc)

