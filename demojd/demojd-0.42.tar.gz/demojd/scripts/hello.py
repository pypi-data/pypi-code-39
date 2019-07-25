from ..src import uncle, other
from ..src.parents import mom, dad
from ..src.parents.kids import boy, girl

import logging
logger = logging.getLogger(__name__)

def hello():
    mom.hello()
    dad.hello()
    boy.hello()
    girl.hello()
    other.hello()
    uncle.hello()
