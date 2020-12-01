import json
from utils.tracer import TraceDecorator, Logger


class GameEntry:
    """
        A class that holds all of the configuration information for a game
        but also space for the actual game function. Settings for a game are

        {
            "name" : "Display name of game",
            "module" : "Pythonic module path",
            ["description" : "Function in module to show description of game",]
            "entry_point": "Function in module to start the game"
        }

    """
    def __init__(self, dict_object):
        self.play_function = None
        self.description_function = None
        for key in dict_object:
            setattr(self, key, dict_object[key])

    def has_description(self):
        return hasattr(self, "description")


@TraceDecorator
def load_configuration(configuration_file):
    """
    Loads the configuration file and returns a list of GameEntry items
    for the main game loop.
    """
    Logger.add_log("Loading configuration from: {}".format(configuration_file))

    config_settings = []
    with open(configuration_file, "r") as configuration:
        file_data = configuration.readlines()
        file_data = json.loads("\n".join(file_data))

        for entry in file_data:
            config_settings.append(GameEntry(entry))

    return config_settings
