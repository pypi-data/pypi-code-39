class BitrixException(Exception):
	def __init__(self, error={}, message=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.error = error
		self.message = message

	def __str__(self):
		if self.error:
			return f"{self.error}"
		if self.message:
			return f"{self.message}"