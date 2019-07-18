import sys

import pandas as pd

from .. import _common

from ._instantiate import instantiate


class Model:

    def __init__(self):
        self.definitions = list()

    def build(self, metadata):
        self.definitions = instantiate(sys.modules[self.__class__.__module__], metadata)

        return pd.DataFrame(self.definitions)

    def to_dataframe(self):
        return pd.DataFrame(self.definitions)


class Mixin:

    def __init__(self, definition):
        if isinstance(definition, Asset):
            self.asset_definition = definition.asset_definition
        elif isinstance(definition, pd.DataFrame):
            if len(definition) != 1:
                raise Exception('DataFrame must be exactly one row')
            self.asset_definition = definition.to_dict(orient='records')[0]
        elif isinstance(definition, pd.Series):
            self.asset_definition = definition.to_dict()
        else:
            self.asset_definition = definition

        self.asset_definition['Type'] = 'Asset'
        self.asset_definition['Template'] = self.__class__.__name__.replace('_', ' ')

    def build(self, metadata):
        definitions = list()
        object_methods = [getattr(self, method_name) for method_name in dir(self)
                          if callable(getattr(self, method_name))]

        for func in object_methods:
            if not hasattr(func, 'spy_model'):
                continue

            attribute = func(metadata)
            attribute['Template'] = self.__class__.__name__.replace('_', ' ')

            if _common.present(self.asset_definition, 'Path'):
                attribute['Path'] = self.asset_definition['Path']

            if _common.present(self.asset_definition, 'Asset'):
                attribute['Asset'] = self.asset_definition['Asset']

            definitions.append(attribute)

        return definitions


class Asset(Mixin):

    def __init__(self, definition):
        Mixin.__init__(self, definition)

    def build(self, metadata):
        definitions = Mixin.build(self, metadata)
        definitions.append(self.asset_definition)
        return definitions

    @classmethod
    def Attribute(cls):
        def attribute_decorator(func):
            def attribute_wrapper(self, metadata):
                func_results = func(self, metadata)

                attribute_definition = dict()

                def _preserve_originals():
                    for key in ['Name', 'Path']:
                        if _common.present(attribute_definition, key):
                            attribute_definition['Referenced ' + key] = attribute_definition[key]
                            del attribute_definition[key]

                if isinstance(func_results, pd.DataFrame):
                    if len(func_results) == 1:
                        attribute_definition.update(func_results.iloc[0].to_dict())
                        _preserve_originals()
                        attribute_definition['Reference'] = True
                    elif len(func_results) > 1:
                        print('Multiple attributes returned by "%s"' % (func.__name__, func_results))

                elif isinstance(func_results, dict):
                    attribute_definition.update(func_results)
                    reference = _common.get(func_results, 'Reference')
                    if reference is not None:
                        if isinstance(reference, pd.DataFrame):
                            if len(reference) == 1:
                                attribute_definition = reference.iloc[0].to_dict()
                                _preserve_originals()
                                attribute_definition['Reference'] = True
                            elif len(reference) > 1:
                                print('Multiple attributes returned by "%s"' % (func.__name__, func_results))

                if not _common.present(attribute_definition, 'Name'):
                    attribute_definition['Name'] = func.__name__.replace('_', ' ')

                return attribute_definition

            setattr(attribute_wrapper, 'spy_model', 'attribute')

            return attribute_wrapper

        return attribute_decorator
