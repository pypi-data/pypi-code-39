"""This is the standard way to include a multiple-line comment in your code."""

def print_lol(the_list, level):
	"""This function takes one positional argument called "the_list", which is any
	python list(of-possibly-nested lists). Each data item in the provided list is
	(recursively) printed to the screen on it's own line."""
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item, level+1)
		else:
			for tab_stop in range(level):
				print('\t', end = '')
			print(each_item)

