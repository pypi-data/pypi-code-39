#!/usr/bin/env python

__copyright__ = 'Copyright 2013-2014, http://radical.rutgers.edu'
__license__   = 'MIT'

import os
import sys

import radical.pilot as rp


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':


    if len(sys.argv) == 2: resource = sys.argv[1]
    else                 : resource = 'local.localhost'

    session = rp.Session()

    try:
        pd_init = {'resource'      : resource,
                   'runtime'       : 10,
                   'cores'         : 128
                  }
        pdesc = rp.ComputePilotDescription(pd_init)
        pmgr  = rp.PilotManager(session=session)
        pilot = pmgr.submit_pilots(pdesc)

        umgr = rp.UnitManager(session=session)
        umgr.add_pilots(pilot)

        n = 2  # number of units to run
        cuds = list()
        for i in range(0, n):

            cud = rp.ComputeUnitDescription()
            cud.executable       = '%s/examples/hello_rp.sh' % os.getcwd()
            cud.arguments        = ['5']
            cud.gpu_processes    = 1
            cud.cpu_processes    = 0
            cud.cpu_threads      = 0
            cud.cpu_process_type = rp.POSIX
            cud.cpu_thread_type  = rp.POSIX
            cuds.append(cud)

        umgr.submit_units(cuds)
        umgr.wait_units()


    finally:
        session.close(download=True)


# ------------------------------------------------------------------------------

