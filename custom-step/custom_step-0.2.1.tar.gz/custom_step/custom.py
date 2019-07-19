# -*- coding: utf-8 -*-

"""Non-graphical part of the Custom step in a SEAMM flowchart"""

import seamm
from seamm_util import ureg, Q_  # noqa: F401
import logging
import os

logger = logging.getLogger(__name__)


class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


class Custom(seamm.Node):

    def __init__(self, flowchart=None, extension=None):
        """Setup the non-graphical part of the Custom step in a
        SEAMM flowchart.

        Keyword arguments:
        """
        logger.debug('Creating Custom {}'.format(self))

        self.script = ''

        super().__init__(
            flowchart=flowchart, title='Custom', extension=extension
        )

    def run(self):
        """Run a Custom step.
        """

        os.makedirs(self.directory, exist_ok=True)
        with cd(self.directory):
            exec(self.script, seamm.flowchart_variables._data)

        return super().run()
