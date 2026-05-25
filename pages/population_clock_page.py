"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  population_clock_page.py — World Population Clock Page Object              ║
║                                                                              ║
║  URL: https://www.theworldcounts.com/challenges/planet-earth/               ║
║       state-of-the-planet/world-population-clock-live                       ║
║                                                                              ║
║  Extracts the live population counter from the page using XPATH only.       ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

"""
===============================================================================
POPULATION CLOCK PAGE
===============================================================================

    This Page Object handles the World Population Clock webpage.
    population_clock_page.py — World Population Clock Page Object
    
    Website:
    --------
    https://www.theworldcounts.com/challenges/planet-earth/
    state-of-the-planet/world-population-clock-live
    
    
    Extracts the live population counter from the page using XPATH only.

===============================================================================
"""

# =============================================================================
# SELENIUM IMPORTS
# =============================================================================

# Used for XPATH locators
from selenium.webdriver.common.by import By

# Selenium Exceptions
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
)

# =============================================================================
# PROJECT IMPORTS
# =============================================================================

# Parent BasePage class
from pages.base_page import BasePage

# Read values from config.json
from utils.config_reader import JsonConfigReader


# =============================================================================
# POPULATION CLOCK PAGE CLASS
# =============================================================================

class PopulationClockPage(BasePage):

    """
    Page Object for World Population Clock page.
    """

    # =========================================================================
    # LOAD CONFIG VALUES
    # =========================================================================

    # Read config file
    config = JsonConfigReader.load_config()

    # Get URL from config.json
    URL = config["base_url"]

    # =========================================================================
    # LOCATORS (XPATH ONLY)
    # =========================================================================

    # Live population counter element
    POPULATION_COUNT = (
        By.XPATH,
        "//div[contains(@class,'counter-ticker')]"
    )

    # Main page heading
    PAGE_HEADING = (
        By.XPATH,
        "//h1[contains(text(),'population')]"
    )

    # =========================================================================
    # PAGE OPEN METHOD
    # =========================================================================

    def open_population_clock(self):
        """
        Open World Population Clock webpage.

        Steps:
        ------
        1. Open webpage URL
        2. Wait for population counter
        3. Confirm page loaded

        Returns:
            self
        """

        self.log.info(
            "Opening World Population Clock page."
        )

        # Open webpage
        self.open(self.URL)

        self.log.info(
            "Waiting for population counter..."
        )

        try:

            # Wait until counter element appears
            self.find_element_present(
                self.POPULATION_COUNT
            )

            self.log.info(
                "Population counter found."
            )

        except TimeoutException:

            self.log.warning(
                "Population counter not found within timeout."
            )

        self.log.info(
            f"Page loaded successfully. "
            f"Title: {self.get_page_title()!r}"
        )

        return self

    # =========================================================================
    # GET POPULATION COUNT
    # =========================================================================

    @property
    def get_population_count(self) -> str:
        """
        Read and return current population count.

        Handles:
        --------
        -> TimeoutException
        -> StaleElementReferenceException

        Returns:
            str
        """

        try:

            # Read counter text
            text = self._read_count_text(
                self.POPULATION_COUNT
            )

            # Validate counter text
            if text and self._looks_like_population(text):

                self.log.debug(
                    f"Population count: {text!r}"
                )

                return text

        except TimeoutException:

            self.log.warning(
                "Timeout while reading population counter."
            )

        except StaleElementReferenceException:

            self.log.warning(
                "Stale element found. Retrying..."
            )

            try:

                # Retry once
                text = self._read_count_text(
                    self.POPULATION_COUNT
                )

                if text and self._looks_like_population(text):

                    self.log.debug(
                        f"Population count after retry: {text!r}"
                    )

                    return text

            except Exception as e:

                self.log.error(
                    f"Retry failed: {e}"
                )

        # Return empty string if extraction fails
        self.log.warning(
            "Could not read population count."
        )

        return ""

    # =========================================================================
    # INTERNAL HELPER METHOD
    # =========================================================================

    def _read_count_text(self, locator: tuple) -> str:
        """
        Read text from counter element.

        Args:
            locator -> Locator tuple

        Returns:
            str
        """

        # Wait until element becomes visible
        element = self.find_element_visible(locator)

        # Get and clean text
        text = element.text.strip()

        return text

    # =========================================================================
    # VALIDATE POPULATION FORMAT
    # =========================================================================

    @staticmethod
    def _looks_like_population(text: str) -> bool:
        """
        Check whether extracted text looks like a population number.

        Valid Examples:
        ---------------
        -> 8,234,567,890
        -> 8234567890

        Conditions:
        ----------
        -> Must contain digits
        -> Must contain minimum 8 digits

        Returns:
            bool
        """

        # Remove separators
        digits_only = (
            text
            .replace(",", "")
            .replace(".", "")
            .replace(" ", "")
        )

        # Check valid number format
        return (
            digits_only.isdigit()
            and len(digits_only) >= 8
        )

    # =========================================================================
    # PAGE VALIDATION METHOD
    # =========================================================================

    def is_page_loaded(self) -> bool:
        """
        Verify page loaded successfully.

        Checks:
        -------
        -> URL contains 'world-population'
        -> Title contains 'population'

        Returns:
            bool
        """

        # Check URL
        url_ok = (
            "world-population"
            in self.get_current_url()
        )

        # Check title
        title_ok = (
            "population"
            in self.get_page_title().lower()
        )

        self.log.debug(
            f"is_page_loaded -> "
            f"url_ok={url_ok}, "
            f"title_ok={title_ok}"
        )

        return url_ok or title_ok