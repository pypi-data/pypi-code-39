from apitaxcore.logs.Log import Log
from apitaxcore.logs.StandardLog import StandardLog
from apitaxcore.models.State import State
from apitaxcore.models.Options import Options
from apitaxcore.flow.LoadedDrivers import LoadedDrivers
from apitaxcore.drivers.Drivers import Drivers
from scriptax.parser.utils.BoilerPlate import customizable_parser, read_string, read_file
from scriptax.models.BlockStatus import BlockStatus
from typing import Tuple
from scriptax.parser.Visitor import AhVisitor
from scriptax_runtime.ScriptaxDriver import ScriptaxDriver

import time
import json
import importlib
from pathlib import Path

State.log = Log(StandardLog(), logColorize=False)
State.log.log("")


def make_file_if_not_exist(drivers_path):
    try:
        with open(drivers_path, 'r') as file:
            pass
    except:
        with open(drivers_path, 'w+') as file:
            json.dump({}, file)


def list(drivers_path):
    make_file_if_not_exist(drivers_path)
    with open(drivers_path, 'r') as file:
        return json.load(file)


def execute(file: str, debug: bool = False) -> Tuple[BlockStatus, AhVisitor, float]:
    Drivers.add("scriptax", ScriptaxDriver(path=file))
    LoadedDrivers.load("scriptax")

    drivers_path = Path(Path(__file__).resolve().parents[1]).joinpath('drivers.json')
    packages = list(drivers_path)
    for key, value in packages.items():
        drivers = value['drivers']

        # Imports default driver
        try:
            module = importlib.import_module(key + '.drivers.driver')
            Drivers.add(key, module.driver)
            LoadedDrivers.load(key)
        except:
            print("Unable to load default driver inside of package: " + key)

        # Imports other drivers
        for driver in drivers:
            try:
                module = importlib.import_module(key + '.drivers.' + driver)
                Drivers.add(key + "_" + driver, module.driver)
                LoadedDrivers.load(key + "_" + driver)
            except:
                print("Unable to load driver `" + driver + "` inside of package: " + key)

    start_time = time.process_time()
    block_status, ahvisitor = customizable_parser(read_file(file), file=file, options=Options(debug=debug))
    total_time = time.process_time() - start_time
    return block_status, ahvisitor, total_time
