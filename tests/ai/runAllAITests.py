import unittest
import sys
import os

projectRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(projectRoot, 'src/ai-algos'))

from heuristicsTests import heuristicsTests
from bfsTests import bfsTests
from aStarTests import TestAStarAlgorithm
from dfsTests import DFSAlgorithmTests

def runAllTests():
    testSuite = unittest.TestSuite()
    
    testSuite.addTest(unittest.makeSuite(heuristicsTests))
    testSuite.addTest(unittest.makeSuite(bfsTests))
    testSuite.addTest(unittest.makeSuite(TestAStarAlgorithm))
    testSuite.addTest(unittest.makeSuite(DFSAlgorithmTests))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(testSuite)
    
    print("\n====================")
    print("SUMMARY:")
    print(f"Ran {result.testsRun} tests")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    return len(result.failures) == 0 and len(result.errors) == 0

if __name__ == "__main__":
    print("Running all Mars Rover navigation tests...\n")
    success = runAllTests()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)