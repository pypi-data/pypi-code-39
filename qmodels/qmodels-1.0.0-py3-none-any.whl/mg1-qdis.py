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
        sim.process(customer)

def customer():
    server.acquire()
    sim.sleep(next(service_time))
    server.release()

def sim_run(qdis):
    global sim, inter_arrival_time, service_time, server
    sim = simulus.simulator()
    inter_arrival_time = exp_generator(1.2, sim.rng().randrange(2**32))
    service_time = truncnorm_generator(0, 1.6, sim.rng().randrange(2**32))
    dc = simulus.DataCollector(system_times='dataseries(all)')
    server = sim.resource(collect=dc, qdis=qdis)
    sim.process(gen_arrivals)
    sim.run(50000)
    return np.array(dc.system_times.data())

print('mean wait time:')
w1 = sim_run(simulus.QDIS.FIFO)
print('  FIFO: mean=%g, stdev=%g' % (w1.mean(), w1.std()))
w2 = sim_run(simulus.QDIS.LIFO)
print('  LIFO: mean=%g, stdev=%g' % (w2.mean(), w2.std()))
w3 = sim_run(simulus.QDIS.SIRO)
print('  SIRO: mean=%g, stdev=%g' % (w3.mean(), w3.std()))
