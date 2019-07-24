from .autoload import *
def admin_settings(request):
	setting_tabs = configuration('admin_settings')
	defaulttab = "general"
	if request.GET.get('tab') is not None:
		defaulttab = request.GET.get('tab')
	return render(request,"adminpanel/settings.html",{'setting_tabs':setting_tabs,'defaulttab':defaulttab})
def submit_options(request):
	dataList = {}
	postdata = request.POST
	for obj in postdata:
		dataList[obj] = postdata.get(obj)
	datakey = dataList.get('data_key')
	del dataList['data_key']
	data = Options.objects.filter(option_key=datakey).first()
	if data is not None:
		data.option_value = json.dumps(dataList)
		data.save()
	else:
		Options.objects.create(option_key=datakey,option_value=json.dumps(dataList))	
	return HttpResponse(json.dumps({"status":"Success"}))	