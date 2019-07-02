class BaseError(Exception):
    '''
    A base error class.
    '''

    def __init__(self, message, type, code, display_message):
        super(BaseError, self).__init__(message)

        # In Python 3, the Exception class does not expose a `message`
        # attribute so we need to set it explicitly. See
        # https://www.python.org/dev/peps/pep-0352/#retracted-ideas.
        self.message = message

        self.type = type
        self.code = code
        self.display_message = display_message


class APIError(BaseError):
    '''Encapsulate info about an error encountered interacting certns API'''

    def __init__(self, message, type, code, display_message, request_id='', causes=None):
        super(APIError, self).__init__(message, type, code, display_message)
        self.request_id = request_id
        self.causes = [
            APICause(
                cause['error_message'],
                cause['error_type'],
                cause['error_code'],
                cause.get('display_message', ''),
                cause['item_id'],
            )
            for cause in causes or []
        ]

    @staticmethod
    def from_response(response):
        '''
        Create an error of the right class from an API response.
        '''
        cls = ERROR_TYPE_MAP.get(response['error_type'], APIError)
        return cls(
            response['error_message'],
            response['error_type'],
            response['error_code'],
            response['display_message'],
            response['request_id'],
            response.get('causes'),
        )


class APICause(BaseError):
    '''
    Encapsulate info about the cause of an error encountered
    '''

    def __init__(self, message, type, code, display_message, item_id):
        super(APICause, self).__init__(message, type, code, display_message)
        self.item_id = item_id


class InvalidRequestError(APIError):
    '''The request is malformed and cannot be processed.'''

    pass


class InvalidInputError(APIError):
    '''The request is correctly formatted, but the values are incorrect.'''

    pass


class RateLimitExceededError(APIError):
    '''The request is valid but has exceeded established rate limits.'''

    pass


class ServerError(APIError):
    '''Planned maintenance or an API internal server error.'''

    pass


class ItemError(APIError):
    '''There is invalid information about an item or it is not supported.'''

    pass


class InstitutionError(APIError):
    '''There are errors for the requested financial institution.'''

    pass


ERROR_TYPE_MAP = {
    'INSTITUTION_ERROR': InstitutionError,
    'INVALID_REQUEST': InvalidRequestError,
    'INVALID_INPUT': InvalidInputError,
    'RATE_LIMIT_EXCEEDED': RateLimitExceededError,
    'API_ERROR': ServerError,
    'ITEM_ERROR': ItemError,
}
