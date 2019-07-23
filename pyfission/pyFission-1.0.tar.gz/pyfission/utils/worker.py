import sys
from os.path import join
import subprocess
from pyfission.custom_logging.__main__ import func_logger


@func_logger(ignore_args=[2], ignore_kwargs=['command_list'])
def bash_multi_ops(log, config, command_list: list, chunk_size: int = 5):
    """
    Wrapper to create a bash file which invokes commands in parallel (chunk_size) and serial
    :param log: logger object for logging progress
    :param config: config module
    :param command_list: list of command to be executed in parallel
    :param chunk_size: Number of ops to run in parallel (Default = 5)
    :return: executes all ops in parallel
    """
    log_file_name = log.handlers[0].baseFilename.split('/')[-1]
    guid = log_file_name.split('__')[-1]

    filename = join(config.dir_logs, log_file_name + '.sh')
    with open(filename, 'w') as f_out:
        # shebangs & fail on error
        for _cmd in ["#!/bin/bash", "# Fail on 1'st error", "set -e"]:
            f_out.write(_cmd)
            f_out.write("\n")

        f_out.write("\n")

        command_list_chunks = [command_list[i:i + chunk_size] for i in range(0, len(command_list), chunk_size)]
        for chunk in command_list_chunks:
            f_out.write(" & ".join(chunk) + " ;\n")

    bash_exec = ['bash', f'{filename}']
    try:
        # _ = subprocess.check_output(bash_exec, universal_newlines=True)
        comp_process = subprocess.run(bash_exec, universal_newlines=True)  # Recommeded instead of check_output
        if comp_process.returncode != 0:
            sys.exit(1)
    except Exception as e:
        log.info(f"Error logged: {e}")
        sys.exit(1)

    return None
