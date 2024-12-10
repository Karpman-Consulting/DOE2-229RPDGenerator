import unittest
import os
import sys
import signal


# Define a timeout handler
def timeout_handler(signum, frame):
    print("Test execution timed out!")
    sys.exit(1)


# Set the timeout (in seconds)
TIMEOUT_SECONDS = 300  # Set timeout for 5 minutes

# Apply the timeout
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(TIMEOUT_SECONDS)

try:
    # Set up test discovery and execution
    current_dir = os.path.dirname(os.path.abspath(__file__))
    bdl_commands_test_dir = os.path.join(
        current_dir, "populate_test", "bdl_commands_test"
    )
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=bdl_commands_test_dir, pattern="*_test.py")

    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    # Cancel the timeout if execution completes
    signal.alarm(0)

    # Check test results
    if not result.wasSuccessful():
        sys.exit(1)
    sys.exit(0)

except Exception as e:
    # Handle any unexpected errors
    print(f"Error during test execution: {e}")
    sys.exit(1)
