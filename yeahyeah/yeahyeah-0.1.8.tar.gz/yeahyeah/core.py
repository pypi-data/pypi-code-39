# -*- coding: utf-8 -*-

"""Core functionality for yeahyeah launch manager"""
import collections
from pathlib import Path

import click
import yaml
from yaml.loader import Loader


class YeahYeah:
    """A cli module that has menu items
    """

    def __init__(self):
        self.configuration_path = Path.home() / "yeahyeah_config"
        self.plugins = []
        self.root_cli = self.get_root_cli()
        self.admin_cli = self.admin_cli_group()
        self.root_cli.add_command(self.admin_cli)
        self.admin_cli.add_command(self.install_info_cli_action())

    @staticmethod
    def get_root_cli():
        """Get the base click group for yeahyeah"""

        @click.group()
        def root_cli():
            """Yeahyeah launch things
            """

        return root_cli

    def add_plugin(self, plugin):
        """Add this plugin and all its actions

        Parameters
        ----------
        plugin: YeahYeahPlugin

        """
        self.plugins.append(plugin)
        for pattern in plugin.get_menu_items():
            command = pattern.to_click_command()
            command.help += f" ({plugin.short_slug})"
            self.root_cli.add_command(command)

        @click.group(name=plugin.slug, help=f"Admin for {plugin.slug}")
        def plugin_admin():
            f"""Admin for {plugin.slug}"""
            pass

        for command in plugin.get_admin_commands():
            plugin_admin.add_command(command)
        self.admin_cli.add_command(plugin_admin)

    def admin_cli_group(self):
        """Returns an 'admin' click group containing all admin actions for this plugin"""

        @click.group()
        def admin():
            """Admin options for yeahyeah and plugins"""
            pass

        return admin

    @staticmethod
    def install_info_cli_action():
        """Returns a click action that prints some info on how to get auto-completion to work for yeahyeah
        """
        @click.command()
        def enable_autocompletion():
            """Print information on how to enable command auto-completion"""
            click.echo('Execute the following line in a terminal to enable auto-completion for that terminal only:\n'
                       '\n'
                       '    $ eval "$(_JJ_COMPLETE=source jj)"\n'
                       '\n'
                       'To enable auto completion permanently, run this\n'
                       '\n'
                       '    $ echo "eval $(_JJ_COMPLETE=source jj)" >> ~/.bashrc\n')

        return enable_autocompletion


class YeahYeahMenuItem:
    """Something you can add to the base yeahyeah menu and then launch"""

    def __init__(self, name, help_text=None):
        """

        Parameters
        ----------
        name: str
            Name to launch this item with, probably you want to keep this short.
        help_text: str, optional
            Short help message for this item. Defaults to empty string
        """
        self.name = name
        self._help_text = help_text

    @property
    def help_text(self):
        if self._help_text is None:
            return ""
        else:
            return self._help_text

    def to_click_command(self):
        """Return a click command representation of this action

        Returns
        -------
        func
            A function that has been processed by the @click.command() decorator.
            <click_group>.add_command(test) should work

        """
        raise NotImplementedError()


class SerialisableMenuItem(YeahYeahMenuItem):
    """A menu item that you can serialise to and from a dict"""

    def get_parameters(self):
        """ Any extra parameters as dict. These are saved along with item name and help_text

        Overwrite this in child classes

        Returns
        -------
        Dict[param_name:param_value]
            Parameters for this menu item that need to be persisted
        """
        return {}

    def to_dict(self):
        """

        Returns
        -------
        Dict[str:Dict[param1,param2, etc..]]:
            [menu item key: [parameters that need to be saved]]

        """
        values = self.get_parameters()
        if self._help_text is not None:
            values["text"] = self._help_text
        return {self.name: values}

    @classmethod
    def from_dict(cls, dict_in):
        """Create an instance of this object from given dict.

        """
        name = list(dict_in.keys()).pop()
        values = dict_in[name]
        help_text = values.pop("text", None)

        return cls(name=name, help_text=help_text, **values)


class MenuItemList(collections.UserList):
    """A list-like list of menu items that can be saved to and loaded from a file"""

    # The type of objects that this list can contain
    item_classes = [SerialisableMenuItem]

    def __init__(self, items):
        """

        Parameters
        ----------
        items: List[SerialisableMenuItem]
            The items to put in this list
        """
        self.data = items

    @property
    def items(self):
        """I find 'items' more descriptive then 'data' """
        return self.data

    def save(self, file):
        """Save list to file

        Parameters
        ----------
        file: Open file handle
            save to this file

        Returns
        -------

        """
        yaml.dump(self.to_dict(), file, default_flow_style=False)

    @classmethod
    def load(cls, file):
        """Try to parse the given file's content into any of the classes in cls.item_classes.

        Parameters
        ----------
        file: open file handle

        Returns
        -------
        MenuItemList
            List of items represented in file

        Raises
        ------
        MenuItemLoadError:
            When object loaded is not a list or when contents could not be parsed as any of the item_classes


        """

        loaded = yaml.load(file, Loader=Loader)

        if type(loaded) is not dict:
            msg = f"Expected to load a dictionary, but found {type(loaded)} instead"
            raise MenuItemLoadError(msg)
        # flatten to list of dicts
        item_list = []
        for key, values in loaded.items():
            item_as_dict = {key: values}
            for ItemClass in cls.item_classes:
                try:
                    item_instance = ItemClass.from_dict(item_as_dict)
                    break
                except TypeError:
                    item_instance = None
                    continue
            if not item_instance:
                msg = f"Could not create any object from {item_as_dict}. Tried {[str(x) for x in cls.item_classes]}.."
                raise MenuItemLoadError(msg)
            else:
                item_list.append(item_instance)

        return cls(items=item_list)

    def to_dict(self):
        """This list as dict, as terse as possible:

        {pattern_name1: {param1: value1,...},
         pattern_name2: {param2: value2,...},

         Notes
         -----
         This function is mainly to make yaml dump something readable to file. Dict of dict renders quite well
        """
        result = {}
        for item in self.data:
            pattern_dict = item.to_dict()
            result.update(pattern_dict)

        return result


class YeahYeahPlugin:
    """A thing that can generate YeahYeahMenuItems that can be added"""

    def __init__(self, slug, short_slug=None):
        """

        Parameters
        ----------
        slug: str
            short, no space name to use for describing this plugin but also as key for admin functions
        short_slug: str, optional
            Slug which is a short as possible, to append to options help text. For example 'url', or 'path'. Defaults
            to slug
        """
        self.slug = slug
        if not short_slug:
            short_slug = slug
        self.short_slug = short_slug

    def get_menu_items(self):
        """Get all menu items that this plugin has

        Returns
        -------
        List[YeahYeahMenuItem]
            menu items that can be added to a click group using <click_group>.add_command(test)
        """
        raise NotImplementedError()

    def get_admin_commands(self):
        """Action to do admin tasks for this plugin, if any

        Returns
        -------
        List[click.Command]
            List of click commands that can be used to admin this plugin

        """
        raise NotImplementedError()


class MenuItemLoadError(Exception):
    pass
