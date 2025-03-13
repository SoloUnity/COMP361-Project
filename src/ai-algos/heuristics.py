from math import sqrt, sin, asin
import math

def euclidean_distance(loc1, loc2) :
    """
    Computes the euclidean distance based on the coordinates of the locations in the map (their indices in the matrix)
    This method considers that the map has a point every 10 meters
    """
    return 10 * sqrt(((loc1.x - loc2.x)**2 + (loc1.y - loc2.y)**2))

def manhattan_distance(loc1, loc2) :
    """
    Computes a modified version of the Manhattan distance based on the coordinates of the 
        locations in the map (their indices in the matrix)
    This version accounts for the fact that rovers can move diagonally in the map
    """
    diagonal = min(abs(loc1.x - loc2.x), abs(loc1.y - loc2.y))
    horizontal= abs(loc1.x - loc2.x) - diagonal
    vertical = abs(loc1.y - loc2.y) - diagonal
    return diagonal + horizontal + vertical

def geographical_distance(loc1, loc2) :
    """
    Computes the distance according to spherical geometry using the Haversine formula
    """
    r = 3389000 # meters
    hav = (1-cos(loc1.lat - loc2.lat))/2 + cos(loc1.lat) * cos(loc1.lat) * (1-cos(loc1.lon - loc2.lon))/2
    return 2 * r * asin(sqrt(hav))

def altitude_difference(loc1, loc2) :
    return loc2.altitude - loc1.altitude

def north_south_slope(loc, mapHandler) :
    """
    Computes the slope on the north-south axis for the provided location
    """
    newY = loc.y
    if (loc.lat > 0 and mapHandler.isValidLocation(loc.x, loc.y-1)) :
        newY -= 1
    elif (loc.lat < 0 and mapHandler.isValidLocation(loc.x, loc.y+1)) :
        newY += 1
    return (mapHandler.getAltitude(loc.x, loc.y) - mapHandler.getAltitude(loc.x, newY)) / 10

def distance_h(path, loc, toLoc, rover, mapHandler) :
    """
    Computes the distance travelled so far using the euclidean distance
    Estimates the distance to go by computing the euclidean distance between loc and toLoc
    """
    soFar = 0
    for i in range(len(path) - 1) :
        soFar += euclidean_distance(path[i], path[i+1])
    soFar += euclidean_distance(path[len(path)-1], loc)
    toGo = euclidean_distance(loc, toLoc)
    return soFar + toGo

def stable_altitude_h(path, loc, toLoc, rover, mapHandler) :
    """
    Computes the average altitude change for each move in the provided path
    Estimates the average altitude change in the path to go by taking the altitude difference between 
        loc and toLoc and dividing by the modified Manhattan distance
    """
    soFar = 0
    if (len(path) > 0): # avoid dividing by zero
        for i in range(len(path) - 1) :
            soFar += abs(altitude_difference(path[i], path[i+1]))
        soFar += abs(altitude_difference(path[len(path)-1], loc))
        soFar = soFar / len(path)
    toGo = abs(altitude_difference(loc, toLoc)) / manhattan_distance(loc, toLoc)
    return soFar + toGo

def avg_altitude_h(path, loc, toLoc, rover, mapHandler) :
    """
    Computes the average altitude of the provided path, loc and toLoc
    Estimates the average altitude of the path to go by taking the middle value between loc.altitude and toLoc.altitude
    Favors paths that with low altitudes
    """
    altitudes = map(lambda l : l.altitude, path)
    soFar = (math.fsum(altitudes) + loc.altitude + toLoc.altitude) / (len(path) + 2)
    toGo = (loc.altitude + toLoc.altitude) / 2
    return (soFar + toGo)/2

def solar_exposure_h(path, loc, toLoc, rover, mapHandler) :
    exposures = map(lambda l : north_south_slope(l, mapHandler))
    soFar = (math.fsum(exposures) + north_south_slope(loc) + north_south_slope(toLoc)) / (len(path) + 2) 
    return soFar

def heuristic(path, loc, toLoc, rover, mapHandler) :
    """
    TODO : parameterize the coefficients
    path : list[Location]
    loc : Location
        location being evaluated by the heuristic
    toLoc : Location
        destination to reach
    rover : Rover
    mapHandler : MapHandler
    """
    return 2 * distance_h(path, loc, toLoc, rover, mapHandler) \
        + stable_altitude_h(path, loc, t, rover, mapHandler) \
        + avg_altitude_h(path, loc, toLoc, rover, mapHandler)
