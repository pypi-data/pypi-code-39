
from configparser import ConfigParser
import logging

from .const import SUPPORTED_EXCHANGES,Channel

logger = logging.getLogger(__name__)

class Config(ConfigParser):

    def __init__(self):
        super(Config, self).__init__()

        self.resolved = None

    def read(self,config_file):
        super().read(config_file)

        logger.info(f"read and resolve config file:{config_file}")

        self.resolved = self.as_dict()

        self.resolved['file_listener']['switch'] = self['file_listener']['switch'] == 'on'
        self.resolved['file_listener']['file_root_path'] = self['file_listener']['file_root_path']
        
        self.resolved['status_listener']['switch'] = self['status_listener']['switch'] == 'on'
        self.resolved['status_listener']['connect_status_minutes'] = int(self['status_listener']['connect_status_minutes'])
        
        self.resolved['redis_listener']['switch'] = self['redis_listener']['switch'] == 'on'
        self.resolved['redis_listener']['redis_host'] = self['redis_listener']['redis_host']
        self.resolved['redis_listener']['redis_port'] = int(self['redis_listener']['redis_port'])
        
        for ex in SUPPORTED_EXCHANGES:
            self.resolved[ex]['switch'] = self[ex]['switch'] == 'on'
            self.resolved[ex]['symbols'] = [ x.strip().split('_') for x in self[ex]['symbols'].split(',')]
            self.resolved[ex]['channels'] = [Channel.rlsv(x.strip()) for x in self[ex]['channels'].split(',')] 

    def as_dict(self):
        d = dict(self._sections)

        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d
