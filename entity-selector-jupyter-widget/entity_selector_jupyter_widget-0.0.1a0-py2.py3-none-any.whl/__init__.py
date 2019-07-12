from ._version import version_info, __version__

from .entity_selector import *


def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'frontend_entity_selector_jupyter_widget',
        'require': 'frontend_entity_selector_jupyter_widget/extension'
    }]
