# Copyright Jonathan Tremesaygues (2019)
#
# Jonathan Tremesaygues <jonathan.tremesaygues@slaanesh.org>
#
# This software is a computer program whose purpose is to [describe
# functionalities and technical features of your software].
#
# This software is governed by the CeCILL-B license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL-B
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL-B license and that you accept its terms.
import argparse
import os
from ..common.commands import BaseCommand, CommandError
from .models import CoreProject, CoreParameters
from .rtlgeneration.writer import write_core_rtl_into_dir


class CreateCoreCommand(BaseCommand):
    """Create a new kFPGA core"""

    def register(self, subparsers):
        """Register the command
        :param subparsers: The subparsers on which register
        """
        parser = subparsers.add_parser(
            "createcore", help="Create a new kFPGA core project"
        )
        parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            help="force the creation of the project",
        )
        parser.add_argument(
            "-x", "--width", type=int, default=1, help="width of the core"
        )
        parser.add_argument(
            "-y", "--height", type=int, default=1, help="height of the core"
        )
        parser.add_argument(
            "--io", type=int, default=1, help="number of IO per side tile"
        )
        parser.add_argument(
            "-c",
            "--clocks",
            type=int,
            default=0,
            help="number of clocks signals",
        )
        parser.add_argument(
            "-s", "--sets", type=int, default=1, help="number of sets signals"
        )
        parser.add_argument(
            "-r",
            "--resets",
            type=int,
            default=0,
            help="number of resets signals",
        )
        parser.add_argument(
            "-e",
            "--enables",
            type=int,
            default=0,
            help="number of enables signals",
        )
        parser.add_argument(
            "-i",
            "--interconnect_width",
            type=int,
            default=0,
            help="width of the interconnects channels",
        )
        parser.add_argument(
            "--le", type=int, default=1, help="number of LUT in a tile"
        )
        parser.add_argument(
            "--lut", type=int, default=2, help="size of a tile"
        )
        parser.add_argument(
            "-p",
            "--project-dir",
            type=str,
            default=os.getcwd(),
            help="folder in which the project folder is created",
        )
        parser.add_argument(
            "project_name", type=str, help="name of the project"
        )
        parser.set_defaults(func=self.run)

    def run(self, args):
        """Run the command
        :param args: Arguments of the command
        :return: True on success, False otherwise
        """
        # Create the directory of the project
        project_path = os.path.join(args.project_dir, args.project_name)
        if os.path.exists(project_path):
            if not args.force:
                raise CommandError(
                    "The specified project dir already exists. Use --force for forcing the creation."
                )
        else:
            os.makedirs(project_path)

        project_file_path = os.path.join(
            project_path, "{}.kcp".format(args.project_name)
        )

        # Create the project file
        core_parameters = CoreParameters(
            args.width,
            args.height,
            args.io,
            args.clocks,
            args.sets,
            args.resets,
            args.enables,
            args.interconnect_width,
            args.le,
            args.lut,
        )

        project = CoreProject(args.project_name, core_parameters)
        project.save(project_file_path)

        return True


class GenerateRTLCommand(BaseCommand):
    """Generate the RTL of a kFPGA core"""

    def register(self, subparsers):
        """Register the command
        :param subparsers: The subparsers on which register
        """

        parser = subparsers.add_parser(
            "generatertl", help="Generate the RTL of a kFPGA core"
        )
        parser.add_argument("project", type=str, help="the .kcp project file")
        parser.set_defaults(func=self.run)

    def run(self, args):
        """Run the command
        :param args: Arguments of the command
        :return: True on success, False otherwise
        """
        project = CoreProject.load(args.project)
        project_path = os.path.dirname(args.project)

        # Write the RTL
        rtl_path = os.path.join(project_path, "rtl")
        rtl_files = write_core_rtl_into_dir(rtl_path, project.core_parameters)

        # Update the project
        project.rtl_files = rtl_files
        project.save(args.project)

        return True
