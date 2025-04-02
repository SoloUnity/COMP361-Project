import unittest
import sys
import os

projectRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(projectRoot, 'src/ai-algos'))

from heuristics import *
from Location import Location
from Rover import Rover
from MapHandler import MapHandler

"""
To run (from the test/ai directory) : python -m unittest heuristicsTests.py
"""

class heuristicsTests(unittest.TestCase):

    def test_euclideanDistance(self):
        loc0 = Location(0, 0, 0, 0, 0)
        loc1 = Location(1, 1, 1, 1, 1)
        loc2 = Location(1, 0, 0, 0, 0)
        self.assertEqual(euclidean_distance(loc0, loc2), 10)
        self.assertAlmostEqual(euclidean_distance(loc0, loc1), 14.14, places = 2)

    def test_manhattanDistance(self):
        loc0 = Location(1, 1, 0, 0, 0)
        loc1 = Location(1, 3, 0, 0, 0)
        loc2 = Location(4, 6, 0, 0, 0)
        self.assertEqual(manhattan_distance(loc0, loc1), 2)
        self.assertEqual(manhattan_distance(loc0, loc2), 5)
        self.assertEqual(manhattan_distance(loc1, loc2), 3)

    def test_distanceH(self):
        loc0 = Location(0, 0, 0, 0, 5)
        loc1 = Location(0, 1, 0, 0, 6)
        loc2 = Location(1, 1, 0, 0, 7)
        loc3 = Location(2, 2, 0, 0, 6)
        loc4 = Location(2, 1, 0, 0, 8)
        toLoc = Location(4, 4, 0, 0, 5)
        path = [loc0, loc1, loc2, loc3]
        rover = Rover(30)
        mh = MapHandler([[]])
        self.assertAlmostEqual(distance_h(path, loc4, toLoc, rover, mh), 80.20, places = 2)

    def test_stableAltitudeH(self):
        loc0 = Location(0, 0, 0, 0, 5)
        loc1 = Location(0, 1, 0, 0, 6)
        loc2 = Location(1, 1, 0, 0, 7)
        loc3 = Location(2, 2, 0, 0, 6)
        loc4 = Location(2, 1, 0, 0, 8)
        toLoc = Location(4, 4, 0, 0, 5)
        path = [loc0, loc1, loc2, loc3]
        rover = Rover(30)
        mh = MapHandler([[]])
        self.assertAlmostEqual(stable_altitude_h(path, loc4, toLoc, rover, mh), 2.25, places = 2)

    def test_avgAltitudeH(self):
        loc0 = Location(0, 0, 0, 0, 5)
        loc1 = Location(0, 1, 0, 0, 6)
        loc2 = Location(1, 1, 0, 0, 7)
        loc3 = Location(2, 2, 0, 0, 6)
        loc4 = Location(2, 1, 0, 0, 8)
        toLoc = Location(4, 4, 0, 0, 5)
        path = [loc0, loc1, loc2, loc3]
        rover = Rover(30)
        mh = MapHandler([[]])
        self.assertAlmostEqual(avg_altitude_h(path, loc4, toLoc, rover, mh), 12.67, places = 2)
