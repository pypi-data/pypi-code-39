# Main logic to handle X-Lambda requests
import logging
import time
from typing import Dict

import xlambda_helper as helper
from xlambda_helper import constants


logger = logging.getLogger()
logger.setLevel(logging.WARNING)


class XLambdaRequest():

    def __init__(self, event: Dict):
        self.xlambda_request = event.get('xlambda')

    @property
    def action(self):
        return self.get_request_param(param='action')

    @property
    def settings(self):
        return self.get_request_param(param='settings')

    @property
    def is_warm_request(self):
        if type(self.action) is not str:
            return None

        else:
            return self.action == constants.WARM_ACTION_INDENTIFIER

    @property
    def warm_method(self):
        return self.get_setting(
            param='warm_method',
            default=constants.DEFAULT_WARM_METHOD,
        )

    @property
    def startup_time(self):
        return self.get_setting(param='startup_time')

    def get_request_param(self, param: str, default=None):
        if type(self.xlambda_request) is dict:
            return self.xlambda_request.get(param)

        else:
            return default

    def get_setting(self, param: str, default=None):
        if type(self.xlambda_request) is dict:
            return self.settings.get(param, default)

        else:
            return default


def warm(handler):
    '''Wraps the Lambda handler function into Lambda helper logic

    :arg handler: the Lambda handler function

    > HOW TO - use as a decorator, like this:

        import xlambda_helper

        @xlambda_helper.warm()
        def lambda_handler(event, context):
            (your code goes here...)
    '''
    def wrapper(event: Dict, context: Dict):
        '''Skip execution of the original Lambda handler in warm-up requests

        :arg event: original event payload received by the Lambda function
        :arg context: context provided by AWS Lambda
        '''
        response = None

        try:
            xlambda_request = XLambdaRequest(event=event)

            is_warm_request = xlambda_request.is_warm_request

            if is_warm_request:
                logger.info('Serving X-Lambda request')
                logger.info(f'IS_COLD_START? {str(constants.IS_COLD_START)}')

                sleep_time = xlambda_request.startup_time

                if not constants.IS_COLD_START and type(sleep_time) is int:
                    logger.info(f'Sleeping for {str(sleep_time)}')
                    time.sleep(sleep_time)

                response = {
                    'status': 200,
                    'xlambda_warmed': True,
                }

        except Exception as error:
            logger.exception(error)
            logger.error('XLambdaHelperError: could not handle request.')

        finally:
            if not response:
                response = handler(event=event, context=context)

        # Now that this container is already warmed up, let's keep in memory
        constants.IS_COLD_START = False

        return response

    return wrapper
