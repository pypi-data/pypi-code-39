#!/usr/bin/env python

import os


from radical.entk import Pipeline, Stage, Task, AppManager


hostname =     os.environ.get('RMQ_HOSTNAME', 'localhost')
port     = int(os.environ.get('RMQ_PORT', 5672))


# ------------------------------------------------------------------------------
#
def generate_pipeline():

    p  = Pipeline()
    s1 = Stage()

    t = Task()
    t.pre_exec             = ['echo module load intel',
                              'echo module load intel-mpi',
                              'echo module load cudatoolkit']

    t.name                 = 'my-first-task'
    t.executable           = '/bin/echo'
    t.arguments            = ['Hello GPU world']
    t.download_output_data = ['STDOUT', 'STDERR']
    t.gpu_reqs             = {'processes'           : 1,
                              'process_type'        : None,
                              'threads_per_process' : 1,
                              'thread_type'         : None}

#   # Appmanager
#   res_dict               = {'resource' : 'princeton.tiger_gpu',
#                             'project'  : 'geo',
#                             'queue'    : 'gpu',
#                             'schema'   : 'local',
#                             'walltime' : 10,
#                             'cpus'     : 1,
#                             'gpus'     : 1}
#

    s1.add_tasks(t)
    p.add_stages(s1)

    return p


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    pipelines = []

    for cnt in range(1):
        pipelines.append(generate_pipeline())

    appman = AppManager(hostname=hostname, port=port)

    res_dict = {'resource': 'local.localhost',
                'walltime': 10,
                'cpus'    : 10,
                'cgus'    : 1}

    appman.resource_desc = res_dict
    appman.workflow      = set(pipelines)
    appman.run()


# ------------------------------------------------------------------------------

