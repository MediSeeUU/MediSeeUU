import sys
import unittest

loader = unittest.TestLoader()
start_dir = 'Tests'
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner()
result = runner.run(suite)

sys.exit(not result.wasSuccessful())
