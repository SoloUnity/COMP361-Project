import unittest
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(project_root, 'src/ai-algos'))

from MapHandler import MapHandler
from AStar import AStar
from Location import Location
from Rover import Rover

class AStarTests(unittest.TestCase):
    def test_goToSimple1(self):
        md = [[[0, 0, 0], [1, 1, 0]]]
        mh = MapHandler(md)
        astar = AStar()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc = Location(0, 1, 1, 1, 0)
        rover = Rover(30)
        path = astar.goTo(fromLoc, toLoc, rover, mh)
        self.assertEqual(len(path), 2)
        self.assertEqual(path[0].y, 0)
        self.assertEqual(path[1].y, 1)

    def test_goToSimple2(self):
        md = [[[0, 0, 0], [1, 1, 0], [2, 2, 0], [3, 3, 0]]]
        mh = MapHandler(md)
        astar = AStar()
        fromLoc = Location(0, 1, 1, 1, 0)
        toLoc = Location(0, 3, 3, 3, 0)
        rover = Rover(30)
        path = astar.goTo(fromLoc, toLoc, rover, mh)
        self.assertEqual(len(path), 3)
        self.assertEqual(path[0].y, 1)
        self.assertEqual(path[1].y, 2)
        self.assertEqual(path[2].y, 3)
        
    def test_visitAllSimple1(self):
        md = [[[0, 0, 0], [1, 1, 0]]]
        mh = MapHandler(md)
        astar = AStar()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc = Location(0, 1, 1, 1, 0)
        rover = Rover(30)
        path = astar.visitAll(fromLoc, [toLoc], rover, mh)
        self.assertEqual(len(path), 2)
        self.assertEqual(path[0].y, 0)
        self.assertEqual(path[1].y, 1)
        
    def test_visitAllSimple2(self):
        md = [[[0, 0, 0], [1, 1, 0], [2, 2, 0], [3, 3, 0]]]
        mh = MapHandler(md)
        astar = AStar()
        fromLoc = Location(0, 1, 1, 1, 0)
        toLoc = Location(0, 3, 3, 3, 0)
        rover = Rover(30)
        path = astar.visitAll(fromLoc, [toLoc], rover, mh)
        self.assertEqual(len(path), 3)
        self.assertEqual(path[0].y, 1)
        self.assertEqual(path[1].y, 2)
        self.assertEqual(path[2].y, 3)
        
    def test_visitAllSimple3(self):
        md = [[[0, 0, 0], [1, 1, 0], [2, 2, 0], [3, 3, 0]]]
        mh = MapHandler(md)
        astar = AStar()
        fromLoc = Location(0, 1, 1, 1, 0)
        toLoc1 = Location(0, 3, 3, 3, 0)
        toLoc2 = Location(0, 0, 0, 0, 0)
        rover = Rover(30)
        path = astar.visitAll(fromLoc, [toLoc2, toLoc1], rover, mh)
        self.assertEqual(len(path), 5)
        self.assertEqual(path[0].y, 1)
        self.assertEqual(path[1].y, 0)
        self.assertEqual(path[2].y, 1)
        self.assertEqual(path[3].y, 2)
        self.assertEqual(path[4].y, 3)

    def test_astarWithObstacle(self):
        # Test A* with an obstacle in the middle
        md = [[[0, 0, 0], [1, 1, 0], [2, 2, 0]],
              [[3, 3, 0], [100, 100, 0], [5, 5, 0]],  # High elevation in middle
              [[6, 6, 0], [7, 7, 0], [8, 8, 0]]]
        mh = MapHandler(md)
        astar = AStar()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc = Location(2, 2, 8, 8, 0)
        rover = Rover(10)  # Limited climbing ability
        path = astar.goTo(fromLoc, toLoc, rover, mh)
        
        # A* should find a path around the obstacle
        self.assertGreater(len(path), 0)
        self.assertEqual(path[0].x, 0)
        self.assertEqual(path[0].y, 0)
        self.assertEqual(path[-1].x, 2)
        self.assertEqual(path[-1].y, 2)
        
        # Make sure the path doesn't go through the obstacle
        for loc in path:
            self.assertFalse(loc.x == 1 and loc.y == 1)
    
    def test_astarShorterPath(self):
        # Create a grid with two possible paths, one shorter than the other
        md = [[[0, 0, 0], [1, 1, 0], [2, 2, 0], [3, 3, 0]],
              [[4, 4, 0], [5, 5, 0], [6, 6, 0], [7, 7, 0]],
              [[8, 8, 0], [9, 9, 0], [10, 10, 0], [11, 11, 0]]]
        mh = MapHandler(md)
        astar = AStar()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc = Location(2, 3, 11, 11, 0)
        rover = Rover(30)
        
        # A* should find the shortest path (diagonal is shorter)
        path = astar.goTo(fromLoc, toLoc, rover, mh)
        self.assertLessEqual(len(path), 6)  # Should be at most 6 steps
        
    def test_astarNoPath(self):
        # Test when no path exists
        md = [[[0, 0, 0], [1, 1, 0]],
              [[2, 2, 0], [100, 100, 0]]]  # Large elevation difference
        mh = MapHandler(md)
        astar = AStar()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc = Location(1, 1, 100, 100, 0)
        rover = Rover(5)  # Low climbing ability
        path = astar.goTo(fromLoc, toLoc, rover, mh)
        self.assertEqual(len(path), 0)  # No path should be found

if __name__ == '__main__':
    unittest.main()