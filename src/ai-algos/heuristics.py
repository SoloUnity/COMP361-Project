#Author : Mathilde Peruzzo

from math import sqrt, sin, asin, tan, fsum
from MapHandler import MapHandler

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

def has_sunlight_obstacle(loc, mapHandler) :
    """
    Returns 0 if the location is exposed to the sun at midday, 1 otherwise
    Neglects the axial tilt of the planet and approximates the ground as a flat surface
    Only considers potential obstacles one kilometer away
    """
    sign = 1 if loc.lat > 0 else -1
    tanlat = sign * tan(loc.lat)
    # checks the the north-south direction towards the equator
    for i in range(1, 100) :
        loc1 = mapHandler.getLocationAt(loc.x, loc.y + sign * i)
        if sign != (1 if loc1.lat > 0 else -1) : return 0 # no obstacle if cross the equator

        alt_diff = altitude_difference(loc, loc1)
        if alt_diff != 0 and (10 * i)/alt_diff > tanlat : return 1
    return 0

def getMidPoint(loc1, loc2) :
    return (loc1.x + (loc2.x - loc1.x)//2, loc1.y + (loc2.y - loc1.y)//2)

def getEnergyForSlope(loc1, loc2, rover) :
    distance = euclidean_distance(loc1, loc2)
    if distance == 0 : return 0

    slope = abs(altitude_difference(loc1, loc2)) / distance
    if (0 <= slope and slope < rover.tanMidSlope) :
        return rover.lowSlopeEnergy
    elif (rover.tanMidSlope <= slope and slope < rover.tanHighSlope) :
        return rover.midSlopeEnergy
    else :
        return rover.highSlopeEnergy

def distance_h(path, loc, toLoc, rover, mapHandler, distance) :
    """
    Computes the distance travelled so far using the provided distance
    Estimates the distance to go by computing the distance between loc and toLoc
    """
    soFar = 0
    for i in range(len(path) - 1) :
        soFar += distance(path[i], path[i+1])
    if (len(path) > 0) : soFar += distance(path[len(path)-1], loc)
    toGo = distance(loc, toLoc)
    return soFar + toGo

def euclidean_distance_h(path, loc, toLoc, rover, mapHandler) :
    """
    Computes the distance travelled so far using the euclidean distance
    Estimates the distance to go by computing the distance between loc and toLoc
    """
    return distance_h(path, loc, toLoc, rover, mapHandler, euclidean_distance)

def manhattan_distance_h(path, loc, toLoc, rover, mapHandler) :
    """
    Computes the distance travelled so far using the Manhattan distance
    Estimates the distance to go by computing the distance between loc and toLoc
    """
    return distance_h(path, loc, toLoc, rover, mapHandler, manhattan_distance)

def geographical_distance_h(path, loc, toLoc, rover, mapHandler) :
    """
    Computes the distance travelled so far using the geographical distance
    Estimates the distance to go by computing the distance between loc and toLoc
    """
    return distance_h(path, loc, toLoc, rover, mapHandler, geographical_distance)

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
    soFar = (fsum(altitudes) + loc.altitude + toLoc.altitude)
    toGo = (loc.altitude + toLoc.altitude)/2
    return (soFar + toGo)/(len(path) + 3)

def solar_exposure_h(path, loc, toLoc, rover, mapHandler) :
    """
    Computes the number of location exposed to the sun on the provided path
    """
    exposures = map(lambda l : has_sunlight_obstacle(l, mapHandler), path)
    soFar = fsum(exposures) + has_sunlight_obstacle(loc, mapHandler)

    midx, midy = getMidPoint(loc, toLoc)
    toGo = has_sunlight_obstacle(mapHandler.getLocationAt(midx, midy), mapHandler)

    return soFar + toGo

def energy_consumption_h(path, loc, toLoc, rover, mapHandler) :
    """
    Computes the energy consumption for the provided path and rover
    Estimates the energy consumption for the remaining distance to toLoc
    """
    soFar = 0
    for i in range(len(path) - 1) :
        soFar += getEnergyForSlope(path[i], path[i+1], rover)
    if (len(path) > 0) : 
        soFar += getEnergyForSlope(path[len(path)-1], loc, rover)
    
    toGo = getEnergyForSlope(loc, toLoc, rover)

    return soFar + toGo
