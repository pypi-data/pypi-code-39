from .functions import *
def adminpanel_page(request,slug):
	template_path = configuration('template_path')
	data = Pages.objects.filter(page_slug=str(slug),page_status='publish').first()
	dataDict = {}
	templateName = "page.html"
	curr_user = 2
	if  request.user.is_authenticated == True and  request.user.is_staff == True:
		curr_user = 1
	elif request.user.is_authenticated == True and  request.user.is_staff == False:	
		curr_user = 0
		
	if data is not None:
		if data.page_visible == "afterlogin" and request.user.is_authenticated != True:
			#return HttpResponse("YES2")
			return render(request,template_path+"404.html",{})
		elif data.page_visible == "beforelogin" and request.user.is_authenticated == True:	
			#return HttpResponse("YES1")
			return render(request,template_path+"404.html",{})
		elif data.page_visible == "afterlogin" and request.user.is_authenticated == True and str(curr_user) not in json.loads(data.page_access_level):
			#return HttpResponse("YES")
			return render(request,template_path+"404.html",{})
	if data is not None:
		id = data.id
		dataDict = {'id':data.id,'page_title':data.page_title,'page_slug': data.page_slug,'page_banner': data.page_banner,'page_excerpt': data.page_excerpt,'page_description': data.page_description,'page_author': data.page_author,'page_parent': data.page_parent,'page_subheading': data.page_subheading,'page_status':data.page_status,'page_visible': data.page_visible,'meta_description': data.meta_description,'meta_title':data.meta_title,'meta_keyword': data.meta_keyword}
		dataList = Pagemeta.objects.filter(page_id=id).all()
		for obj in dataList:
			dataDict[obj.meta_key] = obj.meta_value	
		template_check = django_template_exists(template_path+"page-"+data.page_slug+".html")	
		if template_check == True:
			templateName = "page-"+data.page_slug+".html"
	else:
		return render(request,template_path+"404.html",{})
	
	
	return render(request,template_path+""+templateName,{'data':dataDict})
	
def adminpanel_home(request):
	template_path = configuration('template_path')
	homedata = Options.objects.filter(option_key='generalsetting').first()
	if homedata is None:
		return render(request,template_path+"404.html",{})
	homeslug = json.loads(homedata.option_value)
	slug = homeslug.get('home_page')
	data = Pages.objects.filter(page_slug=str(slug),page_status='publish').first()
	dataDict = {}
	templateName = "home.html"
	curr_user = 2
	if  request.user.is_authenticated == True and  request.user.is_staff == True:
		curr_user = 1
	elif request.user.is_authenticated == True and  request.user.is_staff == False:	
		curr_user = 0
		
	if data is not None:
		if data.page_visible == "afterlogin" and request.user.is_authenticated != True:
			#return HttpResponse("YES2")
			return render(request,template_path+"404.html",{})
		elif data.page_visible == "beforelogin" and request.user.is_authenticated == True:	
			#return HttpResponse("YES1")
			return render(request,template_path+"404.html",{})
		elif data.page_visible == "afterlogin" and request.user.is_authenticated == True and str(curr_user) not in json.loads(data.page_access_level):
			#return HttpResponse("YES")
			return render(request,template_path+"404.html",{})
	if data is not None:
		id = data.id
		dataDict = {'id':data.id,'page_title':data.page_title,'page_slug': data.page_slug,'page_banner': data.page_banner,'page_excerpt': data.page_excerpt,'page_description': data.page_description,'page_author': data.page_author,'page_parent': data.page_parent,'page_subheading': data.page_subheading,'page_status':data.page_status,'page_visible': data.page_visible,'meta_description': data.meta_description,'meta_title':data.meta_title,'meta_keyword': data.meta_keyword}
		dataList = Pagemeta.objects.filter(page_id=id).all()
		for obj in dataList:
			dataDict[obj.meta_key] = obj.meta_value	
		template_check = django_template_exists(template_path+"page-"+data.page_slug+".html")	
		if template_check == True:
			templateName = "page-"+data.page_slug+".html"
	else:
		return render(request,template_path+"404.html",{})
	
	
	return render(request,template_path+""+templateName,{'data':dataDict})	