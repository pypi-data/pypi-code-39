import logging

from fxq.ae.agent.constants import LOGGING_FORMAT
from fxq.ae.agent.fxq_ae_agent_app import app

logging.basicConfig(format=LOGGING_FORMAT, level=logging.getLogger('gunicorn.error').level)
application = app
