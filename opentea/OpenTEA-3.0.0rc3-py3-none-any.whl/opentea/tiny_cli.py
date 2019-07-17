""" module to set up a tiny command line interface cli for opentea startup"""

# def cli_print(msg):
#     """ print for cli, using terminal for the moment """
#     print(msg)
#
# def cli_start_banner():
#     """ startup banner """
#     cli_print("\n \m/_(>_<)_\m/")

# def cli_warning(msg):
#     """ warning message """
#     cli_print("(-_- ;) "+ msg)
#
# def cli_error(msg):
#     """ error message """
#    cli_print("t(-,-t) "+ msg)


def cli_exit_continue():
    """Ask exit or continue on the command line."""
    if cli_question("Continue") is False:
        raise RuntimeError("User aborted through command line")


def cli_question(msg):
    """Ask a question on the comand line."""
    cont_ = input(msg + " Y/N?")
    # will moveto input() for py3
    out = (cont_ not in ["Y", "y", "yes", "YES"])

    return out


if __name__ == "__main__":
    while True:
        cli_exit_continue()
