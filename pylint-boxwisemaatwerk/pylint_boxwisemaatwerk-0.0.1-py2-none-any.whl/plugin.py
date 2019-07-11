"""PyLint plugin spec module."""
from pylint.checkers.base import NameChecker
from pylint_plugin_utils import get_checker

from pylint_boxwisemaatwerk.checkers import register_checkers

# we want to import the transforms to make sure they get added to the astroid manager,
# however we don't actually access them directly, so we'll disable the warning
#from pylint_boxwisemaatwerk import transforms  # noqa, pylint: disable=unused-import
from pylint_boxwisemaatwerk import compat


def load_configuration(linter):
    """
    Amend existing checker config.
    """
    name_checker = get_checker(linter, NameChecker)
    #name_checker.config.good_names += ('qs', 'urlpatterns', 'register', 'app_name', 'handler500')

    # we don't care about South migrations
    #linter.config.black_list += ('migrations', 'south_migrations')


def register(linter):
    """
    Registering additional checkers.
    """
    # add all of the checkers
    register_checkers(linter)

    # register any checking fiddlers
    try:
        from pylint_boxwisemaatwerk.augmentations import apply_augmentations
        apply_augmentations(linter)
    except ImportError:
        pass

    if not compat.LOAD_CONFIGURATION_SUPPORTED:
        load_configuration(linter)
