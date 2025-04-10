import sys
import os
import time

projectRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(projectRoot, 'src/ai-algos'))
sys.path.append(os.path.join(projectRoot, 'src/util'))

mapFilePath = os.path.join(projectRoot, '../Mars_HRSC_MOLA_BlendDEM_Global_200mp_v2.tif')

from MapHandler import MapHandler
from Rover import Rover
from BFS import BFS
from DFS import DFS
from AStar import AStar
from dem_to_matrix import dem_to_matrix
from Location import Location
from heuristics import *

"""
To run : python tests/ai/aiWithMapTests.py
"""

def bfsOnMap() :
    matrix, new_transform = dem_to_matrix(mapFilePath, (5000, 4030), 100, 100)
    mH = MapHandler(matrix)
    fromLoc = mH.getLocationAt(10, 10)
    toLoc1 = mH.getLocationAt(10, 15)
    toLoc2 = mH.getLocationAt(12, 9)
    rover1 = Rover(5)
    rover2 = Rover(10)
    bfs = BFS()
    path1 = bfs.goTo(fromLoc, toLoc1, rover1, mH)
    path2 = bfs.goTo(fromLoc, toLoc1, rover2, mH)
    #path = bfs.visitAll(fromLoc, [toLoc1, toLoc2], rover, mH)
    print("Path 1 :")
    printPath(path1)
    print("Path 2 :")
    printPath(path2)

def dfsOnMap() :
    matrix, new_transform = dem_to_matrix(mapFilePath, (5000, 4030), 100, 100)
    mH = MapHandler(matrix)
    fromLoc = mH.getLocationAt(10, 10)
    toLoc1 = mH.getLocationAt(10, 15)
    toLoc2 = mH.getLocationAt(120, 9)
    rover = Rover(5) # with 10 a different path
    dfs = DFS()
    path = dfs.visitAll(fromLoc, [toLoc1, toLoc2], rover, mH)
    printPath(path)

def aStarOnMap() :
    matrix, new_transform = dem_to_matrix(mapFilePath, (5000, 4030), 100, 100)
    mH = MapHandler(matrix)
    fromLoc = mH.getLocationAt(10, 10)
    toLoc1 = mH.getLocationAt(10, 15)
    toLoc2 = mH.getLocationAt(12, 9)
    rover = Rover(8) # with 10 a different path
    aStar = AStar([(1, euclidean_distance_h)])
    path = aStar.visitAll(fromLoc, [toLoc1, toLoc2], rover, mH)
    printPath(path)

def heuristicsOnMap() :
    matrix, new_transform = dem_to_matrix(mapFilePath, (5000, 4030), 100, 100)
    mH = MapHandler(matrix)
    fromLoc = mH.getLocationAt(10, 10)
    toLoc1 = mH.getLocationAt(10, 15)
    toLoc2 = mH.getLocationAt(12, 9)
    loc = mH.getLocationAt(10, 14)
    rover = Rover(10, 1, 5, 10) # with 10 a different path
    bfs = BFS()
    path = bfs.goTo(fromLoc, toLoc1, rover, mH)
    print(euclidean_distance_h(path, loc, toLoc2, rover, mH))

def printPath(path) :
    for loc in path :
        loc.printLoc()

def algosOnSameMap() :
    matrix, new_transform = dem_to_matrix(mapFilePath, (5000, 4030), 2000, 2000)
    mH = MapHandler(matrix)
    print("Map loaded")

    print("--------------------------------------------------------------------------")

    fromLoc = mH.getLocationAt(10, 10)
    toLoc1 = mH.getLocationAt(10, 1500)
    toLoc2 = mH.getLocationAt(120, 9)
    rover = Rover(8) # with 10 a different path
    """

    print("Running BFS")
    bfs = BFS()
    start_time = time.time()
    bfs_path = bfs.visitAll(fromLoc, [toLoc1, toLoc2], rover, mH)
    print("BFS time : ", time.time() - start_time)
    printPath(bfs_path)

    print("--------------------------------------------------------------------------")

    print("Running DFS")
    bfs = DFS()
    start_time = time.time()
    dfs_path = bfs.visitAll(fromLoc, [toLoc1, toLoc2], rover, mH)
    print("DFS time : ", time.time() - start_time)
    #printPath(dfs_path)

    print("--------------------------------------------------------------------------")
    """

    print("Running aStar")
    aStar = AStar([(1, euclidean_distance_h)])
    start_time = time.time()
    astar_path = aStar.visitAll(fromLoc, [toLoc1, toLoc2], rover, mH)
    print("BFS time : ", time.time() - start_time)
    printPath(astar_path)

if __name__ == "__main__":
    #algosOnSameMap()
    aStarOnMap()
    #heuristicsOnMap()