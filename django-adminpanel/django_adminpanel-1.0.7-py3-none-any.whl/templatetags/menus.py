from django import template
from django.template.defaultfilters import stringfilter
from django.core.paginator import Paginator
from adminpanel.models import *
import urllib
import json
register = template.Library()
@register.inclusion_tag('adminpanel/menus/menu-list.html')	
def menu(request,**menudata):
	menu_slug = ""
	if "menu_slug" in menudata.keys():
		menu_slug= menudata.get("menu_slug")
	dataList = Menus.objects.filter(menu_slug=menu_slug).first()
	datamenu = {}
	if dataList is not None:
		datamenu = json.loads(dataList.menu_content)
	return {'dataList':datamenu,'menudata':menudata,"request":request}