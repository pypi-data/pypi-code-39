
import importlib

import logging

logger = logging.getLogger(__name__)

class ExLoader(object):
    """docstring for Handler"""
    def __init__(self):
        super(ExLoader, self).__init__()

    def load_rest(self, ex ,secrets):
     
        mstr = 'ccindividual.exchanges.' + ex + '.trade_rest'

        logger.debug('load class: ' + mstr)

        m = importlib.import_module(mstr) 

        ex_class = getattr (m, 'TradeRest')

        return ex_class(secrets)
 