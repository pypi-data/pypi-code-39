from django import template
from django.template.defaultfilters import stringfilter
from django.core.paginator import Paginator
from adminpanel.models import *
from adminpanel.configuration import *
import urllib
import json
register = template.Library()
@register.simple_tag
def query_params(params,key,value):
	requesturl=''
	query_data={}
	req_params = params.GET
	for param in req_params:
		query_data[param] = req_params[param]
	query_data[key] = value
	if len(query_data) > 0:
		requesturl = urllib.parse.urlencode(query_data)		
	return requesturl
@register.simple_tag
def query_params_filter(params):
	requesturl=''
	query_data={}
	req_params = params.GET
	for param in req_params:
		query_data[param] = req_params[param]
	if 'page' in query_data.keys():
		del query_data['page']
	if 'filter' in query_data.keys():
		del query_data['filter']
		del query_data['sort']
	if len(query_data) > 0:
		requesturl = "&"+urllib.parse.urlencode(query_data)		
	return requesturl
@register.inclusion_tag('adminpanel/media-image.html')	
def media_image(imagename="page_banner",data={},label = "Upload Image"):
	imageurl = data.get(imagename)
	return {'data':data,'imagename':imagename,'label':label,'imageurl':imageurl}
@register.filter
@stringfilter
def template_exists(slugname="pages",pathname="pages"):
	try:
		template.loader.get_template("adminpanel/"+pathname+"/"+slugname+".html")
		return True
	except template.TemplateDoesNotExist:
		return False
@register.filter
@stringfilter
def settings_template_exists(slugname):
	try:
		template.loader.get_template("adminpanel/settings/"+slugname+".html")
		return True
	except template.TemplateDoesNotExist:
		return False
@register.filter
@stringfilter
def widget_template_exists(slugname):
	try:
		template.loader.get_template("adminpanel/widgets/"+slugname+".html")
		return True
	except template.TemplateDoesNotExist:
		return False		
@register.inclusion_tag('adminpanel/media-load.html')	
def media_load():
	per_page = 20
	defaultsort='-id'
	dataList = Media.objects.order_by(defaultsort).all()
	paginator = Paginator(dataList, per_page)
	page = 1
	dataList = paginator.get_page(page)
	return {'dataList':dataList}
@register.filter
@stringfilter
def get_widget(option_key):
	data = Options.objects.filter(option_key=option_key).first()
	datadict = {}
	if data is not None:
		datadict = json.loads(data.option_value)
	return datadict
@register.simple_tag
def site_settings(object):
    return configuration(object)	