from __future__ import print_function

import json
import os
import re
import subprocess

from IPython.core import magic_arguments as m_args
from IPython.core.magic import (Magics, magics_class, cell_magic, line_cell_magic)
from IPython.utils.tempdir import TemporaryDirectory


PicatModels = {}


@magics_class
class PicatMagics(Magics):

    @m_args.magic_arguments()
    # @m_args.argument('-v', '--verbose', action='store_true', help='Verbose output')
    # @m_args.argument('-m', '--mode', choices=["return", "bind"], default="return", help='Here is a helper message')
    # @m_args.argument('-t', '--time-limit', type=int, help='Time limit in milliseconds')
    # @m_args.argument('-s', '--solver', default="solver", help='Solver to run')
    @m_args.argument('prg', nargs='*', default=[], help='Program inside the cell to execute')
    @m_args.argument('-e', '--execute', help='Execute a Picat program')
    # @m_args.argument('-i', '--input', nargs='+', help='Input variables')
    # @m_args.argument('-b', '--bind', nargs='+', help='Bind the return to variable')
    
    @line_cell_magic
    def picat(self, line, cell=None):
        """Picat magic"""
        picat_proc = ["picat"]

        args = m_args.parse_argstring(self.picat, line)

        # inputs = {}
        # # inputs = []
        # if args.input:
        #     for var in args.input:
        #         if var in self.shell.user_ns.keys():
        #             inputs[var] = self.shell.user_ns[var]
        #             # inputs.append(self.shell.user_ns[var])
        #         else:
        #             return var + " is undefined"
        
        #
        # Executes a script in the same directory
        #
        if args.execute:
            picat_test = picat_proc[:]
            my_env = os.environ.copy()

            pipes = subprocess.Popen(
                picat_test + [args.execute],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)
            (output, erroutput) = pipes.communicate()
            if pipes.returncode != 0:
                print(erroutput.rstrip().decode())
                return
            print(output.decode('utf-8'))       
            return

        picat_test = picat_proc[:]
        # if args.verbose:
        #     picat_proc.append("-v")

        my_env = os.environ.copy()

        with TemporaryDirectory() as tmpdir:
            with open(tmpdir + "/prg.pi", "w") as prgf:
                for m in args.prg:
                    picat = PicatModels.get(m)
                    if picat is not None:
                        args.prg.remove(m)
                        prgf.write(picat)
                if cell is not None:
                    prgf.write(cell)
                prgf.close()
                pipes = subprocess.Popen(
                    picat_test + [tmpdir + "/prg.pi"] + args.prg,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)
                (output, erroutput) = pipes.communicate()
                if pipes.returncode != 0:
                    print(erroutput.rstrip().decode())
                    return
                print(output.decode('utf-8'))
        return

    @cell_magic
    def picat_model(self, line, cell):
        args = m_args.parse_argstring(self.picat, line)
        if not args.prg:
            print("No program name provided")
            return
        elif len(args.prg) > 1:
            print("Multiple program names provided")
            return

        PicatModels[args.prg[0]] = cell
        return


def check_picat():
    try:
        pipes = subprocess.Popen(["picat", "--version"],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output, erroutput) = pipes.communicate()
        if pipes.returncode != 0:
            print("Error while initialising extension: cannot run picat. "
                  "Make sure it is on the PATH when you run the Jupyter server.")
            return False
        print(output.rstrip().decode())
    except OSError as _:
        print("Error while initialising extension: cannot run picat. "
              "Make sure it is on the PATH when you run the Jupyter server.")
        return False
    return True
