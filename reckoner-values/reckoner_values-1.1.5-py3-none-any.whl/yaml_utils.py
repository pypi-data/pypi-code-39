from collections import OrderedDict
import oyaml as yaml
import json

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)

def olddata_to_yaml(data):
    #represent_dict_order = lambda self, data:  self.represent_mapping('tag:yaml.org,2002:map', data.items())
    #yaml.add_representer(OrderedDict, represent_dict_order)
    return yaml.dump(data, Dumper=Dumper)

def data_to_yaml(data, **options):
    opts = dict(indent=4, default_flow_style=False)
    opts.update(options)
    if 'Dumper' not in opts:
        return yaml.safe_dump(data, **opts)
    else:
        return yaml.dump(data, **opts) 
