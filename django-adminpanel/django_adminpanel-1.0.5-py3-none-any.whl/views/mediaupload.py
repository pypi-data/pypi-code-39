from .autoload import *
def media_upload(request):
	if request.method == 'POST' and request.FILES['ajax_file']:
		myfile = request.FILES['ajax_file']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		#print(uploaded_file_url)
		Media.objects.create(image_title=uploaded_file_url,image_url=uploaded_file_url)	
		return HttpResponse("/"+uploaded_file_url)
	return HttpResponse("error")
def media_file_delete(request,id):
	media = Media.objects.filter(id=id).delete()
	return HttpResponse("Successfully deleted")
def media_ajax_file(request,page=1):
	per_page = 20
	defaultsort='-id'
	dataList = Media.objects.order_by(defaultsort).all()
	paginator = Paginator(dataList, per_page)
	dataList = paginator.get_page(page)
	htmldata = ""
	if dataList:
		for data in dataList:
			htmldata += '<li class="attach_thumb" data-id="/'+data.image_url+'"><img src="/'+data.image_url+'" class="im-responsive"><i class="fa fa-trash delete_media_file" data-id="'+str(data.id)+'"></i><span class="attach_filename">/'+data.image_url+'</span></li>'
	return HttpResponse(htmldata)	