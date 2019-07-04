import importlib
import logging

__log__ = logging.getLogger(__name__)


class TelethonAddOnManager:
    """
    The AddOnManager class that forwards user's TelegramClient instance to any package requiring it!
    Args:
        bind (TelegramClient, optional):
            The TelegramClient instance to bind to the TelethonAddOnManager
    """

    def __init__(self, bind=None):
        self.client = bind
        self.loaded_addons = {}

    def load_addon(self, addon=None):
        """
        Loads a given addon!
        Args:
            addon (str, optional) the package to load as an addon
        """
        if addon:
            addon = importlib.import_module(addon)
            main = addon.Main()
            main.client = self.client
            addon_info = "Loaded: {}".format(main.__name__)

            if hasattr(main, "__author__"):
                addon_info += ", Author: {}".format(main.__author__)
            if hasattr(main, "__version__"):
                addon_info += ", Version {}".format(main.__version__)

            self.loaded_addons.update({main.__name__: addon})
            __log__.info(addon_info)
            return main

    def get_loaded_addons(self):
        """Get's a dict with all the loaded addons"""
        return self.loaded_addons
