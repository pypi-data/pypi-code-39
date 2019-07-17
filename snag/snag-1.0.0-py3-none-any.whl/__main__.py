from . import core
from . import fetch
from . import logger

s = core.Core()
if s.download(s.programs):
    s.log_results()
else:
    s.logger.log("Operation failed")
