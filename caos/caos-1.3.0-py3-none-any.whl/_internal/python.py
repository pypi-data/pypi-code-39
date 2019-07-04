"""python - provide an easy access for python in the virtual environment"""

import os
import subprocess
import caos.common
from caos._internal import update as update_module
from caos._internal.exceptions import (
    VenvNotFound, VenvBinariesMissing
)


def _execute_python(args:list, is_unittest:bool = False) -> int:
    if is_unittest:
        process=subprocess.run(
            [os.path.abspath(path=caos.common.constants._PYTHON_PATH)] + args,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(process.stdout)
        print(process.stderr)
        return process.returncode

    process=subprocess.run(
        [os.path.abspath(path=caos.common.constants._PYTHON_PATH)] + args
    )
    return process.returncode


def run_python(args:list, is_unittest:bool = False) -> int:
    try:
        
        if not update_module._venv_exists():
            raise VenvNotFound()

        if not update_module._are_venv_binaries_available():
            raise VenvBinariesMissing()

        return_code = _execute_python(args)
        return return_code

    except VenvNotFound:
        print(update_module._console_messages["no_venv_found"])
        return 1
    except VenvBinariesMissing:
        print(update_module._console_messages["missing_venv_binaries"])
        return 1
    except Exception:
        return 1