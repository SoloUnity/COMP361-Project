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
        # Percentage based approach
        # A 1 m altitude change over 10 m horizontal (each coordinate is 10m apart) results in a 10% slope
        self.roverHigh = Rover(10)
        self.roverLow = Rover(0)

    def testGoToSimpleHorizontal(self):
        mapData = [
            [
                [(0,0), (0,0), 0],
                [(0,0), (1,1), 0]
            ]
        ]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc   = Location(0, 1, 1, 1, 0)
        
        pathHigh = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        pathLow  = astar.goTo(fromLoc, toLoc, self.roverLow, mapHandler)
        
        self.assertEqual(len(pathHigh), 2, "Expected a 2-node path for roverHigh.")
        self.assertEqual(len(pathLow), 2, "Expected a 2-node path for roverLow on flat terrain.")
        self.assertEqual(pathHigh[0].y, 0, "Start location should be at column=0 for roverHigh.")
        self.assertEqual(pathHigh[1].y, 1, "Goal location should be at column=1 for roverHigh.")

    def testGoToSimpleVertical(self):
        """
        Test vertical movement on a flat, single-column grid.
        Both rovers should produce the same optimal path.
        (Note: The code is actually a single 'row' in Python terms, but has 4 cells.)
        """
        # Single row with 4 columns:
        # Each cell: lat/lon=(0,0), elev/slope=(n,n), obstacle=0
        # They are all traversable and represent increasing terrain (flat in practice).
        mapData = [
            [
                [(0,0), (0,0), 0],
                [(0,0), (1,1), 0],
                [(0,0), (2,2), 0],
                [(0,0), (3,3), 0]
            ]
        ]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 1, 1, 1, 0)
        toLoc   = Location(0, 3, 3, 3, 0)
        
        pathHigh = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        pathLow  = astar.goTo(fromLoc, toLoc, self.roverLow, mapHandler)
        
        self.assertEqual(len(pathHigh), 3, "Expected a 3-node path for roverHigh.")
        self.assertEqual(len(pathLow), 3, "Expected a 3-node path for roverLow.")

    def testVisitAllSingleTarget(self):
        """
        Test visiting a single target in a flat grid.
        Both rovers should compute an identical route.
        """
        mapData = [
            [
                [(0,0), (0,0), 0],
                [(0,0), (1,1), 0]
            ]
        ]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc   = Location(0, 0, 0, 0, 0)
        targetLoc = Location(0, 1, 1, 1, 0)
        
        pathHigh = astar.visitAll(fromLoc, [targetLoc], self.roverHigh, mapHandler)
        pathLow  = astar.visitAll(fromLoc, [targetLoc], self.roverLow, mapHandler)
        
        self.assertEqual(len(pathHigh), 2, "Expected a 2-node path for roverHigh.")
        self.assertEqual(len(pathLow), 2, "Expected a 2-node path for roverLow.")

    def testVisitAllMultipleTargets(self):
        """
        Test visiting multiple targets optimally in a flat grid.
        Both rovers should compute the same overall path.
        """
        mapData = [
            [
                [(0,0), (0,0), 0],
                [(0,0), (1,1), 0],
                [(0,0), (2,2), 0],
                [(0,0), (3,3), 0]
            ]
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
        """
        Test that A* finds the shortest path in a flat 3x4 grid.
        Both rovers should compute the same optimal path.
        """
        # 3 rows, 4 columns
        # Elevation/slope values increase from 0->11, obstacle=0
        mapData = [
            [
                [(0,0),(0,0),0],   [(0,0),(1,1),0],
                [(0,0),(2,2),0],   [(0,0),(3,3),0]
            ],
            [
                [(0,0),(4,4),0],   [(0,0),(5,5),0],
                [(0,0),(6,6),0],   [(0,0),(7,7),0]
            ],
            [
                [(0,0),(8,8),0],   [(0,0),(9,9),0],
                [(0,0),(10,10),0], [(0,0),(11,11),0]
            ]
        ]
        mapHandler = MapHandler(mapData)
        astar = AStar()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc   = Location(2, 3, 11, 11, 0)  # bottom-right corner

        pathHigh = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        pathLow  = astar.goTo(fromLoc, toLoc, self.roverLow, mapHandler)
        
        # On a flat grid, the straight-line path from top-left to bottom-right
        # can be done in 5 or 6 steps, depending on diagonal moves or adjacency rules.
        # Adjust as needed for your adjacency constraints.
        self.assertLessEqual(len(pathHigh), 6, "Expected a short path for roverHigh.")
        self.assertLessEqual(len(pathLow), 6, "Expected a short path for roverLow on flat terrain.")

    def testAStarNoPath(self):
        """
        Tests that no path is found if a cell is effectively impassable (huge obstacle or altitude).
        """
        # 2 rows, 2 columns
        # The bottom-right cell is obstacle=999 => impassable
        mapData = [
            [
                [(0,0),(0,0),0],    [(0,0),(1,1),0]
            ],
            [
                [(0,0),(2,2),0],    [(0,0),(3,3),999]
            ]
        ]
        mapHandler = MapHandler(mapData)
        
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc   = Location(1, 1, 3, 3, 999)  # huge obstacle
        
        astar = AStar()
        pathHigh = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        pathLow  = astar.goTo(fromLoc, toLoc, self.roverLow,  mapHandler)

        self.assertEqual(len(pathHigh), 0, "No path should be found for roverHigh.")
        self.assertEqual(len(pathLow),  0, "No path should be found for roverLow.")

    def testAltitudeChangePrioritization(self):
        """
        Checks that a rover with high slope tolerance can climb,
        whereas a rover with low slope tolerance fails.
        """
        # Single row, 2 columns
        # The second cell has elevation=1, slope=1 => ~45° slope
        mapData = [
            [
                [(0,0),(0,0),0],
                [(0,1),(1,1),1]  # third element is now 1 => altitude=1
            ]
        ]

        mapHandler = MapHandler(mapData)
        astar = AStar()
        
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc   = Location(0, 1, 0, 1, 0)  # lat/lon or elev usage depends on your logic

        # High-slope rover: can climb 45° -> path found
        pathHigh = astar.goTo(fromLoc, toLoc, self.roverHigh, mapHandler)
        self.assertTrue(pathHigh, "High-slope rover should succeed.")
        self.assertEqual(len(pathHigh), 2, "Path should be a direct step from (0,0) to (0,1).")

        # Low-slope rover: cannot handle 45°
        pathLow = astar.goTo(fromLoc, toLoc, self.roverLow, mapHandler)
        self.assertFalse(pathLow, "Low-slope rover cannot climb 1 meter in 1 meter (45°).")

if __name__ == '__main__':
    unittest.main()
