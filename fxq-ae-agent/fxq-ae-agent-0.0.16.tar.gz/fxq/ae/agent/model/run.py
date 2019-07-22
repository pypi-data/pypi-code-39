import uuid
from datetime import datetime
from typing import List, Dict

from fxq.ae.agent.callback.handler import do_callback
from fxq.ae.agent.model.job import Job
from fxq.ae.agent.model.status import Status


class Run:
    def __init__(self, job):
        self.uuid: str = str(uuid.uuid4())
        self.job: Job = job
        self._status: Status = Status.PENDING
        self.started: datetime = datetime.now()
        self.ended: datetime = None
        self.steps: List[Step] = []
        self._links: Dict = None
        do_callback(self)

    def to_dict(self):
        dict = {
            'uuid': self.uuid,
            'status': self.status.name,
            'started': self.started.isoformat(),
            'ended': self.ended.isoformat() if self.ended is not None else None
        }

        if self._links:
            dict["_links"] = self._links

        return dict

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status
        do_callback(self)


class Step:
    def __init__(self, run, number, name, image):
        self.run: Run = run
        self.number: int = number
        self.name: str = name
        self.image: str = image
        self._status: Status = Status.PENDING
        self.commands: List[Command] = []
        self._links = None
        do_callback(self)

    def to_dict(self):
        return {
            'number': self.number,
            'name': self.name,
            'image': self.image,
            'status': self.status.name
        }

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status
        do_callback(self)


class Command:
    def __init__(self, step, number, instruction):
        self.step: Step = step
        self.number: int = number
        self.instruction: str = instruction
        self.std_out: List[str] = []
        self.std_err: List[str] = []
        self._links = None
        do_callback(self)

    def add_output(self, output):
        self.std_out.append(output)
        do_callback(self)

    def add_error(self, error):
        self.std_err.append(error)
        do_callback(self)

    def to_dict(self):
        return {
            'number': self.number,
            'instruction': self.instruction,
            'stdOut': "".join(self.std_out),
            'stdErr': "".join(self.std_err)
        }
