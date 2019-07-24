# for random distributions, random number generators, statistics
import random
import numpy as np
import scipy.stats as stats

# for simulation
import simulus

random.seed(13579) # global random seed

def exp_generator(mean, seed):
    rv = stats.expon(scale=mean)
    rv.random_state = np.random.RandomState(seed)
    while True:
        # 100 random numbers as a batch
        for x in rv.rvs(100):
            yield x

def truncnorm_generator(a, b, seed):
    rv = stats.truncnorm(a, b)
    rv.random_state = np.random.RandomState(seed)
    while True:
        # 100 random numbers as a batch
        for x in rv.rvs(100):
            yield x

def gen_arrivals():
    while True:
        sim.sleep(next(inter_arrival_time))
        priority = sim.rng().randrange(2)
        sim.process(customer, priority, prio=priority)

def customer(priority):
    t = sim.now
    server.acquire()
    sim.sleep(next(service_time))
    server.release()
    if priority>0: 
        low_waits.append(sim.now-t)
    else:
        high_waits.append(sim.now-t)

def sim_run():
    global sim, inter_arrival_time, service_time, server, low_waits, high_waits
    sim = simulus.simulator()
    inter_arrival_time = exp_generator(1.2, sim.rng().randrange(2**32))
    service_time = truncnorm_generator(0, 1.6, sim.rng().randrange(2**32))
    dc = simulus.DataCollector(system_times='dataseries(all)')
    server = sim.resource(collect=dc, qdis=simulus.QDIS.PRIORITY)
    sim.process(gen_arrivals)
    low_waits, high_waits = [], []
    sim.run(50000)
    return np.array(dc.system_times.data()), np.array(low_waits), np.array(high_waits)

a, b, c = sim_run()
print('all customers: %d, wait time: mean=%g, stdev=%g' % (len(a), a.mean(), a.std()))
print('low priority customers=%d, wait time: mean=%g, stdev=%g' % (len(b), b.mean(), b.std()))
print('high priority customers=%d, wait time: mean=%g, stdev=%g' % (len(c), c.mean(), c.std()))
