from typing import Union

from aom_framework import Environment, Agent
from aom_framework.protocols_pb2 import VersionInfo
from aom_framework.version import __version__

import grpc


def list_versions(cls: Union[Environment, Agent]):
    reply = VersionInfo()
    reply.versions.add(name='aok_sdk', version=__version__)
    reply.versions.add(name='grpc', version=grpc.__version__)

    try:
        for name, version in cls.VERSIONS.items():
            reply.versions.add(name=name, version=version)
    except AttributeError as error:
        pass

    return reply
