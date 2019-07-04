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


def main(args=None):
    """Entrypoint of kfpga-creator
    :param args: Args of the command
    :return: True on success, False otherwise
    """
    import argparse
    from ..common.commands import CommandError
    from .commands import CreateCoreCommand, GenerateRTLCommand

    parser = argparse.ArgumentParser(description="kFPGA Creator Tools Suite")

    subparsers = parser.add_subparsers(help="sub-command help")

    command_classes = [CreateCoreCommand, GenerateRTLCommand]

    for command_class in command_classes:
        command = command_class()
        command.register(subparsers)

    args = parser.parse_args(args)
    if not hasattr(args, "func"):
        parser.print_usage()

        return False
    else:
        try:
            return args.func(args)
        except CommandError as e:
            print("error:", e)

            return False
