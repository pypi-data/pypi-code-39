import json

from .module_resources import ModuleResource

class NamedtupleDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        self.spec = kwargs.pop('spec')
        super().__init__(object_hook=self._object_hook, *args, **kwargs)

    def _object_hook(self, json_dict):
        return ModuleResource.mapping_to_namedtuple(json_dict, self.spec, 'json')


class JsonModuleResource(ModuleResource):
    filename_glob = '*.json'

    def create_module(self, spec):
        json_filepath = self.import_request_to_filepath(spec)
        json_data = json_filepath.read_text()
        return json.loads(json_data, cls=NamedtupleDecoder, spec=spec)
