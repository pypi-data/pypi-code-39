from django import template
from django.template.defaultfilters import stringfilter
from django.core.paginator import Paginator
from adminpanel.models import *
from apblogs.models import *
from adminpanel.configuration import *
import urllib
import json
register = template.Library()
@register.inclusion_tag('adminpanel/tags/tags-list.html')	
def load_tags_options(cat_parent=0):
	defaultsort='-id'
	dataDict = {}
	dataList = Tags.objects.filter(cat_parent=0).order_by(defaultsort).all()
	hyphon = "-"
	for data in dataList:
		dataDict[data.id] = data.title
		dataList = Tags.objects.filter(cat_parent=data.id).order_by(defaultsort).all()
		
		
	return {'dataDict':dataDict,'cat_parent':cat_parent}
@register.inclusion_tag('adminpanel/tags/cats-list.html')	
def load_category_options(cat_parent=0):
	defaultsort='-id'
	dataDict = {}
	dataList = Category.objects.filter(cat_parent=0).order_by(defaultsort).all()
	hyphon = "-"
	for data in dataList:
		dataDict[data.id] = data.title
		dataList = Category.objects.filter(cat_parent=data.id).order_by(defaultsort).all()
		
		
	return {'dataDict':dataDict,'cat_parent':cat_parent}