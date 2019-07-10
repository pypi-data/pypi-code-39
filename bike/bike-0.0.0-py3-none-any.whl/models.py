from .fields import Field
from .errors import ValidateError


class Model:
	
	@classmethod
	def load(cls, data, raise_exceptions=True):
		cls.pre_load()
		obj = {}
		errors = {}
		for attr in dir(cls):
			field = getattr(cls, attr)
			if isinstance(field, Field):
				field.name = attr
				val = field.load(data.get(attr, None))
				if val:
					if val[2]:
						errors[attr] = val[2]
					else:
						obj[val[0]] = val[1]
		res = None								
		if raise_exceptions:
			if errors:
				raise ValidateError(errors)
			res = obj
		else:
			res = {'data': obj, 'errors': errors}
		cls.pos_load()
		return res
	
	@classmethod	
	def dump(cls, data):
		pass
		
	@classmethod
	def pre_load(cls):
		pass
		
	@classmethod
	def pos_load(cls):
		pass
