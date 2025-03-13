import unittest
import sys
sys.path.append('../../src/ai-algos')
from MapHandler import MapHandler
from BFS import BFS
from Location import Location
from Rover import Rover

"""
To run (from the test/ai directory) : python -m unittest bfsTests.py
"""

class bfsTests(unittest.TestCase):

    def test_goToSimple1(self):
        md = [[[(0, 0), (0, 0), 0], [(0, 0), (1, 1), 0]]]
        mh = MapHandler(md)
        bfs = BFS()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc = Location(0, 1, 1, 1, 0)
        rover = Rover(30)
        path = bfs.goTo(fromLoc, toLoc, rover, mh)

        self.assertEqual(len(path), 2)
        self.assertEqual(path[0].y, 0)
        self.assertEqual(path[1].y, 1)


    def test_goToSimple2(self):
        md = [[[(0, 0), (0, 0), 0], [(0, 0), (1, 1), 0], [(0, 0), (2, 2), 0], [(0, 0), (3, 3), 0]]]
        mh = MapHandler(md)
        bfs = BFS()
        fromLoc = Location(0, 1, 1, 1, 0)
        toLoc = Location(0, 3, 3, 3, 0)
        rover = Rover(30)
        path = bfs.goTo(fromLoc, toLoc, rover, mh)
        
        self.assertEqual(len(path), 3)
        self.assertEqual(path[0].y, 1)
        self.assertEqual(path[1].y, 2)
        self.assertEqual(path[2].y, 3)

    def test_visitAllSimple1(self):
        md = [[[(0, 0), (0, 0), 0], [(0, 0), (1, 1), 0]]]
        mh = MapHandler(md)
        bfs = BFS()
        fromLoc = Location(0, 0, 0, 0, 0)
        toLoc = Location(0, 1, 1, 1, 0)
        rover = Rover(30)
        path = bfs.visitAll(fromLoc, [toLoc], rover, mh)

        self.assertEqual(len(path), 2)
        self.assertEqual(path[0].y, 0)
        self.assertEqual(path[1].y, 1)
        
    def test_visitAllSimple2(self):
        md = [[[(0, 0), (0, 0), 0], [(0, 0), (1, 1), 0], [(0, 0), (2, 2), 0], [(0, 0), (3, 3), 0]]]
        mh = MapHandler(md)
        bfs = BFS()
        fromLoc = Location(0, 1, 1, 1, 0)
        toLoc = Location(0, 3, 3, 3, 0)
        rover = Rover(30)
        path = bfs.visitAll(fromLoc, [toLoc], rover, mh)
        
        self.assertEqual(len(path), 3)
        self.assertEqual(path[0].y, 1)
        self.assertEqual(path[1].y, 2)
        self.assertEqual(path[2].y, 3)

    def test_visitAllSimple3(self) :
        md = [[[(0, 0), (0, 0), 0], [(0, 0), (1, 1), 0], [(0, 0), (2, 2), 0], [(0, 0), (3, 3), 0]]]
        mh = MapHandler(md)
        bfs = BFS()
        fromLoc = Location(0, 1, 1, 1, 0)
        toLoc1 = Location(0, 3, 3, 3, 0)
        toLoc2 = Location(0, 0, 0, 0, 0)
        rover = Rover(30)
        path = bfs.visitAll(fromLoc, [toLoc2, toLoc1], rover, mh)

        self.assertEqual(len(path), 5)
        self.assertEqual(path[0].y, 1)
        self.assertEqual(path[1].y, 0)
        self.assertEqual(path[2].y, 1)
        self.assertEqual(path[3].y, 2)
        self.assertEqual(path[4].y, 3)
