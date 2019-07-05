"""
Find, evaluate and parse blueprint files for commands
"""

"""
Generic library imports
"""
import os
import errno
import json
import jsonschema 	as js
import importlib.resources as res
"""
Functional imports
"""
import pyshellwrapper.defs 	as defs
import pyshellwrapper.utils 	as utils
from . import blueprint


class Parser:
	def __init__(self, file_type, json_file, command):
		self.type = file_type
		self.file = json_file
		self.possible_command = command
		self.command = {
			'index'	: 0,
			'name'	: None
		}
	
	"""
	PUBLIC methods
	"""
	def parse(self):
		self.data = self.handle_json()
		return getattr(self, '_parse_{}'.format(self.type))()
			

	@utils.check_method_validity(type=defs.BLUEPRINT)
	def get_flags(self):
		return self.data['flags']

	@utils.check_method_validity(type=defs.BLUEPRINT)
	def get_command_info(self):
		return self.command

	@utils.check_method_validity(type=defs.ROUTINE)
	def get_fixed(self):
		pass

	@utils.check_method_validity(type=defs.ROUTINE)
	def get_variable(self):
		pass
		
	"""
	PRIVATE methods
	"""
	def handle_json(self):

		"""
		User does not need to specify '.json' at the file name end 
		"""
		file_extenstion = '.json'

		if self.file[-len(file_extenstion):] != file_extenstion:
			self.file += file_extenstion
		"""
		Determine if blueprint is custom or built-in
		"""
		if self.file.find('/') != -1:
			with open(self.file, 'r') as file:
				return json.loads(file.read())
		else:
			if res.is_resource(blueprint, self.file):
				return json.loads(res.read_text(blueprint, self.file))


	def _parse_blueprint(self):
		"""
		Validate general structure (flags list and settings)
		Schema can be found in defs.py
		"""
		try:
			js.validate(instance=self.data, schema=defs.GENERAL_SCHEMA)
		except js.exceptions.ValidationError as expt:
			"""
			TODO: wrap to custom exceptions
			"""
			raise SyntaxError(expt)

		"""
		Multiple libraries can be described in one file if 'commands' key
		is present on 'settings' level
		"""
		commands_list = self.data['settings']['commands']
		self.no_of_commands = len(commands_list)

		"""
		User can either omit 'command' argument completely, that means using
		first comand in 'commmands', specify index or command itself
		"""
		if isinstance(self.possible_command, int):
			if self.possible_command > self.no_of_commands:
				raise IndexError("Can't select command with index {}, only {} available".format(self.possible_command, self.no_of_commands))
			elif self.possible_command < 0:
				raise IndexError("Can't select command with negative index {}".format(self.possible_command))

			self.command = {
				'index': self.possible_command,
				'name': commands_list[self.possible_command]
			}	
		elif isinstance(self.possible_command, str):
			if self.possible_command not in commands_list:
				raise ValueError("Specified library '{}' not found in blueprint '{}'".format(self.possible_command, self.file))

			self.command = {
				'index': commands_list.index(self.possible_command),
				'name': self.possible_command
			}	
		else:
			raise TypeError("Specified command must by either index (int) or name (str), is '{}'".format(type(self.possible_command)))

		if self._check_blueprint():
			return True

	def _parse_routine(self):
		pass

	def _check_blueprint(self):
		"""
		'settings' enables to set required flags
		"""
		all_flags = list(self.data['flags'].keys())
		for required_flag in self.data['settings']['required_flags']:
			if required_flag not in all_flags:
				raise KeyError("Flag '{}' is required but not specified in 'flags'".format(required_flag))
		

		"""
		Two schemas are defined, after checking general structure, each flags is 
		validated againts its schema
		"""
		for flag_key, flag_value in self.data['flags'].items():
			if len(flag_value) != self.no_of_commands:
				raise ValueError("Supplied number of libraries {} does not match all listed variants for '{}'".format(self.no_of_commands, flag_key))

			for flag in flag_value:
				"""
				Sometimes one might want to omit partical library's flag, while doing so supplied
				empty object is not valid according to the schema so it's skipped
				"""
				if flag:
					try:
						js.validate(instance=flag, schema=defs.FLAG_SCHEMA)
					except js.exceptions.ValidationError as expt:
						raise SyntaxError(expt)
		return True

	def _check_routine(self):
		"""
		Validate general structure (fixed flags and variable flags)
		Schema can be found in defs.py
		"""
		pass
			
