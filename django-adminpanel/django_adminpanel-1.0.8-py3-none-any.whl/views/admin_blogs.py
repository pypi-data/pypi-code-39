from .autoload import *
def apblogs_blogs_list(request):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect("/")	
	per_page = configuration('admin_record_per_page_blogs')
	if per_page is None:
		per_page = configuration('admin_record_per_page')
	defaultsort='-id'
	blogslist = Blogs.objects.order_by(defaultsort).all()
	paginator = Paginator(blogslist, per_page)
	page = 1
	if request.GET.get("page") is not None:
		page = request.GET.get("page")
	blogslist = paginator.get_page(page)	
	return render(request,"adminpanel/blogs.html",{'dataList':blogslist})
def apblogs_add_blog(request):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect("/")
	return render(request,"adminpanel/add-blog.html",{'data':{}})
def apblogs_submit_blog(request):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect("/")
	if (request.method != 'POST'):
		messages.add_message(request, messages.ERROR, 'We could not process your request at this time.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	data = request.POST
	tuple = {"title":"Yes"} 
	Blogs.objects.create(tuple)
	return HttpResponse("YEs")