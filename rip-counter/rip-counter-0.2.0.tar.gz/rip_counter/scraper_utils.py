import logging
import io


class InvalidIncapsulaSession(Exception):
  def __str__(self):
    mess = 'Your Incapsula session has expired. '
    mess += 'Generate a new Incapsula cookie at https://www.referendum.interieur.gouv.fr/consultation_publique/8'
    return mess


def _check_valid_cookie(response):
  """Check page is valid
  """
  iframe_src = response.css('iframe').xpath('@src').get()
  if iframe_src and 'Incapsula' in iframe_src:
    raise InvalidIncapsulaSession()


def _batch(iterable, n=1):
  l = len(iterable)
  for ndx in range(0, l, n):
    yield iterable[ndx:min(ndx + n, l)]


class TqdmToLogger(io.StringIO):
  """Output stream for TQDM which will output to logger module instead of
  the stdout.
  """
  logger = None
  level = None
  buf = ''

  def __init__(self, logger, level=None):
    super().__init__()
    self.logger = logger
    self.level = level or logging.INFO

  def write(self, buf):
    self.buf = buf.strip('\r\n\t ')

  def flush(self):
    self.logger.log(self.level, self.buf)
