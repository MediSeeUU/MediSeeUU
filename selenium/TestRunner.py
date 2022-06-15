# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
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
