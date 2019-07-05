import os
import numpy as np
from pathlib import Path

# TODO: can main() be given argument by argparse
# TODO: integrate kappas guessing into .yml file, propt for fit indices

from . import __version__
from .datareader import Data
from .constants import Constants
from .analysis import Analyzer
from .logmaker import Logmaker

from . import __file__
examples_dir = "/" + __file__.strip("/__init__.py") + "/example"

"""
INFO

This module provides the command line interface
"""


class TupleLengthError(Exception):
    pass


class TupleValueError(Exception):
    pass


def constants_dialogue(flg):
    if flg == 'fromFile':
        while True:
            try:
                print("  :: '.yml' files in current directory: ")
                print("  -------------------------------------")
                printfiles('.yml')
                print()
                file_path = input("* specify .yml file for sample: ")
                if file_path == 'example':
                    return Constants.fromFile(
                        examples_dir
                        + "/sample_file_example.yml").getvals()
                else:
                    assert os.path.isfile(file_path)
                    assert file_path.endswith('.yml')
            except AssertionError:
                print("file does not exist or invalid file type")
                continue
            else:
                break
        return Constants.fromFile(file_path).getvals()
    elif flg == 'manualStart':
        return Constants.manualStart().getvals()
    else:
        raise ValueError("invalid flag '{}''".format(flg))


def data_dialogue():
    while True:
        try:
            print()
            print("  :: '.csv' files in current directory: ")
            print("  -------------------------------------")
            printfiles('.csv')
            print()
            file_path = input("* specify .csv file "
                              "containing measured data: ")
            if file_path == 'example':
                return Data(examples_dir
                            + "/measured_data_example.csv")
            else:
                assert os.path.isfile(file_path)
                assert file_path.endswith('.csv')
        except AssertionError:
            print("file does not exist or is invalid type")
            continue
        else:
            break
    return Data(file_path)


def kappas_dialogue(layer_names):
    print()
    print("* enter a guess for each layer's thermal conductivity in [W/m/K]")
    kappas, fit_indices = [], []
    for i, layer_name in enumerate(layer_names):
        print()
        while True:
            try:
                kappa_i = float(input("    thermal conductivity of LAYER #{}"
                                      " ({}): "
                                      .format((i + 1), layer_name)))
                kappas.append(kappa_i)
            except ValueError:
                print("invalid input; numerical values only")
                continue
            else:
                break
        while True:
            try:
                ans = input("    adjust this value when fitting? [y/n]: ")
                assert ans in ['y', 'Y', 'n', 'N']
            except AssertionError:
                continue
            else:
                if ans in ['y', 'Y']:
                    fit_indices.append(i)
                break
    return np.array(kappas, dtype=np.double), fit_indices


def eq_l_dialogue():
    print()
    print("* specify equivalent layers using (semicolon-separated "
          "list of) tuples")
    print("  ex: '(2,4)' OR '(1,3); (4,5)'")
    print("  press <Enter> to skip")
    while True:
        try:
            print()
            ans_str = input("  equivalent layer pairs: ")
            if ans_str == '':
                equivalent_layers = None
            else:
                assert ans_str.count('(') != 0
                assert ans_str.count('(') == ans_str.count(')')
                tupl_str_list = ans_str.split(';')
                equivalent_layers = []
                for tupl_str in tupl_str_list:
                    tmp = tupl_str.strip(' ')
                    tmp = tmp.strip('(')
                    tmp = tmp.strip(')')
                    val_str_list = tmp.split(',')
                    tupl = (int(val_str_list[0]), int(val_str_list[1]))
                    if any(val <= 0 for val in tupl):
                        raise TupleValueError
                    if len(tupl) > 2:
                        raise TupleLengthError
                    equivalent_layers.append(tupl)
        except TupleValueError:
            print("invalid tuple values; positive integers only")
            continue
        except TupleLengthError:
            print("valid syntax is tuples of length 2; use transitivity for "
                  "equivalence between 3 items")
            continue
        except AssertionError:
            print("invalud input; bracket mismatch")
            continue
        else:
            break
    return equivalent_layers


def substrate_dialogue():
    print()
    while True:
        try:
            ans = input("* estimate substrate thermal conductvitiy "
                        "before fitting? (recommended) [y/n]: ")
            assert ans in ['y', 'Y', 'n', 'N']
        except AssertionError:
            continue
        else:
            use_substrate_guess = True if ans in ['y', 'Y'] else False
            break

    # Identify substrate layer
    substrate_layer = None
    if use_substrate_guess:
        while True:
            try:
                substrate_layer = int(input("  identify the substrate by "
                                            "entering corresponding "
                                            "LAYER #: "))
                assert substrate_layer > 0
            except ValueError:
                continue
            except AssertionError:
                print("invalid input; use 'LAYER #' = 1, 2, 3, ...")
                continue
            else:
                break
    return substrate_layer, use_substrate_guess


def boundary_typ_dialogue():
    print()
    while True:
        try:
            ans = input("* select boundary type for model: ")
            assert ans in ['semi-infinite', 'adiabatic', 'isothermal']
        except AssertionError:
            print("invalid input: select 'semi-infinite', 'adiabatic',"
                  " or 'isothermal'")
            continue
        else:
            break
    return ans


def iterations_dialogue():
    print()
    while True:
        try:
            ans = int(input(
                "* select number of iterations (usually > 50): "))
            assert ans > 0
        except AssertionError:
            print("positive integers only!")
            continue
        except ValueError:
            print("(positive) integers only!")
            continue
        else:
            break
    return ans


def display_result(layer_names, kappa_result, fit_indices):
    print()
    print("THERMAL CONDUCTIVITIES [W/m/K]")
    print("------------------------------")
    for i, layer_name in enumerate(layer_names):
        print(("{}: {:.2f} (fit)" if i in fit_indices else "{}: {:.2f}")
              .format(layer_name, kappa_result[i]))
    print()
    return


def printfiles(suffix):
    cwd = os.getcwd()
    for dirpath, dirnames, filenames in os.walk(cwd):
        for file in filenames:
            if file.endswith(suffix):
                full_path = Path(os.path.join(dirpath, file))
                print("  " + str(full_path.relative_to(cwd)))


# TODO: maybe this shouldnt be THE main, but just one version of steps
def main():
    print()
    print("Welcome to tc3omega (version {})!".format(__version__))

    # ask to use preconfigured sample file if it exists
    while True:
        try:
            print()
            ans = input("use preconfigured sample file? [y/n]: ")
            assert ans in ['y', 'Y', 'n', 'N']
        except AssertionError:
            continue
        else:
            break

    if ans in ['y', 'Y']:
        print()
        constants = constants_dialogue('fromFile')
    else:
        print()
        constants = constants_dialogue('manualStart')

    # determine location of measured data
    data = data_dialogue()

    # determine initial guesses for kappas
    kappas, fit_indices = kappas_dialogue(constants['layer_names'])

    # determine equivalent layers
    equivalent_layers = eq_l_dialogue()

    # determine if using substrate guessing (slope) method
    substrate_layer, use_substrate_guess = substrate_dialogue()

    # determine model type to use
    boundary_typ = boundary_typ_dialogue()

    # determine number of iterations to use
    N_its = iterations_dialogue()

    print()
    print("calculating fit...")
    A = Analyzer(
        constants, data, kappas, fit_indices, boundary_typ, substrate_layer,
        use_substrate_guess)

    kappa_result = A.MC_fitlinear_dT(
        int(A.num_points/2), equivalent_layers=equivalent_layers, N=N_its)

    display_result(constants['layer_names'], kappa_result, fit_indices)

    logger = Logmaker(A, kappa_result, N_its, equivalent_layers)

    logger.make_log()
    logger.make_plot()
    logger.print_dir_info()
    return


if __name__ == "__main__":
    main()

# TODO: automatically fit to more than one point
# TODO: remove duplicate prompts when equivalent layers set
# TODO: finite boundary types might need more iterations
# TODO: add smart number of iterations chooser?
# TODO: print out quality of fit in CLI and iterations number
