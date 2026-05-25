"""
===============================================================================
BASE PAGE CLASS
===============================================================================

 -> This is the parent class for all Page Objects.

 -> All page classes will inherit this BasePage class.

===============================================================================
"""

# =============================================================================
# SELENIUM IMPORTS
# =============================================================================

# Explicit wait class
from selenium.webdriver.support.ui import WebDriverWait

# Selenium Expected Conditions
from selenium.webdriver.support import expected_conditions as EC

# Selenium Exceptions
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)

# URL condition
from selenium.webdriver.support.expected_conditions import url_contains


# =============================================================================
# CUSTOM UTILITIES
# =============================================================================

from utils.config_reader import JsonConfigReader
from utils.logger import get_logger


# =============================================================================
# LOAD CONFIG VALUES
# =============================================================================

# Read values from config.json
config = JsonConfigReader.load_config()

# Default explicit wait timeout
DEFAULT_TIMEOUT = config["default_timeout"]

# Polling interval for waits
WAIT_INTERVAL = config["wait_interval"]


# =============================================================================
# BASE PAGE CLASS
# =============================================================================

class BasePage:

    # =========================================================================
    # CONSTRUCTOR
    # =========================================================================

    def __init__(self, driver, timeout: int = DEFAULT_TIMEOUT):
        """
        Constructor runs automatically when object is created.

        Args:
            driver  -> Selenium WebDriver instance
            timeout -> Explicit wait timeout in seconds
        """

        # Store webdriver object
        self.driver = driver

        # Store timeout value
        self.timeout = timeout

        # Create WebDriverWait object
        self.wait = WebDriverWait(
            driver,
            timeout,
            poll_frequency=WAIT_INTERVAL
        )

        # Create logger object
        self.log = get_logger(self.__class__.__module__)

    # =========================================================================
    # PAGE NAVIGATION METHODS
    # =========================================================================

    def open(self, url: str) -> None:
        """
        Open the given URL in browser.
        """

        self.log.info(f"Opening URL: {url}")

        # Open webpage
        self.driver.get(url)

    def get_current_url(self) -> str:
        """
        Return current browser URL.
        """

        url = self.driver.current_url

        self.log.info(f"Current URL: {url}")

        return url

    def get_page_title(self) -> str:
        """
        Return current webpage title.
        """

        title = self.driver.title

        self.log.info(f"Page title: {title}")

        return title

    # =========================================================================
    # WAIT METHODS
    # =========================================================================

    def find_element_visible(self, locator: tuple):
        """
        Wait until element becomes visible.

        Args:
            locator -> Locator tuple

        Returns:
            WebElement
        """

        self.log.debug(f"Waiting for VISIBLE element: {locator}")

        try:
            element = self.wait.until(
                EC.visibility_of_element_located(locator)
            )

            self.log.debug(f"Element visible: {locator}")

            return element

        except TimeoutException:

            self.log.error(
                f"Timeout ({self.timeout}s) - Element not visible: {locator}"
            )

            raise

    def find_element_clickable(self, locator: tuple):
        """
        Wait until element becomes clickable.

        Clickable means:
        -> Visible
        -> Enabled
        """

        self.log.debug(f"Waiting for CLICKABLE element: {locator}")

        try:
            element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )

            self.log.debug(f"Element clickable: {locator}")

            return element

        except TimeoutException:

            self.log.error(
                f"Timeout ({self.timeout}s) - Element not clickable: {locator}"
            )

            raise

    def find_element_present(self, locator: tuple):
        """
        Wait until element is present in DOM.

        NOTE:
        -----
        Element may or may not be visible.
        """

        self.log.debug(f"Waiting for PRESENT element: {locator}")

        try:
            element = self.wait.until(
                EC.presence_of_element_located(locator)
            )

            self.log.debug(f"Element present: {locator}")

            return element

        except TimeoutException:

            self.log.error(
                f"Timeout ({self.timeout}s) - Element not present: {locator}"
            )

            raise

    def wait_for_url_contains(self, text: str) -> bool:
        """
        Wait until URL contains given text.

        Returns:
            True  -> if URL contains text
            False -> if timeout occurs
        """

        self.log.debug(f"Waiting for URL containing: {text}")

        try:

            return self.wait.until(
                EC.url_contains(text)
            )

        except TimeoutException:

            self.log.warning(
                f"URL did not contain '{text}' within {self.timeout}s"
            )

            return False

    # =========================================================================
    # ELEMENT ACTION METHODS
    # =========================================================================

    def click(self, locator: tuple) -> None:
        """
        Click element safely.

        Steps:
        ------
        1. Wait for clickable element
        2. Click normally
        """

        self.log.info(f"Clicking element: {locator}")

        try:

            self.find_element_clickable(locator).click()

        except (
            ElementNotInteractableException,
            ElementClickInterceptedException
        ):

            self.log.warning(
                f"Normal click failed." )

    def get_text(self, locator: tuple) -> str:
        """
        Get visible element text.

        Also handles stale element issue by retrying once.
        """

        try:

            # Get visible element
            element = self.find_element_visible(locator)

            # Read text
            text = element.text.strip()

            self.log.debug(f"Text found: {text!r}")

            return text

        except StaleElementReferenceException:

            # Retry once if DOM refreshes
            self.log.warning(
                f"Stale element detected. Retrying: {locator}"
            )

            element = self.find_element_visible(locator)

            text = element.text.strip()

            self.log.debug(f"Text found after retry: {text!r}")

            return text

    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """
        Return attribute value of element.
        """

        element = self.find_element_present(locator)

        value = element.get_attribute(attribute)

        self.log.debug(
            f"Attribute [{attribute}] = {value!r}"
        )

        return value

    # =========================================================================
    # ELEMENT STATE METHODS
    # =========================================================================

    def is_element_displayed(self, locator: tuple) -> bool:
        """
        Check whether element is visible on screen.

        Returns:
            True  -> visible
            False -> not visible / not found
        """

        try:

            result = self.find_element_visible(locator).is_displayed()

            self.log.debug(f"is_displayed = {result}")

            return result

        except (TimeoutException, NoSuchElementException):

            self.log.debug(f"Element not displayed: {locator}")

            return False

    def is_element_enabled(self, locator: tuple) -> bool:
        """
        Check whether element is enabled.

        Returns:
            True  -> enabled
            False -> disabled / not found
        """

        try:

            result = self.find_element_visible(locator).is_enabled()

            self.log.debug(f"is_enabled = {result}")

            return result

        except (TimeoutException, NoSuchElementException):

            self.log.debug(f"Element not enabled: {locator}")

            return False