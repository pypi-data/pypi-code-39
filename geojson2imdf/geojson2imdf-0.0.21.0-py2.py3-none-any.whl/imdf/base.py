import uuid


class IMDFBase():
    def __init__(self):
        self.id = str(uuid.uuid4())
