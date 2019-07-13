from .codes import ErrorCode


class ErrorCodeException(Exception):
	def __init__(self, error_code: ErrorCode, code = None, params = None):
		self.error_code = error_code
		super().__init__(error_code.description, code, params)


class VerificationException(Exception):
	def __init__(self, message, code = None, params = None):
		super().__init__(message, code, params)


class FieldsException(Exception):
	def __init__(self, fields: dict, message, code = None, params = None):
		super().__init__(message, code, params)
		self.fields = fields
		self.error_code = ErrorCode.INVALID_FIELD_VALUE