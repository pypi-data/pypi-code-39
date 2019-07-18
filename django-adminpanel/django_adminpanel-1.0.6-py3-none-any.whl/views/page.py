from .autoload import *
def adminpanel_pages(request):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect("/")	
	per_page = configuration('admin_record_per_page_pages')
	if per_page is None:
		per_page = configuration('admin_record_per_page')
	defaultsort='-id'
	pageslist = Pages.objects.order_by(defaultsort).all()
	paginator = Paginator(pageslist, per_page)
	page = 1
	if request.GET.get("page") is not None:
		page = request.GET.get("page")
	pageslist = paginator.get_page(page)	
	return render(request,"adminpanel/pages.html",{'dataList':pageslist})
def adminpanel_add_page(request):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect("/")
	return render(request,"adminpanel/add-page.html",{'data':{}})
def adminpanel_edit_page(request,id):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect("/")
	data = Pages.objects.filter(id=id).get()
	dataDict = {}
	if data is not None:
		dataDict = {'id':data.id,'page_title':data.page_title,'page_slug': data.page_slug,'page_banner': data.page_banner,'page_excerpt': data.page_excerpt,'page_description': data.page_description,'page_author': data.page_author,'page_order': data.page_order,'page_parent': data.page_parent,'page_subheading': data.page_subheading,'page_status':data.page_status,'page_visible': data.page_visible,'meta_description': data.meta_description,'meta_title':data.meta_title,'meta_keyword': data.meta_keyword,'page_access_level': json.loads(data.page_access_level)}
		dataList = Pagemeta.objects.filter(page_id=id).all()
		for obj in dataList:
			dataDict[obj.meta_key] = obj.meta_value	
	return render(request,"adminpanel/edit-page.html",{"data":dataDict})
def set_page_slug(request,page_slug,id):
	page_slug = str(re.sub('-+','-',re.sub('\ |\?|\.|\!|\/|\;|\:', '-', re.sub("<.*?>", "-", page_slug))).lower())	
	data = Pages.objects.filter(page_slug__istartswith=page_slug).order_by("-id").first()
	if data is not None and  str(data.id) != str(id):
		page_slug = page_slug+"-"+str(id)
	obj =Pages.objects.filter(id=id).first()
	obj.page_slug = page_slug
	obj.save()
	return page_slug	
def adminpanel_submit_page(request):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect("/")
	if (request.method != 'POST'):
		messages.add_message(request, messages.ERROR, 'We could not process your request at this time.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	data = request.POST
	page_slug = request,data.get('page_slug')
	defaultField = ['page_title','page_slug','page_banner','page_excerpt','page_description','page_author','page_subheading','page_status','page_visible','meta_description','meta_title','meta_keyword','page_access_level','page_order']
	curr_page = Pages.objects.create(page_title = data.get('page_title'),page_slug = page_slug,page_banner = data.get('page_banner'),page_excerpt = data.get('page_excerpt'),page_description = data.get('page_description'),page_author = request.user.id,page_parent = 0,page_subheading = data.get('page_subheading'),page_status = data.get('page_status'),page_visible = data.get('page_visible'),meta_description = data.get('meta_description'),meta_title = data.get('meta_title'),meta_keyword = data.get('meta_keyword'),page_access_level = json.dumps(data.getlist('page_access_level')),page_order=data.get('page_order') )		
	messages.add_message(request, messages.SUCCESS, 'Successfully created page.')
	custom_data = {}
	for obj in data:
		if obj not in defaultField:
			if '[]' in obj:
				custom_data[obj] = json.dumps(data.getlist(obj))
			else:
				custom_data[obj] = data.get(obj)
	if len(custom_data) > 0 :
		for key in custom_data:
			Pagemeta.objects.create(meta_key=key,meta_value=custom_data.get(key),page_id = curr_page.id)
	#print(custom_data)
	#return HttpResponse("YS")
	#return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	set_page_slug(request,data.get('page_slug'),curr_page.id)
	return HttpResponseRedirect("/dj-admin/pages")
def adminpanel_update_page(request):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect("/")
	if (request.method != 'POST'):
		messages.add_message(request, messages.ERROR, 'We could not process your request at this time.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	data = request.POST
	#print(data)
	#return HttpResponse("YEs")
	defaultField = ['id','page_title','page_slug','page_banner','page_excerpt','page_description','page_author','page_subheading','page_status','page_visible','meta_description','meta_title','meta_keyword','page_access_level','page_order']
	#print(data.get("id"))
	#curr_page = Pages.objects.filter(id=data.get("id")).get()
	id = data.get("id")
	curr_page = Pages.objects.filter(id=id).get()
	curr_page.page_title = data.get('page_title')
	curr_page.page_slug = data.get('page_slug')
	curr_page.page_banner = data.get('page_banner')
	curr_page.page_excerpt = data.get('page_excerpt')
	curr_page.page_description = data.get('page_description')
	curr_page.page_subheading = data.get('page_subheading')
	curr_page.page_status = data.get('page_status')
	curr_page.page_visible = data.get('page_visible')
	curr_page.meta_description = data.get('meta_description')
	curr_page.meta_title = data.get('meta_title')
	curr_page.meta_keyword = data.get('meta_keyword')
	curr_page.page_order = data.get('page_order')
	curr_page.page_access_level = json.dumps(data.getlist('page_access_level'))
	curr_page.save()	
	messages.add_message(request, messages.SUCCESS, 'Successfully updated page.')
	custom_data = {}
	for obj in data:
		if obj not in defaultField:
			if '[]' in obj:
				custom_data[obj] = json.dumps(data.getlist(obj))
			else:
				custom_data[obj] = data.get(obj)
	if len(custom_data) > 0 :
		for key in custom_data:
			curr_meta = Pagemeta.objects.filter(meta_key=key,page_id=id).first()
			if curr_meta is None:
				Pagemeta.objects.create(meta_key=key,meta_value=custom_data.get(key),page_id = curr_page.id)
			else:
				curr_meta.meta_key = key
				curr_meta.meta_value = custom_data.get(key)
				curr_meta.save()
	#print(custom_data)
	#return HttpResponse("YS")
	set_page_slug(request,data.get('page_slug'),id)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
def adminpanel_delete_page(request,id):
	Pages.objects.filter(id=id).delete()
	Pagemeta.objects.filter(page_id=id).delete()
	messages.add_message(request, messages.ERROR, 'Successfully deleted page.')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))	