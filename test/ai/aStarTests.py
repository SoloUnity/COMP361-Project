import unittest
import os
import sys

# Set the project root and update import paths
projectRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(projectRoot, 'src/ai-algos'))

from MapHandler import MapHandler
from AStar import AStar
from Location import Location
from Rover import Rover

class TestAStarAlgorithm(unittest.TestCase):
    def setUp(self):
        # Initialize rover instances with different climbing abilities
        self.roverHigh = Rover(30)  # High climbing ability
        self.roverLow = Rover(5)    # Low climbing ability

    def testGoToSimpleHorizontal(self):
        # Test horizontal movement in a single-row grid
        mapData = [[[0, 0, 0], [1, 1, 0]]]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc = Location(0, 1, 1, 1, 0)
        path = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        self.assertEqual(len(path), 2, "Expected a path with 2 nodes.")
        self.assertEqual(path[0].y, 0, "Start location should be at column 0.")
        self.assertEqual(path[1].y, 1, "Goal location should be at column 1.")

    def testGoToSimpleVertical(self):
        # Test vertical movement in a single-row grid
        mapData = [[[0, 0, 0], [1, 1, 0], [2, 2, 0], [3, 3, 0]]]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 1, 1, 1, 0)
        toLoc = Location(0, 3, 3, 3, 0)
        path = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        self.assertEqual(len(path), 3, "Expected a 3-node path for horizontal movement.")

    def testVisitAllSingleTarget(self):
        # Test visiting a single target location
        mapData = [[[0, 0, 0], [1, 1, 0]]]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 0, 0, 0, 0)
        targetLoc = Location(0, 1, 1, 1, 0)
        path = astar.visitAll(fromLoc, [targetLoc], self.roverHigh, mapHandler)
        self.assertEqual(len(path), 2, "Expected a 2-node path.")

    def testVisitAllMultipleTargets(self):
        # Test visiting multiple target locations optimally
        mapData = [[[0, 0, 0], [1, 1, 0], [2, 2, 0], [3, 3, 0]]]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 1, 1, 1, 0)
        target1 = Location(0, 3, 3, 3, 0)
        target2 = Location(0, 0, 0, 0, 0)
        path = astar.visitAll(fromLoc, [target2, target1], self.roverHigh, mapHandler)
        self.assertEqual(len(path), 5, "Expected a 5-node path.")

    def testAStarWithObstacle(self):
        # Test A* pathfinding with an obstacle in a 3x3 grid
        mapData = [
            [[0, 0, 0], [1, 1, 0], [2, 2, 0]],
            [[3, 3, 0], [100, 100, 0], [5, 5, 0]],  # Obstacle at (1,1)
            [[6, 6, 0], [7, 7, 0], [8, 8, 0]]
        ]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc = Location(2, 2, 8, 8, 0)
        path = astar.goTo(fromLoc, toLoc, self.roverLow, mapHandler)
        self.assertGreater(len(path), 0, "A valid path should be found.")
        for loc in path:
            self.assertFalse(loc.x == 1 and loc.y == 1, "Path should avoid the obstacle.")

    def testAStarShortestPath(self):
        # Test A* finds the shortest path in a 3x3 grid
        mapData = [
            [[0, 0, 0], [1, 1, 0], [2, 2, 0], [3, 3, 0]],
            [[4, 4, 0], [5, 5, 0], [6, 6, 0], [7, 7, 0]],
            [[8, 8, 0], [9, 9, 0], [10, 10, 0], [11, 11, 0]]
        ]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc = Location(2, 3, 11, 11, 0)
        path = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        self.assertLessEqual(len(path), 6, "The path should be optimal.")

    def testAStarNoPath(self):
        # Test A* returns an empty path when no valid route exists
        mapData = [
            [[0, 0, 0], [1, 1, 0]],
            [[2, 2, 0], [100, 100, 0]]  # Impassable cell
        ]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc = Location(1, 1, 100, 100, 0)
        path = astar.goTo(fromLoc, toLoc, self.roverLow, mapHandler)
        self.assertEqual(len(path), 0, "No path should be found.")

if __name__ == '__main__':
    unittest.main()
