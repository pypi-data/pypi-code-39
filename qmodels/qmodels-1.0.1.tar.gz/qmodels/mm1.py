import random, logging
from collections import deque
import numpy as np
import scipy.stats as stats
import simulus

from qmodels.rng import *

__all__ = ['mm1']

class mm1(object):
    def __init__(self, sim, mean_iat, mean_svtime):
        self.sim = sim

        self.inter_arrival_time = expon(mean_iat, sim.rng().randrange(2**32))
        self.service_time = expon(mean_svtime, sim.rng().randrange(2**32))

        self.queue = deque()
        self.in_systems = [(0,0)]
        self.waits = []

        self.logger = logging.getLogger('mm1')
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(name)s: %(levelname)s: %(message)s'))
        self.logger.addHandler(handler)

        sim.sched(self.arrive, offset=next(self.inter_arrival_time))

    def arrive(self):
        '''Event handler for customer arrival.'''
        self.logger.info('%g: customer arrives (num_in_system=%d->%d)' %
                         (sim.now, len(self.queue), len(self.queue)+1))

        # add the customer to the end of the queue
        self.queue.append(self.sim.now)
        self.in_systems.append((self.sim.now, len(self.queue)))
    
        # schedule next customer's arrival
        self.sim.sched(self.arrive, offset=next(self.inter_arrival_time))
    
        # the arrived customer is the only one in system
        if len(self.queue) == 1:
            # schedule the customer's departure
            self.sim.sched(self.depart, offset=next(self.service_time))
        
    def depart(self):
        '''Event handler for customer departure.'''
        self.logger.info('%g: customer departs (num_in_system=%d->%d)' %
                         (sim.now, len(self.queue), len(self.queue)-1))

        # remove a customer from the head of the queue
        t = self.queue.popleft()
        self.in_systems.append((self.sim.now, len(self.queue)))
        self.waits.append(self.sim.now-t)
    
        # there are remaining customers in system
        if len(self.queue) > 0:
            # schedule the next customer's departure
            self.sim.sched(self.depart, offset=next(self.service_time))

if __name__ == '__main__':
    random.seed(13579) # global random seed
    sim = simulus.simulator('mm1') # create a simulator instance
    q = mm1(sim, 1.2, 0.8) # create the m/m/1 queue
    q.logger.setLevel(logging.INFO)
    sim.run(10)
