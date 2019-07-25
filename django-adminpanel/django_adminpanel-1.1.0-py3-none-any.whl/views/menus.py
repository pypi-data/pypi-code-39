from .autoload import *

def admin_menus(request):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect("/")	
	per_page = configuration('admin_record_per_page_menus')
	if per_page is None:
		per_page = configuration('admin_record_per_page')
	defaultsort='-id'
	menuslist = Menus.objects.order_by(defaultsort).all()
	paginator = Paginator(menuslist, per_page)
	page = 1
	if request.GET.get("page") is not None:
		page = request.GET.get("page")
	menuslist = paginator.get_page(page)	
	return render(request,"adminpanel/menus.html",{"dataList":menuslist})
	
def admin_add_menu(request):
	return render(request,"adminpanel/add-menu.html",{})
	
def admin_update_menu(request,id):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect("/")
	menudata = Menus.objects.filter(id=id).first()
	return render(request,"adminpanel/edit-menu.html",{"data":menudata})
def adminpanel_delete_menu(request,id):
	Menus.objects.filter(id=id).delete()
	messages.add_message(request, messages.ERROR, 'Successfully deleted menu.')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))	
def admin_submit_menu(request):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect("/")
	if (request.method != 'POST'):
		messages.add_message(request, messages.ERROR, 'We could not process your request at this time.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	data = request.POST
	curr_menu = Menus.objects.filter(menu_slug=data.get('menu_slug')).first()
	if curr_menu is None:	
		Menus.objects.create(menu_title=data.get('menu_title'),menu_slug=data.get('menu_slug'),menu_content=data.get('menu_content'))
	else:
		curr_menu.menu_title = data.get('menu_title')
		curr_menu.menu_content = data.get('menu_content')
		curr_menu.save()
	messages.add_message(request, messages.SUCCESS, 'Successfully updated menu.')
	return HttpResponse(json.dumps({"status":"success"}))
def adminpanel_update_menu(request):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect("/")
	if (request.method != 'POST'):
		messages.add_message(request, messages.ERROR, 'We could not process your request at this time.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	data = request.POST
	curr_menu = Menus.objects.filter(id=data.get('id')).first()
	if curr_menu is not None:
		curr_menu.menu_title = data.get('menu_title')
		curr_menu.menu_slug = data.get('menu_slug')
		curr_menu.menu_content = data.get('menu_content')
		curr_menu.save()		
	return HttpResponse(json.dumps({"status":"success"}))