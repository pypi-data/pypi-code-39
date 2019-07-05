"""
Business logic of the main module.
"""

"""
Generic library imports
"""
from pprint import pprint
"""
Class imports
"""
from pyshellwrapper.parser import Parser
"""
Functional imports
"""
import pyshellwrapper.defs as defs

class PyShellWrapper:
	def __init__(self, blueprint, command=0, reset_after_construct=True, output_format_list=True):
		"""
		Each blueprint can contain multiple libraries so further
		distinguishing needs to take place in form of lib_name providing
		actual name
		"""
		self.blueprint_name = blueprint
		self.command = command
		"""
		Library life cycle can altered to resetting after
		each call of 'construct' method
		"""
		self.reset = reset_after_construct
		self.output_format_list = output_format_list
		"""
		Internal structure for storing flags
		"""
		self.structure = {
			'fixed'		: {
				'already_set'	: [],
				'transformed'	: []
			},
			'variable'	: {},
			'aux': []
		}

		"""
		TODO: this variable is not needed for multiple variable 
		flags but this version only support 1
		"""
		self.is_variable_set = False

		"""
		Fetch correct blueprint for command 
		"""
		self._get_blueprint()

	"""
	PUBLIC methods
	"""
	def list_flags(self):
		"""
		Info for user which flags are ready to be used
		"""
		return list(self.flags_match_table.keys())

	def construct(self):
		"""
		Transform abstract data structure to list used by subprocess 
		"""
		output_buffer = []
		"""
		Add command
		"""
		output_buffer += [self.command_name]
		"""
		Add fixed
		"""
		output_buffer += self.structure['fixed']['transformed']
		aux = self.structure['aux']
		"""
		Add variable
		"""

		variables = self._add_variable()
		if len(variables):
			for var in variables:
				output = output_buffer + var + aux 
				yield output if self.output_format_list else ' '.join(output)
		else:
			output = output_buffer + aux
			yield output if self.output_format_list else ' '.join(output)
		"""
		Cleanup after construction
		"""
		if self.reset:
			self.structure['fixed']['already_set'] = []
			self.structure['fixed']['transformed'] = []
		

	def set_from_routine(self, routine_file):
		parser = Parser('routine', routine_file)

		pass

	def set_fixed(self, **kwargs):
		for flag, opts in kwargs.items():
			"""
			Setting a flag is only allowed once
			"""
			already_set = self.structure['fixed']['already_set']
			if flag in already_set:
				raise ValueError('Flag \'{}\' is already set, fixed flags can only be set once.'.format(flag))
			else:
				already_set.append(flag)
			"""
			Find corresponding partition of the blueprint and 
			transform flag accordingly 
			"""
			flag_blueprint = self._match_flag(flag)
			self.structure['fixed']['transformed'] += self._transform_flag(flag_blueprint, opts)


	def set_variable(self, **kwargs):
		for flag, opts in kwargs.items():
			"""
			Support only for one variable flag
			"""
			if not self.is_variable_set or self.is_variable_set == flag:

				self.is_variable_set = 'tiles'
				"""
				Check if flag is defined
				"""
				self._match_flag(flag)
				"""
				Store flag opts
				"""
				try:
					self._store_variable(flag, opts)
				except KeyError:
					self.structure['variable'][flag] = []
					self._store_variable(flag, opts)
			else:
				raise IndexError('This version only support one variable flag.')

	def set_auxiliary(self, *args):
		for arg in args:
			if self._is_array(arg):
				for a in arg:
					self.structure['aux'].append(a)
			else:
				self.structure['aux'].append(arg)

	"""
	PRIVATE methods
	"""
	def _store_variable(self, flag, payload):
		flag_store = self.structure['variable'][flag]

		if isinstance(payload, list):
			flag_store += payload
		else:
			flag_store.append(payload)

	def _add_variable(self):
		ret_opts = []
		for flag, opts_list in self.structure['variable'].items():
			flag_blueprint = self._match_flag(flag)

			for opts in opts_list:
				ret_opts.append(self._transform_flag(flag_blueprint, opts))

		return ret_opts


	"""
	BLUEPRINT
	"""
	def _get_blueprint(self):
		parser = Parser('blueprint', self.blueprint_name, self.command)
		if not parser.parse():
			return False
		"""
		If there are multiple libraries in blueprint correct index of 
		library must be found to later enable addressing of flag opts
		"""
		self.blueprint_index, self.command_name = parser.get_command_info().values()
		"""
		Get all flags/opts from file
		"""
		self.flags_match_table = parser.get_flags()
		if not self.flags_match_table:
			raise ValueError()

		return True

	"""
	TRANSFORM
	"""
	def _transform_flag(self, flag_blueprint, opts):
		"""
		Take input flag and transform it to the desired format
		described in blueprint
		"""
		transform_buffer 		= []
		"""
		Whilst having multiple commands in blueprint so flags
		does need to be defined for all commands, skip empty ones
		"""
		if flag_blueprint:
			"""
			Mandatory parts of blueprint as local variable for 
			more readable code
			"""
			flag 		= flag_blueprint['flag']
			unifier 	= flag_blueprint['unifier']
			opt_format 	= flag_blueprint['format']

			if opt_format and opt_format['preset']:
				"""
				Opts are the most important part of the transformation because
				they need to put into the right format or even concatenated to
				a list hence they are first to address
				"""
				if 'list' in opt_format:
					transformed_opt = None
				else:
					transformed_opt = self._handle_opts(opt_format, opts)

				if transformed_opt != None:
					"""
					Handle unifier
					"""		
					if unifier:
						transform_buffer.append('{}{}{}'.format(flag, unifier, transformed_opt))
					else:
						"""
						Handle flag
						"""
						if flag:
							transform_buffer.append(flag)
						transform_buffer.append(transformed_opt)
			else:
				"""
				Without format is only toggle
				"""
				if not opt_format:
					if opts:
						transform_buffer.append(flag)
				else:
					"""
					Toggle format, list has two items, indexes as following:
					0 - False, 1 - True
					"""
					indexes = opt_format['pattern']['toggle']
					try:
						if indexes.index(opts):
							transform_buffer.append(flag)
					except ValueError:
						raise ValueError('"{}" is not a toggle match options, available {}'.format(opts, indexes))
		
		return transform_buffer


	def _handle_opts(self, opts_blueprint, opts):
		opts_preset = opts_blueprint['preset']
		"""
		Matching needs to take place
		"""
		if 'pattern' in opts_blueprint:
			pattern = opts_blueprint['pattern']['match']
			try:
				return self._transform_opts(opts_blueprint, pattern[opts])
			except KeyError:
				raise ValueError('"{}" is not a match options, available {}'.format(opts, list(pattern.keys())))
		else:
			return self._transform_opts(opts_blueprint, opts)


	def _transform_opts(self, opts_blueprint, opts):
		opts_preset = opts_blueprint['preset']
		opts_number = opts_blueprint['number'] - 1
		opts_preset_type = type(opts_preset)

		if opts_preset_type == str:
			"""
			String means matching predefined presets
			"""
			matched_preset = defs.FORMAT_OPTIONS[opts_number][opts_preset]

			if opts_number:
				"""
				Multiple part parameter
				"""
				return matched_preset.format(*opts)
			else:
				"""
				Single part
				"""
				return matched_preset.format(opts)

		elif opts_preset_type == dict:
			"""
			Custom formating is also enabled, setting divider/left & right side of expression
			"""
			opts_prepared = '{}'.format(opts_preset['divider']).join([str(_) for _ in opts])
			return '{}{}{}'.format(opts_preset['left'], opts_prepared, opts_preset['right'])




	def _match_flag(self, flag):
		"""
		Find correct flag options in blueprint
		"""
		try:
			return self.flags_match_table[flag][self.blueprint_index]
		except KeyError:
			raise KeyError('flag \'{}\' is not available in current blueprint. You can either try different blueprint or create new one'.format(flag))

	"""
	UTILS
	"""
	def _is_array(self, item):
		accepted_types = [list, tuple]
		for accepted_type in accepted_types:
			if isinstance(item, accepted_type):
				return True
		return False

	def _is_primitive(self, item):
		rejected_types = [list, tuple, set, dict]
		for rejected_type in rejected_types:
			if isinstance(item, rejected_type):
				return False
		return True