from EventChains import SubChain
from EventChains import NewSubChain
from OrderEvents import OrderEvent
import timeit
import logging


def old_subchain():
    l = xrange(1,1000000)
    o = OrderEvent(12223142445, 21231515122.23212, 132141511, "bob", None)
    logger = logging.getLogger()
    for i in l:
        s = SubChain(1255323443, o, 10, logger)


def new_subchain():
    l = xrange(1, 1000000)
    o = OrderEvent(12223142445, 21231515122.23212, 132141511, "bob", None)
    logger = logging.getLogger()
    for i in l:
        s = NewSubChain(1255323443, o, 10, logger)


x=timeit.timeit(old_subchain, number=3)
print x
y = timeit.timeit(new_subchain, number=3)
print y