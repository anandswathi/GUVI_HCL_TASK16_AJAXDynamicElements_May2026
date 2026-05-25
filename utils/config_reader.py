import json
import os


class JsonConfigReader:
    """
    This class is used to:
    - Read data from config.json file
    - Return configuration values as Python dictionary
    """

    # =========================================================================
    # STATIC METHOD : LOAD CONFIG
    # =========================================================================

    @staticmethod
    def load_config():

        # GET PROJECT ROOT DIRECTORY
        # __file__ → current file path
        # dirname() → parent folder


        # This moves 2 folders back to project root
        root_dir = os.path.dirname(
            os.path.dirname(__file__)
        )

        # CREATE FULL CONFIG FILE PATH
        config_path = os.path.join(
            root_dir,
            "config",
            "config.json"
        )


        # OPEN JSON FILE AND READ DATA
        with open(config_path, "r") as file:

            # Convert JSON data into Python dictionary
            config_data = json.load(file)

        # Return config dictionary
        return config_data