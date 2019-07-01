import simulus

def p(sim, params):
    idx = params['idx']
    sem = params['sem']

    # set the priority of the current process (this is only useful 
    # if we use PRIORITY qdis)
    sim.cur_process().set_priority(abs(idx-3.2))

    # make sure the process wait on the semaphore in order
    sim.sleep(idx)

    # the process will block on the semaphore and then print out 
    # a message when it is unblocked
    sem.wait()
    print("p[id=%d,prio=%.1f] resumes at %f" % 
          (idx, sim.cur_process().get_priority(), sim.now))

def test(sim, params):
    sem = params['sem']

    # create ten processes which will all block on the semaphore
    for i in range(10):
        sim.process(p, idx=i, sem=sem)
    sim.sleep(100)
    
    # release them all and check the order they are unblocked
    print('-'*40)
    for i in range(10):
        sem.signal()

sim = simulus.simulator()
s1 = sim.semaphore()
s2 = sim.semaphore(qdis=simulus.Semaphore.QDIS_LIFO)
s3 = sim.semaphore(qdis=simulus.Semaphore.QDIS_RANDOM)
s4 = sim.semaphore(qdis=simulus.Semaphore.QDIS_PRIORITY)
sim.process(test, 0, sem=s1)
sim.process(test, 100, sem=s2)
sim.process(test, 200, sem=s3)
sim.process(test, 300, sem=s4)
sim.run()
