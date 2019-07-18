from django import template
from django.template.defaultfilters import stringfilter
from django.core.paginator import Paginator
from adminpanel.models import *
from adminpanel.configuration import *
import urllib
import json
register = template.Library()
@register.inclusion_tag('adminpanel/settings/pages-list.html')	
def load_page_list(page_slug=""):
	defaultsort='-id'
	dataList = Pages.objects.order_by(defaultsort).all()
	return {'dataList':dataList,'page_slug':page_slug}
@register.inclusion_tag('adminpanel/user-roles.html')	
def user_roles(sel=''):
	dataList = configuration('user_roles')
	return {'roles':dataList,'sel':sel}