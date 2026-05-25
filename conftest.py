import os
import base64

import pytest

from drivers.driver_factory import DriverFactory
from utils.logger import get_logger
from utils.config_reader import JsonConfigReader


# ============================================================================== #
# Logger
# ============================================================================== #
# Logger is used to print messages in console and log file
log = get_logger("conftest")


# ============================================================================== #
# Load JSON Config
# ============================================================================== #
# Read values from config.json file
config = JsonConfigReader.load_config()

# Read browser name from config file
BROWSER = config["browser"]

# ============================================================================== #
# FIXTURE : DRIVER SETUP AND TEARDOWN
# ============================================================================== #

@pytest.fixture(scope="function")
def driver():
    """
    This fixture will:
        1. Open browser before test starts
        2. Pass driver object to test method
        3. Close browser after test finishes
    """
    # Print line in logs
    log.info("=" * 70)

    # Print browser name
    log.info(f"Launching {BROWSER.capitalize()} browser")

    # Create browser driver
    driver = DriverFactory.get_driver(BROWSER)

    # Maximize browser window
    driver.maximize_window()

    log.info("Browser launched successfully")

    # Send driver object to test case
    yield driver

    # Close browser after test execution
    log.info("Closing browser")

    DriverFactory.quit_driver()

    log.info("Browser closed")
    log.info("=" * 70)


# ============================================================================== #
# HOOK — SCREENSHOT ON FAILURE
# ============================================================================== #

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    This hook automatically:
        - Takes screenshot if test fails
        - Saves screenshot inside screenshots folder
        - Adds screenshot to HTML report
    """
    # Run actual test first
    outcome = yield

    # Get test result report
    report = outcome.get_result()

    # Continue only if:
    #   - Test execution phase is "call"
    #   - Test has failed
    if report.when == "call" and report.failed:

        # Get driver object from fixture
        drv = item.funcargs.get("driver")

        # Skip screenshot if driver is not available
        if drv is None:
            log.warning(
                f"No driver found for: {item.nodeid}"
            )
            return

        # ================================================================
        # CREATE SCREENSHOTS FOLDER
        # ================================================================

        # Create screenshots folder path
        ss_dir = os.path.join(
            os.path.dirname(__file__),
            "screenshots"
        )

        # Create folder if not already present
        os.makedirs(ss_dir, exist_ok=True)

        # ================================================================
        # CREATE SAFE FILE NAME
        # ================================================================
        # Replace unsupported symbols in filename

        safe_name = (
            item.nodeid
            .replace("::", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        # Full screenshot path
        ss_path = os.path.join(
            ss_dir,
            f"FAIL_{safe_name}.png"
        )

        try:

            # Take screenshot
            drv.save_screenshot(ss_path)

            # Print failure details
            log.error(f"TEST FAILED : {item.nodeid}")
            log.error(f"Current URL : {drv.current_url}")
            log.error(f"Screenshot  : {ss_path}")

            # ============================================================
            # ADD SCREENSHOT TO HTML REPORT
            # ============================================================

            try:
                import pytest_html

                # Open screenshot image file
                with open(ss_path, "rb") as image_file:

                    # Convert image into Base64 format
                    encoded = base64.b64encode(
                        image_file.read()
                    ).decode()

                # Get existing report data
                extra = getattr(report, "extra", [])

                # Add screenshot to report
                extra.append(
                    pytest_html.extras.png(encoded)
                )

                # Update report
                report.extra = extra

                log.info(
                    "Screenshot added to HTML report"
                )

            except ImportError:

                # pytest-html plugin not installed
                log.warning(
                    "pytest-html plugin not installed"
                )

        except Exception as e:

            # Screenshot failed
            log.warning(
                f"Could not capture screenshot: {e}"
            )


# =============================================================================
# HOOK : PRINT TEST RESULT
# =============================================================================

def pytest_runtest_logreport(report):
    """
    This hook prints:
        - PASSED
        - FAILED
        - SKIPPED
    """
    # Check only test execution result
    if report.when == "call":

        # If test passed
        if report.passed:
            log.info(f"PASSED  : {report.nodeid}")

        # If test failed
        elif report.failed:
            log.error(f"FAILED  : {report.nodeid}")

        # If test skipped
        elif report.skipped:
            log.warning(f"SKIPPED : {report.nodeid}")