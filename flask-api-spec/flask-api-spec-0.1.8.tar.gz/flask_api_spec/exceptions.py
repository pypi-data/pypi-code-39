class ValidationError(ValueError):
    """
    flask_api_spec validation error
    """

    def __init__(self, message, **kwargs):
        ValueError.__init__(self, message)
        self.payload = kwargs.get('payload', None)
