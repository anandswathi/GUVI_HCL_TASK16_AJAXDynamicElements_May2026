from selenium import webdriver

# Import browser option classes
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class DriverFactory:
    """
    Class that -
        1. Creates browser driver
        2. Manages single driver instance
        3. Closes browser after execution
    """

    # Store driver object
    # Initially driver value is None
    driver = None

    @classmethod
    def get_driver(cls, browser):
        """
        This method:
            - Creates browser driver
            - Returns existing driver if already created

        Supported browsers:
            - Chrome
            - Edge
            - Firefox
        """

        # If driver already exists, return same driver
        if cls.driver is not None:
            return cls.driver

        # Convert browser name to lowercase
        browser = browser.lower()

        # =====================================================================
        # CHROME BROWSER
        # =====================================================================
        if browser == "chrome":

            # Create Chrome options object
            options = ChromeOptions()

            # Open browser in maximized mode
            options.add_argument("--start-maximized")

            # Disable browser notifications
            options.add_argument("--disable-notifications")

            # Create Chrome driver
            cls.driver = webdriver.Chrome(options=options)

        # =====================================================================
        # EDGE BROWSER
        # =====================================================================
        elif browser == "edge":

            # Create Edge options object
            options = EdgeOptions()

            # Open browser in maximized mode
            options.add_argument("--start-maximized")

            # Disable browser notifications
            options.add_argument("--disable-notifications")

            # Create Edge driver
            cls.driver = webdriver.Edge(options=options)

        # =====================================================================
        # FIREFOX BROWSER
        # =====================================================================
        elif browser == "firefox":

            # Create Firefox options object
            options = FirefoxOptions()

            # Set browser window width
            options.add_argument("--width=1480")

            # Set browser window height
            options.add_argument("--height=1080")

            # Disable browser notifications
            options.set_preference(
                "dom.webnotifications.enabled",
                False
            )

            # Create Firefox driver
            cls.driver = webdriver.Firefox(options=options)

        # =====================================================================
        # INVALID BROWSER
        # =====================================================================
        else:

            # Raise error if browser name is invalid
            raise ValueError(
                f"Browser not supported: {browser}"
            )

        # Return created driver
        return cls.driver


    @classmethod
    def quit_driver(cls):
        """
        Method that closes browser and resets driver
        """

        # Check if driver exists
        if cls.driver:
            try:
                # Close browser
                cls.driver.quit()

            except Exception as e:
                print(f"Ignoring browser quit exception: {e}")

            finally:
                # Reset driver value
                cls.driver = None
