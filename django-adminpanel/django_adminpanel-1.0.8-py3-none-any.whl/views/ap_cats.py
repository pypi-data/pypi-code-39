from .autoload import *
def apblogs_category_list(request):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect("/")	
	per_page = configuration('admin_record_per_page_category')
	if per_page is None:
		per_page = configuration('admin_record_per_page')
	defaultsort='-id'
	tagslist = Category.objects.order_by(defaultsort).all()
	paginator = Paginator(tagslist, per_page)
	page = 1
	if request.GET.get("page") is not None:
		page = request.GET.get("page")
	tagslist = paginator.get_page(page)	
	return render(request,"adminpanel/category.html",{'dataList':tagslist})
def apblogs_edit_category(request,id):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect("/")
	data = Category.objects.filter(id=id).get()
	if request.user.is_authenticated == False:
		return HttpResponseRedirect("/")	
	per_page = configuration('admin_record_per_page_tags')
	if per_page is None:
		per_page = configuration('admin_record_per_page')
	defaultsort='-id'
	tagslist = Category.objects.order_by(defaultsort).all()
	paginator = Paginator(tagslist, per_page)
	page = 1
	if request.GET.get("page") is not None:
		page = request.GET.get("page")
	tagslist = paginator.get_page(page)	
	return render(request,"adminpanel/edit-category.html",{"cats":data,'dataList':tagslist})
	
def apblogs_category_submit(request):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect("/")
	if (request.method != 'POST'):
		messages.add_message(request, messages.ERROR, 'We could not process your request at this time.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	data = request.POST
	slug = data.get("cat_url")
	tagurl = Category.objects.filter(cat_url=slug).first()
	if tagurl is not None:
		messages.add_message(request, messages.ERROR, 'This url slug already exists.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	Category.objects.create(title=data.get('title'),cat_url=data.get('cat_url'),cat_excerpt=data.get('cat_excerpt'),cat_image=data.get('cat_image'),cat_status=data.get('cat_status'),cat_parent=data.get('cat_parent'),cat_author=request.user.id,cat_order=data.get('cat_order'))
	messages.add_message(request, messages.ERROR, 'Successfully added new category.')
	return HttpResponseRedirect("/dj-admin/blogs/category")
def apblogs_category_update(request):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect("/")
	if (request.method != 'POST'):
		messages.add_message(request, messages.ERROR, 'We could not process your request at this time.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	data = request.POST
	slug = data.get("cat_url")
	id = data.get("id")
	caturl = Category.objects.filter(cat_url=slug).first()
	if caturl is not None and str(caturl.id) != str(data.get("id")):
		messages.add_message(request, messages.ERROR, 'This url slug already exists.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	curr_tag = Category.objects.get(id=id)
	curr_tag.title=data.get('title')
	curr_tag.cat_url=data.get('cat_url')
	curr_tag.cat_excerpt=data.get('cat_excerpt')
	curr_tag.cat_image=data.get('cat_image')
	curr_tag.cat_status=data.get('cat_status')
	curr_tag.cat_parent=data.get('cat_parent')
	curr_tag.cat_author=request.user.id
	curr_tag.cat_order=data.get('cat_order')
	curr_tag.save()
	messages.add_message(request, messages.ERROR, 'Successfully updated category.')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
def apblogs_category_delete(request):
	data = request.POST
	id = data.get("record_id")
	Category.objects.filter(id=id).delete()
	messages.add_message(request, messages.ERROR, 'Successfully deleted category.')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))		