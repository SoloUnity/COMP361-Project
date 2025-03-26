import unittest
import sys
import os

projectRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(projectRoot, 'src/ai-algos'))

from MapHandler import MapHandler
from DFS import DFS
from Location import Location
from Rover import Rover

class DFSAlgorithmTests(unittest.TestCase):
    
    def setUp(self):
        self.roverHigh = Rover(30)
        self.roverLow = Rover(0)

    def testGoToHorizontal(self):
        mapData = [
            [[(0, 0), (0, 0), 0],
            [(0, 1), (1, 1), 0]]
        ]
        mapHandler = MapHandler(mapData)
        dfs = DFS()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc = Location(0, 1, 1, 1, 0)

        path = dfs.goTo(fromLoc, toLoc, self.roverLow, mapHandler)

        self.assertEqual(len(path), 2)
        self.assertEqual(path[0].y, 0)
        self.assertEqual(path[1].y, 1)

    def testGoToVertical(self):
        mapData = [
            [[(0, 0), (0, 0), 0],
            [(0, 1), (1, 1), 0],
            [(0, 2), (2, 2), 0],
            [(0, 3), (3, 3), 0]]
        ]
        mapHandler = MapHandler(mapData)
        dfs = DFS()
        fromLoc = Location(0, 1, 1, 1, 0)
        toLoc   = Location(0, 3, 3, 3, 0)
        
        pathLow  = dfs.goTo(fromLoc, toLoc, self.roverLow, mapHandler)
        
        self.assertEqual(len(pathLow), 3)
    
    def testGoToSimpleMultipleHorizontalSteps(self):
        mapData = [
            [[(0, 0), (0, 0), 0],
            [(0, 1), (1, 1), 0],
            [(0, 2), (2, 2), 0],
            [(0, 3), (3, 3), 0]]
        ]
        mapHandler = MapHandler(mapData)
        dfs = DFS()
        fromLoc = Location(0, 1, 1, 1, 0)
        toLoc   = Location(0, 3, 3, 3, 0)

        path = dfs.goTo(fromLoc, toLoc, self.roverLow, mapHandler)

        self.assertEqual(len(path), 3)
        self.assertEqual(path[0].y, 1)
        self.assertEqual(path[1].y, 2)
        self.assertEqual(path[2].y, 3)
        
    def testVisitAllSingleTarget(self):
        mapData = [
            [[(0, 0), (0, 0), 0],
            [(0, 1), (1, 1), 0]]
        ]
        mapHandler = MapHandler(mapData)
        dfs = DFS()
        fromLoc = Location(0, 0, 0, 0, 0)
        targetLoc = Location(0, 1, 1, 1, 0)

        path = dfs.visitAll(fromLoc, [targetLoc], self.roverLow, mapHandler)

        self.assertEqual(len(path), 2)
        self.assertEqual(path[0].y, 0)
        self.assertEqual(path[1].y, 1)
        
    def testVisitAllSingleTargetMultipleSteps(self):
        mapData = [
            [[(0, 0), (0, 0), 0],
            [(0, 1), (1, 1), 0],
            [(0, 2), (2, 2), 0],
            [(0, 3), (3, 3), 0]]
        ]
        mapHandler = MapHandler(mapData)
        dfs = DFS()
        fromLoc = Location(0, 1, 1, 1, 0)
        targetLoc = Location(0, 3, 3, 3, 0)

        path = dfs.visitAll(fromLoc, [targetLoc], self.roverLow, mapHandler)

        self.assertEqual(len(path), 3)
        self.assertEqual(path[0].y, 1)
        self.assertEqual(path[1].y, 2)
        self.assertEqual(path[2].y, 3)
        
    def testDFSVisitAllMultipleTargets(self):
        mapData = [
            [[(0, 0), (0, 0), 0],
            [(0, 1), (1, 1), 0],
            [(0, 2), (2, 2), 0],
            [(0, 3), (3, 3), 0]]
        ]
        mapHandler = MapHandler(mapData)
        dfs = DFS()
        fromLoc = Location(0, 1, 1, 1, 0)
        targetLoc1 = Location(0, 3, 3, 3, 0)
        targetLoc2 = Location(0, 0, 0, 0, 0)

        path = dfs.visitAll(fromLoc, [targetLoc2, targetLoc1], self.roverLow, mapHandler)

        self.assertEqual(len(path), 5)
        self.assertEqual(path[0].y, 1)
        self.assertEqual(path[1].y, 0)
        self.assertEqual(path[2].y, 1)
        self.assertEqual(path[3].y, 2)
        self.assertEqual(path[4].y, 3)
    
    def testDFSComplexGraphPathfinding(self):
        mapData = [
            [[(0, 0), (0, 0), 0], [(0, 1), (1, 1), 0], [(0, 2), (2, 2), 0]],
            [[(1, 0), (3, 3), 0], [(1, 1), (4, 4), 0], [(1, 2), (5, 5), 0]],
            [[(2, 0), (6, 6), 0], [(2, 1), (7, 7), 0], [(2, 2), (8, 8), 0]]
        ]
        mapHandler = MapHandler(mapData)
        dfs = DFS()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc   = Location(2, 2, 8, 8, 0)

        path = dfs.goTo(fromLoc, toLoc, self.roverLow, mapHandler)

        self.assertGreater(len(path), 0)
        self.assertEqual(path[0].x, 0)
        self.assertEqual(path[0].y, 0)
        self.assertEqual(path[-1].x, 2)
        self.assertEqual(path[-1].y, 2)
    
    def testAStarNoPath(self):
        mapData = [
            [
                [(0, 0), (0, 0), 0], [(0, 1), (1, 1), 0]
            ],
            [
                [(1, 0), (2, 2), 0], [(1, 1), (3, 3), 999]
            ]
        ]
        mapHandler = MapHandler(mapData)
        
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc   = Location(1, 1, 3, 3, 999)  # huge obstacle
        
        dfs = DFS()
        pathHigh = dfs.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        pathLow  = dfs.goTo(fromLoc, toLoc, self.roverLow, mapHandler)

        self.assertEqual(len(pathHigh), 0)
        self.assertEqual(len(pathLow), 0)

    def testAltitudeChangePrioritization(self):
        # 26.6 degrees slope test
        # altitude = 5 and distance = 10 meters
        mapData = [
            [
                [(0, 0), (0, 0), 0],
                [(0, 1), (0, 1), 5]
            ]
        ]

        mapHandler = MapHandler(mapData)
        dfs = DFS()
        
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc   = Location(0, 1, 0, 1, 5)

        pathHigh = dfs.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        self.assertTrue(pathHigh)
        self.assertEqual(len(pathHigh), 2)

        pathLow = dfs.goTo(fromLoc, toLoc, self.roverLow, mapHandler)
        self.assertFalse(pathLow)


if __name__ == '__main__':
    unittest.main()
