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
        # Percentage based approach:
        # A 1 m altitude change over 10 m horizontal (each coordinate is 10 m apart) results in a 10% slope.
        self.roverHigh = Rover(10)
        self.roverLow = Rover(0)

    def testGoToSimpleHorizontal(self):
        mapData = [
            [
                [(0,0), 0],
                [(1,1), 0]
            ]
        ]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc   = Location(0, 1, 1, 1, 0)
        
        pathHigh = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        pathLow  = astar.goTo(fromLoc, toLoc, self.roverLow, mapHandler)
        
        self.assertEqual(len(pathHigh), 2)
        self.assertEqual(len(pathLow), 2)
        self.assertEqual(pathHigh[0].y, 0)
        self.assertEqual(pathHigh[1].y, 1)

    def testGoToSimpleVertical(self):
        mapData = [
            [
                [(0,0), 0],
                [(1,1), 0],
                [(2,2), 0],
                [(3,3), 0]
            ]
        ]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 1, 1, 1, 0)
        toLoc   = Location(0, 3, 3, 3, 0)
        
        pathHigh = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        pathLow  = astar.goTo(fromLoc, toLoc, self.roverLow, mapHandler)
        
        self.assertEqual(len(pathHigh), 3)
        self.assertEqual(len(pathLow), 3)

    def testVisitAllSingleTarget(self):
        mapData = [
            [
                [(0,0), 0],
                [(1,1), 0]
            ]
        ]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 0, 0, 0, 0)
        targetLoc = Location(0, 1, 1, 1, 0)
        
        pathHigh = astar.visitAll(fromLoc, [targetLoc], self.roverHigh, mapHandler)
        pathLow  = astar.visitAll(fromLoc, [targetLoc], self.roverLow, mapHandler)
        
        self.assertEqual(len(pathHigh), 2)
        self.assertEqual(len(pathLow), 2)

    def testVisitAllMultipleTargets(self):
        mapData = [
            [
                [(0,0), 0],
                [(1,1), 0],
                [(2,2), 0],
                [(3,3), 0]
            ]
        ]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 1, 1, 1, 0)
        target1 = Location(0, 3, 3, 3, 0)
        target2 = Location(0, 0, 0, 0, 0)
        
        pathHigh = astar.visitAll(fromLoc, [target2, target1], self.roverHigh, mapHandler)
        pathLow  = astar.visitAll(fromLoc, [target2, target1], self.roverLow, mapHandler)
        
        self.assertEqual(len(pathHigh), 5)
        self.assertEqual(len(pathLow), 5)

    def testAStarShortestPath(self):
        mapData = [
            [
                [(0,0), 0],   [(1,1), 0],
                [(2,2), 0],   [(3,3), 0]
            ],
            [
                [(4,4), 0],   [(5,5), 0],
                [(6,6), 0],   [(7,7), 0]
            ],
            [
                [(8,8), 0],   [(9,9), 0],
                [(10,10), 0], [(11,11), 0]
            ]
        ]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc   = Location(2, 3, 11, 11, 0)  # bottom-right corner

        pathHigh = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        pathLow  = astar.goTo(fromLoc, toLoc, self.roverLow, mapHandler)
        
        self.assertLessEqual(len(pathHigh), 6)
        self.assertLessEqual(len(pathLow), 6)

    def testAStarNoPath(self):
        mapData = [
            [
                [(0,0), 0],    [(1,1), 0]
            ],
            [
                [(2,2), 0],    [(3,3), 999]
            ]
        ]
        mapHandler = MapHandler(mapData)
        
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc   = Location(1, 1, 3, 3, 999)  # huge obstacle
        
        astar = AStar()
        pathHigh = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        pathLow  = astar.goTo(fromLoc, toLoc, self.roverLow, mapHandler)

        self.assertEqual(len(pathHigh), 0)
        self.assertEqual(len(pathLow), 0)

    def testAltitudeChangePrioritization(self):
        mapData = [
            [
                [(0,0), 0],
                [(0,1), 1]
            ]
        ]

        mapHandler = MapHandler(mapData)
        astar = AStar()
        
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc   = Location(0, 1, 0, 1, 0)

        # High-slope rover: should be able to climb (path found)
        pathHigh = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        self.assertTrue(pathHigh)
        self.assertEqual(len(pathHigh), 2)

        # Low-slope rover: should fail to climb (no path)
        pathLow = astar.goTo(fromLoc, toLoc, self.roverLow, mapHandler)
        self.assertFalse(pathLow)

if __name__ == '__main__':
    unittest.main()
