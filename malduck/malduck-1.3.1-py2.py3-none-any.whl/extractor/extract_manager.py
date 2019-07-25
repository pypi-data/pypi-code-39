import warnings
from collections import defaultdict

from .extractor import YaraMatch, Extractor
from .loaders import load_modules, load_yara_rules


def merge_configs(config, new_config):
    for k, v in new_config.items():
        if k == "family":
            continue
        if k not in config:
            config[k] = v
        elif config[k] == v:
            continue
        elif isinstance(config[k], list):
            for el in v:
                if el not in config[k]:
                    config[k] = config[k] + [el]
        else:
            raise RuntimeError("Extractor tries to override '{old_value}' "
                               "value of '{key}' with '{new_value}'".format(key=k,
                                                                            old_value=config[k],
                                                                            new_value=v))


class ExtractManager(object):
    """
    Multi-dump extraction context. Handles merging configs from different dumps, additional dropped families etc.
    """
    def __init__(self, rules, extractors):
        self.rules = rules
        self.extractors = extractors
        self.configs = {}

    def on_error(self, exc, extractor):
        """
        Handler for all Exception's throwed by :py:meth:`Extractor.handle_yara`.

        :param exc: Exception object
        :param extractor: Extractor object which throwed exception
        """
        import traceback
        warnings.warn("{} throwed exception: {}".format(
            self.__class__.__name__,
            extractor,
            traceback.format_exc()))

    @staticmethod
    def init(modules_path):
        """
        Loads modules from specified path and creates ExtractManager object.

        :param modules_path: Path where extraction modules can be found
        :rtype: :class:`ExtractManager`
        """
        # Load Yara rules
        rules = load_yara_rules([modules_path])
        # Preload modules
        load_modules([modules_path])
        return ExtractManager(rules, Extractor.__subclasses__())

    def push_file(self, filepath, base=0, pe=None):
        from ..procmem import ProcessMemory, ProcessMemoryPE
        """
        Pushes file for extraction. Config extractor entrypoint. 
        
        :param filepath: Path to extracted file
        :param base: Memory dump base address
        :param pe: Determines whether file contains PE (default: detect automatically)
        :return: Matched config or None
        """
        with ProcessMemory.from_file(filepath, base=base) as p:
            if pe is None and p.readp(0, 2) == "MZ":
                pe = True
            if pe:
                p = ProcessMemoryPE.from_memory(p, detect_image=True)
            self.push_procmem(p)

    def push_procmem(self, p):
        """
        Pushes ProcessMemory object for extraction

        :param p: ProcessMemory object
        :type p: :class:`malduck.procmem.ProcessMemory`
        """
        extractor = ProcmemExtractManager(self)
        extractor.push_procmem(p)
        if extractor.config:
            if extractor.family not in self.configs:
                self.configs[extractor.family] = extractor.config
            else:
                merge_configs(self.configs[extractor.family], extractor.config)

    @property
    def config(self):
        """
        Extracted configuration or list of configs if there is more than one extracted family.
        """
        if not self.configs:
            return {}
        elif len(self.configs.keys()) == 1:
            _, config = list(self.configs.items())[0]
            return config
        else:
            return list([config for family, config in self.configs.items()])


class ProcmemExtractManager(object):
    """
    Single-dump extraction context (single family)
    """
    def __init__(self, parent):
        self.collected_config = {}  #: Collected configuration so far (especially useful for "final" extractors)
        self.globals = {}
        self.parent = parent        #: Bound ExtractManager instance
        self.family = None          #: Matched family

    def push_procmem(self, p):
        """
        Pushes ProcessMemory object for extraction

        :param p: ProcessMemory object
        :type p: :class:`malduck.procmem.ProcessMemory`
        """

        matched_rules = defaultdict(list)

        for match in self.parent.rules.match(data=p.m):
            rmatch = YaraMatch(match)
            matched_rules[rmatch.rule].append(rmatch)

        for ext_class in self.parent.extractors:
            extractor = ext_class(self)
            # yara_rules can be single string or list/tuple of strings
            ext_rules = [extractor.yara_rules] \
                if type(extractor.yara_rules) not in [list, tuple] \
                else extractor.yara_rules
            # Call handle_yara for each extractor
            for rules in ext_rules:
                for rmatch in matched_rules[rules]:
                    try:
                        extractor.handle_yara(p, rmatch)
                    except Exception as exc:
                        self.parent.on_error(exc, extractor)

    def push_config(self, config, extractor):
        """
        Pushes new partial config

        If strong config provides different family than stored so far
        and that family overrides stored family - set stored family
        Example: citadel overrides zeus

        :param config: Partial config object
        :param extractor: Extractor object reference
        """
        if "family" in config:
            if not self.family or (
                    self.family != extractor.family and
                    self.family in extractor.overrides):
                self.family = config["family"]

        new_config = dict(self.collected_config)

        merge_configs(new_config, config)

        if self.family:
            new_config["family"] = self.family
        self.collected_config = new_config

    @property
    def config(self):
        """
        Returns collected config, but if family is not matched - returns empty dict
        """
        if self.family is None:
            return {}
        return self.collected_config
