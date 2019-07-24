import pprint


class ZabbixCTL(object):
    def __init__(self, zapi, hosts=None, graphs=None, interfaces=None, **kwargs):
        self.zapi = zapi
        self.hosts = hosts
        self.graphs = graphs
        self.interfaces = interfaces
        self.main_options = kwargs

    def __repr__(self):
        return 'zabbixctl-options:\n{}\nhosts:\n{}\ngraphs:\n{}\ninterfaces:\n{}'.format(
            pprint.pformat(self.main_options),
            pprint.pformat(self.hosts),
            pprint.pformat(self.graphs),
            pprint.pformat(self.interfaces),
        )

