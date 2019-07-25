import os
import pkgutil
import warnings

import yara

from ..py2compat import import_module


def load_yara_rules(search_paths):
    """
    Recursively looks for Yara files

    :param search_paths: List of searched paths
    :rtype: :class:`yara.Rules`
    """
    rule_files = {}
    for search_path in search_paths:
        for root, _, files in os.walk(search_path):
            for fname in files:
                if not (fname.endswith(".yar") or fname.endswith(".yara")):
                    continue
                ruleset_name = os.path.splitext(os.path.basename(fname))[0]
                ruleset_path = os.path.join(root, fname)
                if ruleset_name in rule_files:
                    warnings.warn("Yara file name collision - {} overriden by {}".format(
                        rule_files[ruleset_name],
                        ruleset_path
                    ))
                rule_files[ruleset_name] = ruleset_path
    # Compile everything
    return yara.compile(filepaths=rule_files)


def load_modules(search_paths, onerror=None):
    """
    Loads plugin modules under specified paths

    :param search_paths: List of searched paths
    :param onerror: ImportError handler (default: ImportError exceptions are ignored)
    :return: dict {name: module}
    """
    modules = {}
    for importer, module_name, is_pkg in pkgutil.iter_modules(search_paths, "malduck.extractor.modules."):
        if not is_pkg:
            continue
        if module_name in modules:
            warnings.warn("Module collision - {} overriden".format(module_name))
        try:
            modules[module_name] = import_module(importer, module_name)
        except ImportError as exc:
            if onerror:
                onerror(exc)
    return modules
