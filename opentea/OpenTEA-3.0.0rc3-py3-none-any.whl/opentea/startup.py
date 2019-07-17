""" module for Opentea startup """
import os


def tcl_starter(file_obj, project=None):
    """Start the tcl process.

    Parameters :
    ------------
    file_obj : the __file__ of the caller
    project : valid project location

    Effect :
    --------
    NOT STATELESS
    TCL REPLACES THE CURRENT PYTHON PROCESS

    """
    app_path = (os.path.dirname(os.path.realpath(file_obj)))

    ot_path = os.path.join(
        (os.path.dirname(os.path.realpath(__file__))),
        "../tcl/opentea3.tcl")

    exec_ = "/usr/bin/wish"
    args = []
    args.append(exec_)
    args.append(ot_path)
    args.append("-app_path")
    args.append(app_path)
    if project is not None:
        args.append("-file")
        args.append(project)
    os.execv(exec_, args)
