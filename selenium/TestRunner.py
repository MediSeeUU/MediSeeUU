import sys
import unittest

# loads all the tests located in the 'Tests' folder
loader = unittest.TestLoader()
start_dir = 'Tests'
suite = loader.discover(start_dir)

# runs all these tests
runner = unittest.TextTestRunner()
result = runner.run(suite)

sys.exit(not result.wasSuccessful())
