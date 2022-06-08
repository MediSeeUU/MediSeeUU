# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import sys
import unittest

loader = unittest.TestLoader()
start_dir = 'Tests'
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner()
result = runner.run(suite)

sys.exit(not result.wasSuccessful())
