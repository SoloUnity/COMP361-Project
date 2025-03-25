import sys
sys.path.append('../../src/ai-algos')
sys.path.append('../../src/util')

from MapHandler import MapHandler
from Rover import Rover
from BFS import BFS
from dem_to_matrix import dem_to_matrix
from Location import Location
from heuristics import *

def bfsOnMap() :
    matrix, new_transform = dem_to_matrix("./../../../Mars_HRSC_MOLA_BlendDEM_Global_200mp_v2.tif", (5000, 4030), 100, 100)
    mH = MapHandler(matrix)
    fromLoc = mH.getLocationAt(10, 10)
    toLoc1 = mH.getLocationAt(10, 15)
    toLoc2 = mH.getLocationAt(12, 9)
    rover = Rover(8) # with 10 a different path
    bfs = BFS()
    #path = bfs.goTo(fromLoc, toLoc1, rover, mH)
    path = bfs.visitAll(fromLoc, [toLoc1, toLoc2], rover, mH)
    printPath(path)

def heuristicsOnMap() :
    matrix, new_transform = dem_to_matrix("./../../../Mars_HRSC_MOLA_BlendDEM_Global_200mp_v2.tif", (5000, 4030), 100, 100)
    mH = MapHandler(matrix)
    fromLoc = mH.getLocationAt(10, 10)
    toLoc1 = mH.getLocationAt(10, 15)
    toLoc2 = mH.getLocationAt(12, 9)
    loc = mH.getLocationAt(10, 14)
    rover = Rover(10) # with 10 a different path
    bfs = BFS()
    path = bfs.goTo(fromLoc, toLoc1, rover, mH)
    print(distance_h(path, loc, toLoc2, rover, mH))

def printPath(path) :
    for loc in path :
        loc.printLoc()

if __name__ == "__main__":
    #bfsOnMap()
    heuristicsOnMap()