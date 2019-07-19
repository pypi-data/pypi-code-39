# -*- coding: utf-8 -*-

"""Non-graphical part of the Cassandra step in SEAMM

In addition to the normal logger, two logger-like printing facilities are
defined: 'job' and 'printer'. 'job' send output to the main job.out file for
the job, and should be used very sparingly, typically to echo what this step
will do in the initial summary of the job.

'printer' sends output to the file 'step.out' in this steps working
directory, and is used for all normal output from this step.
"""

import logging
import seamm
from seamm_util import ureg, Q_  # noqa: F401
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __
import cassandra_step

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter('lammps')


class Cassandra(seamm.Node):

    def __init__(self, flowchart=None, title='Cassandra', extension=None):
        """A Cassandra step in a MolSSI flowchart.

        You may wish to change the title above, which is the string displayed
        in the box representing the step in the flowchart.

        Keyword arguments:
        """
        logger.debug('Creating Cassandra {}'.format(self))

        super().__init__(
            flowchart=flowchart, title='Cassandra', extension=extension
        )

        self.parameters = cassandra_step.Cassandra_Parameters()

    def description_text(self, P):
        """Create the text description of what this step will do.
        The dictionary of control values is passed in as P so that
        the code can test values, etc.
        """

        text = (
            'Please replace this with a short summary of the '
            'Cassandra step, including key parameters.'
        )

        return text

    def describe(self, indent='', json_dict=None):
        """Write out information about what this step will do
        If json_dict is passed in, add information to that dictionary
        so that it can be written out by the controller as appropriate.
        """

        # Call superclasses which will print some information
        next_node = super().describe()

        # Local copies of variables in a dictionary
        P = self.parameters.values_to_dict()

        text = self.description_text(P)

        job.job(__(text, indent=self.indent + '    ', **P))

        return next_node

    def run(self):
        """Run a Cassandra step.
        """
        # Get the values of the parameters, dereferencing any variables
        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        # Temporary code just to print the parameters. You will need to change
        # this!
        for key in P:
            print('{:>15s} = {}'.format(key, P[key]))
            printer.normal(
                __(
                    '{key:>15s} = {value}',
                    key=key,
                    value=P[key],
                    indent=4 * ' ',
                    wrap=False,
                    dedent=False
                )
            )

        return super().run()

    def analyze(self, indent='', **kwargs):
        """Do any analysis needed for this step, and print important results
        to the local step.out file using 'printer'
        """

        printer.normal(
            __(
                'This is a placeholder for the results form step '
                'Cassandra',
                indent=4 * ' ',
                wrap=True,
                dedent=False
            )
        )
