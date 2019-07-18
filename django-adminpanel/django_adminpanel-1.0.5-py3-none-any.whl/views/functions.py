from django import template
from .autoload import *
def django_template_exists(temp_path):
	try:
		template.loader.get_template(temp_path)
		return True
	except template.TemplateDoesNotExist:
		return False
def get_option(key):
	data = Options.objects.filter(option_key=key).first()
	if data is None:
		return None
	return json.loads(data.option_value)