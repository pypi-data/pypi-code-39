from time import time
from .structure import Pipeline, PipeStage

def compute_throughput(pipeline: Pipeline):
    if not pipeline.start_ts:
        raise Exception("Pipeline hasn't started")

    output = {}

    for name in pipeline.stages.keys():
        wps = pipeline.shared_state.get(f"{name}_wps", None)
        output[name]= wps

    return output


def compute_pipe_sizes(pipeline: Pipeline):
    output = {}

    for name, queue in pipeline.queues.items():
        output[name] = queue.qsize()

    return output


def compute_stage_status(pipeline: Pipeline):
    alives = map(lambda s: s.is_alive(), pipeline.stages.values())
    alives = list(alives)
    return alives
