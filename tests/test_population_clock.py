"""
===============================================================================
TEST FILE : test_population_clock.py
===============================================================================

Project:
--------
test_population_clock.py — World Population Clock Live Extraction

Framework:
----------
Framework : POM + Explicit Wait + Expected Conditions + Pytest

URL       : https://www.theworldcounts.com/challenges/planet-earth/            ║
----              state-of-the-planet/world-population-clock-live

Purpose:
--------
1. Open World Population Clock webpage
2. Validate page loads correctly
3. Extract live population counter
4. Continuously print live counter values
5. Stop safely using CTRL + C

===============================================================================
"""

# =============================================================================
# PYTHON IMPORTS
# =============================================================================

import time
from datetime import datetime


# =============================================================================
# PROJECT IMPORTS
# =============================================================================

# Page Object class
from pages.population_clock_page import PopulationClockPage

# Logger utility
from utils.logger import get_logger

# Config reader
from utils.config_reader import JsonConfigReader


# =============================================================================
# LOGGER SETUP
# =============================================================================

log = get_logger(__name__)


# =============================================================================
# LOAD CONFIG VALUES
# =============================================================================

# Read config.json
config = JsonConfigReader.load_config()

# Delay between each population count read
POLL_INTERVAL_SECONDS = config["wait_interval"]


# =============================================================================
# TEST CLASS
# =============================================================================

class TestPopulationClock:

    """
    Test class for World Population Clock webpage.
    """

    # =========================================================================
    # TEST CASE 01
    # =========================================================================

    def test_population_clock_page_loads(self, driver):
        """
        Verify World Population Clock page loads successfully.

        Test Steps:
        -----------
        1. Open webpage
        2. Verify URL
        3. Verify page title

        Expected Result:
        ----------------
        -> URL should contain 'world-population'
        -> Title should not be empty
        """

        log.info(
            "TEST START: test_population_clock_page_loads"
        )

        # Create page object
        page = PopulationClockPage(driver)

        # Open webpage
        page.open_population_clock()

        # Get current URL
        current_url = page.get_current_url()

        # Get page title
        page_title = page.get_page_title()

        log.info(f"Current URL : {current_url}")
        log.info(f"Page Title  : {page_title!r}")

        # Verify URL
        assert (
            "world-population" in current_url
            or "theworldcounts" in current_url
        ), (
            "\nFAIL: Incorrect webpage opened."
            f"\nActual URL: {current_url}"
        )

        log.info(
            "PASS: Population clock page loaded successfully."
        )

    # =========================================================================
    # TEST CASE 02
    # =========================================================================

    def test_population_counter_is_visible_and_valid(self, driver):
        """
        Verify live population counter is visible and valid.

        Test Steps:
        -----------
        1. Open webpage
        2. Read population counter
        3. Validate extracted value

        Expected Result:
        ----------------
        -> Counter should not be empty
        -> Counter should contain digits
        -> Counter should contain minimum 8 digits
        """

        log.info(
            "TEST START: "
            "test_population_counter_is_visible_and_valid"
        )

        # Create page object
        page = PopulationClockPage(driver)

        # Open webpage
        page.open_population_clock()

        # Read population count
        count = page.get_population_count

        log.info(
            f"Population count extracted: {count!r}"
        )

        # Verify count is not empty
        assert count != "", (
            "\nFAIL: Population counter is empty."
        )

        # Remove separators
        digits = (
            count
            .replace(",", "")
            .replace(".", "")
            .replace(" ", "")
        )

        # Verify valid number
        assert digits.isdigit(), (
            f"\nFAIL: Invalid population value: {count!r}"
        )

        # Verify minimum digits
        assert len(digits) >= 8, (
            f"\nFAIL: Population value too short: {count!r}"
        )

        log.info(
            f"PASS: Valid population count extracted -> {count}"
        )

    # =========================================================================
    # TEST CASE 03
    # =========================================================================

    def test_live_population_count_until_ctrl_c(self, driver):
        """
        MAIN TEST

        Continuously read live population count
        until user presses CTRL + C.

        Test Steps:
        -----------
        1. Open webpage
        2. Read live population count
        3. Print count with timestamp
        4. Wait few seconds
        5. Repeat forever

        Stop:
        -----
        Press CTRL + C in terminal.
        """

        log.info(
            "TEST START: "
            "test_live_population_count_until_ctrl_c"
        )

        log.info(
            "Press CTRL + C to stop execution."
        )

        # Create page object
        page = PopulationClockPage(driver)

        # Open webpage
        page.open_population_clock()

        # =========================================================================
        # PRINT CONSOLE BANNER
        # =========================================================================

        print("\n")

        print("#================================================================#")
        print("#               WORLD POPULATION LIVE COUNTER                    #")
        print("#                    Press CTRL + C to stop                      #")
        print("#================================================================#")

        print("─" * 70)

        # =========================================================================
        # VARIABLES
        # =========================================================================

        # Total successful reads
        read_count = 0

        # Store previous population value
        previous_population = 0

        # Store successful population values
        population_list = []

        # Store failed iteration numbers
        failed_iteration_list = []

        # =========================================================================
        # MAIN LOOP
        # =========================================================================

        try:

            while True:

                # -------------------------------------------------------------
                # Read current population count
                # -------------------------------------------------------------

                population_count = page.get_population_count

                # Get current timestamp
                timestamp = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                # Print in terminal
                print(
                    f"Timestamp: < {timestamp} > "
                    f"-> Population: {population_count}"
                )

                # Log in log file
                log.info(
                    f"Iteration: {read_count} | "
                    f"Timestamp: < {timestamp} > "
                    f"-> Population: {population_count}"
                )

                # -------------------------------------------------------------
                # Wait before next read
                # -------------------------------------------------------------

                time.sleep(POLL_INTERVAL_SECONDS)

                # -------------------------------------------------------------
                # Convert population text into integer
                # -------------------------------------------------------------

                current_population = int(
                    population_count.replace(",", "")
                )

                # -------------------------------------------------------------
                # Validate counter increasing
                # -------------------------------------------------------------

                if current_population > previous_population:

                    population_list.append(current_population)

                else:

                    log.error(
                        f"Counter validation failed "
                        f"at iteration -> {read_count}"
                    )

                    failed_iteration_list.append(read_count)

                # -------------------------------------------------------------
                # Update values for next loop
                # -------------------------------------------------------------

                read_count += 1

                previous_population = current_population

        # =========================================================================
        # HANDLE CTRL + C
        # =========================================================================

        except KeyboardInterrupt:

            print("\n")
            print("Keyboard interruption received -> CTRL + C")

            log.info(
                "User stopped execution using CTRL + C"
            )

            log.info(
                "Stopping population extraction..."
            )

            log.info(
                f"Total reads completed: {read_count}"
            )

            print(f"Read Count : {read_count}")

            print(
                f"Successful Reads : "
                f"{len(population_list)}"
            )

            # Verify all iterations successful
            if read_count == len(population_list):

                log.info(
                    "Population extraction completed successfully."
                )

            else:

                log.error(
                    f"Failed iterations: {failed_iteration_list}"
                )

        # =========================================================================
        # FINALLY BLOCK
        # =========================================================================

        finally:

            print("─" * 70)

            print(
                "Closing browser and exiting program..."
            )

            try:

                # Close browser safely
                driver.quit()

            except Exception:

                driver.quit()

            log.info(
                "Browser closed successfully."
            )