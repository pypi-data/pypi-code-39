from enum import Enum

class Events(Enum):
    """Event Types"""
    FIT_BEFORE = "fit_before"
    FIT_AFTER = "fit_after"

    EPOCH_BEFORE = "epoch_before"
    EPOCH_AFTER = "epoch_after"

    BATCH_BEFORE = "batch_before"
    BATCH_AFTER = "batch_after"

    BACKWARD_BEFORE = "backward_before"
    BACKWARD_AFTER = "backward_after"

    OPTIM_STEP_BEFORE = "optim_step_before"
    OPTIM_STEP_AFTER = "optim_step_after"

    STOP_TRAIN = "stop_train"
    SKIP_EPOCH = "skip_epoch"
    SKIP_BATCH = "skip_batch"
    SKIP_BACKWARD = "skip_backward"
    SKIP_OPTIMIZER_STEP = "skip_optimizer_step"

class StopTrainException(Exception): pass
class SkipEpochException(Exception): pass
class SkipBatchException(Exception): pass
class SkipBackwardException(Exception): pass
class SkipOptimizerStepException(Exception): pass