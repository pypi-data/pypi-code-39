#yourNumber = float('0.1')
#yourNumber = float('alex')
#print(isinstance(yourNumber, (int, float)))
import logging

_LOGGER = logging.getLogger(__name__)

_LOGGER.error('alex %s', 0.01)
