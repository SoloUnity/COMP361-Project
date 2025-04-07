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
        self.roverHigh = Rover(30)
        self.roverLow = Rover(0)

    def testGoToHorizontal(self):
        mapData = [
            [[(0, 0), (0, 0), 0],
            [(0, 1), (1, 1), 0]]
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

    def testGoToVertical(self):
        mapData = [
            [[(0, 0), (0, 0), 0],
            [(0, 1), (1, 1), 0],
            [(0, 2), (2, 2), 0],
            [(0, 3), (3, 3), 0]]
        ]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 1, 1, 1, 0)
        toLoc   = Location(0, 3, 3, 3, 0)
        
        pathHigh = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        pathLow  = astar.goTo(fromLoc, toLoc, self.roverLow, mapHandler)
        
        self.assertEqual(len(pathHigh), 3)
        self.assertEqual(len(pathLow), 3)

        def testDiagonalMovement(self):
            mapData = [
                [
                    [(0, 0), (0, 0), 0], [(0, 1), (1, 1), 0]
                ],
                [
                    [(1, 0), (2, 2), 0], [(1, 1), (3, 3), 0]
                ]
            ]
            
            mapHandler = MapHandler(mapData)
            aStar = AStar()  
            
            fromLoc = Location(0, 0, 0, 0, 0)
            toLoc = Location(1, 1, 3, 3, 0)
                    
            path = aStar.goTo(fromLoc, toLoc, self.roverLow, mapHandler)
            
            self.assertEqual(len(path), 2)
            self.assertEqual(path[0].x, 0)
            self.assertEqual(path[0].y, 0)
            self.assertEqual(path[1].x, 1)
            self.assertEqual(path[1].y, 1)

    def testVisitAllSingleTarget(self):
        mapData = [
            [[(0, 0), (0, 0), 0],
            [(0, 1), (1, 1), 0]]
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
            [[(0, 0), (0, 0), 0],
            [(0, 1), (1, 1), 0],
            [(0, 2), (2, 2), 0],
            [(0, 3), (3, 3), 0]]
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

    def testShortestPath(self):
        mapData = [
            [
                [(0, 0), (0, 0), 0], [(0, 1), (1, 1), 0],
                [(0, 2), (2, 2), 0], [(0, 3), (3, 3), 0]
            ],
            [
                [(1, 0), (4, 4), 0], [(1, 1), (5, 5), 0],
                [(1, 2), (6, 6), 0], [(1, 3), (7, 7), 0]
            ],
            [
                [(2, 0), (8, 8), 0], [(2, 1), (9, 9), 0],
                [(2, 2), (10, 10), 0], [(2, 3), (11, 11), 0]
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

    def testComplexGraphPathfinding(self):
        mapData = [
            [[(0, 0), (0, 0), 0], [(0, 1), (1, 1), 0], [(0, 2), (2, 2), 0]],
            [[(1, 0), (3, 3), 0], [(1, 1), (4, 4), 0], [(1, 2), (5, 5), 0]],
            [[(2, 0), (6, 6), 0], [(2, 1), (7, 7), 0], [(2, 2), (8, 8), 0]]
        ]
        mapHandler = MapHandler(mapData)
        aStar = AStar()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc   = Location(2, 2, 8, 8, 0)

        path = aStar.goTo(fromLoc, toLoc, self.roverLow, mapHandler)

        self.assertGreater(len(path), 0)
        self.assertEqual(path[0].x, 0)
        self.assertEqual(path[0].y, 0)
        self.assertEqual(path[-1].x, 2)
        self.assertEqual(path[-1].y, 2)

    def testNoPath(self):
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
        
        astar = AStar()
        pathHigh = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        pathLow  = astar.goTo(fromLoc, toLoc, self.roverLow, mapHandler)

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
