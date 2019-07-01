from loguru import logger
import uuid
import gpxpy
import requests


class HermesDataPoster(object):
    def __init__(self, **args):
        self.args = args

    def export(self):

        header = {
            'x-correlation-id': '{}'.format(uuid.uuid4()),
            'transport-id': str(self.args['transport-id']),
            'transport-type': str(self.args['transport-type']),
            'Date-Event': str(self.args['event_date']),
            'Content-Type': "application/xml"
        }
        try:
            xid = header['x-correlation-id']
            logger.info(
                'request x-correlation-id {}'.format(xid))
            gpx = None
            with (open(self.args['file'])) as source:
                gpx = gpxpy.parse(source)
                del source
            payload = gpx.to_xml(version='1.0')
            url = self.args['config']['FACADE']['URL']
            response = requests.request(
                "POST", url, data=payload, headers=header)
            message = 'request x-correlation-id {} complete with status {}'.format(xid, response)
            logger.info(message)
        except Exception as exception:
            logger.error(exception)
            raise exception
