#!/usr/bin/env python
"""wlog is a lightweight thin logger that logs against a logger service.

"""

import web_log

_USAGE = """weblog version {}

Usage: wlog application event [extra]\n
       wlog -v (--version)
       wlog -h (--help)
""".format(
    web_log.WEBLOG_VERSION
)


def _exit_with_msg(msg, exitcode=0):
    print(msg)
    exit(exitcode)


def wlog():
    import sys

    args = sys.argv
    if len(args) == 2 and args[1] in ("-v", "--version"):
        _exit_with_msg("wlog {}".format(web_log.WEBLOG_VERSION))
    if len(args) == 2 and args[1] in ("-h", "--help"):
        _exit_with_msg(_USAGE)
    if len(args) < 3:
        _exit_with_msg(_USAGE, exitcode=1)

    extra = ""
    application = args[1]
    event = args[2]
    extra = " ".join(args[3:])
    web_log.log(application, event, extra_info=extra)


if __name__ == "__main__":
    main()
