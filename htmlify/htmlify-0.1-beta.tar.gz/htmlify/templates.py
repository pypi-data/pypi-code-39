# htmlify
# Copyright 2019 to iDoObject
# Some rights reserved
# Licensed under the MIT license
import re

def transformEvals(template, *args, **kwargs):
	occurences = re.findall(r"_%\[.*?\]", template)
	for occurence in occurences:
		instruction = occurence[3:-1]  # strip syntax
		template = template.replace(occurence, str(eval(instruction)))
	return template

def transformGlobals(template, *args, **kwargs):
	occurences = re.findall(r"_%\(.*?\)", template)
	for occurence in occurences:
		instruction = occurence[3:-1]  # strip syntax
		template = template.replace(occurence, str(kwargs[instruction]))
	return template

class Template:
	def __init__(self, name):
		with open(f"templates/{name}.html") as templateFile:
			self._template = templateFile.read()

	def getHTML(self, transforms=[transformGlobals, transformEvals], *args, **kwargs):
		for transform in transforms:
			self._template = transform(self._template, *args, **kwargs)
		return self._template
