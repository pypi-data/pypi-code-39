import json
import logging
import os
import socket

from datetime import datetime

from .encoder import LoggingEncoder


logger = logging.getLogger(__name__)


LEVELNAME = os.environ.get('LEVELNAME', 'LOCAL')
INSTANCE_NAME = socket.gethostname()
ECS_TASK_NAME = os.environ.get('TASK_NAME')


class JsonFormatter(logging.Formatter):
    def __init__(
        self,
        appname,
        levelname=LEVELNAME,
        instance_name=INSTANCE_NAME,
        ecs_task_name=ECS_TASK_NAME,
        **kwargs
    ):
        super().__init__()
        self.appname = appname
        self.levelname = levelname
        self.instance_name = instance_name
        self.ecs_task_name = ecs_task_name
        self.kwargs = kwargs

    def usesTime(self):
        return True

    def format(self, record, etime=None):
        try:
            body = super().format(record)
        except Exception as e:
            logger.error(
                f'Log formatting error: {e}, logrecord_msg: {record.msg}, '
                f'logrecord_args: {record.args}'
            )
            return None

        if etime is None:
            etime = datetime.utcnow()

        info_keys = [
            x for x in record.__dict__ if x not in {'args', 'context'}
        ]
        info = {
            **{key: getattr(record, key, '') for key in info_keys},
            **self.kwargs,
            'created': etime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'appname': self.appname,
            'ecs_task_name': self.ecs_task_name,
            'instance_name': self.instance_name,
            'levelname': self.levelname,
            'loggername': record.name,
            'message': body,
        }
        if record.args and isinstance(record.args, dict):
            info.update(record.args)

        return json.dumps(
            {
                'context': getattr(record, 'context', {}),
                'info': info,
            },
            cls=LoggingEncoder,
        )
