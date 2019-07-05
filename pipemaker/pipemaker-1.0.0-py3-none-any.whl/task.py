from .utils.filepath import Filepath
import logging
log = logging.getLogger()

class Task:
    """ minimal executable that gets passed to task queue
    """
    def __init__(self, func, inputs, output, save):
        log.info("initial task")
        self.func = func
        self.inputs = inputs
        self.output = output
        self.save = save

    def load_inputs(self):
        """ inputs can be filepaths loaded on target machine """
        self.indata = {k: v.load() if isinstance(v, Filepath) else v for k, v in self.inputs.items()}

    def run(self):
        from pipemaker.utils.defaultlog import log
        log.info(f"running task {str(self.func)}")
        self.prerun()
        self.outdata = self.func(**self.indata)
        self.postrun()
        log.info("finished running task")
        return self.outdata

    def prerun(self):
        self.load_inputs()

    def postrun(self):
        log.info("inside postrun")
        if self.save:
            self.output.save(self.outdata)