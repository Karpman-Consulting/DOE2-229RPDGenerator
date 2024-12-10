import unittest
import os
import sys
import threading

# Timeout value (in seconds)
TIMEOUT_SECONDS = 300  # 5 minutes


# Define a timeout handler
def timeout_handler():
    print("Test execution timed out!")
    sys.exit(1)


# Start the timeout timer
timeout_timer = threading.Timer(TIMEOUT_SECONDS, timeout_handler)
timeout_timer.start()

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

    # Cancel the timeout timer if tests complete in time
    timeout_timer.cancel()

    # Check test results
    if not result.wasSuccessful():
        sys.exit(1)
    sys.exit(0)

except Exception as e:
    # Cancel the timeout timer in case of an unexpected error
    timeout_timer.cancel()
    print(f"Error during test execution: {e}")
    sys.exit(1)
