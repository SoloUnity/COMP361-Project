import unittest
import os
import sys

projectRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(projectRoot, 'src/ai-algos'))

from MapHandler import MapHandler
from AStar import AStar
from Location import Location
from Rover import Rover

class TestAStarAlgorithm(unittest.TestCase):
    def setUp(self):
        # Initialize rover instances with different climbing abilities:
        # roverHigh can handle steep elevation changes,
        # roverLow is limited and should avoid moderate elevation bumps.
        self.roverHigh = Rover(45)  # High climbing ability
        self.roverLow = Rover(5)    # Low climbing ability

    def testGoToSimpleHorizontal(self):
        # Test horizontal movement on a flat, single-row grid.
        # Both rovers should yield the same optimal path.
        mapData = [[[0, 0, 0], [1, 1, 0]]]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc   = Location(0, 1, 1, 1, 0)
        
        pathHigh = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        pathLow  = astar.goTo(fromLoc, toLoc, self.roverLow, mapHandler)
        
        self.assertEqual(len(pathHigh), 2, "Expected a 2-node path for roverHigh.")
        self.assertEqual(len(pathLow), 2, "Expected a 2-node path for roverLow on flat terrain.")
        self.assertEqual(pathHigh[0].y, 0, "Start location should be at column 0 for roverHigh.")
        self.assertEqual(pathHigh[1].y, 1, "Goal location should be at column 1 for roverHigh.")

    def testGoToSimpleVertical(self):
        # Test vertical movement on a flat, single-column grid.
        # Both rovers should produce the same optimal path.
        mapData = [
            [[0, 0, 0], [1, 1, 0], [2, 2, 0], [3, 3, 0]]
        ]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 1, 1, 1, 0)
        toLoc   = Location(0, 3, 3, 3, 0)
        
        pathHigh = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        pathLow  = astar.goTo(fromLoc, toLoc, self.roverLow, mapHandler)
        
        self.assertEqual(len(pathHigh), 3, "Expected a 3-node path for roverHigh in vertical movement.")
        self.assertEqual(len(pathLow), 3, "Expected a 3-node path for roverLow in vertical movement.")

    def testVisitAllSingleTarget(self):
        # Test visiting a single target in a flat grid.
        # Both rovers should compute an identical route.
        mapData = [[[0, 0, 0], [1, 1, 0]]]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc   = Location(0, 0, 0, 0, 0)
        targetLoc = Location(0, 1, 1, 1, 0)
        
        pathHigh = astar.visitAll(fromLoc, [targetLoc], self.roverHigh, mapHandler)
        pathLow  = astar.visitAll(fromLoc, [targetLoc], self.roverLow, mapHandler)
        
        self.assertEqual(len(pathHigh), 2, "Expected a 2-node path for roverHigh on visitAll.")
        self.assertEqual(len(pathLow), 2, "Expected a 2-node path for roverLow on visitAll.")

    def testVisitAllMultipleTargets(self):
        # Test visiting multiple targets optimally in a flat grid.
        # Both rovers should compute the same overall path.
        mapData = [
            [[0, 0, 0], [1, 1, 0], [2, 2, 0], [3, 3, 0]]
        ]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 1, 1, 1, 0)
        target1 = Location(0, 3, 3, 3, 0)
        target2 = Location(0, 0, 0, 0, 0)
        
        pathHigh = astar.visitAll(fromLoc, [target2, target1], self.roverHigh, mapHandler)
        pathLow  = astar.visitAll(fromLoc, [target2, target1], self.roverLow, mapHandler)
        
        self.assertEqual(len(pathHigh), 5, "Expected a 5-node path for roverHigh on visitAll.")
        self.assertEqual(len(pathLow), 5, "Expected a 5-node path for roverLow on visitAll.")

    def testAStarShortestPath(self):
        # Test that A* finds the shortest path in a flat 3x4 grid.
        # Both rovers should compute the same optimal path.
        mapData = [
            [[0, 0, 0], [1, 1, 0], [2, 2, 0], [3, 3, 0]],
            [[4, 4, 0], [5, 5, 0], [6, 6, 0], [7, 7, 0]],
            [[8, 8, 0], [9, 9, 0], [10, 10, 0], [11, 11, 0]]
        ]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc   = Location(2, 3, 11, 11, 0)
        
        pathHigh = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        pathLow  = astar.goTo(fromLoc, toLoc, self.roverLow, mapHandler)
        
        self.assertLessEqual(len(pathHigh), 6, "Expected an optimal (short) path for roverHigh.")
        self.assertLessEqual(len(pathLow), 6, "Expected an optimal (short) path for roverLow on flat terrain.")

    def testAStarNoPath(self):
        # Map data: top-left corners are altitude=0,
        # bottom-right corner is altitude=999 => impassable for either rover.
        mapData = [
            [ [0, 0, 0],   [1, 1, 0]   ],
            [ [2, 2, 0],   [3, 3, 999] ]
        ]
        mapHandler = MapHandler(mapData)
        
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc   = Location(1, 1, 3, 3, 999)  # (x=1,y=1 in map indices) => altitude=999

        astar = AStar()

        pathHigh = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        pathLow  = astar.goTo(fromLoc, toLoc, self.roverLow,  mapHandler)

        self.assertEqual(len(pathHigh), 0, "No path should be found for roverHigh.")
        self.assertEqual(len(pathLow),  0, "No path should be found for roverLow.")

    def testAltitudeChangePrioritization(self):

        mapData = [
            [ [0, 0, 0], [0, 1, 1] ],
        ]
        mapHandler = MapHandler(mapData)

        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc   = Location(0, 1, 0, 1, 1)

        # Rover that can climb 45° should find a 2-cell path
        astar = AStar()
        pathHigh = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        self.assertTrue(pathHigh, "High-slope rover should succeed.")
        self.assertEqual(len(pathHigh), 2, "Path should be from (0,0) to (0,1) with no detours.")

        # Rover that can only handle ~5° slope should fail to climb
        pathLow = astar.goTo(fromLoc, toLoc, self.roverLow, mapHandler)
        self.assertFalse(pathLow, "Low-slope rover cannot climb 1 meter in 1 meter distance.")

if __name__ == '__main__':
    unittest.main()
