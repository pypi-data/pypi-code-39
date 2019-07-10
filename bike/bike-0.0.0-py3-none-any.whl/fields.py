from .errors import ValidateError
import datetime as dt
import copy


class Field:
	def __init__(self, default=None, required=False, options=None):
		self.default = default
		self.required = required
		self.options = options
		self.errors = []
	
	def load(self, value):
		self.errors.clear()
		key = self.name
		if not value:
			if self.required:
				self.errors.append({'required': 'Field required'})
			elif self.default:
				self.val = self.default
			else:
				return None
		else:
			self.val = self.validate_type(value)
			self.validate_options()
			self.validates()
		return (key, self.val, self.errors)
		
	def validate_type(self, value):
		pass
		
	def validates(self):
		pass
		
	def validate_options(self):
		if self.options:
			if isinstance(self.options[0], tuple):
				options = [x[0] for x in self.options]
			else:
				options = [x for x in self.options]
			if self.val not in options:
				self.errors.append('Invalid value')
		

class Char(Field):
	def __init__(self, **kwargs):
		super(Char, self).__init__(**kwargs)
		
	def validate_type(self, value):
		try:
			val = str(value)
			if len(val) > 1:
				self.errors.append('Invalid type')
			return val
		except:
			self.errors.append('Invalid type')
			return None
		
		
class String(Field):
	def __init__(self, size=None, **kwargs):
		self.val = None
		self.size = size
		super(String, self).__init__(**kwargs)
		
	def validate_type(self, value):
		try:
			val = str(value)
			return val
		except:
			self.errors.append('Invalid type')
			return None
			
	def validates(self):
		super(String, self).validates()
		self.validate_size()
			
	def validate_size(self):
		if self.size and len(self.val) > self.size:
			self.errors.append(f'Size {self.val} error')
	

class Integer(Field): 
	def __init__(self, **kwargs):
		self.val = None
		super(Integer, self).__init__(**kwargs)
		
	def validate_type(self, value):
		try:
			val = int(value)
			return val
		except:
			self.errors.append('Invalid type')
		return None
		

class Date(Field):
	def __init__(self, format='%Y-%m-%d', **kwargs):
		self.val = None
		self.format = format
		super(Date, self).__init__(**kwargs)
		
	def validate_type(self, value):
		try:
			val = dt.datetime.strptime(value, self.format)
			return val.strftime(self.format)
		except Exception as err:
			self.errors.append('Invalid date')
			return None
	
	
class Bool(Field):
	def __init__(self):
		self.val = None
		super(Bool, self).__init__(**kwargs)
		
	def validate_type(self, value):
		try:
			val = bool(value)
			return val
		except:
			self.errors.append('Invalid type')
			

class Nested(Field):
	def __init__(self, model, **kwargs):
		self.model = model
		super(Nested, self).__init__(**kwargs)
		
	def validate_type(self, value):
		val = self.model.load(value, raise_exceptions=False)
		if val['errors']:
			self.errors.append(val['errors'])
		return val['data']
		

class List(Field):
	def __init__(self, model, **kwargs):
		self.model = model
		super(List, self).__init__(**kwargs)
		
	def validate_type(self, value):
		lst = []
		for i, v in enumerate(value):
			val = self.model.load(v, raise_exceptions=False)
			if val['errors']:
				errors = val['errors']
				self.errors.append(copy.copy(errors))
			lst.append(val['data'])
		return lst

