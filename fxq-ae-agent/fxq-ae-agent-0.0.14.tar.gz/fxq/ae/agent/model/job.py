import logging

LOGGER = logging.getLogger(__name__)


class Job:
    def __init__(self, name: str, git_url: str):
        self.name = name
        self.git_url = git_url
        self._links = None

    def to_dict(self):
        return {
            'name': self.name,
            'gitUrl': self.git_url
        }

    @staticmethod
    def of_dict(_dict):
        job = Job(
            _dict["name"],
            _dict["gitUrl"]
        )
        try:
            job._links = _dict["_links"]
        except KeyError:
            LOGGER.info("No Links detected for Job")
        return job
