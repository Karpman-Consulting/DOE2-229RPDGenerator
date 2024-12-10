import unittest
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
bdl_commands_test_dir = os.path.join(current_dir, "populate_test", "bdl_commands_test")
loader = unittest.TestLoader()
suite = loader.discover(start_dir=bdl_commands_test_dir, pattern="*_test.py")

runner = unittest.TextTestRunner()
result = runner.run(suite)

if not result.wasSuccessful():
    sys.exit(1)
